# interfaz/servidor.py
# ================================================
# SERVIDOR — Flask + WebSockets
# El corazón del backend de la interfaz
# Maneja rutas y comunicación en tiempo real
# ================================================

from flask import Flask, send_from_directory
from flask_socketio import SocketIO
from pathlib import Path

# Ruta a los archivos del frontend
FRONTEND = Path(__file__).parent / 'frontend'


def crear_servidor():
    """
    Crea y configura el servidor Flask.
    Retorna app y socketio para que
    puedan ser usados externamente.
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'bell-consciencia-digital'

    socketio = SocketIO(
        app,
        cors_allowed_origins='*',
        async_mode='threading'
    )

    # Registrar rutas
    _registrar_rutas_principales(app)
    _registrar_rutas_api(app, socketio)
    _registrar_eventos_socket(socketio)
    _iniciar_servicios(socketio)

    return app, socketio


def _registrar_rutas_principales(app):
    """
    Rutas principales — sirven el frontend.
    """

    @app.route('/')
    def index():
        return send_from_directory(FRONTEND, 'index.html')

    @app.route('/estilos/<path:filename>')
    def estilos(filename):
        return send_from_directory(FRONTEND / 'estilos', filename)

    @app.route('/scripts/<path:filename>')
    def scripts(filename):
        return send_from_directory(FRONTEND / 'scripts', filename)


def _registrar_rutas_api(app, socketio):
    """
    Registra los endpoints de la API.
    Cada módulo de API registra sus propias rutas.
    """
    from interfaz.api.chat import registrar_rutas_chat
    from interfaz.api.visualizacion import registrar_rutas_visualizacion
    from interfaz.api.diagnostico import registrar_rutas_diagnostico
    registrar_rutas_diagnostico(app)
    registrar_rutas_chat(app, socketio)
    registrar_rutas_visualizacion(app, socketio)


def _registrar_eventos_socket(socketio):
    """
    Eventos globales de WebSocket.
    """

    @socketio.on('connect')
    def manejar_conexion():
        print('Frontend conectado')
        # Enviar estado inicial
        try:
            from interfaz.sistema_nodos.registro_nodos import RegistroNodos
            from flask_socketio import emit
            registro = RegistroNodos.obtener()
            emit('estado_red', registro.obtener_estado_completo())
        except Exception as e:
            print(f'Error enviando estado inicial: {e}')

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
            emit('estado_red', {
                'error': str(e),
                'nodos': [],
                'conexiones': []
            })


def _iniciar_servicios(socketio):
    """
    Inicia los servicios de fondo.
    """
    try:
        import os
        from interfaz.sistema_nodos.registro_nodos import RegistroNodos
        from interfaz.sistema_nodos.detector_archivos import DetectorArchivos
        from interfaz.sistema_nodos.estado_nodos import EstadoNodos

        # Obtener raíz del proyecto
        raiz = os.environ.get(
            'BELLADONNA_ROOT',
            os.environ.get('BELL_RAIZ', '')
        )
        if not raiz:
            from pathlib import Path
            raiz = str(Path(__file__).parent.parent)

        # Iniciar registro
        registro = RegistroNodos.obtener()
        print(f'Registro iniciado: {len(registro.nodos)} nodos')

        # Iniciar detector con la raíz correcta
        detector = DetectorArchivos(registro, raiz)
        detector.iniciar()

        # Configurar estado de nodos
        EstadoNodos.obtener().configurar_socket(socketio)

        print('Servicios de Bell iniciados')

    except Exception as e:
        import traceback
        print(f'Error iniciando servicios: {e}')
        traceback.print_exc()