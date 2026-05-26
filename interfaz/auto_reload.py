# interfaz/auto_reload.py
# ================================================
# AUTO-RELOAD — recarga el código de Bell en caliente
#
# Vigila los .py del proyecto con watchdog. Cuando uno cambia,
# purga los módulos recargables de sys.modules para que la
# siguiente petición re-importe el código fresco SIN reiniciar
# el proceso (chat.py importa cada capa dentro del handler).
#
# Limitaciones honestas:
#  - Recarga la LÓGICA (capas, habilidades), no las rutas Flask
#    ya registradas: editar servidor.py o el registro de rutas
#    sí requiere reinicio del proceso.
#  - No reconstruye la red neuronal (biblioteca.red/fundacional)
#    para no perder el estado cargado en RAM.
# ================================================

import sys
import threading
from pathlib import Path

# Prefijos de módulos que SÍ se recargan en caliente.
_RECARGABLES = ('capas.', 'biblioteca.habilidades.')

# Prefijos que NUNCA se purgan (estado vivo / infraestructura).
_PROTEGIDOS = (
    'biblioteca.red', 'biblioteca.fundacional', 'biblioteca.grounding',
    'biblioteca.nodos', 'interfaz.servidor', 'interfaz.auto_reload',
)

_IGNORAR_CARPETAS = {
    '__pycache__', '.git', 'venv', 'env', 'node_modules', '.pytest_cache'
}


def _purgar_modulos() -> int:
    purgados = 0
    for nombre in list(sys.modules.keys()):
        if not nombre.startswith(_RECARGABLES):
            continue
        if any(nombre.startswith(p) for p in _PROTEGIDOS):
            continue
        del sys.modules[nombre]
        purgados += 1
    return purgados


def iniciar_auto_reload(raiz: str):
    """
    Arranca el vigilante de archivos. Devuelve el Observer (o None
    si watchdog no está disponible). No bloquea — corre en daemon.
    """
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
    except Exception:
        print('  ♻  Auto-reload: watchdog no instalado — desactivado '
              '(pip install watchdog para activarlo)')
        return None

    raiz_path = Path(raiz)
    _lock  = threading.Lock()
    _timer = {'t': None}

    def _recargar():
        with _lock:
            n = _purgar_modulos()
            print(f'  ♻  Auto-reload: {n} módulos purgados — '
                  f'la próxima petición usará el código nuevo')

    class _Handler(FileSystemEventHandler):
        def on_any_event(self, event):
            if event.is_directory:
                return
            ruta = str(getattr(event, 'src_path', ''))
            if not ruta.endswith('.py'):
                return
            if any(c in Path(ruta).parts for c in _IGNORAR_CARPETAS):
                return
            # Debounce: coalesce ráfagas de eventos en una sola recarga.
            with _lock:
                if _timer['t'] is not None:
                    _timer['t'].cancel()
                _timer['t'] = threading.Timer(0.4, _recargar)
                _timer['t'].daemon = True
                _timer['t'].start()

    observer = Observer()
    observer.schedule(_Handler(), str(raiz_path), recursive=True)
    observer.daemon = True
    observer.start()
    print(f'  ♻  Auto-reload activo (watchdog) sobre {raiz_path}')
    return observer
