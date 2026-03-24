# biblioteca/nodos/tipos/nodo_habilidad.py
# ================================================
# NODO HABILIDAD — Para habilidades ejecutables
# Tiene referencia al archivo que ejecuta
# Su grounding sube con el uso exitoso
# ================================================

from biblioteca.nodos.base_nodo import BaseNodo


class NodoHabilidad(BaseNodo):
    """
    Nodo para habilidades ejecutables de Bell.
    Cuando se activa Bell puede ejecutar
    la habilidad que representa.
    """

    @property
    def tipo(self) -> str:
        return 'habilidad'

    @property
    def grounding_base(self) -> float:
        return 0.8

    @property
    def dimensiones_activas(self):
        return [
            'ejecutabilidad',
            'conocimiento',
            'verificabilidad'
        ]

    @property
    def velocidad_activacion(self) -> str:
        return 'rapida'

    @property
    def umbral_activacion(self) -> float:
        return 0.4