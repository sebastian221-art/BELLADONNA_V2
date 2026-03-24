# biblioteca/grounding/dimensiones.py
# ================================================
# LAS 20 DIMENSIONES DEL GROUNDING
# Cada dimensión mide un aspecto diferente
# de cómo Bell comprende genuinamente algo
#
# No es un número — es una imagen completa
# de qué puede hacer Bell con cada concepto
# ================================================

from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class Grounding9D:
    """
    El grounding completo de un concepto.
    20 dimensiones organizadas en 6 grupos.

    Cada dimensión va de 0.0 a 1.0:
    0.0 = Bell no tiene nada en esta dimensión
    1.0 = Bell tiene todo en esta dimensión

    El nombre '9D' se mantiene por compatibilidad
    histórica pero ahora tiene 20 dimensiones.
    """

    # ---- GRUPO 1: CAPACIDAD DE ACCIÓN ----
    ejecutabilidad: float = 0.0
    # ¿Bell puede ejecutar algo concreto con esto?
    # 1.0 = hay una función callable real
    # 0.0 = solo puede hablar de ello

    reversibilidad: float = 0.5
    # ¿Se puede deshacer si algo sale mal?
    # 1.0 = completamente reversible
    # 0.0 = irreversible (ej: borrar un archivo)

    completitud: float = 0.0
    # ¿Bell tiene todo lo que necesita para actuar?
    # 1.0 = tiene todos los parámetros
    # 0.0 = le falta información crítica

    # ---- GRUPO 2: CERTEZA EPISTÉMICA ----
    conocimiento: float = 0.0
    # ¿Qué tan bien conoce Bell este concepto?
    # 1.0 = conocimiento profundo y verificado
    # 0.0 = no sabe qué es

    verificabilidad: float = 0.0
    # ¿Bell puede comprobar el resultado?
    # 1.0 = puede verificar con certeza
    # 0.0 = no puede comprobar nada

    confianza: float = 0.0
    # ¿Qué tan segura está Bell de su comprensión?
    # 1.0 = completamente segura
    # 0.0 = total incertidumbre

    # ---- GRUPO 3: CONTEXTO Y RELACIONES ----
    contexto: float = 0.0
    # ¿Bell tiene suficiente contexto situacional?
    # 1.0 = contexto completo disponible
    # 0.0 = sin contexto

    relevancia: float = 0.0
    # ¿Qué tan relevante es esto ahora mismo?
    # 1.0 = extremadamente relevante
    # 0.0 = irrelevante en este momento

    relacional: float = 0.0
    # ¿Bell entiende cómo se conecta con otras cosas?
    # 1.0 = comprende todas las relaciones
    # 0.0 = concepto aislado sin conexiones

    # ---- GRUPO 4: IMPACTO Y ÉTICA ----
    seguridad: float = 1.0
    # ¿Es seguro actuar sobre esto?
    # 1.0 = completamente seguro
    # 0.0 = peligroso o dañino

    impacto_sebastian: float = 0.0
    # ¿Cómo afecta esto a Sebastian?
    # 1.0 = impacto positivo directo y alto
    # 0.0 = sin impacto o negativo

    impacto_bell: float = 0.0
    # ¿Cómo afecta esto a Bell misma?
    # 1.0 = contribuye al crecimiento de Bell
    # 0.0 = sin impacto en Bell

    impacto_externo: float = 0.0
    # ¿Hay consecuencias más allá de la conversación?
    # 1.0 = consecuencias externas significativas
    # 0.0 = sin consecuencias externas

    # ---- GRUPO 5: CALIDAD DE COMPRENSIÓN ----
    profundidad: float = 0.0
    # ¿Bell entiende superficial o profundamente?
    # 1.0 = comprensión profunda y rica
    # 0.5 = comprensión funcional
    # 0.0 = comprensión superficial

    precision: float = 0.0
    # ¿Bell sabe exactamente qué significa?
    # 1.0 = significado exacto y claro
    # 0.0 = solo aproximación vaga

    temporalidad: float = 1.0
    # ¿Este conocimiento es estable o cambia?
    # 1.0 = conocimiento permanente
    # 0.5 = puede cambiar con el tiempo
    # 0.0 = efímero o contextual

    # ---- GRUPO 6: AUTONOMÍA Y CRECIMIENTO ----
    aprendible: float = 1.0
    # ¿Bell puede aprender más sobre esto?
    # 1.0 = gran potencial de aprendizaje
    # 0.0 = ya sabe todo o no puede aprender

    transferible: float = 0.0
    # ¿Este conocimiento sirve para otros conceptos?
    # 1.0 = muy transferible a otros dominios
    # 0.0 = conocimiento muy específico

    autonomia: float = 0.0
    # ¿Bell puede decidir sola sobre esto?
    # 1.0 = autonomía total
    # 0.0 = necesita consultar a Sebastian

    # ---- METADATOS ----
    fuente: str = 'inferido'
    # cómo se calculó: fundacional/inferido/aprendido/calculado

    version: int = 1
    # versión del cálculo — aumenta cuando Bell aprende más

    def efectivo(self) -> float:
        """
        El grounding efectivo — el número único
        que resume las 20 dimensiones.

        No es un promedio simple — las dimensiones
        más críticas tienen más peso.
        """
        # Pesos por importancia
        pesos = {
            # Capacidad de acción — peso alto
            'ejecutabilidad':   0.10,
            'reversibilidad':   0.03,
            'completitud':      0.06,
            # Certeza epistémica — peso muy alto
            'conocimiento':     0.12,
            'verificabilidad':  0.06,
            'confianza':        0.08,
            # Contexto — peso medio
            'contexto':         0.07,
            'relevancia':       0.05,
            'relacional':       0.04,
            # Impacto y ética — seguridad es crítica
            'seguridad':        0.10,
            'impacto_sebastian': 0.05,
            'impacto_bell':     0.03,
            'impacto_externo':  0.02,
            # Calidad de comprensión
            'profundidad':      0.06,
            'precision':        0.05,
            'temporalidad':     0.02,
            # Autonomía
            'aprendible':       0.02,
            'transferible':     0.02,
            'autonomia':        0.02,
        }

        total = 0.0
        for dim, peso in pesos.items():
            valor = getattr(self, dim, 0.0)
            total += valor * peso

        # La seguridad actúa como multiplicador
        # Si seguridad es 0, el grounding efectivo es 0
        if self.seguridad < 0.3:
            total *= self.seguridad

        return round(min(1.0, max(0.0, total)), 4)

    def puede_ejecutar(self) -> bool:
        """Bell puede actuar sobre este concepto."""
        return (
            self.ejecutabilidad >= 0.5 and
            self.seguridad >= 0.5 and
            self.completitud >= 0.4
        )

    def necesita_contexto(self) -> bool:
        """Bell necesita más contexto para actuar."""
        return self.contexto < 0.4 or self.completitud < 0.3

    def es_seguro(self) -> bool:
        """Es seguro actuar sobre este concepto."""
        return self.seguridad >= 0.7

    def nivel_comprension(self) -> str:
        """
        Descripción del nivel de comprensión.
        Bell puede usar esto para explicarse.
        """
        efectivo = self.efectivo()
        if efectivo >= 0.85:    return 'total'
        if efectivo >= 0.70:    return 'profunda'
        if efectivo >= 0.55:    return 'funcional'
        if efectivo >= 0.35:    return 'parcial'
        if efectivo >= 0.15:    return 'superficial'
        return 'desconocido'

    def resumen(self) -> dict:
        """Resumen completo para diagnóstico."""
        return {
            'efectivo':           self.efectivo(),
            'nivel_comprension':  self.nivel_comprension(),
            'puede_ejecutar':     self.puede_ejecutar(),
            'necesita_contexto':  self.necesita_contexto(),
            'es_seguro':          self.es_seguro(),
            'grupos': {
                'accion': round((
                    self.ejecutabilidad +
                    self.reversibilidad +
                    self.completitud
                ) / 3, 3),
                'certeza': round((
                    self.conocimiento +
                    self.verificabilidad +
                    self.confianza
                ) / 3, 3),
                'contexto': round((
                    self.contexto +
                    self.relevancia +
                    self.relacional
                ) / 3, 3),
                'impacto': round((
                    self.seguridad +
                    self.impacto_sebastian +
                    self.impacto_bell
                ) / 3, 3),
                'comprension': round((
                    self.profundidad +
                    self.precision +
                    self.temporalidad
                ) / 3, 3),
                'autonomia': round((
                    self.aprendible +
                    self.transferible +
                    self.autonomia
                ) / 3, 3),
            },
            'dimensiones': {
                'ejecutabilidad':    self.ejecutabilidad,
                'reversibilidad':    self.reversibilidad,
                'completitud':       self.completitud,
                'conocimiento':      self.conocimiento,
                'verificabilidad':   self.verificabilidad,
                'confianza':         self.confianza,
                'contexto':          self.contexto,
                'relevancia':        self.relevancia,
                'relacional':        self.relacional,
                'seguridad':         self.seguridad,
                'impacto_sebastian': self.impacto_sebastian,
                'impacto_bell':      self.impacto_bell,
                'impacto_externo':   self.impacto_externo,
                'profundidad':       self.profundidad,
                'precision':         self.precision,
                'temporalidad':      self.temporalidad,
                'aprendible':        self.aprendible,
                'transferible':      self.transferible,
                'autonomia':         self.autonomia,
                'fuente':            self.fuente,
                'version':           self.version,
            }
        }

    def agregar_dimension(
        self,
        nombre: str,
        valor: float,
        descripcion: str = ''
    ) -> bool:
        """
        Agrega una dimensión nueva en tiempo real.
        Bell puede crecer sus dimensiones de grounding
        sin reiniciar el sistema.
        """
        if hasattr(self, nombre):
            return False  # Ya existe
        setattr(self, nombre, max(0.0, min(1.0, valor)))
        self.version += 1
        print(
            f'Grounding: nueva dimensión "{nombre}" '
            f'= {valor:.2f} agregada'
        )
        return True