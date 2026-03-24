# biblioteca/nodos/base_nodo.py
# ================================================
# BASE NODO — Clase base para crear nodos
# Garantiza que todos los nodos tengan
# la estructura mínima correcta
# ================================================

from abc import ABC, abstractmethod
from typing import List


class BaseNodo(ABC):
    """
    Clase base para todos los tipos de nodos.
    Garantiza que la anatomía sea siempre correcta.
    """

    @property
    @abstractmethod
    def tipo(self) -> str:
        """El tipo de este nodo."""
        pass

    @property
    def subtipo(self) -> str:
        return ''

    @property
    def grounding_base(self) -> float:
        return 0.5

    @property
    def dimensiones_activas(self) -> List[str]:
        return ['conocimiento']

    @property
    def es_inmutable(self) -> bool:
        return False

    @property
    def velocidad_activacion(self) -> str:
        return 'media'

    @property
    def umbral_activacion(self) -> float:
        return 0.3

    @property
    def tiene_mielina(self) -> bool:
        return self.grounding_base >= 0.9

    def construir_datos(self, id_nodo: str, **extra) -> dict:
        """
        Construye el diccionario de datos del nodo.
        Garantiza que siempre tenga la estructura correcta.
        """
        nucleo = {
            'tipo':                self.tipo,
            'subtipo':             self.subtipo,
            'grounding_base':      self.grounding_base,
            'dimensiones_activas': self.dimensiones_activas,
            'archivo_real':        None,
            'inmutable':           self.es_inmutable,
        }
        nucleo.update(extra)

        return {
            'id': id_nodo,
            'nucleo': nucleo,
            'activacion': {
                'umbral':    self.umbral_activacion,
                'velocidad': self.velocidad_activacion,
                'mielina':   self.tiene_mielina
            },
            'memoria': {
                'veces_usado':        0,
                'ultimo_uso':         None,
                'contextos_de_uso':   [],
                'resultado_historico': self.grounding_base
            }
        }