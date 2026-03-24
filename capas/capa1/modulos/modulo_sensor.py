# capas/capa1/modulos/modulo_sensor.py
# ================================================
# MÓDULO SENSOR — Para dispositivos IoT futuros
# Por ahora placeholder
# ================================================

from capas.capa1.modulos.base_modulo import BaseModulo, OutputModulo


class ModuloSensor(BaseModulo):

    @property
    def tipo(self) -> str:
        return 'sensor'

    def _procesar_interno(self, estimulo) -> OutputModulo:
        return OutputModulo(
            contenido_limpio=f'[señal de sensor: {str(estimulo)}]',
            tipo_origen='sensor',
            metadata={
                'modo': 'placeholder',
                'sensor_real': False
            },
            contenido_original=str(estimulo)
        )