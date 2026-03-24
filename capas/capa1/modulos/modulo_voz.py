# capas/capa1/modulos/modulo_voz.py
# ================================================
# MÓDULO VOZ — Preparado para audio futuro
# Por ahora recibe texto que simula voz
# ================================================

from capas.capa1.modulos.base_modulo import BaseModulo, OutputModulo
from capas.capa1.modulos.modulo_texto import ModuloTexto


class ModuloVoz(BaseModulo):

    def __init__(self):
        self._modulo_texto = ModuloTexto()

    @property
    def tipo(self) -> str:
        return 'voz'

    def _procesar_interno(self, estimulo) -> OutputModulo:
        # Por ahora procesa como texto
        # Cuando se conecte reconocimiento de voz
        # solo se cambia aquí
        resultado = self._modulo_texto.procesar(estimulo)
        resultado.tipo_origen = 'voz'
        resultado.metadata['modo'] = 'texto_simulado'
        resultado.metadata['voz_real'] = False
        return resultado