# biblioteca/consejeras/base_consejera.py
# ================================================
# BASE DE TODA CONSEJERA — versión 2
# Ahora con PerfilVida completo (23 groundings)
# ================================================

import time
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from abc import ABC, abstractmethod


@dataclass
class IdentidadConsejera:
    id:             str
    nombre:         str
    es:             str
    existe_para:    str
    especialidad:   str
    puede_vetar:    bool = False
    parte_de:       str  = 'BELL_CORE'
    orden_en_flujo: int  = 0
    valor_principal:      str = ''
    valor_secundario:     str = ''
    valor_que_nunca_viola: str = ''

    def a_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass
class EstadoInterno:
    activacion:          float = 0.0
    foco_actual:         str   = ''
    valores_activados:   List[str]        = field(default_factory=list)
    grounding_activado:  Dict[str, float] = field(default_factory=dict)
    intensidad_señal:    float = 0.5
    dominio_activado:    bool  = False
    ultimo_cambio:       float = field(default_factory=time.time)

    def despertar(self, nivel: float, foco: str):
        self.activacion    = min(1.0, nivel)
        self.foco_actual   = foco
        self.ultimo_cambio = time.time()
        self.dominio_activado = nivel > 0.5

    def activar_valor(self, valor_id: str):
        if valor_id not in self.valores_activados:
            self.valores_activados.append(valor_id)

    def elevar_señal(self, cantidad: float = 0.15):
        self.intensidad_señal = min(1.0, self.intensidad_señal + cantidad)

    def calmar_señal(self):
        self.intensidad_señal = max(0.3, self.intensidad_señal - 0.2)

    def a_dict(self) -> dict:
        return {
            'activacion':         self.activacion,
            'foco_actual':        self.foco_actual,
            'valores_activados':  self.valores_activados,
            'grounding_activado': self.grounding_activado,
            'intensidad_señal':   self.intensidad_señal,
            'dominio_activado':   self.dominio_activado,
        }


@dataclass
class MemoriaConsejera:
    evaluaciones_totales: int        = 0
    aciertos:             int        = 0
    patrones_aprendidos:  List[dict] = field(default_factory=list)
    historial_reciente:   List[dict] = field(default_factory=list)
    tasa_acierto:         float      = 0.5

    def registrar_evaluacion(self, exitosa: bool, contexto: str = ''):
        self.evaluaciones_totales += 1
        if exitosa:
            self.aciertos += 1
        self.tasa_acierto = (
            self.aciertos / self.evaluaciones_totales
            if self.evaluaciones_totales > 0 else 0.5
        )
        self.historial_reciente.append({
            'timestamp': time.time(),
            'exitosa':   exitosa,
            'contexto':  contexto[:100]
        })
        if len(self.historial_reciente) > 20:
            self.historial_reciente = self.historial_reciente[-20:]

    def aprender_patron(self, patron: dict):
        self.patrones_aprendidos.append({**patron, 'aprendido_en': time.time()})
        if len(self.patrones_aprendidos) > 50:
            self.patrones_aprendidos = self.patrones_aprendidos[-50:]

    def a_dict(self) -> dict:
        return {
            'evaluaciones_totales': self.evaluaciones_totales,
            'aciertos':             self.aciertos,
            'tasa_acierto':         self.tasa_acierto,
            'patrones_aprendidos':  len(self.patrones_aprendidos),
        }


@dataclass
class ResultadoConsejera:
    consejera_id:   str
    aprobado:       bool = True
    veto:           bool = False
    veto_razon:     str  = ''
    recomendacion:  str  = ''
    tono_sugerido:  str  = ''
    estado_interno: Optional[EstadoInterno] = None
    confianza:      float = 0.8
    intensidad:     float = 0.5
    observaciones:  List[str]       = field(default_factory=list)
    datos_extra:    Dict[str, Any]  = field(default_factory=dict)

    def a_dict(self) -> dict:
        return {
            'consejera_id':   self.consejera_id,
            'aprobado':       self.aprobado,
            'veto':           self.veto,
            'veto_razon':     self.veto_razon,
            'recomendacion':  self.recomendacion,
            'tono_sugerido':  self.tono_sugerido,
            'confianza':      self.confianza,
            'intensidad':     self.intensidad,
            'observaciones':  self.observaciones,
            'estado_interno': self.estado_interno.a_dict() if self.estado_interno else {},
            'datos_extra':    self.datos_extra,
        }


class BaseConsejera(ABC):
    """
    La base de toda consejera.
    Ahora con PerfilVida completo — 23 groundings.
    Una consejera es un organismo vivo dentro de Bell.
    """

    def __init__(self):
        self.identidad  = self._definir_identidad()
        self.estado     = EstadoInterno()
        self.memoria    = MemoriaConsejera()
        self._grounding = self._definir_grounding()
        self._iniciada  = False
        self.perfil_vida = None  # Se carga en _inicializar

        self._inicializar()

    def _inicializar(self):
        """
        La consejera toma conciencia de sí misma.
        Se conecta a la biblioteca.
        Recibe su PerfilVida completo.
        """
        try:
            from biblioteca import Biblioteca
            biblioteca = Biblioteca.obtener()
            if biblioteca.iniciada:
                existe = biblioteca.red.existe_nodo(self.identidad.id)
                if existe:
                    self._iniciada = True

            # Crear perfil de vida con los 23 groundings
            self._crear_perfil_vida()
            print(f'  ✓ {self.identidad.nombre} — vitalidad: {self.perfil_vida.vitalidad():.2f} ({self.perfil_vida.nivel_vida()})')

        except Exception as e:
            self._iniciada = False
            self._crear_perfil_vida()

    def _crear_perfil_vida(self):
        """Crea el PerfilVida de esta consejera."""
        try:
            from biblioteca.grounding.aplicador_vida import AplicadorVida
            aplicador = AplicadorVida.obtener()
            self.perfil_vida = aplicador.aplicar(
                self.identidad.id,
                'consejera',
                {
                    'nombre':           self.identidad.nombre,
                    'existe_para':      self.identidad.existe_para,
                    'valor_principal':  self.identidad.valor_principal,
                }
            )
            # Guardar el valor principal como genuino
            if self.identidad.valor_principal:
                self._aplicar_valor_al_perfil(
                    self.identidad.valor_principal
                )
        except Exception as e:
            from biblioteca.grounding.tipos_vida import PerfilVida
            self.perfil_vida = PerfilVida(
                organismo_id   = self.identidad.id,
                tipo_organismo = 'consejera'
            )

    def _aplicar_valor_al_perfil(self, valor_id: str):
        """Aplica el valor principal con grounding genuino."""
        try:
            from biblioteca.grounding.tipos_vida import GroundingValor
            self.perfil_vida.valores[valor_id] = GroundingValor(
                comprension       = 1.00,
                conviccion        = 1.00,
                activacion_actual = 0.80,
                profundidad       = 0.95,
                transferencia     = 0.90,
                costo_de_violar   = 1.00,
                internalizacion   = 1.00,
                jerarquia         = 0.90,
                resonancia        = 1.00,
            )
        except Exception:
            pass

    # ==========================================
    # ABSTRACTOS
    # ==========================================

    @abstractmethod
    def _definir_identidad(self) -> IdentidadConsejera:
        pass

    @abstractmethod
    def _definir_grounding(self) -> dict:
        pass

    @abstractmethod
    def evaluar(self, contexto: dict) -> ResultadoConsejera:
        pass

    # ==========================================
    # API PÚBLICA
    # ==========================================

    def quien_soy(self) -> dict:
        """Autoconocimiento genuino — incluye perfil de vida."""
        base = {
            'identidad':         self.identidad.a_dict(),
            'estado_actual':     self.estado.a_dict(),
            'memoria':           self.memoria.a_dict(),
            'grounding_dominio': self._grounding,
            'iniciada':          self._iniciada,
            'nivel_experiencia': self._calcular_nivel_experiencia(),
        }
        if self.perfil_vida:
            base['perfil_vida'] = self.perfil_vida.resumen()
            base['vitalidad']   = self.perfil_vida.vitalidad()
            base['nivel_vida']  = self.perfil_vida.nivel_vida()
        return base

    def grounding_para(self, tipo_situacion: str) -> float:
        return self._grounding.get(tipo_situacion, 0.3)

    def esta_en_su_dominio(self, contexto: dict) -> bool:
        tipo = contexto.get('tipo_mensaje', '')
        return self.grounding_para(tipo) > 0.6

    def sentir_evento(self, evento: str, intensidad: float = 0.1):
        """La consejera experimenta un evento — su estado cambia."""
        if self.perfil_vida:
            self.perfil_vida.evento(evento, intensidad)

    def _despertar(self, nivel: float, foco: str):
        self.estado.despertar(nivel, foco)
        if self.perfil_vida:
            self.perfil_vida.emocional.alerta = min(1.0,
                self.perfil_vida.emocional.alerta + nivel * 0.1
            )

    def _activar_valor(self, valor_id: str):
        self.estado.activar_valor(valor_id)
        if self.perfil_vida and valor_id in self.perfil_vida.valores:
            v = self.perfil_vida.valores[valor_id]
            v.activacion_actual = min(1.0, v.activacion_actual + 0.05)

    def _preservarse(self):
        self.estado.elevar_señal()
        if self.perfil_vida:
            self.perfil_vida.autopreservacion.instinto_continuidad = min(
                1.0,
                self.perfil_vida.autopreservacion.instinto_continuidad + 0.02
            )

    def _fue_escuchada(self):
        self.estado.calmar_señal()
        self.memoria.registrar_evaluacion(True)
        if self.perfil_vida:
            self.perfil_vida.evento('proposito_cumplido', 0.05)

    def _calcular_nivel_experiencia(self) -> str:
        t = self.memoria.tasa_acierto
        n = self.memoria.evaluaciones_totales
        if n < 10:                 return 'nueva'
        if n < 50 and t > 0.6:    return 'aprendiendo'
        if n >= 50 and t > 0.75:  return 'experimentada'
        if n >= 100 and t > 0.85: return 'experta'
        return 'en_desarrollo'

    def _crear_resultado(
        self,
        aprobado:      bool,
        recomendacion: str,
        confianza:     float = 0.8,
        tono:          str   = '',
        observaciones: list  = None,
        datos_extra:   dict  = None,
        veto:          bool  = False,
        veto_razon:    str   = ''
    ) -> ResultadoConsejera:
        resultado = ResultadoConsejera(
            consejera_id   = self.identidad.id,
            aprobado       = aprobado,
            veto           = veto and self.identidad.puede_vetar,
            veto_razon     = veto_razon,
            recomendacion  = recomendacion,
            tono_sugerido  = tono,
            estado_interno = EstadoInterno(
                activacion         = self.estado.activacion,
                foco_actual        = self.estado.foco_actual,
                valores_activados  = list(self.estado.valores_activados),
                grounding_activado = dict(self.estado.grounding_activado),
                intensidad_señal   = self.estado.intensidad_señal,
                dominio_activado   = self.estado.dominio_activado,
            ),
            confianza     = confianza,
            intensidad    = self.estado.intensidad_señal,
            observaciones = observaciones or [],
            datos_extra   = datos_extra or {},
        )
        # Agregar vitalidad al resultado
        if self.perfil_vida:
            resultado.datos_extra['vitalidad_consejera'] = self.perfil_vida.vitalidad()
            resultado.datos_extra['nivel_vida']          = self.perfil_vida.nivel_vida()
        return resultado