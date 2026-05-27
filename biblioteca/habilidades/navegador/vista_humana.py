# biblioteca/habilidades/navegador/vista_humana.py
# ============================================================
# VISTA HUMANA — los ojos de Bell (screenshot + Groq + árbol)
#
# Entiende cualquier página como un humano. Si ya conocemos la
# URL (conocimiento_web) no repite el análisis. Si no, mira la
# página (árbol de accesibilidad + screenshot) y se lo guarda.
#
# Groq = visión/análisis. Python = decisión. Fallback-safe.
# ============================================================

import base64
import json
import os
from typing import Optional

_GROQ_URL   = 'https://api.groq.com/openai/v1/chat/completions'
_GROQ_MODEL = os.getenv('GROQ_MODEL', 'openai/gpt-oss-120b')

_JS_ARBOL = """() => {
    const elementos = document.querySelectorAll(
        'button, input, a, textarea, select, [role="button"], [role="link"]'
    );
    return Array.from(elementos).slice(0, 50).map(el => ({
        tipo: el.tagName.toLowerCase(),
        texto: (el.textContent || el.value || el.placeholder ||
                el.getAttribute('aria-label') || '').trim().slice(0, 60),
        selector: el.id ? '#' + el.id :
                  (el.name ? '[name="' + el.name + '"]' : el.tagName.toLowerCase()),
        href: el.href || '',
    })).filter(e => e.texto);
}"""


def _dominio(url: str) -> str:
    try:
        from biblioteca.habilidades.navegador.conocimiento_web import extraer_dominio
        return extraer_dominio(url)
    except Exception:
        return url or ''


def analizar_pagina(page, objetivo: str, conocimiento_web=None) -> dict:
    """
    Analiza la página actual frente a un objetivo.
    Retorna {descripcion, selector_recomendado, accion_recomendada, ...}.
    Nunca lanza — siempre devuelve un dict (posiblemente parcial).
    """
    try:
        url = page.url
    except Exception:
        url = ''
    dominio = _dominio(url)

    # ── 1. ¿Ya conocemos esta URL? ────────────────────────
    if conocimiento_web is not None:
        try:
            if not conocimiento_web.necesita_screenshot(url):
                previo = conocimiento_web.analisis_previo(url)
                if previo:
                    return {'descripcion': previo.get('descripcion', ''),
                            'fuente': 'conocimiento_previo',
                            'elementos': previo.get('elementos', [])}
        except Exception:
            pass

    # ── 2. Árbol de accesibilidad ─────────────────────────
    arbol = []
    try:
        arbol = page.evaluate(_JS_ARBOL) or []
    except Exception:
        arbol = []

    # ── 3. Screenshot (para visión cuando el modelo lo soporte) ──
    screenshot_b64 = ''
    try:
        screenshot_b64 = base64.b64encode(page.screenshot(full_page=False)).decode()
    except Exception:
        pass

    # ── 4. Groq analiza (texto del árbol; imagen si soporta) ──
    resultado = _llamar_groq_vision(objetivo, url, arbol, screenshot_b64)

    # ── 5. Fallback Python si Groq no respondió ───────────
    if not resultado:
        resultado = _analisis_heuristico(objetivo, url, arbol)

    # ── 6. Guardar para no repetir ────────────────────────
    if conocimiento_web is not None and resultado:
        try:
            conocimiento_web.guardar_analisis_screenshot(
                dominio, url, resultado.get('descripcion', ''), arbol)
            if resultado.get('selector_recomendado'):
                conocimiento_web.guardar_selector(
                    dominio, 'ultimo_objetivo', resultado['selector_recomendado'], True)
        except Exception:
            pass

    return resultado or {}


def _llamar_groq_vision(objetivo, url, arbol, screenshot_b64) -> Optional[dict]:
    api_key = os.getenv('GROQ_API_KEY', '')
    if not api_key:
        return None
    prompt = (
        f'Objetivo de Bell: "{objetivo}"\nURL: {url}\n'
        f'Árbol de accesibilidad (elementos interactivos):\n'
        f'{json.dumps(arbol[:20], ensure_ascii=False)}\n\n'
        'Analiza la página y responde SOLO con JSON:\n'
        '{"descripcion":"qué página es en 1 oración",'
        '"elemento_principal":"el más relevante para el objetivo",'
        '"selector_recomendado":"selector CSS más específico para el objetivo",'
        '"accion_recomendada":"click|escribir|scroll|esperar",'
        '"otros_elementos":["..."],"esta_logueado":false,'
        '"tiene_popup":false,"notas":""}'
    )
    try:
        import httpx
        r = httpx.post(
            _GROQ_URL,
            headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'},
            json={'model': _GROQ_MODEL,
                  'messages': [
                      {'role': 'system', 'content': 'Analizas páginas web. Solo JSON válido.'},
                      {'role': 'user', 'content': prompt}],
                  'temperature': 0.1, 'max_tokens': 400},
            timeout=15,
        )
        if r.status_code != 200:
            return None
        cont = (r.json().get('choices', [{}])[0]
                .get('message', {}).get('content', '').strip())
        import re as _re
        m = _re.search(r'\{.*\}', cont, _re.DOTALL)
        return json.loads(m.group(0)) if m else None
    except Exception:
        return None


def _analisis_heuristico(objetivo, url, arbol) -> dict:
    """Sin Groq: usa patrones universales + primer elemento relevante."""
    try:
        from biblioteca.habilidades.navegador.patrones_universales import (
            detectar_tipo_pagina, obtener_selectores_para)
    except Exception:
        detectar_tipo_pagina = lambda a, u: 'general'
        obtener_selectores_para = lambda t: []
    tipo = detectar_tipo_pagina(arbol, url)
    selectores = obtener_selectores_para(tipo)
    sel = selectores[0] if selectores else (arbol[0]['selector'] if arbol else '')
    return {
        'descripcion': f'Página tipo {tipo}',
        'elemento_principal': arbol[0]['texto'] if arbol else '',
        'selector_recomendado': sel,
        'accion_recomendada': 'escribir' if tipo in ('buscador', 'login', 'chat_mensaje') else 'click',
        'otros_elementos': [e['texto'] for e in arbol[:5]],
        'esta_logueado': False,
        'tiene_popup': False,
        'notas': 'análisis heurístico (sin Groq)',
        'fuente': 'heuristico',
    }


# ── Singleton ─────────────────────────────────────────────
class VistaHumana:
    _instancia = None

    @classmethod
    def obtener(cls) -> 'VistaHumana':
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def analizar_pagina(self, page, objetivo: str, conocimiento_web=None) -> dict:
        return analizar_pagina(page, objetivo, conocimiento_web)
