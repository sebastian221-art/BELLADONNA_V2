# capas/capa4/paquete_capa4.py
# ================================================
# PAQUETE CAPA 4 — v2
#
# Contrato de salida de C4 hacia C5.
# NUNCA modificar campos existentes.
#
# v2: Propagación de campos C1/C2/C3
# ================================================

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class RecursosDisponibles:
    nodos_activos:          int        = 0
    nodos_primarios:        int        = 0
    nodos_secundarios:      int        = 0
    tiene_habilidades:      bool       = False
    habilidades_ids:        List[str]  = field(default_factory=list)
    grounding_promedio:     float      = 0.0
    vocabulario_suficiente: bool       = True
    gaps_criticos:          List[str]  = field(default_factory=list)

    def a_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass
class EvaluacionCapacidad:
    puede_responder:  bool  = True
    puede_ejecutar:   bool  = False
    nivel_confianza:  float = 0.7
    tipo_respuesta:   str   = 'conversacional'
    # tipos: conversacional / conversacional_groq /
    #        informativa / emocional / ejecutiva /
    #        tecnica_groq / matematica_python /
    #        honestidad_limitacion
    alternativa:      str   = ''
    razon_limitacion: str   = ''

    def a_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass
class EvaluacionRiesgo:
    nivel:                str       = 'ninguno'
    # ninguno / bajo / medio / alto / critico
    señales:              List[str] = field(default_factory=list)
    requiere_veto:        bool      = False
    principios_en_riesgo: List[str] = field(default_factory=list)
    confianza_evaluacion: float     = 0.9

    def a_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass
class PaqueteCapa4:
    # ── Contexto para GestorConsejeras ───────────────────
    contexto_consejeras: Dict[str, Any] = field(default_factory=dict)

    # ── Evaluaciones ─────────────────────────────────────
    recursos:  RecursosDisponibles = field(default_factory=RecursosDisponibles)
    capacidad: EvaluacionCapacidad = field(default_factory=EvaluacionCapacidad)
    riesgo:    EvaluacionRiesgo    = field(default_factory=EvaluacionRiesgo)

    # ── Decisión de continuar ─────────────────────────────
    lista_para_capa5: bool = False
    razon_bloqueo:    str  = ''

    # ── Resumen ejecutivo ─────────────────────────────────
    resumen_situacion: str = ''

    # ── Paquetes anteriores ───────────────────────────────
    paquete_capa3: Dict[str, Any] = field(default_factory=dict)

    # ── Estado ───────────────────────────────────────────
    exitoso: bool          = True
    error:   Optional[str] = None

    # ── v2: Propagación de C1/C2/C3 ──────────────────────
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
            'contexto_consejeras': self.contexto_consejeras,
            'recursos':            self.recursos.a_dict(),
            'capacidad':           self.capacidad.a_dict(),
            'riesgo':              self.riesgo.a_dict(),
            'lista_para_capa5':    self.lista_para_capa5,
            'razon_bloqueo':       self.razon_bloqueo,
            'resumen_situacion':   self.resumen_situacion,
            'paquete_capa3':       self.paquete_capa3,
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