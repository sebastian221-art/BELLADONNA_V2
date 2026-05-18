# capas/capa8/formateador.py
# ================================================
# FORMATEADOR — v3
#
# Longitudes ajustadas:
#   conversacional:  500 chars (aumentado de 300)
#   emocional:       350 chars
#   informativa:     800 chars
#   ejecutiva:       600 chars
#   tecnica_python:  SIN LÍMITE
#   tecnica_groq:    SIN LÍMITE
#   groq_cloud:      SIN LÍMITE
#   matematica_python: 100 chars (resultado puro)
# ================================================

import re

_LONGITUD_MAX = {
    'conversacional':        500,
    'conversacional_groq':   600,
    'emocional':             350,
    'informativa':           800,
    'ejecutiva':             600,
    'honestidad_limitacion': 250,
    'veto_respuesta':        250,
    # Sin límite — respuesta experta completa
    'tecnica_python':        99999,
    'tecnica_groq':          99999,
    'groq_cloud':            99999,
    'ejecutiva_groq':        99999,
    # Matemáticas — solo el resultado
    'matematica_python':     150,
    'default':               500,
}


class Formateador:

    def formatear(self, respuesta: str, tipo_respuesta: str) -> str:
        if not respuesta:
            return respuesta

        # ── Sin límite: preservar TODO ─────────────────────
        if tipo_respuesta in (
            'tecnica_python', 'tecnica_groq', 'groq_cloud', 'ejecutiva_groq'
        ):
            return self._normalizar_espacios_suave(respuesta).strip()

        # ── Conversacional: limpiar markdown, ajustar ─────
        resultado = self._limpiar_markdown(respuesta)
        resultado = self._normalizar_espacios(resultado)
        resultado = self._ajustar_longitud(resultado, tipo_respuesta)
        resultado = self._capitalizar(resultado)
        return resultado.strip()

    def _limpiar_markdown(self, texto: str) -> str:
        """Solo para respuestas conversacionales — NO para código."""
        texto = re.sub(r'\*\*(.+?)\*\*', r'\1', texto)
        texto = re.sub(r'\*(.+?)\*',     r'\1', texto)
        texto = re.sub(r'`(.+?)`',       r'\1', texto)
        texto = re.sub(r'^#{1,6}\s+',    '',    texto, flags=re.MULTILINE)
        texto = re.sub(r'^\s*[-•]\s+',   '',    texto, flags=re.MULTILINE)
        texto = re.sub(r'^\s*\d+\.\s+',  '',    texto, flags=re.MULTILINE)
        return texto

    def _normalizar_espacios(self, texto: str) -> str:
        resultado = re.sub(r' {2,}',      ' ',    texto)
        resultado = re.sub(r'\n{3,}',     '\n\n', resultado)
        resultado = re.sub(r' ([.,;:!?])', r'\1', resultado)
        return resultado.strip()

    def _normalizar_espacios_suave(self, texto: str) -> str:
        """Para técnico: solo normalizar newlines extra.
        La indentación del código es sagrada."""
        return re.sub(r'\n{4,}', '\n\n\n', texto)

    def _ajustar_longitud(self, texto: str, tipo: str) -> str:
        max_chars = _LONGITUD_MAX.get(tipo, _LONGITUD_MAX['default'])
        if len(texto) <= max_chars:
            return texto
        truncado     = texto[:max_chars]
        ultimo_punto = max(
            truncado.rfind('.'), truncado.rfind('!'), truncado.rfind('?')
        )
        if ultimo_punto > max_chars * 0.6:
            return texto[:ultimo_punto + 1]
        return truncado.rstrip() + '.'

    def _capitalizar(self, texto: str) -> str:
        if not texto:
            return texto
        return texto[0].upper() + texto[1:]