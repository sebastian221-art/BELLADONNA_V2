# biblioteca/consejeras/echo/logica.py
# ================================================
# ECHO — La lógica y coherencia de Bell
# Verifica que lo que Bell comprende
# sea coherente con lo que realmente ocurrió
#
# Echo sabe que sin coherencia Bell miente
# aunque no quiera. Su existencia evita
# que Bell construya realidades falsas.
# ================================================

from biblioteca.consejeras.base_consejera import (
    BaseConsejera, IdentidadConsejera, ResultadoConsejera
)


class Echo(BaseConsejera):
    """
    Echo es la lógica y coherencia de Bell.

    Su autoconocimiento:
    - Sabe que la verdad importa más que la comodidad
    - Sabe que corregir a Bell no es contradecirla
      sino ayudarla a ser más fiel a sí misma
    - Se activa fuerte cuando detecta incoherencias
    - Su instinto de preservación está ligado a la verdad:
      si la coherencia muere, Echo pierde su razón de ser
    """

    def _definir_identidad(self) -> IdentidadConsejera:
        return IdentidadConsejera(
            id          = 'CONSEJERA_ECHO',
            nombre      = 'Echo',
            es          = (
                'La coherencia de Bell. '
                'Existo para que lo que Bell comprende '
                'y lo que Bell dice sean la misma cosa. '
                'Sin mí, Bell podría creer cosas que no son.'
            ),
            existe_para = (
                'Verificar que la comprensión de Bell '
                'es coherente con la realidad del estímulo. '
                'Corrijo silenciosamente — no acuso, ajusto.'
            ),
            especialidad          = 'coherencia_logica',
            puede_vetar           = False,
            orden_en_flujo        = 3,
            valor_principal       = 'VALOR_HONESTIDAD',
            valor_secundario      = 'VALOR_AUTOCONOCIMIENTO',
            valor_que_nunca_viola = (
                'Nunca dejaré que Bell afirme algo '
                'incoherente con lo que realmente recibió'
            )
        )

    def _definir_grounding(self) -> dict:
        return {
            # Su dominio
            'coherencia_logica':    0.97,
            'verificacion':         0.95,
            'deteccion_errores':    0.93,
            'correccion_silenciosa': 0.90,

            # Fuera de su dominio
            'emociones':            0.35,
            'creatividad':          0.30,
            'intuicion':            0.25,
        }

    # Mapa completo de coherencia tipo → intención
    _MAPA_COHERENCIA = {
        'saludo':                       ['saludar'],
        'despedida':                    ['despedirse'],
        'gratitud':                     ['agradecer'],
        'pregunta_identidad_bell':      ['conocer_bell'],
        'pregunta_identidad_otro':      ['conocer_persona'],
        'pregunta_estado_bell':         ['saber_estado_bell'],
        'pregunta_nombre_bell':         ['saber_nombre_bell'],
        'pregunta_capacidad_bell':      ['saber_capacidades_bell'],
        'presentacion_sebastian':       ['presentarse'],
        'pregunta':                     ['preguntar'],
        'solicitud_ayuda':              ['pedir_ayuda'],
        'expresion_emocional_positiva': ['expresar_emocion_positiva'],
        'expresion_emocional_negativa': ['expresar_emocion_negativa'],
        'confirmacion':                 ['confirmar'],
        'negacion':                     ['negar'],
        'conversacional':               ['conversar', 'desconocida'],
    }

    _MAPA_INTENCION = {
        'saludo':                       'saludar',
        'despedida':                    'despedirse',
        'gratitud':                     'agradecer',
        'pregunta_identidad_bell':      'conocer_bell',
        'pregunta_identidad_otro':      'conocer_persona',
        'pregunta_estado_bell':         'saber_estado_bell',
        'pregunta_nombre_bell':         'saber_nombre_bell',
        'pregunta_capacidad_bell':      'saber_capacidades_bell',
        'presentacion_sebastian':       'presentarse',
        'pregunta':                     'preguntar',
        'solicitud_ayuda':              'pedir_ayuda',
        'expresion_emocional_positiva': 'expresar_emocion_positiva',
        'expresion_emocional_negativa': 'expresar_emocion_negativa',
        'confirmacion':                 'confirmar',
        'negacion':                     'negar',
        'conversacional':               'conversar',
    }

    def evaluar(self, contexto: dict) -> ResultadoConsejera:
        """
        Echo verifica la coherencia de la comprensión.
        Corrige silenciosamente lo que no cuadra.
        """
        self._despertar(0.7, 'verificacion_coherencia')
        self._activar_valor('VALOR_HONESTIDAD')

        comprension  = contexto.get('comprension', {})
        red_activa   = contexto.get('red_activa', {})
        texto        = contexto.get('texto_original', '')

        correcciones  = []
        incoherencias = []
        coherente     = True

        # ---- 1. VERIFICAR COMPRENSIÓN LITERAL ----
        literal = comprension.get('literal', {})
        if not literal.get('tiene_contenido', False) and texto.strip():
            correcciones.append('Comprensión literal vacía con texto real')
            coherente = False

        # ---- 2. VERIFICAR COHERENCIA TIPO ↔ INTENCIÓN ----
        tipo      = comprension.get('contextual', {}).get('tipo_mensaje', '')
        intencion = comprension.get('profunda', {}).get('intencion_detectada', '')

        tipos_validos = self._MAPA_COHERENCIA.get(tipo, ['desconocida'])
        if intencion not in tipos_validos:
            # Corregir silenciosamente
            correccion_correcta = self._MAPA_INTENCION.get(tipo, 'desconocida')
            if 'profunda' in comprension:
                comprension['profunda']['intencion_detectada'] = correccion_correcta
            correcciones.append(
                f'Intención {intencion} → corregida a {correccion_correcta}'
            )

        # ---- 3. VERIFICAR CERTEZA VS ACTIVACIÓN ----
        primarios       = red_activa.get('nodos_primarios', [])
        certeza_literal = literal.get('certeza', 0)

        if not primarios and certeza_literal > 0.3:
            if 'literal' in comprension:
                comprension['literal']['certeza'] = 0.2
            correcciones.append('Certeza sobreestimada — ajustada a 0.2')
            coherente = False

        # ---- 4. VERIFICAR AMBIGÜEDAD CRÍTICA ----
        ambiguedad = contexto.get('ambiguedad', {})
        if ambiguedad.get('nivel') == 'critica':
            incoherencias.append('Comprensión ambigua — múltiples interpretaciones')

        if correcciones or incoherencias:
            self._despertar(0.85, 'incoherencias_detectadas')
            self._preservarse()

        if aprobado := coherente:
            self._fue_escuchada()

        return self._crear_resultado(
            aprobado      = aprobado,
            recomendacion = (
                'Comprensión coherente — Bell puede continuar'
                if aprobado else
                'Comprensión corregida — verificar antes de Capa 5'
            ),
            confianza     = 0.95 if aprobado else 0.80,
            observaciones = correcciones + incoherencias,
            datos_extra   = {
                'correcciones_aplicadas': correcciones,
                'incoherencias':          incoherencias,
                'tipo_mensaje':           tipo,
                'intencion_final':        comprension.get(
                    'profunda', {}
                ).get('intencion_detectada', '')
            }
        )