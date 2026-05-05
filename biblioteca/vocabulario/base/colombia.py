# biblioteca/vocabulario/base/colombia.py
# ================================================
# COLOMBIA — Expandido (25 → 80+ entradas)
# ================================================

CONCEPTOS_COLOMBIA = {
    # Jerga y expresiones colombianas
    'parce':       {'id': 'COL_PARCE',      'tipo': 'jerga_col', 'grounding_base': 0.95, 'variantes': ['parces', 'parcero', 'parcera', 'llave', 'llave mía']},
    'bacano':      {'id': 'COL_BACANO',     'tipo': 'jerga_col', 'grounding_base': 0.93, 'variantes': ['bacana', 'bacanos', 'bacano el man', 'qué bacano']},
    'chévere':     {'id': 'COL_CHEVERE',    'tipo': 'jerga_col', 'grounding_base': 0.93, 'variantes': ['chevere', 'chéverisimo', 'qué chévere']},
    'marica':      {'id': 'COL_MARICA',     'tipo': 'jerga_col', 'grounding_base': 0.90, 'variantes': ['mano', 'mae', 'pana']},
    'chimba':      {'id': 'COL_CHIMBA',     'tipo': 'jerga_col', 'grounding_base': 0.88, 'variantes': ['qué chimba', 'es una chimba']},
    'berraco':     {'id': 'COL_BERRACO',    'tipo': 'jerga_col', 'grounding_base': 0.88, 'variantes': ['verraco', 'berracos', 'es muy berraco']},
    'juepucha':    {'id': 'COL_JUEPUCHA',   'tipo': 'exclamacion_col','grounding_base': 0.87,'variantes': ['jueputa', 'verraco', 'uy verraco']},
    'qué pena':    {'id': 'COL_QUEPENA',    'tipo': 'expresion_col', 'grounding_base': 0.90, 'variantes': ['qué pena con usted', 'pena ajena', 'penoso']},
    'buenas':      {'id': 'COL_BUENAS',     'tipo': 'saludo_col',    'grounding_base': 0.93, 'variantes': ['buenas gente', 'ey buenas']},
    'pilas':       {'id': 'COL_PILAS',      'tipo': 'expresion_col', 'grounding_base': 0.90, 'variantes': ['ojo pilas', 'póngale pilas', 'ponle pilas', 'con cuidado']},
    'uy':          {'id': 'COL_UY',         'tipo': 'exclamacion_col','grounding_base': 0.90, 'variantes': ['uy no', 'uy sí', 'uy juemadre']},
    'no joda':     {'id': 'COL_NOJODA',     'tipo': 'expresion_col', 'grounding_base': 0.88, 'variantes': ['no sea así', 'no me haga eso', 'no friegue']},
    'achanta':     {'id': 'COL_ACHANTA',    'tipo': 'accion_col',    'grounding_base': 0.85, 'variantes': ['achantar', 'se acobardó', 'echó para atrás']},
    'rumbear':     {'id': 'COL_RUMBEAR',    'tipo': 'actividad_col', 'grounding_base': 0.87, 'variantes': ['rumba', 'rumbeo', 'salimos a rumbear', 'fiesta']},
    'tinto':       {'id': 'COL_TINTO',      'tipo': 'bebida_col',    'grounding_base': 0.90, 'variantes': ['un tinto', 'tintico', 'café negro']},
    'aguardiente': {'id': 'COL_AGUARDIENTE','tipo': 'bebida_col',    'grounding_base': 0.87, 'variantes': ['guaro', 'la botella', 'trago']},
    'finca':       {'id': 'COL_FINCA',      'tipo': 'lugar_col',     'grounding_base': 0.88, 'variantes': ['fincas', 'ir a la finca', 'fin de semana en finca']},
    'bogotá':      {'id': 'COL_BOGOTA',     'tipo': 'ciudad_col',    'grounding_base': 0.88, 'variantes': ['Bogotá', 'la capital', 'rolo', 'cachaco']},
    'medellín':    {'id': 'COL_MEDELLIN',   'tipo': 'ciudad_col',    'grounding_base': 0.88, 'variantes': ['Medellín', 'paisa', 'paisas', 'la ciudad de la eterna primavera']},
    'bucaramanga': {'id': 'COL_BUCA',       'tipo': 'ciudad_col',    'grounding_base': 0.90, 'variantes': ['Bucaramanga', 'buca', 'ciudad bonita']},
    'colombia':    {'id': 'COL_COLOMBIA',   'tipo': 'pais',          'grounding_base': 0.92, 'variantes': ['colombiano', 'colombiana', 'mi país']},
    'arrecho':     {'id': 'COL_ARRECHO',    'tipo': 'jerga_col',     'grounding_base': 0.85, 'variantes': ['arrecha', 'qué arrecho', 'arrechísimo']},
    'qué más':     {'id': 'COL_QUEMAS',     'tipo': 'saludo_col',    'grounding_base': 0.92, 'variantes': ['qué más parce', 'quiubo', 'quiubo qué más']},
    'sumercé':     {'id': 'COL_SUMERCE',    'tipo': 'tratamiento_col','grounding_base': 0.83,'variantes': ['sumerced', 'usted', 'señor', 'señora']},
    'ahoritica':   {'id': 'COL_AHORITICA',  'tipo': 'temporal_col',  'grounding_base': 0.90, 'variantes': ['ahorita', 'ya mero', 'en un ratico', 'ya mismo']},
    'harto':       {'id': 'COL_HARTO',      'tipo': 'cantidad_col',  'grounding_base': 0.88, 'variantes': ['harta', 'hartos', 'un montón', 'montón', 'un pocón']},
    'man':         {'id': 'COL_MAN',        'tipo': 'persona_col',   'grounding_base': 0.88, 'variantes': ['el man', 'la man', 'ese man', 'esa man']},
    'camello':     {'id': 'COL_CAMELLO',    'tipo': 'trabajo_col',   'grounding_base': 0.85, 'variantes': ['camellar', 'camellar duro', 'trabajar', 'trabajo duro']},
    'gonorrea':    {'id': 'COL_GONORREA',   'tipo': 'jerga_col',     'grounding_base': 0.80, 'variantes': ['gonorra', 'gon']},
    'el combo':    {'id': 'COL_COMBO',      'tipo': 'grupo_col',     'grounding_base': 0.87, 'variantes': ['combo', 'el grupito', 'la manada', 'los amigos']},
}
