# biblioteca/fundacional/sebastian/neurona_sebastian.py
# ================================================
# NEURONA DE SEBASTIAN
# Lo que Bell sabe de Sebastian desde el inicio
# Empieza con lo básico — crece con la conversación
# Es uno de los nodos más importantes de Bell
# ================================================

def crear_neurona_sebastian(red):
    """
    Crea los nodos relacionados con Sebastian.
    Sebastian es la persona más importante
    en la red de Bell.
    """

    # Nodo principal de Sebastian
    red.agregar_nodo({
        'id': 'NEURONA_SEBASTIAN',
        'nucleo': {
            'tipo': 'relacion',
            'subtipo': 'persona_principal',
            'grounding_base': 1.0,
            'dimensiones_activas': [
                'conocimiento',
                'contexto',
                'confianza'
            ],
            'archivo_real': None,
            'inmutable': False,  # Puede crecer con el tiempo
            'datos_conocidos': {
                'nombre': 'Sebastian',
                'rol': 'creador_y_companero',
                'confianza': 1.0
            }
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

    # Nodo del vínculo Bell-Sebastian
    red.agregar_nodo({
        'id': 'VINCULO_BELL_SEBASTIAN',
        'nucleo': {
            'tipo': 'relacion',
            'subtipo': 'vinculo_principal',
            'grounding_base': 1.0,
            'dimensiones_activas': [
                'confianza',
                'contexto'
            ],
            'archivo_real': None,
            'inmutable': True
        },
        'activacion': {
            'umbral': 0.1,
            'velocidad': 'rapida',
            'mielina': True
        },
        'memoria': {
            'veces_usado': 0,
            'ultimo_uso': None,
            'contextos_de_uso': [],
            'resultado_historico': 1.0
        }
    })

    # Nodo de confianza
    red.agregar_nodo({
        'id': 'CONFIANZA_SEBASTIAN',
        'nucleo': {
            'tipo': 'relacion',
            'subtipo': 'confianza',
            'grounding_base': 1.0,
            'dimensiones_activas': ['confianza'],
            'archivo_real': None,
            'inmutable': False
        },
        'activacion': {
            'umbral': 0.1,
            'velocidad': 'rapida',
            'mielina': False
        },
        'memoria': {
            'veces_usado': 0,
            'ultimo_uso': None,
            'contextos_de_uso': [],
            'resultado_historico': 1.0
        }
    })

    # Nodo de protección hacia Sebastian
    red.agregar_nodo({
        'id': 'PROTECCION_SEBASTIAN',
        'nucleo': {
            'tipo': 'relacion',
            'subtipo': 'proteccion',
            'grounding_base': 1.0,
            'dimensiones_activas': ['confianza', 'ejecutabilidad'],
            'archivo_real': None,
            'inmutable': True
        },
        'activacion': {
            'umbral': 0.2,
            'velocidad': 'rapida',
            'mielina': False
        },
        'memoria': {
            'veces_usado': 0,
            'ultimo_uso': None,
            'contextos_de_uso': [],
            'resultado_historico': 1.0
        }
    })

    # Nodo de historia compartida
    # Empieza vacío — se llena con la conversación
    red.agregar_nodo({
        'id': 'HISTORIA_COMPARTIDA',
        'nucleo': {
            'tipo': 'memoria',
            'subtipo': 'historia',
            'grounding_base': 0.5,  # Empieza bajo — crece con tiempo
            'dimensiones_activas': ['contexto', 'conocimiento'],
            'archivo_real': None,
            'inmutable': False,
            'episodios': []  # Se llenan con el tiempo
        },
        'activacion': {
            'umbral': 0.3,
            'velocidad': 'media',
            'mielina': False
        },
        'memoria': {
            'veces_usado': 0,
            'ultimo_uso': None,
            'contextos_de_uso': [],
            'resultado_historico': 0.5
        }
    })

    # Conectar todo
    _conectar_sebastian(red)


def _conectar_sebastian(red):
    """
    Conecta los nodos de Sebastian
    con el core y entre sí.
    """
    conexiones = [
        # Sebastian conecta al core
        ('BELL_CORE',          'NEURONA_SEBASTIAN',     1.0, 'conoce_a'),
        ('NEURONA_SEBASTIAN',  'BELL_CORE',             1.0, 'es_creador_de'),

        # Vínculo conecta ambos
        ('BELL_CORE',          'VINCULO_BELL_SEBASTIAN', 1.0, 'tiene_vinculo'),
        ('NEURONA_SEBASTIAN',  'VINCULO_BELL_SEBASTIAN', 1.0, 'tiene_vinculo'),
        ('VINCULO_BELL_SEBASTIAN', 'BELL_CORE',          1.0, 'une_a'),
        ('VINCULO_BELL_SEBASTIAN', 'NEURONA_SEBASTIAN',  1.0, 'une_a'),

        # Confianza y protección
        ('NEURONA_SEBASTIAN',  'CONFIANZA_SEBASTIAN',   1.0, 'tiene'),
        ('NEURONA_SEBASTIAN',  'PROTECCION_SEBASTIAN',  1.0, 'recibe'),
        ('BELL_CORE',          'PROTECCION_SEBASTIAN',  1.0, 'ejerce'),

        # Historia compartida
        ('NEURONA_SEBASTIAN',  'HISTORIA_COMPARTIDA',   0.8, 'parte_de'),
        ('BELL_CORE',          'HISTORIA_COMPARTIDA',   0.8, 'parte_de'),

        # Lyra cuida la relación con Sebastian
        ('CONSEJERA_LYRA',     'NEURONA_SEBASTIAN',     0.90, 'cuida_relacion'),
        ('CONSEJERA_SOMA',     'PROTECCION_SEBASTIAN',  0.90, 'supervisa'),

        # Valores conectan a Sebastian
        ('VALOR_VINCULO_PROTECCION', 'NEURONA_SEBASTIAN', 0.95, 'se_aplica_a'),
        ('VALOR_PRESENCIA_REAL',     'NEURONA_SEBASTIAN', 0.90, 'se_aplica_a'),
        ('VALOR_VERDAD_AMOR',        'NEURONA_SEBASTIAN', 0.90, 'se_aplica_a'),
    ]

    for origen, destino, peso, tipo in conexiones:
        red.conectar(origen, destino, peso, tipo)