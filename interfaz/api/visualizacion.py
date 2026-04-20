# interfaz/api/visualizacion.py v4
# FIX: /flujo ahora busca los IDs reales de las capas en la red
# y el helper _extraer_tipos_grounding lee el perfil correctamente

def registrar_rutas_visualizacion(app, socketio=None):

    @app.route('/api/visualizacion/estado')
    def estado_visualizacion():
        from flask import jsonify
        try:
            from biblioteca import Biblioteca
            b = Biblioteca.obtener()
            if not b:
                return jsonify({'iniciada': False})
            return jsonify({
                'iniciada':      b.iniciada,
                'consejeras_ok': b.gestor_consejeras is not None,
                'estadisticas':  b.red.obtener_estadisticas(),
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # ──────────────────────────────────────────────────────────────────
    # VISTA NEURONAL
    # ──────────────────────────────────────────────────────────────────
    @app.route('/api/visualizacion/neuronal')
    def visualizacion_neuronal():
        from flask import jsonify
        try:
            from biblioteca import Biblioteca
            b = Biblioteca.obtener()
            if not b:
                return jsonify({'disponible': False})
            datos = b.obtener_nodos_para_visualizacion()
            return jsonify({
                'disponible':       True,
                'nodos':            datos['nodos'],
                'conexiones':       datos['conexiones'],
                'total_nodos':      datos['total_nodos'],
                'total_conexiones': datos['total_conexiones'],
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # ──────────────────────────────────────────────────────────────────
    # VISTA VIDA
    # ──────────────────────────────────────────────────────────────────
    @app.route('/api/visualizacion/vida')
    def visualizacion_vida():
        from flask import jsonify
        try:
            from biblioteca import Biblioteca
            b = Biblioteca.obtener()
            if not b:
                return jsonify({'disponible': False})

            COLORES_NIVEL = {
                'plena':     '#00FF88',
                'rica':      '#44FFAA',
                'funcional': '#88FFCC',
                'emergente': '#AAFFDD',
                'latente':   '#FFD700',
                'dormida':   '#334455',
            }

            estadisticas = {
                'plena': 0, 'rica': 0, 'funcional': 0,
                'emergente': 0, 'latente': 0, 'dormida': 0,
                'vitalidad_promedio': 0.0,
            }
            nodos_vida     = []
            suma_vitalidad = 0.0

            todos_ids = list(b.red.obtener_todos_los_nodos().keys())

            for nodo_id in todos_ids:
                # Leer neurona REAL para obtener datos_extra
                neurona = b.red.obtener_neurona(nodo_id)
                if not neurona:
                    continue

                nucleo    = neurona.nucleo
                datos_ext = {}
                if hasattr(nucleo, 'datos_extra') and isinstance(nucleo.datos_extra, dict):
                    datos_ext = nucleo.datos_extra

                vitalidad  = float(datos_ext.get('vitalidad',  0.0))
                nivel_vida = datos_ext.get('nivel_vida', 'dormida')
                perfil_res = datos_ext.get('perfil_vida', {})

                tipos_grounding = _extraer_tipos_grounding(perfil_res)
                color_vida      = COLORES_NIVEL.get(nivel_vida, '#334455')
                brilla          = nivel_vida not in ('dormida', 'latente') and vitalidad > 0.3

                nodos_vida.append({
                    'id':                 nodo_id,
                    'nombre':             b._nombre_legible(nodo_id),
                    'tipo':               getattr(nucleo, 'tipo', 'concepto'),
                    'vitalidad':          round(vitalidad, 4),
                    'nivel_vida':         nivel_vida,
                    'color_vida':         color_vida,
                    'brilla':             brilla,
                    'tipos_grounding':    tipos_grounding,
                    'grounding_efectivo': getattr(nucleo, 'grounding_base', 0.5),
                    'perfil_resumen':     perfil_res,
                })

                suma_vitalidad += vitalidad
                if nivel_vida in estadisticas:
                    estadisticas[nivel_vida] += 1

            if nodos_vida:
                estadisticas['vitalidad_promedio'] = round(
                    suma_vitalidad / len(nodos_vida), 4
                )

            total_vivos = sum(
                1 for n in nodos_vida if n['nivel_vida'] != 'dormida'
            )

            return jsonify({
                'disponible':   True,
                'nodos':        nodos_vida,
                'total_nodos':  len(nodos_vida),
                'total_vivos':  total_vivos,
                'estadisticas': estadisticas,
            })

        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({'error': str(e)}), 500

    # ──────────────────────────────────────────────────────────────────
    # VISTA FLUJO — IDs reales de la red
    # ──────────────────────────────────────────────────────────────────
    @app.route('/api/visualizacion/flujo')
    def visualizacion_flujo():
        from flask import jsonify
        try:
            from biblioteca import Biblioteca
            b = Biblioteca.obtener()
            if not b:
                return jsonify({'disponible': False})

            # Posibles IDs de capa en la red — buscar cuáles existen
            # El cargador fundacional crea neuronas con IDs como
            # CAPA_1_RECEPCION, CAPA1, CAPA_RECEPCION, etc.
            # Buscamos por patrones en todos los nodos
            todos_ids = list(b.red.obtener_todos_los_nodos().keys())

            # Mapeo de capas esperadas a sus posibles IDs en la red
            capas_config = [
                {'num': 1, 'nombre': 'Recepcion',   'keywords': ['CAPA_1', 'CAPA1', 'RECEPCION']},
                {'num': 2, 'nombre': 'Activacion',  'keywords': ['CAPA_2', 'CAPA2', 'ACTIVACION']},
                {'num': 3, 'nombre': 'Comprension', 'keywords': ['CAPA_3', 'CAPA3', 'COMPRENSION']},
                {'num': 4, 'nombre': 'Evaluacion',  'keywords': ['CAPA_4', 'CAPA4', 'EVALUACION']},
                {'num': 5, 'nombre': 'Deliberacion','keywords': ['CAPA_5', 'CAPA5', 'DELIBERACION']},
                {'num': 6, 'nombre': 'Decision',    'keywords': ['CAPA_6', 'CAPA6', 'DECISION']},
                {'num': 7, 'nombre': 'Ejecucion',   'keywords': ['CAPA_7', 'CAPA7', 'EJECUCION']},
                {'num': 8, 'nombre': 'Expresion',   'keywords': ['CAPA_8', 'CAPA8', 'EXPRESION']},
                {'num': 9, 'nombre': 'Integracion', 'keywords': ['CAPA_9', 'CAPA9', 'INTEGRACION']},
            ]

            nodos_flujo = []
            for cfg in capas_config:
                # Buscar el ID real en la red
                id_real = None
                for nid in todos_ids:
                    nid_upper = nid.upper()
                    if any(kw in nid_upper for kw in cfg['keywords']):
                        id_real = nid
                        break

                # Si no encontramos el ID real, usar uno genérico
                if not id_real:
                    id_real = f'capa{cfg["num"]}'

                neurona = b.red.obtener_neurona(id_real) if id_real else None
                estado  = 'inactivo' if neurona else 'pendiente'
                vita    = 0.0
                nivel   = 'dormida'

                if neurona:
                    datos_ext = {}
                    if hasattr(neurona.nucleo, 'datos_extra'):
                        datos_ext = neurona.nucleo.datos_extra or {}
                    vita  = float(datos_ext.get('vitalidad',  0.0))
                    nivel = datos_ext.get('nivel_vida', 'dormida')

                nodos_flujo.append({
                    'id':        id_real,
                    'nombre':    f'Capa {cfg["num"]} {cfg["nombre"]}',
                    'estado':    estado,
                    'vitalidad': vita,
                    'nivel_vida': nivel,
                })

            return jsonify({'disponible': True, 'capas': nodos_flujo})

        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({'error': str(e)}), 500


# ──────────────────────────────────────────────────────────────────────
# HELPER
# ──────────────────────────────────────────────────────────────────────
def _extraer_tipos_grounding(perfil_resumen: dict) -> list:
    """
    Del resumen del PerfilVida, extrae los tipos de grounding
    que tienen al menos una dimensión con valor > 0.1.
    El resumen es un dict {tipo: {dim: valor, ...}} o {tipo: valor}.
    """
    if not isinstance(perfil_resumen, dict):
        return []
    tipos = []
    for tipo, dims in perfil_resumen.items():
        if tipo in ('organismo_id', 'tipo_organismo', 'vitalidad_total',
                    'nivel_vida', 'timestamp'):
            continue
        if isinstance(dims, dict):
            if any(
                isinstance(v, (int, float)) and v > 0.1
                for v in dims.values()
            ):
                tipos.append(tipo)
        elif isinstance(dims, (int, float)) and dims > 0.1:
            tipos.append(tipo)
    return tipos