"""
Belladonna v4.0 — FASE 4A COMPLETA

ARQUITECTURA MENTE PURA:
    Bell (Python)  = Razona con 1,483 conceptos verificados
    Groq  (API)    = SOLO embellece texto
    Echo  (Python) = Verifica que Groq no invente nada

FIX v3 CRÍTICO:
    Memoria compartida inyectada al generador en iniciar_sesion().
    Sin esto: el generador crea su propia instancia de GestorMemoria
    → dos objetos separados en RAM → Groq nunca ve el historial → inventa libremente.
    Con esto: generador.memoria = self.gestor_memoria → una sola instancia.

USO:
    python main.py              → Sin Groq (honesta, simbólica)
    python main.py --use-groq   → Con Groq (honesta, natural)
    python main.py -v           → Verbose (metadata de cada paso)
    python main.py --use-groq -v
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


# ─── Helpers de importación ───────────────────────────────────────────────────

def _importar(ruta: str, clase: str):
    """Importa una clase; devuelve None si el módulo no existe."""
    try:
        m = __import__(ruta, fromlist=[clase])
        return getattr(m, clase)
    except (ImportError, AttributeError):
        return None


def _importar_obligatorio(ruta: str, clase: str):
    """Importa una clase crítica; aborta con mensaje claro si falla."""
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
    Belladonna v4.0 — Sistema Conversacional Completo.

    Flujo por mensaje:
        1. TraductorEntrada   → español → ConceptosAnclados
        2. MotorRazonamiento  → clasificar intención → Decision + hechos reales
        3. Consejeras deliberan (Vega puede vetar cualquier decisión)
        4. GeneradorSalida    → Decision → español natural (Groq + Echo si activo)
        5. GestorMemoria      → persiste historial de la sesión

    Módulos opcionales (el sistema funciona sin ellos):
        bucles/, aprendizaje/, grounding/, operaciones/, base_datos/
    """

    def __init__(self, usar_groq: bool = False, verbose: bool = False):
        self.usar_groq       = usar_groq
        self.verbose         = verbose
        self.turnos          = 0
        self._fase2_activa   = False
        self._emociones: dict = {}
        self.id_sesion       = None

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
        # Inyectar vocabulario para conteos dinámicos en _hechos_identidad()
        self.motor.gestor_vocabulario = self.gestor_vocab
        print(f"  {GREEN}✅ Motor:{RST}         razonamiento v3")

        # ── Consejeras ────────────────────────────────────────────────────────
        self._cargar_consejeras()

        # ── Generador de salida ───────────────────────────────────────────────
        self.generador = GeneradorSalida(usar_groq=usar_groq)
        modo = f"{GREEN}Groq + Echo ACTIVOS{RST}" if usar_groq else f"{YELL}modo simbólico{RST}"
        print(f"  {GREEN}✅ Generador:{RST}     {modo}")

        # ── Memoria ───────────────────────────────────────────────────────────
        self.gestor_memoria = GestorMemoria()
        print(f"  {GREEN}✅ Memoria:{RST}       persistente lista")

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
        print()
        print(f"  {'═'*58}")
        print(f"  {BOLD}{CYAN}{'🌺  BELLADONNA  v4.0  🌺':^58}{RST}")
        print(f"  {'Sistema Conversacional — FASE 4A':^58}")
        print(f"  {'1,483 conceptos  ·  Groq Natural  ·  Echo':^58}")
        print(f"  {'═'*58}")
        print()
        print("  Iniciando sistemas...")
        print()

    def _total_conceptos(self) -> int:
        for metodo in ("total_conceptos", ):
            if hasattr(self.gestor_vocab, metodo):
                try:
                    return getattr(self.gestor_vocab, metodo)()
                except Exception:
                    pass
        try:
            return len(self.gestor_vocab.obtener_todos())
        except Exception:
            return 1483

    def _cargar_consejeras(self):
        """Carga el gestor de consejeras con fallbacks en cascada."""
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

        # Fallback: solo Vega
        Vega = (_importar("consejeras.vega.vega", "Vega")
                or _importar("consejeras.vega", "Vega"))
        if Vega:
            try:
                self.consejeras = [Vega()]
                print(f"  {YELL}⚠  Consejeras:{RST}    solo Vega (guardiana de principios)")
                return
            except Exception:
                pass

        print(f"  {YELL}⚠  Consejeras:{RST}    no disponibles")

    def _cargar_opcionales(self):
        """Carga módulos opcionales de forma tolerante."""
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
        """Arranca la sesión e inyecta la memoria compartida al generador."""
        if self._fase2_activa:
            return

        print(f"  {CYAN}▶ Iniciando sesión...{RST}")

        try:
            self.id_sesion = self.gestor_memoria.iniciar_sesion()
            print(f"  {GREEN}✅{RST} Sesión: {self.id_sesion[:8]}...")
        except Exception:
            self.id_sesion = datetime.now().isoformat()

        # ══════════════════════════════════════════════════════════════════════
        # FIX v3 CRÍTICO — INYECCIÓN DE MEMORIA COMPARTIDA
        # ══════════════════════════════════════════════════════════════════════
        # PROBLEMA: GeneradorSalida._obtener_memoria() crea su propio
        # GestorMemoria en la primera llamada → dos instancias en RAM → el
        # generador nunca ve el nombre ni historial registrado aquí → Groq
        # recibe contexto vacío → inventa libremente.
        #
        # SOLUCIÓN: apuntar generador.memoria a la instancia compartida ANTES
        # del primer mensaje. Ambos leen y escriben en el mismo objeto.
        # ══════════════════════════════════════════════════════════════════════
        self.generador.memoria = self.gestor_memoria
        print(f"  {GREEN}✅{RST} Memoria compartida inyectada al generador")

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
        """Detiene subsistemas y guarda la sesión."""
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

        Flujo completo:
            Emoción → Traducción → Razonamiento → Consejeras → Generación → Memoria
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
            decision = self.motor.razonar(traduccion)
            if v:
                print(f"\n  🧠 Decisión: {decision.tipo.name}  "
                      f"certeza={decision.certeza:.0%}  "
                      f"ejecutar={decision.puede_ejecutar}")

            # 3 · Consejeras (todas deliberan; Vega puede vetar)
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

            # 4 · Generación (Groq + Echo si activo, simbólico si no)
            if v:
                modo = "GROQ+ECHO" if self.usar_groq else "SIMBÓLICO"
                print(f"\n  🎨 Generando [{modo}]...")

            respuesta = self.generador.generar(decision, contexto)

            if v:
                preview = (respuesta[:100] + "...") if len(respuesta) > 100 else respuesta
                print(f"  → \"{preview}\"")

            # 5 · Registro operacional en memoria
            # (el generador ya registra usuario + bell en _generar_conversacional)
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
        """Loop conversacional principal."""
        self.iniciar_sesion()

        # Saludo inicial personalizado
        nombre = ""
        try:
            nombre = self.gestor_memoria.el_usuario_se_llama() or ""
        except Exception:
            pass

        hora = datetime.now().hour
        if nombre:
            saludo = f"¡Hola de nuevo, {nombre}! Aquí estoy. ¿En qué te ayudo?"
        elif 5 <= hora < 12:
            saludo = "¡Buenos días! Soy Bell. ¿Cómo te llamas y en qué te ayudo?"
        elif 12 <= hora < 19:
            saludo = "¡Buenas tardes! Soy Bell. ¿En qué puedo ayudarte?"
        else:
            saludo = "¡Buenas noches! Soy Bell. ¿En qué puedo ayudarte?"

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
                    self._cmd_help();   continue
                if el == "stats":
                    self._cmd_stats();  continue
                if el == "groq":
                    self._cmd_groq();   continue
                if el == "memoria":
                    self._cmd_memoria(); continue
                if el == "emociones":
                    self._cmd_emociones(); continue
                if el == "toggle_groq":
                    self._cmd_toggle_groq(); continue
                if el == "verbose":
                    self.verbose = not self.verbose
                    print(f"   {YELL}Verbose: {'ON 🔍' if self.verbose else 'OFF'}{RST}\n")
                    continue

                # ── Mensaje normal ────────────────────────────────────────────
                respuesta = self.procesar(entrada)
                self.turnos += 1
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
  {'─'*38}
  stats        Estadísticas del sistema
  groq         Estado de Groq y Echo
  memoria      Lo que Bell recuerda de ti
  emociones    Emociones detectadas en la sesión
  toggle_groq  Activar/desactivar Groq en caliente
  verbose      Activar/desactivar debug detallado
  help         Esta ayuda
  salir        Terminar
  {'─'*38}
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
  {'─'*38}
  Vocabulario   {total} conceptos
  Consejeras    {len(self.consejeras)} activas
  Turnos        {self.turnos}
  Groq          {'ON ✅' if self.usar_groq else 'OFF'}
  {'─'*38}
  Respuestas    {sg.get('total_generadas', 0)}
  Con Groq      {sg.get('groq_usadas', 0)}
  Bloqueadas    {sg.get('groq_bloqueadas', 0)}
  Fallback      {sg.get('fallback_a_simbolico', 0)}
""")

    def _cmd_groq(self):
        if self.usar_groq:
            sg = {}
            try:
                sg = self.generador.obtener_estadisticas()
            except Exception:
                pass
            print(f"""
  {GREEN}Groq: ACTIVO{RST}
  {'─'*38}
  Llamadas Groq     {sg.get('groq_usadas', 0)}
  Bloqueadas Echo   {sg.get('groq_bloqueadas', 0)}
  Tasa éxito        {sg.get('tasa_groq', 0):.1%}
  {'─'*38}
  Anti-invención    {GREEN}ACTIVA{RST}
  Echo verificando  {GREEN}ACTIVO{RST}
  Memoria inyectada {GREEN}SÍ{RST}
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
        try:
            datos    = self.gestor_memoria.obtener_datos_usuario()
            historial = self.gestor_memoria.obtener_contexto(n_mensajes=6)
            print(f"\n  {BOLD}Lo que Bell recuerda:{RST}")
            print(f"  {'─'*38}")
            if datos:
                for k, v in datos.items():
                    print(f"  {k}: {v}")
            else:
                print("  (sin datos del usuario todavía)")
            if historial:
                lines = historial.strip().split("\n")[-6:]
                print(f"\n  Últimos mensajes:")
                for l in lines:
                    print(f"  {DIM}{l}{RST}")
        except Exception as e:
            print(f"  Error: {e}")
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
    parser = argparse.ArgumentParser(description="Belladonna v4.0 — FASE 4A")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Mostrar metadata de cada paso")
    parser.add_argument("--use-groq", action="store_true",
                        help="Activar Groq para respuestas naturales")
    args = parser.parse_args()

    bell = Belladonna(usar_groq=args.use_groq, verbose=args.verbose)
    bell.loop()


if __name__ == "__main__":
    main()