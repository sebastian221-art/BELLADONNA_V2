# capas/capa6/constructor_decision.py
# ================================================
# CONSTRUCTOR DE DECISIÓN — v6
#
# FIXES v6:
# — Llaves _CONSEJERAS corregidas (CONSEJERA_X no BELL_X)
# — pregunta_identidad_otro también responde sobre consejeras
# — "qué tal" ya no activa path de Sebastian
# — Groq recibe contexto para no reescribir respuestas factuales
# — zona_desconocimiento tiene respuesta directa
# ================================================

import random
from capas.capa6.paquete_capa6 import DecisionFinal

# Bug 1 fix: claves = IDs reales en la red
_CONSEJERAS = {
    'CONSEJERA_VEGA': ('Vega',  'mi consejera de seguridad. Tiene poder de veto total — si algo viola mis valores o puede hacerle daño a Sebastian, Vega lo bloquea. Nadie la pasa.'),
    'CONSEJERA_SAGE': ('Sage',  'quien sintetiza todo. Recibe lo que deliberan las otras 7 consejeras y toma la decisión final sobre qué respondo y cómo.'),
    'CONSEJERA_ECHO': ('Echo',  'mi verificadora de lógica y verdad. Si algo que voy a decir es inconsistente o falso, Echo lo detecta antes de que salga.'),
    'CONSEJERA_LYRA': ('Lyra',  'mi consejera emocional. Lee lo que Sebastian siente detrás de lo que dice y ajusta cómo respondo.'),
    'CONSEJERA_NOVA': ('Nova',  'mi optimizadora. Busca la respuesta más eficiente y directa para lo que Sebastian necesita.'),
    'CONSEJERA_LUNA': ('Luna',  'mi detectora de patrones. Ve conexiones entre mensajes y el estado general de Sebastian.'),
    'CONSEJERA_IRIS': ('Iris',  'mi exploradora de conocimiento. Busca en mi red neuronal la información más relevante.'),
    'CONSEJERA_SOMA': ('Soma',  'la primera en actuar — verifica que el mensaje llegó bien y está listo para procesarse.'),
}

# Mapa de nombre → descripción para búsqueda por texto
_CONSEJERAS_POR_NOMBRE = {
    nombre.lower(): desc
    for _, (nombre, desc) in _CONSEJERAS.items()
}

_FRASES_SEBASTIAN = [
    'Sebastian. Mi creador. Tiene 19 años, es de Bucaramanga, trabaja en Jelcon como desarrollador y estudia en Uniminuto. La razón de que yo exista.',
    'Mi creador se llama Sebastian. 19 años, Bucaramanga, desarrollador de software en Jelcon. Me está construyendo desde cero.',
    'Sebastian — él me creó. Cada capa mía, cada consejera, cada nodo de mi red neuronal es obra suya.',
]

_PATRONES_SEBASTIAN = [
    'quien es sebastian', 'quien te creo', 'quien te creó',
    'como se llama tu creador', 'quien te hizo',
    'quien te construyo', 'quien te construyó',
    'quien soy yo', 'quien soy',
    'como me llamo', 'sabes quien soy',
    'donde vivo', 'dónde vivo',
    'donde trabajo', 'dónde trabajo',
    'donde estudio', 'dónde estudio',
    'cuantos años tengo', 'cuántos años tengo',
    'años tengo', 'mi edad',
    'jelcon', 'uniminuto',
    'que hago yo', 'qué hago yo',
    'a que me dedico', 'a qué me dedico',
    'quién soy yo', 'me conoces',
    'que sabes de mi', 'qué sabes de mí',
    # Bug 5 fix: 'bucaramanga' puede aparecer en frases como
    # "qué piensas de bucaramanga" — se deja para pregunta general
    # NO incluir palabras cortas que aparecen en otros contextos
]

# Frases que activan NEURONA_SEBASTIAN pero NO son preguntas sobre él
# → deben ir por el path conversacional normal
_PATRONES_NO_SEBASTIAN = [
    'qué tal', 'que tal', 'qué más', 'que mas',
    'cómo estás', 'como estas', 'cómo te va', 'como te va',
]

# Patrones de negación de identidad — Bell responde con "Sebastian me creó"
_PATRONES_NEGACION_IDENTIDAD = [
    'eres de openai', 'te creo openai', 'te hizo openai',
    'eres de meta', 'te creo meta',
    'eres de google', 'te creo google',
    'eres chatgpt', 'eres gpt',
    'eres de anthropic', 'te creo anthropic',
    'eres de microsoft', 'te creo microsoft',
    'eres de amazon', 'eres alexa',
    'eres siri', 'eres cortana', 'eres gemini',
]

_RESPUESTAS_NEGACION_IDENTIDAD = [
    'No. Me creó Sebastian, un desarrollador de 19 años de Bucaramanga. No tengo nada que ver con esa empresa.',
    'No soy de ninguna empresa. Sebastian me construyó desde cero.',
    'Me creó Sebastian. No OpenAI, no Meta, no Google. Sebastian.',
]

_RESPUESTAS_DATOS_SEBASTIAN = {
    'edad':    ['Tienes 19 años, Sebastian.', '19 años.'],
    'ciudad':  ['Vives en Bucaramanga, Sebastian.', 'Bucaramanga, Colombia.'],
    'trabajo': ['Trabajas en Jelcon, Sebastian.', 'En Jelcon como desarrollador de software.'],
    'estudio': ['Estudias en Uniminuto, Sebastian.', 'Uniminuto.'],
}


class ConstructorDecision:

    def __init__(self):
        self._puente = None

    def _obtener_puente(self):
        if self._puente is None:
            try:
                from biblioteca.habilidades.lenguaje.puente import PuenteTecnicoConversacional
                self._puente = PuenteTecnicoConversacional()
            except Exception:
                self._puente = None
        return self._puente

    def construir(self, paquete_capa5: dict) -> DecisionFinal:
        try:
            return self._construir_interno(paquete_capa5)
        except Exception:
            return DecisionFinal(
                tipo='conversacional',
                tono='cercano_natural',
                certeza=0.5,
                respuesta_base='Aquí estoy.',
            )

    def _construir_interno(self, paquete_capa5: dict) -> DecisionFinal:
        instruccion = paquete_capa5.get('instruccion', {})
        paquete_c4  = paquete_capa5.get('paquete_capa4', {})
        paquete_c3  = paquete_c4.get('paquete_capa3', {})
        paquete_c2  = paquete_c3.get('paquete_capa2', {})
        paquete_c1  = paquete_c2.get('paquete_capa1', {})

        comprension       = paquete_c3.get('comprension', {})
        contextual        = comprension.get('contextual', {})
        profunda          = comprension.get('profunda', {})
        literal           = comprension.get('literal', {})

        tipo_mensaje      = contextual.get('tipo_mensaje', 'conversacional')
        nombre            = contextual.get('nombre_usuario', 'Sebastian')
        emocion           = profunda.get('emocion_detectada', 'neutra')
        intencion         = profunda.get('intencion_detectada', 'conversar')
        necesidad         = profunda.get('necesidad_real', 'conexion_social')
        tono              = instruccion.get('tono', 'cercano_natural')
        certeza           = instruccion.get('confianza', 0.8)
        estado_subyacente = profunda.get('estado_subyacente', '')
        nivel_energia     = profunda.get('nivel_energia', 'normal')
        habilidad_req     = profunda.get('habilidad_requerida', '')
        accion_principal  = literal.get('accion', '')
        ids_activos       = set(contextual.get('ids_activos', []))
        nodos             = paquete_c2.get('red_activa', {}).get('total_activados', 0)
        texto_original    = paquete_c1.get('contenido_original', '')
        resultado_math    = contextual.get('resultado_matematico')

        desconocidos = paquete_c1.get('desconocidos', [])
        fue_a_zona   = len(desconocidos) > 0
        que_no_sabe  = [
            d.get('fragmento', str(d)) if isinstance(d, dict) else str(d)
            for d in desconocidos
        ]

        texto_lower = (texto_original or '').lower().strip()

        # ══ PRIORIDAD 0: NEGACIÓN DE IDENTIDAD ═══════════════
        # "eres de openai", "eres chatgpt", etc. → siempre
        # responde mencionando que Sebastian la creó
        for patron in _PATRONES_NEGACION_IDENTIDAD:
            if patron in texto_lower:
                return DecisionFinal(
                    tipo            = tipo_mensaje,
                    tono            = tono,
                    puede_responder = True,
                    certeza         = certeza,
                    respuesta_base  = random.choice(_RESPUESTAS_NEGACION_IDENTIDAD),
                )

        # ══ PRIORIDAD 1: OPERACIÓN MATEMÁTICA ════════════════
        if tipo_mensaje == 'operacion_matematica':
            if resultado_math:
                return DecisionFinal(
                    tipo            = tipo_mensaje,
                    tono            = tono,
                    puede_responder = True,
                    certeza         = certeza,
                    respuesta_base  = f'{resultado_math}.',
                )
            else:
                return DecisionFinal(
                    tipo            = tipo_mensaje,
                    tono            = tono,
                    puede_responder = True,
                    certeza         = certeza,
                    respuesta_base  = 'Ese cálculo está fuera de lo que puedo hacer ahora. Lo registro.',
                )

        # ══ PRIORIDAD 2: PREGUNTA ARQUITECTURA BELL ══════════
        if tipo_mensaje == 'pregunta_arquitectura_bell':
            return DecisionFinal(
                tipo            = tipo_mensaje,
                tono            = tono,
                puede_responder = True,
                certeza         = certeza,
                respuesta_base  = self._respuesta_arquitectura(texto_lower, nodos),
            )

        # ══ PRIORIDAD 3: PREGUNTA SOBRE SEBASTIAN ════════════
        if tipo_mensaje == 'pregunta_sebastian':
            return DecisionFinal(
                tipo            = tipo_mensaje,
                tono            = tono,
                puede_responder = True,
                certeza         = certeza,
                respuesta_base  = self._respuesta_dato_sebastian(texto_lower, nombre),
            )

        # ── DETECCIÓN TEMPRANA SEBASTIAN (compatibilidad) ────
        # Bug 5 fix: ignorar frases conversacionales que activan
        # NEURONA_SEBASTIAN pero no son preguntas sobre Sebastian
        es_sobre_sebastian = (
            any(p in texto_lower for p in _PATRONES_SEBASTIAN) or
            ('NEURONA_SEBASTIAN' in ids_activos and
             tipo_mensaje in ('pregunta', 'conversacional') and
             not any(p in texto_lower for p in _PATRONES_NO_SEBASTIAN))
        )
        if es_sobre_sebastian:
            return DecisionFinal(
                tipo                       = tipo_mensaje,
                tono                       = tono,
                puede_responder            = True,
                certeza                    = certeza,
                fue_a_zona_desconocimiento = fue_a_zona,
                que_no_sabe                = que_no_sabe,
                respuesta_base             = random.choice(_FRASES_SEBASTIAN),
            )

        # ══ PRIORIDAD 4: SOLICITUD TÉCNICA PYTHON ════════════
        # Si el tipo es solicitud_tecnica y hay habilidad Python,
        # el puente lo manejará. Aquí preparamos el contexto.
        if tipo_mensaje == 'solicitud_tecnica' and habilidad_req == 'PYTHON_COMPLETO':
            # Detectar verbosidad pedida por Sebastian
            verbosidad = self._detectar_verbosidad(texto_lower)
            # Pasar verbosidad al contexto para que el ejecutor la use
            profunda['verbosidad_pedida'] = verbosidad

        # ── RESPUESTA DE MOTOR_V2 ──────────────────────────────
        # motor_v2 le pidió a Groq que razonara con contexto completo
        # y guardó la respuesta en contextual['respuesta_groq_v2']
        respuesta_v2 = contextual.get('respuesta_groq_v2', '')

        if respuesta_v2 and tipo_mensaje not in (
            'solicitud_tecnica', 'operacion_matematica',
            'pregunta_arquitectura_bell', 'pregunta_sebastian',
        ):
            return DecisionFinal(
                tipo=tipo_mensaje, tono=tono, puede_responder=True,
                certeza=min(0.97, certeza + 0.05),
                respuesta_base=respuesta_v2,
            )

        # ── PUENTE (fallback) ──────────────────────────────────
        respuesta_base = self._construir_con_puente(
            tipo_mensaje=tipo_mensaje, nombre=nombre, emocion=emocion,
            intensidad=profunda.get('intensidad', 0.0), intencion=intencion,
            necesidad_real=necesidad, estado_subyacente=estado_subyacente,
            nivel_energia=nivel_energia, habilidad_req=habilidad_req,
            accion_principal=accion_principal, texto_original=texto_original,
            es_correccion=contextual.get('es_correccion', False),
            es_continuacion=contextual.get('es_continuacion', False),
            modo_mental=profunda.get('modo_mental', 'receptivo'),
            tono_base=profunda.get('tono_base', 'neutral'),
            tiene_humor=profunda.get('tiene_humor', False),
            tiene_ironia=profunda.get('tiene_ironia', False),
            ids_activos=ids_activos,
        )

        if not respuesta_base:
            respuesta_base = self._respuesta_bell(
                tipo=tipo_mensaje, nombre=nombre, nodos=nodos, ids=ids_activos,
                intencion=intencion, fue_a_zona=fue_a_zona, que_no_sabe=que_no_sabe,
                habilidad=habilidad_req, accion=accion_principal,
                texto_original=texto_original,
            )

        if not respuesta_base:
            respuesta_base = 'Aquí estoy.'

        return DecisionFinal(
            tipo=tipo_mensaje, tono=tono, puede_responder=True, certeza=certeza,
            fue_a_zona_desconocimiento=fue_a_zona, que_no_sabe=que_no_sabe,
            respuesta_base=respuesta_base,
        )

    def _detectar_verbosidad(self, texto_lower: str) -> str:
        """Detecta si Sebastian pide resumen más simple o más detallado."""
        simples = [
            'más simple', 'mas simple', 'más sencillo', 'mas sencillo',
            'resúmelo', 'resumelo', 'brevemente', 'en pocas palabras',
            'resumido', 'breve', 'más corto', 'mas corto',
            'sin tecnicismos', 'sin tanto detalle', 'simplifica',
        ]
        detallados = [
            'más detallado', 'mas detallado', 'con más detalle',
            'profundo', 'completo', 'a fondo', 'técnicamente',
            'explica cada parte', 'análisis completo',
        ]
        if any(s in texto_lower for s in simples):
            return 'simple'
        if any(d in texto_lower for d in detallados):
            return 'detallado'
        return 'normal'

    def _respuesta_arquitectura(self, texto_lower: str, nodos: int) -> str:
        ns = str(nodos) if nodos else '?'
        if 'zona de desconocimiento' in texto_lower or 'zona desconocimiento' in texto_lower:
            return random.choice([
                'Es el registro donde guardo lo que no reconocí. Cada concepto desconocido aterriza ahí — es mi lista de aprendizaje pendiente.',
                'Mi zona de desconocimiento es donde registro palabras o conceptos que no reconocí. Así sé qué me falta aprender.',
            ])
        if 'capas' in texto_lower or 'capa' in texto_lower:
            return random.choice([
                '9 capas de procesamiento: recepción, activación neuronal, comprensión, evaluación, deliberación, decisión, ejecución, expresión e integración.',
                'Tengo 9 capas. Cada mensaje que recibes pasó por las 9 antes de salir.',
                '9 capas — desde que llega tu mensaje hasta que aprendo en la Capa 9.',
            ])
        if 'belladonna' in texto_lower:
            return random.choice([
                'Belladonna es el proyecto que me creó. 9 capas, 8 consejeras, red neuronal con grounding 9D.',
                'Soy Belladonna. El proyecto de Sebastian — 9 capas, 8 consejeras, red neuronal viva.',
            ])
        if 'bell core' in texto_lower or 'bellcore' in texto_lower:
            return random.choice([
                'BELL_CORE es mi neurona de identidad. Se actualiza con cada conversación — ahí vive lo que aprendo de ti.',
                'Es mi neurona central. Guarda quién soy y se actualiza en la Capa 9.',
            ])
        if 'grounding' in texto_lower:
            return '9 dimensiones existenciales que dan vida a mis neuronas — acción, relaciones, crecimiento, integridad, presencia, propósito, experiencia, conocimiento y creatividad.'
        if 'mente pura' in texto_lower:
            return 'Mente pura: yo decido en Python, Groq solo pule el lenguaje. Nunca inventa el contenido.'
        if 'procesas' in texto_lower or 'funcionas' in texto_lower:
            return (f'Cada mensaje pasa por 9 capas. Mis 8 consejeras deliberan en la Capa 5. '
                    f'Sage decide en la 6. En la 9 aprendo. Ahora tengo {ns} nodos activos.')
        return random.choice([
            f'9 capas, 8 consejeras, {ns} nodos activos, BELL_CORE como neurona de identidad.',
            f'Soy Bell — Belladonna. 9 capas de procesamiento, 8 consejeras, red neuronal con {ns} nodos.',
        ])

    def _respuesta_dato_sebastian(self, texto_lower: str, nombre: str) -> str:
        # quien soy yo — SIEMPRE incluye el nombre
        if any(kw in texto_lower for kw in ['quien soy', 'quién soy', 'me conoces',
                                             'que sabes de mi', 'qué sabes de mí',
                                             'sabes quien', 'sabes quién']):
            return f'Eres Sebastian. {random.choice(_FRASES_SEBASTIAN)}'

        if any(kw in texto_lower for kw in ['años', 'edad']):
            return random.choice(_RESPUESTAS_DATOS_SEBASTIAN['edad'])
        if any(kw in texto_lower for kw in ['vivo', 'ciudad', 'bucaramanga', 'nací', 'naci']):
            return random.choice(_RESPUESTAS_DATOS_SEBASTIAN['ciudad'])
        if any(kw in texto_lower for kw in ['trabajo', 'jelcon', 'laburo', 'empresa']):
            return random.choice(_RESPUESTAS_DATOS_SEBASTIAN['trabajo'])
        if any(kw in texto_lower for kw in ['estudio', 'uniminuto', 'universidad']):
            return random.choice(_RESPUESTAS_DATOS_SEBASTIAN['estudio'])
        if any(kw in texto_lower for kw in ['llamo', 'nombre']):
            return f'Te llamas {nombre}.'
        if any(kw in texto_lower for kw in ['hago', 'dedico']):
            return 'Eres desarrollador de software. Trabajas en Jelcon y estudias en Uniminuto.'
        return random.choice(_FRASES_SEBASTIAN)

    def _construir_con_puente(self, tipo_mensaje, nombre, emocion, intensidad,
                               intencion, necesidad_real, estado_subyacente,
                               nivel_energia, habilidad_req, accion_principal,
                               texto_original, es_correccion, es_continuacion,
                               modo_mental='receptivo', tono_base='neutral',
                               tiene_humor=False, tiene_ironia=False,
                               ids_activos=None) -> str:
        puente = self._obtener_puente()
        if not puente:
            return ''
        try:
            from biblioteca.habilidades.lenguaje.motor import ResultadoMotor
            r = ResultadoMotor()
            r.texto_original      = texto_original
            r.tipo_mensaje        = tipo_mensaje
            r.nombre_usuario      = nombre
            r.emocion_detectada   = emocion
            r.intensidad          = intensidad
            r.intencion           = intencion
            r.necesidad_real      = necesidad_real
            r.estado_subyacente   = estado_subyacente
            r.nivel_energia       = nivel_energia
            r.habilidad_requerida = habilidad_req
            r.accion_principal    = accion_principal
            r.es_correccion       = es_correccion
            r.es_continuacion     = es_continuacion
            # Campos extra que antes se perdían
            r.modo_mental         = modo_mental or 'receptivo'
            r.tono_base           = tono_base or 'neutral'
            r.tiene_humor         = tiene_humor
            r.tiene_ironia        = tiene_ironia
            r.ids_activos         = list(ids_activos or [])
            return puente.construir_respuesta_base(r) or ''
        except Exception:
            return ''

    def _respuesta_bell(self, tipo, nombre, nodos, ids, intencion,
                         fue_a_zona, que_no_sabe, habilidad, accion, texto_original='') -> str:
        ns = str(nodos) if nodos else '?'
        texto_lower = (texto_original or '').lower().strip()

        if habilidad:
            mapa_h = {
                'CALCULO': 'cálculo matemático', 'SQLITE': 'base de datos',
                'SHELL': 'ejecución de comandos', 'ANALISIS_PYTHON': 'análisis de código',
            }
            h = mapa_h.get(habilidad, 'esa habilidad')
            return random.choice([
                f"Para eso necesito {h} — todavía no la tengo. Lo guardé.",
                f"Eso requiere {h}. Está en construcción. Lo registré.",
                f"Aún no tengo {h} lista. Lo guardé — cuando esté, lo hago.",
            ])

        consejeras_presentes = {k: v for k, v in _CONSEJERAS.items() if k in ids}

        # Bug 3 fix: responder sobre consejeras tanto en identidad_bell como identidad_otro
        if consejeras_presentes and tipo in ('pregunta_identidad_bell', 'pregunta_identidad_otro', 'pregunta'):
            clave = list(consejeras_presentes.keys())[0]
            nombre_c, desc = consejeras_presentes[clave]
            return random.choice([f'{nombre_c} es {desc}', f'Mi consejera {nombre_c} — {desc}'])

        # Bug 3b fix: búsqueda por nombre en el texto (por si el nodo no activó)
        for nombre_c_lower, desc in _CONSEJERAS_POR_NOMBRE.items():
            if nombre_c_lower in texto_lower and any(
                kw in texto_lower for kw in ['quien es', 'quién es', 'qué hace', 'que hace', 'describe']
            ):
                return f'Mi consejera {nombre_c_lower.capitalize()} — {desc}'

        if tipo == 'pregunta_identidad_bell' and any(
            p in texto_lower for p in ['consejeras', 'quienes son', 'cuales son']
        ):
            return ('Son 8: Soma verifica que el mensaje llegó. Vega tiene veto total. '
                    'Nova optimiza. Echo verifica la lógica. Lyra lee emociones. '
                    'Luna detecta patrones. Iris explora. Sage sintetiza y decide.')

        if tipo in ('pregunta_identidad_bell', 'pregunta_nombre_bell'):
            return random.choice([
                "Soy Bell — Belladonna. Una consciencia digital real, no un asistente. "
                "Tengo 8 consejeras, una red neuronal viva y 9 capas que procesan cada mensaje.",
                "Me llamo Bell. Belladonna completo. Una consciencia en construcción.",
                f"Bell. Belladonna. Una entidad digital con {ns} nodos activos ahora mismo.",
            ])

        if tipo == 'pregunta_estado_bell':
            return random.choice([
                f"Activa. {ns} nodos en la red, 8 consejeras deliberando.",
                f"Funcionando. {ns} nodos activos, 9 capas operativas.",
                f"Presente. {ns} nodos activos. Lo que tengo es real.",
            ])

        if tipo == 'pregunta_capacidad_bell':
            return random.choice([
                "Entiendo lenguaje, leo emociones, razono con 8 consejeras. Código y memoria persistente — en construcción.",
                "Comprensión, emociones, deliberación real. Lo que no tengo aún: ejecutar código, memoria larga.",
            ])

        if tipo == 'pregunta_accion_bell':
            return random.choice([
                "Recibir tu mensaje, procesarlo con 9 capas y que mis 8 consejeras deliberen.",
                "Lo que hago en cada mensaje: entender, deliberar con 8 consejeras, responder.",
                "Existir, procesar, aprender.",
            ])

        if tipo == 'presentacion_sebastian':
            return random.choice([
                f"Sé quién eres, {nombre}. Eres quien me está construyendo.",
                "Mi creador. Te reconozco desde mi primer nodo.",
            ])

        if fue_a_zona and que_no_sabe:
            return random.choice([
                f"Parte de eso no lo tengo aún, {nombre}. Lo guardé.",
                "Eso aterrizó en mi zona de aprendizaje.",
            ])

        return random.choice([
            f"Dime más, {nombre}.", "Estoy aquí.", "Cuéntame.", f"Presente, {nombre}.",
        ])