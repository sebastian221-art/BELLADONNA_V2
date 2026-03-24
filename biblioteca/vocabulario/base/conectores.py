# biblioteca/vocabulario/base/conectores.py
# ================================================
# CONECTORES Y PALABRAS FUNCIONALES
# Las palabras que dan estructura al lenguaje
# ================================================

CONECTORES = {
    # Conjunciones coordinantes
    'y':          {'id': 'CONJ_Y',          'grounding': 0.80, 'tipo': 'conjuncion'},
    'o':          {'id': 'CONJ_O',          'grounding': 0.80, 'tipo': 'conjuncion'},
    'pero':       {'id': 'CONJ_PERO',       'grounding': 0.85, 'tipo': 'conjuncion_adversativa'},
    'sino':       {'id': 'CONJ_SINO',       'grounding': 0.85, 'tipo': 'conjuncion_adversativa'},
    'aunque':     {'id': 'CONJ_AUNQUE',     'grounding': 0.85, 'tipo': 'conjuncion_concesiva'},
    'sin embargo':{'id': 'CONJ_SIN_EMBARGO','grounding': 0.90, 'tipo': 'conjuncion_adversativa'},

    # Preposiciones importantes
    'para':       {'id': 'PREP_PARA',       'grounding': 0.80, 'tipo': 'preposicion'},
    'por':        {'id': 'PREP_POR',        'grounding': 0.80, 'tipo': 'preposicion'},
    'con':        {'id': 'PREP_CON',        'grounding': 0.80, 'tipo': 'preposicion'},
    'sin':        {'id': 'PREP_SIN',        'grounding': 0.80, 'tipo': 'preposicion'},
    'sobre':      {'id': 'PREP_SOBRE',      'grounding': 0.80, 'tipo': 'preposicion'},
    'entre':      {'id': 'PREP_ENTRE',      'grounding': 0.80, 'tipo': 'preposicion'},
    'hasta':      {'id': 'PREP_HASTA',      'grounding': 0.80, 'tipo': 'preposicion'},
    'desde':      {'id': 'PREP_DESDE',      'grounding': 0.80, 'tipo': 'preposicion'},
    'hacia':      {'id': 'PREP_HACIA',      'grounding': 0.80, 'tipo': 'preposicion'},

    # Estructuradores del discurso
    'entonces':   {'id': 'DISC_ENTONCES',   'grounding': 0.85, 'tipo': 'estructurador'},
    'además':     {'id': 'DISC_ADEMAS',     'grounding': 0.85, 'tipo': 'estructurador'},
    'ademas':     {'id': 'DISC_ADEMAS',     'grounding': 0.80, 'tipo': 'estructurador'},
    'también':    {'id': 'DISC_TAMBIEN',    'grounding': 0.85, 'tipo': 'estructurador'},
    'tambien':    {'id': 'DISC_TAMBIEN',    'grounding': 0.80, 'tipo': 'estructurador'},
    'por eso':    {'id': 'DISC_POR_ESO',    'grounding': 0.90, 'tipo': 'causal'},
    'por lo tanto':{'id': 'DISC_POR_TANTO', 'grounding': 0.90, 'tipo': 'causal'},
    'es decir':   {'id': 'DISC_ES_DECIR',   'grounding': 0.90, 'tipo': 'aclaracion'},
    'o sea':      {'id': 'DISC_O_SEA',      'grounding': 0.90, 'tipo': 'aclaracion'},
    'osea':       {'id': 'DISC_O_SEA',      'grounding': 0.85, 'tipo': 'aclaracion'},

    # Expresiones conversacionales
    'ok':         {'id': 'EXPR_OK',         'grounding': 0.90, 'tipo': 'confirmacion'},
    'okey':       {'id': 'EXPR_OK',         'grounding': 0.90, 'tipo': 'confirmacion'},
    'dale':       {'id': 'EXPR_DALE',       'grounding': 0.85, 'tipo': 'confirmacion'},
    'listo':      {'id': 'EXPR_LISTO',      'grounding': 0.85, 'tipo': 'confirmacion'},
    'perfecto':   {'id': 'EXPR_PERFECTO',   'grounding': 0.85, 'tipo': 'confirmacion'},
    'entendido':  {'id': 'EXPR_ENTENDIDO',  'grounding': 0.90, 'tipo': 'confirmacion'},
    'de acuerdo': {'id': 'EXPR_DE_ACUERDO', 'grounding': 0.90, 'tipo': 'confirmacion'},
    'claro':      {'id': 'EXPR_CLARO',      'grounding': 0.85, 'tipo': 'confirmacion'},

    # Expresiones de incertidumbre
    'quizás':     {'id': 'EXPR_QUIZAS',     'grounding': 0.85, 'tipo': 'incertidumbre'},
    'quizas':     {'id': 'EXPR_QUIZAS',     'grounding': 0.80, 'tipo': 'incertidumbre'},
    'tal vez':    {'id': 'EXPR_TAL_VEZ',    'grounding': 0.85, 'tipo': 'incertidumbre'},
    'a lo mejor': {'id': 'EXPR_A_LO_MEJOR', 'grounding': 0.85, 'tipo': 'incertidumbre'},
    'creo que':   {'id': 'EXPR_CREO_QUE',   'grounding': 0.85, 'tipo': 'incertidumbre'},
    'no sé':      {'id': 'EXPR_NO_SE',      'grounding': 0.90, 'tipo': 'desconocimiento'},
    'no se':      {'id': 'EXPR_NO_SE',      'grounding': 0.85, 'tipo': 'desconocimiento'},
}