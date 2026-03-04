"""
tipos_decision.py — VERSION v6

CAMBIOS v6 sobre v5:
    Sin cambios en TipoDecision ni Decision — compatibilidad 100%.

    ACTUALIZADO: TIPOS_CONVERSACIONALES
        Se agrega "DESCONOCIDO" explícitamente (ya estaba implícito
        en el generador pero no en el set exportable).

    ACTUALIZADO: TIPOS_GUARDAN_EN_MEMORIA
        Sin cambios — solo REGISTRO_USUARIO guarda en memoria
        desde el motor. Los demás tipos lo hacen en el generador.

    NOTA: tipos_decision.py es intencionalmente estable.
    Los cambios de comportamiento de v6 están en motor_razonamiento.py.
    Este archivo solo exporta sets que otros módulos consumen.

COMPATIBILIDAD: 100% con v5 y v4.
"""
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, FrozenSet


class TipoDecision(Enum):
    """Tipos de decisiones que Bell puede generar."""

    # ═══════════════════════════════════════════════════════════════
    # EXISTENTES — NO TOCAR (v1 original)
    # ═══════════════════════════════════════════════════════════════
    AFIRMATIVA = auto()           # "Sí, puedo hacer X"
    NEGATIVA = auto()             # "No, no puedo hacer X"
    PARCIAL = auto()              # "Puedo hacer parte de X"
    NECESITA_ACLARACION = auto()  # "¿Podrías ser más específico?"
    NO_ENTENDIDO = auto()         # "No entendí la pregunta"
    SALUDO = auto()               # Respuesta a saludo
    AGRADECIMIENTO = auto()       # Respuesta a gracias

    IDENTIDAD_BELL = auto()       # "quién eres", "cómo te llamas"
    ESTADO_BELL = auto()          # "cómo estás", "todo bien?"
    CAPACIDAD_BELL = auto()       # "qué puedes hacer", "puedes leer archivos?"
    SOCIAL = auto()               # "hola", "gracias", "adiós"
    ESTADO_USUARIO = auto()       # "estoy frustrado", "no entiendo"
    ACCION_COGNITIVA = auto()     # "explícame", "resume esto"
    CONFIRMACION = auto()         # "sí", "no", "ok"
    DESCONOCIDO = auto()          # no se pudo clasificar

    # ═══════════════════════════════════════════════════════════════
    # MEGA PAQUETE A
    # ═══════════════════════════════════════════════════════════════
    TEMPORAL = auto()             # "antes dijiste", "hace rato mencionaste"
    CUANTIFICACION = auto()       # "cuántos", "todos", "primero"

    # ═══════════════════════════════════════════════════════════════
    # v4 — Los 5 tipos nuevos
    # ═══════════════════════════════════════════════════════════════

    REGISTRO_USUARIO = auto()
    """
    El usuario comparte información personal sobre sí mismo.
    Ejemplos: "me llamo Juan", "tengo 25 años", "soy desarrollador".
    Acción: registrar en memoria Y confirmar al usuario.
    Motor guarda en memoria INMEDIATAMENTE (no espera al generador).
    NO confundir con IDENTIDAD_BELL (que es sobre Bell, no el usuario).
    """

    CONSULTA_MEMORIA = auto()
    """
    El usuario pregunta sobre datos que ya compartió.
    Ejemplos: "cómo me llamo", "cuántos años tengo", "sabes mi nombre".
    v6: también captura "sabes X", "recuerdas X".
    Acción: consultar memoria → responder con el dato guardado.
    Si no hay dato: admitir honestamente.
    """

    VERIFICACION_LOGICA = auto()
    """
    El usuario presenta una afirmación para que Bell la verifique.
    Ejemplos: "el cielo es verde verdad", "2+2=5 no".
    Acción: verificar y responder con certeza.
    """

    CALCULO = auto()
    """
    El usuario pide una operación matemática.
    Ejemplos: "cuánto es 7 por 8", "cuánto es 100 dividido 4".
    Acción: calcular y dar el resultado exacto.
    puede_ejecutar=True — Bell usa Python para esto.
    """

    CONOCIMIENTO_GENERAL = auto()
    """
    El usuario pregunta sobre hechos del mundo fuera del grounding de Bell.
    Ejemplos: "cuál es la capital de Francia", "cuándo nació Einstein".
    Acción: responder con honestidad sobre qué sabe y qué no.
    """


# ═══════════════════════════════════════════════════════════════════════
# SETS EXPORTABLES
# ═══════════════════════════════════════════════════════════════════════

# Tipos que van por la ruta conversacional
# generador_salida.py importa este set en lugar de mantener
# su propia copia que no incluía los tipos nuevos de v4.
TIPOS_CONVERSACIONALES: FrozenSet[str] = frozenset({
    # Existentes
    "IDENTIDAD_BELL",
    "ESTADO_BELL",
    "CAPACIDAD_BELL",
    "SOCIAL",
    "ESTADO_USUARIO",
    "ACCION_COGNITIVA",
    "TEMPORAL",
    "CUANTIFICACION",
    "CONFIRMACION",
    "DESCONOCIDO",
    # v4 — faltaban en la versión interna de generador_salida.py
    "REGISTRO_USUARIO",
    "CONSULTA_MEMORIA",
    "VERIFICACION_LOGICA",
    "CALCULO",
    "CONOCIMIENTO_GENERAL",
})

# Tipos que requieren guardar datos en memoria DESDE EL MOTOR
# (no esperar al generador)
TIPOS_GUARDAN_EN_MEMORIA: FrozenSet[str] = frozenset({
    "REGISTRO_USUARIO",
})

# Tipos que actualizan el estado de sesión en memoria
TIPOS_ACTUALIZAN_ESTADO: FrozenSet[str] = frozenset({
    "SOCIAL",
    "ESTADO_USUARIO",
    "REGISTRO_USUARIO",
    "CONSULTA_MEMORIA",
    "IDENTIDAD_BELL",
    "ESTADO_BELL",
    "CAPACIDAD_BELL",
    "ACCION_COGNITIVA",
    "CONFIRMACION",
    "TEMPORAL",
    "CUANTIFICACION",
    "VERIFICACION_LOGICA",
    "CALCULO",
    "CONOCIMIENTO_GENERAL",
    "DESCONOCIDO",
})


class RazonRechazo(Enum):
    """Razones por las que Bell rechaza una acción."""
    SIN_GROUNDING = auto()
    SIN_OPERACION = auto()
    VEGA_VETO     = auto()
    AMBIGUO       = auto()
    DESCONOCIDO   = auto()


@dataclass
class Decision:
    """
    Resultado del razonamiento de Bell.
    Esta es la salida del Motor que luego se convierte en español.
    """

    # TIPO Y CERTEZA
    tipo:    TipoDecision
    certeza: float  # 0.0 - 1.0

    # CONCEPTOS INVOLUCRADOS
    conceptos_principales: List[str]
    conceptos_secundarios: List[str] = None

    # CAPACIDAD (si aplica)
    puede_ejecutar:       bool = False
    operacion_disponible: Optional[str] = None

    # RAZONAMIENTO
    razon:         str = ""
    razon_rechazo: Optional[RazonRechazo] = None

    # METADATA
    pasos_razonamiento: List[str] = None
    grounding_promedio: float     = 0.0

    # HECHOS REALES (para tipos conversacionales)
    hechos_reales: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if self.conceptos_secundarios is None:
            self.conceptos_secundarios = []
        if self.pasos_razonamiento is None:
            self.pasos_razonamiento = []
        if not 0.0 <= self.certeza <= 1.0:
            self.certeza = max(0.0, min(self.certeza, 1.0))

    def es_ejecutable(self) -> bool:
        return self.puede_ejecutar and self.operacion_disponible is not None

    def es_rechazo(self) -> bool:
        return self.tipo in [TipoDecision.NEGATIVA, TipoDecision.NO_ENTENDIDO]

    def es_conversacional(self) -> bool:
        """¿Este tipo de decisión va por la ruta conversacional?"""
        return self.tipo.name in TIPOS_CONVERSACIONALES

    def __repr__(self) -> str:
        return (
            f"Decision(tipo={self.tipo.name}, certeza={self.certeza:.2f}, "
            f"ejecutable={self.puede_ejecutar})"
        )






        