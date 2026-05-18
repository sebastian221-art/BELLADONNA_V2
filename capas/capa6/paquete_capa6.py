# capas/capa6/paquete_capa6.py
# ================================================
# PAQUETE CAPA 6 — v3
#
# Contrato de salida de C6 hacia C7.
# v3: Propagación de campos v2 + tipo_respuesta
# ================================================

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class DecisionFinal:
    """Lo que Python decidió — nunca cambia después."""
    tipo:               str   = 'conversacional'
    tono:               str   = 'cercano_natural'
    puede_responder:    bool  = True
    puede_ejecutar:     bool  = False
    certeza:            float = 0.8
    que_sabe:           List  = field(default_factory=list)
    que_no_sabe:        List  = field(default_factory=list)
    que_puede_hacer:    List  = field(default_factory=list)
    que_no_puede_hacer: List  = field(default_factory=list)
    fue_a_zona_desconocimiento: bool = False
    contexto_previo:    List  = field(default_factory=list)
    respuesta_base:     str   = ''

    def a_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass
class PaqueteCapa6:
    decision:         DecisionFinal  = field(default_factory=DecisionFinal)
    respuesta_final:  str            = ''
    fuente_respuesta: str            = 'groq'
    # fuente: base_python / groq / groq_cloud / veto_capa5 / error
    prompt_usado:     str            = ''
    paquete_capa5:    Dict[str, Any] = field(default_factory=dict)
    exitoso:          bool           = True
    error:            Optional[str]  = None
    # v3 propagación
    motor_sugerido:   str            = 'local'
    contiene_codigo:  bool           = False
    tipo_respuesta:   str            = 'conversacional'
    modo_mental:      str            = 'social'

    def a_dict(self) -> dict:
        return {
            'decision':         self.decision.a_dict(),
            'respuesta_final':  self.respuesta_final,
            'fuente_respuesta': self.fuente_respuesta,
            'paquete_capa5':    self.paquete_capa5,
            'exitoso':          self.exitoso,
            'error':            self.error,
            'motor_sugerido':   self.motor_sugerido,
            'contiene_codigo':  self.contiene_codigo,
            'tipo_respuesta':   self.tipo_respuesta,
            'modo_mental':      self.modo_mental,
        }