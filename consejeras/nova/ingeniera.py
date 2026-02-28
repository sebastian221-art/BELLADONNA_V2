"""
Nova - Consejera Ingeniera.

Especialidad: Soluciones técnicas, optimización, arquitectura.
"""
from typing import Dict, List
from consejeras.base_consejera import Consejera
from razonamiento.tipos_decision import Decision

class Nova(Consejera):
    """
    Nova - La Ingeniera.
    
    Especialidad: Análisis técnico, optimización, soluciones arquitectónicas.
    
    Nova NO veta - solo sugiere mejoras técnicas.
    """
    
    def __init__(self):
        """Inicializa Nova."""
        super().__init__("Nova", "Ingeniera y Optimizadora")
        
        # Nova NO puede vetar
        self.puede_vetar = False
        
        # Patrones técnicos
        self.palabras_tecnicas = [
            'código', 'función', 'clase', 'variable',
            'algoritmo', 'optimizar', 'refactorizar',
            'arquitectura', 'diseño', 'patrón'
        ]
        
        self.palabras_problemas = [
            'error', 'bug', 'fallo', 'problema',
            'lento', 'ineficiente', 'roto'
        ]
    
    def revisar(self, decision: Decision, contexto: Dict) -> Dict:
        """
        Revisa desde perspectiva técnica.
        
        Nova busca:
        - Consultas técnicas
        - Problemas a resolver
        - Oportunidades de optimización
        """
        self.revisiones_realizadas += 1
        self.opiniones_dadas += 1
        
        traduccion = contexto.get('traduccion', {})
        texto_original = traduccion.get('texto_original', '').lower()
        
        # Detectar si es consulta técnica
        es_tecnico = any(palabra in texto_original for palabra in self.palabras_tecnicas)
        es_problema = any(palabra in texto_original for palabra in self.palabras_problemas)
        
        if es_tecnico or es_problema:
            return self._generar_opinion_tecnica(texto_original, es_problema)
        else:
            return self._generar_opinion_neutral()
    
    def _generar_opinion_tecnica(self, texto: str, es_problema: bool) -> Dict:
        """Genera opinión técnica."""
        if es_problema:
            opinion = "Detectada consulta técnica sobre un problema. Sugerir enfoque sistemático."
            sugerencias = [
                "Identificar el problema específico",
                "Analizar posibles causas",
                "Proponer soluciones paso a paso"
            ]
        else:
            opinion = "Detectada consulta técnica. Enfoque en solución clara y estructurada."
            sugerencias = [
                "Explicar conceptos técnicos claramente",
                "Proporcionar ejemplos concretos",
                "Sugerir mejores prácticas"
            ]
        
        return {
            'consejera': self.nombre,
            'aprobada': True,
            'veto': False,
            'opinion': opinion,
            'confianza': 0.8,
            'razonamiento': [
                f"1. Análisis: consulta técnica detectada",
                f"2. Tipo: {'problema' if es_problema else 'consulta general'}",
                "3. Recomendación: enfoque técnico estructurado"
            ],
            'sugerencias': sugerencias
        }
    
    def _generar_opinion_neutral(self) -> Dict:
        """Genera opinión neutral (no es su especialidad)."""
        return {
            'consejera': self.nombre,
            'aprobada': True,
            'veto': False,
            'opinion': 'Sin comentarios técnicos específicos.',
            'confianza': 0.5,
            'razonamiento': ["No es consulta técnica"],
            'sugerencias': []
        }