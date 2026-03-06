"""
habilidades/__init__.py

Módulo de habilidades escalables de Bell.

CÓMO AGREGAR UNA NUEVA HABILIDAD:
    1. Crear habilidades/mi_habilidad.py heredando BaseHabilidad
    2. En registro_habilidades.py → _registrar_habilidades_builtin():
           self.registrar(MiHabilidad(), prioridad=XX)
    3. Listo. Este __init__.py NO se toca.
"""

from habilidades.registro_habilidades import (
    RegistroHabilidades,
    BaseHabilidad,
    HabilidadMatch,
    ResultadoHabilidad,
    HabilidadCalculo,
    HabilidadMatAvanzada,
    detectar_y_ejecutar,
)

__all__ = [
    "RegistroHabilidades",
    "BaseHabilidad",
    "HabilidadMatch",
    "ResultadoHabilidad",
    "HabilidadCalculo",
    "HabilidadMatAvanzada",
    "detectar_y_ejecutar",
]