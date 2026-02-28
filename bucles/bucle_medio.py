"""
Bucle Medio - Análisis de patrones conversacionales.

Ejecuta cada 120 segundos.
Propósito: Detectar patrones en las conversaciones y tipos de interacción.
"""
from typing import Dict, Any, List
from bucles.base_bucle import BaseBucle
from collections import Counter
from datetime import datetime

class BucleMedio(BaseBucle):
    """
    Bucle de análisis de patrones (120 segundos).
    
    Funciones:
    - Analizar tipos de decisiones tomadas
    - Detectar patrones de interacción
    - Identificar tendencias conversacionales
    """
    
    def __init__(self):
        super().__init__(nombre="BucleMedio", intervalo_segundos=120)
        
        # Datos compartidos con el sistema
        self.decisiones_recientes: List[Dict[str, Any]] = []
        self.max_decisiones = 30
        
        # Análisis
        self.patrones_detectados: List[Dict[str, Any]] = []
        self.estadisticas_conversacion: Dict[str, Any] = {}
    
    def registrar_decision(self, decision_info: Dict[str, Any]):
        """
        Registra una decisión tomada por Bell.
        
        Args:
            decision_info: Info de la decisión (tipo, puede_ejecutar, certeza, etc.)
        """
        entrada = {
            'timestamp': datetime.now().isoformat(),
            **decision_info
        }
        
        self.decisiones_recientes.append(entrada)
        
        # Mantener ventana de decisiones
        if len(self.decisiones_recientes) > self.max_decisiones:
            self.decisiones_recientes.pop(0)
    
    def procesar(self) -> Dict[str, Any]:
        """
        Analiza patrones en las decisiones recientes.
        
        Returns:
            Dict con análisis de patrones conversacionales
        """
        if not self.decisiones_recientes:
            return {
                'decisiones_analizadas': 0,
                'patrones': [],
                'mensaje': 'Sin decisiones para analizar'
            }
        
        # Análisis de tipos de decisión
        tipos = Counter(d.get('tipo', 'DESCONOCIDO') for d in self.decisiones_recientes)
        
        # Análisis de capacidad de ejecución
        ejecutables = sum(1 for d in self.decisiones_recientes if d.get('puede_ejecutar', False))
        tasa_ejecucion = round((ejecutables / len(self.decisiones_recientes)) * 100, 1)
        
        # Análisis de certeza promedio
        certezas = [d.get('certeza', 0.0) for d in self.decisiones_recientes if 'certeza' in d]
        certeza_promedio = round(sum(certezas) / len(certezas), 2) if certezas else 0.0
        
        # Detectar patrones
        patrones = self._detectar_patrones()
        self.patrones_detectados = patrones
        
        # Estadísticas generales
        self.estadisticas_conversacion = {
            'total_decisiones': len(self.decisiones_recientes),
            'tipos_decision': dict(tipos.most_common()),
            'tasa_ejecucion_porcentaje': tasa_ejecucion,
            'certeza_promedio': certeza_promedio,
            'decision_mas_comun': tipos.most_common(1)[0][0] if tipos else None
        }
        
        return {
            'decisiones_analizadas': len(self.decisiones_recientes),
            'tipos_detectados': len(tipos),
            'tasa_ejecucion': tasa_ejecucion,
            'certeza_promedio': certeza_promedio,
            'patrones_detectados': len(patrones),
            'patrones': patrones,
            'mensaje': f'Analizadas {len(self.decisiones_recientes)} decisiones, {len(patrones)} patrones detectados'
        }
    
    def _detectar_patrones(self) -> List[Dict[str, Any]]:
        """
        Detecta patrones en las decisiones.
        
        Returns:
            Lista de patrones detectados
        """
        patrones = []
        
        if len(self.decisiones_recientes) < 3:
            return patrones
        
        # Patrón 1: Secuencia de preguntas sobre capacidades
        preguntas_capacidad = [
            d for d in self.decisiones_recientes[-5:]
            if d.get('tipo') == 'PREGUNTA_CAPACIDAD'
        ]
        if len(preguntas_capacidad) >= 3:
            patrones.append({
                'tipo': 'EXPLORACION_CAPACIDADES',
                'descripcion': 'Usuario explorando capacidades de Bell',
                'frecuencia': len(preguntas_capacidad),
                'confianza': 0.8
            })
        
        # Patrón 2: Muchas decisiones no entendidas
        no_entendidas = [
            d for d in self.decisiones_recientes[-10:]
            if d.get('tipo') == 'NO_ENTENDIDO'
        ]
        if len(no_entendidas) >= 4:
            patrones.append({
                'tipo': 'COMUNICACION_PROBLEMATICA',
                'descripcion': 'Dificultad para entender al usuario',
                'frecuencia': len(no_entendidas),
                'confianza': 0.9
            })
        
        # Patrón 3: Conversación social (saludos, agradecimientos)
        social = [
            d for d in self.decisiones_recientes[-5:]
            if d.get('tipo') in ['SALUDO', 'AGRADECIMIENTO']
        ]
        if len(social) >= 2:
            patrones.append({
                'tipo': 'INTERACCION_SOCIAL',
                'descripcion': 'Conversación social/cortés',
                'frecuencia': len(social),
                'confianza': 0.7
            })
        
        # Patrón 4: Alta tasa de ejecución
        ejecutables = [d for d in self.decisiones_recientes if d.get('puede_ejecutar', False)]
        if len(ejecutables) >= len(self.decisiones_recientes) * 0.7:
            patrones.append({
                'tipo': 'USO_PRODUCTIVO',
                'descripcion': 'Alta proporción de tareas ejecutables',
                'frecuencia': len(ejecutables),
                'confianza': 0.85
            })
        
        return patrones
    
    def obtener_estadisticas_conversacion(self) -> Dict[str, Any]:
        """
        Retorna estadísticas de la conversación.
        
        Returns:
            Dict con estadísticas conversacionales
        """
        return self.estadisticas_conversacion.copy()
    
    def obtener_patrones(self) -> List[Dict[str, Any]]:
        """
        Retorna patrones detectados.
        
        Returns:
            Lista de patrones detectados
        """
        return self.patrones_detectados.copy()
    
    def limpiar_historial(self):
        """Limpia el historial de decisiones."""
        self.decisiones_recientes.clear()
        self.patrones_detectados.clear()
        self.estadisticas_conversacion.clear()