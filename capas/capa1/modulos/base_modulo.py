# capas/capa1/modulos/base_modulo.py
# ================================================
# BASE MÓDULO — Clase base para todos los módulos
# Todo módulo de entrada hereda de aquí
# Garantiza que todos produzcan el mismo formato
# ================================================

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class OutputModulo:
    """
    El formato de salida estándar de cualquier módulo.
    Este formato es lo que el Normalizador recibe.
    """
    contenido_limpio: str
    tipo_origen: str
    tono_detectado: str = 'neutral'
    idioma: str = 'es'
    metadata: Dict[str, Any] = field(default_factory=dict)
    contenido_original: str = ''
    exitoso: bool = True
    error: str = ''


class BaseModulo(ABC):
    """
    Clase base que todos los módulos heredan.
    Define los tres métodos obligatorios.
    """

    @property
    @abstractmethod
    def tipo(self) -> str:
        """
        El tipo de entrada que maneja este módulo.
        Ejemplo: 'texto', 'voz', 'imagen'
        """
        pass

    def puede_procesar(self, estimulo) -> bool:
        """
        Verifica si este módulo puede procesar
        el estímulo dado.
        Puede sobrescribirse para lógica específica.
        """
        return True

    @abstractmethod
    def _procesar_interno(self, estimulo) -> OutputModulo:
        """
        La lógica específica de cada módulo.
        Debe implementarse en cada módulo hijo.
        """
        pass

    def procesar(self, estimulo) -> OutputModulo:
        """
        Método público de procesamiento.
        Maneja errores y garantiza que siempre
        se retorne un OutputModulo válido.
        """
        try:
            resultado = self._procesar_interno(estimulo)
            if not isinstance(resultado, OutputModulo):
                raise ValueError(
                    f'El módulo {self.tipo} debe retornar OutputModulo'
                )
            return resultado
        except Exception as e:
            # Nunca falla — retorna output con error marcado
            return OutputModulo(
                contenido_limpio=str(estimulo) if estimulo else '',
                tipo_origen=self.tipo,
                contenido_original=str(estimulo) if estimulo else '',
                exitoso=False,
                error=f'Error en módulo {self.tipo}: {str(e)}'
            )