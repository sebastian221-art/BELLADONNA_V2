# biblioteca/habilidades/navegador/sesion_manager.py
# ============================================================
# GESTOR DE SESIONES — El browser de Bell siempre está listo
#
# El browser NO se abre y cierra en cada petición.
# Persiste entre turnos para que:
#   - Instagram siga con sesión iniciada
#   - GitHub recuerde el login
#   - YouTube mantenga el video
#   - Los formularios no se reseteen
#
# Singleton: una instancia por sesión de Bell.
# ============================================================

import os
import json
from pathlib import Path
from typing import Optional

_RAIZ        = Path(os.environ.get('BELL_ROOT', str(Path(__file__).resolve().parents[4])))
_COOKIES_DIR = _RAIZ / 'datos' / 'browser_sessions'
_COOKIES_DIR.mkdir(parents=True, exist_ok=True)


class SesionManager:
    """
    Gestiona el ciclo de vida del browser de Bell.
    Crea una instancia por thread para compatibilidad con Flask.
    """

    _instancia: Optional['SesionManager'] = None
    _thread_id: int = 0

    def __init__(self):
        self._playwright   = None
        self._browser      = None
        self._contextos    = {}
        self._pagina_actual = None
        self._modo_visible = False
        self._activo       = False
        self._thread_id    = 0

    @classmethod
    def obtener(cls) -> 'SesionManager':
        import threading
        current_tid = threading.current_thread().ident
        # Si la instancia existe pero es de otro thread → crear nueva
        if cls._instancia is not None and cls._instancia._thread_id != current_tid:
            try:
                cls._instancia.cerrar()
            except Exception:
                pass
            cls._instancia = None
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    @classmethod
    def reiniciar(cls):
        if cls._instancia and cls._instancia._activo:
            cls._instancia.cerrar()
        cls._instancia = None

    # ── Inicialización ────────────────────────────────────

    def iniciar(self, visible: bool = False):
        """Inicia el browser si no está activo."""
        if self._activo:
            return

        import threading
        from playwright.sync_api import sync_playwright
        self._playwright   = sync_playwright().start()
        self._modo_visible  = visible
        self._thread_id    = threading.current_thread().ident

        self._browser = self._playwright.chromium.launch(
            headless=not visible,
            args=[
                '--no-sandbox',
                '--disable-blink-features=AutomationControlled',
                '--disable-infobars',
            ]
        )
        self._activo = True
        print(f"  [Browser] ✅ Chromium iniciado — {'visible' if visible else 'headless'} (thread={self._thread_id})")

    def asegurar_activo(self, visible: bool = False):
        """Inicia el browser si no estaba activo."""
        if not self._activo:
            self.iniciar(visible)

    # ── Contextos (sesiones por sitio) ───────────────────

    def obtener_contexto(self, dominio: str):
        """
        Devuelve o crea un contexto para el dominio dado.
        Cada contexto tiene sus propias cookies — Instagram puede estar
        logueado sin afectar a GitHub.
        """
        self.asegurar_activo()

        if dominio not in self._contextos:
            # Cargar cookies guardadas si existen
            storage = self._cargar_sesion(dominio)
            kwargs = {
                'viewport': {'width': 1280, 'height': 900},
                'user_agent': (
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/120.0.0.0 Safari/537.36'
                ),
                'locale': 'es-CO',
            }
            if storage:
                kwargs['storage_state'] = storage

            ctx = self._browser.new_context(**kwargs)
            self._contextos[dominio] = ctx
            print(f"  [Browser] 📂 Contexto creado para {dominio}")

        return self._contextos[dominio]

    def nueva_pagina(self, dominio: str = 'general'):
        """Abre una nueva pestaña en el contexto del dominio."""
        ctx  = self.obtener_contexto(dominio)
        page = ctx.new_page()

        # Interceptar errores de página silenciosamente
        page.on('pageerror', lambda e: None)
        page.on('console',   lambda m: None)

        self._pagina_actual = page
        return page

    def pagina_actual(self):
        return self._pagina_actual

    # ── Sesiones persistentes (cookies entre reinicios) ──

    def guardar_sesion(self, dominio: str):
        """Guarda las cookies del contexto para no perder la sesión."""
        if dominio not in self._contextos:
            return
        try:
            ruta = _COOKIES_DIR / f'{dominio}.json'
            state = self._contextos[dominio].storage_state()
            ruta.write_text(json.dumps(state), encoding='utf-8')
            print(f"  [Browser] 💾 Sesión guardada: {dominio}")
        except Exception as e:
            print(f"  [Browser] ⚠️  No se pudo guardar sesión {dominio}: {e}")

    def _cargar_sesion(self, dominio: str) -> Optional[dict]:
        ruta = _COOKIES_DIR / f'{dominio}.json'
        if ruta.exists():
            try:
                data = json.loads(ruta.read_text(encoding='utf-8'))
                print(f"  [Browser] ✅ Sesión cargada: {dominio}")
                return data
            except Exception:
                pass
        return None

    def sesion_guardada(self, dominio: str) -> bool:
        return (_COOKIES_DIR / f'{dominio}.json').exists()

    def borrar_sesion(self, dominio: str):
        ruta = _COOKIES_DIR / f'{dominio}.json'
        if ruta.exists():
            ruta.unlink()
            print(f"  [Browser] 🗑️  Sesión borrada: {dominio}")

    # ── Cierre ────────────────────────────────────────────

    def cerrar(self):
        """Cierra el browser limpiamente."""
        try:
            for dominio, ctx in self._contextos.items():
                try:
                    ctx.close()
                except Exception:
                    pass
            if self._browser:
                self._browser.close()
            if self._playwright:
                self._playwright.stop()
        except Exception:
            pass
        finally:
            self._activo      = False
            self._contextos   = {}
            self._browser     = None
            self._playwright  = None
            print("  [Browser] 🔴 Chromium cerrado")

    def esta_activo(self) -> bool:
        return self._activo