"""
Evaluador de Capacidades - ¿Bell PUEDE hacer algo?

Este módulo determina si Bell tiene la capacidad REAL de hacer algo
basándose en el grounding de conceptos.
"""
from typing import List, Dict, Optional, Tuple
from core.concepto_anclado import ConceptoAnclado

class EvaluadorCapacidades:
    """
    Evalúa si Bell puede ejecutar una acción basándose en conceptos.
    
    NO es magia. Es evaluación lógica de grounding y operaciones.
    """
    
    # Umbrales de confianza
    UMBRAL_GROUNDING_ALTO = 0.9   # Puede ejecutar con confianza
    UMBRAL_GROUNDING_MEDIO = 0.7  # Puede intentar, advertir
    UMBRAL_GROUNDING_BAJO = 0.5   # No puede ejecutar
    
    def __init__(self):
        """Inicializa evaluador."""
        pass
    
    def evaluar_capacidad_accion(self, 
                                 conceptos: List[ConceptoAnclado]) -> Dict:
        """
        Evalúa si Bell puede realizar una acción basándose en conceptos.
        
        Args:
            conceptos: Lista de ConceptosAnclados traducidos
            
        Returns:
            {
                'puede_ejecutar': bool,
                'confianza': float,
                'operacion': str or None,
                'concepto_clave': ConceptoAnclado or None,
                'razon': str,
                'groundings': List[float]
            }
        """
        if not conceptos:
            return {
                'puede_ejecutar': False,
                'confianza': 0.0,
                'operacion': None,
                'concepto_clave': None,
                'razon': 'No hay conceptos para evaluar',
                'groundings': []
            }
        
        # Buscar concepto de acción principal (con mayor grounding)
        concepto_principal = max(conceptos, key=lambda c: c.confianza_grounding)
        
        # Extraer groundings
        groundings = [c.confianza_grounding for c in conceptos]
        grounding_promedio = sum(groundings) / len(groundings)
        
        # ¿Tiene operaciones ejecutables?
        tiene_operaciones = len(concepto_principal.operaciones) > 0
        
        # Decidir
        if concepto_principal.confianza_grounding >= self.UMBRAL_GROUNDING_ALTO and \
           tiene_operaciones:
            # PUEDE ejecutar con confianza
            operacion = list(concepto_principal.operaciones.keys())[0]
            return {
                'puede_ejecutar': True,
                'confianza': concepto_principal.confianza_grounding,
                'operacion': operacion,
                'concepto_clave': concepto_principal,
                'razon': f'Grounding alto ({concepto_principal.confianza_grounding}) con operación ejecutable',
                'groundings': groundings
            }
        
        elif concepto_principal.confianza_grounding >= self.UMBRAL_GROUNDING_MEDIO and \
             tiene_operaciones:
            # PUEDE ejecutar con advertencia
            operacion = list(concepto_principal.operaciones.keys())[0]
            return {
                'puede_ejecutar': True,
                'confianza': concepto_principal.confianza_grounding,
                'operacion': operacion,
                'concepto_clave': concepto_principal,
                'razon': f'Grounding medio ({concepto_principal.confianza_grounding}), puede intentar',
                'groundings': groundings
            }
        
        else:
            # NO puede ejecutar
            if not tiene_operaciones:
                razon = f'Concepto "{concepto_principal.id}" no tiene operaciones ejecutables'
            else:
                razon = f'Grounding muy bajo ({concepto_principal.confianza_grounding})'
            
            return {
                'puede_ejecutar': False,
                'confianza': concepto_principal.confianza_grounding,
                'operacion': None,
                'concepto_clave': concepto_principal,
                'razon': razon,
                'groundings': groundings
            }
    
    def verificar_requisitos(self, 
                            concepto: ConceptoAnclado,
                            conceptos_disponibles: List[ConceptoAnclado]) -> Tuple[bool, List[str]]:
        """
        Verifica si están presentes los conceptos requeridos.
        
        Args:
            concepto: Concepto principal a evaluar
            conceptos_disponibles: Conceptos detectados en la frase
            
        Returns:
            (todos_presentes: bool, faltantes: List[str])
        """
        if 'requiere' not in concepto.relaciones:
            return (True, [])
        
        requeridos = concepto.relaciones['requiere']
        disponibles_ids = {c.id for c in conceptos_disponibles}
        
        faltantes = [req for req in requeridos if req not in disponibles_ids]
        
        return (len(faltantes) == 0, faltantes)
    
    def calcular_confianza_total(self, 
                                 conceptos: List[ConceptoAnclado]) -> float:
        """
        Calcula confianza total de una traducción.
        
        Penaliza si hay conceptos con grounding bajo.
        """
        if not conceptos:
            return 0.0
        
        groundings = [c.confianza_grounding for c in conceptos]
        
        # Promedio ponderado (dar más peso a groundings altos)
        promedio = sum(groundings) / len(groundings)
        
        # Penalizar si hay algún grounding muy bajo
        minimo = min(groundings)
        if minimo < 0.3:
            promedio *= 0.7  # Reducir 30%
        
        return round(promedio, 2)