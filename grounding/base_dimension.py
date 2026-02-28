"""
Clase base abstracta para todas las dimensiones de grounding.

Cada nueva dimensión debe heredar de DimensionGrounding.
Esto garantiza consistencia y facilita agregar dimensiones.

Ejemplo de uso:
    class MiNuevaDimension(DimensionGrounding):
        @property
        def nombre(self):
            return "Mi Dimensión"
        
        def evaluar(self, concepto):
            return 0.8  # Tu lógica aquí
"""

from abc import ABC, abstractmethod
from typing import Any, Dict

class DimensionGrounding(ABC):
    """
    Clase base abstracta para una dimensión de grounding.
    
    Cualquier dimensión debe implementar:
    - nombre: Nombre de la dimensión
    - descripcion: Qué mide esta dimensión  
    - evaluar(): Calcula grounding [0.0-1.0]
    """
    
    def __init__(self):
        """Inicializa dimensión con cache vacío."""
        self.cache = {}  # Cache de evaluaciones
        self._estadisticas = {
            'evaluaciones': 0,
            'cache_hits': 0
        }
    
    @property
    @abstractmethod
    def nombre(self) -> str:
        """
        Nombre de la dimensión.
        
        Ejemplos: 'Computacional', 'Semántico', 'Temporal'
        """
        pass
    
    @property
    @abstractmethod
    def descripcion(self) -> str:
        """
        Descripción de qué mide esta dimensión.
        
        Ejemplo: "¿Bell tiene código ejecutable para este concepto?"
        """
        pass
    
    @abstractmethod
    def evaluar(self, concepto: Any) -> float:
        """
        Evalúa grounding de un concepto en esta dimensión.
        
        Args:
            concepto: ConceptoAnclado a evaluar
        
        Returns:
            float entre 0.0 (sin grounding) y 1.0 (grounding perfecto)
        
        Raises:
            ValueError: Si el concepto no es válido
        """
        pass
    
    def evaluar_con_cache(self, concepto: Any) -> float:
        """
        Evalúa con cache para optimizar rendimiento.
        
        Args:
            concepto: ConceptoAnclado a evaluar
        
        Returns:
            float: Grounding [0.0-1.0]
        """
        concepto_id = getattr(concepto, 'id', str(concepto))
        
        # Cache hit
        if concepto_id in self.cache:
            self._estadisticas['cache_hits'] += 1
            return self.cache[concepto_id]
        
        # Cache miss - evaluar
        valor = self.evaluar(concepto)
        self._estadisticas['evaluaciones'] += 1
        
        # Validar rango
        if not 0.0 <= valor <= 1.0:
            raise ValueError(
                f"Grounding debe estar entre 0.0 y 1.0. "
                f"Dimensión {self.nombre} devolvió {valor}"
            )
        
        # Guardar en cache
        self.cache[concepto_id] = valor
        
        return valor
    
    def limpiar_cache(self):
        """Limpia cache de evaluaciones."""
        self.cache.clear()
        self._estadisticas['cache_hits'] = 0
        self._estadisticas['evaluaciones'] = 0
    
    def obtener_estadisticas(self) -> Dict:
        """
        Obtiene estadísticas de uso de esta dimensión.
        
        Returns:
            Dict con evaluaciones, cache hits, etc.
        """
        tasa_cache = (
            self._estadisticas['cache_hits'] / 
            (self._estadisticas['evaluaciones'] + self._estadisticas['cache_hits'])
            if (self._estadisticas['evaluaciones'] + self._estadisticas['cache_hits']) > 0
            else 0.0
        )
        
        return {
            'dimension': self.nombre,
            'evaluaciones': self._estadisticas['evaluaciones'],
            'cache_hits': self._estadisticas['cache_hits'],
            'tasa_cache': f"{tasa_cache:.1%}",
            'items_en_cache': len(self.cache)
        }
    
    def __repr__(self):
        return f"<Dimensión: {self.nombre}>"
    
    def __str__(self):
        return f"{self.nombre}: {self.descripcion}"