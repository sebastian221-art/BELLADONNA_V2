# biblioteca/vocabulario/base/preguntas.py
# ================================================
# PREGUNTAS Y REFERENCIAS
# Palabras interrogativas y de referencia
# ================================================

PREGUNTAS = {
    # Interrogativas directas
    'qué':        {'id': 'PREG_QUE',      'grounding': 0.90, 'tipo': 'pregunta'},
    'que':        {'id': 'PREG_QUE',      'grounding': 0.85, 'tipo': 'pregunta'},
    'quién':      {'id': 'PREG_QUIEN',    'grounding': 0.90, 'tipo': 'pregunta'},
    'quien':      {'id': 'PREG_QUIEN',    'grounding': 0.85, 'tipo': 'pregunta'},
    'cómo':       {'id': 'PREG_COMO',     'grounding': 0.90, 'tipo': 'pregunta'},
    'como':       {'id': 'PREG_COMO',     'grounding': 0.85, 'tipo': 'pregunta'},
    'cuándo':     {'id': 'PREG_CUANDO',   'grounding': 0.90, 'tipo': 'pregunta'},
    'cuando':     {'id': 'PREG_CUANDO',   'grounding': 0.85, 'tipo': 'pregunta'},
    'dónde':      {'id': 'PREG_DONDE',    'grounding': 0.90, 'tipo': 'pregunta'},
    'donde':      {'id': 'PREG_DONDE',    'grounding': 0.85, 'tipo': 'pregunta'},
    'por qué':    {'id': 'PREG_POR_QUE',  'grounding': 0.95, 'tipo': 'pregunta'},
    'por que':    {'id': 'PREG_POR_QUE',  'grounding': 0.90, 'tipo': 'pregunta'},
    'porqué':     {'id': 'PREG_POR_QUE',  'grounding': 0.90, 'tipo': 'pregunta'},
    'porque':     {'id': 'PREG_PORQUE',   'grounding': 0.85, 'tipo': 'causa'},
    'cuánto':     {'id': 'PREG_CUANTO',   'grounding': 0.90, 'tipo': 'pregunta'},
    'cuanto':     {'id': 'PREG_CUANTO',   'grounding': 0.85, 'tipo': 'pregunta'},
    'cuántos':    {'id': 'PREG_CUANTOS',  'grounding': 0.90, 'tipo': 'pregunta'},
    'cuantos':    {'id': 'PREG_CUANTOS',  'grounding': 0.85, 'tipo': 'pregunta'},
    'cuál':       {'id': 'PREG_CUAL',     'grounding': 0.90, 'tipo': 'pregunta'},
    'cual':       {'id': 'PREG_CUAL',     'grounding': 0.85, 'tipo': 'pregunta'},
    'cuáles':     {'id': 'PREG_CUALES',   'grounding': 0.90, 'tipo': 'pregunta'},

    # Referencias personales
    'yo':         {'id': 'REF_YO',        'grounding': 0.90, 'tipo': 'referencia_personal'},
    'tú':         {'id': 'REF_TU',        'grounding': 0.90, 'tipo': 'referencia_personal'},
    'tu':         {'id': 'REF_TU',        'grounding': 0.85, 'tipo': 'referencia_personal'},
    'él':         {'id': 'REF_EL',        'grounding': 0.85, 'tipo': 'referencia_personal'},
    'ella':       {'id': 'REF_ELLA',      'grounding': 0.85, 'tipo': 'referencia_personal'},
    'nosotros':   {'id': 'REF_NOSOTROS',  'grounding': 0.85, 'tipo': 'referencia_personal'},
    'me':         {'id': 'REF_ME',        'grounding': 0.80, 'tipo': 'referencia_personal'},
    'mi':         {'id': 'REF_MI',        'grounding': 0.80, 'tipo': 'referencia_personal'},
    'mí':         {'id': 'REF_MI',        'grounding': 0.80, 'tipo': 'referencia_personal'},
    'te':         {'id': 'REF_TE',        'grounding': 0.80, 'tipo': 'referencia_personal'},

    # Afirmación y negación
    'sí':         {'id': 'AFIRMACION',    'grounding': 0.95, 'tipo': 'confirmacion'},
    'si':         {'id': 'AFIRMACION',    'grounding': 0.90, 'tipo': 'confirmacion'},
    'no':         {'id': 'NEGACION',      'grounding': 0.95, 'tipo': 'negacion'},
    'claro':      {'id': 'AFIRMACION_FUERTE','grounding': 0.90, 'tipo': 'confirmacion'},
    'exacto':     {'id': 'AFIRMACION_FUERTE','grounding': 0.90, 'tipo': 'confirmacion'},
    'correcto':   {'id': 'AFIRMACION_FUERTE','grounding': 0.90, 'tipo': 'confirmacion'},
    'nunca':      {'id': 'NEGACION_FUERTE', 'grounding': 0.90, 'tipo': 'negacion'},
    'jamás':      {'id': 'NEGACION_FUERTE', 'grounding': 0.90, 'tipo': 'negacion'},
    'tampoco':    {'id': 'NEGACION',       'grounding': 0.85, 'tipo': 'negacion'},

    # Cuantificadores
    'todo':       {'id': 'CUANT_TODO',    'grounding': 0.85, 'tipo': 'cuantificador'},
    'todos':      {'id': 'CUANT_TODOS',   'grounding': 0.85, 'tipo': 'cuantificador'},
    'algo':       {'id': 'CUANT_ALGO',    'grounding': 0.80, 'tipo': 'cuantificador'},
    'nada':       {'id': 'CUANT_NADA',    'grounding': 0.85, 'tipo': 'cuantificador'},
    'mucho':      {'id': 'CUANT_MUCHO',   'grounding': 0.85, 'tipo': 'cuantificador'},
    'poco':       {'id': 'CUANT_POCO',    'grounding': 0.85, 'tipo': 'cuantificador'},
    'más':        {'id': 'CUANT_MAS',     'grounding': 0.85, 'tipo': 'cuantificador'},
    'mas':        {'id': 'CUANT_MAS',     'grounding': 0.80, 'tipo': 'cuantificador'},
    'menos':      {'id': 'CUANT_MENOS',   'grounding': 0.85, 'tipo': 'cuantificador'},
    'muy':        {'id': 'CUANT_MUY',     'grounding': 0.80, 'tipo': 'intensificador'},
    'bastante':   {'id': 'CUANT_BASTANTE','grounding': 0.80, 'tipo': 'intensificador'},
}