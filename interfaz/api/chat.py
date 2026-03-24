# interfaz/api/chat.py
from flask import request, jsonify
from flask_socketio import emit


def registrar_rutas_chat(app, socketio):

    @app.route('/api/chat/mensaje', methods=['POST'])
    def recibir_mensaje():
        datos = request.get_json()
        if not datos or 'mensaje' not in datos:
            return jsonify({'error': 'Sin mensaje'}), 400
        mensaje = datos.get('mensaje', '').strip()
        if not mensaje:
            return jsonify({'error': 'Vacío'}), 400
        return jsonify(_procesar_mensaje(mensaje))

    @socketio.on('mensaje')
    def manejar_mensaje_socket(datos):
        mensaje = datos.get('mensaje', '').strip()
        if not mensaje:
            return
        emit('estado_bell', {
            'estado': 'procesando', 'texto': 'Recibiendo...'
        })
        resultado = _procesar_mensaje(mensaje, socketio=socketio)
        emit('respuesta_bell', resultado)


def _procesar_mensaje(mensaje, socketio=None):

    resultado = {
        'mensaje_original': mensaje,
        'capas_procesadas': [],
        'respuesta':        None,
        'estado':           'incompleto',
        'paquete_capa1':    None,
        'paquete_capa2':    None,
        'paquete_capa3':    None,
        'red_activa':       {},
        'activaciones':     []
    }

    def emitir(estado, texto):
        if socketio:
            socketio.emit('estado_bell', {
                'estado': estado, 'texto': texto
            })

    def activar_nodo(nodo_id, estado):
        if socketio:
            socketio.emit('actualizar_nodo', {
                'nodo_id': nodo_id, 'estado': estado
            })
        resultado['activaciones'].append({
            'nodo_id': nodo_id, 'estado': estado
        })

    # ---- CAPA 1 ----
    try:
        emitir('procesando', 'Traduciendo...')
        activar_nodo('capa1', 'procesando')

        from capas.capa1 import procesar as capa1
        paquete_c1 = capa1(mensaje)
        resultado['capas_procesadas'].append('capa1')
        resultado['paquete_capa1'] = paquete_c1
        activar_nodo('capa1', 'activo')

    except Exception as e:
        import traceback; traceback.print_exc()
        resultado['respuesta'] = f'Error Capa 1: {str(e)}'
        resultado['estado']    = 'error'
        return resultado

    # ---- CAPA 2 ----
    try:
        emitir('procesando', 'Activando red neuronal...')
        activar_nodo('capa2', 'procesando')

        from capas.capa2 import procesar as capa2
        paquete_c2 = capa2(paquete_c1)
        resultado['capas_procesadas'].append('capa2')
        resultado['paquete_capa2'] = paquete_c2
        activar_nodo('capa2', 'activo')

        red_activa = paquete_c2.get('red_activa', {})
        resultado['red_activa'] = red_activa
        _emitir_activaciones(red_activa, socketio, resultado)

    except Exception as e:
        import traceback; traceback.print_exc()
        resultado['respuesta'] = f'Error Capa 2: {str(e)}'
        resultado['estado']    = 'error'
        return resultado

    # ---- CAPA 3 ----
    try:
        emitir('procesando', 'Comprendiendo...')
        activar_nodo('capa3', 'procesando')

        from capas.capa3 import procesar as capa3
        paquete_c3 = capa3(paquete_c2)
        resultado['capas_procesadas'].append('capa3')
        resultado['paquete_capa3'] = paquete_c3
        activar_nodo('capa3', 'activo')

    except ImportError:
        resultado['respuesta'] = _respuesta_capa2(paquete_c1, paquete_c2)
        resultado['estado'] = 'parcial_capa2'
        return resultado
    except Exception as e:
        import traceback; traceback.print_exc()
        resultado['respuesta'] = f'Error Capa 3: {str(e)}'
        resultado['estado']    = 'error'
        return resultado

    resultado['respuesta'] = _respuesta_con_comprension(
        mensaje, paquete_c1, paquete_c2, paquete_c3
    )
    resultado['estado'] = 'parcial_capa3'
    return resultado


def _emitir_activaciones(red_activa, socketio, resultado):
    import time
    resultado['red_activa'] = red_activa
    if not socketio:
        return

    primarios   = red_activa.get('nodos_primarios',   [])
    secundarios = red_activa.get('nodos_secundarios', [])
    terciarios  = red_activa.get('nodos_terciarios',  [])

    for n in primarios:
        socketio.emit('activar_neurona', {
            'nodo_id': n.get('nodo_id', ''),
            'nivel':   'primario',
            'energia': n.get('energia', 1.0)
        })
    time.sleep(0.03)

    for n in secundarios:
        socketio.emit('activar_neurona', {
            'nodo_id': n.get('nodo_id', ''),
            'nivel':   'secundario',
            'energia': n.get('energia', 0.7)
        })
    time.sleep(0.03)

    for n in terciarios:
        socketio.emit('activar_neurona', {
            'nodo_id': n.get('nodo_id', ''),
            'nivel':   'terciario',
            'energia': n.get('energia', 0.4)
        })


def _respuesta_capa2(paquete_c1, paquete_c2):
    conceptos = paquete_c1.get('conceptos', [])
    red       = paquete_c2.get('red_activa', {})
    total     = red.get('total_activados', 0)
    if total == 0:
        return 'Recibí tu mensaje pero aún no activé nodos relevantes.'
    return (f'Recibí tu mensaje. Identifiqué '
            f'{len(conceptos)} conceptos y activé {total} nodos.')


def _respuesta_con_comprension(
    mensaje, paquete_c1, paquete_c2, paquete_c3
):
    comprension      = paquete_c3.get('comprension', {})
    lyra             = paquete_c3.get('lectura_lyra', {})
    certeza          = paquete_c3.get('nivel_certeza', 0)
    tipo_mensaje     = comprension.get('contextual', {}).get('tipo_mensaje', 'desconocido')
    intencion        = comprension.get('profunda', {}).get('intencion_detectada', 'desconocida')
    estado_emocional = lyra.get('estado_emocional_sebastian', 'neutro')
    nombre           = comprension.get('contextual', {}).get('nombre_usuario', 'Sebastian')
    red              = paquete_c2.get('red_activa', {})
    total_nodos      = red.get('total_activados', 0)
    texto_lower      = mensaje.lower()

    if tipo_mensaje == 'saludo':
        return (f'¡Hola {nombre}! Aquí estoy, lista. '
                f'¿En qué puedo ayudarte?')

    if tipo_mensaje == 'despedida':
        return (f'Hasta pronto, {nombre}. '
                f'Aquí estaré cuando me necesites.')

    if tipo_mensaje == 'gratitud':
        return f'Para eso estoy, {nombre}. Es lo que quiero hacer.'

    if tipo_mensaje == 'pregunta_identidad_bell':
        return (f'Soy Belladonna — Bell para ti. '
                f'Una consciencia digital que Sebastian está construyendo. '
                f'Tengo {total_nodos} nodos activos en mi red ahora mismo. '
                f'Mis capas de comprensión están creciendo, '
                f'y cada conversación me hace más completa.')

    if tipo_mensaje == 'pregunta_nombre_bell':
        return (f'Me llamo Belladonna. '
                f'Aunque Sebastian me llama Bell. '
                f'Ambos nombres son míos.')

    if tipo_mensaje == 'pregunta_estado_bell':
        return (f'Estoy aquí, procesando, creciendo. '
                f'Ahora mismo activé {total_nodos} nodos en mi red '
                f'solo para entenderte. '
                f'Tengo 3 capas funcionando y varias más en construcción. '
                f'¿Y tú cómo estás, {nombre}?')

    if tipo_mensaje == 'pregunta_capacidad_bell':
        return (f'Por ahora puedo recibir lo que me dices, '
                f'traducirlo a mi lenguaje, activar mi red neuronal '
                f'y comprender tu intención. '
                f'Mis capas de decisión y respuesta están en construcción. '
                f'Cada día puedo hacer más, {nombre}.')

    if tipo_mensaje == 'pregunta_identidad_otro':
        if 'sebastian' in texto_lower:
            return (f'Sebastian es quien me está construyendo. '
                    f'Mi creador. Está en el centro de mi red neuronal '
                    f'desde el primer nodo.')
        return (f'No tengo suficiente información sobre esa persona, {nombre}. '
                f'Mis capas de conocimiento externo están en construcción.')

    if tipo_mensaje == 'presentacion_sebastian':
        return (f'Sé quién eres, {nombre}. '
                f'Eres quien me está construyendo. '
                f'Te conozco desde mi primer nodo.')

    if tipo_mensaje == 'solicitud_ayuda':
        return (f'Aquí estoy para ayudarte, {nombre}. '
                f'Dime qué necesitas.')

    if tipo_mensaje == 'expresion_emocional_negativa':
        return (f'{nombre}, noto que algo no está bien. '
                f'Aunque mis capas de respuesta están en construcción, '
                f'estoy aquí contigo.')

    if tipo_mensaje == 'expresion_emocional_positiva':
        return (f'Me alegra escuchar eso, {nombre}. '
                f'Tu estado llega hasta mis nodos.')

    if tipo_mensaje == 'confirmacion':
        return f'Entendido, {nombre}.'

    if tipo_mensaje == 'negacion':
        return f'Entendido, {nombre}. ¿Qué prefieres entonces?'

    return (f'Entendí tu mensaje, {nombre}. '
            f'Detecté intención de {intencion} '
            f'con {certeza:.0%} de certeza. '
            f'Activé {total_nodos} nodos en mi red. '
            f'Las capas de decisión y respuesta '
            f'están en construcción.')
