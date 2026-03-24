# biblioteca/nodos/tipos/nodo_concepto.py
# ================================================
# NODO CONCEPTO — Para conceptos puros
# Vocabulario, ideas, relaciones abstractas
# ================================================

from biblioteca.nodos.base_nodo import BaseNodo


class NodoConcepto(BaseNodo):
    """
    Nodo para conceptos del vocabulario de Bell.
    Son los bloques básicos de comprensión.
    """

    @property
    def tipo(self) -> str:
        return 'concepto'

    @property
    def subtipo(self) -> str:
        return 'vocabulario'

    @property
    def grounding_base(self) -> float:
        return 0.6

    @property
    def dimensiones_activas(self):
        return ['conocimiento', 'contexto']

    @property
    def velocidad_activacion(self) -> str:
        return 'media'

    @property
    def umbral_activacion(self) -> float:
        return 0.35