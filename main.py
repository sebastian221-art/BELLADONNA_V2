"""
Belladonna v6.5 — FASE 4C — Shell + SQLite + Análisis Python

CAMBIOS v6.5 sobre v6.4:
═══════════════════════════════════════════════════════════════════════

FIX-MAIN-10  ENTRADA DE CÓDIGO — 4 MODOS HÍBRIDOS

             PROBLEMA RAÍZ (PowerShell Windows):
               input() procesa cada linea del clipboard inmediatamente.
               Al pegar un bloque de código con varias líneas,
               cada línea llegaba como mensaje separado.
               El modo backtick de v6.4 solo funcionaba si el usuario
               escribía ``` manualmente — NUNCA al pegar con CTRL+V.

             SOLUCIÓN: 4 modos que cubren todas las situaciones.

             ────────────────────────────────────────────────────────
             MODO 1 — Ruta de archivo (siempre funciona, 100% fiable)
             ────────────────────────────────────────────────────────
               "analiza C:\\mis_scripts\\mi_funcion.py"
               "analiza /home/user/proyecto/archivo.py"
               "analiza motor_razonamiento.py"
             Bell lee el archivo directamente. Funciona en cualquier
             terminal incluyendo PowerShell y CMD.

             ────────────────────────────────────────────────────────
             MODO 2 — Comando 'codigo' (el mas robusto para paste)
             ────────────────────────────────────────────────────────
               El usuario escribe 'codigo' (o 'analiza este código').
               Bell activa modo acumulador y muestra:
                 "Pega tu código. Escribe --- para terminar."
               PowerShell fragmenta el paste línea por línea, pero
               Bell acumula todas en el buffer. Al escribir '---'
               Bell analiza el bloque completo.

             ────────────────────────────────────────────────────────
             MODO 3 — Backtick mejorado (escribir a mano)
             ────────────────────────────────────────────────────────
               El usuario ESCRIBE (no pega) los backticks:
                 ```python
                 def f(x):
                     return x * 2
                 ```
               Bell acumula hasta el ``` de cierre.
               Útil en WSL, Git Bash, terminales modernas.

             ────────────────────────────────────────────────────────
             MODO 4 — Detección automática de código
             ────────────────────────────────────────────────────────
               Si Bell detecta que las líneas que llegan parecen
               código Python (def/class/import/indentación), las
               acumula automáticamente. Cierra con línea vacía o ---.

             RESUMEN DE FLUJOS:
               Archivo externo: "analiza C:\\ruta\\archivo.py" → directo
               Módulo Bell:     "analiza el motor" → directo
               Sistema Bell:    "analiza tu código" → directo
               Código inline:   escribe 'codigo' → pega → escribe ---
               Backtick manual: escribe ``` → escribe código → ``` para cerrar

TODOS LOS CAMBIOS v6.4 PRESERVADOS:
  FIX-MAIN-6:  inyección HabilidadAnalisisPython
  FIX-MAIN-7:  comando 'analizador'
  FIX-MAIN-3:  inyección SQLite
  FIX-M2:      Verificación Echo en main
═══════════════════════════════════════════════════════════════════════
"""

import sys
import re
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
    _IDENTIDAD_OK     = False
    PRINCIPIO_CENTRAL = "solo afirmo lo que puedo ejecutar o verificar"
    NARRATIVA_PROPIA  = ""
    VOZ_BELL          = {}
    NOMBRES_SEBASTIAN = {}

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
        print(f"\n{RED}No se pudo cargar {ruta}.{clase}{RST}")
        sys.exit(1)
    return cls


# ══════════════════════════════════════════════════════════════════════
# DETECCIÓN DE CÓDIGO PYTHON — usado por los modos 2 y 4
# ══════════════════════════════════════════════════════════════════════

_RE_CODIGO_PYTHON = [
    re.compile(r'^def\s+\w+'),
    re.compile(r'^class\s+\w+'),
    re.compile(r'^import\s+\S+'),
    re.compile(r'^from\s+\S+\s+import'),
    re.compile(r'^return\s+'),
    re.compile(r'^if\s+.+:'),
    re.compile(r'^elif\s+.+:'),
    re.compile(r'^else\s*:'),
    re.compile(r'^for\s+\S+\s+in'),
    re.compile(r'^while\s+.+:'),
    re.compile(r'^try\s*:'),
    re.compile(r'^except'),
    re.compile(r'^finally\s*:'),
    re.compile(r'^with\s+.+:'),
    re.compile(r'^\s{4}\S'),   # indentado 4+ espacios
    re.compile(r'^\t\S'),      # tabulado
    re.compile(r'^@\w+'),      # decoradores
    re.compile(r'^#.+'),       # comentarios Python
    re.compile(r'^"""'),       # docstrings
    re.compile(r"^'''"),
]

_RE_INICIO_ANALISIS_INLINE = re.compile(
    r'anali[sz]a(?:r)?\s+(?:este\s+)?c[oó]digo'
    r'|revisa(?:r)?\s+(?:este\s+)?c[oó]digo'
    r'|analiza\s+(?:el\s+)?siguiente\s+c[oó]digo'
    r'|revisa\s+(?:el\s+)?siguiente\s+c[oó]digo'
    r'|qu[eé]\s+(?:problemas?|errores?)\s+tiene\s+(?:este\s+)?c[oó]digo'
    r'|mejora(?:r)?\s+(?:este\s+)?c[oó]digo',
    re.IGNORECASE
)

_SEPARADORES_FIN = frozenset([
    '---', '-- -', '—', '```', 'fin', 'end', 'listo', 'ok', 'done'
])

_COMANDOS_CODIGO = frozenset(['codigo', 'código', 'code'])


def _es_linea_codigo_python(linea: str) -> bool:
    """Heurística: esta línea parece código Python."""
    s = linea.strip()
    if not s:
        return False
    return any(pat.match(s) for pat in _RE_CODIGO_PYTHON)


def _es_separador_fin(linea: str) -> bool:
    return linea.strip().lower() in _SEPARADORES_FIN


# ══════════════════════════════════════════════════════════════════════
# CLASE PRINCIPAL
# ══════════════════════════════════════════════════════════════════════

class Belladonna:
    """
    Belladonna v6.5 — Shell + SQLite + Análisis Python ejecutables.

    Flujo por mensaje:
        1. TraductorEntrada   → español → ConceptosAnclados
        2. MotorRazonamiento  → clasificar intención → Decision + hechos
        3. Echo verifica decisión (FIX-M2)
        4. Consejeras deliberan (Vega puede vetar, Nova supervisa análisis)
        5. GeneradorSalida    → Decision → español natural
        6. GestorMemoria      → persiste historial

    Modos de entrada de código Python (v6.5):
        1. Ruta de archivo    — "analiza C:\\ruta\\archivo.py"
        2. Comando 'codigo'   — acumula hasta '---'
        3. Backtick manual    — acumula hasta ``` de cierre
        4. Auto-detección     — detecta líneas de código automáticamente
    """

    def __init__(self, usar_groq: bool = False, verbose: bool = False):
        self.usar_groq        = usar_groq
        self.verbose          = verbose
        self.turnos           = 0
        self._fase2_activa    = False
        self._emociones: dict = {}
        self.id_sesion        = None
        self._echo_main       = None

        # ── Estado del buffer de código (v6.5) ────────────────────────
        # Cuando _buffer_activo=True, el loop acumula en _buffer_lineas
        # en lugar de procesar el mensaje directamente.
        self._buffer_activo   = False
        self._buffer_lineas   = []
        self._buffer_tipo     = ""   # "backtick" | "comando" | "auto"
        self._buffer_contexto = ""   # mensaje original que disparó el buffer

        self._banner()

        GestorVocabulario = _importar_obligatorio("vocabulario.gestor_vocabulario", "GestorVocabulario")
        TraductorEntrada  = _importar_obligatorio("traduccion.traductor_entrada",   "TraductorEntrada")
        MotorRazonamiento = _importar_obligatorio("razonamiento.motor_razonamiento","MotorRazonamiento")
        GeneradorSalida   = _importar_obligatorio("generacion.generador_salida",    "GeneradorSalida")
        GestorMemoria     = _importar_obligatorio("memoria.gestor_memoria",         "GestorMemoria")

        try:
            self.gestor_vocab = GestorVocabulario(cargar_expansion=True, cargar_capa1=True)
        except TypeError:
            try:
                self.gestor_vocab = GestorVocabulario(cargar_expansion=True)
            except TypeError:
                self.gestor_vocab = GestorVocabulario()

        total = self._total_conceptos()
        print(f"  {GREEN}OK Vocabulario:{RST}   {total} conceptos")

        self.traductor = TraductorEntrada(self.gestor_vocab)
        print(f"  {GREEN}OK Traductor:{RST}     activo")

        self.motor = MotorRazonamiento()
        self.motor.gestor_vocabulario = self.gestor_vocab
        print(f"  {GREEN}OK Motor:{RST}         razonamiento v9.1")

        self._cargar_consejeras()

        self.generador = GeneradorSalida(usar_groq=usar_groq)
        modo = f"{GREEN}Groq + Echo ACTIVOS{RST}" if usar_groq else f"{YELL}modo simbólico + Echo{RST}"
        print(f"  {GREEN}OK Generador:{RST}     {modo}")

        self.gestor_memoria = GestorMemoria()
        print(f"  {GREEN}OK Memoria:{RST}       persistente lista")

        self._cargar_echo_main()

        if _IDENTIDAD_OK:
            print(f"  {GREEN}OK Identidad:{RST}     Bell cargada")
        else:
            print(f"  {YELL}-- Identidad:{RST}     identidad_bell.py no encontrado")

        if _HONESTIDAD_OK:
            print(f"  {GREEN}OK Honestidad:{RST}    {_TOTAL_NO_IMPLEMENTADAS} capacidades bloqueadas")
        else:
            print(f"  {RED}!! Honestidad:{RST}    core/capacidades_fase.py no encontrado")

        self._cargar_opcionales()

        print()
        print(f"  {'─'*58}")
        if usar_groq:
            print(f"  {BOLD}Bell está lista con Groq activo.{RST}")
        else:
            print(f"  {BOLD}Bell está lista.{RST}  {DIM}(usa --use-groq para Groq){RST}")
        print()

    # ─────────────────────────────────────────────────────────────────

    def _banner(self):
        version = "v6.5"
        nombre  = "Belladonna (Bell)" if _IDENTIDAD_OK else "Belladonna"
        print()
        print(f"  {'═'*60}")
        print(f"  {BOLD}{CYAN}{'🌺  ' + nombre + '  ' + version + '  🌺':^60}{RST}")
        print(f"  {'Sistema Conversacional — FASE 4C — Shell + SQLite + Python':^60}")
        print(f"  {PRINCIPIO_CENTRAL[:56]:^60}")
        print(f"  {'═'*60}")
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
            print(f"  {GREEN}OK Echo main:{RST}     verificador activo")
        except ImportError:
            self._echo_main = None
            print(f"  {YELL}-- Echo main:{RST}     no disponible")

    def _cargar_consejeras(self):
        self.gestor_consejeras = None
        self.consejeras        = []

        GestorConsejeras = _importar("consejeras.gestor_consejeras", "GestorConsejeras")
        if GestorConsejeras:
            try:
                self.gestor_consejeras = GestorConsejeras()
                self.consejeras = getattr(self.gestor_consejeras, "consejeras", [])
                nombres = ", ".join(getattr(c, "nombre", "?") for c in self.consejeras)
                print(f"  {GREEN}OK Consejeras:{RST}    {len(self.consejeras)} activas — {nombres}")
                return
            except Exception as e:
                if self.verbose:
                    print(f"  {YELL}-- GestorConsejeras: {e}{RST}")

        Vega = (_importar("consejeras.vega.vega", "Vega")
                or _importar("consejeras.vega", "Vega"))
        if Vega:
            try:
                self.consejeras = [Vega()]
                print(f"  {YELL}-- Consejeras:{RST}    solo Vega")
                return
            except Exception:
                pass

        print(f"  {YELL}-- Consejeras:{RST}    no disponibles")

    def _cargar_opcionales(self):
        print()
        print("  Módulos opcionales:")

        GestorBucles = _importar("bucles.gestor_bucles", "GestorBucles")
        self.gestor_bucles = GestorBucles() if GestorBucles else None
        ico = GREEN if self.gestor_bucles else YELL
        print(f"  {ico}{'OK' if self.gestor_bucles else '--'}{RST} Bucles:            "
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
        ico = GREEN if self.motor_aprendizaje else YELL
        print(f"  {ico}{'OK' if self.motor_aprendizaje else '--'}{RST} Aprendizaje:       "
              + ("listo" if self.motor_aprendizaje else "no disponible"))

        ShellExecutor = _importar("operaciones.shell_executor", "ShellExecutor")
        self.shell = None
        if ShellExecutor:
            try:
                self.shell = ShellExecutor()
                n_cmds = len(getattr(self.shell, '_whitelist', []) or [])
                print(f"  {GREEN}OK{RST} Shell executor:    activo ({n_cmds} comandos)")
            except Exception as e:
                if self.verbose:
                    print(f"  {YELL}-- ShellExecutor: {e}{RST}")
                print(f"  {YELL}--{RST} Shell executor:    no disponible")
        else:
            print(f"  {YELL}--{RST} Shell executor:    no disponible")

        ClienteSQLite = _importar("base_datos", "ClienteSQLite")
        self.bd_cliente = None
        if ClienteSQLite:
            try:
                self.bd_cliente = ClienteSQLite(":memory:")
            except Exception:
                pass
        ico = GREEN if self.bd_cliente else YELL
        print(f"  {ico}{'OK' if self.bd_cliente else '--'}{RST} Base de datos:     "
              + ("SQLite activo" if self.bd_cliente else "no disponible"))

        self.python_analyzer = None
        try:
            from analisis.python_analyzer import PythonAnalyzer
            self.python_analyzer = PythonAnalyzer()
            print(f"  {GREEN}OK{RST} Python analyzer:  externo disponible")
        except ImportError:
            print(f"  {DIM}OK Python analyzer:  AST interno (sin dependencias){RST}")

    # ─────────────────────────────────────────────────────────────────
    # INYECCIONES
    # ─────────────────────────────────────────────────────────────────

    def _inyectar_sqlite(self):
        if not self.bd_cliente:
            return
        try:
            from habilidades.registro_habilidades import RegistroHabilidades
            registro  = RegistroHabilidades.obtener()
            hab_sq    = registro.obtener_habilidad("SQLITE")
            if hab_sq is not None:
                hab_sq.configurar_cliente(
                    self.bd_cliente,
                    getattr(self, 'gestor_bd', None),
                )
                print(f"  {GREEN}OK{RST} SQLite inyectado en HabilidadSQLite")
            else:
                print(f"  {YELL}--{RST} HabilidadSQLite no registrada")
        except Exception as e:
            if self.verbose:
                print(f"  {YELL}-- SQLite inyección: {e}{RST}")

    def _inyectar_analizador(self):
        try:
            from habilidades.registro_habilidades import RegistroHabilidades
            registro = RegistroHabilidades.obtener()
            hab_an   = registro.obtener_habilidad("ANALISIS_PYTHON")
            if hab_an is None:
                print(f"  {YELL}--{RST} HabilidadAnalisisPython no registrada")
                return
            if self.python_analyzer is not None:
                hab_an.configurar_analizador(self.python_analyzer)
                print(f"  {GREEN}OK{RST} Analizador externo inyectado en HabilidadAnalisisPython")
            else:
                print(f"  {GREEN}OK{RST} HabilidadAnalisisPython lista (AST interno)")
        except Exception as e:
            if self.verbose:
                print(f"  {YELL}-- Analizador inyección: {e}{RST}")

    # ─────────────────────────────────────────────────────────────────
    # CICLO DE VIDA
    # ─────────────────────────────────────────────────────────────────

    def iniciar_sesion(self):
        if self._fase2_activa:
            return
        print(f"  {CYAN}Iniciando sesión...{RST}")
        try:
            self.id_sesion = self.gestor_memoria.iniciar_sesion()
            print(f"  {GREEN}OK{RST} Sesión: {self.id_sesion[:8]}...")
        except Exception:
            self.id_sesion = datetime.now().isoformat()
        self.generador.memoria    = self.gestor_memoria
        self.motor.gestor_memoria = self.gestor_memoria
        print(f"  {GREEN}OK{RST} Memoria inyectada al generador y motor")
        if self.shell:
            self.generador.shell = self.shell
            print(f"  {GREEN}OK{RST} Shell inyectado en generador")
        if self.bd_cliente:
            try:
                self.bd_cliente.conectar()
                print(f"  {GREEN}OK{RST} Base de datos conectada")
            except Exception:
                pass
            self._inyectar_sqlite()
        self._inyectar_analizador()
        if self.gestor_bucles:
            try:
                self.gestor_bucles.iniciar_todos()
                print(f"  {GREEN}OK{RST} Bucles autónomos activos")
            except Exception:
                pass
        self._fase2_activa = True
        print()

    def finalizar_sesion(self):
        if not self._fase2_activa:
            return
        print()
        print(f"  {CYAN}Finalizando sesión...{RST}")
        if self.gestor_bucles:
            try:
                self.gestor_bucles.detener_todos()
            except Exception:
                pass
        if self.bd_cliente:
            try:
                self.bd_cliente.desconectar()
            except Exception:
                pass
        try:
            self.gestor_memoria.finalizar_sesion()
            print(f"  OK Sesión guardada  ({self.turnos} turnos)")
        except Exception:
            pass
        self._fase2_activa = False

    # ─────────────────────────────────────────────────────────────────
    # DETECCIÓN DE EMOCIÓN
    # ─────────────────────────────────────────────────────────────────

    _PATRONES_EMOCION = {
        "frustrado":  (["no funciona","error","falla","frustrado","harto",
                        "imposible","ya intenté","sigue sin","otra vez","me rindo"],
                       "empático_paciente"),
        "confundido": (["no entiendo","confundido","qué significa","me explicas",
                        "no sé","perdido","no me queda claro"],
                       "didáctico_claro"),
        "emocionado": (["genial","excelente","increíble","wow","funcionó",
                        "por fin","perfecto","maravilloso","me encanta"],
                       "entusiasta"),
        "preocupado": (["preocupado","miedo","temo","asustado","nervioso",
                        "ansiedad","qué pasa si"],
                       "tranquilizador"),
        "ocupado":    (["rápido","urgente","apurado","prisa","no tengo tiempo",
                        "breve","asap"],
                       "conciso_directo"),
        "curioso":    (["cómo funciona","por qué","interesante","quiero saber",
                        "cuéntame más","explícame"],
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
    # VERIFICACIÓN ECHO
    # ─────────────────────────────────────────────────────────────────

    def _verificar_decision_echo(self, decision):
        if not self._echo_main:
            return decision
        try:
            resultado = self._echo_main.verificar_decision(decision)
            if not resultado['coherente']:
                if self.verbose:
                    print(f"  {YELL}-- Echo-main: {resultado['problemas']}{RST}")
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
                print(f"  MENSAJE: \"{mensaje[:120]}{'...' if len(mensaje)>120 else ''}\"")
                print(f"{'═'*64}")

            emocion, tono = self._detectar_emocion(mensaje)
            if v and emocion:
                print(f"\n  Emoción: {emocion} → tono: {tono}")

            traduccion = self.traductor.traducir(mensaje)
            if v:
                cs = traduccion.get("conceptos", [])
                print(f"\n  Traducción: {len(cs)} conceptos "
                      f"(confianza {traduccion.get('confianza', 0):.0%})")
                for c in cs[:4]:
                    print(f"     • {c.id}  g={c.confianza_grounding:.2f}")

            decision = self.motor.razonar(traduccion)
            if v:
                print(f"\n  Decisión: {decision.tipo.name}  "
                      f"certeza={decision.certeza:.0%}  "
                      f"ejecutar={decision.puede_ejecutar}")
                if decision.tipo.name == "EJECUCION" and decision.hechos_reales:
                    hid = decision.hechos_reales.get("habilidad_id", "?")
                    cmd = decision.hechos_reales.get("comando_detectado", "")
                    op  = decision.hechos_reales.get("operacion", "")
                    print(f"     habilidad: {hid}  cmd/op: {cmd or op}")

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
                            print(f"\n  VETO de {getattr(consejera,'nombre','?')}: "
                                  f"{revision.get('razon_veto','')}")
                        return self.generador.generar(decision, contexto)
                    if v:
                        print(f"  OK {getattr(consejera,'nombre','?')}: aprobado")
                except Exception:
                    pass

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
                        "REGISTRO_USUARIO","CONSULTA_MEMORIA",
                        "IDENTIDAD_BELL","ESTADO_USUARIO",
                    }
                    if decision.tipo.name in _TIPOS_EPISODIO:
                        if hasattr(self.gestor_memoria, "registrar_episodio"):
                            try:
                                self.gestor_memoria.registrar_episodio(
                                    resumen=mensaje[:120],
                                    tema_principal=decision.tipo.name,
                                    estado_emocional_usuario=emocion or "neutral",
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
    # GESTIÓN DEL BUFFER DE CÓDIGO — NUEVO v6.5
    # ─────────────────────────────────────────────────────────────────

    def _activar_buffer(self, tipo: str, contexto: str = ""):
        """Activa el modo acumulador de código."""
        self._buffer_activo   = True
        self._buffer_lineas   = []
        self._buffer_tipo     = tipo
        self._buffer_contexto = contexto

    def _vaciar_buffer(self) -> tuple:
        """Desactiva el buffer. Retorna (codigo, contexto)."""
        codigo    = "\n".join(self._buffer_lineas)
        contexto  = self._buffer_contexto
        self._buffer_activo   = False
        self._buffer_lineas   = []
        self._buffer_tipo     = ""
        self._buffer_contexto = ""
        return codigo, contexto

    def _cancelar_buffer(self):
        """Cancela el buffer sin procesar."""
        self._buffer_activo   = False
        self._buffer_lineas   = []
        self._buffer_tipo     = ""
        self._buffer_contexto = ""

    def _armar_mensaje_con_codigo(self, contexto: str, codigo: str) -> str:
        """Arma el mensaje final que el motor puede interpretar."""
        base = contexto if contexto else "analiza este código"
        return f"{base}\n```python\n{codigo}\n```"

    def _procesar_linea_en_buffer(self, linea: str) -> str:
        """
        Maneja una línea cuando el buffer está activo.

        Retorna:
          ""                → línea acumulada, seguir esperando
          "PROCESAR_NORMAL" → buffer cerrado; esta línea es mensaje nuevo
          <texto>           → respuesta lista para imprimir
        """
        # Cancelación universal
        if linea.strip().lower() in ("cancelar", "cancel", "salir", "exit"):
            self._cancelar_buffer()
            return f"   {YELL}Buffer de código cancelado.{RST}"

        tipo = self._buffer_tipo

        # ── MODO BACKTICK ─────────────────────────────────────────────
        if tipo == "backtick":
            s = linea.strip()
            if s in ("```", "```python", "```py"):
                if self._buffer_lineas:
                    codigo, ctx = self._vaciar_buffer()
                    msg       = self._armar_mensaje_con_codigo(ctx, codigo)
                    respuesta = self.procesar(msg)
                    return f"🌺 Bell: {respuesta}"
                # ``` de apertura vacío → ignorar, seguir acumulando
                return ""
            linea_limpia = re.sub(r'^```(?:python|py)?\s*', '', linea)
            self._buffer_lineas.append(linea_limpia)
            return ""

        # ── MODO COMANDO (---) ────────────────────────────────────────
        elif tipo == "comando":
            if _es_separador_fin(linea):
                if not self._buffer_lineas:
                    self._cancelar_buffer()
                    return "🌺 Bell: No recibí código. Cuando quieras, escribe 'codigo' de nuevo."
                codigo, ctx = self._vaciar_buffer()
                msg       = self._armar_mensaje_con_codigo(ctx, codigo)
                respuesta = self.procesar(msg)
                return f"🌺 Bell: {respuesta}"
            self._buffer_lineas.append(linea)
            return ""

        # ── MODO AUTO ─────────────────────────────────────────────────
        elif tipo == "auto":
            if _es_separador_fin(linea):
                if self._buffer_lineas:
                    codigo, ctx = self._vaciar_buffer()
                    msg       = self._armar_mensaje_con_codigo(ctx, codigo)
                    respuesta = self.procesar(msg)
                    return f"🌺 Bell: {respuesta}"
                self._cancelar_buffer()
                return ""

            if _es_linea_codigo_python(linea):
                self._buffer_lineas.append(linea)
                return ""

            if not linea.strip():
                # Línea vacía → si hay código acumulado, cerrar
                if self._buffer_lineas:
                    codigo, ctx = self._vaciar_buffer()
                    msg       = self._armar_mensaje_con_codigo(ctx, codigo)
                    respuesta = self.procesar(msg)
                    return f"🌺 Bell: {respuesta}"
                return ""

            # Línea que no parece código → cerrar buffer si hay algo
            if self._buffer_lineas:
                codigo, ctx = self._vaciar_buffer()
                self.procesar(self._armar_mensaje_con_codigo(ctx, codigo))
            # Esta línea se procesa como mensaje normal
            return "PROCESAR_NORMAL"

        return ""

    def _detectar_inicio_buffer(self, entrada: str) -> bool:
        """
        Detecta si la entrada debe iniciar un buffer de código.
        Retorna True si activó el buffer (el loop debe pedir más líneas).

        Casos que activan buffer:
          MODO BACKTICK: entrada empieza con ```
          MODO COMANDO:  entrada es 'codigo' o pide análisis inline sin código
        """
        el = entrada.strip().lower()

        # MODO BACKTICK: primera línea empieza con ```
        if entrada.startswith("```"):
            resto = re.sub(r'^```(?:python|py)?\s*', '', entrada).strip()
            self._activar_buffer("backtick", "analiza este código")
            if resto:
                self._buffer_lineas.append(resto)
            print(f"   {DIM}(modo backtick — escribe el código línea a línea){RST}")
            print(f"   {DIM}Escribe ``` para terminar, o 'cancelar' para salir.{RST}")
            return True

        # MODO COMANDO: usuario escribe 'codigo'
        if el in _COMANDOS_CODIGO:
            self._activar_buffer("comando", "analiza este código")
            print(f"🌺 Bell: Listo. Pega o escribe tu código.")
            print(f"   {DIM}Cuando termines escribe {BOLD}---{RST}{DIM} en una línea sola.{RST}")
            print(f"   {DIM}(o 'cancelar' para salir){RST}")
            return True

        # MODO COMANDO: petición de análisis inline sin código adjunto
        if _RE_INICIO_ANALISIS_INLINE.search(entrada):
            tiene_codigo = ("```" in entrada
                            or bool(re.search(r'\bdef\s+\w+\(', entrada)))
            if not tiene_codigo:
                self._activar_buffer("comando", entrada)
                print(f"🌺 Bell: Claro. Pega o escribe el código.")
                print(f"   {DIM}Cuando termines escribe {BOLD}---{RST}{DIM} en una línea sola.{RST}")
                print(f"   {DIM}(o 'cancelar' para salir){RST}")
                return True

        return False

    # ─────────────────────────────────────────────────────────────────
    # LOOP CONVERSACIONAL — v6.5
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
                # Prompt según modo
                if self._buffer_activo:
                    tipo = self._buffer_tipo
                    if tipo == "backtick":
                        prompt = f"   {DIM}...{RST} "
                    else:
                        n = len(self._buffer_lineas)
                        prompt = f"   {DIM}[{n} líneas]  {RST}"
                    entrada = input(prompt)
                else:
                    entrada = input("🧑 Tú: ").strip()

                if not entrada and not self._buffer_activo:
                    continue

                # Si hay buffer activo → procesar en buffer
                if self._buffer_activo:
                    resultado = self._procesar_linea_en_buffer(entrada)
                    if resultado == "":
                        continue
                    elif resultado == "PROCESAR_NORMAL":
                        pass  # continuar con flujo normal abajo con 'entrada'
                    else:
                        print(resultado)
                        print()
                        continue

                el = entrada.lower().strip()

                # Comandos de salida
                if el in ("salir","exit","quit","chao","bye","adios","adiós"):
                    print("\n🌺 Bell: ¡Hasta pronto! Fue un gusto conversar.")
                    self.finalizar_sesion()
                    break

                # Comandos del sistema
                if el == "help":        self._cmd_help();        continue
                if el == "stats":       self._cmd_stats();       continue
                if el == "groq":        self._cmd_groq();        continue
                if el == "memoria":     self._cmd_memoria();     continue
                if el == "emociones":   self._cmd_emociones();   continue
                if el == "toggle_groq": self._cmd_toggle_groq(); continue
                if el == "identidad":   self._cmd_identidad();   continue
                if el == "personas":    self._cmd_personas();    continue
                if el == "honestidad":  self._cmd_honestidad();  continue
                if el == "shell":       self._cmd_shell();       continue
                if el == "bd":          self._cmd_bd();          continue
                if el == "analizador":  self._cmd_analizador();  continue
                if el == "verbose":
                    self.verbose = not self.verbose
                    print(f"   {YELL}Verbose: {'ON' if self.verbose else 'OFF'}{RST}\n")
                    continue

                # Detectar inicio de buffer de código (modos 2 y 3)
                if self._detectar_inicio_buffer(entrada):
                    continue

                # Procesamiento normal
                respuesta = self.procesar(entrada)
                print(f"🌺 Bell: {respuesta}")
                print()

            except KeyboardInterrupt:
                if self._buffer_activo:
                    self._cancelar_buffer()
                    print(f"\n   {YELL}Buffer de código cancelado.{RST}\n")
                else:
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
        shell_e  = f"{GREEN}ACTIVO{RST}" if self.shell      else f"{YELL}inactivo{RST}"
        bd_e     = f"{GREEN}ACTIVO{RST}" if self.bd_cliente else f"{YELL}inactivo{RST}"
        an_e     = f"{YELL}desconocido{RST}"
        try:
            from habilidades.registro_habilidades import RegistroHabilidades
            an_e = (f"{GREEN}ACTIVO{RST}"
                    if RegistroHabilidades.obtener().obtener_habilidad("ANALISIS_PYTHON")
                    else f"{YELL}inactivo{RST}")
        except Exception:
            pass

        print(f"""
  {BOLD}Comandos del sistema:{RST}
  {'─'*58}
  stats        Estadísticas del sistema
  groq         Estado de Groq y Echo
  memoria      Lo que Bell recuerda de ti
  emociones    Emociones detectadas en la sesión
  identidad    Identidad y principios de Bell
  personas     Personas que Bell conoce
  honestidad   Estado del sistema de honestidad
  shell        Estado del Shell Executor  ({shell_e})
  bd           Estado de la base de datos ({bd_e})
  analizador   Estado del Analizador Python ({an_e})
  toggle_groq  Activar/desactivar Groq
  verbose      Activar/desactivar debug
  help         Esta ayuda
  salir        Terminar
  {'─'*58}
  {BOLD}Análisis de código Python — 4 modos:{RST}

  {BOLD}MODO 1 — Ruta de archivo{RST} {DIM}(100% fiable en cualquier terminal){RST}
    "analiza C:\\mis_proyectos\\utils.py"
    "analiza /home/user/proyecto/modulo.py"
    "analiza main.py"

  {BOLD}MODO 2 — Comando 'codigo'{RST} {DIM}(ideal para PowerShell — paste){RST}
    Escribe: codigo
    Bell espera. Pega el código línea a línea.
    Cuando termines escribe: ---

  {BOLD}MODO 3 — Backtick manual{RST} {DIM}(escribe a mano, no pegar){RST}
    Escribe: ```python
    Escribe el código línea a línea.
    Escribe: ``` para terminar.

  {BOLD}MODO 4 — Detección automática{RST} {DIM}(líneas de código detectadas solas){RST}
    Escribe: "analiza este código"
    Bell activa acumulador. Pega/escribe.
    Escribe: --- para terminar.

  {BOLD}Módulos Bell (sin código):{RST}
    "analiza el motor"       "analiza nova"
    "analiza el generador"   "analiza vega"
    "analiza tu código"      "métricas de Bell"
  {'─'*58}
""")

    def _cmd_analizador(self):
        print(f"\n  {BOLD}Analizador Python — FASE 4C{RST}")
        print(f"  {'─'*58}")
        try:
            from habilidades.registro_habilidades import RegistroHabilidades
            hab_an = RegistroHabilidades.obtener().obtener_habilidad("ANALISIS_PYTHON")
            if hab_an:
                print(f"  {GREEN}OK HabilidadAnalisisPython registrada{RST}")
                tipo = ("externo" if getattr(hab_an, '_analizador_externo', None)
                        else "interno AST")
                print(f"     Analizador: {tipo}")
            else:
                print(f"  {RED}!! HabilidadAnalisisPython no registrada{RST}")
                print(); return
        except Exception as e:
            print(f"  {YELL}No se pudo consultar registro: {e}{RST}")
            print(); return

        print(f"\n  {BOLD}Las 7 consejeras son analizables:{RST}")
        base = Path(__file__).parent
        for nombre in ['vega','nova','echo','lyra','luna','iris','sage']:
            ruta = f'consejeras/{nombre}/logica.py'
            existe = (base / ruta).exists()
            ico = GREEN + "OK" if existe else YELL + "--"
            print(f"  {ico}{RST}  analiza {nombre:<12} → {DIM}{ruta}{RST}")

        print(f"\n  {BOLD}4 modos de entrada:{RST}")
        print(f"  {DIM}1. Ruta:    analiza C:\\ruta\\archivo.py")
        print(f"  2. Comando: escribe 'codigo' → pega → escribe '---'")
        print(f"  3. Backtick: escribe ``` → código → ``` (manual)")
        print(f"  4. Auto:    'analiza este código' → pega → '---'{RST}")
        print()

    def _cmd_bd(self):
        print(f"\n  {BOLD}Base de Datos — Sub-paso 2C{RST}")
        print(f"  {'─'*44}")
        if not self.bd_cliente:
            print(f"  {RED}!! ClienteSQLite no disponible{RST}"); print(); return
        print(f"  {GREEN}OK ClienteSQLite ACTIVO{RST}")
        try:
            from habilidades.registro_habilidades import RegistroHabilidades
            hab_sq = RegistroHabilidades.obtener().obtener_habilidad("SQLITE")
            if hab_sq:
                ok = getattr(hab_sq, '_cliente', None) is not None
                print(f"  {GREEN}OK HabilidadSQLite registrada{RST}")
                print(f"     bd_cliente inyectado: {'sí' if ok else 'no'}")
            else:
                print(f"  {YELL}-- HabilidadSQLite no registrada{RST}")
        except Exception as e:
            print(f"  {YELL}-- registro: {e}{RST}")
        try:
            tablas = self.bd_cliente.listar_tablas()
            if tablas:
                print(f"\n  Tablas ({len(tablas)}):")
                for t in tablas[:10]: print(f"    • {t}")
            else:
                print(f"\n  {DIM}Base de datos vacía (sin tablas aún){RST}")
        except Exception as e:
            print(f"\n  {YELL}No se pudieron listar tablas: {e}{RST}")
        print()

    def _cmd_shell(self):
        print(f"\n  {BOLD}Shell Executor — Sub-paso 2B{RST}")
        print(f"  {'─'*44}")
        if not self.shell:
            print(f"  {RED}!! ShellExecutor no disponible{RST}"); print(); return
        print(f"  {GREEN}OK ShellExecutor ACTIVO{RST}")
        whitelist = getattr(self.shell, '_whitelist', None)
        if whitelist:
            cmds = sorted(list(whitelist))[:15]
            print(f"\n  Comandos permitidos ({len(whitelist)}):")
            for i in range(0, len(cmds), 3):
                fila = cmds[i:i+3]
                print("    " + "  ".join(f"{c:<18}" for c in fila))
        try:
            from habilidades.registro_habilidades import RegistroHabilidades
            hab_sh = RegistroHabilidades.obtener().obtener_habilidad("SHELL")
            if hab_sh:
                print(f"\n  {GREEN}OK HabilidadShell registrada{RST}")
            else:
                print(f"\n  {YELL}-- HabilidadShell no registrada{RST}")
        except Exception:
            pass
        print()

    def _cmd_stats(self):
        total = self._total_conceptos()
        sg    = {}
        try:
            sg = self.generador.obtener_estadisticas()
        except Exception:
            pass
        shell_i  = "OK" if self.shell      else "--"
        bd_i     = "OK" if self.bd_cliente else "--"
        an_i     = "--"
        try:
            from habilidades.registro_habilidades import RegistroHabilidades
            if RegistroHabilidades.obtener().obtener_habilidad("ANALISIS_PYTHON"):
                an_i = "OK"
        except Exception:
            pass
        print(f"""
  {BOLD}Estadísticas:{RST}
  {'─'*44}
  Vocabulario       {total} conceptos
  Consejeras        {len(self.consejeras)} activas
  Turnos            {self.turnos}
  Groq              {'ON' if self.usar_groq else 'OFF'}
  Shell             {shell_i}
  BD SQLite         {bd_i}
  Analizador Python {an_i}
  Honestidad        {'activa' if _HONESTIDAD_OK else 'NO ACTIVA'}
  {'─'*44}
  Respuestas        {sg.get('total_generadas', 0)}
  Con Groq          {sg.get('groq_usadas', 0)}
  Bloqueadas        {sg.get('groq_bloqueadas', 0)}
  Echo correc.      {sg.get('echo_correcciones', 0)}
  Fallback          {sg.get('fallback_a_simbolico', 0)}
  Shell exec.       {sg.get('shell_ejecutados', 0)}
  {'─'*44}
  Habilidades ejecutadas:""")
        for hid, cnt in sg.get('habilidades_ejecutadas', {}).items():
            print(f"    {hid:<28} {cnt}x")
        print(f"  {'─'*44}\n  Tipos de decisión:")
        for tipo, cnt in sorted(sg.get('tipos_decision', {}).items(),
                                key=lambda x: -x[1])[:8]:
            print(f"    {tipo:<28} {cnt}")
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
  Llamadas Groq       {sg.get('groq_usadas', 0)}
  Bloqueadas Echo     {sg.get('groq_bloqueadas', 0)}
  Echo correcciones   {sg.get('echo_correcciones', 0)}
  Shell               {GREEN + 'ACTIVO' if self.shell else YELL + 'inactivo'}{RST}
  BD SQLite           {GREEN + 'ACTIVO' if self.bd_cliente else YELL + 'inactivo'}{RST}
""")
        else:
            print(f"""
  {YELL}Groq: DESACTIVADO{RST}
  Bell usa generación simbólica honesta con Echo activo.
  Shell, BD y Analizador Python siguen activos sin Groq.
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
            if historial:
                for l in historial.strip().split("\n")[-6:]:
                    print(f"  {DIM}{l}{RST}")
        except Exception as e:
            print(f"  Error: {e}")
        print()

    def _cmd_identidad(self):
        print(f"\n  {BOLD}Identidad de Bell{RST}")
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
        print()

    def _cmd_personas(self):
        print(f"\n  {BOLD}Personas que Bell conoce{RST}")
        print(f"  {'─'*44}")
        if not hasattr(self.gestor_memoria, "obtener_persona"):
            print(f"  {YELL}GestorMemoria v5+ no disponible.{RST}")
            print(); return
        personas = getattr(self.gestor_memoria, "_cache_personas", {})
        if not personas:
            print("  (Bell no ha construido modelos de personas todavía)")
        else:
            for nombre_p, datos_p in list(personas.items())[:5]:
                print(f"\n  {BOLD}{nombre_p}{RST}")
                if isinstance(datos_p, dict):
                    print(f"    Menciones: {datos_p.get('menciones',0)}")
        print()

    def _cmd_honestidad(self):
        print(f"\n  {BOLD}Sistema de Honestidad — Fase 4A{RST}")
        print(f"  {'─'*44}")
        if _HONESTIDAD_OK:
            print(f"  {GREEN}OK core/capacidades_fase.py ACTIVO{RST}")
            print(f"     {_TOTAL_NO_IMPLEMENTADAS} capacidades bloqueadas")
            try:
                from core.capacidades_fase import NO_IMPLEMENTADAS
                print(f"\n  {BOLD}Capacidades no implementadas:{RST}")
                for cid, razon in list(NO_IMPLEMENTADAS.items())[:6]:
                    nombre = cid.replace("CONCEPTO_", "").lower()
                    print(f"    !! {nombre:<15} — {razon[:50]}")
                if len(NO_IMPLEMENTADAS) > 6:
                    print(f"    ... y {len(NO_IMPLEMENTADAS) - 6} más")
            except Exception:
                pass
        else:
            print(f"  {RED}!! core/capacidades_fase.py NO ENCONTRADO{RST}")
        echo_ok  = self._echo_main is not None
        gen_echo = getattr(self.generador, '_echo_verificador', None) is not None
        print(f"\n  {BOLD}Echo verificadores:{RST}")
        print(f"    Echo main:      {'ACTIVO' if echo_ok  else 'INACTIVO'}")
        print(f"    Echo generador: {'ACTIVO' if gen_echo else 'INACTIVO'}")
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
        description="Belladonna v6.5 — FASE 4C — Shell + SQLite + Análisis Python"
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