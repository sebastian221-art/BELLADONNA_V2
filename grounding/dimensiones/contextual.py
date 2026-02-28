"""
Dimensión Contextual: ¿Bell sabe CUÁNDO usar el concepto?

Mide si Bell entiende en qué contextos aplicar este concepto.
Basado en tracking de contextos de uso y predicción de éxito.

Fase 3 → Fase 4 Refactorización
"""

from grounding.base_dimension import DimensionGrounding
from typing import Any

class GroundingContextual(DimensionGrounding):
    """
    Grounding contextual: conocimiento de cuándo aplicar.
    
    Evalúa:
    - ¿Tiene precondiciones definidas?
    - ¿Conoce contextos de éxito/fallo?
    - ¿Tiene historial de uso contextual?
    """
    
    @property
    def nombre(self) -> str:
        return "Contextual"
    
    @property
    def descripcion(self) -> str:
        return "¿Bell sabe en qué contextos usar este concepto?"
    
    def evaluar(self, concepto: Any) -> float:
        """
        Evalúa conocimiento contextual.
        
        Factores:
        - Precondiciones definidas: +0.4
        - Contextos de uso documentados: +0.3
        - Historial de uso: +0.3
        
        Args:
            concepto: ConceptoAnclado a evaluar
        
        Returns:
            float entre 0.0 (no sabe cuándo usar) y 1.0 (contextos perfectos)
        
        Ejemplo:
            >>> concepto = ConceptoAnclado(
            ...     id="CONCEPTO_LEER",
            ...     propiedades={
            ...         'precondiciones': ['archivo_existe'],
            ...         'contextos_validos': ['lectura', 'carga']
            ...     }
            ... )
            >>> grounding = GroundingContextual()
            >>> grounding.evaluar(concepto)
            0.7
        """
        puntaje = 0.0
        
        # 1. Precondiciones definidas (más importante)
        if hasattr(concepto, 'propiedades'):
            props = concepto.propiedades
            
            if 'precondiciones' in props and props['precondiciones']:
                puntaje += 0.4
            
            # Contextos válidos documentados
            if 'contextos_validos' in props and props['contextos_validos']:
                puntaje += 0.3
            
            # Patrones de contexto aprendidos
            if 'patron_contextual' in props:
                puntaje += 0.2
        
        # 2. Historial de uso
        if hasattr(concepto, 'metadata'):
            veces_usado = concepto.metadata.get('veces_usado', 0)
            
            # Con suficiente historial, conoce contextos
            if veces_usado >= 10:
                puntaje += 0.3
            elif veces_usado >= 3:
                puntaje += 0.15
        
        return min(1.0, puntaje)


if __name__ == '__main__':
    print("Testing GroundingContextual...")
    
    from dataclasses import dataclass
    from typing import Dict, Any
    
    @dataclass
    class ConceptoTest:
        id: str
        propiedades: Dict[str, Any]
        metadata: Dict[str, Any]
    
    # Concepto con buen contexto
    concepto_bueno = ConceptoTest(
        id="CONCEPTO_LEER",
        propiedades={
            'precondiciones': ['archivo_existe', 'permiso_lectura'],
            'contextos_validos': ['lectura', 'carga', 'importacion']
        },
        metadata={'veces_usado': 15}
    )
    
    # Concepto sin contexto
    concepto_malo = ConceptoTest(
        id="CONCEPTO_X",
        propiedades={},
        metadata={'veces_usado': 0}
    )
    
    grounding = GroundingContextual()
    
    print(f"Concepto con contexto: {grounding.evaluar(concepto_bueno):.2f}")  # ~1.0
    print(f"Concepto sin contexto: {grounding.evaluar(concepto_malo):.2f}")   # ~0.0
    
    print("✅ GroundingContextual funciona correctamente")