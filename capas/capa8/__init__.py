# capas/capa8/__init__.py
# ================================================
# CAPA 8 — EXPRESIÓN FINAL — v3
#
# Prepara la respuesta para el usuario:
#   1. Detectar tipo de respuesta real
#   2. Verificar tono emocional
#   3. Formatear (limpiar/preservar según tipo)
#   4. Registrar turno para C9
#
# v3:
# — Logs diagnósticos
# — Propagación campos v2
# — Detección ampliada de respuestas técnicas
#   (Python, Groq cloud, búsqueda, auto-análisis)
# ================================================

from capas.capa8.paquete_capa8     import PaqueteCapa8, RegistroTurno
from capas.capa8.verificador_tono  import VerificadorTono
from capas.capa8.formateador       import Formateador
from capas.capa8.registrador_turno import RegistradorTurno

_verificador_tono = VerificadorTono()
_formateador      = Formateador()
_registrador      = RegistradorTurno()

# Habilidades cuya respuesta no debe tocarse
_HABILIDADES_SIN_LIMITE = {
    'PYTHON_COMPLETO', 'BUSQUEDA_INTERNET',
    'AUTO_ANALISIS_TOTAL',
}

# Tipos de respuesta que no deben truncarse
_TIPOS_SIN_LIMITE = {
    'tecnica_python', 'tecnica_groq', 'groq_cloud',
    'matematica_python', 'ejecutiva',
}


def procesar(paquete_capa7: dict) -> dict:
    try:
        return _procesar_interno(paquete_capa7)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return PaqueteCapa8(
            respuesta_final = paquete_capa7.get('respuesta_final', ''),
            paquete_capa7   = paquete_capa7,
            exitoso         = False,
            error           = str(e),
        ).a_dict()


def _procesar_interno(paquete_capa7: dict) -> dict:

    respuesta_c7 = paquete_capa7.get('respuesta_final', '')

    # ── Extraer datos del pipeline ─────────────────────────
    paquete_c6 = paquete_capa7.get('paquete_capa6', {})
    paquete_c5 = paquete_c6.get('paquete_capa5', {})
    paquete_c4 = paquete_c5.get('paquete_capa4', {})
    paquete_c3 = paquete_c4.get('paquete_capa3', {})
    paquete_c2 = paquete_c3.get('paquete_capa2', {})
    paquete_c1 = paquete_c2.get('paquete_capa1', {})

    instruccion         = paquete_c5.get('instruccion', {})
    tono_esperado       = instruccion.get('tono', 'cercano_natural')
    tipo_respuesta      = instruccion.get('tipo_respuesta', 'conversacional')
    prioridad_emocional = instruccion.get('prioridad_emocional', False)
    texto_usuario       = paquete_c1.get('contenido_original', '')

    # ── Campos v2 propagados ──────────────────────────────
    motor_sugerido      = paquete_capa7.get('motor_sugerido', 'local')
    contiene_codigo     = paquete_capa7.get('contiene_codigo', False)
    habilidad_ejecutada = paquete_capa7.get('habilidad_ejecutada', '')

    # ── 1. Detectar tipo real de respuesta ────────────────
    ejecucion   = paquete_capa7.get('ejecucion', {})
    tiene_real  = paquete_capa7.get('tiene_resultado_real', False)
    hab_id      = ejecucion.get('habilidad_id', '') if isinstance(ejecucion, dict) else ''
    fuente_c6   = paquete_c6.get('fuente_respuesta', '')

    # Resultado de habilidad real → no truncar
    if tiene_real and hab_id in _HABILIDADES_SIN_LIMITE:
        tipo_respuesta = 'tecnica_python'

    # Groq cloud respondió → no truncar
    if fuente_c6 == 'groq_cloud':
        tipo_respuesta = 'tecnica_groq'

    # Código en la respuesta → no truncar
    if tipo_respuesta not in _TIPOS_SIN_LIMITE:
        if ('```python' in respuesta_c7 or
            ('```' in respuesta_c7 and len(respuesta_c7) > 400)):
            tipo_respuesta = 'tecnica_python'

    # ── 2. Verificar tono ─────────────────────────────────
    if tipo_respuesta in _TIPOS_SIN_LIMITE:
        respuesta_con_tono = respuesta_c7
    else:
        respuesta_con_tono = _verificador_tono.verificar_y_ajustar(
            respuesta           = respuesta_c7,
            tono_esperado       = tono_esperado,
            prioridad_emocional = prioridad_emocional,
        )

    # ── 3. Formatear ──────────────────────────────────────
    respuesta_final = _formateador.formatear(
        respuesta      = respuesta_con_tono,
        tipo_respuesta = tipo_respuesta,
    )

    # ── 4. Registrar turno ────────────────────────────────
    registro = _registrador.registrar(
        texto_usuario       = texto_usuario,
        respuesta_bell      = respuesta_final,
        paquete_capa7       = paquete_capa7,
        paquete_capa5       = paquete_c5,
        habilidad_ejecutada = habilidad_ejecutada,
    )

    # ── 5. Logs ───────────────────────────────────────────
    motor_icon = '🤖' if motor_sugerido == 'groq' else '⚡'
    print(f'  C8 tono_final: {tono_esperado}')
    print(f'  C8 tipo:       {tipo_respuesta} | chars: {len(respuesta_final)}')
    print(f'  C8 motor:      {motor_icon} {motor_sugerido}'
          + (f' | hab: {habilidad_ejecutada}' if habilidad_ejecutada else ''))

    return PaqueteCapa8(
        respuesta_final     = respuesta_final,
        tono_final          = tono_esperado,
        tipo_respuesta      = tipo_respuesta,
        longitud_chars      = len(respuesta_final),
        registro_turno      = registro,
        paquete_capa7       = paquete_capa7,
        motor_sugerido      = motor_sugerido,
        contiene_codigo     = contiene_codigo,
        habilidad_ejecutada = habilidad_ejecutada,
    ).a_dict()