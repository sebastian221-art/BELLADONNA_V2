# capas/capa1/modulos/modulo_imagen.py
# ================================================
# MÓDULO IMAGEN — Preparado para visión futura
# Por ahora retorna placeholder
# ================================================

from capas.capa1.modulos.base_modulo import BaseModulo, OutputModulo


class ModuloImagen(BaseModulo):

    @property
    def tipo(self) -> str:
        return 'imagen'

    def _procesar_interno(self, estimulo) -> OutputModulo:
        return OutputModulo(
            contenido_limpio='[imagen recibida — procesamiento visual pendiente]',
            tipo_origen='imagen',
            tono_detectado='neutral',
            metadata={
                'modo': 'placeholder',
                'vision_real': False
            },
            contenido_original=str(estimulo)
        )