# biblioteca/habilidades/lenguaje/dimensiones/psicologica.py
# ================================================
# DIMENSIÓN PSICOLÓGICA
#
# Lee el estado emocional, la necesidad real
# y la intención profunda detrás del mensaje.
#
# CORRECCIÓN: ahora usa los ids_conocidos que
# vienen de GestorVocabulario y la red neuronal.
# Si la red ya identificó EMOCION_FRUSTRADO,
# esta dimensión lo usa directamente en lugar
# de redescubrirlo desde cero.
# ================================================

import re
from .base import DimensionLenguaje, ResultadoDimension


class DimensionPsicologica(DimensionLenguaje):

    NOMBRE = 'psicologica'
    PESO   = 1.3

    _EMOCIONES = {
        'frustracion': {
            'palabras': [
                'frustrado', 'frustrada', 'harto', 'harta', 'cansado de',
                'cansada de', 'hastiado', 'desesperado', 'desesperada',
                'no aguanto', 'no puedo más', 'ya no más', 'esto es un caos',
                'no funciona nada', 'todo está mal', 'para qué', 'que caso tiene',
                'ya no sé', 'me tiene loco', 'me tiene loca',
            ],
            'intensidad': 0.8,
            'necesidad': 'validacion_y_solucion',
            'tono_bell': 'empático_firme',
            'id_lyra':   'EMOCION_FRUSTRADO',
        },
        'cansancio': {
            'palabras': [
                'cansado', 'cansada', 'agotado', 'agotada', 'exhausto', 'exhausta',
                'sin energía', 'sin energia', 'no puedo', 'ya no puedo',
                'me rindo', 'rendido', 'rendida', 'muerto', 'muerta',
                'no doy más', 'estoy frito', 'reventado', 'no tengo fuerzas',
            ],
            'intensidad': 0.75,
            'necesidad': 'apoyo_y_simplificacion',
            'tono_bell': 'tranquilizador_suave',
            'id_lyra':   'EMOCION_CANSADO',
        },
        'ansiedad': {
            'palabras': [
                'ansioso', 'ansiosa', 'nervioso', 'nerviosa', 'preocupado',
                'preocupada', 'angustiado', 'asustado', 'asustada', 'con miedo',
                'no sé si', 'y si falla', 'qué pasa si', 'me da miedo',
                'espero que', 'ojalá', 'estoy tenso', 'estoy tensa',
            ],
            'intensidad': 0.70,
            'necesidad': 'certeza_y_calma',
            'tono_bell': 'tranquilizador_suave',
            'id_lyra':   'EMOCION_ASUSTADO',
        },
        'entusiasmo': {
            'palabras': [
                'emocionado', 'emocionada', 'entusiasmado', 'qué bueno', 'genial',
                'increíble', 'increible', 'excelente', 'me encanta', 'me gusta',
                'buenísimo', 'perfecto', 'fantástico', 'me alegra', 'qué bien',
                'por fin', 'lo logramos', 'funcionó', 'funciono',
            ],
            'intensidad': 0.65,
            'necesidad': 'compartir_y_avanzar',
            'tono_bell': 'celebratorio_cálido',
            'id_lyra':   'EMOCION_FELIZ',
        },
        'confusion': {
            'palabras': [
                'confundido', 'confundida', 'perdido', 'perdida',
                'no entiendo', 'no entendí', 'no se qué', 'no sé qué',
                'no me queda claro', 'qué significa', 'cómo funciona',
                'no sé cómo', 'me explicas', 'no lo capto',
            ],
            'intensidad': 0.55,
            'necesidad': 'clarificacion',
            'tono_bell': 'cercano_natural',
            'id_lyra':   'EMOCION_CONFUNDIDO',
        },
        'determinacion': {
            'palabras': [
                'quiero', 'necesito', 'voy a', 'tengo que', 'hay que', 'debo',
                'es necesario', 'es fundamental', 'es urgente', 'sin falta',
                'obligatorio', 'crucial', 'lo haré', 'vamos a', 'hagamos',
            ],
            'intensidad': 0.60,
            'necesidad': 'ejecucion_eficiente',
            'tono_bell': 'presente_inmediato',
            'id_lyra':   'EMOCION_NEUTRAL',
        },
        'tristeza': {
            'palabras': [
                'triste', 'mal', 'no estoy bien', 'todo mal',
                'todo sale mal', 'nada funciona', 'qué difícil', 'es muy duro',
                'no logro', 'fallé', 'falle', 'fallamos', 'perdí', 'no pude',
            ],
            'intensidad': 0.85,
            'necesidad': 'apoyo_emocional',
            'tono_bell': 'empático_suave',
            'id_lyra':   'EMOCION_TRISTE',
        },
        'impaciencia': {
            'palabras': [
                'rápido', 'rapido', 'apúrate', 'apurate', 'ya', 'ahorita',
                'inmediatamente', 'urgente', 'cuánto falta', 'tarda mucho',
                'por qué tarda', 'ya debería',
            ],
            'intensidad': 0.65,
            'necesidad': 'velocidad_y_eficiencia',
            'tono_bell': 'presente_inmediato',
            'id_lyra':   'EMOCION_FRUSTRADO',
        },
        'gratitud': {
            'palabras': [
                'gracias', 'muchas gracias', 'mil gracias', 'agradecido',
                'agradecida', 'te lo agradezco', 'me ayudaste', 'me salvaste',
                'excelente trabajo', 'bien hecho',
            ],
            'intensidad': 0.50,
            'necesidad': 'reconocimiento_reciproco',
            'tono_bell': 'cálido_genuino',
            'id_lyra':   'GRATITUD',
        },
    }

    _NECESIDADES = {
        'validacion': [
            'está bien', 'es correcto', 'voy bien', 'qué opinas',
            'crees que', 'está bien así', 'es mejor', 'cuál es mejor',
        ],
        'conexion': [
            'cómo estás', 'como estas', 'qué tal', 'que tal',
            'cómo te va', 'buenas', 'hola', 'hey', 'oye',
        ],
        'autonomia': [
            'yo lo hago', 'yo puedo', 'sin ayuda', 'solo quiero',
            'nada más dime', 'solo explícame', 'enséñame',
        ],
        'comprension': [
            'no entiendo', 'explícame', 'cómo funciona', 'por qué', 'para qué',
            'qué significa',
        ],
        'seguridad': [
            'es seguro', 'no va a pasar nada', 'está bien hacer',
            'es posible', 'funciona', 'va a funcionar',
        ],
    }

    _ALTA_CARGA = [
        'no sé por dónde empezar', 'hay demasiado', 'es muy complejo',
        'no entiendo nada', 'todo junto', 'de golpe', 'me abruma',
        'son muchas cosas', 'no sé qué hacer primero',
    ]

    _CONFIANZA_ALTA = [
        'sé que puedes', 'tú puedes', 'confío en ti', 'confio en ti',
        'lo que tú digas', 'hazlo como creas', 'en tus manos', 'te lo dejo a ti',
    ]

    # Mapa de ID de red → emoción interna
    # Si la red ya identificó el nodo, usamos eso directamente
    _ID_RED_A_EMOCION = {
        'EMOCION_FRUSTRADO': 'frustracion',
        'EMOCION_CANSADO':   'cansancio',
        'EMOCION_AGOTADO':   'cansancio',
        'EMOCION_ASUSTADO':  'ansiedad',
        'EMOCION_TRISTE':    'tristeza',
        'EMOCION_FELIZ':     'entusiasmo',
        'EMOCION_CONFUNDIDO':'confusion',
        'EMOCION_ENOJADO':   'frustracion',
        'EMOCION_MAL':       'tristeza',
        'EMOCION_ESTRESADO': 'ansiedad',
        'EMOCION_PREOCUPADO':'ansiedad',
        'GRATITUD':          'gratitud',
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

        # ── PASO 1: Emociones ya identificadas por la red de Bell ──
        # Si GestorVocabulario + Capa 1/2 ya detectaron nodos de emoción,
        # los usamos directamente. Son la fuente más confiable.
        ids_conocidos = contexto.get('ids_conocidos', [])
        emocion_desde_red = self._emocion_desde_red(ids_conocidos)

        if emocion_desde_red:
            config = self._EMOCIONES[emocion_desde_red]
            hallazgos['emocion_detectada']    = emocion_desde_red
            hallazgos['intensidad_emocional'] = config['intensidad']
            hallazgos['necesidad_emocional']  = config['necesidad']
            hallazgos['tono_recomendado']     = config['tono_bell']
            hallazgos['id_lyra']              = config['id_lyra']
            hallazgos['fuente_emocion']       = 'red_neuronal'
            senales.append(f'emocion:{emocion_desde_red}')
            senales.append(f'intensidad:{config["intensidad"]:.1f}')
            senales.append('fuente:red')

        # ── PASO 2: Análisis propio del texto ──
        # Aunque la red ya detectó algo, hacemos análisis propio
        # para encontrar matices, combinar emociones, etc.
        emociones_texto = self._detectar_emociones_texto(tl)

        if emociones_texto and not emocion_desde_red:
            emocion_principal = emociones_texto[0]
            hallazgos['emocion_detectada']    = emocion_principal['emocion']
            hallazgos['intensidad_emocional'] = emocion_principal['intensidad']
            hallazgos['necesidad_emocional']  = emocion_principal['necesidad']
            hallazgos['tono_recomendado']     = emocion_principal['tono_bell']
            hallazgos['id_lyra']              = emocion_principal['id_lyra']
            hallazgos['fuente_emocion']       = 'analisis_texto'
            senales.append(f'emocion:{emocion_principal["emocion"]}')
            senales.append(f'intensidad:{emocion_principal["intensidad"]:.1f}')

        if emociones_texto:
            hallazgos['todas_emociones'] = [e['emocion'] for e in emociones_texto]

        # ── Necesidad profunda ──
        necesidad = self._detectar_necesidad(tl)
        if necesidad:
            hallazgos['necesidad_real'] = necesidad
            senales.append(f'necesidad:{necesidad}')

        # ── Carga cognitiva ──
        if any(c in tl for c in self._ALTA_CARGA):
            hallazgos['alta_carga_cognitiva'] = True
            hallazgos['recomendacion_bell']   = 'simplificar_y_guiar_paso_a_paso'
            senales.append('alta_carga_cognitiva')

        # ── Confianza en Bell ──
        if any(c in tl for c in self._CONFIANZA_ALTA):
            hallazgos['confia_en_bell'] = True
            senales.append('confianza_en_bell_alta')

        # ── Tono ──
        emocion_final = hallazgos.get('emocion_detectada', '')
        tono = self._analizar_tono(tl, emocion_final)
        hallazgos['tono_base'] = tono
        senales.append(f'tono:{tono}')

        activa    = bool(hallazgos.get('emocion_detectada'))
        confianza = 0.4 + (0.1 * len(senales)) if activa else 0.2
        confianza = min(0.95, confianza)

        return self._resultado(
            activa    = activa,
            confianza = confianza,
            hallazgos = hallazgos,
            senales   = senales,
        )

    def _emocion_desde_red(self, ids_conocidos: list) -> str:
        """
        Si la red de Bell ya identificó un nodo de emoción,
        lo mapea a la emoción interna de esta dimensión.
        Prioriza la emoción de mayor intensidad.
        """
        encontradas = []
        for id_nodo in ids_conocidos:
            emocion = self._ID_RED_A_EMOCION.get(id_nodo)
            if emocion:
                config = self._EMOCIONES.get(emocion, {})
                encontradas.append((emocion, config.get('intensidad', 0.5)))

        if not encontradas:
            return ''

        encontradas.sort(key=lambda x: x[1], reverse=True)
        return encontradas[0][0]

    def _detectar_emociones_texto(self, texto: str) -> list:
        detectadas = []
        for nombre, config in self._EMOCIONES.items():
            for palabra in config['palabras']:
                if palabra in texto:
                    detectadas.append({
                        'emocion':    nombre,
                        'intensidad': config['intensidad'],
                        'necesidad':  config['necesidad'],
                        'tono_bell':  config['tono_bell'],
                        'id_lyra':    config['id_lyra'],
                    })
                    break
        detectadas.sort(key=lambda x: x['intensidad'], reverse=True)
        return detectadas

    def _detectar_necesidad(self, texto: str) -> str:
        for necesidad, patrones in self._NECESIDADES.items():
            if any(p in texto for p in patrones):
                return necesidad
        return ''

    def _analizar_tono(self, texto: str, emocion: str) -> str:
        if not emocion:
            if '?' in texto:
                return 'curioso'
            if '!' in texto:
                return 'enfático'
            return 'neutral'
        mapa = {
            'frustracion':   'tenso',
            'cansancio':     'exhausto',
            'ansiedad':      'nervioso',
            'entusiasmo':    'positivo',
            'confusion':     'perdido',
            'determinacion': 'decidido',
            'tristeza':      'bajo',
            'impaciencia':   'urgente',
            'gratitud':      'cálido',
        }
        return mapa.get(emocion, 'neutral')