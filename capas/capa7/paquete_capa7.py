# capas/capa7/paquete_capa7.py
# ================================================
# PAQUETE CAPA 7 — v2
# Contrato de salida de C7 hacia C8.
# v2: Propagación de campos v2
# ================================================

from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class ResultadoEjecucion:
    ejecuto:      bool = False
    habilidad_id: str  = ''
    resultado:    str  = ''
    error:        str  = ''
    fue_a_zona:   bool = False

    def a_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass
class PaqueteCapa7:
    respuesta_final:      str               = ''
    ejecucion:            ResultadoEjecucion = field(
        default_factory=ResultadoEjecucion
    )
    tiene_resultado_real: bool              = False
    paquete_capa6:        Dict[str, Any]    = field(default_factory=dict)
    exitoso:              bool              = True
    error:                Optional[str]     = None
    # v2
    motor_sugerido:       str               = 'local'
    contiene_codigo:      bool              = False
    habilidad_ejecutada:  str               = ''

    def a_dict(self) -> dict:
        return {
            'respuesta_final':      self.respuesta_final,
            'ejecucion':            self.ejecucion.a_dict(),
            'tiene_resultado_real': self.tiene_resultado_real,
            'paquete_capa6':        self.paquete_capa6,
            'exitoso':              self.exitoso,
            'error':                self.error,
            'motor_sugerido':       self.motor_sugerido,
            'contiene_codigo':      self.contiene_codigo,
            'habilidad_ejecutada':  self.habilidad_ejecutada,
        }