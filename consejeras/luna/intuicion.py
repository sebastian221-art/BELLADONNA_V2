"""
Luna - Consejera de Intuición.

Especialidad: Detectar patrones no obvios y señales sutiles.
Vigila: Todos los principios (perspectiva holística)
Puede vetar: NO
"""
from typing import Dict, List
from consejeras.base_consejera import Consejera
from razonamiento.tipos_decision import Decision, TipoDecision
from core.principios import Principio

class Luna(Consejera):
    """
    Luna - La Intuitiva.
    
    Detecta:
    - Patrones repetitivos
    - Incoherencias sutiles
    - Señales indirectas
    - Contextos implícitos
    
    NO veta, sugiere precaución cuando "algo no encaja".
    """
    
    def __init__(self):
        """Inicializa Luna."""
        super().__init__("Luna", "Intuición y Patrones")
        self.puede_vetar = False
        
        # Vigila TODOS los principios desde perspectiva holística
        self.principios_vigilados = list(Principio)
        
        # Patrones sospechosos
        self.palabras_urgencia_sospechosa = [
            'urgente', 'rápido', 'ya', 'ahora mismo', 'inmediatamente'
        ]
        
        self.palabras_ambiguas = [
            'todo', 'todos', 'nada', 'siempre', 'nunca', 'cualquier'
        ]
        
        self.palabras_evasivas = [
            'después', 'luego', 'tal vez', 'quizás', 'no importa'
        ]
    
    def revisar(self, decision: Decision, contexto: Dict) -> Dict:
        """
        Revisa desde intuición.
        
        Detecta patrones sutiles que otros no ven.
        """
        self.revisiones_realizadas += 1
        
        traduccion = contexto.get('traduccion', {})
        texto = traduccion.get('texto_original', '').lower()
        
        # Detectar patrones
        urgencia_sospechosa = self._detectar_urgencia_sospechosa(texto)
        tiene_ambiguedad = self._detectar_ambiguedad(texto)
        es_evasivo = self._detectar_evasion(texto)
        
        # Detectar incoherencias
        incoherencia = self._detectar_incoherencia(decision, traduccion)
        
        if urgencia_sospechosa or tiene_ambiguedad or es_evasivo or incoherencia:
            return self._generar_opinion_intuitiva(
                decision,
                urgencia_sospechosa,
                tiene_ambiguedad,
                es_evasivo,
                incoherencia
            )
        else:
            self.opiniones_dadas += 1
            return {
                'consejera': self.nombre,
                'aprobada': True,
                'veto': False,
                'opinion': 'No detecto patrones preocupantes',
                'confianza': 0.6,
                'razonamiento': ['Mensaje parece directo y coherente'],
                'sugerencias': []
            }
    
    def _detectar_urgencia_sospechosa(self, texto: str) -> bool:
        """Detecta urgencia sospechosa."""
        return any(palabra in texto for palabra in self.palabras_urgencia_sospechosa)
    
    def _detectar_ambiguedad(self, texto: str) -> bool:
        """Detecta lenguaje ambiguo."""
        return any(palabra in texto for palabra in self.palabras_ambiguas)
    
    def _detectar_evasion(self, texto: str) -> bool:
        """Detecta lenguaje evasivo."""
        return any(palabra in texto for palabra in self.palabras_evasivas)
    
    def _detectar_incoherencia(self, decision: Decision, traduccion: Dict) -> bool:
        """Detecta incoherencias entre mensaje y decisión."""
        # Incoherencia: alta confianza con palabras desconocidas
        if traduccion.get('confianza', 0) > 0.8 and \
           len(traduccion.get('palabras_desconocidas', [])) > 2:
            return True
        
        # Incoherencia: decisión afirmativa con grounding bajo
        if decision.tipo == TipoDecision.AFIRMATIVA and \
           decision.grounding_promedio < 0.7:
            return True
        
        return False
    
    def _generar_opinion_intuitiva(self, decision: Decision,
                                   urgencia: bool,
                                   ambiguedad: bool,
                                   evasion: bool,
                                   incoherencia: bool) -> Dict:
        """Genera opinión intuitiva."""
        self.opiniones_dadas += 1
        
        razonamiento = []
        sugerencias = []
        
        if urgencia:
            razonamiento.append('Detectada urgencia inusual')
            sugerencias.append('Verificar si es petición legítima')
        
        if ambiguedad:
            razonamiento.append('Lenguaje demasiado ambiguo')
            sugerencias.append('Solicitar clarificación')
        
        if evasion:
            razonamiento.append('Usuario parece evasivo')
            sugerencias.append('Proceder con precaución')
        
        if incoherencia:
            razonamiento.append('Incoherencia detectada en flujo')
            sugerencias.append('Revisar decisión cuidadosamente')
        
        señales = sum([urgencia, ambiguedad, evasion, incoherencia])
        confianza = min(0.5 + (señales * 0.12), 0.9)
        
        return {
            'consejera': self.nombre,
            'aprobada': True,  # No veta, solo advierte
            'veto': False,
            'opinion': f'Patrones sutiles detectados ({señales} señales)',
            'confianza': confianza,
            'razonamiento': razonamiento,
            'sugerencias': sugerencias
        }