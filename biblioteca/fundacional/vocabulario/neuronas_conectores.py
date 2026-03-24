# biblioteca/fundacional/vocabulario/neuronas_conectores.py
# ================================================
# NEURONAS DE CONECTORES
# Palabras funcionales y expresiones
# ================================================

def crear_neuronas_conectores(red):

    conectores = [
        ('CONJ_PERO',         0.85, 'conjuncion_adversativa'),
        ('CONJ_AUNQUE',       0.85, 'conjuncion_concesiva'),
        ('CONJ_SIN_EMBARGO',  0.90, 'conjuncion_adversativa'),
        ('DISC_ENTONCES',     0.85, 'estructurador'),
        ('DISC_ADEMAS',       0.85, 'estructurador'),
        ('DISC_TAMBIEN',      0.85, 'estructurador'),
        ('DISC_POR_ESO',      0.90, 'causal'),
        ('DISC_ES_DECIR',     0.90, 'aclaracion'),
        ('DISC_O_SEA',        0.85, 'aclaracion'),
        ('EXPR_OK',           0.90, 'confirmacion'),
        ('EXPR_DALE',         0.85, 'confirmacion'),
        ('EXPR_LISTO',        0.85, 'confirmacion'),
        ('EXPR_PERFECTO',     0.85, 'confirmacion'),
        ('EXPR_ENTENDIDO',    0.90, 'confirmacion'),
        ('EXPR_DE_ACUERDO',   0.90, 'confirmacion'),
        ('EXPR_CLARO',        0.85, 'confirmacion'),
        ('EXPR_QUIZAS',       0.85, 'incertidumbre'),
        ('EXPR_TAL_VEZ',      0.85, 'incertidumbre'),
        ('EXPR_NO_SE',        0.90, 'desconocimiento'),
    ]

    for nodo_id, grounding, subtipo in conectores:
        red.agregar_nodo({
            'id': nodo_id,
            'nucleo': {
                'tipo': 'concepto',
                'subtipo': subtipo,
                'grounding_base': grounding,
                'dimensiones_activas': ['conocimiento', 'contexto'],
                'archivo_real': None,
                'inmutable': False
            },
            'activacion': {
                'umbral': 0.30,
                'velocidad': 'media',
                'mielina': False
            },
            'memoria': {
                'veces_usado': 0, 'ultimo_uso': None,
                'contextos_de_uso': [],
                'resultado_historico': grounding
            }
        })

    _conectar_conectores(red)


def _conectar_conectores(red):
    conexiones = [
        ('EXPR_OK',        'NEURONA_SEBASTIAN', 0.80),
        ('EXPR_OK',        'CONSEJERA_ECHO',    0.75),
        ('EXPR_LISTO',     'NEURONA_SEBASTIAN', 0.80),
        ('EXPR_ENTENDIDO', 'NEURONA_SEBASTIAN', 0.80),
        ('EXPR_ENTENDIDO', 'CONSEJERA_ECHO',    0.80),
        ('EXPR_NO_SE',     'CONSEJERA_ECHO',    0.85),
        ('EXPR_NO_SE',     'BELL_CORE',         0.75),
        ('EXPR_QUIZAS',    'CONSEJERA_ECHO',    0.80),
        ('CONJ_PERO',      'CONSEJERA_ECHO',    0.70),
        ('DISC_POR_ESO',   'CONSEJERA_IRIS',    0.75),
    ]

    for origen, destino, peso in conexiones:
        if red.existe_nodo(origen) and red.existe_nodo(destino):
            red.conectar(origen, destino, peso, 'relacionado_con')