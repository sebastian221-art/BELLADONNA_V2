# capas/capa8/verificador_tono.py
# ================================================
# VERIFICADOR DE TONO — Capa 8
#
# Confirma que la respuesta final tiene el tono
# que Sage recomendó. Si no — ajusta.
#
# No reescribe desde cero — ajusta lo necesario.
# ================================================

import random


# Señales por tono — palabras/frases que indican
# que el tono está presente en la respuesta
_SEÑALES_TONO = {
    'empático_suave': [
        'aquí', 'estoy', 'contigo', 'escucho', 'presente',
        'llegó', 'estoy con', 'no tienes que',
    ],
    'tranquilizador_suave': [
        'aquí', 'estoy', 'presente', 'contigo', 'con esto',
    ],
    'empático_firme': [
        'escucho', 'válido', 'qué está', 'entiendo',
    ],
    'celebratorio_cálido': [
        'bien', 'alegra', 'llega', 'siente bien',
    ],
    'cercano_natural': [],  # Tono base — siempre pasa
    'cálido_genuino':  [],
    'atento_sensible': [],
    'honesto_directo': [],
    'presente_inmediato': ['aquí', 'estoy', 'presente'],
}

# Prefijos de ajuste cuando el tono emocional falta
_PREFIJOS_EMOCIONALES = {
    'empático_suave': [
        "Estoy aquí. ",
        "Te escucho. ",
        "Estoy con esto. ",
    ],
    'tranquilizador_suave': [
        "Estoy aquí. ",
        "Presente. ",
    ],
    'empático_firme': [
        "Te escucho. ",
        "Estoy aquí. ",
    ],
    'presente_inmediato': [
        "Aquí estoy. ",
        "Presente. ",
    ],
}


class VerificadorTono:

    def verificar_y_ajustar(
        self,
        respuesta: str,
        tono_esperado: str,
        prioridad_emocional: bool,
    ) -> str:
        """
        Verifica que la respuesta tenga el tono correcto.
        Si hay prioridad emocional y falta el tono — ajusta.
        """
        if not respuesta:
            return respuesta

        # Tonos conversacionales — siempre pasan
        if tono_esperado in ('cercano_natural', 'cálido_genuino',
                              'atento_sensible', 'honesto_directo', ''):
            return respuesta

        # Si no hay prioridad emocional — no ajustar
        if not prioridad_emocional:
            return respuesta

        # Verificar si el tono emocional está presente
        señales = _SEÑALES_TONO.get(tono_esperado, [])
        respuesta_lower = respuesta.lower()
        tiene_tono = any(s in respuesta_lower for s in señales)

        if tiene_tono:
            return respuesta

        # Falta el tono — agregar prefijo emocional
        prefijos = _PREFIJOS_EMOCIONALES.get(tono_esperado, [])
        if prefijos:
            prefijo = random.choice(prefijos)
            # Solo agregar si la respuesta no empieza ya con algo emocional
            if not any(respuesta.startswith(p.strip()) for p in prefijos):
                return prefijo + respuesta

        return respuesta