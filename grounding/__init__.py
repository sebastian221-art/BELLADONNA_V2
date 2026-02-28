"""
Módulo Grounding - Sistema de Grounding 9D para Belladonna

Este módulo coordina las 9 dimensiones de grounding:
1. Computacional - ¿Tiene código ejecutable?
2. Semántico - ¿Comprende el significado?
3. Contextual - ¿Sabe cuándo usarlo?
4. Pragmático - ¿Conoce efectos prácticos?
5. Social - ¿Entiende componente social?
6. Temporal - ¿Comprende el tiempo?
7. Causal - ¿Entiende causa-efecto?
8. Metacognitivo - ¿Puede razonar sobre sí mismo?
9. Predictivo - ¿Puede predecir resultados?

Uso básico:
    from grounding import GestorGrounding
    
    gestor = GestorGrounding()
    grounding_9d = gestor.evaluar_9d(concepto)
    
    print(grounding_9d)
    # {
    #     'computacional': 1.0,
    #     'semantico': 0.9,
    #     'contextual': 0.85,
    #     ...
    # }

Uso avanzado - Agregar dimensión personalizada:
    from grounding import GestorGrounding, DimensionGrounding
    
    class MiDimension(DimensionGrounding):
        @property
        def nombre(self):
            return "Mi Dimensión"
        
        @property
        def descripcion(self):
            return "Descripción de qué mide"
        
        def evaluar(self, concepto):
            # Tu lógica aquí
            return 0.8
    
    gestor = GestorGrounding()
    gestor.agregar_dimension('mi_dimension', MiDimension())
    
    # Ahora puedes evaluar con 10 dimensiones
    grounding_10d = gestor.evaluar_9d(concepto)
"""

# Imports principales
from grounding.gestor_grounding import GestorGrounding, crear_gestor
from grounding.base_dimension import DimensionGrounding

# Imports de dimensiones (opcional - para uso avanzado)
from grounding.dimensiones.computacional import GroundingComputacional
from grounding.dimensiones.semantico import GroundingSemantico
from grounding.dimensiones.contextual import GroundingContextual
from grounding.dimensiones.pragmatico import GroundingPragmatico
from grounding.dimensiones.social import GroundingSocial
from grounding.dimensiones.temporal import GroundingTemporal
from grounding.dimensiones.causal import GroundingCausal
from grounding.dimensiones.metacognitivo import GroundingMetacognitivo
from grounding.dimensiones.predictivo import GroundingPredictivo

# Metadata del módulo
__version__ = '1.0.0'
__author__ = 'Proyecto Belladonna'
__description__ = 'Sistema de Grounding 9D para conciencia artificial'

# Exports públicos (lo que se puede importar con 'from grounding import X')
__all__ = [
    # Principales
    'GestorGrounding',
    'DimensionGrounding',
    'crear_gestor',
    
    # Dimensiones individuales (uso avanzado)
    'GroundingComputacional',
    'GroundingSemantico',
    'GroundingContextual',
    'GroundingPragmatico',
    'GroundingSocial',
    'GroundingTemporal',
    'GroundingCausal',
    'GroundingMetacognitivo',
    'GroundingPredictivo'
]


def version():
    """Retorna versión del módulo."""
    return __version__


def ayuda():
    """Muestra ayuda rápida."""
    print(__doc__)