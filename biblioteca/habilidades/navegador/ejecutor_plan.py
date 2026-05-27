# biblioteca/habilidades/navegador/ejecutor_plan.py
# ============================================================
# EJECUTOR DE PLAN — Hace que el plan se vuelva realidad
#
# Toma el plan del planificador y ejecuta cada paso.
# Si algo falla:
#   1. Intenta estrategia alternativa
#   2. Toma screenshot para diagnóstico
#   3. Si es paso opcional → continúa
#   4. Si es crítico → pide a Groq que adapte el plan
#
# Principio: Bell nunca miente sobre lo que hizo.
# Si no pudo hacer algo, lo dice exactamente.
# ============================================================

import time
from dataclasses import dataclass, field
from typing import List, Optional

from biblioteca.habilidades.navegador.planificador import Plan, Paso
from biblioteca.habilidades.navegador.controlador_browser import ControladorBrowser
from biblioteca.habilidades.navegador.lector_pagina import (
    leer_pagina, leer_screenshot_ocr
)


@dataclass
class ResultadoPaso:
    numero:    int
    accion:    str
    exitoso:   bool
    detalle:   str = ''
    error:     str = ''


@dataclass
class ResultadoEjecucion:
    exitoso:         bool
    objetivo:        str
    pasos_ejecutados: List[ResultadoPaso] = field(default_factory=list)
    datos_extraidos: dict                 = field(default_factory=dict)
    url_final:       str                  = ''
    screenshot:      bytes                = b''
    resumen:         str                  = ''
    error_critico:   str                  = ''


class EjecutorPlan:
    """Ejecuta planes paso a paso con manejo de errores inteligente."""

    def __init__(self):
        self._ctrl    = ControladorBrowser()
        self._datos   = {}   # datos acumulados durante la ejecución
        self._pagina  = None

    def ejecutar(self, plan: Plan) -> ResultadoEjecucion:
        """Ejecuta el plan completo y retorna resultado consolidado."""
        print(f"  [Ejecutor] 🎯 Objetivo: {plan.objetivo[:60]}")
        print(f"  [Ejecutor] 📋 {len(plan.pasos)} pasos a ejecutar")

        resultado = ResultadoEjecucion(exitoso=False, objetivo=plan.objetivo)
        pasos_ok  = 0

        for paso in plan.pasos:
            print(f"  [Ejecutor] ▶ Paso {paso.numero}: {paso.descripcion or paso.accion}")

            res_paso = self._ejecutar_paso(paso)
            resultado.pasos_ejecutados.append(res_paso)

            if res_paso.exitoso:
                pasos_ok += 1
            elif not paso.opcional:
                # Paso crítico falló — intentar alternativa
                alt = self._intentar_alternativa(paso, res_paso.error)
                if alt and alt.exitoso:
                    resultado.pasos_ejecutados[-1] = alt
                    pasos_ok += 1
                else:
                    # Fallo real en paso crítico
                    print(f"  [Ejecutor] ❌ Paso {paso.numero} falló: {res_paso.error[:60]}")
                    # Si es un paso de lectura, puede continuar
                    if paso.accion not in ('navegar', 'escribir'):
                        continue
                    resultado.error_critico = f"Paso {paso.numero} ({paso.accion}): {res_paso.error}"
                    break
            else:
                print(f"  [Ejecutor] ⏭ Paso {paso.numero} opcional falló — continuando")

        # Consolidar datos
        resultado.exitoso        = pasos_ok >= max(1, len(plan.pasos) // 2)
        resultado.datos_extraidos = self._datos
        resultado.url_final      = self._url_actual()
        resultado.resumen        = self._generar_resumen(plan, resultado)

        print(f"  [Ejecutor] {'✅' if resultado.exitoso else '⚠️'} {pasos_ok}/{len(plan.pasos)} pasos OK")
        return resultado

    # ── Ejecutor de paso individual ───────────────────────

    def _ejecutar_paso(self, paso: Paso) -> ResultadoPaso:
        """Despacha el paso al método correcto."""
        acc = paso.accion
        p   = paso.parametros

        try:
            if acc == 'navegar':
                return self._paso_navegar(paso)
            elif acc == 'click':
                return self._paso_click(paso)
            elif acc == 'escribir':
                return self._paso_escribir(paso)
            elif acc == 'tecla':
                return self._paso_tecla(paso)
            elif acc == 'scroll':
                return self._paso_scroll(paso)
            elif acc == 'esperar':
                return self._paso_esperar(paso)
            elif acc == 'leer':
                return self._paso_leer(paso)
            elif acc == 'screenshot':
                return self._paso_screenshot(paso)
            elif acc == 'descargar':
                return self._paso_descargar(paso)
            else:
                return ResultadoPaso(paso.numero, acc, False, error=f"Acción desconocida: {acc}")
        except Exception as e:
            return ResultadoPaso(paso.numero, acc, False, error=str(e)[:200])

    def _paso_navegar(self, paso: Paso) -> ResultadoPaso:
        url = paso.parametros.get('url', '')
        if not url:
            return ResultadoPaso(paso.numero, 'navegar', False, error='URL vacía')
        res = self._ctrl.navegar(url)
        if res.exitoso:
            self._datos['url_actual'] = res.url_actual
        return ResultadoPaso(paso.numero, 'navegar', res.exitoso,
                             detalle=res.detalle, error=res.error)

    def _paso_click(self, paso: Paso) -> ResultadoPaso:
        p = paso.parametros

        # Click en primer video relevante (YouTube especial)
        if p.get('tipo') == 'primer_video_relevante':
            return self._click_primer_video()

        selector = p.get('selector', '')
        texto    = p.get('texto', '')

        # Intentar múltiples selectores si se dan separados por coma
        selectores = [s.strip() for s in selector.split(',') if s.strip()] if selector else []

        for sel in selectores:
            res = self._ctrl.click(selector=sel, texto=texto)
            if res.exitoso:
                return ResultadoPaso(paso.numero, 'click', True, detalle=res.detalle)

        # Último intento: solo por texto
        if texto and not selectores:
            res = self._ctrl.click(texto=texto)
            if res.exitoso:
                return ResultadoPaso(paso.numero, 'click', True, detalle=res.detalle)

        return ResultadoPaso(paso.numero, 'click', False,
                             error=f"No encontré: selector={selector[:40]} texto={texto[:40]}")

    def _paso_escribir(self, paso: Paso) -> ResultadoPaso:
        p = paso.parametros
        texto    = p.get('texto', '')
        selector = p.get('selector', '')
        res = self._ctrl.escribir(selector=selector, texto=texto)
        return ResultadoPaso(paso.numero, 'escribir', res.exitoso,
                             detalle=res.detalle, error=res.error)

    def _paso_tecla(self, paso: Paso) -> ResultadoPaso:
        tecla = paso.parametros.get('tecla', 'Enter')
        res   = self._ctrl.presionar_tecla(tecla)
        return ResultadoPaso(paso.numero, 'tecla', res.exitoso,
                             detalle=tecla, error=res.error)

    def _paso_scroll(self, paso: Paso) -> ResultadoPaso:
        p = paso.parametros
        res = self._ctrl.scroll(p.get('direccion', 'abajo'), p.get('cantidad', 500))
        return ResultadoPaso(paso.numero, 'scroll', res.exitoso, detalle=res.detalle)

    def _paso_esperar(self, paso: Paso) -> ResultadoPaso:
        p = paso.parametros
        if 'tiempo' in p:
            time.sleep(p['tiempo'] / 1000)
            return ResultadoPaso(paso.numero, 'esperar', True, detalle=f"{p['tiempo']}ms")
        if 'selector' in p:
            encontrado = self._ctrl.esperar_elemento(p['selector'], timeout=10_000)
            return ResultadoPaso(paso.numero, 'esperar', encontrado,
                                 detalle=p['selector'],
                                 error='' if encontrado else f"No apareció: {p['selector']}")
        time.sleep(1)
        return ResultadoPaso(paso.numero, 'esperar', True)

    def _paso_leer(self, paso: Paso) -> ResultadoPaso:
        """Lee la página y guarda los datos extraídos."""
        tipo = paso.parametros.get('tipo', 'pagina_completa')
        page = self._ctrl._page
        if not page:
            return ResultadoPaso(paso.numero, 'leer', False, error='No hay página activa')

        contenido = leer_pagina(page)

        # Guardar según el tipo
        if tipo == 'youtube_resultados':
            videos = contenido.datos_especiales.get('videos', [])
            self._datos['videos_youtube'] = videos
            self._datos['video_seleccionado'] = videos[0] if videos else {}
            return ResultadoPaso(paso.numero, 'leer', True,
                                 detalle=f"{len(videos)} videos encontrados")

        elif tipo == 'primer_video_relevante':
            videos = self._datos.get('videos_youtube', [])
            self._datos['video_seleccionado'] = videos[0] if videos else {}
            return ResultadoPaso(paso.numero, 'leer', bool(videos),
                                 detalle=videos[0].get('titulo', '') if videos else '')

        elif tipo == 'confirmar_video':
            video_actual = contenido.datos_especiales.get('video_actual', '')
            self._datos['video_reproduciendo'] = video_actual or contenido.titulo
            return ResultadoPaso(paso.numero, 'leer', True,
                                 detalle=f"Reproduciendo: {video_actual[:60]}")

        elif tipo == 'instagram_estado':
            url = contenido.url
            logueado = 'login' not in url and 'accounts' not in url
            self._datos['instagram_logueado'] = logueado
            return ResultadoPaso(paso.numero, 'leer', True,
                                 detalle='logueado' if logueado else 'necesita login')

        elif tipo == 'confirmar_mensaje_enviado':
            self._datos['mensaje_enviado'] = True
            return ResultadoPaso(paso.numero, 'leer', True, detalle='Mensaje enviado')

        elif tipo == 'github_repos':
            repos = contenido.datos_especiales.get('repos', [])
            self._datos['repos_github'] = repos
            return ResultadoPaso(paso.numero, 'leer', True,
                                 detalle=f"{len(repos)} repos encontrados")

        elif tipo == 'github_url_clone':
            url_clone = contenido.datos_especiales.get('url_clone', '')
            if not url_clone:
                # Extraer de la URL actual
                url_clone = contenido.url
            self._datos['url_repo'] = url_clone
            return ResultadoPaso(paso.numero, 'leer', bool(url_clone),
                                 detalle=f"URL: {url_clone}")

        elif tipo == 'gmail_lista':
            emails = contenido.datos_especiales.get('emails', [])
            self._datos['emails'] = emails
            return ResultadoPaso(paso.numero, 'leer', True,
                                 detalle=f"{len(emails)} emails encontrados")

        elif tipo == 'verificar_login':
            url = contenido.url
            exito = 'login' not in url and 'signin' not in url
            self._datos['login_exitoso'] = exito
            return ResultadoPaso(paso.numero, 'leer', True,
                                 detalle='login OK' if exito else 'login fallido')

        else:
            page = self._ctrl._page
            texto_rico = contenido.texto_principal

            # Extraer contenido JS-rendered si el texto básico es escaso
            if page and len(texto_rico) < 500:
                try:
                    _js = (
                        '() => {'
                        ' const sels = ["main","article","#content",".content","body"];'
                        ' for (const s of sels) {'
                        '  const el = document.querySelector(s);'
                        '  if (el) { const t = el.innerText || el.textContent;'
                        '    if (t && t.trim().length > 200) return t.trim().slice(0,3000); }'
                        ' } return document.body.innerText.slice(0,3000); }'
                    )
                    texto_js = page.evaluate(_js)
                    if texto_js and len(texto_js) > len(texto_rico):
                        texto_rico = texto_js
                except Exception:
                    pass

            # Extraer headings para estructura
            headings = []
            try:
                if page:
                    _js_h = (
                        '() => Array.from(document.querySelectorAll("h1,h2,h3"))'
                        '.slice(0,8).map(h => h.innerText.trim()).filter(t => t.length > 2)'
                    )
                    headings = page.evaluate(_js_h) or []
            except Exception:
                pass

            self._datos['texto_pagina']     = texto_rico
            self._datos['titulo_pagina']    = contenido.titulo
            self._datos['url_pagina']       = contenido.url
            self._datos['links']            = contenido.links[:15]
            self._datos['headings']         = headings
            self._datos['datos_especiales'] = contenido.datos_especiales
            chars = len(texto_rico)
            print(f"  [Lector] \U0001f4c4 {chars} chars | {len(headings)} headings | {len(contenido.links)} links")
            return ResultadoPaso(paso.numero, 'leer', True,
                                 detalle=f"{chars} chars leídos")

    def _paso_screenshot(self, paso: Paso) -> ResultadoPaso:
        ss = self._ctrl.screenshot()
        if ss:
            self._datos['screenshot'] = ss
            # Si hay OCR configurado, también extraer texto
            texto_ocr = leer_screenshot_ocr(ss)
            if texto_ocr:
                self._datos['texto_ocr'] = texto_ocr
            return ResultadoPaso(paso.numero, 'screenshot', True,
                                 detalle=f"{len(ss)} bytes")
        return ResultadoPaso(paso.numero, 'screenshot', False, error='Screenshot vacío')

    def _paso_descargar(self, paso: Paso) -> ResultadoPaso:
        p   = paso.parametros
        res = self._ctrl.descargar(p.get('selector', ''), p.get('ruta', ''))
        return ResultadoPaso(paso.numero, 'descargar', res.exitoso,
                             detalle=res.detalle, error=res.error)

    # ── Click inteligente en primer video YouTube ────────

    def _click_primer_video(self) -> ResultadoPaso:
        """Hace click en el primer video relevante de YouTube."""
        page = self._ctrl._page
        if not page:
            return ResultadoPaso(0, 'click', False, error='Sin página')

        video = self._datos.get('video_seleccionado', {})
        url   = video.get('url', '')

        # Estrategia 1: navegar directamente a la URL del video
        if url and url.startswith('http'):
            res = self._ctrl.navegar(url)
            return ResultadoPaso(0, 'click', res.exitoso, detalle=f"Video: {video.get('titulo', '')[:50]}")

        # Estrategia 2: click en el primer elemento de video
        selectores_yt = [
            'ytd-video-renderer:first-child #video-title',
            'ytd-compact-video-renderer:first-child a',
            'a.yt-simple-endpoint.ytd-video-renderer',
        ]
        for sel in selectores_yt:
            res = self._ctrl.click(selector=sel)
            if res.exitoso:
                return ResultadoPaso(0, 'click', True, detalle=f"Video: {video.get('titulo', '')[:50]}")

        return ResultadoPaso(0, 'click', False, error='No pude hacer click en el video')

    # ── Alternativas cuando falla un paso ────────────────

    def _intentar_alternativa(self, paso: Paso, error: str) -> Optional[ResultadoPaso]:
        """
        CUA Loop: cuando un paso falla, Bell mira la página (árbol de
        accesibilidad) y reintenta con patrones universales + texto visible.
        Lo que funciona se guarda en memoria_planes. Sólo se rinde al final.
        """
        page = self._ctrl._page
        if not page:
            return None

        if paso.accion in ('click', 'escribir'):
            # 1. Árbol de accesibilidad: qué hay en la página AHORA
            try:
                elementos = page.evaluate("""() => {
                    const els = document.querySelectorAll(
                        'button, input, a, textarea, select, [role="button"]'
                    );
                    return Array.from(els).slice(0, 40).map(el => ({
                        tipo: el.tagName.toLowerCase(),
                        texto: (el.textContent || el.value || el.placeholder ||
                                el.getAttribute('aria-label') || '').trim().slice(0, 50),
                        selector: el.id ? '#' + el.id :
                                  (el.getAttribute('name') ? '[name="' + el.getAttribute('name') + '"]' :
                                   el.tagName.toLowerCase()),
                    })).filter(e => e.texto);
                }""")
            except Exception:
                elementos = []

            # 2. Patrones universales según la descripción del paso
            try:
                from biblioteca.habilidades.navegador.patrones_universales import obtener_selectores_para
                desc = (paso.descripcion or '').lower()
                tipo_patron = None
                if any(p in desc for p in ['búsqueda', 'busqueda', 'buscar', 'search']):
                    tipo_patron = 'buscador'
                elif any(p in desc for p in ['login', 'usuario', 'contraseña', 'password', 'entrar']):
                    tipo_patron = 'login'
                elif any(p in desc for p in ['mensaje', 'chat', 'escribir']):
                    tipo_patron = 'chat_mensaje'
                elif any(p in desc for p in ['popup', 'cerrar', 'close']):
                    tipo_patron = 'popup_cerrar'

                if tipo_patron:
                    for selector in obtener_selectores_para(tipo_patron):
                        try:
                            res = self._ctrl.click(selector=selector)
                            if res.exitoso and paso.accion == 'escribir':
                                page.keyboard.type(paso.parametros.get('texto', ''), delay=50)
                            if res.exitoso:
                                print(f"  [Ejecutor] ✅ Alternativa por patrón universal: {selector}")
                                try:
                                    from biblioteca.habilidades.navegador.memoria_planes import MemoriaPlanes
                                    MemoriaPlanes.obtener().guardar_exito(tipo_patron, {desc[:30]: selector}, 0)
                                except Exception:
                                    pass
                                return ResultadoPaso(paso.numero, paso.accion, True,
                                                     detalle=f'patrón universal: {selector}')
                        except Exception:
                            continue
            except Exception:
                pass

            # 3. Buscar por texto visible entre los elementos hallados
            if elementos and paso.accion == 'click':
                texto_buscado = (paso.parametros.get('texto', '') or paso.descripcion)[:20].lower()
                for el in elementos:
                    if texto_buscado and texto_buscado in el.get('texto', '').lower():
                        sel = el.get('selector', '')
                        if sel:
                            try:
                                res = self._ctrl.click(selector=sel)
                                if res.exitoso:
                                    print(f"  [Ejecutor] ✅ Alternativa por texto: {sel}")
                                    return ResultadoPaso(paso.numero, 'click', True,
                                                         detalle=f'texto visible: {sel}')
                            except Exception:
                                continue

        # 4. Escribir sin selector: teclado directo
        if paso.accion == 'escribir':
            try:
                page.keyboard.type(paso.parametros.get('texto', ''), delay=80)
                return ResultadoPaso(paso.numero, 'escribir', True, detalle='teclado directo')
            except Exception:
                pass

        return None

    # ── Utilidades ────────────────────────────────────────

    def _url_actual(self) -> str:
        try:
            return self._ctrl._page.url if self._ctrl._page else ''
        except Exception:
            return ''

    def _generar_resumen(self, plan: Plan, resultado: ResultadoEjecucion) -> str:
        """Genera un resumen conciso de lo que se hizo."""
        datos = resultado.datos_extraidos
        lineas = []

        if datos.get('video_reproduciendo'):
            lineas.append(f"Video reproduciendo: '{datos['video_reproduciendo']}'")
        if datos.get('videos_youtube'):
            vids = datos['videos_youtube']
            lineas.append(f"Encontré {len(vids)} videos. Primero: '{vids[0].get('titulo', '')}'")
        if datos.get('mensaje_enviado'):
            lineas.append("Mensaje enviado exitosamente")
        if datos.get('repos_github'):
            repos = datos['repos_github']
            nombres = [r.get('nombre', '') for r in repos[:5]]
            lineas.append(f"Repos: {', '.join(nombres)}")
        if datos.get('url_repo'):
            lineas.append(f"URL del repositorio: {datos['url_repo']}")
        if datos.get('emails'):
            emails = datos['emails']
            lineas.append(f"Encontré {len(emails)} emails")
        if datos.get('titulo_pagina'):
            lineas.append(f"Página: {datos['titulo_pagina']}")
        if datos.get('texto_pagina'):
            lineas.append(f"Contenido ({len(datos['texto_pagina'])} chars extraídos)")

        if not lineas:
            lineas.append(f"Ejecuté {len(resultado.pasos_ejecutados)} pasos en {resultado.url_final}")

        return ' | '.join(lineas)