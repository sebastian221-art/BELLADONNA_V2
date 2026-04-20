# interfaz/api/chat.py
# ================================================
# CHAT — Capas 1-9 COMPLETAS
# El flujo completo de Bell.
# ================================================

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
        emit('estado_bell', {'estado': 'procesando', 'texto': 'Recibiendo...'})
        resultado = _procesar_mensaje(mensaje, socketio=socketio)
        emit('respuesta_bell', resultado)


def _procesar_mensaje(mensaje, socketio=None):

    resultado = {
        'mensaje_original': mensaje,
        'capas_procesadas': [],
        'respuesta':        None,
        'estado':           'incompleto',
        'red_activa':       {},
        'activaciones':     [],
        'deliberacion':     None,
        'fuente_respuesta': None,
        'ejecucion':        None,
        'tono_final':       None,
        'bell_core_actualizado': False,
    }

    def emitir(estado, texto):
        if socketio:
            socketio.emit('estado_bell', {'estado': estado, 'texto': texto})

    def nodo(nodo_id, estado):
        if socketio:
            socketio.emit('actualizar_nodo', {'nodo_id': nodo_id, 'estado': estado})
        resultado['activaciones'].append({'nodo_id': nodo_id, 'estado': estado})

    # ── CAPA 1 ───────────────────────────────────────────
    try:
        emitir('procesando', 'Traduciendo...')
        nodo('capa1', 'procesando')
        from capas.capa1 import procesar as c1
        pc1 = c1(mensaje)
        resultado['capas_procesadas'].append('capa1')
        nodo('capa1', 'activo')
    except Exception as e:
        resultado['respuesta'] = f'Error Capa 1: {e}'
        resultado['estado'] = 'error'
        return resultado

    # ── CAPA 2 ───────────────────────────────────────────
    try:
        emitir('procesando', 'Activando red neuronal...')
        nodo('capa2', 'procesando')
        from capas.capa2 import procesar as c2
        pc2 = c2(pc1)
        resultado['capas_procesadas'].append('capa2')
        resultado['red_activa'] = pc2.get('red_activa', {})
        nodo('capa2', 'activo')
        _emitir_activaciones(pc2.get('red_activa', {}), socketio, resultado)
    except Exception as e:
        resultado['respuesta'] = f'Error Capa 2: {e}'
        resultado['estado'] = 'error'
        return resultado

    # ── CAPA 3 ───────────────────────────────────────────
    try:
        emitir('procesando', 'Comprendiendo...')
        nodo('capa3', 'procesando')
        from capas.capa3 import procesar as c3
        pc3 = c3(pc2)
        resultado['capas_procesadas'].append('capa3')
        nodo('capa3', 'activo')
    except ImportError:
        resultado['respuesta'] = 'Capa 3 no disponible.'
        resultado['estado'] = 'parcial_capa2'
        return resultado
    except Exception as e:
        resultado['respuesta'] = f'Error Capa 3: {e}'
        resultado['estado'] = 'error'
        return resultado

    # ── CAPA 4 ───────────────────────────────────────────
    try:
        emitir('procesando', 'Evaluando...')
        nodo('capa4', 'procesando')
        from capas.capa4 import procesar as c4
        pc4 = c4(pc3)
        resultado['capas_procesadas'].append('capa4')
        nodo('capa4', 'activo')
    except Exception as e:
        resultado['respuesta'] = _fb_c3(mensaje, pc2, pc3)
        resultado['estado'] = 'parcial_capa3'
        return resultado

    # ── CAPA 5 ───────────────────────────────────────────
    try:
        emitir('procesando', 'Deliberando...')
        nodo('capa5', 'procesando')
        from capas.capa5 import procesar as c5
        pc5 = c5(pc4)
        resultado['capas_procesadas'].append('capa5')
        resultado['deliberacion'] = pc5.get('deliberacion')
        nodo('capa5', 'activo')
        if socketio and pc5.get('deliberacion'):
            socketio.emit('capa5_deliberacion', {
                'aprobado':   pc5.get('aprobado'),
                'veto':       pc5.get('veto'),
                'tono_final': pc5.get('instruccion', {}).get('tono'),
                'consejeras': len(pc5.get('deliberacion', {}).get('resultados', [])),
            })
    except Exception as e:
        resultado['respuesta'] = _fb_c4(mensaje, pc2, pc3, pc4)
        resultado['estado'] = 'parcial_capa4'
        return resultado

    # ── CAPA 6 ───────────────────────────────────────────
    try:
        emitir('procesando', 'Expresando...')
        nodo('capa6', 'procesando')
        from capas.capa6 import procesar as c6
        pc6 = c6(pc5)
        resultado['capas_procesadas'].append('capa6')
        resultado['fuente_respuesta'] = pc6.get('fuente_respuesta')
        nodo('capa6', 'activo')
    except Exception as e:
        import traceback; traceback.print_exc()
        resultado['respuesta'] = _fb_c5(pc5)
        resultado['estado'] = 'parcial_capa5'
        return resultado

    # ── CAPA 7 ───────────────────────────────────────────
    try:
        emitir('procesando', 'Ejecutando...')
        nodo('capa7', 'procesando')
        from capas.capa7 import procesar as c7
        pc7 = c7(pc6)
        resultado['capas_procesadas'].append('capa7')
        resultado['ejecucion'] = pc7.get('ejecucion')
        nodo('capa7', 'activo')
        if socketio:
            socketio.emit('capa7_ejecucion', {
                'ejecuto':    pc7.get('ejecucion', {}).get('ejecuto', False),
                'habilidad':  pc7.get('ejecucion', {}).get('habilidad_id', ''),
                'fue_a_zona': pc7.get('ejecucion', {}).get('fue_a_zona', False),
            })
    except Exception as e:
        import traceback; traceback.print_exc()
        resultado['respuesta'] = pc6.get('respuesta_final', '')
        resultado['estado']    = 'parcial_capa6'
        return resultado

    # ── CAPA 8 ───────────────────────────────────────────
    try:
        emitir('procesando', 'Finalizando...')
        nodo('capa8', 'procesando')
        from capas.capa8 import procesar as c8
        pc8 = c8(pc7)
        resultado['capas_procesadas'].append('capa8')
        resultado['tono_final'] = pc8.get('tono_final')
        nodo('capa8', 'activo')
        if socketio:
            socketio.emit('capa8_expresion', {
                'tono':     pc8.get('tono_final'),
                'tipo':     pc8.get('tipo_respuesta'),
                'longitud': pc8.get('longitud_chars'),
            })
    except Exception as e:
        import traceback; traceback.print_exc()
        resultado['respuesta'] = pc7.get('respuesta_final', '')
        resultado['estado']    = 'parcial_capa7'
        return resultado

    # ── CAPA 9 ───────────────────────────────────────────
    try:
        emitir('procesando', 'Integrando...')
        nodo('capa9', 'procesando')
        from capas.capa9 import procesar as c9
        pc9 = c9(pc8)
        resultado['capas_procesadas'].append('capa9')
        nodo('capa9', 'activo')

        # Informar si BELL_CORE se actualizó
        actualizacion = pc9.get('actualizacion', {})
        if actualizacion.get('accion', 0) > 0 or actualizacion.get('relaciones', 0) > 0:
            resultado['bell_core_actualizado'] = True
            if socketio:
                socketio.emit('bell_core_actualizado', {
                    'accion':      actualizacion.get('accion', 0),
                    'relaciones':  actualizacion.get('relaciones', 0),
                    'crecimiento': actualizacion.get('crecimiento', 0),
                    'integridad':  actualizacion.get('integridad', 0),
                    'descripcion': actualizacion.get('descripcion', ''),
                })

    except ImportError:
        resultado['respuesta'] = pc8.get('respuesta_final', '')
        resultado['estado']    = 'parcial_capa8'
        return resultado
    except Exception as e:
        import traceback; traceback.print_exc()
        resultado['respuesta'] = pc8.get('respuesta_final', '')
        resultado['estado']    = 'parcial_capa8_error_capa9'
        return resultado

    # ── RESPUESTA FINAL ──────────────────────────────────
    resultado['respuesta'] = pc9.get('respuesta_final', '')
    resultado['estado']    = 'completo'
    return resultado


# ── FALLBACKS ─────────────────────────────────────────

def _fb_c3(mensaje, pc2, pc3):
    import random
    comprension = pc3.get('comprension', {})
    nombre = comprension.get('contextual', {}).get('nombre_usuario', 'Sebastian')
    tipo   = comprension.get('contextual', {}).get('tipo_mensaje', '')
    if tipo == 'saludo':
        return random.choice([f"Hola {nombre}.", f"Aquí estoy, {nombre}."])
    if tipo == 'expresion_emocional_negativa':
        return f"Estoy aquí, {nombre}."
    return f"Recibí tu mensaje, {nombre}."


def _fb_c4(mensaje, pc2, pc3, pc4):
    import random
    comprension = pc3.get('comprension', {})
    nombre = comprension.get('contextual', {}).get('nombre_usuario', 'Sebastian')
    alternativa = pc4.get('capacidad', {}).get('alternativa', '')
    if alternativa:
        return alternativa
    return random.choice([f"Aquí estoy, {nombre}.", f"Presente, {nombre}."])


def _fb_c5(pc5):
    import random
    if pc5.get('veto'):
        return pc5.get('respuesta_directa', 'No puedo ayudarte con eso.')
    return random.choice(["Bell sigue aquí. Intenta de nuevo.", "Algo falló. Intenta de nuevo."])


def _emitir_activaciones(red_activa, socketio, resultado):
    import time
    if not socketio:
        return
    for n in red_activa.get('nodos_primarios', []):
        socketio.emit('activar_neurona', {
            'nodo_id': n.get('nodo_id', ''), 'nivel': 'primario', 'energia': n.get('energia', 1.0)
        })
    time.sleep(0.03)
    for n in red_activa.get('nodos_secundarios', []):
        socketio.emit('activar_neurona', {
            'nodo_id': n.get('nodo_id', ''), 'nivel': 'secundario', 'energia': n.get('energia', 0.7)
        })
    time.sleep(0.03)
    for n in red_activa.get('nodos_terciarios', []):
        socketio.emit('activar_neurona', {
            'nodo_id': n.get('nodo_id', ''), 'nivel': 'terciario', 'energia': n.get('energia', 0.4)
        })