# capas/capa8/registrador_turno.py
# ================================================
# REGISTRADOR DE TURNO — Capa 8
#
# Guarda el registro de lo que pasó en este turno.
# Capa 9 lo usará para actualizar la red neuronal,
# subir dimensiones de crecimiento y aprender.
#
# Sin este registro Capa 9 no tiene nada que
# procesar. Este es el puente entre responder
# y aprender.
# ================================================

import time
from capas.capa8.paquete_capa8 import RegistroTurno


class RegistradorTurno:

    def registrar(
        self,
        texto_usuario:  str,
        respuesta_bell: str,
        paquete_capa7:  dict,
        paquete_capa5:  dict,
    ) -> RegistroTurno:
        """
        Construye el registro completo del turno.
        """
        # Extraer datos de las capas anteriores
        instruccion  = paquete_capa5.get('instruccion', {})
        deliberacion = paquete_capa5.get('deliberacion', {})
        ejecucion    = paquete_capa7.get('ejecucion', {})

        tono_usado    = instruccion.get('tono', 'cercano_natural')
        tipo_mensaje  = instruccion.get('tipo_respuesta', 'conversacional')
        certeza       = instruccion.get('confianza', 0.8)
        hubo_veto     = paquete_capa5.get('veto', False)
        hubo_ejecucion = ejecucion.get('ejecuto', False) if isinstance(ejecucion, dict) else False

        registro = RegistroTurno(
            texto_usuario   = texto_usuario,
            respuesta_bell  = respuesta_bell,
            tono_usado      = tono_usado,
            tipo_mensaje    = tipo_mensaje,
            hubo_ejecucion  = hubo_ejecucion,
            hubo_veto       = hubo_veto,
            certeza         = certeza,
            timestamp       = time.time(),
        )

        # Guardar en buffer de sesión para Capa 9
        self._guardar_en_sesion(registro)

        return registro

    def _guardar_en_sesion(self, registro: RegistroTurno):
        """
        Guarda el registro en el historial de sesión.
        Capa 9 lo leerá para actualizar la red.
        """
        try:
            from capas.capa8.historial_sesion import HistorialSesion
            HistorialSesion.obtener().agregar(registro)
        except Exception:
            pass