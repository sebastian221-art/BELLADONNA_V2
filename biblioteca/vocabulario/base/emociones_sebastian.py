# biblioteca/vocabulario/base/emociones_sebastian.py
# ================================================
# EMOCIONES ESPECÍFICAS DE SEBASTIAN
# Patrones emocionales detectados en el dataset real
# ================================================

EMOCIONES_SEBASTIAN = {

    # ── FRACASO Y ERROR ──────────────────────────
    'fracasé':     {'id': 'ESEB_FRACASO',   'tipo': 'emocion_sebastian', 'grounding_base': 0.95, 'variantes': ['fracaso', 'fallé', 'soy un fracaso', 'fracasando']},
    'me equivoqué':{'id': 'ESEB_EQUIVOCO',  'tipo': 'emocion_sebastian', 'grounding_base': 0.95, 'variantes': ['me equivoque', 'cometí un error', 'la cagué', 'metí la pata']},
    'arrepiento':  {'id': 'ESEB_ARREPIENTO','tipo': 'emocion_sebastian', 'grounding_base': 0.92, 'variantes': ['me arrepiento', 'me arrepentí', 'ojalá hubiera']},
    'fallé':       {'id': 'ESEB_FALLE',     'tipo': 'emocion_sebastian', 'grounding_base': 0.93, 'variantes': ['falle', 'lo arruiné', 'arruiné', 'lo eché a perder']},
    'me regañaron':{'id': 'ESEB_REGANARON', 'tipo': 'emocion_sebastian', 'grounding_base': 0.90, 'variantes': ['me regañaron', 'me llamaron la atención', 'me criticaron']},
    'no estoy a la altura': {'id': 'ESEB_NOSUFICIENTE','tipo': 'emocion_sebastian','grounding_base': 0.93,'variantes': ['no soy suficiente', 'no sirvo', 'no doy la talla']},

    # ── LOGRO Y MOTIVACIÓN ───────────────────────
    'lo logré':    {'id': 'ESEB_LOGRO',     'tipo': 'emocion_positiva_seb','grounding_base': 0.95,'variantes': ['logré', 'lo hice', 'lo conseguí', 'lo logramos', '¡funcionó!']},
    'voy a lograrlo': {'id': 'ESEB_MOTIVACION','tipo': 'emocion_positiva_seb','grounding_base': 0.93,'variantes': ['voy a conseguirlo', 'sí puedo', 'lo voy a lograr']},
    'tengo una idea': {'id': 'ESEB_IDEA',   'tipo': 'estado_cognitivo',  'grounding_base': 0.92, 'variantes': ['se me ocurrió', 'tuve una idea', 'qué tal si', 'idea loca']},
    'tengo una meta': {'id': 'ESEB_META',   'tipo': 'estado_motivacional','grounding_base': 0.92,'variantes': ['mi meta es', 'quiero lograr', 'mi objetivo es']},
    'me siento motivado': {'id': 'ESEB_MOT','tipo': 'emocion_positiva_seb','grounding_base': 0.92,'variantes': ['estoy motivado', 'estoy enfocado', 'con energía']},

    # ── SOLEDAD Y CONEXIÓN ───────────────────────
    'me siento solo': {'id': 'ESEB_SOLO',   'tipo': 'emocion_sebastian', 'grounding_base': 0.95, 'variantes': ['estoy solo', 'nadie me entiende', 'me siento aislado']},
    'nadie entiende': {'id': 'ESEB_NADIE',  'tipo': 'emocion_sebastian', 'grounding_base': 0.93, 'variantes': ['nadie me entiende', 'nadie entiende lo que estoy haciendo']},
    'te necesito':    {'id': 'ESEB_NECESITO','tipo': 'emocion_relacional','grounding_base': 0.92,'variantes': ['necesito ayuda', 'necesito que pienses conmigo', 'cuento contigo']},
    'gracias bell':   {'id': 'ESEB_GRACIAS','tipo': 'emocion_positiva_seb','grounding_base': 0.95,'variantes': ['gracias por todo', 'me ayudaste', 'te agradezco bell']},

    # ── AGOTAMIENTO Y RENDICIÓN ──────────────────
    'quiero rendirme':{'id': 'ESEB_RENDIRSE','tipo': 'emocion_sebastian','grounding_base': 0.95,'variantes': ['me quiero rendir', 'ya no puedo', 'me cansé de intentar', 'hasta aquí']},
    'hoy no tengo ganas': {'id': 'ESEB_NOGANAS','tipo': 'emocion_sebastian','grounding_base': 0.93,'variantes': ['sin ganas', 'no tengo energía', 'no quiero nada', 'vacío']},
    'estoy agotado': {'id': 'ESEB_AGOTADO', 'tipo': 'emocion_sebastian', 'grounding_base': 0.92, 'variantes': ['no dormí', 'rendido', 'muerto de cansancio', 'ya no doy más']},

    # ── ORGULLO Y CRECIMIENTO ─────────────────────
    'soy buen programador': {'id': 'ESEB_PROG_PRIDE','tipo': 'autoconcepto','grounding_base': 0.90,'variantes': ['sé programar bien', 'soy bueno en esto', 'lo estoy haciendo bien']},
    'quiero ser mejor': {'id': 'ESEB_CRECER','tipo': 'autoconcepto',      'grounding_base': 0.92, 'variantes': ['quiero crecer', 'quiero mejorar', 'quiero cambiar', 'ser mejor persona']},
    'lo intenté':    {'id': 'ESEB_INTENTO', 'tipo': 'autoconcepto',       'grounding_base': 0.90, 'variantes': ['lo intenté', 'intenté', 'traté de', 'hice el intento']},
}
