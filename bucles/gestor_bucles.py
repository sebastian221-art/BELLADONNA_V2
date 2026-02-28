"""
Gestor de Bucles - Coordina los bucles autónomos de Bell.

Gestiona los 3 bucles:
- BucleCorto (60s): Análisis rápido de conceptos
- BucleMedio (120s): Análisis de patrones
- BucleLargo (600s): Consolidación de aprendizaje
"""
from typing import Dict, Any, List, Optional
from bucles.base_bucle import BaseBucle
from bucles.bucle_corto import BucleCorto
from bucles.bucle_medio import BucleMedio
from bucles.bucle_largo import BucleLargo

class GestorBucles:
    """
    Gestor central de bucles autónomos.
    
    Responsabilidades:
    - Iniciar/detener bucles
    - Coordinar comunicación entre bucles
    - Proporcionar interfaz unificada
    """
    
    def __init__(self):
        """Inicializa gestor y crea bucles."""
        # Crear instancias de bucles
        self.bucle_corto = BucleCorto()
        self.bucle_medio = BucleMedio()
        self.bucle_largo = BucleLargo()
        
        # Configurar dependencias del bucle largo
        self.bucle_largo.configurar_bucles(
            self.bucle_corto,
            self.bucle_medio
        )
        
        # Estado
        self._todos_activos = False
    
    def iniciar_todos(self) -> Dict[str, bool]:
        """
        Inicia todos los bucles.
        
        Returns:
            Dict con estado de inicio de cada bucle
        """
        resultados = {
            'corto': self.bucle_corto.iniciar(),
            'medio': self.bucle_medio.iniciar(),
            'largo': self.bucle_largo.iniciar()
        }
        
        self._todos_activos = all(resultados.values())
        
        return resultados
    
    def detener_todos(self) -> Dict[str, bool]:
        """
        Detiene todos los bucles.
        
        Returns:
            Dict con estado de detención de cada bucle
        """
        resultados = {
            'corto': self.bucle_corto.detener(),
            'medio': self.bucle_medio.detener(),
            'largo': self.bucle_largo.detener()
        }
        
        self._todos_activos = False
        
        return resultados
    
    def iniciar_bucle(self, nombre: str) -> bool:
        """
        Inicia un bucle específico.
        
        Args:
            nombre: 'corto', 'medio' o 'largo'
        
        Returns:
            True si se inició correctamente
        """
        bucle = self._obtener_bucle(nombre)
        if bucle:
            return bucle.iniciar()
        return False
    
    def detener_bucle(self, nombre: str) -> bool:
        """
        Detiene un bucle específico.
        
        Args:
            nombre: 'corto', 'medio' o 'largo'
        
        Returns:
            True si se detuvo correctamente
        """
        bucle = self._obtener_bucle(nombre)
        if bucle:
            return bucle.detener()
        return False
    
    def _obtener_bucle(self, nombre: str) -> Optional[BaseBucle]:
        """Obtiene instancia de bucle por nombre."""
        nombre_lower = nombre.lower()
        if nombre_lower == 'corto':
            return self.bucle_corto
        elif nombre_lower == 'medio':
            return self.bucle_medio
        elif nombre_lower == 'largo':
            return self.bucle_largo
        return None
    
    def registrar_concepto_usado(self, concepto_id: str):
        """
        Registra que un concepto fue usado (para bucle corto).
        
        Args:
            concepto_id: ID del concepto usado
        """
        self.bucle_corto.registrar_concepto_usado(concepto_id)
    
    def registrar_decision(self, decision_info: Dict[str, Any]):
        """
        Registra una decisión tomada (para bucle medio).
        
        Args:
            decision_info: Info de la decisión
        """
        self.bucle_medio.registrar_decision(decision_info)
    
    def obtener_estadisticas(self, nombre: Optional[str] = None) -> Dict[str, Any]:
        """
        Obtiene estadísticas de bucles.
        
        Args:
            nombre: Bucle específico o None para todos
        
        Returns:
            Dict con estadísticas
        """
        if nombre:
            bucle = self._obtener_bucle(nombre)
            if bucle:
                return bucle.obtener_estadisticas()
            return {}
        
        return {
            'corto': self.bucle_corto.obtener_estadisticas(),
            'medio': self.bucle_medio.obtener_estadisticas(),
            'largo': self.bucle_largo.obtener_estadisticas()
        }
    
    def obtener_conceptos_calientes(self) -> List[Dict[str, Any]]:
        """
        Obtiene conceptos calientes del bucle corto.
        
        Returns:
            Lista de conceptos calientes
        """
        return self.bucle_corto.obtener_conceptos_calientes()
    
    def obtener_patrones(self) -> List[Dict[str, Any]]:
        """
        Obtiene patrones detectados del bucle medio.
        
        Returns:
            Lista de patrones
        """
        return self.bucle_medio.obtener_patrones()
    
    def obtener_insights(
        self,
        tipo: Optional[str] = None,
        n: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Obtiene insights del bucle largo.
        
        Args:
            tipo: Filtrar por tipo
            n: Número de insights
        
        Returns:
            Lista de insights
        """
        return self.bucle_largo.obtener_insights(tipo, n)
    
    def obtener_ajustes_recomendados(self) -> List[Dict[str, Any]]:
        """
        Obtiene ajustes de grounding recomendados del bucle largo.
        
        Returns:
            Lista de ajustes recomendados
        """
        return self.bucle_largo.obtener_ajustes_recomendados()
    
    def estado_sistema(self) -> Dict[str, Any]:
        """
        Retorna estado completo del sistema de bucles.
        
        Returns:
            Dict con estado de todos los bucles
        
        ✅ CORRECCIÓN: Usar nombres consistentes con main.py
        """
        return {
            'todos_activos': self._todos_activos,
            'bucles_activos': self._todos_activos,  # ← AGREGADO para consistencia
            'bucles': {
                'corto': {
                    'activo': self.bucle_corto.esta_activo(),
                    'ciclos_ejecutados': self.bucle_corto.estadisticas['ejecuciones'],  # ← RENOMBRADO
                    'intervalo_segundos': self.bucle_corto.intervalo_segundos,
                    'ultimo_ciclo': self.bucle_corto.estadisticas.get('ultima_ejecucion', 'Nunca')  # ← AGREGADO
                },
                'medio': {
                    'activo': self.bucle_medio.esta_activo(),
                    'ciclos_ejecutados': self.bucle_medio.estadisticas['ejecuciones'],  # ← RENOMBRADO
                    'intervalo_segundos': self.bucle_medio.intervalo_segundos,
                    'ultimo_ciclo': self.bucle_medio.estadisticas.get('ultima_ejecucion', 'Nunca')  # ← AGREGADO
                },
                'largo': {
                    'activo': self.bucle_largo.esta_activo(),
                    'ciclos_ejecutados': self.bucle_largo.estadisticas['ejecuciones'],  # ← RENOMBRADO
                    'intervalo_segundos': self.bucle_largo.intervalo_segundos,
                    'ultimo_ciclo': self.bucle_largo.estadisticas.get('ultima_ejecucion', 'Nunca')  # ← AGREGADO
                }
            },
            'resumen': {
                'conceptos_calientes': len(self.bucle_corto.obtener_conceptos_calientes()),
                'patrones_detectados': len(self.bucle_medio.obtener_patrones()),
                'insights_generados': len(self.bucle_largo.obtener_insights()),
                'ajustes_pendientes': len(self.bucle_largo.obtener_ajustes_recomendados())
            }
        }
    
    def limpiar_historial_todos(self):
        """Limpia historial de todos los bucles."""
        self.bucle_corto.limpiar_historial()
        self.bucle_medio.limpiar_historial()
        self.bucle_largo.limpiar_historial()