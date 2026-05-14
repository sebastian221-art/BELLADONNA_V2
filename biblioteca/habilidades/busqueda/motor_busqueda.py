# biblioteca/habilidades/busqueda/motor_busqueda.py
# ============================================================
# MOTOR BÚSQUEDA — Bell busca, entiende y responde
#
# Flujo completo:
# 1. Detectar ambigüedad → pedir clarificación si es necesario
# 2. Construir query rica con contexto
# 3. Buscar + leer página
# 4. Groq procesa y responde en voz de Bell
# ============================================================

import os
import re
import httpx
from typing import Optional

from .buscador import buscar_y_leer

# ── Estado de búsqueda pendiente (entre turnos) ──────────────
# Cuando Bell pide clarificación, guarda la pregunta original
# para retomarla cuando el usuario responda.
_PENDIENTE: dict = {
    'activo':    False,
    'pregunta':  '',   # "qué es Rust"
    'termino':   '',   # "rust"
    'opcion1':   '',
    'opcion2':   '',
}

# ── Frases que indican respuesta de clarificación ────────────
_FRASES_CLARIFICACION = [
    r'me refiero',
    r'el lenguaje',
    r'el lenguaje de programacion',
    r'programacion',
    r'programar',
    r'el oxido',
    r'el metal',
    r'la ciudad',
    r'el animal',
    r'la planta',
    r'es el lenguaje',
    r'es la ciudad',
    r'es el metal',
]

_GROQ_URL   = 'https://api.groq.com/openai/v1/chat/completions'
_GROQ_MODEL = 'openai/gpt-oss-120b'
_GROQ_KEY   = os.getenv('GROQ_API_KEY', '')

# ── Términos conocidos con múltiples significados ────────────
_AMBIGUOS = {
    'rust':    ('lenguaje de programación de sistemas', 'óxido o corrosión en metales'),
    'python':  ('lenguaje de programación', 'serpiente pitón'),
    'swift':   ('lenguaje de programación de Apple', 'Taylor Swift o ave vencejo'),
    'java':    ('lenguaje de programación', 'isla de Indonesia o café'),
    'go':      ('lenguaje de programación de Google', 'juego de mesa asiático'),
    'mercury': ('planeta del sistema solar', 'elemento químico o empresa'),
    'cobra':   ('serpiente venenosa', 'herramienta o lenguaje'),
    'scala':   ('lenguaje de programación', 'ciudad en Italia'),
    'ruby':    ('lenguaje de programación', 'piedra preciosa o nombre'),
    'crystal': ('lenguaje de programación', 'cristal mineral'),
    'phoenix': ('framework de Elixir', 'ciudad de Arizona o ave mítica'),
    'elm':     ('lenguaje de programación', 'árbol olmo'),
}

# ── Palabras que indican contexto de programación ────────────
_CONTEXTO_TECH = {
    'lenguaje', 'programacion', 'programación', 'codigo', 'código',
    'framework', 'libreria', 'librería', 'biblioteca', 'compilador',
    'backend', 'frontend', 'web', 'software', 'desarrollar', 'instalar',
    'aprender', 'tutorial', 'syntax', 'sintaxis', 'tipos', 'funciones',
    'async', 'concurrencia', 'memoria', 'ownership',
}


def _detectar_ambiguedad(texto: str) -> Optional[tuple]:
    """
    Detecta si la pregunta es sobre un término ambiguo sin suficiente contexto.
    Retorna (termino, opcion1, opcion2) si es ambiguo, None si está claro.
    """
    tl = texto.lower()
    palabras = set(re.findall(r'\b\w+\b', tl))

    # Si ya hay contexto técnico, no preguntar
    if palabras & _CONTEXTO_TECH:
        return None

    # Buscar término ambiguo en la pregunta
    for termino, (op1, op2) in _AMBIGUOS.items():
        if termino in palabras:
            return (termino, op1, op2)
    return None


def _construir_query(texto: str, clarificacion: Optional[str] = None) -> str:
    """
    Construye una query de búsqueda precisa a partir del texto del usuario.
    Si hay clarificación de Bell, la usa para enriquecer la query.
    """
    tl = texto.lower().strip()

    # Eliminar prefijos conversacionales
    prefijos = [
        r'^busca\s+(en\s+internet\s+|en\s+la\s+web\s+)?',
        r'^(?:qué|que)\s+es\s+',
        r'^(?:cómo|como)\s+funciona\s+',
        r'^(?:dime|cuéntame|cuentame)\s+(?:qué|que)\s+es\s+',
        r'^busca\s+información\s+(?:sobre|de)\s+',
        r'^investiga\s+(?:sobre\s+|acerca\s+de\s+)?',
        r'^explícame\s+|^explicame\s+',
        r'^quiero\s+saber\s+(?:sobre|de)\s+',
        r'^información\s+(?:de|sobre)\s+',
        r'^para\s+qué\s+sirve\s+',
    ]
    query = tl
    for p in prefijos:
        nuevo = re.sub(p, '', query, flags=re.IGNORECASE).strip()
        if nuevo:
            query = nuevo
            break

    query = query.strip('?¿ ')

    # Enriquecer con clarificación si viene
    if clarificacion:
        query = f"{query} {clarificacion}"

    # Si la query es muy corta (1 palabra) y no tiene contexto, añadir contexto de la pregunta original
    if len(query.split()) == 1:
        if 'funciona' in tl or 'cómo' in tl or 'como' in tl:
            query += ' cómo funciona'
        elif 'qué es' in tl or 'que es' in tl:
            query += ' qué es definición'

    return query.strip()


def _groq_procesar(pregunta: str, contenido_web: str, url: str) -> str:
    """Groq lee el contenido web y genera respuesta en voz de Bell."""
    if not _GROQ_KEY:
        return ''
    try:
        contexto = (
            f"CONTENIDO REAL DE INTERNET:\n"
            f"Fuente: {url}\n\n"
            f"{contenido_web[:1800]}"
        )
        r = httpx.post(
            _GROQ_URL,
            headers={'Authorization': f'Bearer {_GROQ_KEY}',
                     'Content-Type': 'application/json'},
            json={
                'model': _GROQ_MODEL,
                'messages': [
                    {'role': 'system', 'content': (
                        "Eres Bell — IA de Sebastian Gómez (Bucaramanga). "
                        "Encontraste esta información en internet y la explicas en primera persona. "
                        "NUNCA inventes ni añadas datos que no estén en el contenido. "
                        "NUNCA uses markdown, tablas ni bullets. "
                        "NUNCA empieces con Claro, Por supuesto, Hola ni te presentes. "
                        "Prosa fluida en español. 3-4 oraciones directas y completas."
                    )},
                    {'role': 'user', 'content': (
                        f"{contexto}\n\n"
                        f"Sebastian pregunta: {pregunta}\n\n"
                        "Responde basándote SOLO en el contenido encontrado. "
                        "Si el contenido no responde bien la pregunta, dilo honestamente."
                    )},
                ],
                'temperature': 0.25,
                'max_tokens':  280,
            },
            timeout=25,
        )
        if r.status_code == 200:
            content = r.json().get('choices', [{}])[0].get('message', {}).get('content', '').strip()
            if content and len(content) > 20:
                if content[-1] not in '.!?':
                    content += '.'
                return content
    except Exception as e:
        print(f"  [Busqueda Groq] {e}")
    return ''


def _groq_pedir_clarificacion(termino: str, opcion1: str, opcion2: str) -> str:
    """Bell pide clarificación antes de buscar un término ambiguo."""
    if not _GROQ_KEY:
        return f"Cuando dices '{termino}', ¿te refieres al {opcion1} o al {opcion2}?"
    try:
        r = httpx.post(
            _GROQ_URL,
            headers={'Authorization': f'Bearer {_GROQ_KEY}',
                     'Content-Type': 'application/json'},
            json={
                'model': _GROQ_MODEL,
                'messages': [
                    {'role': 'system', 'content': (
                        "Eres Bell — IA de Sebastian. Hablas en primera persona, natural y directa. "
                        "NUNCA uses markdown ni bullets. Una sola pregunta corta."
                    )},
                    {'role': 'user', 'content': (
                        f"El usuario preguntó sobre '{termino}' que puede significar: "
                        f"(1) {opcion1} o (2) {opcion2}. "
                        "Pide clarificación en UNA oración natural, sin listar opciones numéricas."
                    )},
                ],
                'temperature': 0.3,
                'max_tokens': 60,
            },
            timeout=10,
        )
        if r.status_code == 200:
            content = r.json().get('choices', [{}])[0].get('message', {}).get('content', '').strip()
            if content:
                return content
    except Exception:
        pass
    return f"Cuando dices '{termino}', ¿te refieres al {opcion1} o al {opcion2}?"


def _es_respuesta_clarificacion(texto: str) -> bool:
    """Detecta si el texto es una respuesta a la pregunta de clarificación de Bell."""
    if not _PENDIENTE['activo']:
        return False
    tl = texto.lower().strip()
    # Respuesta corta (menos de 8 palabras) → probable clarificación
    if len(tl.split()) > 8:
        return False
    for patron in _FRASES_CLARIFICACION:
        if re.search(patron, tl, re.IGNORECASE):
            return True
    return False


def ejecutar_busqueda(texto: str, clarificacion_previa: Optional[str] = None) -> dict:
    """
    Punto de entrada principal.
    clarificacion_previa: si el usuario ya aclaró ('el lenguaje', 'el óxido'), se usa directamente.
    """

    global _PENDIENTE

    # 1. Verificar si es respuesta a clarificación pendiente
    if _es_respuesta_clarificacion(texto):
        pregunta_original = _PENDIENTE['pregunta']
        _PENDIENTE['activo'] = False
        # Usar la respuesta como clarificación para la pregunta original
        return ejecutar_busqueda(pregunta_original, clarificacion_previa=texto)

    # 2. Detectar ambigüedad (solo si no hay clarificación previa)
    if not clarificacion_previa:
        ambiguedad = _detectar_ambiguedad(texto)
        if ambiguedad:
            termino, op1, op2 = ambiguedad
            # Guardar estado pendiente
            _PENDIENTE.update({
                'activo':   True,
                'pregunta': texto,
                'termino':  termino,
                'opcion1':  op1,
                'opcion2':  op2,
            })
            pregunta_clarificacion = _groq_pedir_clarificacion(termino, op1, op2)
            return {
                'exitoso':   True,
                'respuesta': pregunta_clarificacion,
                'tipo':      'pide_clarificacion',
            }

    # Limpiar pendiente si llegamos aquí con clarificación
    _PENDIENTE['activo'] = False

    # 3. Construir query rica
    _query_original = texto  # guardar para cache con query limpia
    query = _construir_query(texto, clarificacion_previa)
    print(f"  [Busqueda] Query: '{query}'")

    # 3a. Revisar cache de memoria antes de buscar en internet
    try:
        from biblioteca.memoria import obtener_memoria
        mem = obtener_memoria()

        # ¿Ya tenemos esta búsqueda en cache reciente?
        cached = mem.buscar_cache_web(query, max_horas=48)
        if cached:
            print(f"  [Busqueda] ✓ Desde memoria cache")
            return {
                'exitoso':   True,
                'respuesta': cached,
                'url':       '(memoria)',
                'tipo':      'desde_memoria',
            }

        # ¿Bell ya conoce el tema?
        tema = query.replace('que es ', '').replace('quien es ', '')                     .replace('donde queda ', '').strip()
        conocido = mem.consultar_conocimiento(tema)
        if conocido and conocido.get('confianza', 0) >= 0.7:
            print(f"  [Busqueda] ✓ Desde conocimiento")
            return {
                'exitoso':   True,
                'respuesta': conocido['respuesta'],
                'url':       conocido.get('url', '(conocimiento)'),
                'tipo':      'desde_conocimiento',
            }
    except Exception:
        pass  # memoria no bloquea la búsqueda

    # 3b. Buscar en internet
    resultado = buscar_y_leer(query)

    if not resultado['contenido']:
        return {
            'exitoso':   False,
            'respuesta': f"Busqué '{query}' en internet pero no encontré información útil.",
            'url':       '',
            'tipo':      'sin_resultados',
        }

    # 4. Groq procesa y responde
    respuesta = _groq_procesar(texto, resultado['contenido'], resultado['url'])

    if not respuesta:
        # Fallback: resumen de los snippets de DDG
        snippets = [r['resumen'] for r in resultado['resultados'][:2] if r.get('resumen')]
        respuesta = ' '.join(snippets)[:350] if snippets else "No pude procesar los resultados."

    # Guardar en memoria para uso futuro
    try:
        from biblioteca.memoria import obtener_memoria
        obtener_memoria().guardar_busqueda_web(
            query, respuesta, resultado['url'],
            calidad=0.8 if respuesta and len(respuesta) > 50 else 0.4
        )
    except Exception:
        pass

    return {
        'exitoso':   True,
        'respuesta': respuesta,
        'url':       resultado['url'],
        'tipo':      'busqueda_directa',
    }