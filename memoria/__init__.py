"""
Paquete de Memoria Persistente - Fase 2.

Permite a Bell guardar y recuperar información entre sesiones.

Componentes:
- GestorMemoria: Interfaz principal de alto nivel
- AlmacenJSON: Implementación de persistencia en JSON
- tipos_memoria: Enumeraciones y tipos de datos
"""
from memoria.gestor_memoria import GestorMemoria
from memoria.almacen import AlmacenJSON
from memoria.tipos_memoria import TipoMemoria

__all__ = [
    'GestorMemoria',
    'AlmacenJSON',
    'TipoMemoria'
]