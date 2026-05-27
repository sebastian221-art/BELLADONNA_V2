# biblioteca/habilidades/navegador/patrones_universales.py
# ============================================================
# PATRONES UNIVERSALES DE INTERNET
#
# Principios de cómo funciona la web — Python puro, sin Groq.
# Bell entiende internet como una persona: sabe que un login
# tiene usuario+password+submit, que un buscador es un input, etc.
# ============================================================

PATRONES = {
    'login': {
        'descripcion': 'Páginas de login tienen campo username/email + password + submit',
        'selectores_probables': [
            'input[name="username"]', 'input[name="email"]', 'input[type="email"]',
            'input[name="password"]', 'input[type="password"]',
            'button[type="submit"]', 'input[type="submit"]',
            'button:has-text("Entrar")', 'button:has-text("Sign in")',
            'button:has-text("Iniciar sesión")', 'button:has-text("Login")',
        ],
        'estrategia': 'buscar input type=email o name=username, luego password, luego submit',
    },
    'buscador': {
        'descripcion': 'Barras de búsqueda son inputs de texto + Enter o botón buscar',
        'selectores_probables': [
            'input[type="search"]', 'input[name="q"]', 'input[name="query"]',
            'input[name="search"]', 'input[name="search_query"]',
            '[role="searchbox"]', 'input[placeholder*="Buscar"]',
            'input[placeholder*="Search"]', 'input[aria-label*="buscar"]',
        ],
        'estrategia': 'buscar input con role=searchbox o name=q, escribir texto, Enter',
    },
    'feed_social': {
        'descripcion': 'Feeds son listas de posts/artículos scrolleables',
        'selectores_probables': [
            'article', '[role="article"]', '[data-testid="tweet"]',
            '.post', '.feed-item', 'ytd-video-renderer',
        ],
        'estrategia': 'scroll y leer article o [role=article]',
    },
    'chat_mensaje': {
        'descripcion': 'Campos de chat son textareas editables cerca de botón enviar',
        'selectores_probables': [
            'div[contenteditable="true"]', 'textarea[placeholder]',
            '[role="textbox"]', 'input[type="text"][placeholder*="mensaje"]',
        ],
        'estrategia': 'buscar contenteditable=true o textarea, escribir, Enter',
    },
    'ecommerce_precio': {
        'descripcion': 'Precios están cerca del nombre del producto',
        'selectores_probables': [
            '[class*="price"]', '[class*="precio"]', '[itemprop="price"]',
            '.a-price', '[data-price]',
        ],
        'estrategia': 'buscar itemprop=price o class con price',
    },
    'popup_cerrar': {
        'descripcion': 'Popups tienen botón X o "Cerrar" o "No gracias"',
        'selectores_probables': [
            'button[aria-label="Close"]', 'button[aria-label="Cerrar"]',
            '[class*="close"]', '[class*="dismiss"]', 'button:has-text("×")',
            'button:has-text("No gracias")', '[data-dismiss]',
        ],
        'estrategia': 'buscar aria-label=Close o clase close, hacer click',
    },
    'paginacion': {
        'descripcion': 'Paginación usa botones Next/Siguiente o números',
        'selectores_probables': [
            'a[rel="next"]', 'button:has-text("Next")', 'button:has-text("Siguiente")',
            '[aria-label="Next page"]', '.pagination .next',
        ],
        'estrategia': 'buscar rel=next o aria-label=Next page',
    },
}


def obtener_selectores_para(tipo_accion: str) -> list:
    """Retorna lista de selectores a intentar para un tipo de acción."""
    return PATRONES.get(tipo_accion, {}).get('selectores_probables', [])


def estrategia_para(tipo_accion: str) -> str:
    return PATRONES.get(tipo_accion, {}).get('estrategia', 'intentar selectores conocidos')


def detectar_tipo_pagina(accessibility_tree: list, url: str) -> str:
    """Detecta qué tipo de página es basándose en sus elementos."""
    tree = accessibility_tree or []
    has_password = any(
        'password' in (e.get('selector', '') or '').lower()
        for e in tree
    )
    if has_password:
        return 'login'
    u = (url or '').lower()
    if 'youtube.com' in u:
        return 'feed_social'
    if any('search' in (e.get('selector', '') or '').lower() for e in tree):
        return 'buscador'
    return 'general'


# ── Singleton (interfaz uniforme con los demás módulos) ────
class PatronesUniversales:
    _instancia = None

    @classmethod
    def obtener(cls) -> 'PatronesUniversales':
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def selectores_para(self, tipo_accion: str) -> list:
        return obtener_selectores_para(tipo_accion)

    def estrategia_para(self, tipo_accion: str) -> str:
        return estrategia_para(tipo_accion)

    def detectar_tipo_pagina(self, accessibility_tree: list, url: str) -> str:
        return detectar_tipo_pagina(accessibility_tree, url)
