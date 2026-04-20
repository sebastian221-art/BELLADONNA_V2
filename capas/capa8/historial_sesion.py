# capas/capa8/historial_sesion.py
# ================================================
# HISTORIAL DE SESIÓN — Capa 8
#
# Almacena todos los turnos de la sesión actual.
# Capa 9 los lee para aprender y actualizar
# la red neuronal de Bell.
#
# Se limpia al reiniciar Bell.
# No es memoria persistente — es memoria de sesión.
# La memoria persistente viene en Capa 9.
# ================================================

from collections import deque
from typing import List


class HistorialSesion:
    _instancia = None

    def __init__(self, max_turnos: int = 50):
        self._turnos: deque = deque(maxlen=max_turnos)
        self._stats = {
            'total_turnos':     0,
            'vetos':            0,
            'ejecuciones':      0,
            'tipos_mensajes':   {},
            'tonos_usados':     {},
        }

    @classmethod
    def obtener(cls) -> 'HistorialSesion':
        if cls._instancia is None:
            cls._instancia = HistorialSesion()
        return cls._instancia

    def agregar(self, registro) -> None:
        """Agrega un turno al historial."""
        self._turnos.append(registro)
        self._actualizar_stats(registro)

    def _actualizar_stats(self, registro) -> None:
        self._stats['total_turnos'] += 1

        if registro.hubo_veto:
            self._stats['vetos'] += 1

        if registro.hubo_ejecucion:
            self._stats['ejecuciones'] += 1

        tipo = registro.tipo_mensaje
        self._stats['tipos_mensajes'][tipo] = (
            self._stats['tipos_mensajes'].get(tipo, 0) + 1
        )

        tono = registro.tono_usado
        self._stats['tonos_usados'][tono] = (
            self._stats['tonos_usados'].get(tono, 0) + 1
        )

    def obtener_todos(self) -> List:
        return list(self._turnos)

    def obtener_ultimos(self, n: int = 5) -> List:
        return list(self._turnos)[-n:]

    def obtener_stats(self) -> dict:
        return dict(self._stats)

    def tiene_turnos(self) -> bool:
        return len(self._turnos) > 0

    def limpiar(self) -> None:
        self._turnos.clear()
        self._stats = {
            'total_turnos':   0,
            'vetos':          0,
            'ejecuciones':    0,
            'tipos_mensajes': {},
            'tonos_usados':   {},
        }