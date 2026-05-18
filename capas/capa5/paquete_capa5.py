# capas/capa5/paquete_capa5.py
# ================================================
# PAQUETE CAPA 5 — v2
#
# Contrato de salida de C5 hacia C6.
# NUNCA modificar campos existentes.
#
# v2: Propagación de campos C1/C2/C3/C4
# ================================================

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class InstruccionRespuesta:
    """Instrucciones concretas para Capa 6."""
    tipo_respuesta:      str   = 'conversacional'
    # conversacional / conversacional_groq /
    # informativa / emocional / ejecutiva /
    # tecnica_groq / matematica_python /
    # honestidad_limitacion / veto_respuesta
    tono:                str   = 'cercano_natural'
    confianza:           float = 0.8
    prioridad_emocional: bool  = False
    incluir_nombre:      bool  = True
    nivel_detalle:       str   = 'normal'  # breve / normal / detallado
    recomendacion_sage:  str   = ''
    # Alias para compatibilidad
    @property
    def nivel_confianza(self) -> float:
        return self.confianza

    def a_dict(self) -> dict:
        return {
            'tipo_respuesta':      self.tipo_respuesta,
            'tono':                self.tono,
            'confianza':           self.confianza,
            'prioridad_emocional': self.prioridad_emocional,
            'incluir_nombre':      self.incluir_nombre,
            'nivel_detalle':       self.nivel_detalle,
            'recomendacion_sage':  self.recomendacion_sage,
        }


@dataclass
class PaqueteCapa5:
    # ── Resultado de la deliberación ─────────────────────
    aprobado:    bool = True
    veto:        bool = False
    veto_por:    str  = ''
    veto_razon:  str  = ''

    # ── Instrucciones para C6 ─────────────────────────────
    instruccion: InstruccionRespuesta = field(
        default_factory=InstruccionRespuesta
    )

    # ── Respuesta directa (veto o casos especiales) ───────
    respuesta_directa: Optional[str] = None

    # ── Deliberación completa ─────────────────────────────
    deliberacion: Dict[str, Any] = field(default_factory=dict)

    # ── Paquetes anteriores ───────────────────────────────
    paquete_capa4: Dict[str, Any] = field(default_factory=dict)

    # ── Estado ───────────────────────────────────────────
    exitoso: bool          = True
    error:   Optional[str] = None

    # ── v2: Propagación de C1/C2/C3/C4 ──────────────────
    motor_sugerido:       str  = 'local'
    contiene_codigo:      bool = False
    lenguaje_codigo:      str  = 'ninguno'
    es_pregunta:          bool = False
    complejidad:          str  = 'simple'
    perfil_activacion:    str  = 'conversacional'
    fuente_clasificacion: str  = 'patrones'
    modo_mental:          str  = 'social'

    def a_dict(self) -> dict:
        return {
            'aprobado':            self.aprobado,
            'veto':                self.veto,
            'veto_por':            self.veto_por,
            'veto_razon':          self.veto_razon,
            'instruccion':         self.instruccion.a_dict(),
            'respuesta_directa':   self.respuesta_directa,
            'deliberacion':        self.deliberacion,
            'paquete_capa4':       self.paquete_capa4,
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