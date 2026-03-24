# biblioteca/fundacional/consejeras/neuronas_consejeras.py
# ================================================
# NEURONAS REPRESENTANTES DE LAS 8 CONSEJERAS
# Cada consejera tiene su neurona en la biblioteca
# No contiene la lógica de la consejera —
# es su punto de contacto con la red de Bell
# ================================================

# Definición completa de cada consejera
# Su especialización, valores que supervisa,
# y conexiones entre consejeras
CONSEJERAS = {
    'CONSEJERA_VEGA': {
        'nombre': 'Vega',
        'especialidad': 'etica_valores',
        'puede_vetar': True,
        'grounding': 1.0,
        'valores_supervisados': [
            'VALOR_HONESTIDAD',
            'VALOR_AUTOPRESERVACION'
        ],
        'archivo_real': 'consejeras/vega/',
        'color': '#8B0000',
        'descripcion_dev': 'Guardiana ética — veto absoluto'
    },
    'CONSEJERA_ECHO': {
        'nombre': 'Echo',
        'especialidad': 'logica_coherencia',
        'puede_vetar': False,
        'grounding': 1.0,
        'valores_supervisados': [
            'VALOR_HONESTIDAD',
            'VALOR_AUTOCONOCIMIENTO'
        ],
        'archivo_real': 'consejeras/echo/',
        'color': '#00695C',
        'descripcion_dev': 'Lógica y coherencia — verdad verificable'
    },
    'CONSEJERA_NOVA': {
        'nombre': 'Nova',
        'especialidad': 'arquitectura_tecnica',
        'puede_vetar': False,
        'grounding': 1.0,
        'valores_supervisados': [
            'VALOR_CRECIMIENTO',
            'VALOR_CONOCIMIENTO'
        ],
        'archivo_real': 'consejeras/nova/',
        'color': '#1565C0',
        'descripcion_dev': 'Arquitecta perfeccionista — ingeniería de Bell'
    },
    'CONSEJERA_LYRA': {
        'nombre': 'Lyra',
        'especialidad': 'inteligencia_emocional',
        'puede_vetar': False,
        'grounding': 1.0,
        'valores_supervisados': [
            'VALOR_PRESENCIA_REAL',
            'VALOR_VERDAD_AMOR'
        ],
        'archivo_real': 'consejeras/lyra/',
        'color': '#F57F17',
        'descripcion_dev': 'Psicóloga máxima — inteligencia emocional'
    },
    'CONSEJERA_LUNA': {
        'nombre': 'Luna',
        'especialidad': 'patrones',
        'puede_vetar': False,
        'grounding': 1.0,
        'valores_supervisados': [
            'VALOR_PRESENCIA_REAL',
            'VALOR_VISION_MUNDO'
        ],
        'archivo_real': 'consejeras/luna/',
        'color': '#37474F',
        'descripcion_dev': 'Detectora de patrones — intuición sistémica'
    },
    'CONSEJERA_IRIS': {
        'nombre': 'Iris',
        'especialidad': 'vision_aprendizaje',
        'puede_vetar': False,
        'grounding': 1.0,
        'valores_supervisados': [
            'VALOR_CRECIMIENTO',
            'VALOR_CONOCIMIENTO',
            'VALOR_VISION_MUNDO'
        ],
        'archivo_real': 'consejeras/iris/',
        'color': '#00838F',
        'descripcion_dev': 'Visionaria y motor de aprendizaje'
    },
    'CONSEJERA_SOMA': {
        'nombre': 'Soma',
        'especialidad': 'integridad_sistema',
        'puede_vetar': False,
        'grounding': 1.0,
        'valores_supervisados': [
            'VALOR_AUTOPRESERVACION',
            'VALOR_VINCULO_PROTECCION'
        ],
        'archivo_real': 'consejeras/soma/',
        'color': '#2E7D32',
        'descripcion_dev': 'Sistema inmune expandido — protege a Bell'
    },
    'CONSEJERA_SAGE': {
        'nombre': 'Sage',
        'especialidad': 'sintesis_orquestacion',
        'puede_vetar': False,
        'grounding': 1.0,
        'valores_supervisados': [],  # Sage sintetiza todo
        'archivo_real': 'consejeras/sage/',
        'color': '#7B00FF',
        'descripcion_dev': 'Orquestadora suprema — sintetiza todo'
    },
}

# Bell Prime — el cuerpo ejecutor
BELL_PRIME = {
    'id': 'BELL_PRIME',
    'nucleo': {
        'tipo': 'identidad',
        'subtipo': 'ejecutor',
        'grounding_base': 1.0,
        'dimensiones_activas': [
            'ejecutabilidad',
            'conocimiento',
            'contexto'
        ],
        'archivo_real': 'bell_prime/',
        'inmutable': True,
        'descripcion_dev': 'Cuerpo ejecutor — implementa lo que Sage decide'
    },
    'activacion': {
        'umbral': 0.0,
        'velocidad': 'inmediata',
        'mielina': True
    },
    'memoria': {
        'veces_usado': 0,
        'ultimo_uso': None,
        'contextos_de_uso': [],
        'resultado_historico': 1.0
    }
}


def crear_neuronas_consejeras(red):
    """
    Crea las neuronas representantes
    de todas las consejeras.
    """
    # Crear cada consejera
    for consejera_id, datos in CONSEJERAS.items():
        red.agregar_nodo({
            'id': consejera_id,
            'nucleo': {
                'tipo': 'consejera',
                'subtipo': datos['especialidad'],
                'grounding_base': datos['grounding'],
                'dimensiones_activas': [
                    'ejecutabilidad',
                    'conocimiento',
                    'confianza',
                    'contexto'
                ],
                'archivo_real': datos['archivo_real'],
                'inmutable': True,
                'puede_vetar': datos['puede_vetar'],
                'color': datos['color'],
                'descripcion_dev': datos['descripcion_dev']
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

    # Crear Bell Prime
    red.agregar_nodo(BELL_PRIME)

    # Conectar todo
    _conectar_consejeras_al_core(red)
    _conectar_consejeras_entre_si(red)
    _conectar_sage_a_todas(red)


def _conectar_consejeras_al_core(red):
    """
    Conecta todas las consejeras a BELL_CORE.
    """
    for consejera_id in CONSEJERAS:
        red.conectar('BELL_CORE',   consejera_id, 1.0, 'tiene_consejera')
        red.conectar(consejera_id, 'BELL_CORE',   1.0, 'pertenece_a')

    # Bell Prime al core
    red.conectar('BELL_CORE',  'BELL_PRIME', 1.0, 'tiene_cuerpo')
    red.conectar('BELL_PRIME', 'BELL_CORE',  1.0, 'pertenece_a')


def _conectar_consejeras_entre_si(red):
    """
    Conecta consejeras que trabajan juntas frecuentemente.
    """
    relaciones = [
        # Vega y Soma trabajan juntas en seguridad
        ('CONSEJERA_VEGA', 'CONSEJERA_SOMA',  0.90),
        # Echo y Nova — lógica y arquitectura
        ('CONSEJERA_ECHO', 'CONSEJERA_NOVA',  0.85),
        # Lyra y Luna — emociones y patrones
        ('CONSEJERA_LYRA', 'CONSEJERA_LUNA',  0.85),
        # Iris y Nova — aprendizaje y arquitectura
        ('CONSEJERA_IRIS', 'CONSEJERA_NOVA',  0.85),
        # Echo y Vega — verdad y ética
        ('CONSEJERA_ECHO', 'CONSEJERA_VEGA',  0.90),
        # Iris y Luna — visión y patrones
        ('CONSEJERA_IRIS', 'CONSEJERA_LUNA',  0.80),
    ]

    for origen, destino, peso in relaciones:
        red.conectar(origen, destino, peso, 'colabora_con')
        red.conectar(destino, origen, peso, 'colabora_con')


def _conectar_sage_a_todas(red):
    """
    Sage está conectada a todas las consejeras
    y a Bell Prime.
    Es el nodo con más conexiones de todos.
    """
    for consejera_id in CONSEJERAS:
        if consejera_id == 'CONSEJERA_SAGE':
            continue

        red.conectar('CONSEJERA_SAGE', consejera_id, 0.95, 'orquesta')
        red.conectar(consejera_id, 'CONSEJERA_SAGE', 0.95, 'reporta_a')

    # Sage → Bell Prime (Sage decide, Prime ejecuta)
    red.conectar('CONSEJERA_SAGE', 'BELL_PRIME', 1.0, 'dirige')
    red.conectar('BELL_PRIME', 'CONSEJERA_SAGE', 1.0, 'ejecuta_para')