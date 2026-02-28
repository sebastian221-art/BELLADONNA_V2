"""
Tipos y Enums para el Sistema de Memoria.

Define los tipos de datos que se pueden guardar en memoria persistente.
"""
from enum import Enum
from typing import TypedDict, Any, Optional, List

class TipoMemoria(Enum):
    """Tipos de información que se pueden guardar."""
    CONCEPTO_USADO = "concepto_usado"
    DECISION = "decision"
    PATRON = "patron"
    INSIGHT = "insight"
    AJUSTE_GROUNDING = "ajuste_grounding"
    SESION = "sesion"
    ESTADISTICA = "estadistica"

class RegistroConcepto(TypedDict):
    """Registro de un concepto usado."""
    concepto_id: str
    timestamp: str
    veces_usado: int
    ultima_certeza: float

class RegistroDecision(TypedDict):
    """Registro de una decisión tomada."""
    timestamp: str
    tipo: str
    puede_ejecutar: bool
    certeza: float
    conceptos_principales: List[str]
    grounding_promedio: float

class RegistroPatron(TypedDict):
    """Registro de un patrón detectado."""
    timestamp: str
    tipo_patron: str
    descripcion: str
    frecuencia: int
    confianza: float

class RegistroInsight(TypedDict):
    """Registro de un insight generado."""
    timestamp: str
    tipo_insight: str
    descripcion: str
    relevancia: str
    datos: dict

class RegistroAjuste(TypedDict):
    """Registro de un ajuste de grounding."""
    timestamp: str
    concepto_id: str
    grounding_anterior: float
    grounding_nuevo: float
    razon: str
    aplicado: bool

class RegistroSesion(TypedDict):
    """Registro de una sesión de conversación."""
    id_sesion: str
    inicio: str
    fin: Optional[str]
    mensajes_procesados: int
    decisiones_tomadas: int
    conceptos_usados: int
    patrones_detectados: int