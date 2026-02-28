"""
Integrador de Grounding con Bell.

Conecta el sistema de grounding 9D con el núcleo de Bell.
Permite que Bell consulte su grounding en tiempo real.

Fase 3 → Fase 4 Refactorización
"""

from typing import Dict, Any, Optional
from grounding.gestor_grounding import GestorGrounding
from grounding.calculadores.calculador_9d import Calculador9D


class IntegradorGroundingBell:
    """
    Integra grounding 9D con Bell.
    
    Responsabilidades:
    - Calcular grounding cuando Bell lo necesita
    - Cachear resultados para eficiencia
    - Proveer API simple para Bell
    
    Uso en Bell:
        class Bell:
            def __init__(self):
                self.grounding = IntegradorGroundingBell(self.vocabulario)
            
            def consultar_grounding(self, concepto_id):
                return self.grounding.obtener_grounding(concepto_id)
    """
    
    def __init__(self, gestor_vocabulario):
        """
        Inicializa integrador.
        
        Args:
            gestor_vocabulario: GestorVocabulario de Bell
        """
        self.vocabulario = gestor_vocabulario
        
        # Calculador 9D
        self.calculador = Calculador9D(gestor_vocabulario)
        
        # Gestor de grounding
        self.gestor = self.calculador.gestor
    
    def obtener_grounding(self, concepto_id: str) -> Dict[str, float]:
        """
        Obtiene grounding 9D de un concepto.
        
        Args:
            concepto_id: ID del concepto (ej: "CONCEPTO_LEER")
        
        Returns:
            Dict con grounding 9D o None si concepto no existe
        
        Example:
            >>> grounding = integrador.obtener_grounding("CONCEPTO_LEER")
            >>> print(grounding['computacional'])
            1.0
        """
        # Buscar concepto
        concepto = self.vocabulario.buscar_por_id(concepto_id)
        
        if not concepto:
            return None
        
        # Calcular grounding
        return self.calculador.calcular_concepto(concepto)
    
    def obtener_dimension(self, concepto_id: str, dimension: str) -> Optional[float]:
        """
        Obtiene puntaje de una dimensión específica.
        
        Args:
            concepto_id: ID del concepto
            dimension: Nombre de la dimensión ('computacional', 'semantico', etc.)
        
        Returns:
            float entre 0.0-1.0 o None si no existe
        
        Example:
            >>> puntaje = integrador.obtener_dimension("CONCEPTO_LEER", "semantico")
            >>> print(puntaje)
            0.9
        """
        grounding = self.obtener_grounding(concepto_id)
        
        if not grounding:
            return None
        
        return grounding.get(dimension)
    
    def obtener_promedio(self, concepto_id: str) -> Optional[float]:
        """
        Obtiene grounding promedio de un concepto.
        
        Args:
            concepto_id: ID del concepto
        
        Returns:
            float entre 0.0-1.0 o None si no existe
        
        Example:
            >>> promedio = integrador.obtener_promedio("CONCEPTO_LEER")
            >>> print(f"Grounding promedio: {promedio:.2f}")
            Grounding promedio: 0.87
        """
        grounding = self.obtener_grounding(concepto_id)
        
        if not grounding:
            return None
        
        return self.calculador.calcular_promedio(grounding)
    
    def verificar_grounding_minimo(
        self, 
        concepto_id: str, 
        umbral: float = 0.5
    ) -> bool:
        """
        Verifica si concepto tiene grounding mínimo requerido.
        
        Args:
            concepto_id: ID del concepto
            umbral: Umbral mínimo de grounding promedio (default: 0.5)
        
        Returns:
            True si grounding >= umbral, False en caso contrario
        
        Example:
            >>> if integrador.verificar_grounding_minimo("CONCEPTO_X", 0.7):
            ...     print("Concepto tiene grounding suficiente")
        """
        promedio = self.obtener_promedio(concepto_id)
        
        if promedio is None:
            return False
        
        return promedio >= umbral
    
    def generar_reporte_simple(self, concepto_id: str) -> str:
        """
        Genera reporte simple de grounding.
        
        Args:
            concepto_id: ID del concepto
        
        Returns:
            str con reporte formateado
        """
        grounding = self.obtener_grounding(concepto_id)
        
        if not grounding:
            return f"❌ Concepto '{concepto_id}' no encontrado"
        
        promedio = self.calculador.calcular_promedio(grounding)
        
        # Crear reporte
        reporte = f"\n{'='*60}\n"
        reporte += f"GROUNDING - {concepto_id}\n"
        reporte += f"{'='*60}\n\n"
        
        # Dimensiones
        for dimension, puntaje in grounding.items():
            barra = self._generar_barra(puntaje)
            reporte += f"  {dimension:15s} │ {barra} │ {puntaje:.2f}\n"
        
        # Promedio
        reporte += f"\n{'─'*60}\n"
        reporte += f"PROMEDIO: {promedio:.2f}\n"
        reporte += f"{'='*60}\n"
        
        return reporte
    
    def _generar_barra(self, valor: float, longitud: int = 20) -> str:
        """Genera barra visual de progreso."""
        lleno = int(valor * longitud)
        vacio = longitud - lleno
        return '█' * lleno + '░' * vacio
    
    def calcular_todos_async(self, callback=None):
        """
        Calcula grounding para todos los conceptos (asíncrono).
        
        Args:
            callback: Función a llamar con cada resultado (opcional)
        
        Returns:
            Dict de {concepto_id: grounding_9d}
        """
        conceptos = self.vocabulario.obtener_todos()
        resultados = {}
        
        for concepto in conceptos:
            grounding = self.calculador.calcular_concepto(concepto)
            resultados[concepto.id] = grounding
            
            # Callback si está definido
            if callback:
                callback(concepto.id, grounding)
        
        return resultados


if __name__ == '__main__':
    print("""
╔══════════════════════════════════════════════════════════╗
║      INTEGRADOR GROUNDING-BELL - BELLADONNA             ║
╚══════════════════════════════════════════════════════════╝

Integra el sistema de grounding 9D con el núcleo de Bell.

Uso:
    from grounding.integracion import IntegradorGroundingBell
    from vocabulario.gestor_vocabulario import GestorVocabulario
    
    # Inicializar
    vocabulario = GestorVocabulario()
    integrador = IntegradorGroundingBell(vocabulario)
    
    # Consultar grounding
    grounding = integrador.obtener_grounding("CONCEPTO_LEER")
    promedio = integrador.obtener_promedio("CONCEPTO_LEER")
    
    # Generar reporte
    print(integrador.generar_reporte_simple("CONCEPTO_LEER"))
    """)