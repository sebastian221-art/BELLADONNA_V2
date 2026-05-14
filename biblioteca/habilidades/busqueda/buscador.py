# biblioteca/habilidades/busqueda/buscador.py
# ============================================================
# BUSCADOR — Bell busca en internet y lee páginas reales
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

_TIMEOUT = 15
_MAX_CHARS = 2500
_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/120.0.0.0 Safari/537.36'
}
_SKIP_URLS = ['youtube.com', '.pdf', 'facebook.com', 'instagram.com',
              'tiktok.com', 'twitter.com', 'x.com']


def buscar_web(query: str, max_resultados: int = 5) -> list:
    """Busca en DuckDuckGo global. Retorna [{titulo, url, resumen}]"""
    if not DDGS_OK:
        return []
    try:
        resultados = []
        with DDGS() as ddgs:
            for r in ddgs.text(
                query,
                max_results=max_resultados,
                region='wt-wt',       # global — mejores resultados
                safesearch='moderate',
            ):
                resultados.append({
                    'titulo':  r.get('title', ''),
                    'url':     r.get('href', ''),
                    'resumen': r.get('body', ''),
                })
        return resultados
    except Exception as e:
        print(f"  [Busqueda DDG] {e}")
        return []


def leer_pagina(url: str) -> Optional[str]:
    """Lee el contenido principal de una URL sin ruido."""
    try:
        resp = httpx.get(url, headers=_HEADERS, timeout=_TIMEOUT,
                         follow_redirects=True)
        if resp.status_code != 200:
            return None
        soup = BeautifulSoup(resp.text, 'lxml')
        for tag in soup(['script', 'style', 'nav', 'footer',
                         'header', 'aside', 'iframe', 'form']):
            tag.decompose()
        partes = []
        for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'li']):
            texto = tag.get_text(separator=' ', strip=True)
            if len(texto) > 40:
                partes.append(texto)
        contenido = '\n'.join(partes)
        return contenido[:_MAX_CHARS] if contenido else None
    except Exception as e:
        print(f"  [Busqueda Leer] {e}")
        return None


def buscar_y_leer(query: str) -> dict:
    """Busca + lee la primera página válida."""
    resultados = buscar_web(query, max_resultados=5)
    if not resultados:
        return {'query': query, 'resultados': [], 'contenido': '', 'url': ''}

    contenido = ''
    url_leida = ''
    for r in resultados[:4]:
        url = r.get('url', '')
        if not url or any(s in url for s in _SKIP_URLS):
            continue
        c = leer_pagina(url)
        if c and len(c) > 200:
            contenido = c
            url_leida = url
            break

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