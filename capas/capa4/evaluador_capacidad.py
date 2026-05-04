# capas/capa4/evaluador_capacidad.py
# ================================================
# EVALUADOR DE CAPACIDAD — Capa 4
#
# FIX: intenciones alineadas con las que genera
# el motor de lenguaje real. Antes usaba nombres
# como 'preguntar_identidad' cuando el motor
# genera 'conocer_bell'.
# ================================================

from capas.capa4.paquete_capa4 import EvaluacionCapacidad, RecursosDisponibles

# Intenciones conversacionales — Bell siempre puede responder
INTENCIONES_CONVERSACIONALES = {
    'saludar', 'despedirse', 'agradecer', 'conversar',
    # Sobre Bell
    'conocer_bell',          # "quien eres"
    'saber_estado_bell',     # "como estas"
    'saber_nombre_bell',     # "como te llamas"
    'saber_capacidades_bell',# "que puedes hacer"
    # Sobre Sebastian
    'preguntar',             # "quien es sebastian", preguntas generales
    # Interacción
    'presentarse', 'confirmar', 'negar',
    'expresar_emocion_positiva',
    'expresar_emocion_negativa',
    'pedir_ayuda',
    'desconocida',           # siempre responde algo honesto
}

# Intenciones informativas — Bell responde con lo que sabe
INTENCIONES_INFORMATIVAS = {
    'preguntar_capacidad', 'preguntar_estado', 'preguntar_como',
    'pedir_explicacion', 'pedir_definicion',
}

# Intenciones ejecutivas — requieren habilidades de Capa 7
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

        intencion = profunda.get('intencion_detectada', 'conversar')
        necesidad = profunda.get('necesidad_real', 'conexion_social')
        certeza   = paquete_capa3.get('nivel_certeza', 0.5)

        # ¿Conversacional? — Bell siempre puede
        if intencion in INTENCIONES_CONVERSACIONALES:
            return EvaluacionCapacidad(
                puede_responder=True,
                puede_ejecutar=False,
                nivel_confianza=min(0.95, certeza + 0.1),
                tipo_respuesta='conversacional',
            )

        # ¿Informativa? — Bell responde con lo que tiene
        if intencion in INTENCIONES_INFORMATIVAS:
            confianza = certeza * 0.9 if recursos.nodos_activos > 0 else 0.4
            return EvaluacionCapacidad(
                puede_responder=True,
                puede_ejecutar=False,
                nivel_confianza=confianza,
                tipo_respuesta='informativa',
            )

        # ¿Ejecutiva? — depende de habilidades disponibles
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
                razon_limitacion='Habilidades de ejecución pendientes',
            )

        # ¿Necesidad emocional? — Bell siempre puede estar presente
        if necesidad in ('apoyo_emocional', 'ser_escuchado', 'compania',
                         'conexion_social', 'compartir_alegria'):
            return EvaluacionCapacidad(
                puede_responder=True,
                puede_ejecutar=False,
                nivel_confianza=min(0.90, certeza + 0.15),
                tipo_respuesta='emocional',
            )

        # Caso general — Bell siempre responde algo honesto
        confianza = certeza * 0.8 if recursos.nodos_activos > 3 else 0.5
        return EvaluacionCapacidad(
            puede_responder=True,
            puede_ejecutar=False,
            nivel_confianza=confianza,
            tipo_respuesta='conversacional',
        )