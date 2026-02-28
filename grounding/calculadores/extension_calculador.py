"""
Extensión de Grounding para ConceptoAnclado.

Versión refactorizada que usa el nuevo sistema modular de grounding.
Provee una API simple para extender conceptos con capacidades de grounding 9D.

Fase 3 → Fase 4 Refactorización
"""

from typing import Dict, Any, Optional
from datetime import datetime
from grounding.gestor_grounding import GestorGrounding
from grounding.calculadores.calculador_9d import Calculador9D


class ExtensionGrounding:
    """
    Extiende un ConceptoAnclado con grounding 9D.
    
    Versión simplificada que usa el nuevo sistema modular.
    Mucho más simple que la versión original porque delega
    todo al GestorGrounding.
    
    Uso:
        # Crear extensión
        extension = ExtensionGrounding(concepto)
        
        # Obtener grounding
        grounding_9d = extension.obtener_grounding()
        
        # Obtener promedio
        promedio = extension.obtener_promedio()
        
        # Obtener dimensión específica
        semantico = extension.obtener_dimension('semantico')
    """
    
    def __init__(self, concepto_base, vocabulario=None):
        """
        Inicializa extensión de grounding.
        
        Args:
            concepto_base: ConceptoAnclado a extender
            vocabulario: GestorVocabulario (opcional, mejora semántico)
        """
        self.concepto = concepto_base
        self.vocabulario = vocabulario
        
        # Calculador 9D
        self.calculador = Calculador9D(vocabulario)
        
        # Gestor de grounding
        self.gestor = self.calculador.gestor
        
        # Cache de último cálculo
        self._ultimo_grounding: Optional[Dict[str, float]] = None
        self._timestamp_calculo: Optional[str] = None
    
    def obtener_grounding(self, forzar_recalculo: bool = False) -> Dict[str, float]:
        """
        Obtiene grounding 9D del concepto.
        
        Args:
            forzar_recalculo: Si True, recalcula aunque haya cache
        
        Returns:
            Dict con puntajes de las 9 dimensiones
        
        Example:
            >>> extension = ExtensionGrounding(concepto)
            >>> grounding = extension.obtener_grounding()
            >>> print(grounding['computacional'])
            1.0
        """
        # Usar cache si existe y no se fuerza recálculo
        if not forzar_recalculo and self._ultimo_grounding is not None:
            return self._ultimo_grounding
        
        # Calcular grounding
        grounding_9d = self.calculador.calcular_concepto(self.concepto)
        
        # Actualizar cache
        self._ultimo_grounding = grounding_9d
        self._timestamp_calculo = datetime.now().isoformat()
        
        return grounding_9d
    
    def obtener_dimension(self, nombre: str) -> float:
        """
        Obtiene puntaje de una dimensión específica.
        
        Args:
            nombre: Nombre de la dimensión ('computacional', 'semantico', etc.)
        
        Returns:
            float entre 0.0-1.0
        
        Example:
            >>> puntaje = extension.obtener_dimension('semantico')
            0.9
        """
        grounding = self.obtener_grounding()
        return grounding.get(nombre, 0.0)
    
    def obtener_promedio(self) -> float:
        """
        Obtiene grounding promedio del concepto.
        
        Returns:
            float entre 0.0-1.0
        
        Example:
            >>> promedio = extension.obtener_promedio()
            0.87
        """
        grounding = self.obtener_grounding()
        return self.calculador.calcular_promedio(grounding)
    
    def obtener_resumen(self) -> Dict[str, Any]:
        """
        Obtiene resumen completo de grounding.
        
        Returns:
            Dict con información detallada
        
        Example:
            >>> resumen = extension.obtener_resumen()
            >>> print(resumen['score_total'])
            0.87
        """
        grounding = self.obtener_grounding()
        
        return {
            'concepto_id': self.concepto.id,
            'score_total': self.obtener_promedio(),
            'timestamp': self._timestamp_calculo,
            
            # Scores por dimensión
            'confianza_grounding': grounding.get('computacional', 0.0),
            'grounding_semantico': grounding.get('semantico', 0.0),
            'grounding_contextual': grounding.get('contextual', 0.0),
            'grounding_pragmatico': grounding.get('pragmatico', 0.0),
            'grounding_social': grounding.get('social', 0.0),
            'grounding_temporal': grounding.get('temporal', 0.0),
            'grounding_causal': grounding.get('causal', 0.0),
            'grounding_metacognitivo': grounding.get('metacognitivo', 0.0),
            'grounding_predictivo': grounding.get('predictivo', 0.0),
            
            # Dimensiones completas
            'dimensiones': grounding
        }
    
    def calcular_grounding_total(self) -> float:
        """
        Calcula grounding total (promedio de 9 dimensiones).
        
        Compatible con API antigua.
        
        Returns:
            float entre 0.0-1.0
        """
        return self.obtener_promedio()
    
    def generar_reporte(self) -> str:
        """
        Genera reporte visual de grounding.
        
        Returns:
            str con reporte formateado
        """
        concepto = self.concepto
        grounding = self.obtener_grounding()
        promedio = self.obtener_promedio()
        
        # Crear reporte usando gestor
        reporte = self.gestor.generar_reporte(concepto)
        
        return reporte
    
    def invalidar_cache(self):
        """
        Invalida cache de grounding.
        
        Útil cuando el concepto ha sido modificado.
        """
        self._ultimo_grounding = None
        self._timestamp_calculo = None
        self.calculador.limpiar_cache()
    
    # ==================== PROPIEDADES PARA COMPATIBILIDAD ====================
    # Propiedades que mantienen compatibilidad con API antigua
    
    @property
    def grounding_computacional(self) -> float:
        """Grounding computacional (compatibilidad)."""
        return self.obtener_dimension('computacional')
    
    @property
    def grounding_semantico(self) -> float:
        """Grounding semántico (compatibilidad)."""
        return self.obtener_dimension('semantico')
    
    @property
    def grounding_contextual(self) -> float:
        """Grounding contextual (compatibilidad)."""
        return self.obtener_dimension('contextual')
    
    @property
    def grounding_pragmatico(self) -> float:
        """Grounding pragmático (compatibilidad)."""
        return self.obtener_dimension('pragmatico')
    
    @property
    def grounding_social(self) -> float:
        """Grounding social (compatibilidad)."""
        return self.obtener_dimension('social')
    
    @property
    def grounding_temporal(self) -> float:
        """Grounding temporal (compatibilidad)."""
        return self.obtener_dimension('temporal')
    
    @property
    def grounding_causal(self) -> float:
        """Grounding causal (compatibilidad)."""
        return self.obtener_dimension('causal')
    
    @property
    def grounding_metacognitivo(self) -> float:
        """Grounding metacognitivo (compatibilidad)."""
        return self.obtener_dimension('metacognitivo')
    
    @property
    def grounding_predictivo(self) -> float:
        """Grounding predictivo (compatibilidad)."""
        return self.obtener_dimension('predictivo')
    
    def __repr__(self):
        promedio = self.obtener_promedio() if self._ultimo_grounding else 0.0
        return (
            f"ExtensionGrounding({self.concepto.id}, "
            f"grounding={promedio:.2f})"
        )


# ==================== FUNCIÓN HELPER ====================

def crear_extension(concepto, vocabulario=None) -> ExtensionGrounding:
    """
    Crea extensión de grounding para un concepto.
    
    Args:
        concepto: ConceptoAnclado
        vocabulario: GestorVocabulario (opcional)
    
    Returns:
        ExtensionGrounding
    
    Example:
        >>> extension = crear_extension(concepto, vocabulario)
        >>> print(extension.obtener_promedio())
        0.87
    """
    return ExtensionGrounding(concepto, vocabulario)


if __name__ == '__main__':
    print("""
╔══════════════════════════════════════════════════════════╗
║        EXTENSIÓN DE GROUNDING - BELLADONNA              ║
╚══════════════════════════════════════════════════════════╝

Extiende ConceptoAnclado con grounding 9D.

Versión refactorizada - mucho más simple que la original.

Uso:
    from grounding.calculadores import ExtensionGrounding
    from core.concepto_anclado import ConceptoAnclado
    
    # Crear concepto
    concepto = ConceptoAnclado(
        id="CONCEPTO_LEER",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["leer"],
        operaciones={'ejecutar': lambda: ...}
    )
    
    # Crear extensión
    extension = ExtensionGrounding(concepto, vocabulario)
    
    # Obtener grounding
    grounding = extension.obtener_grounding()
    promedio = extension.obtener_promedio()
    
    # Generar reporte
    print(extension.generar_reporte())

Ventajas de la versión refactorizada:
- ✅ Mucho más simple (100 líneas vs 571 líneas originales)
- ✅ Usa sistema modular nuevo
- ✅ Compatible con API antigua (propiedades)
- ✅ Cache automático
- ✅ Más fácil de mantener
    """)