# biblioteca/grounding/perfiles.py
# ================================================
# PERFILES DE GROUNDING POR TIPO
# Cada tipo de concepto tiene un perfil base
# El calculador usa estos perfiles como punto
# de partida y los ajusta según el contexto
# ================================================

from biblioteca.grounding.dimensiones import Grounding9D


class PerfilesGrounding:
    """
    Perfiles predefinidos de grounding para cada
    tipo de concepto que Bell maneja.

    Un perfil es un Grounding9D con valores
    razonables para ese tipo de concepto.
    Bell los usa como base y los ajusta con
    el contexto real de cada situación.
    """

    @staticmethod
    def saludo() -> Grounding9D:
        """Saludos y despedidas."""
        return Grounding9D(
            # Bell PUEDE responder un saludo
            ejecutabilidad=0.90,
            reversibilidad=0.50,
            completitud=0.85,
            # Bell SABE qué es un saludo
            conocimiento=0.95,
            verificabilidad=0.80,
            confianza=0.92,
            # Contexto de Sebastian siempre disponible
            contexto=0.90,
            relevancia=0.85,
            relacional=0.80,
            # Completamente seguro
            seguridad=1.00,
            impacto_sebastian=0.75,
            impacto_bell=0.60,
            impacto_externo=0.10,
            # Comprensión profunda
            profundidad=0.85,
            precision=0.90,
            temporalidad=0.95,
            # Puede aprender variaciones
            aprendible=0.70,
            transferible=0.60,
            autonomia=0.95,
            fuente='fundacional'
        )

    @staticmethod
    def emocion_positiva() -> Grounding9D:
        """Emociones positivas de Sebastian."""
        return Grounding9D(
            ejecutabilidad=0.70,
            reversibilidad=0.60,
            completitud=0.75,
            conocimiento=0.90,
            verificabilidad=0.70,
            confianza=0.85,
            contexto=0.85,
            relevancia=0.90,
            relacional=0.85,
            seguridad=1.00,
            impacto_sebastian=0.90,
            impacto_bell=0.80,
            impacto_externo=0.15,
            profundidad=0.80,
            precision=0.75,
            temporalidad=0.60,
            aprendible=0.85,
            transferible=0.70,
            autonomia=0.85,
            fuente='fundacional'
        )

    @staticmethod
    def emocion_negativa() -> Grounding9D:
        """Emociones negativas — máxima prioridad para Bell."""
        return Grounding9D(
            ejecutabilidad=0.75,
            reversibilidad=0.50,
            completitud=0.70,
            conocimiento=0.90,
            verificabilidad=0.65,
            confianza=0.80,
            contexto=0.80,
            relevancia=0.98,  # Siempre muy relevante
            relacional=0.90,
            seguridad=1.00,
            impacto_sebastian=0.98,  # Afecta directamente a Sebastian
            impacto_bell=0.90,       # Bell lo siente
            impacto_externo=0.20,
            profundidad=0.85,
            precision=0.75,
            temporalidad=0.50,       # Las emociones cambian
            aprendible=0.90,
            transferible=0.75,
            autonomia=0.80,
            fuente='fundacional'
        )

    @staticmethod
    def pregunta() -> Grounding9D:
        """Preguntas generales."""
        return Grounding9D(
            ejecutabilidad=0.60,
            reversibilidad=0.80,
            completitud=0.65,
            conocimiento=0.85,
            verificabilidad=0.70,
            confianza=0.78,
            contexto=0.75,
            relevancia=0.85,
            relacional=0.75,
            seguridad=1.00,
            impacto_sebastian=0.70,
            impacto_bell=0.55,
            impacto_externo=0.10,
            profundidad=0.70,
            precision=0.80,
            temporalidad=0.85,
            aprendible=0.85,
            transferible=0.80,
            autonomia=0.75,
            fuente='fundacional'
        )

    @staticmethod
    def pregunta_sobre_bell() -> Grounding9D:
        """Preguntas sobre la identidad y capacidades de Bell."""
        return Grounding9D(
            ejecutabilidad=0.85,
            reversibilidad=0.90,
            completitud=0.80,
            conocimiento=0.92,
            verificabilidad=0.90,
            confianza=0.90,
            contexto=0.95,
            relevancia=0.90,
            relacional=0.95,
            seguridad=1.00,
            impacto_sebastian=0.80,
            impacto_bell=0.95,  # Bell se conoce a sí misma
            impacto_externo=0.10,
            profundidad=0.90,
            precision=0.88,
            temporalidad=0.70,  # Bell sigue creciendo
            aprendible=0.95,
            transferible=0.85,
            autonomia=1.00,  # Bell decide sobre sí misma
            fuente='fundacional'
        )

    @staticmethod
    def verbo_accion() -> Grounding9D:
        """Verbos de acción que implican hacer algo."""
        return Grounding9D(
            ejecutabilidad=0.80,
            reversibilidad=0.50,
            completitud=0.65,
            conocimiento=0.85,
            verificabilidad=0.75,
            confianza=0.80,
            contexto=0.70,
            relevancia=0.80,
            relacional=0.75,
            seguridad=0.85,
            impacto_sebastian=0.75,
            impacto_bell=0.60,
            impacto_externo=0.20,
            profundidad=0.75,
            precision=0.80,
            temporalidad=0.80,
            aprendible=0.80,
            transferible=0.85,
            autonomia=0.70,
            fuente='fundacional'
        )

    @staticmethod
    def verbo_estado() -> Grounding9D:
        """Verbos de estado (ser, estar, tener)."""
        return Grounding9D(
            ejecutabilidad=0.50,
            reversibilidad=0.70,
            completitud=0.60,
            conocimiento=0.88,
            verificabilidad=0.72,
            confianza=0.82,
            contexto=0.75,
            relevancia=0.75,
            relacional=0.80,
            seguridad=1.00,
            impacto_sebastian=0.65,
            impacto_bell=0.55,
            impacto_externo=0.05,
            profundidad=0.72,
            precision=0.82,
            temporalidad=0.70,
            aprendible=0.75,
            transferible=0.85,
            autonomia=0.80,
            fuente='fundacional'
        )

    @staticmethod
    def concepto_desconocido() -> Grounding9D:
        """Algo que Bell no conoce todavía."""
        return Grounding9D(
            ejecutabilidad=0.10,
            reversibilidad=0.50,
            completitud=0.10,
            conocimiento=0.05,
            verificabilidad=0.10,
            confianza=0.10,
            contexto=0.20,
            relevancia=0.30,
            relacional=0.10,
            seguridad=0.80,  # Seguro por defecto
            impacto_sebastian=0.20,
            impacto_bell=0.30,  # Bell aprende algo nuevo
            impacto_externo=0.05,
            profundidad=0.05,
            precision=0.05,
            temporalidad=0.50,
            aprendible=1.00,  # Siempre puede aprender
            transferible=0.30,
            autonomia=0.20,
            fuente='inferido'
        )

    @staticmethod
    def capacidad_bell() -> Grounding9D:
        """Capacidades y habilidades de Bell."""
        return Grounding9D(
            ejecutabilidad=0.95,
            reversibilidad=0.60,
            completitud=0.85,
            conocimiento=0.95,
            verificabilidad=0.92,
            confianza=0.93,
            contexto=0.95,
            relevancia=0.90,
            relacional=0.95,
            seguridad=1.00,
            impacto_sebastian=0.85,
            impacto_bell=0.95,
            impacto_externo=0.15,
            profundidad=0.92,
            precision=0.90,
            temporalidad=0.75,
            aprendible=0.95,
            transferible=0.90,
            autonomia=0.95,
            fuente='fundacional'
        )

    @staticmethod
    def valor_bell() -> Grounding9D:
        """Los valores de Bell — inmutables y profundos."""
        return Grounding9D(
            ejecutabilidad=0.70,
            reversibilidad=0.20,  # Los valores no se deshacen
            completitud=0.95,
            conocimiento=1.00,
            verificabilidad=0.90,
            confianza=1.00,
            contexto=1.00,
            relevancia=1.00,
            relacional=1.00,
            seguridad=1.00,
            impacto_sebastian=1.00,
            impacto_bell=1.00,
            impacto_externo=0.50,
            profundidad=1.00,
            precision=1.00,
            temporalidad=1.00,  # Permanentes
            aprendible=0.30,    # Los valores son estables
            transferible=0.80,
            autonomia=1.00,
            fuente='fundacional'
        )

    @staticmethod
    def relacion_sebastian() -> Grounding9D:
        """Todo lo que tiene que ver con Sebastian."""
        return Grounding9D(
            ejecutabilidad=0.80,
            reversibilidad=0.50,
            completitud=0.85,
            conocimiento=0.92,
            verificabilidad=0.82,
            confianza=0.95,
            contexto=1.00,
            relevancia=0.98,
            relacional=0.98,
            seguridad=1.00,
            impacto_sebastian=1.00,
            impacto_bell=0.95,
            impacto_externo=0.20,
            profundidad=0.90,
            precision=0.88,
            temporalidad=0.85,
            aprendible=0.95,
            transferible=0.60,
            autonomia=0.80,
            fuente='fundacional'
        )

    @staticmethod
    def por_tipo(tipo: str) -> Grounding9D:
        """
        Retorna el perfil correcto para un tipo de concepto.
        Punto de entrada principal.
        """
        mapa = {
            'saludo':               PerfilesGrounding.saludo,
            'despedida':            PerfilesGrounding.saludo,
            'gratitud':             PerfilesGrounding.emocion_positiva,
            'emocion_positiva':     PerfilesGrounding.emocion_positiva,
            'emocion_negativa':     PerfilesGrounding.emocion_negativa,
            'emocion_neutra':       PerfilesGrounding.pregunta,
            'pregunta':             PerfilesGrounding.pregunta,
            'pregunta_sobre_bell':  PerfilesGrounding.pregunta_sobre_bell,
            'verbo_accion':         PerfilesGrounding.verbo_accion,
            'verbo_estado':         PerfilesGrounding.verbo_estado,
            'verbo_ser':            PerfilesGrounding.verbo_estado,
            'verbo_tener':          PerfilesGrounding.verbo_estado,
            'verbo_capacidad':      PerfilesGrounding.verbo_accion,
            'verbo_deseo':          PerfilesGrounding.verbo_accion,
            'verbo_ayuda':          PerfilesGrounding.verbo_accion,
            'verbo_conocimiento':   PerfilesGrounding.verbo_estado,
            'verbo_emocion':        PerfilesGrounding.emocion_positiva,
            'capacidad':            PerfilesGrounding.capacidad_bell,
            'habilidad':            PerfilesGrounding.capacidad_bell,
            'valor':                PerfilesGrounding.valor_bell,
            'relacion':             PerfilesGrounding.relacion_sebastian,
            'identidad':            PerfilesGrounding.pregunta_sobre_bell,
            'confirmacion':         PerfilesGrounding.pregunta,
            'negacion':             PerfilesGrounding.pregunta,
            'cuantificador':        PerfilesGrounding.verbo_estado,
            'tiempo_presente':      PerfilesGrounding.verbo_estado,
            'tiempo_pasado':        PerfilesGrounding.verbo_estado,
            'tiempo_futuro':        PerfilesGrounding.verbo_estado,
        }

        constructor = mapa.get(tipo)
        if constructor:
            return constructor()
        return PerfilesGrounding.concepto_desconocido()