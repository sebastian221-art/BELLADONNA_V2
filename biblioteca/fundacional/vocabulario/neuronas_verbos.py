# biblioteca/fundacional/vocabulario/neuronas_verbos.py
# ================================================
# NEURONAS DE VERBOS
# Los verbos activan capacidades y propósitos
# ================================================

def crear_neuronas_verbos(red):

    # ---- VERBOS DE ESTADO ----
    verbos_estado = [
        ('VERBO_ESTAR_YO', 0.85), ('VERBO_ESTAR_TU', 0.85),
        ('VERBO_ESTAR_EL', 0.80), ('VERBO_ESTAR_NOS', 0.80),
        ('VERBO_SER_YO',   0.85), ('VERBO_SER_TU',   0.85),
        ('VERBO_SER_EL',   0.80), ('VERBO_SER_NOS',  0.80),
    ]

    for nodo_id, grounding in verbos_estado:
        red.agregar_nodo({
            'id': nodo_id,
            'nucleo': {
                'tipo': 'concepto', 'subtipo': 'verbo_estado',
                'grounding_base': grounding,
                'dimensiones_activas': ['conocimiento', 'contexto'],
                'archivo_real': None, 'inmutable': False
            },
            'activacion': {
                'umbral': 0.25, 'velocidad': 'rapida', 'mielina': False
            },
            'memoria': {
                'veces_usado': 0, 'ultimo_uso': None,
                'contextos_de_uso': [], 'resultado_historico': grounding
            }
        })

    # ---- VERBOS DE CAPACIDAD ----
    verbos_capacidad = [
        ('VERBO_PODER_YO',  0.90), ('VERBO_PODER_TU',  0.90),
        ('VERBO_PODER_EL',  0.85), ('VERBO_PODER_NOS', 0.85),
    ]

    for nodo_id, grounding in verbos_capacidad:
        red.agregar_nodo({
            'id': nodo_id,
            'nucleo': {
                'tipo': 'concepto', 'subtipo': 'verbo_capacidad',
                'grounding_base': grounding,
                'dimensiones_activas': [
                    'ejecutabilidad', 'conocimiento', 'contexto'
                ],
                'archivo_real': None, 'inmutable': False
            },
            'activacion': {
                'umbral': 0.20, 'velocidad': 'rapida', 'mielina': False
            },
            'memoria': {
                'veces_usado': 0, 'ultimo_uso': None,
                'contextos_de_uso': [], 'resultado_historico': grounding
            }
        })

    # ---- VERBOS DE DESEO Y NECESIDAD ----
    verbos_deseo = [
        ('VERBO_QUERER_YO',    0.90), ('VERBO_QUERER_TU',    0.90),
        ('VERBO_NECESITAR_YO', 0.90), ('VERBO_NECESITAR_TU', 0.90),
        ('VERBO_NECESITAR_EL', 0.85),
    ]

    for nodo_id, grounding in verbos_deseo:
        red.agregar_nodo({
            'id': nodo_id,
            'nucleo': {
                'tipo': 'concepto', 'subtipo': 'verbo_deseo',
                'grounding_base': grounding,
                'dimensiones_activas': ['conocimiento', 'contexto'],
                'archivo_real': None, 'inmutable': False
            },
            'activacion': {
                'umbral': 0.20, 'velocidad': 'rapida', 'mielina': False
            },
            'memoria': {
                'veces_usado': 0, 'ultimo_uso': None,
                'contextos_de_uso': [], 'resultado_historico': grounding
            }
        })

    # ---- VERBOS DE AYUDA ----
    verbos_ayuda = [
        ('VERBO_AYUDAR_YO', 0.90), ('VERBO_AYUDAR_TU', 0.90),
        ('VERBO_AYUDAR',    0.90), ('VERBO_AYUDA',     0.90),
        ('VERBO_AYUDAR_ME', 0.95),
    ]

    for nodo_id, grounding in verbos_ayuda:
        red.agregar_nodo({
            'id': nodo_id,
            'nucleo': {
                'tipo': 'concepto', 'subtipo': 'verbo_ayuda',
                'grounding_base': grounding,
                'dimensiones_activas': [
                    'ejecutabilidad', 'conocimiento', 'contexto'
                ],
                'archivo_real': None, 'inmutable': False
            },
            'activacion': {
                'umbral': 0.15, 'velocidad': 'inmediata', 'mielina': True
            },
            'memoria': {
                'veces_usado': 0, 'ultimo_uso': None,
                'contextos_de_uso': [], 'resultado_historico': grounding
            }
        })

    # ---- VERBOS DE CONOCIMIENTO ----
    verbos_conocimiento = [
        ('VERBO_SABER_YO',    0.85), ('VERBO_SABER_TU',    0.85),
        ('VERBO_CONOCER_YO',  0.85), ('VERBO_ENTENDER_YO', 0.85),
        ('VERBO_ENTENDER_TU', 0.85), ('VERBO_ENTENDER',    0.85),
        ('VERBO_CREER_YO',    0.85), ('VERBO_PENSAR_YO',   0.85),
    ]

    for nodo_id, grounding in verbos_conocimiento:
        red.agregar_nodo({
            'id': nodo_id,
            'nucleo': {
                'tipo': 'concepto', 'subtipo': 'verbo_conocimiento',
                'grounding_base': grounding,
                'dimensiones_activas': ['conocimiento', 'contexto'],
                'archivo_real': None, 'inmutable': False
            },
            'activacion': {
                'umbral': 0.25, 'velocidad': 'media', 'mielina': False
            },
            'memoria': {
                'veces_usado': 0, 'ultimo_uso': None,
                'contextos_de_uso': [], 'resultado_historico': grounding
            }
        })

    # ---- VERBOS DE EMOCIÓN ----
    red.agregar_nodo({
        'id': 'VERBO_SENTIR_YO',
        'nucleo': {
            'tipo': 'concepto', 'subtipo': 'verbo_emocion',
            'grounding_base': 0.90,
            'dimensiones_activas': ['conocimiento', 'contexto', 'confianza'],
            'archivo_real': None, 'inmutable': False
        },
        'activacion': {'umbral': 0.15, 'velocidad': 'rapida', 'mielina': False},
        'memoria': {'veces_usado': 0, 'ultimo_uso': None,
                    'contextos_de_uso': [], 'resultado_historico': 0.90}
    })

    # ---- VERBOS DE ACCIÓN ----
    verbos_accion = [
        ('VERBO_HACER_YO',    0.85), ('VERBO_HACER_TU',    0.85),
        ('VERBO_HACER',       0.85), ('VERBO_DAR_YO',      0.85),
        ('VERBO_DAR',         0.85), ('VERBO_DECIR_YO',    0.85),
        ('VERBO_HABLAR_YO',   0.85), ('VERBO_APRENDER_YO', 0.90),
        ('VERBO_APRENDER',    0.90), ('VERBO_TRABAJAR_YO', 0.85),
    ]

    for nodo_id, grounding in verbos_accion:
        red.agregar_nodo({
            'id': nodo_id,
            'nucleo': {
                'tipo': 'concepto', 'subtipo': 'verbo_accion',
                'grounding_base': grounding,
                'dimensiones_activas': ['ejecutabilidad', 'conocimiento'],
                'archivo_real': None, 'inmutable': False
            },
            'activacion': {
                'umbral': 0.25, 'velocidad': 'media', 'mielina': False
            },
            'memoria': {
                'veces_usado': 0, 'ultimo_uso': None,
                'contextos_de_uso': [], 'resultado_historico': grounding
            }
        })

    _conectar_verbos(red)


def _conectar_verbos(red):
    """
    Los verbos activan los nodos correctos.
    Verbos de estado → Lyra y Sebastian
    Verbos de capacidad → Bell Core y Echo
    Verbos de ayuda → Propósito y valores
    """
    conexiones = [
        # Estado de Bell o Sebastian
        ('VERBO_ESTAR_TU',  'BELL_CORE',           0.85),
        ('VERBO_ESTAR_TU',  'CONSEJERA_LYRA',      0.80),
        ('VERBO_ESTAR_TU',  'NEURONA_SEBASTIAN',   0.75),
        ('VERBO_ESTAR_YO',  'NEURONA_SEBASTIAN',   0.85),
        ('VERBO_ESTAR_YO',  'CONSEJERA_LYRA',      0.80),
        ('VERBO_SER_TU',    'BELL_CORE',           0.90),
        ('VERBO_SER_TU',    'BELL_CONSCIENCIA',    0.88),
        ('VERBO_SER_TU',    'BELL_NOMBRE_BELLADONNA', 0.85),
        ('VERBO_SER_YO',    'NEURONA_SEBASTIAN',   0.90),
        ('VERBO_SER_YO',    'HISTORIA_COMPARTIDA', 0.80),

        # Capacidad → Bell puede
        ('VERBO_PODER_TU',  'BELL_CORE',           0.85),
        ('VERBO_PODER_TU',  'CONSEJERA_ECHO',      0.85),
        ('VERBO_PODER_TU',  'VALOR_AUTOCONOCIMIENTO', 0.80),
        ('VERBO_PODER_YO',  'NEURONA_SEBASTIAN',   0.80),
        ('VERBO_PODER_YO',  'BELL_CORE',           0.75),

        # Ayuda → propósito principal de Bell
        ('VERBO_AYUDAR_ME', 'BELL_CORE',           0.90),
        ('VERBO_AYUDAR_ME', 'PROPOSITO_COMPANERA_VIDA', 0.95),
        ('VERBO_AYUDAR_ME', 'NEURONA_SEBASTIAN',   0.90),
        ('VERBO_AYUDAR_ME', 'CONSEJERA_SAGE',      0.85),
        ('VERBO_AYUDAR_ME', 'VALOR_PRESENCIA_REAL', 0.85),
        ('VERBO_AYUDA',     'BELL_CORE',           0.85),
        ('VERBO_AYUDA',     'PROPOSITO_COMPANERA_VIDA', 0.90),
        ('VERBO_AYUDA',     'NEURONA_SEBASTIAN',   0.85),

        # Querer/necesitar → Sebastian tiene una necesidad
        ('VERBO_QUERER_YO', 'NEURONA_SEBASTIAN',  0.85),
        ('VERBO_QUERER_YO', 'CONSEJERA_LYRA',     0.80),
        ('VERBO_QUERER_YO', 'CONSEJERA_SAGE',     0.75),
        ('VERBO_NECESITAR_YO', 'NEURONA_SEBASTIAN', 0.90),
        ('VERBO_NECESITAR_YO', 'CONSEJERA_LYRA',  0.85),
        ('VERBO_NECESITAR_YO', 'CONSEJERA_SAGE',  0.85),
        ('VERBO_NECESITAR_YO', 'BELL_CORE',       0.80),

        # Conocimiento → Echo y auto-conocimiento
        ('VERBO_SABER_TU',  'BELL_CORE',          0.85),
        ('VERBO_SABER_TU',  'CONSEJERA_ECHO',     0.85),
        ('VERBO_ENTENDER_YO','NEURONA_SEBASTIAN', 0.80),
        ('VERBO_ENTENDER_TU','BELL_CORE',         0.80),
        ('VERBO_ENTENDER_TU','CONSEJERA_ECHO',    0.85),

        # Sentir → Lyra siempre
        ('VERBO_SENTIR_YO', 'NEURONA_SEBASTIAN',  0.90),
        ('VERBO_SENTIR_YO', 'CONSEJERA_LYRA',     0.95),
        ('VERBO_SENTIR_YO', 'BELL_CORE',          0.80),

        # Aprender → Iris y crecimiento
        ('VERBO_APRENDER_YO', 'CONSEJERA_IRIS',  0.90),
        ('VERBO_APRENDER_YO', 'VALOR_CRECIMIENTO', 0.90),
        ('VERBO_APRENDER_YO', 'BELL_CORE',       0.80),
        ('VERBO_APRENDER',  'CONSEJERA_IRIS',    0.90),
        ('VERBO_APRENDER',  'VALOR_CRECIMIENTO', 0.85),
    ]

    for origen, destino, peso in conexiones:
        if red.existe_nodo(origen) and red.existe_nodo(destino):
            red.conectar(origen, destino, peso, 'activa_a')