# biblioteca/habilidades/lenguaje/dimensiones/contextual.py
# ================================================
# DIMENSIÓN CONTEXTUAL
#
# Lee el mensaje en función de todo lo que
# ya ocurrió en la conversación.
#
# CORRECCIÓN: usa el historial que ya viene
# del BufferSesion (cargado por el ejecutor),
# los vocab_tipos para clasificar mejor,
# y los ids_conocidos de la red de Bell.
# ================================================

from .base import DimensionLenguaje, ResultadoDimension


class DimensionContextual(DimensionLenguaje):

    NOMBRE = 'contextual'
    PESO   = 1.1

    _REFERENCIAS_PREVIAS = [
        'eso', 'esto', 'lo mismo', 'lo anterior', 'lo que dijiste',
        'lo que hiciste', 'lo que te pedí', 'lo de antes', 'aquello',
        'como dijiste', 'como acordamos', 'sigue', 'continúa', 'continua',
        'y ahora', 'y después', 'y luego', 'el siguiente paso',
    ]

    _CORRECCIONES = [
        'no', 'espera', 'para', 'no es así', 'no es eso',
        'me equivoqué', 'quise decir', 'en realidad', 'mejor dicho',
        'en cambio', 'sino', 'más bien', 'o sea', 'es decir',
    ]

    _CAMBIOS_TEMA = [
        'otra cosa', 'cambiando de tema', 'ahora dime', 'también quiero',
        'y qué tal', 'por cierto', 'a propósito',
    ]

    def analizar(self, texto: str, contexto: dict) -> ResultadoDimension:
        try:
            return self._analizar_interno(texto, contexto)
        except Exception:
            return self._resultado_vacio()

    def _analizar_interno(self, texto: str, contexto: dict) -> ResultadoDimension:
        tl = texto.lower().strip()

        hallazgos = {}
        senales   = []

        historial       = contexto.get('historial', [])
        nombre_usuario  = contexto.get('nombre_usuario', 'Sebastian')
        turno_actual    = len(historial)
        ids_conocidos   = contexto.get('ids_conocidos', [])
        vocab_tipos     = contexto.get('vocab_tipos', {})

        hallazgos['nombre_usuario']  = nombre_usuario
        hallazgos['turno_actual']    = turno_actual
        hallazgos['tiene_historial'] = turno_actual > 0

        # ── SEBASTIAN detectado por la red ──
        if 'NEURONA_SEBASTIAN' in ids_conocidos:
            hallazgos['nombre_usuario'] = 'Sebastian'
            senales.append('sebastian_detectado')

        # ── Referencias a contexto previo ──
        refs = [r for r in self._REFERENCIAS_PREVIAS if r in tl]
        if refs:
            hallazgos['referencias_previas'] = refs
            hallazgos['necesita_historial']  = True
            if historial:
                ultimo = historial[-1]
                hallazgos['contexto_referido'] = {
                    'texto':     ultimo.get('texto', '')[:80],
                    'respuesta': ultimo.get('respuesta_bell', '')[:80],
                }
            senales.append('referencia_contexto_previo')

        # ── Continuación de tarea ──
        es_continuacion = self._es_continuacion(tl, historial)
        if es_continuacion:
            hallazgos['es_continuacion'] = True
            hallazgos['tarea_en_curso']  = es_continuacion
            senales.append('continuacion_tarea')

        # ── Corrección ──
        es_correccion = any(c in tl for c in self._CORRECCIONES) and turno_actual > 0
        if es_correccion:
            hallazgos['es_correccion'] = True
            if historial:
                hallazgos['corrige_a'] = historial[-1].get('respuesta_bell', '')[:60]
            senales.append('correccion_detectada')

        # ── Cambio de tema ──
        if any(c in tl for c in self._CAMBIOS_TEMA):
            hallazgos['cambio_de_tema'] = True
            senales.append('cambio_tema')

        # ── Tipo de mensaje en contexto ──
        # Usamos vocab_tipos para apoyar la clasificación
        tipo = self._clasificar_en_contexto(
            tl, historial, es_continuacion, es_correccion, ids_conocidos, vocab_tipos
        )
        hallazgos['tipo_mensaje'] = tipo
        senales.append(f'tipo:{tipo}')

        # ── Patrón de trabajo de Sebastian ──
        patron = self._inferir_patron(historial)
        if patron:
            hallazgos['patron_trabajo'] = patron
            senales.append(f'patron:{patron}')

        activa    = len(senales) > 0
        confianza = 0.5 + (0.08 * len(senales)) if activa else 0.3
        confianza = min(0.90, confianza)

        return self._resultado(
            activa    = activa,
            confianza = confianza,
            hallazgos = hallazgos,
            senales   = senales,
        )

    def _es_continuacion(self, texto: str, historial: list) -> str:
        marcadores = ['y ahora', 'ahora', 'siguiente paso', 'y después',
                      'y luego', 'continúa', 'sigue']
        if any(m in texto for m in marcadores) and historial:
            return historial[-1].get('texto', '')[:40]
        return ''

    def _clasificar_en_contexto(
        self, texto: str, historial: list,
        es_continuacion: bool, es_correccion: bool,
        ids_conocidos: list, vocab_tipos: dict
    ) -> str:
        if es_correccion:
            return 'correccion'
        if es_continuacion:
            return 'continuacion'

        # Tipo basado en vocab_tipos de la red de Bell
        tipos_encontrados = set(vocab_tipos.values())

        if 'pregunta_bell' in tipos_encontrados or 'identidad_bell' in tipos_encontrados:
            return 'pregunta_identidad_bell'

        if 'valor_bell' in tipos_encontrados:
            return 'pregunta_identidad_bell'

        # Saludo detectado por vocabulario de la red
        ids = set(ids_conocidos)
        if any(i.startswith('SALUDO_') for i in ids):
            return 'saludo'

        if any(i.startswith('DESPEDIDA_') for i in ids):
            return 'despedida'

        # Clasificación por contenido del texto
        preguntas = ['qué', 'que', 'cómo', 'como', 'cuándo', 'cuando',
                     'dónde', 'donde', 'quién', 'quien', 'cuál', 'cual',
                     'cuánto', 'cuanto', '?']
        if any(p in texto for p in preguntas):
            return 'pregunta'

        saludos = ['hola', 'hey', 'buenas', 'buenos', 'qué tal', 'que tal']
        if any(s in texto for s in saludos):
            return 'saludo'

        acciones = ['crea', 'hacer', 'haz', 'genera', 'escribe', 'ejecuta',
                    'corre', 'calcula', 'analiza', 'muestra', 'dame', 'pon']
        if any(a in texto for a in acciones):
            return 'solicitud_accion'

        emociones = ['gracias', 'bien', 'mal', 'cansado', 'frustrado',
                     'emocionado', 'perfecto', 'genial']
        if any(e in texto for e in emociones):
            return 'expresion_emocional'

        if not historial:
            return 'inicio_conversacion'

        return 'conversacional'

    def _inferir_patron(self, historial: list) -> str:
        if len(historial) < 3:
            return ''
        tipos = [h.get('tipo_mensaje', '') for h in historial[-5:]]
        if tipos.count('solicitud_accion') >= 3:
            return 'enfocado_en_construccion'
        if tipos.count('pregunta') >= 3:
            return 'modo_exploratorio'
        if tipos.count('conversacional') >= 3:
            return 'modo_conversacional'
        return 'mixto'


# ════════════════════════════════════════════════
# DIMENSIÓN INTRÍNSECA — en el mismo módulo
# ════════════════════════════════════════════════

class DimensionIntrinseca(DimensionLenguaje):

    NOMBRE = 'intrinseca'
    PESO   = 0.9

    _PATRONES_SUBYACENTES = {
        'busca_validacion': {
            'senales': [
                'está bien', 'verdad', 'cierto', 'correcto', 'sí o no',
                'qué crees', 'qué piensas', 'lo ves bien',
            ],
            'lectura': 'Busca confirmación de que va por buen camino',
            'respuesta_bell': 'validar_y_guiar',
        },
        'procesando_problema': {
            'senales': [
                'no sé cómo', 'no encuentro', 'no entiendo',
                'llevo rato', 'no me sale', 'no me funciona', 'algo está mal',
            ],
            'lectura': 'Está atascado y necesita perspectiva externa',
            'respuesta_bell': 'ofrecer_perspectiva_nueva',
        },
        'testando_a_bell': {
            'senales': [
                'a ver si', 'a ver qué', 'cuánto sabes', 'dime algo sobre',
                'conoces', 'has oído',
            ],
            'lectura': 'Está evaluando las capacidades de Bell',
            'respuesta_bell': 'demostrar_con_precision',
        },
        'necesita_estructura': {
            'senales': [
                'no sé por dónde empezar', 'hay mucho', 'es muy grande',
                'son muchas cosas', 'está muy desordenado',
            ],
            'lectura': 'Necesita que Bell ponga orden en el caos',
            'respuesta_bell': 'estructurar_y_priorizar',
        },
        'confiando_plenamente': {
            'senales': [
                'tú decides', 'como quieras', 'lo que creas', 'en tus manos',
                'hazlo como tú veas', 'confío en ti', 'te lo dejo',
            ],
            'lectura': 'Delega completamente — máxima confianza en Bell',
            'respuesta_bell': 'tomar_decision_y_explicar',
        },
        'buscando_conexion': {
            'senales': [
                'cómo estás', 'como estas', 'qué tal', 'hola', 'hey', 'oye',
            ],
            'lectura': 'El objetivo principal es la conexión, no la tarea',
            'respuesta_bell': 'presencia_genuina_primero',
        },
        'frustracion_con_proceso': {
            'senales': [
                'de nuevo', 'otra vez', 'siempre pasa', 'nunca funciona',
                'cada vez que', 'llevo días', 'llevo horas',
            ],
            'lectura': 'Frustración con el proceso repetido, no con la tarea',
            'respuesta_bell': 'reconocer_esfuerzo_y_solucionar',
        },
    }

    def analizar(self, texto: str, contexto: dict) -> ResultadoDimension:
        try:
            return self._analizar_interno(texto, contexto)
        except Exception:
            return self._resultado_vacio()

    def _analizar_interno(self, texto: str, contexto: dict) -> ResultadoDimension:
        tl = texto.lower().strip()

        hallazgos = {}
        senales   = []

        subyacentes = self._detectar_subyacente(tl)
        if subyacentes:
            principal = subyacentes[0]
            hallazgos['estado_subyacente']  = principal['estado']
            hallazgos['lectura_intrinseca'] = principal['lectura']
            hallazgos['respuesta_sugerida'] = principal['respuesta_bell']
            senales.append(f'subyacente:{principal["estado"]}')

        energia = self._inferir_energia(tl)
        hallazgos['nivel_energia'] = energia
        if energia in ('bajo', 'muy_bajo'):
            senales.append(f'energia:{energia}')

        modo = self._inferir_modo_mental(tl)
        hallazgos['modo_mental'] = modo
        senales.append(f'modo:{modo}')

        activa    = len(subyacentes) > 0
        confianza = 0.4 + (0.1 * len(subyacentes)) if activa else 0.2
        confianza = min(0.80, confianza)

        return self._resultado(
            activa    = activa,
            confianza = confianza,
            hallazgos = hallazgos,
            senales   = senales,
        )

    def _detectar_subyacente(self, texto: str) -> list:
        detectados = []
        for estado, config in self._PATRONES_SUBYACENTES.items():
            if any(s in texto for s in config['senales']):
                detectados.append({
                    'estado':        estado,
                    'lectura':       config['lectura'],
                    'respuesta_bell': config['respuesta_bell'],
                })
        return detectados

    def _inferir_energia(self, texto: str) -> str:
        bajo = ['cansado', 'agotado', 'no puedo', 'rendido', 'sin ganas',
                'sin energía', 'muerto', 'no tengo fuerzas']
        alto = ['vamos', 'arriba', 'dale', 'emocionado', 'listo',
                'empecemos', 'a full', 'motivado']
        if any(b in texto for b in bajo):
            return 'muy_bajo' if texto.count('no') > 2 else 'bajo'
        if any(a in texto for a in alto):
            return 'alto'
        return 'normal'

    def _inferir_modo_mental(self, texto: str) -> str:
        if '?' in texto and texto.count('?') > 1:
            return 'exploratorio_intenso'
        if '?' in texto:
            return 'exploratorio'
        if any(w in texto for w in ['crea', 'haz', 'construye', 'genera', 'escribe']):
            return 'constructivo'
        if any(w in texto for w in ['arregla', 'corrige', 'repara', 'soluciona']):
            return 'reparador'
        if any(w in texto for w in ['analiza', 'revisa', 'verifica', 'evalúa']):
            return 'analitico'
        return 'receptivo'