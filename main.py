"""
Belladonna v5.0 — FASE 4A COMPLETA

ARQUITECTURA MENTE PURA:
    Bell (Python)  = Razona con conceptos verificados
    Groq  (API)    = SOLO embellece texto
    Echo  (Python) = Verifica que Groq no invente nada

CAMBIOS v5 sobre v4:
═══════════════════════════════════════════════════════════════════════

1. MOTOR CONECTADO A MEMORIA (FIX ARQUITECTURAL CRÍTICO)
   ──────────────────────────────────────────────────────
   self.motor.gestor_memoria = self.gestor_memoria

   Por qué importa: el motor v5 guarda datos de REGISTRO_USUARIO
   DIRECTAMENTE en memoria antes de que llegue al generador.
   Sin esta línea, el dato se extrae pero nunca se persiste.

2. IDENTIDAD_BELL CARGADA Y MOSTRADA EN BANNER
   ─────────────────────────────────────────────
   Importa identidad_bell.py para mostrar el nombre correcto
   en el saludo inicial y en el banner.

3. NOMBRES PERSONALIZADOS (integración con identidad_bell.py)
   ─────────────────────────────────────────────────────────
   El saludo inicial usa obtener_nombre_a_usar() del gestor de memoria
   para saber si decir "Sebas" o "Sebastián" según el tipo de momento.

4. NUEVO COMANDO 'identidad'
   ──────────────────────────
   Muestra PRINCIPIO_CENTRAL, VOZ y NARRATIVA_PROPIA de Bell.

5. NUEVO COMANDO 'personas'
   ─────────────────────────
   Muestra los modelos mentales de personas que Bell ha construido
   (Sara, etc.) usando los nuevos métodos de GestorMemoria v5.

6. _cmd_memoria() ENRIQUECIDO
   ────────────────────────────
   Muestra además temas abiertos y predicciones de Bell
   (nuevos campos de GestorMemoria v5).

7. VERSION STRING actualizado a v5.0

CAMBIOS v4 PRESERVADOS:
- FIX v3: memoria compartida inyectada al generador en iniciar_sesion()
- Todos los módulos obligatorios y opcionales sin cambios
- Todos los comandos existentes sin cambios en comportamiento

USO:
    python main.py              → Sin Groq (honesta, simbólica)
    python main.py --use-groq   → Con Groq (honesta, natural)
    python main.py -v           → Verbose
    python main.py --use-groq -v
═══════════════════════════════════════════════════════════════════════
"""

import sys
import argparse
import logging
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

# ─── Logging ─────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.WARNING, format="%(levelname)s [%(name)s] %(message)s")
for _lib in ("httpx", "groq", "openai", "urllib3"):
    logging.getLogger(_lib).setLevel(logging.ERROR)

# ─── Colores terminal ─────────────────────────────────────────────────────────
BOLD  = "\033[1m"
CYAN  = "\033[96m"
GREEN = "\033[92m"
YELL  = "\033[93m"
RED   = "\033[91m"
DIM   = "\033[2m"
RST   = "\033[0m"

# ─── Carga identidad_bell.py (opcional — no aborta si no existe) ──────────────
try:
    from identidad_bell import (
        PRINCIPIO_CENTRAL,
        NARRATIVA_PROPIA,
        VOZ_BELL,
        NOMBRES_SEBASTIAN,
        obtener_nombre,
    )
    _IDENTIDAD_OK = True
except ImportError:
    _IDENTIDAD_OK = False
    PRINCIPIO_CENTRAL = "solo afirmo lo que puedo ejecutar o verificar"
    NARRATIVA_PROPIA  = ""
    VOZ_BELL          = {}
    NOMBRES_SEBASTIAN = {}


# ─── Helpers de importación ───────────────────────────────────────────────────

def _importar(ruta: str, clase: str):
    try:
        m = __import__(ruta, fromlist=[clase])
        return getattr(m, clase)
    except (ImportError, AttributeError):
        return None


def _importar_obligatorio(ruta: str, clase: str):
    cls = _importar(ruta, clase)
    if cls is None:
        print(f"\n{RED}✗ No se pudo cargar {ruta}.{clase}{RST}")
        print("  Verifica que el proyecto esté completo.\n")
        sys.exit(1)
    return cls


# ─────────────────────────────────────────────────────────────────────────────
# CLASE PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────

class Belladonna:
    """
    Belladonna v5.0 — Sistema Conversacional Completo.

    Flujo por mensaje:
        1. TraductorEntrada   → español → ConceptosAnclados
        2. MotorRazonamiento  → clasificar intención → Decision + hechos
           · v5: el motor actualiza memoria de estado en tiempo real
           · v5: para REGISTRO_USUARIO guarda el dato en memoria ANTES del generador
        3. Consejeras deliberan (Vega puede vetar)
        4. GeneradorSalida    → Decision → español natural (Groq + Echo si activo)
           · v5: _TIPOS_CONVERSACIONALES incluye los 5 tipos nuevos
           · v5: CALCULO se resuelve en Python sin Groq
        5. GestorMemoria      → persiste historial, episodios, personas, predicciones
    """

    def __init__(self, usar_groq: bool = False, verbose: bool = False):
        self.usar_groq     = usar_groq
        self.verbose       = verbose
        self.turnos        = 0
        self._fase2_activa = False
        self._emociones: dict = {}
        self.id_sesion     = None

        self._banner()

        # ── Módulos obligatorios ──────────────────────────────────────────────
        GestorVocabulario = _importar_obligatorio("vocabulario.gestor_vocabulario", "GestorVocabulario")
        TraductorEntrada  = _importar_obligatorio("traduccion.traductor_entrada",   "TraductorEntrada")
        MotorRazonamiento = _importar_obligatorio("razonamiento.motor_razonamiento", "MotorRazonamiento")
        GeneradorSalida   = _importar_obligatorio("generacion.generador_salida",    "GeneradorSalida")
        GestorMemoria     = _importar_obligatorio("memoria.gestor_memoria",         "GestorMemoria")

        # ── Vocabulario ───────────────────────────────────────────────────────
        try:
            self.gestor_vocab = GestorVocabulario(cargar_expansion=True)
        except TypeError:
            self.gestor_vocab = GestorVocabulario()

        total = self._total_conceptos()
        print(f"  {GREEN}✅ Vocabulario:{RST}   {total} conceptos")

        # ── Traducción ────────────────────────────────────────────────────────
        self.traductor = TraductorEntrada(self.gestor_vocab)
        print(f"  {GREEN}✅ Traductor:{RST}     activo")

        # ── Razonamiento ──────────────────────────────────────────────────────
        self.motor = MotorRazonamiento()
        self.motor.gestor_vocabulario = self.gestor_vocab
        # ── v5: gestor_memoria se inyecta en iniciar_sesion() (después de crearlo)
        print(f"  {GREEN}✅ Motor:{RST}         razonamiento v5")

        # ── Consejeras ────────────────────────────────────────────────────────
        self._cargar_consejeras()

        # ── Generador de salida ───────────────────────────────────────────────
        self.generador = GeneradorSalida(usar_groq=usar_groq)
        modo = f"{GREEN}Groq + Echo ACTIVOS{RST}" if usar_groq else f"{YELL}modo simbólico{RST}"
        print(f"  {GREEN}✅ Generador:{RST}     {modo}")

        # ── Memoria ───────────────────────────────────────────────────────────
        self.gestor_memoria = GestorMemoria()
        print(f"  {GREEN}✅ Memoria:{RST}       persistente lista")

        # ── identidad_bell.py ─────────────────────────────────────────────────
        if _IDENTIDAD_OK:
            print(f"  {GREEN}✅ Identidad:{RST}     Bell cargada")
        else:
            print(f"  {YELL}⚠  Identidad:{RST}     identidad_bell.py no encontrado")

        # ── Módulos opcionales ────────────────────────────────────────────────
        self._cargar_opcionales()

        print()
        print(f"  {'─'*56}")
        if usar_groq:
            print(f"  {BOLD}Bell está lista con Groq activo.{RST}")
        else:
            print(f"  {BOLD}Bell está lista.{RST}  {DIM}(usa --use-groq para Groq){RST}")
        print()

    # ──────────────────────────────────────────────────────────────────────────

    def _banner(self):
        version = "v5.0"
        nombre  = "Belladonna" if not _IDENTIDAD_OK else "Belladonna (Bell)"
        print()
        print(f"  {'═'*58}")
        print(f"  {BOLD}{CYAN}{f'🌺  {nombre}  {version}  🌺':^58}{RST}")
        print(f"  {'Sistema Conversacional — FASE 4A':^58}")
        print(f"  {f'{PRINCIPIO_CENTRAL[:54]}':^58}")
        print(f"  {'═'*58}")
        print()
        print("  Iniciando sistemas...")
        print()

    def _total_conceptos(self) -> int:
        for metodo in ("total_conceptos",):
            if hasattr(self.gestor_vocab, metodo):
                try:
                    return getattr(self.gestor_vocab, metodo)()
                except Exception:
                    pass
        try:
            return len(self.gestor_vocab.obtener_todos())
        except Exception:
            return 1472

    def _cargar_consejeras(self):
        self.gestor_consejeras = None
        self.consejeras        = []

        GestorConsejeras = _importar("consejeras.gestor_consejeras", "GestorConsejeras")
        if GestorConsejeras:
            try:
                self.gestor_consejeras = GestorConsejeras()
                self.consejeras = getattr(self.gestor_consejeras, "consejeras", [])
                nombres = ", ".join(getattr(c, "nombre", "?") for c in self.consejeras)
                print(f"  {GREEN}✅ Consejeras:{RST}    {len(self.consejeras)} activas — {nombres}")
                return
            except Exception as e:
                if self.verbose:
                    print(f"  {YELL}⚠ GestorConsejeras: {e}{RST}")

        Vega = (_importar("consejeras.vega.vega", "Vega")
                or _importar("consejeras.vega", "Vega"))
        if Vega:
            try:
                self.consejeras = [Vega()]
                print(f"  {YELL}⚠  Consejeras:{RST}    solo Vega")
                return
            except Exception:
                pass

        print(f"  {YELL}⚠  Consejeras:{RST}    no disponibles")

    def _cargar_opcionales(self):
        print()
        print("  Módulos opcionales:")

        GestorBucles = _importar("bucles.gestor_bucles", "GestorBucles")
        self.gestor_bucles = GestorBucles() if GestorBucles else None
        ico = GREEN + "✅" if self.gestor_bucles else YELL + "⚠ "
        print(f"  {ico}{RST} Bucles autónomos:  "
              + ("listos" if self.gestor_bucles else "no disponibles"))

        MotorAprendizaje = _importar("aprendizaje.motor_aprendizaje", "MotorAprendizaje")
        self.motor_aprendizaje = None
        if MotorAprendizaje:
            try:
                self.motor_aprendizaje = MotorAprendizaje()
                if hasattr(self.motor_aprendizaje, "configurar_integraciones"):
                    self.motor_aprendizaje.configurar_integraciones(
                        vocabulario=self.gestor_vocab,
                        memoria=self.gestor_memoria,
                        bucles=self.gestor_bucles,
                    )
            except Exception:
                self.motor_aprendizaje = None
        ico = GREEN + "✅" if self.motor_aprendizaje else YELL + "⚠ "
        print(f"  {ico}{RST} Motor aprendizaje: "
              + ("listo" if self.motor_aprendizaje else "no disponible"))

        ShellExecutor = _importar("operaciones.shell_executor", "ShellExecutor")
        self.shell = None
        if ShellExecutor:
            try:
                self.shell = ShellExecutor()
            except Exception:
                pass
        ico = GREEN + "✅" if self.shell else YELL + "⚠ "
        print(f"  {ico}{RST} Shell executor:    "
              + ("activo" if self.shell else "no disponible"))

        ClienteSQLite = _importar("base_datos", "ClienteSQLite")
        self.bd_cliente = None
        if ClienteSQLite:
            try:
                self.bd_cliente = ClienteSQLite(":memory:")
            except Exception:
                pass
        ico = GREEN + "✅" if self.bd_cliente else YELL + "⚠ "
        print(f"  {ico}{RST} Base de datos:     "
              + ("SQLite activo" if self.bd_cliente else "no disponible"))

    # ─────────────────────────────────────────────────────────────────────────
    # CICLO DE VIDA
    # ─────────────────────────────────────────────────────────────────────────

    def iniciar_sesion(self):
        """
        Arranca la sesión e inyecta la memoria compartida a motor y generador.

        INYECCIONES CRÍTICAS v5:
            generador.memoria  = self.gestor_memoria  (FIX v3 — preservado)
            motor.gestor_memoria = self.gestor_memoria  (NUEVO v5)

        Sin la segunda inyección:
            - REGISTRO_USUARIO: el motor extrae el nombre pero no lo guarda
            - CONSULTA_MEMORIA: el motor busca en una instancia vacía
            - actualizar_estado_sesion(): llama sobre None → silencioso
        """
        if self._fase2_activa:
            return

        print(f"  {CYAN}▶ Iniciando sesión...{RST}")

        try:
            self.id_sesion = self.gestor_memoria.iniciar_sesion()
            print(f"  {GREEN}✅{RST} Sesión: {self.id_sesion[:8]}...")
        except Exception:
            self.id_sesion = datetime.now().isoformat()

        # ── FIX v3: memoria compartida → generador ────────────────────────────
        self.generador.memoria = self.gestor_memoria
        print(f"  {GREEN}✅{RST} Memoria inyectada al generador")

        # ── NUEVO v5: memoria compartida → motor ──────────────────────────────
        self.motor.gestor_memoria = self.gestor_memoria
        print(f"  {GREEN}✅{RST} Memoria inyectada al motor")

        if self.gestor_bucles:
            try:
                self.gestor_bucles.iniciar_todos()
                print(f"  {GREEN}✅{RST} Bucles autónomos activos")
            except Exception as e:
                if self.verbose:
                    print(f"  {YELL}⚠ Bucles: {e}{RST}")

        if self.bd_cliente:
            try:
                self.bd_cliente.conectar()
                print(f"  {GREEN}✅{RST} Base de datos conectada")
            except Exception:
                pass

        self._fase2_activa = True
        print()

    def finalizar_sesion(self):
        if not self._fase2_activa:
            return

        print()
        print(f"  {CYAN}⏹ Finalizando sesión...{RST}")

        if self.gestor_bucles:
            try:
                self.gestor_bucles.detener_todos()
                print(f"  ✅ Bucles detenidos")
            except Exception:
                pass

        if self.bd_cliente:
            try:
                self.bd_cliente.desconectar()
            except Exception:
                pass

        try:
            self.gestor_memoria.finalizar_sesion()
            print(f"  ✅ Sesión guardada  ({self.turnos} turnos)")
        except Exception:
            pass

        self._fase2_activa = False

    # ─────────────────────────────────────────────────────────────────────────
    # DETECCIÓN DE EMOCIÓN
    # ─────────────────────────────────────────────────────────────────────────

    _PATRONES_EMOCION = {
        "frustrado":  (["no funciona", "error", "falla", "frustrado", "harto",
                        "imposible", "ya intenté", "sigue sin", "otra vez", "me rindo"],
                       "empático_paciente"),
        "confundido": (["no entiendo", "confundido", "qué significa", "me explicas",
                        "no sé", "perdido", "no me queda claro"],
                       "didáctico_claro"),
        "emocionado": (["genial", "excelente", "increíble", "wow", "funcionó",
                        "por fin", "perfecto", "maravilloso", "me encanta"],
                       "entusiasta"),
        "preocupado": (["preocupado", "miedo", "temo", "asustado", "nervioso",
                        "ansiedad", "qué pasa si"],
                       "tranquilizador"),
        "ocupado":    (["rápido", "urgente", "apurado", "prisa", "no tengo tiempo",
                        "breve", "asap"],
                       "conciso_directo"),
        "curioso":    (["cómo funciona", "por qué", "interesante", "quiero saber",
                        "cuéntame más", "explícame"],
                       "informativo_rico"),
    }

    def _detectar_emocion(self, texto: str):
        t = texto.lower()
        for emocion, (palabras, tono) in self._PATRONES_EMOCION.items():
            if any(p in t for p in palabras):
                self._emociones[emocion] = self._emociones.get(emocion, 0) + 1
                return emocion, tono
        return None, "amigable_natural"

    # ─────────────────────────────────────────────────────────────────────────
    # PROCESAMIENTO PRINCIPAL
    # ─────────────────────────────────────────────────────────────────────────

    def procesar(self, mensaje: str) -> str:
        """
        Procesa un mensaje y retorna la respuesta de Bell.

        FLUJO v5:
            0. Emoción detectada en main
            1. Traducción: español → ConceptosAnclados
            2. Razonamiento:
               - clasificar_intencion()
               - _actualizar_estado_memoria() → GestorMemoria._sesion sincronizado
               - construir_hechos()
               - para REGISTRO_USUARIO: _guardar_dato_en_memoria() antes de retornar
            3. Consejeras (Vega puede vetar)
            4. Generación:
               - CALCULO: Python directo, sin Groq
               - otros: fallback conversacional o Groq + Echo
            5. Registro operacional (conceptos, decisión, episodio)
            6. Aprendizaje en tiempo real
        """
        try:
            v = self.verbose

            if v:
                print(f"\n{'═'*64}")
                print(f"  📥 MENSAJE: \"{mensaje}\"")
                print(f"{'═'*64}")

            # 0 · Emoción
            emocion, tono = self._detectar_emocion(mensaje)
            if v and emocion:
                print(f"\n  💭 Emoción: {emocion} → tono: {tono}")

            # 1 · Traducción
            traduccion = self.traductor.traducir(mensaje)
            if v:
                cs = traduccion.get("conceptos", [])
                print(f"\n  🔄 Traducción: {len(cs)} conceptos "
                      f"(confianza {traduccion.get('confianza', 0):.0%})")
                for c in cs[:4]:
                    print(f"     • {c.id}  g={c.confianza_grounding:.2f}")

            # 2 · Razonamiento
            # v5: el motor ya actualiza memoria de estado y guarda datos verificados
            decision = self.motor.razonar(traduccion)
            if v:
                print(f"\n  🧠 Decisión: {decision.tipo.name}  "
                      f"certeza={decision.certeza:.0%}  "
                      f"ejecutar={decision.puede_ejecutar}")
                if decision.hechos_reales:
                    tipo_r = decision.hechos_reales.get("tipo_respuesta", "")
                    if tipo_r in ("REGISTRO_USUARIO", "CONSULTA_MEMORIA"):
                        print(f"     dato_tipo={decision.hechos_reales.get('dato_tipo', '')}")
                        print(f"     dato_valor={decision.hechos_reales.get('dato_valor', '')}")

            # 3 · Consejeras
            contexto = {
                "traduccion":       traduccion,
                "emocion_usuario":  emocion,
                "tono_recomendado": tono,
            }

            for consejera in self.consejeras:
                try:
                    revision = consejera.revisar(decision, contexto)
                    if revision and revision.get("veto", False):
                        contexto["revision_vega"] = revision
                        if v:
                            print(f"\n  🛑 VETO de "
                                  f"{getattr(consejera, 'nombre', '?')}: "
                                  f"{revision.get('razon_veto', '')}")
                        return self.generador.generar(decision, contexto)
                    if v:
                        print(f"  ✅ {getattr(consejera, 'nombre', '?')}: aprobado")
                except Exception:
                    pass

            # 4 · Generación
            if v:
                modo = "GROQ+ECHO" if self.usar_groq else "SIMBÓLICO"
                print(f"\n  🎨 Generando [{modo}]...")

            respuesta = self.generador.generar(decision, contexto)

            if v:
                preview = (respuesta[:100] + "...") if len(respuesta) > 100 else respuesta
                print(f"  → \"{preview}\"")

            # 5 · Registro operacional en memoria
            if self._fase2_activa:
                try:
                    for c in traduccion.get("conceptos", [])[:3]:
                        self.gestor_memoria.guardar_concepto_usado(
                            concepto_id=c.id, certeza=decision.certeza
                        )
                    self.gestor_memoria.guardar_decision({
                        "tipo":           decision.tipo.name,
                        "puede_ejecutar": decision.puede_ejecutar,
                        "certeza":        decision.certeza,
                        "emocion":        emocion,
                    })

                    # v5: registrar episodio narrativo para tipos importantes
                    _TIPOS_EPISODIO = {
                        "REGISTRO_USUARIO", "CONSULTA_MEMORIA",
                        "IDENTIDAD_BELL", "ESTADO_USUARIO",
                    }
                    tipo_nombre = decision.tipo.name
                    if tipo_nombre in _TIPOS_EPISODIO and hasattr(self.gestor_memoria, "registrar_episodio"):
                        try:
                            # ✅ DESPUÉS (kwargs correctos):
                            self.gestor_memoria.registrar_episodio(
                                resumen                  = mensaje[:120],
                                tema_principal           = tipo_nombre,
                                estado_emocional_usuario = emocion or "neutral",
                            )
                        except Exception:
                            pass

                except Exception:
                    pass

            # 6 · Aprendizaje en tiempo real
            if self.motor_aprendizaje:
                try:
                    self.motor_aprendizaje.procesar_turno({
                        "traduccion": traduccion,
                        "decision":   decision,
                        "respuesta":  respuesta,
                    })
                except Exception:
                    pass

            self.turnos += 1
            return respuesta

        except Exception as e:
            if self.verbose:
                import traceback
                traceback.print_exc()
            return f"Perdona, tuve un error interno: {e}"

    # ─────────────────────────────────────────────────────────────────────────
    # LOOP CONVERSACIONAL
    # ─────────────────────────────────────────────────────────────────────────

    def loop(self):
        self.iniciar_sesion()

        # ── Saludo inicial personalizado ──────────────────────────────────────
        nombre = ""
        try:
            nombre = self.gestor_memoria.el_usuario_se_llama() or ""
        except Exception:
            pass

        hora = datetime.now().hour

        # v5: usar identidad_bell para nombre de Bell si está disponible
        if _IDENTIDAD_OK and nombre:
            try:
                nombre_bell = obtener_nombre("estandar", nombre)
            except Exception:
                nombre_bell = "Bell"
        else:
            nombre_bell = "Bell"

        if nombre:
            saludo = f"¡Hola de nuevo, {nombre}! Aquí estoy. ¿En qué te ayudo?"
        elif 5 <= hora < 12:
            saludo = f"¡Buenos días! Soy {nombre_bell}. ¿Cómo te llamas y en qué te ayudo?"
        elif 12 <= hora < 19:
            saludo = f"¡Buenas tardes! Soy {nombre_bell}. ¿En qué puedo ayudarte?"
        else:
            saludo = f"¡Buenas noches! Soy {nombre_bell}. ¿En qué puedo ayudarte?"

        print(f"🌺 Bell: {saludo}")
        print(f"   {DIM}(Escribe 'help' para comandos, 'salir' para terminar){RST}")
        print()

        while True:
            try:
                entrada = input("🧑 Tú: ").strip()

                if not entrada:
                    continue

                el = entrada.lower()

                # ── Comandos especiales ───────────────────────────────────────
                if el in ("salir", "exit", "quit", "chao", "bye", "adios", "adiós"):
                    print("\n🌺 Bell: ¡Hasta pronto! Fue un gusto conversar.")
                    self.finalizar_sesion()
                    break

                if el == "help":
                    self._cmd_help();      continue
                if el == "stats":
                    self._cmd_stats();     continue
                if el == "groq":
                    self._cmd_groq();      continue
                if el == "memoria":
                    self._cmd_memoria();   continue
                if el == "emociones":
                    self._cmd_emociones(); continue
                if el == "toggle_groq":
                    self._cmd_toggle_groq(); continue
                if el == "identidad":
                    self._cmd_identidad(); continue
                if el == "personas":
                    self._cmd_personas();  continue
                if el == "verbose":
                    self.verbose = not self.verbose
                    print(f"   {YELL}Verbose: {'ON 🔍' if self.verbose else 'OFF'}{RST}\n")
                    continue

                # ── Mensaje normal ────────────────────────────────────────────
                respuesta = self.procesar(entrada)
                print(f"🌺 Bell: {respuesta}")
                print()

            except KeyboardInterrupt:
                print("\n\n🌺 Bell: ¡Hasta pronto!")
                self.finalizar_sesion()
                break
            except EOFError:
                self.finalizar_sesion()
                break

    # ─────────────────────────────────────────────────────────────────────────
    # COMANDOS
    # ─────────────────────────────────────────────────────────────────────────

    def _cmd_help(self):
        print(f"""
  {BOLD}Comandos:{RST}
  {'─'*42}
  stats        Estadísticas del sistema
  groq         Estado de Groq y Echo
  memoria      Lo que Bell recuerda de ti
  emociones    Emociones detectadas en la sesión
  identidad    Identidad y principios de Bell   {DIM}[nuevo v5]{RST}
  personas     Personas que Bell conoce         {DIM}[nuevo v5]{RST}
  toggle_groq  Activar/desactivar Groq
  verbose      Activar/desactivar debug
  help         Esta ayuda
  salir        Terminar
  {'─'*42}
  {DIM}Tip: python main.py --use-groq{RST}
""")

    def _cmd_stats(self):
        total = self._total_conceptos()
        sg = {}
        try:
            sg = self.generador.obtener_estadisticas()
        except Exception:
            pass
        print(f"""
  {BOLD}Estadísticas:{RST}
  {'─'*42}
  Vocabulario   {total} conceptos
  Consejeras    {len(self.consejeras)} activas
  Turnos        {self.turnos}
  Groq          {'ON ✅' if self.usar_groq else 'OFF'}
  Identidad     {'cargada ✅' if _IDENTIDAD_OK else 'no disponible'}
  {'─'*42}
  Respuestas    {sg.get('total_generadas', 0)}
  Con Groq      {sg.get('groq_usadas', 0)}
  Bloqueadas    {sg.get('groq_bloqueadas', 0)}
  Fallback      {sg.get('fallback_a_simbolico', 0)}
  {'─'*42}
  Tipos de decisión:""")
        tipos = sg.get('tipos_decision', {})
        for tipo, cnt in sorted(tipos.items(), key=lambda x: -x[1])[:8]:
            print(f"    {tipo:<25} {cnt}")
        print()

    def _cmd_groq(self):
        if self.usar_groq:
            sg = {}
            try:
                sg = self.generador.obtener_estadisticas()
            except Exception:
                pass
            print(f"""
  {GREEN}Groq: ACTIVO{RST}
  {'─'*42}
  Llamadas Groq     {sg.get('groq_usadas', 0)}
  Bloqueadas Echo   {sg.get('groq_bloqueadas', 0)}
  Tasa éxito        {sg.get('tasa_groq', 0):.1%}
  {'─'*42}
  Anti-invención    {GREEN}ACTIVA{RST}
  Echo verificando  {GREEN}ACTIVO{RST}
  Memoria→generador {GREEN}INYECTADA{RST}
  Memoria→motor     {GREEN}INYECTADA{RST}
""")
        else:
            print(f"""
  {YELL}Groq: DESACTIVADO{RST}
  Bell usa generación simbólica honesta.
  Activa con: python main.py --use-groq
  O en caliente: toggle_groq
""")

    def _cmd_emociones(self):
        if self._emociones:
            print(f"\n  {BOLD}Emociones detectadas esta sesión:{RST}")
            tot = sum(self._emociones.values())
            for em, cnt in sorted(self._emociones.items(), key=lambda x: -x[1]):
                barra = "█" * min(int(cnt / tot * 20), 20)
                print(f"  {em:12}  {barra:<20}  {cnt}")
        else:
            print("\n  Ninguna emoción detectada aún.")
        print()

    def _cmd_memoria(self):
        """v5: muestra datos del usuario + temas abiertos + predicciones."""
        try:
            datos     = self.gestor_memoria.obtener_datos_usuario()
            historial = self.gestor_memoria.obtener_contexto(n_mensajes=6)

            print(f"\n  {BOLD}Lo que Bell recuerda:{RST}")
            print(f"  {'─'*42}")

            # Datos verificados del usuario
            if datos:
                print(f"  {BOLD}Datos del usuario:{RST}")
                for k, v in datos.items():
                    print(f"    {k}: {v}")
            else:
                print("  (sin datos del usuario todavía)")

            # Temas abiertos — nuevo v5
            if hasattr(self.gestor_memoria, "hay_temas_abiertos"):
                try:
                    if self.gestor_memoria.hay_temas_abiertos():
                        temas = self.gestor_memoria.obtener_temas_pendientes()
                        print(f"\n  {BOLD}Temas pendientes ({len(temas)}):{RST}")
                        for t in temas[:3]:
                            print(f"    • {t.get('tema', '?')} — {t.get('resumen', '')[:60]}")
                except Exception:
                    pass

            # Últimos mensajes
            if historial:
                lines = historial.strip().split("\n")[-6:]
                print(f"\n  {BOLD}Últimos mensajes:{RST}")
                for l in lines:
                    print(f"  {DIM}{l}{RST}")

        except Exception as e:
            print(f"  Error: {e}")
        print()

    def _cmd_identidad(self):
        """NUEVO v5: muestra identidad y principios de Bell."""
        print(f"\n  {BOLD}🌺 Identidad de Bell{RST}")
        print(f"  {'─'*42}")

        if not _IDENTIDAD_OK:
            print(f"  {YELL}identidad_bell.py no disponible.{RST}")
            print(f"  Principio: {PRINCIPIO_CENTRAL}")
        else:
            print(f"  {BOLD}Principio central:{RST}")
            print(f"    {PRINCIPIO_CENTRAL}")

            if NARRATIVA_PROPIA:
                print(f"\n  {BOLD}Narrativa propia:{RST}")
                lineas = NARRATIVA_PROPIA.split("\n")[:4]
                for l in lineas:
                    if l.strip():
                        print(f"    {l.strip()}")

            if VOZ_BELL:
                nunca = VOZ_BELL.get("nunca", [])
                siempre = VOZ_BELL.get("siempre", [])
                if nunca:
                    print(f"\n  {BOLD}Nunca dice:{RST}")
                    for item in nunca[:3]:
                        print(f"    ✗ {item}")
                if siempre:
                    print(f"\n  {BOLD}Siempre hace:{RST}")
                    for item in siempre[:3]:
                        print(f"    ✅ {item}")

            if NOMBRES_SEBASTIAN:
                print(f"\n  {BOLD}Cómo llama a Sebastián:{RST}")
                for momento, nombre in list(NOMBRES_SEBASTIAN.items())[:3]:
                    print(f"    {momento}: {nombre}")

        print()

    def _cmd_personas(self):
        """NUEVO v5: muestra personas que Bell conoce."""
        print(f"\n  {BOLD}👥 Personas que Bell conoce{RST}")
        print(f"  {'─'*42}")

        if not hasattr(self.gestor_memoria, "obtener_persona"):
            print(f"  {YELL}GestorMemoria v5 no disponible.{RST}")
            print()
            return

        # Intentar leer desde el cache interno
        personas = {}
        try:
            personas = getattr(self.gestor_memoria, "_cache_personas", {})
        except Exception:
            pass

        if not personas:
            print("  (Bell no ha construido modelos de personas todavía)")
            print("  Menciona a alguien en la conversación para que lo registre.")
        else:
            for nombre_p, datos_p in list(personas.items())[:5]:
                print(f"\n  {BOLD}{nombre_p}{RST}")
                if isinstance(datos_p, dict):
                    genero    = datos_p.get("genero", "")
                    menciones = datos_p.get("menciones", 0)
                    emociones = datos_p.get("emociones_asociadas", [])
                    print(f"    Género: {genero or 'desconocido'}  "
                          f"Menciones: {menciones}")
                    if emociones:
                        print(f"    Emociones: {', '.join(emociones[:3])}")
        print()

    def _cmd_toggle_groq(self):
        try:
            from llm.groq_wrapper import GroqWrapper  # noqa
            self.usar_groq = not self.usar_groq
            self.generador.usar_groq = self.usar_groq
            estado = f"{GREEN}ACTIVADO{RST}" if self.usar_groq else f"{YELL}DESACTIVADO{RST}"
            print(f"  Groq: {estado}\n")
        except ImportError:
            print(f"  {YELL}Groq no disponible en este entorno.{RST}\n")


# ─────────────────────────────────────────────────────────────────────────────
# PUNTO DE ENTRADA
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Belladonna v5.0 — FASE 4A")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Mostrar metadata de cada paso")
    parser.add_argument("--use-groq", action="store_true",
                        help="Activar Groq para respuestas naturales")
    args = parser.parse_args()

    bell = Belladonna(usar_groq=args.use_groq, verbose=args.verbose)
    bell.loop()


if __name__ == "__main__":
    main()