# interfaz/api/chat.py
# ================================================
# CHAT — Capas 1-9 + Voz automática
#
# Después de cada respuesta, si la voz está activa,
# Bell habla por el Nest Mini automáticamente.
#
# LOGS:
#   Sin variable:   solo errores
#   BELL_DEBUG=1:   flujo completo por mensaje
# ================================================

import os
from flask import request, jsonify
from flask_socketio import emit

_DEBUG = os.getenv('BELL_DEBUG', '0') == '1'


def _log(msg: str):
    if _DEBUG:
        print(f'  {msg}')


def _error(capa: str, descripcion: str, exc: Exception = None):
    causa = f'\n    Causa: {type(exc).__name__}: {exc}' if exc else ''
    print(f'\n❌ [{capa}] {descripcion}{causa}\n')
    if exc and _DEBUG:
        import traceback
        traceback.print_exc()


def _hablar(texto: str):
    """Envía la respuesta al Nest Mini si la voz está activa."""
    try:
        from interfaz.api.voz import GestorVoz
        GestorVoz.obtener().hablar(texto)
    except Exception:
        pass


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
        'mensaje_original':      mensaje,
        'capas_procesadas':      [],
        'respuesta':             None,
        'estado':                'incompleto',
        'red_activa':            {},
        'activaciones':          [],
        'deliberacion':          None,
        'fuente_respuesta':      None,
        'ejecucion':             None,
        'tono_final':            None,
        'bell_core_actualizado': False,
    }

    def emitir(estado, texto):
        if socketio:
            socketio.emit('estado_bell', {'estado': estado, 'texto': texto})

    def nodo(nodo_id, estado):
        if socketio:
            socketio.emit('actualizar_nodo', {'nodo_id': nodo_id, 'estado': estado})
        resultado['activaciones'].append({'nodo_id': nodo_id, 'estado': estado})

    if _DEBUG:
        print(f'\n{"─"*60}')
        print(f'📨 "{mensaje}"')
        print(f'{"─"*60}')

    # ── CAPA 1 ───────────────────────────────────────────
    try:
        emitir('procesando', 'Traduciendo...')
        nodo('capa1', 'procesando')
        from capas.capa1 import procesar as c1
        pc1 = c1(mensaje)
        resultado['capas_procesadas'].append('capa1')
        nodo('capa1', 'activo')
        conceptos = [(c.get('id','') if isinstance(c,dict) else getattr(c,'id','')) for c in pc1.get('conceptos', [])]
        descono   = [(d.get('fragmento','') if isinstance(d,dict) else getattr(d,'fragmento','')) for d in pc1.get('desconocidos', [])]
        _log(f'C1 conceptos: {conceptos}')
        if descono: _log(f'C1 desconocidos→zona: {descono}')
    except Exception as e:
        _error('CAPA 1', 'No pudo traducir el mensaje a conceptos de Bell', e)
        resultado['respuesta'] = f'Error Capa 1: {e}'
        resultado['estado']    = 'error'
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
        red = pc2.get('red_activa', {})
        _log(f'C2 nodos_primarios: {[n.get("nodo_id","") for n in red.get("nodos_primarios",[])]}')
        _log(f'C2 total_activados: {red.get("total_activados", 0)}')
    except Exception as e:
        _error('CAPA 2', 'No pudo activar la red neuronal', e)
        resultado['respuesta'] = f'Error Capa 2: {e}'
        resultado['estado']    = 'error'
        return resultado

    # ── CAPA 3 ───────────────────────────────────────────
    try:
        emitir('procesando', 'Comprendiendo...')
        nodo('capa3', 'procesando')
        from capas.capa3 import procesar as c3
        pc3 = c3(pc2)
        resultado['capas_procesadas'].append('capa3')
        nodo('capa3', 'activo')
        comp = pc3.get('comprension', {})
        ctx  = comp.get('contextual', {})
        pro  = comp.get('profunda', {})
        _log(f'C3 tipo_mensaje:  {ctx.get("tipo_mensaje","?")}')
        _log(f'C3 emocion:       {pro.get("emocion_detectada","?")}')
        _log(f'C3 intencion:     {pro.get("intencion_detectada","?")}')
        _log(f'C3 necesidad:     {pro.get("necesidad_real","?")}')
        if pro.get('estado_subyacente'): _log(f'C3 estado_sub: {pro["estado_subyacente"]}')
        if pro.get('habilidad_requerida'): _log(f'C3 habilidad_req: {pro["habilidad_requerida"]}')
    except ImportError as e:
        _error('CAPA 3', 'Módulo no encontrado', e)
        resultado['respuesta'] = 'Capa 3 no disponible.'
        resultado['estado']    = 'parcial_capa2'
        return resultado
    except Exception as e:
        _error('CAPA 3', 'No pudo construir comprensión', e)
        resultado['respuesta'] = f'Error Capa 3: {e}'
        resultado['estado']    = 'error'
        return resultado

    # ── CAPA 4 ───────────────────────────────────────────
    try:
        emitir('procesando', 'Evaluando...')
        nodo('capa4', 'procesando')
        from capas.capa4 import procesar as c4
        pc4 = c4(pc3)
        resultado['capas_procesadas'].append('capa4')
        nodo('capa4', 'activo')
        _log(f'C4 riesgo:    {pc4.get("evaluacion_riesgo",{}).get("nivel","?")}')
        _log(f'C4 capacidad: {pc4.get("evaluacion_capacidad",{}).get("puede","?")}')
    except Exception as e:
        _error('CAPA 4', 'Fallo en evaluación — fallback C3', e)
        resultado['respuesta'] = _fb_c3(mensaje, pc2, pc3)
        resultado['estado']    = 'parcial_capa3'
        _hablar(resultado['respuesta'])
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
        delib = pc5.get('deliberacion', {}) or {}
        tono  = pc5.get('instruccion', {}).get('tono', '?')
        veto  = pc5.get('veto', False)
        _log(f'C5 tono: {tono} | veto: {veto}')
        if delib.get('recomendacion_sage'): _log(f'C5 sage: "{delib["recomendacion_sage"][:60]}"')
        if socketio and pc5.get('deliberacion'):
            socketio.emit('capa5_deliberacion', {
                'aprobado': pc5.get('aprobado'), 'veto': veto,
                'tono_final': tono, 'consejeras': len(delib.get('resultados', [])),
            })
    except Exception as e:
        _error('CAPA 5', 'Fallo en deliberación — fallback C4', e)
        resultado['respuesta'] = _fb_c4(mensaje, pc2, pc3, pc4)
        resultado['estado']    = 'parcial_capa4'
        _hablar(resultado['respuesta'])
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
        dec    = pc6.get('decision') or {}
        base   = dec.get('respuesta_base', '')[:80] if dec else ''
        fuente = pc6.get('fuente_respuesta', '?')
        final6 = pc6.get('respuesta_final', '')[:80]
        _log(f'C6 respuesta_base:  "{base}"')
        _log(f'C6 fuente:          {fuente}')
        _log(f'C6 respuesta_final: "{final6}"')
    except Exception as e:
        _error('CAPA 6', 'Fallo al construir respuesta — fallback C5', e)
        resultado['respuesta'] = _fb_c5(pc5)
        resultado['estado']    = 'parcial_capa5'
        _hablar(resultado['respuesta'])
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
        ejec = pc7.get('ejecucion') or {}
        _log(f'C7 habilidad: {ejec.get("habilidad_id","ninguna")} | ejecuto: {ejec.get("ejecuto",False)}')
        if socketio:
            socketio.emit('capa7_ejecucion', {
                'ejecuto': ejec.get('ejecuto',False),
                'habilidad': ejec.get('habilidad_id','ninguna'),
                'fue_a_zona': ejec.get('fue_a_zona',False),
            })
    except Exception as e:
        _error('CAPA 7', 'Fallo en ejecución — usando C6', e)
        resultado['respuesta'] = pc6.get('respuesta_final', '')
        resultado['estado']    = 'parcial_capa6'
        _hablar(resultado['respuesta'])
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
        _log(f'C8 tono_final: {pc8.get("tono_final","?")}')
        if socketio:
            socketio.emit('capa8_expresion', {
                'tono': pc8.get('tono_final'), 'tipo': pc8.get('tipo_respuesta'),
                'longitud': pc8.get('longitud_chars'),
            })
    except Exception as e:
        _error('CAPA 8', 'Fallo en formato — usando C7', e)
        resultado['respuesta'] = pc7.get('respuesta_final', '')
        resultado['estado']    = 'parcial_capa7'
        _hablar(resultado['respuesta'])
        return resultado

    # ── CAPA 9 ───────────────────────────────────────────
    try:
        emitir('procesando', 'Integrando...')
        nodo('capa9', 'procesando')
        from capas.capa9 import procesar as c9
        pc9 = c9(pc8)
        resultado['capas_procesadas'].append('capa9')
        nodo('capa9', 'activo')
        act = pc9.get('actualizacion', {}) or {}
        if act.get('accion', 0) > 0 or act.get('relaciones', 0) > 0:
            resultado['bell_core_actualizado'] = True
            _log(f'C9 BELL_CORE: accion={act.get("accion",0):.3f}')
            if socketio:
                socketio.emit('bell_core_actualizado', {
                    'accion': act.get('accion',0), 'relaciones': act.get('relaciones',0),
                    'crecimiento': act.get('crecimiento',0), 'integridad': act.get('integridad',0),
                    'descripcion': act.get('descripcion',''),
                })
    except Exception as e:
        _error('CAPA 9', 'Fallo en integración — usando C8', e)
        resultado['respuesta'] = pc8.get('respuesta_final', '')
        resultado['estado']    = 'parcial_capa8_error_capa9'
        _hablar(resultado['respuesta'])
        return resultado

    # ── FINAL ────────────────────────────────────────────
    resultado['respuesta'] = pc9.get('respuesta_final', '')
    resultado['estado']    = 'completo'

    # Hablar por el Nest Mini automáticamente
    _hablar(resultado['respuesta'])

    if _DEBUG:
        print(f'✅ "{resultado["respuesta"]}"')
        fuente = resultado.get('fuente_respuesta','?')
        print(f'   fuente: {fuente}')
        print(f'{"─"*60}\n')

    return resultado


# ── FALLBACKS ─────────────────────────────────────────────

def _fb_c3(mensaje, pc2, pc3):
    import random
    comp   = pc3.get('comprension', {})
    nombre = comp.get('contextual', {}).get('nombre_usuario', 'Sebastian')
    tipo   = comp.get('contextual', {}).get('tipo_mensaje', '')
    if tipo == 'saludo': return random.choice([f"Hola {nombre}.", f"Aquí estoy."])
    if tipo == 'expresion_emocional_negativa': return f"Estoy aquí, {nombre}."
    return f"Aquí estoy, {nombre}."

def _fb_c4(mensaje, pc2, pc3, pc4):
    import random
    comp   = pc3.get('comprension', {})
    nombre = comp.get('contextual', {}).get('nombre_usuario', 'Sebastian')
    alt    = pc4.get('capacidad', {}).get('alternativa', '')
    return alt or random.choice([f"Aquí estoy, {nombre}.", f"Presente."])

def _fb_c5(pc5):
    import random
    if pc5.get('veto'): return pc5.get('respuesta_directa', 'No puedo ayudarte con eso.')
    return random.choice(["Bell sigue aquí. Intenta de nuevo.", "Algo falló. Intenta de nuevo."])

def _emitir_activaciones(red_activa, socketio, resultado):
    import time
    if not socketio: return
    for n in red_activa.get('nodos_primarios', []):
        socketio.emit('activar_neurona', {'nodo_id': n.get('nodo_id',''), 'nivel': 'primario', 'energia': n.get('energia', 1.0)})
    time.sleep(0.03)
    for n in red_activa.get('nodos_secundarios', []):
        socketio.emit('activar_neurona', {'nodo_id': n.get('nodo_id',''), 'nivel': 'secundario', 'energia': n.get('energia', 0.7)})
    time.sleep(0.03)
    for n in red_activa.get('nodos_terciarios', []):
        socketio.emit('activar_neurona', {'nodo_id': n.get('nodo_id',''), 'nivel': 'terciario', 'energia': n.get('energia', 0.4)})