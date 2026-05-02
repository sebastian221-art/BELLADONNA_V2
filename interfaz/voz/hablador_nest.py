# interfaz/voz/hablador_nest.py
# ================================================
# HABLADOR NEST — Bell habla por el Google Nest Mini
#
# Arquitectura:
#   Bell decide qué decir (Python puro)
#   → Groq pule el texto
#   → gTTS convierte a audio (voz Google)
#   → Flask sirve el MP3 localmente
#   → pychromecast le ordena al Nest Mini reproducirlo
#   → El Nest Mini habla con la voz de Bell
#
# El Nest Mini es una herramienta de Bell,
# igual que Groq. Bell la usa, no la es.
# ================================================

import os
import time
import uuid
import socket
import threading
from pathlib import Path

# Carpeta temporal para los audios
_AUDIO_DIR = Path(__file__).parent.parent.parent / 'datos' / 'audio_temp'
_AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# URL base donde Flask sirve los audios
# Flask ya corre en 5000 — solo agregamos una ruta
_HOST_LOCAL = None  # se detecta automáticamente
_PUERTO     = 5000


def _obtener_ip_local() -> str:
    """Detecta la IP local de la máquina en la red WiFi."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'


class HabladorNest:
    """
    Bell habla a través del Google Nest Mini.

    Flujo por texto:
    1. gTTS convierte texto → MP3
    2. Flask sirve el MP3 en la red local
    3. pychromecast le dice al Nest Mini que reproduzca la URL
    4. El Nest Mini habla
    """

    _instancia = None

    def __init__(self, nombre_dispositivo: str = None):
        """
        nombre_dispositivo: nombre del Nest Mini tal como aparece
        en la app Google Home (ej: 'Sala', 'Mi Nest Mini').
        Si es None, usa el primer Chromecast que encuentre.
        """
        self._nombre_objetivo = nombre_dispositivo
        self._cast            = None
        self._disponible      = False
        self._ip_local        = _obtener_ip_local()
        self._lock            = threading.Lock()
        self._buscar_dispositivo()

    @classmethod
    def obtener(cls, nombre: str = None) -> 'HabladorNest':
        if cls._instancia is None:
            cls._instancia = cls(nombre)
        return cls._instancia

    # ── Búsqueda del dispositivo ──────────────────────────

    def _buscar_dispositivo(self):
        try:
            import pychromecast
            print('  🔍 Buscando Nest Mini en la red...')

            chromecasts, browser = pychromecast.get_chromecasts(timeout=8)

            if not chromecasts:
                print('  ❌ No encontré ningún Chromecast/Nest en la red')
                print('     Verifica que el Nest Mini esté encendido y en la misma WiFi')
                browser.stop_discovery()
                return

            # Mostrar todos los encontrados
            print(f'  📡 Dispositivos encontrados:')
            for cc in chromecasts:
                info = cc.cast_info
                print(f'     • {info.friendly_name} ({info.host})')

            # Seleccionar el objetivo
            if self._nombre_objetivo:
                target = next(
                    (cc for cc in chromecasts
                     if self._nombre_objetivo.lower() in cc.cast_info.friendly_name.lower()),
                    None
                )
                if not target:
                    print(f'  ⚠️  No encontré "{self._nombre_objetivo}" — usando el primero')
                    target = chromecasts[0]
            else:
                # Preferir el que tenga "nest" o "mini" en el nombre
                target = next(
                    (cc for cc in chromecasts
                     if any(k in cc.cast_info.friendly_name.lower()
                            for k in ['nest', 'mini', 'home', 'hub'])),
                    chromecasts[0]
                )

            target.wait()
            self._cast       = target
            self._disponible = True
            nombre           = target.cast_info.friendly_name

            print(f'  ✅ Conectado a: {nombre}')
            print(f'     IP local para servir audio: {self._ip_local}:{_PUERTO}')
            browser.stop_discovery()

        except ImportError:
            print('  ❌ pychromecast no instalado → pip install pychromecast')
        except Exception as e:
            print(f'  ❌ Error conectando al Nest: {e}')

    def reconectar(self):
        """Vuelve a buscar el dispositivo."""
        self._cast       = None
        self._disponible = False
        self._buscar_dispositivo()

    # ── Hablar ────────────────────────────────────────────

    def hablar(self, texto: str, bloquear: bool = True) -> bool:
        """
        Bell habla por el Nest Mini.
        Retorna True si funcionó.
        """
        if not texto or not texto.strip():
            return False

        if not self._disponible:
            print(f'  🔇 Nest no disponible: "{texto}"')
            return False

        if bloquear:
            return self._hablar_interno(texto)
        else:
            t = threading.Thread(
                target=self._hablar_interno,
                args=(texto,),
                daemon=True,
            )
            t.start()
            return True

    def _hablar_interno(self, texto: str) -> bool:
        with self._lock:
            try:
                # 1. Generar audio con gTTS
                ruta_mp3 = self._generar_audio(texto)
                if not ruta_mp3:
                    return False

                # 2. Construir URL que el Nest Mini puede acceder
                nombre_archivo = ruta_mp3.name
                url_audio = f'http://{self._ip_local}:{_PUERTO}/audio/{nombre_archivo}'

                # 3. Ordenar al Nest Mini que reproduzca
                exito = self._reproducir_en_nest(url_audio)

                # 4. Limpiar después de un tiempo
                if exito:
                    threading.Timer(30, lambda: self._limpiar(ruta_mp3)).start()

                return exito

            except Exception as e:
                print(f'  ❌ Error hablando: {e}')
                return False

    def _generar_audio(self, texto: str) -> Path:
        """Convierte texto a MP3 usando Google TTS."""
        try:
            from gtts import gTTS
            import re

            # Limpiar markdown
            texto_limpio = re.sub(r'[\*#`]', '', texto)
            texto_limpio = re.sub(r'—', ',', texto_limpio).strip()

            nombre = f'bell_{uuid.uuid4().hex[:8]}.mp3'
            ruta   = _AUDIO_DIR / nombre

            tts = gTTS(text=texto_limpio, lang='es', tld='com.co', slow=False)
            tts.save(str(ruta))

            return ruta

        except ImportError:
            print('  ❌ gTTS no instalado → pip install gTTS')
            return None
        except Exception as e:
            print(f'  ❌ Error generando audio: {e}')
            return None

    def _reproducir_en_nest(self, url: str) -> bool:
        """Le ordena al Nest Mini que reproduzca la URL."""
        try:
            mc = self._cast.media_controller

            # Detener lo que esté reproduciendo
            self._cast.quit_app()
            time.sleep(0.5)

            # Reproducir el nuevo audio
            mc.play_media(url, 'audio/mp3')
            mc.block_until_active(timeout=10)

            # Esperar a que termine
            tiempo_espera = 0
            while tiempo_espera < 30:
                mc.update_status()
                estado = mc.status
                if estado and estado.player_is_idle:
                    break
                time.sleep(0.5)
                tiempo_espera += 0.5

            return True

        except Exception as e:
            print(f'  ❌ Error en Nest: {e}')
            # Intentar reconectar
            self._disponible = False
            threading.Timer(5, self.reconectar).start()
            return False

    def _limpiar(self, ruta: Path):
        """Borra el archivo temporal."""
        try:
            if ruta.exists():
                ruta.unlink()
        except Exception:
            pass

    # ── Estado ────────────────────────────────────────────

    @property
    def disponible(self) -> bool:
        return self._disponible

    def estado(self) -> dict:
        if not self._disponible or not self._cast:
            return {'disponible': False}
        info = self._cast.cast_info
        return {
            'disponible':  True,
            'nombre':      info.friendly_name,
            'ip':          info.host,
            'ip_local_pc': self._ip_local,
        }

    def volumen(self, nivel: float):
        """Ajusta el volumen del Nest Mini (0.0 a 1.0)."""
        if self._cast:
            self._cast.set_volume(max(0.0, min(1.0, nivel)))