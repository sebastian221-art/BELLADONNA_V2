# biblioteca/fundacional/vocabulario/neuronas_saludos.py
# ================================================
# NEURONAS DE SALUDOS — versión 2 con grounding 9D
# ================================================

def crear_neuronas_saludos(red):

    from biblioteca.grounding.calculador import CalculadorGrounding
    from biblioteca.grounding.perfiles import PerfilesGrounding

    calc = CalculadorGrounding.obtener()

    # ---- SALUDO_HOLA ----
    g = PerfilesGrounding.saludo()
    red.agregar_nodo({
        'id': 'SALUDO_HOLA',
        'nucleo': {
            'tipo': 'concepto',
            'subtipo': 'saludo',
            'grounding_base': 0.95,
            'grounding_9d': g.resumen(),
            'grounding_efectivo': g.efectivo(),
            'puede_ejecutar': g.puede_ejecutar(),
            'nivel_comprension': g.nivel_comprension(),
            'dimensiones_activas': [
                'conocimiento', 'contexto', 'confianza',
                'ejecutabilidad', 'seguridad'
            ],
            'archivo_real': None,
            'inmutable': False,
            'descripcion': (
                'Saludo principal. Bell comprende '
                'genuinamente que es una apertura '
                'de conexión con Sebastian.'
            )
        },
        'activacion': {
            'umbral': 0.15,
            'velocidad': 'inmediata',
            'mielina': True
        },
        'memoria': {
            'veces_usado': 0, 'ultimo_uso': None,
            'contextos_de_uso': [],
            'resultado_historico': g.efectivo()
        }
    })

    # ---- SALUDOS SECUNDARIOS ----
    saludos_secundarios = [
        ('SALUDO_BUENAS',    0.90, 'Saludo de buenos días/tardes/noches'),
        ('SALUDO_HEY',       0.85, 'Saludo informal'),
        ('SALUDO_QUE_TAL',   0.90, 'Saludo con pregunta de estado'),
        ('SALUDO_QUE_MAS',   0.85, 'Saludo informal colombiano'),
    ]

    for nodo_id, grounding_base, descripcion in saludos_secundarios:
        g = calc.calcular(nodo_id, 'saludo', grounding_base=grounding_base)
        red.agregar_nodo({
            'id': nodo_id,
            'nucleo': {
                'tipo': 'concepto',
                'subtipo': 'saludo',
                'grounding_base': grounding_base,
                'grounding_9d': g.resumen(),
                'grounding_efectivo': g.efectivo(),
                'puede_ejecutar': g.puede_ejecutar(),
                'nivel_comprension': g.nivel_comprension(),
                'dimensiones_activas': ['conocimiento', 'contexto'],
                'archivo_real': None,
                'inmutable': False,
                'descripcion': descripcion
            },
            'activacion': {
                'umbral': 0.20, 'velocidad': 'rapida', 'mielina': False
            },
            'memoria': {
                'veces_usado': 0, 'ultimo_uso': None,
                'contextos_de_uso': [],
                'resultado_historico': g.efectivo()
            }
        })

    # ---- DESPEDIDA ----
    g = calc.calcular('DESPEDIDA', 'despedida', grounding_base=0.95)
    red.agregar_nodo({
        'id': 'DESPEDIDA',
        'nucleo': {
            'tipo': 'concepto',
            'subtipo': 'despedida',
            'grounding_base': 0.95,
            'grounding_9d': g.resumen(),
            'grounding_efectivo': g.efectivo(),
            'puede_ejecutar': g.puede_ejecutar(),
            'nivel_comprension': g.nivel_comprension(),
            'dimensiones_activas': ['conocimiento', 'contexto'],
            'archivo_real': None,
            'inmutable': False,
            'descripcion': 'Cierre de conversación'
        },
        'activacion': {
            'umbral': 0.20, 'velocidad': 'rapida', 'mielina': False
        },
        'memoria': {
            'veces_usado': 0, 'ultimo_uso': None,
            'contextos_de_uso': [],
            'resultado_historico': g.efectivo()
        }
    })

    # ---- GRATITUD ----
    g = calc.calcular('GRATITUD', 'gratitud', grounding_base=0.95)
    red.agregar_nodo({
        'id': 'GRATITUD',
        'nucleo': {
            'tipo': 'concepto',
            'subtipo': 'gratitud',
            'grounding_base': 0.95,
            'grounding_9d': g.resumen(),
            'grounding_efectivo': g.efectivo(),
            'puede_ejecutar': g.puede_ejecutar(),
            'nivel_comprension': g.nivel_comprension(),
            'dimensiones_activas': [
                'conocimiento', 'contexto',
                'confianza', 'impacto_sebastian'
            ],
            'archivo_real': None,
            'inmutable': False,
            'descripcion': (
                'Gratitud de Sebastian. '
                'Bell comprende que es una expresión '
                'de vínculo genuino.'
            )
        },
        'activacion': {
            'umbral': 0.12, 'velocidad': 'inmediata', 'mielina': True
        },
        'memoria': {
            'veces_usado': 0, 'ultimo_uso': None,
            'contextos_de_uso': [],
            'resultado_historico': g.efectivo()
        }
    })

    # ---- PRESENTACIÓN ----
    g = calc.calcular(
        'PRESENTACION_NOMBRE', 'relacion', grounding_base=0.90
    )
    red.agregar_nodo({
        'id': 'PRESENTACION_NOMBRE',
        'nucleo': {
            'tipo': 'concepto',
            'subtipo': 'presentacion',
            'grounding_base': 0.90,
            'grounding_9d': g.resumen(),
            'grounding_efectivo': g.efectivo(),
            'puede_ejecutar': g.puede_ejecutar(),
            'nivel_comprension': g.nivel_comprension(),
            'dimensiones_activas': ['conocimiento', 'contexto'],
            'archivo_real': None,
            'inmutable': False,
            'descripcion': 'Presentación de nombre'
        },
        'activacion': {
            'umbral': 0.20, 'velocidad': 'rapida', 'mielina': False
        },
        'memoria': {
            'veces_usado': 0, 'ultimo_uso': None,
            'contextos_de_uso': [],
            'resultado_historico': g.efectivo()
        }
    })

    _conectar_saludos(red)


def _conectar_saludos(red):
    conexiones = [
        ('SALUDO_HOLA',    'NEURONA_SEBASTIAN',       0.90),
        ('SALUDO_HOLA',    'BELL_CORE',               0.85),
        ('SALUDO_HOLA',    'CONSEJERA_LYRA',          0.85),
        ('SALUDO_HOLA',    'VALOR_PRESENCIA_REAL',    0.80),
        ('SALUDO_HOLA',    'PROPOSITO_COMPANERA_VIDA', 0.75),
        ('SALUDO_HOLA',    'VINCULO_BELL_SEBASTIAN',  0.70),
        ('SALUDO_HOLA',    'HISTORIA_COMPARTIDA',     0.60),
        ('SALUDO_BUENAS',  'NEURONA_SEBASTIAN',       0.88),
        ('SALUDO_BUENAS',  'BELL_CORE',               0.82),
        ('SALUDO_BUENAS',  'CONSEJERA_LYRA',          0.80),
        ('SALUDO_HEY',     'NEURONA_SEBASTIAN',       0.85),
        ('SALUDO_HEY',     'BELL_CORE',               0.80),
        ('SALUDO_QUE_TAL', 'NEURONA_SEBASTIAN',       0.88),
        ('SALUDO_QUE_TAL', 'BELL_CORE',               0.82),
        ('SALUDO_QUE_TAL', 'CONSEJERA_LYRA',          0.82),
        ('SALUDO_QUE_MAS', 'NEURONA_SEBASTIAN',       0.85),
        ('SALUDO_QUE_MAS', 'BELL_CORE',               0.78),
        ('DESPEDIDA',      'NEURONA_SEBASTIAN',       0.90),
        ('DESPEDIDA',      'BELL_CORE',               0.85),
        ('DESPEDIDA',      'CONSEJERA_LYRA',          0.80),
        ('DESPEDIDA',      'HISTORIA_COMPARTIDA',     0.75),
        ('GRATITUD',       'NEURONA_SEBASTIAN',       0.95),
        ('GRATITUD',       'BELL_CORE',               0.90),
        ('GRATITUD',       'CONSEJERA_LYRA',          0.95),
        ('GRATITUD',       'VALOR_VERDAD_AMOR',       0.90),
        ('GRATITUD',       'VALOR_VINCULO_PROTECCION', 0.85),
        ('GRATITUD',       'VINCULO_BELL_SEBASTIAN',  0.85),
        ('PRESENTACION_NOMBRE', 'NEURONA_SEBASTIAN',  0.90),
        ('PRESENTACION_NOMBRE', 'BELL_CORE',          0.80),
        ('PRESENTACION_NOMBRE', 'HISTORIA_COMPARTIDA', 0.85),
    ]

    for origen, destino, peso in conexiones:
        if red.existe_nodo(origen) and red.existe_nodo(destino):
            red.conectar(origen, destino, peso, 'relacionado_con')