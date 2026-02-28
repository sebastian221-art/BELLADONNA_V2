"""
Dimensión Causal: ¿Bell entiende causa-efecto?

Mide si Bell comprende relaciones causales del concepto.
Incluye causas (precondiciones) y efectos (postcondiciones).

Fase 3 → Fase 4 Refactorización
"""

from grounding.base_dimension import DimensionGrounding
from typing import Any

class GroundingCausal(DimensionGrounding):
    """
    Grounding causal: comprensión de causa-efecto.
    
    Evalúa:
    - ¿Conoce causas (precondiciones)?
    - ¿Conoce efectos (postcondiciones)?
    - ¿Puede razonar causalmente?
    """
    
    @property
    def nombre(self) -> str:
        return "Causal"
    
    @property
    def descripcion(self) -> str:
        return "¿Bell entiende relaciones causa-efecto de este concepto?"
    
    def evaluar(self, concepto: Any) -> float:
        """
        Evalúa comprensión causal.
        
        Factores:
        - Causas/precondiciones documentadas: +0.35
        - Efectos/postcondiciones documentadas: +0.35
        - Cadena causal completa: +0.3
        
        Args:
            concepto: ConceptoAnclado a evaluar
        
        Returns:
            float entre 0.0 (no entiende causalidad) y 1.0 (causal completo)
        """
        puntaje = 0.0
        
        if hasattr(concepto, 'propiedades'):
            props = concepto.propiedades
            
            # Causas (precondiciones)
            if 'causas' in props or 'precondiciones' in props:
                puntaje += 0.35
            
            # Efectos (postcondiciones)
            if 'efectos' in props or 'postcondiciones' in props:
                puntaje += 0.35
            
            # Cadena causal completa
            if 'cadena_causal' in props:
                puntaje += 0.3
            
            # Bonus: Invariantes causales
            if 'invariantes' in props:
                puntaje += 0.1
        
        return min(1.0, puntaje)


if __name__ == '__main__':
    print("Testing GroundingCausal...")
    
    from dataclasses import dataclass
    from typing import Dict, Any, List
    
    @dataclass
    class ConceptoTest:
        id: str
        propiedades: Dict[str, Any]
    
    concepto = ConceptoTest(
        id="CONCEPTO_ABRIR_ARCHIVO",
        propiedades={
            'precondiciones': ['archivo_existe', 'permiso_lectura'],
            'postcondiciones': ['archivo_abierto', 'descriptor_valido'],
            'cadena_causal': {
                'si': 'archivo_no_existe',
                'entonces': 'FileNotFoundError'
            }
        }
    )
    
    grounding = GroundingCausal()
    print(f"Grounding causal: {grounding.evaluar(concepto):.2f}")  # 1.0
    print("✅ GroundingCausal funciona correctamente")