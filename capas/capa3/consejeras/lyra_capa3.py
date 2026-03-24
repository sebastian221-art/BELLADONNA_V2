# capas/capa3/consejeras/lyra_capa3.py
# ================================================
# LYRA EN CAPA 3
# Lectura emocional y psicológica
# Primera consejera que interviene en el flujo
# ================================================


class LyraCapa3:
    """
    Lyra lee la dimensión emocional del mensaje.
    No analiza texto directamente — interpreta
    la comprensión profunda que ya construyó
    el Constructor de Comprensión.
    """

    # Tonos recomendados según estado emocional
    TONOS_RESPUESTA = {
        'emocion_positiva': 'celebratorio_cálido',
        'emocion_negativa': 'empático_suave',
        'gratitud':         'cálido_genuino',
        'saludo':           'cercano_natural',
        'pregunta':         'claro_directo',
        'accion':           'eficiente_amigable',
        'desconocida':      'neutral_atento'
    }

    def leer(
        self,
        texto_original: str,
        tono: str,
        comprension_profunda: dict,
        contexto: dict
    ) -> dict:
        """
        Lyra lee la dimensión emocional completa.
        """
        intencion = comprension_profunda.get(
            'intencion_detectada', 'desconocida'
        )
        necesidad = comprension_profunda.get(
            'necesidad_real', 'desconocida'
        )
        emocion   = comprension_profunda.get(
            'emocion_detectada', 'neutra'
        )

        # Estado emocional de Sebastian
        estado_emocional = self._evaluar_estado(
            tono, emocion, texto_original
        )

        # Tono recomendado para la respuesta
        tono_respuesta = self.TONOS_RESPUESTA.get(
            intencion,
            self.TONOS_RESPUESTA['desconocida']
        )

        # Observaciones de Lyra
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

    def _evaluar_estado(
        self,
        tono: str,
        emocion: str,
        texto: str
    ) -> str:
        if tono == 'urgente':
            return 'urgente'
        if emocion == 'emocion_negativa':
            return 'necesita_apoyo'
        if emocion == 'gratitud':
            return 'agradecido'
        if emocion == 'emocion_positiva':
            return 'positivo'
        if tono == 'emocional':
            return 'emocional'
        return 'neutro'

    def _generar_observaciones(
        self,
        estado: str,
        necesidad: str,
        contexto: dict
    ) -> list:
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