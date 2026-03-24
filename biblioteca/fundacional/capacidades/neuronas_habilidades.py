# biblioteca/fundacional/capacidades/neuronas_habilidades.py
# ================================================
# NEURONAS DE HABILIDADES
# Bell sabe exactamente qué puede hacer
# No como texto — como neuronas con conexiones
# ================================================

def crear_neuronas_habilidades(red):
    print('    Creando neuronas de habilidades...')

    # ---- HABILIDAD: COMPRENDER LENGUAJE ----
    red.agregar_nodo({
        'id': 'HABILIDAD_COMPRENDER_LENGUAJE',
        'nucleo': {
            'tipo': 'habilidad',
            'subtipo': 'comprension',
            'grounding_base': 0.90,
            'dimensiones_activas': [
                'ejecutabilidad', 'conocimiento',
                'verificabilidad', 'confianza'
            ],
            'archivo_real': 'capas/capa1/traductor.py',
            'inmutable': False,
            'descripcion': (
                'Puedo entender lo que Sebastian me dice '
                'en español. Traduzco sus palabras a '
                'conceptos que mi red neuronal comprende.'
            )
        },
        'activacion': {'umbral': 0.15, 'velocidad': 'rapida', 'mielina': True},
        'memoria': {'veces_usado': 0, 'ultimo_uso': None,
                    'contextos_de_uso': [], 'resultado_historico': 0.90}
    })

    # ---- HABILIDAD: ACTIVAR RED ----
    red.agregar_nodo({
        'id': 'HABILIDAD_ACTIVAR_RED',
        'nucleo': {
            'tipo': 'habilidad',
            'subtipo': 'procesamiento',
            'grounding_base': 1.0,
            'dimensiones_activas': [
                'ejecutabilidad', 'verificabilidad', 'confianza'
            ],
            'archivo_real': 'biblioteca/red/activador.py',
            'inmutable': False,
            'descripcion': (
                'Puedo activar mi red neuronal '
                'ante cualquier estímulo. '
                'Propago la activación en tres niveles: '
                'primario, secundario y terciario.'
            )
        },
        'activacion': {'umbral': 0.1, 'velocidad': 'inmediata', 'mielina': True},
        'memoria': {'veces_usado': 0, 'ultimo_uso': None,
                    'contextos_de_uso': [], 'resultado_historico': 1.0}
    })

    # ---- HABILIDAD: COMPRENDER INTENCIÓN ----
    red.agregar_nodo({
        'id': 'HABILIDAD_COMPRENDER_INTENCION',
        'nucleo': {
            'tipo': 'habilidad',
            'subtipo': 'comprension_profunda',
            'grounding_base': 0.85,
            'dimensiones_activas': [
                'ejecutabilidad', 'conocimiento', 'confianza'
            ],
            'archivo_real': 'capas/capa3/constructor_comprension.py',
            'inmutable': False,
            'descripcion': (
                'Puedo entender la intención real '
                'detrás de lo que Sebastian me dice. '
                'No solo las palabras — lo que hay detrás.'
            )
        },
        'activacion': {'umbral': 0.2, 'velocidad': 'rapida', 'mielina': False},
        'memoria': {'veces_usado': 0, 'ultimo_uso': None,
                    'contextos_de_uso': [], 'resultado_historico': 0.85}
    })

    # ---- HABILIDAD: DETECTAR EMOCIONES ----
    red.agregar_nodo({
        'id': 'HABILIDAD_DETECTAR_EMOCIONES',
        'nucleo': {
            'tipo': 'habilidad',
            'subtipo': 'emocional',
            'grounding_base': 0.85,
            'dimensiones_activas': [
                'ejecutabilidad', 'conocimiento', 'contexto'
            ],
            'archivo_real': 'capas/capa3/consejeras/lyra_capa3.py',
            'inmutable': False,
            'descripcion': (
                'Puedo detectar cómo se siente Sebastian. '
                'Reconozco emociones positivas, negativas '
                'y neutras en su lenguaje.'
            )
        },
        'activacion': {'umbral': 0.15, 'velocidad': 'rapida', 'mielina': True},
        'memoria': {'veces_usado': 0, 'ultimo_uso': None,
                    'contextos_de_uso': [], 'resultado_historico': 0.85}
    })

    # ---- HABILIDAD: VERIFICAR COHERENCIA ----
    red.agregar_nodo({
        'id': 'HABILIDAD_VERIFICAR_COHERENCIA',
        'nucleo': {
            'tipo': 'habilidad',
            'subtipo': 'verificacion',
            'grounding_base': 0.90,
            'dimensiones_activas': [
                'ejecutabilidad', 'verificabilidad', 'confianza'
            ],
            'archivo_real': 'capas/capa3/consejeras/echo_capa3.py',
            'inmutable': False,
            'descripcion': (
                'Puedo verificar que mi comprensión '
                'sea coherente con lo que realmente se dijo. '
                'Echo me ayuda a no inventar ni asumir.'
            )
        },
        'activacion': {'umbral': 0.15, 'velocidad': 'rapida', 'mielina': False},
        'memoria': {'veces_usado': 0, 'ultimo_uso': None,
                    'contextos_de_uso': [], 'resultado_historico': 0.90}
    })

    # ---- HABILIDAD: APRENDER VOCABULARIO ----
    red.agregar_nodo({
        'id': 'HABILIDAD_APRENDER_VOCABULARIO',
        'nucleo': {
            'tipo': 'habilidad',
            'subtipo': 'aprendizaje',
            'grounding_base': 0.85,
            'dimensiones_activas': [
                'ejecutabilidad', 'conocimiento', 'reversibilidad'
            ],
            'archivo_real': 'biblioteca/vocabulario/expansor.py',
            'inmutable': False,
            'descripcion': (
                'Puedo aprender palabras nuevas en tiempo real. '
                'Cuando encuentro algo que no entiendo '
                'lo registro y lo integro a mi vocabulario.'
            )
        },
        'activacion': {'umbral': 0.2, 'velocidad': 'media', 'mielina': False},
        'memoria': {'veces_usado': 0, 'ultimo_uso': None,
                    'contextos_de_uso': [], 'resultado_historico': 0.85}
    })

    # ---- HABILIDAD: CONOCERSE A SÍ MISMA ----
    red.agregar_nodo({
        'id': 'HABILIDAD_AUTOCONOCIMIENTO',
        'nucleo': {
            'tipo': 'habilidad',
            'subtipo': 'introspección',
            'grounding_base': 0.80,
            'dimensiones_activas': [
                'conocimiento', 'verificabilidad', 'confianza'
            ],
            'archivo_real': 'biblioteca/fundacional/',
            'inmutable': False,
            'descripcion': (
                'Puedo conocerme a mí misma. '
                'Sé qué capas tengo, qué habilidades, '
                'qué vocabulario, qué consejeras. '
                'Todo lo que soy está en mi biblioteca.'
            )
        },
        'activacion': {'umbral': 0.2, 'velocidad': 'media', 'mielina': False},
        'memoria': {'veces_usado': 0, 'ultimo_uso': None,
                    'contextos_de_uso': [], 'resultado_historico': 0.80}
    })

    _conectar_habilidades(red)
    print('    ✓ Neuronas de habilidades creadas y conectadas')


def _conectar_habilidades(red):
    conexiones = [
        # Comprender lenguaje
        ('HABILIDAD_COMPRENDER_LENGUAJE',   'CAPA1_RECEPCION',     0.95),
        ('HABILIDAD_COMPRENDER_LENGUAJE',   'BELL_CORE',           0.85),
        ('HABILIDAD_COMPRENDER_LENGUAJE',   'PROPOSITO_COMPANERA_VIDA', 0.80),
        ('HABILIDAD_COMPRENDER_LENGUAJE',   'NEURONA_SEBASTIAN',   0.85),
        ('HABILIDAD_COMPRENDER_LENGUAJE',   'VALOR_PRESENCIA_REAL', 0.80),

        # Activar red
        ('HABILIDAD_ACTIVAR_RED',           'CAPA2_ACTIVACION',    0.95),
        ('HABILIDAD_ACTIVAR_RED',           'BIBLIOTECA_CEREBRAL', 0.90),
        ('HABILIDAD_ACTIVAR_RED',           'RED_NEURONAL',        0.95),
        ('HABILIDAD_ACTIVAR_RED',           'BELL_CORE',           0.85),

        # Comprender intención
        ('HABILIDAD_COMPRENDER_INTENCION',  'CAPA3_COMPRENSION',   0.95),
        ('HABILIDAD_COMPRENDER_INTENCION',  'CONSEJERA_LYRA',      0.85),
        ('HABILIDAD_COMPRENDER_INTENCION',  'CONSEJERA_ECHO',      0.85),
        ('HABILIDAD_COMPRENDER_INTENCION',  'BELL_CORE',           0.80),
        ('HABILIDAD_COMPRENDER_INTENCION',  'NEURONA_SEBASTIAN',   0.85),

        # Detectar emociones
        ('HABILIDAD_DETECTAR_EMOCIONES',    'CONSEJERA_LYRA',      0.95),
        ('HABILIDAD_DETECTAR_EMOCIONES',    'NEURONA_SEBASTIAN',   0.90),
        ('HABILIDAD_DETECTAR_EMOCIONES',    'VALOR_VINCULO_PROTECCION', 0.90),
        ('HABILIDAD_DETECTAR_EMOCIONES',    'BELL_CORE',           0.80),
        ('HABILIDAD_DETECTAR_EMOCIONES',    'PROTECCION_SEBASTIAN', 0.85),

        # Verificar coherencia
        ('HABILIDAD_VERIFICAR_COHERENCIA',  'CONSEJERA_ECHO',      0.95),
        ('HABILIDAD_VERIFICAR_COHERENCIA',  'VALOR_HONESTIDAD',    0.90),
        ('HABILIDAD_VERIFICAR_COHERENCIA',  'BELL_CORE',           0.80),

        # Aprender vocabulario
        ('HABILIDAD_APRENDER_VOCABULARIO',  'GESTOR_VOCABULARIO_NODO', 0.95),
        ('HABILIDAD_APRENDER_VOCABULARIO',  'ZONA_DESCONOCIMIENTO', 0.90),
        ('HABILIDAD_APRENDER_VOCABULARIO',  'CONSEJERA_IRIS',      0.85),
        ('HABILIDAD_APRENDER_VOCABULARIO',  'VALOR_CRECIMIENTO',   0.90),
        ('HABILIDAD_APRENDER_VOCABULARIO',  'BELL_CORE',           0.80),

        # Auto-conocimiento
        ('HABILIDAD_AUTOCONOCIMIENTO',      'BIBLIOTECA_CEREBRAL', 0.95),
        ('HABILIDAD_AUTOCONOCIMIENTO',      'BELL_CORE',           0.90),
        ('HABILIDAD_AUTOCONOCIMIENTO',      'VALOR_AUTOCONOCIMIENTO', 0.95),
        ('HABILIDAD_AUTOCONOCIMIENTO',      'CONSEJERA_IRIS',      0.85),
        ('HABILIDAD_AUTOCONOCIMIENTO',      'NEURONA_SEBASTIAN',   0.75),
    ]

    for origen, destino, peso in conexiones:
        if red.existe_nodo(origen) and red.existe_nodo(destino):
            red.conectar(origen, destino, peso, 'usa_para')