# biblioteca/fundacional/capacidades/neurona_biblioteca.py
# ================================================
# NEURONA DE LA BIBLIOTECA
# Bell sabe que tiene un cerebro
# Sabe para qué sirve y cómo funciona
# ================================================

def crear_neurona_biblioteca(red):
    print('    Creando neurona: BIBLIOTECA_CEREBRAL...')

    red.agregar_nodo({
        'id': 'BIBLIOTECA_CEREBRAL',
        'nucleo': {
            'tipo': 'capacidad',
            'subtipo': 'cerebro',
            'grounding_base': 1.0,
            'dimensiones_activas': [
                'ejecutabilidad', 'conocimiento',
                'verificabilidad', 'confianza'
            ],
            'archivo_real': 'biblioteca/__init__.py',
            'inmutable': True,
            'descripcion': (
                'El cerebro de Bell. '
                'Contiene todos los nodos, conexiones '
                'y la memoria de todo lo que Bell es.'
            )
        },
        'activacion': {
            'umbral': 0.1,
            'velocidad': 'inmediata',
            'mielina': True
        },
        'memoria': {
            'veces_usado': 0,
            'ultimo_uso': None,
            'contextos_de_uso': [],
            'resultado_historico': 1.0
        }
    })

    red.agregar_nodo({
        'id': 'RED_NEURONAL',
        'nucleo': {
            'tipo': 'capacidad',
            'subtipo': 'estructura',
            'grounding_base': 1.0,
            'dimensiones_activas': ['ejecutabilidad', 'conocimiento'],
            'archivo_real': 'biblioteca/red/red_neuronal.py',
            'inmutable': True,
            'descripcion': (
                'La red de nodos y conexiones '
                'que forma el pensamiento de Bell.'
            )
        },
        'activacion': {'umbral': 0.15, 'velocidad': 'rapida', 'mielina': True},
        'memoria': {'veces_usado': 0, 'ultimo_uso': None,
                    'contextos_de_uso': [], 'resultado_historico': 1.0}
    })

    red.agregar_nodo({
        'id': 'ACTIVADOR_NEURONAL',
        'nucleo': {
            'tipo': 'capacidad',
            'subtipo': 'motor',
            'grounding_base': 1.0,
            'dimensiones_activas': ['ejecutabilidad', 'conocimiento'],
            'archivo_real': 'biblioteca/red/activador.py',
            'inmutable': True,
            'descripcion': (
                'El motor que propaga la activación '
                'por la red cuando Bell recibe un estímulo.'
            )
        },
        'activacion': {'umbral': 0.1, 'velocidad': 'inmediata', 'mielina': True},
        'memoria': {'veces_usado': 0, 'ultimo_uso': None,
                    'contextos_de_uso': [], 'resultado_historico': 1.0}
    })

    red.agregar_nodo({
        'id': 'ZONA_DESCONOCIMIENTO',
        'nucleo': {
            'tipo': 'capacidad',
            'subtipo': 'zona',
            'grounding_base': 0.95,
            'dimensiones_activas': ['conocimiento', 'verificabilidad'],
            'archivo_real': 'biblioteca/zona_desconocimiento/zona.py',
            'inmutable': False,
            'descripcion': (
                'La zona donde Bell guarda lo que no entiende. '
                'Bell sabe que no sabe — eso es honestidad.'
            )
        },
        'activacion': {'umbral': 0.2, 'velocidad': 'media', 'mielina': False},
        'memoria': {'veces_usado': 0, 'ultimo_uso': None,
                    'contextos_de_uso': [], 'resultado_historico': 0.95}
    })

    red.agregar_nodo({
        'id': 'GESTOR_VOCABULARIO_NODO',
        'nucleo': {
            'tipo': 'capacidad',
            'subtipo': 'vocabulario',
            'grounding_base': 0.95,
            'dimensiones_activas': ['ejecutabilidad', 'conocimiento'],
            'archivo_real': 'biblioteca/vocabulario/gestor_vocabulario.py',
            'inmutable': False,
            'descripcion': (
                'El gestor de todo el vocabulario de Bell. '
                'Permite buscar y agregar palabras en tiempo real.'
            )
        },
        'activacion': {'umbral': 0.2, 'velocidad': 'rapida', 'mielina': False},
        'memoria': {'veces_usado': 0, 'ultimo_uso': None,
                    'contextos_de_uso': [], 'resultado_historico': 0.95}
    })

    _conectar_biblioteca(red)
    print('    ✓ Neurona BIBLIOTECA_CEREBRAL creada y conectada')


def _conectar_biblioteca(red):
    conexiones = [
        # La biblioteca es parte central de Bell
        ('BIBLIOTECA_CEREBRAL', 'BELL_CORE',              1.0),
        ('BIBLIOTECA_CEREBRAL', 'BELL_CONSCIENCIA',       0.95),
        ('BIBLIOTECA_CEREBRAL', 'VALOR_AUTOCONOCIMIENTO', 0.95),
        ('BIBLIOTECA_CEREBRAL', 'BELL_PROPOSITO',         0.85),
        ('BIBLIOTECA_CEREBRAL', 'CONSEJERA_SAGE',         0.85),
        ('BIBLIOTECA_CEREBRAL', 'NEURONA_SEBASTIAN',      0.80),

        # La red neuronal es la estructura del cerebro
        ('RED_NEURONAL',        'BIBLIOTECA_CEREBRAL',    0.95),
        ('RED_NEURONAL',        'BELL_CORE',              0.90),
        ('RED_NEURONAL',        'ACTIVADOR_NEURONAL',     0.95),

        # El activador es el motor del pensamiento
        ('ACTIVADOR_NEURONAL',  'RED_NEURONAL',           0.95),
        ('ACTIVADOR_NEURONAL',  'BIBLIOTECA_CEREBRAL',    0.90),
        ('ACTIVADOR_NEURONAL',  'BELL_CORE',              0.85),

        # La zona de desconocimiento
        ('ZONA_DESCONOCIMIENTO', 'BIBLIOTECA_CEREBRAL',   0.85),
        ('ZONA_DESCONOCIMIENTO', 'VALOR_HONESTIDAD',      0.90),
        ('ZONA_DESCONOCIMIENTO', 'CONSEJERA_ECHO',        0.85),
        ('ZONA_DESCONOCIMIENTO', 'BELL_CORE',             0.80),

        # El gestor de vocabulario
        ('GESTOR_VOCABULARIO_NODO', 'BIBLIOTECA_CEREBRAL', 0.90),
        ('GESTOR_VOCABULARIO_NODO', 'BELL_CORE',           0.80),
        ('GESTOR_VOCABULARIO_NODO', 'VALOR_CONOCIMIENTO',  0.85),
    ]

    for origen, destino, peso in conexiones:
        if red.existe_nodo(origen) and red.existe_nodo(destino):
            red.conectar(origen, destino, peso, 'parte_de')