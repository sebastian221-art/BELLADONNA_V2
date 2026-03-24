# biblioteca/vocabulario/base/verbos_comunes.py
# ================================================
# VERBOS COMUNES DEL ESPAÑOL
# Los verbos más frecuentes que Bell necesita
# ================================================

VERBOS_COMUNES = {
    # Estado y ser
    'estoy':      {'id': 'VERBO_ESTAR_YO',    'grounding': 0.85, 'tipo': 'verbo_estado'},
    'estás':      {'id': 'VERBO_ESTAR_TU',    'grounding': 0.85, 'tipo': 'verbo_estado'},
    'estas':      {'id': 'VERBO_ESTAR_TU',    'grounding': 0.85, 'tipo': 'verbo_estado'},
    'está':       {'id': 'VERBO_ESTAR_EL',    'grounding': 0.85, 'tipo': 'verbo_estado'},
    'esta':       {'id': 'VERBO_ESTAR_EL',    'grounding': 0.85, 'tipo': 'verbo_estado'},
    'estamos':    {'id': 'VERBO_ESTAR_NOS',   'grounding': 0.85, 'tipo': 'verbo_estado'},
    'eres':       {'id': 'VERBO_SER_TU',      'grounding': 0.85, 'tipo': 'verbo_ser'},
    'es':         {'id': 'VERBO_SER_EL',      'grounding': 0.80, 'tipo': 'verbo_ser'},
    'somos':      {'id': 'VERBO_SER_NOS',     'grounding': 0.80, 'tipo': 'verbo_ser'},
    'soy':        {'id': 'VERBO_SER_YO',      'grounding': 0.85, 'tipo': 'verbo_ser'},

    # Tener
    'tengo':      {'id': 'VERBO_TENER_YO',   'grounding': 0.85, 'tipo': 'verbo_tener'},
    'tienes':     {'id': 'VERBO_TENER_TU',   'grounding': 0.85, 'tipo': 'verbo_tener'},
    'tiene':      {'id': 'VERBO_TENER_EL',   'grounding': 0.80, 'tipo': 'verbo_tener'},

    # Poder
    'puedo':      {'id': 'VERBO_PODER_YO',   'grounding': 0.90, 'tipo': 'verbo_capacidad'},
    'puedes':     {'id': 'VERBO_PODER_TU',   'grounding': 0.90, 'tipo': 'verbo_capacidad'},
    'puede':      {'id': 'VERBO_PODER_EL',   'grounding': 0.85, 'tipo': 'verbo_capacidad'},
    'podemos':    {'id': 'VERBO_PODER_NOS',  'grounding': 0.85, 'tipo': 'verbo_capacidad'},

    # Querer y necesitar
    'quiero':     {'id': 'VERBO_QUERER_YO',   'grounding': 0.90, 'tipo': 'verbo_deseo'},
    'quieres':    {'id': 'VERBO_QUERER_TU',   'grounding': 0.90, 'tipo': 'verbo_deseo'},
    'quiere':     {'id': 'VERBO_QUERER_EL',   'grounding': 0.85, 'tipo': 'verbo_deseo'},
    'necesito':   {'id': 'VERBO_NECESITAR_YO','grounding': 0.90, 'tipo': 'verbo_necesidad'},
    'necesitas':  {'id': 'VERBO_NECESITAR_TU','grounding': 0.90, 'tipo': 'verbo_necesidad'},
    'necesita':   {'id': 'VERBO_NECESITAR_EL','grounding': 0.85, 'tipo': 'verbo_necesidad'},

    # Saber y conocer
    'sé':         {'id': 'VERBO_SABER_YO',   'grounding': 0.85, 'tipo': 'verbo_conocimiento'},
    'se':         {'id': 'VERBO_SABER_YO',   'grounding': 0.75, 'tipo': 'verbo_conocimiento'},
    'sabes':      {'id': 'VERBO_SABER_TU',   'grounding': 0.85, 'tipo': 'verbo_conocimiento'},
    'sabe':       {'id': 'VERBO_SABER_EL',   'grounding': 0.80, 'tipo': 'verbo_conocimiento'},
    'conozco':    {'id': 'VERBO_CONOCER_YO', 'grounding': 0.85, 'tipo': 'verbo_conocimiento'},
    'conoces':    {'id': 'VERBO_CONOCER_TU', 'grounding': 0.85, 'tipo': 'verbo_conocimiento'},
    'entiendo':   {'id': 'VERBO_ENTENDER_YO','grounding': 0.85, 'tipo': 'verbo_comprension'},
    'entiendes':  {'id': 'VERBO_ENTENDER_TU','grounding': 0.85, 'tipo': 'verbo_comprension'},
    'entender':   {'id': 'VERBO_ENTENDER',   'grounding': 0.85, 'tipo': 'verbo_comprension'},

    # Hacer
    'hago':       {'id': 'VERBO_HACER_YO',   'grounding': 0.85, 'tipo': 'verbo_accion'},
    'haces':      {'id': 'VERBO_HACER_TU',   'grounding': 0.85, 'tipo': 'verbo_accion'},
    'hace':       {'id': 'VERBO_HACER_EL',   'grounding': 0.80, 'tipo': 'verbo_accion'},
    'hacemos':    {'id': 'VERBO_HACER_NOS',  'grounding': 0.80, 'tipo': 'verbo_accion'},
    'hacer':      {'id': 'VERBO_HACER',      'grounding': 0.85, 'tipo': 'verbo_accion'},

    # Hablar y decir
    'digo':       {'id': 'VERBO_DECIR_YO',   'grounding': 0.85, 'tipo': 'verbo_comunicacion'},
    'dices':      {'id': 'VERBO_DECIR_TU',   'grounding': 0.85, 'tipo': 'verbo_comunicacion'},
    'dice':       {'id': 'VERBO_DECIR_EL',   'grounding': 0.80, 'tipo': 'verbo_comunicacion'},
    'decir':      {'id': 'VERBO_DECIR',      'grounding': 0.85, 'tipo': 'verbo_comunicacion'},
    'hablo':      {'id': 'VERBO_HABLAR_YO',  'grounding': 0.85, 'tipo': 'verbo_comunicacion'},
    'hablas':     {'id': 'VERBO_HABLAR_TU',  'grounding': 0.85, 'tipo': 'verbo_comunicacion'},
    'hablar':     {'id': 'VERBO_HABLAR',     'grounding': 0.85, 'tipo': 'verbo_comunicacion'},

    # Pensar y sentir
    'pienso':     {'id': 'VERBO_PENSAR_YO',  'grounding': 0.85, 'tipo': 'verbo_pensamiento'},
    'piensas':    {'id': 'VERBO_PENSAR_TU',  'grounding': 0.85, 'tipo': 'verbo_pensamiento'},
    'pensar':     {'id': 'VERBO_PENSAR',     'grounding': 0.85, 'tipo': 'verbo_pensamiento'},
    'siento':     {'id': 'VERBO_SENTIR_YO',  'grounding': 0.90, 'tipo': 'verbo_emocion'},
    'sientes':    {'id': 'VERBO_SENTIR_TU',  'grounding': 0.90, 'tipo': 'verbo_emocion'},
    'sentir':     {'id': 'VERBO_SENTIR',     'grounding': 0.85, 'tipo': 'verbo_emocion'},
    'creo':       {'id': 'VERBO_CREER_YO',   'grounding': 0.85, 'tipo': 'verbo_pensamiento'},
    'crees':      {'id': 'VERBO_CREER_TU',   'grounding': 0.85, 'tipo': 'verbo_pensamiento'},

    # Ir y venir
    'voy':        {'id': 'VERBO_IR_YO',      'grounding': 0.85, 'tipo': 'verbo_movimiento'},
    'vas':        {'id': 'VERBO_IR_TU',      'grounding': 0.85, 'tipo': 'verbo_movimiento'},
    'va':         {'id': 'VERBO_IR_EL',      'grounding': 0.80, 'tipo': 'verbo_movimiento'},
    'vamos':      {'id': 'VERBO_IR_NOS',     'grounding': 0.85, 'tipo': 'verbo_movimiento'},
    'vengo':      {'id': 'VERBO_VENIR_YO',   'grounding': 0.85, 'tipo': 'verbo_movimiento'},
    'vienes':     {'id': 'VERBO_VENIR_TU',   'grounding': 0.85, 'tipo': 'verbo_movimiento'},

    # Dar y recibir
    'doy':        {'id': 'VERBO_DAR_YO',     'grounding': 0.85, 'tipo': 'verbo_accion'},
    'das':        {'id': 'VERBO_DAR_TU',     'grounding': 0.85, 'tipo': 'verbo_accion'},
    'dar':        {'id': 'VERBO_DAR',        'grounding': 0.85, 'tipo': 'verbo_accion'},

    # Ayudar
    'ayudo':      {'id': 'VERBO_AYUDAR_YO',  'grounding': 0.90, 'tipo': 'verbo_ayuda'},
    'ayudas':     {'id': 'VERBO_AYUDAR_TU',  'grounding': 0.90, 'tipo': 'verbo_ayuda'},
    'ayudar':     {'id': 'VERBO_AYUDAR',     'grounding': 0.90, 'tipo': 'verbo_ayuda'},
    'ayuda':      {'id': 'VERBO_AYUDA',      'grounding': 0.90, 'tipo': 'verbo_ayuda'},
    'ayúdame':    {'id': 'VERBO_AYUDAR_ME',  'grounding': 0.95, 'tipo': 'verbo_ayuda'},
    'ayudame':    {'id': 'VERBO_AYUDAR_ME',  'grounding': 0.95, 'tipo': 'verbo_ayuda'},

    # Trabajar
    'trabajo':    {'id': 'VERBO_TRABAJAR_YO','grounding': 0.85, 'tipo': 'verbo_trabajo'},
    'trabajas':   {'id': 'VERBO_TRABAJAR_TU','grounding': 0.85, 'tipo': 'verbo_trabajo'},
    'trabajar':   {'id': 'VERBO_TRABAJAR',   'grounding': 0.85, 'tipo': 'verbo_trabajo'},

    # Aprender
    'aprendo':    {'id': 'VERBO_APRENDER_YO','grounding': 0.90, 'tipo': 'verbo_aprendizaje'},
    'aprendes':   {'id': 'VERBO_APRENDER_TU','grounding': 0.90, 'tipo': 'verbo_aprendizaje'},
    'aprender':   {'id': 'VERBO_APRENDER',   'grounding': 0.90, 'tipo': 'verbo_aprendizaje'},
}