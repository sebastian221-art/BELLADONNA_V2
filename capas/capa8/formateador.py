# capas/capa8/formateador.py
# ================================================
# FORMATEADOR — Capa 8
#
# FIX: _limpiar_markdown más segura — solo elimina
# símbolos de markdown, no borra contenido válido.
# Bell no genera markdown pero si llegara algo
# con formato, se limpia sin perder el texto.
# ================================================

import re

_LONGITUD_MAX = {
    'conversacional':        300,
    'emocional':             250,
    'informativa':           500,
    'ejecutiva':             400,
    'honestidad_limitacion': 200,
    'veto_respuesta':        200,
    'default':               350,
}


class Formateador:

    def formatear(self, respuesta: str, tipo_respuesta: str) -> str:
        if not respuesta:
            return respuesta

        resultado = self._limpiar_markdown(respuesta)
        resultado = self._normalizar_espacios(resultado)
        resultado = self._ajustar_longitud(resultado, tipo_respuesta)
        resultado = self._capitalizar(resultado)

        return resultado.strip()

    def _limpiar_markdown(self, texto: str) -> str:
        # FIX: extraer SOLO el contenido, nunca borrar
        # **negrita** → negrita
        texto = re.sub(r'\*\*(.+?)\*\*', r'\1', texto)
        # *itálica* → itálica (solo si hay contenido dentro)
        texto = re.sub(r'\*(.+?)\*', r'\1', texto)
        # `código` → código
        texto = re.sub(r'`(.+?)`', r'\1', texto)
        # ### Headers → texto limpio
        texto = re.sub(r'^#{1,6}\s+', '', texto, flags=re.MULTILINE)
        # - bullets al inicio de línea → quitar solo el símbolo
        texto = re.sub(r'^\s*[-•]\s+', '', texto, flags=re.MULTILINE)
        # 1. listas numeradas → quitar solo el número
        texto = re.sub(r'^\s*\d+\.\s+', '', texto, flags=re.MULTILINE)
        return texto

    def _normalizar_espacios(self, texto: str) -> str:
        resultado = re.sub(r' {2,}', ' ', texto)
        resultado = re.sub(r'\n{3,}', '\n\n', resultado)
        resultado = re.sub(r' ([.,;:!?])', r'\1', resultado)
        return resultado.strip()

    def _ajustar_longitud(self, texto: str, tipo: str) -> str:
        max_chars = _LONGITUD_MAX.get(tipo, _LONGITUD_MAX['default'])
        if len(texto) <= max_chars:
            return texto

        truncado = texto[:max_chars]
        ultimo_punto = max(
            truncado.rfind('.'),
            truncado.rfind('!'),
            truncado.rfind('?'),
        )
        if ultimo_punto > max_chars * 0.6:
            return texto[:ultimo_punto + 1]

        return truncado.rstrip() + '.'

    def _capitalizar(self, texto: str) -> str:
        if not texto:
            return texto
        return texto[0].upper() + texto[1:]