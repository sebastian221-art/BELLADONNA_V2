# biblioteca/habilidades/navegador/lector_destilador.py
# ============================================================
# LECTOR DESTILADOR — Bell responde al objetivo, no la página
#
# Dado el contenido crudo de una página y el objetivo de Sebastian,
# extrae SOLO lo relevante. Groq destila; fallback al texto.
# Guarda el resultado en conocimiento_web para no repetir.
# ============================================================

import json
import os
from typing import Optional

_GROQ_URL   = 'https://api.groq.com/openai/v1/chat/completions'
_GROQ_MODEL = os.getenv('GROQ_MODEL', 'openai/gpt-oss-120b')


def _attr(obj, nombre, default=''):
    """Lee atributo de dataclass O clave de dict, defensivamente."""
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(nombre, default)
    return getattr(obj, nombre, default)


def destilar_para_objetivo(contenido_pagina, objetivo: str, conocimiento_web=None) -> str:
    url            = _attr(contenido_pagina, 'url', '')
    titulo         = _attr(contenido_pagina, 'titulo', '')
    texto_principal = _attr(contenido_pagina, 'texto_principal', '') or _attr(contenido_pagina, 'texto', '')
    datos_esp      = _attr(contenido_pagina, 'datos_especiales', {}) or {}

    contexto = (
        f'Objetivo de Sebastian: "{objetivo}"\n'
        f'URL: {url}\nTítulo: {titulo}\n'
        f'Contenido principal (primeros 1500 chars): {str(texto_principal)[:1500]}\n'
    )
    if isinstance(datos_esp, dict):
        if datos_esp.get('repos'):
            contexto += f"\nRepos encontrados: {json.dumps(datos_esp['repos'][:5], ensure_ascii=False)}"
        if datos_esp.get('videos'):
            contexto += f"\nVideos encontrados: {json.dumps(datos_esp['videos'][:5], ensure_ascii=False)}"

    respuesta = _destilar_groq(contexto, objetivo)

    if respuesta and conocimiento_web is not None:
        try:
            from biblioteca.habilidades.navegador.conocimiento_web import extraer_dominio
            conocimiento_web.guardar_analisis_screenshot(
                extraer_dominio(url), url, respuesta, [])
        except Exception:
            pass

    # Fallback: el texto principal recortado
    return respuesta or (str(texto_principal)[:500] if texto_principal else 'No encontré contenido relevante.')


def _destilar_groq(contexto: str, objetivo: str) -> Optional[str]:
    api_key = os.getenv('GROQ_API_KEY', '')
    if not api_key:
        return None
    prompt = (
        f'{contexto}\n\n'
        'Extrae SOLO la información relevante al objetivo en máximo 3 oraciones. '
        'Incluye datos específicos: URLs, precios, fechas, nombres exactos. '
        'Si no hay información relevante, dilo honestamente. '
        'No expliques el proceso — solo la información.'
    )
    try:
        import httpx
        r = httpx.post(
            _GROQ_URL,
            headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'},
            json={'model': _GROQ_MODEL,
                  'messages': [
                      {'role': 'system', 'content': 'Destilas contenido web a lo esencial del objetivo. Conciso.'},
                      {'role': 'user', 'content': prompt}],
                  'temperature': 0.2, 'max_tokens': 220},
            timeout=15,
        )
        if r.status_code == 200:
            return (r.json().get('choices', [{}])[0]
                    .get('message', {}).get('content', '').strip()) or None
    except Exception:
        pass
    return None


# ── Singleton ─────────────────────────────────────────────
class LectorDestilador:
    _instancia = None

    @classmethod
    def obtener(cls) -> 'LectorDestilador':
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def destilar_para_objetivo(self, contenido_pagina, objetivo: str, conocimiento_web=None) -> str:
        return destilar_para_objetivo(contenido_pagina, objetivo, conocimiento_web)
