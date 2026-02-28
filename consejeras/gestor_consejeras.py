"""
Gestor de Consejeras - Coordina todas las consejeras de Belladonna.

FASE 2: 7 Consejeras activas.
"""
from typing import List, Dict
from consejeras.base_consejera import Consejera
from consejeras.vega import Vega
from consejeras.nova import Nova
from consejeras.echo import Echo
from consejeras.lyra import Lyra  # ← NUEVO
from consejeras.luna import Luna  # ← NUEVO
from consejeras.iris import Iris  # ← NUEVO
from consejeras.sage import Sage  # ← NUEVO
from razonamiento.tipos_decision import Decision

class GestorConsejeras:
    """
    Coordina el sistema de consejeras.
    
    FASE 1: Vega, Nova, Echo (3 consejeras)
    FASE 2: + Lyra, Luna, Iris, Sage (7 consejeras total)
    """
    
    def __init__(self, fase: int = 2):
        """
        Inicializa gestor.
        
        Args:
            fase: 1 (solo Vega, Nova, Echo) o 2 (todas las 7)
        """
        self.fase = fase
        self.consejeras: List[Consejera] = []
        self._cargar_consejeras()
    
    def _cargar_consejeras(self):
        """Carga consejeras según fase."""
        
        # FASE 1: Consejeras básicas
        self.consejeras.append(Vega())   # Guardiana - PUEDE VETAR
        self.consejeras.append(Nova())   # Ingeniera
        self.consejeras.append(Echo())   # Lógica
        
        # FASE 2: Consejeras adicionales
        if self.fase >= 2:
            self.consejeras.append(Lyra())  # Empatía
            self.consejeras.append(Luna())  # Intuición
            self.consejeras.append(Iris())  # Visión
            self.consejeras.append(Sage())  # Síntesis (ÚLTIMA)
    
    def consultar_todas(self, decision: Decision, contexto: Dict) -> Dict:
        """
        Consulta a TODAS las consejeras en orden.
        
        Orden de consulta:
        1. Vega (puede vetar inmediatamente)
        2. Nova, Echo, Lyra, Luna, Iris (opinan)
        3. Sage (sintetiza todo)
        
        Returns:
            {
                'aprobada': bool,
                'veto': bool,
                'veto_por': str or None,
                'opiniones': List[Dict],
                'sintesis': Dict,
                'sugerencias_finales': List[str]
            }
        """
        opiniones = []
        
        # 1. Vega primero (puede vetar)
        if self.consejeras:
            vega = self.consejeras[0]  # Vega es siempre la primera
            opinion_vega = vega.revisar(decision, contexto)
            opiniones.append(opinion_vega)
            
            if opinion_vega.get('veto', False):
                # VETO - detener consulta
                return {
                    'aprobada': False,
                    'veto': True,
                    'veto_por': vega.nombre,
                    'opiniones': [opinion_vega],
                    'sintesis': opinion_vega,
                    'sugerencias_finales': opinion_vega.get('sugerencias', [])
                }
        
        # 2. Consultar demás consejeras (excepto Sage)
        for consejera in self.consejeras[1:-1]:  # Todas menos Vega y Sage
            opinion = consejera.revisar(decision, contexto)
            opiniones.append(opinion)
        
        # 3. Sage al final (sintetiza)
        if len(self.consejeras) > 1:
            sage = self.consejeras[-1]  # Sage es siempre la última
            contexto_sage = contexto.copy()
            contexto_sage['opiniones_consejeras'] = opiniones
            
            sintesis = sage.revisar(decision, contexto_sage)
            opiniones.append(sintesis)
        else:
            # Sin Sage, usar opinión de Vega como síntesis
            sintesis = opiniones[0] if opiniones else {}
        
        # 4. Generar resultado final
        return {
            'aprobada': sintesis.get('aprobada', True),
            'veto': False,  # No hay veto si llegamos aquí
            'veto_por': None,
            'opiniones': opiniones,
            'sintesis': sintesis,
            'sugerencias_finales': sintesis.get('sugerencias', [])
        }
    
    def obtener_consejera(self, nombre: str) -> Consejera:
        """Obtiene una consejera por nombre."""
        for consejera in self.consejeras:
            if consejera.nombre.lower() == nombre.lower():
                return consejera
        return None
    
    def estadisticas_globales(self) -> Dict:
        """Retorna estadísticas de todas las consejeras."""
        stats = {
            'total_consejeras': len(self.consejeras),
            'fase': self.fase,
            'consejeras': []
        }
        
        for consejera in self.consejeras:
            stats['consejeras'].append(consejera.estadisticas())
        
        return stats
    
    def __repr__(self) -> str:
        return f"<GestorConsejeras: {len(self.consejeras)} activas, Fase {self.fase}>"