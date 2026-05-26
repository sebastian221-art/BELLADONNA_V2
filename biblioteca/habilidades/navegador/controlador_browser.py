# biblioteca/habilidades/navegador/controlador_browser.py
# ============================================================
# CONTROLADOR DEL BROWSER — Las manos de Bell
#
# Todo lo que un humano haría con un browser, Bell lo hace aquí:
#   - navegar a URLs
#   - hacer click en elementos
#   - escribir texto
#   - scrollear
#   - tomar screenshots
#   - esperar que cargue
#   - manejar popups y diálogos
#   - descargar archivos
#   - ejecutar JavaScript
#
# NUNCA inventa — si algo falla, reporta exactamente qué pasó.
# ============================================================

import base64
import re
import time
from dataclasses import dataclass, field
from typing import Optional
from urllib.parse import urlparse


@dataclass
class ResultadoAccion:
    exitoso:    bool
    accion:     str
    detalle:    str   = ''
    error:      str   = ''
    screenshot: bytes = b''   # PNG bytes si se tomó screenshot
    html:       str   = ''    # HTML de la página después de la acción
    url_actual: str   = ''


def _dominio(url: str) -> str:
    """Extrae el dominio limpio de una URL."""
    try:
        parsed = urlparse(url)
        host = parsed.netloc or url
        return re.sub(r'^www\.', '', host).split('/')[0]
    except Exception:
        return 'general'


class ControladorBrowser:
    """Ejecuta acciones físicas en el browser."""

    def __init__(self, pagina=None):
        self._page    = pagina
        self._timeout = 15_000   # 15 segundos por defecto

    def establecer_pagina(self, page):
        self._page = page

    def _p(self):
        """Devuelve la página activa o lanza error claro."""
        if not self._page:
            raise RuntimeError("No hay página activa. Usa navegar() primero.")
        return self._page

    # ── Navegación ────────────────────────────────────────

    def navegar(self, url: str, esperar: str = 'domcontentloaded') -> ResultadoAccion:
        """Navega a una URL y espera a que cargue."""
        try:
            from biblioteca.habilidades.navegador.sesion_manager import SesionManager
            sm = SesionManager.obtener()
            sm.asegurar_activo()
            dom = _dominio(url)
            self._page = sm.nueva_pagina(dom)
            self._page.goto(url, wait_until=esperar, timeout=30_000)
            url_final = self._page.url
            print(f"  [Browser] 🌐 Navegué a: {url_final[:70]}")
            return ResultadoAccion(
                exitoso=True, accion='navegar',
                detalle=f"En: {url_final}",
                url_actual=url_final,
                html=self._page.content()[:5000],
            )
        except Exception as e:
            return ResultadoAccion(exitoso=False, accion='navegar', error=str(e)[:200])

    def ir_atras(self) -> ResultadoAccion:
        try:
            self._p().go_back(wait_until='domcontentloaded', timeout=10_000)
            return ResultadoAccion(exitoso=True, accion='ir_atras', url_actual=self._p().url)
        except Exception as e:
            return ResultadoAccion(exitoso=False, accion='ir_atras', error=str(e)[:200])

    def recargar(self) -> ResultadoAccion:
        try:
            self._p().reload(wait_until='domcontentloaded', timeout=10_000)
            return ResultadoAccion(exitoso=True, accion='recargar', url_actual=self._p().url)
        except Exception as e:
            return ResultadoAccion(exitoso=False, accion='recargar', error=str(e)[:200])

    # ── Clicks ────────────────────────────────────────────

    def click(self, selector: str = '', texto: str = '', screenshot_si_falla: bool = True) -> ResultadoAccion:
        """
        Hace click en un elemento.
        Intenta por selector CSS primero, luego por texto visible.
        """
        page = self._p()
        intentos = []

        # Estrategia 1: selector CSS directo
        if selector:
            try:
                page.wait_for_selector(selector, timeout=5_000)
                page.click(selector, timeout=5_000)
                print(f"  [Browser] 👆 Click en: {selector[:50]}")
                return ResultadoAccion(exitoso=True, accion='click', detalle=f"selector: {selector}")
            except Exception as e:
                intentos.append(f"CSS '{selector}': {str(e)[:60]}")

        # Estrategia 2: texto visible del elemento
        if texto:
            try:
                page.get_by_text(texto, exact=False).first.click(timeout=5_000)
                print(f"  [Browser] 👆 Click en texto: '{texto[:40]}'")
                return ResultadoAccion(exitoso=True, accion='click', detalle=f"texto: {texto}")
            except Exception as e:
                intentos.append(f"texto '{texto}': {str(e)[:60]}")

        # Estrategia 3: aria-label
        if texto:
            try:
                page.get_by_role('button', name=texto).first.click(timeout=5_000)
                return ResultadoAccion(exitoso=True, accion='click', detalle=f"aria: {texto}")
            except Exception as e:
                intentos.append(f"aria '{texto}': {str(e)[:60]}")

        # Falló todo → screenshot
        ss = b''
        if screenshot_si_falla:
            try:
                ss = page.screenshot()
            except Exception:
                pass
        error_msg = ' | '.join(intentos)
        return ResultadoAccion(exitoso=False, accion='click', error=error_msg, screenshot=ss)

    def click_coordenadas(self, x: int, y: int) -> ResultadoAccion:
        """Click en coordenadas específicas (para cuando el selector no funciona)."""
        try:
            self._p().mouse.click(x, y)
            return ResultadoAccion(exitoso=True, accion='click_coordenadas', detalle=f"({x},{y})")
        except Exception as e:
            return ResultadoAccion(exitoso=False, accion='click_coordenadas', error=str(e)[:200])

    # ── Escritura ─────────────────────────────────────────

    def escribir(self, selector: str = '', texto: str = '', limpiar: bool = True) -> ResultadoAccion:
        """Escribe en un input o textarea."""
        page = self._p()

        # Estrategia 1: selector específico
        if selector:
            try:
                page.wait_for_selector(selector, timeout=5_000)
                if limpiar:
                    page.fill(selector, '')
                page.type(selector, texto, delay=50)
                print(f"  [Browser] ⌨️  Escribí '{texto[:30]}' en {selector[:40]}")
                return ResultadoAccion(exitoso=True, accion='escribir', detalle=f"'{texto[:40]}' en {selector}")
            except Exception as e:
                pass

        # Estrategia 2: input activo en foco
        try:
            page.keyboard.type(texto, delay=50)
            return ResultadoAccion(exitoso=True, accion='escribir', detalle=f"'{texto[:40]}' en foco")
        except Exception as e:
            return ResultadoAccion(exitoso=False, accion='escribir', error=str(e)[:200])

    def limpiar_y_escribir(self, selector: str, texto: str) -> ResultadoAccion:
        """Limpia el campo y escribe nuevo texto."""
        page = self._p()
        try:
            page.wait_for_selector(selector, timeout=5_000)
            page.triple_click(selector)
            page.keyboard.press('Backspace')
            page.type(selector, texto, delay=50)
            return ResultadoAccion(exitoso=True, accion='limpiar_y_escribir', detalle=f"'{texto[:40]}'")
        except Exception as e:
            return ResultadoAccion(exitoso=False, accion='limpiar_y_escribir', error=str(e)[:200])

    # ── Teclado ───────────────────────────────────────────

    def presionar_tecla(self, tecla: str) -> ResultadoAccion:
        """Presiona una tecla: 'Enter', 'Tab', 'Escape', 'ArrowDown', etc."""
        try:
            self._p().keyboard.press(tecla)
            return ResultadoAccion(exitoso=True, accion='tecla', detalle=tecla)
        except Exception as e:
            return ResultadoAccion(exitoso=False, accion='tecla', error=str(e)[:200])

    def presionar_enter(self) -> ResultadoAccion:
        return self.presionar_tecla('Enter')

    # ── Scroll ────────────────────────────────────────────

    def scroll(self, direccion: str = 'abajo', cantidad: int = 500) -> ResultadoAccion:
        """Scrollea la página."""
        try:
            delta = cantidad if direccion in ('abajo', 'down') else -cantidad
            self._p().mouse.wheel(0, delta)
            return ResultadoAccion(exitoso=True, accion='scroll', detalle=f"{direccion} {cantidad}px")
        except Exception as e:
            return ResultadoAccion(exitoso=False, accion='scroll', error=str(e)[:200])

    def scroll_al_elemento(self, selector: str) -> ResultadoAccion:
        try:
            el = self._p().locator(selector).first
            el.scroll_into_view_if_needed(timeout=5_000)
            return ResultadoAccion(exitoso=True, accion='scroll_elemento', detalle=selector)
        except Exception as e:
            return ResultadoAccion(exitoso=False, accion='scroll_elemento', error=str(e)[:200])

    # ── Screenshots ───────────────────────────────────────

    def screenshot(self, selector: str = '') -> bytes:
        """Toma screenshot completa o de un elemento específico."""
        try:
            if selector:
                el = self._p().locator(selector).first
                return el.screenshot()
            return self._p().screenshot(full_page=False)
        except Exception:
            return b''

    def screenshot_base64(self) -> str:
        """Screenshot en base64 para enviar a Groq como imagen."""
        datos = self.screenshot()
        return base64.b64encode(datos).decode() if datos else ''

    # ── Esperas ───────────────────────────────────────────

    def esperar_elemento(self, selector: str, timeout: int = 10_000) -> bool:
        """Espera a que aparezca un elemento. True si apareció."""
        try:
            self._p().wait_for_selector(selector, timeout=timeout)
            return True
        except Exception:
            return False

    def esperar_url(self, patron: str, timeout: int = 10_000) -> bool:
        """Espera hasta que la URL contenga el patrón dado."""
        try:
            self._p().wait_for_url(f'**{patron}**', timeout=timeout)
            return True
        except Exception:
            return False

    def esperar_carga(self, timeout: int = 10_000):
        """Espera a que la página termine de cargar."""
        try:
            self._p().wait_for_load_state('networkidle', timeout=timeout)
        except Exception:
            pass

    def pausa(self, segundos: float = 1.0):
        time.sleep(segundos)

    # ── JavaScript ────────────────────────────────────────

    def ejecutar_js(self, script: str):
        """Ejecuta JavaScript en la página."""
        try:
            return self._p().evaluate(script)
        except Exception as e:
            return None

    def obtener_propiedad(self, selector: str, propiedad: str) -> str:
        """Obtiene una propiedad de un elemento (value, href, src, etc.)."""
        try:
            return self._p().locator(selector).first.get_attribute(propiedad) or ''
        except Exception:
            return ''

    # ── Información de la página ──────────────────────────

    def url_actual(self) -> str:
        try:
            return self._p().url
        except Exception:
            return ''

    def titulo(self) -> str:
        try:
            return self._p().title()
        except Exception:
            return ''

    def html_completo(self) -> str:
        try:
            return self._p().content()
        except Exception:
            return ''

    # ── Popups y diálogos ─────────────────────────────────

    def aceptar_dialogo(self):
        """Acepta automáticamente los próximos diálogos (alert, confirm, prompt)."""
        self._p().on('dialog', lambda d: d.accept())

    def manejar_popup(self) -> Optional[object]:
        """Espera y devuelve una nueva pestaña/popup si aparece."""
        try:
            with self._p().expect_popup(timeout=5_000) as popup_info:
                pass
            return popup_info.value
        except Exception:
            return None

    # ── Descarga de archivos ──────────────────────────────

    def descargar(self, selector: str, ruta_destino: str = '') -> ResultadoAccion:
        """Hace click en un botón de descarga y guarda el archivo."""
        try:
            with self._p().expect_download(timeout=30_000) as dl_info:
                self.click(selector)
            descarga = dl_info.value
            if ruta_destino:
                descarga.save_as(ruta_destino)
            else:
                ruta_destino = descarga.suggested_filename
                descarga.save_as(ruta_destino)
            return ResultadoAccion(
                exitoso=True, accion='descargar',
                detalle=f"Guardado en: {ruta_destino}"
            )
        except Exception as e:
            return ResultadoAccion(exitoso=False, accion='descargar', error=str(e)[:200])

    # ── Selects y checkboxes ──────────────────────────────

    def seleccionar_opcion(self, selector: str, valor: str) -> ResultadoAccion:
        try:
            self._p().select_option(selector, value=valor, timeout=5_000)
            return ResultadoAccion(exitoso=True, accion='seleccionar', detalle=f"{selector}={valor}")
        except Exception as e:
            return ResultadoAccion(exitoso=False, accion='seleccionar', error=str(e)[:200])

    def marcar_checkbox(self, selector: str, marcar: bool = True) -> ResultadoAccion:
        try:
            if marcar:
                self._p().check(selector, timeout=5_000)
            else:
                self._p().uncheck(selector, timeout=5_000)
            return ResultadoAccion(exitoso=True, accion='checkbox', detalle=f"{selector}={'✓' if marcar else '○'}")
        except Exception as e:
            return ResultadoAccion(exitoso=False, accion='checkbox', error=str(e)[:200])