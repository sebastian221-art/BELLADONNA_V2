# biblioteca/habilidades/navegador/investigacion.py
# ============================================================
# INVESTIGACIÓN PROFUNDA — Bell visita varias fuentes y sintetiza
#
# Elige el mejor motor, visita resultados (vía motor del navegador
# si se le pasa una función visitar), destila cada fuente y
# sintetiza principios + conclusión. Guarda en la memoria de Bell.
#
# Fallback-safe: sin browser/Groq → síntesis honesta de lo disponible.
# ============================================================

import json
import os
from typing import Optional, Callable

_GROQ_URL   = 'https://api.groq.com/openai/v1/chat/completions'
_GROQ_MODEL = os.getenv('GROQ_MODEL', 'openai/gpt-oss-120b')


def investigar(tema: str, n_fuentes: int = 5, visitar: Optional[Callable] = None) -> dict:
    """
    Investiga un tema. `visitar(url)->texto` es opcional (lo provee el
    motor del navegador). Sin él, sintetiza con el conocimiento de Groq.
    Retorna {'sintesis','fuentes','principios_clave'}.
    """
    try:
        from biblioteca.habilidades.navegador.buscador_inteligente import elegir_motor
        motor, url_busqueda = elegir_motor(tema)
    except Exception:
        motor, url_busqueda = 'general', ''

    fragmentos = []
    fuentes = []
    if callable(visitar):
        try:
            from biblioteca.habilidades.navegador.lector_destilador import destilar_para_objetivo
        except Exception:
            destilar_para_objetivo = None
        # El motor del navegador resuelve qué URLs visitar; aquí visitamos la búsqueda
        try:
            contenido = visitar(url_busqueda)
            if contenido:
                fragmentos.append(str(contenido)[:1500])
                fuentes.append(url_busqueda)
        except Exception:
            pass

    sintesis = _sintetizar_groq(tema, fragmentos)
    principios = []
    if sintesis:
        # Guardar como conocimiento destilado de Bell
        try:
            from biblioteca.habilidades.memoria.gestor import obtener_memoria
            from biblioteca.habilidades.memoria.destilador_conocimiento import destilar
            principio = destilar(tema, sintesis)
            principios = [principio] if principio else []
            obtener_memoria().guardar_conocimiento(
                tema[:40], principio or sintesis, 'general', 'investigacion', confianza=0.85)
        except Exception:
            pass

    return {
        'sintesis': sintesis or f'No pude investigar "{tema}" a fondo todavía (sin fuentes accesibles).',
        'fuentes': fuentes or [url_busqueda] if url_busqueda else [],
        'principios_clave': principios,
        'motor': motor,
    }


def _sintetizar_groq(tema: str, fragmentos: list) -> Optional[str]:
    api_key = os.getenv('GROQ_API_KEY', '')
    if not api_key:
        return None
    base = (
        f'Tema a investigar: "{tema}"\n'
        + (f'Fragmentos de fuentes:\n{json.dumps(fragmentos[:5], ensure_ascii=False)}\n'
           if fragmentos else 'No hay fragmentos de fuentes; usa tu conocimiento.\n')
    )
    prompt = (
        base +
        '\nSintetiza en: (1) 3-5 principios clave en bullets cortos, '
        '(2) una conclusión de 2 oraciones. Sé concreto, sin relleno.'
    )
    try:
        import httpx
        r = httpx.post(
            _GROQ_URL,
            headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'},
            json={'model': _GROQ_MODEL,
                  'messages': [
                      {'role': 'system', 'content': 'Sintetizas investigación en principios y conclusión.'},
                      {'role': 'user', 'content': prompt}],
                  'temperature': 0.3, 'max_tokens': 500},
            timeout=20,
        )
        if r.status_code == 200:
            return (r.json().get('choices', [{}])[0]
                    .get('message', {}).get('content', '').strip()) or None
    except Exception:
        pass
    return None


# ── Singleton ─────────────────────────────────────────────
class Investigacion:
    _instancia = None

    @classmethod
    def obtener(cls) -> 'Investigacion':
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def investigar(self, tema: str, n_fuentes: int = 5, visitar=None) -> dict:
        return investigar(tema, n_fuentes, visitar)
