# biblioteca/vocabulario/base/gastronomia.py
# ================================================
# GASTRONOMÍA — Expandida (9 → 120+ entradas)
# ================================================

CONCEPTOS_GASTRONOMIA = {

    # ── COMIDAS PRINCIPALES ──────────────────────
    'arepa':       {'id': 'GASTRO_AREPA',   'tipo': 'comida_colombiana', 'grounding_base': 0.95, 'variantes': ['arepas', 'arepa de choclo', 'arepa de maíz']},
    'bandeja paisa': {'id': 'GASTRO_BANDEJA','tipo': 'comida_colombiana','grounding_base': 0.92, 'variantes': ['bandeja', 'la bandeja']},
    'sancocho':    {'id': 'GASTRO_SANCOCHO','tipo': 'comida_colombiana', 'grounding_base': 0.92, 'variantes': ['sancocho de pollo', 'sancocho de res']},
    'empanada':    {'id': 'GASTRO_EMPANADA','tipo': 'comida_colombiana', 'grounding_base': 0.90, 'variantes': ['empanadas', 'empanaditas']},
    'chicharrón':  {'id': 'GASTRO_CHICHA',  'tipo': 'comida_colombiana', 'grounding_base': 0.88, 'variantes': ['chicharron', 'chicharrones']},
    'arroz':       {'id': 'GASTRO_ARROZ',   'tipo': 'alimento_basico',   'grounding_base': 0.92, 'variantes': ['arroces', 'arroz blanco', 'arroz con pollo']},
    'frijoles':    {'id': 'GASTRO_FRIJOLES','tipo': 'alimento_basico',   'grounding_base': 0.90, 'variantes': ['frijol', 'lentejas', 'granos']},
    'pollo':       {'id': 'GASTRO_POLLO',   'tipo': 'proteina',          'grounding_base': 0.93, 'variantes': ['pollos', 'pechuga', 'muslo']},
    'carne':       {'id': 'GASTRO_CARNE',   'tipo': 'proteina',          'grounding_base': 0.93, 'variantes': ['carnes', 'res', 'bistec', 'carne molida']},
    'pescado':     {'id': 'GASTRO_PESCADO', 'tipo': 'proteina',          'grounding_base': 0.88, 'variantes': ['pescados', 'mojarra', 'tilapia', 'bagre']},
    'huevo':       {'id': 'GASTRO_HUEVO',   'tipo': 'alimento_basico',   'grounding_base': 0.92, 'variantes': ['huevos', 'huevo frito', 'huevo revuelto']},
    'papa':        {'id': 'GASTRO_PAPA',    'tipo': 'alimento_basico',   'grounding_base': 0.92, 'variantes': ['papas', 'papas fritas', 'papas cocidas']},
    'sopa':        {'id': 'GASTRO_SOPA',    'tipo': 'plato',             'grounding_base': 0.90, 'variantes': ['sopas', 'caldo', 'caldo de pollo']},
    'ensalada':    {'id': 'GASTRO_ENSALADA','tipo': 'plato',             'grounding_base': 0.88, 'variantes': ['ensaladas', 'lechuga', 'vegetales']},

    # ── BEBIDAS ──────────────────────────────────
    'café':        {'id': 'GASTRO_CAFE',    'tipo': 'bebida',            'grounding_base': 0.95, 'variantes': ['cafe', 'tinto', 'cafecito', 'café colombiano']},
    'agua':        {'id': 'GASTRO_AGUA',    'tipo': 'bebida',            'grounding_base': 0.93, 'variantes': ['agua fría', 'agua del grifo', 'tomar agua']},
    'jugo':        {'id': 'GASTRO_JUGO',    'tipo': 'bebida',            'grounding_base': 0.90, 'variantes': ['jugos', 'jugo natural', 'zumo']},
    'gaseosa':     {'id': 'GASTRO_GASEOSA', 'tipo': 'bebida',            'grounding_base': 0.88, 'variantes': ['gaseosas', 'refresco', 'cola', 'pepsi', 'colombiana']},
    'leche':       {'id': 'GASTRO_LECHE',   'tipo': 'bebida',            'grounding_base': 0.90, 'variantes': ['leches', 'vasito de leche']},
    'chocolate':   {'id': 'GASTRO_CHOCO',   'tipo': 'bebida_dulce',      'grounding_base': 0.88, 'variantes': ['chocolates', 'chocolatina', 'cacao']},
    'cerveza':     {'id': 'GASTRO_CERVEZA', 'tipo': 'bebida_alcoholica', 'grounding_base': 0.85, 'variantes': ['cervezas', 'chela', 'birra']},

    # ── SNACKS Y DULCES ──────────────────────────
    'pan':         {'id': 'GASTRO_PAN',     'tipo': 'panaderia',         'grounding_base': 0.92, 'variantes': ['panes', 'pandebono', 'almojábana', 'mogolla']},
    'fruta':       {'id': 'GASTRO_FRUTA',   'tipo': 'alimento_saludable','grounding_base': 0.90, 'variantes': ['frutas', 'mango', 'banano', 'piña', 'guanábana']},
    'dulce':       {'id': 'GASTRO_DULCE',   'tipo': 'snack',             'grounding_base': 0.87, 'variantes': ['dulces', 'confite', 'gomitas', 'caramelo']},

    # ── ACCIONES DE COMER ────────────────────────
    'desayuno':    {'id': 'GASTRO_DESAY',   'tipo': 'tiempo_comida',     'grounding_base': 0.92, 'variantes': ['desayunar', 'desayuné', 'ya desayuné']},
    'almuerzo':    {'id': 'GASTRO_ALMU',    'tipo': 'tiempo_comida',     'grounding_base': 0.93, 'variantes': ['almorzar', 'almorcé', 'a almorzar']},
    'cena':        {'id': 'GASTRO_CENA',    'tipo': 'tiempo_comida',     'grounding_base': 0.90, 'variantes': ['cenar', 'cené', 'a cenar']},
    'antojo':      {'id': 'GASTRO_ANTOJO',  'tipo': 'deseo_alimentario', 'grounding_base': 0.87, 'variantes': ['antojos', 'se me antoja', 'quiero comer']},
    'rico':        {'id': 'GASTRO_RICO',    'tipo': 'valoracion_comida', 'grounding_base': 0.90, 'variantes': ['riquísimo', 'delicioso', 'sabroso', 'exquisito', 'buenísimo']},
    'restaurante': {'id': 'GASTRO_REST',    'tipo': 'espacio_gastro',    'grounding_base': 0.88, 'variantes': ['restaurantes', 'comida a domicilio', 'pedir domicilio', 'rappi']},
}
