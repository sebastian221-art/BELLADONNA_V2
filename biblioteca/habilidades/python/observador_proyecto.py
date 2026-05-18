# biblioteca/habilidades/python/observador_proyecto.py
# ============================================================
# OBSERVADOR DE PROYECTO — Pair Programmer Activo
#
# Bell observa el proyecto de Sebastian en tiempo real.
# Cuando detecta cambios en archivos .py, los analiza
# automáticamente y tiene el análisis listo antes de
# que Sebastian le pregunte.
#
# PAIR PROGRAMMER significa:
#   - Bell monitorea cambios en el filesystem
#   - Al guardar un archivo, Bell lo analiza en background
#   - Si CC sube mucho, Bell alerta proactivamente
#   - Si hay errores de sintaxis, Bell los detecta al instante
#   - Si la función cambió 5+ veces, Bell sugiere refactoring
#
# Watchdog ya está instalado en el sistema.
# ============================================================

import os
import time
import threading
import hashlib
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable
from queue import Queue, Empty

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileModifiedEvent
    WATCHDOG_OK = True
except ImportError:
    WATCHDOG_OK = False


@dataclass
class CambioArchivo:
    ruta:           str
    timestamp:      float
    hash_anterior:  str = ''
    hash_nuevo:     str = ''
    analisis:       Optional[dict] = None
    alertas:        List[str] = field(default_factory=list)


@dataclass
class HistorialArchivo:
    ruta:         str
    cambios:      int = 0
    cc_historico: List[float] = field(default_factory=list)
    ultimo_hash:  str = ''


class _HandlerCambios(FileSystemEventHandler if WATCHDOG_OK else object):
    """Manejador de eventos del filesystem para el pair programmer."""

    def __init__(self, queue_cambios: Queue, extensiones: tuple = ('.py',)):
        self._queue = queue_cambios
        self._extensiones = extensiones
        self._ultimo_evento: Dict[str, float] = {}
        self._debounce_seg = 1.5  # evitar doble-procesamiento al guardar

    def on_modified(self, evento):
        if hasattr(evento, 'is_directory') and evento.is_directory:
            return
        ruta = getattr(evento, 'src_path', '')
        if not any(ruta.endswith(ext) for ext in self._extensiones):
            return

        ahora = time.time()
        ultimo = self._ultimo_evento.get(ruta, 0)
        if ahora - ultimo < self._debounce_seg:
            return

        self._ultimo_evento[ruta] = ahora
        self._queue.put({'tipo': 'modificacion', 'ruta': ruta,
                         'timestamp': ahora})


class ObservadorProyecto:
    """
    Pair programmer activo de Bell.

    Monitorea el proyecto de Sebastian en tiempo real,
    analiza cambios automáticamente y genera alertas
    cuando detecta problemas antes de que Sebastian pregunte.
    """

    def __init__(self, ruta_proyecto: str = ''):
        self._ruta = ruta_proyecto or _detectar_raiz_proyecto()
        self._activo = False
        self._observer = None
        self._queue: Queue = Queue()
        self._historial: Dict[str, HistorialArchivo] = {}
        self._ultimo_analisis: Dict[str, dict] = {}
        self._callbacks: List[Callable] = []
        self._thread_proceso: Optional[threading.Thread] = None

        # Singleton
        self._lock = threading.Lock()

    def iniciar(self):
        """Inicia el monitoreo del proyecto en background."""
        if not WATCHDOG_OK:
            print('  [Observador] watchdog no disponible')
            return False

        if self._activo:
            return True

        if not os.path.exists(self._ruta):
            print(f'  [Observador] Ruta no existe: {self._ruta}')
            return False

        try:
            handler = _HandlerCambios(self._queue)
            self._observer = Observer()
            self._observer.schedule(handler, self._ruta, recursive=True)
            self._observer.start()

            # Thread procesador de cola
            self._activo = True
            self._thread_proceso = threading.Thread(
                target=self._procesar_cola,
                daemon=True,
                name='BellObservador',
            )
            self._thread_proceso.start()

            print(f'  [Observador] 👁️  Pair programmer activo — monitoreando: {self._ruta}')
            return True

        except Exception as e:
            print(f'  [Observador] Error iniciando: {e}')
            return False

    def detener(self):
        """Detiene el monitoreo."""
        self._activo = False
        if self._observer:
            try:
                self._observer.stop()
                self._observer.join(timeout=2)
            except Exception:
                pass
        print('  [Observador] Pair programmer detenido.')

    def on_alerta(self, callback: Callable):
        """Registra un callback para alertas del pair programmer."""
        self._callbacks.append(callback)

    def obtener_analisis_reciente(self, ruta: str) -> Optional[dict]:
        """Retorna el análisis más reciente de un archivo."""
        return self._ultimo_analisis.get(ruta)

    def obtener_historial(self, ruta: str) -> Optional[HistorialArchivo]:
        """Retorna el historial de cambios de un archivo."""
        return self._historial.get(ruta)

    def analizar_ahora(self, codigo: str, nombre: str = '') -> dict:
        """
        Analiza código inmediatamente (sin esperar al watcher).
        Útil cuando Bell recibe código por chat.
        """
        return self._analizar_codigo(codigo, nombre or 'chat')

    def _procesar_cola(self):
        """Thread que procesa cambios de archivos en background."""
        while self._activo:
            try:
                evento = self._queue.get(timeout=1.0)
                if evento['tipo'] == 'modificacion':
                    self._procesar_modificacion(evento['ruta'])
            except Empty:
                continue
            except Exception as e:
                pass

    def _procesar_modificacion(self, ruta: str):
        """Procesa la modificación de un archivo Python."""
        # Ignorar archivos de cache, tests generados, etc.
        nombre = os.path.basename(ruta)
        if any(p in ruta for p in ['__pycache__', '.git', 'venv', 'env']):
            return
        if nombre.startswith('test_hypothesis_'):
            return

        try:
            with open(ruta, 'r', encoding='utf-8', errors='replace') as f:
                codigo = f.read()
        except Exception:
            return

        hash_nuevo = hashlib.md5(codigo.encode()).hexdigest()

        # Actualizar historial
        with self._lock:
            hist = self._historial.get(ruta, HistorialArchivo(ruta=ruta))
            if hash_nuevo == hist.ultimo_hash:
                return  # sin cambios reales
            hist.cambios += 1
            hist.ultimo_hash = hash_nuevo
            self._historial[ruta] = hist

        # Analizar en el mismo thread (background)
        analisis = self._analizar_codigo(codigo, ruta)
        self._ultimo_analisis[ruta] = analisis

        # Generar alertas
        alertas = self._generar_alertas(analisis, ruta, hist)
        if alertas:
            for callback in self._callbacks:
                try:
                    callback(ruta, alertas, analisis)
                except Exception:
                    pass

            # Log de alertas
            print(f'\n  [👁️  Pair Programmer] {os.path.basename(ruta)}:')
            for alerta in alertas:
                print(f'  {alerta}')

    def _analizar_codigo(self, codigo: str, ruta: str) -> dict:
        """Análisis rápido de un archivo modificado."""
        resultado = {
            'ruta': ruta,
            'timestamp': time.time(),
            'es_valido': False,
            'cc': 0.0,
            'mi': 0.0,
            'n_funciones': 0,
            'n_problemas': 0,
            'antipatrones': [],
            'errores_sintaxis': [],
        }

        try:
            from biblioteca.habilidades.python.analizador_codigo import obtener as get_analizador
            analisis = get_analizador().analizar(codigo)

            resultado['es_valido'] = analisis.es_valido_ast
            resultado['cc'] = analisis.metricas.cc
            resultado['mi'] = analisis.metricas.mi
            resultado['n_funciones'] = len(analisis.funciones)
            resultado['n_problemas'] = len(analisis.problemas)

            if not analisis.es_valido_ast and analisis.error_fatal:
                resultado['errores_sintaxis'].append(analisis.error_fatal)

        except Exception as e:
            resultado['error'] = str(e)

        # Antipatrones (rápido)
        try:
            from biblioteca.habilidades.python.detector_antipatrones import analizar
            resultado['antipatrones'] = analizar(codigo)
        except Exception:
            pass

        # Actualizar historial de CC
        if ruta in self._historial:
            self._historial[ruta].cc_historico.append(resultado['cc'])

        return resultado

    def _generar_alertas(self, analisis: dict, ruta: str,
                          hist: HistorialArchivo) -> List[str]:
        """Genera alertas proactivas basadas en el análisis."""
        alertas = []
        nombre = os.path.basename(ruta)

        # Alerta: error de sintaxis
        if analisis.get('errores_sintaxis'):
            for err in analisis['errores_sintaxis'][:2]:
                alertas.append(f'🔴 Sintaxis: {err}')

        # Alerta: CC alta
        cc = analisis.get('cc', 0)
        if cc > 10:
            alertas.append(
                f'🔴 CC={cc:.0f} — complejidad crítica en {nombre}. '
                f'Refactoriza antes de continuar.'
            )
        elif cc > 7:
            alertas.append(
                f'⚠️  CC={cc:.0f} — complejidad elevada en {nombre}.'
            )

        # Alerta: CC creciente
        cc_hist = hist.cc_historico
        if len(cc_hist) >= 3:
            if cc_hist[-1] > cc_hist[-2] > cc_hist[-3]:
                alertas.append(
                    f'📈 CC creciendo en {nombre}: '
                    f'{cc_hist[-3]:.0f}→{cc_hist[-2]:.0f}→{cc_hist[-1]:.0f}. '
                    f'Tendencia de complejidad aumentando.'
                )

        # Alerta: archivo modificado muchas veces
        if hist.cambios == 5:
            alertas.append(
                f'🔄 {nombre} modificado {hist.cambios} veces seguidas. '
                f'¿Quieres que analice la evolución del código?'
            )

        # Alerta: antipatrones críticos
        criticos = [a for a in analisis.get('antipatrones', [])
                    if a.severidad == 'critico']
        if criticos:
            for a in criticos[:2]:
                alertas.append(
                    f'🔴 Antipatrón crítico línea {a.linea}: {a.problema}'
                )

        # Alerta: MI baja
        mi = analisis.get('mi', 100)
        if 0 < mi < 30:
            alertas.append(
                f'⚠️  Mantenibilidad MI={mi:.0f}/100 en {nombre} — '
                f'código difícil de mantener.'
            )

        return alertas


# ── Singleton global ──────────────────────────────────────

_instancia: Optional[ObservadorProyecto] = None


def obtener(ruta_proyecto: str = '') -> ObservadorProyecto:
    """Retorna la instancia singleton del observador."""
    global _instancia
    if _instancia is None:
        _instancia = ObservadorProyecto(ruta_proyecto)
    return _instancia


def iniciar_pair_programmer(ruta_proyecto: str = '',
                              callback_alerta: Optional[Callable] = None) -> bool:
    """
    Inicia el pair programmer.
    Llama esto al arrancar Bell para activar el monitoreo continuo.
    """
    obs = obtener(ruta_proyecto)
    if callback_alerta:
        obs.on_alerta(callback_alerta)
    return obs.iniciar()


def _detectar_raiz_proyecto() -> str:
    """Intenta detectar la raíz del proyecto BELLADONNA."""
    # Buscar hacia arriba desde el directorio actual
    current = os.path.dirname(os.path.abspath(__file__))
    for _ in range(6):
        if os.path.exists(os.path.join(current, 'capas')) and \
           os.path.exists(os.path.join(current, 'biblioteca')):
            return current
        current = os.path.dirname(current)
    return os.getcwd()