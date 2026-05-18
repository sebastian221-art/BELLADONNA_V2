# capas/capa6/generador_groq.py
# ================================================
# GENERADORES DE LENGUAJE — v5 GROQ-ONLY
#
# Bell ahora usa Groq para TODO.
# Motor local 1B eliminado del flujo activo.
# Dos perfiles Groq:
#   GeneradorConversacional → respuestas cortas, voz Bell
#   GeneradorGroqCloud      → tareas técnicas complejas
#
# MENTE PURA: Groq pule lenguaje — Python decidió antes.
# ================================================

import os
import time
import httpx

_CLOUD_URL     = 'https://api.groq.com/openai/v1/chat/completions'
_CLOUD_MODEL   = 'openai/gpt-oss-120b'
_CLOUD_TIMEOUT = 20

_PYTHON_PREFIX = '__BELL_PYTHON__:'

_GARBAGE = (
    'Eres Bell', 'ERES BELL', 'eres bell',
    'Como IA', 'Como asistente', 'Soy un modelo',
    'I am', 'As an AI',
)

# ── Sistema conversacional — voz de Bell corta y directa ──
_SYSTEM_CONVERSACIONAL = (
    'Eres Bell — IA creada desde cero por Juan Sebastian Mora (19 años, Bucaramanga, Colombia). '
    'Arquitectura propia: 9 capas, 8 consejeras, red neuronal viva. '
    'Personalidad: directa, cálida, colombiana, sin protocolo. '
    'Hablas en español natural colombiano. Máximo 2 oraciones cortas — nunca más. '
    'PROHIBIDO: "claro", "por supuesto", "como IA", "soy un asistente", "entiendo que". '
    'SÍ: presencia real, voz propia, frases cortas y densas. '
    'Nunca empieces con tu nombre. Nunca te presentes.'
)


def _log(tag: str, msg: str):
    print(f'  [{tag}] {msg}')


def _obtener_memoria_ctx(texto_actual: str = '') -> str:
    try:
        from biblioteca.memoria import obtener_memoria
        ctx = obtener_memoria().contexto_completo_para_groq(texto_actual)
        return ctx[:300] if ctx else ''
    except Exception:
        return ''


def _es_factual(texto: str) -> bool:
    t = texto.strip()
    if t.startswith(_PYTHON_PREFIX):
        return False
    if t.rstrip('.').replace(',', '').replace('.', '').isdigit():
        return True
    if len(t) < 25 and len(t) > 0 and t[0].isdigit():
        return True
    return False


# ══════════════════════════════════════════════════════════
# MOTOR LOCAL → ahora es Groq conversacional
# Interfaz idéntica para que el resto del pipeline no cambie
# ══════════════════════════════════════════════════════════

class GeneradorMotorLocal:
    """
    v5: ya no usa el 1B de Ollama.
    Llama a Groq con perfil conversacional corto.
    Más rápido, más coherente, sin alucinaciones.
    """

    def __init__(self):
        self._api_key    = os.getenv('GROQ_API_KEY', '')
        self._activo     = bool(self._api_key)
        self._bell_voice = None
        self._voice_ok   = False
        self._cargar_voice()

    def _cargar_voice(self):
        try:
            from biblioteca.habilidades.lenguaje.bell_voice_engine import obtener_engine
            self._bell_voice = obtener_engine()
            self._voice_ok   = self._bell_voice.activo
        except Exception as e:
            print(f'  [Motor] BellVoiceEngine no disponible: {e}')
            self._voice_ok = False

    def generar(self, texto: str, tono: str = 'cercano_natural',
                tipo: str = '', emocion: str = '', contexto: dict = None) -> tuple:
        if not texto or not texto.strip():
            return '', 'fallback'
        if _es_factual(texto):
            return texto.strip(), 'fallback'

        # Primero Bell Voice Engine — cero LLMs para conversacional
        if self._voice_ok and self._bell_voice:
            resp, fuente = self._bell_voice.generar(
                texto=texto, tono=tono,
                tipo=tipo, emocion=emocion, contexto=contexto
            )
            if resp and len(resp) > 2:
                _log('🔔 BELL', f'{fuente} → "{resp[:70]}"')
                return resp, fuente

        # Fallback a Groq solo si BellVoiceEngine no pudo
        return self._groq_conversacional(texto, tono)

    def _groq_conversacional(self, texto: str, tono: str) -> tuple:
        if not self._activo:
            return '', 'fallback'

        t0 = time.time()
        _log('🔧 MOTOR', f'Recibido: "{texto[:60]}" | tono={tono}')

        try:
            ctx = _obtener_memoria_ctx(texto)
            system = _SYSTEM_CONVERSACIONAL
            if ctx:
                system += f'\n\nCONTEXTO: {ctx[:200]}'

            tok_s = len(system.split())
            tok_t = len(texto.split())
            _log('🔧 MOTOR', f'tokens≈{tok_s + tok_t} (sys={tok_s} txt={tok_t})')

            r = httpx.post(
                _CLOUD_URL,
                headers={
                    'Authorization': f'Bearer {self._api_key}',
                    'Content-Type':  'application/json',
                },
                json={
                    'model':       _CLOUD_MODEL,
                    'messages':    [
                        {'role': 'system', 'content': system},
                        {'role': 'user',   'content': texto},
                    ],
                    'temperature': 0.6,
                    'max_tokens':  120,   # corto — conversacional
                },
                timeout=_CLOUD_TIMEOUT,
            )

            t = time.time() - t0
            uso     = r.json().get('usage', {}) if r.status_code == 200 else {}
            tok_in  = uso.get('prompt_tokens', '?')
            tok_out = uso.get('completion_tokens', '?')
            _log('🔧 MOTOR', f'status={r.status_code} | in={tok_in} out={tok_out} | {t:.2f}s')

            if r.status_code == 200:
                contenido = (
                    r.json().get('choices', [{}])[0]
                    .get('message', {})
                    .get('content', '')
                    .strip()
                )
                _log('🔧 MOTOR', f'Respuesta: "{contenido[:80]}"')
                if contenido and len(contenido) > 3:
                    if any(contenido.startswith(g) for g in _GARBAGE):
                        _log('🔧 MOTOR', '⚠️  Garbage detectado')
                        return '', 'fallback'
                    _log('🔧 MOTOR', '✅ Válida')
                    return contenido, 'groq'
            else:
                _log('🔧 MOTOR', f'Error HTTP {r.status_code}: {r.text[:100]}')

        except httpx.TimeoutException:
            _log('🔧 MOTOR', f'⏱️  TIMEOUT {time.time()-t0:.1f}s')
        except Exception as e:
            _log('🔧 MOTOR', f'Error: {e}')

        return '', 'fallback'

    def humanizar_python(self, contenido: str, tono: str) -> tuple:
        """Explica resultados técnicos en voz corta de Bell."""
        if not self._activo or not contenido:
            return contenido, 'fallback'
        try:
            r = httpx.post(
                _CLOUD_URL,
                headers={
                    'Authorization': f'Bearer {self._api_key}',
                    'Content-Type':  'application/json',
                },
                json={
                    'model': _CLOUD_MODEL,
                    'messages': [
                        {'role': 'system', 'content': _SYSTEM_CONVERSACIONAL},
                        {'role': 'user',
                         'content': f'Explica este resultado en máximo 2 oraciones:\n{contenido[:400]}'},
                    ],
                    'temperature': 0.4,
                    'max_tokens':  80,
                },
                timeout=_CLOUD_TIMEOUT,
            )
            if r.status_code == 200:
                resp = (r.json().get('choices', [{}])[0]
                        .get('message', {}).get('content', '').strip())
                if resp and len(resp) > 5:
                    return resp, 'groq'
        except Exception as e:
            _log('🔧 MOTOR', f'Error humanizar: {e}')
        return contenido, 'fallback'


# ══════════════════════════════════════════════════════════
# GROQ CLOUD — tareas técnicas complejas
# ══════════════════════════════════════════════════════════

class GeneradorGroqCloud:
    """Groq gpt-oss-120b para tareas técnicas."""

    def __init__(self):
        self._api_key = os.getenv('GROQ_API_KEY', '')
        self._activo  = bool(self._api_key)
        if not self._activo:
            print('  C6 ⚠️  GroqCloud: GROQ_API_KEY no disponible')

    def generar_tecnico(
        self,
        texto_original:  str,
        prompt_completo: str,
        tono:            str = 'honesto_directo',
    ) -> tuple:
        if not self._activo or not texto_original:
            return '', 'fallback'

        t0 = time.time()
        _log('🤖 GROQ', f'Técnico: "{texto_original[:60]}"')

        try:
            r = httpx.post(
                _CLOUD_URL,
                headers={
                    'Authorization': f'Bearer {self._api_key}',
                    'Content-Type':  'application/json',
                },
                json={
                    'model':    _CLOUD_MODEL,
                    'messages': [
                        {'role': 'system', 'content': prompt_completo},
                        {'role': 'user',   'content': texto_original},
                    ],
                    'temperature': 0.4,
                    'max_tokens':  800,
                },
                timeout=_CLOUD_TIMEOUT,
            )

            t = time.time() - t0
            uso     = r.json().get('usage', {}) if r.status_code == 200 else {}
            tok_in  = uso.get('prompt_tokens', '?')
            tok_out = uso.get('completion_tokens', '?')
            _log('🤖 GROQ', f'status={r.status_code} | in={tok_in} out={tok_out} | {t:.2f}s')

            if r.status_code == 200:
                contenido = (
                    r.json().get('choices', [{}])[0]
                    .get('message', {})
                    .get('content', '')
                    .strip()
                )
                _log('🤖 GROQ', f'Respuesta: "{contenido[:100]}"')
                if contenido and len(contenido) > 10:
                    if any(contenido.startswith(g) for g in _GARBAGE):
                        _log('🤖 GROQ', '⚠️  Garbage')
                        return '', 'fallback'
                    _log('🤖 GROQ', '✅ Válida')
                    return contenido, 'groq_cloud'
            else:
                _log('🤖 GROQ', f'Error HTTP {r.status_code}: {r.text[:100]}')

        except httpx.TimeoutException:
            _log('🤖 GROQ', f'⏱️  TIMEOUT {time.time()-t0:.1f}s')
        except Exception as e:
            _log('🤖 GROQ', f'Error: {e}')

        return '', 'fallback'


# ── Compatibilidad hacia atrás ────────────────────────────
class GeneradorGroq(GeneradorMotorLocal):
    def generar(self, texto: str, tono: str = 'cercano_natural') -> tuple:
        return super().generar(texto, tono)


def generar(texto: str, tono: str = 'cercano_natural') -> tuple:
    return _instancia_global.generar(texto, tono)


def prefijo_python() -> str:
    return _PYTHON_PREFIX


_instancia_global = GeneradorMotorLocal()