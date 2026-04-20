# capas/capa4/paquete_capa4.py
# ================================================
# PAQUETE CAPA 4 — El contrato de salida
# Lo que la Capa 4 entrega a la Capa 5
# Este formato NUNCA cambia — solo se expande
# ================================================

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class RecursosDisponibles:
    """
    Qué tiene Bell para responder.
    """
    nodos_activos:        int   = 0
    nodos_primarios:      int   = 0
    nodos_secundarios:    int   = 0
    tiene_habilidades:    bool  = False
    habilidades_ids:      List[str] = field(default_factory=list)
    grounding_promedio:   float = 0.0
    vocabulario_suficiente: bool = True
    gaps_criticos:        List[str] = field(default_factory=list)

    def a_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass
class EvaluacionCapacidad:
    """
    ¿Puede Bell hacer lo que se pide?
    """
    puede_responder:     bool  = True
    puede_ejecutar:      bool  = False
    nivel_confianza:     float = 0.7
    tipo_respuesta:      str   = 'conversacional'
    # tipos: conversacional / informativa / emocional /
    #        ejecutiva / honestidad_limitacion
    alternativa:         str   = ''
    razon_limitacion:    str   = ''

    def a_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass
class EvaluacionRiesgo:
    """
    ¿Hay algo que Vega debe revisar?
    """
    nivel:          str   = 'ninguno'
    # ninguno / bajo / medio / alto / critico
    señales:        List[str] = field(default_factory=list)
    requiere_veto:  bool  = False
    principios_en_riesgo: List[str] = field(default_factory=list)
    confianza_evaluacion: float = 0.9

    def a_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass
class PaqueteCapa4:
    """
    El paquete completo que sale de la Capa 4.
    Contiene todo lo que Capa 5 necesita para
    que las consejeras deliberen correctamente.
    """

    # El contexto listo para GestorConsejeras.consultar_todas()
    contexto_consejeras: Dict[str, Any] = field(default_factory=dict)

    # Las evaluaciones
    recursos:    RecursosDisponibles = field(default_factory=RecursosDisponibles)
    capacidad:   EvaluacionCapacidad = field(default_factory=EvaluacionCapacidad)
    riesgo:      EvaluacionRiesgo    = field(default_factory=EvaluacionRiesgo)

    # Decisión de continuar
    lista_para_capa5: bool  = False
    razon_bloqueo:    str   = ''

    # Resumen ejecutivo para las consejeras
    resumen_situacion: str  = ''

    # Paquetes anteriores preservados
    paquete_capa3: Dict[str, Any] = field(default_factory=dict)

    # Estado
    exitoso: bool = True
    error:   Optional[str] = None

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
        }