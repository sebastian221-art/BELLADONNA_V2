"""
Aplicador de Insights - Convierte insights en acciones.

Toma insights generados por bucles y los convierte en
acciones concretas sobre el sistema.
"""
from typing import Dict, Any, List, Optional
from datetime import datetime  # ✅ AGREGADO - FALTABA ESTE IMPORT

class AplicadorInsights:
    """
    Aplicador de insights.
    
    Responsabilidades:
    - Analizar insights generados
    - Convertir insights en acciones
    - Priorizar qué insights aplicar
    - Registrar resultados de aplicación
    """
    
    def __init__(self):
        """Inicializa aplicador."""
        self.insights_procesados: List[Dict[str, Any]] = []
        self.acciones_generadas: List[Dict[str, Any]] = []
    
    def procesar_insight(self, insight: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Procesa un insight y genera acciones.
        
        Args:
            insight: Insight a procesar
        
        Returns:
            Lista de acciones a realizar
        """
        tipo = insight.get('tipo', '')
        relevancia = insight.get('relevancia', 'BAJA')
        
        # Registrar insight procesado
        self.insights_procesados.append(insight)
        
        # Generar acciones según tipo
        acciones = []
        
        if tipo == 'CONCEPTO_DOMINANTE':
            acciones = self._procesar_concepto_dominante(insight)
        
        elif tipo == 'PATRON_CONDUCTUAL':
            acciones = self._procesar_patron_conductual(insight)
        
        elif tipo == 'EFECTIVIDAD_SISTEMA':
            acciones = self._procesar_efectividad(insight)
        
        elif tipo == 'CERTEZA_BAJA':
            acciones = self._procesar_certeza_baja(insight)
        
        # Registrar acciones generadas
        for accion in acciones:
            accion['relevancia_insight'] = relevancia
            self.acciones_generadas.append(accion)
        
        return acciones
    
    def _procesar_concepto_dominante(
        self,
        insight: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Procesa insight de concepto dominante.
        
        Acción: Aumentar grounding del concepto dominante.
        """
        datos = insight.get('datos', {})
        concepto_id = datos.get('concepto_id')
        porcentaje = datos.get('porcentaje', 0)
        
        if not concepto_id or porcentaje < 30:
            return []
        
        # Calcular ajuste proporcional al dominio
        ajuste = 0.03 if porcentaje < 40 else 0.05
        
        return [{
            'tipo': 'AJUSTAR_GROUNDING',
            'concepto_id': concepto_id,
            'ajuste_sugerido': ajuste,
            'razon': f"Concepto dominante ({porcentaje}% de uso)",
            'prioridad': 'ALTA' if porcentaje > 40 else 'MEDIA'
        }]
    
    def _procesar_patron_conductual(
        self,
        insight: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Procesa insight de patrón conductual.
        
        Diferentes acciones según el patrón detectado.
        """
        datos = insight.get('datos', {})
        patron = datos.get('patron', '')
        
        acciones = []
        
        if patron == 'COMUNICACION_PROBLEMATICA':
            # Sugerencia: Revisar conceptos de conversación
            acciones.append({
                'tipo': 'REVISAR_VOCABULARIO',
                'area': 'conversacion',
                'razon': 'Alta tasa de mensajes no entendidos',
                'prioridad': 'ALTA'
            })
        
        elif patron == 'EXPLORACION_CAPACIDADES':
            # Sugerencia: Usuario está aprendiendo, mantener paciencia
            acciones.append({
                'tipo': 'AJUSTAR_RESPUESTAS',
                'modo': 'educativo',
                'razon': 'Usuario explorando capacidades',
                'prioridad': 'MEDIA'
            })
        
        elif patron == 'USO_PRODUCTIVO':
            # Sistema funcionando bien, consolidar aprendizaje
            acciones.append({
                'tipo': 'CONSOLIDAR',
                'razon': 'Alta efectividad del sistema',
                'prioridad': 'BAJA'
            })
        
        return acciones
    
    def _procesar_efectividad(
        self,
        insight: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Procesa insight de efectividad del sistema.
        """
        datos = insight.get('datos', {})
        tasa = datos.get('tasa_ejecucion', 0)
        
        acciones = []
        
        if tasa < 40:
            # Baja efectividad: revisar conceptos
            acciones.append({
                'tipo': 'REVISAR_SISTEMA',
                'area': 'conceptos_bajos_grounding',
                'razon': f"Baja efectividad ({tasa}%)",
                'prioridad': 'ALTA'
            })
        
        elif tasa > 80:
            # Alta efectividad: consolidar
            acciones.append({
                'tipo': 'CONSOLIDAR',
                'razon': f"Alta efectividad ({tasa}%)",
                'prioridad': 'BAJA'
            })
        
        return acciones
    
    def _procesar_certeza_baja(
        self,
        insight: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Procesa insight de certeza baja.
        """
        datos = insight.get('datos', {})
        certeza = datos.get('certeza_promedio', 0)
        
        if certeza >= 0.6:
            return []
        
        return [{
            'tipo': 'REVISAR_VOCABULARIO',
            'area': 'conceptos_ambiguos',
            'razon': f"Certeza promedio baja ({certeza})",
            'prioridad': 'MEDIA'
        }]
    
    def procesar_multiples_insights(
        self,
        insights: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Procesa múltiples insights y prioriza acciones.
        
        Args:
            insights: Lista de insights
        
        Returns:
            Lista priorizada de acciones
        """
        todas_acciones = []
        
        # Procesar cada insight
        for insight in insights:
            acciones = self.procesar_insight(insight)
            todas_acciones.extend(acciones)
        
        # Eliminar duplicados
        acciones_unicas = self._eliminar_duplicados(todas_acciones)
        
        # Priorizar
        acciones_priorizadas = self._priorizar_acciones(acciones_unicas)
        
        return acciones_priorizadas
    
    def _eliminar_duplicados(
        self,
        acciones: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Elimina acciones duplicadas."""
        vistas = set()
        unicas = []
        
        for accion in acciones:
            # Crear clave única
            clave = (
                accion['tipo'],
                accion.get('concepto_id', ''),
                accion.get('area', '')
            )
            
            if clave not in vistas:
                vistas.add(clave)
                unicas.append(accion)
        
        return unicas
    
    def _priorizar_acciones(
        self,
        acciones: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Ordena acciones por prioridad."""
        prioridades = {'ALTA': 3, 'MEDIA': 2, 'BAJA': 1}
        
        return sorted(
            acciones,
            key=lambda a: prioridades.get(a.get('prioridad', 'BAJA'), 0),
            reverse=True
        )
    
    def obtener_acciones_pendientes(
        self,
        prioridad_minima: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Obtiene acciones pendientes de aplicar.
        
        Args:
            prioridad_minima: Prioridad mínima ('ALTA', 'MEDIA', 'BAJA')
        
        Returns:
            Lista de acciones pendientes
        """
        acciones = self.acciones_generadas.copy()
        
        if prioridad_minima:
            prioridades_incluir = []
            if prioridad_minima == 'ALTA':
                prioridades_incluir = ['ALTA']
            elif prioridad_minima == 'MEDIA':
                prioridades_incluir = ['ALTA', 'MEDIA']
            else:
                prioridades_incluir = ['ALTA', 'MEDIA', 'BAJA']
            
            acciones = [
                a for a in acciones
                if a.get('prioridad', 'BAJA') in prioridades_incluir
            ]
        
        return acciones
    
    def marcar_accion_aplicada(self, accion: Dict[str, Any]):
        """Marca una acción como aplicada."""
        accion['aplicada'] = True
        accion['timestamp_aplicacion'] = datetime.now().isoformat()
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas del aplicador.
        
        Returns:
            Dict con estadísticas
        """
        return {
            'insights_procesados': len(self.insights_procesados),
            'acciones_generadas': len(self.acciones_generadas),
            'acciones_aplicadas': sum(
                1 for a in self.acciones_generadas if a.get('aplicada', False)
            ),
            'por_tipo': self._contar_por_tipo(),
            'por_prioridad': self._contar_por_prioridad()
        }
    
    def _contar_por_tipo(self) -> Dict[str, int]:
        """Cuenta acciones por tipo."""
        conteo: Dict[str, int] = {}
        for accion in self.acciones_generadas:
            tipo = accion.get('tipo', 'DESCONOCIDO')
            conteo[tipo] = conteo.get(tipo, 0) + 1
        return conteo
    
    def _contar_por_prioridad(self) -> Dict[str, int]:
        """Cuenta acciones por prioridad."""
        conteo: Dict[str, int] = {}
        for accion in self.acciones_generadas:
            prio = accion.get('prioridad', 'BAJA')
            conteo[prio] = conteo.get(prio, 0) + 1
        return conteo