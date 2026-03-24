# biblioteca/nodos/tipos/nodo_memoria.py
# ================================================
# NODO MEMORIA — Para memorias y episodios
# Lo que Bell recuerda de conversaciones
# y experiencias pasadas
# ================================================

from biblioteca.nodos.base_nodo import BaseNodo


class NodoMemoria(BaseNodo):
    """
    Nodo para memorias de Belladonna.
    Su grounding sube con el tiempo
    conforme la memoria se consolida.
    """

    @property
    def tipo(self) -> str:
        return 'memoria'

    @property
    def grounding_base(self) -> float:
        return 0.5  # Empieza bajo — crece con tiempo

    @property
    def dimensiones_activas(self):
        return ['conocimiento', 'contexto']

    @property
    def velocidad_activacion(self) -> str:
        return 'media'

    @property
    def umbral_activacion(self) -> float:
        return 0.4