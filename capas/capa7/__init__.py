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