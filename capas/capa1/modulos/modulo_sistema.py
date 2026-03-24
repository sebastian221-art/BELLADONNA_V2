# capas/capa1/modulos/modulo_sistema.py
# ================================================
# MÓDULO SISTEMA — Señales internas de Bell
# Alertas de SOMA, notificaciones entre capas
# ================================================

from capas.capa1.modulos.base_modulo import BaseModulo, OutputModulo


class ModuloSistema(BaseModulo):

    @property
    def tipo(self) -> str:
        return 'sistema'

    def _procesar_interno(self, estimulo) -> OutputModulo:
        datos = estimulo if isinstance(estimulo, dict) else {
            'mensaje': str(estimulo)
        }

        return OutputModulo(
            contenido_limpio=datos.get('mensaje', str(estimulo)),
            tipo_origen='sistema',
            tono_detectado='neutral',
            metadata={
                'origen_interno': datos.get('origen', 'desconocido'),
                'prioridad': datos.get('prioridad', 'normal'),
                'datos': datos
            },
            contenido_original=str(estimulo)
        )