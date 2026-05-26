# interfaz/servidor.py
# ================================================
# SERVIDOR — Flask + WebSockets + Voz integrada
# ================================================

from flask import Flask, send_from_directory
from flask_socketio import SocketIO
from pathlib import Path

import socketio

FRONTEND = Path(__file__).parent / 'frontend'


def crear_servidor():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'bell-consciencia-digital'

    socketio = SocketIO(
        app,
        cors_allowed_origins='*',
        async_mode='threading',
    )

    _registrar_rutas_principales(app)
    _registrar_rutas_api(app, socketio)
    _registrar_eventos_socket(socketio)
    _iniciar_servicios(socketio)

    return app, socketio


def _registrar_rutas_principales(app):

    @app.route('/')
    def index():
        return send_from_directory(FRONTEND, 'index.html')

    @app.route('/chat')
    def chat():
        return send_from_directory(FRONTEND, 'chat.html')

    @app.route('/estilos/<path:filename>')
    def estilos(filename):
        return send_from_directory(FRONTEND / 'estilos', filename)

    @app.route('/scripts/<path:filename>')
    def scripts(filename):
        return send_from_directory(FRONTEND / 'scripts', filename)


def _registrar_rutas_api(app, socketio):
    from interfaz.api.audio        import registrar_rutas_audio
    from interfaz.api.chat         import registrar_rutas_chat
    from interfaz.api.visualizacion import registrar_rutas_visualizacion
    from interfaz.api.diagnostico  import registrar_rutas_diagnostico
    from interfaz.api.voz          import registrar_rutas_voz

    # audio.py registra /audio/<nombre> — debe ir PRIMERO
    # para que el Nest Mini pueda descargar los MP3 generados por gTTS
    registrar_rutas_audio(app)

    registrar_rutas_diagnostico(app)
    registrar_rutas_chat(app, socketio)
    registrar_rutas_visualizacion(app, socketio)
    registrar_rutas_voz(app, socketio)


def _registrar_eventos_socket(socketio):

    @socketio.on('connect')
    def manejar_conexion():
        from flask_socketio import emit
        print('Frontend conectado')
        try:
            from interfaz.sistema_nodos.registro_nodos import RegistroNodos
            registro = RegistroNodos.obtener()
            emit('estado_red', registro.obtener_estado_completo())
        except Exception as e:
            print(f'Error enviando estado inicial: {e}')

        try:
            from interfaz.api.voz import GestorVoz
            emit('voz_estado', GestorVoz.obtener().estado())
        except Exception:
            pass

    @socketio.on('disconnect')
    def manejar_desconexion():
        print('Frontend desconectado')

    @socketio.on('solicitar_estado')
    def manejar_solicitud_estado():
        from interfaz.sistema_nodos.registro_nodos import RegistroNodos
        from flask_socketio import emit
        try:
            registro = RegistroNodos.obtener()
            emit('estado_red', registro.obtener_estado_completo())
        except Exception as e:
            emit('estado_red', {'error': str(e), 'nodos': [], 'conexiones': []})


def _iniciar_servicios(socketio):
    try:
        import os
        from interfaz.sistema_nodos.registro_nodos import RegistroNodos
        from interfaz.sistema_nodos.detector_archivos import DetectorArchivos
        from interfaz.sistema_nodos.estado_nodos import EstadoNodos

        raiz = os.environ.get('BELLADONNA_ROOT', os.environ.get('BELL_RAIZ', ''))
        if not raiz:
            raiz = str(Path(__file__).parent.parent)

        registro = RegistroNodos.obtener()
        print(f'Registro iniciado: {len(registro.nodos)} nodos')

        detector = DetectorArchivos(registro, raiz)
        detector.iniciar()

        # Auto-reload de código en caliente (no mata el proceso)
        try:
            from interfaz.auto_reload import iniciar_auto_reload
            iniciar_auto_reload(raiz)
        except Exception as e:
            print(f'  ♻  Auto-reload no disponible: {e}')

        EstadoNodos.obtener().configurar_socket(socketio)
        print('Servicios de Bell iniciados')

    except Exception as e:
        import traceback
        print(f'Error iniciando servicios: {e}')
        traceback.print_exc()


from biblioteca.habilidades.python.observador_proyecto import iniciar_pair_programmer

def alerta_callback(ruta, alertas, analisis):
    socketio.emit('bell_alerta', {'ruta': ruta, 'alertas': alertas})

iniciar_pair_programmer('/ruta/a/BELLADONNA', alerta_callback)