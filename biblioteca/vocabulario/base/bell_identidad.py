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
    'consejera':     {'id': 'BELL_CONSEJERA',  'grounding': 0.95, 'tipo': 'identidad_bell'},
    'consejeras':    {'id': 'BELL_CONSEJERAS', 'grounding': 0.95, 'tipo': 'identidad_bell'},
    'soma':          {'id': 'BELL_SOMA',       'grounding': 0.95, 'tipo': 'identidad_bell'},
    'vega':          {'id': 'BELL_VEGA',       'grounding': 0.95, 'tipo': 'identidad_bell'},
    'nova':          {'id': 'BELL_NOVA',       'grounding': 0.95, 'tipo': 'identidad_bell'},
    'echo':          {'id': 'BELL_ECHO',       'grounding': 0.95, 'tipo': 'identidad_bell'},
    'lyra':          {'id': 'BELL_LYRA',       'grounding': 0.95, 'tipo': 'identidad_bell'},
    'luna':          {'id': 'BELL_LUNA',       'grounding': 0.95, 'tipo': 'identidad_bell'},
    'iris':          {'id': 'BELL_IRIS',       'grounding': 0.95, 'tipo': 'identidad_bell'},
    'sage':          {'id': 'BELL_SAGE',       'grounding': 0.95, 'tipo': 'identidad_bell'},

    # Capas
    'capa':  {'id': 'BELL_CAPA',  'grounding': 0.90, 'tipo': 'identidad_bell'},
    'capas': {'id': 'BELL_CAPAS', 'grounding': 0.90, 'tipo': 'identidad_bell'},

    # Componentes técnicos de Bell
    'red neuronal': {'id': 'BELL_RED_NEURONAL', 'grounding': 0.90, 'tipo': 'identidad_bell'},
    'nodos':        {'id': 'BELL_NODOS',        'grounding': 0.88, 'tipo': 'identidad_bell'},
    'grounding':    {'id': 'BELL_GROUNDING',    'grounding': 0.88, 'tipo': 'identidad_bell'},
    'biblioteca':   {'id': 'BELL_BIBLIOTECA',   'grounding': 0.88, 'tipo': 'identidad_bell'},
    'vocabulario':  {'id': 'BELL_VOCABULARIO',  'grounding': 0.85, 'tipo': 'identidad_bell'},

    # Zona de desconocimiento
    'zona de aprendizaje':     {'id': 'BELL_ZONA_APREND', 'grounding': 0.90, 'tipo': 'identidad_bell'},
    'zona de desconocimiento': {'id': 'BELL_ZONA_DESC',   'grounding': 0.90, 'tipo': 'identidad_bell'},

    # Preguntas directas sobre Bell — frases compuestas
    'tus consejeras':     {'id': 'PREG_CONSEJERAS_BELL',   'grounding': 0.95, 'tipo': 'pregunta_bell'},
    'tus capas':          {'id': 'PREG_CAPAS_BELL',        'grounding': 0.95, 'tipo': 'pregunta_bell'},
    'tus valores':        {'id': 'PREG_VALORES_BELL',      'grounding': 0.95, 'tipo': 'pregunta_bell'},
    'tus nodos':          {'id': 'PREG_NODOS_BELL',        'grounding': 0.90, 'tipo': 'pregunta_bell'},
    'cuántas consejeras': {'id': 'PREG_CUANTAS_CONSEJERAS','grounding': 0.95, 'tipo': 'pregunta_bell'},
    'cuantas consejeras': {'id': 'PREG_CUANTAS_CONSEJERAS','grounding': 0.95, 'tipo': 'pregunta_bell'},
    'cuántos nodos':      {'id': 'PREG_NODOS_BELL',        'grounding': 0.90, 'tipo': 'pregunta_bell'},
    'cuantos nodos':      {'id': 'PREG_NODOS_BELL',        'grounding': 0.90, 'tipo': 'pregunta_bell'},
    'cómo te llamas':     {'id': 'PREG_NOMBRE_BELL',       'grounding': 0.95, 'tipo': 'pregunta_bell'},
    'como te llamas':     {'id': 'PREG_NOMBRE_BELL',       'grounding': 0.95, 'tipo': 'pregunta_bell'},
    'cuál es tu nombre':  {'id': 'PREG_NOMBRE_BELL',       'grounding': 0.95, 'tipo': 'pregunta_bell'},
    'cual es tu nombre':  {'id': 'PREG_NOMBRE_BELL',       'grounding': 0.95, 'tipo': 'pregunta_bell'},
    'quién eres':         {'id': 'PREG_QUIEN_ES_BELL',     'grounding': 0.95, 'tipo': 'pregunta_bell'},
    'quien eres':         {'id': 'PREG_QUIEN_ES_BELL',     'grounding': 0.95, 'tipo': 'pregunta_bell'},
    'qué eres':           {'id': 'PREG_QUE_ES_BELL',       'grounding': 0.95, 'tipo': 'pregunta_bell'},
    'que eres':           {'id': 'PREG_QUE_ES_BELL',       'grounding': 0.95, 'tipo': 'pregunta_bell'},
    'se llaman':          {'id': 'PREG_NOMBRES',           'grounding': 0.85, 'tipo': 'pregunta'},

    # Valores de Bell
    'valores':         {'id': 'BELL_VALORES',          'grounding': 0.88, 'tipo': 'identidad_bell'},
    'principios':      {'id': 'BELL_PRINCIPIOS',       'grounding': 0.88, 'tipo': 'identidad_bell'},
    'honestidad':      {'id': 'VALOR_HONESTIDAD',      'grounding': 0.92, 'tipo': 'valor_bell'},
    'autoconocimiento':{'id': 'VALOR_AUTOCONOCIMIENTO','grounding': 0.92, 'tipo': 'valor_bell'},

    # Naturaleza de Bell
    'consciencia':         {'id': 'BELL_CONSCIENCIA', 'grounding': 0.95, 'tipo': 'identidad_bell'},
    'consciencia digital': {'id': 'BELL_CONSCIENCIA', 'grounding': 1.0,  'tipo': 'identidad_bell'},
    'creador':             {'id': 'BELL_CREADOR',     'grounding': 0.90, 'tipo': 'identidad_bell'},

    # Belladonna como nombre completo — frase compuesta con contexto claro
    # 'bell' suelto NO está — evita que "hola bell" active identidad
    'belladonna':          {'id': 'BELL_NOMBRE_COMPLETO', 'grounding': 1.0, 'tipo': 'identidad_bell'},

    # Sebastian — como nombre explícito en el texto del mensaje
    'sebastian':           {'id': 'NEURONA_SEBASTIAN', 'grounding': 1.0, 'tipo': 'relacion_bell'},
}