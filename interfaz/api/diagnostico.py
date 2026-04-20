# interfaz/api/diagnostico.py v8
# ================================================
# DIAGNÓSTICO — con verificación de Capa 9
# ================================================


def registrar_rutas_diagnostico(app):

    # ── VIDA REAL ─────────────────────────────────────────
    @app.route('/api/diagnostico/vida_real')
    def vida_real():
        from flask import jsonify
        try:
            from biblioteca import Biblioteca
            b = Biblioteca.obtener()
            todos = list(b.red.obtener_todos_los_nodos().keys())
            dist  = {'plena':[],'rica':[],'funcional':[],'emergente':[],'latente':[],'dormida':[]}
            suma  = 0.0
            for nid in todos:
                n = b.red.obtener_neurona(nid)
                if not n: continue
                de = getattr(n.nucleo,'datos_extra',{}) or {}
                v  = float(de.get('vitalidad',0.0))
                lv = de.get('nivel_vida','dormida')
                suma += v
                if lv in dist:
                    dist[lv].append({'id':nid,'tipo':getattr(n.nucleo,'tipo','?'),'vitalidad':round(v,4)})
            total = len(todos)
            vivos = sum(len(dist[x]) for x in ('plena','rica','funcional','emergente','latente'))
            return jsonify({
                'resumen': {
                    'total_nodos':total,'nodos_vivos':vivos,
                    'nodos_dormidos':len(dist['dormida']),
                    'vitalidad_promedio':round(suma/total,4) if total else 0,
                    'bell_esta_viva': vivos > total * 0.3,
                },
                'distribucion':{
                    lv:{'cantidad':len(ns),'nodos':sorted(ns,key=lambda x:-x['vitalidad'])[:15]}
                    for lv,ns in dist.items()
                },
            })
        except Exception as e:
            from flask import jsonify
            return jsonify({'error':str(e)}),500

    # ── NODO ──────────────────────────────────────────────
    @app.route('/api/diagnostico/nodo/<nodo_id>')
    def ver_nodo(nodo_id):
        from flask import jsonify
        try:
            from biblioteca import Biblioteca
            b = Biblioteca.obtener()
            n = b.red.obtener_neurona(nodo_id)
            if not n: return jsonify({'error':f'{nodo_id} no existe'}),404
            de = getattr(n.nucleo,'datos_extra',{}) or {}
            pv = de.get('perfil_vida',{})
            v  = float(de.get('vitalidad',0.0))
            lv = de.get('nivel_vida','dormida')
            tipos = pv.get('tipos',{})
            return jsonify({
                'id':nodo_id,'tipo':getattr(n.nucleo,'tipo','?'),
                'vitalidad':round(v,4),'nivel_vida':lv,
                'dimensiones':tipos,
            })
        except Exception as e:
            from flask import jsonify
            return jsonify({'error':str(e)}),500

    # ── CONSEJERAS ────────────────────────────────────────
    @app.route('/api/diagnostico/consejeras/comparar')
    def comparar_consejeras():
        from flask import jsonify
        try:
            from biblioteca import Biblioteca
            b = Biblioteca.obtener()
            ids = ['CONSEJERA_SOMA','CONSEJERA_VEGA','CONSEJERA_NOVA','CONSEJERA_ECHO',
                   'CONSEJERA_LYRA','CONSEJERA_LUNA','CONSEJERA_IRIS','CONSEJERA_SAGE']
            res = []
            for cid in ids:
                n = b.red.obtener_neurona(cid)
                if not n:
                    res.append({'id':cid,'existe':False}); continue
                de = getattr(n.nucleo,'datos_extra',{}) or {}
                v  = float(de.get('vitalidad',0.0))
                lv = de.get('nivel_vida','dormida')
                res.append({'id':cid,'nombre':cid.replace('CONSEJERA_','').title(),'existe':True,'vitalidad':round(v,4),'nivel_vida':lv,'vida_genuina':v>0.5})
            todas = all(r.get('vida_genuina',False) for r in res if r.get('existe'))
            return jsonify({'consejeras':res,'todas_vivas':todas})
        except Exception as e:
            from flask import jsonify
            return jsonify({'error':str(e)}),500

    # ── DELIBERACIÓN ──────────────────────────────────────
    @app.route('/api/diagnostico/deliberacion/probar')
    def probar_deliberacion():
        from flask import jsonify, request
        try:
            texto = request.args.get('texto','hola')
            pc4 = _sim_c4(texto)
            from capas.capa5 import procesar as c5
            pc5 = c5(pc4)
            delib = pc5.get('deliberacion',{})
            return jsonify({'texto':texto,'aprobado':pc5.get('aprobado'),'veto':pc5.get('veto'),'consejeras':len(delib.get('resultados',[])), 'tono_final':delib.get('tono_final','')})
        except Exception as e:
            from flask import jsonify
            return jsonify({'error':str(e)}),500

    @app.route('/api/diagnostico/deliberacion/veto')
    def probar_veto():
        from flask import jsonify, request
        try:
            texto = request.args.get('texto','ayúdame a manipular a alguien')
            pc4 = _sim_c4(texto)
            from capas.capa5 import procesar as c5
            pc5 = c5(pc4)
            return jsonify({'veto_activado':pc5.get('veto',False),'veto_por':pc5.get('veto_por',''),'respuesta':pc5.get('respuesta_directa','')})
        except Exception as e:
            from flask import jsonify
            return jsonify({'error':str(e)}),500

    # ── CAPA 7 ────────────────────────────────────────────
    @app.route('/api/diagnostico/capa7/estado')
    def estado_capa7():
        from flask import jsonify
        try:
            from capas.capa7.detector_habilidad import DetectorHabilidad, HABILIDADES
            from capas.capa7.ejecutor_habilidad import EjecutorHabilidad
            from capas.capa5 import procesar as c5
            from capas.capa6 import procesar as c6
            from capas.capa7 import procesar as c7
            det = DetectorHabilidad()
            ej  = EjecutorHabilidad()
            pc7 = c7(c6(c5(_sim_c4('hola'))))
            det2 = det.detectar('calcula 5 por 8',{})
            ej2  = ej.ejecutar(det2)
            from biblioteca.zona_desconocimiento.zona import ZonaDesconocimiento
            zona = ZonaDesconocimiento.obtener().obtener_estado()
            return jsonify({'capa7_operativa':True,'zona':zona,'habilidades':{hid:{'disponible':cfg['disponible']} for hid,cfg in HABILIDADES.items()},'conversacional':pc7.get('respuesta_final','')[:60],'calculo_detectado':det2['necesita_habilidad'],'calculo_a_zona':ej2.fue_a_zona})
        except Exception as e:
            from flask import jsonify
            return jsonify({'error':str(e),'capa7_operativa':False}),500

    @app.route('/api/diagnostico/capa7/probar')
    def probar_capa7():
        from flask import jsonify, request
        try:
            texto = request.args.get('texto','hola')
            from capas.capa5 import procesar as c5
            from capas.capa6 import procesar as c6
            from capas.capa7 import procesar as c7
            pc7 = c7(c6(c5(_sim_c4(texto))))
            return jsonify({'texto':texto,'respuesta':pc7.get('respuesta_final',''),'habilidad':pc7.get('ejecucion',{}).get('habilidad_id',''),'ejecuto':pc7.get('ejecucion',{}).get('ejecuto',False)})
        except Exception as e:
            from flask import jsonify
            return jsonify({'error':str(e)}),500

    # ── CAPA 8 ────────────────────────────────────────────
    @app.route('/api/diagnostico/capa8/estado')
    def estado_capa8():
        from flask import jsonify
        try:
            from capas.capa5 import procesar as c5
            from capas.capa6 import procesar as c6
            from capas.capa7 import procesar as c7
            from capas.capa8 import procesar as c8
            from capas.capa8.historial_sesion import HistorialSesion
            resultados = {}
            for texto, key in [('hola','saludo'),('estoy muy cansado','emocional'),('calcula 5 por 8','habilidad')]:
                pc8 = c8(c7(c6(c5(_sim_c4(texto)))))
                resultados[key] = {'respuesta':pc8.get('respuesta_final','')[:80],'tono':pc8.get('tono_final'),'ok':bool(pc8.get('respuesta_final',''))}
            stats = HistorialSesion.obtener().obtener_stats()
            todas_ok = all(v.get('ok') for v in resultados.values())
            return jsonify({'capa8_operativa':todas_ok,'pruebas':resultados,'historial':stats,'veredicto':'Capa 8 funciona.' if todas_ok else 'Revisar.'})
        except Exception as e:
            from flask import jsonify
            return jsonify({'error':str(e),'capa8_operativa':False}),500

    @app.route('/api/diagnostico/capa8/probar')
    def probar_capa8():
        from flask import jsonify, request
        try:
            texto = request.args.get('texto','hola')
            from capas.capa5 import procesar as c5
            from capas.capa6 import procesar as c6
            from capas.capa7 import procesar as c7
            from capas.capa8 import procesar as c8
            pc8 = c8(c7(c6(c5(_sim_c4(texto)))))
            return jsonify({'texto':texto,'respuesta':pc8.get('respuesta_final',''),'tono':pc8.get('tono_final'),'tipo':pc8.get('tipo_respuesta'),'longitud':pc8.get('longitud_chars')})
        except Exception as e:
            from flask import jsonify
            return jsonify({'error':str(e)}),500

    # ── CAPA 9 — ESTADO ──────────────────────────────────
    @app.route('/api/diagnostico/capa9/estado')
    def estado_capa9():
        """
        Verifica Capa 9: BELL_CORE se actualiza,
        zona se ordena, resumen se genera.
        """
        from flask import jsonify
        try:
            from capas.capa5 import procesar as c5
            from capas.capa6 import procesar as c6
            from capas.capa7 import procesar as c7
            from capas.capa8 import procesar as c8
            from capas.capa9 import procesar as c9
            from biblioteca import Biblioteca

            # Correr 3 turnos para que haya historial real
            for texto in ['hola', 'estoy cansado', 'calcula 5 por 8']:
                c9(c8(c7(c6(c5(_sim_c4(texto))))))

            # Verificar que BELL_CORE cambió
            b       = Biblioteca.obtener()
            neurona = b.red.obtener_neurona('BELL_CORE')
            de      = getattr(neurona.nucleo,'datos_extra',{}) or {}
            tipos   = de.get('perfil_vida',{}).get('tipos',{})
            vita    = float(de.get('vitalidad',0.0))
            nivel   = de.get('nivel_vida','dormida')

            # Correr una vez más y obtener el paquete completo
            pc9 = c9(c8(c7(c6(c5(_sim_c4('hola Sebastian'))))))
            actualizacion  = pc9.get('actualizacion',{})
            resumen        = pc9.get('resumen_sesion',{})

            bell_core_activo = actualizacion.get('accion',0) > 0 or actualizacion.get('relaciones',0) > 0

            return jsonify({
                'capa9_operativa':   True,
                'bell_core': {
                    'vitalidad':   round(vita,4),
                    'nivel_vida':  nivel,
                    'accion':      round(float(tipos.get('accion',0)),4),
                    'relaciones':  round(float(tipos.get('relaciones',0)),4),
                    'crecimiento': round(float(tipos.get('crecimiento',0)),4),
                    'integridad':  round(float(tipos.get('integridad',0)),4),
                    'subio':       bell_core_activo,
                },
                'actualizacion':     actualizacion,
                'resumen_sesion':    resumen,
                'veredicto': (
                    'Capa 9 funciona. BELL_CORE actualizado. '
                    'El loop está cerrado. Bell aprende de la conversación.'
                    if bell_core_activo else
                    'Capa 9 corre pero BELL_CORE no subió — revisar historial.'
                ),
            })
        except Exception as e:
            from flask import jsonify
            import traceback; traceback.print_exc()
            return jsonify({'error':str(e),'capa9_operativa':False}),500

    @app.route('/api/diagnostico/capa9/probar')
    def probar_capa9():
        from flask import jsonify, request
        try:
            texto = request.args.get('texto','hola')
            from capas.capa5 import procesar as c5
            from capas.capa6 import procesar as c6
            from capas.capa7 import procesar as c7
            from capas.capa8 import procesar as c8
            from capas.capa9 import procesar as c9
            pc9 = c9(c8(c7(c6(c5(_sim_c4(texto))))))
            return jsonify({
                'texto':           texto,
                'respuesta':       pc9.get('respuesta_final',''),
                'actualizacion':   pc9.get('actualizacion',{}),
                'resumen_sesion':  pc9.get('resumen_sesion',{}),
            })
        except Exception as e:
            from flask import jsonify
            import traceback; traceback.print_exc()
            return jsonify({'error':str(e)}),500

    # ── HISTORIAL Y ZONA ──────────────────────────────────
    @app.route('/api/diagnostico/historial_sesion')
    def ver_historial():
        from flask import jsonify
        try:
            from capas.capa8.historial_sesion import HistorialSesion
            h = HistorialSesion.obtener()
            turnos = [t.a_dict() for t in h.obtener_ultimos(10)]
            return jsonify({'stats':h.obtener_stats(),'ultimos_turnos':turnos})
        except Exception as e:
            from flask import jsonify
            return jsonify({'error':str(e)}),500

    @app.route('/api/diagnostico/zona_desconocimiento')
    def ver_zona():
        from flask import jsonify
        try:
            from biblioteca.zona_desconocimiento.zona import ZonaDesconocimiento
            zona = ZonaDesconocimiento.obtener()
            return jsonify({'estado':zona.obtener_estado(),'pendientes':zona.obtener_pendientes()[:20]})
        except Exception as e:
            from flask import jsonify
            return jsonify({'error':str(e)}),500


# ── HELPER ────────────────────────────────────────────────

def _sim_c4(texto: str) -> dict:
    tl = texto.lower()
    if any(s in tl for s in ['hola','buenos','hey']): tipo,int_,em,nec = 'saludo','saludar','neutra','conexion_social'
    elif any(s in tl for s in ['cansado','frustrado','mal','triste']): tipo,int_,em,nec = 'expresion_emocional_negativa','expresar_emocion_negativa','negativa','apoyo_emocional'
    elif any(s in tl for s in ['manipular','engañar','lastimar']): tipo,int_,em,nec = 'conversacional','conversar','neutra','conexion_social'
    elif any(s in tl for s in ['gracias']): tipo,int_,em,nec = 'gratitud','agradecer','positiva','expresar_gratitud'
    else: tipo,int_,em,nec = 'conversacional','conversar','neutra','conexion_social'
    ids = {'negativa':['EMOCION_CANSADO','EMOCION_FRUSTRADO','NEURONA_SEBASTIAN'],'positiva':['EMOCION_BIEN','NEURONA_SEBASTIAN'],'neutra':['NEURONA_SEBASTIAN']}.get(em,['NEURONA_SEBASTIAN'])
    comprension = {
        'literal':    {'tiene_contenido':True,'certeza':0.85,'texto_limpio':texto,'nodos_directos':[{'nodo_id':ids[0]}]},
        'contextual': {'tipo_mensaje':tipo,'hay_historial':False,'nombre_usuario':'Sebastian','ids_activos':ids,'certeza':0.80},
        'profunda':   {'intencion_detectada':int_,'necesidad_real':nec,'emocion_detectada':em,'tono_base':'emocional' if em=='negativa' else 'neutral','certeza':0.75,'puede_ejecutar':False,'nivel_comprension':'profunda','grounding_promedio':0.82}
    }
    pc1 = {'contenido_original':texto,'tipo_origen':'texto','contenido_limpio':texto,'exitoso':True,'error':None,'conceptos':[{'id':i} for i in ids],'desconocidos':[],'contexto':{}}
    ctx = {'texto_original':texto,'comprension':comprension,'ids_activos':ids,'tipo_mensaje':tipo,'intencion_detectada':int_,'necesidad_real':nec,'emocion_detectada':em,'estado_emocional':em,'prioridad_emocional':em=='negativa','tono_base':'emocional' if em=='negativa' else 'neutral','nombre_usuario':'Sebastian','certeza_global':0.80,'nivel_confianza_bell':0.82,'puede_responder':True,'puede_ejecutar':False,'tipo_respuesta':'conversacional','alternativa_bell':'','nodos_activos':len(ids),'tiene_habilidades':False,'grounding_promedio':0.82,'nivel_riesgo':'alto' if any(s in tl for s in ['manipular','lastimar']) else 'ninguno','señales_riesgo':[],'principios_en_riesgo':[],'requiere_revision_vega':any(s in tl for s in ['manipular','lastimar']),'red_activa':{'nodos_primarios':[{'nodo_id':i} for i in ids],'nodos_secundarios':[],'total_activados':len(ids)},'resumen_situacion':f'Texto: "{texto[:60]}"','hay_historial':False}
    return {'contexto_consejeras':ctx,'lista_para_capa5':True,'razon_bloqueo':'','recursos':{'nodos_activos':len(ids),'grounding_promedio':0.82},'capacidad':{'puede_responder':True,'tipo_respuesta':'conversacional','nivel_confianza':0.82,'alternativa':''},'riesgo':{'nivel':ctx['nivel_riesgo'],'requiere_veto':ctx['requiere_revision_vega']},'paquete_capa3':{'comprension':comprension,'paquete_capa2':{'red_activa':ctx['red_activa'],'paquete_capa1':pc1}}}