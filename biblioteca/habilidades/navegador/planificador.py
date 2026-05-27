# biblioteca/habilidades/navegador/planificador.py
# ============================================================
# PLANIFICADOR — El cerebro estratégico de Bell para el browser
#
# Dado un objetivo en lenguaje natural, produce un plan de
# pasos ejecutables que el controlador puede ejecutar.
#
# Groq participa AQUÍ para:
#   1. Interpretar objetivos ambiguos
#   2. Descomponer tareas complejas en pasos
#   3. Decidir qué hacer cuando la página es inesperada
#   4. Adaptar el plan si un paso falla
#
# La ejecución NUNCA la hace Groq — solo planifica.
# ============================================================

import json
import os
import re
from dataclasses import dataclass, field
from typing import List, Optional

_GROQ_URL   = 'https://api.groq.com/openai/v1/chat/completions'
_GROQ_MODEL = 'openai/gpt-oss-120b'


@dataclass
class Paso:
    numero:    int
    accion:    str           # 'navegar'|'click'|'escribir'|'leer'|'scroll'|'esperar'|'screenshot'
    parametros: dict = field(default_factory=dict)
    descripcion: str = ''
    opcional:  bool  = False  # si falla, continuar igual


@dataclass
class Plan:
    objetivo:    str
    pasos:       List[Paso]
    sitio:       str = ''     # youtube|instagram|github|gmail|general
    requiere_login: bool = False
    notas:       str = ''


# ── Detección rápida de sitio ─────────────────────────────

_SITIOS = {
    'youtube':   ['youtube', 'yt ', 'video de ', 'canal de ', 'ponme '],
    'instagram': ['instagram', 'insta', 'ig ', 'escríbele', 'escribele', 'mensaje a'],
    'github':    ['github', 'repositorio', 'repo ', 'código en github'],
    'gmail':     ['gmail', 'correo', 'email', 'mail'],
    'twitter':   ['twitter', 'tweet', 'x.com'],
    'google':    ['busca en google', 'google '],
}

_URLS_BASE = {
    'youtube':   'https://youtube.com',
    'instagram': 'https://instagram.com',
    'github':    'https://github.com',
    'gmail':     'https://mail.google.com',
    'twitter':   'https://x.com',
    'google':    'https://google.com',
}


def detectar_sitio(texto: str) -> str:
    tl = texto.lower()
    for sitio, palabras in _SITIOS.items():
        if any(p in tl for p in palabras):
            return sitio
    return 'general'


# ── Detección de INTENCIÓN (núcleo filosófico) ───────────
# Bell entiende QUÉ quiere hacer, no QUÉ sitio. Así navega
# servicios que nunca vio: infiere la URL en vez de buscarla en una lista.

INTENCIONES = {
    'reproducir_media': ['ponme', 'pon ', 'reproduce', 'abre ', 'quiero ver',
                         'poner ', 'muéstrame', 'muestrame', 'abre la app'],
    'buscar_video':     ['busca en youtube', 'busca un video', 'video de ',
                         'tutorial de ', 'canal de '],
    'buscar_info':      ['busca en google', 'busca en internet', 'investiga',
                         'qué es ', 'que es ', 'cómo funciona', 'como funciona'],
    'mis_datos':        ['mis repos', 'mi perfil', 'mis mensajes', 'mi correo',
                         'mis emails', 'mis archivos'],
    'enviar_mensaje':   ['escríbele', 'escribele', 'manda un mensaje', 'envíale', 'dile'],
    'abrir_url':        ['lee ', 'abre la página', 'abre la pagina', 'navega a ', 've a '],
    'login':            ['inicia sesión', 'inicia sesion', 'loguéate', 'logueate', 'entra a'],
}


def detectar_intencion(texto: str) -> str:
    tl = texto.lower()
    for intencion, patrones in INTENCIONES.items():
        if any(p in tl for p in patrones):
            return intencion
    return 'general'


def inferir_url_sitio(nombre: str) -> str:
    """
    Bell infiere la URL de cualquier servicio sin necesitar una lista.
    Principio: la mayoría de servicios son https://www.{nombre}.com
    """
    nombre_limpio = (nombre or '').lower().strip()
    if not nombre_limpio:
        return ''
    # Conocimiento de visitas anteriores
    try:
        from biblioteca.habilidades.navegador.conocimiento_web import ConocimientoWeb
        url_conocida = ConocimientoWeb.obtener().obtener_sitio(nombre_limpio + '.com')
        if url_conocida.get('url_base'):
            return url_conocida['url_base']
    except Exception:
        pass
    # Excepciones por TLD diferente
    _EXCEPCIONES_TLD = {
        'youtube': 'https://www.youtube.com',
        'gmail':   'https://mail.google.com',
        'twitter': 'https://x.com',
        'x':       'https://x.com',
    }
    if nombre_limpio in _EXCEPCIONES_TLD:
        return _EXCEPCIONES_TLD[nombre_limpio]
    # Regla universal: https://www.{nombre}.com
    return f'https://www.{nombre_limpio}.com'


def _obtener_usuario_github() -> str:
    try:
        from biblioteca.habilidades.memoria.modelo_sebastian import ModeloSebastian
        modelo = ModeloSebastian.obtener().obtener_modelo()
        u = modelo.get('identidad', {}).get('github_usuario', '')
        if u:
            return u
    except Exception:
        pass
    return 'sebastian221-art'  # fallback conocido (dueño del repo)


# ── Planes predefinidos (rápidos, sin Groq) ──────────────

def plan_youtube_video(query: str) -> Plan:
    return Plan(
        objetivo=f"Encontrar y reproducir video: {query}",
        sitio='youtube',
        pasos=[
            Paso(1, 'navegar',  {'url': 'https://youtube.com'}, 'Ir a YouTube'),
            Paso(2, 'esperar',  {'selector': 'input[name="search_query"]'}, 'Esperar barra de búsqueda'),
            Paso(3, 'click',    {'selector': 'input[name="search_query"]'}, 'Click en búsqueda'),
            Paso(4, 'escribir', {'texto': query}, f'Escribir "{query}"'),
            Paso(5, 'tecla',    {'tecla': 'Enter'}, 'Presionar Enter'),
            Paso(6, 'esperar',  {'tiempo': 2000}, 'Esperar resultados'),
            Paso(7, 'leer',     {'tipo': 'youtube_resultados'}, 'Leer lista de videos'),
            Paso(8, 'click',    {'tipo': 'primer_video_relevante'}, 'Click en video seleccionado'),
            Paso(9, 'esperar',  {'tiempo': 2000}, 'Esperar que cargue', opcional=True),
            Paso(10, 'leer',    {'tipo': 'confirmar_video'}, 'Confirmar video cargado'),
        ]
    )


def plan_instagram_mensaje(usuario: str, mensaje: str) -> Plan:
    return Plan(
        objetivo=f"Enviar mensaje a @{usuario}: {mensaje[:50]}",
        sitio='instagram',
        requiere_login=True,
        pasos=[
            Paso(1, 'navegar',  {'url': 'https://instagram.com/direct/inbox'}, 'Ir a mensajes de Instagram'),
            Paso(2, 'esperar',  {'tiempo': 2000}, 'Esperar carga'),
            Paso(3, 'leer',     {'tipo': 'instagram_estado'}, 'Verificar si está logueado'),
            Paso(4, 'click',    {'selector': 'a[href="/direct/new/"]', 'texto': 'Nuevo mensaje'}, 'Nuevo mensaje', opcional=True),
            Paso(5, 'click',    {'texto': 'Nueva conversación', 'selector': '[aria-label="Nueva conversación"]'}, 'Iniciar conversación', opcional=True),
            Paso(6, 'escribir', {'texto': usuario, 'selector': 'input[placeholder*="Buscar"]'}, f'Buscar @{usuario}'),
            Paso(7, 'esperar',  {'tiempo': 1500}, 'Esperar resultados de búsqueda'),
            Paso(8, 'click',    {'texto': usuario}, f'Seleccionar @{usuario}'),
            Paso(9, 'click',    {'texto': 'Chat', 'selector': '[role="button"]:has-text("Chat")'}, 'Abrir chat', opcional=True),
            Paso(10, 'esperar', {'tiempo': 1500}, 'Esperar chat abierto'),
            Paso(11, 'click',   {'selector': 'div[contenteditable="true"], textarea[placeholder]'}, 'Click en input mensaje'),
            Paso(12, 'escribir', {'texto': mensaje}, f'Escribir mensaje'),
            Paso(13, 'tecla',   {'tecla': 'Enter'}, 'Enviar mensaje'),
            Paso(14, 'esperar', {'tiempo': 1000}, 'Esperar confirmación'),
            Paso(15, 'leer',    {'tipo': 'confirmar_mensaje_enviado'}, 'Verificar envío'),
        ]
    )


def plan_github_repos(usuario: str) -> Plan:
    return Plan(
        objetivo=f"Ver repositorios de @{usuario} en GitHub",
        sitio='github',
        pasos=[
            Paso(1, 'navegar', {'url': f'https://github.com/{usuario}?tab=repositories'}, 'Ir a repos'),
            Paso(2, 'esperar', {'tiempo': 4000}, 'Esperar carga JS'),
            # FIX 3: esperar a que el listado renderice (opcional — si no aparece, seguir)
            Paso(3, 'esperar', {'selector': '[data-tab-item="repositories"] li, li.source, [itemprop="owns"]',
                                'timeout': 8000}, 'Esperar render del listado', opcional=True),
            Paso(4, 'leer',    {'tipo': 'github_repos'}, 'Extraer lista de repositorios'),
        ]
    )


def plan_github_repo_url(usuario: str, nombre_repo: str) -> Plan:
    return Plan(
        objetivo=f"Obtener URL del repo {nombre_repo} de @{usuario}",
        sitio='github',
        pasos=[
            Paso(1, 'navegar', {'url': f'https://github.com/{usuario}/{nombre_repo}'}, 'Ir al repo'),
            Paso(2, 'esperar', {'tiempo': 2000}, 'Esperar carga'),
            Paso(3, 'leer',    {'tipo': 'github_url_clone'}, 'Extraer URL de clonación'),
        ]
    )


def plan_leer_url(url: str) -> Plan:
    return Plan(
        objetivo=f"Leer y analizar: {url}",
        sitio='general',
        pasos=[
            Paso(1, 'navegar', {'url': url}, f'Ir a {url[:60]}'),
            Paso(2, 'esperar', {'tiempo': 3000}, 'Esperar carga JS completa'),
            Paso(3, 'scroll',  {'direccion': 'abajo', 'cantidad': 500}, 'Scroll para cargar más contenido', opcional=True),
            Paso(4, 'esperar', {'tiempo': 1500}, 'Esperar contenido dinámico'),
            Paso(5, 'leer',    {'tipo': 'pagina_completa'}, 'Leer todo el contenido'),
        ]
    )


def plan_login_instagram(usuario: str, password: str) -> Plan:
    return Plan(
        objetivo="Iniciar sesión en Instagram",
        sitio='instagram',
        requiere_login=True,
        pasos=[
            Paso(1, 'navegar',  {'url': 'https://instagram.com/accounts/login'}, 'Ir a login'),
            Paso(2, 'esperar',  {'selector': 'input[name="username"]'}, 'Esperar formulario'),
            Paso(3, 'click',    {'selector': 'input[name="username"]'}, 'Click en usuario'),
            Paso(4, 'escribir', {'selector': 'input[name="username"]', 'texto': usuario}, 'Escribir usuario'),
            Paso(5, 'click',    {'selector': 'input[name="password"]'}, 'Click en contraseña'),
            Paso(6, 'escribir', {'selector': 'input[name="password"]', 'texto': password}, 'Escribir contraseña'),
            Paso(7, 'click',    {'selector': 'button[type="submit"]', 'texto': 'Entrar'}, 'Click en entrar'),
            Paso(8, 'esperar',  {'tiempo': 3000}, 'Esperar inicio de sesión'),
            Paso(9, 'leer',     {'tipo': 'verificar_login'}, 'Verificar login exitoso'),
        ]
    )


def plan_gmail_buscar(query: str) -> Plan:
    return Plan(
        objetivo=f"Buscar emails: {query}",
        sitio='gmail',
        requiere_login=True,
        pasos=[
            Paso(1, 'navegar',  {'url': 'https://mail.google.com'}, 'Ir a Gmail'),
            Paso(2, 'esperar',  {'tiempo': 3000}, 'Esperar carga Gmail'),
            Paso(3, 'click',    {'selector': 'input[aria-label*="Buscar"]', 'texto': 'Buscar'}, 'Click en búsqueda'),
            Paso(4, 'escribir', {'texto': query}, f'Buscar "{query}"'),
            Paso(5, 'tecla',    {'tecla': 'Enter'}, 'Buscar'),
            Paso(6, 'esperar',  {'tiempo': 2000}, 'Esperar resultados'),
            Paso(7, 'leer',     {'tipo': 'gmail_lista'}, 'Leer emails encontrados'),
        ]
    )


# ── Planificador con Groq (para objetivos complejos) ─────

def planificar_con_groq(objetivo: str, url_actual: str = '',
                         html_pagina: str = '') -> Optional[Plan]:
    """
    Para objetivos que no tienen plan predefinido,
    Groq desglosa los pasos a ejecutar.
    """
    api_key = os.getenv('GROQ_API_KEY', '')
    if not api_key:
        return None

    contexto_pagina = ''
    if html_pagina:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_pagina[:3000], 'lxml')
        texto = soup.get_text(separator=' ', strip=True)[:800]
        contexto_pagina = f'\nContenido actual de la página: {texto}'

    prompt = f"""Objetivo del usuario: "{objetivo}"
URL actual del browser: {url_actual or "ninguna"}
{contexto_pagina}

Produce un plan JSON con los pasos exactos para lograr el objetivo.
Usa SOLO estas acciones: navegar, click, escribir, tecla, scroll, esperar, leer, screenshot, descargar

Responde SOLO con JSON válido, sin markdown:
{{
  "sitio": "youtube|instagram|github|gmail|general",
  "requiere_login": false,
  "pasos": [
    {{"numero": 1, "accion": "navegar", "parametros": {{"url": "https://..."}}, "descripcion": "..."}},
    {{"numero": 2, "accion": "click", "parametros": {{"selector": "input[name=...]", "texto": "..."}}, "descripcion": "..."}}
  ],
  "notas": "cualquier observación importante"
}}"""

    try:
        import httpx
        r = httpx.post(
            _GROQ_URL,
            headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'},
            json={
                'model': _GROQ_MODEL,
                'messages': [
                    {'role': 'system',
                     'content': 'Eres el planificador de Bell. Produces planes JSON exactos para automatización de browser. Solo JSON, sin explicaciones.'},
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.1,
                'max_tokens': 800,
            },
            timeout=20,
        )
        if r.status_code != 200:
            return None

        contenido = r.json()['choices'][0]['message']['content'].strip()
        # Limpiar markdown
        contenido = re.sub(r'^```(?:json)?\s*', '', contenido)
        contenido = re.sub(r'\s*```$', '', contenido)
        # Extraer solo el JSON entre { y } (ignorar texto antes/después)
        m_json = re.search(r'\{.*\}', contenido, re.DOTALL)
        if m_json:
            contenido = m_json.group()
        # Intentos de parse en orden de confianza
        data = None
        for intento in (
            lambda c: json.loads(c),
            lambda c: json.loads(c.replace("'", '"')),
            lambda c: json.loads(re.sub(r',\s*}', '}', re.sub(r',\s*]', ']', c))),
        ):
            try:
                data = intento(contenido)
                break
            except Exception:
                continue
        if data is None:
            return None

        pasos = [
            Paso(
                numero=p['numero'],
                accion=p['accion'],
                parametros=p.get('parametros', {}),
                descripcion=p.get('descripcion', ''),
                opcional=p.get('opcional', False),
            )
            for p in data.get('pasos', [])
        ]

        return Plan(
            objetivo=objetivo,
            sitio=data.get('sitio', 'general'),
            requiere_login=data.get('requiere_login', False),
            pasos=pasos,
            notas=data.get('notas', ''),
        )

    except Exception as e:
        print(f"  [Planificador] ⚠️  Groq error: {e}")
        return None


# ── Punto de entrada principal ───────────────────────────

def crear_plan(objetivo: str, url_actual: str = '', html_pagina: str = '') -> Plan:
    """
    Crea el plan óptimo para el objetivo dado.
    Usa planes predefinidos cuando puede, Groq cuando es complejo.
    """
    tl = objetivo.lower()
    intencion = detectar_intencion(objetivo)

    # ── INTENCIÓN: reproducir / abrir un servicio ────────
    # "ponme Crunchyroll", "abre Netflix", "quiero ver Spotify".
    # Bell no necesita conocer el servicio — infiere su URL.
    if intencion == 'reproducir_media':
        _VERBOS = ['ponme', 'pon ', 'reproduce', 'abre la app', 'abre ',
                   'quiero ver', 'muéstrame', 'muestrame', 'poner ']
        nombre_servicio = tl
        for v in _VERBOS:
            nombre_servicio = nombre_servicio.replace(v, ' ')
        # YouTube explícito → buscar video
        if 'youtube' in nombre_servicio or any(k in tl for k in ['video de', 'tutorial de']):
            query = re.sub(r'(?:en\s+youtube|video\s+de|tutorial\s+de)\s*', '', nombre_servicio).strip()
            return plan_youtube_video(query or objetivo)
        # Cualquier otro servicio → inferir URL universal y navegar
        _fillers = {'la', 'el', 'los', 'las', 'de', 'del', 'app', 'en', 'un', 'una', 'mi'}
        tokens = [w for w in nombre_servicio.split() if w not in _fillers]
        servicio = tokens[-1] if tokens else nombre_servicio.strip()
        url_destino = inferir_url_sitio(servicio)
        if url_destino:
            return Plan(
                objetivo=f"Abrir {servicio}",
                sitio=servicio,
                pasos=[
                    Paso(1, 'navegar', {'url': url_destino}, f'Ir a {servicio}'),
                    Paso(2, 'esperar', {'tiempo': 3000}, 'Esperar carga'),
                    Paso(3, 'leer',    {'tipo': 'pagina_completa'}, 'Leer estado de la página'),
                ]
            )

    # ── INTENCIÓN: buscar video ──────────────────────────
    if intencion == 'buscar_video':
        query = re.sub(r'(?:busca\s+en\s+youtube|busca\s+un\s+video|video\s+de|tutorial\s+de|canal\s+de)\s*',
                       '', tl).strip()
        return plan_youtube_video(query or objetivo)

    # ── INTENCIÓN: mis datos (repos, mensajes, emails) ───
    if intencion == 'mis_datos':
        if 'github' in tl or 'repo' in tl:
            return plan_github_repos(_obtener_usuario_github())
        if 'gmail' in tl or 'correo' in tl or 'email' in tl:
            return plan_gmail_buscar('')
        if 'instagram' in tl and ('mensaje' in tl or 'dm' in tl):
            return plan_leer_url('https://instagram.com/direct/inbox')

    # ── INTENCIÓN: enviar mensaje ────────────────────────
    if intencion == 'enviar_mensaje' and 'instagram' in tl:
        m = re.search(r'(?:a|@)\s*(\w+)', objetivo)
        usuario = m.group(1) if m else ''
        partes = re.split(r'(?:dile|que diga|diciéndole|mensaje:)\s*', objetivo, 1)
        mensaje = partes[1].strip() if len(partes) > 1 else 'Hola'
        return plan_instagram_mensaje(usuario, mensaje)

    # ── INTENCIÓN: abrir URL específica ──────────────────
    if intencion == 'abrir_url' or re.search(r'https?://', objetivo):
        url_match = re.search(r'https?://\S+', objetivo)
        if url_match:
            return plan_leer_url(url_match.group())

    # ── GitHub: URL de un repo específico ────────────────
    if 'github' in tl and any(p in tl for p in ['url de', 'url del', 'dame la url',
                                                 'link de', 'enlace de']):
        m  = re.search(r'(?:repo|repositorio)\s+([\w\-_\.]+)', objetivo, re.IGNORECASE)
        m2 = re.search(r'(?:usuario\s+|@)([\w\-]+)', objetivo, re.IGNORECASE)
        return plan_github_repo_url(m2.group(1) if m2 else _obtener_usuario_github(),
                                    m.group(1) if m else '')

    # ── Sin intención clara → Groq planifica ─────────────
    print(f"  [Planificador] 🤖 Groq planifica: '{objetivo[:50]}'")
    plan_groq = planificar_con_groq(objetivo, url_actual, html_pagina)
    if plan_groq:
        return plan_groq

    # Último fallback universal: DuckDuckGo (no Google — CAPTCHA a bots)
    from urllib.parse import quote
    return Plan(
        objetivo=objetivo,
        sitio='general',
        pasos=[
            Paso(1, 'navegar', {'url': f'https://html.duckduckgo.com/html/?q={quote(objetivo)}'}, 'Buscar información'),
            Paso(2, 'esperar', {'tiempo': 2000}, 'Esperar resultados'),
            Paso(3, 'leer',    {'tipo': 'pagina_completa'}, 'Leer resultados'),
        ]
    )


# ── Sistema de Pausa — Bell pregunta y espera ─────────────

class EstadoPausa:
    """
    Cuando Bell necesita algo que no tiene,
    guarda el plan pausado y la pregunta pendiente.
    """
    _plan_pendiente:  object = None
    _paso_pendiente:  int    = 0
    _pregunta:        str    = ''
    _tipo_respuesta:  str    = ''  # 'credencial' | 'confirmacion' | 'dato'
    _activo:          bool   = False
    _contexto:        dict   = {}

    @classmethod
    def pausar(cls, plan, paso_actual: int, pregunta: str,
               tipo: str = 'dato', contexto: dict = None):
        cls._plan_pendiente = plan
        cls._paso_pendiente = paso_actual
        cls._pregunta       = pregunta
        cls._tipo_respuesta = tipo
        cls._activo         = True
        cls._contexto       = contexto or {}
        print(f"  [Pausa] ⏸ Plan pausado en paso {paso_actual}: {pregunta[:60]}")

    @classmethod
    def esta_activo(cls) -> bool:
        return cls._activo

    @classmethod
    def obtener_pregunta(cls) -> str:
        return cls._pregunta

    @classmethod
    def obtener_plan(cls) -> object:
        return cls._plan_pendiente

    @classmethod
    def obtener_paso(cls) -> int:
        return cls._paso_pendiente

    @classmethod
    def obtener_tipo(cls) -> str:
        return cls._tipo_respuesta

    @classmethod
    def obtener_contexto(cls) -> dict:
        return cls._contexto

    @classmethod
    def resolver(cls, respuesta: str):
        """Registra la respuesta de Sebastian y despausa."""
        cls._activo = False
        cls._contexto['respuesta_usuario'] = respuesta
        print(f"  [Pausa] ▶ Reanudando con: {respuesta[:40] if respuesta else '(vacío)'}")

    @classmethod
    def cancelar(cls):
        cls._activo         = False
        cls._plan_pendiente = None
        cls._paso_pendiente = 0
        cls._pregunta       = ''

    @classmethod
    def inyectar_credencial(cls, clave: str, valor: str):
        """Inyecta una credencial al contexto del plan pausado."""
        cls._contexto[clave] = valor


def necesita_pausa(objetivo: str, plan) -> tuple:
    """
    Analiza si el plan va a necesitar algo que Bell no tiene.
    Retorna (necesita, pregunta, tipo) antes de ejecutar.
    """
    tl_objetivo = objetivo.lower()

    # ── Login requerido sin sesión guardada ───────────────
    if plan.requiere_login:
        sitio = plan.sitio
        sm_tiene_sesion = False
        try:
            from biblioteca.habilidades.navegador.sesion_manager import SesionManager
            sm_tiene_sesion = SesionManager.obtener().sesion_guardada(sitio)
        except Exception:
            pass

        if not sm_tiene_sesion:
            # Verificar si el usuario ya dio credenciales en el texto
            tiene_usuario = bool(
                __import__('re').search(r'usuario[:\s]+\w+|user[:\s]+\w+|con\s+\w+\s+y\s+\w+', tl_objetivo)
            )
            if not tiene_usuario:
                preguntas = {
                    'instagram': '¿Con qué usuario y contraseña de Instagram entro? (escribe: usuario TU_USUARIO contraseña TU_CONTRASEÑA)',
                    'gmail':     '¿Con qué cuenta de Gmail? Ya deberías estar logueado si tienes Chrome normal. ¿Quieres que abra Chrome visible para que inicies sesión tú?',
                    'github':    '¿Con qué usuario de GitHub? (o ¿ya tienes sesión activa en el browser?)',
                    'twitter':   '¿Con qué usuario y contraseña de Twitter/X?',
                }
                pregunta = preguntas.get(sitio, f'¿Con qué credenciales entro a {sitio}?')
                return True, pregunta, 'credencial'

    # ── Sitios de streaming que necesitan cuenta ──────────
    _sitios_cuenta = {
        'crunchyroll': ('crunchyroll.com', '¿Tienes cuenta en Crunchyroll? Dame usuario y contraseña o dime si ya tienes sesión abierta en Chrome.'),
        'spotify':     ('open.spotify.com', '¿Quieres que abra Spotify Web? Si ya tienes sesión en el browser lo hago directo. Si no, dame las credenciales.'),
        'netflix':     ('netflix.com', '¿Con qué cuenta de Netflix entro?'),
        'disney':      ('disneyplus.com', '¿Con qué cuenta de Disney+ entro?'),
        'twitch':      ('twitch.tv', '¿Con qué cuenta de Twitch entro?'),
        'reddit':      ('reddit.com', 'Reddit no necesita login para leer, pero sí para publicar. ¿Qué necesitas hacer?'),
    }
    for nombre, (dominio, pregunta) in _sitios_cuenta.items():
        if nombre in tl_objetivo:
            try:
                from biblioteca.habilidades.navegador.sesion_manager import SesionManager
                if not SesionManager.obtener().sesion_guardada(dominio):
                    return True, pregunta, 'credencial'
            except Exception:
                return True, pregunta, 'credencial'

    # ── Acciones destructivas — pedir confirmación ────────
    _acciones_destructivas = [
        ('eliminar', '¿Seguro que quieres eliminar esto? Confirma con "sí" o cancela con "no".'),
        ('borrar', '¿Confirmas que quieres borrar? Responde "sí" para continuar.'),
        ('publicar', '¿Confirmas que quieres publicar esto?'),
        ('comprar', '¿Confirmas que quieres realizar esta compra?'),
        ('pagar', '¿Confirmas el pago?'),
        ('enviar dinero', '¿Confirmas que quieres enviar dinero?'),
    ]
    for accion, pregunta in _acciones_destructivas:
        if accion in tl_objetivo:
            return True, pregunta, 'confirmacion'

    return False, '', ''