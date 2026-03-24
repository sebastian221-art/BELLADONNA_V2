# interfaz/api/visualizacion.py
# ================================================
# API de visualización — versión 2
# Ahora incluye vitalidad y nivel de vida
# en todos los nodos
# ================================================

from flask import jsonify
from flask_socketio import emit


def registrar_rutas_visualizacion(app, socketio):

    @app.route('/api/visualizacion/estado', methods=['GET'])
    def obtener_estado():
        try:
            from interfaz.sistema_nodos.registro_nodos import RegistroNodos
            registro = RegistroNodos.obtener()
            estado   = registro.obtener_estado_completo()
            estado['biblioteca'] = _estado_biblioteca()
            return jsonify(estado)
        except Exception as e:
            return jsonify({'error': str(e), 'nodos': [], 'conexiones': []}), 500

    @app.route('/api/visualizacion/neuronal', methods=['GET'])
    def obtener_red_neuronal():
        try:
            datos = _red_neuronal_visual()
            return jsonify(datos)
        except Exception as e:
            return jsonify({'error': str(e), 'nodos': [], 'conexiones': [], 'disponible': False})

    @app.route('/api/visualizacion/vida', methods=['GET'])
    def obtener_vista_vida():
        """
        NUEVA — Vista de vida.
        Retorna todos los nodos con su nivel de vitalidad
        para la vista de vida 3D.
        """
        try:
            datos = _vida_visual()
            return jsonify(datos)
        except Exception as e:
            return jsonify({'error': str(e), 'disponible': False})

    @app.route('/api/visualizacion/nodo/<nodo_id>', methods=['GET'])
    def obtener_nodo(nodo_id):
        try:
            from interfaz.sistema_nodos.registro_nodos import RegistroNodos
            nodo = RegistroNodos.obtener().obtener_nodo(nodo_id)
            if not nodo:
                nodo = _buscar_en_biblioteca(nodo_id)
            if not nodo:
                return jsonify({'error': f'Nodo {nodo_id} no encontrado'}), 404
            return jsonify(nodo)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @socketio.on('solicitar_estado')
    def manejar_solicitud_estado():
        try:
            from interfaz.sistema_nodos.registro_nodos import RegistroNodos
            estado = RegistroNodos.obtener().obtener_estado_completo()
            estado['biblioteca'] = _estado_biblioteca()
            emit('estado_red', estado)
        except Exception as e:
            emit('estado_red', {'error': str(e), 'nodos': [], 'conexiones': []})

    @socketio.on('solicitar_red_neuronal')
    def manejar_solicitud_neuronal():
        try:
            emit('red_neuronal', _red_neuronal_visual())
        except Exception as e:
            emit('red_neuronal', {'error': str(e), 'disponible': False})

    @socketio.on('solicitar_vista_vida')
    def manejar_solicitud_vida():
        try:
            emit('vista_vida', _vida_visual())
        except Exception as e:
            emit('vista_vida', {'error': str(e), 'disponible': False})


def _estado_biblioteca() -> dict:
    try:
        from biblioteca import Biblioteca
        return Biblioteca.obtener().estado()
    except Exception as e:
        return {'disponible': False, 'error': str(e)}


def _red_neuronal_visual() -> dict:
    try:
        from biblioteca import Biblioteca
        biblioteca = Biblioteca.obtener()
        if not biblioteca.iniciada:
            return {'disponible': False, 'nodos': [], 'conexiones': []}
        datos = biblioteca.obtener_nodos_para_visualizacion()
        datos['disponible'] = True
        return datos
    except Exception as e:
        return {'disponible': False, 'error': str(e), 'nodos': [], 'conexiones': []}


def _vida_visual() -> dict:
    """
    Retorna nodos con información de vida para la vista de vida.
    Incluye vitalidad, nivel_vida y los tipos de grounding activos.
    """
    try:
        from biblioteca import Biblioteca
        biblioteca = Biblioteca.obtener()
        if not biblioteca.iniciada:
            return {'disponible': False, 'nodos': [], 'estadisticas': {}}

        todos  = biblioteca.red.obtener_todos_los_nodos()
        nodos  = []
        stats  = {
            'plena': 0, 'rica': 0, 'funcional': 0,
            'emergente': 0, 'latente': 0, 'dormida': 0,
            'total': 0, 'vitalidad_promedio': 0.0
        }
        vitalidades = []

        for nid in todos:
            neurona = biblioteca.red.obtener_neurona(nid)
            if not neurona:
                continue

            datos_ext  = neurona.nucleo.datos_extra
            vitalidad  = datos_ext.get('vitalidad',  0.0)
            nivel_vida = datos_ext.get('nivel_vida', 'dormida')
            perfil     = datos_ext.get('perfil_vida', {})

            # Color según nivel de vida
            color = _color_vida(nivel_vida, vitalidad)

            nodos.append({
                'id':         nid,
                'nombre':     nid.replace('_', ' ').title(),
                'tipo':       neurona.nucleo.tipo,
                'vitalidad':  vitalidad,
                'nivel_vida': nivel_vida,
                'color_vida': color,
                'brilla':     vitalidad > 0.2,
                'intensidad_brillo': vitalidad,
                'tipos_grounding': _tipos_activos(perfil),
                'grounding_efectivo': neurona.grounding_efectivo(),
            })

            vitalidades.append(vitalidad)
            if nivel_vida in stats:
                stats[nivel_vida] += 1
            stats['total'] += 1

        if vitalidades:
            stats['vitalidad_promedio'] = round(
                sum(vitalidades) / len(vitalidades), 3
            )

        return {
            'disponible':  True,
            'nodos':       nodos,
            'estadisticas': stats,
            'total_vivos': sum(1 for v in vitalidades if v > 0.2),
        }

    except Exception as e:
        return {'disponible': False, 'error': str(e), 'nodos': [], 'estadisticas': {}}


def _color_vida(nivel: str, vitalidad: float) -> str:
    """Color hexadecimal según el nivel de vida."""
    colores = {
        'plena':      '#00FF88',  # Verde brillante
        'rica':       '#44FFAA',  # Verde claro
        'funcional':  '#88FFCC',  # Verde suave
        'emergente':  '#AAFFDD',  # Verde muy suave
        'latente':    '#FFD700',  # Dorado — vida latente
        'dormida':    '#334455',  # Gris azulado — dormido
    }
    return colores.get(nivel, '#334455')


def _tipos_activos(perfil: dict) -> list:
    """Lista de tipos de grounding con valor > 0.3."""
    if not perfil or 'tipos' not in perfil:
        return []
    tipos = perfil.get('tipos', {})
    return [
        tipo for tipo, valor in tipos.items()
        if isinstance(valor, float) and valor > 0.3
    ]


def _buscar_en_biblioteca(nodo_id: str) -> dict:
    try:
        from biblioteca import Biblioteca
        return Biblioteca.obtener().red.obtener_nodo(nodo_id)
    except Exception:
        return None


def emitir_actualizacion_nodo(socketio, nodo_id, nuevo_estado):
    socketio.emit('actualizar_nodo', {'nodo_id': nodo_id, 'estado': nuevo_estado})