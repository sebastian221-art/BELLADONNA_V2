# biblioteca/nodos/registro_tipos.py
# ================================================
# REGISTRO DE TIPOS DE NODOS
# Mapea tipos a sus clases
# Agregar un tipo nuevo = registrarlo aquí
# y crear su clase — nada más
# ================================================

from biblioteca.nodos.tipos.nodo_concepto import NodoConcepto
from biblioteca.nodos.tipos.nodo_valor import NodoValor
from biblioteca.nodos.tipos.nodo_consejera import NodoConsejera
from biblioteca.nodos.tipos.nodo_habilidad import NodoHabilidad
from biblioteca.nodos.tipos.nodo_memoria import NodoMemoria
from biblioteca.nodos.tipos.nodo_identidad import NodoIdentidad

# Mapa de tipos a clases
REGISTRO_TIPOS = {
    'concepto':   NodoConcepto,
    'valor':      NodoValor,
    'consejera':  NodoConsejera,
    'habilidad':  NodoHabilidad,
    'memoria':    NodoMemoria,
    'identidad':  NodoIdentidad,
}


def obtener_clase_nodo(tipo: str):
    """
    Retorna la clase del nodo según su tipo.
    Si el tipo no existe retorna NodoConcepto por defecto.
    """
    return REGISTRO_TIPOS.get(tipo, NodoConcepto)


def crear_nodo_datos(
    tipo: str,
    id_nodo: str,
    **extra
) -> dict:
    """
    Crea el diccionario de datos de un nodo
    usando la clase correcta según su tipo.
    """
    clase = obtener_clase_nodo(tipo)
    instancia = clase()
    return instancia.construir_datos(id_nodo, **extra)


def tipos_disponibles() -> list:
    return list(REGISTRO_TIPOS.keys())