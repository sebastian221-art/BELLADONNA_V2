# interfaz/api/audio.py
# ================================================
# RUTA DE AUDIO — sirve los MP3 al Nest Mini
#
# El Nest Mini necesita una URL HTTP para reproducir.
# Flask ya corre en el puerto 5000.
# Esta ruta sirve los archivos de audio temporales.
#
# URL: http://192.168.x.x:5000/audio/bell_abc123.mp3
# ================================================

from flask import send_from_directory, abort
from pathlib import Path

_AUDIO_DIR = Path(__file__).parent.parent.parent / 'datos' / 'audio_temp'


def registrar_rutas_audio(app):

    @app.route('/audio/<nombre_archivo>')
    def servir_audio(nombre_archivo: str):
        # Seguridad: solo servir archivos .mp3 de bell_
        if not nombre_archivo.startswith('bell_') or not nombre_archivo.endswith('.mp3'):
            abort(403)
        if not (_AUDIO_DIR / nombre_archivo).exists():
            abort(404)
        return send_from_directory(str(_AUDIO_DIR), nombre_archivo)