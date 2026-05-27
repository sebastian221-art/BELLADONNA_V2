# biblioteca/habilidades/navegador/motor_navegador.py
# ============================================================
# MOTOR NAVEGADOR — El director de orquesta
#
# Punto de entrada único para toda la habilidad.
# Recibe el texto de Sebastian, decide qué hacer,
# coordina planificador → ejecutor → Groq narrativa.
#
# Flujo completo:
#   1. Entender el objetivo (qué quiere Sebastian)
#   2. Crear el plan (planificador.py)
#   3. Ejecutar el plan (ejecutor_plan.py)
#   4. Narrar el resultado con voz Bell (Groq)
#
# Principio Mente Pura:
#   Python hace TODO el trabajo real.
#   Groq solo narra lo que Bell realmente hizo.
# ============================================================

import os
import re
from typing import Optional

_GROQ_URL   = 'https://api.groq.com/openai/v1/chat/completions'
_GROQ_MODEL = 'openai/gpt-oss-120b'


def ejecutar(texto: str, visible: bool = False) -> dict:
    """
    Punto de entrada principal de la habilidad navegador.

    Args:
        texto:   Lo que Sebastian quiere hacer en el browser
        visible: True = mostrar Chrome abierto, False = headless

    Returns:
        dict con 'exitoso', 'respuesta', 'datos', 'url_final', 'pausado'
    """
    # FIX 1: browser fresco en cada request — el del request anterior quedó
    # en un thread muerto (Flask threading) → "cannot switch to a different thread".
    from biblioteca.habilidades.navegador.sesion_manager import SesionManager
    SesionManager.reiniciar()

    from biblioteca.habilidades.navegador.planificador import (
        crear_plan, necesita_pausa, EstadoPausa
    )
    from biblioteca.habilidades.navegador.ejecutor_plan import EjecutorPlan
    from biblioteca.habilidades.navegador.sesion_manager import SesionManager

    print(f"  [Navegador] 🌐 Objetivo: {texto[:70]}")

    # ── CASO 1: Hay un plan pausado — Sebastian respondió ────
    if EstadoPausa.esta_activo():
        return _retomar_plan_pausado(texto)

    # ── CASO 2: Plan nuevo ───────────────────────────────────
    sm = SesionManager.obtener()
    sm.asegurar_activo(visible=visible)

    url_actual = ''
    try:
        p = sm.pagina_actual()
        url_actual = p.url if p else ''
    except Exception:
        pass

    plan = crear_plan(texto, url_actual=url_actual)
    print(f"  [Navegador] 📋 Plan: {len(plan.pasos)} pasos | sitio={plan.sitio}")

    # ── VERIFICAR si necesita algo antes de ejecutar ─────────
    necesita, pregunta, tipo_resp = necesita_pausa(texto, plan)
    if necesita:
        EstadoPausa.pausar(plan, 0, pregunta, tipo_resp, {'objetivo_original': texto})
        return {
            'exitoso':   False,
            'pausado':   True,
            'respuesta': pregunta,
            'datos':     {},
            'url_final': '',
        }

    # ── Ejecutar directamente ────────────────────────────────
    ejecutor  = EjecutorPlan()
    resultado = ejecutor.ejecutar(plan)

    if plan.requiere_login and resultado.exitoso:
        sm.guardar_sesion(plan.sitio)

    respuesta = _narrar_resultado(texto, plan, resultado)

    # Cerrar browser después de cada request — garantiza thread safety con Flask
    # La próxima petición abre un browser fresco en su propio thread
    try:
        sm.cerrar()
    except Exception:
        pass

    return {
        'exitoso':   resultado.exitoso,
        'pausado':   False,
        'respuesta': respuesta,
        'datos':     resultado.datos_extraidos,
        'url_final': resultado.url_final,
        'resumen':   resultado.resumen,
    }


def _retomar_plan_pausado(respuesta_sebastian: str) -> dict:
    """
    Sebastian respondió la pregunta — reanudar el plan.
    Extrae las credenciales del texto y continúa.
    """
    from biblioteca.habilidades.navegador.planificador import EstadoPausa
    from biblioteca.habilidades.navegador.ejecutor_plan import EjecutorPlan
    from biblioteca.habilidades.navegador.sesion_manager import SesionManager
    import re

    plan      = EstadoPausa.obtener_plan()
    tipo      = EstadoPausa.obtener_tipo()
    contexto  = EstadoPausa.obtener_contexto()
    objetivo  = contexto.get('objetivo_original', '')

    print(f"  [Navegador] ▶ Reanudando: '{objetivo[:50]}'")

    # Cancelar si Sebastian dice no
    tl = respuesta_sebastian.lower()
    if any(p in tl for p in ['no', 'cancela', 'olvídalo', 'olvida', 'no quiero']):
        EstadoPausa.cancelar()
        return {
            'exitoso':   False,
            'pausado':   False,
            'respuesta': 'Entendido — cancelado.',
            'datos':     {},
            'url_final': '',
        }

    # Extraer credenciales del texto de Sebastian
    if tipo == 'credencial':
        _extraer_credenciales(respuesta_sebastian, plan, contexto)

    EstadoPausa.resolver(respuesta_sebastian)

    # Re-crear plan con las credenciales inyectadas
    from biblioteca.habilidades.navegador.planificador import crear_plan, plan_login_instagram

    plan_actualizado = _actualizar_plan_con_credenciales(plan, contexto)

    sm = SesionManager.obtener()
    sm.asegurar_activo()

    ejecutor  = EjecutorPlan()
    resultado = ejecutor.ejecutar(plan_actualizado)

    if plan_actualizado.requiere_login and resultado.exitoso:
        sm.guardar_sesion(plan_actualizado.sitio)

    respuesta = _narrar_resultado(objetivo, plan_actualizado, resultado)
    return {
        'exitoso':   resultado.exitoso,
        'pausado':   False,
        'respuesta': respuesta,
        'datos':     resultado.datos_extraidos,
        'url_final': resultado.url_final,
        'resumen':   resultado.resumen,
    }


def _extraer_credenciales(texto: str, plan, contexto: dict):
    """Extrae usuario/contraseña del texto de Sebastian."""
    import re
    tl = texto.lower()

    # Patrones: "usuario xxx contraseña yyy" o "user xxx pass yyy"
    m_user = re.search(
        r'(?:usuario|user|email|correo)[:\s]+([^\s,]+)', tl
    )
    m_pass = re.search(
        r'(?:contraseña|contrasena|clave|password|pass)[:\s]+([^\s,]+)', texto
    )

    if m_user:
        contexto['usuario'] = m_user.group(1)
        print(f"  [Navegador] 🔑 Usuario extraído: {contexto['usuario']}")
    if m_pass:
        contexto['password'] = m_pass.group(1)
        print(f"  [Navegador] 🔑 Contraseña extraída: ***")


def _actualizar_plan_con_credenciales(plan, contexto: dict):
    """Actualiza el plan con las credenciales obtenidas."""
    from biblioteca.habilidades.navegador.planificador import (
        plan_login_instagram, Paso
    )

    usuario  = contexto.get('usuario', '')
    password = contexto.get('password', '')

    # Si el sitio es Instagram y tenemos credenciales
    if plan.sitio == 'instagram' and usuario and password:
        # Crear plan de login + el plan original
        plan_login = plan_login_instagram(usuario, password)
        pasos_combinados = plan_login.pasos + [
            Paso(len(plan_login.pasos)+i+1, p.accion, p.parametros,
                 p.descripcion, p.opcional)
            for i, p in enumerate(plan.pasos)
        ]
        plan.pasos = pasos_combinados
        return plan

    return plan


def _abrir_en_browser_sistema(url: str, sitio: str = '') -> str:
    """
    Para medios (YouTube, Spotify, Netflix) abre la URL en el browser del sistema.
    El usuario ve el video/música en su browser real con su cuenta.
    """
    import webbrowser
    try:
        webbrowser.open(url)
        nombre = {
            'youtube': 'YouTube',
            'spotify': 'Spotify',
            'netflix': 'Netflix',
            'crunchyroll': 'Crunchyroll',
            'twitch': 'Twitch',
        }.get(sitio, 'el navegador')
        print(f"  [Navegador] 🌐 Abriendo en {nombre} del sistema: {url[:60]}")
        return nombre
    except Exception as e:
        return ''


def _narrar_resultado(objetivo: str, plan, resultado) -> str:
    """
    Groq recibe los datos REALES y produce la narrativa Bell.
    Si Groq no está disponible, usa template local.
    """
    datos = resultado.datos_extraidos

    # Para YouTube: abrir el video en el browser del sistema
    _SITIOS_MEDIA = {'youtube', 'spotify', 'netflix', 'crunchyroll', 'twitch'}
    if plan.sitio in _SITIOS_MEDIA and resultado.url_final:
        nombre_browser = _abrir_en_browser_sistema(resultado.url_final, plan.sitio)
        if nombre_browser and plan.sitio == 'youtube':
            video = (datos.get('video_reproduciendo') or
                     datos.get('video_seleccionado', {}).get('titulo', ''))
            msg = f"Abrí en tu {nombre_browser}"
            if video:
                msg += f": '{video}'"
            msg += f". URL: {resultado.url_final}"
            return msg

    # ── Template local (sin Groq) — siempre disponible ───
    respuesta_local = _template_local(objetivo, plan.sitio, datos, resultado)

    # ── Intentar con Groq para respuesta más natural ──────
    api_key = os.getenv('GROQ_API_KEY', '')
    if not api_key:
        return respuesta_local

    # Construir contexto de lo que Bell hizo
    contexto = _construir_contexto_groq(objetivo, plan, resultado, datos)

    try:
        import httpx
        r = httpx.post(
            _GROQ_URL,
            headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'},
            json={
                'model': _GROQ_MODEL,
                'messages': [
                    {'role': 'system', 'content': _SYSTEM_NAVEGADOR},
                    {'role': 'user', 'content': contexto}
                ],
                'temperature': 0.4,
                'max_tokens': 400,
            },
            timeout=15,
        )
        if r.status_code == 200:
            resp = r.json()['choices'][0]['message']['content'].strip()
            if resp and len(resp) > 10:
                print(f"  [Navegador] ✅ Groq narró resultado")
                return resp
    except Exception as e:
        print(f"  [Navegador] ⚠️  Groq falló: {e}")

    return respuesta_local


def _construir_contexto_groq(objetivo: str, plan, resultado, datos: dict) -> str:
    """Construye el contexto para Groq con todos los datos reales."""
    lineas = [
        f'<objetivo>"{objetivo}"</objetivo>',
        f'<sitio>{plan.sitio}</sitio>',
        f'<exito>{"sí" if resultado.exitoso else "no"}</exito>',
        f'<url_final>{resultado.url_final}</url_final>',
    ]

    if datos.get('videos_youtube'):
        vids = datos['videos_youtube'][:3]
        lineas.append('<videos_encontrados>')
        for v in vids:
            lineas.append(f'  - "{v.get("titulo","")}" de {v.get("canal","")} ({v.get("fecha","")})')
        lineas.append('</videos_encontrados>')

    if datos.get('video_reproduciendo'):
        lineas.append(f'<video_reproduciendo>{datos["video_reproduciendo"]}</video_reproduciendo>')

    if datos.get('mensaje_enviado'):
        lineas.append('<mensaje>enviado exitosamente</mensaje>')

    if datos.get('repos_github'):
        repos = datos['repos_github'][:5]
        lineas.append('<repositorios>')
        for r in repos:
            lineas.append(f'  - {r.get("nombre","")} — {r.get("url","")}')
        lineas.append('</repositorios>')

    if datos.get('url_repo'):
        lineas.append(f'<url_repo>{datos["url_repo"]}</url_repo>')

    if datos.get('emails'):
        emails = datos['emails'][:5]
        lineas.append('<emails>')
        for e in emails:
            lineas.append(f'  - De: {e.get("remitente","")} | Asunto: {e.get("asunto","")}')
        lineas.append('</emails>')

    if datos.get('titulo_pagina'):
        lineas.append(f'<titulo_pagina>{datos["titulo_pagina"]}</titulo_pagina>')

    if datos.get('headings'):
        lineas.append(f'<secciones_pagina>{" | ".join(datos["headings"][:6])}</secciones_pagina>')

    if datos.get('texto_pagina'):
        lineas.append(f'<contenido_pagina>{datos["texto_pagina"][:1200]}</contenido_pagina>')

    if datos.get('links'):
        links_str = ' | '.join(f"{l.get('texto','')[:30]}" for l in datos['links'][:6] if l.get('texto'))
        if links_str:
            lineas.append(f'<links_principales>{links_str}</links_principales>')

    if resultado.error_critico:
        lineas.append(f'<error>{resultado.error_critico}</error>')

    return '\n'.join(lineas)


def _template_local(objetivo: str, sitio: str, datos: dict, resultado) -> str:
    """Respuesta sin Groq — siempre funciona."""
    if not resultado.exitoso:
        error = resultado.error_critico or 'No pude completar la acción'
        return f"Intenté pero no pude: {error}. Dime si quieres que reintente."

    if sitio == 'youtube':
        video = datos.get('video_reproduciendo') or datos.get('video_seleccionado', {}).get('titulo', '')
        if video:
            return f"Reproduciendo: '{video}'"
        vids = datos.get('videos_youtube', [])
        if vids:
            return f"Encontré {len(vids)} videos. Primero: '{vids[0].get('titulo','')}'"
        return "Abrí YouTube."

    if sitio == 'instagram':
        if datos.get('mensaje_enviado'):
            return "Mensaje enviado."
        if datos.get('instagram_logueado') == False:
            return "Instagram necesita que inicies sesión. ¿Quieres que lo haga?"
        return "En Instagram."

    if sitio == 'github':
        if datos.get('url_repo'):
            return f"URL del repo: {datos['url_repo']}"
        repos = datos.get('repos_github', [])
        if repos:
            nombres = [r.get('nombre', '') for r in repos[:5]]
            return f"Repos: {', '.join(nombres)}"
        return "En GitHub."

    if sitio == 'gmail':
        emails = datos.get('emails', [])
        if emails:
            return f"Encontré {len(emails)} emails."
        return "Revisé Gmail."

    titulo = datos.get('titulo_pagina', '')
    texto  = datos.get('texto_pagina', '')[:200]
    if titulo:
        return f"'{titulo}' — {texto}" if texto else f"'{titulo}'"
    return resultado.resumen or "Listo."


_SYSTEM_NAVEGADOR = """Eres Bell. Controlaste el browser y tienes los datos REALES.

REGLAS ABSOLUTAS:
1. SOLO describe lo que los datos dicen — nunca inventes
2. Para páginas web: da un resumen ÚTIL — qué tiene, para qué sirve, qué encontraste importante
3. Incluye datos exactos: títulos, URLs, nombres, precios, fechas — lo que sea relevante
4. Si hay headings, úsalos para estructurar el resumen
5. Si algo falló, dilo directamente
6. Voz Bell: directa, informativa, sin "Aquí tienes:" ni "Por supuesto:"
7. Para páginas de contenido: mínimo 3-5 oraciones con la información real encontrada

EJEMPLOS buenos:
✅ "python.org es el sitio oficial de Python. Tiene documentación, descargas (Python 3.13 actual), 
   tutoriales para principiantes, el Python Package Index (PyPI) y noticias de la comunidad.
   También incluye una shell interactiva para probar código sin instalar nada."
✅ "El repo BELLADONNA_V2 de sebastian221-art tiene 300 nodos, 724 conexiones.
   URL: https://github.com/sebastian221-art/BELLADONNA_V2.git"
✅ "Abrí el video de Fireship en tu YouTube. Título: 'I can\'t believe this trial is real'"
❌ "La página muestra un mensaje de fallback..." (demasiado vago)
❌ "Aquí tienes los resultados..."
"""


# ── Función auxiliar: Bell describe qué puede hacer ─────

def describir_capacidades() -> str:
    return """Puedo controlar el browser por ti:
• YouTube: buscar y reproducir videos
• Instagram: enviar mensajes directos, leer perfil, ver feed
• GitHub: ver repos, obtener URLs, leer código
• Gmail: buscar emails, leer mensajes
• Cualquier página web: leer contenido, hacer click, llenar formularios
• Login: iniciar sesión en cualquier sitio (y recordar la sesión)
• Descarga: guardar archivos de cualquier página
Dime qué necesitas y lo hago."""