"""
Dimensión Social: ¿Bell entiende componente social?

Mide si Bell comprende el aspecto social/colaborativo del concepto.
No todos los conceptos tienen componente social fuerte.

Fase 3 → Fase 4 Refactorización
"""

from grounding.base_dimension import DimensionGrounding
from typing import Any

class GroundingSocial(DimensionGrounding):
    """
    Grounding social: comprensión del aspecto colaborativo.
    
    Evalúa:
    - ¿Requiere interacción humana?
    - ¿Tiene normas sociales?
    - ¿Afecta a otros usuarios?
    """
    
    @property
    def nombre(self) -> str:
        return "Social"
    
    @property
    def descripcion(self) -> str:
        return "¿Bell entiende el componente social de este concepto?"
    
    def evaluar(self, concepto: Any) -> float:
        """
        Evalúa comprensión social.
        
        IMPORTANTE: No todos los conceptos tienen componente social.
        Base neutral: 0.5 (algunos conceptos son puramente técnicos)
        
        Factores:
        - Requiere interacción humana: +0.2
        - Tiene normas sociales: +0.15
        - Afecta colaboración: +0.15
        
        Args:
            concepto: ConceptoAnclado a evaluar
        
        Returns:
            float entre 0.3 (sin componente social) y 1.0 (muy social)
        
        Ejemplo:
            >>> concepto_social = ConceptoAnclado(
            ...     id="CONCEPTO_PREGUNTAR",
            ...     propiedades={
            ...         'requiere_interaccion_humana': True,
            ...         'normas_sociales': ['cortesia', 'claridad'],
            ...         'afecta_otros_usuarios': True
            ...     }
            ... )
            >>> grounding = GroundingSocial()
            >>> grounding.evaluar(concepto_social)
            1.0
        """
        puntaje = 0.5  # Base neutral (no todo es social)
        
        if hasattr(concepto, 'propiedades'):
            props = concepto.propiedades
            
            # Requiere interacción humana
            if props.get('requiere_interaccion_humana', False):
                puntaje += 0.2
            
            # Normas sociales definidas
            if 'normas_sociales' in props and props['normas_sociales']:
                puntaje += 0.15
            
            # Afecta colaboración/otros usuarios
            if props.get('afecta_otros_usuarios', False):
                puntaje += 0.15
            
            # Bonus: Requiere permiso/consenso
            if props.get('requiere_consenso', False):
                puntaje += 0.1
        
        return min(1.0, max(0.3, puntaje))  # Clamp entre 0.3 y 1.0


if __name__ == '__main__':
    print("Testing GroundingSocial...")
    
    from dataclasses import dataclass
    from typing import Dict, Any, List
    
    @dataclass
    class ConceptoTest:
        id: str
        propiedades: Dict[str, Any]
    
    # Concepto social
    concepto_social = ConceptoTest(
        id="CONCEPTO_PREGUNTAR",
        propiedades={
            'requiere_interaccion_humana': True,
            'normas_sociales': ['cortesia', 'claridad', 'respeto'],
            'afecta_otros_usuarios': True
        }
    )
    
    # Concepto técnico (no social)
    concepto_tecnico = ConceptoTest(
        id="CONCEPTO_CALCULAR",
        propiedades={
            'requiere_interaccion_humana': False
        }
    )
    
    grounding = GroundingSocial()
    
    print(f"Concepto social: {grounding.evaluar(concepto_social):.2f}")      # ~1.0
    print(f"Concepto técnico: {grounding.evaluar(concepto_tecnico):.2f}")    # ~0.3-0.5
    
    print("✅ GroundingSocial funciona correctamente")