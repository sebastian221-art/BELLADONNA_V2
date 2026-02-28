"""
Módulo de Red y APIs.
FASE 3 - Red.
"""

from .cliente_http import ClienteHTTP, Respuesta
from .manejador_requests import ManejadorRequests, ConfiguracionAPI

__all__ = [
    'ClienteHTTP',
    'Respuesta',
    'ManejadorRequests',
    'ConfiguracionAPI'
]