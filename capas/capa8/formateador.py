# capas/capa8/formateador.py — v2 con modo técnico Python
# ================================================
# FORMATEADOR — Capa 8
#
# FIX CRÍTICO: 'tecnica_python' no trunca ni borra código.
# Las respuestas del skill Python llegan completas.
#
# LONGITUDES:
#   Conversacional:  300 chars  (respuestas de chat normales)
#   Informativa:     600 chars
#   Ejecutiva:       400 chars
#   Técnica Python:  SIN LÍMITE — Bell responde completo
# ================================================

import re

_LONGITUD_MAX = {
    'conversacional':        300,
    'emocional':             250,
    'informativa':           600,
    'ejecutiva':             400,
    'honestidad_limitacion': 200,
    'veto_respuesta':        200,
    'tecnica_python':        99999,  # Sin límite — respuesta experta completa
    'default':               350,
}


class Formateador:

    def formatear(self, respuesta: str, tipo_respuesta: str) -> str:
        if not respuesta:
            return respuesta

        # ── Modo técnico Python: preservar TODO ───────────
        # No tocar código, no truncar, no limpiar backticks
        if tipo_respuesta == 'tecnica_python':
            return self._normalizar_espacios_suave(respuesta).strip()

        # ── Modo conversacional normal ─────────────────────
        resultado = self._limpiar_markdown(respuesta)
        resultado = self._normalizar_espacios(resultado)
        resultado = self._ajustar_longitud(resultado, tipo_respuesta)
        resultado = self._capitalizar(resultado)
        return resultado.strip()

    def _limpiar_markdown(self, texto: str) -> str:
        """Solo para respuestas conversacionales — NO para Python."""
        texto = re.sub(r'\*\*(.+?)\*\*', r'\1', texto)
        texto = re.sub(r'\*(.+?)\*',     r'\1', texto)
        texto = re.sub(r'`(.+?)`',       r'\1', texto)
        texto = re.sub(r'^#{1,6}\s+',    '',    texto, flags=re.MULTILINE)
        texto = re.sub(r'^\s*[-•]\s+',   '',    texto, flags=re.MULTILINE)
        texto = re.sub(r'^\s*\d+\.\s+',  '',    texto, flags=re.MULTILINE)
        return texto

    def _normalizar_espacios(self, texto: str) -> str:
        resultado = re.sub(r' {2,}',    ' ',    texto)
        resultado = re.sub(r'\n{3,}',   '\n\n', resultado)
        resultado = re.sub(r' ([.,;:!?])', r'\1', resultado)
        return resultado.strip()

    def _normalizar_espacios_suave(self, texto: str) -> str:
        """Para modo técnico: solo normalizar newlines extra.
        NO tocar espacios — la indentación del código es sagrada."""
        resultado = re.sub(r'\n{4,}', '\n\n\n', texto)
        return resultado

    def _ajustar_longitud(self, texto: str, tipo: str) -> str:
        max_chars = _LONGITUD_MAX.get(tipo, _LONGITUD_MAX['default'])
        if len(texto) <= max_chars:
            return texto
        truncado    = texto[:max_chars]
        ultimo_punto = max(truncado.rfind('.'), truncado.rfind('!'), truncado.rfind('?'))
        if ultimo_punto > max_chars * 0.6:
            return texto[:ultimo_punto + 1]
        return truncado.rstrip() + '.'

    def _capitalizar(self, texto: str) -> str:
        if not texto:
            return texto
        return texto[0].upper() + texto[1:]