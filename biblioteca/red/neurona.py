# biblioteca/red/neurona.py
# ================================================
# NEURONA — La unidad base de la red
# Ahora con grounding 9D integrado
# ================================================

import time
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any


@dataclass
class Conexion:
    nodo_destino:       str
    peso:               float
    tipo_relacion:      str
    historial_exito:    float = 0.5
    veces_usada:        int   = 0
    timestamp_creacion: float = field(default_factory=time.time)

    def es_fuerte(self)  -> bool: return self.peso >= 0.7
    def es_media(self)   -> bool: return 0.4 <= self.peso < 0.7
    def es_debil(self)   -> bool: return self.peso < 0.4

    def reforzar(self, cantidad: float = 0.05):
        self.peso = min(1.0, self.peso + cantidad)
        self.veces_usada += 1

    def debilitar(self, cantidad: float = 0.03):
        self.peso = max(0.1, self.peso - cantidad)

    def a_dict(self) -> dict:
        return {
            'nodo_destino':    self.nodo_destino,
            'peso':            self.peso,
            'tipo_relacion':   self.tipo_relacion,
            'historial_exito': self.historial_exito,
            'veces_usada':     self.veces_usada
        }


@dataclass
class NucleoNeurona:
    tipo:                str
    subtipo:             str             = ''
    grounding_base:      float           = 0.5
    dimensiones_activas: List[str]       = field(default_factory=list)
    archivo_real:        Optional[str]   = None
    inmutable:           bool            = False
    datos_extra:         Dict[str, Any]  = field(default_factory=dict)

    # ---- GROUNDING 9D ----
    # Almacenado directamente en el núcleo
    # para acceso rápido sin imports adicionales
    grounding_9d:        Optional[dict]  = None
    grounding_efectivo_9d: Optional[float] = None
    puede_ejecutar_9d:   Optional[bool]  = None
    nivel_comprension_9d: Optional[str]  = None

    def a_dict(self) -> dict:
        base = {
            'tipo':                  self.tipo,
            'subtipo':               self.subtipo,
            'grounding_base':        self.grounding_base,
            'dimensiones_activas':   self.dimensiones_activas,
            'archivo_real':          self.archivo_real,
            'inmutable':             self.inmutable,
        }
        # Incluir grounding 9D si existe
        if self.grounding_9d is not None:
            base['grounding_9d']          = self.grounding_9d
            base['grounding_efectivo_9d'] = self.grounding_efectivo_9d
            base['puede_ejecutar_9d']     = self.puede_ejecutar_9d
            base['nivel_comprension_9d']  = self.nivel_comprension_9d

        # Incluir datos extra
        base.update(self.datos_extra)
        return base


@dataclass
class ConfigActivacion:
    umbral:    float = 0.3
    velocidad: str   = 'media'
    mielina:   bool  = False

    VELOCIDADES = {
        'lenta':     0.25,
        'media':     0.50,
        'rapida':    0.75,
        'inmediata': 1.00
    }

    def factor_velocidad(self) -> float:
        return self.VELOCIDADES.get(self.velocidad, 0.50)

    def a_dict(self) -> dict:
        return {
            'umbral':    self.umbral,
            'velocidad': self.velocidad,
            'mielina':   self.mielina
        }


@dataclass
class MemoriaNeurona:
    veces_usado:          int            = 0
    ultimo_uso:           Optional[float] = None
    contextos_de_uso:     List[str]      = field(default_factory=list)
    resultado_historico:  float          = 0.5

    def registrar_uso(self, contexto: str = '', exito: bool = True):
        self.veces_usado  += 1
        self.ultimo_uso    = time.time()

        if contexto:
            self.contextos_de_uso.append(contexto)
            if len(self.contextos_de_uso) > 20:
                self.contextos_de_uso = self.contextos_de_uso[-20:]

        valor = 1.0 if exito else 0.0
        self.resultado_historico = (
            self.resultado_historico * 0.9 + valor * 0.1
        )

    def a_dict(self) -> dict:
        return {
            'veces_usado':         self.veces_usado,
            'ultimo_uso':          self.ultimo_uso,
            'contextos_de_uso':    self.contextos_de_uso[-5:],
            'resultado_historico': self.resultado_historico
        }


class Neurona:
    """
    La neurona completa de Belladonna.
    Ahora con grounding 9D integrado.
    """

    def __init__(self, id: str, datos: dict):
        self.id = id

        nucleo_datos = datos.get('nucleo', {})

        # Extraer campos conocidos del núcleo
        campos_nucleo = {
            'tipo', 'subtipo', 'grounding_base',
            'dimensiones_activas', 'archivo_real', 'inmutable',
            'grounding_9d', 'grounding_efectivo_9d',
            'puede_ejecutar_9d', 'nivel_comprension_9d'
        }

        self.nucleo = NucleoNeurona(
            tipo=nucleo_datos.get('tipo', 'concepto'),
            subtipo=nucleo_datos.get('subtipo', ''),
            grounding_base=nucleo_datos.get('grounding_base', 0.5),
            dimensiones_activas=nucleo_datos.get('dimensiones_activas', []),
            archivo_real=nucleo_datos.get('archivo_real'),
            inmutable=nucleo_datos.get('inmutable', False),
            # Grounding 9D — se carga si existe
            grounding_9d=nucleo_datos.get('grounding_9d'),
            grounding_efectivo_9d=nucleo_datos.get('grounding_efectivo_9d'),
            puede_ejecutar_9d=nucleo_datos.get('puede_ejecutar_9d'),
            nivel_comprension_9d=nucleo_datos.get('nivel_comprension_9d'),
            # Todo lo demás va a datos_extra
            datos_extra={
                k: v for k, v in nucleo_datos.items()
                if k not in campos_nucleo
            }
        )

        activacion_datos = datos.get('activacion', {})
        self.activacion = ConfigActivacion(
            umbral=activacion_datos.get('umbral', 0.3),
            velocidad=activacion_datos.get('velocidad', 'media'),
            mielina=activacion_datos.get('mielina', False)
        )

        memoria_datos = datos.get('memoria', {})
        self.memoria = MemoriaNeurona(
            veces_usado=memoria_datos.get('veces_usado', 0),
            ultimo_uso=memoria_datos.get('ultimo_uso'),
            contextos_de_uso=memoria_datos.get('contextos_de_uso', []),
            resultado_historico=memoria_datos.get('resultado_historico', 0.5)
        )

        self.conexiones: Dict[str, Conexion] = {}

    def agregar_conexion(
        self, destino_id: str, peso: float, tipo_relacion: str
    ):
        if destino_id in self.conexiones:
            existente = self.conexiones[destino_id]
            if peso > existente.peso:
                existente.peso = peso
        else:
            self.conexiones[destino_id] = Conexion(
                nodo_destino=destino_id,
                peso=peso,
                tipo_relacion=tipo_relacion
            )

    def obtener_conexiones_fuertes(self)   -> List[Conexion]:
        return [c for c in self.conexiones.values() if c.es_fuerte()]

    def obtener_conexiones_medias(self)    -> List[Conexion]:
        return [c for c in self.conexiones.values() if c.es_media()]

    def obtener_conexiones_debiles(self)   -> List[Conexion]:
        return [c for c in self.conexiones.values() if c.es_debil()]

    def obtener_conexiones_ordenadas(self) -> List[Conexion]:
        return sorted(
            self.conexiones.values(),
            key=lambda c: c.peso,
            reverse=True
        )

    def puede_activarse(self, energia: float) -> bool:
        return energia >= self.activacion.umbral

    def grounding_efectivo(self) -> float:
        """
        El grounding efectivo real.
        Prioriza el grounding 9D si está disponible.
        Si no, usa el cálculo simple de base + historial.
        """
        # Si tiene grounding 9D calculado usarlo
        if self.nucleo.grounding_efectivo_9d is not None:
            # Combinar 9D con historial de uso
            g9d  = self.nucleo.grounding_efectivo_9d
            hist = self.memoria.resultado_historico
            return round(g9d * 0.85 + hist * 0.15, 4)

        # Fallback al cálculo simple
        return round(
            self.nucleo.grounding_base * 0.8 +
            self.memoria.resultado_historico * 0.2,
            4
        )

    def tiene_grounding_9d(self) -> bool:
        return self.nucleo.grounding_9d is not None

    def puede_ejecutar(self) -> bool:
        """¿Bell puede actuar genuinamente sobre este nodo?"""
        if self.nucleo.puede_ejecutar_9d is not None:
            return self.nucleo.puede_ejecutar_9d
        # Fallback
        return self.grounding_efectivo() >= 0.6

    def nivel_comprension(self) -> str:
        """Nivel de comprensión genuina de Bell."""
        if self.nucleo.nivel_comprension_9d is not None:
            return self.nucleo.nivel_comprension_9d
        # Fallback
        g = self.grounding_efectivo()
        if g >= 0.85: return 'total'
        if g >= 0.70: return 'profunda'
        if g >= 0.55: return 'funcional'
        if g >= 0.35: return 'parcial'
        if g >= 0.15: return 'superficial'
        return 'desconocido'

    def a_dict(self) -> dict:
        return {
            'id':               self.id,
            'nucleo':           self.nucleo.a_dict(),
            'activacion':       self.activacion.a_dict(),
            'memoria':          self.memoria.a_dict(),
            'conexiones': {
                k: v.a_dict()
                for k, v in self.conexiones.items()
            },
            'grounding_efectivo': self.grounding_efectivo(),
            'tiene_grounding_9d': self.tiene_grounding_9d(),
            'puede_ejecutar':     self.puede_ejecutar(),
            'nivel_comprension':  self.nivel_comprension(),
        }