# interfaz/voz/escuchador_sd.py
# ================================================
# ESCUCHADOR CON SOUNDDEVICE
# Alternativa a pyaudio para Python 3.14+
#
# Instalar:
#   pip install sounddevice soundfile numpy
# ================================================

import io
import time
import threading
import tempfile
from pathlib import Path


class EscuchadorSD:
    """
    Escucha el micrófono usando sounddevice (sin pyaudio).
    Compatible con Python 3.14+.
    """

    def __init__(self):
        self._sd      = None
        self._sr_lib  = None
        self._ok      = False
        self._idioma  = 'es-CO'
        self._init()

    def _init(self):
        try:
            import sounddevice as sd
            import speech_recognition as sr
            import numpy as np

            self._sd     = sd
            self._sr_lib = sr
            self._np     = np
            self._rec    = sr.Recognizer()

            # Verificar que hay micrófono
            dispositivos = sd.query_devices()
            hay_entrada  = any(d['max_input_channels'] > 0 for d in dispositivos)

            if not hay_entrada:
                print('  ❌ No se detectó micrófono')
                return

            # Mostrar dispositivo seleccionado
            default = sd.default.device[0]
            nombre  = dispositivos[default]['name'] if default is not None else 'predeterminado'
            print(f'  ✅ Micrófono: {nombre}')

            self._ok = True

        except ImportError as e:
            faltante = str(e).split("'")[1] if "'" in str(e) else str(e)
            print(f'  ❌ Falta: pip install {faltante}')
            if 'sounddevice' in str(e):
                print('     Instala: pip install sounddevice soundfile numpy')
        except Exception as e:
            print(f'  ❌ Error mic: {e}')

    def _grabar(self, segundos: float, samplerate: int = 16000) -> bytes:
        """Graba audio y retorna bytes WAV."""
        import soundfile as sf

        frames = int(samplerate * segundos)
        audio  = self._sd.rec(frames, samplerate=samplerate, channels=1, dtype='int16')
        self._sd.wait()

        # Convertir a WAV en memoria
        buffer = io.BytesIO()
        sf.write(buffer, audio, samplerate, format='WAV', subtype='PCM_16')
        buffer.seek(0)
        return buffer.read()

    def _reconocer(self, wav_bytes: bytes) -> str:
        """Envía el WAV a Google Speech Recognition."""
        sr  = self._sr_lib
        rec = self._rec
        fuente = sr.AudioData(wav_bytes, 16000, 2)
        return rec.recognize_google(fuente, language=self._idioma).strip()

    def escuchar_corto(self) -> str:
        """Graba 4 segundos y retorna lo que escuchó."""
        if not self._ok:
            return ''
        try:
            wav = self._grabar(4.0)
            return self._reconocer(wav).lower()
        except Exception:
            return ''

    def escuchar_mensaje(self) -> str:
        """Graba hasta 12 segundos para el mensaje completo."""
        if not self._ok:
            return ''
        try:
            print('  🎤 Habla ahora...', end='', flush=True)
            wav = self._grabar(12.0)
            texto = self._reconocer(wav)
            print(f'\r  ✓ "{texto}"          ')
            return texto
        except Exception:
            print('\r  (no escuché nada)          ')
            return ''

    def escuchar_con_vad(self, timeout: int = 6) -> str:
        """
        Versión mejorada: escucha hasta detectar silencio.
        Más natural que grabar tiempo fijo.
        """
        if not self._ok:
            return ''
        try:
            sr  = self._sr_lib
            rec = self._rec

            # Usar micrófono virtual construido desde sounddevice
            wav_bytes = self._grabar_con_silencio(timeout)
            if not wav_bytes:
                return ''
            return self._reconocer(wav_bytes).lower()
        except Exception:
            return ''

    def _grabar_con_silencio(self, timeout: int = 6, samplerate: int = 16000) -> bytes:
        """
        Graba hasta detectar silencio sostenido.
        Para hacer la conversación más natural.
        """
        import soundfile as sf

        umbral_silencio = 500   # energía mínima para considerar voz
        segundos_silencio = 1.5  # segundos de silencio para cortar
        chunk_ms  = 200          # ms por chunk
        chunk_frames = int(samplerate * chunk_ms / 1000)

        frames_totales   = []
        frames_silencio  = 0
        max_frames_sil   = int(segundos_silencio * 1000 / chunk_ms)
        max_total        = int(timeout * 1000 / chunk_ms)
        encontro_voz     = False
        contador         = 0

        with self._sd.InputStream(samplerate=samplerate, channels=1, dtype='int16') as stream:
            while contador < max_total:
                chunk, _ = stream.read(chunk_frames)
                energia  = int(self._np.abs(chunk).mean())
                frames_totales.append(chunk.copy())
                contador += 1

                if energia > umbral_silencio:
                    encontro_voz  = True
                    frames_silencio = 0
                elif encontro_voz:
                    frames_silencio += 1
                    if frames_silencio >= max_frames_sil:
                        break

        if not encontro_voz or not frames_totales:
            return b''

        audio_completo = self._np.concatenate(frames_totales, axis=0)
        buffer = io.BytesIO()
        import soundfile as sf
        sf.write(buffer, audio_completo, samplerate, format='WAV', subtype='PCM_16')
        buffer.seek(0)
        return buffer.read()

    @property
    def ok(self) -> bool:
        return self._ok