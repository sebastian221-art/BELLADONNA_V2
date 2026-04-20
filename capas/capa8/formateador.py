# capas/capa8/formateador.py
# ================================================
# FORMATEADOR — Capa 8
#
# Limpia la respuesta para que llegue perfecta
# al usuario. Sin artefactos, sin markdown
# innecesario, longitud adecuada.
# ================================================

import re


# Longitudes máximas por tipo de respuesta
_LONGITUD_MAX = {
    'conversacional':      300,
    'emocional':           250,
    'informativa':         500,
    'ejecutiva':           400,
    'honestidad_limitacion': 200,
    'veto_respuesta':      200,
    'default':             350,
}

# Artefactos que no deben aparecer en la respuesta final
_ARTEFACTOS = [
    r'\*\*.*?\*\*',     # **negrita**
    r'\*.*?\*',          # *itálica*
    r'`.*?`',            # `código`
    r'#{1,6}\s',         # # headers
    r'^\s*[-•]\s',       # bullets al inicio de línea
    r'^\s*\d+\.\s',      # listas numeradas
]


class Formateador:

    def formatear(
        self,
        respuesta:     str,
        tipo_respuesta: str,
    ) -> str:
        """
        Aplica formato final a la respuesta.
        """
        if not respuesta:
            return respuesta

        # 1. Limpiar artefactos de markdown
        resultado = self._limpiar_markdown(respuesta)

        # 2. Normalizar espacios y saltos de línea
        resultado = self._normalizar_espacios(resultado)

        # 3. Verificar longitud
        resultado = self._ajustar_longitud(resultado, tipo_respuesta)

        # 4. Capitalizar primera letra si hace falta
        resultado = self._capitalizar(resultado)

        return resultado.strip()

    def _limpiar_markdown(self, texto: str) -> str:
        resultado = texto
        for patron in _ARTEFACTOS:
            # Extraer el contenido sin los símbolos de markdown
            resultado = re.sub(patron, lambda m: self._extraer_contenido(m.group()), resultado, flags=re.MULTILINE)
        return resultado

    def _extraer_contenido(self, match: str) -> str:
        """Extrae el texto limpio de un artefacto markdown."""
        # Remover símbolos de markdown al inicio y final
        limpio = re.sub(r'^[\*#`\-•\d\.>\s]+', '', match)
        limpio = re.sub(r'[\*#`]+$', '', limpio)
        return limpio.strip()

    def _normalizar_espacios(self, texto: str) -> str:
        # Múltiples espacios → uno
        resultado = re.sub(r' {2,}', ' ', texto)
        # Múltiples saltos de línea → máximo uno
        resultado = re.sub(r'\n{3,}', '\n\n', resultado)
        # Espacios antes de puntuación
        resultado = re.sub(r' ([.,;:!?])', r'\1', resultado)
        return resultado.strip()

    def _ajustar_longitud(self, texto: str, tipo: str) -> str:
        max_chars = _LONGITUD_MAX.get(tipo, _LONGITUD_MAX['default'])
        if len(texto) <= max_chars:
            return texto

        # Cortar en el último punto antes del límite
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