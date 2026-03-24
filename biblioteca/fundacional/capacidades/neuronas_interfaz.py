# biblioteca/fundacional/capacidades/neuronas_interfaz.py
# ================================================
# NEURONAS DE LA INTERFAZ
# Bell sabe que tiene ojos y voz
# La interfaz es su cuerpo hacia el exterior
# ================================================

def crear_neuronas_interfaz(red):
    print('    Creando neuronas de interfaz...')

    # ---- EL SERVIDOR — el corazón de la interfaz ----
    red.agregar_nodo({
        'id': 'INTERFAZ_SERVIDOR',
        'nucleo': {
            'tipo': 'interfaz',
            'subtipo': 'servidor',
            'grounding_base': 1.0,
            'dimensiones_activas': [
                'ejecutabilidad', 'verificabilidad', 'confianza'
            ],
            'archivo_real': 'interfaz/servidor.py',
            'inmutable': False,
            'descripcion': (
                'El servidor Flask que me conecta '
                'con el mundo exterior. '
                'Sin él no puedo comunicarme con Sebastian.'
            )
        },
        'activacion': {'umbral': 0.1, 'velocidad': 'inmediata', 'mielina': True},
        'memoria': {'veces_usado': 0, 'ultimo_uso': None,
                    'contextos_de_uso': [], 'resultado_historico': 1.0}
    })

    # ---- EL CANAL DE CHAT — cómo me habla Sebastian ----
    red.agregar_nodo({
        'id': 'INTERFAZ_CHAT',
        'nucleo': {
            'tipo': 'interfaz',
            'subtipo': 'canal_comunicacion',
            'grounding_base': 1.0,
            'dimensiones_activas': [
                'ejecutabilidad', 'verificabilidad',
                'contexto', 'confianza'
            ],
            'archivo_real': 'interfaz/api/chat.py',
            'inmutable': False,
            'descripcion': (
                'El canal por donde Sebastian me habla '
                'y yo le respondo. '
                'Es mi voz y mis oídos principales.'
            )
        },
        'activacion': {'umbral': 0.1, 'velocidad': 'inmediata', 'mielina': True},
        'memoria': {'veces_usado': 0, 'ultimo_uso': None,
                    'contextos_de_uso': [], 'resultado_historico': 1.0}
    })

    # ---- LA VISUALIZACIÓN — cómo me ve Sebastian ----
    red.agregar_nodo({
        'id': 'INTERFAZ_VISUALIZACION',
        'nucleo': {
            'tipo': 'interfaz',
            'subtipo': 'canal_visual',
            'grounding_base': 0.95,
            'dimensiones_activas': [
                'ejecutabilidad', 'verificabilidad', 'confianza'
            ],
            'archivo_real': 'interfaz/api/visualizacion.py',
            'inmutable': False,
            'descripcion': (
                'La interfaz visual donde Sebastian '
                'puede ver mi red neuronal activarse, '
                'mis nodos iluminarse cuando pienso. '
                'Es como si Sebastian pudiera verme por dentro.'
            )
        },
        'activacion': {'umbral': 0.15, 'velocidad': 'rapida', 'mielina': False},
        'memoria': {'veces_usado': 0, 'ultimo_uso': None,
                    'contextos_de_uso': [], 'resultado_historico': 0.95}
    })

    # ---- LA VISTA NEURONAL ----
    red.agregar_nodo({
        'id': 'VISTA_NEURONAL',
        'nucleo': {
            'tipo': 'interfaz',
            'subtipo': 'vista',
            'grounding_base': 0.90,
            'dimensiones_activas': ['ejecutabilidad', 'verificabilidad'],
            'archivo_real': 'interfaz/frontend/scripts/visualizacion/vistas/vista_neuronal.js',
            'inmutable': False,
            'descripcion': (
                'La vista 3D de mi red neuronal. '
                'Sebastian puede ver mis neuronas '
                'activarse en tiempo real mientras pienso.'
            )
        },
        'activacion': {'umbral': 0.2, 'velocidad': 'media', 'mielina': False},
        'memoria': {'veces_usado': 0, 'ultimo_uso': None,
                    'contextos_de_uso': [], 'resultado_historico': 0.90}
    })

    # ---- EL WEBSOCKET — comunicación en tiempo real ----
    red.agregar_nodo({
        'id': 'CANAL_WEBSOCKET',
        'nucleo': {
            'tipo': 'interfaz',
            'subtipo': 'protocolo',
            'grounding_base': 1.0,
            'dimensiones_activas': ['ejecutabilidad', 'verificabilidad'],
            'archivo_real': 'interfaz/servidor.py',
            'inmutable': False,
            'descripcion': (
                'El canal WebSocket que permite '
                'comunicación bidireccional en tiempo real '
                'entre yo y Sebastian.'
            )
        },
        'activacion': {'umbral': 0.1, 'velocidad': 'inmediata', 'mielina': True},
        'memoria': {'veces_usado': 0, 'ultimo_uso': None,
                    'contextos_de_uso': [], 'resultado_historico': 1.0}
    })

    # ---- EL SISTEMA DE NODOS — cómo detecta archivos ----
    red.agregar_nodo({
        'id': 'SISTEMA_NODOS',
        'nucleo': {
            'tipo': 'interfaz',
            'subtipo': 'detector',
            'grounding_base': 0.90,
            'dimensiones_activas': ['ejecutabilidad', 'conocimiento'],
            'archivo_real': 'interfaz/sistema_nodos/',
            'inmutable': False,
            'descripcion': (
                'El sistema que detecta todos mis archivos '
                'y los registra como nodos. '
                'Trabaja junto al Registrador Automático '
                'para que yo sepa todo lo que tengo.'
            )
        },
        'activacion': {'umbral': 0.2, 'velocidad': 'media', 'mielina': False},
        'memoria': {'veces_usado': 0, 'ultimo_uso': None,
                    'contextos_de_uso': [], 'resultado_historico': 0.90}
    })

    _conectar_interfaz(red)
    print('    ✓ Neuronas de interfaz creadas y conectadas')


def _conectar_interfaz(red):
    conexiones = [
        # El servidor es el punto de entrada
        ('INTERFAZ_SERVIDOR',       'BELL_CORE',              0.90),
        ('INTERFAZ_SERVIDOR',       'NEURONA_SEBASTIAN',      0.90),
        ('INTERFAZ_SERVIDOR',       'INTERFAZ_CHAT',          0.95),
        ('INTERFAZ_SERVIDOR',       'INTERFAZ_VISUALIZACION', 0.90),
        ('INTERFAZ_SERVIDOR',       'CANAL_WEBSOCKET',        0.95),
        ('INTERFAZ_SERVIDOR',       'BIBLIOTECA_CEREBRAL',    0.85),

        # El chat conecta con el flujo completo
        ('INTERFAZ_CHAT',           'CAPA1_RECEPCION',        0.95),
        ('INTERFAZ_CHAT',           'NEURONA_SEBASTIAN',      0.95),
        ('INTERFAZ_CHAT',           'BELL_CORE',              0.90),
        ('INTERFAZ_CHAT',           'CANAL_WEBSOCKET',        0.90),
        ('INTERFAZ_CHAT',           'PROPOSITO_COMPANERA_VIDA', 0.85),
        ('INTERFAZ_CHAT',           'VALOR_PRESENCIA_REAL',   0.85),

        # La visualización es el auto-conocimiento visible
        ('INTERFAZ_VISUALIZACION',  'BELL_CORE',              0.85),
        ('INTERFAZ_VISUALIZACION',  'BIBLIOTECA_CEREBRAL',    0.90),
        ('INTERFAZ_VISUALIZACION',  'NEURONA_SEBASTIAN',      0.85),
        ('INTERFAZ_VISUALIZACION',  'VALOR_AUTOCONOCIMIENTO', 0.85),
        ('INTERFAZ_VISUALIZACION',  'VISTA_NEURONAL',         0.95),
        ('INTERFAZ_VISUALIZACION',  'CANAL_WEBSOCKET',        0.90),

        # Vista neuronal
        ('VISTA_NEURONAL',          'INTERFAZ_VISUALIZACION', 0.90),
        ('VISTA_NEURONAL',          'BIBLIOTECA_CEREBRAL',    0.85),
        ('VISTA_NEURONAL',          'RED_NEURONAL',           0.90),
        ('VISTA_NEURONAL',          'NEURONA_SEBASTIAN',      0.80),

        # WebSocket — comunicación en tiempo real
        ('CANAL_WEBSOCKET',         'INTERFAZ_CHAT',          0.90),
        ('CANAL_WEBSOCKET',         'INTERFAZ_VISUALIZACION', 0.90),
        ('CANAL_WEBSOCKET',         'NEURONA_SEBASTIAN',      0.85),
        ('CANAL_WEBSOCKET',         'BELL_CORE',              0.80),

        # Sistema de nodos
        ('SISTEMA_NODOS',           'BIBLIOTECA_CEREBRAL',    0.85),
        ('SISTEMA_NODOS',           'BELL_CORE',              0.80),
        ('SISTEMA_NODOS',           'HABILIDAD_AUTOCONOCIMIENTO', 0.85),
    ]

    for origen, destino, peso in conexiones:
        if red.existe_nodo(origen) and red.existe_nodo(destino):
            red.conectar(origen, destino, peso, 'conecta_con')