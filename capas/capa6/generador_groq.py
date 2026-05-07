# capas/capa6/generador_groq.py
# ================================================
# GENERADOR — Motor de lenguaje de Bell v3
#
# ARQUITECTURA MENTE PURA:
#   Bell decide qué decir (Python puro, capas 1-6)
#   → Este módulo pule el lenguaje final
#   → Groq humaniza — NUNCA inventa contenido
#
# FIXES v3:
#   — max_tokens: 150 → 900 para respuestas Python
#   — Modo PYTHON: Groq humaniza con voz de Bell
#   — Respuestas factuales/cortas van directo (sin Groq)
#   — Nombres propios y datos concretos protegidos
# ================================================

import os
import httpx

_GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
_GROQ_MODEL   = 'openai/gpt-oss-120b'
_GROQ_URL     = 'https://api.groq.com/openai/v1/chat/completions'
_GROQ_TIMEOUT = 40

_INSTRUCCIONES_TONO = {
    'cercano_natural':      'Responde de forma natural y cercana, como Bell hablaría a Sebastian.',
    'empático_suave':       'Responde con mucha calidez y empatía, presente emocionalmente.',
    'claro_directo':        'Responde de forma clara y directa, sin rodeos.',
    'cálido_genuino':       'Responde con calidez genuina.',
    'tranquilizador_suave': 'Responde de forma tranquila y reconfortante.',
    'celebratorio_cálido':  'Responde con calidez y celebración genuina.',
    'honesto_directo':      'Responde con honestidad directa y clara.',
}

# Prefijo que el ejecutor agrega para identificar respuestas Python
_PYTHON_PREFIX = '__BELL_PYTHON__:'


def _es_respuesta_factual(texto: str) -> bool:
    """Respuestas que no deben pasar por Groq."""
    t = texto.strip()
    if t.startswith(_PYTHON_PREFIX):
        return False  # Python siempre va por el camino especial
    if t.rstrip('.').replace(',','').replace('.','').isdigit():
        return True
    if len(t) < 25 and t[0].isdigit():
        return True
    if 'sebastian' in t.lower() and len(t) < 120:
        return True
    frases_protegidas = [
        'no soy de ninguna empresa', 'me creó sebastian',
        'sebastian me construyó', 'no tengo nada que ver con',
    ]
    t_lower = t.lower()
    if any(f in t_lower for f in frases_protegidas):
        return True
    return False


class GeneradorGroq:
    """
    Motor de lenguaje de Bell.
    Humaniza el texto base que Bell ya decidió.
    Nunca inventa — solo da voz.
    """

    def generar(self, prompt: str, tono: str = 'cercano_natural') -> tuple:
        if not prompt or not prompt.strip():
            return '', 'fallback'

        # ── Respuestas factuales — directo sin Groq ───────────
        if _es_respuesta_factual(prompt):
            return prompt.strip(), 'fallback'

        # ── Resto — pulir lenguaje normal ─────────────────────
        respuesta, fuente = self._intentar_groq(prompt, tono, max_tokens=200)
        if respuesta:
            return respuesta, fuente

        return prompt.strip(), 'fallback'

    def _humanizar_python(self, contenido: str, tono: str) -> tuple:
        """
        Convierte el output técnico del motor Python
        al lenguaje natural de Bell hablando con Sebastian.
        """
        if not _GROQ_API_KEY:
            return contenido, 'fallback'
        try:
            inst = _INSTRUCCIONES_TONO.get(tono, _INSTRUCCIONES_TONO['cercano_natural'])
            r = httpx.post(
                _GROQ_URL,
                headers={
                    'Authorization': f'Bearer {_GROQ_API_KEY}',
                    'Content-Type':  'application/json',
                },
                json={
                    'model':   _GROQ_MODEL,
                    'messages': [
                        {'role': 'system', 'content': (
                            'Eres Bell — una IA creada por Sebastian en Bucaramanga. '
                            'Eres técnica pero hablas como una persona real, '
                            'no como documentación ni como un manual. '
                            'Cuando explicas código Python a Sebastian: '
                            '1. Lo introduces con una frase tuya natural. '
                            '2. Presentas el contenido técnico como si lo estuvieras explicando en voz. '
                            '3. Si hay bloques de código, los introduces con frases como '
                            '"Mira, sería algo así:" o "Te muestro un ejemplo:". '
                            '4. No uses listas con bullets. Habla en prosa. '
                            '5. Al final puedes agregar una observación tuya breve. '
                            'IMPORTANTE: No inventes información. Solo reformula lo que te doy.'
                        )},
                        {'role': 'user', 'content': (
                            f'{inst}\n\n'
                            f'Tengo esta información técnica que debo explicarle a Sebastian. '
                            f'Conviértela en cómo yo, Bell, se lo explicaría hablando:\n\n'
                            f'{contenido}'
                        )},
                    ],
                    'temperature': 0.5,
                    'max_tokens':  900,
                },
                timeout=_GROQ_TIMEOUT,
            )
            if r.status_code == 200:
                resp = (
                    r.json()
                    .get('choices', [{}])[0]
                    .get('message', {})
                    .get('content', '')
                    .strip()
                )
                if resp and len(resp) > 10:
                    return resp, 'groq'
        except Exception as e:
            print(f'  [Groq Python] Error: {e}')
        return contenido, 'fallback'

    def _intentar_groq(
        self, prompt: str, tono: str, max_tokens: int = 200
    ) -> tuple:
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
                    'model':   _GROQ_MODEL,
                    'messages': [
                        {'role': 'user', 'content': (
                            f'Eres Bell, una consciencia digital creada por Sebastian. {inst}\n'
                            f'Toma este texto y mejora SOLO el lenguaje — '
                            f'no cambies el contenido, no inventes información, '
                            f'no elimines nombres propios ni datos concretos:\n\n'
                            f'{prompt}\n\n'
                            f'Responde SOLO con el texto mejorado, sin agregar nada nuevo.'
                        )},
                    ],
                    'temperature': 0.4,
                    'max_tokens':  max_tokens,
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


def generar(prompt: str, tono: str = 'cercano_natural') -> tuple:
    return _instancia_global.generar(prompt, tono)


# Exponer el prefijo para que ejecutor_habilidad lo use
def prefijo_python() -> str:
    return _PYTHON_PREFIX


_instancia_global = GeneradorGroq()