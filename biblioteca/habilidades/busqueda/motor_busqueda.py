# biblioteca/habilidades/busqueda/motor_busqueda.py
# ============================================================
# MOTOR BÚSQUEDA — Bell busca, entiende y responde
#
# NIVELES IMPLEMENTADOS:
#   L1 — Búsqueda básica + cache + clarificación (fix: query limpia)
#   L2 — Decisión inteligente: buscar vs memoria + frescura
#   L3 — Multi-fuente para preguntas importantes
#   L6 — Búsqueda contextualizada con perfil Sebastian
#   L8 — Verificación de hechos (FYI)
#
# NIVELES EN ESPERA (infraestructura lista):
#   L5 — Búsqueda proactiva (requiere background worker)
#   L7 — Aprendizaje permanente (requiere habilidad Memoria avanzada)
#   L9 — Agente multi-paso (requiere habilidad Agentes)
# ============================================================

import os
import re
import unicodedata
from typing import Optional

from .buscador     import buscar_y_leer, buscar_multifuente
from .sintetizador import _groq_sintetizar, _groq_respuesta_simple, _groq_clarificacion
from .verificador  import verificar_hecho, _es_verificable

# ── Estado de búsqueda pendiente (entre turnos) ──────────────
_PENDIENTE: dict = {
    'activo':   False,
    'pregunta': '',
    'termino':  '',
    'opcion1':  '',
    'opcion2':  '',
}

# ── Temas que cambian rápido → siempre buscar aunque haya cache ──
_TEMAS_VOLATILES = {
    'precio', 'costo', 'cotización', 'tasa', 'dólar', 'bitcoin',
    'noticia', 'hoy', 'ahora', 'hoy ', 'este año', 'este mes',
    'resultado', 'ganó', 'perdió', 'elección', 'partido',
    'clima', 'temperatura', 'versión', 'lanzó', 'nuevo',
}

# ── Preguntas complejas que merecen multi-fuente ─────────────
_TRIGGERS_MULTIFUENTE = [
    r'\bcompara\b', r'\bdiferencia\s+entre\b', r'\bvs\b', r'\bversus\b',
    r'\bqué\s+es\s+mejor\b', r'\bcuál\s+es\s+mejor\b',
    r'\bpros\s+y\s+contras\b', r'\bventajas\s+y\s+desventajas\b',
    r'\bhistoria\s+de\b', r'\bbiografía\s+de\b', r'\bbiografia\s+de\b',
    r'\bexplícame?\s+(bien|completo|todo)\b',
    r'\bcómo\s+(funciona|se\s+hace|se\s+usa)\b',
    r'\bqué\s+es\s+exactamente\b',
    r'\btutorial\b', r'\bguía\b', r'\bguia\b',
]

# ── Preguntas de datos simples → respuesta corta ─────────────
_TRIGGERS_SIMPLE = [
    r'\bcapital\s+de\b', r'\bcuántos\s+habitantes\b', r'\bpoblación\s+de\b',
    r'\bcuándo\s+nació\b', r'\bcuándo\s+murió\b', r'\bfecha\s+de\s+nacimiento\b',
    r'\bcuánto\s+cuesta\b', r'\bprecio\s+de\b', r'\bedad\s+de\b',
]

# ── Términos conocidos con múltiples significados ────────────
_AMBIGUOS = {
    # Lenguajes vs cosas físicas
    'rust':    ('lenguaje de programación de sistemas', 'óxido o corrosión en metales'),
    'python':  ('lenguaje de programación', 'serpiente pitón'),
    'swift':   ('lenguaje de programación de Apple', 'Taylor Swift o ave vencejo'),
    'java':    ('lenguaje de programación', 'isla de Indonesia o café java'),
    'go':      ('lenguaje de programación de Google', 'juego de mesa asiático'),
    'ruby':    ('lenguaje de programación', 'piedra preciosa o nombre de persona'),
    'crystal': ('lenguaje de programación', 'cristal mineral'),
    'elm':     ('lenguaje de programación funcional', 'árbol olmo'),
    'scala':   ('lenguaje de programación JVM', 'ciudad italiana o escala musical'),
    'cobra':   ('lenguaje de programación', 'serpiente venenosa cobra'),
    'phoenix': ('framework web de Elixir', 'ciudad de Arizona o ave mítica'),
    # Tecnología vs personas
    'mercury': ('planet del sistema solar', 'elemento químico o banda de rock'),
    'apollo':  ('framework o proyecto NASA', 'nombre propio o misión lunar'),
    'ada':     ('lenguaje de programación militar', 'nombre de persona'),
    'grace':   ('framework web', 'nombre de persona'),
    # Frameworks vs conceptos generales
    'django':  ('framework web Python', 'Django Unchained o nombre'),
    'rails':   ('framework Ruby on Rails', 'trenes o rieles'),
    'spring':  ('framework Java', 'primavera estación del año'),
    'flask':   ('microframework Python', 'frasco o termo'),
    'vapor':   ('framework Swift', 'vapor de agua o gas'),
    'falcon':  ('framework Python REST', 'halcón o película/personaje'),
    # Conceptos de hardware vs software
    'butterfly': ('efecto butterfly', 'mariposa insecto'),
    'docker':  ('herramienta de contenedores', 'trabajador del muelle'),
    'harbor':  ('registro de contenedores', 'puerto marítimo'),
    # Nombres de proyectos ambiguos
    'atlas':   ('base de datos MongoDB o proyecto IA', 'gigante mitológico o atlas geográfico'),
    'titan':   ('proyecto tecnológico', 'luna de Saturno o titán mitológico'),
    'aurora':  ('base de datos AWS', 'aurora boreal o nombre propio'),
    'cassandra': ('base de datos NoSQL', 'personaje mitológico o nombre'),
    'redis':   ('base de datos en memoria', 'nada — siempre es la BD'),
    'kafka':   ('sistema de mensajería', 'Franz Kafka escritor'),
    'spark':   ('procesamiento de datos Apache', 'chispa o nombre'),
    'hadoop':  ('framework big data', 'nada — siempre es el framework'),
    'elastic': ('Elasticsearch', 'elástico material'),
    'grafana': ('herramienta de dashboards', 'nada — siempre es la herramienta'),
}

# ── Contexto técnico → no preguntar ambigüedad ───────────────
_CONTEXTO_TECH = {
    'lenguaje', 'programacion', 'programación', 'codigo', 'código',
    'framework', 'libreria', 'librería', 'biblioteca', 'compilador',
    'backend', 'frontend', 'web', 'software', 'desarrollar', 'instalar',
    'aprender', 'tutorial', 'syntax', 'sintaxis', 'tipos', 'funciones',
    'async', 'concurrencia', 'memoria', 'ownership', 'container',
    'contenedor', 'docker', 'kubernetes', 'deploy', 'desplegar',
    'servidor', 'api', 'endpoint', 'base de datos', 'query',
    'python', 'javascript', 'java ', 'nodejs', 'react', 'flask',
}

# ── Frases de clarificación que Bell reconoce ────────────────
_FRASES_CLARIFICACION = [
    r'\bme\s+refiero',
    r'\bel\s+lenguaje\b',
    r'\bde\s+programacion\b', r'\bde\s+programación\b',
    r'\bprogramar\b', r'\bprogramacion\b',
    r'\bel\s+oxido\b', r'\bel\s+metal\b',
    r'\bla\s+ciudad\b', r'\bel\s+animal\b',
    r'\bla\s+planta\b', r'\bla\s+serpiente\b',
    r'\bla\s+piedra\b', r'\bel\s+ave\b',
    r'\bes\s+el\s+lenguaje\b',
    r'\bes\s+la\s+herramienta\b',
    r'\bes\s+el\s+framework\b',
    r'\bes\s+la\s+base\s+de\s+datos\b',
    r'\bno\s+la\s+(roca|planta|persona|animal)\b',
    r'\bla\s+(primera|segunda|tercera)\s+opcion\b',
    r'\b(1|2|opcion\s+1|opcion\s+2)\b',
]

_AÑO_ACTUAL = '2026'


def _normalizar(texto: str) -> str:
    """Normaliza texto: minúsculas + sin acentos."""
    texto = texto.lower().strip()
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )


def _es_tema_volatile(texto: str) -> bool:
    tl = texto.lower()
    return any(t in tl for t in _TEMAS_VOLATILES)


def _necesita_multifuente(texto: str) -> bool:
    tl = texto.lower()
    return any(re.search(p, tl) for p in _TRIGGERS_MULTIFUENTE)


def _es_simple(texto: str) -> bool:
    tl = texto.lower()
    return any(re.search(p, tl) for p in _TRIGGERS_SIMPLE)


def _detectar_ambiguedad(texto: str) -> Optional[tuple]:
    tl = texto.lower()
    palabras = set(re.findall(r'\b\w+\b', tl))
    if palabras & _CONTEXTO_TECH:
        return None
    for termino, (op1, op2) in _AMBIGUOS.items():
        if termino in palabras:
            return (termino, op1, op2)
    return None


def _es_respuesta_clarificacion(texto: str) -> bool:
    if not _PENDIENTE['activo']:
        return False
    tl = texto.lower().strip()
    if len(tl.split()) > 10:
        return False
    return any(re.search(p, tl, re.IGNORECASE) for p in _FRASES_CLARIFICACION)


def _construir_query(texto: str, clarificacion: Optional[str] = None) -> str:
    """
    L1 fix + L6: Construye query limpia y enriquecida.
    Elimina prefijos conversacionales y añade contexto según tipo.
    """
    tl = texto.lower().strip()

    # Eliminar prefijos conversacionales
    prefijos = [
        r'^busca\s+(?:en\s+(?:internet|la\s+web)\s+)?',
        r'^(?:qué|que)\s+es\s+(?:exactamente\s+)?',
        r'^(?:qué|que)\s+son\s+',
        r'^(?:cómo|como)\s+(?:funciona|se\s+hace|se\s+usa|se\s+instala)\s+',
        r'^(?:dime|cuéntame|cuentame|háblame|hablame)\s+(?:qué|que|sobre|de|acerca\s+de)\s+',
        r'^busca\s+información\s+(?:sobre|de)\s+',
        r'^investiga\s+(?:sobre\s+|acerca\s+de\s+)?',
        r'^(?:explícame?|explicame?)\s+',
        r'^quiero\s+saber\s+(?:sobre|de|acerca\s+de)?\s+',
        r'^información\s+(?:de|sobre)\s+',
        r'^para\s+qué\s+sirve\s+',
        r'^(?:quién|quien)\s+es\s+',
        r'^(?:dónde|donde)\s+queda\s+',
        r'^(?:cuándo|cuando)\s+(?:fue|nació|murió)\s+',
        r'^histori(?:a|a\s+de)\s+',
        r'^biografi(?:a|a\s+de)\s+',
        r'^define\s+',
        r'^definición\s+de\s+', r'^definicion\s+de\s+',
    ]
    query = tl
    for p in prefijos:
        nuevo = re.sub(p, '', query, flags=re.IGNORECASE).strip()
        if nuevo and len(nuevo) > 2:
            query = nuevo
            break

    query = query.strip('?¿ ')

    # Enriquecer con clarificación si hay
    if clarificacion:
        query = f'{query} {clarificacion}'

    # Añadir año para temas volátiles
    if _es_tema_volatile(texto):
        if _AÑO_ACTUAL not in query:
            query = f'{query} {_AÑO_ACTUAL}'

    # Enriquecer según tipo de pregunta
    original_lower = texto.lower()
    if any(w in original_lower for w in ['quién es', 'quien es', 'quién fue', 'quien fue']):
        if 'wikipedia' not in query and 'biography' not in query:
            query = f'{query} wikipedia'
    elif any(w in original_lower for w in ['cómo funciona', 'como funciona',
                                            'cómo se hace', 'como se hace']):
        query = f'{query} explicación'
    elif any(w in original_lower for w in ['precio', 'cuánto cuesta', 'cuanto cuesta']):
        query = f'{query} precio Colombia'

    return query.strip()


def _obtener_perfil_sebastian() -> str:
    """
    L6: Obtiene contexto de Sebastian para enriquecer búsquedas.
    Retorna string compacto para incluir en prompts.
    """
    try:
        from biblioteca.memoria import obtener_memoria
        mem = obtener_memoria()
        perfil = mem.obtener_perfil()
        if not perfil:
            return ''
        items = []
        for k in ('nombre', 'ciudad', 'trabajo', 'proyectos', 'lenguaje_favorito'):
            v = perfil.get(k, '')
            if v:
                items.append(f'{k}={v}')
        return ', '.join(items[:6])
    except Exception:
        return 'nombre=Sebastian, ciudad=Bucaramanga, trabajo=Jelcon, proyecto=BELLADONNA'


def _enriquecer_query_con_perfil(query: str, texto_original: str, perfil: str) -> str:
    """
    L6: Añade contexto de Sebastian si es relevante.
    Solo para preguntas que se benefician del contexto.
    """
    if not perfil:
        return query
    tl = texto_original.lower()
    # "qué framework usar" → añadir Python al contexto de búsqueda
    if any(w in tl for w in ['framework', 'librería', 'libreria', 'qué usar',
                               'que usar', 'recomienda', 'mejor para',
                               'para mi proyecto']):
        return f'{query} Python Flask'
    return query


def _revision_memoria_l2(query: str, texto: str) -> Optional[str]:
    """
    L2: Antes de ir a internet, verificar si Bell ya sabe esto.
    Usa TF-IDF semántico + cache + conocimiento propio.
    """
    if _es_tema_volatile(texto):
        return None  # temas volátiles → siempre buscar

    try:
        from biblioteca.memoria import obtener_memoria
        mem = obtener_memoria()

        # 1. Cache exacto reciente (48h)
        query_norm = _normalizar(query)
        cached = mem.buscar_cache_web(query_norm, max_horas=48)
        if cached:
            print('  [Búsqueda L2] ✓ Cache reciente')
            return cached

        # 2. Búsqueda semántica TF-IDF (nuevo en v2)
        semantico = mem.buscar_semantico(query)
        if semantico and len(semantico) > 50:
            print('  [Búsqueda L2] ✓ TF-IDF semántico')
            return semantico

        # 3. Conocimiento aprendido con alta confianza
        tema = re.sub(r'\b(wikipedia|definicion|definición|explicacion|explicación)\b',
                      '', query_norm).strip()
        conocido = mem.consultar_conocimiento(tema)
        if conocido and conocido.get('confianza', 0) >= 0.78:
            print('  [Búsqueda L2] ✓ Conocimiento propio')
            return conocido['respuesta']

    except Exception:
        pass

    return None


def ejecutar_busqueda(texto: str, clarificacion_previa: Optional[str] = None) -> dict:
    """
    Punto de entrada principal. Orquesta todos los niveles.
    """
    global _PENDIENTE

    # ── 1. Verificación de hecho FYI (L8) ─────────────────
    if _es_verificable(texto) and not clarificacion_previa:
        verif = verificar_hecho(texto)
        if verif.get('verificado') and verif.get('respuesta'):
            print(f'  [Búsqueda L8] Verificación: correcto={verif["correcto"]}')
            return {
                'exitoso':   True,
                'respuesta': verif['respuesta'],
                'url':       verif.get('fuente', ''),
                'tipo':      'verificacion_hecho',
            }

    # ── 2. Respuesta a clarificación pendiente ─────────────
    if _es_respuesta_clarificacion(texto):
        pregunta_original = _PENDIENTE['pregunta']
        _PENDIENTE['activo'] = False
        return ejecutar_busqueda(pregunta_original, clarificacion_previa=texto)

    # ── 3. Detectar ambigüedad (L1) ────────────────────────
    if not clarificacion_previa:
        ambiguedad = _detectar_ambiguedad(texto)
        if ambiguedad:
            termino, op1, op2 = ambiguedad
            _PENDIENTE.update({
                'activo':   True,
                'pregunta': texto,
                'termino':  termino,
                'opcion1':  op1,
                'opcion2':  op2,
            })
            pregunta_clar = _groq_clarificacion(termino, op1, op2)
            return {
                'exitoso':   True,
                'respuesta': pregunta_clar,
                'tipo':      'pide_clarificacion',
            }

    _PENDIENTE['activo'] = False

    # ── 4. Construir query limpia + enriquecida ────────────
    perfil = _obtener_perfil_sebastian()  # L6
    query  = _construir_query(texto, clarificacion_previa)
    query  = _enriquecer_query_con_perfil(query, texto, perfil)  # L6
    print(f'  [Búsqueda] Query: "{query}"')

    # ── 5. L2: Revisar memoria antes de internet ───────────
    desde_memoria = _revision_memoria_l2(query, texto)
    if desde_memoria:
        return {
            'exitoso':   True,
            'respuesta': desde_memoria,
            'url':       '(memoria)',
            'tipo':      'desde_memoria',
        }

    # ── 6. Decidir modo: multi-fuente vs simple ────────────
    usar_multifuente = _necesita_multifuente(texto)
    es_simple        = _es_simple(texto)

    if usar_multifuente:
        # L3: Multi-fuente
        print('  [Búsqueda L3] Multi-fuente')
        datos = buscar_multifuente(query, max_fuentes=3)
        if datos['total_fuentes'] == 0:
            return {
                'exitoso':   False,
                'respuesta': f"Busqué '{query}' pero no encontré fuentes válidas.",
                'tipo':      'sin_resultados',
            }
        detallado = datos['total_fuentes'] >= 2 or not es_simple
        respuesta = _groq_sintetizar(
            pregunta   = texto,
            fuentes    = datos['fuentes'],
            perfil_ctx = perfil,
            detallado  = detallado,
        )
        if not respuesta:
            # Fallback: concatenar snippets
            respuesta = '\n'.join(
                f['resumen'] for f in datos['fuentes'][:2] if f.get('resumen')
            )[:400]
        url = datos['fuentes'][0]['url'] if datos['fuentes'] else ''

    else:
        # L1/L4: Una fuente, lectura profunda
        resultado = buscar_y_leer(query)
        if not resultado['contenido']:
            return {
                'exitoso':   False,
                'respuesta': f"Busqué '{query}' pero no encontré información útil.",
                'url':       '',
                'tipo':      'sin_resultados',
            }
        url       = resultado['url']
        detallado = not es_simple
        respuesta = _groq_respuesta_simple(
            pregunta   = texto,
            contenido  = resultado['contenido'],
            url        = url,
            perfil_ctx = perfil,
            detallado  = detallado,
        )
        if not respuesta:
            # Fallback: snippet del primer resultado
            snippets  = [r['resumen'] for r in resultado['resultados'][:2] if r.get('resumen')]
            respuesta = ' '.join(snippets)[:350] if snippets else 'No pude procesar los resultados.'

    # ── 7. Guardar en memoria L7 — aprendizaje permanente activo ──
    try:
        from biblioteca.memoria import obtener_memoria
        mem = obtener_memoria()
        query_norm = _normalizar(query)
        calidad    = 0.85 if len(respuesta) > 80 else 0.5

        # L7a: Cache de búsqueda web (temporal, 48h)
        mem.guardar_busqueda_web(query_norm, respuesta, url, calidad=calidad)

        # L7b: Aprendizaje permanente — guarda como conocimiento
        # Solo si la respuesta tiene calidad suficiente
        if calidad >= 0.75 and len(respuesta) > 80:
            tema_limpio = re.sub(
                r'\b(wikipedia|definicion|explicacion|que es|quien es)\b',
                '', query_norm
            ).strip()
            if tema_limpio:
                mem.guardar_conocimiento(
                    tema       = tema_limpio,
                    respuesta  = respuesta,
                    tipo       = _detectar_tipo_conocimiento(query),
                    fuente     = 'busqueda_internet',
                    pregunta   = query,
                    url        = url,
                    confianza  = calidad,
                )
                print(f'  [Búsqueda L7] 📚 Aprendido: "{tema_limpio[:40]}"')
    except Exception:
        pass

    return {
        'exitoso':   True,
        'respuesta': respuesta,
        'url':       url,
        'tipo':      'busqueda_multifuente' if usar_multifuente else 'busqueda_directa',
    }