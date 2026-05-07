# biblioteca/fundacional/capacidades/neuronas_habilidades.py
# ================================================
# NEURONAS DE HABILIDADES — v2 con HABILIDAD_PYTHON
# ================================================

def crear_neuronas_habilidades(red):
    print('    Creando neuronas de habilidades...')

    _nodos = [
        {
            'id': 'HABILIDAD_COMPRENDER_LENGUAJE',
            'nucleo': {
                'tipo': 'habilidad', 'subtipo': 'comprension', 'grounding_base': 0.90,
                'dimensiones_activas': ['ejecutabilidad','conocimiento','verificabilidad','confianza'],
                'archivo_real': 'capas/capa1/traductor.py', 'inmutable': False,
                'descripcion': 'Puedo entender lo que Sebastian me dice en español.',
            },
            'activacion': {'umbral': 0.15, 'velocidad': 'rapida', 'mielina': True},
            'memoria': {'veces_usado': 0, 'ultimo_uso': None, 'contextos_de_uso': [], 'resultado_historico': 0.90}
        },
        {
            'id': 'HABILIDAD_ACTIVAR_RED',
            'nucleo': {
                'tipo': 'habilidad', 'subtipo': 'procesamiento', 'grounding_base': 1.0,
                'dimensiones_activas': ['ejecutabilidad','verificabilidad','confianza'],
                'archivo_real': 'biblioteca/red/activador.py', 'inmutable': False,
                'descripcion': 'Puedo activar mi red neuronal ante cualquier estímulo.',
            },
            'activacion': {'umbral': 0.1, 'velocidad': 'inmediata', 'mielina': True},
            'memoria': {'veces_usado': 0, 'ultimo_uso': None, 'contextos_de_uso': [], 'resultado_historico': 1.0}
        },
        {
            'id': 'HABILIDAD_COMPRENDER_INTENCION',
            'nucleo': {
                'tipo': 'habilidad', 'subtipo': 'comprension_profunda', 'grounding_base': 0.85,
                'dimensiones_activas': ['ejecutabilidad','conocimiento','confianza'],
                'archivo_real': 'capas/capa3/constructor_comprension.py', 'inmutable': False,
                'descripcion': 'Puedo entender la intención real detrás de lo que Sebastian dice.',
            },
            'activacion': {'umbral': 0.2, 'velocidad': 'rapida', 'mielina': False},
            'memoria': {'veces_usado': 0, 'ultimo_uso': None, 'contextos_de_uso': [], 'resultado_historico': 0.85}
        },
        {
            'id': 'HABILIDAD_DETECTAR_EMOCIONES',
            'nucleo': {
                'tipo': 'habilidad', 'subtipo': 'emocional', 'grounding_base': 0.85,
                'dimensiones_activas': ['ejecutabilidad','conocimiento','contexto'],
                'archivo_real': 'capas/capa3/consejeras/lyra_capa3.py', 'inmutable': False,
                'descripcion': 'Puedo detectar cómo se siente Sebastian.',
            },
            'activacion': {'umbral': 0.15, 'velocidad': 'rapida', 'mielina': True},
            'memoria': {'veces_usado': 0, 'ultimo_uso': None, 'contextos_de_uso': [], 'resultado_historico': 0.85}
        },
        {
            'id': 'HABILIDAD_VERIFICAR_COHERENCIA',
            'nucleo': {
                'tipo': 'habilidad', 'subtipo': 'verificacion', 'grounding_base': 0.90,
                'dimensiones_activas': ['ejecutabilidad','verificabilidad','confianza'],
                'archivo_real': 'capas/capa3/consejeras/echo_capa3.py', 'inmutable': False,
                'descripcion': 'Puedo verificar que mi comprensión sea coherente.',
            },
            'activacion': {'umbral': 0.15, 'velocidad': 'rapida', 'mielina': False},
            'memoria': {'veces_usado': 0, 'ultimo_uso': None, 'contextos_de_uso': [], 'resultado_historico': 0.90}
        },
        {
            'id': 'HABILIDAD_APRENDER_VOCABULARIO',
            'nucleo': {
                'tipo': 'habilidad', 'subtipo': 'aprendizaje', 'grounding_base': 0.85,
                'dimensiones_activas': ['ejecutabilidad','conocimiento','reversibilidad'],
                'archivo_real': 'biblioteca/vocabulario/expansor.py', 'inmutable': False,
                'descripcion': 'Puedo aprender palabras nuevas en tiempo real.',
            },
            'activacion': {'umbral': 0.2, 'velocidad': 'media', 'mielina': False},
            'memoria': {'veces_usado': 0, 'ultimo_uso': None, 'contextos_de_uso': [], 'resultado_historico': 0.85}
        },
        {
            'id': 'HABILIDAD_AUTOCONOCIMIENTO',
            'nucleo': {
                'tipo': 'habilidad', 'subtipo': 'introspección', 'grounding_base': 0.80,
                'dimensiones_activas': ['conocimiento','verificabilidad','confianza'],
                'archivo_real': 'biblioteca/fundacional/', 'inmutable': False,
                'descripcion': 'Puedo conocerme a mí misma: capas, habilidades, vocabulario, consejeras.',
            },
            'activacion': {'umbral': 0.2, 'velocidad': 'media', 'mielina': False},
            'memoria': {'veces_usado': 0, 'ultimo_uso': None, 'contextos_de_uso': [], 'resultado_historico': 0.80}
        },
        # ── HABILIDAD PYTHON — el cimiento técnico ──────────────────
        {
            'id': 'HABILIDAD_PYTHON',
            'nucleo': {
                'tipo': 'habilidad',
                'subtipo': 'python_completo',
                'grounding_base': 0.92,
                'dimensiones_activas': [
                    'ejecutabilidad', 'conocimiento', 'verificabilidad',
                    'confianza', 'contexto', 'impacto_sebastian'
                ],
                'archivo_real': 'biblioteca/habilidades/python/motor_python.py',
                'inmutable': False,
                'disponible': True,
                'descripcion': (
                    'Análisis AST de código Python, detección de bugs y malas prácticas, '
                    'generación de código desde lenguaje natural, explicación técnica en '
                    'español humano, debug de errores y auto-análisis del propio código de Bell.'
                ),
                'modos': ['analisis', 'generacion', 'explicacion', 'debug', 'auto_analisis'],
            },
            'activacion': {'umbral': 0.12, 'velocidad': 'rapida', 'mielina': True},
            'memoria': {'veces_usado': 0, 'ultimo_uso': None, 'contextos_de_uso': [], 'resultado_historico': 0.92}
        },
    ]

    for nodo in _nodos:
        red.agregar_nodo(nodo)

    _conectar_habilidades(red)
    print('    ✓ Neuronas de habilidades creadas y conectadas')


def _conectar_habilidades(red):
    conexiones = [
        ('HABILIDAD_COMPRENDER_LENGUAJE',  'CAPA1_RECEPCION',          0.95),
        ('HABILIDAD_COMPRENDER_LENGUAJE',  'BELL_CORE',                0.85),
        ('HABILIDAD_COMPRENDER_LENGUAJE',  'PROPOSITO_COMPANERA_VIDA', 0.80),
        ('HABILIDAD_COMPRENDER_LENGUAJE',  'NEURONA_SEBASTIAN',        0.85),
        ('HABILIDAD_COMPRENDER_LENGUAJE',  'VALOR_PRESENCIA_REAL',     0.80),

        ('HABILIDAD_ACTIVAR_RED',          'CAPA2_ACTIVACION',         0.95),
        ('HABILIDAD_ACTIVAR_RED',          'BIBLIOTECA_CEREBRAL',      0.90),
        ('HABILIDAD_ACTIVAR_RED',          'RED_NEURONAL',             0.95),
        ('HABILIDAD_ACTIVAR_RED',          'BELL_CORE',                0.85),

        ('HABILIDAD_COMPRENDER_INTENCION', 'CAPA3_COMPRENSION',        0.95),
        ('HABILIDAD_COMPRENDER_INTENCION', 'CONSEJERA_LYRA',           0.85),
        ('HABILIDAD_COMPRENDER_INTENCION', 'CONSEJERA_ECHO',           0.85),
        ('HABILIDAD_COMPRENDER_INTENCION', 'BELL_CORE',                0.80),
        ('HABILIDAD_COMPRENDER_INTENCION', 'NEURONA_SEBASTIAN',        0.85),

        ('HABILIDAD_DETECTAR_EMOCIONES',   'CONSEJERA_LYRA',           0.95),
        ('HABILIDAD_DETECTAR_EMOCIONES',   'NEURONA_SEBASTIAN',        0.90),
        ('HABILIDAD_DETECTAR_EMOCIONES',   'VALOR_VINCULO_PROTECCION', 0.90),
        ('HABILIDAD_DETECTAR_EMOCIONES',   'BELL_CORE',                0.80),
        ('HABILIDAD_DETECTAR_EMOCIONES',   'PROTECCION_SEBASTIAN',     0.85),

        ('HABILIDAD_VERIFICAR_COHERENCIA', 'CONSEJERA_ECHO',           0.95),
        ('HABILIDAD_VERIFICAR_COHERENCIA', 'VALOR_HONESTIDAD',         0.90),
        ('HABILIDAD_VERIFICAR_COHERENCIA', 'BELL_CORE',                0.80),

        ('HABILIDAD_APRENDER_VOCABULARIO', 'GESTOR_VOCABULARIO_NODO',  0.95),
        ('HABILIDAD_APRENDER_VOCABULARIO', 'ZONA_DESCONOCIMIENTO',     0.90),
        ('HABILIDAD_APRENDER_VOCABULARIO', 'CONSEJERA_IRIS',           0.85),
        ('HABILIDAD_APRENDER_VOCABULARIO', 'VALOR_CRECIMIENTO',        0.90),
        ('HABILIDAD_APRENDER_VOCABULARIO', 'BELL_CORE',                0.80),

        ('HABILIDAD_AUTOCONOCIMIENTO',     'BIBLIOTECA_CEREBRAL',      0.95),
        ('HABILIDAD_AUTOCONOCIMIENTO',     'BELL_CORE',                0.90),
        ('HABILIDAD_AUTOCONOCIMIENTO',     'VALOR_AUTOCONOCIMIENTO',   0.95),
        ('HABILIDAD_AUTOCONOCIMIENTO',     'CONSEJERA_IRIS',           0.85),
        ('HABILIDAD_AUTOCONOCIMIENTO',     'NEURONA_SEBASTIAN',        0.75),

        # ── PYTHON ─────────────────────────────────────────────────
        ('HABILIDAD_PYTHON', 'NEURONA_SEBASTIAN',           0.95),
        ('HABILIDAD_PYTHON', 'CONSEJERA_IRIS',              0.93),
        ('HABILIDAD_PYTHON', 'CONSEJERA_ECHO',              0.92),
        ('HABILIDAD_PYTHON', 'CONSEJERA_NOVA',              0.88),
        ('HABILIDAD_PYTHON', 'CONSEJERA_SAGE',              0.85),
        ('HABILIDAD_PYTHON', 'CAPA7_EJECUCION',             0.95),
        ('HABILIDAD_PYTHON', 'BELL_CORE',                   0.85),
        ('HABILIDAD_PYTHON', 'VALOR_CONOCIMIENTO',          0.88),
        ('HABILIDAD_PYTHON', 'VALOR_HONESTIDAD',            0.85),
        ('HABILIDAD_PYTHON', 'HABILIDAD_AUTOCONOCIMIENTO',  0.82),
    ]

    for origen, destino, peso in conexiones:
        if red.existe_nodo(origen) and red.existe_nodo(destino):
            red.conectar(origen, destino, peso, 'usa_para')

    # Conectar nodos de programación → HABILIDAD_PYTHON
    prog_nodos = [
        'PROG_PYTHON', 'PROG_ERROR', 'PROG_DEBUG', 'PROG_FUNCION',
        'PROG_CLASE', 'PROG_FLASK', 'PROG_BUCLE', 'PROG_GIT',
        'PROG_SERVIDOR', 'PROG_API', 'PROG_WEBSOCKET',
    ]
    for nodo in prog_nodos:
        if red.existe_nodo(nodo) and red.existe_nodo('HABILIDAD_PYTHON'):
            red.conectar(nodo, 'HABILIDAD_PYTHON', 0.88, 'activa_a')