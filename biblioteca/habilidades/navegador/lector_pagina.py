# biblioteca/habilidades/navegador/lector_pagina.py
# ============================================================
# LECTOR DE PÁGINA — Los ojos de Bell
#
# Convierte el HTML crudo en información estructurada que
# Bell puede usar para tomar decisiones.
#
# Sabe leer:
#   - Páginas genéricas (extraer texto, links, botones)
#   - YouTube (títulos, URLs, fechas de videos)
#   - Instagram (perfil, mensajes, posts)
#   - GitHub (repos, archivos, issues, PRs)
#   - Gmail (lista de emails, asuntos, remitentes)
#   - Cualquier formulario web
#   - Artículos y noticias
#
# Cuando el HTML falla, usa OCR sobre screenshot.
# ============================================================

import re
from dataclasses import dataclass, field
from typing import List, Optional
from bs4 import BeautifulSoup


@dataclass
class ElementoInteractivo:
    tipo:     str    # 'boton' | 'input' | 'link' | 'select' | 'textarea'
    texto:    str
    selector: str
    href:     str = ''
    placeholder: str = ''


@dataclass
class ContenidoPagina:
    url:           str
    titulo:        str
    texto_principal: str          # texto limpio, sin nav/ads
    links:         List[dict]     = field(default_factory=list)
    botones:       List[dict]     = field(default_factory=list)
    inputs:        List[dict]     = field(default_factory=list)
    imagenes:      List[str]      = field(default_factory=list)
    datos_especiales: dict        = field(default_factory=dict)
    # datos_especiales: depende del sitio:
    #   youtube: lista de videos [{titulo, url, canal, fecha}]
    #   instagram: {mensajes: [...], perfil: {...}}
    #   github: {repos: [...], archivos: [...]}
    #   gmail: {emails: [{asunto, remitente, fecha, preview}]}


def leer_pagina(page) -> ContenidoPagina:
    """
    Lee la página actual y extrae toda la información relevante.
    Detecta el tipo de sitio y usa el lector especializado.
    """
    try:
        url   = page.url
        html  = page.content()
        titulo = page.title()
    except Exception:
        return ContenidoPagina(url='', titulo='', texto_principal='Error leyendo página')

    soup = BeautifulSoup(html, 'lxml')
    _limpiar_html(soup)

    # Detectar sitio y usar lector especializado
    if 'youtube.com' in url:
        especial = _leer_youtube(soup, page)
    elif 'instagram.com' in url:
        especial = _leer_instagram(soup, page)
    elif 'github.com' in url:
        especial = _leer_github(soup, url)
    elif 'mail.google.com' in url or 'gmail.com' in url:
        especial = _leer_gmail(soup, page)
    elif 'twitter.com' in url or 'x.com' in url:
        especial = _leer_twitter(soup, page)
    else:
        especial = _leer_general(soup)

    return ContenidoPagina(
        url=url,
        titulo=titulo,
        texto_principal=_extraer_texto_principal(soup),
        links=_extraer_links(soup, url),
        botones=_extraer_botones(soup),
        inputs=_extraer_inputs(soup),
        imagenes=_extraer_imagenes(soup, url),
        datos_especiales=especial,
    )


# ── Limpieza de HTML ─────────────────────────────────────

def _limpiar_html(soup: BeautifulSoup):
    """Elimina elementos que no aportan contenido."""
    for tag in soup.find_all(['script', 'style', 'noscript', 'svg',
                               'meta', 'link', 'head', 'footer',
                               'nav', 'aside', 'advertisement']):
        tag.decompose()
    for attr in ['class', 'style', 'data-testid', 'aria-hidden']:
        for tag in soup.find_all(True):
            if hasattr(tag, 'attrs'):
                tag.attrs.pop(attr, None)


# ── Extracción genérica ──────────────────────────────────

def _extraer_texto_principal(soup: BeautifulSoup) -> str:
    """Extrae el texto principal limpio de la página."""
    # Priorizar article, main, [role=main]
    for selector in ['article', 'main', '[role="main"]', '.content', '#content']:
        el = soup.find(selector.lstrip('.#[').split(']')[0])
        if el and len(el.get_text(strip=True)) > 100:
            texto = el.get_text(separator=' ', strip=True)
            return re.sub(r'\s+', ' ', texto)[:3000]

    # Fallback: todo el body
    body = soup.find('body')
    if body:
        texto = body.get_text(separator=' ', strip=True)
        return re.sub(r'\s+', ' ', texto)[:3000]
    return ''


def _extraer_links(soup: BeautifulSoup, url_base: str) -> List[dict]:
    links = []
    for a in soup.find_all('a', href=True)[:30]:
        href = a.get('href', '')
        texto = a.get_text(strip=True)[:80]
        if texto and href and not href.startswith('javascript:'):
            links.append({'texto': texto, 'href': href})
    return links


def _extraer_botones(soup: BeautifulSoup) -> List[dict]:
    botones = []
    for btn in soup.find_all(['button', 'input'], type=lambda t: t in (None, 'submit', 'button'))[:20]:
        texto = btn.get_text(strip=True) or btn.get('value', '') or btn.get('aria-label', '')
        if texto:
            botones.append({'texto': texto[:60], 'tipo': btn.name})
    return botones


def _extraer_inputs(soup: BeautifulSoup) -> List[dict]:
    inputs = []
    for inp in soup.find_all(['input', 'textarea', 'select'])[:15]:
        tipo = inp.get('type', 'text')
        if tipo in ('hidden', 'submit', 'button', 'image'):
            continue
        inputs.append({
            'tipo': tipo,
            'name': inp.get('name', ''),
            'placeholder': inp.get('placeholder', ''),
            'id': inp.get('id', ''),
            'aria_label': inp.get('aria-label', ''),
        })
    return inputs


def _extraer_imagenes(soup: BeautifulSoup, url_base: str) -> List[str]:
    imgs = []
    for img in soup.find_all('img', src=True)[:10]:
        src = img.get('src', '')
        alt = img.get('alt', '')
        if src and (src.startswith('http') or src.startswith('/')):
            imgs.append(f"{alt}: {src[:100]}" if alt else src[:100])
    return imgs


# ── Lectura de YouTube ───────────────────────────────────

def _leer_youtube(soup: BeautifulSoup, page) -> dict:
    """Extrae videos, títulos, canales y fechas de YouTube."""
    datos = {'tipo': 'youtube', 'videos': [], 'video_actual': ''}

    # Si estamos en un video
    url = page.url
    if 'watch?v=' in url:
        titulo_el = soup.find('h1', class_=re.compile('title'))
        if titulo_el:
            datos['video_actual'] = titulo_el.get_text(strip=True)
        return datos

    # Si estamos en resultados de búsqueda o página de canal
    # YouTube renderiza con JS — necesitamos extraer de la estructura dinámica
    try:
        # Usar JS para obtener los títulos directamente del DOM renderizado
        videos_js = page.evaluate("""() => {
            const items = document.querySelectorAll('ytd-video-renderer, ytd-compact-video-renderer, ytd-grid-video-renderer');
            return Array.from(items).slice(0, 10).map(el => {
                const titulo = el.querySelector('#video-title');
                const canal  = el.querySelector('.ytd-channel-name a, #channel-name');
                const fecha  = el.querySelector('#metadata-line span:last-child, .ytd-grid-video-renderer #metadata-line span');
                const link   = el.querySelector('a#video-title, a.ytd-thumbnail');
                return {
                    titulo: titulo ? titulo.textContent.trim() : '',
                    canal:  canal  ? canal.textContent.trim()  : '',
                    fecha:  fecha  ? fecha.textContent.trim()  : '',
                    url:    link   ? link.href : '',
                };
            }).filter(v => v.titulo);
        }""")
        if videos_js:
            datos['videos'] = videos_js
            print(f"  [Lector] 🎬 YouTube: {len(videos_js)} videos encontrados")
    except Exception:
        pass

    # Fallback: parsear HTML directamente
    if not datos['videos']:
        for h3 in soup.find_all(['h3', 'yt-formatted-string'], id='video-title')[:10]:
            texto = h3.get_text(strip=True)
            if texto:
                datos['videos'].append({'titulo': texto, 'url': '', 'canal': '', 'fecha': ''})

    return datos


# ── Lectura de Instagram ─────────────────────────────────

def _leer_instagram(soup: BeautifulSoup, page) -> dict:
    """Extrae información relevante de Instagram."""
    datos = {'tipo': 'instagram', 'pagina': '', 'elementos': []}

    url = page.url

    # Página de mensajes directos
    if '/direct/' in url or '/inbox' in url:
        datos['pagina'] = 'mensajes'
        try:
            conversaciones = page.evaluate("""() => {
                const convs = document.querySelectorAll('div[role="listbox"] > div, ul li');
                return Array.from(convs).slice(0, 20).map(el => ({
                    nombre: el.querySelector('span') ? el.querySelector('span').textContent.trim() : '',
                    preview: el.textContent.trim().slice(0, 100),
                })).filter(c => c.nombre);
            }""")
            datos['conversaciones'] = conversaciones or []
        except Exception:
            pass

    # Perfil de usuario
    elif re.search(r'instagram\.com/[^/?]+/?$', url):
        datos['pagina'] = 'perfil'
        try:
            info = page.evaluate("""() => {
                const meta = document.querySelector('meta[name="description"]');
                const h1   = document.querySelector('h1, header h2');
                return {
                    descripcion: meta ? meta.content : '',
                    nombre: h1 ? h1.textContent.trim() : '',
                };
            }""")
            datos['perfil'] = info or {}
        except Exception:
            pass

    # Feed o explorar
    else:
        datos['pagina'] = 'feed'
        try:
            posts = page.evaluate("""() => {
                const articles = document.querySelectorAll('article, div[role="presentation"]');
                return Array.from(articles).slice(0, 10).map(el => ({
                    texto: el.textContent.trim().slice(0, 150),
                })).filter(p => p.texto.length > 10);
            }""")
            datos['posts'] = posts or []
        except Exception:
            pass

    return datos


# ── Lectura de GitHub ────────────────────────────────────

def _leer_github(soup: BeautifulSoup, url: str) -> dict:
    """Extrae información de GitHub: repos, archivos, código, issues."""
    datos = {'tipo': 'github', 'pagina': ''}

    # Página de repositorios del usuario
    if re.search(r'github\.com/[^/]+\?tab=repositories', url) or \
       re.search(r'github\.com/[^/]+/?$', url):
        datos['pagina'] = 'perfil_repos'
        repos = []
        for li in soup.find_all('li', class_=re.compile('repo')):
            nombre = li.find('a', itemprop='name codeRepository')
            desc   = li.find('p', class_=re.compile('description'))
            link   = li.find('a', href=True)
            if nombre:
                repo_url = f"https://github.com{link['href']}" if link else ''
                repos.append({
                    'nombre': nombre.get_text(strip=True),
                    'descripcion': desc.get_text(strip=True) if desc else '',
                    'url': repo_url,
                })
        datos['repos'] = repos

    # Repositorio específico
    elif re.search(r'github\.com/[^/]+/[^/]+/?$', url) and \
         'issues' not in url and 'pull' not in url:
        datos['pagina'] = 'repositorio'
        # README
        readme = soup.find(id='readme')
        if readme:
            datos['readme'] = readme.get_text(separator=' ', strip=True)[:1000]
        # Archivos
        archivos = []
        for row in soup.find_all('tr', class_=re.compile('js-navigation-item'))[:20]:
            nombre = row.find(class_=re.compile('js-navigation-open'))
            if nombre:
                archivos.append(nombre.get_text(strip=True))
        datos['archivos'] = archivos
        # URL del repo (clonar)
        clone_input = soup.find('input', id=re.compile('clone'))
        if clone_input:
            datos['url_clone'] = clone_input.get('value', '')

    # Issues
    elif 'issues' in url:
        datos['pagina'] = 'issues'
        issues = []
        for li in soup.find_all('div', class_=re.compile('Box-row'))[:10]:
            titulo = li.find('a', class_=re.compile('Link--primary'))
            numero = li.find('span', class_=re.compile('opened-by'))
            if titulo:
                issues.append({
                    'titulo': titulo.get_text(strip=True),
                    'info': numero.get_text(strip=True) if numero else '',
                    'href': titulo.get('href', ''),
                })
        datos['issues'] = issues

    # Archivo de código
    elif 'blob' in url:
        datos['pagina'] = 'archivo_codigo'
        codigo = soup.find(id='raw-url')
        lineas = soup.find_all('td', class_=re.compile('js-file-line'))[:50]
        if lineas:
            datos['codigo'] = '\n'.join(l.get_text() for l in lineas)

    return datos


# ── Lectura de Gmail ─────────────────────────────────────

def _leer_gmail(soup: BeautifulSoup, page) -> dict:
    """Extrae lista de emails de Gmail."""
    datos = {'tipo': 'gmail', 'emails': []}
    try:
        emails = page.evaluate("""() => {
            const rows = document.querySelectorAll('tr.zA');
            return Array.from(rows).slice(0, 20).map(row => {
                const remitente = row.querySelector('.yP, .zF');
                const asunto    = row.querySelector('.bog span, .y6 span');
                const preview   = row.querySelector('.y2');
                const fecha     = row.querySelector('.xW, .G3');
                return {
                    remitente: remitente ? remitente.textContent.trim() : '',
                    asunto:    asunto    ? asunto.textContent.trim()    : '',
                    preview:   preview   ? preview.textContent.trim()   : '',
                    fecha:     fecha     ? fecha.textContent.trim()     : '',
                    no_leido:  row.classList.contains('zE'),
                };
            }).filter(e => e.asunto || e.remitente);
        }""")
        datos['emails'] = emails or []
    except Exception:
        pass
    return datos


# ── Lectura de Twitter/X ─────────────────────────────────

def _leer_twitter(soup: BeautifulSoup, page) -> dict:
    datos = {'tipo': 'twitter', 'tweets': []}
    try:
        tweets = page.evaluate("""() => {
            const articles = document.querySelectorAll('article[data-testid="tweet"]');
            return Array.from(articles).slice(0, 10).map(a => ({
                texto: a.querySelector('[data-testid="tweetText"]')?.textContent?.trim() || '',
                autor: a.querySelector('[data-testid="User-Name"]')?.textContent?.trim() || '',
            })).filter(t => t.texto);
        }""")
        datos['tweets'] = tweets or []
    except Exception:
        pass
    return datos


# ── Lectura genérica ─────────────────────────────────────

def _leer_general(soup: BeautifulSoup) -> dict:
    datos = {'tipo': 'general'}
    # Detectar si hay formulario de login
    inputs = soup.find_all('input', type=['password'])
    if inputs:
        datos['tiene_login'] = True
    # Detectar si es un formulario
    forms = soup.find_all('form')
    if forms:
        campos = []
        for f in forms[:3]:
            for inp in f.find_all(['input', 'textarea', 'select']):
                name = inp.get('name') or inp.get('placeholder') or inp.get('aria-label', '')
                if name and inp.get('type', 'text') not in ('hidden', 'submit'):
                    campos.append(name)
        datos['campos_formulario'] = campos
    return datos


# ── OCR como último recurso ──────────────────────────────

def leer_screenshot_ocr(screenshot_bytes: bytes) -> str:
    """Extrae texto de un screenshot usando Tesseract OCR."""
    try:
        import pytesseract
        from PIL import Image
        import io
        img  = Image.open(io.BytesIO(screenshot_bytes))
        text = pytesseract.image_to_string(img, lang='spa+eng', config='--psm 3')
        return re.sub(r'\s+', ' ', text).strip()
    except Exception:
        return ''


# ── Encontrar selector de elemento ──────────────────────

def encontrar_selector(page, descripcion: str) -> str:
    """
    Usa Groq para encontrar el selector CSS de un elemento
    dado una descripción en lenguaje natural.
    """
    # Obtener todos los elementos interactivos de la página
    try:
        elementos = page.evaluate("""() => {
            const sels = [];
            const interactivos = document.querySelectorAll(
                'button, a, input, textarea, select, [role="button"], [onclick]'
            );
            Array.from(interactivos).slice(0, 40).forEach((el, i) => {
                const texto = (el.textContent || el.value || el.placeholder ||
                               el.getAttribute('aria-label') || '').trim().slice(0, 60);
                const id    = el.id ? `#${el.id}` : '';
                const cls   = el.className ? `.${el.className.split(' ')[0]}` : '';
                if (texto) sels.push({texto, id, cls, tag: el.tagName.toLowerCase(), i});
            });
            return sels;
        }""")
    except Exception:
        return ''

    if not elementos:
        return ''

    # Buscar el más parecido a la descripción
    desc_lower = descripcion.lower()
    for el in elementos:
        texto_el = el.get('texto', '').lower()
        if any(palabra in texto_el for palabra in desc_lower.split()[:3]):
            if el.get('id'):
                return el['id']
            if el.get('cls'):
                return f"{el['tag']}{el['cls']}"
            return el['tag']

    return ''