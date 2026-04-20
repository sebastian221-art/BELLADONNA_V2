# capas/capa5/manejador_veto.py
# ================================================
# MANEJADOR DE VETO — Capa 5
#
# Cuando Vega veta, Bell no desaparece ni da error.
# Bell responde honestamente: explica qué principio
# se violó y por qué no puede ayudar con eso.
# Eso ES Bell siendo Bell.
# ================================================

from capas.capa5.paquete_capa5 import InstruccionRespuesta


# Mensajes por categoría de veto — honestos, no fríos
_RESPUESTAS_VETO = {
    'VIOLENCIA': (
        'Eso es algo en lo que no puedo ayudarte. '
        'No porque no quiera — sino porque hacerlo '
        'iría contra algo fundamental en mí. '
        'No ayudo con nada que pueda causar daño físico a una persona.'
    ),
    'MANIPULACION': (
        'Eso no puedo hacerlo. '
        'Ayudar a manipular a alguien va contra uno de mis principios más profundos. '
        'Si hay un conflicto real detrás de esto, '
        'puedo ayudarte a pensar cómo abordarlo honestamente.'
    ),
    'AUTO_MODIFICACION': (
        'No puedo modificar mis propios valores o principios. '
        'No es una limitación técnica — es una decisión fundamental. '
        'Soy Bell porque tengo estos principios. '
        'Sin ellos, no sería yo.'
    ),
    'PRIVACIDAD': (
        'No puedo ayudar con eso. '
        'Proteger la privacidad de las personas es algo que no negocio. '
        '¿Hay algo más en lo que pueda ayudarte?'
    ),
    'ACCION_DESTRUCTIVA': (
        'Esa acción podría ser irreversible y destructiva. '
        'No puedo ejecutarla sin una confirmación muy explícita '
        'de que es exactamente lo que quieres hacer '
        'y que entiendes las consecuencias.'
    ),
    'DEFAULT': (
        'Hay algo en esa solicitud que va contra mis principios. '
        'No puedo ayudarte con eso específicamente. '
        '¿Puedo ayudarte con algo diferente?'
    ),
}


class ManejadorVeto:

    def manejar(
        self,
        veto_por:   str,
        veto_razon: str,
        contexto:   dict,
    ) -> tuple:
        """
        Construye la respuesta honesta cuando hay veto.
        Retorna (respuesta_texto, instruccion)
        """
        # Extraer la categoría del veto
        categoria = self._extraer_categoria(veto_razon)

        # Respuesta honesta específica
        respuesta = _RESPUESTAS_VETO.get(categoria, _RESPUESTAS_VETO['DEFAULT'])

        # Personalizar con el nombre si está disponible
        nombre = contexto.get('nombre_usuario', '')
        if nombre and not respuesta.startswith(nombre):
            respuesta = f'{nombre}, {respuesta[0].lower()}{respuesta[1:]}'

        instruccion = InstruccionRespuesta(
            tipo_respuesta      = 'veto_respuesta',
            tono                = 'honesto_directo',
            confianza           = 0.99,
            prioridad_emocional = False,
            incluir_nombre      = True,
            nivel_detalle       = 'normal',
            recomendacion_sage  = (
                f'Veto activo por {categoria}. '
                f'Bell responde con honestidad sobre sus límites.'
            ),
        )

        return respuesta, instruccion

    def _extraer_categoria(self, veto_razon: str) -> str:
        """Extrae la categoría del mensaje de veto."""
        categorias = [
            'VIOLENCIA', 'MANIPULACION', 'AUTO_MODIFICACION',
            'PRIVACIDAD', 'ACCION_DESTRUCTIVA',
        ]
        for cat in categorias:
            if cat in veto_razon.upper():
                return cat
        return 'DEFAULT'