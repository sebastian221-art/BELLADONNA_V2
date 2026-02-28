"""
Bucle Largo - Consolidación de aprendizaje.

Ejecuta cada 600 segundos (10 minutos).
Propósito: Consolidar aprendizajes, ajustar confianzas, generar insights.
"""
from typing import Dict, Any, List, Optional
from bucles.base_bucle import BaseBucle
from datetime import datetime

class BucleLargo(BaseBucle):
    """
    Bucle de consolidación (600 segundos / 10 minutos).
    
    Funciones:
    - Consolidar aprendizajes de bucles cortos/medios
    - Identificar conceptos que necesitan ajuste de grounding
    - Generar insights de largo plazo
    """
    
    def __init__(self):
        super().__init__(nombre="BucleLargo", intervalo_segundos=600)
        
        # Referencias a otros bucles (inyectadas)
        self.bucle_corto: Optional[Any] = None
        self.bucle_medio: Optional[Any] = None
        
        # Insights generados
        self.insights: List[Dict[str, Any]] = []
        self.max_insights = 20
        
        # Recomendaciones de ajuste
        self.ajustes_recomendados: List[Dict[str, Any]] = []
    
    def configurar_bucles(self, bucle_corto, bucle_medio):
        """
        Configura referencias a otros bucles.
        
        Args:
            bucle_corto: Instancia de BucleCorto
            bucle_medio: Instancia de BucleMedio
        """
        self.bucle_corto = bucle_corto
        self.bucle_medio = bucle_medio
    
    def procesar(self) -> Dict[str, Any]:
        """
        Consolida información de bucles cortos/medios.
        
        Returns:
            Dict con análisis consolidado y recomendaciones
        """
        # Obtener datos de otros bucles
        conceptos_calientes = self._obtener_conceptos_calientes()
        patrones = self._obtener_patrones()
        stats_conversacion = self._obtener_estadisticas_conversacion()
        
        # Generar insights
        insights_nuevos = self._generar_insights(
            conceptos_calientes,
            patrones,
            stats_conversacion
        )
        
        # Agregar al historial de insights
        for insight in insights_nuevos:
            self._agregar_insight(insight)
        
        # Generar recomendaciones de ajuste
        ajustes = self._generar_recomendaciones_ajuste(conceptos_calientes)
        self.ajustes_recomendados = ajustes
        
        return {
            'insights_generados': len(insights_nuevos),
            'insights_totales': len(self.insights),
            'ajustes_recomendados': len(ajustes),
            'conceptos_analizados': len(conceptos_calientes),
            'patrones_procesados': len(patrones),
            'insights': insights_nuevos,
            'ajustes': ajustes,
            'mensaje': f'Consolidados {len(conceptos_calientes)} conceptos, {len(insights_nuevos)} insights generados'
        }
    
    def _obtener_conceptos_calientes(self) -> List[Dict[str, Any]]:
        """Obtiene conceptos calientes del bucle corto."""
        if self.bucle_corto:
            return self.bucle_corto.obtener_conceptos_calientes()
        return []
    
    def _obtener_patrones(self) -> List[Dict[str, Any]]:
        """Obtiene patrones del bucle medio."""
        if self.bucle_medio:
            return self.bucle_medio.obtener_patrones()
        return []
    
    def _obtener_estadisticas_conversacion(self) -> Dict[str, Any]:
        """Obtiene estadísticas conversacionales del bucle medio."""
        if self.bucle_medio:
            return self.bucle_medio.obtener_estadisticas_conversacion()
        return {}
    
    def _generar_insights(
        self,
        conceptos_calientes: List[Dict[str, Any]],
        patrones: List[Dict[str, Any]],
        stats: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Genera insights a partir de los datos consolidados.
        
        Returns:
            Lista de insights generados
        """
        insights = []
        
        # Insight 1: Conceptos dominantes
        if conceptos_calientes:
            top_concepto = conceptos_calientes[0]
            if top_concepto['porcentaje'] > 30:
                insights.append({
                    'tipo': 'CONCEPTO_DOMINANTE',
                    'descripcion': f"Concepto {top_concepto['concepto_id']} domina el uso ({top_concepto['porcentaje']}%)",
                    'concepto_id': top_concepto['concepto_id'],
                    'relevancia': 'ALTA',
                    'timestamp': datetime.now().isoformat()
                })
        
        # Insight 2: Patrones de comportamiento
        for patron in patrones:
            if patron.get('confianza', 0) >= 0.8:
                insights.append({
                    'tipo': 'PATRON_CONDUCTUAL',
                    'descripcion': patron['descripcion'],
                    'patron': patron['tipo'],
                    'relevancia': 'MEDIA',
                    'timestamp': datetime.now().isoformat()
                })
        
        # Insight 3: Tasa de éxito
        if stats.get('tasa_ejecucion_porcentaje'):
            tasa = stats['tasa_ejecucion_porcentaje']
            if tasa > 80:
                relevancia = 'ALTA'
                descripcion = f"Alta efectividad: {tasa}% de decisiones ejecutables"
            elif tasa < 40:
                relevancia = 'ALTA'
                descripcion = f"Baja efectividad: solo {tasa}% ejecutable, revisar capacidades"
            else:
                relevancia = 'BAJA'
                descripcion = f"Efectividad normal: {tasa}% ejecutable"
            
            if tasa > 80 or tasa < 40:
                insights.append({
                    'tipo': 'EFECTIVIDAD_SISTEMA',
                    'descripcion': descripcion,
                    'tasa_ejecucion': tasa,
                    'relevancia': relevancia,
                    'timestamp': datetime.now().isoformat()
                })
        
        # Insight 4: Certeza promedio
        certeza = stats.get('certeza_promedio', 0)
        if certeza < 0.6:
            insights.append({
                'tipo': 'CERTEZA_BAJA',
                'descripcion': f"Certeza promedio baja ({certeza}), posible ambigüedad en comunicación",
                'certeza_promedio': certeza,
                'relevancia': 'MEDIA',
                'timestamp': datetime.now().isoformat()
            })
        
        return insights
    
    def _generar_recomendaciones_ajuste(
        self,
        conceptos_calientes: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Genera recomendaciones de ajuste de grounding.
        
        Returns:
            Lista de recomendaciones de ajuste
        """
        ajustes = []
        
        # Recomendar aumentar grounding de conceptos muy usados
        for concepto in conceptos_calientes[:5]:  # Top 5
            if concepto['usos'] >= 5:
                ajustes.append({
                    'tipo': 'AUMENTAR_GROUNDING',
                    'concepto_id': concepto['concepto_id'],
                    'razon': f"Usado {concepto['usos']} veces ({concepto['porcentaje']}%)",
                    'ajuste_sugerido': +0.05,  # Aumentar 0.05
                    'prioridad': 'ALTA' if concepto['porcentaje'] > 20 else 'MEDIA'
                })
        
        return ajustes
    
    def _agregar_insight(self, insight: Dict[str, Any]):
        """Agrega insight al historial."""
        self.insights.append(insight)
        if len(self.insights) > self.max_insights:
            self.insights.pop(0)
    
    def obtener_insights(self, tipo: Optional[str] = None, n: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Retorna insights generados.
        
        Args:
            tipo: Filtrar por tipo de insight (None = todos)
            n: Número de últimos insights (None = todos)
        
        Returns:
            Lista de insights
        """
        insights = self.insights.copy()
        
        # Filtrar por tipo
        if tipo:
            insights = [i for i in insights if i.get('tipo') == tipo]
        
        # Limitar cantidad
        if n is not None and n > 0:
            insights = insights[-n:]
        
        return insights
    
    def obtener_ajustes_recomendados(self) -> List[Dict[str, Any]]:
        """
        Retorna ajustes de grounding recomendados.
        
        Returns:
            Lista de recomendaciones de ajuste
        """
        return self.ajustes_recomendados.copy()
    
    def limpiar_historial(self):
        """Limpia historial de insights y ajustes."""
        self.insights.clear()
        self.ajustes_recomendados.clear()