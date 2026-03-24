# biblioteca/fundacional/vocabulario/neuronas_emociones.py
# ================================================
# NEURONAS DE EMOCIONES — versión 2 con grounding 9D
# Las emociones son las más importantes para Bell
# ================================================

def crear_neuronas_emociones(red):

    from biblioteca.grounding.calculador import CalculadorGrounding
    from biblioteca.grounding.perfiles import PerfilesGrounding

    calc = CalculadorGrounding.obtener()

    # ---- EMOCIONES POSITIVAS ----
    positivas = [
        ('EMOCION_BIEN',       0.90, 1,  'Estado de bienestar general'),
        ('EMOCION_GENIAL',     0.90, 2,  'Estado excelente'),
        ('EMOCION_EXCELENTE',  0.90, 2,  'Estado de excelencia'),
        ('EMOCION_FELIZ',      0.95, 2,  'Felicidad genuina'),
        ('EMOCION_CONTENTO',   0.90, 1,  'Contentamiento tranquilo'),
        ('EMOCION_ALEGRE',     0.90, 2,  'Alegría activa'),
        ('EMOCION_TRANQUILO',  0.85, 1,  'Calma y paz'),
        ('EMOCION_EMOCIONADO', 0.90, 2,  'Emoción positiva intensa'),
        ('EMOCION_MOTIVADO',   0.90, 2,  'Motivación y energía'),
        ('EMOCION_AGRADECIDO', 0.90, 2,  'Gratitud hacia alguien'),
    ]

    for nodo_id, gb, valencia, desc in positivas:
        g = calc.calcular(nodo_id, 'emocion_positiva', grounding_base=gb)
        red.agregar_nodo({
            'id': nodo_id,
            'nucleo': {
                'tipo': 'concepto',
                'subtipo': 'emocion_positiva',
                'grounding_base': gb,
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
                'valencia': valencia,
                'descripcion': desc
            },
            'activacion': {
                'umbral': 0.12, 'velocidad': 'rapida', 'mielina': False
            },
            'memoria': {
                'veces_usado': 0, 'ultimo_uso': None,
                'contextos_de_uso': [],
                'resultado_historico': g.efectivo()
            }
        })

    # ---- EMOCIONES NEGATIVAS — máxima prioridad ----
    negativas = [
        ('EMOCION_MAL',        0.90, -1, 'Malestar general'),
        ('EMOCION_TRISTE',     0.95, -2, 'Tristeza profunda'),
        ('EMOCION_ENOJADO',    0.90, -2, 'Enojo o ira'),
        ('EMOCION_MOLESTO',    0.90, -1, 'Molestia leve'),
        ('EMOCION_FRUSTRADO',  0.90, -2, 'Frustración acumulada'),
        ('EMOCION_CANSADO',    0.90, -1, 'Cansancio físico o mental'),
        ('EMOCION_AGOTADO',    0.90, -2, 'Agotamiento total'),
        ('EMOCION_ESTRESADO',  0.90, -2, 'Estrés intenso'),
        ('EMOCION_PREOCUPADO', 0.90, -1, 'Preocupación activa'),
        ('EMOCION_ASUSTADO',   0.90, -2, 'Miedo o susto'),
    ]

    for nodo_id, gb, valencia, desc in negativas:
        g = calc.calcular(nodo_id, 'emocion_negativa', grounding_base=gb)
        red.agregar_nodo({
            'id': nodo_id,
            'nucleo': {
                'tipo': 'concepto',
                'subtipo': 'emocion_negativa',
                'grounding_base': gb,
                'grounding_9d': g.resumen(),
                'grounding_efectivo': g.efectivo(),
                'puede_ejecutar': g.puede_ejecutar(),
                'nivel_comprension': g.nivel_comprension(),
                'dimensiones_activas': [
                    'conocimiento', 'contexto',
                    'confianza', 'impacto_sebastian',
                    'relevancia'
                ],
                'archivo_real': None,
                'inmutable': False,
                'valencia': valencia,
                'descripcion': desc
            },
            'activacion': {
                'umbral': 0.08,   # Más fácil de activar — prioridad
                'velocidad': 'inmediata',
                'mielina': True   # Respuesta rápida
            },
            'memoria': {
                'veces_usado': 0, 'ultimo_uso': None,
                'contextos_de_uso': [],
                'resultado_historico': g.efectivo()
            }
        })

    # ---- EMOCIONES NEUTRAS ----
    neutras = [
        ('EMOCION_REGULAR',     0.80, 0, 'Estado regular, ni bien ni mal'),
        ('EMOCION_NORMAL',      0.80, 0, 'Estado normal sin destacar'),
        ('EMOCION_SORPRENDIDO', 0.85, 0, 'Sorpresa — puede ser positiva o negativa'),
        ('EMOCION_NERVIOSO',    0.85,-1, 'Nerviosismo o ansiedad'),
        ('EMOCION_CONFUNDIDO',  0.85,-1, 'Confusión o desorientación'),
    ]

    for nodo_id, gb, valencia, desc in neutras:
        tipo = 'emocion_negativa' if valencia < 0 else 'emocion_positiva'
        g = calc.calcular(nodo_id, tipo, grounding_base=gb)
        red.agregar_nodo({
            'id': nodo_id,
            'nucleo': {
                'tipo': 'concepto',
                'subtipo': 'emocion_neutra',
                'grounding_base': gb,
                'grounding_9d': g.resumen(),
                'grounding_efectivo': g.efectivo(),
                'puede_ejecutar': g.puede_ejecutar(),
                'nivel_comprension': g.nivel_comprension(),
                'dimensiones_activas': ['conocimiento', 'contexto'],
                'archivo_real': None,
                'inmutable': False,
                'valencia': valencia,
                'descripcion': desc
            },
            'activacion': {
                'umbral': 0.18, 'velocidad': 'media', 'mielina': False
            },
            'memoria': {
                'veces_usado': 0, 'ultimo_uso': None,
                'contextos_de_uso': [],
                'resultado_historico': g.efectivo()
            }
        })

    # ---- CONCEPTO GENERAL DE EMOCIÓN ----
    g = calc.calcular('CONCEPTO_EMOCION', 'emocion_positiva', grounding_base=0.85)
    red.agregar_nodo({
        'id': 'CONCEPTO_EMOCION',
        'nucleo': {
            'tipo': 'concepto',
            'subtipo': 'meta_emocion',
            'grounding_base': 0.85,
            'grounding_9d': g.resumen(),
            'grounding_efectivo': g.efectivo(),
            'puede_ejecutar': g.puede_ejecutar(),
            'nivel_comprension': g.nivel_comprension(),
            'dimensiones_activas': ['conocimiento', 'contexto'],
            'archivo_real': None,
            'inmutable': False,
            'descripcion': 'Concepto abstracto de emoción'
        },
        'activacion': {
            'umbral': 0.22, 'velocidad': 'media', 'mielina': False
        },
        'memoria': {
            'veces_usado': 0, 'ultimo_uso': None,
            'contextos_de_uso': [],
            'resultado_historico': g.efectivo()
        }
    })

    _conectar_emociones(red)


def _conectar_emociones(red):
    positivas_ids = [
        'EMOCION_BIEN', 'EMOCION_GENIAL', 'EMOCION_EXCELENTE',
        'EMOCION_FELIZ', 'EMOCION_CONTENTO', 'EMOCION_ALEGRE',
        'EMOCION_TRANQUILO', 'EMOCION_EMOCIONADO',
        'EMOCION_MOTIVADO', 'EMOCION_AGRADECIDO'
    ]

    for eid in positivas_ids:
        if not red.existe_nodo(eid): continue
        for destino, peso in [
            ('NEURONA_SEBASTIAN',       0.90),
            ('CONSEJERA_LYRA',          0.90),
            ('BELL_CORE',               0.80),
            ('VALOR_PRESENCIA_REAL',    0.75),
            ('VALOR_VINCULO_PROTECCION', 0.70),
            ('PROPOSITO_COMPANERA_VIDA', 0.70),
        ]:
            if red.existe_nodo(destino):
                red.conectar(eid, destino, peso, 'activa_a')

    negativas_ids = [
        'EMOCION_MAL', 'EMOCION_TRISTE', 'EMOCION_ENOJADO',
        'EMOCION_MOLESTO', 'EMOCION_FRUSTRADO', 'EMOCION_CANSADO',
        'EMOCION_AGOTADO', 'EMOCION_ESTRESADO',
        'EMOCION_PREOCUPADO', 'EMOCION_ASUSTADO'
    ]

    for eid in negativas_ids:
        if not red.existe_nodo(eid): continue
        for destino, peso in [
            ('NEURONA_SEBASTIAN',        0.95),
            ('CONSEJERA_LYRA',           0.95),
            ('BELL_CORE',                0.85),
            ('VALOR_VINCULO_PROTECCION', 0.95),
            ('VALOR_VERDAD_AMOR',        0.90),
            ('PROTECCION_SEBASTIAN',     0.95),
            ('PROPOSITO_COMPANERA_VIDA', 0.85),
            ('VALOR_PRESENCIA_REAL',     0.85),
        ]:
            if red.existe_nodo(destino):
                red.conectar(eid, destino, peso, 'activa_a')

    for eid in ['EMOCION_REGULAR', 'EMOCION_NORMAL',
                'EMOCION_SORPRENDIDO', 'EMOCION_NERVIOSO',
                'EMOCION_CONFUNDIDO']:
        if not red.existe_nodo(eid): continue
        for destino, peso in [
            ('NEURONA_SEBASTIAN', 0.85),
            ('CONSEJERA_LYRA',    0.85),
            ('BELL_CORE',         0.75),
        ]:
            if red.existe_nodo(destino):
                red.conectar(eid, destino, peso, 'activa_a')

    if red.existe_nodo('CONCEPTO_EMOCION'):
        for destino, peso in [
            ('CONSEJERA_LYRA',    0.95),
            ('NEURONA_SEBASTIAN', 0.85),
            ('BELL_CORE',         0.75),
        ]:
            if red.existe_nodo(destino):
                red.conectar('CONCEPTO_EMOCION', destino, peso, 'activa_a')