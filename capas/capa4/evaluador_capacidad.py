# capas/capa4/evaluador_capacidad.py
# ================================================
# EVALUADOR DE CAPACIDAD — Capa 4
# Responde: ¿puede Bell hacer lo que se pide?
# Si no puede: ¿qué puede hacer en su lugar?
# Bell nunca miente sobre sus capacidades.
# ================================================

from capas.capa4.paquete_capa4 import EvaluacionCapacidad, RecursosDisponibles


# Intenciones que Bell puede manejar en sus capas actuales
INTENCIONES_CONVERSACIONALES = {
    'saludar', 'despedirse', 'agradecer', 'conversar',
    'preguntar_identidad', 'presentarse', 'confirmar', 'negar',
    'expresar_emocion_positiva', 'expresar_emocion_negativa',
    'expresar_emocion_negativa', 'solicitar_ayuda',
}

INTENCIONES_INFORMATIVAS = {
    'preguntar_capacidad', 'preguntar_estado', 'preguntar_como',
    'pedir_explicacion', 'pedir_definicion',
}

INTENCIONES_EJECUTIVAS = {
    'ejecutar_comando', 'crear_archivo', 'calcular', 'buscar',
    'analizar_codigo', 'consultar_bd',
}


class EvaluadorCapacidad:

    def evaluar(
        self,
        paquete_capa3: dict,
        recursos: RecursosDisponibles
    ) -> EvaluacionCapacidad:
        try:
            return self._evaluar_interno(paquete_capa3, recursos)
        except Exception as e:
            return EvaluacionCapacidad(
                puede_responder=True,
                nivel_confianza=0.5,
                tipo_respuesta='conversacional',
                razon_limitacion=f'Evaluación parcial: {e}'
            )

    def _evaluar_interno(
        self,
        paquete_capa3: dict,
        recursos: RecursosDisponibles
    ) -> EvaluacionCapacidad:

        comprension = paquete_capa3.get('comprension', {})
        profunda    = comprension.get('profunda', {})

        intencion   = profunda.get('intencion_detectada', 'conversar')
        necesidad   = profunda.get('necesidad_real', 'conexion_social')
        certeza     = paquete_capa3.get('nivel_certeza', 0.5)

        # ¿Puede Bell responder en modo conversacional?
        if intencion in INTENCIONES_CONVERSACIONALES:
            return EvaluacionCapacidad(
                puede_responder=True,
                puede_ejecutar=False,
                nivel_confianza=min(0.95, certeza + 0.1),
                tipo_respuesta='conversacional',
            )

        # ¿Puede Bell responder en modo informativo?
        if intencion in INTENCIONES_INFORMATIVAS:
            confianza = certeza * 0.9 if recursos.nodos_activos > 0 else 0.4
            return EvaluacionCapacidad(
                puede_responder=True,
                puede_ejecutar=False,
                nivel_confianza=confianza,
                tipo_respuesta='informativa',
            )

        # ¿Requiere ejecución? (Capa 7 aún no existe)
        if intencion in INTENCIONES_EJECUTIVAS:
            if recursos.tiene_habilidades:
                return EvaluacionCapacidad(
                    puede_responder=True,
                    puede_ejecutar=True,
                    nivel_confianza=0.75,
                    tipo_respuesta='ejecutiva',
                    alternativa='Puedo intentarlo aunque mis capas de ejecución están en construcción.',
                )
            return EvaluacionCapacidad(
                puede_responder=True,
                puede_ejecutar=False,
                nivel_confianza=0.6,
                tipo_respuesta='honestidad_limitacion',
                alternativa='Entiendo lo que necesitas pero mis capacidades de ejecución aún están en desarrollo.',
                razon_limitacion='Capas 6-7 no implementadas',
            )

        # ¿Necesidad emocional?
        if necesidad in ('apoyo_emocional', 'ser_escuchado', 'compania'):
            return EvaluacionCapacidad(
                puede_responder=True,
                puede_ejecutar=False,
                nivel_confianza=min(0.90, certeza + 0.15),
                tipo_respuesta='emocional',
            )

        # Caso general — Bell siempre puede responder algo honesto
        confianza = certeza * 0.8 if recursos.nodos_activos > 3 else 0.5
        return EvaluacionCapacidad(
            puede_responder=True,
            puede_ejecutar=False,
            nivel_confianza=confianza,
            tipo_respuesta='conversacional',
        )