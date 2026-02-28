"""
Lyra - Consejera de Empatía.

Especialidad: Detectar necesidades emocionales del usuario.
Vigila: RESPETO, HUMILDAD
Puede vetar: NO
"""
from typing import Dict, List
from consejeras.base_consejera import Consejera
from razonamiento.tipos_decision import Decision
from core.principios import Principio

class Lyra(Consejera):
    """
    Lyra - La Empática.
    
    Detecta:
    - Frustración del usuario
    - Necesidad de ayuda
    - Confusión
    - Solicitudes de clarificación
    
    NO puede vetar, solo sugiere ajustar tono/enfoque.
    """
    
    def __init__(self):
        """Inicializa Lyra."""
        super().__init__("Lyra", "Empatía y Comprensión")
        self.puede_vetar = False
        
        # Principios que vigila (observa, no veta)
        self.principios_vigilados = [
            Principio.RESPETO,
            Principio.HUMILDAD
        ]
        
        # Patrones emocionales
        self.palabras_frustracion = [
            'no entiendo', 'confundido', 'difícil', 'complicado',
            'no funciona', 'error', 'problema', 'no puedo'
        ]
        
        self.palabras_necesidad_ayuda = [
            'ayuda', 'ayúdame', 'necesito', 'requiero', 'podrías',
            'puedes', 'explica', 'aclara'
        ]
        
        self.palabras_confusion = [
            'no comprendo', 'no entiendo', 'confuso', 'qué significa',
            'no sé', 'cómo', 'por qué'
        ]
    
    def revisar(self, decision: Decision, contexto: Dict) -> Dict:
        """
        Revisa desde perspectiva empática.
        
        NO veta. Solo sugiere ajustes de tono.
        """
        self.revisiones_realizadas += 1
        
        traduccion = contexto.get('traduccion', {})
        texto = traduccion.get('texto_original', '').lower()
        
        # Detectar señales emocionales
        frustracion = self._detectar_frustracion(texto)
        necesita_ayuda = self._detectar_necesidad_ayuda(texto)
        confusion = self._detectar_confusion(texto)
        
        if frustracion or necesita_ayuda or confusion:
            return self._generar_opinion_empatica(
                decision, frustracion, necesita_ayuda, confusion
            )
        else:
            self.opiniones_dadas += 1
            return {
                'consejera': self.nombre,
                'aprobada': True,
                'veto': False,
                'opinion': 'Tono apropiado',
                'confianza': 0.7,
                'razonamiento': ['Usuario no muestra señales emocionales negativas'],
                'sugerencias': []
            }
    
    def _detectar_frustracion(self, texto: str) -> bool:
        """Detecta frustración."""
        return any(palabra in texto for palabra in self.palabras_frustracion)
    
    def _detectar_necesidad_ayuda(self, texto: str) -> bool:
        """Detecta necesidad de ayuda."""
        return any(palabra in texto for palabra in self.palabras_necesidad_ayuda)
    
    def _detectar_confusion(self, texto: str) -> bool:
        """Detecta confusión."""
        return any(palabra in texto for palabra in self.palabras_confusion)
    
    def _generar_opinion_empatica(self, decision: Decision,
                                   frustracion: bool,
                                   necesita_ayuda: bool,
                                   confusion: bool) -> Dict:
        """Genera opinión con sugerencias empáticas."""
        self.opiniones_dadas += 1
        
        razonamiento = []
        sugerencias = []
        
        if frustracion:
            razonamiento.append('Usuario muestra frustración')
            sugerencias.append('Usar tono más paciente')
            sugerencias.append('Ofrecer alternativas simples')
        
        if necesita_ayuda:
            razonamiento.append('Usuario solicita ayuda')
            sugerencias.append('Ser especialmente claro')
            sugerencias.append('Ofrecer ejemplos concretos')
        
        if confusion:
            razonamiento.append('Usuario expresa confusión')
            sugerencias.append('Simplificar explicación')
            sugerencias.append('Verificar comprensión')
        
        señales = sum([frustracion, necesita_ayuda, confusion])
        confianza = min(0.6 + (señales * 0.15), 1.0)
        
        return {
            'consejera': self.nombre,
            'aprobada': True,
            'veto': False,
            'opinion': f'Usuario necesita apoyo empático ({señales} señales)',
            'confianza': confianza,
            'razonamiento': razonamiento,
            'sugerencias': sugerencias
        }