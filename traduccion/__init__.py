"""
Paquete de Traducción - Español → Conceptos.

Convierte lenguaje natural español al lenguaje interno de Bell.
"""
from traduccion.analizador_español import AnalizadorEspañol
from traduccion.traductor_entrada import TraductorEntrada

__all__ = [
    'AnalizadorEspañol',
    'TraductorEntrada'
]