# capas/capa9/paquete_capa9.py
# ================================================
# PAQUETE CAPA 9 — Integración
# El último paquete del flujo de Bell.
# ================================================

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class ActualizacionBellCore:
    """
    Qué dimensiones de BELL_CORE se actualizaron
    en esta sesión y cuánto subieron.
    """
    accion:        float = 0.0
    relaciones:    float = 0.0
    crecimiento:   float = 0.0
    integridad:    float = 0.0
    descripcion:   str   = ''

    def a_dict(self) -> dict:
        return self.__dict__.copy()

    def hubo_cambio(self) -> bool:
        return any([
            self.accion > 0, self.relaciones > 0,
            self.crecimiento > 0, self.integridad > 0,
        ])


@dataclass
class ResumenSesion:
    """
    Lo más importante de esta sesión.
    Semilla de la memoria persistente futura.
    """
    total_turnos:       int   = 0
    emocion_dominante:  str   = 'neutra'
    tono_dominante:     str   = 'cercano_natural'
    habilidades_pedidas: List[str] = field(default_factory=list)
    hubo_veto:          bool  = False
    hubo_ejecucion:     bool  = False
    zona_pendientes:    int   = 0
    bell_core_subio:    bool  = False
    timestamp_inicio:   float = 0.0
    timestamp_fin:      float = 0.0

    def a_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass
class PaqueteCapa9:
    # La respuesta final — idéntica a Capa 8
    # Capa 9 no cambia la respuesta, solo integra
    respuesta_final:    str                = ''

    # Lo que cambió en Bell
    actualizacion:      ActualizacionBellCore = field(
        default_factory=ActualizacionBellCore
    )

    # El resumen de la sesión
    resumen_sesion:     ResumenSesion      = field(
        default_factory=ResumenSesion
    )

    # Paquete anterior
    paquete_capa8:      Dict[str, Any]     = field(default_factory=dict)

    exitoso:            bool               = True
    error:              Optional[str]      = None

    def a_dict(self) -> dict:
        return {
            'respuesta_final':  self.respuesta_final,
            'actualizacion':    self.actualizacion.a_dict(),
            'resumen_sesion':   self.resumen_sesion.a_dict(),
            'paquete_capa8':    self.paquete_capa8,
            'exitoso':          self.exitoso,
            'error':            self.error,
        }