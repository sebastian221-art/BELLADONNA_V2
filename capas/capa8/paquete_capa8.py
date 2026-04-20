# capas/capa8/paquete_capa8.py
# ================================================
# PAQUETE CAPA 8 — Expresión Final
# Lo que sale de aquí va directo al usuario.
# Este es el último paquete interno de Bell.
# ================================================

from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class RegistroTurno:
    """
    Registro de lo que pasó en este turno.
    Capa 9 lo usará para aprender.
    """
    texto_usuario:    str   = ''
    respuesta_bell:   str   = ''
    tono_usado:       str   = ''
    tipo_mensaje:     str   = ''
    hubo_ejecucion:   bool  = False
    hubo_veto:        bool  = False
    certeza:          float = 0.8
    timestamp:        float = 0.0

    def a_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass
class PaqueteCapa8:
    # La respuesta final — lo que ve Sebastian
    respuesta_final:  str            = ''

    # Metadatos de la respuesta
    tono_final:       str            = 'cercano_natural'
    tipo_respuesta:   str            = 'conversacional'
    longitud_chars:   int            = 0

    # El registro para Capa 9
    registro_turno:   RegistroTurno  = field(
        default_factory=RegistroTurno
    )

    # Paquetes anteriores
    paquete_capa7:    Dict[str, Any] = field(default_factory=dict)

    exitoso:          bool           = True
    error:            Optional[str]  = None

    def a_dict(self) -> dict:
        return {
            'respuesta_final':  self.respuesta_final,
            'tono_final':       self.tono_final,
            'tipo_respuesta':   self.tipo_respuesta,
            'longitud_chars':   self.longitud_chars,
            'registro_turno':   self.registro_turno.a_dict(),
            'paquete_capa7':    self.paquete_capa7,
            'exitoso':          self.exitoso,
            'error':            self.error,
        }