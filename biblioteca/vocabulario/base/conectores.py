# biblioteca/vocabulario/base/conectores.py
# ================================================
# CONECTORES Y PALABRAS FUNCIONALES
# Las palabras que dan estructura al lenguaje
# ================================================

CONECTORES = {
    # Conjunciones coordinantes
    'y':          {'id': 'CONJ_Y',          'grounding_base': 0.80, 'tipo': 'conjuncion', 'variantes': []},
    'o':          {'id': 'CONJ_O',          'grounding_base': 0.80, 'tipo': 'conjuncion', 'variantes': []},
    'pero':       {'id': 'CONJ_PERO',       'grounding_base': 0.85, 'tipo': 'conjuncion_adversativa', 'variantes': []},
    'sino':       {'id': 'CONJ_SINO',       'grounding_base': 0.85, 'tipo': 'conjuncion_adversativa', 'variantes': []},
    'aunque':     {'id': 'CONJ_AUNQUE',     'grounding_base': 0.85, 'tipo': 'conjuncion_concesiva', 'variantes': []},
    'sin embargo':{'id': 'CONJ_SIN_EMBARGO','grounding_base': 0.90, 'tipo': 'conjuncion_adversativa', 'variantes': []},

    # Preposiciones importantes
    'para':       {'id': 'PREP_PARA',       'grounding_base': 0.80, 'tipo': 'preposicion', 'variantes': []},
    'por':        {'id': 'PREP_POR',        'grounding_base': 0.80, 'tipo': 'preposicion', 'variantes': []},
    'con':        {'id': 'PREP_CON',        'grounding_base': 0.80, 'tipo': 'preposicion', 'variantes': []},
    'sin':        {'id': 'PREP_SIN',        'grounding_base': 0.80, 'tipo': 'preposicion', 'variantes': []},
    'sobre':      {'id': 'PREP_SOBRE',      'grounding_base': 0.80, 'tipo': 'preposicion', 'variantes': []},
    'entre':      {'id': 'PREP_ENTRE',      'grounding_base': 0.80, 'tipo': 'preposicion', 'variantes': []},
    'hasta':      {'id': 'PREP_HASTA',      'grounding_base': 0.80, 'tipo': 'preposicion', 'variantes': []},
    'desde':      {'id': 'PREP_DESDE',      'grounding_base': 0.80, 'tipo': 'preposicion', 'variantes': []},
    'hacia':      {'id': 'PREP_HACIA',      'grounding_base': 0.80, 'tipo': 'preposicion', 'variantes': []},

    # Estructuradores del discurso
    'entonces':   {'id': 'DISC_ENTONCES',   'grounding_base': 0.85, 'tipo': 'estructurador', 'variantes': []},
    'además':     {'id': 'DISC_ADEMAS',     'grounding_base': 0.85, 'tipo': 'estructurador', 'variantes': []},
    'ademas':     {'id': 'DISC_ADEMAS',     'grounding_base': 0.80, 'tipo': 'estructurador', 'variantes': []},
    'también':    {'id': 'DISC_TAMBIEN',    'grounding_base': 0.85, 'tipo': 'estructurador', 'variantes': []},
    'tambien':    {'id': 'DISC_TAMBIEN',    'grounding_base': 0.80, 'tipo': 'estructurador', 'variantes': []},
    'por eso':    {'id': 'DISC_POR_ESO',    'grounding_base': 0.90, 'tipo': 'causal', 'variantes': []},
    'por lo tanto':{'id': 'DISC_POR_TANTO', 'grounding_base': 0.90, 'tipo': 'causal', 'variantes': []},
    'es decir':   {'id': 'DISC_ES_DECIR',   'grounding_base': 0.90, 'tipo': 'aclaracion', 'variantes': []},
    'o sea':      {'id': 'DISC_O_SEA',      'grounding_base': 0.90, 'tipo': 'aclaracion', 'variantes': []},
    'osea':       {'id': 'DISC_O_SEA',      'grounding_base': 0.85, 'tipo': 'aclaracion', 'variantes': []},

    # Expresiones conversacionales
    'ok':         {'id': 'EXPR_OK',         'grounding_base': 0.90, 'tipo': 'confirmacion', 'variantes': []},
    'okey':       {'id': 'EXPR_OK',         'grounding_base': 0.90, 'tipo': 'confirmacion', 'variantes': []},
    'dale':       {'id': 'EXPR_DALE',       'grounding_base': 0.85, 'tipo': 'confirmacion', 'variantes': []},
    'listo':      {'id': 'EXPR_LISTO',      'grounding_base': 0.85, 'tipo': 'confirmacion', 'variantes': []},
    'perfecto':   {'id': 'EXPR_PERFECTO',   'grounding_base': 0.85, 'tipo': 'confirmacion', 'variantes': []},
    'entendido':  {'id': 'EXPR_ENTENDIDO',  'grounding_base': 0.90, 'tipo': 'confirmacion', 'variantes': []},
    'de acuerdo': {'id': 'EXPR_DE_ACUERDO', 'grounding_base': 0.90, 'tipo': 'confirmacion', 'variantes': []},
    'claro':      {'id': 'EXPR_CLARO',      'grounding_base': 0.85, 'tipo': 'confirmacion', 'variantes': []},

    # Expresiones de incertidumbre
    'quizás':     {'id': 'EXPR_QUIZAS',     'grounding_base': 0.85, 'tipo': 'incertidumbre', 'variantes': []},
    'quizas':     {'id': 'EXPR_QUIZAS',     'grounding_base': 0.80, 'tipo': 'incertidumbre', 'variantes': []},
    'tal vez':    {'id': 'EXPR_TAL_VEZ',    'grounding_base': 0.85, 'tipo': 'incertidumbre', 'variantes': []},
    'a lo mejor': {'id': 'EXPR_A_LO_MEJOR', 'grounding_base': 0.85, 'tipo': 'incertidumbre', 'variantes': []},
    'creo que':   {'id': 'EXPR_CREO_QUE',   'grounding_base': 0.85, 'tipo': 'incertidumbre', 'variantes': []},
    'no sé':      {'id': 'EXPR_NO_SE',      'grounding_base': 0.90, 'tipo': 'desconocimiento', 'variantes': []},
    'no se':      {'id': 'EXPR_NO_SE',      'grounding_base': 0.85, 'tipo': 'desconocimiento', 'variantes': []},
}