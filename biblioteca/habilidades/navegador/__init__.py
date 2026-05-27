"""
Habilidad Navegador — Bell controla el browser como un humano.

Punto de entrada: ejecutar(texto, visible=False)
"""
from biblioteca.habilidades.navegador.motor_navegador import ejecutar, describir_capacidades

# Módulos del navegador supremo (importables, fallback-safe)
from biblioteca.habilidades.navegador.conocimiento_web import ConocimientoWeb
from biblioteca.habilidades.navegador.vista_humana import VistaHumana
from biblioteca.habilidades.navegador.patrones_universales import PatronesUniversales
from biblioteca.habilidades.navegador.detector_api import DetectorApi
from biblioteca.habilidades.navegador.memoria_planes import MemoriaPlanes
from biblioteca.habilidades.navegador.lector_destilador import LectorDestilador
from biblioteca.habilidades.navegador.buscador_inteligente import BuscadorInteligente
from biblioteca.habilidades.navegador.monitor_cambios import MonitorCambios
from biblioteca.habilidades.navegador.investigacion import Investigacion

__all__ = [
    'ejecutar', 'describir_capacidades',
    'ConocimientoWeb', 'VistaHumana', 'PatronesUniversales', 'DetectorApi',
    'MemoriaPlanes', 'LectorDestilador', 'BuscadorInteligente',
    'MonitorCambios', 'Investigacion',
]
