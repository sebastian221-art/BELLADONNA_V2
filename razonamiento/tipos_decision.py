"""
Tipos de Decisiones que Bell puede tomar.

Una Decision es la salida del Motor de Razonamiento.

MODIFICADO — Mega Paquete A:
- Agregados TEMPORAL y CUANTIFICACION al enum
"""
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Dict, Any, Optional


class TipoDecision(Enum):
    """Tipos de decisiones que Bell puede generar."""

    # ═══════════════════════════════════════════════════════════════
    # EXISTENTES — NO TOCAR
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
    # NUEVOS — Mega Paquete A
    # ═══════════════════════════════════════════════════════════════
    TEMPORAL = auto()             # "antes dijiste", "hace rato mencionaste"
    CUANTIFICACION = auto()       # "cuántos", "todos", "primero"


class RazonRechazo(Enum):
    """Razones por las que Bell rechaza una acción."""
    SIN_GROUNDING = auto()    # Grounding < umbral
    SIN_OPERACION = auto()    # No tiene operación ejecutable
    VEGA_VETO = auto()        # Vega bloqueó (Semana 4)
    AMBIGUO = auto()          # Muchas interpretaciones posibles
    DESCONOCIDO = auto()      # Palabras no reconocidas


@dataclass
class Decision:
    """
    Resultado del razonamiento de Bell.

    Esta es la salida del Motor que luego se convierte en español.
    """

    # TIPO Y CERTEZA
    tipo: TipoDecision
    certeza: float  # 0.0 - 1.0

    # CONCEPTOS INVOLUCRADOS
    conceptos_principales: List[str]   # IDs de conceptos clave
    conceptos_secundarios: List[str] = None  # IDs de conceptos relacionados

    # CAPACIDAD (si aplica)
    puede_ejecutar: bool = False
    operacion_disponible: Optional[str] = None  # Nombre de operación

    # RAZONAMIENTO
    razon: str = ""                              # Explicación textual
    razon_rechazo: Optional[RazonRechazo] = None # Si tipo=NEGATIVA

    # METADATA
    pasos_razonamiento: List[str] = None  # Traza de pensamiento
    grounding_promedio: float = 0.0

    # HECHOS REALES (para tipos conversacionales — Mega Paquete A)
    hechos_reales: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        """Validaciones."""
        if self.conceptos_secundarios is None:
            self.conceptos_secundarios = []
        if self.pasos_razonamiento is None:
            self.pasos_razonamiento = []
        if not 0.0 <= self.certeza <= 1.0:
            raise ValueError(f"Certeza debe estar entre 0.0 y 1.0: {self.certeza}")

    def es_ejecutable(self) -> bool:
        """¿Esta decisión implica una acción que Bell puede ejecutar?"""
        return self.puede_ejecutar and self.operacion_disponible is not None

    def es_rechazo(self) -> bool:
        """¿Esta decisión rechaza la petición?"""
        return self.tipo in [TipoDecision.NEGATIVA, TipoDecision.NO_ENTENDIDO]

    def __repr__(self) -> str:
        return (f"Decision(tipo={self.tipo.name}, certeza={self.certeza:.2f}, "
                f"ejecutable={self.puede_ejecutar})")