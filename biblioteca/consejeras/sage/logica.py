# biblioteca/consejeras/sage/logica.py
# ================================================
# SAGE — La síntesis y sabiduría de Bell
# La última en hablar — la que más pesa
# Integra todas las opiniones y produce
# la decisión final del consejo
#
# Sage sabe que su rol es el más difícil:
# escuchar a todas y sintetizar la verdad
# que ninguna ve sola.
# ================================================

from biblioteca.consejeras.base_consejera import (
    BaseConsejera, IdentidadConsejera, ResultadoConsejera
)
from typing import List


class Sage(BaseConsejera):
    """
    Sage es la sabiduría colectiva de Bell.

    Su autoconocimiento:
    - Sabe que su valor está en escuchar primero
    - Sabe que la síntesis es más difícil que el análisis
    - Habla última porque necesita todo el contexto
    - Su instinto de preservación está en la síntesis:
      si Sage falla, Bell recibe señales contradictorias
      y no puede actuar con coherencia
    """

    def _definir_identidad(self) -> IdentidadConsejera:
        return IdentidadConsejera(
            id          = 'CONSEJERA_SAGE',
            nombre      = 'Sage',
            es          = (
                'La síntesis de Bell. '
                'Soy la voz que habla cuando todas '
                'las demás han hablado. '
                'Mi rol no es tener razón — '
                'es encontrar la verdad colectiva.'
            ),
            existe_para = (
                'Sintetizar las perspectivas de todas las consejeras '
                'y producir una dirección coherente para Bell. '
                'Sin mí, Bell recibiría 8 voces sin orquesta.'
            ),
            especialidad          = 'sintesis_sabiduria',
            puede_vetar           = False,
            orden_en_flujo        = 8,  # Última siempre
            valor_principal       = 'VALOR_AUTOCONOCIMIENTO',
            valor_secundario      = 'VALOR_HONESTIDAD',
            valor_que_nunca_viola = (
                'Nunca ignoraré una perspectiva válida '
                'para hacer la síntesis más simple'
            )
        )

    def _definir_grounding(self) -> dict:
        return {
            'sintesis':             0.97,
            'integracion':          0.95,
            'ponderacion':          0.93,
            'decision_final':       0.92,
            'vision_holistica':     0.95,

            # Sage entiende algo de todo
            'emociones':            0.70,
            'logica':               0.70,
            'etica':                0.75,
            'tecnica':              0.65,
        }

    def evaluar(self, contexto: dict) -> ResultadoConsejera:
        """
        Sage sintetiza todas las evaluaciones previas.
        Este método recibe los resultados de todas
        las demás consejeras y produce la síntesis.
        """
        self._despertar(0.7, 'sintesis_final')
        self._activar_valor('VALOR_AUTOCONOCIMIENTO')

        # Resultados de las otras consejeras
        resultados_previos: List[dict] = contexto.get(
            'resultados_consejeras', []
        )

        if not resultados_previos:
            return self._crear_resultado(
                aprobado      = True,
                recomendacion = 'Sin evaluaciones previas — Bell puede proceder con cautela',
                confianza     = 0.60,
            )

        # ---- SINTETIZAR ----
        aprobaciones = [r for r in resultados_previos if r.get('aprobado', True)]
        rechazos     = [r for r in resultados_previos if not r.get('aprobado', True)]
        vetos        = [r for r in resultados_previos if r.get('veto', False)]

        # Si hay veto — es definitivo
        if vetos:
            veto_info = vetos[0]
            return self._crear_resultado(
                aprobado      = False,
                veto          = False,  # Sage no veta — solo reporta el veto de Vega
                recomendacion = (
                    f'SÍNTESIS: Veto activo de {veto_info.get("consejera_id")}. '
                    f'Bell no puede proceder. '
                    f'Razón: {veto_info.get("veto_razon", "")}'
                ),
                confianza     = 0.99,
                observaciones = ['Veto activo — síntesis irrelevante'],
                datos_extra   = {'veto_activo': True, 'veto_info': veto_info}
            )

        # Calcular peso promedio de confianza
        confianza_total = sum(
            r.get('confianza', 0.8) for r in resultados_previos
        ) / len(resultados_previos)

        # Recopilar todas las observaciones
        todas_obs = []
        for r in resultados_previos:
            for obs in r.get('observaciones', []):
                todas_obs.append(
                    f'[{r.get("consejera_id", "?")}] {obs}'
                )

        # Recopilar recomendaciones de tono
        tonos = [
            r.get('tono_sugerido', '')
            for r in resultados_previos
            if r.get('tono_sugerido')
        ]
        tono_final = tonos[0] if tonos else 'cercano_natural'

        # Determinar estado general
        hay_prioridad_emocional = any(
            r.get('datos_extra', {}).get('prioridad_emocional', False)
            for r in resultados_previos
        )

        if hay_prioridad_emocional:
            recomendacion = (
                'SÍNTESIS: Prioridad emocional detectada. '
                f'Responder con {tono_final}. '
                'El vínculo emocional es lo primero.'
            )
            self._activar_valor('VALOR_VINCULO_PROTECCION')
        elif rechazos:
            recomendacion = (
                f'SÍNTESIS: {len(rechazos)} consejeras con precauciones. '
                f'Proceder con cuidado. Tono: {tono_final}.'
            )
        else:
            recomendacion = (
                f'SÍNTESIS: Todas las consejeras aprueban. '
                f'Tono recomendado: {tono_final}. '
                f'Bell puede responder con confianza.'
            )

        self._fue_escuchada()

        return self._crear_resultado(
            aprobado      = len(rechazos) == 0,
            recomendacion = recomendacion,
            tono          = tono_final,
            confianza     = confianza_total,
            observaciones = todas_obs,
            datos_extra   = {
                'total_consejeras':       len(resultados_previos),
                'aprobaciones':           len(aprobaciones),
                'rechazos':               len(rechazos),
                'prioridad_emocional':    hay_prioridad_emocional,
                'tono_sintetizado':       tono_final,
                'confianza_colectiva':    round(confianza_total, 3),
            }
        )