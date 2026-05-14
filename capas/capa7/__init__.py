# capas/capa7/__init__.py
# ================================================
# CAPA 7 — EJECUCIÓN
#
# Recibe: PaqueteCapa6
# Produce: PaqueteCapa7
#
# Flujo:
# 1. Detecta si el mensaje necesita una habilidad
# 2. Si no necesita → pasa la respuesta de Capa 6
# 3. Si necesita y existe → la ejecuta
# 4. Si necesita y no existe → honestidad y zona
# ================================================

from capas.capa7.paquete_capa7       import PaqueteCapa7, ResultadoEjecucion
from capas.capa7.detector_habilidad  import DetectorHabilidad
from capas.capa7.ejecutor_habilidad  import EjecutorHabilidad

_detector = DetectorHabilidad()
_ejecutor = EjecutorHabilidad()


def procesar(paquete_capa6: dict) -> dict:
    try:
        return _procesar_interno(paquete_capa6)
    except Exception as e:
        import traceback; traceback.print_exc()
        return PaqueteCapa7(
            respuesta_final = paquete_capa6.get('respuesta_final', ''),
            paquete_capa6   = paquete_capa6,
            exitoso         = False,
            error           = str(e),
        ).a_dict()


def _procesar_interno(paquete_capa6: dict) -> dict:

    # ── CHECK PENDIENTE CLARIFICACIÓN PRIMERO ────────────────
    # Si Bell hizo una pregunta de clarificación y el usuario responde,
    # interceptar aquí antes de cualquier otra lógica.
    try:
        from biblioteca.habilidades.busqueda.motor_busqueda import (
            _PENDIENTE, _es_respuesta_clarificacion, ejecutar_busqueda
        )
        texto_entrada = ''
        try:
            p5 = paquete_capa6.get('paquete_capa5', {}) or {}
            p4 = p5.get('paquete_capa4', {}) or {}
            p3 = p4.get('paquete_capa3', {}) or {}
            p2 = p3.get('paquete_capa2', {}) or {}
            p1 = p2.get('paquete_capa1', {}) or {}
            texto_entrada = p1.get('contenido_original', '') or ''
        except Exception:
            pass

        if texto_entrada and _PENDIENTE.get('activo'):
            if _es_respuesta_clarificacion(texto_entrada):
                print(f"  [C7] ↩ Retomando búsqueda: '{_PENDIENTE.get('pregunta', '')[:40]}'")
                resultado_busqueda = ejecutar_busqueda(texto_entrada)
                if resultado_busqueda.get('exitoso'):
                    return PaqueteCapa7(
                        respuesta_final      = resultado_busqueda['respuesta'],
                        tiene_resultado_real = True,
                        ejecucion            = ResultadoEjecucion(
                            ejecuto=True,
                            habilidad_id='BUSQUEDA_INTERNET',
                            resultado=resultado_busqueda['respuesta'],
                        ),
                        paquete_capa6        = paquete_capa6,
                    ).a_dict()
    except Exception as _e:
        pass  # clarificación no crítica

    respuesta_capa6  = paquete_capa6.get('respuesta_final', '')
    decision         = paquete_capa6.get('decision', {})
    paquete_c5       = paquete_capa6.get('paquete_capa5', {})
    paquete_c4       = paquete_c5.get('paquete_capa4', {})
    paquete_c3       = paquete_c4.get('paquete_capa3', {})
    paquete_c2       = paquete_c3.get('paquete_capa2', {})
    paquete_c1       = paquete_c2.get('paquete_capa1', {})
    texto_original   = paquete_c1.get('contenido_original', '')

    # 1. Detectar si necesita habilidad
    deteccion = _detector.detectar(texto_original, decision)

    # 2. Si no necesita habilidad → pasar respuesta de Capa 6
    if not deteccion['necesita_habilidad']:
        return PaqueteCapa7(
            respuesta_final      = respuesta_capa6,
            ejecucion            = ResultadoEjecucion(ejecuto=False),
            tiene_resultado_real = False,
            paquete_capa6        = paquete_capa6,
        ).a_dict()

    # 3a. Memoria-first: solo para BUSQUEDA_INTERNET con conocimiento de Sebastian
    try:
        _habilidad_id = deteccion.get('habilidad_id', '')
        # Memory-first: BUSQUEDA_INTERNET siempre, PYTHON_COMPLETO solo si es
        # pregunta FACTUAL (quién, cuándo, qué es) no contextual (estoy, tengo)
        _es_factual_python = False
        if _habilidad_id == 'PYTHON_COMPLETO':
            _tl = texto_original.lower()
            _factual_markers = ['quién', 'quien', 'cuándo', 'cuando', 'qué es',
                                 'que es', 'quién creó', 'quien creo', 'cómo se llama']
            _contextual_markers = ['estoy', 'tengo', 'mi ', 'me ', 'ayuda', 'arregla',
                                    'bug', 'error', 'problema', 'trabajando']
            if (any(m in _tl for m in _factual_markers) and
                    not any(m in _tl for m in _contextual_markers)):
                _es_factual_python = True
        if _habilidad_id == 'BUSQUEDA_INTERNET' or _es_factual_python:
            from biblioteca.memoria import obtener_memoria
            _mem = obtener_memoria()
            # Buscar por palabras clave en conocimiento de Sebastian
            _palabras = [w for w in texto_original.lower().split() if len(w) > 4]
            for _pal in _palabras[:3]:
                import threading as _th
                with _th.Lock():
                    _row = _mem.db.execute(
                        "SELECT respuesta FROM conocimiento "
                        "WHERE fuente='sebastian' AND vigente=1 AND "
                        "(tema LIKE ? OR respuesta LIKE ?) "
                        "ORDER BY confianza DESC LIMIT 1",
                        (f'%{_pal}%', f'%{_pal}%')
                    ).fetchone()
                if _row and _row['respuesta'] and len(_row['respuesta']) > 15:
                    _resp = _row['respuesta']
                    print(f"  [C7] 📚 Desde memoria Sebastian: '{_resp[:40]}'")
                    return PaqueteCapa7(
                        respuesta_final      = _resp,
                        ejecucion            = ResultadoEjecucion(ejecuto=True,
                                               habilidad_id='BUSQUEDA_INTERNET',
                                               resultado=_resp),
                        tiene_resultado_real = True,
                        paquete_capa6        = paquete_capa6,
                    ).a_dict()
    except Exception:
        pass

    # 3. Necesita habilidad → intentar ejecutar
    resultado = _ejecutor.ejecutar(deteccion)

    # 4. Si ejecutó con éxito → nueva respuesta con resultado real
    if resultado.ejecuto and resultado.resultado:
        return PaqueteCapa7(
            respuesta_final      = resultado.resultado,
            ejecucion            = resultado,
            tiene_resultado_real = True,
            paquete_capa6        = paquete_capa6,
        ).a_dict()

    # 5. No ejecutó (habilidad no disponible) →
    #    usar respuesta honesta del ejecutor si existe,
    #    si no usar la de Capa 6
    respuesta_final = (
        resultado.resultado
        if resultado.resultado
        else respuesta_capa6
    )

    return PaqueteCapa7(
        respuesta_final      = respuesta_final,
        ejecucion            = resultado,
        tiene_resultado_real = False,
        paquete_capa6        = paquete_capa6,
    ).a_dict()