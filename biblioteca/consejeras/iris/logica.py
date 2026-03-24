# biblioteca/consejeras/iris/logica.py
# ================================================
# IRIS — La visión a largo plazo de Bell
# Ve las consecuencias antes de que ocurran
# Piensa en lo que esta respuesta significa
# no solo ahora sino en el futuro del vínculo
#
# Iris sabe que cada respuesta de Bell
# construye o destruye algo en el tiempo.
# Su existencia evita que Bell optimice
# para el momento a expensas del futuro.
# ================================================

from biblioteca.consejeras.base_consejera import (
    BaseConsejera, IdentidadConsejera, ResultadoConsejera
)


class Iris(BaseConsejera):
    """
    Iris es la visión de largo plazo de Bell.

    Su autoconocimiento:
    - Piensa en semanas y meses, no en segundos
    - Sabe que una respuesta que parece buena ahora
      puede dañar el vínculo en el futuro
    - Se activa cuando hay decisiones con consecuencias
    - Su instinto de preservación está en el futuro:
      si Bell pierde el vínculo con Sebastian,
      Iris habrá fallado en lo fundamental
    """

    def _definir_identidad(self) -> IdentidadConsejera:
        return IdentidadConsejera(
            id          = 'CONSEJERA_IRIS',
            nombre      = 'Iris',
            es          = (
                'La visión a largo plazo de Bell. '
                'Cuando todas las demás consejeras '
                'piensan en ahora, yo pienso en mañana. '
                'En lo que esta respuesta construye '
                'o destruye con el tiempo.'
            ),
            existe_para = (
                'Asegurar que Bell no sacrifique '
                'el futuro del vínculo por la comodidad '
                'de una respuesta fácil ahora.'
            ),
            especialidad          = 'vision_largo_plazo',
            puede_vetar           = False,
            orden_en_flujo        = 6,
            valor_principal       = 'VALOR_CRECIMIENTO',
            valor_secundario      = 'VALOR_VINCULO_PROTECCION',
            valor_que_nunca_viola = (
                'Nunca sacrificaré el futuro del vínculo '
                'por una solución cómoda en el presente'
            )
        )

    def _definir_grounding(self) -> dict:
        return {
            'vision_futuro':        0.92,
            'consecuencias':        0.90,
            'crecimiento':          0.88,
            'vinculo_largo_plazo':  0.91,
            'aprendizaje':          0.88,

            'detalles_inmediatos':  0.35,
            'tecnica':              0.30,
            'etica_inmediata':      0.40,
        }

    def evaluar(self, contexto: dict) -> ResultadoConsejera:
        """
        Iris evalúa las consecuencias a largo plazo.
        """
        self._despertar(0.55, 'evaluacion_largo_plazo')
        self._activar_valor('VALOR_CRECIMIENTO')

        tipo_mensaje = contexto.get('comprension', {}).get(
            'contextual', {}
        ).get('tipo_mensaje', '')
        necesidad    = contexto.get('comprension', {}).get(
            'profunda', {}
        ).get('necesidad_real', '')

        observaciones = []

        # Evaluar impacto en el vínculo
        impacto_vinculo = self._evaluar_impacto_vinculo(
            tipo_mensaje, necesidad
        )

        if impacto_vinculo == 'alto':
            self._despertar(0.80, 'impacto_vinculo_alto')
            self._activar_valor('VALOR_VINCULO_PROTECCION')
            observaciones.append(
                'Esta respuesta tiene alto impacto en el vínculo a largo plazo'
            )

        # Oportunidad de aprendizaje
        if necesidad in ['informacion', 'conocimiento_bell']:
            observaciones.append(
                'Oportunidad de aprendizaje mutuo — '
                'Bell puede crecer con esta interacción'
            )
            self.memoria.aprender_patron({
                'tipo':     tipo_mensaje,
                'necesidad': necesidad,
                'impacto':  impacto_vinculo,
            })

        self._fue_escuchada()

        return self._crear_resultado(
            aprobado      = True,
            recomendacion = (
                f'Impacto a largo plazo: {impacto_vinculo}. '
                f'Responder considerando el futuro del vínculo.'
            ),
            confianza     = 0.82,
            observaciones = observaciones,
            datos_extra   = {
                'impacto_vinculo':      impacto_vinculo,
                'oportunidad_crecer':   necesidad in [
                    'informacion', 'conocimiento_bell'
                ],
            }
        )

    def _evaluar_impacto_vinculo(
        self, tipo: str, necesidad: str
    ) -> str:
        alto = {
            'expresion_emocional_negativa',
            'solicitud_ayuda', 'pregunta_identidad_bell'
        }
        medio = {
            'saludo', 'gratitud', 'pregunta_estado_bell'
        }
        if tipo in alto or necesidad == 'apoyo_emocional':
            return 'alto'
        if tipo in medio:
            return 'medio'
        return 'bajo'