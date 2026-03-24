# capas/capa3/paquete_capa3.py
# ================================================
# PAQUETE CAPA 3 — El contrato de salida
# Lo que la Capa 3 entrega a la Capa 4
# Este formato NUNCA cambia — solo se expande
# ================================================

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class PaqueteCapa3:
    """
    El paquete completo que sale de la Capa 3.
    Contiene las tres comprensiones simultáneas
    más el análisis de Lyra y Echo.
    """

    # Las tres comprensiones
    comprension: Dict[str, Any] = field(default_factory=dict)

    # Análisis de ambigüedad
    ambiguedad: Dict[str, Any] = field(default_factory=dict)

    # Lectura emocional de Lyra
    lectura_lyra: Dict[str, Any] = field(default_factory=dict)

    # Verificación de coherencia de Echo
    verificacion_echo: Dict[str, Any] = field(default_factory=dict)

    # Gaps detectados
    gaps: List[Dict] = field(default_factory=list)

    # Estado global
    nivel_certeza:    float = 0.0
    lista_para_capa4: bool  = False

    # Paquetes anteriores preservados
    paquete_capa2: Dict[str, Any] = field(default_factory=dict)

    # Estado
    exitoso: bool = True
    error:   Optional[str] = None

    def a_dict(self) -> dict:
        return {
            'comprension':      self.comprension,
            'ambiguedad':       self.ambiguedad,
            'lectura_lyra':     self.lectura_lyra,
            'verificacion_echo': self.verificacion_echo,
            'gaps':             self.gaps,
            'nivel_certeza':    self.nivel_certeza,
            'lista_para_capa4': self.lista_para_capa4,
            'paquete_capa2':    self.paquete_capa2,
            'exitoso':          self.exitoso,
            'error':            self.error
        }