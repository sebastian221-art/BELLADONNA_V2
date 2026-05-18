# capas/capa5/sintetizador.py
# ================================================
# SINTETIZADOR — v2
#
# Convierte la deliberación de las consejeras
# en InstruccionRespuesta para C6.
#
# v2:
# — Mapeo completo de todos los tipos de C3 v2
# — Usa tipo_respuesta de C4 cuando ya es preciso
# — Considera motor_sugerido y contiene_codigo
# — Nivel de detalle dinámico
# ================================================

from capas.capa5.paquete_capa5 import InstruccionRespuesta

_TONOS_VALIDOS = {
    'empático_suave', 'presente_inmediato', 'cálido_genuino',
    'celebratorio_cálido', 'cercano_natural', 'atento_sensible',
    'tranquilizador_suave', 'empático_firme', 'honesto_directo',
}
_TONO_DEFAULT = 'cercano_natural'

# Mapeo completo de intenciones → tipo de respuesta
_TIPO_POR_INTENCION = {
    # ── Conversacionales ──────────────────────────────────
    'saludar':              'conversacional',
    'despedirse':           'conversacional',
    'agradecer':            'conversacional',
    'conversar':            'conversacional',
    'presentarse':          'conversacional',
    'confirmar':            'conversacional',
    'negar':                'conversacional',
    'hacer_humor':          'conversacional',
    'reflexionar':          'conversacional',
    'desconocida':          'conversacional',
    # ── Informativas ─────────────────────────────────────
    'preguntar':                 'informativa',
    'conocer_bell':              'informativa',
    'saber_estado_bell':         'informativa',
    'saber_nombre_bell':         'informativa',
    'saber_capacidades_bell':    'informativa',
    'conocer_arquitectura_bell': 'informativa',
    'saber_accion_bell':         'informativa',
    'preguntar_sobre_sebastian': 'informativa',
    # ── Emocionales ──────────────────────────────────────
    'expresar_emocion_negativa': 'emocional',
    'expresar_emocion_positiva': 'emocional',
    'compartir_logro':           'emocional',
    'expresar_queja':            'emocional',
    'expresar_preocupacion':     'emocional',
    'pedir_ayuda':               'emocional',
    # ── Técnicas (requieren Groq o Python) ───────────────
    'calcular':          'matematica_python',
    'analizar_codigo':   'tecnica_groq',
    'crear_archivo':     'tecnica_groq',
    'buscar':            'ejecutiva',
    'ejecutar_comando':  'ejecutiva',
    'consultar_bd':      'ejecutiva',
}

# Tipos que vienen de C4 y son definitivos — no reclasificar
_TIPOS_DEFINITIVOS_C4 = {
    'tecnica_groq', 'matematica_python',
    'honestidad_limitacion', 'veto_respuesta',
}


class Sintetizador:

    def sintetizar(
        self,
        deliberacion,
        paquete_capa4,
        motor_sugerido:  str  = 'local',
        contiene_codigo: bool = False,
        modo_mental:     str  = 'social',
    ) -> InstruccionRespuesta:
        try:
            return self._sintetizar_interno(
                deliberacion, paquete_capa4,
                motor_sugerido, contiene_codigo, modo_mental
            )
        except Exception as e:
            return InstruccionRespuesta(
                tipo_respuesta     = 'conversacional',
                tono               = _TONO_DEFAULT,
                confianza          = 0.5,
                recomendacion_sage = f'Síntesis parcial: {e}',
            )

    def _sintetizar_interno(
        self,
        deliberacion,
        paquete_capa4,
        motor_sugerido:  str,
        contiene_codigo: bool,
        modo_mental:     str,
    ) -> InstruccionRespuesta:

        ctx      = paquete_capa4.get('contexto_consejeras', {})
        intencion = ctx.get('intencion_detectada', 'conversar')
        capacidad = paquete_capa4.get('capacidad', {})

        delib_dict = (
            deliberacion.a_dict() if hasattr(deliberacion, 'a_dict')
            else (deliberacion if isinstance(deliberacion, dict) else {})
        )

        tono_sage       = delib_dict.get('tono_final', _TONO_DEFAULT)
        recomendacion   = delib_dict.get('recomendacion_sage', '')
        confianza       = delib_dict.get('confianza_colectiva', 0.8)
        prio_emocional  = delib_dict.get('prioridad_emocional', False)

        tono = tono_sage if tono_sage in _TONOS_VALIDOS else _TONO_DEFAULT

        # ── 1. Tipo definitivo de C4 — no reclasificar ────
        tipo_c4 = capacidad.get('tipo_respuesta', '')
        if tipo_c4 in _TIPOS_DEFINITIVOS_C4:
            tipo = tipo_c4
        # ── 2. Código detectado → siempre técnico ─────────
        elif contiene_codigo:
            tipo = 'tecnica_groq'
        # ── 3. Motor sugerido + modo mental ───────────────
        elif motor_sugerido == 'groq' and modo_mental == 'tecnico':
            tipo = 'tecnica_groq'
        # ── 4. Mapeo estándar por intención ───────────────
        else:
            tipo = _TIPO_POR_INTENCION.get(intencion, 'conversacional')
            # Si capacidad pide honestidad — respetar
            if tipo_c4 == 'honestidad_limitacion':
                tipo = 'honestidad_limitacion'

        # ── Nivel de detalle dinámico ──────────────────────
        nivel_detalle = self._calcular_nivel_detalle(
            tipo, confianza, prio_emocional, modo_mental
        )

        return InstruccionRespuesta(
            tipo_respuesta      = tipo,
            tono                = tono,
            confianza           = round(confianza, 3),
            prioridad_emocional = prio_emocional,
            incluir_nombre      = True,
            nivel_detalle       = nivel_detalle,
            recomendacion_sage  = recomendacion,
        )

    def _calcular_nivel_detalle(
        self,
        tipo:          str,
        confianza:     float,
        prio_emocional: bool,
        modo_mental:   str,
    ) -> str:
        # Técnico/ejecutivo → detallado siempre
        if tipo in ('tecnica_groq', 'matematica_python', 'ejecutiva'):
            return 'detallado'
        # Emocional con prioridad → breve (presencia, no info)
        if tipo == 'emocional' and prio_emocional:
            return 'breve'
        # Informativo con alta confianza → detallado
        if tipo == 'informativa' and confianza > 0.80:
            return 'detallado'
        # Modo exploratorio → detallado
        if modo_mental == 'exploratorio' and confianza > 0.75:
            return 'detallado'
        # Default
        return 'normal'