# capas/capa7/paquete_capa7.py
# ================================================
# PAQUETE CAPA 7 — El contrato de salida
# ================================================

from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class ResultadoEjecucion:
    ejecuto:       bool  = False
    habilidad_id:  str   = ''
    resultado:     str   = ''
    error:         str   = ''
    fue_a_zona:    bool  = False

    def a_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass
class PaqueteCapa7:
    # La respuesta final — puede ser la de Capa 6
    # o una nueva si hubo ejecución real
    respuesta_final:   str               = ''

    # Si hubo ejecución
    ejecucion:         ResultadoEjecucion = field(
        default_factory=ResultadoEjecucion
    )

    # Para Capa 8 — sabe si usar Groq o no
    tiene_resultado_real: bool           = False
    paquete_capa6:        Dict[str, Any] = field(default_factory=dict)

    exitoso: bool          = True
    error:   Optional[str] = None

    def a_dict(self) -> dict:
        return {
            'respuesta_final':     self.respuesta_final,
            'ejecucion':           self.ejecucion.a_dict(),
            'tiene_resultado_real': self.tiene_resultado_real,
            'paquete_capa6':       self.paquete_capa6,
            'exitoso':             self.exitoso,
            'error':               self.error,
        }