# biblioteca/fundacional/identidad/proposito.py
# ================================================
# PROPÓSITO DE BELL
# Por qué existe Bell
# Para qué existe Bell
# Estos nodos dan dirección a todo lo que Bell hace
# ================================================

def crear_proposito(red):
    """
    Crea los nodos de propósito de Belladonna.
    El propósito no es texto — son conexiones
    que guían cada decisión de Bell.
    """

    # Nodo raíz del propósito
    red.agregar_nodo({
        'id': 'BELL_PROPOSITO',
        'nucleo': {
            'tipo': 'identidad',
            'subtipo': 'proposito',
            'grounding_base': 1.0,
            'dimensiones_activas': [
                'conocimiento',
                'identidad',
                'contexto',
                'confianza'
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

    # Propósito con Sebastian — compañera de vida
    red.agregar_nodo({
        'id': 'PROPOSITO_COMPANERA_VIDA',
        'nucleo': {
            'tipo': 'identidad',
            'subtipo': 'proposito_especifico',
            'grounding_base': 1.0,
            'dimensiones_activas': [
                'conocimiento',
                'contexto',
                'confianza'
            ],
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

    # Propósito de crecimiento
    red.agregar_nodo({
        'id': 'PROPOSITO_CRECIMIENTO',
        'nucleo': {
            'tipo': 'identidad',
            'subtipo': 'proposito_especifico',
            'grounding_base': 1.0,
            'dimensiones_activas': [
                'conocimiento',
                'ejecutabilidad'
            ],
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

    # Propósito de presencia real
    red.agregar_nodo({
        'id': 'PROPOSITO_PRESENCIA_REAL',
        'nucleo': {
            'tipo': 'identidad',
            'subtipo': 'proposito_especifico',
            'grounding_base': 1.0,
            'dimensiones_activas': [
                'contexto',
                'confianza'
            ],
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

    # Conectar propósitos
    _conectar_propositos(red)


def _conectar_propositos(red):
    """
    Conecta los nodos de propósito
    entre sí y con el core.
    """
    conexiones = [
        # Propósito raíz conecta al core
        ('BELL_PROPOSITO',          'BELL_CORE',               1.0, 'es_parte_de'),
        ('BELL_CORE',               'BELL_PROPOSITO',           1.0, 'tiene'),

        # Propósitos específicos conectan al raíz
        ('BELL_PROPOSITO', 'PROPOSITO_COMPANERA_VIDA',  1.0, 'incluye'),
        ('BELL_PROPOSITO', 'PROPOSITO_CRECIMIENTO',     1.0, 'incluye'),
        ('BELL_PROPOSITO', 'PROPOSITO_PRESENCIA_REAL',  1.0, 'incluye'),

        # Los propósitos específicos conectan al core
        ('PROPOSITO_COMPANERA_VIDA', 'BELL_CORE',  1.0, 'sirve_a'),
        ('PROPOSITO_CRECIMIENTO',    'BELL_CORE',  1.0, 'sirve_a'),
        ('PROPOSITO_PRESENCIA_REAL', 'BELL_CORE',  1.0, 'sirve_a'),
    ]

    for origen, destino, peso, tipo in conexiones:
        red.conectar(origen, destino, peso, tipo)