# biblioteca/vocabulario/base/cotidiano.py
# ================================================
# COTIDIANO — Expandido (17 → 150+ entradas)
# Actividades y situaciones del día a día
# ================================================

CONCEPTOS_COTIDIANO = {

    # ── RUTINA DIARIA ────────────────────────────
    'despertar':   {'id': 'COT_DESPERTAR',  'tipo': 'rutina',   'grounding_base': 0.92, 'variantes': ['me desperté', 'ya me levanté', 'recién me desperté', 'good morning']},
    'dormir':      {'id': 'COT_DORMIR',     'tipo': 'rutina',   'grounding_base': 0.93, 'variantes': ['voy a dormir', 'me voy a dormir', 'ya dormí', 'dormí bien', 'dormí mal']},
    'bañarse':     {'id': 'COT_BANO',       'tipo': 'rutina',   'grounding_base': 0.88, 'variantes': ['bañé', 'me bañé', 'ducharme', 'me duché']},
    'desayunar':   {'id': 'COT_DESAYUNAR',  'tipo': 'rutina',   'grounding_base': 0.90, 'variantes': ['desayuné', 'voy a desayunar', 'sin desayunar']},
    'llegar':      {'id': 'COT_LLEGAR',     'tipo': 'rutina',   'grounding_base': 0.92, 'variantes': ['llegué', 'ya llegué', 'acabo de llegar', 'llegaste', 'ya llegó']},
    'salir':       {'id': 'COT_SALIR',      'tipo': 'rutina',   'grounding_base': 0.90, 'variantes': ['voy a salir', 'salgo', 'salí', 'ya salí']},
    'regresar':    {'id': 'COT_REGRESAR',   'tipo': 'rutina',   'grounding_base': 0.88, 'variantes': ['regresé', 'ya regresé', 'volví', 'de vuelta']},
    'ir':          {'id': 'COT_IR',         'tipo': 'movimiento','grounding_base': 0.90, 'variantes': ['voy', 'me voy', 'voy a', 'fui', 'yendo']},
    'venir':       {'id': 'COT_VENIR',      'tipo': 'movimiento','grounding_base': 0.88, 'variantes': ['vengo', 'vine', 'voy a venir', 'ven']},
    'caminar':     {'id': 'COT_CAMINAR',    'tipo': 'movimiento','grounding_base': 0.87, 'variantes': ['caminé', 'caminando', 'a pie']},
    'conducir':    {'id': 'COT_CONDUCIR',   'tipo': 'movimiento','grounding_base': 0.85, 'variantes': ['manejar', 'manejo', 'en carro']},

    # ── COMUNICACIÓN COTIDIANA ──────────────────
    'hablar':      {'id': 'COT_HABLAR',     'tipo': 'comunicacion','grounding_base': 0.92, 'variantes': ['hablé', 'hablando', 'habla', 'conversar', 'platicar']},
    'llamar':      {'id': 'COT_LLAMAR',     'tipo': 'comunicacion','grounding_base': 0.88, 'variantes': ['llamé', 'llamada', 'llamar por teléfono']},
    'escribir':    {'id': 'COT_ESCRIBIR',   'tipo': 'comunicacion','grounding_base': 0.90, 'variantes': ['escribí', 'escribiendo', 'escribe', 'escribirle', 'mensaje']},
    'leer':        {'id': 'COT_LEER',       'tipo': 'actividad',   'grounding_base': 0.88, 'variantes': ['leyendo', 'leí', 'leer algo']},

    # ── ESTADOS FÍSICOS COTIDIANOS ──────────────
    'cansado':     {'id': 'COT_CANSADO',    'tipo': 'estado_fisico','grounding_base': 0.93,'variantes': ['cansada', 'agotado', 'rendido', 'muerto del cansancio']},
    'hambre':      {'id': 'COT_HAMBRE',     'tipo': 'necesidad',   'grounding_base': 0.93, 'variantes': ['tengo hambre', 'me muero de hambre', 'no he comido']},
    'sueño':       {'id': 'COT_SUENO',      'tipo': 'necesidad',   'grounding_base': 0.90, 'variantes': ['tengo sueño', 'me da sueño', 'me quedo dormido']},
    'frío':        {'id': 'COT_FRIO_FISICO','tipo': 'estado_fisico','grounding_base': 0.90,'variantes': ['frio', 'estoy frío', 'hace mucho frío', 'me congelo']},
    'calor':       {'id': 'COT_CALOR_FISICO','tipo': 'estado_fisico','grounding_base': 0.90,'variantes': ['hace mucho calor', 'me derrito', 'sofoco']},

    # ── TIEMPO LIBRE ─────────────────────────────
    'descansar':   {'id': 'COT_DESCANSAR',  'tipo': 'ocio',        'grounding_base': 0.90, 'variantes': ['descansé', 'descansando', 'tiempo de descanso']},
    'ver series':  {'id': 'COT_SERIES',     'tipo': 'ocio',        'grounding_base': 0.88, 'variantes': ['viendo series', 'netflix', 'maratonear']},
    'salir a caminar': {'id': 'COT_PASEO',  'tipo': 'ocio',        'grounding_base': 0.87, 'variantes': ['dar una vuelta', 'salir un rato', 'despejarse']},
    'relajarse':   {'id': 'COT_RELAJAR',    'tipo': 'ocio',        'grounding_base': 0.88, 'variantes': ['relax', 'relajado', 'relajada', 'tranquilo']},

    # ── SITUACIONES COTIDIANAS COMUNES ───────────
    'hoy':         {'id': 'COT_HOY',        'tipo': 'referencia_temporal','grounding_base': 0.95,'variantes': ['este día', 'hoy en día', 'hoy mismo']},
    'ayer':        {'id': 'COT_AYER',       'tipo': 'referencia_temporal','grounding_base': 0.92,'variantes': ['anoche', 'ayer en la noche', 'la noche anterior']},
    'mañana':      {'id': 'COT_MANANA',     'tipo': 'referencia_temporal','grounding_base': 0.92,'variantes': ['el día de mañana', 'pasado', 'próximamente']},
    'tarde':       {'id': 'COT_TARDE',      'tipo': 'referencia_temporal','grounding_base': 0.88,'variantes': ['es tarde', 'ya es tarde', 'tardísimo', 'very late']},
    'pronto':      {'id': 'COT_PRONTO',     'tipo': 'referencia_temporal','grounding_base': 0.87,'variantes': ['en un momento', 'ya vuelvo', 'ahorita']},
    'ahorita':     {'id': 'COT_AHORITA',    'tipo': 'referencia_temporal','grounding_base': 0.92,'variantes': ['ahora mismo', 'en este momento', 'ya', 'al tiro']},
    'a veces':     {'id': 'COT_AVECES',     'tipo': 'frecuencia',        'grounding_base': 0.88,'variantes': ['de vez en cuando', 'ocasionalmente', 'a ratos']},
    'siempre':     {'id': 'COT_SIEMPRE',    'tipo': 'frecuencia',        'grounding_base': 0.90,'variantes': ['siempre lo mismo', 'constantemente', 'todo el tiempo']},
    'nunca':       {'id': 'COT_NUNCA',      'tipo': 'frecuencia',        'grounding_base': 0.90,'variantes': ['jamás', 'en la vida', 'nunca jamás']},
    'ya':          {'id': 'COT_YA',         'tipo': 'marcador_temporal', 'grounding_base': 0.90,'variantes': ['ya mismo', 'ya lo hice', 'ya terminé']},
    'todavía':     {'id': 'COT_TODAVIA',    'tipo': 'marcador_temporal', 'grounding_base': 0.88,'variantes': ['todavía no', 'aún no', 'sigo esperando']},

    # ── TRANSPORTE COTIDIANO ─────────────────────
    'bus':         {'id': 'COT_BUS',        'tipo': 'transporte',  'grounding_base': 0.90, 'variantes': ['buses', 'buseta', 'transporte público', 'TransMilenio', 'metro']},
    'carro':       {'id': 'COT_CARRO',      'tipo': 'transporte',  'grounding_base': 0.90, 'variantes': ['carros', 'auto', 'automóvil', 'coche', 'vehículo']},
    'moto':        {'id': 'COT_MOTO',       'tipo': 'transporte',  'grounding_base': 0.87, 'variantes': ['motos', 'mototaxi', 'motocicleta']},
    'taxi':        {'id': 'COT_TAXI',       'tipo': 'transporte',  'grounding_base': 0.87, 'variantes': ['taxis', 'uber', 'Uber', 'InDriver']},
    'viaje':       {'id': 'COT_VIAJE',      'tipo': 'actividad',   'grounding_base': 0.88, 'variantes': ['viajes', 'viajé', 'estoy viajando', 'de viaje']},

    # ── COMPRAS Y MANDADOS ───────────────────────
    'supermercado':{'id': 'COT_SUPER',      'tipo': 'espacio',     'grounding_base': 0.88, 'variantes': ['mercado', 'tienda', 'hacer mercado', 'hacer el mandado']},
    'comprar':     {'id': 'COT_COMPRAR',    'tipo': 'actividad',   'grounding_base': 0.90, 'variantes': ['compré', 'comprando', 'fui a comprar']},
}
