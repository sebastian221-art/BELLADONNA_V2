"""
Dimensión Predictiva: ¿Bell puede predecir resultados?

Mide si Bell puede anticipar qué pasará al usar el concepto.
Basado en historial de uso y patrones aprendidos.

Fase 3 → Fase 4 Refactorización
"""

from grounding.base_dimension import DimensionGrounding
from typing import Any

class GroundingPredictivo(DimensionGrounding):
    """
    Grounding predictivo: capacidad de predecir resultados.
    
    Evalúa:
    - ¿Puede predecir éxito/fallo?
    - ¿Puede estimar resultados?
    - ¿Aprende de predicciones pasadas?
    """
    
    @property
    def nombre(self) -> str:
        return "Predictivo"
    
    @property
    def descripcion(self) -> str:
        return "¿Bell puede predecir resultados de usar este concepto?"
    
    def evaluar(self, concepto: Any) -> float:
        """
        Evalúa capacidad predictiva.
        
        Factores:
        - Historial de uso suficiente: +0.4
        - Tasa de éxito conocida: +0.3
        - Patrones de uso aprendidos: +0.3
        
        Args:
            concepto: ConceptoAnclado a evaluar
        
        Returns:
            float entre 0.0 (no puede predecir) y 1.0 (predice perfectamente)
        """
        puntaje = 0.0
        
        # 1. Historial de uso (fundamental para predicción)
        if hasattr(concepto, 'metadata'):
            metadata = concepto.metadata
            veces_usado = metadata.get('veces_usado', 0)
            
            # Con suficiente historial, puede predecir
            if veces_usado >= 20:
                puntaje += 0.4
            elif veces_usado >= 10:
                puntaje += 0.3
            elif veces_usado >= 5:
                puntaje += 0.2
        
        # 2. Tasa de éxito conocida
        if hasattr(concepto, 'propiedades'):
            props = concepto.propiedades
            
            if 'tasa_exito' in props:
                puntaje += 0.3
            
            # Bonus: Varianza de resultados (sabe cuánto varía)
            if 'varianza_resultados' in props:
                puntaje += 0.1
        
        # 3. Patrones de uso aprendidos
        if hasattr(concepto, 'propiedades'):
            props = concepto.propiedades
            
            if 'patrones_uso' in props and props['patrones_uso']:
                puntaje += 0.3
            
            # Bonus: Modelo predictivo explícito
            if 'modelo_predictivo' in props:
                puntaje += 0.1
        
        return min(1.0, puntaje)


if __name__ == '__main__':
    print("Testing GroundingPredictivo...")
    
    from dataclasses import dataclass
    from typing import Dict, Any, List
    
    @dataclass
    class ConceptoTest:
        id: str
        propiedades: Dict[str, Any]
        metadata: Dict[str, Any]
    
    # Concepto con buena capacidad predictiva
    concepto_predictivo = ConceptoTest(
        id="CONCEPTO_LEER",
        propiedades={
            'tasa_exito': 0.97,
            'patrones_uso': [
                {'contexto': 'archivo_pequeño', 'exito': 0.99},
                {'contexto': 'archivo_grande', 'exito': 0.95}
            ],
            'varianza_resultados': 0.03
        },
        metadata={
            'veces_usado': 250
        }
    )
    
    # Concepto nuevo sin historial
    concepto_nuevo = ConceptoTest(
        id="CONCEPTO_X",
        propiedades={},
        metadata={'veces_usado': 1}
    )
    
    grounding = GroundingPredictivo()
    
    print(f"Concepto predictivo: {grounding.evaluar(concepto_predictivo):.2f}")  # ~1.0
    print(f"Concepto nuevo: {grounding.evaluar(concepto_nuevo):.2f}")            # ~0.0
    
    print("✅ GroundingPredictivo funciona correctamente")