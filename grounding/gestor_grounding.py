"""
Gestor Central de Grounding - Coordina todas las dimensiones.

Este es el punto de entrada principal para evaluar grounding 9D.

Uso básico:
    from grounding import GestorGrounding
    
    gestor = GestorGrounding()
    grounding_9d = gestor.evaluar_9d(concepto)
    
    # grounding_9d = {
    #     'computacional': 1.0,
    #     'semantico': 0.9,
    #     'contextual': 0.85,
    #     ...
    # }
"""

from typing import Any, Dict, List, Optional
from grounding.base_dimension import DimensionGrounding

# Importar todas las dimensiones
from grounding.dimensiones.computacional import GroundingComputacional
from grounding.dimensiones.semantico import GroundingSemantico
from grounding.dimensiones.contextual import GroundingContextual
from grounding.dimensiones.pragmatico import GroundingPragmatico
from grounding.dimensiones.social import GroundingSocial
from grounding.dimensiones.temporal import GroundingTemporal
from grounding.dimensiones.causal import GroundingCausal
from grounding.dimensiones.metacognitivo import GroundingMetacognitivo
from grounding.dimensiones.predictivo import GroundingPredictivo

class GestorGrounding:
    """
    Gestor que coordina evaluación de todas las dimensiones de grounding.
    
    Responsabilidades:
    - Mantener registro de todas las dimensiones
    - Evaluar concepto en todas las dimensiones
    - Permitir agregar dimensiones dinámicamente
    - Generar reportes de grounding
    """
    
    def __init__(self):
        """Inicializa gestor con las 9 dimensiones base."""
        
        # Instanciar todas las dimensiones
        self.dimensiones: Dict[str, DimensionGrounding] = {
            'computacional': GroundingComputacional(),
            'semantico': GroundingSemantico(),
            'contextual': GroundingContextual(),
            'pragmatico': GroundingPragmatico(),
            'social': GroundingSocial(),
            'temporal': GroundingTemporal(),
            'causal': GroundingCausal(),
            'metacognitivo': GroundingMetacognitivo(),
            'predictivo': GroundingPredictivo()
        }
        
        # Orden de evaluación (por defecto: orden de registro)
        self.orden_evaluacion = list(self.dimensiones.keys())
    
    def evaluar_9d(self, concepto: Any) -> Dict[str, float]:
        """
        Evalúa concepto en las 9 dimensiones.
        
        Args:
            concepto: ConceptoAnclado a evaluar
        
        Returns:
            Dict con puntaje de cada dimensión:
            {
                'computacional': 1.0,
                'semantico': 0.9,
                'contextual': 0.85,
                ...
            }
        
        Example:
            >>> gestor = GestorGrounding()
            >>> grounding = gestor.evaluar_9d(concepto_leer)
            >>> print(grounding['computacional'])
            1.0
        """
        resultado = {}
        
        for nombre in self.orden_evaluacion:
            dimension = self.dimensiones[nombre]
            puntaje = dimension.evaluar_con_cache(concepto)
            resultado[nombre] = puntaje
        
        return resultado
    
    def evaluar_dimension(self, 
                         concepto: Any, 
                         nombre_dimension: str) -> float:
        """
        Evalúa una dimensión específica.
        
        Args:
            concepto: ConceptoAnclado
            nombre_dimension: 'computacional', 'semantico', etc.
        
        Returns:
            float entre 0.0-1.0
        
        Raises:
            ValueError: Si dimensión no existe
        
        Example:
            >>> puntaje = gestor.evaluar_dimension(concepto, 'semantico')
            0.9
        """
        if nombre_dimension not in self.dimensiones:
            dimensiones_validas = ", ".join(self.dimensiones.keys())
            raise ValueError(
                f"Dimensión '{nombre_dimension}' no existe. "
                f"Dimensiones válidas: {dimensiones_validas}"
            )
        
        return self.dimensiones[nombre_dimension].evaluar_con_cache(concepto)
    
    def agregar_dimension(self, 
                         nombre: str, 
                         dimension: DimensionGrounding):
        """
        Agrega nueva dimensión dinámicamente.
        
        IMPORTANTE: Esto hace FÁCIL extender grounding en el futuro.
        
        Args:
            nombre: Identificador único de la dimensión
            dimension: Instancia que hereda de DimensionGrounding
        
        Raises:
            ValueError: Si dimensión no hereda de DimensionGrounding
            ValueError: Si nombre ya existe
        
        Example:
            >>> class MiDimension(DimensionGrounding):
            ...     @property
            ...     def nombre(self):
            ...         return "Mi Dimensión"
            ...     def evaluar(self, concepto):
            ...         return 0.8
            >>> 
            >>> gestor.agregar_dimension('mi_dimension', MiDimension())
            ✅ Dimensión 'mi_dimension' agregada
        """
        # Validar que hereda de DimensionGrounding
        if not isinstance(dimension, DimensionGrounding):
            raise ValueError(
                f"Dimensión debe heredar de DimensionGrounding. "
                f"Recibido: {type(dimension)}"
            )
        
        # Validar que nombre no existe
        if nombre in self.dimensiones:
            raise ValueError(
                f"Ya existe una dimensión con nombre '{nombre}'. "
                f"Use otro nombre o elimine la existente primero."
            )
        
        # Agregar
        self.dimensiones[nombre] = dimension
        self.orden_evaluacion.append(nombre)
        
        print(f"✅ Dimensión '{nombre}' agregada al gestor")
    
    def eliminar_dimension(self, nombre: str):
        """
        Elimina una dimensión.
        
        Args:
            nombre: Nombre de la dimensión a eliminar
        
        Raises:
            ValueError: Si dimensión no existe
        """
        if nombre not in self.dimensiones:
            raise ValueError(f"Dimensión '{nombre}' no existe")
        
        del self.dimensiones[nombre]
        self.orden_evaluacion.remove(nombre)
        
        print(f"✅ Dimensión '{nombre}' eliminada")
    
    def listar_dimensiones(self) -> List[str]:
        """
        Lista todas las dimensiones disponibles.
        
        Returns:
            Lista de nombres de dimensiones
        
        Example:
            >>> gestor.listar_dimensiones()
            ['computacional', 'semantico', 'contextual', ...]
        """
        return list(self.dimensiones.keys())
    
    def obtener_dimension(self, nombre: str) -> Optional[DimensionGrounding]:
        """
        Obtiene instancia de una dimensión.
        
        Args:
            nombre: Nombre de la dimensión
        
        Returns:
            Instancia de DimensionGrounding o None
        """
        return self.dimensiones.get(nombre)
    
    def limpiar_caches(self):
        """
        Limpia cache de todas las dimensiones.
        
        Útil cuando conceptos han cambiado y cache está obsoleto.
        """
        for dimension in self.dimensiones.values():
            dimension.limpiar_cache()
        
        print(f"✅ Cache limpiado en {len(self.dimensiones)} dimensiones")
    
    def obtener_estadisticas(self) -> Dict[str, Dict]:
        """
        Obtiene estadísticas de todas las dimensiones.
        
        Returns:
            Dict con estadísticas por dimensión
        """
        estadisticas = {}
        
        for nombre, dimension in self.dimensiones.items():
            estadisticas[nombre] = dimension.obtener_estadisticas()
        
        return estadisticas
    
    def calcular_promedio(self, grounding_9d: Dict[str, float]) -> float:
        """
        Calcula grounding promedio de las 9 dimensiones.
        
        Args:
            grounding_9d: Dict con puntajes de cada dimensión
        
        Returns:
            float: Promedio [0.0-1.0]
        
        Example:
            >>> grounding = gestor.evaluar_9d(concepto)
            >>> promedio = gestor.calcular_promedio(grounding)
            0.87
        """
        if not grounding_9d:
            return 0.0
        
        return sum(grounding_9d.values()) / len(grounding_9d)
    
    def generar_reporte(self, concepto: Any) -> str:
        """
        Genera reporte detallado de grounding.
        
        Args:
            concepto: ConceptoAnclado a evaluar
        
        Returns:
            str: Reporte formateado
        """
        grounding_9d = self.evaluar_9d(concepto)
        promedio = self.calcular_promedio(grounding_9d)
        
        # Header
        reporte = f"\n{'='*60}\n"
        reporte += f"REPORTE GROUNDING 9D - {concepto.id}\n"
        reporte += f"{'='*60}\n\n"
        
        # Puntajes por dimensión
        reporte += "DIMENSIONES:\n"
        for nombre in self.orden_evaluacion:
            puntaje = grounding_9d[nombre]
            dimension = self.dimensiones[nombre]
            barra = self._generar_barra(puntaje)
            
            reporte += f"  {dimension.nombre:15s} │ {barra} │ {puntaje:.2f}\n"
        
        # Promedio
        reporte += f"\n{'─'*60}\n"
        reporte += f"PROMEDIO: {promedio:.2f}\n"
        reporte += f"{'='*60}\n"
        
        return reporte
    
    def _generar_barra(self, valor: float, longitud: int = 20) -> str:
        """
        Genera barra visual de progreso.
        
        Args:
            valor: Valor entre 0.0 y 1.0
            longitud: Longitud de la barra
        
        Returns:
            str: Barra visual
        """
        lleno = int(valor * longitud)
        vacio = longitud - lleno
        
        return '█' * lleno + '░' * vacio
    
    def __repr__(self):
        return f"<GestorGrounding: {len(self.dimensiones)} dimensiones>"
    
    def __str__(self):
        dimensiones_str = ", ".join(self.dimensiones.keys())
        return f"Gestor Grounding con {len(self.dimensiones)} dimensiones: {dimensiones_str}"


# Función helper para crear gestor (conveniencia)
def crear_gestor() -> GestorGrounding:
    """
    Crea instancia de GestorGrounding.
    
    Returns:
        GestorGrounding configurado con 9 dimensiones
    
    Example:
        >>> from grounding import crear_gestor
        >>> gestor = crear_gestor()
    """
    return GestorGrounding()