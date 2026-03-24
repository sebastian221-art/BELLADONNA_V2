# biblioteca/nodos/tipos/nodo_valor.py
# ================================================
# NODO VALOR — Para los 10 valores inmutables
# Nunca se debilita
# Nunca se elimina
# Máxima prioridad en activación
# ================================================

from biblioteca.nodos.base_nodo import BaseNodo


class NodoValor(BaseNodo):
    """
    Nodo para los valores inmutables de Belladonna.
    Tiene el grounding más alto posible.
    Sus conexiones con BELL_CORE son permanentes.
    """

    @property
    def tipo(self) -> str:
        return 'valor'

    @property
    def subtipo(self) -> str:
        return 'inmutable'

    @property
    def grounding_base(self) -> float:
        return 1.0

    @property
    def dimensiones_activas(self):
        return [
            'ejecutabilidad',
            'conocimiento',
            'confianza',
            'identidad'
        ]

    @property
    def es_inmutable(self) -> bool:
        return True  # Los valores NUNCA se eliminan

    @property
    def velocidad_activacion(self) -> str:
        return 'inmediata'

    @property
    def umbral_activacion(self) -> float:
        return 0.1  # Se activa con muy poca energía

    @property
    def tiene_mielina(self) -> bool:
        return True  # Siempre máxima velocidad