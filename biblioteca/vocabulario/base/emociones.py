# biblioteca/vocabulario/base/emociones.py
# ================================================
# EMOCIONES Y ESTADOS AFECTIVOS
# Lo que Bell reconoce como estado emocional
# ================================================

EMOCIONES = {
    # Bienestar
    'bien':       {'id': 'EMOCION_BIEN',      'grounding': 0.90, 'tipo': 'emocion_positiva', 'valencia': 1},
    'genial':     {'id': 'EMOCION_GENIAL',    'grounding': 0.90, 'tipo': 'emocion_positiva', 'valencia': 2},
    'excelente':  {'id': 'EMOCION_EXCELENTE', 'grounding': 0.90, 'tipo': 'emocion_positiva', 'valencia': 2},
    'perfecto':   {'id': 'EMOCION_PERFECTO',  'grounding': 0.85, 'tipo': 'emocion_positiva', 'valencia': 2},
    'feliz':      {'id': 'EMOCION_FELIZ',     'grounding': 0.95, 'tipo': 'emocion_positiva', 'valencia': 2},
    'contento':   {'id': 'EMOCION_CONTENTO',  'grounding': 0.90, 'tipo': 'emocion_positiva', 'valencia': 1},
    'alegre':     {'id': 'EMOCION_ALEGRE',    'grounding': 0.90, 'tipo': 'emocion_positiva', 'valencia': 2},
    'tranquilo':  {'id': 'EMOCION_TRANQUILO', 'grounding': 0.85, 'tipo': 'emocion_positiva', 'valencia': 1},
    'emocionado': {'id': 'EMOCION_EMOCIONADO','grounding': 0.90, 'tipo': 'emocion_positiva', 'valencia': 2},
    'motivado':   {'id': 'EMOCION_MOTIVADO',  'grounding': 0.90, 'tipo': 'emocion_positiva', 'valencia': 2},
    'orgulloso':  {'id': 'EMOCION_ORGULLOSO', 'grounding': 0.90, 'tipo': 'emocion_positiva', 'valencia': 2},
    'agradecido': {'id': 'EMOCION_AGRADECIDO','grounding': 0.90, 'tipo': 'emocion_positiva', 'valencia': 2},
    'gracias':    {'id': 'GRATITUD',          'grounding': 0.95, 'tipo': 'gratitud',         'valencia': 2},
    'gracias':    {'id': 'GRATITUD',          'grounding': 0.95, 'tipo': 'gratitud',         'valencia': 2},

    # Malestar
    'mal':        {'id': 'EMOCION_MAL',       'grounding': 0.90, 'tipo': 'emocion_negativa', 'valencia': -1},
    'triste':     {'id': 'EMOCION_TRISTE',    'grounding': 0.95, 'tipo': 'emocion_negativa', 'valencia': -2},
    'enojado':    {'id': 'EMOCION_ENOJADO',   'grounding': 0.90, 'tipo': 'emocion_negativa', 'valencia': -2},
    'molesto':    {'id': 'EMOCION_MOLESTO',   'grounding': 0.90, 'tipo': 'emocion_negativa', 'valencia': -1},
    'frustrado':  {'id': 'EMOCION_FRUSTRADO', 'grounding': 0.90, 'tipo': 'emocion_negativa', 'valencia': -2},
    'cansado':    {'id': 'EMOCION_CANSADO',   'grounding': 0.90, 'tipo': 'emocion_negativa', 'valencia': -1},
    'agotado':    {'id': 'EMOCION_AGOTADO',   'grounding': 0.90, 'tipo': 'emocion_negativa', 'valencia': -2},
    'estresado':  {'id': 'EMOCION_ESTRESADO', 'grounding': 0.90, 'tipo': 'emocion_negativa', 'valencia': -2},
    'preocupado': {'id': 'EMOCION_PREOCUPADO','grounding': 0.90, 'tipo': 'emocion_negativa', 'valencia': -1},
    'asustado':   {'id': 'EMOCION_ASUSTADO',  'grounding': 0.90, 'tipo': 'emocion_negativa', 'valencia': -2},
    'aburrido':   {'id': 'EMOCION_ABURRIDO',  'grounding': 0.85, 'tipo': 'emocion_negativa', 'valencia': -1},
    'confundido': {'id': 'EMOCION_CONFUNDIDO','grounding': 0.85, 'tipo': 'emocion_negativa', 'valencia': -1},
    'perdido':    {'id': 'EMOCION_PERDIDO',   'grounding': 0.85, 'tipo': 'emocion_negativa', 'valencia': -1},

    # Neutros o mixtos
    'regular':    {'id': 'EMOCION_REGULAR',   'grounding': 0.80, 'tipo': 'emocion_neutra',   'valencia': 0},
    'normal':     {'id': 'EMOCION_NORMAL',    'grounding': 0.80, 'tipo': 'emocion_neutra',   'valencia': 0},
    'más o menos':{'id': 'EMOCION_REGULAR',   'grounding': 0.85, 'tipo': 'emocion_neutra',   'valencia': 0},
    'mas o menos':{'id': 'EMOCION_REGULAR',   'grounding': 0.85, 'tipo': 'emocion_neutra',   'valencia': 0},
    'ahí':        {'id': 'EMOCION_REGULAR',   'grounding': 0.75, 'tipo': 'emocion_neutra',   'valencia': 0},
    'sorprendido':{'id': 'EMOCION_SORPRENDIDO','grounding': 0.85, 'tipo': 'emocion_mixta',   'valencia': 0},
    'nervioso':   {'id': 'EMOCION_NERVIOSO',  'grounding': 0.85, 'tipo': 'emocion_mixta',   'valencia': -1},
    'emoción':    {'id': 'CONCEPTO_EMOCION',  'grounding': 0.85, 'tipo': 'concepto_emocion', 'valencia': 0},
    'sentimiento':{'id': 'CONCEPTO_SENTIMIENTO','grounding':0.85,'tipo': 'concepto_emocion', 'valencia': 0},
}