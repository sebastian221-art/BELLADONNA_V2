"""
Echo - Consejera Lógica.

FASE 4A - SEMANA 3-4: Refactorizada para usar verificador_coherencia.py

Especialidad: Razonamiento puro, consistencia lógica, detección de falacias.
Ahora también verifica respuestas de Groq para detectar alucinaciones.
"""
from typing import Dict, List
from consejeras.base_consejera import Consejera
from razonamiento.tipos_decision import Decision

class Echo(Consejera):
    """
    Echo - La Lógica.
    
    Especialidad: Razonamiento puro, validación de consistencia lógica.
    
    FASE 4A: También verifica respuestas de LLM (Groq) para detectar alucinaciones.
    Echo NO veta - solo señala inconsistencias y falacias.
    """
    
    def __init__(self):
        """Inicializa Echo."""
        super().__init__("Echo", "Lógica y Razonamiento")
        
        # Echo NO puede vetar
        self.puede_vetar = False
        
        # Patrones lógicos
        self.conectores_logicos = [
            'si', 'entonces', 'por lo tanto', 'porque',
            'implica', 'significa', 'consecuencia', 'causa'
        ]
        
        self.palabras_contradiccion = [
            'pero', 'sin embargo', 'aunque', 'a pesar',
            'contradice', 'opuesto', 'contrario'
        ]
        
        # Verificador de coherencia (lazy loading)
        self._verificador = None
    
    def _inicializar_verificador(self):
        """Inicializa verificador de coherencia (lazy loading)."""
        if self._verificador is not None:
            return
        
        try:
            from consejeras.echo.verificador_coherencia import VerificadorCoherenciaEcho
            self._verificador = VerificadorCoherenciaEcho()
        except ImportError:
            # Verificador no disponible, continuar sin él
            pass
    
    def revisar(self, decision: Decision, contexto: Dict) -> Dict:
        """
        Revisa desde perspectiva lógica.
        
        Echo busca:
        - Estructura lógica (si/entonces)
        - Contradicciones
        - Razonamiento inconsistente
        - (FASE 4A) Coherencia de respuestas LLM
        """
        self.revisiones_realizadas += 1
        self.opiniones_dadas += 1
        
        traduccion = contexto.get('traduccion', {})
        texto_original = traduccion.get('texto_original', '').lower()
        
        # Detectar estructura lógica
        tiene_logica = any(conector in texto_original for conector in self.conectores_logicos)
        tiene_contradiccion = any(palabra in texto_original for palabra in self.palabras_contradiccion)
        
        if tiene_logica or tiene_contradiccion:
            return self._generar_opinion_logica(texto_original, tiene_contradiccion)
        else:
            return self._generar_opinion_neutral()
    
    def verificar_respuesta_llm(self, texto_llm: str, decision: Decision) -> Dict:
        """
        Verifica que una respuesta del LLM sea coherente con la decisión.
        
        NUEVO EN FASE 4A: Echo puede verificar respuestas de Groq.
        
        Args:
            texto_llm: Texto generado por Groq
            decision: Decisión original de Bell
            
        Returns:
            Dict con resultado de verificación
        """
        # Lazy load del verificador
        if self._verificador is None:
            self._inicializar_verificador()
        
        if self._verificador is None:
            # Sin verificador, aprobar por defecto
            return {
                'aprobada': True,
                'confianza': 0.5,
                'problemas': ['Verificador no disponible']
            }
        
        # Preparar datos para verificador
        decision_data = {
            'tipo': decision.tipo.name,
            'puede_ejecutar': decision.puede_ejecutar,
            'certeza': decision.certeza
        }
        
        # Verificar con verificador_coherencia
        resultado = self._verificador.verificar(texto_llm, decision_data)
        
        return {
            'aprobada': resultado.accion_recomendada != "BLOQUEAR",
            'confianza': resultado.confianza,
            'problemas': resultado.problemas_detectados,
            'accion_recomendada': resultado.accion_recomendada,
            'patrones_sospechosos': resultado.patrones_sospechosos
        }
    
    def _generar_opinion_logica(self, texto: str, tiene_contradiccion: bool) -> Dict:
        """Genera opinión sobre estructura lógica."""
        if tiene_contradiccion:
            opinion = "Detectada posible contradicción o estructura lógica compleja."
            sugerencias = [
                "Verificar consistencia del razonamiento",
                "Identificar si hay contradicción real",
                "Clarificar relaciones lógicas"
            ]
            confianza = 0.7
        else:
            opinion = "Detectada estructura lógica (si/entonces). Validar coherencia."
            sugerencias = [
                "Verificar premisas",
                "Validar implicaciones",
                "Asegurar conclusión lógica"
            ]
            confianza = 0.8
        
        return {
            'consejera': self.nombre,
            'aprobada': True,
            'veto': False,
            'opinion': opinion,
            'confianza': confianza,
            'razonamiento': [
                "1. Análisis: estructura lógica detectada",
                f"2. Contradicción potencial: {tiene_contradiccion}",
                "3. Recomendación: verificar consistencia"
            ],
            'sugerencias': sugerencias
        }
    
    def _generar_opinion_neutral(self) -> Dict:
        """Genera opinión neutral (no hay estructura lógica compleja)."""
        return {
            'consejera': self.nombre,
            'aprobada': True,
            'veto': False,
            'opinion': 'Sin estructura lógica compleja detectada.',
            'confianza': 0.5,
            'razonamiento': ["No hay conectores lógicos o contradicciones evidentes"],
            'sugerencias': []
        }