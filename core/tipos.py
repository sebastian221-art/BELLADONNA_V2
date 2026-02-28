"""
Tipos y enums fundamentales de Belladonna.
"""
from enum import Enum, auto

class TipoConcepto(Enum):
    """Categorías de conceptos que Bell puede manejar."""
    OPERACION_SISTEMA = auto()     # leer, escribir, ejecutar
    ENTIDAD_DIGITAL = auto()       # archivo, carpeta, proceso
    ACCION_COGNITIVA = auto()      # pensar, razonar, decidir
    PROPIEDAD = auto()             # tamaño, tipo, permiso
    CONCEPTO_ABSTRACTO = auto()    # certeza, confianza, razón
    PALABRA_CONVERSACION = auto()  # hola, ayuda, gracias

class NivelGrounding(Enum):
    """Nivel de anclaje a realidad ejecutable."""
    DIRECTO = 1.0          # Bell PUEDE ejecutar
    RELACIONAL = 0.8       # Bell PUEDE medir/detectar
    DATOS = 0.6            # Bell tiene indicadores
    CONCEPTUAL = 0.3       # Bell solo tiene definición
    DESCONOCIDO = 0.0      # Bell no sabe qué es