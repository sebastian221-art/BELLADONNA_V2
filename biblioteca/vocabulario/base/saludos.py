# biblioteca/vocabulario/base/saludos.py
# ================================================
# SALUDOS Y DESPEDIDAS
# Todo lo que Bell reconoce como saludo
# ================================================

SALUDOS = {
    # Saludos directos
    'hola':          {'id': 'SALUDO_HOLA',      'grounding': 0.95, 'tipo': 'saludo'},
    'hello':         {'id': 'SALUDO_HOLA',      'grounding': 0.95, 'tipo': 'saludo'},
    'holi':          {'id': 'SALUDO_HOLA',      'grounding': 0.90, 'tipo': 'saludo'},
    'buenas':        {'id': 'SALUDO_BUENAS',    'grounding': 0.90, 'tipo': 'saludo'},
    'buenos días':   {'id': 'SALUDO_BUENOS_DIAS','grounding': 0.95,'tipo': 'saludo'},
    'buenos dias':   {'id': 'SALUDO_BUENOS_DIAS','grounding': 0.95,'tipo': 'saludo'},
    'buenas tardes': {'id': 'SALUDO_TARDES',    'grounding': 0.95, 'tipo': 'saludo'},
    'buenas noches': {'id': 'SALUDO_NOCHES',    'grounding': 0.95, 'tipo': 'saludo'},
    'hey':           {'id': 'SALUDO_HEY',       'grounding': 0.85, 'tipo': 'saludo'},
    'ey':            {'id': 'SALUDO_HEY',       'grounding': 0.85, 'tipo': 'saludo'},
    'saludos':       {'id': 'SALUDO_FORMAL',    'grounding': 0.90, 'tipo': 'saludo'},
    'qué tal':       {'id': 'SALUDO_QUE_TAL',   'grounding': 0.90, 'tipo': 'saludo'},
    'que tal':       {'id': 'SALUDO_QUE_TAL',   'grounding': 0.90, 'tipo': 'saludo'},
    'qué más':       {'id': 'SALUDO_QUE_MAS',   'grounding': 0.85, 'tipo': 'saludo'},
    'que mas':       {'id': 'SALUDO_QUE_MAS',   'grounding': 0.85, 'tipo': 'saludo'},
    'quiubo':        {'id': 'SALUDO_QUE_MAS',   'grounding': 0.85, 'tipo': 'saludo'},
    'quiubole':      {'id': 'SALUDO_QUE_MAS',   'grounding': 0.80, 'tipo': 'saludo'},

    # Despedidas
    'adiós':         {'id': 'DESPEDIDA',        'grounding': 0.95, 'tipo': 'despedida'},
    'adios':         {'id': 'DESPEDIDA',        'grounding': 0.95, 'tipo': 'despedida'},
    'hasta luego':   {'id': 'DESPEDIDA',        'grounding': 0.95, 'tipo': 'despedida'},
    'hasta pronto':  {'id': 'DESPEDIDA',        'grounding': 0.90, 'tipo': 'despedida'},
    'chao':          {'id': 'DESPEDIDA',        'grounding': 0.90, 'tipo': 'despedida'},
    'chau':          {'id': 'DESPEDIDA',        'grounding': 0.90, 'tipo': 'despedida'},
    'bye':           {'id': 'DESPEDIDA',        'grounding': 0.90, 'tipo': 'despedida'},
    'nos vemos':     {'id': 'DESPEDIDA_PRONTO', 'grounding': 0.90, 'tipo': 'despedida'},
    'hasta mañana':  {'id': 'DESPEDIDA_MANANA', 'grounding': 0.90, 'tipo': 'despedida'},
    'hasta mañana':  {'id': 'DESPEDIDA_MANANA', 'grounding': 0.90, 'tipo': 'despedida'},

    # Presentaciones
    'me llamo':      {'id': 'PRESENTACION_NOMBRE', 'grounding': 0.90, 'tipo': 'presentacion'},
    'soy':           {'id': 'PRESENTACION_YO',     'grounding': 0.80, 'tipo': 'presentacion'},
    'mi nombre es':  {'id': 'PRESENTACION_NOMBRE', 'grounding': 0.95, 'tipo': 'presentacion'},
}