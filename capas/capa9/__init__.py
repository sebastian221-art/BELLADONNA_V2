# capas/capa9/__init__.py
# ================================================
# CAPA 9 — INTEGRACIÓN
# La última capa. Cierra el loop.
#
# Recibe: PaqueteCapa8
# Produce: PaqueteCapa9
#
# Lo que hace:
# 1. Lee el historial de Capa 8
# 2. Actualiza BELL_CORE — por primera vez
#    acción, relaciones, crecimiento suben
# 3. Ordena la zona de desconocimiento
# 4. Genera resumen de sesión
# 5. Pasa la respuesta final intacta
# ================================================

import time
from capas.capa9.paquete_capa9         import PaqueteCapa9, ActualizacionBellCore, ResumenSesion
from capas.capa9.actualizador_bell_core import ActualizadorBellCore
from capas.capa9.actualizador_zona      import ActualizadorZona
from capas.capa9.generador_resumen      import GeneradorResumen

_actualizador_bell = ActualizadorBellCore()
_actualizador_zona = ActualizadorZona()
_generador_resumen = GeneradorResumen()

# Timestamp de inicio de sesión — primera vez que se llama
_timestamp_inicio = time.time()



def procesar(paquete_capa8: dict) -> dict:
    """C9: integración final + memoria."""
    # 1. Procesar normalmente
    resultado = {}
    try:
        resultado = _procesar_interno(paquete_capa8)
    except Exception as e:
        import traceback; traceback.print_exc()
        resultado = PaqueteCapa9(
            respuesta_final = paquete_capa8.get('respuesta_final', ''),
            paquete_capa8   = paquete_capa8,
            exitoso         = False,
            error           = str(e),
        ).a_dict()

    # 2. Memoria — SIEMPRE corre, no bloquea el flujo
    respuesta_final = resultado.get('respuesta_final', '') if resultado else ''
    try:
        from biblioteca.memoria import obtener_memoria
        mem = obtener_memoria()

        reg_raw = paquete_capa8.get('registro_turno')

        # Extraer mensaje_user
        mensaje_user = ''
        tipo = ''
        desconocidos = []
        habilidad = ''

        # Ruta 1: registro_turno
        if reg_raw is not None:
            if isinstance(reg_raw, dict):
                mensaje_user = reg_raw.get('texto_usuario', '') or ''
                tipo = reg_raw.get('tipo_mensaje', '') or ''
            elif hasattr(reg_raw, 'texto_usuario'):
                mensaje_user = str(reg_raw.texto_usuario or '')
                tipo = str(getattr(reg_raw, 'tipo_mensaje', '') or '')

        # Ruta 2: cadena de paquetes
        if not mensaje_user:
            try:
                p7 = paquete_capa8.get('paquete_capa7', {}) or {}
                p6 = p7.get('paquete_capa6', {}) or {}
                p5 = p6.get('paquete_capa5', {}) or {}
                p4 = p5.get('paquete_capa4', {}) or {}
                p3 = p4.get('paquete_capa3', {}) or {}
                p2 = p3.get('paquete_capa2', {}) or {}
                p1 = p2.get('paquete_capa1', {}) or {}
                for campo in ('contenido_original', 'texto_original', 'texto', 'mensaje'):
                    val = p1.get(campo, '')
                    if val and isinstance(val, str):
                        mensaje_user = val
                        break
                tipo = tipo or p3.get('tipo_mensaje', '') or ''
                desconocidos = p1.get('desconocidos', []) or []
                ejec = p7.get('ejecucion')
                if ejec:
                    habilidad = (ejec.get('habilidad_id', '') if isinstance(ejec, dict)
                                 else str(getattr(ejec, 'habilidad_id', '') or ''))
            except Exception:
                pass

        # Guardar intercambio
        if mensaje_user and respuesta_final:
            mem.guardar_intercambio(mensaje_user, respuesta_final,
                                     tipo=tipo, habilidad=habilidad)

        # Desconocidos
        for word in desconocidos:
            if len(word) > 2:
                mem.registrar_desconocido(word, mensaje_user[:100])

        # Perfil + aprendizaje
        if mensaje_user:
            mem.extraer_datos_sebastian(mensaje_user, respuesta_final)
            mem.aprender_de_mensaje(mensaje_user)
            tl = mensaje_user.lower()
            for pref in ('fyi:', 'fyi :', 'tip:', 'dato:', 'recuerda:', 'nota:'):
                if tl.startswith(pref):
                    conocimiento = mensaje_user[len(pref):].strip()
                    if len(conocimiento) > 10:
                        mem.guardar_conocimiento(conocimiento[:40], conocimiento,
                                                  'general', 'sebastian', confianza=0.95)
                        print(f"  [Memoria] 📚 FYI aprendido: '{conocimiento[:60]}'")
                        # Actualizar respuesta para que Bell acuse recibo
                        import hashlib
                        _opciones = ["Anotado.", "Lo tendré en cuenta.",
                                     "Guardado. Gracias por decirme.",
                                     "Lo tengo. Gracias."]
                        _idx = int(hashlib.md5(conocimiento.encode()).hexdigest(), 16) % len(_opciones)
                        _nueva_resp = _opciones[_idx]
                        resultado['respuesta_final'] = _nueva_resp
                        paquete_capa8['respuesta_final'] = _nueva_resp
                    break

        # Cache búsqueda
        if habilidad == 'BUSQUEDA_INTERNET' and respuesta_final and mensaje_user:
            mem.guardar_busqueda_web(mensaje_user.lower(), respuesta_final)


        # ── CORRECCIÓN DE RESPUESTAS INCORRECTAS ─────────────
        # Cuando Python base genera "Mi creador se llama Sebastian"
        # para preguntas donde debería responder sobre Sebastian.
        _resp_actual = resultado.get('respuesta_final', '')
        # Todos los patrones incorrectos que C6 Python genera para preguntas
        # sobre Sebastian o sesión — confirmados en logs reales
        _patrones_error = [
            'Mi creador se llama Sebastian',
            'Sebastian. Mi creador.',
            'Mi creador. Tiene 19',
            'Sebastian — él me creó',
            'él me creó. Cada capa mía',
            'Sebastian. Mi creador. Tiene',
        ]
        if any(p in _resp_actual for p in _patrones_error) and mensaje_user:
            tl_msg = mensaje_user.lower()

            # Preguntas de auto-referencia
            _autoref = ['de dónde soy', 'donde soy', 'cuántos años', 'cuantos años',
                        'cómo me llamo', 'como me llamo', 'quién soy', 'quien soy',
                        'dónde vivo', 'donde vivo', 'mi ciudad', 'cuál es mi nombre']
            if any(p in tl_msg for p in _autoref):
                _perfil = mem.obtener_perfil()
                _ciudad = _perfil.get('ciudad', 'Bucaramanga')
                _pais   = _perfil.get('pais', 'Colombia')
                _edad   = _perfil.get('edad', '19')
                _corr   = f"De {_ciudad}, {_pais}. Tienes {_edad} años."
                resultado['respuesta_final'] = _corr
                paquete_capa8['respuesta_final'] = _corr
                print(f"  [Memoria] 🔧 Auto-ref corregida: '{_corr}'")

            # Preguntas sobre sesión
            elif any(p in tl_msg for p in ['qué hice', 'que hice', 'cuéntame hoy',
                     'cuentame hoy', 'qué pasó hoy', 'hice hoy', 'de qué hablamos']):
                _ctx = mem.obtener_contexto_sesion(6)
                if _ctx and len(_ctx) > 1:
                    _n = len(_ctx)
                    _t0 = _ctx[0].get('user', '')[:50]
                    _tN = _ctx[-1].get('user', '')[:50]
                    _plural = "intercambio" if _n == 1 else "intercambios"
                    _corr = f"Esta sesión llevamos {_n} {_plural}. Empezaste con '{_t0}'"
                    if _n > 1:
                        _corr += f" y terminamos hablando de '{_tN}'"
                    _corr += "."
                    resultado['respuesta_final'] = _corr
                    paquete_capa8['respuesta_final'] = _corr
                    print(f"  [Memoria] 🔧 Sesión corregida: {_n} intercambios")

        mem.actualizar_self_post_sesion()

    except Exception as _mem_err:
        print(f"  [Memoria] ⚠ Error C9: {_mem_err}")
        import traceback; traceback.print_exc()

    return resultado



def _procesar_interno(paquete_capa8: dict) -> dict:

    respuesta_final = paquete_capa8.get('respuesta_final', '')

    # ── 1. LEER HISTORIAL DE CAPA 8 ─────────────────────
    try:
        from capas.capa8.historial_sesion import HistorialSesion
        historial       = HistorialSesion.obtener()
        historial_stats = historial.obtener_stats()
    except Exception:
        historial_stats = {'total_turnos': 0, 'vetos': 0, 'ejecuciones': 0, 'tipos_mensajes': {}, 'tonos_usados': {}}

    # ── 2. ACTUALIZAR BELL_CORE ──────────────────────────
    try:
        from biblioteca.zona_desconocimiento.zona import ZonaDesconocimiento
        zona_pendientes = ZonaDesconocimiento.obtener().cantidad_pendientes()
    except Exception:
        zona_pendientes = 0

    actualizacion = _actualizador_bell.actualizar(
        historial_stats = historial_stats,
        zona_pendientes = zona_pendientes,
    )

    # ── 3. ACTUALIZAR ZONA ───────────────────────────────
    zona_stats = _actualizador_zona.actualizar()

    # ── 4. GENERAR RESUMEN ───────────────────────────────
    resumen = _generador_resumen.generar(
        historial_stats  = historial_stats,
        zona_stats       = zona_stats,
        actualizacion    = actualizacion,
        timestamp_inicio = _timestamp_inicio,
    )

    return PaqueteCapa9(
        respuesta_final = respuesta_final,
        actualizacion   = actualizacion,
        resumen_sesion  = resumen,
        paquete_capa8   = paquete_capa8,
    ).a_dict()