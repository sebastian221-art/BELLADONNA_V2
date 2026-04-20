# capas/capa6/paquete_capa6.py v2
from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class DecisionFinal:
    tipo:               str   = 'conversacional'
    tono:               str   = 'cercano_natural'
    puede_responder:    bool  = True
    puede_ejecutar:     bool  = False
    certeza:            float = 0.8
    que_sabe:           list  = field(default_factory=list)
    que_no_sabe:        list  = field(default_factory=list)
    que_puede_hacer:    list  = field(default_factory=list)
    que_no_puede_hacer: list  = field(default_factory=list)
    fue_a_zona_desconocimiento: bool = False
    contexto_previo:    list  = field(default_factory=list)
    respuesta_base:     str   = ''  # Bell construye esto. Groq solo pule.

    def a_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass
class PaqueteCapa6:
    decision:         DecisionFinal  = field(default_factory=DecisionFinal)
    respuesta_final:  str            = ''
    fuente_respuesta: str            = 'groq'
    prompt_usado:     str            = ''
    paquete_capa5:    Dict[str, Any] = field(default_factory=dict)
    exitoso:          bool           = True
    error:            Optional[str]  = None

    def a_dict(self) -> dict:
        return {
            'decision':         self.decision.a_dict(),
            'respuesta_final':  self.respuesta_final,
            'fuente_respuesta': self.fuente_respuesta,
            'paquete_capa5':    self.paquete_capa5,
            'exitoso':          self.exitoso,
            'error':            self.error,
        }