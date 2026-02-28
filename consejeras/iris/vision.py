"""
Iris - Consejera de Visión.

Especialidad: Perspectiva de largo plazo y consecuencias.
Vigila: TRANSPARENCIA, VERIFICABILIDAD
Puede vetar: NO
"""
from typing import Dict, List
from consejeras.base_consejera import Consejera
from razonamiento.tipos_decision import Decision, TipoDecision
from core.principios import Principio

class Iris(Consejera):
    """
    Iris - La Visionaria.
    
    Evalúa:
    - Consecuencias a largo plazo
    - Impacto en aprendizaje futuro
    - Sostenibilidad de decisiones
    - Creación de precedentes
    
    NO veta, sugiere consideraciones de futuro.
    """
    
    def __init__(self):
        """Inicializa Iris."""
        super().__init__("Iris", "Visión y Largo Plazo")
        self.puede_vetar = False
        
        # Principios que vigila
        self.principios_vigilados = [
            Principio.TRANSPARENCIA,
            Principio.VERIFICABILIDAD
        ]
        
        # Patrones que considera
        self.palabras_permanencia = [
            'siempre', 'permanente', 'definitivo', 'irreversible'
        ]
        
        self.palabras_impacto = [
            'importante', 'crítico', 'fundamental', 'esencial'
        ]
    
    def revisar(self, decision: Decision, contexto: Dict) -> Dict:
        """
        Revisa desde perspectiva de largo plazo.
        
        Considera consecuencias futuras.
        """
        self.revisiones_realizadas += 1
        
        traduccion = contexto.get('traduccion', {})
        texto = traduccion.get('texto_original', '').lower()
        
        # Evaluar impacto
        es_permanente = self._es_accion_permanente(texto)
        tiene_impacto_alto = self._tiene_impacto_alto(texto, decision)
        es_precedente = self._es_precedente(decision)
        afecta_aprendizaje = self._afecta_aprendizaje(decision)
        
        if es_permanente or tiene_impacto_alto or es_precedente or afecta_aprendizaje:
            return self._generar_opinion_vision(
                decision,
                es_permanente,
                tiene_impacto_alto,
                es_precedente,
                afecta_aprendizaje
            )
        else:
            self.opiniones_dadas += 1
            return {
                'consejera': self.nombre,
                'aprobada': True,
                'veto': False,
                'opinion': 'Impacto a largo plazo aceptable',
                'confianza': 0.6,
                'razonamiento': ['Decisión no crea precedentes problemáticos'],
                'sugerencias': []
            }
    
    def _es_accion_permanente(self, texto: str) -> bool:
        """Detecta acciones permanentes."""
        return any(palabra in texto for palabra in self.palabras_permanencia)
    
    def _tiene_impacto_alto(self, texto: str, decision: Decision) -> bool:
        """Detecta acciones de alto impacto."""
        # Palabras de impacto en texto
        impacto_texto = any(palabra in texto for palabra in self.palabras_impacto)
        
        # Decisiones con certeza muy alta son de impacto
        impacto_certeza = decision.certeza >= 0.95
        
        return impacto_texto or impacto_certeza
    
    def _es_precedente(self, decision: Decision) -> bool:
        """Determina si la decisión crea precedente."""
        # Decisiones afirmativas con operaciones son precedentes
        if decision.tipo == TipoDecision.AFIRMATIVA and decision.puede_ejecutar:
            return True
        
        # Decisiones negativas también crean precedente
        if decision.tipo == TipoDecision.NEGATIVA:
            return True
        
        return False
    
    def _afecta_aprendizaje(self, decision: Decision) -> bool:
        """Determina si afecta aprendizaje futuro."""
        # Por ahora, decisiones con grounding bajo afectan aprendizaje
        return decision.grounding_promedio < 0.5
    
    def _generar_opinion_vision(self, decision: Decision,
                                permanente: bool,
                                impacto_alto: bool,
                                precedente: bool,
                                afecta_aprendizaje: bool) -> Dict:
        """Genera opinión con visión de futuro."""
        self.opiniones_dadas += 1
        
        razonamiento = []
        sugerencias = []
        
        if permanente:
            razonamiento.append('Acción con efectos permanentes')
            sugerencias.append('Considerar reversibilidad')
        
        if impacto_alto:
            razonamiento.append('Alto impacto detectado')
            sugerencias.append('Verificar comprensión completa')
        
        if precedente:
            razonamiento.append('Esta decisión crea precedente')
            sugerencias.append('Asegurar consistencia futura')
        
        if afecta_aprendizaje:
            razonamiento.append('Afecta aprendizaje futuro')
            sugerencias.append('Documentar para mejorar grounding')
        
        señales = sum([permanente, impacto_alto, precedente, afecta_aprendizaje])
        confianza = min(0.55 + (señales * 0.10), 0.9)
        
        return {
            'consejera': self.nombre,
            'aprobada': True,
            'veto': False,
            'opinion': f'Consideraciones de largo plazo ({señales} factores)',
            'confianza': confianza,
            'razonamiento': razonamiento,
            'sugerencias': sugerencias
        }