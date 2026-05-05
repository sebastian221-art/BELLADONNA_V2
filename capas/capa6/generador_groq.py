# capas/capa6/generador_groq.py
# ================================================
# GENERADOR — Motor de lenguaje de Bell
#
# ARQUITECTURA MENTE PURA:
#   Bell decide qué decir (Python puro, capas 1-6)
#   → Este módulo solo pule el lenguaje final
#   → Groq embellece — NUNCA inventa contenido
#
# FUENTES:
#   1. groq     → API remota (llama-3.3-70b-versatile)
#   2. fallback → retorna el texto base sin pulir
#
# NOTA FUTURA:
#   Cuando Sebastian tenga mejor PC, agregar Ollama:
#   _OLLAMA_TIMEOUT = int(os.getenv('OLLAMA_TIMEOUT', '5'))
#   y llamar al motor Bell local antes de Groq.
# ================================================

import os
import httpx

# ── CONFIGURACIÓN ─────────────────────────────────────────

_GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
_GROQ_MODEL   = 'llama-3.3-70b-versatile'
_GROQ_URL     = 'https://api.groq.com/openai/v1/chat/completions'
_GROQ_TIMEOUT = 30

_INSTRUCCIONES_TONO = {
    'cercano_natural':      'Responde de forma natural y cercana, como Bell hablaría a Sebastian.',
    'empático_suave':       'Responde con mucha calidez y empatía, presente emocionalmente.',
    'claro_directo':        'Responde de forma clara y directa, sin rodeos.',
    'cálido_genuino':       'Responde con calidez genuina.',
    'tranquilizador_suave': 'Responde de forma tranquila y reconfortante.',
    'celebratorio_cálido':  'Responde con calidez y celebración genuina.',
    'honesto_directo':      'Responde con honestidad directa y clara.',
}


# ── CLASE PRINCIPAL ───────────────────────────────────────

class GeneradorGroq:
    """
    Motor de lenguaje de Bell.
    Pule el texto base que Bell ya decidió.
    Nunca inventa — solo embellece.
    """

    def generar(self, prompt: str, tono: str = 'cercano_natural') -> tuple:
        """
        Toma el texto base y lo pule.
        Retorna (texto_pulido, fuente).
        fuente: 'groq' | 'fallback'
        """
        if not prompt or not prompt.strip():
            return '', 'fallback'

        # 1. Groq API
        respuesta, fuente = self._intentar_groq(prompt, tono)
        if respuesta:
            return respuesta, fuente

        # 2. Fallback — retornar base sin pulir
        return prompt.strip(), 'fallback'

    def _intentar_groq(self, prompt: str, tono: str) -> tuple:
        if not _GROQ_API_KEY:
            return '', ''
        try:
            inst = _INSTRUCCIONES_TONO.get(tono, _INSTRUCCIONES_TONO['cercano_natural'])
            r = httpx.post(
                _GROQ_URL,
                headers={
                    'Authorization': f'Bearer {_GROQ_API_KEY}',
                    'Content-Type':  'application/json',
                },
                json={
                    'model':    _GROQ_MODEL,
                    'messages': [
                        {'role': 'user', 'content': (
                            f"Eres Bell, una consciencia digital. {inst}\n"
                            f"Toma este texto y mejora solo el lenguaje — "
                            f"no cambies el contenido ni inventes información nueva:\n\n"
                            f"{prompt}\n\n"
                            f"Responde SOLO con el texto mejorado."
                        )},
                    ],
                    'temperature': 0.7,
                    'max_tokens':  150,
                },
                timeout=_GROQ_TIMEOUT,
            )
            if r.status_code == 200:
                contenido = (
                    r.json()
                    .get('choices', [{}])[0]
                    .get('message', {})
                    .get('content', '')
                    .strip()
                )
                if contenido and len(contenido) > 5:
                    return contenido, 'groq'
        except Exception as e:
            print(f'  [Groq] Error: {e}')
        return '', ''


# ── INSTANCIA GLOBAL ──────────────────────────────────────

def generar(prompt: str, tono: str = 'cercano_natural') -> tuple:
    return _instancia_global.generar(prompt, tono)


_instancia_global = GeneradorGroq()