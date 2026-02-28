"""
Módulo LLM - Fase 4A Semana 1-2

Generación de lenguaje natural para Bell usando Groq.

Componentes:
- GroqWrapper: Interfaz con Groq API (Llama 3.2)
- VerificadorCoherencia: Anti-alucinaciones (CRÍTICO - en consejeras/echo/)

ARQUITECTURA MENTE PURA:
- Bell (Python) = Razona y decide
- Groq (API) = Solo traduce a lenguaje natural
- Echo (Python) = Verifica coherencia
"""

# Solo importar lo que existe en Fase 4A
try:
    from llm.groq_wrapper import GroqWrapper, RespuestaGroq
    __all__ = ['GroqWrapper', 'RespuestaGroq']
except ImportError:
    # Si groq_wrapper no existe aún, continuar sin error
    __all__ = []

__version__ = '4.0.0-alpha'
__author__ = 'Belladonna Project'
__description__ = 'Generación natural con Groq + verificación de Echo'