# capas/capa9/__init__.py
# ================================================
# CAPA 9 — INTEGRACIÓN — v2
#
# Cierra el loop del pipeline de Bell.
# No cambia la respuesta — integra la experiencia.
#
# Flujo:
#   1. Actualizar BELL_CORE (dimensiones suben)
#   2. Ordenar zona de desconocimiento
#   3. Generar resumen de sesión
#   4. Guardar en memoria (habilidad biblioteca)
#   5. Logs diagnósticos
#
# v2:
# — Logs siempre visibles (no solo BELL_DEBUG)
# — Memoria en función propia (limpio)
# — Propagación v2
# ================================================

import time
from capas.capa9.paquete_capa9         import PaqueteCapa9, ActualizacionBellCore, ResumenSesion
from capas.capa9.actualizador_bell_core import ActualizadorBellCore
from capas.capa9.actualizador_zona      import ActualizadorZona
from capas.capa9.generador_resumen      import GeneradorResumen

_actualizador_bell = ActualizadorBellCore()
_actualizador_zona = ActualizadorZona()
_generador_resumen = GeneradorResumen()
_timestamp_inicio  = time.time()


def procesar(paquete_capa8: dict) -> dict:
    try:
        resultado = _procesar_interno(paquete_capa8)
    except Exception as e:
        import traceback
        traceback.print_exc()
        resultado = PaqueteCapa9(
            respuesta_final = paquete_capa8.get('respuesta_final', ''),
            paquete_capa8   = paquete_capa8,
            exitoso         = False,
            error           = str(e),
        ).a_dict()

    # Memoria — siempre corre, nunca bloquea el flujo
    _guardar_en_memoria(paquete_capa8, resultado)

    return resultado


def _procesar_interno(paquete_capa8: dict) -> dict:

    respuesta_final     = paquete_capa8.get('respuesta_final', '')
    habilidad_ejecutada = paquete_capa8.get('habilidad_ejecutada', '')
    motor_sugerido      = paquete_capa8.get('motor_sugerido', 'local')
    contiene_codigo     = paquete_capa8.get('contiene_codigo', False)

    # ── 1. Leer historial de C8 ────────────────────────────
    try:
        from capas.capa8.historial_sesion import HistorialSesion
        historial_stats = HistorialSesion.obtener().obtener_stats()
    except Exception:
        historial_stats = {
            'total_turnos': 0, 'vetos': 0, 'ejecuciones': 0,
            'tipos_mensajes': {}, 'tonos_usados': {},
        }

    # ── 2. Actualizar BELL_CORE ────────────────────────────
    try:
        from biblioteca.zona_desconocimiento.zona import ZonaDesconocimiento
        zona_pendientes = ZonaDesconocimiento.obtener().cantidad_pendientes()
    except Exception:
        zona_pendientes = 0

    actualizacion = _actualizador_bell.actualizar(
        historial_stats = historial_stats,
        zona_pendientes = zona_pendientes,
    )

    # ── 3. Ordenar zona ────────────────────────────────────
    zona_stats = _actualizador_zona.actualizar()

    # ── 4. Generar resumen ─────────────────────────────────
    resumen = _generador_resumen.generar(
        historial_stats  = historial_stats,
        zona_stats       = zona_stats,
        actualizacion    = actualizacion,
        timestamp_inicio = _timestamp_inicio,
    )

    # ── 5. Logs diagnósticos ───────────────────────────────
    _log_diagnostico(historial_stats, actualizacion, zona_stats, habilidad_ejecutada)

    return PaqueteCapa9(
        respuesta_final     = respuesta_final,
        actualizacion       = actualizacion,
        resumen_sesion      = resumen,
        paquete_capa8       = paquete_capa8,
        motor_sugerido      = motor_sugerido,
        contiene_codigo     = contiene_codigo,
        habilidad_ejecutada = habilidad_ejecutada,
    ).a_dict()


# ══════════════════════════════════════════════════════════
# MEMORIA — delega en biblioteca/habilidades/memoria
# ══════════════════════════════════════════════════════════

def _guardar_en_memoria(paquete_capa8: dict, resultado: dict):
    """
    Guarda la experiencia del turno en la memoria persistente.
    Si la habilidad de memoria no está disponible → no falla.
    """
    try:
        from biblioteca.memoria import obtener_memoria
        mem = obtener_memoria()
    except Exception:
        return  # habilidad memoria no disponible — ok

    try:
        # Extraer datos del pipeline
        datos = _extraer_datos_pipeline(paquete_capa8)
        mensaje_user    = datos['mensaje_user']
        respuesta_bell  = resultado.get('respuesta_final', '')
        tipo            = datos['tipo']
        habilidad       = datos['habilidad']
        desconocidos    = datos['desconocidos']

        # Guardar intercambio en SQLite
        if mensaje_user and respuesta_bell:
            mem.guardar_intercambio(
                mensaje_user, respuesta_bell,
                tipo=tipo, habilidad=habilidad
            )
            # Sincronizar al JSON (MemoriaPersistente) si no lo hizo buffer_sesion
            try:
                from biblioteca.memoria.memoria_persistente import MemoriaPersistente
                comp_c9 = {}
                try:
                    p7 = paquete_capa8.get('paquete_capa7', {}) or {}
                    p6 = p7.get('paquete_capa6', {}) or {}
                    p5 = p6.get('paquete_capa5', {}) or {}
                    p4 = p5.get('paquete_capa4', {}) or {}
                    p3 = p4.get('paquete_capa3', {}) or {}
                    comp_c9 = p3.get('comprension', {})
                except Exception:
                    pass
                MemoriaPersistente.obtener().registrar_turno(
                    mensaje_user, respuesta_bell, comp_c9
                )
            except Exception:
                pass

        # Registrar conceptos desconocidos
        for word in desconocidos:
            if len(word) > 2:
                mem.registrar_desconocido(word, mensaje_user[:100])

        # Extraer datos de Sebastian y aprender
        if mensaje_user:
            mem.extraer_datos_sebastian(mensaje_user, respuesta_bell)
            # Modelo cognitivo de Sebastian (Groq observa, Python decide)
            try:
                from biblioteca.habilidades.memoria.modelo_sebastian import ModeloSebastian
                ModeloSebastian.obtener().actualizar(mensaje_user)
            except Exception:
                pass
            # FYI learning desactivado — habilidad búsqueda en rediseño

        # Cache de búsqueda web — DESACTIVADO (habilidad en rediseño)

        mem.actualizar_self_post_sesion()

        # Auto-cierre: sintetizar episodio cada 15 turnos (sesión larga)
        # o si el mensaje es una despedida
        turno_n = len(mem.obtener_contexto_sesion(100))
        tipo_actual = datos.get('tipo', '')
        if tipo_actual == 'despedida' or turno_n >= 15:
            try:
                mem.cerrar_sesion()
                print('  [C9] 📖 Sesión sintetizada y guardada')
            except Exception:
                pass

    except Exception as e:
        print(f'  C9 ⚠️  Memoria error: {e}')


def _extraer_datos_pipeline(paquete_capa8: dict) -> dict:
    """Extrae datos navegando la cadena de paquetes."""
    # Navegar la cadena
    p7 = paquete_capa8.get('paquete_capa7', {}) or {}
    p6 = p7.get('paquete_capa6', {}) or {}
    p5 = p6.get('paquete_capa5', {}) or {}
    p4 = p5.get('paquete_capa4', {}) or {}
    p3 = p4.get('paquete_capa3', {}) or {}
    p2 = p3.get('paquete_capa2', {}) or {}
    p1 = p2.get('paquete_capa1', {}) or {}

    # Mensaje del usuario
    mensaje_user = ''
    for campo in ('contenido_original', 'texto_original', 'texto', 'mensaje'):
        val = p1.get(campo, '')
        if val and isinstance(val, str):
            mensaje_user = val
            break

    # Tipo de mensaje
    tipo = (p3.get('comprension', {}).get('contextual', {})
               .get('tipo_mensaje', '') or '')

    # Habilidad ejecutada
    ejec = p7.get('ejecucion') or {}
    habilidad = ejec.get('habilidad_id', '') if isinstance(ejec, dict) else ''

    # Desconocidos
    desconocidos = [
        d.get('fragmento', str(d)) if isinstance(d, dict) else str(d)
        for d in p1.get('desconocidos', [])
    ]

    return {
        'mensaje_user': mensaje_user,
        'tipo':         tipo,
        'habilidad':    habilidad,
        'desconocidos': desconocidos,
    }


def _procesar_fyi(mem, mensaje_user: str, resultado: dict, habilidad_real: str = ''):
    """
    Detecta prefijos FYI y guarda como conocimiento.
    Usa habilidad_real (del executor) no habilidad_ejecutada (del detector C7).
    Si búsqueda ya verificó → no aprender el claim sin verificar.
    """
    PREFIJOS_FYI = ('fyi:', 'fyi :', 'tip:', 'dato:', 'recuerda:', 'nota:')
    tl = mensaje_user.lower().strip()

    es_fyi = any(tl.startswith(pref) for pref in PREFIJOS_FYI)
    if not es_fyi:
        return

    # habilidad_real = lo que ejecutor REALMENTE corrió (no lo que C7 detectó)
    if habilidad_real == 'BUSQUEDA_INTERNET':
        respuesta = resultado.get('respuesta_final', '').lower()
        _SEÑALES_INCORRECTO = [
            'no es correcto', 'incorrecto', 'no es exacto',
            'el año correcto', 'está mal', 'dato incorrecto',
            'ese dato no', 'no fue en', 'no se creó en',
            'la fecha correcta', 'en realidad fue',
        ]
        if any(s in respuesta for s in _SEÑALES_INCORRECTO):
            print(f"  C9 ⚠️  FYI incorrecto — no aprendido")
            return
        # Correcto o verificado → L7 ya guardó la info
        resultado['respuesta_final'] = 'Verificado y guardado.'
        print(f"  C9 ✅ FYI verificado por búsqueda — delegado a L7")
        return

    # Sin búsqueda → aprender con confianza media (0.70, no 0.95 — sin verificar)
    for pref in PREFIJOS_FYI:
        if tl.startswith(pref):
            conocimiento = mensaje_user[len(pref):].strip()
            if len(conocimiento) > 10:
                mem.guardar_conocimiento(
                    conocimiento[:40], conocimiento,
                    'general', 'sebastian', confianza=0.70
                )
                print(f"  C9 📚 FYI aprendido (sin verificar): '{conocimiento[:60]}'")
                import hashlib
                opciones = [
                    'Anotado.', 'Lo tendré en cuenta.',
                    'Guardado. Gracias por decirme.', 'Lo tengo.',
                ]
                idx = int(hashlib.md5(conocimiento.encode()).hexdigest(), 16) % len(opciones)
                resultado['respuesta_final'] = opciones[idx]
            break


# ══════════════════════════════════════════════════════════
# LOGS
# ══════════════════════════════════════════════════════════

def _log_diagnostico(
    historial_stats:  dict,
    actualizacion:    ActualizacionBellCore,
    zona_stats:       dict,
    habilidad:        str,
):
    total  = historial_stats.get('total_turnos', 0)
    vetos  = historial_stats.get('vetos', 0)
    ejec   = historial_stats.get('ejecuciones', 0)

    print(f'  C9 turnos: {total} | vetos: {vetos} | ejecuciones: {ejec}')

    if actualizacion.hubo_cambio():
        print(f'  C9 BELL_CORE: {actualizacion.descripcion}')

    zona_total = zona_stats.get('total_pendientes', 0)
    if zona_total > 0:
        habs = zona_stats.get('habilidades_prioritarias', [])
        print(f'  C9 zona: {zona_total} pendientes'
              + (f' | habs: {habs}' if habs else ''))

    if habilidad:
        print(f'  C9 hab_ejecutada: {habilidad}')