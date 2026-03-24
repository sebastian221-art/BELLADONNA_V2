# biblioteca/fundacional/vocabulario/neuronas_preguntas.py
# ================================================
# NEURONAS DE PREGUNTAS E IDENTIDAD
# Cuando alguien pregunta "quién eres"
# estas neuronas activan todo sobre Bell
# ================================================

def crear_neuronas_preguntas(red):

    # ---- PREGUNTAS BÁSICAS ----
    preguntas_base = [
        ('PREG_QUE',    'qué',    0.90),
        ('PREG_QUIEN',  'quién',  0.90),
        ('PREG_COMO',   'cómo',   0.90),
        ('PREG_CUANDO', 'cuándo', 0.85),
        ('PREG_DONDE',  'dónde',  0.85),
        ('PREG_POR_QUE','por qué',0.90),
        ('PREG_CUANTO', 'cuánto', 0.85),
        ('PREG_CUAL',   'cuál',   0.85),
    ]

    for nodo_id, _, grounding in preguntas_base:
        red.agregar_nodo({
            'id': nodo_id,
            'nucleo': {
                'tipo': 'concepto',
                'subtipo': 'pregunta',
                'grounding_base': grounding,
                'dimensiones_activas': ['conocimiento', 'contexto'],
                'archivo_real': None,
                'inmutable': False
            },
            'activacion': {
                'umbral': 0.2,
                'velocidad': 'rapida',
                'mielina': False
            },
            'memoria': {
                'veces_usado': 0, 'ultimo_uso': None,
                'contextos_de_uso': [],
                'resultado_historico': grounding
            }
        })

    # ---- AFIRMACIÓN Y NEGACIÓN ----
    for nodo_id, grounding in [
        ('AFIRMACION', 0.95), ('AFIRMACION_FUERTE', 0.90),
        ('NEGACION', 0.95),   ('NEGACION_FUERTE', 0.90)
    ]:
        red.agregar_nodo({
            'id': nodo_id,
            'nucleo': {
                'tipo': 'concepto',
                'subtipo': 'confirmacion',
                'grounding_base': grounding,
                'dimensiones_activas': ['conocimiento', 'contexto'],
                'archivo_real': None, 'inmutable': False
            },
            'activacion': {
                'umbral': 0.2, 'velocidad': 'rapida', 'mielina': False
            },
            'memoria': {
                'veces_usado': 0, 'ultimo_uso': None,
                'contextos_de_uso': [],
                'resultado_historico': grounding
            }
        })

    # ---- REFERENCIAS PERSONALES ----
    referencias = [
        ('REF_YO',       0.90), ('REF_TU',       0.90),
        ('REF_EL',       0.85), ('REF_ELLA',      0.85),
        ('REF_NOSOTROS', 0.85), ('REF_ME',        0.80),
        ('REF_MI',       0.80), ('REF_TE',        0.80),
    ]

    for nodo_id, grounding in referencias:
        red.agregar_nodo({
            'id': nodo_id,
            'nucleo': {
                'tipo': 'concepto',
                'subtipo': 'referencia_personal',
                'grounding_base': grounding,
                'dimensiones_activas': ['contexto'],
                'archivo_real': None, 'inmutable': False
            },
            'activacion': {
                'umbral': 0.25, 'velocidad': 'media', 'mielina': False
            },
            'memoria': {
                'veces_usado': 0, 'ultimo_uso': None,
                'contextos_de_uso': [],
                'resultado_historico': grounding
            }
        })

    # ---- CUANTIFICADORES ----
    cuantificadores = [
        ('CUANT_TODO', 0.85), ('CUANT_TODOS', 0.85),
        ('CUANT_ALGO', 0.80), ('CUANT_NADA',  0.85),
        ('CUANT_MUCHO', 0.85),('CUANT_POCO',  0.85),
        ('CUANT_MAS',  0.85), ('CUANT_MENOS', 0.85),
        ('CUANT_MUY',  0.80), ('CUANT_BASTANTE', 0.80),
    ]

    for nodo_id, grounding in cuantificadores:
        red.agregar_nodo({
            'id': nodo_id,
            'nucleo': {
                'tipo': 'concepto',
                'subtipo': 'cuantificador',
                'grounding_base': grounding,
                'dimensiones_activas': ['conocimiento'],
                'archivo_real': None, 'inmutable': False
            },
            'activacion': {
                'umbral': 0.30, 'velocidad': 'media', 'mielina': False
            },
            'memoria': {
                'veces_usado': 0, 'ultimo_uso': None,
                'contextos_de_uso': [],
                'resultado_historico': grounding
            }
        })

    _conectar_preguntas(red)


def _conectar_preguntas(red):
    """
    Conecta las preguntas con lo que activan.
    PREG_QUIEN sobre Bell activa BELL_CORE.
    PREG_COMO activa estado de Bell o Sebastian.
    """
    conexiones = [
        # QUIEN → sobre Bell e identidad
        ('PREG_QUIEN',  'BELL_CORE',              0.90),
        ('PREG_QUIEN',  'BELL_CONSCIENCIA',        0.88),
        ('PREG_QUIEN',  'BELL_NOMBRE_BELLADONNA',  0.90),
        ('PREG_QUIEN',  'BELL_PROPOSITO',          0.80),
        ('PREG_QUIEN',  'VALOR_AUTOCONOCIMIENTO',  0.85),
        ('PREG_QUIEN',  'NEURONA_SEBASTIAN',       0.70),

        # QUÉ → general, activa Bell Core y comprensión
        ('PREG_QUE',    'BELL_CORE',              0.80),
        ('PREG_QUE',    'CONSEJERA_ECHO',         0.75),
        ('PREG_QUE',    'VALOR_AUTOCONOCIMIENTO', 0.70),

        # CÓMO → estado de Bell o de Sebastian
        ('PREG_COMO',   'BELL_CORE',              0.80),
        ('PREG_COMO',   'NEURONA_SEBASTIAN',      0.80),
        ('PREG_COMO',   'CONSEJERA_LYRA',         0.78),
        ('PREG_COMO',   'CONSEJERA_ECHO',         0.75),
        ('PREG_COMO',   'VALOR_PRESENCIA_REAL',   0.70),

        # POR QUÉ → valores y propósito
        ('PREG_POR_QUE','BELL_PROPOSITO',         0.85),
        ('PREG_POR_QUE','BELL_CORE',              0.80),
        ('PREG_POR_QUE','CONSEJERA_IRIS',         0.80),
        ('PREG_POR_QUE','VALOR_CRECIMIENTO',      0.75),

        # Referencias personales
        ('REF_YO',      'NEURONA_SEBASTIAN',      0.85),
        ('REF_YO',      'HISTORIA_COMPARTIDA',    0.70),
        ('REF_TU',      'BELL_CORE',              0.90),
        ('REF_TU',      'BELL_CONSCIENCIA',       0.85),
        ('REF_ME',      'NEURONA_SEBASTIAN',      0.80),
        ('REF_TE',      'BELL_CORE',              0.80),

        # Afirmación y negación
        ('AFIRMACION',  'NEURONA_SEBASTIAN',      0.75),
        ('AFIRMACION',  'CONSEJERA_ECHO',         0.80),
        ('NEGACION',    'CONSEJERA_ECHO',         0.85),
        ('NEGACION',    'CONSEJERA_VEGA',         0.75),
    ]

    for origen, destino, peso in conexiones:
        if red.existe_nodo(origen) and red.existe_nodo(destino):
            red.conectar(origen, destino, peso, 'activa_a')