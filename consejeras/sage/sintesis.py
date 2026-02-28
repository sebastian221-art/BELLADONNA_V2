"""
Sage - Consejera de Síntesis.

Especialidad: Sintetizar todas las opiniones y generar decisión final.
Vigila: Todos los principios
Puede vetar: NO (pero su palabra es la más importante)
"""
from typing import Dict, List
from consejeras.base_consejera import Consejera
from razonamiento.tipos_decision import Decision
from core.principios import Principio

class Sage(Consejera):
    """
    Sage - La Sintetizadora.
    
    Responsabilidades:
    - Sintetizar opiniones de todas las consejeras
    - Resolver conflictos entre opiniones
    - Generar recomendación final coherente
    - Ser la "voz de la razón" del consejo
    
    Es la ÚLTIMA consejera en opinar.
    Su opinión pesa más que las demás (excepto vetos de Vega).
    """
    
    def __init__(self):
        """Inicializa Sage."""
        super().__init__("Sage", "Síntesis y Sabiduría")
        self.puede_vetar = False
        
        # Vigila TODOS los principios holísticamente
        self.principios_vigilados = list(Principio)
    
    def revisar(self, decision: Decision, contexto: Dict) -> Dict:
        """
        Revisa la decisión y sintetiza opiniones previas.
        
        Esta consejera debe recibir las opiniones de TODAS
        las demás consejeras en el contexto.
        """
        self.revisiones_realizadas += 1
        
        # Obtener opiniones previas
        opiniones_previas = contexto.get('opiniones_consejeras', [])
        
        if not opiniones_previas:
            # Si no hay opiniones previas, generar opinión simple
            return self._generar_opinion_simple(decision)
        
        # Sintetizar opiniones
        return self._sintetizar_opiniones(decision, opiniones_previas)
    
    def _generar_opinion_simple(self, decision: Decision) -> Dict:
        """Genera opinión cuando no hay otras consejeras."""
        self.opiniones_dadas += 1
        
        return {
            'consejera': self.nombre,
            'aprobada': True,
            'veto': False,
            'opinion': 'Decisión parece razonable',
            'confianza': 0.7,
            'razonamiento': ['No hay opiniones previas para sintetizar'],
            'sugerencias': []
        }
    
    def _sintetizar_opiniones(self, decision: Decision, 
                             opiniones: List[Dict]) -> Dict:
        """
        Sintetiza opiniones de todas las consejeras.
        
        Proceso:
        1. Verificar si hay vetos (Vega)
        2. Contar aprobaciones/rechazos
        3. Recopilar todas las sugerencias
        4. Evaluar nivel de consenso
        5. Generar síntesis coherente
        """
        self.opiniones_dadas += 1
        
        # 1. Verificar vetos
        tiene_veto = any(op.get('veto', False) for op in opiniones)
        
        if tiene_veto:
            # Si hay veto, Sage no puede aprobar
            veto_opinion = next(op for op in opiniones if op.get('veto'))
            return {
                'consejera': self.nombre,
                'aprobada': False,
                'veto': False,  # Sage no veta, pero respeta vetos
                'opinion': f'Veto de {veto_opinion["consejera"]} es válido',
                'confianza': 1.0,
                'razonamiento': [
                    f'{veto_opinion["consejera"]} aplicó veto',
                    'El consejo respalda la decisión de veto'
                ],
                'sugerencias': veto_opinion.get('sugerencias', [])
            }
        
        # 2. Contar aprobaciones
        aprobadas = sum(1 for op in opiniones if op.get('aprobada', False))
        total = len(opiniones)
        consenso = aprobadas / total if total > 0 else 0
        
        # 3. Recopilar sugerencias
        todas_sugerencias = []
        for op in opiniones:
            todas_sugerencias.extend(op.get('sugerencias', []))
        
        # Eliminar duplicados manteniendo orden
        sugerencias_unicas = list(dict.fromkeys(todas_sugerencias))
        
        # 4. Recopilar razonamientos
        razonamientos = []
        for op in opiniones:
            consejera = op.get('consejera', 'Desconocida')
            opinion = op.get('opinion', '')
            razonamientos.append(f'{consejera}: {opinion}')
        
        # 5. Generar síntesis
        if consenso >= 0.8:
            # Alto consenso - aprobar con confianza
            return {
                'consejera': self.nombre,
                'aprobada': True,
                'veto': False,
                'opinion': f'Consenso fuerte ({int(consenso*100)}%)',
                'confianza': min(consenso, 0.95),
                'razonamiento': ['Alto consenso entre consejeras'] + razonamientos[:3],
                'sugerencias': sugerencias_unicas[:3]
            }
        
        elif consenso >= 0.5:
            # Consenso moderado - aprobar con precaución
            return {
                'consejera': self.nombre,
                'aprobada': True,
                'veto': False,
                'opinion': f'Consenso moderado ({int(consenso*100)}%)',
                'confianza': consenso,
                'razonamiento': ['Opiniones divididas pero mayoría aprueba'] + razonamientos[:3],
                'sugerencias': sugerencias_unicas[:5]
            }
        
        else:
            # Bajo consenso - precaución
            return {
                'consejera': self.nombre,
                'aprobada': False,
                'veto': False,
                'opinion': f'Consenso insuficiente ({int(consenso*100)}%)',
                'confianza': 0.8,
                'razonamiento': ['Múltiples consejeras expresan preocupación'] + razonamientos,
                'sugerencias': sugerencias_unicas
            }