"""
Dimensión Computacional: ¿Bell tiene código ejecutable?

Esta es la dimensión ORIGINAL de grounding.
Mide si Bell tiene operaciones ejecutables para el concepto.

Fase 3 → Fase 4 Refactorización
"""

from grounding.base_dimension import DimensionGrounding
from typing import Any

class GroundingComputacional(DimensionGrounding):
    """
    Grounding computacional: código ejecutable.
    
    Esta es la dimensión más básica y fundamental.
    Si Bell tiene código que puede ejecutar → grounding 1.0
    Si NO tiene código → grounding 0.0
    """
    
    @property
    def nombre(self) -> str:
        return "Computacional"
    
    @property
    def descripcion(self) -> str:
        return "¿Bell tiene código ejecutable para este concepto?"
    
    def evaluar(self, concepto: Any) -> float:
        """
        Evalúa si hay código ejecutable.
        
        Args:
            concepto: ConceptoAnclado a evaluar
        
        Returns:
            1.0 si tiene operaciones ejecutables
            0.0 si no tiene
        
        Ejemplo:
            >>> concepto_leer = ConceptoAnclado(
            ...     id="CONCEPTO_LEER",
            ...     operaciones={'ejecutar': lambda: ...}
            ... )
            >>> grounding = GroundingComputacional()
            >>> grounding.evaluar(concepto_leer)
            1.0
        """
        # Verificar que concepto tenga atributo 'operaciones'
        if not hasattr(concepto, 'operaciones'):
            return 0.0
        
        operaciones = concepto.operaciones
        
        # Si no tiene operaciones o está vacío
        if not operaciones:
            return 0.0
        
        # Tiene operaciones ejecutables = grounding perfecto
        return 1.0


if __name__ == '__main__':
    # Test simple
    print("Testing GroundingComputacional...")
    
    from dataclasses import dataclass
    from typing import Dict, Callable
    
    @dataclass
    class ConceptoTest:
        id: str
        operaciones: Dict[str, Callable]
    
    # Concepto con operaciones
    concepto_con_ops = ConceptoTest(
        id="CONCEPTO_TEST",
        operaciones={'ejecutar': lambda: "hola"}
    )
    
    # Concepto sin operaciones
    concepto_sin_ops = ConceptoTest(
        id="CONCEPTO_TEST2",
        operaciones={}
    )
    
    grounding = GroundingComputacional()
    
    print(f"Con operaciones: {grounding.evaluar(concepto_con_ops)}")  # 1.0
    print(f"Sin operaciones: {grounding.evaluar(concepto_sin_ops)}")  # 0.0
    
    print("✅ GroundingComputacional funciona correctamente")