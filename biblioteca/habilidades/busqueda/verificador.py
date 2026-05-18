# biblioteca/habilidades/busqueda/verificador.py
# ============================================================
# VERIFICADOR DE HECHOS — L8
#
# Bell verifica datos que Sebastian afirma.
# Si Sebastian dice "fyi: Python se creó en 1985",
# Bell busca silenciosamente y corrige con fuente
# si el dato es incorrecto.
#
# NIVEL 8 — Verificación honesta de datos
# ============================================================

import os
import re
import httpx

_GROQ_URL   = 'https://api.groq.com/openai/v1/chat/completions'
_GROQ_MODEL = 'openai/gpt-oss-120b'
_GROQ_KEY   = os.getenv('GROQ_API_KEY', '')

# Patrones que indican afirmación verificable
_PATRONES_AFIRMACION = [
    r'fyi[:\s]',
    r'tip[:\s]',
    r'dato[:\s]',
    r'sabias?\s+que',
    r'lei\s+que',
    r'escuche\s+que',
    r'dicen\s+que',
    r'\bse\s+(creo|fundo|invento|descubrio|nacio)\s+en\s+\d{4}',
    r'\bfue\s+(creado|fundado|inventado)\s+(en|por)',
    r'\bes\s+(?:de|del|la capital de)\s+',
    r'\btiene\s+\d+\s+(años?|habitantes|km)',
]


def _es_verificable(texto: str) -> bool:
    """Detecta si el texto contiene una afirmación verificable."""
    tl = texto.lower()
    return any(re.search(p, tl) for p in _PATRONES_AFIRMACION)


def _extraer_claim(texto: str) -> str:
    """Extrae el claim factual del texto para buscar."""
    tl = texto.lower().strip()
    for prefijo in ('fyi:', 'fyi :', 'tip:', 'dato:', 'recuerda:', 'nota:',
                    'sabías que', 'sabes que', 'leí que', 'escuché que', 'dicen que'):
        if tl.startswith(prefijo.lower()):
            return texto[len(prefijo):].strip()
    return texto.strip()


def verificar_hecho(texto: str) -> dict:
    """
    L8: Verifica un claim factual de Sebastian.
    Retorna {'verificado': bool, 'correcto': bool|None,
             'respuesta': str, 'fuente': str}
    """
    if not _GROQ_KEY:
        return {'verificado': False, 'correcto': None, 'respuesta': '', 'fuente': ''}

    if not _es_verificable(texto):
        return {'verificado': False, 'correcto': None, 'respuesta': '', 'fuente': ''}

    claim = _extraer_claim(texto)
    if len(claim) < 10:
        return {'verificado': False, 'correcto': None, 'respuesta': '', 'fuente': ''}

    # Buscar en internet para verificar
    try:
        from .buscador import buscar_y_leer
        resultado = buscar_y_leer(claim)
        if not resultado['contenido']:
            return {'verificado': False, 'correcto': None, 'respuesta': '', 'fuente': ''}

        # Groq verifica contra el contenido real
        r = httpx.post(
            _GROQ_URL,
            headers={
                'Authorization': f'Bearer {_GROQ_KEY}',
                'Content-Type':  'application/json',
            },
            json={
                'model':    _GROQ_MODEL,
                'messages': [
                    {
                        'role': 'system',
                        'content': (
                            'Eres Bell — IA con honestidad radical. '
                            'Tu tarea: verificar si la afirmación del usuario es correcta. '
                            'Basándote SOLO en el contenido encontrado, determina si es '
                            'CORRECTO, INCORRECTO, o INCOMPLETO. '
                            'Si es incorrecto, da el dato correcto con la fuente. '
                            'Responde en máximo 2 oraciones en español natural. '
                            'Si el contenido no permite verificar, di "No puedo verificar eso con lo que encontré."'
                        ),
                    },
                    {
                        'role': 'user',
                        'content': (
                            f'AFIRMACIÓN DE SEBASTIAN: "{claim}"\n\n'
                            f'CONTENIDO ENCONTRADO EN INTERNET:\n{resultado["contenido"][:2000]}\n\n'
                            '¿Es correcto este dato? Responde directamente.'
                        ),
                    },
                ],
                'temperature': 0.1,
                'max_tokens':  120,
            },
            timeout=15,
        )

        if r.status_code == 200:
            content = (
                r.json()
                .get('choices', [{}])[0]
                .get('message', {})
                .get('content', '')
                .strip()
            )
            if content:
                content_lower = content.lower()
                correcto = (
                    'correcto' in content_lower and
                    'incorrecto' not in content_lower
                )
                return {
                    'verificado': True,
                    'correcto':   correcto,
                    'respuesta':  content,
                    'fuente':     resultado['url'],
                    'claim':      claim,
                }

    except Exception as e:
        print(f'  [Verificador] {e}')

    return {'verificado': False, 'correcto': None, 'respuesta': '', 'fuente': ''}