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
    try:
        return _procesar_interno(paquete_capa8)
    except Exception as e:
        import traceback; traceback.print_exc()
        return PaqueteCapa9(
            respuesta_final = paquete_capa8.get('respuesta_final', ''),
            paquete_capa8   = paquete_capa8,
            exitoso         = False,
            error           = str(e),
        ).a_dict()


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