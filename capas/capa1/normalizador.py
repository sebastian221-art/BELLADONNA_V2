# capas/capa1/normalizador.py
# ================================================
# NORMALIZADOR UNIVERSAL
# Convierte el output de cualquier módulo
# al formato único e invariable
# ================================================

from capas.capa1.modulos.base_modulo import OutputModulo


class Normalizador:
    """
    Recibe el output de cualquier módulo y
    lo convierte al formato universal.
    El formato de salida es sagrado — nunca cambia.
    """

    def normalizar(self, output_modulo: OutputModulo) -> dict:
        """
        Retorna siempre el mismo formato
        sin importar qué módulo lo produjo.
        """
        if not isinstance(output_modulo, OutputModulo):
            # Si no es OutputModulo crear uno básico
            output_modulo = OutputModulo(
                contenido_limpio=str(output_modulo),
                tipo_origen='texto',
                contenido_original=str(output_modulo)
            )

        return {
            'contenido_limpio':    output_modulo.contenido_limpio,
            'tipo_origen':         output_modulo.tipo_origen,
            'tono_detectado':      output_modulo.tono_detectado,
            'idioma':              output_modulo.idioma,
            'metadata_especifica': output_modulo.metadata,
            'contenido_original':  output_modulo.contenido_original,
            'exitoso':             output_modulo.exitoso,
            'error':               output_modulo.error
        }