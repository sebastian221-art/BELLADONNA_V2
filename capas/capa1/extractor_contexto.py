# capas/capa1/extractor_contexto.py
# ================================================
# EXTRACTOR DE CONTEXTO
# Agrega contexto de conversación,
# Sebastian y temporal al paquete
# ================================================

import time
from datetime import datetime
from capas.capa1.paquete_capa1 import ContextoPaquete


class ExtractorContexto:
    """
    Extrae y agrega contexto al paquete.
    El contexto se irá enriqueciendo con el tiempo
    conforme Bell aprenda más sobre Sebastian.
    """

    def __init__(self):
        self._historial_sesion = []
        self._contexto_sebastian = {}
        self._turno_actual = 0

    def extraer(self, contenido_normalizado: dict) -> ContextoPaquete:
        """
        Extrae todo el contexto disponible
        y retorna un ContextoPaquete.
        """
        return ContextoPaquete(
            conversacion=self._contexto_conversacion(
                contenido_normalizado
            ),
            sebastian=self._contexto_sebastian_actual(),
            temporal=self._contexto_temporal()
        )

    def _contexto_conversacion(self, contenido: dict) -> dict:
        """
        Contexto de la conversación actual.
        """
        self._turno_actual += 1

        return {
            'turno': self._turno_actual,
            'historial_reciente': self._historial_sesion[-5:]
                if self._historial_sesion else [],
            'hay_contexto_previo': len(self._historial_sesion) > 0,
            'tipo_origen': contenido.get('tipo_origen', 'texto')
        }

    def _contexto_sebastian_actual(self) -> dict:
        """
        Lo que Bell sabe sobre Sebastian.
        Se enriquece con el tiempo.
        """
        if self._contexto_sebastian:
            return self._contexto_sebastian

        # Contexto base por defecto
        return {
            'nombre': 'Sebastian',
            'conocido': True,
            'estado_emocional': 'desconocido',
            'proyectos_activos': [],
            'preferencias': {}
        }

    def _contexto_temporal(self) -> dict:
        """
        Contexto del momento actual.
        """
        ahora = datetime.now()
        return {
            'timestamp': time.time(),
            'hora': ahora.hour,
            'dia_semana': ahora.weekday(),
            'momento_dia': self._momento_del_dia(ahora.hour)
        }

    def _momento_del_dia(self, hora: int) -> str:
        if 5 <= hora < 12:
            return 'mañana'
        elif 12 <= hora < 18:
            return 'tarde'
        elif 18 <= hora < 22:
            return 'noche'
        else:
            return 'madrugada'

    def agregar_al_historial(self, turno: dict):
        """
        Agrega un turno al historial de la sesión.
        """
        self._historial_sesion.append(turno)
        # Mantener solo los últimos 20 turnos en memoria
        if len(self._historial_sesion) > 20:
            self._historial_sesion = self._historial_sesion[-20:]

    def actualizar_sebastian(self, datos: dict):
        """
        Actualiza el contexto de Sebastian
        cuando Bell aprende algo nuevo sobre él.
        """
        self._contexto_sebastian.update(datos)