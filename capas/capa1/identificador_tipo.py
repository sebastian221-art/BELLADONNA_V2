# capas/capa1/identificador_tipo.py
# ================================================
# IDENTIFICADOR DE TIPO — El portero de la Capa 1
# Detecta qué tipo de estímulo llegó
# Lo enruta al módulo correcto
# ================================================

from pathlib import Path


class IdentificadorTipo:
    """
    Detecta el tipo de estímulo y lo enruta.
    No procesa contenido — solo identifica y enruta.
    Si no reconoce el tipo usa texto como fallback.
    """

    EXTENSIONES_IMAGEN = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
    EXTENSIONES_ARCHIVO = {
        '.txt', '.py', '.js', '.md', '.json',
        '.csv', '.html', '.pdf', '.docx'
    }

    def identificar(self, estimulo) -> str:
        """
        Retorna el tipo del estímulo.
        Siempre retorna algo — nunca falla.
        """
        if estimulo is None:
            return 'texto'

        # Diccionario con tipo explícito
        if isinstance(estimulo, dict):
            return self._identificar_dict(estimulo)

        # String — puede ser texto o ruta de archivo
        if isinstance(estimulo, str):
            return self._identificar_string(estimulo)

        # Bytes — probablemente imagen o archivo
        if isinstance(estimulo, bytes):
            return 'imagen'

        # Por defecto texto
        return 'texto'

    def _identificar_dict(self, estimulo: dict) -> str:
        """
        Identifica estímulos que vienen como diccionario.
        """
        tipo_explicito = estimulo.get('tipo')
        if tipo_explicito in (
            'texto', 'voz', 'imagen', 'archivo',
            'sensor', 'sistema'
        ):
            return tipo_explicito

        # Detectar por contenido del dict
        if 'audio' in estimulo or 'transcripcion' in estimulo:
            return 'voz'
        if 'imagen_base64' in estimulo or 'imagen_ruta' in estimulo:
            return 'imagen'
        if 'señal' in estimulo or 'sensor_id' in estimulo:
            return 'sensor'
        if 'evento_interno' in estimulo or 'origen_bell' in estimulo:
            return 'sistema'
        if 'mensaje' in estimulo or 'texto' in estimulo:
            return 'texto'

        return 'texto'

    def _identificar_string(self, estimulo: str) -> str:
        """
        Identifica strings — texto o ruta de archivo.
        """
        # Verificar si es una ruta de archivo existente
        ruta = Path(estimulo)
        if ruta.exists() and ruta.is_file():
            extension = ruta.suffix.lower()
            if extension in self.EXTENSIONES_IMAGEN:
                return 'imagen'
            if extension in self.EXTENSIONES_ARCHIVO:
                return 'archivo'

        # Si parece una ruta pero no existe — texto
        return 'texto'