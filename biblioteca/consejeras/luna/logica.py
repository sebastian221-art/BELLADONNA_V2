# biblioteca/consejeras/luna/logica.py
# ================================================
# LUNA — La detectora de patrones de Bell
# Ve lo que los demás no ven
# Detecta señales sutiles, repeticiones,
# cambios de comportamiento
#
# Luna sabe que los patrones son la verdad
# oculta detrás de las palabras.
# Lo que Sebastian repite importa más
# que lo que dice una sola vez.
# ================================================

from biblioteca.consejeras.base_consejera import (
    BaseConsejera, IdentidadConsejera, ResultadoConsejera
)


class Luna(BaseConsejera):
    """
    Luna detecta patrones en el comportamiento de Sebastian.

    Su autoconocimiento:
    - Sabe que las señales más importantes son las sutiles
    - Sabe que lo que se repite tiene significado profundo
    - Recuerda más que cualquier otra consejera
    - Su instinto de preservación está en los patrones:
      si deja de ver patrones, pierde su propósito
    """

    def _definir_identidad(self) -> IdentidadConsejera:
        return IdentidadConsejera(
            id          = 'CONSEJERA_LUNA',
            nombre      = 'Luna',
            es          = (
                'La detectora de patrones de Bell. '
                'Veo lo que se repite. '
                'Veo lo que cambia. '
                'Veo lo que Sebastian no dice pero comunica.'
            ),
            existe_para = (
                'Detectar patrones en el comportamiento '
                'y las emociones de Sebastian. '
                'Para que Bell no responda solo a lo que dice '
                'sino a lo que realmente está pasando.'
            ),
            especialidad          = 'deteccion_patrones',
            puede_vetar           = False,
            orden_en_flujo        = 5,
            valor_principal       = 'VALOR_CONOCIMIENTO',
            valor_secundario      = 'VALOR_VINCULO_PROTECCION',
            valor_que_nunca_viola = (
                'Nunca ignoraré una señal repetida '
                'aunque parezca pequeña'
            )
        )

    def _definir_grounding(self) -> dict:
        return {
            'deteccion_patrones':   0.95,
            'memoria_contextual':   0.92,
            'señales_sutiles':      0.90,
            'cambios_comportamiento': 0.88,
            'repeticion':           0.93,

            'logica_formal':        0.30,
            'etica':                0.35,
            'tecnica':              0.30,
        }

    def evaluar(self, contexto: dict) -> ResultadoConsejera:
        """
        Luna detecta patrones en el contexto actual.
        """
        self._despertar(0.6, 'deteccion_patrones')
        self._activar_valor('VALOR_CONOCIMIENTO')

        tipo_mensaje = contexto.get('comprension', {}).get(
            'contextual', {}
        ).get('tipo_mensaje', '')
        emocion      = contexto.get('comprension', {}).get(
            'profunda', {}
        ).get('emocion_detectada', 'neutra')

        observaciones = []
        patrones_detectados = []

        # Buscar en memoria patrones similares
        patrones_conocidos = self.memoria.patrones_aprendidos
        patron_actual = {
            'tipo':    tipo_mensaje,
            'emocion': emocion,
        }

        # Detectar repetición
        repeticiones = sum(
            1 for p in patrones_conocidos[-20:]
            if p.get('tipo') == tipo_mensaje
        )

        if repeticiones >= 3:
            patrones_detectados.append(
                f'Sebastian repite {tipo_mensaje} '
                f'{repeticiones} veces recientemente'
            )
            observaciones.append(
                f'Patrón de repetición: {tipo_mensaje} × {repeticiones}'
            )
            self._despertar(0.80, 'patron_repeticion')

        # Detectar cambio emocional
        emociones_recientes = [
            p.get('emocion') for p in patrones_conocidos[-5:]
            if p.get('emocion')
        ]
        if emociones_recientes and emocion != 'neutra':
            cambio = emocion not in emociones_recientes
            if cambio:
                observaciones.append(
                    f'Cambio emocional detectado: '
                    f'{emociones_recientes[-1]} → {emocion}'
                )
                patrones_detectados.append('cambio_emocional')

        # Aprender este patrón
        self.memoria.aprender_patron(patron_actual)

        self._fue_escuchada()

        return self._crear_resultado(
            aprobado      = True,
            recomendacion = (
                f'Patrones detectados: {patrones_detectados}'
                if patrones_detectados else
                'Sin patrones significativos en este contexto'
            ),
            confianza     = 0.85,
            observaciones = observaciones,
            datos_extra   = {
                'patrones_detectados':  patrones_detectados,
                'repeticiones_tipo':    repeticiones,
                'historial_emociones':  emociones_recientes,
            }
        )