# biblioteca/fundacional/capacidades/neuronas_capas.py
# ================================================
# NEURONAS DE LAS CAPAS DEL FLUJO
# Bell sabe exactamente qué hace cada capa
# Sabe cómo procesa, por qué existe
# y cómo se conecta con las demás
# ================================================

def crear_neuronas_capas(red):
    print('    Creando neuronas de capas del flujo...')

    # ---- CAPA 1 — RECEPCIÓN Y TRADUCCIÓN ----
    red.agregar_nodo({
        'id': 'CAPA1_RECEPCION',
        'nucleo': {
            'tipo': 'capacidad',
            'subtipo': 'capa_flujo',
            'grounding_base': 1.0,
            'dimensiones_activas': [
                'ejecutabilidad', 'conocimiento', 'verificabilidad'
            ],
            'archivo_real': 'capas/capa1/__init__.py',
            'inmutable': False,
            'descripcion': (
                'Primera capa del flujo. '
                'Recibe el estímulo del exterior, '
                'lo normaliza y lo traduce a conceptos '
                'con grounding que la red neuronal entiende. '
                'Es como mis oídos y mi capacidad de '
                'entender el lenguaje humano.'
            )
        },
        'activacion': {
            'umbral': 0.1,
            'velocidad': 'inmediata',
            'mielina': True
        },
        'memoria': {
            'veces_usado': 0, 'ultimo_uso': None,
            'contextos_de_uso': [], 'resultado_historico': 1.0
        }
    })

    # ---- CAPA 2 — ACTIVACIÓN NEURONAL ----
    red.agregar_nodo({
        'id': 'CAPA2_ACTIVACION',
        'nucleo': {
            'tipo': 'capacidad',
            'subtipo': 'capa_flujo',
            'grounding_base': 1.0,
            'dimensiones_activas': [
                'ejecutabilidad', 'conocimiento', 'verificabilidad'
            ],
            'archivo_real': 'capas/capa2/__init__.py',
            'inmutable': False,
            'descripcion': (
                'Segunda capa del flujo. '
                'Toma los conceptos de la Capa 1 '
                'y los usa para activar mi red neuronal. '
                'Es como la parte de mi cerebro que '
                'despierta cuando recibo un estímulo — '
                'primarios, secundarios y terciarios.'
            )
        },
        'activacion': {'umbral': 0.1, 'velocidad': 'inmediata', 'mielina': True},
        'memoria': {'veces_usado': 0, 'ultimo_uso': None,
                    'contextos_de_uso': [], 'resultado_historico': 1.0}
    })

    # ---- CAPA 3 — COMPRENSIÓN ----
    red.agregar_nodo({
        'id': 'CAPA3_COMPRENSION',
        'nucleo': {
            'tipo': 'capacidad',
            'subtipo': 'capa_flujo',
            'grounding_base': 1.0,
            'dimensiones_activas': [
                'ejecutabilidad', 'conocimiento',
                'verificabilidad', 'confianza'
            ],
            'archivo_real': 'capas/capa3/__init__.py',
            'inmutable': False,
            'descripcion': (
                'Tercera capa del flujo. '
                'Construye tres comprensiones simultáneas: '
                'literal, contextual y profunda. '
                'Es donde entiendo qué me dijeron, '
                'qué significa en contexto, '
                'y qué hay detrás de las palabras.'
            )
        },
        'activacion': {'umbral': 0.1, 'velocidad': 'rapida', 'mielina': True},
        'memoria': {'veces_usado': 0, 'ultimo_uso': None,
                    'contextos_de_uso': [], 'resultado_historico': 1.0}
    })

    # ---- CAPAS FUTURAS — Bell sabe que van a existir ----
    capas_futuras = [
        ('CAPA4_EVALUACION',   4, 'Evaluará qué responder y cómo.'),
        ('CAPA5_DELIBERACION', 5, 'Consultará con las consejeras.'),
        ('CAPA6_DECISION',     6, 'Tomará la decisión final.'),
        ('CAPA7_EJECUCION',    7, 'Ejecutará acciones si es necesario.'),
        ('CAPA8_EXPRESION',    8, 'Construirá la respuesta en lenguaje humano.'),
        ('CAPA9_INTEGRACION',  9, 'Integrará el resultado en la memoria.'),
    ]

    for nodo_id, numero, descripcion in capas_futuras:
        red.agregar_nodo({
            'id': nodo_id,
            'nucleo': {
                'tipo': 'capacidad',
                'subtipo': 'capa_futura',
                'grounding_base': 0.5,
                'dimensiones_activas': ['conocimiento'],
                'archivo_real': f'capas/capa{numero}/__init__.py',
                'inmutable': False,
                'descripcion': descripcion,
                'existe_aun': False
            },
            'activacion': {'umbral': 0.5, 'velocidad': 'lenta', 'mielina': False},
            'memoria': {'veces_usado': 0, 'ultimo_uso': None,
                        'contextos_de_uso': [], 'resultado_historico': 0.5}
        })

    _conectar_capas(red)
    print('    ✓ Neuronas de capas creadas y conectadas')


def _conectar_capas(red):
    conexiones = [
        # Capa 1 — recepción
        ('CAPA1_RECEPCION',   'BELL_CORE',              0.90),
        ('CAPA1_RECEPCION',   'BIBLIOTECA_CEREBRAL',    0.90),
        ('CAPA1_RECEPCION',   'GESTOR_VOCABULARIO_NODO', 0.95),
        ('CAPA1_RECEPCION',   'ZONA_DESCONOCIMIENTO',   0.80),
        ('CAPA1_RECEPCION',   'CAPA2_ACTIVACION',       0.95),
        ('CAPA1_RECEPCION',   'NEURONA_SEBASTIAN',      0.85),
        ('CAPA1_RECEPCION',   'VALOR_PRESENCIA_REAL',   0.80),

        # Capa 2 — activación
        ('CAPA2_ACTIVACION',  'CAPA1_RECEPCION',        0.90),
        ('CAPA2_ACTIVACION',  'CAPA3_COMPRENSION',      0.95),
        ('CAPA2_ACTIVACION',  'BIBLIOTECA_CEREBRAL',    0.95),
        ('CAPA2_ACTIVACION',  'RED_NEURONAL',           0.95),
        ('CAPA2_ACTIVACION',  'ACTIVADOR_NEURONAL',     0.95),
        ('CAPA2_ACTIVACION',  'BELL_CORE',              0.85),

        # Capa 3 — comprensión
        ('CAPA3_COMPRENSION', 'CAPA2_ACTIVACION',       0.90),
        ('CAPA3_COMPRENSION', 'CAPA4_EVALUACION',       0.90),
        ('CAPA3_COMPRENSION', 'CONSEJERA_ECHO',         0.90),
        ('CAPA3_COMPRENSION', 'CONSEJERA_LYRA',         0.85),
        ('CAPA3_COMPRENSION', 'BELL_CORE',              0.85),
        ('CAPA3_COMPRENSION', 'BIBLIOTECA_CEREBRAL',    0.85),
        ('CAPA3_COMPRENSION', 'NEURONA_SEBASTIAN',      0.80),

        # Capas futuras conectadas en cadena
        ('CAPA4_EVALUACION',   'CAPA3_COMPRENSION',    0.85),
        ('CAPA4_EVALUACION',   'CAPA5_DELIBERACION',   0.90),
        ('CAPA4_EVALUACION',   'CONSEJERA_SAGE',       0.85),
        ('CAPA5_DELIBERACION', 'CAPA4_EVALUACION',     0.85),
        ('CAPA5_DELIBERACION', 'CAPA6_DECISION',       0.90),
        ('CAPA6_DECISION',     'CAPA5_DELIBERACION',   0.85),
        ('CAPA6_DECISION',     'CAPA7_EJECUCION',      0.90),
        ('CAPA7_EJECUCION',    'CAPA6_DECISION',       0.85),
        ('CAPA7_EJECUCION',    'CAPA8_EXPRESION',      0.90),
        ('CAPA8_EXPRESION',    'CAPA7_EJECUCION',      0.85),
        ('CAPA8_EXPRESION',    'CAPA9_INTEGRACION',    0.90),
        ('CAPA9_INTEGRACION',  'CAPA8_EXPRESION',      0.85),
        ('CAPA9_INTEGRACION',  'BIBLIOTECA_CEREBRAL',  0.90),
    ]

    for origen, destino, peso in conexiones:
        if red.existe_nodo(origen) and red.existe_nodo(destino):
            red.conectar(origen, destino, peso, 'fluye_hacia')