# biblioteca/vocabulario/base/tiempo.py
# ================================================
# TIEMPO Y TEMPORALIDAD
# Referencias al tiempo que Bell necesita entender
# ================================================

TIEMPO = {
    # Momentos
    'ahora':       {'id': 'TIEMPO_AHORA',     'grounding_base': 0.95, 'tipo': 'tiempo_presente', 'variantes': []},
    'hoy':         {'id': 'TIEMPO_HOY',       'grounding_base': 0.95, 'tipo': 'tiempo_presente', 'variantes': []},
    'ayer':        {'id': 'TIEMPO_AYER',       'grounding_base': 0.90, 'tipo': 'tiempo_pasado', 'variantes': []},
    'mañana':      {'id': 'TIEMPO_MANANA',     'grounding_base': 0.90, 'tipo': 'tiempo_futuro', 'variantes': []},
    'manana':      {'id': 'TIEMPO_MANANA',     'grounding_base': 0.85, 'tipo': 'tiempo_futuro', 'variantes': []},
    'después':     {'id': 'TIEMPO_DESPUES',    'grounding_base': 0.90, 'tipo': 'tiempo_futuro', 'variantes': []},
    'despues':     {'id': 'TIEMPO_DESPUES',    'grounding_base': 0.85, 'tipo': 'tiempo_futuro', 'variantes': []},
    'antes':       {'id': 'TIEMPO_ANTES',      'grounding_base': 0.90, 'tipo': 'tiempo_pasado', 'variantes': []},
    'luego':       {'id': 'TIEMPO_LUEGO',      'grounding_base': 0.85, 'tipo': 'tiempo_futuro', 'variantes': []},
    'pronto':      {'id': 'TIEMPO_PRONTO',     'grounding_base': 0.85, 'tipo': 'tiempo_futuro', 'variantes': []},
    'ya':          {'id': 'TIEMPO_YA',         'grounding_base': 0.80, 'tipo': 'tiempo_presente', 'variantes': []},
    'todavía':     {'id': 'TIEMPO_TODAVIA',    'grounding_base': 0.85, 'tipo': 'tiempo_continuidad', 'variantes': []},
    'todavia':     {'id': 'TIEMPO_TODAVIA',    'grounding_base': 0.80, 'tipo': 'tiempo_continuidad', 'variantes': []},
    'aún':         {'id': 'TIEMPO_AUN',        'grounding_base': 0.85, 'tipo': 'tiempo_continuidad', 'variantes': []},
    'aun':         {'id': 'TIEMPO_AUN',        'grounding_base': 0.80, 'tipo': 'tiempo_continuidad', 'variantes': []},
    'siempre':     {'id': 'TIEMPO_SIEMPRE',    'grounding_base': 0.90, 'tipo': 'tiempo_permanencia', 'variantes': []},
    'nunca':       {'id': 'TIEMPO_NUNCA',      'grounding_base': 0.90, 'tipo': 'tiempo_negacion', 'variantes': []},

    # Períodos
    'momento':     {'id': 'TIEMPO_MOMENTO',    'grounding_base': 0.85, 'tipo': 'periodo', 'variantes': []},
    'rato':        {'id': 'TIEMPO_RATO',       'grounding_base': 0.80, 'tipo': 'periodo', 'variantes': []},
    'tiempo':      {'id': 'CONCEPTO_TIEMPO',   'grounding_base': 0.85, 'tipo': 'concepto', 'variantes': []},
    'día':         {'id': 'TIEMPO_DIA',        'grounding_base': 0.85, 'tipo': 'periodo', 'variantes': []},
    'dia':         {'id': 'TIEMPO_DIA',        'grounding_base': 0.80, 'tipo': 'periodo', 'variantes': []},
    'semana':      {'id': 'TIEMPO_SEMANA',     'grounding_base': 0.85, 'tipo': 'periodo', 'variantes': []},
    'mes':         {'id': 'TIEMPO_MES',        'grounding_base': 0.85, 'tipo': 'periodo', 'variantes': []},
    'año':         {'id': 'TIEMPO_ANO',        'grounding_base': 0.85, 'tipo': 'periodo', 'variantes': []},
    'hora':        {'id': 'TIEMPO_HORA',       'grounding_base': 0.85, 'tipo': 'periodo', 'variantes': []},
    'minuto':      {'id': 'TIEMPO_MINUTO',     'grounding_base': 0.85, 'tipo': 'periodo', 'variantes': []},

    # Frecuencia
    'siempre':     {'id': 'FREQ_SIEMPRE',      'grounding_base': 0.90, 'tipo': 'frecuencia', 'variantes': []},
    'nunca':       {'id': 'FREQ_NUNCA',        'grounding_base': 0.90, 'tipo': 'frecuencia', 'variantes': []},
    'a veces':     {'id': 'FREQ_AVECES',       'grounding_base': 0.90, 'tipo': 'frecuencia', 'variantes': []},
    'aveces':      {'id': 'FREQ_AVECES',       'grounding_base': 0.85, 'tipo': 'frecuencia', 'variantes': []},
    'frecuente':   {'id': 'FREQ_FRECUENTE',    'grounding_base': 0.85, 'tipo': 'frecuencia', 'variantes': []},
    'seguido':     {'id': 'FREQ_SEGUIDO',      'grounding_base': 0.85, 'tipo': 'frecuencia', 'variantes': []},
    'rara vez':    {'id': 'FREQ_RARAMENTE',    'grounding_base': 0.85, 'tipo': 'frecuencia', 'variantes': []},
}