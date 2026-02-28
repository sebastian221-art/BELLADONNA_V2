"""
Dimensiones de Grounding - Sistema 9D.

Este módulo contiene las 9 dimensiones de grounding de Bell:

1. Computacional - ¿Tiene código ejecutable?
2. Semántico - ¿Comprende el significado?
3. Contextual - ¿Sabe cuándo usarlo?
4. Pragmático - ¿Conoce efectos prácticos?
5. Social - ¿Entiende componente social?
6. Temporal - ¿Comprende el tiempo?
7. Causal - ¿Entiende causa-efecto?
8. Metacognitivo - ¿Puede razonar sobre sí mismo?
9. Predictivo - ¿Puede predecir resultados?

Uso:
    from grounding.dimensiones import GroundingSemantico
    
    dimension = GroundingSemantico()
    puntaje = dimension.evaluar(concepto)

O importar todas:
    from grounding.dimensiones import *
"""

# Importar todas las dimensiones
from grounding.dimensiones.computacional import GroundingComputacional
from grounding.dimensiones.semantico import GroundingSemantico
from grounding.dimensiones.contextual import GroundingContextual
from grounding.dimensiones.pragmatico import GroundingPragmatico
from grounding.dimensiones.social import GroundingSocial
from grounding.dimensiones.temporal import GroundingTemporal
from grounding.dimensiones.causal import GroundingCausal
from grounding.dimensiones.metacognitivo import GroundingMetacognitivo
from grounding.dimensiones.predictivo import GroundingPredictivo

# Lista de todas las dimensiones (orden estándar)
DIMENSIONES_9D = [
    GroundingComputacional,
    GroundingSemantico,
    GroundingContextual,
    GroundingPragmatico,
    GroundingSocial,
    GroundingTemporal,
    GroundingCausal,
    GroundingMetacognitivo,
    GroundingPredictivo
]

# Mapeo nombre → clase
DIMENSIONES_POR_NOMBRE = {
    'computacional': GroundingComputacional,
    'semantico': GroundingSemantico,
    'contextual': GroundingContextual,
    'pragmatico': GroundingPragmatico,
    'social': GroundingSocial,
    'temporal': GroundingTemporal,
    'causal': GroundingCausal,
    'metacognitivo': GroundingMetacognitivo,
    'predictivo': GroundingPredictivo
}

# Exports públicos
__all__ = [
    # Clases de dimensiones
    'GroundingComputacional',
    'GroundingSemantico',
    'GroundingContextual',
    'GroundingPragmatico',
    'GroundingSocial',
    'GroundingTemporal',
    'GroundingCausal',
    'GroundingMetacognitivo',
    'GroundingPredictivo',
    
    # Listas auxiliares
    'DIMENSIONES_9D',
    'DIMENSIONES_POR_NOMBRE'
]


def listar_dimensiones():
    """
    Lista todas las dimensiones disponibles.
    
    Returns:
        Lista de nombres de dimensiones
    """
    return list(DIMENSIONES_POR_NOMBRE.keys())


def obtener_dimension(nombre: str):
    """
    Obtiene clase de dimensión por nombre.
    
    Args:
        nombre: Nombre de la dimensión ('computacional', 'semantico', etc.)
    
    Returns:
        Clase de la dimensión o None si no existe
    
    Ejemplo:
        >>> clase = obtener_dimension('semantico')
        >>> dimension = clase()
        >>> dimension.evaluar(concepto)
    """
    return DIMENSIONES_POR_NOMBRE.get(nombre.lower())


def crear_todas_dimensiones(vocabulario=None):
    """
    Crea instancias de todas las dimensiones.
    
    Args:
        vocabulario: GestorVocabulario (opcional, para semántico)
    
    Returns:
        Dict con {nombre: instancia} de todas las dimensiones
    
    Ejemplo:
        >>> dimensiones = crear_todas_dimensiones()
        >>> for nombre, dimension in dimensiones.items():
        ...     print(f"{nombre}: {dimension.evaluar(concepto)}")
    """
    return {
        'computacional': GroundingComputacional(),
        'semantico': GroundingSemantico(vocabulario),
        'contextual': GroundingContextual(),
        'pragmatico': GroundingPragmatico(),
        'social': GroundingSocial(),
        'temporal': GroundingTemporal(),
        'causal': GroundingCausal(),
        'metacognitivo': GroundingMetacognitivo(),
        'predictivo': GroundingPredictivo()
    }


if __name__ == '__main__':
    print("Dimensiones de Grounding disponibles:")
    print("="*60)
    
    for nombre in listar_dimensiones():
        clase = obtener_dimension(nombre)
        dimension = clase()
        print(f"  {dimension.nombre:15s} - {dimension.descripcion}")
    
    print("\n✅ 9 dimensiones cargadas correctamente")