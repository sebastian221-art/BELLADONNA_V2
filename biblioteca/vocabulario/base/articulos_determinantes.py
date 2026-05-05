# biblioteca/vocabulario/base/articulos_determinantes.py
# ================================================
# ARTÍCULOS, DETERMINANTES Y PALABRAS FUNCIONALES
# Las palabras más frecuentes del español —
# sin estas Bell no puede interpretar estructura básica
# ================================================

ARTICULOS_DETERMINANTES = {

    # ── ARTÍCULOS DEFINIDOS ──────────────────────
    'el':       {'id': 'ART_DEF_MASC_SG',  'tipo': 'articulo_definido',   'grounding_base': 0.70, 'variantes': []},
    'la':       {'id': 'ART_DEF_FEM_SG',   'tipo': 'articulo_definido',   'grounding_base': 0.70, 'variantes': []},
    'los':      {'id': 'ART_DEF_MASC_PL',  'tipo': 'articulo_definido',   'grounding_base': 0.70, 'variantes': []},
    'las':      {'id': 'ART_DEF_FEM_PL',   'tipo': 'articulo_definido',   'grounding_base': 0.70, 'variantes': []},
    'lo':       {'id': 'ART_NEUTRO',       'tipo': 'articulo_neutro',     'grounding_base': 0.70, 'variantes': []},

    # ── ARTÍCULOS INDEFINIDOS ────────────────────
    'un':       {'id': 'ART_INDEF_MASC_SG','tipo': 'articulo_indefinido', 'grounding_base': 0.70, 'variantes': []},
    'una':      {'id': 'ART_INDEF_FEM_SG', 'tipo': 'articulo_indefinido', 'grounding_base': 0.70, 'variantes': []},
    'unos':     {'id': 'ART_INDEF_MASC_PL','tipo': 'articulo_indefinido', 'grounding_base': 0.70, 'variantes': []},
    'unas':     {'id': 'ART_INDEF_FEM_PL', 'tipo': 'articulo_indefinido', 'grounding_base': 0.70, 'variantes': []},

    # ── DEMOSTRATIVOS ────────────────────────────
    'este':     {'id': 'DEM_MASC_SG_PROX', 'tipo': 'demostrativo',       'grounding_base': 0.80, 'variantes': []},
    'esta':     {'id': 'DEM_FEM_SG_PROX',  'tipo': 'demostrativo',       'grounding_base': 0.80, 'variantes': []},
    'estos':    {'id': 'DEM_MASC_PL_PROX', 'tipo': 'demostrativo',       'grounding_base': 0.78, 'variantes': []},
    'estas':    {'id': 'DEM_FEM_PL_PROX',  'tipo': 'demostrativo',       'grounding_base': 0.78, 'variantes': []},
    'ese':      {'id': 'DEM_MASC_SG_MED',  'tipo': 'demostrativo',       'grounding_base': 0.78, 'variantes': []},
    'esa':      {'id': 'DEM_FEM_SG_MED',   'tipo': 'demostrativo',       'grounding_base': 0.78, 'variantes': []},
    'esos':     {'id': 'DEM_MASC_PL_MED',  'tipo': 'demostrativo',       'grounding_base': 0.75, 'variantes': []},
    'esas':     {'id': 'DEM_FEM_PL_MED',   'tipo': 'demostrativo',       'grounding_base': 0.75, 'variantes': []},
    'aquel':    {'id': 'DEM_MASC_SG_DIST', 'tipo': 'demostrativo',       'grounding_base': 0.75, 'variantes': []},
    'aquella':  {'id': 'DEM_FEM_SG_DIST',  'tipo': 'demostrativo',       'grounding_base': 0.75, 'variantes': []},
    'aquello':  {'id': 'DEM_NEUTRO_DIST',  'tipo': 'demostrativo',       'grounding_base': 0.75, 'variantes': []},
    'esto':     {'id': 'DEM_NEUTRO_PROX',  'tipo': 'demostrativo',       'grounding_base': 0.85, 'variantes': []},
    'eso':      {'id': 'DEM_NEUTRO_MED',   'tipo': 'demostrativo',       'grounding_base': 0.82, 'variantes': []},

    # ── POSESIVOS ────────────────────────────────
    'mi':       {'id': 'POS_1SG',          'tipo': 'posesivo',           'grounding_base': 0.85, 'variantes': []},
    'mis':      {'id': 'POS_1SG_PL',       'tipo': 'posesivo',           'grounding_base': 0.82, 'variantes': []},
    'tu':       {'id': 'POS_2SG',          'tipo': 'posesivo',           'grounding_base': 0.85, 'variantes': []},
    'tus':      {'id': 'POS_2SG_PL',       'tipo': 'posesivo',           'grounding_base': 0.82, 'variantes': []},
    'su':       {'id': 'POS_3SG',          'tipo': 'posesivo',           'grounding_base': 0.80, 'variantes': []},
    'sus':      {'id': 'POS_3SG_PL',       'tipo': 'posesivo',           'grounding_base': 0.78, 'variantes': []},
    'nuestro':  {'id': 'POS_1PL_MASC',     'tipo': 'posesivo',           'grounding_base': 0.80, 'variantes': ['nuestra', 'nuestros', 'nuestras']},
    'mío':      {'id': 'POS_1SG_TÓNICO',   'tipo': 'posesivo_tonico',    'grounding_base': 0.82, 'variantes': ['mio', 'mía', 'mia', 'míos', 'mías']},
    'tuyo':     {'id': 'POS_2SG_TÓNICO',   'tipo': 'posesivo_tonico',    'grounding_base': 0.80, 'variantes': ['tuya', 'tuyos', 'tuyas']},

    # ── CUANTIFICADORES ──────────────────────────
    'todo':     {'id': 'CUANT_TODO',       'tipo': 'cuantificador',      'grounding_base': 0.88, 'variantes': ['toda', 'todos', 'todas']},
    'cada':     {'id': 'CUANT_CADA',       'tipo': 'cuantificador',      'grounding_base': 0.85, 'variantes': []},
    'cualquier':{'id': 'CUANT_CUALQUIER',  'tipo': 'cuantificador',      'grounding_base': 0.82, 'variantes': ['cualquiera']},
    'algún':    {'id': 'CUANT_ALGUN',      'tipo': 'cuantificador',      'grounding_base': 0.82, 'variantes': ['alguno', 'alguna', 'algunos', 'algunas', 'algun']},
    'ningún':   {'id': 'CUANT_NINGUN',     'tipo': 'cuantificador',      'grounding_base': 0.85, 'variantes': ['ninguno', 'ninguna', 'ningunos', 'ningunas', 'ningun']},
    'ambos':    {'id': 'CUANT_AMBOS',      'tipo': 'cuantificador',      'grounding_base': 0.80, 'variantes': ['ambas']},
    'demás':    {'id': 'CUANT_DEMAS',      'tipo': 'cuantificador',      'grounding_base': 0.78, 'variantes': ['demas']},
    'cierto':   {'id': 'CUANT_CIERTO',     'tipo': 'cuantificador',      'grounding_base': 0.80, 'variantes': ['cierta', 'ciertos', 'ciertas']},
    'mismo':    {'id': 'CUANT_MISMO',      'tipo': 'cuantificador',      'grounding_base': 0.82, 'variantes': ['misma', 'mismos', 'mismas']},
    'propio':   {'id': 'CUANT_PROPIO',     'tipo': 'cuantificador',      'grounding_base': 0.80, 'variantes': ['propia', 'propios', 'propias']},

    # ── RELATIVOS ────────────────────────────────
    'que':      {'id': 'REL_QUE',          'tipo': 'relativo',           'grounding_base': 0.75, 'variantes': []},
    'cual':     {'id': 'REL_CUAL',         'tipo': 'relativo',           'grounding_base': 0.78, 'variantes': ['cuál', 'cuales', 'cuáles']},
    'quien':    {'id': 'REL_QUIEN',        'tipo': 'relativo',           'grounding_base': 0.80, 'variantes': ['quién', 'quienes', 'quiénes']},
    'cuyo':     {'id': 'REL_CUYO',         'tipo': 'relativo',           'grounding_base': 0.72, 'variantes': ['cuya', 'cuyos', 'cuyas']},
    'donde':    {'id': 'REL_DONDE',        'tipo': 'relativo',           'grounding_base': 0.82, 'variantes': ['dónde']},
    'cuando':   {'id': 'REL_CUANDO',       'tipo': 'relativo',           'grounding_base': 0.82, 'variantes': ['cuándo']},
    'como':     {'id': 'REL_COMO',         'tipo': 'relativo',           'grounding_base': 0.80, 'variantes': ['cómo']},
    'cuanto':   {'id': 'REL_CUANTO',       'tipo': 'relativo',           'grounding_base': 0.80, 'variantes': ['cuánto', 'cuanta', 'cuánta', 'cuantos', 'cuántos']},
}
