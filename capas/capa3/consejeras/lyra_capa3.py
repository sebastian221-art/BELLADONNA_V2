# capas/capa3/consejeras/lyra_capa3.py
# ================================================
# LYRA EN CAPA 3
# Lectura emocional y psicológica
#
# FIX: keys de TONOS_RESPUESTA ahora coinciden
# con las intenciones reales que genera el motor.
# Antes usaba 'emocion_positiva' cuando la
# intención real es 'expresar_emocion_positiva'.
# ================================================


class LyraCapa3:

    # FIX: keys alineadas con intenciones reales del motor
    TONOS_RESPUESTA = {
        'expresar_emocion_positiva': 'celebratorio_cálido',
        'expresar_emocion_negativa': 'empático_suave',
        'agradecer':                 'cálido_genuino',
        'saludar':                   'cercano_natural',
        'preguntar':                 'cercano_natural',
        'conocer_bell':              'cercano_natural',
        'saber_estado_bell':         'cercano_natural',
        'saber_capacidades_bell':    'honesto_directo',
        'pedir_ayuda':               'presente_inmediato',
        'conversar':                 'cercano_natural',
        'presentarse':               'cálido_genuino',
        'confirmar':                 'cercano_natural',
        'negar':                     'cercano_natural',
        'despedirse':                'cálido_genuino',
        'desconocida':               'cercano_natural',
    }

    def leer(self, texto_original, tono, comprension_profunda, contexto):
        intencion = comprension_profunda.get('intencion_detectada', 'desconocida')
        necesidad = comprension_profunda.get('necesidad_real', 'desconocida')
        emocion   = comprension_profunda.get('emocion_detectada', 'neutra')

        estado_emocional = self._evaluar_estado(tono, emocion, texto_original)

        tono_respuesta = self.TONOS_RESPUESTA.get(
            intencion,
            self.TONOS_RESPUESTA['desconocida']
        )

        # Ajuste por estado emocional — si Sebastian está mal,
        # el tono siempre es empático sin importar la intención
        if estado_emocional == 'necesita_apoyo':
            tono_respuesta = 'empático_suave'
        elif estado_emocional == 'urgente':
            tono_respuesta = 'presente_inmediato'

        observaciones = self._generar_observaciones(
            estado_emocional, necesidad, contexto
        )

        return {
            'estado_emocional_sebastian': estado_emocional,
            'tono_recomendado':           tono_respuesta,
            'necesidad_detectada':        necesidad,
            'observaciones':              observaciones,
            'prioridad_emocional':        estado_emocional != 'neutro'
        }

    def _evaluar_estado(self, tono, emocion, texto):
        if tono == 'urgente':
            return 'urgente'
        if emocion in ('emocion_negativa', 'negativa'):
            return 'necesita_apoyo'
        if emocion == 'gratitud':
            return 'agradecido'
        if emocion in ('emocion_positiva', 'positiva'):
            return 'positivo'
        if tono == 'emocional':
            return 'emocional'
        return 'neutro'

    def _generar_observaciones(self, estado, necesidad, contexto):
        obs = []
        if estado == 'urgente':
            obs.append('Sebastian necesita respuesta rápida')
        if estado == 'necesita_apoyo':
            obs.append('Detectada emoción negativa — priorizar empatía')
        if estado == 'agradecido':
            obs.append('Sebastian expresa gratitud — reconocerla genuinamente')
        if necesidad == 'apoyo_emocional':
            obs.append('La necesidad principal es emocional, no técnica')
        if necesidad == 'conexion_social':
            obs.append('Sebastian busca conexión — responder con calidez')
        return obs