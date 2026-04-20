# capas/capa9/generador_resumen.py
# ================================================
# GENERADOR DE RESUMEN — Capa 9
#
# Produce un resumen limpio de la sesión.
# Es la semilla de la memoria persistente futura.
# Cuando llegue la habilidad de memoria,
# este resumen es lo que se guardará entre sesiones.
# ================================================

import time
from capas.capa9.paquete_capa9 import ResumenSesion


class GeneradorResumen:

    def generar(
        self,
        historial_stats:  dict,
        zona_stats:       dict,
        actualizacion:    object,
        timestamp_inicio: float,
    ) -> ResumenSesion:

        total_turnos    = historial_stats.get('total_turnos', 0)
        tipos_mensajes  = historial_stats.get('tipos_mensajes', {})
        tonos_usados    = historial_stats.get('tonos_usados', {})
        hubo_veto       = historial_stats.get('vetos', 0) > 0
        hubo_ejecucion  = historial_stats.get('ejecuciones', 0) > 0

        # Emoción dominante
        emocion_dominante = self._emocion_dominante(tipos_mensajes)

        # Tono dominante
        tono_dominante = 'cercano_natural'
        if tonos_usados:
            tono_dominante = max(tonos_usados, key=tonos_usados.get)

        # Habilidades que se pidieron
        habilidades = list(set(
            zona_stats.get('habilidades_prioritarias', [])
        ))

        return ResumenSesion(
            total_turnos       = total_turnos,
            emocion_dominante  = emocion_dominante,
            tono_dominante     = tono_dominante,
            habilidades_pedidas = habilidades,
            hubo_veto          = hubo_veto,
            hubo_ejecucion     = hubo_ejecucion,
            zona_pendientes    = zona_stats.get('total_pendientes', 0),
            bell_core_subio    = actualizacion.hubo_cambio() if hasattr(actualizacion, 'hubo_cambio') else False,
            timestamp_inicio   = timestamp_inicio,
            timestamp_fin      = time.time(),
        )

    def _emocion_dominante(self, tipos: dict) -> str:
        emociones_neg = (
            tipos.get('expresion_emocional_negativa', 0) +
            tipos.get('emocional', 0)
        )
        emociones_pos = tipos.get('expresion_emocional_positiva', 0)
        saludos       = tipos.get('saludo', 0)

        if emociones_neg > emociones_pos and emociones_neg > 0:
            return 'negativa'
        if emociones_pos > emociones_neg and emociones_pos > 0:
            return 'positiva'
        if saludos > 0:
            return 'neutra_social'
        return 'neutra'