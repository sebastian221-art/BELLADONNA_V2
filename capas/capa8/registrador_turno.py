# capas/capa8/registrador_turno.py
# ================================================
# REGISTRADOR DE TURNO — v2
#
# Construye el RegistroTurno completo para C9.
# v2: incluye habilidad_ejecutada para que C9
# sepa qué skill se usó y pueda aprender de eso.
# ================================================

import time
from capas.capa8.paquete_capa8 import RegistroTurno


class RegistradorTurno:

    def registrar(
        self,
        texto_usuario:       str,
        respuesta_bell:      str,
        paquete_capa7:       dict,
        paquete_capa5:       dict,
        habilidad_ejecutada: str = '',
    ) -> RegistroTurno:

        instruccion  = paquete_capa5.get('instruccion', {})
        ejecucion    = paquete_capa7.get('ejecucion', {})

        tono_usado      = instruccion.get('tono', 'cercano_natural')
        tipo_mensaje    = instruccion.get('tipo_respuesta', 'conversacional')
        certeza         = instruccion.get('confianza', 0.8)
        hubo_veto       = paquete_capa5.get('veto', False)
        hubo_ejecucion  = (
            ejecucion.get('ejecuto', False)
            if isinstance(ejecucion, dict) else False
        )

        registro = RegistroTurno(
            texto_usuario       = texto_usuario,
            respuesta_bell      = respuesta_bell,
            tono_usado          = tono_usado,
            tipo_mensaje        = tipo_mensaje,
            hubo_ejecucion      = hubo_ejecucion,
            hubo_veto           = hubo_veto,
            certeza             = certeza,
            habilidad_ejecutada = habilidad_ejecutada,
            timestamp           = time.time(),
        )

        self._guardar_en_sesion(registro)
        return registro

    def _guardar_en_sesion(self, registro: RegistroTurno):
        try:
            from capas.capa8.historial_sesion import HistorialSesion
            HistorialSesion.obtener().agregar(registro)
        except Exception:
            pass