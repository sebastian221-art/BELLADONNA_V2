# capas/capa5/paquete_capa5.py
# ================================================
# PAQUETE CAPA 5 — El contrato de salida
# Lo que la deliberación de las consejeras produce
# Este formato NUNCA cambia — solo se expande
# ================================================

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class InstruccionRespuesta:
    """
    Las instrucciones concretas para Capa 6.
    Sage las produce, Capa 5 las empaqueta.
    """
    tipo_respuesta:      str   = 'conversacional'
    # conversacional / informativa / emocional /
    # ejecutiva / honestidad_limitacion / veto_respuesta
    tono:                str   = 'cercano_natural'
    confianza:           float = 0.8
    prioridad_emocional: bool  = False
    incluir_nombre:      bool  = True
    nivel_detalle:       str   = 'normal'
    # breve / normal / detallado
    recomendacion_sage:  str   = ''

    def a_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass
class PaqueteCapa5:
    """
    El paquete completo que sale de la Capa 5.
    Contiene la deliberación completa de las 8 consejeras
    y las instrucciones para Capa 6.
    """

    # ¿Las consejeras aprobaron?
    aprobado:    bool = True
    veto:        bool = False
    veto_por:    str  = ''
    veto_razon:  str  = ''

    # Instrucciones para Capa 6
    instruccion: InstruccionRespuesta = field(
        default_factory=InstruccionRespuesta
    )

    # Respuesta directa si hay veto o caso especial
    # (Capa 6 la usa si existe, si no genera la propia)
    respuesta_directa: Optional[str] = None

    # La deliberación completa — para diagnóstico
    deliberacion: Dict[str, Any] = field(default_factory=dict)

    # Paquetes anteriores
    paquete_capa4: Dict[str, Any] = field(default_factory=dict)

    # Estado
    exitoso: bool = True
    error:   Optional[str] = None

    def a_dict(self) -> dict:
        return {
            'aprobado':          self.aprobado,
            'veto':              self.veto,
            'veto_por':          self.veto_por,
            'veto_razon':        self.veto_razon,
            'instruccion':       self.instruccion.a_dict(),
            'respuesta_directa': self.respuesta_directa,
            'deliberacion':      self.deliberacion,
            'paquete_capa4':     self.paquete_capa4,
            'exitoso':           self.exitoso,
            'error':             self.error,
        }