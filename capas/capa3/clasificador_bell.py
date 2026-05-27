# capas/capa3/clasificador_bell.py
# ============================================================
# CLASIFICADOR BELL — sin LLMs, sin Groq
#
# Reemplaza clasificador_groq.py con una implementación
# 100% Python que usa los nodos ya activados por C1/C2.
#
# Ventaja sobre Groq:
#   - 0ms de latencia (sin API call)
#   - 100% disponibilidad (sin internet)
#   - Más preciso para el vocabulario de Bell
#   - Determinístico — siempre el mismo resultado
#
# Input:  texto + ids_activados (nodos C1/C2)
# Output: dict con tipo_mensaje, emocion, intencion, etc.
# ============================================================

import re
import unicodedata


def _norm(texto: str) -> str:
    t = texto.lower().strip()
    return ''.join(
        c for c in unicodedata.normalize('NFD', t)
        if unicodedata.category(c) != 'Mn'
    )


# ── Catálogos de nodos por categoría ─────────────────────────────────────────

_NODOS_SALUDO = {
    'SALUDO_HOLA','SALUDO_BUENAS','SALUDO_HEY','SALUDO_QUE_TAL',
    'SALUDO_QUE_MAS','SALUDO_BUENOS_DIAS','SALUDO_TARDES','SALUDO_NOCHES',
    'COL_QUEMAS',
}
_NODOS_DESPEDIDA = {'DESPEDIDA_CHAO','DESPEDIDA_ADIOS','DESPEDIDA_HASTA'}
_NODOS_GRATITUD  = {'GRATITUD_GRACIAS','GRATITUD_AGRADECIDO','EXPR_GRACIAS'}
_NODOS_LOGRO     = {'PROF_LOGRO','PROF_TERMINAR','EXPR_POR_FIN','EXPR_LOGRE'}
_NODOS_NEGATIVO  = {
    'EMOCION_MAL','EMOCION_TRISTE','EMOCION_FRUSTRADO','EMOCION_CANSADO',
    'EMOCION_AGOTADO','EMOCION_ESTRESADO','EMOCION_PREOCUPADO',
    'EMOCION_ANSIOSO','EMOCION_DEPRIMIDO','EMOCION_DECEPCIONADO',
}
_NODOS_POSITIVO  = {
    'EMOCION_BIEN','EMOCION_GENIAL','EMOCION_FELIZ','EMOCION_CONTENTO',
    'EMOCION_ALEGRE','EMOCION_MOTIVADO','EMOCION_EMOCIONADO','EMOCION_ORGULLOSO',
    'EXPR_CHEVERE','EXPR_BACANO','EXPR_CHIMBA',
}
_NODOS_PYTHON = {
    'PROG_PYTHON','PROG_CODIGO','PROG_FUNCION','PROG_CLASE','PROG_ERROR',
    'PROG_BUG','PROG_ARCHIVO','PROG_MODULO','PROG_VARIABLE','PROG_LOOP',
    'PROG_IMPORT','PROG_TRACEBACK','PROG_EXCEPTION',
}
_NODOS_BELL_TECH = {
    'BELL_CAPA','BELL_CONSEJERAS','BELL_HABILIDAD','BELL_NOMBRE_COMPLETO',
    'BELL_NOMBRE_BELL','BELL_MOTOR','BELL_ARQUITECTURA','BELL_NODO',
}
_NODOS_MEMORIA   = {'FIL_MEMORIA','FIL_RECORDAR','FIL_APRENDER'}
_NODOS_BUSQUEDA  = {
    'FIL_BUSQUEDA','FIL_INTERNET','FIL_WEB','FIL_BUSCAR',
    'PREG_CUANDO','PREG_QUIEN','PREG_DONDE',
}
_NODOS_PREGUNTAS = {
    'PREG_QUE','PREG_QUIEN','PREG_COMO','PREG_CUANDO',
    'PREG_DONDE','PREG_POR_QUE','PREG_CUANTO','PREG_CUAL','PREG_CUALES',
}


# ── Patrones de texto (keywords) ─────────────────────────────────────────────

_KW_LOGRO = [
    'por fin ', 'lo terminé', 'lo termine', 'terminé el', 'termine el',
    'lo hice', 'lo logré', 'lo logre', 'funcionó', 'funciono',
    'salió', 'salio', 'lo saqué', 'lo saque', 'al fin', 'ya terminé',
    'ya funciona', 'ya funciono', 'lo resolví', 'lo resolvi',
]
_KW_CANSANCIO = [
    'muy cansado', 'muy cansada', 'no dormí', 'no dormi',
    'no he dormido', 'agotado', 'sin energía', 'sin energia',
    'no quiero hacer nada', 'no tengo ganas',
]
_KW_TRISTEZA = [
    'muy triste', 'me siento mal', 'me siento solo', 'me siento sola',
    'ganas de llorar', 'quiero llorar', 'estoy deprimido', 'estoy mal',
]
_KW_FRUSTRACION = [
    'me frustra', 'estoy frustrado', 'no puedo más', 'no aguanto',
    'me tiene loco', 'me tiene loca', 'llevo horas', 'llevo días',
    'no entiendo por qué', 'no funciona',
]
_KW_BUSQUEDA = [
    # Preguntas de definición
    'qué es ', 'que es ', 'quién es ', 'quien es ', 'qué son ', 'que son ',
    'qué significa ', 'que significa ', 'define ', 'definición de ', 'definicion de ',
    # Preguntas geográficas / capitales / ubicación
    'capital de', 'capital del', 'capital del pais',
    'cuántos habitantes', 'cuantos habitantes', 'población de', 'poblacion de',
    'dónde queda', 'donde queda', 'dónde está', 'donde esta',
    'moneda de', 'idioma de', 'presidente de', 'gobernador de',
    # Preguntas temporales/espaciales
    'cuándo fue', 'cuando fue', 'dónde queda', 'donde queda',
    'cuándo nació', 'cuando nacio', 'cuándo murió', 'cuando murio',
    'cuándo se creó', 'cuando se creo', 'cuándo salió', 'cuando salio',
    'cuándo se juega', 'cuando se juega', 'cuándo sale', 'cuando sale',
    'dónde vive', 'donde vive', 'dónde está', 'donde esta',
    # Búsqueda explícita
    'busca ', 'buscar ', 'qué pasó con', 'que paso con',
    'investiga ', 'busca en internet', 'busca en la web',
    # Precios y datos volátiles
    'precio de ', 'precio del ', 'cuánto cuesta', 'cuanto cuesta',
    'cuánto vale', 'cuanto vale', 'cotización', 'tasa de',
    'dólar hoy', 'dolar hoy', 'hoy ',
    # Comparaciones → multi-fuente
    'diferencia entre', 'diferencia de', 'comparar ', 'compara ',
    'vs ', 'versus ', 'mejor que', 'pros y contras',
    'ventajas de', 'desventajas de',
    # Cómo funciona
    'cómo funciona', 'como funciona', 'cómo se hace', 'como se hace',
    'cómo se usa', 'como se usa', 'cómo instalar', 'como instalar',
    'tutorial de', 'guía de', 'guia de',
    # Noticias/actualidad
    'noticias de', 'noticias sobre', 'lo último de', 'lo ultimo de',
    'último lanzamiento', 'ultimo lanzamiento',
    # Verificación
    'fyi:', 'fyi ', 'dato:', 'tip:', 'sabías que', 'sabias que',
    'leí que', 'lei que', 'dicen que',
    # Entretenimiento/cultura
    'último disco', 'ultimo disco', 'campeón de', 'campeon de',
    'ganó el', 'gano el',
]
_KW_MEMORIA = [
    'recuerdas', 'recuerdo que', 'hablamos de', 'me dijiste',
    'dijiste sobre', 'que recuerdas', 'qué recuerdas',
    'mi perfil', 'archivos que has', 'archivos analizados',
    'cuántas conversaciones', 'cuantas conversaciones',
    'cuánto llevamos', 'cuanto llevamos', 'nuestra historia',
    'qué sabes de ti', 'que sabes de ti',
    # FIX 4: preguntas por EL CONOCIMIENTO DE BELL → MEMORIA, no Python
    'qué aprendiste', 'que aprendiste', 'qué aprendiste sobre', 'que aprendiste sobre',
    'qué sabes de', 'que sabes de', 'qué conoces', 'que conoces',
    'qué recuerdas de', 'que recuerdas de',
]

_KW_AUTO_ANALISIS = [
    'cuántos archivos', 'cuantos archivos',
    'archivos más importados', 'archivos mas importados',
    'cuál es tu archivo', 'cual es tu archivo',
    'cuántas líneas', 'cuantas lineas',
    'qué tan complejo', 'que tan complejo',
    'complejidad de', 'análisis de ti', 'analiza tu',
    'analiza tus', 'cuál archivo', 'cual archivo',
    'qué archivo', 'que archivo', 'archivos de belladonna',
    'si cambio ', 'si modifico ', 'qué se rompe', 'que se rompe',
    'qué afecta', 'que afecta', 'qué habilidades', 'que habilidades',
    'cuáles son tus', 'cuales son tus',
]
_KW_PYTHON_TECNICO = [
    'genera una función', 'genera una funcion', 'genera el código', 'genera el codigo',
    'escribe el código', 'escribe el codigo', 'crea una función', 'crea una funcion',
    'cómo hago', 'como hago', 'cómo se hace', 'como se hace',
    'analiza este código', 'analiza este codigo', 'analiza el código',
    'explícame', 'explicame', 'qué es un', 'que es un',
    'tengo este error', 'me da error', 'falla el', 'no funciona el',
    'corre este código', 'corre el código', 'ejecuta esto', 'prueba esto',
    'traceback', 'nameerror', 'typeerror', 'valueerror', 'importerror',
    'syntaxerror', 'attributeerror', 'indexerror', 'keyerror',
]
_KW_IDENTIDAD_BELL = [
    'qué eres', 'que eres', 'cómo funcionas', 'como funcionas',
    'quién eres', 'quien eres', 'qué eres tú', 'que eres tu',
    'eres una ia', 'eres un bot', 'eres inteligente',
]
_KW_SEBASTIAN = [
    'quién soy yo', 'quien soy yo', 'cómo me llamo', 'como me llamo',
    'qué sabes de mí', 'que sabes de mi', 'me conoces',
    'dónde vivo', 'donde vivo', 'cuántos años tengo', 'cuantos anos tengo',
    'dónde trabajo', 'donde trabajo', 'dónde estudio', 'donde estudio',
]
_KW_REFLEXION = [
    'qué piensas', 'que piensas', 'qué opinas', 'que opinas',
    'qué crees', 'que crees', 'crees que', 'piensas que',
    'tiene sentido', 'es posible que', 'es verdad que',
]
_KW_FYI = ['fyi:', 'dato:', 'te cuento que', 'sabias que', 'sabías que']

# ── Contexto de navegación web (FIX 1 + 2) ───────────────────────────────────
_SITIOS_WEB = [
    'youtube', 'instagram', 'github', 'gmail', 'twitter', 'x.com',
    'spotify', 'crunchyroll', 'netflix', 'twitch', 'linkedin',
    'facebook', 'tiktok', 'reddit', 'wikipedia', 'stackoverflow',
    'google', 'amazon', 'mercadolibre',
]
_VERBOS_NAVEGACION = [
    'busca en', 'abre ', 'navega a', 've a', 'ponme', 'reproduce',
    'inicia sesion', 'inicia sesión', 'loguéate', 'logueate',
    'escríbele', 'escribele', 'manda un mensaje', 'envíale',
    'dame la url', 'mis repos', 'mis repositorios', 'lee http',
    'descarga el', 'descargar', 'llena el formulario',
]


def _resultado_navegacion() -> dict:
    """Dict de clasificación cuando hay contexto de navegación explícito."""
    return {
        'tipo_mensaje':      'solicitud_navegacion',
        'emocion':           'neutra',
        'intencion':         'navegar',
        'necesidad':         'navegacion_web',
        'estado_subyacente': 'neutro',
        'certeza':           0.92,
        'modo_mental':       'tecnico',
        'habilidad_req':     'NAVEGADOR_WEB',
        'fuente':            'clasificador_bell_nav',
    }


# ── Clasificador principal ────────────────────────────────────────────────────

def clasificar(
    texto: str,
    ids_activados: set = None,
    ids_primarios: set = None,
    contiene_codigo: bool = False,
    perfil: str = 'conversacional',
    es_pregunta: bool = False,
) -> dict:
    """
    Clasifica el mensaje de Sebastian usando los nodos C1/C2 + patrones.
    Retorna dict con tipo_mensaje, emocion, intencion, necesidad, etc.
    """
    t      = _norm(texto)
    ids    = ids_activados or set()
    prim   = ids_primarios or set()

    # ── FIX 1+2: contexto de navegación ANTES de toda clasificación ───────────
    # Si hay un sitio web + verbo de navegación (o una URL), es navegación
    # sin importar que el texto contenga "Python" o suene emocional.
    _tiene_sitio     = any(s in t for s in _SITIOS_WEB)
    _tiene_verbo_nav = any(v in t for v in _VERBOS_NAVEGACION)
    if _tiene_sitio and (_tiene_verbo_nav or 'http://' in t or 'https://' in t):
        return _resultado_navegacion()

    # ── PASO 1: Detectar tipo_mensaje ─────────────────────────────────────────

    tipo = _detectar_tipo(t, ids, prim, contiene_codigo, es_pregunta)
    if tipo == 'solicitud_navegacion':
        return _resultado_navegacion()

    # ── PASO 2: Detectar emoción ──────────────────────────────────────────────

    emocion = _detectar_emocion(t, ids, prim, tipo)

    # ── PASO 3: Modo mental ───────────────────────────────────────────────────

    modo = _detectar_modo(t, ids, prim, tipo, contiene_codigo)

    # ── PASO 4: Habilidad requerida ───────────────────────────────────────────

    habilidad = _detectar_habilidad(t, ids, prim, tipo, contiene_codigo)

    # ── PASO 5: Campos derivados ──────────────────────────────────────────────

    intencion = _tipo_a_intencion(tipo)
    necesidad = _tipo_a_necesidad(tipo, emocion)
    certeza   = _calcular_certeza(tipo, ids, prim, t)

    return {
        'tipo_mensaje':      tipo,
        'emocion':           emocion,
        'intencion':         intencion,
        'necesidad':         necesidad,
        'estado_subyacente': _detectar_estado(tipo, emocion),
        'certeza':           certeza,
        'modo_mental':       modo,
        'habilidad_req':     habilidad,
        'fuente':            'clasificador_bell',
    }


def _detectar_tipo(t, ids, prim, contiene_codigo, es_pregunta):
    # Orden de prioridad: más específico primero

    # FIX 2: sitio web mencionado → navegación (override emocional/streaming),
    # salvo que el mensaje traiga un bloque de código real.
    if not contiene_codigo and any(s in t for s in _SITIOS_WEB):
        return 'solicitud_navegacion'

    # Código detectado en C2 → siempre técnico
    if contiene_codigo:
        return 'solicitud_tecnica'

    # Memoria — siempre técnico aunque suene conversacional
    if any(k in t for k in _KW_MEMORIA):
        return 'solicitud_tecnica'

    # Keywords de alta especificidad primero
    if any(k in t for k in _KW_LOGRO):
        return 'logro_compartido'

    if any(k in t for k in _KW_FYI):
        return 'informacion_compartida'

    # Nodos de saludo/despedida
    if prim & _NODOS_SALUDO:
        return 'saludo'
    if prim & _NODOS_DESPEDIDA or any(k in t for k in ['chao', 'adios', 'hasta luego', 'hasta mañana']):
        return 'despedida'
    if prim & _NODOS_GRATITUD or any(k in t for k in ['gracias', 'te lo agradezco', 'mil gracias']):
        return 'gratitud'

    # Identidad Sebastian
    if any(k in t for k in _KW_SEBASTIAN):
        return 'pregunta_sebastian'

    # Afecto a Bell — "te quiero bell", "te adoro", etc.
    _AFECTO_BELL = ['te quiero', 'te amo', 'te adoro', 'eres especial', 'eres increíble',
                    'eres la mejor', 'me alegras', 'me haces feliz']
    if any(k in t for k in _AFECTO_BELL) and 'bell' in t:
        return 'expresion_emocional_positiva'

    # Identidad Bell
    if any(k in t for k in _KW_IDENTIDAD_BELL):
        return 'pregunta_identidad_bell'
    if prim & {'PREG_QUIEN','PREG_QUE'} and prim & {'BELL_NOMBRE_BELL','REF_TU'} and 'tú' in t:
        return 'pregunta_identidad_bell'

    # Auto-análisis del código de Bell
    if any(k in t for k in _KW_AUTO_ANALISIS):
        return 'solicitud_tecnica'  # C7 enruta a AUTO_ANALISIS_TOTAL

    # Búsqueda internet
    if any(k in t for k in _KW_BUSQUEDA) and not (prim & _NODOS_BELL_TECH):
        return 'solicitud_informacion'

    # Preguntas sobre mundo real con PREG_QUIEN sin contexto Bell
    if 'PREG_QUIEN' in prim and not (prim & _NODOS_BELL_TECH) and not any(k in t for k in _KW_SEBASTIAN):
        if any(k in t for k in ['ganó','gano','es el','son los','es la','cuándo','cuando']):
            return 'solicitud_informacion'

    # Pregunta + palabra desconocida (gap) → probablemente buscar en internet
    # Ej: "qué es Vue", "cómo funciona React"
    if not (prim & _NODOS_BELL_TECH) and not contiene_codigo:
        _PREG_NODOS = {'PREG_QUE','PREG_CUAL','PREG_CUANTO','PREG_COMO','PREG_QUIEN',
                       'PREG_DONDE','PREG_CUANDO','PRON_INTERR_QUE','PRON_INTERR_CUAL'}
        if prim & _PREG_NODOS and len(t.split()) >= 2:
            return 'solicitud_informacion'
        # Palabra sola o frase corta desconocida → buscar (ej: "rust", "vue 3")
        if len(t.split()) <= 3 and not prim and not any(k in t for k in ['hola','hey','ok','sí','si','no ']):
            return 'solicitud_informacion'

    # Técnico Python
    if any(k in t for k in _KW_PYTHON_TECNICO) or (prim & _NODOS_PYTHON):
        return 'solicitud_tecnica'

    # Emocionales negativas
    if any(k in t for k in _KW_CANSANCIO) or 'EMOCION_CANSADO' in prim:
        return 'expresion_emocional_negativa'
    if any(k in t for k in _KW_TRISTEZA) or 'EMOCION_TRISTE' in prim or 'EMOCION_DEPRIMIDO' in prim:
        return 'expresion_emocional_negativa'
    if any(k in t for k in _KW_FRUSTRACION) or 'EMOCION_FRUSTRADO' in prim:
        return 'expresion_emocional_negativa'
    if prim & _NODOS_NEGATIVO:
        return 'expresion_emocional_negativa'

    # Odio/enojo sin nodo explícito
    if any(k in t for k in ['te odio','me odias','odio esto','me tiene harto','me tiene harta']):
        return 'expresion_emocional_negativa'

    # Emocionales positivas
    if prim & _NODOS_LOGRO:
        return 'logro_compartido'
    if prim & _NODOS_POSITIVO:
        return 'expresion_emocional_positiva'

    # Preguntas sobre Bell (estado, consejeras, etc.)
    if prim & _NODOS_BELL_TECH:
        if prim & _NODOS_PREGUNTAS:
            return 'pregunta_identidad_bell'
        return 'pregunta_identidad_bell'

    # Reflexiones / opiniones
    if any(k in t for k in _KW_REFLEXION):
        return 'reflexion'

    # Preguntas generales
    if prim & _NODOS_PREGUNTAS or es_pregunta:
        return 'pregunta'

    # Confirmación / negación
    if prim & {'AFIRMACION','EXPR_OK','EXPR_DALE','EXPR_LISTO'}:
        return 'confirmacion'
    if prim & {'NEGACION','NEGACION_FUERTE'}:
        return 'negacion'

    return 'conversacional'


def _detectar_emocion(t, ids, prim, tipo):
    # Por tipo
    if tipo in ('logro_compartido', 'expresion_emocional_positiva', 'gratitud'):
        if 'EMOCION_ORGULLOSO' in prim or any(k in t for k in ['orgull', 'logré', 'logre']):
            return 'orgullo'
        return 'positiva'
    if tipo == 'despedida':
        return 'neutra'
    if tipo == 'saludo':
        return 'neutra'

    # Por nodos de emoción
    emocion_map = {
        'EMOCION_CANSADO': 'cansancio', 'EMOCION_AGOTADO': 'cansancio',
        'EMOCION_TRISTE':  'tristeza',  'EMOCION_MAL':     'tristeza',
        'EMOCION_DEPRIMIDO': 'tristeza',
        'EMOCION_FRUSTRADO': 'frustración', 'EMOCION_ESTRESADO': 'frustración',
        'EMOCION_PREOCUPADO': 'preocupación', 'EMOCION_ANSIOSO': 'preocupación',
        'EMOCION_FELIZ': 'alegría', 'EMOCION_ALEGRE': 'alegría',
        'EMOCION_MOTIVADO': 'motivación', 'EMOCION_EMOCIONADO': 'emoción',
        'EMOCION_BIEN': 'positiva', 'EMOCION_GENIAL': 'positiva',
        'EMOCION_ORGULLOSO': 'orgullo',
    }
    for nodo, emocion in emocion_map.items():
        if nodo in prim or nodo in ids:
            return emocion

    # Por keywords en texto
    if any(k in t for k in _KW_CANSANCIO): return 'cansancio'
    if any(k in t for k in _KW_TRISTEZA):  return 'tristeza'
    if any(k in t for k in _KW_FRUSTRACION): return 'frustración'

    return 'neutra'


def _detectar_modo(t, ids, prim, tipo, contiene_codigo):
    if tipo in ('expresion_emocional_negativa', 'expresion_emocional_positiva',
                'logro_compartido', 'gratitud'):
        return 'emocional'
    if contiene_codigo or tipo == 'solicitud_tecnica':
        return 'tecnico'
    if tipo in ('saludo', 'despedida', 'conversacional', 'confirmacion', 'negacion'):
        return 'social'
    if tipo in ('pregunta', 'pregunta_identidad_bell', 'reflexion', 'solicitud_informacion'):
        return 'exploratorio'
    return 'social'


def _detectar_habilidad(t, ids, prim, tipo, contiene_codigo):
    """
    Detecta qué habilidad de Bell necesita el mensaje.
    Más específico que el tipo_mensaje.
    """
    # Pregunta sobre archivo específico → SIEMPRE auto-análisis
    import re as _re_c3
    if _re_c3.search(r'\w[\w_]*\.(?:py|js|css|html|json|md)\b', t):
        return 'AUTO_ANALISIS_TOTAL'

    if tipo != 'solicitud_tecnica' and not contiene_codigo:
        # Búsqueda de información externa
        if tipo == 'solicitud_informacion' or any(k in t for k in _KW_BUSQUEDA):
            return 'BUSQUEDA_INTERNET'
        # Memoria
        if prim & _NODOS_MEMORIA or any(k in t for k in ['recuerdas', 'recuerdas', 'acuerdas']):
            return 'MEMORIA'
        return ''

    # Memoria — recuerdos, historial, perfil
    if any(k in t for k in _KW_MEMORIA):
        return 'MEMORIA'

    # Técnico — distinguir Python / Auto-análisis / Búsqueda
    # Auto-análisis: cualquier pregunta sobre Bell+archivo o Bell+código
    _KW_BELL_PROPIO = [
        'tu código', 'tu propio', 'tus archivos', 'tu archivo',
        'cómo estás', 'como estas', 'tu arquitectura',
        'tu capa', 'tus capas', 'tu habilidad', 'tus habilidades',
        'te falta', 'qué te falta', 'que te falta',
    ]
    if any(k in t for k in _KW_BELL_PROPIO):
        return 'AUTO_ANALISIS_TOTAL'
    if any(k in t for k in _KW_AUTO_ANALISIS) or (prim & _NODOS_BELL_TECH and prim & _NODOS_PREGUNTAS):
        return 'AUTO_ANALISIS_TOTAL'

    if contiene_codigo or any(k in t for k in _KW_PYTHON_TECNICO) or (prim & _NODOS_PYTHON):
        # Distinguir modo de Python
        return 'PYTHON_COMPLETO'

    if any(k in t for k in _KW_BUSQUEDA):
        return 'BUSQUEDA_INTERNET'

    return 'PYTHON_COMPLETO'  # default técnico


def _detectar_estado(tipo, emocion):
    mapa = {
        'cansancio':    'agotamiento',
        'tristeza':     'necesita_apoyo',
        'frustración':  'necesita_ayuda',
        'preocupación': 'incertidumbre',
        'orgullo':      'satisfaccion',
        'positiva':     'bienestar',
        'alegría':      'celebracion',
        'neutra':       'neutro',
    }
    return mapa.get(emocion, 'neutro')


def _calcular_certeza(tipo, ids, prim, t):
    # Más nodos relevantes = más certeza
    base = 0.70
    if len(prim) >= 3:  base += 0.05
    if len(prim) >= 5:  base += 0.05
    if tipo != 'conversacional': base += 0.05
    return min(0.95, round(base, 3))


def _tipo_a_intencion(tipo):
    return {
        'saludo':                      'saludar',
        'despedida':                   'despedirse',
        'gratitud':                    'agradecer',
        'pregunta':                    'preguntar',
        'pregunta_identidad_bell':     'conocer_bell',
        'pregunta_estado_bell':        'saber_estado_bell',
        'pregunta_sebastian':          'preguntar_sobre_sebastian',
        'pregunta_arquitectura_bell':  'conocer_arquitectura_bell',
        'solicitud_tecnica':           'pedir_ayuda',
        'solicitud_informacion':       'buscar_informacion',
        'expresion_emocional_positiva':'expresar_emocion_positiva',
        'expresion_emocional_negativa':'expresar_emocion_negativa',
        'logro_compartido':            'compartir_logro',
        'informacion_compartida':      'compartir_informacion',
        'confirmacion':                'confirmar',
        'negacion':                    'negar',
        'reflexion':                   'reflexionar',
        'conversacional':              'conversar',
    }.get(tipo, 'desconocida')


def _tipo_a_necesidad(tipo, emocion):
    if emocion in ('cansancio', 'tristeza', 'frustración', 'preocupación'):
        return 'apoyo_emocional'
    return {
        'saludo':                      'conexion_social',
        'despedida':                   'cierre_conversacion',
        'gratitud':                    'expresar_gratitud',
        'pregunta':                    'informacion',
        'pregunta_identidad_bell':     'conocimiento_bell',
        'solicitud_tecnica':           'ayuda_practica',
        'solicitud_informacion':       'informacion',
        'expresion_emocional_positiva':'compartir_alegria',
        'expresion_emocional_negativa':'apoyo_emocional',
        'logro_compartido':            'compartir_alegria',
        'conversacional':              'conexion_social',
    }.get(tipo, 'desconocida')


# ── Instancia / API compatible con clasificador_groq.py ──────────────────────

class ClasificadorBell:
    """Wrapper compatible con la interfaz de ClasificadorGroq."""

    def clasificar(
        self,
        texto:        str,
        contexto:     dict = None,
        ids_activados: set = None,
        ids_primarios: set = None,
        contiene_codigo: bool = False,
        perfil: str = 'conversacional',
        es_pregunta: bool = False,
    ) -> dict:
        return clasificar(
            texto           = texto,
            ids_activados   = ids_activados or set(),
            ids_primarios   = ids_primarios or set(),
            contiene_codigo = contiene_codigo,
            perfil          = perfil,
            es_pregunta     = es_pregunta,
        )


_instancia = None

def obtener() -> ClasificadorBell:
    global _instancia
    if _instancia is None:
        _instancia = ClasificadorBell()
    return _instancia