# biblioteca/vocabulario/base/tiempo.py
# ================================================
# TIEMPO Y TEMPORALIDAD
# Referencias al tiempo que Bell necesita entender
# ================================================

TIEMPO = {
    # Momentos
    'ahora':       {'id': 'TIEMPO_AHORA',     'grounding': 0.95, 'tipo': 'tiempo_presente'},
    'hoy':         {'id': 'TIEMPO_HOY',       'grounding': 0.95, 'tipo': 'tiempo_presente'},
    'ayer':        {'id': 'TIEMPO_AYER',       'grounding': 0.90, 'tipo': 'tiempo_pasado'},
    'mañana':      {'id': 'TIEMPO_MANANA',     'grounding': 0.90, 'tipo': 'tiempo_futuro'},
    'manana':      {'id': 'TIEMPO_MANANA',     'grounding': 0.85, 'tipo': 'tiempo_futuro'},
    'después':     {'id': 'TIEMPO_DESPUES',    'grounding': 0.90, 'tipo': 'tiempo_futuro'},
    'despues':     {'id': 'TIEMPO_DESPUES',    'grounding': 0.85, 'tipo': 'tiempo_futuro'},
    'antes':       {'id': 'TIEMPO_ANTES',      'grounding': 0.90, 'tipo': 'tiempo_pasado'},
    'luego':       {'id': 'TIEMPO_LUEGO',      'grounding': 0.85, 'tipo': 'tiempo_futuro'},
    'pronto':      {'id': 'TIEMPO_PRONTO',     'grounding': 0.85, 'tipo': 'tiempo_futuro'},
    'ya':          {'id': 'TIEMPO_YA',         'grounding': 0.80, 'tipo': 'tiempo_presente'},
    'todavía':     {'id': 'TIEMPO_TODAVIA',    'grounding': 0.85, 'tipo': 'tiempo_continuidad'},
    'todavia':     {'id': 'TIEMPO_TODAVIA',    'grounding': 0.80, 'tipo': 'tiempo_continuidad'},
    'aún':         {'id': 'TIEMPO_AUN',        'grounding': 0.85, 'tipo': 'tiempo_continuidad'},
    'aun':         {'id': 'TIEMPO_AUN',        'grounding': 0.80, 'tipo': 'tiempo_continuidad'},
    'siempre':     {'id': 'TIEMPO_SIEMPRE',    'grounding': 0.90, 'tipo': 'tiempo_permanencia'},
    'nunca':       {'id': 'TIEMPO_NUNCA',      'grounding': 0.90, 'tipo': 'tiempo_negacion'},

    # Períodos
    'momento':     {'id': 'TIEMPO_MOMENTO',    'grounding': 0.85, 'tipo': 'periodo'},
    'rato':        {'id': 'TIEMPO_RATO',       'grounding': 0.80, 'tipo': 'periodo'},
    'tiempo':      {'id': 'CONCEPTO_TIEMPO',   'grounding': 0.85, 'tipo': 'concepto'},
    'día':         {'id': 'TIEMPO_DIA',        'grounding': 0.85, 'tipo': 'periodo'},
    'dia':         {'id': 'TIEMPO_DIA',        'grounding': 0.80, 'tipo': 'periodo'},
    'semana':      {'id': 'TIEMPO_SEMANA',     'grounding': 0.85, 'tipo': 'periodo'},
    'mes':         {'id': 'TIEMPO_MES',        'grounding': 0.85, 'tipo': 'periodo'},
    'año':         {'id': 'TIEMPO_ANO',        'grounding': 0.85, 'tipo': 'periodo'},
    'hora':        {'id': 'TIEMPO_HORA',       'grounding': 0.85, 'tipo': 'periodo'},
    'minuto':      {'id': 'TIEMPO_MINUTO',     'grounding': 0.85, 'tipo': 'periodo'},

    # Frecuencia
    'siempre':     {'id': 'FREQ_SIEMPRE',      'grounding': 0.90, 'tipo': 'frecuencia'},
    'nunca':       {'id': 'FREQ_NUNCA',        'grounding': 0.90, 'tipo': 'frecuencia'},
    'a veces':     {'id': 'FREQ_AVECES',       'grounding': 0.90, 'tipo': 'frecuencia'},
    'aveces':      {'id': 'FREQ_AVECES',       'grounding': 0.85, 'tipo': 'frecuencia'},
    'frecuente':   {'id': 'FREQ_FRECUENTE',    'grounding': 0.85, 'tipo': 'frecuencia'},
    'seguido':     {'id': 'FREQ_SEGUIDO',      'grounding': 0.85, 'tipo': 'frecuencia'},
    'rara vez':    {'id': 'FREQ_RARAMENTE',    'grounding': 0.85, 'tipo': 'frecuencia'},
}