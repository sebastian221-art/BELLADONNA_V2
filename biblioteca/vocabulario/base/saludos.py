# biblioteca/vocabulario/base/saludos.py
# ================================================
# SALUDOS Y DESPEDIDAS
# Todo lo que Bell reconoce como saludo
# ================================================

SALUDOS = {
    # Saludos directos
    'hola':          {'id': 'SALUDO_HOLA',      'grounding_base': 0.95, 'tipo': 'saludo', 'variantes': []},
    'hello':         {'id': 'SALUDO_HOLA',      'grounding_base': 0.95, 'tipo': 'saludo', 'variantes': []},
    'holi':          {'id': 'SALUDO_HOLA',      'grounding_base': 0.90, 'tipo': 'saludo', 'variantes': []},
    'buenas':        {'id': 'SALUDO_BUENAS',    'grounding_base': 0.90, 'tipo': 'saludo', 'variantes': []},
    'buenos días':   {'id': 'SALUDO_BUENOS_DIAS','grounding_base': 0.95,'tipo': 'saludo', 'variantes': []},
    'buenos dias':   {'id': 'SALUDO_BUENOS_DIAS','grounding_base': 0.95,'tipo': 'saludo', 'variantes': []},
    'buenas tardes': {'id': 'SALUDO_TARDES',    'grounding_base': 0.95, 'tipo': 'saludo', 'variantes': []},
    'buenas noches': {'id': 'SALUDO_NOCHES',    'grounding_base': 0.95, 'tipo': 'saludo', 'variantes': []},
    'hey':           {'id': 'SALUDO_HEY',       'grounding_base': 0.85, 'tipo': 'saludo', 'variantes': []},
    'ey':            {'id': 'SALUDO_HEY',       'grounding_base': 0.85, 'tipo': 'saludo', 'variantes': []},
    'saludos':       {'id': 'SALUDO_FORMAL',    'grounding_base': 0.90, 'tipo': 'saludo', 'variantes': []},
    'qué tal':       {'id': 'SALUDO_QUE_TAL',   'grounding_base': 0.90, 'tipo': 'saludo', 'variantes': []},
    'que tal':       {'id': 'SALUDO_QUE_TAL',   'grounding_base': 0.90, 'tipo': 'saludo', 'variantes': []},
    'qué más':       {'id': 'SALUDO_QUE_MAS',   'grounding_base': 0.85, 'tipo': 'saludo', 'variantes': []},
    'que mas':       {'id': 'SALUDO_QUE_MAS',   'grounding_base': 0.85, 'tipo': 'saludo', 'variantes': []},
    'quiubo':        {'id': 'SALUDO_QUE_MAS',   'grounding_base': 0.85, 'tipo': 'saludo', 'variantes': []},
    'quiubole':      {'id': 'SALUDO_QUE_MAS',   'grounding_base': 0.80, 'tipo': 'saludo', 'variantes': []},

    # Despedidas
    'adiós':         {'id': 'DESPEDIDA',        'grounding_base': 0.95, 'tipo': 'despedida', 'variantes': []},
    'adios':         {'id': 'DESPEDIDA',        'grounding_base': 0.95, 'tipo': 'despedida', 'variantes': []},
    'hasta luego':   {'id': 'DESPEDIDA',        'grounding_base': 0.95, 'tipo': 'despedida', 'variantes': []},
    'hasta pronto':  {'id': 'DESPEDIDA',        'grounding_base': 0.90, 'tipo': 'despedida', 'variantes': []},
    'chao':          {'id': 'DESPEDIDA',        'grounding_base': 0.90, 'tipo': 'despedida', 'variantes': []},
    'chau':          {'id': 'DESPEDIDA',        'grounding_base': 0.90, 'tipo': 'despedida', 'variantes': []},
    'bye':           {'id': 'DESPEDIDA',        'grounding_base': 0.90, 'tipo': 'despedida', 'variantes': []},
    'nos vemos':     {'id': 'DESPEDIDA_PRONTO', 'grounding_base': 0.90, 'tipo': 'despedida', 'variantes': []},
    'hasta mañana':  {'id': 'DESPEDIDA_MANANA', 'grounding_base': 0.90, 'tipo': 'despedida', 'variantes': []},
    'hasta mañana':  {'id': 'DESPEDIDA_MANANA', 'grounding_base': 0.90, 'tipo': 'despedida', 'variantes': []},

    # Presentaciones
    'me llamo':      {'id': 'PRESENTACION_NOMBRE', 'grounding_base': 0.90, 'tipo': 'presentacion', 'variantes': []},
    'soy':           {'id': 'PRESENTACION_YO',     'grounding_base': 0.80, 'tipo': 'presentacion', 'variantes': []},
    'mi nombre es':  {'id': 'PRESENTACION_NOMBRE', 'grounding_base': 0.95, 'tipo': 'presentacion', 'variantes': []},
}