# capas/capa3/constructor_comprension.py
# ================================================
# CONSTRUCTOR DE COMPRENSIÓN — v6
#
# v6: Recibe clasificacion_groq como hint opcional.
# Si Groq clasificó el mensaje, construye la
# comprensión a partir de esa clasificación
# en vez de usar patrones/motor.
#
# Prioridad:
#   1. clasificacion_groq (hint semántico)
#   2. MotorComprension / spaCy
#   3. Keyword patterns (fallback siempre)
# ================================================

import re
from typing import Optional

_IDS_SIEMPRE_ACTIVOS = {
    'BELL_NOMBRE_BELL', 'BELL_NOMBRE_BELLADONNA',
    'BELL_NOMBRE_COMPLETO', 'BELL_NOMBRE_CORTO',
    'BELL_CONSCIENCIA', 'BELL_CORE',
}

_KEYWORDS_SEBASTIAN = [
    'cuántos años tengo', 'cuantos años tengo', 'años tengo', 'mi edad',
    'dónde vivo', 'donde vivo', 'en qué ciudad vivo', 'en que ciudad vivo',
    'dónde trabajo', 'donde trabajo', 'en qué trabajo', 'en que trabajo',
    'mi trabajo', 'jelcon', 'dónde estudio', 'donde estudio', 'uniminuto',
    'dónde nací', 'donde naci', 'cómo me llamo', 'como me llamo',
    'qué hago yo', 'que hago yo', 'a qué me dedico', 'a que me dedico',
    'quién soy yo', 'quien soy yo', 'sabes quién soy', 'sabes quien soy',
    'me conoces', 'qué sabes de mí', 'que sabes de mi', 'bucaramanga',
]
_KEYWORDS_ARQUITECTURA = [
    'cuántas capas', 'cuantas capas', 'tienes capas', 'qué capas', 'que capas',
    'qué es belladonna', 'que es belladonna', 'qué es bell core', 'que es bell core',
    'qué es el grounding', 'que es el grounding', 'qué es grounding', 'que es grounding',
    'qué es mente pura', 'que es mente pura', 'mente pura',
    'tu arquitectura', 'arquitectura de bell', 'cómo procesas', 'como procesas',
    'zona de desconocimiento', 'zona desconocimiento',
]
_KEYWORDS_ACCION_BELL = [
    'qué haces', 'que haces', 'qué estás haciendo', 'que estas haciendo',
    'qué estás pensando', 'que estas pensando', 'en qué piensas ahora',
]
_KEYWORDS_COTIDIANO = [
    'logré', 'logre', 'arreglé', 'arregle', 'ya funciona', 'por fin funciona',
    'funcionó', 'lo resolví', 'lo arreglé', 'terminé', 'lo terminé', 'acabé',
    'hace frío', 'hace frio', 'hace calor', 'ya dormí', 'ya dormi',
    'dormí bien', 'dormi bien', 'dormí mal', 'no dormí', 'no dormi',
    'voy a comer', 'voy a dormir', 'ya llegué', 'ya llegue', 'ya comí', 'ya comi',
    'tengo hambre', 'tengo sueño', 'es tarde', 'ya es tarde',
]
_KEYWORDS_PYTHON_DEBUG = [
    'tengo este error', 'me sale este error', 'me da este error', 'por qué falla',
    'por qué no funciona', 'no corre', 'no arranca', 'cómo debugueo',
    'recursionerror', 'typeerror', 'attributeerror', 'keyerror', 'valueerror',
    'nameerror', 'indexerror', 'importerror', 'syntaxerror', 'indentationerror',
]
_KEYWORDS_PYTHON_ANALISIS = [
    'analiza este código', 'analiza el código', 'analiza mi código',
    'revisa este código', 'qué hace este código', 'tiene errores', 'tiene bugs',
    'code review', 'analiza esta clase', 'analiza esta función',
]
_KEYWORDS_PYTHON_GENERACION = [
    'crea una función', 'crea un script', 'escribe el código', 'hazme el código',
    'hazme una función', 'genera el código', 'necesito un script',
    'crea una clase', 'hazme un endpoint', 'hazme un', 'escríbeme',
]
_KEYWORDS_PYTHON_EXPLICACION = [
    'cómo hago un bucle', 'qué es async', 'cómo funciona async',
    'qué son los generadores', 'qué es yield', 'qué es lambda',
    'qué es un decorador', 'generators', 'generator', 'context manager',
    'metaclass', 'asyncio', 'coroutine', 'threading', 'dataclass',
]
_KEYWORDS_OPERACION = [
    'cuánto es ', 'cuanto es ', 'cuánto da ', 'cuanto da ',
    'calcula ', 'calcúlame ', 'calculame ', 'raíz de ', 'raiz de ',
]


class ConstructorComprension:

    def construir(
        self,
        red_activa,
        texto_original,
        contexto,
        tono,
        clasificacion_groq=None,
    ):
        primarios   = red_activa.get('nodos_primarios',   [])
        secundarios = red_activa.get('nodos_secundarios', [])
        terciarios  = red_activa.get('nodos_terciarios',  [])
        todos       = primarios + secundarios + terciarios

        ids_activos   = {n.get('nodo_id', '') for n in todos}
        ids_primarios = {n.get('nodo_id', '') for n in primarios}

        # ── PRIORIDAD 1: clasificación de Groq ────────────
        if clasificacion_groq:
            return self._comprension_desde_groq(
                clasificacion_groq, primarios, texto_original, contexto
            )

        # ── PRIORIDAD 2: motor de lenguaje (spaCy) ────────
        resultado_motor = self._usar_motor_lenguaje(
            texto_original, ids_activos, ids_primarios, contexto
        )
        if resultado_motor:
            return self._comprension_desde_motor(resultado_motor, primarios, texto_original)

        # ── PRIORIDAD 3: keyword patterns (siempre) ───────
        return {
            'literal':    self._comprension_literal(primarios, texto_original),
            'contextual': self._comprension_contextual(
                ids_activos, ids_primarios, contexto, texto_original
            ),
            'profunda':   self._comprension_profunda(
                ids_activos, ids_primarios, contexto, tono, texto_original
            ),
        }

    # ── Comprensión desde Groq ─────────────────────────────

    def _comprension_desde_groq(
        self, groq: dict, primarios: list, texto_original: str, contexto: dict
    ) -> dict:
        """
        Construye comprensión usando la clasificación de Groq.
        Groq provee tipo, emocion, intencion, necesidad.
        Enriched con datos de la red neuronal.
        """
        certeza = groq.get('certeza', 0.90)

        nodos = [
            {'nodo_id': n.get('nodo_id', ''), 'energia': n.get('energia', 0)}
            for n in primarios
        ]

        tipo = groq.get('tipo_mensaje', 'conversacional')
        resultado_math = None
        if tipo == 'operacion_matematica':
            resultado_math = self._evaluar_matematica(texto_original)

        literal = {
            'nodos_directos':  nodos,
            'certeza':         certeza,
            'tiene_contenido': bool(texto_original.strip()),
            'texto_limpio':    texto_original,
            'accion':          None,
            'objetos':         [],
        }

        contextual = {
            'tipo_mensaje':         tipo,
            'fuente_clasificacion': 'groq',
            'certeza_groq':         certeza,
            'hay_historial':        bool(contexto.get('conversacion', {}).get('historial_reciente')),
            'nombre_usuario':       contexto.get('sebastian', {}).get('nombre', 'Sebastian'),
            'ids_activos':          [n.get('nodo_id', '') for n in primarios],
            'certeza':              certeza,
            'es_continuacion':      False,
            'es_correccion':        False,
            'resultado_matematico': resultado_math,
        }

        profunda = {
            'intencion_detectada':    groq.get('intencion', 'desconocida'),
            'necesidad_real':         groq.get('necesidad', 'desconocida'),
            'emocion_detectada':      groq.get('emocion', 'neutra'),
            'tono_base':              'neutral',
            'certeza':                certeza,
            'puede_ejecutar':         tipo in ('solicitud_tecnica', 'operacion_matematica'),
            'nivel_comprension':      'profunda' if certeza > 0.8 else 'media',
            'grounding_promedio':     certeza,
            'dimensiones_dominantes': [],
            'estado_subyacente':      groq.get('estado_subyacente', 'neutro'),
            'modo_mental':            groq.get('modo_mental', 'social'),
            'habilidad_requerida':    self._habilidad_desde_tipo(tipo),
            'dominio_tecnico':        'python' if tipo == 'solicitud_tecnica' else None,
        }

        return {'literal': literal, 'contextual': contextual, 'profunda': profunda}

    def _habilidad_desde_tipo(self, tipo: str) -> str | None:
        mapa = {
            'solicitud_tecnica':       'PYTHON',
            'operacion_matematica':    'MATEMATICA',
            'pregunta_arquitectura_bell': 'AUTO_ANALISIS',
            'pregunta_accion_bell':    'AUTO_ANALISIS',
        }
        return mapa.get(tipo)

    # ── Comprensión desde MotorComprension (spaCy) ─────────

    def _usar_motor_lenguaje(self, texto, ids_activos, ids_primarios, contexto):
        try:
            from biblioteca.habilidades.lenguaje.motor import MotorComprension
            from capas.capa6.buffer_sesion import BufferSesion

            vocab_context = contexto.get('vocab_match', [])
            if not vocab_context:
                try:
                    from biblioteca.vocabulario.gestor_vocabulario import GestorVocabulario
                    vocab_context = GestorVocabulario.obtener().buscar_frase(texto)
                except Exception:
                    vocab_context = []

            ids_vocab = [
                m['concepto'].get('id', '')
                for m in vocab_context
                if m.get('concepto', {}).get('id')
                and m['concepto']['id'] not in _IDS_SIEMPRE_ACTIVOS
            ]
            vocab_tipos = {
                m['concepto'].get('id', ''): m['concepto'].get('tipo', '')
                for m in vocab_context
                if m.get('concepto', {}).get('id')
            }
            ids_activos_limpios = ids_activos - _IDS_SIEMPRE_ACTIVOS
            todos_ids = list(ids_activos_limpios | set(ids_vocab))

            historial = []
            try:
                buffer = BufferSesion.obtener()
                historial = [
                    {'respuesta_bell': r}
                    for r in buffer.obtener_ultimas_respuestas_bell(4)
                ]
            except Exception:
                pass

            nombre = contexto.get('sebastian', {}).get('nombre', 'Sebastian')
            ctx_motor = {
                'nombre_usuario': nombre,
                'historial':      historial,
                'vocab_match':    vocab_context,
                'ids_activos':    todos_ids,
                'ids_conocidos':  todos_ids,
                'vocab_tipos':    vocab_tipos,
                'conceptos_red':  [],
            }
            return MotorComprension.obtener().comprender(texto, ctx_motor)
        except Exception:
            return None

    def _comprension_desde_motor(self, motor, primarios, texto_original):
        certeza_lit = motor.confianza_global if motor.confianza_global > 0 else 0.7
        certeza_ctx = min(0.95, certeza_lit + 0.05)
        certeza_pro = min(0.95, certeza_lit + 0.03)

        literal = {
            'nodos_directos':  [
                {'nodo_id': n.get('nodo_id', ''), 'energia': n.get('energia', 0)}
                for n in primarios
            ],
            'certeza':         certeza_lit,
            'tiene_contenido': bool(texto_original),
            'texto_limpio':    texto_original,
            'accion':          motor.accion_principal,
            'objetos':         motor.objetos,
        }

        tipo_motor = motor.tipo_mensaje
        tipo_final = self._override_tipo_conservador(texto_original, tipo_motor)
        resultado_math = None
        if tipo_final == 'operacion_matematica':
            resultado_math = self._evaluar_matematica(texto_original)

        contextual = {
            'tipo_mensaje':          tipo_final,
            'fuente_clasificacion':  'motor',
            'tipo_motor_original':   tipo_motor,
            'hay_historial':         motor.es_continuacion,
            'nombre_usuario':        motor.nombre_usuario,
            'ids_activos':           motor.ids_activos,
            'certeza':               certeza_ctx,
            'es_continuacion':       motor.es_continuacion,
            'es_correccion':         motor.es_correccion,
            'resultado_matematico':  resultado_math,
        }

        profunda = {
            'intencion_detectada':    self._intencion_desde_tipo(tipo_final),
            'necesidad_real':         self._necesidad_desde_intencion(
                self._intencion_desde_tipo(tipo_final)
            ),
            'emocion_detectada':      motor.emocion_detectada,
            'tono_base':              motor.tono_base,
            'certeza':                certeza_pro,
            'puede_ejecutar':         bool(motor.habilidad_requerida),
            'nivel_comprension':      'profunda' if motor.confianza_global > 0.7 else 'parcial',
            'grounding_promedio':     motor.confianza_global,
            'dimensiones_dominantes': motor.dimensiones_activas,
            'habilidad_requerida':    motor.habilidad_requerida,
            'dominio_tecnico':        motor.dominio_tecnico,
            'estado_subyacente':      motor.estado_subyacente,
            'modo_mental':            motor.modo_mental,
            'nivel_energia':          motor.nivel_energia,
        }

        return {'literal': literal, 'contextual': contextual, 'profunda': profunda}

    def _override_tipo_conservador(self, texto: str, tipo_actual: str) -> str:
        t = texto.lower().strip()
        _SALUDOS = ['buenos días','buenos dias','buenas noches','buenas tardes',
                    'buen día','buen dia','buenas bell','hola bell','hola belladonna']
        if any(s in t for s in _SALUDOS) or tipo_actual == 'saludo':
            return 'saludo'
        _LOGROS = ['logré','logre ','arreglé','arregle ','ya funciona',
                   'por fin funciona','funcionó','funciono','lo resolví',
                   'lo arreglé','terminé','lo terminé','acabé','salió']
        if any(s in t for s in _LOGROS):
            return tipo_actual if tipo_actual in ('logro_compartido','expresion_emocional_positiva') else 'logro_compartido'
        for kw in _KEYWORDS_COTIDIANO:
            if kw in t: return 'conversacional'
        for kw in _KEYWORDS_PYTHON_DEBUG:
            if kw in t: return 'solicitud_tecnica'
        for kw in _KEYWORDS_PYTHON_ANALISIS:
            if kw in t: return 'solicitud_tecnica'
        for kw in _KEYWORDS_PYTHON_GENERACION:
            if kw in t: return 'solicitud_tecnica'
        for kw in _KEYWORDS_PYTHON_EXPLICACION:
            if kw in t: return 'solicitud_tecnica'
        for kw in _KEYWORDS_OPERACION:
            if kw in t: return 'operacion_matematica'
        for kw in _KEYWORDS_SEBASTIAN:
            if kw in t: return 'pregunta_sebastian'
        for kw in _KEYWORDS_ARQUITECTURA:
            if kw in t: return 'pregunta_arquitectura_bell'
        for kw in _KEYWORDS_ACCION_BELL:
            if kw in t: return 'pregunta_accion_bell'
        return tipo_actual

    # ── Comprensión por patrones (fallback puro) ───────────

    def _comprension_literal(self, primarios, texto):
        if not primarios:
            return {'nodos_directos': [], 'certeza': 0.0,
                    'tiene_contenido': bool(texto.strip()), 'texto_limpio': texto}
        nodos   = [{'nodo_id': n.get('nodo_id',''), 'energia': n.get('energia',0)} for n in primarios]
        certeza = sum(n['energia'] for n in primarios) / len(primarios)
        return {'nodos_directos': nodos, 'certeza': min(1.0, certeza),
                'tiene_contenido': True, 'texto_limpio': texto,
                'fuente_clasificacion': 'patrones'}

    def _comprension_contextual(self, ids_activos, ids_primarios, contexto, texto):
        tipo = self._determinar_tipo_mensaje(ids_activos, ids_primarios, texto)
        resultado_math = self._evaluar_matematica(texto) if tipo == 'operacion_matematica' else None
        return {
            'tipo_mensaje':          tipo,
            'fuente_clasificacion':  'patrones',
            'hay_historial':         bool(contexto.get('conversacion',{}).get('historial_reciente')),
            'nombre_usuario':        contexto.get('sebastian',{}).get('nombre','Sebastian'),
            'ids_activos':           list(ids_activos),
            'certeza':               0.60,
            'resultado_matematico':  resultado_math,
        }

    def _comprension_profunda(self, ids_activos, ids_primarios, contexto, tono, texto):
        tipo      = self._determinar_tipo_mensaje(ids_activos, ids_primarios, texto)
        intencion = self._intencion_desde_tipo(tipo)
        necesidad = self._necesidad_desde_intencion(intencion)
        emocion   = self._detectar_emocion(ids_activos)
        info_9d   = self._obtener_info_grounding(ids_primarios, contexto)
        certeza   = info_9d.get('confianza_promedio', 0.60) if intencion != 'desconocida' else 0.30
        return {
            'intencion_detectada':    intencion,
            'necesidad_real':         necesidad,
            'emocion_detectada':      emocion,
            'tono_base':              tono,
            'certeza':                certeza,
            'puede_ejecutar':         info_9d.get('puede_ejecutar', False),
            'nivel_comprension':      info_9d.get('nivel_comprension', 'parcial'),
            'grounding_promedio':     info_9d.get('grounding_promedio', 0.5),
            'dimensiones_dominantes': info_9d.get('dimensiones_dominantes', []),
            'fuente_clasificacion':   'patrones',
        }

    def _determinar_tipo_mensaje(self, ids, ids_primarios, texto):
        t = texto.lower().strip()
        for kw in _KEYWORDS_OPERACION:
            if kw in t: return 'operacion_matematica'
        for kw in _KEYWORDS_SEBASTIAN:
            if kw in t: return 'pregunta_sebastian'
        for kw in _KEYWORDS_ARQUITECTURA:
            if kw in t: return 'pregunta_arquitectura_bell'
        for kw in _KEYWORDS_ACCION_BELL:
            if kw in t: return 'pregunta_accion_bell'

        saludos = {'SALUDO_HOLA','SALUDO_BUENAS','SALUDO_HEY','SALUDO_QUE_TAL',
                   'SALUDO_QUE_MAS','SALUDO_BUENOS_DIAS','SALUDO_TARDES','SALUDO_NOCHES'}
        if ids_primarios & saludos: return 'saludo'
        if any('DESPEDIDA' in i for i in ids_primarios): return 'despedida'
        if any('GRATITUD' in i for i in ids_primarios): return 'gratitud'

        if 'PREG_QUIEN' in ids_primarios and 'VERBO_SER_TU' in ids_primarios:
            return 'pregunta_identidad_bell'
        if 'PREG_COMO' in ids_primarios and 'VERBO_ESTAR_TU' in ids_primarios:
            return 'pregunta_estado_bell'

        neg = {'EMOCION_MAL','EMOCION_TRISTE','EMOCION_FRUSTRADO','EMOCION_CANSADO',
               'EMOCION_AGOTADO','EMOCION_ESTRESADO','EMOCION_PREOCUPADO'}
        pos = {'EMOCION_BIEN','EMOCION_GENIAL','EMOCION_FELIZ','EMOCION_CONTENTO',
               'EMOCION_ALEGRE','EMOCION_MOTIVADO'}
        if ids_primarios & neg: return 'expresion_emocional_negativa'
        if ids_primarios & pos: return 'expresion_emocional_positiva'

        confirma = {'AFIRMACION','EXPR_OK','EXPR_DALE','EXPR_LISTO'}
        if ids_primarios & confirma: return 'confirmacion'
        if {'NEGACION','NEGACION_FUERTE'} & ids_primarios: return 'negacion'

        preguntas = {'PREG_QUE','PREG_QUIEN','PREG_COMO','PREG_CUANDO',
                     'PREG_DONDE','PREG_POR_QUE','PREG_CUANTO','PREG_CUAL'}
        if ids_primarios & preguntas: return 'pregunta'

        ayuda = {'VERBO_AYUDAR_ME','VERBO_AYUDA','VERBO_AYUDAR'}
        if ids_primarios & ayuda: return 'solicitud_ayuda'

        if t.endswith('?') or t.startswith(('qué','que','quién','quien','cómo',
            'como','cuándo','cuando','dónde','donde','por qué','por que')):
            return 'pregunta'
        return 'conversacional'

    def _evaluar_matematica(self, texto: str) -> Optional[str]:
        try:
            t = texto.lower().strip()
            for frase in ['cuánto es','cuanto es','cuánto da','cuanto da',
                          'cuánto son','cuanto son','calcula','calcúlame',
                          'calculame','dime cuánto','dime cuanto','resuelve']:
                t = t.replace(frase, ' ')
            t = (t.replace('más','+').replace(' mas ','+').replace('mas','+')
                  .replace(' menos ','-').replace('menos','-')
                  .replace('multiplicado por','*').replace(' por ','*')
                  .replace('dividido entre','/').replace('dividido por','/')
                  .replace(' entre ','/').replace('al cuadrado','**2')
                  .replace('elevado a ','**'))
            t = re.sub(r'^[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ\s]+', '', t).strip()
            t = re.sub(r'[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ\s\?\.]+$', '', t).strip()
            if not t or not any(c.isdigit() for c in t):
                return None
            for c in t.replace(' ',''):
                if c not in '0123456789+-*/().':
                    return None
            resultado = eval(t, {"__builtins__": {}})
            if isinstance(resultado, bool): return None
            if isinstance(resultado, float):
                return str(int(resultado)) if resultado.is_integer() else str(round(resultado, 4))
            return str(resultado)
        except Exception:
            return None

    def _intencion_desde_tipo(self, tipo):
        return {
            'saludo':'saludar','despedida':'despedirse','gratitud':'agradecer',
            'pregunta_identidad_bell':'conocer_bell','pregunta_estado_bell':'saber_estado_bell',
            'pregunta_nombre_bell':'saber_nombre_bell','pregunta_capacidad_bell':'saber_capacidades_bell',
            'pregunta_arquitectura_bell':'conocer_arquitectura_bell',
            'pregunta_accion_bell':'saber_accion_bell','pregunta_sebastian':'preguntar_sobre_sebastian',
            'operacion_matematica':'calcular','presentacion_sebastian':'presentarse',
            'pregunta':'preguntar','solicitud_ayuda':'pedir_ayuda',
            'expresion_emocional_positiva':'expresar_emocion_positiva',
            'expresion_emocional_negativa':'expresar_emocion_negativa',
            'logro_compartido':'compartir_logro',
            'confirmacion':'confirmar','negacion':'negar','conversacional':'conversar',
            'solicitud_tecnica':'pedir_ayuda',
        }.get(tipo, 'desconocida')

    def _necesidad_desde_intencion(self, intencion):
        return {
            'saludar':'conexion_social','despedirse':'cierre_conversacion',
            'agradecer':'expresar_gratitud','conocer_bell':'conocimiento_bell',
            'saber_estado_bell':'conocimiento_bell','saber_nombre_bell':'conocimiento_bell',
            'saber_capacidades_bell':'conocimiento_bell','conocer_arquitectura_bell':'conocimiento_bell',
            'saber_accion_bell':'conocimiento_bell','preguntar_sobre_sebastian':'conocimiento_sebastian',
            'calcular':'ayuda_practica','presentarse':'ser_reconocido',
            'preguntar':'informacion','pedir_ayuda':'ayuda_practica',
            'expresar_emocion_positiva':'compartir_alegria',
            'expresar_emocion_negativa':'apoyo_emocional',
            'compartir_logro':'compartir_alegria',
            'confirmar':'acuerdo','negar':'desacuerdo','conversar':'conexion_social',
        }.get(intencion, 'desconocida')

    def _detectar_emocion(self, ids):
        if any('GRATITUD' in i for i in ids): return 'gratitud'
        neg = {'EMOCION_TRISTE','EMOCION_MAL','EMOCION_FRUSTRADO','EMOCION_CANSADO',
               'EMOCION_AGOTADO','EMOCION_ESTRESADO','EMOCION_PREOCUPADO'}
        pos = {'EMOCION_FELIZ','EMOCION_GENIAL','EMOCION_ALEGRE',
               'EMOCION_BIEN','EMOCION_EMOCIONADO','EMOCION_MOTIVADO'}
        if ids & neg: return 'negativa'
        if ids & pos: return 'positiva'
        return 'neutra'

    def _obtener_info_grounding(self, ids_primarios, contexto):
        try:
            from biblioteca.grounding.calculador import CalculadorGrounding
            calc = CalculadorGrounding.obtener()
            groundings = []
            for nodo_id in ids_primarios:
                tipo = self._tipo_desde_id(nodo_id)
                groundings.append(calc.calcular(nodo_id, tipo, contexto))
            if not groundings:
                return {}
            g_prom = sum(g.efectivo() for g in groundings) / len(groundings)
            c_prom = sum(g.confianza  for g in groundings) / len(groundings)
            niveles = [g.nivel_comprension() for g in groundings]
            nivel_dom = max(set(niveles), key=niveles.count)
            dims = {}
            for g in groundings:
                for dim, val in g.resumen()['dimensiones'].items():
                    if isinstance(val, float):
                        dims[dim] = dims.get(dim, 0) + val
            dims_top = sorted(
                [(d, round(v/len(groundings),3)) for d, v in dims.items()],
                key=lambda x: x[1], reverse=True
            )[:5]
            return {
                'grounding_promedio': round(g_prom, 3),
                'confianza_promedio': round(c_prom, 3),
                'puede_ejecutar':     all(g.puede_ejecutar() for g in groundings),
                'nivel_comprension':  nivel_dom,
                'dimensiones_dominantes': [d[0] for d in dims_top],
            }
        except Exception:
            return {'grounding_promedio':0.5,'confianza_promedio':0.7,
                    'puede_ejecutar':False,'nivel_comprension':'parcial',
                    'dimensiones_dominantes':[]}

    def _tipo_desde_id(self, nodo_id):
        if any(s in nodo_id for s in ['SALUDO','DESPEDIDA']): return 'saludo'
        if 'GRATITUD' in nodo_id: return 'gratitud'
        if 'EMOCION_' in nodo_id:
            return 'emocion_negativa' if any(
                n in nodo_id for n in ['TRISTE','MAL','FRUSTRADO','CANSADO','ESTRESADO']
            ) else 'emocion_positiva'
        if 'PREG_' in nodo_id: return 'pregunta'
        if 'BELL_' in nodo_id: return 'pregunta_sobre_bell'
        return 'concepto'