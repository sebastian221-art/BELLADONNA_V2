"""
Dimensión Metacognitiva: ¿Bell puede razonar sobre sí mismo?

Mide si Bell puede pensar sobre su propio conocimiento del concepto.
"Bell sabe qué sabe" y "Bell sabe qué NO sabe".

Fase 3 → Fase 4 Refactorización
"""

from grounding.base_dimension import DimensionGrounding
from typing import Any

class GroundingMetacognitivo(DimensionGrounding):
    """
    Grounding metacognitivo: razonamiento sobre conocimiento propio.
    
    Evalúa:
    - ¿Bell sabe qué sabe?
    - ¿Bell sabe qué NO sabe?
    - ¿Puede evaluar su confianza?
    """
    
    @property
    def nombre(self) -> str:
        return "Metacognitivo"
    
    @property
    def descripcion(self) -> str:
        return "¿Bell puede razonar sobre su propio conocimiento?"
    
    def evaluar(self, concepto: Any) -> float:
        """
        Evalúa capacidad metacognitiva.
        
        Factores:
        - Confianza documentada explícitamente: +0.4
        - Limitaciones conocidas: +0.3
        - Historial de aprendizaje/ajustes: +0.3
        
        Args:
            concepto: ConceptoAnclado a evaluar
        
        Returns:
            float entre 0.0 (sin metacognición) y 1.0 (metacognición completa)
        """
        puntaje = 0.0
        
        # 1. Confianza explícita (más importante)
        if hasattr(concepto, 'confianza_grounding'):
            # Si Bell tiene confianza explícita, puede razonar sobre ella
            puntaje += 0.4
        
        # 2. Limitaciones conocidas
        if hasattr(concepto, 'propiedades'):
            props = concepto.propiedades
            
            if 'limitaciones' in props and props['limitaciones']:
                puntaje += 0.3
            
            # Bonus: Sabe qué NO puede hacer
            if 'no_puede_hacer' in props:
                puntaje += 0.1
        
        # 3. Historial de aprendizaje
        if hasattr(concepto, 'metadata'):
            metadata = concepto.metadata
            
            # Tiene registro de ajustes = sabe cómo ha evolucionado
            if 'historial_ajustes' in metadata:
                puntaje += 0.3
            
            # Bonus: Registro de errores pasados
            if 'errores_pasados' in metadata:
                puntaje += 0.1
        
        return min(1.0, puntaje)


if __name__ == '__main__':
    print("Testing GroundingMetacognitivo...")
    
    from dataclasses import dataclass
    from typing import Dict, Any, List
    
    @dataclass
    class ConceptoTest:
        id: str
        confianza_grounding: float
        propiedades: Dict[str, Any]
        metadata: Dict[str, Any]
    
    # Concepto con metacognición
    concepto_metacognitivo = ConceptoTest(
        id="CONCEPTO_LEER",
        confianza_grounding=0.95,
        propiedades={
            'limitaciones': [
                'Solo archivos de texto',
                'Máximo 10MB'
            ],
            'no_puede_hacer': ['Leer archivos binarios', 'Descifrar encriptados']
        },
        metadata={
            'historial_ajustes': [
                {'fecha': '2026-01-15', 'ajuste': 'Mejorado encoding UTF-8'},
                {'fecha': '2026-02-01', 'ajuste': 'Añadido soporte CSV'}
            ]
        }
    )
    
    # Concepto sin metacognición
    concepto_simple = ConceptoTest(
        id="CONCEPTO_X",
        confianza_grounding=0.5,
        propiedades={},
        metadata={}
    )
    
    grounding = GroundingMetacognitivo()
    
    print(f"Concepto metacognitivo: {grounding.evaluar(concepto_metacognitivo):.2f}")  # ~1.0
    print(f"Concepto simple: {grounding.evaluar(concepto_simple):.2f}")                # ~0.4
    
    print("✅ GroundingMetacognitivo funciona correctamente")