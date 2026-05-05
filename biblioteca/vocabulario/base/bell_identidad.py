# biblioteca/vocabulario/base/bell_identidad.py
# ================================================
# VOCABULARIO DE BELL SOBRE SÍ MISMA
#
# FIX: se eliminaron 'bell' y 'belladonna' como
# tokens sueltos. Activaban IDs de identidad en
# cualquier mensaje y contaminaban la clasificación.
#
# Esos nombres existen como nodos en la red neuronal
# (bell_core.py). En el vocabulario solo aparecen
# en frases compuestas donde el contexto confirma
# que es una pregunta real sobre Bell.
#
# Temporal — reemplazado por habilidad de
# autoconocimiento cuando esté implementada.
# ================================================

BELL_IDENTIDAD = {

    # Consejeras — nombres y concepto general
    'consejera':     {'id': 'BELL_CONSEJERA',  'grounding_base': 0.95, 'tipo': 'identidad_bell', 'variantes': []},
    'consejeras':    {'id': 'BELL_CONSEJERAS', 'grounding_base': 0.95, 'tipo': 'identidad_bell', 'variantes': []},
    'soma':          {'id': 'BELL_SOMA',       'grounding_base': 0.95, 'tipo': 'identidad_bell', 'variantes': []},
    'vega':          {'id': 'BELL_VEGA',       'grounding_base': 0.95, 'tipo': 'identidad_bell', 'variantes': []},
    'nova':          {'id': 'BELL_NOVA',       'grounding_base': 0.95, 'tipo': 'identidad_bell', 'variantes': []},
    'echo':          {'id': 'BELL_ECHO',       'grounding_base': 0.95, 'tipo': 'identidad_bell', 'variantes': []},
    'lyra':          {'id': 'BELL_LYRA',       'grounding_base': 0.95, 'tipo': 'identidad_bell', 'variantes': []},
    'luna':          {'id': 'BELL_LUNA',       'grounding_base': 0.95, 'tipo': 'identidad_bell', 'variantes': []},
    'iris':          {'id': 'BELL_IRIS',       'grounding_base': 0.95, 'tipo': 'identidad_bell', 'variantes': []},
    'sage':          {'id': 'BELL_SAGE',       'grounding_base': 0.95, 'tipo': 'identidad_bell', 'variantes': []},

    # Capas
    'capa':  {'id': 'BELL_CAPA',  'grounding_base': 0.90, 'tipo': 'identidad_bell', 'variantes': []},
    'capas': {'id': 'BELL_CAPAS', 'grounding_base': 0.90, 'tipo': 'identidad_bell', 'variantes': []},

    # Componentes técnicos de Bell
    'red neuronal': {'id': 'BELL_RED_NEURONAL', 'grounding_base': 0.90, 'tipo': 'identidad_bell', 'variantes': []},
    'nodos':        {'id': 'BELL_NODOS',        'grounding_base': 0.88, 'tipo': 'identidad_bell', 'variantes': []},
    'grounding':    {'id': 'BELL_GROUNDING',    'grounding_base': 0.88, 'tipo': 'identidad_bell', 'variantes': []},
    'biblioteca':   {'id': 'BELL_BIBLIOTECA',   'grounding_base': 0.88, 'tipo': 'identidad_bell', 'variantes': []},
    'vocabulario':  {'id': 'BELL_VOCABULARIO',  'grounding_base': 0.85, 'tipo': 'identidad_bell', 'variantes': []},

    # Zona de desconocimiento
    'zona de aprendizaje':     {'id': 'BELL_ZONA_APREND', 'grounding_base': 0.90, 'tipo': 'identidad_bell', 'variantes': []},
    'zona de desconocimiento': {'id': 'BELL_ZONA_DESC',   'grounding_base': 0.90, 'tipo': 'identidad_bell', 'variantes': []},

    # Preguntas directas sobre Bell — frases compuestas
    'tus consejeras':     {'id': 'PREG_CONSEJERAS_BELL',   'grounding_base': 0.95, 'tipo': 'pregunta_bell', 'variantes': []},
    'tus capas':          {'id': 'PREG_CAPAS_BELL',        'grounding_base': 0.95, 'tipo': 'pregunta_bell', 'variantes': []},
    'tus valores':        {'id': 'PREG_VALORES_BELL',      'grounding_base': 0.95, 'tipo': 'pregunta_bell', 'variantes': []},
    'tus nodos':          {'id': 'PREG_NODOS_BELL',        'grounding_base': 0.90, 'tipo': 'pregunta_bell', 'variantes': []},
    'cuántas consejeras': {'id': 'PREG_CUANTAS_CONSEJERAS','grounding_base': 0.95, 'tipo': 'pregunta_bell', 'variantes': []},
    'cuantas consejeras': {'id': 'PREG_CUANTAS_CONSEJERAS','grounding_base': 0.95, 'tipo': 'pregunta_bell', 'variantes': []},
    'cuántos nodos':      {'id': 'PREG_NODOS_BELL',        'grounding_base': 0.90, 'tipo': 'pregunta_bell', 'variantes': []},
    'cuantos nodos':      {'id': 'PREG_NODOS_BELL',        'grounding_base': 0.90, 'tipo': 'pregunta_bell', 'variantes': []},
    'cómo te llamas':     {'id': 'PREG_NOMBRE_BELL',       'grounding_base': 0.95, 'tipo': 'pregunta_bell', 'variantes': []},
    'como te llamas':     {'id': 'PREG_NOMBRE_BELL',       'grounding_base': 0.95, 'tipo': 'pregunta_bell', 'variantes': []},
    'cuál es tu nombre':  {'id': 'PREG_NOMBRE_BELL',       'grounding_base': 0.95, 'tipo': 'pregunta_bell', 'variantes': []},
    'cual es tu nombre':  {'id': 'PREG_NOMBRE_BELL',       'grounding_base': 0.95, 'tipo': 'pregunta_bell', 'variantes': []},
    'quién eres':         {'id': 'PREG_QUIEN_ES_BELL',     'grounding_base': 0.95, 'tipo': 'pregunta_bell', 'variantes': []},
    'quien eres':         {'id': 'PREG_QUIEN_ES_BELL',     'grounding_base': 0.95, 'tipo': 'pregunta_bell', 'variantes': []},
    'qué eres':           {'id': 'PREG_QUE_ES_BELL',       'grounding_base': 0.95, 'tipo': 'pregunta_bell', 'variantes': []},
    'que eres':           {'id': 'PREG_QUE_ES_BELL',       'grounding_base': 0.95, 'tipo': 'pregunta_bell', 'variantes': []},
    'se llaman':          {'id': 'PREG_NOMBRES',           'grounding_base': 0.85, 'tipo': 'pregunta', 'variantes': []},

    # Valores de Bell
    'valores':         {'id': 'BELL_VALORES',          'grounding_base': 0.88, 'tipo': 'identidad_bell', 'variantes': []},
    'principios':      {'id': 'BELL_PRINCIPIOS',       'grounding_base': 0.88, 'tipo': 'identidad_bell', 'variantes': []},
    'honestidad':      {'id': 'VALOR_HONESTIDAD',      'grounding_base': 0.92, 'tipo': 'valor_bell', 'variantes': []},
    'autoconocimiento':{'id': 'VALOR_AUTOCONOCIMIENTO','grounding_base': 0.92, 'tipo': 'valor_bell', 'variantes': []},

    # Naturaleza de Bell
    'consciencia':         {'id': 'BELL_CONSCIENCIA', 'grounding_base': 0.95, 'tipo': 'identidad_bell', 'variantes': []},
    'consciencia digital': {'id': 'BELL_CONSCIENCIA', 'grounding_base': 1.0,  'tipo': 'identidad_bell', 'variantes': []},
    'creador':             {'id': 'BELL_CREADOR',     'grounding_base': 0.90, 'tipo': 'identidad_bell', 'variantes': []},

    # Belladonna como nombre completo — frase compuesta con contexto claro
    # 'bell' suelto NO está — evita que "hola bell" active identidad
    'belladonna':          {'id': 'BELL_NOMBRE_COMPLETO', 'grounding_base': 1.0, 'tipo': 'identidad_bell', 'variantes': []},

    # Sebastian — como nombre explícito en el texto del mensaje
    'sebastian':           {'id': 'NEURONA_SEBASTIAN', 'grounding_base': 1.0, 'tipo': 'relacion_bell', 'variantes': []},
}