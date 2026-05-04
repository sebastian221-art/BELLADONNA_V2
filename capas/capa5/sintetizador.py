# capas/capa5/sintetizador.py
# ================================================
# SINTETIZADOR — Capa 5
#
# FIX: intenciones alineadas con las que genera
# el motor real. Antes usaba 'preguntar_identidad'
# cuando el motor genera 'conocer_bell'.
# ================================================

from capas.capa5.paquete_capa5 import InstruccionRespuesta

_TONOS_VALIDOS = {
    'empático_suave', 'presente_inmediato', 'cálido_genuino',
    'celebratorio_cálido', 'cercano_natural', 'atento_sensible',
    'tranquilizador_suave', 'empático_firme', 'honesto_directo',
}

_TONO_DEFAULT = 'cercano_natural'

# FIX: nombres alineados con intenciones reales del motor
_TIPO_POR_INTENCION = {
    # Conversacionales
    'saludar':                    'conversacional',
    'despedirse':                 'conversacional',
    'agradecer':                  'conversacional',
    'conversar':                  'conversacional',
    'presentarse':                'conversacional',
    'confirmar':                  'conversacional',
    'negar':                      'conversacional',
    'preguntar':                  'conversacional',  # preguntas sobre Sebastian etc.
    # Informativas sobre Bell
    'conocer_bell':               'informativa',
    'saber_estado_bell':          'informativa',
    'saber_nombre_bell':          'informativa',
    'saber_capacidades_bell':     'informativa',
    # Emocionales
    'expresar_emocion_negativa':  'emocional',
    'expresar_emocion_positiva':  'emocional',
    'pedir_ayuda':                'emocional',
    # Ejecutivas
    'ejecutar_comando':           'ejecutiva',
    'calcular':                   'ejecutiva',
    'analizar_codigo':            'ejecutiva',
    'crear_archivo':              'ejecutiva',
    'buscar':                     'ejecutiva',
    'consultar_bd':               'ejecutiva',
}


class Sintetizador:

    def sintetizar(self, deliberacion, paquete_capa4) -> InstruccionRespuesta:
        try:
            return self._sintetizar_interno(deliberacion, paquete_capa4)
        except Exception as e:
            return InstruccionRespuesta(
                tipo_respuesta     = 'conversacional',
                tono               = _TONO_DEFAULT,
                confianza          = 0.5,
                recomendacion_sage = f'Síntesis parcial: {e}',
            )

    def _sintetizar_interno(self, deliberacion, paquete_capa4) -> InstruccionRespuesta:
        ctx       = paquete_capa4.get('contexto_consejeras', {})
        intencion = ctx.get('intencion_detectada', 'conversar')
        capacidad = paquete_capa4.get('capacidad', {})

        if hasattr(deliberacion, 'a_dict'):
            delib_dict = deliberacion.a_dict()
        else:
            delib_dict = deliberacion if isinstance(deliberacion, dict) else {}

        tono_sage           = delib_dict.get('tono_final', _TONO_DEFAULT)
        recomendacion       = delib_dict.get('recomendacion_sage', '')
        confianza           = delib_dict.get('confianza_colectiva', 0.8)
        prioridad_emocional = delib_dict.get('prioridad_emocional', False)

        tono = tono_sage if tono_sage in _TONOS_VALIDOS else _TONO_DEFAULT
        tipo = _TIPO_POR_INTENCION.get(intencion, 'conversacional')

        # Si capacidad reporta limitación — honestidad
        tipo_cap = capacidad.get('tipo_respuesta', '')
        if tipo_cap == 'honestidad_limitacion':
            tipo = 'honestidad_limitacion'

        # Nivel de detalle
        if tipo == 'informativa' and confianza > 0.8:
            nivel_detalle = 'detallado'
        elif tipo in ('conversacional', 'emocional'):
            nivel_detalle = 'breve' if prioridad_emocional else 'normal'
        else:
            nivel_detalle = 'normal'

        return InstruccionRespuesta(
            tipo_respuesta      = tipo,
            tono                = tono,
            confianza           = round(confianza, 3),
            prioridad_emocional = prioridad_emocional,
            incluir_nombre      = True,
            nivel_detalle       = nivel_detalle,
            recomendacion_sage  = recomendacion,
        )