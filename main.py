"""
Belladonna v6.2 — FASE 4A — SUB-PASO 2C: SQLite Ejecutable

CAMBIOS v6.2 sobre v6.1:
═══════════════════════════════════════════════════════════════════════

FIX-MAIN-3  INYECCIÓN DE SQLITE EN GENERADOR
            En iniciar_sesion(), después de inyectar shell, también
            se inyecta bd_cliente en HabilidadSQLite:
                self._inyectar_sqlite()
            Permite que _ejecutar_habilidad_generica() en el generador
            use el ClienteSQLite ya inicializado y conectado.

FIX-MAIN-4  COMANDO 'bd' EN LOOP
            Nuevo comando de diagnóstico: 'bd'
            Muestra estado de la base de datos, tablas disponibles
            y estado de HabilidadSQLite en el registro.

FIX-MAIN-5  Banner y motor actualizados a v8.9 / v6.2.

TODOS LOS CAMBIOS v6.1 PRESERVADOS:
- FIX-MAIN-1: inyección de shell en generador
- FIX-MAIN-2: comando 'shell' en loop
- FIX-M1: cargar_capa1=True
- FIX-M2: verificación Echo en main.procesar()
- FIX-M3: importación de capacidades_fase.py
- Inyecciones: generador.memoria, motor.gestor_memoria
═══════════════════════════════════════════════════════════════════════
"""

import sys
import argparse
import logging
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

logging.basicConfig(level=logging.WARNING, format="%(levelname)s [%(name)s] %(message)s")
for _lib in ("httpx", "groq", "openai", "urllib3"):
    logging.getLogger(_lib).setLevel(logging.ERROR)

BOLD  = "\033[1m"
CYAN  = "\033[96m"
GREEN = "\033[92m"
YELL  = "\033[93m"
RED   = "\033[91m"
DIM   = "\033[2m"
RST   = "\033[0m"

try:
    from identidad_bell import (
        PRINCIPIO_CENTRAL, NARRATIVA_PROPIA, VOZ_BELL,
        NOMBRES_SEBASTIAN, obtener_nombre,
    )
    _IDENTIDAD_OK = True
except ImportError:
    _IDENTIDAD_OK         = False
    PRINCIPIO_CENTRAL     = "solo afirmo lo que puedo ejecutar o verificar"
    NARRATIVA_PROPIA      = ""
    VOZ_BELL              = {}
    NOMBRES_SEBASTIAN     = {}

try:
    from core.capacidades_fase import NO_IMPLEMENTADAS_IDS, esta_implementada
    _HONESTIDAD_OK          = True
    _TOTAL_NO_IMPLEMENTADAS = len(NO_IMPLEMENTADAS_IDS)
except ImportError:
    _HONESTIDAD_OK          = False
    _TOTAL_NO_IMPLEMENTADAS = 0
    def esta_implementada(cid): return True


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
        sys.exit(1)
    return cls


class Belladonna:
    """
    Belladonna v6.2 — Shell + SQLite ejecutables.

    Flujo por mensaje:
        1. TraductorEntrada   → español → ConceptosAnclados
        2. MotorRazonamiento  → clasificar intención → Decision + hechos
           · v8.9: P0.5 detecta SHELL y BD antes que P1
           · P0.5 EXT: patrones_habilidades.py para habilidades futuras
        3. FIX-M2: Verificación Echo en main
        4. Consejeras deliberan (Vega puede vetar)
        5. GeneradorSalida    → Decision → español natural
           · EJECUCION SHELL  → _ejecutar_shell_conversacional()
           · EJECUCION BD     → _ejecutar_habilidad_generica("SQLITE")
        6. GestorMemoria      → persiste historial
    """

    def __init__(self, usar_groq: bool = False, verbose: bool = False):
        self.usar_groq      = usar_groq
        self.verbose        = verbose
        self.turnos         = 0
        self._fase2_activa  = False
        self._emociones: dict = {}
        self.id_sesion      = None
        self._echo_main     = None

        self._banner()

        GestorVocabulario = _importar_obligatorio("vocabulario.gestor_vocabulario", "GestorVocabulario")
        TraductorEntrada  = _importar_obligatorio("traduccion.traductor_entrada",   "TraductorEntrada")
        MotorRazonamiento = _importar_obligatorio("razonamiento.motor_razonamiento", "MotorRazonamiento")
        GeneradorSalida   = _importar_obligatorio("generacion.generador_salida",    "GeneradorSalida")
        GestorMemoria     = _importar_obligatorio("memoria.gestor_memoria",         "GestorMemoria")

        # FIX-M1: cargar_capa1=True
        try:
            self.gestor_vocab = GestorVocabulario(cargar_expansion=True, cargar_capa1=True)
        except TypeError:
            try:
                self.gestor_vocab = GestorVocabulario(cargar_expansion=True)
            except TypeError:
                self.gestor_vocab = GestorVocabulario()

        total = self._total_conceptos()
        print(f"  {GREEN}✅ Vocabulario:{RST}   {total} conceptos")

        self.traductor = TraductorEntrada(self.gestor_vocab)
        print(f"  {GREEN}✅ Traductor:{RST}     activo")

        self.motor = MotorRazonamiento()
        self.motor.gestor_vocabulario = self.gestor_vocab
        print(f"  {GREEN}✅ Motor:{RST}         razonamiento v8.9")

        self._cargar_consejeras()

        self.generador = GeneradorSalida(usar_groq=usar_groq)
        modo = f"{GREEN}Groq + Echo ACTIVOS{RST}" if usar_groq else f"{YELL}modo simbólico + Echo{RST}"
        print(f"  {GREEN}✅ Generador:{RST}     {modo}")

        self.gestor_memoria = GestorMemoria()
        print(f"  {GREEN}✅ Memoria:{RST}       persistente lista")

        self._cargar_echo_main()

        if _IDENTIDAD_OK:
            print(f"  {GREEN}✅ Identidad:{RST}     Bell cargada")
        else:
            print(f"  {YELL}⚠  Identidad:{RST}     identidad_bell.py no encontrado")

        if _HONESTIDAD_OK:
            print(f"  {GREEN}✅ Honestidad:{RST}    {_TOTAL_NO_IMPLEMENTADAS} capacidades bloqueadas")
        else:
            print(f"  {RED}✗  Honestidad:{RST}    core/capacidades_fase.py no encontrado — RIESGO")

        self._cargar_opcionales()

        print()
        print(f"  {'─'*56}")
        if usar_groq:
            print(f"  {BOLD}Bell está lista con Groq activo.{RST}")
        else:
            print(f"  {BOLD}Bell está lista.{RST}  {DIM}(usa --use-groq para Groq){RST}")
        print()

    def _banner(self):
        version = "v6.2"
        nombre  = "Belladonna (Bell)" if _IDENTIDAD_OK else "Belladonna"
        print()
        print(f"  {'═'*58}")
        print(f"  {BOLD}{CYAN}{f'🌺  {nombre}  {version}  🌺':^58}{RST}")
        print(f"  {'Sistema Conversacional — FASE 4A — Shell + SQLite':^58}")
        print(f"  {f'{PRINCIPIO_CENTRAL[:54]}':^58}")
        print(f"  {'═'*58}")
        print()
        print("  Iniciando sistemas...")
        print()

    def _total_conceptos(self) -> int:
        if hasattr(self.gestor_vocab, "total_conceptos"):
            try:
                return self.gestor_vocab.total_conceptos()
            except Exception:
                pass
        try:
            return len(self.gestor_vocab.obtener_todos())
        except Exception:
            return 1472

    def _cargar_echo_main(self):
        try:
            from consejeras.echo.logica import Echo
            self._echo_main = Echo()
            print(f"  {GREEN}✅ Echo main:{RST}     verificador activo")
        except ImportError:
            self._echo_main = None
            print(f"  {YELL}⚠  Echo main:{RST}     no disponible")

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

        # FIX-MAIN-1: ShellExecutor
        ShellExecutor = _importar("operaciones.shell_executor", "ShellExecutor")
        self.shell = None
        if ShellExecutor:
            try:
                self.shell = ShellExecutor()
                cmds   = getattr(self.shell, '_whitelist', None)
                n_cmds = len(cmds) if cmds else "?"
                print(f"  {GREEN}✅{RST} Shell executor:    activo ({n_cmds} comandos en whitelist)")
            except Exception as e:
                if self.verbose:
                    print(f"  {YELL}⚠ ShellExecutor: {e}{RST}")
                print(f"  {YELL}⚠ {RST} Shell executor:    no disponible")
        else:
            print(f"  {YELL}⚠ {RST} Shell executor:    no disponible")

        # SQLite
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

    # ─────────────────────────────────────────────────────────────────
    # FIX-MAIN-3: INYECCIÓN DE SQLITE
    # ─────────────────────────────────────────────────────────────────

    def _inyectar_sqlite(self):
        """
        FIX-MAIN-3: inyecta bd_cliente y gestor_bd en HabilidadSQLite.
        Patrón idéntico al de inyección de ShellExecutor.
        Se llama desde iniciar_sesion() una vez que bd_cliente está conectado.
        """
        if not self.bd_cliente:
            return
        try:
            from habilidades.registro_habilidades import RegistroHabilidades
            registro         = RegistroHabilidades.obtener()
            habilidad_sqlite = registro.obtener_habilidad("SQLITE")
            if habilidad_sqlite is not None:
                habilidad_sqlite.configurar_cliente(
                    self.bd_cliente,
                    getattr(self, 'gestor_bd', None),
                )
                logging.getLogger("main").info("HabilidadSQLite: bd_cliente inyectado")
                print(f"  {GREEN}✅{RST} SQLite inyectado en HabilidadSQLite")
            else:
                logging.getLogger("main").warning("HabilidadSQLite no encontrada en registro")
                print(f"  {YELL}⚠ {RST} HabilidadSQLite no registrada — BD sin habilidad")
        except Exception as e:
            logging.getLogger("main").error(f"Error inyectando SQLite: {e}")
            if self.verbose:
                print(f"  {YELL}⚠ SQLite inyección: {e}{RST}")

    # ─────────────────────────────────────────────────────────────────
    # CICLO DE VIDA
    # ─────────────────────────────────────────────────────────────────

    def iniciar_sesion(self):
        if self._fase2_activa:
            return

        print(f"  {CYAN}▶ Iniciando sesión...{RST}")

        try:
            self.id_sesion = self.gestor_memoria.iniciar_sesion()
            print(f"  {GREEN}✅{RST} Sesión: {self.id_sesion[:8]}...")
        except Exception:
            self.id_sesion = datetime.now().isoformat()

        # Inyecciones críticas
        self.generador.memoria    = self.gestor_memoria
        self.motor.gestor_memoria = self.gestor_memoria
        print(f"  {GREEN}✅{RST} Memoria inyectada al generador y motor")

        # FIX-MAIN-1: Inyectar shell en generador
        if self.shell:
            self.generador.shell = self.shell
            print(f"  {GREEN}✅{RST} Shell inyectado en generador")
        else:
            print(f"  {YELL}⚠ {RST} Shell no disponible — comandos de terminal desactivados")

        # Conectar BD y luego inyectar en HabilidadSQLite
        if self.bd_cliente:
            try:
                self.bd_cliente.conectar()
                print(f"  {GREEN}✅{RST} Base de datos conectada")
            except Exception:
                pass
            self._inyectar_sqlite()   # FIX-MAIN-3
        else:
            print(f"  {YELL}⚠ {RST} Base de datos no disponible — consultas BD desactivadas")

        if self.gestor_bucles:
            try:
                self.gestor_bucles.iniciar_todos()
                print(f"  {GREEN}✅{RST} Bucles autónomos activos")
            except Exception as e:
                if self.verbose:
                    print(f"  {YELL}⚠ Bucles: {e}{RST}")

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

    # ─────────────────────────────────────────────────────────────────
    # DETECCIÓN DE EMOCIÓN
    # ─────────────────────────────────────────────────────────────────

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

    # ─────────────────────────────────────────────────────────────────
    # FIX-M2: VERIFICACIÓN ECHO EN MAIN
    # ─────────────────────────────────────────────────────────────────

    def _verificar_decision_echo(self, decision):
        if not self._echo_main:
            return decision
        try:
            resultado = self._echo_main.verificar_decision(decision)
            if not resultado['coherente']:
                if self.verbose:
                    print(f"  {YELL}⚠ Echo-main: {resultado['problemas']}{RST}")
                from razonamiento.tipos_decision import TipoDecision, Decision as DecisionCls
                if decision.tipo == TipoDecision.AFIRMATIVA and not decision.puede_ejecutar:
                    hechos = decision.hechos_reales or {}
                    hechos['capacidad_solicitada_disponible'] = False
                    return DecisionCls(
                        tipo=TipoDecision.CAPACIDAD_BELL,
                        certeza=decision.certeza,
                        conceptos_principales=decision.conceptos_principales,
                        puede_ejecutar=False,
                        razon="Echo-main corrigió AFIRMATIVA incoherente",
                        hechos_reales=hechos,
                    )
        except Exception as e:
            if self.verbose:
                print(f"  {DIM}Echo-main error: {e}{RST}")
        return decision

    # ─────────────────────────────────────────────────────────────────
    # PROCESAMIENTO PRINCIPAL
    # ─────────────────────────────────────────────────────────────────

    def procesar(self, mensaje: str) -> str:
        try:
            v = self.verbose

            if v:
                print(f"\n{'═'*64}")
                print(f"  📥 MENSAJE: \"{mensaje}\"")
                print(f"{'═'*64}")

            emocion, tono = self._detectar_emocion(mensaje)
            if v and emocion:
                print(f"\n  💭 Emoción: {emocion} → tono: {tono}")

            traduccion = self.traductor.traducir(mensaje)
            if v:
                cs = traduccion.get("conceptos", [])
                print(f"\n  🔄 Traducción: {len(cs)} conceptos "
                      f"(confianza {traduccion.get('confianza', 0):.0%})")
                for c in cs[:4]:
                    print(f"     • {c.id}  g={c.confianza_grounding:.2f}")

            decision = self.motor.razonar(traduccion)
            if v:
                print(f"\n  🧠 Decisión: {decision.tipo.name}  "
                      f"certeza={decision.certeza:.0%}  "
                      f"ejecutar={decision.puede_ejecutar}")
                if decision.tipo.name == "EJECUCION" and decision.hechos_reales:
                    hid = decision.hechos_reales.get("habilidad_id", "?")
                    cmd = decision.hechos_reales.get("comando_detectado", "")
                    op  = decision.hechos_reales.get("operacion", "")
                    print(f"     → habilidad: {hid}  cmd/op: {cmd or op}")

            decision = self._verificar_decision_echo(decision)

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

            if v:
                modo = "GROQ+ECHO" if self.usar_groq else "SIMBÓLICO+ECHO"
                print(f"\n  🎨 Generando [{modo}]...")

            respuesta = self.generador.generar(decision, contexto)

            if v:
                preview = (respuesta[:100] + "...") if len(respuesta) > 100 else respuesta
                print(f"  → \"{preview}\"")

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

                    _TIPOS_EPISODIO = {
                        "REGISTRO_USUARIO", "CONSULTA_MEMORIA",
                        "IDENTIDAD_BELL", "ESTADO_USUARIO",
                    }
                    tipo_nombre = decision.tipo.name
                    if tipo_nombre in _TIPOS_EPISODIO and hasattr(self.gestor_memoria, "registrar_episodio"):
                        try:
                            self.gestor_memoria.registrar_episodio(
                                resumen                  = mensaje[:120],
                                tema_principal           = tipo_nombre,
                                estado_emocional_usuario = emocion or "neutral",
                            )
                        except Exception:
                            pass
                except Exception:
                    pass

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

    # ─────────────────────────────────────────────────────────────────
    # LOOP CONVERSACIONAL
    # ─────────────────────────────────────────────────────────────────

    def loop(self):
        self.iniciar_sesion()

        nombre = ""
        try:
            nombre = self.gestor_memoria.el_usuario_se_llama() or ""
        except Exception:
            pass

        hora = datetime.now().hour

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

                if el in ("salir", "exit", "quit", "chao", "bye", "adios", "adiós"):
                    print("\n🌺 Bell: ¡Hasta pronto! Fue un gusto conversar.")
                    self.finalizar_sesion()
                    break

                if el == "help":        self._cmd_help();       continue
                if el == "stats":       self._cmd_stats();      continue
                if el == "groq":        self._cmd_groq();       continue
                if el == "memoria":     self._cmd_memoria();    continue
                if el == "emociones":   self._cmd_emociones();  continue
                if el == "toggle_groq": self._cmd_toggle_groq(); continue
                if el == "identidad":   self._cmd_identidad();  continue
                if el == "personas":    self._cmd_personas();   continue
                if el == "honestidad":  self._cmd_honestidad(); continue
                if el == "shell":       self._cmd_shell();      continue
                if el == "bd":          self._cmd_bd();         continue  # FIX-MAIN-4
                if el == "verbose":
                    self.verbose = not self.verbose
                    print(f"   {YELL}Verbose: {'ON 🔍' if self.verbose else 'OFF'}{RST}\n")
                    continue

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

    # ─────────────────────────────────────────────────────────────────
    # COMANDOS
    # ─────────────────────────────────────────────────────────────────

    def _cmd_help(self):
        shell_estado = f"{GREEN}ACTIVO{RST}" if self.shell      else f"{YELL}inactivo{RST}"
        bd_estado    = f"{GREEN}ACTIVO{RST}" if self.bd_cliente else f"{YELL}inactivo{RST}"
        print(f"""
  {BOLD}Comandos:{RST}
  {'─'*44}
  stats        Estadísticas del sistema
  groq         Estado de Groq y Echo
  memoria      Lo que Bell recuerda de ti
  emociones    Emociones detectadas en la sesión
  identidad    Identidad y principios de Bell
  personas     Personas que Bell conoce
  honestidad   Estado del sistema de honestidad
  shell        Estado del Shell Executor  ({shell_estado})
  bd           Estado de la base de datos  ({bd_estado})  {DIM}[nuevo v6.2]{RST}
  toggle_groq  Activar/desactivar Groq
  verbose      Activar/desactivar debug
  help         Esta ayuda
  salir        Terminar
  {'─'*44}
  {DIM}Shell: "lista tus archivos", "dónde estás", "estado de git"
  BD:    "qué tablas tienes", "esquema de X", "datos de X"
         "cuántos registros en X", "SELECT ... FROM X"{RST}
""")

    def _cmd_bd(self):
        """FIX-MAIN-4: Estado de la base de datos SQLite."""
        print(f"\n  {BOLD}🗄  Base de Datos — Sub-paso 2C{RST}")
        print(f"  {'─'*44}")

        if not self.bd_cliente:
            print(f"  {RED}✗ ClienteSQLite no disponible{RST}")
            print(f"    Verifica base_datos.py y su importación en _cargar_opcionales()")
            print()
            return

        print(f"  {GREEN}✅ ClienteSQLite ACTIVO{RST}")

        # Estado de HabilidadSQLite en el registro
        try:
            from habilidades.registro_habilidades import RegistroHabilidades
            reg    = RegistroHabilidades.obtener()
            hab_sq = reg.obtener_habilidad("SQLITE")
            if hab_sq:
                print(f"  {GREEN}✅ HabilidadSQLite registrada{RST}")
                cliente_ok = getattr(hab_sq, '_cliente', None) is not None
                print(f"     bd_cliente inyectado: {'sí ✅' if cliente_ok else 'no ⚠️'}")
                if hasattr(hab_sq, 'descripcion_para_bell'):
                    print(f"     {DIM}{hab_sq.descripcion_para_bell[:70]}...{RST}")
            else:
                print(f"  {YELL}⚠  HabilidadSQLite no registrada{RST}")
        except Exception as e:
            print(f"  {YELL}⚠  No se pudo consultar el registro: {e}{RST}")

        # Tablas disponibles
        try:
            tablas = self.bd_cliente.listar_tablas()
            if tablas:
                print(f"\n  {BOLD}Tablas ({len(tablas)}):{RST}")
                for t in tablas[:10]:
                    print(f"    • {t}")
                if len(tablas) > 10:
                    print(f"    ... y {len(tablas) - 10} más")
            else:
                print(f"\n  {DIM}Base de datos vacía (sin tablas aún){RST}")
        except Exception as e:
            print(f"\n  {YELL}No se pudieron listar tablas: {e}{RST}")

        # Patrones registrados
        try:
            from razonamiento.patrones_habilidades import (
                listar_habilidades_registradas,
                obtener_patrones_por_habilidad,
            )
            habs = listar_habilidades_registradas()
            print(f"\n  {BOLD}Habilidades con patrones externos ({len(habs)}):{RST}")
            for hid in habs:
                n = len(obtener_patrones_por_habilidad(hid))
                print(f"    • {hid:<20} {n} patrones")
        except Exception:
            pass

        print(f"\n  {DIM}Prueba: 'qué tablas tienes', 'esquema de usuarios',")
        print(f"         'cuántos registros en pedidos', 'SELECT * FROM ...'{RST}")
        print()

    def _cmd_shell(self):
        """Estado del ShellExecutor."""
        print(f"\n  {BOLD}🖥  Shell Executor — Sub-paso 2B{RST}")
        print(f"  {'─'*44}")

        if not self.shell:
            print(f"  {RED}✗ ShellExecutor no disponible{RST}")
            print(f"    Verifica operaciones/shell_executor.py")
            print()
            return

        print(f"  {GREEN}✅ ShellExecutor ACTIVO{RST}")

        whitelist = getattr(self.shell, '_whitelist', None) or getattr(self.shell, 'whitelist', None)
        if whitelist:
            print(f"\n  {BOLD}Comandos permitidos ({len(whitelist)}):{RST}")
            cmds = sorted(list(whitelist))[:15]
            for i in range(0, len(cmds), 3):
                fila = cmds[i:i+3]
                print("    " + "  ".join(f"{c:<18}" for c in fila))
            if len(whitelist) > 15:
                print(f"    ... y {len(whitelist) - 15} más")

        timeout = getattr(self.shell, 'timeout', None)
        if timeout:
            print(f"\n  Timeout:    {timeout}s")

        directorio = getattr(self.shell, 'working_dir', None) or getattr(self.shell, 'cwd', None)
        if directorio:
            print(f"  Directorio: {directorio}")

        try:
            from habilidades.registro_habilidades import RegistroHabilidades
            reg       = RegistroHabilidades.obtener()
            shell_hab = reg.obtener_habilidad("SHELL")
            if shell_hab:
                print(f"\n  {GREEN}✅ HabilidadShell registrada (prioridad 80){RST}")
                print(f"     {DIM}{shell_hab.descripcion_para_bell[:70]}...{RST}")
            else:
                print(f"\n  {YELL}⚠  HabilidadShell no registrada{RST}")
        except Exception:
            pass

        print(f"\n  {DIM}Prueba: 'lista tus archivos', 'dónde estás',")
        print(f"         'estado de git', 'cuánta memoria tienes'{RST}")
        print()

    def _cmd_stats(self):
        total = self._total_conceptos()
        sg    = {}
        try:
            sg = self.generador.obtener_estadisticas()
        except Exception:
            pass
        shell_ico = "✅" if self.shell      else "⚠️"
        bd_ico    = "✅" if self.bd_cliente else "⚠️"
        print(f"""
  {BOLD}Estadísticas:{RST}
  {'─'*44}
  Vocabulario   {total} conceptos
  Consejeras    {len(self.consejeras)} activas
  Turnos        {self.turnos}
  Groq          {'ON ✅' if self.usar_groq else 'OFF'}
  Shell         {shell_ico}
  BD SQLite     {bd_ico}
  Honestidad    {'activa ✅' if _HONESTIDAD_OK else 'NO ACTIVA ⚠️'}
  {'─'*44}
  Respuestas    {sg.get('total_generadas', 0)}
  Con Groq      {sg.get('groq_usadas', 0)}
  Bloqueadas    {sg.get('groq_bloqueadas', 0)}
  Echo correc.  {sg.get('echo_correcciones', 0)}
  Fallback      {sg.get('fallback_a_simbolico', 0)}
  Shell exec.   {sg.get('shell_ejecutados', 0)}
  Shell fall.   {sg.get('shell_fallidos', 0)}
  {'─'*44}
  Habilidades ejecutadas:""")
        for hid, cnt in sg.get('habilidades_ejecutadas', {}).items():
            print(f"    {hid:<25} {cnt}x")
        print(f"""  {'─'*44}
  Tipos de decisión:""")
        for tipo, cnt in sorted(sg.get('tipos_decision', {}).items(), key=lambda x: -x[1])[:8]:
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
  {'─'*44}
  Llamadas Groq     {sg.get('groq_usadas', 0)}
  Bloqueadas Echo   {sg.get('groq_bloqueadas', 0)}
  Echo correcciones {sg.get('echo_correcciones', 0)}
  Tasa éxito        {sg.get('tasa_groq', 0):.1%}
  {'─'*44}
  Anti-invención    {GREEN}ACTIVA{RST}
  Echo verificando  {GREEN}ACTIVO{RST}
  Honestidad        {GREEN + 'ACTIVA' if _HONESTIDAD_OK else RED + 'INACTIVA'}{RST}
  Shell ejecutable  {GREEN + 'ACTIVO' if self.shell else YELL + 'inactivo'}{RST}
  BD SQLite         {GREEN + 'ACTIVO' if self.bd_cliente else YELL + 'inactivo'}{RST}
""")
        else:
            print(f"""
  {YELL}Groq: DESACTIVADO{RST}
  Bell usa generación simbólica honesta con Echo activo.
  Shell y BD siguen activos — funcionan sin Groq.
  Activa con: python main.py --use-groq
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
            datos     = self.gestor_memoria.obtener_datos_usuario()
            historial = self.gestor_memoria.obtener_contexto(n_mensajes=6)

            print(f"\n  {BOLD}Lo que Bell recuerda:{RST}")
            print(f"  {'─'*44}")

            if datos:
                print(f"  {BOLD}Datos del usuario:{RST}")
                for k, v in datos.items():
                    print(f"    {k}: {v}")
            else:
                print("  (sin datos del usuario todavía)")

            if hasattr(self.gestor_memoria, "hay_temas_abiertos"):
                try:
                    if self.gestor_memoria.hay_temas_abiertos():
                        temas = self.gestor_memoria.obtener_temas_pendientes()
                        print(f"\n  {BOLD}Temas pendientes ({len(temas)}):{RST}")
                        for t in temas[:3]:
                            print(f"    • {t.get('tema', '?')} — {t.get('resumen', '')[:60]}")
                except Exception:
                    pass

            if historial:
                lines = historial.strip().split("\n")[-6:]
                print(f"\n  {BOLD}Últimos mensajes:{RST}")
                for l in lines:
                    print(f"  {DIM}{l}{RST}")

        except Exception as e:
            print(f"  Error: {e}")
        print()

    def _cmd_identidad(self):
        print(f"\n  {BOLD}🌺 Identidad de Bell{RST}")
        print(f"  {'─'*44}")
        if not _IDENTIDAD_OK:
            print(f"  {YELL}identidad_bell.py no disponible.{RST}")
            print(f"  Principio: {PRINCIPIO_CENTRAL}")
        else:
            print(f"  {BOLD}Principio central:{RST}")
            print(f"    {PRINCIPIO_CENTRAL}")
            if NARRATIVA_PROPIA:
                print(f"\n  {BOLD}Narrativa propia:{RST}")
                for l in NARRATIVA_PROPIA.split("\n")[:4]:
                    if l.strip():
                        print(f"    {l.strip()}")
            if VOZ_BELL:
                nunca   = VOZ_BELL.get("nunca", [])
                siempre = VOZ_BELL.get("siempre", [])
                if nunca:
                    print(f"\n  {BOLD}Nunca dice:{RST}")
                    for item in nunca[:4]:
                        print(f"    ✗ {item}")
                if siempre:
                    print(f"\n  {BOLD}Siempre hace:{RST}")
                    for item in siempre[:3]:
                        print(f"    ✅ {item}")
        print()

    def _cmd_personas(self):
        print(f"\n  {BOLD}👥 Personas que Bell conoce{RST}")
        print(f"  {'─'*44}")
        if not hasattr(self.gestor_memoria, "obtener_persona"):
            print(f"  {YELL}GestorMemoria v5+ no disponible.{RST}")
            print()
            return
        personas = {}
        try:
            personas = getattr(self.gestor_memoria, "_cache_personas", {})
        except Exception:
            pass
        if not personas:
            print("  (Bell no ha construido modelos de personas todavía)")
        else:
            for nombre_p, datos_p in list(personas.items())[:5]:
                print(f"\n  {BOLD}{nombre_p}{RST}")
                if isinstance(datos_p, dict):
                    print(f"    Género: {datos_p.get('genero','desconocido')}  "
                          f"Menciones: {datos_p.get('menciones',0)}")
        print()

    def _cmd_honestidad(self):
        print(f"\n  {BOLD}🛡 Sistema de Honestidad — Fase 4A{RST}")
        print(f"  {'─'*44}")
        if _HONESTIDAD_OK:
            print(f"  {GREEN}✅ core/capacidades_fase.py ACTIVO{RST}")
            print(f"     {_TOTAL_NO_IMPLEMENTADAS} capacidades bloqueadas")
            try:
                from core.capacidades_fase import NO_IMPLEMENTADAS
                print(f"\n  {BOLD}Capacidades no implementadas:{RST}")
                for cid, razon in list(NO_IMPLEMENTADAS.items())[:6]:
                    nombre = cid.replace("CONCEPTO_", "").lower()
                    print(f"    ✗ {nombre:<15} — {razon[:50]}")
                if len(NO_IMPLEMENTADAS) > 6:
                    print(f"    ... y {len(NO_IMPLEMENTADAS) - 6} más")
            except Exception:
                pass
        else:
            print(f"  {RED}✗ core/capacidades_fase.py NO ENCONTRADO{RST}")

        echo_ok  = self._echo_main is not None
        gen_echo = getattr(self.generador, '_echo_verificador', None) is not None
        print(f"\n  {BOLD}Echo verificadores:{RST}")
        print(f"    Echo main:      {GREEN + 'ACTIVO' if echo_ok  else RED + 'INACTIVO'}{RST}")
        print(f"    Echo generador: {GREEN + 'ACTIVO' if gen_echo else RED + 'INACTIVO'}{RST}")
        sg = {}
        try:
            sg = self.generador.obtener_estadisticas()
        except Exception:
            pass
        print(f"\n  {BOLD}Correcciones esta sesión:{RST}")
        print(f"    Echo correcciones: {sg.get('echo_correcciones', 0)}")
        print(f"    Bloqueadas:        {sg.get('groq_bloqueadas', 0)}")
        print()

    def _cmd_toggle_groq(self):
        try:
            from llm.groq_wrapper import GroqWrapper  # noqa
            self.usar_groq           = not self.usar_groq
            self.generador.usar_groq = self.usar_groq
            estado = f"{GREEN}ACTIVADO{RST}" if self.usar_groq else f"{YELL}DESACTIVADO{RST}"
            print(f"  Groq: {estado}\n")
        except ImportError:
            print(f"  {YELL}Groq no disponible en este entorno.{RST}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Belladonna v6.2 — FASE 4A — Shell + SQLite Ejecutable"
    )
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Mostrar metadata de cada paso")
    parser.add_argument("--use-groq", action="store_true",
                        help="Activar Groq para respuestas naturales")
    args = parser.parse_args()

    bell = Belladonna(usar_groq=args.use_groq, verbose=args.verbose)
    bell.loop()


if __name__ == "__main__":
    main()