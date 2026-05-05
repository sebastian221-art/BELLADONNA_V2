# biblioteca/vocabulario/base/pronombres.py
# ================================================
# PRONOMBRES — Personales, reflexivos, indefinidos
# Esenciales para entender de quién se habla
# ================================================

PRONOMBRES = {

    # ── PERSONALES SUJETO ────────────────────────
    'yo':         {'id': 'PRON_YO',         'tipo': 'pronombre_personal', 'grounding_base': 0.90, 'variantes': []},
    'tú':         {'id': 'PRON_TU',         'tipo': 'pronombre_personal', 'grounding_base': 0.90, 'variantes': ['tu']},
    'vos':        {'id': 'PRON_VOS',        'tipo': 'pronombre_personal', 'grounding_base': 0.85, 'variantes': []},
    'él':         {'id': 'PRON_EL',         'tipo': 'pronombre_personal', 'grounding_base': 0.85, 'variantes': ['el']},
    'ella':       {'id': 'PRON_ELLA',       'tipo': 'pronombre_personal', 'grounding_base': 0.85, 'variantes': []},
    'nosotros':   {'id': 'PRON_NOS_MASC',   'tipo': 'pronombre_personal', 'grounding_base': 0.85, 'variantes': ['nosotras']},
    'ustedes':    {'id': 'PRON_USTEDES',    'tipo': 'pronombre_personal', 'grounding_base': 0.85, 'variantes': ['usted']},
    'ellos':      {'id': 'PRON_ELLOS',      'tipo': 'pronombre_personal', 'grounding_base': 0.83, 'variantes': ['ellas']},

    # ── PERSONALES OBJETO ────────────────────────
    'me':         {'id': 'PRON_OBJ_1SG',    'tipo': 'pronombre_objeto',   'grounding_base': 0.88, 'variantes': []},
    'te':         {'id': 'PRON_OBJ_2SG',    'tipo': 'pronombre_objeto',   'grounding_base': 0.88, 'variantes': []},
    'se':         {'id': 'PRON_OBJ_3SG',    'tipo': 'pronombre_objeto',   'grounding_base': 0.85, 'variantes': []},
    'nos':        {'id': 'PRON_OBJ_1PL',    'tipo': 'pronombre_objeto',   'grounding_base': 0.83, 'variantes': []},
    'les':        {'id': 'PRON_OBJ_3PL',    'tipo': 'pronombre_objeto',   'grounding_base': 0.82, 'variantes': []},
    'le':         {'id': 'PRON_OBJ_3SG_D',  'tipo': 'pronombre_objeto',   'grounding_base': 0.80, 'variantes': []},

    # ── REFLEXIVOS / RECÍPROCOS ──────────────────
    'sí mismo':   {'id': 'PRON_REFL_3SG',   'tipo': 'pronombre_reflexivo','grounding_base': 0.82, 'variantes': ['sí misma', 'sí mismos']},
    'uno mismo':  {'id': 'PRON_REFL_INDEF',  'tipo': 'pronombre_reflexivo','grounding_base': 0.80, 'variantes': ['una misma']},

    # ── INDEFINIDOS ──────────────────────────────
    'alguien':    {'id': 'PRON_INDEF_POS',   'tipo': 'pronombre_indefinido','grounding_base': 0.88, 'variantes': []},
    'nadie':      {'id': 'PRON_INDEF_NEG',   'tipo': 'pronombre_indefinido','grounding_base': 0.88, 'variantes': []},
    'algo':       {'id': 'PRON_INDEF_COSA',  'tipo': 'pronombre_indefinido','grounding_base': 0.88, 'variantes': []},
    'nada':       {'id': 'PRON_INDEF_NEG_C', 'tipo': 'pronombre_indefinido','grounding_base': 0.90, 'variantes': []},
    'todo':       {'id': 'PRON_INDEF_TODO',  'tipo': 'pronombre_indefinido','grounding_base': 0.85, 'variantes': []},
    'todos':      {'id': 'PRON_INDEF_PL',    'tipo': 'pronombre_indefinido','grounding_base': 0.83, 'variantes': ['todas']},
    'uno':        {'id': 'PRON_INDEF_UNO',   'tipo': 'pronombre_indefinido','grounding_base': 0.80, 'variantes': ['una']},
    'otro':       {'id': 'PRON_INDEF_OTRO',  'tipo': 'pronombre_indefinido','grounding_base': 0.82, 'variantes': ['otra', 'otros', 'otras']},
    'mucho':      {'id': 'PRON_INDEF_MUCH',  'tipo': 'pronombre_indefinido','grounding_base': 0.85, 'variantes': ['mucha', 'muchos', 'muchas']},
    'poco':       {'id': 'PRON_INDEF_POCO',  'tipo': 'pronombre_indefinido','grounding_base': 0.83, 'variantes': ['poca', 'pocos', 'pocas']},
    'varios':     {'id': 'PRON_INDEF_VAR',   'tipo': 'pronombre_indefinido','grounding_base': 0.80, 'variantes': ['varias']},
    'algunos':    {'id': 'PRON_INDEF_ALG',   'tipo': 'pronombre_indefinido','grounding_base': 0.82, 'variantes': ['algunas']},
    'ninguno':    {'id': 'PRON_INDEF_NING',  'tipo': 'pronombre_indefinido','grounding_base': 0.83, 'variantes': ['ninguna']},
    'cualquiera': {'id': 'PRON_INDEF_CUAL',  'tipo': 'pronombre_indefinido','grounding_base': 0.80, 'variantes': []},
    'quienquiera':{'id': 'PRON_INDEF_QQUIEN','tipo': 'pronombre_indefinido','grounding_base': 0.72, 'variantes': []},

    # ── DEMOSTRATIVOS PRONOMINALES ───────────────
    'este':       {'id': 'PRON_DEM_PROX_M',  'tipo': 'pronombre_demostrativo','grounding_base': 0.82, 'variantes': ['esta', 'estos', 'estas']},
    'ese':        {'id': 'PRON_DEM_MED_M',   'tipo': 'pronombre_demostrativo','grounding_base': 0.80, 'variantes': ['esa', 'esos', 'esas']},
    'aquél':      {'id': 'PRON_DEM_DIST_M',  'tipo': 'pronombre_demostrativo','grounding_base': 0.75, 'variantes': ['aquella', 'aquellos', 'aquellas']},

    # ── RELATIVOS PRONOMINALES ───────────────────
    'el que':     {'id': 'PRON_REL_MASC',    'tipo': 'pronombre_relativo', 'grounding_base': 0.80, 'variantes': ['la que', 'los que', 'las que', 'lo que']},
    'quien':      {'id': 'PRON_REL_QUIEN',   'tipo': 'pronombre_relativo', 'grounding_base': 0.82, 'variantes': ['quienes']},
    'cuanto':     {'id': 'PRON_REL_CUANTO',  'tipo': 'pronombre_relativo', 'grounding_base': 0.78, 'variantes': ['cuanta', 'cuantos', 'cuantas']},

    # ── INTERROGATIVOS ───────────────────────────
    'quién':      {'id': 'PRON_INTERR_QUIEN','tipo': 'pronombre_interrogativo','grounding_base': 0.90, 'variantes': ['quien']},
    'qué':        {'id': 'PRON_INTERR_QUE',  'tipo': 'pronombre_interrogativo','grounding_base': 0.90, 'variantes': ['que']},
    'cuál':       {'id': 'PRON_INTERR_CUAL', 'tipo': 'pronombre_interrogativo','grounding_base': 0.88, 'variantes': ['cual', 'cuáles', 'cuales']},
    'cuánto':     {'id': 'PRON_INTERR_CUANT','tipo': 'pronombre_interrogativo','grounding_base': 0.88, 'variantes': ['cuanto', 'cuánta', 'cuantos', 'cuántos']},
}
