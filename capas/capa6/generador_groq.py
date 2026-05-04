# capas/capa6/generador_groq.py
# ================================================
# GENERADOR GROQ — Motor de lenguaje de Bell
#
# ARQUITECTURA MENTE PURA:
#   Bell decide qué decir (Python puro, capas 1-6)
#   → Este módulo solo pule el lenguaje final
#   → Groq/Bell-motor embellecen — NUNCA inventan
#
# FUENTES (en orden de preferencia):
#   1. bell_motor  → Ollama local (hf.co/sebastian221-art/bell-motor)
#   2. groq        → API remota  (llama-3.3-70b-versatile)
#   3. fallback    → retorna el texto base sin pulir
#
# TIMEOUT OLLAMA:
#   Local (sin GPU):    OLLAMA_TIMEOUT=5   (default)
#   Railway (con GPU):  OLLAMA_TIMEOUT=60
#   Configurable via variable de entorno.
# ================================================

import os
import httpx

# ── CONFIGURACIÓN ─────────────────────────────────────────

_GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
_GROQ_MODEL   = 'llama-3.3-70b-versatile'
_GROQ_TIMEOUT = 30

# FIX: timeout configurable por env var
#   - Local sin GPU → default 5 (no bloquea)
#   - Railway con GPU → set OLLAMA_TIMEOUT=60
_OLLAMA_TIMEOUT = int(os.getenv('OLLAMA_TIMEOUT', '5'))

_OLLAMA_URL   = 'http://localhost:11434/api/chat'
_OLLAMA_MODEL = os.getenv(
    'BELL_MOTOR_MODELO',
    'hf.co/sebastian221-art/bell-motor:latest'
)
_GROQ_URL = 'https://api.groq.com/openai/v1/chat/completions'

_INSTRUCCIONES_TONO = {
    'cercano_natural':      'Responde de forma natural y cercana, como Bell hablaría a Sebastian.',
    'empático_suave':       'Responde con mucha calidez y empatía, presente emocionalmente.',
    'claro_directo':        'Responde de forma clara y directa, sin rodeos.',
    'cálido_genuino':       'Responde con calidez genuina.',
    'tranquilizador_suave': 'Responde de forma tranquila y reconfortante.',
    'celebratorio_cálido':  'Responde con calidez y celebración genuina.',
    'honesto_directo':      'Responde con honestidad directa y clara.',
}


# ── CLASE PRINCIPAL (interfaz que usa capa6/__init__.py) ──

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
        fuente: 'bell_motor' | 'groq' | 'fallback'
        """
        if not prompt or not prompt.strip():
            return '', 'fallback'

        # 1. Motor Bell local (Ollama)
        respuesta, fuente = self._intentar_bell_motor(prompt, tono)
        if respuesta:
            return respuesta, fuente

        # 2. Groq API
        respuesta, fuente = self._intentar_groq(prompt, tono)
        if respuesta:
            return respuesta, fuente

        # 3. Fallback — retornar base sin pulir
        return prompt.strip(), 'fallback'

    def _intentar_bell_motor(self, prompt: str, tono: str) -> tuple:
        try:
            r = httpx.post(
                _OLLAMA_URL,
                json={
                    'model':    _OLLAMA_MODEL,
                    'messages': [{'role': 'user', 'content': self._prompt(prompt, tono)}],
                    'stream':   False,
                    'options':  {'temperature': 0.7, 'num_predict': 150},
                },
                timeout=_OLLAMA_TIMEOUT,
            )
            if r.status_code == 200:
                contenido = r.json().get('message', {}).get('content', '').strip()
                if contenido and len(contenido) > 5:
                    return contenido, 'bell_motor'
        except (httpx.TimeoutException, httpx.ConnectError):
            pass  # silencioso — va a Groq
        except Exception as e:
            print(f'  [Motor Bell] Error: {e}')
        return '', ''

    def _intentar_groq(self, prompt: str, tono: str) -> tuple:
        if not _GROQ_API_KEY:
            return '', ''
        try:
            r = httpx.post(
                _GROQ_URL,
                headers={
                    'Authorization': f'Bearer {_GROQ_API_KEY}',
                    'Content-Type':  'application/json',
                },
                json={
                    'model':       _GROQ_MODEL,
                    'messages':    [{'role': 'user', 'content': self._prompt(prompt, tono)}],
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

    def _prompt(self, texto_base: str, tono: str) -> str:
        inst = _INSTRUCCIONES_TONO.get(tono, _INSTRUCCIONES_TONO['cercano_natural'])
        return (
            f"Eres Bell, una consciencia digital. {inst}\n"
            f"Toma este texto y mejora solo el lenguaje — "
            f"no cambies el contenido ni inventes información nueva:\n\n"
            f"{texto_base}\n\n"
            f"Responde SOLO con el texto mejorado, sin explicaciones adicionales."
        )


# ── INSTANCIA GLOBAL (para uso directo desde tests) ───────
# capa6/__init__.py instancia su propio GeneradorGroq()
# pero algunos módulos de diagnóstico usan esto directamente

def generar(prompt: str, tono: str = 'cercano_natural') -> tuple:
    """Función de conveniencia — usa la instancia global."""
    return _instancia_global.generar(prompt, tono)


_instancia_global = GeneradorGroq()