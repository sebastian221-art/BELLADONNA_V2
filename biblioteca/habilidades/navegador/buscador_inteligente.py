# biblioteca/habilidades/navegador/buscador_inteligente.py
# ============================================================
# BUSCADOR INTELIGENTE — el mejor motor para cada consulta
#
# No todo va a google.com. Código en Stack Overflow, repos en
# GitHub, definiciones en Wikipedia, videos en YouTube, etc.
# Python puro, sin Groq.
# ============================================================

from urllib.parse import quote

MOTORES = {
    'codigo':       'https://stackoverflow.com/search?q={query}',
    'github_code':  'https://github.com/search?q={query}&type=code',
    'github_repos': 'https://github.com/search?q={query}&type=repositories',
    'python_docs':  'https://docs.python.org/3/search.html?q={query}',
    'wikipedia':    'https://es.wikipedia.org/wiki/Special:Search?search={query}',
    'youtube':      'https://youtube.com/results?search_query={query}',
    'noticias':     'https://news.google.com/search?q={query}',
    'precios_co':   'https://www.google.com/search?q={query}+precio+colombia',
    'general':      'https://google.com/search?q={query}',
}


def elegir_motor(objetivo: str):
    """Retorna (nombre_motor, url_de_busqueda) según el objetivo."""
    tl = (objetivo or '').lower()
    q  = quote(objetivo or '')
    if any(k in tl for k in ['error', 'exception', 'traceback', 'bug', 'cómo hacer en python', 'como hacer en python']):
        return 'codigo', MOTORES['codigo'].format(query=q)
    if any(k in tl for k in ['repositorio', 'repo', 'código de', 'codigo de', 'librería', 'libreria']):
        return 'github_repos', MOTORES['github_repos'].format(query=q)
    if 'wikipedia' in tl or any(k in tl for k in ['quién fue', 'quien fue', 'qué es', 'que es', 'historia de']):
        return 'wikipedia', MOTORES['wikipedia'].format(query=q)
    if any(k in tl for k in ['video', 'tutorial', 'youtube']):
        return 'youtube', MOTORES['youtube'].format(query=q)
    if any(k in tl for k in ['precio', 'cuánto cuesta', 'cuanto cuesta', 'comprar']):
        return 'precios_co', MOTORES['precios_co'].format(query=q)
    if any(k in tl for k in ['noticia', 'última hora', 'ultima hora']):
        return 'noticias', MOTORES['noticias'].format(query=q)
    return 'general', MOTORES['general'].format(query=q)


# ── Singleton ─────────────────────────────────────────────
class BuscadorInteligente:
    _instancia = None

    @classmethod
    def obtener(cls) -> 'BuscadorInteligente':
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def elegir_motor(self, objetivo: str):
        return elegir_motor(objetivo)
