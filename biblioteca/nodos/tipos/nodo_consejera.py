# biblioteca/nodos/tipos/nodo_consejera.py
# ================================================
# NODO CONSEJERA — Neurona representante
# de cada consejera en la red
# Punto de contacto entre la red y el módulo real
# ================================================

from biblioteca.nodos.base_nodo import BaseNodo


class NodoConsejera(BaseNodo):
    """
    Neurona representante de una consejera.
    No contiene la lógica de la consejera —
    es su presencia en la red neuronal.
    """

    @property
    def tipo(self) -> str:
        return 'consejera'

    @property
    def grounding_base(self) -> float:
        return 1.0

    @property
    def dimensiones_activas(self):
        return [
            'ejecutabilidad',
            'conocimiento',
            'confianza',
            'contexto'
        ]

    @property
    def es_inmutable(self) -> bool:
        return True

    @property
    def velocidad_activacion(self) -> str:
        return 'rapida'

    @property
    def umbral_activacion(self) -> float:
        return 0.1

    @property
    def tiene_mielina(self) -> bool:
        return True