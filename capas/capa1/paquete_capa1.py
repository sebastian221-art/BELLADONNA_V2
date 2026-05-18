# capas/capa1/paquete_capa1.py
# ================================================
# PAQUETE CAPA 1 — v2
#
# El contrato de salida de C1 hacia C2.
# NUNCA modificar campos existentes.
# Solo agregar campos nuevos.
#
# NUEVO v2:
# — contiene_codigo: bool
# — lenguaje_codigo: str
# — es_pregunta: bool
# — complejidad: str (simple/media/compleja)
# — motor_sugerido: str (hint para C6)
# ================================================

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any


@dataclass
class ConceptoTraducido:
    """Un concepto que Bell identificó en el estímulo."""
    id: str
    texto_original: str
    grounding: float        # 0.0 a 1.0
    certeza: str            # directo / inferido / desconocido
    tipo: str = 'concepto'  # concepto / accion / entidad / relacion


@dataclass
class Desconocido:
    """Una parte del estímulo que Bell no pudo traducir."""
    fragmento: str
    tipo: str               # concepto / habilidad / contexto
    inferencia: Optional[str] = None


@dataclass
class ContextoPaquete:
    """El contexto disponible al procesar este estímulo."""
    conversacion: Dict[str, Any] = field(default_factory=dict)
    sebastian:    Dict[str, Any] = field(default_factory=dict)
    temporal:     Dict[str, Any] = field(default_factory=dict)


@dataclass
class VerificacionSoma:
    """El resultado de la verificación de SOMA."""
    estado: str             # aprobado / retenido / fragmentado
    integridad: bool    = True
    origen_seguro: bool = True
    carga_normal: bool  = True
    notas: List[str]    = field(default_factory=list)


@dataclass
class PaqueteCapa1:
    """
    El paquete completo que sale de la Capa 1.
    Contrato sagrado con la Capa 2.

    v2 agrega campos de análisis de input para que
    las capas siguientes puedan tomar mejores decisiones
    sin tener que re-analizar el texto original.
    """
    # ── Lo que Bell entendió ─────────────────────────────
    conceptos: List[ConceptoTraducido] = field(default_factory=list)
    nivel_certeza_global: float = 0.0

    # ── El original — siempre preservado ─────────────────
    contenido_original: str = ''
    tipo_origen: str = 'texto'

    # ── Información emocional y de tono ──────────────────
    tono_detectado: str = 'neutral'  # neutral/emocional/urgente/tecnico
    idioma: str = 'es'

    # ── Contexto ─────────────────────────────────────────
    contexto: ContextoPaquete = field(default_factory=ContextoPaquete)

    # ── Lo que Bell no pudo traducir ─────────────────────
    desconocidos: List[Desconocido] = field(default_factory=list)

    # ── Verificación de SOMA ─────────────────────────────
    verificacion_soma: VerificacionSoma = field(
        default_factory=VerificacionSoma
    )

    # ── Estado del paquete ───────────────────────────────
    exitoso: bool = True
    error: Optional[str] = None

    # ── NUEVO v2: Análisis del input ─────────────────────
    # Detectado en C1 para que C3, C6, C7 lo usen
    # sin necesidad de re-analizar el texto
    contiene_codigo: bool = False
    lenguaje_codigo: str  = 'ninguno'  # python/javascript/sql/bash/ninguno
    es_pregunta: bool     = False
    complejidad: str      = 'simple'   # simple/media/compleja
    motor_sugerido: str   = 'local'    # local/groq — hint para C6

    # ── Métodos de conveniencia ───────────────────────────

    def tiene_conceptos(self) -> bool:
        return len(self.conceptos) > 0

    def tiene_desconocidos(self) -> bool:
        return len(self.desconocidos) > 0

    def esta_aprobado_por_soma(self) -> bool:
        return self.verificacion_soma.estado == 'aprobado'

    def a_dict(self) -> dict:
        return {
            'conceptos': [
                {
                    'id':              c.id,
                    'texto_original':  c.texto_original,
                    'grounding':       c.grounding,
                    'certeza':         c.certeza,
                    'tipo':            c.tipo,
                }
                for c in self.conceptos
            ],
            'nivel_certeza_global': self.nivel_certeza_global,
            'contenido_original':   self.contenido_original,
            'tipo_origen':          self.tipo_origen,
            'tono_detectado':       self.tono_detectado,
            'idioma':               self.idioma,
            'desconocidos': [
                {
                    'fragmento':  d.fragmento,
                    'tipo':       d.tipo,
                    'inferencia': d.inferencia,
                }
                for d in self.desconocidos
            ],
            'verificacion_soma': {
                'estado':     self.verificacion_soma.estado,
                'integridad': self.verificacion_soma.integridad,
                'notas':      self.verificacion_soma.notas,
            },
            'exitoso': self.exitoso,
            'error':   self.error,
            # v2
            'contiene_codigo':  self.contiene_codigo,
            'lenguaje_codigo':  self.lenguaje_codigo,
            'es_pregunta':      self.es_pregunta,
            'complejidad':      self.complejidad,
            'motor_sugerido':   self.motor_sugerido,
        }