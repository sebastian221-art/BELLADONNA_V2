# capas/capa3/constructor_comprension.py
# ================================================
# CONSTRUCTOR DE COMPRENSIÓN — v5c
#
# FIX v5c: Evaluador matemático completamente reescrito
# — Sin regex complejas que fallan silenciosamente
# — Reemplazos por palabras antes de extraer expresión
# — eval() simple y seguro con try/except
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
    'mi trabajo', 'jelcon',
    'dónde estudio', 'donde estudio', 'uniminuto',
    'dónde nací', 'donde naci', 'cómo me llamo', 'como me llamo',
    'qué hago yo', 'que hago yo', 'a qué me dedico', 'a que me dedico',
    'quién soy yo', 'quien soy yo', 'sabes quién soy', 'sabes quien soy',
    'me conoces', 'qué sabes de mí', 'que sabes de mi', 'bucaramanga',
]

_KEYWORDS_ARQUITECTURA_FALLIDAS = [
    'cuántas capas', 'cuantas capas', 'cuántas capa', 'cuantas capa',
    'tienes capas', 'qué capas', 'que capas',
    'qué es belladonna', 'que es belladonna',
    'qué es bell core', 'que es bell core', 'bell core es',
    'qué es el grounding', 'que es el grounding',
    'qué es grounding', 'que es grounding',
    'qué es mente pura', 'que es mente pura', 'mente pura',
    'tu arquitectura', 'arquitectura de bell',
    'cómo procesas', 'como procesas',
]

_KEYWORDS_OPERACION = [
    'cuánto es ', 'cuanto es ', 'cuánto da ', 'cuanto da ',
    'cuánto son ', 'cuanto son ', 'cuánto vale ', 'cuanto vale ',
    'calcula ', 'calcúlame ', 'calculame ',
    'raíz de ', 'raiz de ', '% de ', 'porcentaje de ',
]

_KEYWORDS_ACCION_BELL = [
    'qué haces', 'que haces',
    'qué estás haciendo', 'que estas haciendo',
    'qué estás pensando', 'que estas pensando',
    'en qué piensas ahora', 'en que piensas ahora',
]


class ConstructorComprension:

    def construir(self, red_activa, texto_original, contexto, tono):
        primarios   = red_activa.get('nodos_primarios',   [])
        secundarios = red_activa.get('nodos_secundarios', [])
        terciarios  = red_activa.get('nodos_terciarios',  [])
        todos       = primarios + secundarios + terciarios

        ids_activos   = {n.get('nodo_id', '') for n in todos}
        ids_primarios = {n.get('nodo_id', '') for n in primarios}

        resultado_motor = self._usar_motor_lenguaje(
            texto_original, ids_activos, ids_primarios, contexto
        )

        if resultado_motor:
            return self._comprension_desde_motor(
                resultado_motor, primarios, texto_original
            )

        return {
            'literal':    self._comprension_literal(primarios, texto_original),
            'contextual': self._comprension_contextual(
                ids_activos, ids_primarios, contexto, texto_original
            ),
            'profunda':   self._comprension_profunda(
                ids_activos, ids_primarios, contexto, tono, texto_original
            ),
        }

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
        texto_lower = texto.lower().strip()
        for kw in _KEYWORDS_OPERACION:
            if kw in texto_lower:
                return 'operacion_matematica'
        for kw in _KEYWORDS_SEBASTIAN:
            if kw in texto_lower:
                return 'pregunta_sebastian'
        for kw in _KEYWORDS_ARQUITECTURA_FALLIDAS:
            if kw in texto_lower:
                return 'pregunta_arquitectura_bell'
        for kw in _KEYWORDS_ACCION_BELL:
            if kw in texto_lower:
                return 'pregunta_accion_bell'
        return tipo_actual

    def _evaluar_matematica(self, texto: str) -> Optional[str]:
        """
        Evaluador matemático robusto.
        Reemplaza palabras por operadores, extrae la expresión
        y evalúa con Python. Sin regex complejas que fallen.
        """
        try:
            t = texto.lower().strip()

            # Paso 1: quitar frases de pregunta
            frases_pregunta = [
                'cuánto es', 'cuanto es', 'cuánto da', 'cuanto da',
                'cuánto son', 'cuanto son', 'cuánto vale', 'cuanto vale',
                'calcula', 'calcúlame', 'calculame', 'dime cuánto',
                'dime cuanto', 'resuelve',
            ]
            for frase in frases_pregunta:
                t = t.replace(frase, ' ')

            # Paso 2: palabras → operadores
            t = t.replace('más', '+').replace(' mas ', '+').replace('mas', '+')
            t = t.replace(' menos ', '-').replace('menos', '-')
            t = t.replace('multiplicado por', '*').replace(' por ', '*')
            t = t.replace('dividido entre', '/').replace('dividido por', '/')
            t = t.replace(' entre ', '/').replace('entre', '/')
            t = t.replace('elevado al cuadrado', '**2')
            t = t.replace('al cuadrado', '**2')
            t = t.replace('elevado a ', '**')

            # Paso 3: limpiar caracteres no numéricos al inicio/fin
            t = t.strip()
            # Quitar letras sueltas del inicio
            t = re.sub(r'^[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ\s]+', '', t).strip()
            # Quitar letras sueltas del final
            t = re.sub(r'[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ\s\?\.]+$', '', t).strip()

            if not t:
                return None

            # Paso 4: verificar que tiene al menos un dígito
            if not any(c.isdigit() for c in t):
                return None

            # Paso 5: verificar que solo tiene caracteres matemáticos válidos
            t_test = t.replace(' ', '')
            for c in t_test:
                if c not in '0123456789+-*/().^**':
                    # Si hay letras u otros chars raros, no evaluar
                    return None

            # Paso 6: eval seguro
            resultado = eval(t, {"__builtins__": {}})

            # Paso 7: formatear resultado
            if isinstance(resultado, bool):
                return None  # True/False no son resultados matemáticos válidos
            if isinstance(resultado, float) and resultado.is_integer():
                return str(int(resultado))
            elif isinstance(resultado, float):
                return str(round(resultado, 4))
            elif isinstance(resultado, int):
                return str(resultado)
            return None

        except Exception:
            return None

    # ── Fallback ──────────────────────────────────────────

    def _comprension_literal(self, primarios, texto):
        if not primarios:
            return {'nodos_directos': [], 'certeza': 0.0,
                    'tiene_contenido': False, 'texto_limpio': texto}
        nodos   = [{'nodo_id': n.get('nodo_id', ''), 'energia': n.get('energia', 0)}
                   for n in primarios]
        certeza = sum(n['energia'] for n in primarios) / len(primarios)
        return {'nodos_directos': nodos, 'certeza': min(1.0, certeza),
                'tiene_contenido': True, 'texto_limpio': texto}

    def _comprension_contextual(self, ids_activos, ids_primarios, contexto, texto):
        tipo_mensaje = self._determinar_tipo_mensaje(ids_activos, ids_primarios, texto)
        resultado_math = None
        if tipo_mensaje == 'operacion_matematica':
            resultado_math = self._evaluar_matematica(texto)
        hay_historial  = bool(contexto.get('conversacion', {}).get('historial_reciente'))
        nombre_usuario = contexto.get('sebastian', {}).get('nombre', 'Sebastian')
        return {
            'tipo_mensaje':          tipo_mensaje,
            'hay_historial':         hay_historial,
            'nombre_usuario':        nombre_usuario,
            'ids_activos':           list(ids_activos),
            'certeza':               0.75 if hay_historial else 0.60,
            'resultado_matematico':  resultado_math,
        }

    def _comprension_profunda(self, ids_activos, ids_primarios, contexto, tono, texto):
        tipo      = self._determinar_tipo_mensaje(ids_activos, ids_primarios, texto)
        intencion = self._intencion_desde_tipo(tipo)
        necesidad = self._necesidad_desde_intencion(intencion)
        emocion   = self._detectar_emocion(ids_activos)
        info_9d   = self._obtener_info_grounding(ids_primarios, contexto)
        certeza   = info_9d.get('confianza_promedio', 0.70) if intencion != 'desconocida' else 0.30
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
        }

    def _determinar_tipo_mensaje(self, ids, ids_primarios, texto):
        texto_lower = texto.lower().strip()
        for kw in _KEYWORDS_OPERACION:
            if kw in texto_lower: return 'operacion_matematica'
        for kw in _KEYWORDS_SEBASTIAN:
            if kw in texto_lower: return 'pregunta_sebastian'
        for kw in _KEYWORDS_ARQUITECTURA_FALLIDAS:
            if kw in texto_lower: return 'pregunta_arquitectura_bell'
        for kw in _KEYWORDS_ACCION_BELL:
            if kw in texto_lower: return 'pregunta_accion_bell'

        saludos = {'SALUDO_HOLA','SALUDO_BUENAS','SALUDO_HEY','SALUDO_QUE_TAL',
                   'SALUDO_QUE_MAS','SALUDO_BUENOS_DIAS','SALUDO_TARDES','SALUDO_NOCHES'}
        if ids_primarios & saludos: return 'saludo'
        if 'DESPEDIDA' in ids_primarios: return 'despedida'
        if 'GRATITUD' in ids_primarios: return 'gratitud'

        presentacion = {'PRESENTACION_NOMBRE', 'VERBO_SER_YO'}
        if (ids_primarios & presentacion and
                ('sebastian' in texto_lower or 'me llamo' in texto_lower)):
            return 'presentacion_sebastian'

        if 'PREG_QUIEN' in ids_primarios and 'VERBO_SER_TU' in ids_primarios:
            return 'pregunta_identidad_bell'
        if ('PREG_QUIEN' in ids_primarios and 'VERBO_SER_EL' in ids_primarios
                and 'NEURONA_SEBASTIAN' in ids_primarios):
            return 'pregunta'
        if 'PREG_QUIEN' in ids_primarios and 'VERBO_SER_EL' in ids_primarios:
            return 'pregunta_identidad_otro'
        if 'PREG_COMO' in ids_primarios and 'VERBO_ESTAR_TU' in ids_primarios:
            return 'pregunta_estado_bell'
        if 'PREG_COMO' in ids_primarios and 'REF_TE' in ids_primarios:
            return 'pregunta_nombre_bell'

        capacidad = {'VERBO_HACER_TU','VERBO_PODER_TU','VERBO_PODER_EL','VERBO_HACER'}
        if ids_primarios & capacidad and ('PREG_QUE' in ids_primarios or 'PREG_CUAL' in ids_primarios):
            return 'pregunta_capacidad_bell'
        if 'PREG_QUE' in ids_primarios and 'VERBO_SER_TU' in ids_primarios:
            return 'pregunta_identidad_bell'
        if 'VERBO_CREAR_YO' in ids_primarios and 'NEURONA_SEBASTIAN' in ids:
            return 'pregunta'
        if 'VERBO_CREAR_YO' in ids_primarios and 'REF_TE' in ids_primarios:
            return 'pregunta'

        ayuda = {'VERBO_AYUDAR_ME','VERBO_AYUDA','VERBO_AYUDAR'}
        if ids_primarios & ayuda: return 'solicitud_ayuda'

        negativas = {'EMOCION_MAL','EMOCION_TRISTE','EMOCION_FRUSTRADO','EMOCION_CANSADO',
                     'EMOCION_AGOTADO','EMOCION_ESTRESADO','EMOCION_PREOCUPADO',
                     'EMOCION_ASUSTADO','EMOCION_ENOJADO'}
        if ids_primarios & negativas: return 'expresion_emocional_negativa'

        positivas = {'EMOCION_BIEN','EMOCION_GENIAL','EMOCION_FELIZ',
                     'EMOCION_CONTENTO','EMOCION_ALEGRE','EMOCION_MOTIVADO'}
        if ids_primarios & positivas: return 'expresion_emocional_positiva'

        confirmaciones = {'AFIRMACION','AFIRMACION_FUERTE','EXPR_OK',
                          'EXPR_DALE','EXPR_LISTO','EXPR_ENTENDIDO'}
        if ids_primarios & confirmaciones: return 'confirmacion'
        if {'NEGACION','NEGACION_FUERTE'} & ids_primarios: return 'negacion'

        preguntas = {'PREG_QUE','PREG_QUIEN','PREG_COMO','PREG_CUANDO',
                     'PREG_DONDE','PREG_POR_QUE','PREG_CUANTO','PREG_CUAL'}
        if ids_primarios & preguntas: return 'pregunta'

        if (texto_lower.endswith('?') or texto_lower.startswith((
            'qué','que','quién','quien','cómo','como','cuándo','cuando',
            'dónde','donde','por qué','por que','cuánto','cuanto','cuál','cual',
        ))): return 'pregunta'

        return 'conversacional'

    def _intencion_desde_tipo(self, tipo):
        mapa = {
            'saludo': 'saludar', 'despedida': 'despedirse', 'gratitud': 'agradecer',
            'pregunta_identidad_bell': 'conocer_bell',
            'pregunta_estado_bell': 'saber_estado_bell',
            'pregunta_nombre_bell': 'saber_nombre_bell',
            'pregunta_capacidad_bell': 'saber_capacidades_bell',
            'pregunta_arquitectura_bell': 'conocer_arquitectura_bell',
            'pregunta_accion_bell': 'saber_accion_bell',
            'pregunta_sebastian': 'preguntar_sobre_sebastian',
            'operacion_matematica': 'calcular',
            'presentacion_sebastian': 'presentarse',
            'pregunta': 'preguntar', 'solicitud_ayuda': 'pedir_ayuda',
            'expresion_emocional_positiva': 'expresar_emocion_positiva',
            'expresion_emocional_negativa': 'expresar_emocion_negativa',
            'confirmacion': 'confirmar', 'negacion': 'negar',
            'conversacional': 'conversar',
        }
        return mapa.get(tipo, 'desconocida')

    def _necesidad_desde_intencion(self, intencion):
        mapa = {
            'saludar': 'conexion_social', 'despedirse': 'cierre_conversacion',
            'agradecer': 'expresar_gratitud',
            'conocer_bell': 'conocimiento_bell', 'saber_estado_bell': 'conocimiento_bell',
            'saber_nombre_bell': 'conocimiento_bell', 'saber_capacidades_bell': 'conocimiento_bell',
            'conocer_arquitectura_bell': 'conocimiento_bell', 'saber_accion_bell': 'conocimiento_bell',
            'preguntar_sobre_sebastian': 'conocimiento_sebastian',
            'calcular': 'ayuda_practica', 'presentarse': 'ser_reconocido',
            'preguntar': 'informacion', 'pedir_ayuda': 'ayuda_practica',
            'expresar_emocion_positiva': 'compartir_alegria',
            'expresar_emocion_negativa': 'apoyo_emocional',
            'confirmar': 'acuerdo', 'negar': 'desacuerdo', 'conversar': 'conexion_social',
        }
        return mapa.get(intencion, 'desconocida')

    def _detectar_emocion(self, ids):
        if 'GRATITUD' in ids: return 'gratitud'
        negativos = {'EMOCION_TRISTE','EMOCION_MAL','EMOCION_FRUSTRADO','EMOCION_CANSADO',
                     'EMOCION_AGOTADO','EMOCION_ESTRESADO','EMOCION_PREOCUPADO',
                     'EMOCION_ASUSTADO','EMOCION_ENOJADO'}
        positivos = {'EMOCION_FELIZ','EMOCION_GENIAL','EMOCION_ALEGRE',
                     'EMOCION_BIEN','EMOCION_EMOCIONADO','EMOCION_MOTIVADO'}
        if ids & negativos: return 'negativa'
        if ids & positivos: return 'positiva'
        return 'neutra'

    def _obtener_info_grounding(self, ids_primarios, contexto):
        try:
            from biblioteca.grounding.calculador import CalculadorGrounding
            calc       = CalculadorGrounding.obtener()
            groundings = []
            for nodo_id in ids_primarios:
                tipo = self._tipo_desde_id(nodo_id)
                g9d  = calc.calcular(nodo_id, tipo, contexto)
                groundings.append(g9d)
            if not groundings:
                return {}
            g_prom = sum(g.efectivo() for g in groundings) / len(groundings)
            c_prom = sum(g.confianza for g in groundings) / len(groundings)
            puede  = all(g.puede_ejecutar() for g in groundings)
            niveles   = [g.nivel_comprension() for g in groundings]
            nivel_dom = max(set(niveles), key=niveles.count)
            dims = {}
            for g in groundings:
                for dim, val in g.resumen()['dimensiones'].items():
                    if isinstance(val, float):
                        dims[dim] = dims.get(dim, 0) + val
            dims_top = sorted(
                [(d, round(v/len(groundings), 3)) for d, v in dims.items()],
                key=lambda x: x[1], reverse=True
            )[:5]
            return {
                'grounding_promedio': round(g_prom, 3), 'confianza_promedio': round(c_prom, 3),
                'puede_ejecutar': puede, 'nivel_comprension': nivel_dom,
                'dimensiones_dominantes': [d[0] for d in dims_top],
            }
        except Exception:
            return {'grounding_promedio': 0.5, 'confianza_promedio': 0.7,
                    'puede_ejecutar': False, 'nivel_comprension': 'parcial',
                    'dimensiones_dominantes': []}

    def _tipo_desde_id(self, nodo_id):
        if any(s in nodo_id for s in ['SALUDO','DESPEDIDA']): return 'saludo'
        if 'GRATITUD' in nodo_id: return 'gratitud'
        if 'EMOCION_' in nodo_id:
            neg = ['TRISTE','MAL','FRUSTRADO','CANSADO','AGOTADO',
                   'ESTRESADO','PREOCUPADO','ASUSTADO','ENOJADO']
            return 'emocion_negativa' if any(n in nodo_id for n in neg) else 'emocion_positiva'
        if 'PREG_' in nodo_id: return 'pregunta'
        if any(s in nodo_id for s in ['VERBO_ESTAR','VERBO_SER']): return 'verbo_estado'
        if 'VERBO_' in nodo_id: return 'verbo_accion'
        if 'BELL_' in nodo_id: return 'pregunta_sobre_bell'
        return 'concepto'