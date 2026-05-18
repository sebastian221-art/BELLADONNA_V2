# biblioteca/habilidades/busqueda/sintetizador.py
# ============================================================
# SINTETIZADOR DE FUENTES — L3
#
# Recibe contenido de múltiples fuentes y genera
# una respuesta unificada en voz de Bell.
#
# NIVELES:
#   L3 — Síntesis multi-fuente, detecta contradicciones
#   L6 — Síntesis contextualizada con perfil Sebastian
# ============================================================

import os
import httpx

_GROQ_URL   = 'https://api.groq.com/openai/v1/chat/completions'
_GROQ_MODEL = 'openai/gpt-oss-120b'
_GROQ_KEY   = os.getenv('GROQ_API_KEY', '')


def _groq_sintetizar(
    pregunta:    str,
    fuentes:     list,
    perfil_ctx:  str = '',
    detallado:   bool = False,
) -> str:
    """
    L3/L6: Groq sintetiza múltiples fuentes en voz de Bell.
    Si `perfil_ctx` tiene datos de Sebastian, los usa para contextualizar.
    """
    if not _GROQ_KEY or not fuentes:
        return ''

    # Construir bloque de fuentes
    bloques_fuente = []
    for i, f in enumerate(fuentes[:3], 1):
        contenido = f.get('contenido', f.get('resumen', ''))[:1500]
        titulo    = f.get('titulo', f.get('url', f'Fuente {i}'))[:60]
        bloques_fuente.append(f'[Fuente {i} — {titulo}]\n{contenido}')
    fuentes_texto = '\n\n'.join(bloques_fuente)

    # System prompt adaptativo
    largo = 'Respuesta completa en 5-6 oraciones con todos los datos relevantes.' if detallado else 'Respuesta en 3-4 oraciones directas.'

    perfil_bloque = f'\nCONTEXTO DE SEBASTIAN:\n{perfil_ctx}\n' if perfil_ctx else ''

    system = (
        'Eres Bell — IA de Sebastian Gómez (Bucaramanga, Colombia). '
        'Encontraste esta información en internet desde múltiples fuentes. '
        'SINTETIZA las fuentes en una respuesta coherente y precisa. '
        'Si las fuentes se contradicen, menciónalo brevemente. '
        'NUNCA inventes datos que no estén en las fuentes. '
        'NUNCA uses markdown, tablas ni bullets. '
        'NUNCA empieces con Claro, Por supuesto, Hola. '
        f'{largo} Prosa fluida en español.'
    )

    user_msg = (
        f'{perfil_bloque}'
        f'FUENTES ENCONTRADAS EN INTERNET:\n{fuentes_texto}\n\n'
        f'Sebastian pregunta: {pregunta}\n\n'
        'Sintetiza la información de las fuentes. '
        'Responde basándote SOLO en lo encontrado.'
    )

    try:
        r = httpx.post(
            _GROQ_URL,
            headers={
                'Authorization': f'Bearer {_GROQ_KEY}',
                'Content-Type':  'application/json',
            },
            json={
                'model':    _GROQ_MODEL,
                'messages': [
                    {'role': 'system', 'content': system},
                    {'role': 'user',   'content': user_msg},
                ],
                'temperature': 0.2,
                'max_tokens':  400 if detallado else 280,
            },
            timeout=20,
        )
        if r.status_code == 200:
            content = (
                r.json()
                .get('choices', [{}])[0]
                .get('message', {})
                .get('content', '')
                .strip()
            )
            if content and len(content) > 20:
                if content[-1] not in '.!?':
                    content += '.'
                return content
    except Exception as e:
        print(f'  [Sintetizador] {e}')

    return ''


def _groq_respuesta_simple(
    pregunta:   str,
    contenido:  str,
    url:        str,
    perfil_ctx: str = '',
    detallado:  bool = False,
) -> str:
    """
    L1/L6: Groq procesa una sola fuente.
    Versión mejorada del _groq_procesar original.
    """
    if not _GROQ_KEY or not contenido:
        return ''

    largo = '5-6 oraciones completas.' if detallado else '3-4 oraciones directas.'
    perfil_bloque = f'\nCONTEXTO DE SEBASTIAN:\n{perfil_ctx}\n' if perfil_ctx else ''

    system = (
        'Eres Bell — IA de Sebastian Gómez (Bucaramanga, Colombia). '
        'Encontraste esta información en internet y la explicas en primera persona. '
        'NUNCA inventes ni añadas datos que no estén en el contenido. '
        'NUNCA uses markdown, tablas ni bullets. '
        'NUNCA empieces con Claro, Por supuesto, Hola ni te presentes. '
        f'Prosa fluida en español. {largo}'
    )

    user_msg = (
        f'{perfil_bloque}'
        f'CONTENIDO REAL DE INTERNET:\nFuente: {url}\n\n{contenido[:2000]}\n\n'
        f'Sebastian pregunta: {pregunta}\n\n'
        'Responde basándote SOLO en el contenido encontrado. '
        'Si el contenido no responde bien la pregunta, dilo honestamente.'
    )

    try:
        r = httpx.post(
            _GROQ_URL,
            headers={
                'Authorization': f'Bearer {_GROQ_KEY}',
                'Content-Type':  'application/json',
            },
            json={
                'model':    _GROQ_MODEL,
                'messages': [
                    {'role': 'system', 'content': system},
                    {'role': 'user',   'content': user_msg},
                ],
                'temperature': 0.25,
                'max_tokens':  350 if detallado else 250,
            },
            timeout=20,
        )
        if r.status_code == 200:
            content = (
                r.json()
                .get('choices', [{}])[0]
                .get('message', {})
                .get('content', '')
                .strip()
            )
            if content and len(content) > 20:
                if content[-1] not in '.!?':
                    content += '.'
                return content
    except Exception as e:
        print(f'  [Sintetizador Simple] {e}')

    return ''


def _groq_clarificacion(termino: str, opcion1: str, opcion2: str) -> str:
    """Genera pregunta de clarificación natural en voz de Bell."""
    if not _GROQ_KEY:
        return f"¿Cuando dices '{termino}' te refieres al {opcion1} o al {opcion2}?"
    try:
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
                            'Eres Bell — IA de Sebastian. Natural, directa, sin protocolos. '
                            'Una sola pregunta corta de clarificación. Sin listas numéricas.'
                        ),
                    },
                    {
                        'role': 'user',
                        'content': (
                            f"El usuario preguntó sobre '{termino}' que puede ser: "
                            f"(1) {opcion1} o (2) {opcion2}. "
                            'Pide clarificación en una oración natural, como lo haría un amigo.'
                        ),
                    },
                ],
                'temperature': 0.4,
                'max_tokens':  60,
            },
            timeout=8,
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
                return content
    except Exception:
        pass
    return f"¿Cuando dices '{termino}' te refieres al {opcion1} o al {opcion2}?"