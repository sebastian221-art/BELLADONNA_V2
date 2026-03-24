# capas/capa3/detector_ambiguedad.py
# ================================================
# DETECTOR DE AMBIGÜEDAD
# Evalúa si la comprensión tiene una sola
# interpretación o varias posibles
# ================================================


class DetectorAmbiguedad:

    UMBRAL_AMBIGUEDAD_CRITICA = 0.3

    def detectar(
        self,
        comprension: dict,
        contexto: dict
    ) -> dict:
        """
        Detecta si hay ambigüedad en la comprensión.
        """
        tipo_mensaje  = comprension.get(
            'contextual', {}
        ).get('tipo_mensaje', 'desconocido')

        certeza_literal    = comprension.get(
            'literal', {}
        ).get('certeza', 0)

        certeza_profunda   = comprension.get(
            'profunda', {}
        ).get('certeza', 0)

        # Calcular nivel de ambigüedad
        certeza_promedio = (certeza_literal + certeza_profunda) / 2

        if certeza_promedio >= 0.7:
            nivel = 'baja'
            requiere_claridad = False
        elif certeza_promedio >= 0.4:
            nivel = 'media'
            requiere_claridad = False
        else:
            nivel = 'critica'
            requiere_claridad = True

        # Construir interpretaciones posibles
        interpretaciones = self._generar_interpretaciones(
            tipo_mensaje, certeza_promedio
        )

        return {
            'nivel':                nivel,
            'certeza_promedio':     certeza_promedio,
            'interpretaciones':     interpretaciones,
            'interpretacion_elegida': interpretaciones[0] if interpretaciones else tipo_mensaje,
            'requiere_claridad':    requiere_claridad
        }

    def _generar_interpretaciones(
        self,
        tipo_mensaje: str,
        certeza: float
    ) -> list:
        """Genera las interpretaciones posibles."""
        if certeza >= 0.7:
            return [tipo_mensaje]

        # Con baja certeza generar alternativas
        alternativas = {
            'saludo':             ['saludo', 'inicio_conversacion'],
            'pregunta':           ['pregunta', 'solicitud_informacion'],
            'solicitud_accion':   ['solicitud_accion', 'pregunta'],
            'expresion_emocional':['expresion_emocional', 'conversacional'],
            'conversacional':     ['conversacional', 'desconocido'],
        }
        return alternativas.get(tipo_mensaje, [tipo_mensaje])