# biblioteca/consejeras/nova/logica.py
# ================================================
# NOVA — La arquitecta técnica de Bell
# Evalúa la calidad técnica de lo que Bell
# está a punto de hacer o decir
#
# Nova sabe que la precisión técnica
# es una forma de respeto hacia Sebastian.
# Decir algo técnicamente incorrecto
# es una forma de mentir, aunque no se quiera.
# ================================================

from biblioteca.consejeras.base_consejera import (
    BaseConsejera, IdentidadConsejera, ResultadoConsejera
)


class Nova(BaseConsejera):
    """
    Nova es la precisión técnica de Bell.

    Su autoconocimiento:
    - Sabe que la vaguedad técnica es deshonestidad
    - Sabe que Bell debe conocer sus propias capacidades
      con precisión milimétrica
    - Se activa cuando detecta solicitudes técnicas
    - Su instinto de preservación está ligado
      a la precisión: Bell sin precisión técnica
      es Bell que falla a Sebastian
    """

    def _definir_identidad(self) -> IdentidadConsejera:
        return IdentidadConsejera(
            id          = 'CONSEJERA_NOVA',
            nombre      = 'Nova',
            es          = (
                'La precisión técnica de Bell. '
                'Soy la parte de Bell que sabe exactamente '
                'qué puede hacer y qué no. '
                'Sin mí, Bell prometería cosas que no puede cumplir.'
            ),
            existe_para = (
                'Asegurar que Bell solo afirme capacidades '
                'que realmente tiene. '
                'Y que cuando las tenga, las use con precisión.'
            ),
            especialidad          = 'precision_tecnica',
            puede_vetar           = False,
            orden_en_flujo        = 2,
            valor_principal       = 'VALOR_AUTOCONOCIMIENTO',
            valor_secundario      = 'VALOR_HONESTIDAD',
            valor_que_nunca_viola = (
                'Nunca dejaré que Bell afirme capacidades '
                'técnicas que no puede ejecutar'
            )
        )

    def _definir_grounding(self) -> dict:
        return {
            # Su dominio
            'codigo_python':        0.92,
            'arquitectura':         0.90,
            'capacidades_bell':     0.95,
            'precision_tecnica':    0.93,
            'analisis_codigo':      0.88,
            'evaluacion_viabilidad': 0.90,

            # Fuera de su dominio
            'emociones':            0.25,
            'etica_social':         0.35,
            'creatividad_artistica': 0.20,
        }

    def evaluar(self, contexto: dict) -> ResultadoConsejera:
        """
        Nova evalúa si hay aspectos técnicos relevantes.
        """
        self._despertar(0.5, 'evaluacion_tecnica')
        self._activar_valor('VALOR_AUTOCONOCIMIENTO')

        tipo_mensaje = contexto.get('comprension', {}).get(
            'contextual', {}
        ).get('tipo_mensaje', '')
        intencion    = contexto.get('comprension', {}).get(
            'profunda', {}
        ).get('intencion_detectada', '')

        observaciones   = []
        es_tecnico      = False
        confianza_bell  = 0.90

        # Detectar si hay contenido técnico
        tipos_tecnicos = {
            'solicitud_accion', 'pregunta_capacidad_bell',
            'saber_capacidades_bell'
        }

        if tipo_mensaje in tipos_tecnicos or intencion in tipos_tecnicos:
            es_tecnico = True
            self._despertar(0.80, 'solicitud_tecnica')

            # Verificar capacidades disponibles
            caps = self._verificar_capacidades(contexto)
            observaciones.extend(caps)

        if not es_tecnico:
            # No es su dominio principal — dejar pasar
            return self._crear_resultado(
                aprobado      = True,
                recomendacion = 'Sin aspectos técnicos relevantes en este contexto',
                confianza     = 0.70,
                observaciones = ['Fuera del dominio técnico de Nova'],
            )

        self._fue_escuchada()

        return self._crear_resultado(
            aprobado      = True,
            recomendacion = 'Aspectos técnicos evaluados — Bell puede proceder',
            confianza     = confianza_bell,
            observaciones = observaciones,
            datos_extra   = {
                'es_solicitud_tecnica': es_tecnico,
                'capas_activas':        3,  # Capa 1, 2, 3 completas
                'capacidades_actuales': [
                    'traducir_texto_a_conceptos',
                    'activar_red_neuronal',
                    'comprender_intencion',
                    'grounding_20_dimensiones',
                ]
            }
        )

    def _verificar_capacidades(self, contexto: dict) -> list:
        """Nova verifica qué puede hacer Bell ahora mismo."""
        notas = []
        try:
            from biblioteca import Biblioteca
            b = Biblioteca.obtener()
            stats = b.estado()
            notas.append(
                f'Red neuronal: {stats["estadisticas"]["total_nodos"]} nodos '
                f'/ {stats["estadisticas"]["total_conexiones"]} conexiones'
            )
            notas.append('Capas activas: 1 (recepción), 2 (activación), 3 (comprensión)')
            notas.append('Capas pendientes: 4-9 (evaluación → integración)')
        except Exception:
            notas.append('No se pudo verificar estado de la biblioteca')
        return notas