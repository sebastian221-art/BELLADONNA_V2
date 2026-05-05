# biblioteca/vocabulario/base/emociones.py
# ================================================
# EMOCIONES — Expandida (35 → 100+ entradas)
# ================================================

EMOCIONES = {
    # Bienestar positivo
    'bien':          {'id': 'EMOCION_BIEN',      'tipo': 'emocion_positiva', 'grounding_base': 0.90, 'variantes': ['me siento bien', 'estoy bien'], 'valencia': 1},
    'genial':        {'id': 'EMOCION_GENIAL',    'tipo': 'emocion_positiva', 'grounding_base': 0.90, 'variantes': ['genial parce', 'qué genial'], 'valencia': 2},
    'excelente':     {'id': 'EMOCION_EXCELENTE', 'tipo': 'emocion_positiva', 'grounding_base': 0.90, 'variantes': ['excelente día', 'excelente trabajo'], 'valencia': 2},
    'perfecto':      {'id': 'EMOCION_PERFECTO',  'tipo': 'emocion_positiva', 'grounding_base': 0.85, 'variantes': ['perfecto gracias', 'quedó perfecto'], 'valencia': 2},
    'feliz':         {'id': 'EMOCION_FELIZ',     'tipo': 'emocion_positiva', 'grounding_base': 0.95, 'variantes': ['felicísimo', 'muy feliz', 'soy feliz'], 'valencia': 2},
    'contento':      {'id': 'EMOCION_CONTENTO',  'tipo': 'emocion_positiva', 'grounding_base': 0.90, 'variantes': ['contenta', 'muy contento'], 'valencia': 1},
    'alegre':        {'id': 'EMOCION_ALEGRE',    'tipo': 'emocion_positiva', 'grounding_base': 0.90, 'variantes': ['alegría', 'con alegría'], 'valencia': 2},
    'tranquilo':     {'id': 'EMOCION_TRANQUILO', 'tipo': 'emocion_positiva', 'grounding_base': 0.85, 'variantes': ['tranquila', 'tranquilos', 'más tranquilo'], 'valencia': 1},
    'emocionado':    {'id': 'EMOCION_EMOCIONADO','tipo': 'emocion_positiva', 'grounding_base': 0.90, 'variantes': ['emocionada', 'súper emocionado'], 'valencia': 2},
    'motivado':      {'id': 'EMOCION_MOTIVADO',  'tipo': 'emocion_positiva', 'grounding_base': 0.90, 'variantes': ['motivada', 'con motivación'], 'valencia': 2},
    'orgulloso':     {'id': 'EMOCION_ORGULLOSO', 'tipo': 'emocion_positiva', 'grounding_base': 0.90, 'variantes': ['orgullosa', 'muy orgulloso', 'estoy orgulloso'], 'valencia': 2},
    'agradecido':    {'id': 'EMOCION_AGRADECIDO','tipo': 'emocion_positiva', 'grounding_base': 0.90, 'variantes': ['agradecida', 'muy agradecido'], 'valencia': 2},
    'gracias':       {'id': 'GRATITUD',          'tipo': 'gratitud',         'grounding_base': 0.95, 'variantes': ['muchas gracias', 'gracias por todo', 'te lo agradezco'], 'valencia': 2},
    'esperanza':     {'id': 'EMOCION_ESPERANZA', 'tipo': 'emocion_positiva', 'grounding_base': 0.90, 'variantes': ['tengo esperanza', 'con esperanza', 'espero que'], 'valencia': 1},
    'ilusión':       {'id': 'EMOCION_ILUSION',   'tipo': 'emocion_positiva', 'grounding_base': 0.88, 'variantes': ['ilusion', 'ilusionado', 'ilusionada'], 'valencia': 2},
    'entusiasmado':  {'id': 'EMOCION_ENTUS',     'tipo': 'emocion_positiva', 'grounding_base': 0.88, 'variantes': ['entusiasmada', 'con entusiasmo'], 'valencia': 2},
    'satisfecho':    {'id': 'EMOCION_SATISF',    'tipo': 'emocion_positiva', 'grounding_base': 0.88, 'variantes': ['satisfecha', 'satisfacción'], 'valencia': 1},
    'enamorado':     {'id': 'EMOCION_ENAMORADO', 'tipo': 'emocion_relacional','grounding_base': 0.90,'variantes': ['enamorada', 'me enamoré', 'estar enamorado'], 'valencia': 2},

    # Malestar
    'mal':           {'id': 'EMOCION_MAL',       'tipo': 'emocion_negativa', 'grounding_base': 0.90, 'variantes': ['me siento mal', 'estoy mal', 'todo mal'], 'valencia': -1},
    'triste':        {'id': 'EMOCION_TRISTE',    'tipo': 'emocion_negativa', 'grounding_base': 0.95, 'variantes': ['tristeza', 'muy triste', 'me puse triste'], 'valencia': -2},
    'enojado':       {'id': 'EMOCION_ENOJADO',   'tipo': 'emocion_negativa', 'grounding_base': 0.90, 'variantes': ['enojada', 'estoy enojado', 'furioso'], 'valencia': -2},
    'molesto':       {'id': 'EMOCION_MOLESTO',   'tipo': 'emocion_negativa', 'grounding_base': 0.90, 'variantes': ['molesta', 'me molesta', 'estoy molesto'], 'valencia': -1},
    'frustrado':     {'id': 'EMOCION_FRUSTRADO', 'tipo': 'emocion_negativa', 'grounding_base': 0.90, 'variantes': ['frustrada', 'frustración', 'frustrado con el código'], 'valencia': -2},
    'cansado':       {'id': 'EMOCION_CANSADO',   'tipo': 'emocion_negativa', 'grounding_base': 0.90, 'variantes': ['cansada', 'muy cansado', 'rendido'], 'valencia': -1},
    'agotado':       {'id': 'EMOCION_AGOTADO',   'tipo': 'emocion_negativa', 'grounding_base': 0.90, 'variantes': ['agotada', 'completamente agotado'], 'valencia': -2},
    'estresado':     {'id': 'EMOCION_ESTRESADO', 'tipo': 'emocion_negativa', 'grounding_base': 0.90, 'variantes': ['estresada', 'estrés', 'al tope'], 'valencia': -2},
    'preocupado':    {'id': 'EMOCION_PREOCUPADO','tipo': 'emocion_negativa', 'grounding_base': 0.90, 'variantes': ['preocupada', 'me tiene preocupado', 'preocupación'], 'valencia': -1},
    'asustado':      {'id': 'EMOCION_ASUSTADO',  'tipo': 'emocion_negativa', 'grounding_base': 0.90, 'variantes': ['asustada', 'le tengo miedo', 'da susto'], 'valencia': -2},
    'aburrido':      {'id': 'EMOCION_ABURRIDO',  'tipo': 'emocion_negativa', 'grounding_base': 0.85, 'variantes': ['aburrida', 'qué aburrimiento', 'me aburro'], 'valencia': -1},
    'confundido':    {'id': 'EMOCION_CONFUNDIDO','tipo': 'emocion_negativa', 'grounding_base': 0.85, 'variantes': ['confundida', 'confusión', 'no entiendo'], 'valencia': -1},
    'perdido':       {'id': 'EMOCION_PERDIDO',   'tipo': 'emocion_negativa', 'grounding_base': 0.85, 'variantes': ['perdida', 'me siento perdido', 'sin rumbo'], 'valencia': -1},
    'llorar':        {'id': 'EMOCION_LLORAR',    'tipo': 'emocion_negativa', 'grounding_base': 0.92, 'variantes': ['lloré', 'lloro', 'llorando', 'con ganas de llorar', 'ganas de llorar'], 'valencia': -2},
    'deprimido':     {'id': 'EMOCION_DEPRIMIDO', 'tipo': 'emocion_negativa', 'grounding_base': 0.93, 'variantes': ['deprimida', 'depresión', 'muy bajoneado', 'bajoneado'], 'valencia': -2},
    'vacío':         {'id': 'EMOCION_VACIO',     'tipo': 'emocion_negativa', 'grounding_base': 0.92, 'variantes': ['vacio', 'me siento vacío', 'sinsentido'], 'valencia': -2},
    'solo':          {'id': 'EMOCION_SOLO',      'tipo': 'emocion_negativa', 'grounding_base': 0.93, 'variantes': ['sola', 'me siento solo', 'soledad', 'nadie'], 'valencia': -2},
    'herido':        {'id': 'EMOCION_HERIDO',    'tipo': 'emocion_negativa', 'grounding_base': 0.88, 'variantes': ['herida', 'me hirieron', 'me dolió'], 'valencia': -2},
    'decepcionado':  {'id': 'EMOCION_DECEP',     'tipo': 'emocion_negativa', 'grounding_base': 0.90, 'variantes': ['decepcionada', 'decepción', 'qué decepción'], 'valencia': -2},
    'avergonzado':   {'id': 'EMOCION_VERGÜENZA', 'tipo': 'emocion_negativa', 'grounding_base': 0.87, 'variantes': ['vergüenza', 'vergüenza ajena', 'qué pena'], 'valencia': -1},

    # Neutros o mixtos
    'regular':       {'id': 'EMOCION_REGULAR',   'tipo': 'emocion_neutra', 'grounding_base': 0.80, 'variantes': [], 'valencia': 0},
    'normal':        {'id': 'EMOCION_NORMAL',    'tipo': 'emocion_neutra', 'grounding_base': 0.80, 'variantes': [], 'valencia': 0},
    'más o menos':   {'id': 'EMOCION_REGULAR',   'tipo': 'emocion_neutra', 'grounding_base': 0.85, 'variantes': ['mas o menos', 'ahí más o menos'], 'valencia': 0},
    'sorprendido':   {'id': 'EMOCION_SORPRENDIDO','tipo': 'emocion_mixta', 'grounding_base': 0.85, 'variantes': ['sorprendida', 'sorpresa', 'qué sorpresa'], 'valencia': 0},
    'nervioso':      {'id': 'EMOCION_NERVIOSO',  'tipo': 'emocion_mixta',  'grounding_base': 0.85, 'variantes': ['nerviosa', 'nervios', 'estoy nervioso'], 'valencia': -1},
    'emoción':       {'id': 'CONCEPTO_EMOCION',  'tipo': 'concepto_emocion','grounding_base': 0.85,'variantes': ['emociones'], 'valencia': 0},
    'sentimiento':   {'id': 'CONCEPTO_SENTIMIENTO','tipo': 'concepto_emocion','grounding_base': 0.85,'variantes': ['sentimientos', 'lo que siento'], 'valencia': 0},
    'nostalgia':     {'id': 'EMOCION_NOSTALGIA', 'tipo': 'emocion_mixta',  'grounding_base': 0.88, 'variantes': ['nostálgico', 'nostalgico', 'extraño algo'], 'valencia': -1},
    'extrañar':      {'id': 'EMOCION_EXTRANAR',  'tipo': 'emocion_mixta',  'grounding_base': 0.90, 'variantes': ['extraño a alguien', 'te extraño', 'lo extraño', 'extrañas'], 'valencia': -1},
}
