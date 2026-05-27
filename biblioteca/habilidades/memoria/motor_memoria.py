# biblioteca/habilidades/memoria/motor_memoria.py
# ============================================================
# MOTOR DE MEMORIA — punto de entrada de la habilidad MEMORIA
#
# Una función pública: procesar(texto) -> dict
#
# Flujo:
#   1. Clasificar el tipo de consulta (Python puro, sin Groq)
#   2. Recuperar del store correcto (recuperador_inteligente)
#   3. Construir respuesta factual. Sin datos → honesto.
#
# Groq NO interviene aquí: clasificación y respuesta son Python.
# ============================================================

PERFIL       = 'PERFIL'
EPISODIO     = 'EPISODIO'
CONOCIMIENTO = 'CONOCIMIENTO'
BELL_SELF    = 'BELL_SELF'
SESION       = 'SESION'

# Orden de chequeo importa: BELL_SELF y CONOCIMIENTO antes que PERFIL
# para que "qué sabes sobre Docker" no se confunda con el perfil.
_KW = {
    BELL_SELF: [
        'quién eres', 'quien eres', 'qué puedes', 'que puedes',
        'cuántas conversaciones', 'cuantas conversaciones',
        'cuánto llevamos', 'cuanto llevamos', 'qué eres', 'que eres',
    ],
    CONOCIMIENTO: [
        'qué aprendiste de', 'que aprendiste de',
        'qué aprendiste sobre', 'que aprendiste sobre',
        'sabes algo de', 'qué sabes sobre', 'que sabes sobre',
    ],
    PERFIL: [
        'qué sabes de mí', 'que sabes de mi', 'sabes de mí', 'sabes de mi',
        'mi perfil', 'sabes sobre mí', 'sabes sobre mi',
        'qué sé de ti', 'que se de ti', 'qué sabes de mi', 'me conoces',
    ],
    EPISODIO: [
        'recuerdas', 'hablamos', 'me dijiste', 'quedamos', 'me contaste',
        'la última vez', 'la ultima vez', 'ayer', 'la semana',
        'en qué quedamos', 'en que quedamos',
    ],
}


def _clasificar(texto: str) -> str:
    tl = texto.lower().strip()
    for tipo in (BELL_SELF, CONOCIMIENTO, PERFIL, EPISODIO):
        if any(k in tl for k in _KW[tipo]):
            return tipo
    return SESION


def procesar(texto: str) -> dict:
    """Punto de entrada. Retorna {'respuesta','exitoso','tipo'}."""
    tipo = _clasificar(texto or '')
    try:
        from biblioteca.habilidades.memoria.gestor import obtener_memoria
        from biblioteca.habilidades.memoria.recuperador_inteligente import RecuperadorInteligente
        gestor    = obtener_memoria()
        respuesta = RecuperadorInteligente.obtener().recuperar(texto, tipo, gestor)
    except Exception as e:
        return {
            'respuesta': 'No pude consultar mi memoria en este momento.',
            'exitoso':   False,
            'tipo':      'error',
            'error':     str(e),
        }

    # FIX 3: validar relevancia del conocimiento recuperado.
    # Si la respuesta no menciona ninguna palabra clave de la pregunta,
    # es un resultado irrelevante → ser honesta en vez de devolverlo.
    if respuesta and tipo == CONOCIMIENTO:
        palabras_clave = [w for w in texto.lower().split() if len(w) > 3]
        if palabras_clave and not any(p in respuesta.lower() for p in palabras_clave):
            respuesta = 'No tengo conocimiento guardado sobre eso todavía.'

    if not respuesta or not respuesta.strip():
        respuesta = 'No tengo registro de eso todavía.'

    return {'respuesta': respuesta.strip(), 'exitoso': True, 'tipo': tipo}
