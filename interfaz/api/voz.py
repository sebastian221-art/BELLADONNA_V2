# interfaz/api/voz.py
# ================================================
# VOZ — GestorVoz + API integrada al servidor
# ================================================

import os
import threading
import uuid
import socket
import time
from pathlib import Path
from flask import request, jsonify

_AUDIO_DIR = Path(__file__).parent.parent.parent / 'datos' / 'audio_temp'
_AUDIO_DIR.mkdir(parents=True, exist_ok=True)

_CHROMECAST_PORT = 8009


def _ip_local() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'


def _stop_browser_diferido(browser):
    time.sleep(3)
    try:
        browser.stop_discovery()
    except Exception:
        pass


# ── GESTOR DE VOZ ─────────────────────────────────────────

class GestorVoz:

    _instancia          = None
    _lock_inst          = threading.Lock()
    _dispositivos_cache = []

    def __init__(self):
        self._cast      = None
        self._activa    = False
        self._nombre    = None
        self._ip_cast   = None
        self._ip_local  = _ip_local()
        self._puerto    = 5000
        self._volumen   = 0.8
        self._lock      = threading.Lock()
        self._socketio  = None

    @classmethod
    def obtener(cls) -> 'GestorVoz':
        with cls._lock_inst:
            if cls._instancia is None:
                cls._instancia = cls()
        return cls._instancia

    def configurar_socket(self, socketio):
        self._socketio = socketio

    # ── Conexión ──────────────────────────────────────────

    def activar(self, nombre_dispositivo: str = None, ip_directa: str = None) -> dict:
        try:
            import pychromecast  # noqa
        except ImportError:
            return {'ok': False, 'error': 'pychromecast no instalado'}

        if ip_directa:
            return self._conectar_por_ip(ip_directa, nombre_dispositivo or 'Nest Mini')

        for d in GestorVoz._dispositivos_cache:
            if not nombre_dispositivo or nombre_dispositivo.lower() in d['nombre'].lower():
                return self._conectar_por_ip(d['ip'], d['nombre'])

        return self._activar_via_mdns(nombre_dispositivo)

    def _conectar_por_ip(self, ip: str, nombre: str = 'Nest Mini') -> dict:
        try:
            import pychromecast
            host_tuple = (ip, _CHROMECAST_PORT, None, None, nombre)
            cast = pychromecast.get_chromecast_from_host(host_tuple, timeout=10)
            cast.wait(timeout=10)

            self._cast    = cast
            self._nombre  = cast.cast_info.friendly_name or nombre
            self._ip_cast = ip
            self._activa  = True
            self._emitir_estado()

            print(f'  [Voz] Conectado a {self._nombre} ({ip}) | IP local: {self._ip_local}:{self._puerto}')

            return {
                'ok':       True,
                'nombre':   self._nombre,
                'ip':       self._ip_cast,
                'ip_local': self._ip_local,
            }
        except Exception as e:
            return {'ok': False, 'error': f'No se pudo conectar a {ip}: {e}'}

    def _activar_via_mdns(self, nombre_dispositivo: str = None) -> dict:
        import pychromecast
        chromecasts, browser = pychromecast.get_chromecasts(timeout=8)

        threading.Thread(
            target=_stop_browser_diferido,
            args=(browser,),
            daemon=True
        ).start()

        if not chromecasts:
            return {'ok': False, 'error': 'No se encontraron dispositivos en la red'}

        if nombre_dispositivo:
            target = next(
                (c for c in chromecasts
                 if nombre_dispositivo.lower() in c.cast_info.friendly_name.lower()),
                None
            ) or chromecasts[0]
        else:
            target = next(
                (c for c in chromecasts
                 if any(k in c.cast_info.friendly_name.lower()
                        for k in ['nest', 'mini', 'home', 'hub'])),
                chromecasts[0]
            )

        GestorVoz._dispositivos_cache = [
            {
                'nombre': c.cast_info.friendly_name,
                'ip':     c.cast_info.host,
                'modelo': c.cast_info.model_name or 'Chromecast',
            }
            for c in chromecasts
        ]

        return self._conectar_por_ip(target.cast_info.host, target.cast_info.friendly_name)

    def desactivar(self):
        if self._cast:
            try:
                self._cast.quit_app()
            except Exception:
                pass
        self._cast   = None
        self._activa = False
        self._nombre = None
        self._emitir_estado()

    def buscar_dispositivos(self) -> list:
        try:
            import pychromecast
            chromecasts, browser = pychromecast.get_chromecasts(timeout=8)

            threading.Thread(
                target=_stop_browser_diferido,
                args=(browser,),
                daemon=True
            ).start()

            resultado = [
                {
                    'nombre':    c.cast_info.friendly_name,
                    'ip':        c.cast_info.host,
                    'modelo':    c.cast_info.model_name or 'Chromecast',
                    'conectado': (self._ip_cast == c.cast_info.host),
                }
                for c in chromecasts
            ]

            GestorVoz._dispositivos_cache = [
                {'nombre': r['nombre'], 'ip': r['ip'], 'modelo': r['modelo']}
                for r in resultado
            ]

            return resultado
        except Exception:
            return []

    # ── Hablar ────────────────────────────────────────────

    def hablar(self, texto: str, bloquear: bool = False) -> bool:
        if not self._activa or not self._cast or not texto:
            return False
        if bloquear:
            return self._hablar_interno(texto)
        threading.Thread(
            target=self._hablar_interno,
            args=(texto,),
            daemon=True,
        ).start()
        return True

    def _hablar_interno(self, texto: str) -> bool:
        with self._lock:
            try:
                ruta = self._generar_audio(texto)
                if not ruta:
                    print('  [Voz] Error: no se generó el audio')
                    return False

                url = f'http://{self._ip_local}:{self._puerto}/audio/{ruta.name}'
                print(f'  [Voz] URL del audio: {url}')

                return self._reproducir(url)

            except Exception as e:
                print(f'  [Voz] Error en _hablar_interno: {e}')
                import traceback; traceback.print_exc()
                return False

    def _generar_audio(self, texto: str) -> Path:
        try:
            from gtts import gTTS
            import re
            t = re.sub(r'[\*#`]', '', texto)
            t = re.sub(r'—', ',', t).strip()
            nombre = f'bell_{uuid.uuid4().hex[:8]}.mp3'
            ruta   = _AUDIO_DIR / nombre
            gTTS(text=t, lang='es', tld='com.co', slow=False).save(str(ruta))
            print(f'  [Voz] Audio generado: {ruta.name} ({ruta.stat().st_size} bytes)')
            threading.Timer(120, lambda: ruta.unlink(missing_ok=True)).start()
            return ruta
        except Exception as e:
            print(f'  [Voz] Error gTTS: {e}')
            return None

    def _reproducir(self, url: str) -> bool:
        """
        Reproduce audio en el Nest Mini.
        Logs detallados para diagnosticar problemas.
        NO mata self._activa en errores temporales.
        """
        try:
            mc = self._cast.media_controller
            print(f'  [Voz] Enviando play_media → {url}')

            # BUFFERED = archivo estático (no stream en vivo)
            # Sin esto el Nest trata el MP3 como stream LIVE y puede fallar
            from pychromecast.controllers.media import STREAM_TYPE_BUFFERED
            mc.play_media(url, 'audio/mpeg', stream_type=STREAM_TYPE_BUFFERED)

            print('  [Voz] Esperando que el reproductor se active...')
            mc.block_until_active(timeout=15)
            print(f'  [Voz] Reproductor activo — estado: {mc.status}')

            # Esperar a que termine la reproducción
            tiempo_espera = 0
            while tiempo_espera < 60:
                time.sleep(0.5)
                tiempo_espera += 0.5
                try:
                    mc.update_status()
                except Exception:
                    break
                if mc.status and mc.status.player_is_idle:
                    break

            print(f'  [Voz] Reproducción completada ({tiempo_espera:.1f}s)')
            return True

        except Exception as e:
            # Log completo del error sin matar _activa
            # (podría ser un error temporal de red, no de conexión)
            print(f'  [Voz] Error en _reproducir: {type(e).__name__}: {e}')
            import traceback; traceback.print_exc()
            return False

    def volumen(self, nivel: float):
        self._volumen = max(0.0, min(1.0, nivel))
        if self._cast:
            try:
                self._cast.set_volume(self._volumen)
            except Exception:
                pass

    # ── Estado ────────────────────────────────────────────

    def estado(self) -> dict:
        return {
            'activa':   self._activa,
            'nombre':   self._nombre,
            'ip':       self._ip_cast,
            'volumen':  self._volumen,
            'ip_local': self._ip_local,
        }

    def _emitir_estado(self):
        if self._socketio:
            try:
                self._socketio.emit('voz_estado', self.estado())
            except Exception:
                pass


# ── RUTAS API ─────────────────────────────────────────────

def registrar_rutas_voz(app, socketio):
    gestor = GestorVoz.obtener()
    gestor.configurar_socket(socketio)

    @app.route('/api/voz/estado')
    def voz_estado():
        return jsonify(gestor.estado())

    @app.route('/api/voz/dispositivos')
    def voz_dispositivos():
        dispositivos = gestor.buscar_dispositivos()
        return jsonify({'dispositivos': dispositivos, 'total': len(dispositivos)})

    @app.route('/api/voz/activar', methods=['POST'])
    def voz_activar():
        datos      = request.get_json() or {}
        nombre     = datos.get('nombre')
        ip_directa = datos.get('ip')
        result = gestor.activar(nombre_dispositivo=nombre, ip_directa=ip_directa)
        if result['ok']:
            socketio.emit('voz_estado', gestor.estado())
        return jsonify(result)

    @app.route('/api/voz/desactivar', methods=['POST'])
    def voz_desactivar():
        gestor.desactivar()
        socketio.emit('voz_estado', gestor.estado())
        return jsonify({'ok': True})

    @app.route('/api/voz/volumen', methods=['POST'])
    def voz_volumen():
        datos = request.get_json() or {}
        nivel = float(datos.get('nivel', 0.8))
        gestor.volumen(nivel)
        return jsonify({'ok': True, 'volumen': nivel})

    @app.route('/api/voz/hablar', methods=['POST'])
    def voz_hablar():
        datos = request.get_json() or {}
        texto = datos.get('texto', '')
        if not texto:
            return jsonify({'ok': False, 'error': 'Sin texto'})
        gestor.hablar(texto)
        return jsonify({'ok': True})

    @socketio.on('voz_comando')
    def manejar_comando_voz(datos):
        accion = datos.get('accion', '')
        if accion == 'activar':
            gestor.activar(
                nombre_dispositivo=datos.get('nombre'),
                ip_directa=datos.get('ip'),
            )
            socketio.emit('voz_estado', gestor.estado())
        elif accion == 'desactivar':
            gestor.desactivar()
            socketio.emit('voz_estado', gestor.estado())
        elif accion == 'volumen':
            gestor.volumen(float(datos.get('nivel', 0.8)))
        elif accion == 'buscar':
            dispositivos = gestor.buscar_dispositivos()
            socketio.emit('voz_dispositivos', {'dispositivos': dispositivos})