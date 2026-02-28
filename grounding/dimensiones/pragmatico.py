"""
Dimensión Pragmática: ¿Bell conoce efectos prácticos?

Mide si Bell sabe qué pasa cuando ejecuta este concepto.
Incluye efectos principales, secundarios y casos de fallo.

Fase 3 → Fase 4 Refactorización
"""

from grounding.base_dimension import DimensionGrounding
from typing import Any

class GroundingPragmatico(DimensionGrounding):
    """
    Grounding pragmático: efectos y consecuencias.
    
    Evalúa:
    - ¿Conoce efectos principales?
    - ¿Conoce efectos secundarios?
    - ¿Conoce casos de fallo?
    """
    
    @property
    def nombre(self) -> str:
        return "Pragmático"
    
    @property
    def descripcion(self) -> str:
        return "¿Bell conoce los efectos prácticos de usar este concepto?"
    
    def evaluar(self, concepto: Any) -> float:
        """
        Evalúa conocimiento pragmático.
        
        Factores:
        - Efectos/postcondiciones documentados: +0.35
        - Efectos secundarios conocidos: +0.35
        - Casos de fallo documentados: +0.3
        
        Args:
            concepto: ConceptoAnclado a evaluar
        
        Returns:
            float entre 0.0 (no sabe efectos) y 1.0 (conoce todo)
        
        Ejemplo:
            >>> concepto = ConceptoAnclado(
            ...     id="CONCEPTO_ESCRIBIR",
            ...     propiedades={
            ...         'postcondiciones': ['archivo_creado'],
            ...         'efectos_secundarios': ['consume_disco'],
            ...         'casos_fallo': ['disco_lleno', 'sin_permiso']
            ...     }
            ... )
            >>> grounding = GroundingPragmatico()
            >>> grounding.evaluar(concepto)
            1.0
        """
        puntaje = 0.0
        
        if hasattr(concepto, 'propiedades'):
            props = concepto.propiedades
            
            # 1. Efectos principales (postcondiciones)
            if 'efectos' in props or 'postcondiciones' in props:
                puntaje += 0.35
            
            # 2. Efectos secundarios conocidos
            if 'efectos_secundarios' in props:
                efectos_sec = props['efectos_secundarios']
                if efectos_sec:  # No vacío
                    puntaje += 0.35
            
            # 3. Casos de fallo documentados
            if 'casos_fallo' in props or 'excepciones' in props:
                puntaje += 0.3
            
            # Bonus: Affordances (qué habilita)
            if 'affordances' in props:
                puntaje += 0.1
        
        return min(1.0, puntaje)


if __name__ == '__main__':
    print("Testing GroundingPragmatico...")
    
    from dataclasses import dataclass
    from typing import Dict, Any
    
    @dataclass
    class ConceptoTest:
        id: str
        propiedades: Dict[str, Any]
    
    # Concepto con conocimiento pragmático completo
    concepto_completo = ConceptoTest(
        id="CONCEPTO_ESCRIBIR",
        propiedades={
            'postcondiciones': ['archivo_creado', 'datos_guardados'],
            'efectos_secundarios': ['consume_disco', 'actualiza_fecha_modificacion'],
            'casos_fallo': ['disco_lleno', 'sin_permiso', 'archivo_bloqueado']
        }
    )
    
    # Concepto sin conocimiento pragmático
    concepto_vacio = ConceptoTest(
        id="CONCEPTO_X",
        propiedades={}
    )
    
    grounding = GroundingPragmatico()
    
    print(f"Concepto completo: {grounding.evaluar(concepto_completo):.2f}")  # 1.0
    print(f"Concepto vacío: {grounding.evaluar(concepto_vacio):.2f}")        # 0.0
    
    print("✅ GroundingPragmatico funciona correctamente")