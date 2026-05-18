# capas/capa4/evaluador_capacidad.py
# ================================================
# EVALUADOR DE CAPACIDAD — v2
#
# v2:
# — Maneja nuevos tipos de C3 v2:
#   solicitud_tecnica, operacion_matematica,
#   compartir_logro, hacer_humor, reflexionar,
#   preguntar_sobre_sebastian, etc.
# — Usa motor_sugerido de C1 como hint
# — Tipos de respuesta más precisos
# ================================================

from capas.capa4.paquete_capa4 import EvaluacionCapacidad, RecursosDisponibles

# ── Bell siempre puede responder ──────────────────────────
INTENCIONES_CONVERSACIONALES = {
    'saludar', 'despedirse', 'agradecer', 'conversar',
    'conocer_bell', 'saber_estado_bell', 'saber_nombre_bell',
    'saber_capacidades_bell', 'conocer_arquitectura_bell',
    'saber_accion_bell', 'preguntar_sobre_sebastian',
    'presentarse', 'confirmar', 'negar',
    'expresar_emocion_positiva', 'expresar_emocion_negativa',
    'compartir_logro', 'expresar_queja', 'expresar_preocupacion',
    'hacer_humor', 'reflexionar',
    'pedir_ayuda', 'desconocida',
}

# ── Bell responde con conocimiento disponible ─────────────
INTENCIONES_INFORMATIVAS = {
    'preguntar', 'preguntar_capacidad', 'preguntar_estado',
    'pedir_explicacion', 'pedir_definicion',
    'preguntar_sobre_sebastian',
}

# ── Requieren ejecución real de habilidades ───────────────
INTENCIONES_EJECUTIVAS = {
    'ejecutar_comando', 'crear_archivo',
    'analizar_codigo', 'consultar_bd', 'buscar',
}

# ── Requieren Groq o Python para procesar ────────────────
INTENCIONES_TECNICAS = {
    'pedir_ayuda',       # puede ser técnico según contexto
}

# ── Necesidades emocionales — Bell siempre presente ──────
NECESIDADES_EMOCIONALES = {
    'apoyo_emocional', 'ser_escuchado', 'compania',
    'conexion_social', 'compartir_alegria', 'desahogarse',
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
                puede_responder  = True,
                nivel_confianza  = 0.5,
                tipo_respuesta   = 'conversacional',
                razon_limitacion = f'Evaluación parcial: {e}'
            )

    def _evaluar_interno(
        self,
        paquete_capa3: dict,
        recursos: RecursosDisponibles
    ) -> EvaluacionCapacidad:

        comprension    = paquete_capa3.get('comprension', {})
        profunda       = comprension.get('profunda', {})
        contextual     = comprension.get('contextual', {})

        intencion      = profunda.get('intencion_detectada', 'conversar')
        necesidad      = profunda.get('necesidad_real', 'conexion_social')
        tipo_mensaje   = contextual.get('tipo_mensaje', 'conversacional')
        certeza        = paquete_capa3.get('nivel_certeza', 0.5)

        # Campos de C1/C2/C3 propagados
        motor_sugerido  = paquete_capa3.get('motor_sugerido', 'local')
        contiene_codigo = paquete_capa3.get('contiene_codigo', False)
        complejidad     = paquete_capa3.get('complejidad', 'simple')
        modo_mental     = paquete_capa3.get('modo_mental', 'social')

        # ── Código detectado → técnico con Groq ───────────
        if contiene_codigo or tipo_mensaje == 'solicitud_tecnica':
            return EvaluacionCapacidad(
                puede_responder = True,
                puede_ejecutar  = True,
                nivel_confianza = 0.90,
                tipo_respuesta  = 'tecnica_groq',
                alternativa     = '',
            )

        # ── Matemáticas → Python puro ─────────────────────
        if tipo_mensaje == 'operacion_matematica':
            resultado = comprension.get('contextual', {}).get('resultado_matematico')
            if resultado:
                return EvaluacionCapacidad(
                    puede_responder = True,
                    puede_ejecutar  = True,
                    nivel_confianza = 0.99,
                    tipo_respuesta  = 'matematica_python',
                )
            return EvaluacionCapacidad(
                puede_responder = True,
                puede_ejecutar  = False,
                nivel_confianza = 0.70,
                tipo_respuesta  = 'conversacional',
                razon_limitacion = 'Expresión matemática no evaluable',
            )

        # ── Conversacional → Bell siempre ─────────────────
        if intencion in INTENCIONES_CONVERSACIONALES:
            # Ajuste por complejidad
            if complejidad == 'compleja' and motor_sugerido == 'groq':
                tipo = 'conversacional_groq'
                conf = min(0.95, certeza + 0.15)
            else:
                tipo = 'conversacional'
                conf = min(0.95, certeza + 0.10)
            return EvaluacionCapacidad(
                puede_responder = True,
                puede_ejecutar  = False,
                nivel_confianza = conf,
                tipo_respuesta  = tipo,
            )

        # ── Emocional → Bell siempre presente ────────────
        if necesidad in NECESIDADES_EMOCIONALES or modo_mental == 'emocional':
            return EvaluacionCapacidad(
                puede_responder = True,
                puede_ejecutar  = False,
                nivel_confianza = min(0.92, certeza + 0.15),
                tipo_respuesta  = 'emocional',
            )

        # ── Informativa → responde con lo disponible ─────
        if intencion in INTENCIONES_INFORMATIVAS:
            conf = certeza * 0.9 if recursos.nodos_activos > 0 else 0.55
            return EvaluacionCapacidad(
                puede_responder = True,
                puede_ejecutar  = False,
                nivel_confianza = conf,
                tipo_respuesta  = 'informativa',
            )

        # ── Ejecutiva → depende de habilidades ───────────
        if intencion in INTENCIONES_EJECUTIVAS:
            if recursos.tiene_habilidades:
                return EvaluacionCapacidad(
                    puede_responder = True,
                    puede_ejecutar  = True,
                    nivel_confianza = 0.80,
                    tipo_respuesta  = 'ejecutiva',
                )
            return EvaluacionCapacidad(
                puede_responder  = True,
                puede_ejecutar   = False,
                nivel_confianza  = 0.60,
                tipo_respuesta   = 'honestidad_limitacion',
                alternativa      = 'Entiendo lo que necesitas pero esa habilidad está en desarrollo.',
                razon_limitacion = 'Habilidad pendiente de implementación',
            )

        # ── Caso general ──────────────────────────────────
        conf = certeza * 0.85 if recursos.nodos_activos > 3 else 0.55
        return EvaluacionCapacidad(
            puede_responder = True,
            puede_ejecutar  = False,
            nivel_confianza = conf,
            tipo_respuesta  = 'conversacional',
        )