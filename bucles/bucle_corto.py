"""
Bucle Corto - Revisión rápida de conceptos recientes.

Ejecuta cada 60 segundos.
Propósito: Revisar qué conceptos se están usando más frecuentemente.
"""
from typing import Dict, Any, List
from bucles.base_bucle import BaseBucle
from collections import Counter

class BucleCorto(BaseBucle):
    """
    Bucle de análisis rápido (60 segundos).
    
    Funciones:
    - Revisar conceptos más usados recientemente
    - Detectar patrones inmediatos de uso
    - Identificar conceptos "calientes"
    """
    
    def __init__(self):
        super().__init__(nombre="BucleCorto", intervalo_segundos=60)
        
        # Datos compartidos con el sistema
        self.conceptos_recientes: List[str] = []
        self.max_conceptos_recientes = 50
        
        # Análisis
        self.conceptos_calientes: List[Dict[str, Any]] = []
        self.umbral_caliente = 3  # Usado 3+ veces en ventana
    
    def registrar_concepto_usado(self, concepto_id: str):
        """
        Registra que un concepto fue usado.
        
        Args:
            concepto_id: ID del concepto usado
        """
        self.conceptos_recientes.append(concepto_id)
        
        # Mantener ventana de conceptos recientes
        if len(self.conceptos_recientes) > self.max_conceptos_recientes:
            self.conceptos_recientes.pop(0)
    
    def procesar(self) -> Dict[str, Any]:
        """
        Analiza conceptos usados recientemente.
        
        Returns:
            Dict con análisis de conceptos recientes
        """
        if not self.conceptos_recientes:
            return {
                'conceptos_analizados': 0,
                'conceptos_calientes': [],
                'mensaje': 'Sin conceptos para analizar'
            }
        
        # Contar frecuencias
        contador = Counter(self.conceptos_recientes)
        
        # Identificar conceptos "calientes" (usados frecuentemente)
        calientes = [
            {
                'concepto_id': concepto_id,
                'usos': count,
                'porcentaje': round((count / len(self.conceptos_recientes)) * 100, 1)
            }
            for concepto_id, count in contador.most_common(10)
            if count >= self.umbral_caliente
        ]
        
        self.conceptos_calientes = calientes
        
        # Análisis de diversidad
        conceptos_unicos = len(contador)
        diversidad = round((conceptos_unicos / len(self.conceptos_recientes)) * 100, 1) if self.conceptos_recientes else 0
        
        return {
            'conceptos_analizados': len(self.conceptos_recientes),
            'conceptos_unicos': conceptos_unicos,
            'diversidad_porcentaje': diversidad,
            'conceptos_calientes': calientes,
            'top_3': [c['concepto_id'] for c in calientes[:3]],
            'mensaje': f'Analizados {conceptos_unicos} conceptos únicos en {len(self.conceptos_recientes)} usos'
        }
    
    def obtener_conceptos_calientes(self) -> List[Dict[str, Any]]:
        """
        Retorna conceptos que se están usando frecuentemente.
        
        Returns:
            Lista de conceptos calientes con estadísticas
        """
        return self.conceptos_calientes.copy()
    
    def limpiar_historial(self):
        """Limpia el historial de conceptos recientes."""
        self.conceptos_recientes.clear()
        self.conceptos_calientes.clear()