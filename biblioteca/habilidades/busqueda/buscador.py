# biblioteca/habilidades/busqueda/buscador.py
# ============================================================
# BUSCADOR — Bell busca, lee y extrae contenido real
#
# NIVELES CUBIERTOS:
#   L1 — Búsqueda básica DDG + lectura de página
#   L3 — Multi-fuente: lee 3 páginas y fusiona
#   L4 — Extracción profunda: article/main/section
# ============================================================

import httpx
from bs4 import BeautifulSoup
from typing import Optional

try:
    from ddgs import DDGS
    DDGS_OK = True
except ImportError:
    try:
        from duckduckgo_search import DDGS
        DDGS_OK = True
    except ImportError:
        DDGS_OK = False

_TIMEOUT   = 15
_MAX_CHARS = 4000   # aumentado — Groq procesa más contexto = mejor respuesta
_HEADERS   = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/124.0.0.0 Safari/537.36'
    ),
    'Accept-Language': 'es,en;q=0.9',
}
_SKIP_URLS = [
    'youtube.com', '.pdf', 'facebook.com', 'instagram.com',
    'tiktok.com', 'twitter.com', 'x.com', 'pinterest.com',
    'reddit.com/r/', 'amazon.com', 'mercadolibre',
]
# Fuentes de alta confianza — suben en prioridad
_FUENTES_PREMIUM = [
    'wikipedia.org', 'docs.python.org', 'developer.mozilla.org',
    'stackoverflow.com', 'github.com', 'arxiv.org', 'medium.com',
    'docs.', '.gov', '.edu', 'techcrunch.com', 'bbc.com', 'reuters.com',
]


def _es_skip(url: str) -> bool:
    return any(s in url for s in _SKIP_URLS)


def _es_premium(url: str) -> bool:
    return any(p in url for p in _FUENTES_PREMIUM)


def _parsear_html(html: str) -> str:
    """
    Extrae contenido real de HTML.
    L4: prioriza <article><main><section> sobre el body completo.
    Fallback: html.parser si lxml no está instalado.
    """
    try:
        soup = BeautifulSoup(html, 'lxml')
    except Exception:
        soup = BeautifulSoup(html, 'html.parser')

    # Limpiar ruido
    for tag in soup(['script', 'style', 'nav', 'footer', 'header',
                     'aside', 'iframe', 'form', 'noscript', 'svg',
                     'button', 'input', 'select', 'textarea']):
        tag.decompose()

    # L4: Buscar contenido principal primero
    contenedor = (
        soup.find('article') or
        soup.find('main') or
        soup.find(id='content') or
        soup.find(id='main-content') or
        soup.find(class_='content') or
        soup.find(class_='article-body') or
        soup.find(class_='post-content') or
        soup.find(class_='entry-content') or
        soup
    )

    partes = []
    for tag in contenedor.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'li', 'td', 'dt', 'dd']):
        texto = tag.get_text(separator=' ', strip=True)
        if len(texto) > 30:
            partes.append(texto)

    return '\n'.join(partes)


def buscar_web(query: str, max_resultados: int = 6) -> list:
    """
    Busca en DuckDuckGo.
    Retorna lista [{titulo, url, resumen, premium}]
    ordenada: premium primero.
    """
    if not DDGS_OK:
        return []
    try:
        resultados = []
        with DDGS() as ddgs:
            for r in ddgs.text(
                query,
                max_results=max_resultados,
                region='wt-wt',
                safesearch='moderate',
            ):
                url = r.get('href', '')
                resultados.append({
                    'titulo':  r.get('title', ''),
                    'url':     url,
                    'resumen': r.get('body', ''),
                    'premium': _es_premium(url),
                })

        # Premium primero, luego el resto
        resultados.sort(key=lambda x: x['premium'], reverse=True)
        return resultados

    except Exception as e:
        print(f'  [Buscador DDG] {e}')
        return []


def leer_pagina(url: str, max_chars: int = _MAX_CHARS) -> Optional[str]:
    """
    Lee el contenido principal de una URL.
    L4: extracción profunda con prioridad article/main.
    """
    try:
        resp = httpx.get(
            url, headers=_HEADERS,
            timeout=_TIMEOUT, follow_redirects=True
        )
        if resp.status_code != 200:
            return None
        contenido = _parsear_html(resp.text)
        if not contenido or len(contenido) < 100:
            return None
        return contenido[:max_chars]
    except Exception as e:
        print(f'  [Buscador Leer] {url[:50]} → {e}')
        return None


def buscar_y_leer(query: str) -> dict:
    """L1: Busca + lee la primera página válida."""
    resultados = buscar_web(query, max_resultados=6)
    if not resultados:
        return {'query': query, 'resultados': [], 'contenido': '', 'url': ''}

    contenido = ''
    url_leida = ''
    for r in resultados[:5]:
        url = r.get('url', '')
        if not url or _es_skip(url):
            continue
        c = leer_pagina(url)
        if c and len(c) > 150:
            contenido = c
            url_leida = url
            break

    # Fallback: snippets de DDG
    if not contenido:
        contenido = '\n'.join(
            f"{r['titulo']}: {r['resumen']}"
            for r in resultados if r.get('resumen')
        )[:_MAX_CHARS]

    return {
        'query':      query,
        'resultados': resultados,
        'contenido':  contenido,
        'url':        url_leida or (resultados[0]['url'] if resultados else ''),
    }


def buscar_multifuente(query: str, max_fuentes: int = 3) -> dict:
    """
    L3: Lee hasta 3 páginas y fusiona el contenido.
    Para preguntas importantes donde una sola fuente no basta.
    Retorna dict con contenido de cada fuente y snippets.
    """
    resultados = buscar_web(query, max_resultados=8)
    if not resultados:
        return {'query': query, 'fuentes': [], 'contenido_fusionado': '', 'total_fuentes': 0}

    fuentes = []
    for r in resultados:
        if len(fuentes) >= max_fuentes:
            break
        url = r.get('url', '')
        if not url or _es_skip(url):
            continue
        contenido = leer_pagina(url, max_chars=2000)  # menos por fuente, más fuentes
        if contenido and len(contenido) > 100:
            fuentes.append({
                'url':      url,
                'titulo':   r.get('titulo', ''),
                'resumen':  r.get('resumen', ''),
                'contenido': contenido,
                'premium':  r.get('premium', False),
            })

    # Si no se leyeron páginas, usar snippets
    if not fuentes:
        for r in resultados[:3]:
            if r.get('resumen'):
                fuentes.append({
                    'url':       r['url'],
                    'titulo':    r['titulo'],
                    'resumen':   r['resumen'],
                    'contenido': f"{r['titulo']}: {r['resumen']}",
                    'premium':   r.get('premium', False),
                })

    # Fusionar contenidos separados por fuente
    bloques = []
    for i, f in enumerate(fuentes, 1):
        bloques.append(
            f"[Fuente {i}: {f['titulo'][:60]}]\n{f['contenido'][:1500]}"
        )
    contenido_fusionado = '\n\n'.join(bloques)

    return {
        'query':             query,
        'fuentes':           fuentes,
        'contenido_fusionado': contenido_fusionado,
        'total_fuentes':     len(fuentes),
        'tiene_premium':     any(f['premium'] for f in fuentes),
    }