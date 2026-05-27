# biblioteca/habilidades/navegador/detector_api.py
# ============================================================
# DETECTOR DE API — Bell usa APIs públicas cuando existen
#
# Más confiable que scraping. Si la API responde, no se navega.
# Python puro + httpx. Fallback-safe: si falla → {}.
# ============================================================

APIS_CONOCIDAS = {
    'github.com': {
        'base': 'https://api.github.com',
        'endpoints': {
            'repos_usuario': '/users/{usuario}/repos?per_page=20&sort=updated',
            'repo_info':     '/repos/{usuario}/{repo}',
            'issues':        '/repos/{usuario}/{repo}/issues',
            'readme':        '/repos/{usuario}/{repo}/readme',
        },
        'auth': 'opcional',  # 60 req/hora sin auth
        'headers': {'Accept': 'application/vnd.github.v3+json',
                    'User-Agent': 'Bell/1.0'},
    },
    'wikipedia.org': {
        'base': 'https://es.wikipedia.org/api/rest_v1',
        'endpoints': {
            'resumen': '/page/summary/{titulo}',
        },
        'auth': 'no_requiere',
        'headers': {'User-Agent': 'Bell/1.0'},
    },
    'reddit.com': {
        'base': 'https://www.reddit.com',
        'endpoints': {
            'subreddit_hot': '/r/{subreddit}/hot.json',
            'busqueda':      '/search.json?q={query}',
        },
        'auth': 'no_requiere',
        'headers': {'User-Agent': 'Bell/1.0'},
    },
}


def tiene_api(dominio: str) -> bool:
    dominio = (dominio or '').lower()
    return any(d in dominio for d in APIS_CONOCIDAS)


def url_api(dominio: str) -> str:
    for d, cfg in APIS_CONOCIDAS.items():
        if d in (dominio or '').lower():
            return cfg['base']
    return ''


def llamar_api(dominio: str, endpoint_nombre: str, **params):
    """Llama a la API del dominio. Retorna datos (dict/list) o {} si falla."""
    dominio = (dominio or '').lower()
    for d, cfg in APIS_CONOCIDAS.items():
        if d in dominio:
            template = cfg['endpoints'].get(endpoint_nombre, '')
            if not template:
                return {}
            try:
                url = cfg['base'] + template.format(**params)
            except Exception:
                return {}
            try:
                import httpx
                r = httpx.get(url, headers=cfg.get('headers', {}),
                              timeout=10, follow_redirects=True)
                if r.status_code == 200:
                    return r.json()
            except Exception:
                pass
    return {}


# ── Singleton ─────────────────────────────────────────────
class DetectorApi:
    _instancia = None

    @classmethod
    def obtener(cls) -> 'DetectorApi':
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def tiene_api(self, dominio: str) -> bool:
        return tiene_api(dominio)

    def llamar(self, dominio: str, endpoint_nombre: str, **params):
        return llamar_api(dominio, endpoint_nombre, **params)
