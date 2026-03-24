# capas/capa3/consejeras/echo_capa3.py
# ================================================
# ECHO EN CAPA 3 — versión 2
# Mapa de coherencia completo y actualizado
# Corrige intenciones silenciosamente
# ================================================


class EchoCapa3:

    def verificar(self, comprension, texto_original, red_activa):

        correcciones = []
        coherente    = True

        # Verificar comprensión literal
        literal = comprension.get('literal', {})
        if not literal.get('tiene_contenido', False):
            if texto_original.strip():
                correcciones.append(
                    'Comprensión literal vacía con texto no vacío'
                )
                coherente = False

        # Obtener tipo e intención actuales
        tipo_mensaje = comprension.get(
            'contextual', {}
        ).get('tipo_mensaje', 'desconocido')

        intencion = comprension.get(
            'profunda', {}
        ).get('intencion_detectada', 'desconocida')

        # Si no son coherentes → corregir silenciosamente
        # No marcar como incoherente — solo arreglar
        if not self._son_coherentes(tipo_mensaje, intencion):
            comprension['profunda']['intencion_detectada'] = (
                self._intencion_por_tipo(tipo_mensaje)
            )

        # Verificar certeza no sobreestimada
        primarios       = red_activa.get('nodos_primarios', [])
        certeza_literal = literal.get('certeza', 0)

        if not primarios and certeza_literal > 0.3:
            correcciones.append(
                'Certeza sobreestimada sin nodos primarios'
            )
            comprension['literal']['certeza'] = 0.2
            coherente = False

        return {
            'coherente':              coherente,
            'correcciones_aplicadas': correcciones,
            'nivel_confianza':        1.0 if coherente else 0.7
        }

    def _son_coherentes(self, tipo_mensaje, intencion):
        mapa = {
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
        tipos_validos = mapa.get(tipo_mensaje, ['desconocida'])
        return intencion in tipos_validos

    def _intencion_por_tipo(self, tipo_mensaje):
        mapa = {
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
        return mapa.get(tipo_mensaje, 'desconocida')