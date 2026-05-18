# capas/capa7/__init__.py
# ================================================
# CAPA 7 — EJECUCIÓN — v2
#
# Flujo:
# 1. Si tipo_respuesta es simple → pasar directo (sin habilidad)
# 2. Detectar si necesita habilidad
# 3. Revisar memoria antes de buscar (evita internet innecesario)
# 4. Ejecutar habilidad si corresponde
# 5. Retornar mejor respuesta
#
# v2:
# — Logs diagnósticos completos
# — Propagación campos v2
# — Bypass para mensajes conversacionales/emocionales
# — Fix búsqueda Sebastian
# ================================================

from capas.capa7.paquete_capa7      import PaqueteCapa7, ResultadoEjecucion
from capas.capa7.detector_habilidad import DetectorHabilidad
from capas.capa7.ejecutor_habilidad import EjecutorHabilidad

_detector = DetectorHabilidad()
_ejecutor  = EjecutorHabilidad()

# Tipos de respuesta que NUNCA necesitan habilidad externa
_TIPOS_SIN_HABILIDAD = {
    'emocional', 'veto_respuesta',
    'matematica_python', 'honestidad_limitacion',
    'presentacion_sebastian',
}


def procesar(paquete_capa6: dict) -> dict:
    try:
        return _procesar_interno(paquete_capa6)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return PaqueteCapa7(
            respuesta_final = paquete_capa6.get('respuesta_final', ''),
            paquete_capa6   = paquete_capa6,
            exitoso         = False,
            error           = str(e),
        ).a_dict()


def _procesar_interno(paquete_capa6: dict) -> dict:

    respuesta_capa6  = paquete_capa6.get('respuesta_final', '')
    decision         = paquete_capa6.get('decision', {})
    tipo_respuesta   = paquete_capa6.get('tipo_respuesta', 'conversacional')
    motor_sugerido   = paquete_capa6.get('motor_sugerido', 'local')
    contiene_codigo  = paquete_capa6.get('contiene_codigo', False)

    # Extraer texto original
    texto_original = _extraer_texto(paquete_capa6)

    # ── BYPASS: mensajes simples nunca necesitan habilidades ──────
    if tipo_respuesta in _TIPOS_SIN_HABILIDAD:
        print(f'  C7 habilidad:  (bypass {tipo_respuesta}) | ejecuto: False')
        return _paquete_directo(respuesta_capa6, paquete_capa6,
                                motor_sugerido, contiene_codigo)

    # ── CHECK clarificación pendiente ─────────────────────────────
    clarificacion = _check_clarificacion(texto_original, paquete_capa6)
    if clarificacion:
        return clarificacion

    # ── 1. Detectar si necesita habilidad ─────────────────────────
    deteccion = _detector.detectar(
        texto          = texto_original,
        decision_final = decision,
        tipo_respuesta = tipo_respuesta,
    )

    # ── 2. No necesita habilidad → pasar C6 ──────────────────────
    if not deteccion['necesita_habilidad']:
        print(f'  C7 habilidad:  | ejecuto: False')
        return _paquete_directo(respuesta_capa6, paquete_capa6,
                                motor_sugerido, contiene_codigo)

    habilidad_id = deteccion.get('habilidad_id', '')
    modo         = deteccion.get('modo', '')
    print(f'  C7 habilidad: {habilidad_id} | modo: {modo or "-"}')

    # ── 3. Revisar memoria — DESACTIVADO (habilidad en rediseño) ─

    # ── 4. Ejecutar habilidad ─────────────────────────────────────
    resultado = _ejecutor.ejecutar(deteccion)
    print(f'  C7 ejecuto: {resultado.ejecuto} | hab: {resultado.habilidad_id}')

    if resultado.ejecuto and resultado.resultado:
        return PaqueteCapa7(
            respuesta_final      = resultado.resultado,
            ejecucion            = resultado,
            tiene_resultado_real = True,
            paquete_capa6        = paquete_capa6,
            motor_sugerido       = motor_sugerido,
            contiene_codigo      = contiene_codigo,
            habilidad_ejecutada  = habilidad_id,
        ).a_dict()

    # ── 5. Habilidad falló → mejor respuesta disponible ──────────
    respuesta_final = (
        resultado.resultado if resultado.resultado else respuesta_capa6
    )
    return PaqueteCapa7(
        respuesta_final      = respuesta_final,
        ejecucion            = resultado,
        tiene_resultado_real = False,
        paquete_capa6        = paquete_capa6,
        motor_sugerido       = motor_sugerido,
        contiene_codigo      = contiene_codigo,
        habilidad_ejecutada  = habilidad_id,
    ).a_dict()


# ══════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════

def _extraer_texto(paquete_capa6: dict) -> str:
    try:
        return (paquete_capa6
                .get('paquete_capa5', {})
                .get('paquete_capa4', {})
                .get('paquete_capa3', {})
                .get('paquete_capa2', {})
                .get('paquete_capa1', {})
                .get('contenido_original', ''))
    except Exception:
        return ''


def _paquete_directo(respuesta: str, paquete_capa6: dict,
                     motor_sugerido: str, contiene_codigo: bool) -> dict:
    return PaqueteCapa7(
        respuesta_final      = respuesta,
        ejecucion            = ResultadoEjecucion(ejecuto=False),
        tiene_resultado_real = False,
        paquete_capa6        = paquete_capa6,
        motor_sugerido       = motor_sugerido,
        contiene_codigo      = contiene_codigo,
    ).a_dict()


def _check_clarificacion(texto: str, paquete_capa6: dict) -> dict | None:
    """Retoma búsquedas pendientes de clarificación."""
    try:
        from biblioteca.habilidades.busqueda.motor_busqueda import (
            _PENDIENTE, _es_respuesta_clarificacion, ejecutar_busqueda
        )
        if texto and _PENDIENTE.get('activo') and _es_respuesta_clarificacion(texto):
            print(f"  C7 ↩ Retomando búsqueda pendiente")
            resultado = ejecutar_busqueda(texto)
            if resultado.get('exitoso'):
                motor = paquete_capa6.get('motor_sugerido', 'local')
                codigo = paquete_capa6.get('contiene_codigo', False)
                return PaqueteCapa7(
                    respuesta_final      = resultado['respuesta'],
                    tiene_resultado_real = True,
                    ejecucion            = ResultadoEjecucion(
                        ejecuto=True,
                        habilidad_id='BUSQUEDA_INTERNET',
                        resultado=resultado['respuesta'],
                    ),
                    paquete_capa6       = paquete_capa6,
                    motor_sugerido      = motor,
                    contiene_codigo     = codigo,
                    habilidad_ejecutada = 'BUSQUEDA_INTERNET',
                ).a_dict()
    except Exception:
        pass
    return None


def _buscar_en_memoria(texto: str) -> str:
    """
    Busca en memoria antes de ir a internet.
    Valida relevancia real con overlap de tokens antes de devolver cache.
    El threshold del gestor (0.12) es demasiado bajo — aquí exigimos 0.40.
    """
    # Nunca usar cache para FYI/verificación — necesita búsqueda fresca
    tl_check = texto.lower().strip()
    if any(tl_check.startswith(p) for p in ('fyi:', 'fyi :', 'tip:', 'dato:', 'nota:')):
        return ''

    try:
        from biblioteca.memoria import obtener_memoria
        import unicodedata, re
        mem = obtener_memoria()

        _STOP = {
            'qué','que','es','son','la','el','de','del','un','una','en',
            'y','a','por','para','con','como','cómo','cual','cuál','los',
            'las','fue','era','hay','ser','tiene','su','sus',
        }

        def _overlap(q: str, r: str) -> float:
            qt = set(w for w in re.findall(r'\b\w{3,}\b', q.lower()) if w not in _STOP)
            rt = set(w for w in re.findall(r'\b\w{3,}\b', r[:250].lower()) if w not in _STOP)
            if not qt:
                return 0.0
            return len(qt & rt) / len(qt)

        # 1. Búsqueda semántica — validar overlap ≥ 0.40
        resultado = mem.buscar_semantico(texto)
        if resultado and len(resultado) > 30:
            if _overlap(texto, resultado) >= 0.40:
                return resultado

        # 2. Cache exacto de búsquedas web recientes
        query_norm = ''.join(
            ch for ch in unicodedata.normalize('NFD', texto.lower().strip())
            if unicodedata.category(ch) != 'Mn'
        )
        cached = mem.buscar_cache_web(query_norm, max_horas=48)
        if cached and _overlap(texto, cached) >= 0.35:
            return cached

    except Exception:
        pass
    return ''

# capas/capa7/__init__.py
# ================================================
# CAPA 7 — EJECUCIÓN — v2
#
# Flujo:
# 1. Si tipo_respuesta es simple → pasar directo (sin habilidad)
# 2. Detectar si necesita habilidad
# 3. Revisar memoria antes de buscar (evita internet innecesario)
# 4. Ejecutar habilidad si corresponde
# 5. Retornar mejor respuesta
#
# v2:
# — Logs diagnósticos completos
# — Propagación campos v2
# — Bypass para mensajes conversacionales/emocionales
# — Fix búsqueda Sebastian
# ================================================

from capas.capa7.paquete_capa7      import PaqueteCapa7, ResultadoEjecucion
from capas.capa7.detector_habilidad import DetectorHabilidad
from capas.capa7.ejecutor_habilidad import EjecutorHabilidad

_detector = DetectorHabilidad()
_ejecutor  = EjecutorHabilidad()

# Tipos de respuesta que NUNCA necesitan habilidad externa
_TIPOS_SIN_HABILIDAD = {
    'emocional', 'veto_respuesta',
    'matematica_python', 'honestidad_limitacion',
    'presentacion_sebastian',
}


def procesar(paquete_capa6: dict) -> dict:
    try:
        return _procesar_interno(paquete_capa6)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return PaqueteCapa7(
            respuesta_final = paquete_capa6.get('respuesta_final', ''),
            paquete_capa6   = paquete_capa6,
            exitoso         = False,
            error           = str(e),
        ).a_dict()


def _procesar_interno(paquete_capa6: dict) -> dict:

    respuesta_capa6  = paquete_capa6.get('respuesta_final', '')
    decision         = paquete_capa6.get('decision', {})
    tipo_respuesta   = paquete_capa6.get('tipo_respuesta', 'conversacional')
    motor_sugerido   = paquete_capa6.get('motor_sugerido', 'local')
    contiene_codigo  = paquete_capa6.get('contiene_codigo', False)

    # Extraer texto original
    texto_original = _extraer_texto(paquete_capa6)

    # ── BYPASS: mensajes simples nunca necesitan habilidades ──────
    if tipo_respuesta in _TIPOS_SIN_HABILIDAD:
        print(f'  C7 habilidad:  (bypass {tipo_respuesta}) | ejecuto: False')
        return _paquete_directo(respuesta_capa6, paquete_capa6,
                                motor_sugerido, contiene_codigo)

    # ── CHECK clarificación pendiente ─────────────────────────────
    clarificacion = _check_clarificacion(texto_original, paquete_capa6)
    if clarificacion:
        return clarificacion

    # ── 1. Detectar si necesita habilidad ─────────────────────────
    deteccion = _detector.detectar(
        texto          = texto_original,
        decision_final = decision,
        tipo_respuesta = tipo_respuesta,
    )

    # ── 2. No necesita habilidad → pasar C6 ──────────────────────
    if not deteccion['necesita_habilidad']:
        print(f'  C7 habilidad:  | ejecuto: False')
        return _paquete_directo(respuesta_capa6, paquete_capa6,
                                motor_sugerido, contiene_codigo)

    habilidad_id = deteccion.get('habilidad_id', '')
    modo         = deteccion.get('modo', '')
    print(f'  C7 habilidad: {habilidad_id} | modo: {modo or "-"}')

    # ── 3. Revisar memoria — DESACTIVADO (habilidad en rediseño) ─

    # ── 4. Ejecutar habilidad ─────────────────────────────────────
    resultado = _ejecutor.ejecutar(deteccion)
    print(f'  C7 ejecuto: {resultado.ejecuto} | hab: {resultado.habilidad_id}')

    if resultado.ejecuto and resultado.resultado:
        return PaqueteCapa7(
            respuesta_final      = resultado.resultado,
            ejecucion            = resultado,
            tiene_resultado_real = True,
            paquete_capa6        = paquete_capa6,
            motor_sugerido       = motor_sugerido,
            contiene_codigo      = contiene_codigo,
            habilidad_ejecutada  = habilidad_id,
        ).a_dict()

    # ── 5. Habilidad falló → mejor respuesta disponible ──────────
    respuesta_final = (
        resultado.resultado if resultado.resultado else respuesta_capa6
    )
    return PaqueteCapa7(
        respuesta_final      = respuesta_final,
        ejecucion            = resultado,
        tiene_resultado_real = False,
        paquete_capa6        = paquete_capa6,
        motor_sugerido       = motor_sugerido,
        contiene_codigo      = contiene_codigo,
        habilidad_ejecutada  = habilidad_id,
    ).a_dict()


# ══════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════

def _extraer_texto(paquete_capa6: dict) -> str:
    try:
        return (paquete_capa6
                .get('paquete_capa5', {})
                .get('paquete_capa4', {})
                .get('paquete_capa3', {})
                .get('paquete_capa2', {})
                .get('paquete_capa1', {})
                .get('contenido_original', ''))
    except Exception:
        return ''


def _paquete_directo(respuesta: str, paquete_capa6: dict,
                     motor_sugerido: str, contiene_codigo: bool) -> dict:
    return PaqueteCapa7(
        respuesta_final      = respuesta,
        ejecucion            = ResultadoEjecucion(ejecuto=False),
        tiene_resultado_real = False,
        paquete_capa6        = paquete_capa6,
        motor_sugerido       = motor_sugerido,
        contiene_codigo      = contiene_codigo,
    ).a_dict()


def _check_clarificacion(texto: str, paquete_capa6: dict) -> dict | None:
    """Retoma búsquedas pendientes de clarificación."""
    try:
        from biblioteca.habilidades.busqueda.motor_busqueda import (
            _PENDIENTE, _es_respuesta_clarificacion, ejecutar_busqueda
        )
        if texto and _PENDIENTE.get('activo') and _es_respuesta_clarificacion(texto):
            print(f"  C7 ↩ Retomando búsqueda pendiente")
            resultado = ejecutar_busqueda(texto)
            if resultado.get('exitoso'):
                motor = paquete_capa6.get('motor_sugerido', 'local')
                codigo = paquete_capa6.get('contiene_codigo', False)
                return PaqueteCapa7(
                    respuesta_final      = resultado['respuesta'],
                    tiene_resultado_real = True,
                    ejecucion            = ResultadoEjecucion(
                        ejecuto=True,
                        habilidad_id='BUSQUEDA_INTERNET',
                        resultado=resultado['respuesta'],
                    ),
                    paquete_capa6       = paquete_capa6,
                    motor_sugerido      = motor,
                    contiene_codigo     = codigo,
                    habilidad_ejecutada = 'BUSQUEDA_INTERNET',
                ).a_dict()
    except Exception:
        pass
    return None