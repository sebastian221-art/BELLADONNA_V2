# capas/capa1/modulos/modulo_texto.py
# ================================================
# MÓDULO TEXTO — El más importante
# Limpia texto, detecta tono e idioma
# ================================================

import re
from capas.capa1.modulos.base_modulo import BaseModulo, OutputModulo


class ModuloTexto(BaseModulo):

    @property
    def tipo(self) -> str:
        return 'texto'

    def _procesar_interno(self, estimulo) -> OutputModulo:
        texto = str(estimulo) if estimulo else ''
        original = texto

        # Limpiar caracteres innecesarios
        texto_limpio = self._limpiar(texto)

        # Detectar tono
        tono = self._detectar_tono(texto)

        # Detectar idioma básico
        idioma = self._detectar_idioma(texto)

        return OutputModulo(
            contenido_limpio=texto_limpio,
            tipo_origen='texto',
            tono_detectado=tono,
            idioma=idioma,
            metadata={
                'longitud_original': len(original),
                'tiene_mayusculas': any(c.isupper() for c in original),
                'signos_exclamacion': original.count('!'),
                'signos_pregunta': original.count('?')
            },
            contenido_original=original
        )

    def _limpiar(self, texto: str) -> str:
        # Normalizar espacios
        texto = re.sub(r'\s+', ' ', texto)
        # Eliminar caracteres de control
        texto = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', texto)
        return texto.strip()

    def _detectar_tono(self, texto: str) -> str:
        texto_lower = texto.lower()

        # Urgencia
        palabras_urgencia = [
            'urgente', 'rapido', 'ahora', 'inmediatamente',
            'ya', 'pronto', '!', 'URGENTE'
        ]
        if any(p in texto for p in palabras_urgencia):
            return 'urgente'

        # Técnico
        palabras_tecnicas = [
            'función', 'clase', 'archivo', 'código',
            'error', 'bug', 'import', 'def ', 'class '
        ]
        if any(p in texto_lower for p in palabras_tecnicas):
            return 'tecnico'

        # Emocional
        palabras_emocionales = [
            'siento', 'pienso', 'creo', 'me gusta',
            'me preocupa', 'estoy', 'me alegra'
        ]
        if any(p in texto_lower for p in palabras_emocionales):
            return 'emocional'

        return 'neutral'

    def _detectar_idioma(self, texto: str) -> str:
        # Detección básica por caracteres típicos del español
        caracteres_es = set('áéíóúüñ¿¡')
        palabras_es = {
            'el', 'la', 'los', 'las', 'de', 'en', 'que',
            'y', 'a', 'un', 'una', 'es', 'se', 'no', 'con'
        }

        texto_lower = texto.lower()
        palabras = set(texto_lower.split())

        if (any(c in texto_lower for c in caracteres_es) or
                len(palabras & palabras_es) >= 2):
            return 'es'

        return 'es'  # Default español por ahora