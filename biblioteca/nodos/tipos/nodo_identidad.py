# biblioteca/nodos/tipos/nodo_identidad.py
# ================================================
# NODO IDENTIDAD — Para lo que define a Bell
# Los más protegidos de la red
# BELL_CORE y todo lo que forma su ser
# ================================================

from biblioteca.nodos.base_nodo import BaseNodo


class NodoIdentidad(BaseNodo):
    """
    Nodo para elementos de identidad de Bell.
    Son los más protegidos de la red.
    No se pueden eliminar.
    """

    @property
    def tipo(self) -> str:
        return 'identidad'

    @property
    def grounding_base(self) -> float:
        return 1.0

    @property
    def dimensiones_activas(self):
        return [
            'ejecutabilidad',
            'conocimiento',
            'confianza',
            'identidad',
            'contexto'
        ]

    @property
    def es_inmutable(self) -> bool:
        return True

    @property
    def velocidad_activacion(self) -> str:
        return 'inmediata'

    @property
    def umbral_activacion(self) -> float:
        return 0.0  # Siempre disponible

    @property
    def tiene_mielina(self) -> bool:
        return True