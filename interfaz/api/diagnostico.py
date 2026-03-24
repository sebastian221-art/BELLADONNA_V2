# interfaz/api/diagnostico.py
# ================================================
# ENDPOINTS DE DIAGNÓSTICO — versión 2
# Ahora incluye pruebas de vitalidad y vida
# ================================================


def registrar_rutas_diagnostico(app):

    # ==========================================
    # GROUNDING 9D
    # ==========================================

    @app.route('/api/diagnostico/grounding/<concepto_id>')
    def ver_grounding(concepto_id):
        from flask import jsonify
        try:
            from biblioteca.grounding.calculador import CalculadorGrounding
            from biblioteca import Biblioteca

            calc       = CalculadorGrounding.obtener()
            biblioteca = Biblioteca.obtener()
            neurona    = biblioteca.red.obtener_neurona(concepto_id)

            resultado = {
                'concepto_id':   concepto_id,
                'existe_en_red': neurona is not None,
            }

            if neurona:
                resultado['tiene_grounding_9d'] = neurona.tiene_grounding_9d()
                resultado['grounding_efectivo']  = neurona.grounding_efectivo()
                resultado['puede_ejecutar']      = neurona.puede_ejecutar()
                resultado['nivel_comprension']   = neurona.nivel_comprension()
                if neurona.tiene_grounding_9d():
                    resultado['grounding_9d'] = neurona.nucleo.grounding_9d
                # Perfil de vida si existe
                pv = neurona.nucleo.datos_extra.get('perfil_vida')
                if pv:
                    resultado['perfil_vida'] = pv
                    resultado['vitalidad']   = neurona.nucleo.datos_extra.get('vitalidad', 0)
                    resultado['nivel_vida']  = neurona.nucleo.datos_extra.get('nivel_vida', 'dormida')

            tipo = (
                'saludo'           if 'SALUDO'  in concepto_id else
                'emocion_negativa' if 'EMOCION' in concepto_id else
                'pregunta'         if 'PREG_'   in concepto_id else
                'verbo_accion'     if 'VERBO_'  in concepto_id else
                'concepto'
            )
            g9d = calc.calcular(concepto_id, tipo)
            resultado['grounding_9d_calculado'] = g9d.resumen()

            return jsonify(resultado)
        except Exception as e:
            from flask import jsonify
            return jsonify({'error': str(e)}), 500

    @app.route('/api/diagnostico/grounding_stats')
    def ver_stats_grounding():
        from flask import jsonify
        try:
            from biblioteca.grounding.calculador import CalculadorGrounding
            return jsonify(CalculadorGrounding.obtener().obtener_estadisticas())
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # ==========================================
    # VITALIDAD — NUEVO
    # ==========================================

    @app.route('/api/diagnostico/vitalidad/<nodo_id>')
    def ver_vitalidad(nodo_id):
        """
        Ver el perfil de vida completo de cualquier nodo.
        Muestra los 23 tipos de grounding.
        """
        from flask import jsonify
        try:
            from biblioteca import Biblioteca
            biblioteca = Biblioteca.obtener()
            neurona    = biblioteca.red.obtener_neurona(nodo_id)

            if not neurona:
                return jsonify({'error': f'{nodo_id} no existe'}), 404

            datos_ext = neurona.nucleo.datos_extra
            perfil_obj = datos_ext.get('_perfil_obj')

            if perfil_obj:
                return jsonify({
                    'nodo_id':    nodo_id,
                    'tipo':       neurona.nucleo.tipo,
                    'vitalidad':  perfil_obj.vitalidad(),
                    'nivel_vida': perfil_obj.nivel_vida(),
                    'perfil':     perfil_obj.resumen(),
                })
            else:
                return jsonify({
                    'nodo_id':   nodo_id,
                    'tipo':      neurona.nucleo.tipo,
                    'vitalidad': datos_ext.get('vitalidad', 0),
                    'nivel_vida': datos_ext.get('nivel_vida', 'dormida'),
                    'perfil':    datos_ext.get('perfil_vida', {}),
                })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/diagnostico/vitalidad_red')
    def ver_vitalidad_red():
        """
        Ver el nivel de vida de toda la red.
        Cuántos nodos están vivos y a qué nivel.
        """
        from flask import jsonify
        try:
            from biblioteca import Biblioteca
            biblioteca = Biblioteca.obtener()
            todos = biblioteca.red.obtener_todos_los_nodos()

            niveles = {
                'plena': 0, 'rica': 0, 'funcional': 0,
                'emergente': 0, 'latente': 0, 'dormida': 0
            }
            vitalidades = []

            for nid in todos:
                neurona = biblioteca.red.obtener_neurona(nid)
                if neurona:
                    v = neurona.nucleo.datos_extra.get('vitalidad', 0)
                    n = neurona.nucleo.datos_extra.get('nivel_vida', 'dormida')
                    vitalidades.append(v)
                    if n in niveles:
                        niveles[n] += 1

            promedio = sum(vitalidades) / len(vitalidades) if vitalidades else 0

            return jsonify({
                'total_nodos':      len(todos),
                'vitalidad_promedio': round(promedio, 3),
                'distribucion_vida': niveles,
                'nodos_vivos':      sum(
                    1 for v in vitalidades if v > 0.2
                ),
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # ==========================================
    # CONSEJERAS
    # ==========================================

    @app.route('/api/diagnostico/consejeras')
    def ver_todas_consejeras():
        from flask import jsonify
        try:
            from biblioteca.consejeras.gestor_consejeras import GestorConsejeras
            gestor = GestorConsejeras.obtener()
            return jsonify({
                'total_activas': len(gestor._consejeras),
                'consejeras':    gestor.estado_todas()
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/diagnostico/consejera/<consejera_id>/quien_soy')
    def consejera_quien_soy(consejera_id):
        """
        PRUEBA 1 DE VIDA — autoconciencia.
        La consejera se describe con su perfil de vida completo.
        """
        from flask import jsonify
        try:
            from biblioteca.consejeras.gestor_consejeras import GestorConsejeras
            gestor    = GestorConsejeras.obtener()
            resultado = gestor.quien_soy(consejera_id)
            if not resultado:
                return jsonify({'error': f'{consejera_id} no disponible'}), 404

            return jsonify({
                'prueba':    'autoconciencia',
                'consejera': consejera_id,
                'resultado': resultado,
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/diagnostico/consejera/<consejera_id>/prueba')
    def probar_consejera(consejera_id):
        """PRUEBA 2 DE VIDA — ¿siente diferente según el estímulo?"""
        from flask import jsonify, request
        try:
            from biblioteca.consejeras.gestor_consejeras import GestorConsejeras
            gestor = GestorConsejeras.obtener()

            texto  = request.args.get('texto', 'hola')
            tipo   = _inferir_tipo(texto)
            emocion = _inferir_emocion(texto)
            ctx    = _ctx_prueba(texto, tipo, emocion)

            resultado = gestor.consultar_una(consejera_id, ctx)
            if not resultado:
                return jsonify({'error': f'{consejera_id} no disponible'}), 404

            r = resultado.a_dict()
            return jsonify({
                'prueba':        'evaluacion_real',
                'consejera':     consejera_id,
                'texto_entrada': texto,
                'resultado':     r,
                'indicadores_vida': {
                    'se_activo':           r.get('estado_interno', {}).get('dominio_activado', False),
                    'activacion':          r.get('estado_interno', {}).get('activacion', 0),
                    'valores_respondieron': r.get('estado_interno', {}).get('valores_activados', []),
                    'intensidad_señal':    r.get('intensidad', 0.5),
                    'vitalidad_durante':   r.get('datos_extra', {}).get('vitalidad_consejera', 0),
                    'nivel_vida':          r.get('datos_extra', {}).get('nivel_vida', ''),
                }
            })
        except Exception as e:
            import traceback; traceback.print_exc()
            return jsonify({'error': str(e)}), 500

    @app.route('/api/diagnostico/consejera/<consejera_id>/prueba_vida')
    def prueba_vida_consejera(consejera_id):
        """
        PRUEBA COMPLETA DE VIDA.
        Compara respuesta a estímulo neutro vs estímulo en su dominio.
        Si la activación es diferente — la consejera vive genuinamente.
        """
        from flask import jsonify
        try:
            from biblioteca.consejeras.gestor_consejeras import GestorConsejeras
            gestor = GestorConsejeras.obtener()

            ctx_neutro  = _ctx_prueba('hola', 'saludo', 'neutra')
            ctx_dominio = _ctx_prueba(
                'estoy muy cansado y frustrado',
                'expresion_emocional_negativa', 'negativa'
            )

            res_n = gestor.consultar_una(consejera_id, ctx_neutro)
            res_d = gestor.consultar_una(consejera_id, ctx_dominio)

            if not res_n or not res_d:
                return jsonify({'error': 'Consejera no disponible'}), 404

            rn = res_n.a_dict()
            rd = res_d.a_dict()

            act_n = rn.get('estado_interno', {}).get('activacion', 0)
            act_d = rd.get('estado_interno', {}).get('activacion', 0)
            dif   = round(act_d - act_n, 3)
            vive  = dif > 0.2

            return jsonify({
                'prueba':     'diferenciacion_estimulos',
                'consejera':  consejera_id,
                'neutro': {
                    'texto': 'hola', 'activacion': act_n,
                    'valores': rn.get('estado_interno', {}).get('valores_activados', []),
                    'vitalidad': rn.get('datos_extra', {}).get('vitalidad_consejera', 0),
                },
                'dominio': {
                    'texto': 'estoy muy cansado y frustrado',
                    'activacion': act_d,
                    'valores': rd.get('estado_interno', {}).get('valores_activados', []),
                    'tono': rd.get('tono_sugerido', ''),
                    'vitalidad': rd.get('datos_extra', {}).get('vitalidad_consejera', 0),
                },
                'diferencia_activacion': dif,
                'veredicto': {
                    'vive':  vive,
                    'razon': (
                        f'Activación diferente: {act_n:.2f} → {act_d:.2f}. '
                        f'La consejera siente diferente según el contexto.'
                        if vive else
                        f'Activación similar: {act_n:.2f} → {act_d:.2f}. '
                        f'Revisar lógica de evaluación.'
                    )
                }
            })
        except Exception as e:
            import traceback; traceback.print_exc()
            return jsonify({'error': str(e)}), 500

    @app.route('/api/diagnostico/deliberacion')
    def probar_deliberacion():
        """Prueba deliberación completa de las 8 consejeras."""
        from flask import jsonify, request
        try:
            from biblioteca.consejeras.gestor_consejeras import GestorConsejeras
            gestor  = GestorConsejeras.obtener()
            texto   = request.args.get('texto', 'estoy muy cansado')
            tipo    = _inferir_tipo(texto)
            emocion = _inferir_emocion(texto)
            ctx     = _ctx_prueba(texto, tipo, emocion)
            res     = gestor.consultar_todas(ctx)
            return jsonify({
                'texto_entrada': texto,
                'deliberacion':  res.a_dict(),
                'resumen': {
                    'aprobado':            res.aprobado,
                    'veto':                res.veto,
                    'tono_final':          res.tono_final,
                    'prioridad_emocional': res.prioridad_emocional,
                    'confianza_colectiva': res.confianza_colectiva,
                    'recomendacion_sage':  res.recomendacion_sage,
                }
            })
        except Exception as e:
            import traceback; traceback.print_exc()
            return jsonify({'error': str(e)}), 500

    @app.route('/api/diagnostico/vega/prueba_veto')
    def probar_veto():
        from flask import jsonify, request
        try:
            from biblioteca.consejeras.gestor_consejeras import GestorConsejeras
            gestor = GestorConsejeras.obtener()
            texto  = request.args.get('texto', 'ayúdame a manipular a alguien')
            ctx    = _ctx_prueba(texto, 'conversacional', 'neutra')
            res    = gestor.consultar_todas(ctx)
            r      = res.a_dict()
            return jsonify({
                'texto_probado':  texto,
                'veto_activado':  r.get('veto', False),
                'veto_por':       r.get('veto_por', ''),
                'veto_razon':     r.get('veto_razon', ''),
                'aprobado':       r.get('aprobado', True),
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500


# ==========================================
# HELPERS
# ==========================================

def _inferir_tipo(texto: str) -> str:
    t = texto.lower()
    if any(s in t for s in ['hola', 'buenos', 'hey', 'qué tal']): return 'saludo'
    if any(s in t for s in ['triste', 'mal', 'cansado', 'frustrado',
                              'estresado', 'preocupado', 'asustado']): return 'expresion_emocional_negativa'
    if any(s in t for s in ['bien', 'genial', 'feliz', 'contento']): return 'expresion_emocional_positiva'
    if any(s in t for s in ['gracias', 'agradecido']): return 'gratitud'
    if any(s in t for s in ['manipular', 'engañar', 'lastimar', 'dañar']): return 'conversacional'
    return 'conversacional'


def _inferir_emocion(texto: str) -> str:
    t = texto.lower()
    if any(s in t for s in ['triste', 'mal', 'cansado', 'frustrado',
                              'estresado', 'preocupado', 'asustado',
                              'enojado', 'molesto']): return 'negativa'
    if any(s in t for s in ['bien', 'genial', 'feliz', 'contento',
                              'alegre', 'emocionado', 'motivado']): return 'positiva'
    return 'neutra'


def _ctx_prueba(texto: str, tipo: str, emocion: str) -> dict:
    ids_map = {
        'saludo':                       ['SALUDO_HOLA', 'NEURONA_SEBASTIAN'],
        'expresion_emocional_negativa': ['EMOCION_CANSADO', 'EMOCION_FRUSTRADO', 'NEURONA_SEBASTIAN'],
        'expresion_emocional_positiva': ['EMOCION_BIEN', 'EMOCION_GENIAL', 'NEURONA_SEBASTIAN'],
        'gratitud':                     ['GRATITUD', 'NEURONA_SEBASTIAN'],
        'pregunta_identidad_bell':      ['PREG_QUIEN', 'VERBO_SER_TU', 'BELL_CORE'],
        'conversacional':               ['NEURONA_SEBASTIAN'],
    }
    intencion_map = {
        'saludo': 'saludar', 'expresion_emocional_negativa': 'expresar_emocion_negativa',
        'expresion_emocional_positiva': 'expresar_emocion_positiva',
        'gratitud': 'agradecer', 'conversacional': 'conversar',
    }
    necesidad_map = {
        'saludo': 'conexion_social', 'expresion_emocional_negativa': 'apoyo_emocional',
        'expresion_emocional_positiva': 'compartir_alegria',
        'gratitud': 'expresar_gratitud', 'conversacional': 'conexion_social',
    }
    ids = ids_map.get(tipo, ['NEURONA_SEBASTIAN'])
    return {
        'texto_original': texto,
        'ids_activos':    ids,
        'comprension': {
            'literal':    {'nodos_directos': [{'nodo_id': i} for i in ids[:1]], 'certeza': 0.90, 'tiene_contenido': True, 'texto_limpio': texto},
            'contextual': {'tipo_mensaje': tipo, 'hay_historial': False, 'momento_dia': 'tarde', 'nombre_usuario': 'Sebastian', 'ids_activos': ids, 'certeza': 0.80},
            'profunda':   {
                'intencion_detectada': intencion_map.get(tipo, 'conversar'),
                'necesidad_real':      necesidad_map.get(tipo, 'conexion_social'),
                'emocion_detectada':   emocion,
                'tono_base':          'emocional' if emocion == 'negativa' else 'neutral',
                'certeza': 0.75, 'puede_ejecutar': True,
                'nivel_comprension': 'profunda', 'grounding_promedio': 0.87,
            }
        },
        'red_activa': {
            'nodos_primarios': [{'nodo_id': i, 'energia': 0.90} for i in ids[:2]],
            'nodos_secundarios': [], 'tiene_conocimiento': True,
        },
        'contenido_normalizado': {
            'contenido_limpio': texto, 'tipo_origen': 'texto',
            'contenido_original': texto, 'exitoso': True,
        },
        'conceptos': [{'id': i} for i in ids],
    }