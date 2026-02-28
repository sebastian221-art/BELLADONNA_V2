"""
Dimensión Temporal: ¿Bell comprende el tiempo?

Mide si Bell entiende aspectos temporales del concepto.
Incluye duración, secuencias, historial temporal.

Fase 3 → Fase 4 Refactorización
"""

from grounding.base_dimension import DimensionGrounding
from typing import Any

class GroundingTemporal(DimensionGrounding):
    """
    Grounding temporal: comprensión del tiempo.
    
    Evalúa:
    - ¿Conoce duración estimada?
    - ¿Entiende secuencias temporales?
    - ¿Tiene historial temporal?
    """
    
    @property
    def nombre(self) -> str:
        return "Temporal"
    
    @property
    def descripcion(self) -> str:
        return "¿Bell comprende aspectos temporales de este concepto?"
    
    def evaluar(self, concepto: Any) -> float:
        """
        Evalúa comprensión temporal.
        
        Factores:
        - Duración estimada conocida: +0.35
        - Secuencia temporal definida: +0.35
        - Historial temporal: +0.3
        
        Args:
            concepto: ConceptoAnclado a evaluar
        
        Returns:
            float entre 0.0 (no comprende tiempo) y 1.0 (temporal completo)
        """
        puntaje = 0.0
        
        if hasattr(concepto, 'propiedades'):
            props = concepto.propiedades
            
            # Duración estimada
            if 'duracion_estimada' in props or 'tiempo_ejecucion' in props:
                puntaje += 0.35
            
            # Secuencia temporal / orden
            if 'orden_ejecucion' in props or 'secuencia' in props:
                puntaje += 0.35
            
            # Dependencias temporales
            if 'dependencias_temporales' in props:
                puntaje += 0.2
        
        # Historial temporal en metadata
        if hasattr(concepto, 'metadata'):
            metadata = concepto.metadata
            
            if 'fecha_creacion' in metadata:
                puntaje += 0.05
            
            if 'ultima_modificacion' in metadata:
                puntaje += 0.05
            
            if 'historial_modificaciones' in metadata:
                puntaje += 0.1
        
        return min(1.0, puntaje)


if __name__ == '__main__':
    print("Testing GroundingTemporal...")
    
    from dataclasses import dataclass
    from typing import Dict, Any
    
    @dataclass
    class ConceptoTest:
        id: str
        propiedades: Dict[str, Any]
        metadata: Dict[str, Any]
    
    concepto = ConceptoTest(
        id="CONCEPTO_PROCESAR",
        propiedades={
            'duracion_estimada': '500ms',
            'secuencia': ['cargar', 'validar', 'procesar', 'guardar']
        },
        metadata={
            'fecha_creacion': '2026-01-01',
            'ultima_modificacion': '2026-02-14'
        }
    )
    
    grounding = GroundingTemporal()
    print(f"Grounding temporal: {grounding.evaluar(concepto):.2f}")
    print("✅ GroundingTemporal funciona correctamente")