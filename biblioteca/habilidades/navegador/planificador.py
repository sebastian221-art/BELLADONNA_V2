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
            Paso(2, 'esperar', {'tiempo': 2000}, 'Esperar carga'),
            Paso(3, 'leer',    {'tipo': 'github_repos'}, 'Extraer lista de repositorios'),
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
        contenido = re.sub(r'^```json\s*', '', contenido)
        contenido = re.sub(r'\s*```$', '', contenido)
        data = json.loads(contenido)

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
    sitio = detectar_sitio(objetivo)

    # ── Plans predefinidos (sin Groq, más rápidos) ───────

    # YouTube
    if sitio == 'youtube':
        query = re.sub(r'(?:ponme|pon|reproduce|busca|encuentra|buscar|ver)\s+', '', tl)
        query = re.sub(r'(?:en\s+youtube|el\s+video\s+de|un\s+video\s+de)\s*', '', query).strip()
        return plan_youtube_video(query or objetivo)

    # Instagram — mensaje directo
    if sitio == 'instagram' and any(p in tl for p in ['escríbele', 'escribele', 'mensaje a', 'manda un mensaje']):
        # Extraer usuario y mensaje
        m = re.search(r'(?:a|@)\s*(\w+)', objetivo)
        usuario = m.group(1) if m else ''
        # El mensaje es todo lo que viene después del usuario
        partes = re.split(r'(?:dile|que diga|diciéndole|con el mensaje|mensaje:)\s*', objetivo, 1)
        mensaje = partes[1].strip() if len(partes) > 1 else 'Hola'
        return plan_instagram_mensaje(usuario, mensaje)

    # GitHub — buscar repos
    if sitio == 'github' and any(p in tl for p in ['repositorios', 'repos', 'mis repos']):
        # Buscar "usuario X" o "@X" con soporte para guiones y números
        m = re.search(r'(?:usuario\s+|@)([\w\-]+)', objetivo, re.IGNORECASE)
        usuario = m.group(1) if m else ''
        return plan_github_repos(usuario)

    # GitHub — URL de repo específico
    if sitio == 'github' and any(p in tl for p in ['url de', 'link de', 'enlace de',
                                                      'url del', 'dame la url', 'dame url']):
        m = re.search(r'(?:repo|repositorio)\s+([\w\-_\.]+)', objetivo, re.IGNORECASE)
        repo = m.group(1) if m else ''
        m2 = re.search(r'(?:usuario\s+|@)([\w\-]+)', objetivo, re.IGNORECASE)
        usuario = m2.group(1) if m2 else ''
        return plan_github_repo_url(usuario, repo)

    # Leer una URL específica
    if any(p in tl for p in ['lee ', 'leer ', 'analiza ', 'qué dice', 'que dice']) or \
       re.search(r'https?://', objetivo):
        url_match = re.search(r'https?://\S+', objetivo)
        if url_match:
            return plan_leer_url(url_match.group())

    # Gmail — buscar emails
    if sitio == 'gmail':
        query = re.sub(r'(?:busca|encuentra|emails de|correos de|mensajes de)\s*', '', tl).strip()
        return plan_gmail_buscar(query)

    # ── Groq para lo que no tiene plan predefinido ───────
    print(f"  [Planificador] 🤖 Usando Groq para planificar: '{objetivo[:50]}'")
    plan_groq = planificar_con_groq(objetivo, url_actual, html_pagina)
    if plan_groq:
        return plan_groq

    # Fallback: navegar si hay URL en el texto
    url_match = re.search(r'https?://\S+', objetivo)
    if url_match:
        return plan_leer_url(url_match.group())

    # Último fallback: buscar en Google
    return Plan(
        objetivo=objetivo,
        sitio='google',
        pasos=[
            Paso(1, 'navegar', {'url': f'https://google.com/search?q={objetivo}'}, 'Buscar en Google'),
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