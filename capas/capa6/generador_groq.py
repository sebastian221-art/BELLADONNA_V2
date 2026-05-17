# capas/capa6/generador_groq.py
# ================================================
# GENERADOR — Motor de lenguaje de Bell v4
#
# ARQUITECTURA MENTE PURA:
#   Bell decide qué decir (Python puro, capas 1-6)
#   → Este módulo pule el lenguaje final
#   → Motor Bell humaniza — NUNCA inventa contenido
#
# v4: Motor local Ollama + logs de diagnóstico completos
# ================================================

import os
import time
import httpx

_GROQ_URL     = "http://localhost:11434/v1/chat/completions"
_GROQ_MODEL   = "hf.co/sebastian221-art/bell-motor-local:bell-motor-local.Q4_K_M"
_GROQ_API_KEY = "ollama"
_GROQ_TIMEOUT = 120

_INSTRUCCIONES_TONO = {
    'cercano_natural':      'Responde natural y cercano, como Bell hablaría a Sebastian.',
    'empático_suave':       'Responde con calidez y empatía.',
    'claro_directo':        'Responde claro y directo, sin rodeos.',
    'cálido_genuino':       'Responde con calidez genuina.',
    'tranquilizador_suave': 'Responde tranquilo y reconfortante.',
    'celebratorio_cálido':  'Responde con calidez y celebración.',
    'honesto_directo':      'Responde con honestidad directa.',
}

_PYTHON_PREFIX = '__BELL_PYTHON__:'


def _log_motor(msg: str):
    """Log de diagnóstico del motor — siempre visible."""
    print(f'  [🔧 MOTOR] {msg}')


def _es_respuesta_factual(texto: str) -> bool:
    t = texto.strip()
    if t.startswith(_PYTHON_PREFIX):
        return False
    if t.rstrip('.').replace(',', '').replace('.', '').isdigit():
        return True
    if len(t) < 25 and t[0].isdigit():
        return True
    if 'sebastian' in t.lower() and len(t) < 120:
        return True
    frases_protegidas = [
        'no soy de ninguna empresa', 'me creó sebastian',
        'sebastian me construyó', 'no tengo nada que ver con',
    ]
    if any(f in texto.lower() for f in frases_protegidas):
        return True
    return False


def _obtener_contexto_memoria() -> str:
    try:
        from biblioteca.memoria import obtener_memoria
        mem = obtener_memoria()
        ctx = mem.contexto_completo_para_groq()
        return ctx[:300] if ctx else ''  # limitar a 300 chars para velocidad
    except Exception as e:
        _log_motor(f'Memoria no disponible: {e}')
        return ''


def _construir_system_prompt(ctx_memoria: str) -> str:
    """System prompt CORTO — menos tokens = más rápido en CPU."""
    base = (
        'Eres Bell, IA creada por Sebastian (19 años, Bucaramanga). '
        'Directa, cercana, personalidad propia. '
        'Máximo 2 oraciones. Solo mejora el lenguaje — no inventes.'
    )
    if ctx_memoria:
        return base + f'\nContexto: {ctx_memoria}'
    return base


class GeneradorGroq:
    """Motor de lenguaje de Bell — usa Ollama local."""

    def generar(self, prompt: str, tono: str = 'cercano_natural') -> tuple:
        if not prompt or not prompt.strip():
            _log_motor('Prompt vacío — fallback directo')
            return '', 'fallback'

        _log_motor(f'Prompt recibido: "{prompt[:60]}..." | tono={tono}')

        if _es_respuesta_factual(prompt):
            _log_motor(f'Respuesta factual detectada — sin motor | len={len(prompt)}')
            return prompt.strip(), 'fallback'

        respuesta, fuente = self._intentar_groq(prompt, tono, max_tokens=80)
        if respuesta:
            return respuesta, fuente

        _log_motor('Motor falló — usando fallback base_python')
        return prompt.strip(), 'fallback'

    def _humanizar_python(self, contenido: str, tono: str) -> tuple:
        if not _GROQ_API_KEY:
            return contenido, 'fallback'

        _log_motor(f'Humanizando Python | len_contenido={len(contenido)}')
        t0 = time.time()

        try:
            inst = _INSTRUCCIONES_TONO.get(tono, _INSTRUCCIONES_TONO['cercano_natural'])
            system = (
                'Eres Bell, IA de Sebastian en Bucaramanga. '
                'Técnica pero natural. Explica código en prosa, sin bullets. '
                'No inventes — solo reformula lo que te doy.'
            )

            _log_motor(f'system_tokens≈{len(system.split())} | contenido_tokens≈{len(contenido.split())}')

            r = httpx.post(
                _GROQ_URL,
                headers={'Authorization': f'Bearer {_GROQ_API_KEY}', 'Content-Type': 'application/json'},
                json={
                    'model': _GROQ_MODEL,
                    'messages': [
                        {'role': 'system', 'content': system},
                        {'role': 'user', 'content': f'{inst}\n\nConvierte esto al lenguaje de Bell:\n\n{contenido}'},
                    ],
                    'temperature': 0.5,
                    'max_tokens': 300,
                },
                timeout=_GROQ_TIMEOUT,
            )

            t_total = time.time() - t0
            _log_motor(f'Python humanizado | status={r.status_code} | tiempo={t_total:.1f}s')

            if r.status_code == 200:
                data = r.json()
                resp = data.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
                uso = data.get('usage', {})
                _log_motor(
                    f'tokens_in={uso.get("prompt_tokens","?")} | '
                    f'tokens_out={uso.get("completion_tokens","?")} | '
                    f'tok/s={uso.get("completion_tokens", 0) / t_total:.1f}'
                )
                if resp and len(resp) > 10:
                    return resp, 'groq'

        except Exception as e:
            _log_motor(f'Error Python humanizer: {e} | tiempo={time.time()-t0:.1f}s')

        return contenido, 'fallback'

    def _intentar_groq(self, prompt: str, tono: str, max_tokens: int = 80) -> tuple:
        if not _GROQ_API_KEY:
            _log_motor('Sin API key — skip')
            return '', ''

        t0 = time.time()
        _log_motor(f'Llamando motor | max_tokens={max_tokens} | timeout={_GROQ_TIMEOUT}s')

        try:
            inst = _INSTRUCCIONES_TONO.get(tono, _INSTRUCCIONES_TONO['cercano_natural'])

            t_mem = time.time()
            ctx_memoria = _obtener_contexto_memoria()
            _log_motor(f'Memoria obtenida en {time.time()-t_mem:.2f}s | len={len(ctx_memoria)}')

            system_prompt = _construir_system_prompt(ctx_memoria)
            tokens_system = len(system_prompt.split())
            tokens_user   = len(prompt.split()) + len(inst.split())

            _log_motor(
                f'system_tokens≈{tokens_system} | '
                f'user_tokens≈{tokens_user} | '
                f'total_entrada≈{tokens_system + tokens_user}'
            )

            t_request = time.time()
            r = httpx.post(
                _GROQ_URL,
                headers={'Authorization': f'Bearer {_GROQ_API_KEY}', 'Content-Type': 'application/json'},
                json={
                    'model': _GROQ_MODEL,
                    'messages': [
                        {'role': 'system', 'content': system_prompt},
                        {'role': 'user',   'content': f'{inst}\n\nMejora solo el lenguaje:\n\n{prompt}'},
                    ],
                    'temperature': 0.4,
                    'max_tokens':  max_tokens,
                },
                timeout=_GROQ_TIMEOUT,
            )

            t_respuesta = time.time() - t_request
            t_total     = time.time() - t0

            _log_motor(f'Respuesta recibida | status={r.status_code} | t_request={t_respuesta:.1f}s | t_total={t_total:.1f}s')

            if r.status_code == 200:
                data     = r.json()
                contenido = data.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
                uso       = data.get('usage', {})
                tok_in    = uso.get('prompt_tokens', '?')
                tok_out   = uso.get('completion_tokens', '?')
                tok_seg   = tok_out / t_total if isinstance(tok_out, int) and t_total > 0 else '?'

                _log_motor(
                    f'tokens_in={tok_in} | tokens_out={tok_out} | '
                    f'tok/s={tok_seg:.2f}' if isinstance(tok_seg, float)
                    else f'tokens_in={tok_in} | tokens_out={tok_out} | tok/s=?'
                )
                _log_motor(f'Contenido: "{contenido[:80]}"')

                _GROQ_GARBAGE = ('Eres Bell', 'ERES BELL', 'eres bell', 'Una consciencia digital')
                if contenido and len(contenido) > 5:
                    if any(contenido.startswith(g) for g in _GROQ_GARBAGE):
                        _log_motor('⚠️  Garbage detectado — motor echó system prompt')
                    else:
                        _log_motor('✅ Respuesta válida del motor')
                        return contenido, 'groq'
            else:
                _log_motor(f'Error HTTP: {r.status_code} | {r.text[:200]}')

        except httpx.TimeoutException:
            _log_motor(f'⏱️  TIMEOUT después de {time.time()-t0:.1f}s')
        except Exception as e:
            _log_motor(f'Error inesperado: {e} | tiempo={time.time()-t0:.1f}s')

        return '', ''


def generar(prompt: str, tono: str = 'cercano_natural') -> tuple:
    return _instancia_global.generar(prompt, tono)


def prefijo_python() -> str:
    return _PYTHON_PREFIX


_instancia_global = GeneradorGroq()