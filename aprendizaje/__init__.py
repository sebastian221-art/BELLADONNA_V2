"""
Paquete de Aprendizaje Básico - Fase 2.

Permite que Bell aprenda de su experiencia, ajustando el
grounding de conceptos y aplicando insights detectados.

Componentes:
- MotorAprendizaje: Coordinador principal
- AjustadorGrounding: Ajusta grounding de conceptos
- AplicadorInsights: Convierte insights en acciones
- Estrategias: Define cómo calcular ajustes
"""
from aprendizaje.motor_aprendizaje import MotorAprendizaje
from aprendizaje.ajustador_grounding import AjustadorGrounding
from aprendizaje.aplicador_insights import AplicadorInsights
from aprendizaje.estrategias import (
    EstrategiaAprendizaje,
    EstrategiaUsoFrecuente,
    EstrategiaExitoFallido,
    EstrategiaInsights,
    EstrategiaConservadora,
    EstrategiaComposite
)

__all__ = [
    'MotorAprendizaje',
    'AjustadorGrounding',
    'AplicadorInsights',
    'EstrategiaAprendizaje',
    'EstrategiaUsoFrecuente',
    'EstrategiaExitoFallido',
    'EstrategiaInsights',
    'EstrategiaConservadora',
    'EstrategiaComposite'
]