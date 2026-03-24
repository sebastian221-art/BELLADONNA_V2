# capas/capa1/modulos/modulo_archivo.py
# ================================================
# MÓDULO ARCHIVO — Procesa archivos subidos
# Detecta el tipo y extrae el contenido
# ================================================

from pathlib import Path
from capas.capa1.modulos.base_modulo import BaseModulo, OutputModulo


class ModuloArchivo(BaseModulo):

    TIPOS_SOPORTADOS = {
        '.txt':  'texto_plano',
        '.py':   'codigo_python',
        '.js':   'codigo_javascript',
        '.md':   'markdown',
        '.json': 'datos_json',
        '.csv':  'datos_csv',
        '.html': 'html'
    }

    @property
    def tipo(self) -> str:
        return 'archivo'

    def _procesar_interno(self, estimulo) -> OutputModulo:
        # estimulo puede ser ruta o contenido
        if isinstance(estimulo, str) and Path(estimulo).exists():
            return self._procesar_ruta(Path(estimulo))
        else:
            # Tratar como contenido directo
            return OutputModulo(
                contenido_limpio=str(estimulo),
                tipo_origen='archivo',
                metadata={'subtipo': 'contenido_directo'},
                contenido_original=str(estimulo)
            )

    def _procesar_ruta(self, ruta: Path) -> OutputModulo:
        extension = ruta.suffix.lower()
        subtipo = self.TIPOS_SOPORTADOS.get(
            extension, 'desconocido'
        )

        try:
            contenido = ruta.read_text(encoding='utf-8')
            return OutputModulo(
                contenido_limpio=contenido,
                tipo_origen='archivo',
                metadata={
                    'subtipo': subtipo,
                    'nombre': ruta.name,
                    'extension': extension,
                    'tamanio': ruta.stat().st_size
                },
                contenido_original=contenido
            )
        except Exception as e:
            return OutputModulo(
                contenido_limpio='',
                tipo_origen='archivo',
                exitoso=False,
                error=f'No se pudo leer el archivo: {str(e)}',
                contenido_original=str(ruta)
            )