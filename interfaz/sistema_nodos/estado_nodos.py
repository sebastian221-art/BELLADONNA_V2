# interfaz/sistema_nodos/estado_nodos.py
# ================================================
# ESTADO DE NODOS — Estado actual en tiempo real
# Mantiene qué nodos están activos, procesando
# o con error en este momento
# ================================================

import time


class EstadoNodos:
    """
    Mantiene el estado actual de cada nodo
    en tiempo real durante el procesamiento.
    """

    _instancia = None

    def __init__(self):
        self.estados = {}
        self.historial = []
        self.socketio = None
        self.max_historial = 100

    @classmethod
    def obtener(cls):
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def configurar_socket(self, socketio):
        """
        Configura el WebSocket para notificaciones
        en tiempo real.
        """
        self.socketio = socketio

    def activar(self, nodo_id, texto_indicador=None):
        """
        Marca un nodo como activo.
        Notifica al frontend automáticamente.
        """
        self._cambiar_estado(nodo_id, 'activo', texto_indicador)

    def procesando(self, nodo_id, texto_indicador=None):
        """
        Marca un nodo como en procesamiento.
        """
        self._cambiar_estado(nodo_id, 'procesando', texto_indicador)

    def completar(self, nodo_id):
        """
        Marca un nodo como completado — activo.
        """
        self._cambiar_estado(nodo_id, 'activo')

        # Volver a inactivo después de un momento
        # para que la visualización no quede saturada
        self._programar_inactivar(nodo_id, delay=2.0)

    def error(self, nodo_id, mensaje=None):
        """
        Marca un nodo con error.
        """
        self._cambiar_estado(nodo_id, 'error', mensaje)

    def inactivar(self, nodo_id):
        """
        Marca un nodo como inactivo.
        """
        self._cambiar_estado(nodo_id, 'inactivo')

    def inactivar_todos(self):
        """
        Inactiva todos los nodos activos.
        Se llama cuando Bell termina de procesar.
        """
        nodos_activos = [
            nodo_id for nodo_id, estado in self.estados.items()
            if estado['estado'] in ('activo', 'procesando')
        ]
        for nodo_id in nodos_activos:
            self.inactivar(nodo_id)

    def _cambiar_estado(self, nodo_id, nuevo_estado,
                        texto=None):
        """
        Cambia el estado de un nodo y notifica.
        """
        estado_anterior = self.estados.get(
            nodo_id, {}
        ).get('estado', 'inactivo')

        self.estados[nodo_id] = {
            'estado': nuevo_estado,
            'texto': texto,
            'timestamp': time.time()
        }

        # Guardar en historial
        self.historial.append({
            'nodo_id': nodo_id,
            'estado_anterior': estado_anterior,
            'estado_nuevo': nuevo_estado,
            'timestamp': time.time()
        })

        # Limpiar historial si es muy largo
        if len(self.historial) > self.max_historial:
            self.historial = self.historial[-self.max_historial:]

        # Actualizar registro central
        try:
            from interfaz.sistema_nodos.registro_nodos import RegistroNodos
            RegistroNodos.obtener().actualizar_estado_nodo(
                nodo_id, nuevo_estado
            )
        except Exception:
            pass

        # Notificar al frontend via WebSocket
        self._notificar(nodo_id, nuevo_estado, texto)

    def _notificar(self, nodo_id, estado, texto=None):
        """
        Envía actualización al frontend via WebSocket.
        """
        if not self.socketio:
            return

        datos = {
            'nodo_id': nodo_id,
            'estado': estado
        }

        if texto:
            datos['texto'] = texto

        try:
            self.socketio.emit('actualizar_nodo', datos)

            if texto:
                self.socketio.emit('estado_bell', {
                    'estado': estado,
                    'texto': texto
                })
        except Exception as e:
            print(f'Error notificando estado: {e}')

    def _programar_inactivar(self, nodo_id, delay=2.0):
        """
        Inactiva un nodo después de un delay.
        Usa un hilo separado para no bloquear.
        """
        import threading

        def inactivar_despues():
            time.sleep(delay)
            self.inactivar(nodo_id)

        hilo = threading.Thread(
            target=inactivar_despues,
            daemon=True
        )
        hilo.start()

    def obtener_estado(self, nodo_id):
        """
        Retorna el estado actual de un nodo.
        """
        return self.estados.get(nodo_id, {
            'estado': 'inactivo',
            'texto': None,
            'timestamp': None
        })