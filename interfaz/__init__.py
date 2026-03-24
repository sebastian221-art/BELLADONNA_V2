# interfaz/__init__.py
# Módulo principal de la interfaz de Bell
# Expone la función para iniciar el servidor

from interfaz.servidor import crear_servidor


def iniciar(host='127.0.0.1', port=5000, debug=False):
    """
    Inicia la interfaz de Bell.
    Llama esto desde el archivo principal.
    """
    app, socketio = crear_servidor()
    print(f'\nBell Interface iniciando en http://{host}:{port}')
    print('Presiona Ctrl+C para detener\n')
    socketio.run(app, host=host, port=port, debug=debug)