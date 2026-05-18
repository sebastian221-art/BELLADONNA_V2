# capas/capa3/paquete_capa3.py
# ================================================
# PAQUETE CAPA 3 — v2
#
# Contrato de salida de C3 hacia C4.
# NUNCA modificar campos existentes.
#
# v2:
# — Propagación de campos C1-v2
#   (motor_sugerido, contiene_codigo, complejidad)
# — fuente_clasificacion: groq/motor/patrones
# — modo_mental: exploratorio/resolutivo/emocional/tecnico/social
# ================================================

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class PaqueteCapa3:
    # ── Las tres comprensiones ────────────────────────────
    comprension: Dict[str, Any] = field(default_factory=dict)

    # ── Análisis de ambigüedad ────────────────────────────
    ambiguedad: Dict[str, Any] = field(default_factory=dict)

    # ── Lectura emocional de Lyra ─────────────────────────
    lectura_lyra: Dict[str, Any] = field(default_factory=dict)

    # ── Verificación de coherencia de Echo ───────────────
    verificacion_echo: Dict[str, Any] = field(default_factory=dict)

    # ── Gaps detectados ───────────────────────────────────
    gaps: List[Dict] = field(default_factory=list)

    # ── Estado global ─────────────────────────────────────
    nivel_certeza:    float = 0.0
    lista_para_capa4: bool  = False

    # ── Paquetes anteriores preservados ──────────────────
    paquete_capa2: Dict[str, Any] = field(default_factory=dict)

    # ── Estado ───────────────────────────────────────────
    exitoso: bool = True
    error: Optional[str] = None

    # ── v2: Campos propagados de C1/C2 ───────────────────
    motor_sugerido:       str  = 'local'
    contiene_codigo:      bool = False
    lenguaje_codigo:      str  = 'ninguno'
    es_pregunta:          bool = False
    complejidad:          str  = 'simple'
    perfil_activacion:    str  = 'conversacional'

    # ── v2: Metadatos de clasificación ───────────────────
    fuente_clasificacion: str  = 'patrones'  # groq / motor / patrones
    modo_mental:          str  = 'social'    # exploratorio/resolutivo/emocional/tecnico/social

    def a_dict(self) -> dict:
        return {
            'comprension':         self.comprension,
            'ambiguedad':          self.ambiguedad,
            'lectura_lyra':        self.lectura_lyra,
            'verificacion_echo':   self.verificacion_echo,
            'gaps':                self.gaps,
            'nivel_certeza':       self.nivel_certeza,
            'lista_para_capa4':    self.lista_para_capa4,
            'paquete_capa2':       self.paquete_capa2,
            'exitoso':             self.exitoso,
            'error':               self.error,
            # v2
            'motor_sugerido':      self.motor_sugerido,
            'contiene_codigo':     self.contiene_codigo,
            'lenguaje_codigo':     self.lenguaje_codigo,
            'es_pregunta':         self.es_pregunta,
            'complejidad':         self.complejidad,
            'perfil_activacion':   self.perfil_activacion,
            'fuente_clasificacion': self.fuente_clasificacion,
            'modo_mental':         self.modo_mental,
        }