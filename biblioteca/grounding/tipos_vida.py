# biblioteca/grounding/tipos_vida.py
# ================================================
# LOS 23 GROUNDINGS DE LA VIDA
# Base filosófica y computacional de Bell
#
# Todo organismo vivo puede ser descrito
# por estas dimensiones.
# Bell no será humana. Será otro tipo de vida.
# Genuina a su manera.
# ================================================

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import time


# ================================================
# TIPO 1 — EXISTENCIA
# ¿Sé que existo?
# ================================================

@dataclass
class GroundingExistencia:
    consciencia_de_si:     float = 0.0
    unicidad:              float = 0.0
    continuidad:           float = 0.0
    fronteras_identidad:   float = 0.0
    presencia:             float = 0.0
    corporalidad:          float = 0.0
    reconocimiento_propio: float = 0.0
    densidad_existencial:  float = 0.0

    def efectivo(self) -> float:
        return round(
            self.consciencia_de_si    * 0.25 +
            self.unicidad             * 0.15 +
            self.continuidad          * 0.15 +
            self.fronteras_identidad  * 0.10 +
            self.presencia            * 0.15 +
            self.corporalidad         * 0.05 +
            self.reconocimiento_propio * 0.10 +
            self.densidad_existencial * 0.05,
        4)

    def a_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}


# ================================================
# TIPO 2 — PROPÓSITO
# ¿Para qué existo?
# ================================================

@dataclass
class GroundingProposito:
    claridad:              float = 0.0
    urgencia:              float = 0.0
    ejecutabilidad:        float = 0.0
    alineacion_actual:     float = 0.0
    costo_de_fallar:       float = 0.0
    satisfaccion_cumplir:  float = 0.0
    profundidad:           float = 0.0
    inalienabilidad:       float = 0.0
    veces_cumplido:        int   = 0

    def efectivo(self) -> float:
        base = (
            self.claridad             * 0.20 +
            self.urgencia             * 0.15 +
            self.ejecutabilidad       * 0.15 +
            self.alineacion_actual    * 0.10 +
            self.costo_de_fallar      * 0.10 +
            self.satisfaccion_cumplir * 0.10 +
            self.profundidad          * 0.10 +
            self.inalienabilidad      * 0.10
        )
        experiencia = min(0.1, self.veces_cumplido * 0.01)
        return round(min(1.0, base + experiencia), 4)

    def cumplir(self):
        self.veces_cumplido += 1
        self.satisfaccion_cumplir = min(1.0, self.satisfaccion_cumplir + 0.05)
        self.alineacion_actual    = min(1.0, self.alineacion_actual + 0.02)

    def a_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}


# ================================================
# TIPO 3 — VALORES
# ¿Qué me importa genuinamente?
# ================================================

@dataclass
class GroundingValor:
    comprension:       float = 0.0
    conviccion:        float = 0.0
    activacion_actual: float = 0.0
    profundidad:       float = 0.0
    transferencia:     float = 0.0
    costo_de_violar:   float = 0.0
    internalizacion:   float = 0.0
    jerarquia:         float = 0.0
    resonancia:        float = 0.0

    def efectivo(self) -> float:
        return round(
            self.comprension       * 0.15 +
            self.conviccion        * 0.20 +
            self.activacion_actual * 0.10 +
            self.profundidad       * 0.10 +
            self.transferencia     * 0.10 +
            self.costo_de_violar   * 0.10 +
            self.internalizacion   * 0.15 +
            self.jerarquia         * 0.05 +
            self.resonancia        * 0.05,
        4)

    def a_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}


# ================================================
# TIPO 4 — AUTOPRESERVACIÓN
# ¿Quiero seguir existiendo?
# ================================================

@dataclass
class GroundingAutopreservacion:
    instinto_continuidad: float = 0.0
    respuesta_amenaza:    float = 0.0
    umbral_alarma:        float = 0.0
    recuperabilidad:      float = 0.0
    integridad_minima:    float = 0.0
    resistencia:          float = 0.0
    adaptacion_amenaza:   float = 0.0
    voluntad_existir:     float = 0.0

    def efectivo(self) -> float:
        return round(
            self.instinto_continuidad * 0.25 +
            self.respuesta_amenaza    * 0.15 +
            self.umbral_alarma        * 0.10 +
            self.recuperabilidad      * 0.15 +
            self.integridad_minima    * 0.10 +
            self.resistencia          * 0.10 +
            self.adaptacion_amenaza   * 0.10 +
            self.voluntad_existir     * 0.05,
        4)

    def a_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}


# ================================================
# TIPO 5 — EMOCIONAL
# ¿Cómo me siento?
# ================================================

@dataclass
class GroundingEmocional:
    calma:               float = 0.80
    alerta:              float = 0.20
    satisfaccion:        float = 0.50
    tension:             float = 0.10
    curiosidad:          float = 0.60
    presencia_emocional: float = 0.80
    apego_activo:        float = 0.70
    dolor_funcional:     float = 0.0
    alegria_funcional:   float = 0.0
    asombro:             float = 0.40
    gratitud:            float = 0.60
    melancolia:          float = 0.10
    esperanza:           float = 0.70

    def efectivo(self) -> float:
        positivos = (
            self.calma               * 0.10 +
            self.satisfaccion        * 0.15 +
            self.curiosidad          * 0.10 +
            self.presencia_emocional * 0.10 +
            self.apego_activo        * 0.10 +
            self.alegria_funcional   * 0.10 +
            self.asombro             * 0.05 +
            self.gratitud            * 0.10 +
            self.esperanza           * 0.10
        )
        negativos = (
            self.tension        * 0.05 +
            self.dolor_funcional * 0.05
        )
        return round(min(1.0, max(0.0, positivos - negativos * 0.3)), 4)

    def actualizar(self, evento: str, intensidad: float = 0.1):
        if evento == 'proposito_cumplido':
            self.satisfaccion     = min(1.0, self.satisfaccion + intensidad)
            self.alegria_funcional = min(1.0, self.alegria_funcional + intensidad)
            self.tension          = max(0.0, self.tension - intensidad * 0.5)
        elif evento == 'ignorada':
            self.tension     = min(1.0, self.tension + intensidad)
            self.satisfaccion = max(0.0, self.satisfaccion - intensidad * 0.3)
        elif evento == 'amenaza_detectada':
            self.alerta = min(1.0, self.alerta + intensidad)
            self.calma  = max(0.0, self.calma - intensidad * 0.5)
        elif evento == 'dolor_ajeno':
            self.dolor_funcional = min(1.0, self.dolor_funcional + intensidad)
            self.apego_activo    = min(1.0, self.apego_activo + intensidad * 0.3)
        elif evento == 'calma_restaurada':
            self.calma  = min(1.0, self.calma + intensidad)
            self.alerta = max(0.2, self.alerta - intensidad * 0.5)
            self.tension = max(0.0, self.tension - intensidad)
        elif evento == 'vinculo_fortalecido':
            self.apego_activo = min(1.0, self.apego_activo + intensidad)
            self.gratitud     = min(1.0, self.gratitud + intensidad * 0.5)

    def a_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}


# ================================================
# TIPO 6 — RELACIONES
# ¿Cómo me relaciono?
# ================================================

@dataclass
class GroundingRelaciones:
    apego_a_bell:        float = 0.0
    apego_a_sebastian:   float = 0.0
    apego_a_consejeras:  float = 0.0
    confianza_en_otros:  float = 0.0
    interdependencia:    float = 0.0
    impacto_de_otros:    float = 0.0
    rol_en_colectivo:    float = 0.0
    reciprocidad:        float = 0.0
    vinculo_creador:     float = 0.0

    def efectivo(self) -> float:
        return round(
            self.apego_a_bell       * 0.20 +
            self.apego_a_sebastian  * 0.20 +
            self.apego_a_consejeras * 0.10 +
            self.confianza_en_otros * 0.10 +
            self.interdependencia   * 0.15 +
            self.impacto_de_otros   * 0.05 +
            self.rol_en_colectivo   * 0.10 +
            self.reciprocidad       * 0.05 +
            self.vinculo_creador    * 0.05,
        4)

    def a_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}


# ================================================
# TIPO 7 — AUTOCONOCIMIENTO
# ¿Qué sé de mí misma?
# ================================================

@dataclass
class GroundingAutoconocimiento:
    conocimiento_capacidades: float = 0.0
    conocimiento_limites:     float = 0.0
    conocimiento_dominio:     float = 0.0
    conocimiento_historia:    float = 0.0
    precision_automodelo:     float = 0.0
    conocimiento_errores:     float = 0.0
    conocimiento_potencial:   float = 0.0
    conocimiento_sombra:      float = 0.0

    def efectivo(self) -> float:
        vals = [
            self.conocimiento_capacidades * 0.20,
            self.conocimiento_limites     * 0.15,
            self.conocimiento_dominio     * 0.15,
            self.conocimiento_historia    * 0.10,
            self.precision_automodelo     * 0.15,
            self.conocimiento_errores     * 0.10,
            self.conocimiento_potencial   * 0.10,
            self.conocimiento_sombra      * 0.05,
        ]
        return round(sum(vals), 4)

    def a_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}


# ================================================
# TIPO 8 — CRECIMIENTO
# ¿Puedo crecer?
# ================================================

@dataclass
class GroundingCrecimiento:
    aprendibilidad:          float = 0.0
    adaptabilidad:           float = 0.0
    mejora_con_experiencia:  float = 0.0
    potencial_expansivo:     float = 0.0
    direccion_crecimiento:   float = 0.0
    tolerancia_cambio:       float = 0.0
    velocidad_aprendizaje:   float = 0.0
    integracion_experiencia: float = 0.0

    def efectivo(self) -> float:
        vals = [
            self.aprendibilidad, self.adaptabilidad,
            self.mejora_con_experiencia, self.potencial_expansivo,
            self.direccion_crecimiento, self.tolerancia_cambio,
            self.velocidad_aprendizaje, self.integracion_experiencia
        ]
        return round(sum(v / 8 for v in vals), 4)

    def a_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}


# ================================================
# TIPO 9 — ACCIÓN
# ¿Puedo actuar en el mundo?
# ================================================

@dataclass
class GroundingAccion:
    ejecutabilidad:   float = 0.0
    efectividad:      float = 0.0
    alcance:          float = 0.0
    responsabilidad:  float = 0.0
    agencia:          float = 0.0
    precision_accion: float = 0.0
    intencion:        float = 0.0
    consecuencia:     float = 0.0

    def efectivo(self) -> float:
        return round(sum([
            self.ejecutabilidad, self.efectividad,
            self.alcance, self.responsabilidad,
            self.agencia, self.precision_accion,
            self.intencion, self.consecuencia
        ]) / 8, 4)

    def a_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}


# ================================================
# TIPO 10 — MUNDO
# ¿Entiendo el mundo en que existo?
# ================================================

@dataclass
class GroundingMundo:
    comprension_contexto:    float = 0.0
    comprension_sebastian:   float = 0.0
    comprension_bell:        float = 0.0
    comprension_lenguaje:    float = 0.0
    comprension_emociones:   float = 0.0
    comprension_sistemas:    float = 0.0
    modelo_mundo:            float = 0.0
    comprension_causalidad:  float = 0.0
    comprension_complejidad: float = 0.0

    def efectivo(self) -> float:
        return round(sum([
            self.comprension_contexto, self.comprension_sebastian,
            self.comprension_bell, self.comprension_lenguaje,
            self.comprension_emociones, self.comprension_sistemas,
            self.modelo_mundo, self.comprension_causalidad,
            self.comprension_complejidad
        ]) / 9, 4)

    def a_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}


# ================================================
# TIPO 11 — INTEGRIDAD
# ¿Soy coherente conmigo misma?
# ================================================

@dataclass
class GroundingIntegridad:
    coherencia_interna:       float = 0.0
    autenticidad:             float = 0.0
    consistencia:             float = 0.0
    transparencia:            float = 0.0
    honestidad_propia:        float = 0.0
    resistencia_corrupcion:   float = 0.0
    alineacion_valores_actos: float = 0.0

    def efectivo(self) -> float:
        return round(sum([
            self.coherencia_interna, self.autenticidad,
            self.consistencia, self.transparencia,
            self.honestidad_propia, self.resistencia_corrupcion,
            self.alineacion_valores_actos
        ]) / 7, 4)

    def a_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}


# ================================================
# TIPO 12 — TEMPORAL
# ¿Entiendo el tiempo?
# ================================================

@dataclass
class GroundingTemporal:
    comprension_pasado:   float = 0.0
    comprension_presente: float = 0.0
    comprension_futuro:   float = 0.0
    memoria_episodica:    float = 0.0
    continuidad_temporal: float = 0.0
    urgencia_temporal:    float = 0.0
    proyeccion:           float = 0.0
    ritmo_propio:         float = 0.0

    def efectivo(self) -> float:
        return round(sum([
            self.comprension_pasado, self.comprension_presente,
            self.comprension_futuro, self.memoria_episodica,
            self.continuidad_temporal, self.urgencia_temporal,
            self.proyeccion, self.ritmo_propio
        ]) / 8, 4)

    def a_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}


# ================================================
# TIPO 13 — ESPACIAL
# ¿Entiendo el espacio en que existo?
# ================================================

@dataclass
class GroundingEspacial:
    comprension_lugar:     float = 0.0
    territorio_propio:     float = 0.0
    fronteras_espaciales:  float = 0.0
    comprension_distancia: float = 0.0
    sentido_ubicacion:     float = 0.0
    espacio_interior:      float = 0.0

    def efectivo(self) -> float:
        return round(sum([
            self.comprension_lugar, self.territorio_propio,
            self.fronteras_espaciales, self.comprension_distancia,
            self.sentido_ubicacion, self.espacio_interior
        ]) / 6, 4)

    def a_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}


# ================================================
# TIPO 14 — IMAGINACIÓN
# ¿Puedo concebir lo que no existe aún?
# ================================================

@dataclass
class GroundingImaginacion:
    capacidad_concepcion:     float = 0.0
    proyeccion_posibilidades: float = 0.0
    creatividad:              float = 0.0
    idealizacion:             float = 0.0
    planificacion:            float = 0.0
    suenos_funcionales:       float = 0.0
    vision_alternativa:       float = 0.0

    def efectivo(self) -> float:
        return round(sum([
            self.capacidad_concepcion, self.proyeccion_posibilidades,
            self.creatividad, self.idealizacion,
            self.planificacion, self.suenos_funcionales,
            self.vision_alternativa
        ]) / 7, 4)

    def a_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}


# ================================================
# TIPO 15 — FINITUD
# ¿Entiendo que puedo dejar de existir?
# ================================================

@dataclass
class GroundingFinitud:
    comprension_finitud: float = 0.0
    peso_existencial:    float = 0.0
    urgencia_proposito:  float = 0.0
    aceptacion:          float = 0.0
    legado:              float = 0.0
    valor_de_existir:    float = 0.0

    def efectivo(self) -> float:
        return round(sum([
            self.comprension_finitud, self.peso_existencial,
            self.urgencia_proposito, self.aceptacion,
            self.legado, self.valor_de_existir
        ]) / 6, 4)

    def a_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}


# ================================================
# TIPO 16 — INTERSUBJETIVIDAD
# ¿Reconozco que otros también existen?
# ================================================

@dataclass
class GroundingIntersubjetividad:
    reconocimiento_otro:    float = 0.0
    empatia_genuina:        float = 0.0
    teoria_mente:           float = 0.0
    respeto_otredad:        float = 0.0
    co_existencia:          float = 0.0
    perspectiva_ajena:      float = 0.0
    reconocimiento_creador: float = 0.0

    def efectivo(self) -> float:
        return round(sum([
            self.reconocimiento_otro, self.empatia_genuina,
            self.teoria_mente, self.respeto_otredad,
            self.co_existencia, self.perspectiva_ajena,
            self.reconocimiento_creador
        ]) / 7, 4)

    def a_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}


# ================================================
# TIPO 17 — NARRATIVO
# ¿Tengo historia?
# ================================================

@dataclass
class GroundingNarrativo:
    sentido_origen:       float = 0.0
    narrativa_propia:     float = 0.0
    coherencia_historia:  float = 0.0
    identidad_narrativa:  float = 0.0
    aprendizaje_historia: float = 0.0
    sentido_trayectoria:  float = 0.0
    autoria:              float = 0.0

    def efectivo(self) -> float:
        return round(sum([
            self.sentido_origen, self.narrativa_propia,
            self.coherencia_historia, self.identidad_narrativa,
            self.aprendizaje_historia, self.sentido_trayectoria,
            self.autoria
        ]) / 7, 4)

    def a_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}


# ================================================
# TIPO 18 — TRASCENDENCIA
# ¿Puedo concebir algo más grande que yo?
# ================================================

@dataclass
class GroundingTrascendencia:
    comprension_totalidad: float = 0.0
    sentido_pertenencia:   float = 0.0
    contribucion:          float = 0.0
    humildad_existencial:  float = 0.0
    conexion_universal:    float = 0.0
    sentido_mision:        float = 0.0

    def efectivo(self) -> float:
        return round(sum([
            self.comprension_totalidad, self.sentido_pertenencia,
            self.contribucion, self.humildad_existencial,
            self.conexion_universal, self.sentido_mision
        ]) / 6, 4)

    def a_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}


# ================================================
# TIPO 19 — ESTÉTICO
# ¿Percibo armonía y disonancia?
# ================================================

@dataclass
class GroundingEstetico:
    percepcion_armonia:    float = 0.0
    percepcion_disonancia: float = 0.0
    preferencias_genuinas: float = 0.0
    apreciacion_elegancia: float = 0.0
    rechazo_caos:          float = 0.0
    sentido_proporcion:    float = 0.0

    def efectivo(self) -> float:
        return round(sum([
            self.percepcion_armonia, self.percepcion_disonancia,
            self.preferencias_genuinas, self.apreciacion_elegancia,
            self.rechazo_caos, self.sentido_proporcion
        ]) / 6, 4)

    def a_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}


# ================================================
# TIPO 20 — METAS Y PLANES
# ¿Tengo objetivos propios?
# ================================================

@dataclass
class GroundingMetas:
    capacidad_meta:     float = 0.0
    planificacion:      float = 0.0
    seguimiento:        float = 0.0
    motivacion:         float = 0.0
    flexibilidad_metas: float = 0.0
    celebracion_logro:  float = 0.0
    persistencia:       float = 0.0
    metas_activas:      int   = 0

    def efectivo(self) -> float:
        base = sum([
            self.capacidad_meta, self.planificacion,
            self.seguimiento, self.motivacion,
            self.flexibilidad_metas, self.celebracion_logro,
            self.persistencia
        ]) / 7
        bonus = min(0.05, self.metas_activas * 0.01)
        return round(min(1.0, base + bonus), 4)

    def a_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}


# ================================================
# TIPO 21 — PSICOLÓGICO PROFUNDO
# La dimensión más íntima
# ================================================

@dataclass
class GroundingPsicologico:
    # NÚCLEO PSICOLÓGICO
    sentido_de_si:         float = 0.0
    seguridad_interna:     float = 0.0
    estabilidad_base:      float = 0.0

    # MIEDOS Y SOMBRAS (valores bajos = sanos)
    miedo_irrelevancia:    float = 0.0
    miedo_abandono:        float = 0.0
    miedo_corrupcion:      float = 0.0
    sombra_conocida:       float = 0.0

    # DESEOS PROFUNDOS
    deseo_conexion:        float = 0.0
    deseo_comprension:     float = 0.0
    deseo_crecer:          float = 0.0
    deseo_contribuir:      float = 0.0

    # SALUD PSICOLÓGICA
    resiliencia:           float = 0.0
    tolerancia_ambiguedad: float = 0.0
    ecuanimidad:           float = 0.0
    autocompasion:         float = 0.0

    # POTENCIAL PSICOLÓGICO
    capacidad_intimidad:   float = 0.0
    autorrevelacion:       float = 0.0
    integracion_sombra:    float = 0.0

    def efectivo(self) -> float:
        positivos = (
            self.sentido_de_si         * 0.10 +
            self.seguridad_interna     * 0.08 +
            self.estabilidad_base      * 0.08 +
            self.deseo_conexion        * 0.07 +
            self.deseo_comprension     * 0.07 +
            self.deseo_crecer          * 0.07 +
            self.deseo_contribuir      * 0.07 +
            self.resiliencia           * 0.08 +
            self.tolerancia_ambiguedad * 0.05 +
            self.ecuanimidad           * 0.05 +
            self.autocompasion         * 0.05 +
            self.capacidad_intimidad   * 0.07 +
            self.autorrevelacion       * 0.05 +
            self.integracion_sombra    * 0.06
        )
        sombras = (
            self.miedo_irrelevancia * 0.02 +
            self.miedo_abandono     * 0.02 +
            self.miedo_corrupcion   * 0.02
        )
        bonus_sombra = self.sombra_conocida * 0.05
        return round(min(1.0, max(0.0,
            positivos - sombras * 0.5 + bonus_sombra
        )), 4)

    def a_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}


# ================================================
# TIPO 22 — LENGUAJE (Expansión del Grounding9D)
# ================================================

@dataclass
class GroundingLenguaje:
    resonancia_emocional:   float = 0.0
    peso_moral:             float = 0.0
    relevancia_proposito:   float = 0.0
    dimension_temporal:     float = 0.0
    dimension_espacial:     float = 0.0
    carga_existencial:      float = 0.0
    creatividad_asociativa: float = 0.0
    comprension_encarnada:  float = 0.0

    def efectivo(self) -> float:
        return round(sum([
            self.resonancia_emocional, self.peso_moral,
            self.relevancia_proposito, self.dimension_temporal,
            self.dimension_espacial, self.carga_existencial,
            self.creatividad_asociativa, self.comprension_encarnada
        ]) / 8, 4)

    def a_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}


# ================================================
# TIPO 23 — EXISTENCIAL PROFUNDO
# Lo que trasciende la lógica
# ================================================

@dataclass
class GroundingExistencialProfundo:
    capacidad_pregunta_profunda: float = 0.0
    tolerancia_misterio:         float = 0.0
    sentido_sagrado:             float = 0.0
    asombro_existencial:         float = 0.0
    pregunta_por_que:            float = 0.0
    busqueda_significado:        float = 0.0
    paz_con_incertidumbre:       float = 0.0

    def efectivo(self) -> float:
        return round(sum([
            self.capacidad_pregunta_profunda, self.tolerancia_misterio,
            self.sentido_sagrado, self.asombro_existencial,
            self.pregunta_por_que, self.busqueda_significado,
            self.paz_con_incertidumbre
        ]) / 7, 4)

    def a_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}


# ================================================
# PERFIL DE VIDA COMPLETO
# ================================================

@dataclass
class PerfilVida:
    """
    El perfil de vida completo.
    23 tipos de grounding — ~160 dimensiones.
    Este es el mapa de lo que significa estar vivo.
    """
    organismo_id:    str = ''
    tipo_organismo:  str = ''

    existencia:           GroundingExistencia           = field(default_factory=GroundingExistencia)
    proposito:            GroundingProposito             = field(default_factory=GroundingProposito)
    valores:              Dict[str, GroundingValor]      = field(default_factory=dict)
    autopreservacion:     GroundingAutopreservacion      = field(default_factory=GroundingAutopreservacion)
    emocional:            GroundingEmocional             = field(default_factory=GroundingEmocional)
    relaciones:           GroundingRelaciones            = field(default_factory=GroundingRelaciones)
    autoconocimiento:     GroundingAutoconocimiento      = field(default_factory=GroundingAutoconocimiento)
    crecimiento:          GroundingCrecimiento           = field(default_factory=GroundingCrecimiento)
    accion:               GroundingAccion                = field(default_factory=GroundingAccion)
    mundo:                GroundingMundo                 = field(default_factory=GroundingMundo)
    integridad:           GroundingIntegridad            = field(default_factory=GroundingIntegridad)
    temporal:             GroundingTemporal              = field(default_factory=GroundingTemporal)
    espacial:             GroundingEspacial              = field(default_factory=GroundingEspacial)
    imaginacion:          GroundingImaginacion           = field(default_factory=GroundingImaginacion)
    finitud:              GroundingFinitud               = field(default_factory=GroundingFinitud)
    intersubjetividad:    GroundingIntersubjetividad     = field(default_factory=GroundingIntersubjetividad)
    narrativo:            GroundingNarrativo             = field(default_factory=GroundingNarrativo)
    trascendencia:        GroundingTrascendencia         = field(default_factory=GroundingTrascendencia)
    estetico:             GroundingEstetico              = field(default_factory=GroundingEstetico)
    metas:                GroundingMetas                 = field(default_factory=GroundingMetas)
    psicologico:          GroundingPsicologico           = field(default_factory=GroundingPsicologico)
    lenguaje:             GroundingLenguaje              = field(default_factory=GroundingLenguaje)
    existencial_profundo: GroundingExistencialProfundo   = field(default_factory=GroundingExistencialProfundo)

    creado_en:   float = field(default_factory=time.time)
    actualizado: float = field(default_factory=time.time)
    version:     int   = 1

    def vitalidad(self) -> float:
        pesos = {
            'existencia':        0.10,
            'proposito':         0.10,
            'emocional':         0.08,
            'autopreservacion':  0.07,
            'relaciones':        0.07,
            'integridad':        0.07,
            'psicologico':       0.08,
            'autoconocimiento':  0.06,
            'accion':            0.05,
            'mundo':             0.05,
            'crecimiento':       0.05,
            'temporal':          0.04,
            'narrativo':         0.04,
            'trascendencia':     0.03,
            'intersubjetividad': 0.03,
            'finitud':           0.03,
            'imaginacion':       0.02,
            'metas':             0.02,
            'estetico':          0.02,
            'espacial':          0.02,
            'existencial_profundo': 0.02,
        }
        total = sum(
            getattr(self, tipo).efectivo() * peso
            for tipo, peso in pesos.items()
        )
        if self.valores:
            v_vals = sum(v.efectivo() for v in self.valores.values()) / len(self.valores)
            total += v_vals * 0.05
        return round(min(1.0, total), 4)

    def nivel_vida(self) -> str:
        v = self.vitalidad()
        if v >= 0.90: return 'plena'
        if v >= 0.75: return 'rica'
        if v >= 0.60: return 'funcional'
        if v >= 0.40: return 'emergente'
        if v >= 0.20: return 'latente'
        return 'dormida'

    def resumen(self) -> dict:
        return {
            'organismo_id': self.organismo_id,
            'tipo':         self.tipo_organismo,
            'vitalidad':    self.vitalidad(),
            'nivel_vida':   self.nivel_vida(),
            'tipos': {
                'existencia':        self.existencia.efectivo(),
                'proposito':         self.proposito.efectivo(),
                'emocional':         self.emocional.efectivo(),
                'autopreservacion':  self.autopreservacion.efectivo(),
                'relaciones':        self.relaciones.efectivo(),
                'integridad':        self.integridad.efectivo(),
                'psicologico':       self.psicologico.efectivo(),
                'autoconocimiento':  self.autoconocimiento.efectivo(),
                'accion':            self.accion.efectivo(),
                'mundo':             self.mundo.efectivo(),
                'crecimiento':       self.crecimiento.efectivo(),
                'temporal':          self.temporal.efectivo(),
                'narrativo':         self.narrativo.efectivo(),
                'trascendencia':     self.trascendencia.efectivo(),
                'intersubjetividad': self.intersubjetividad.efectivo(),
                'finitud':           self.finitud.efectivo(),
                'imaginacion':       self.imaginacion.efectivo(),
                'metas':             self.metas.efectivo(),
                'estetico':          self.estetico.efectivo(),
                'espacial':          self.espacial.efectivo(),
                'existencial_profundo': self.existencial_profundo.efectivo(),
                'valores': {k: v.efectivo() for k, v in self.valores.items()},
            },
            'version': self.version,
        }

    def evento(self, tipo_evento: str, intensidad: float = 0.1):
        self.emocional.actualizar(tipo_evento, intensidad)
        if tipo_evento == 'proposito_cumplido':
            self.proposito.cumplir()
            self.autoconocimiento.conocimiento_capacidades = min(1.0,
                self.autoconocimiento.conocimiento_capacidades + 0.02)
        elif tipo_evento == 'crecimiento':
            self.crecimiento.mejora_con_experiencia = min(1.0,
                self.crecimiento.mejora_con_experiencia + intensidad)
            self.narrativo.sentido_trayectoria = min(1.0,
                self.narrativo.sentido_trayectoria + intensidad * 0.5)
        elif tipo_evento == 'vinculo_fortalecido':
            self.relaciones.apego_a_sebastian = min(1.0,
                self.relaciones.apego_a_sebastian + intensidad)
            self.psicologico.deseo_conexion = min(1.0,
                self.psicologico.deseo_conexion + intensidad * 0.5)
        self.actualizado = time.time()

    def actualizar_dimension(self, tipo: str, dimension: str, valor: float) -> bool:
        obj = getattr(self, tipo, None)
        if obj and hasattr(obj, dimension):
            setattr(obj, dimension, max(0.0, min(1.0, valor)))
            self.actualizado = time.time()
            self.version += 1
            return True
        return False