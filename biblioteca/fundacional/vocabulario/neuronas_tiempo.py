# biblioteca/fundacional/vocabulario/neuronas_tiempo.py
# ================================================
# NEURONAS DE TIEMPO
# Referencias temporales conectadas al contexto
# ================================================

def crear_neuronas_tiempo(red):

    conceptos_tiempo = [
        ('TIEMPO_AHORA',      0.95, 'tiempo_presente'),
        ('TIEMPO_HOY',        0.95, 'tiempo_presente'),
        ('TIEMPO_AYER',       0.90, 'tiempo_pasado'),
        ('TIEMPO_MANANA',     0.90, 'tiempo_futuro'),
        ('TIEMPO_DESPUES',    0.90, 'tiempo_futuro'),
        ('TIEMPO_ANTES',      0.90, 'tiempo_pasado'),
        ('TIEMPO_LUEGO',      0.85, 'tiempo_futuro'),
        ('TIEMPO_PRONTO',     0.85, 'tiempo_futuro'),
        ('TIEMPO_YA',         0.80, 'tiempo_presente'),
        ('TIEMPO_TODAVIA',    0.85, 'tiempo_continuidad'),
        ('TIEMPO_AUN',        0.85, 'tiempo_continuidad'),
        ('TIEMPO_SIEMPRE',    0.90, 'tiempo_permanencia'),
        ('TIEMPO_NUNCA',      0.90, 'tiempo_negacion'),
        ('TIEMPO_MOMENTO',    0.85, 'periodo'),
        ('CONCEPTO_TIEMPO',   0.85, 'concepto'),
        ('TIEMPO_DIA',        0.85, 'periodo'),
        ('TIEMPO_SEMANA',     0.85, 'periodo'),
        ('TIEMPO_MES',        0.85, 'periodo'),
        ('FREQ_SIEMPRE',      0.90, 'frecuencia'),
        ('FREQ_NUNCA',        0.90, 'frecuencia'),
        ('FREQ_AVECES',       0.90, 'frecuencia'),
    ]

    for nodo_id, grounding, subtipo in conceptos_tiempo:
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

    _conectar_tiempo(red)


def _conectar_tiempo(red):
    conexiones = [
        ('TIEMPO_AHORA',   'BELL_CORE',           0.75),
        ('TIEMPO_AHORA',   'NEURONA_SEBASTIAN',   0.75),
        ('TIEMPO_HOY',     'NEURONA_SEBASTIAN',   0.75),
        ('TIEMPO_MANANA',  'CONSEJERA_IRIS',      0.80),
        ('TIEMPO_MANANA',  'VALOR_CRECIMIENTO',   0.70),
        ('TIEMPO_SIEMPRE', 'BELL_CORE',           0.80),
        ('TIEMPO_SIEMPRE', 'VALOR_PRESENCIA_REAL',0.75),
        ('FREQ_SIEMPRE',   'BELL_CORE',           0.75),
        ('FREQ_NUNCA',     'CONSEJERA_VEGA',      0.70),
    ]

    for origen, destino, peso in conexiones:
        if red.existe_nodo(origen) and red.existe_nodo(destino):
            red.conectar(origen, destino, peso, 'relacionado_con')