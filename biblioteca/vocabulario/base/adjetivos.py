# biblioteca/vocabulario/base/adjetivos.py
# ================================================
# ADJETIVOS — Descriptivos, evaluativos, físicos
# Bell necesita estos para entender descripciones
# ================================================

ADJETIVOS = {

    # ── TAMAÑO ───────────────────────────────────
    'grande':      {'id': 'ADJ_GRANDE',     'tipo': 'adjetivo_tamaño',    'grounding_base': 0.88, 'variantes': ['gran', 'grandes']},
    'pequeño':     {'id': 'ADJ_PEQUEÑO',    'tipo': 'adjetivo_tamaño',    'grounding_base': 0.88, 'variantes': ['pequeña', 'pequeños', 'chico', 'chica', 'chiquito']},
    'enorme':      {'id': 'ADJ_ENORME',     'tipo': 'adjetivo_tamaño',    'grounding_base': 0.85, 'variantes': ['enorme', 'enormes', 'gigante', 'gigantesco']},
    'mínimo':      {'id': 'ADJ_MINIMO',     'tipo': 'adjetivo_tamaño',    'grounding_base': 0.82, 'variantes': ['minimo', 'mínima', 'minima']},
    'máximo':      {'id': 'ADJ_MAXIMO',     'tipo': 'adjetivo_tamaño',    'grounding_base': 0.82, 'variantes': ['maximo', 'máxima', 'maxima']},
    'medio':       {'id': 'ADJ_MEDIO',      'tipo': 'adjetivo_tamaño',    'grounding_base': 0.82, 'variantes': ['media', 'mediano', 'mediana']},

    # ── VALORACIÓN GENERAL ───────────────────────
    'bueno':       {'id': 'ADJ_BUENO',      'tipo': 'adjetivo_valoracion', 'grounding_base': 0.90, 'variantes': ['buena', 'buenos', 'buenas', 'buen']},
    'malo':        {'id': 'ADJ_MALO',       'tipo': 'adjetivo_valoracion', 'grounding_base': 0.90, 'variantes': ['mala', 'malos', 'malas', 'mal']},
    'mejor':       {'id': 'ADJ_MEJOR',      'tipo': 'adjetivo_valoracion', 'grounding_base': 0.90, 'variantes': ['mejores']},
    'peor':        {'id': 'ADJ_PEOR',       'tipo': 'adjetivo_valoracion', 'grounding_base': 0.88, 'variantes': ['peores']},
    'bonito':      {'id': 'ADJ_BONITO',     'tipo': 'adjetivo_valoracion', 'grounding_base': 0.85, 'variantes': ['bonita', 'bonitos', 'lindo', 'linda']},
    'feo':         {'id': 'ADJ_FEO',        'tipo': 'adjetivo_valoracion', 'grounding_base': 0.85, 'variantes': ['fea', 'feos', 'horrible']},
    'perfecto':    {'id': 'ADJ_PERFECTO',   'tipo': 'adjetivo_valoracion', 'grounding_base': 0.88, 'variantes': ['perfecta', 'perfectos']},
    'terrible':    {'id': 'ADJ_TERRIBLE',   'tipo': 'adjetivo_valoracion', 'grounding_base': 0.85, 'variantes': ['terribles', 'terrible']},
    'increíble':   {'id': 'ADJ_INCREIBLE',  'tipo': 'adjetivo_valoracion', 'grounding_base': 0.87, 'variantes': ['increible', 'increíbles']},
    'genial':      {'id': 'ADJ_GENIAL',     'tipo': 'adjetivo_valoracion', 'grounding_base': 0.87, 'variantes': ['geniales']},
    'importante':  {'id': 'ADJ_IMPORTANTE', 'tipo': 'adjetivo_valoracion', 'grounding_base': 0.90, 'variantes': ['importantes']},
    'especial':    {'id': 'ADJ_ESPECIAL',   'tipo': 'adjetivo_valoracion', 'grounding_base': 0.87, 'variantes': ['especiales']},
    'normal':      {'id': 'ADJ_NORMAL',     'tipo': 'adjetivo_valoracion', 'grounding_base': 0.85, 'variantes': ['normales']},
    'raro':        {'id': 'ADJ_RARO',       'tipo': 'adjetivo_valoracion', 'grounding_base': 0.83, 'variantes': ['rara', 'raros', 'extraño', 'extraña']},
    'simple':      {'id': 'ADJ_SIMPLE',     'tipo': 'adjetivo_valoracion', 'grounding_base': 0.83, 'variantes': ['simples', 'sencillo', 'sencilla']},
    'complejo':    {'id': 'ADJ_COMPLEJO',   'tipo': 'adjetivo_valoracion', 'grounding_base': 0.85, 'variantes': ['compleja', 'complejos', 'complicado', 'complicada']},
    'útil':        {'id': 'ADJ_UTIL',       'tipo': 'adjetivo_valoracion', 'grounding_base': 0.85, 'variantes': ['util', 'útiles', 'utiles']},
    'inútil':      {'id': 'ADJ_INUTIL',     'tipo': 'adjetivo_valoracion', 'grounding_base': 0.85, 'variantes': ['inutil', 'inútiles']},
    'necesario':   {'id': 'ADJ_NECESARIO',  'tipo': 'adjetivo_valoracion', 'grounding_base': 0.87, 'variantes': ['necesaria', 'necesarios', 'necesarias']},
    'suficiente':  {'id': 'ADJ_SUFICIENTE', 'tipo': 'adjetivo_valoracion', 'grounding_base': 0.83, 'variantes': ['suficientes']},
    'posible':     {'id': 'ADJ_POSIBLE',    'tipo': 'adjetivo_valoracion', 'grounding_base': 0.87, 'variantes': ['posibles', 'imposible', 'imposibles']},
    'real':        {'id': 'ADJ_REAL',       'tipo': 'adjetivo_valoracion', 'grounding_base': 0.88, 'variantes': ['reales', 'verdadero', 'verdadera']},
    'falso':       {'id': 'ADJ_FALSO',      'tipo': 'adjetivo_valoracion', 'grounding_base': 0.85, 'variantes': ['falsa', 'falsos']},
    'correcto':    {'id': 'ADJ_CORRECTO',   'tipo': 'adjetivo_valoracion', 'grounding_base': 0.87, 'variantes': ['correcta', 'correctos', 'correcto']},
    'incorrecto':  {'id': 'ADJ_INCORRECTO', 'tipo': 'adjetivo_valoracion', 'grounding_base': 0.85, 'variantes': ['incorrecta', 'incorrectos', 'erróneo', 'erroneo']},
    'distinto':    {'id': 'ADJ_DISTINTO',   'tipo': 'adjetivo_valoracion', 'grounding_base': 0.83, 'variantes': ['distinta', 'distintos', 'diferente', 'diferentes']},
    'igual':       {'id': 'ADJ_IGUAL',      'tipo': 'adjetivo_valoracion', 'grounding_base': 0.85, 'variantes': ['iguales', 'mismo', 'misma']},

    # ── TEMPORALES ───────────────────────────────
    'nuevo':       {'id': 'ADJ_NUEVO',      'tipo': 'adjetivo_temporal',   'grounding_base': 0.87, 'variantes': ['nueva', 'nuevos', 'nuevas']},
    'viejo':       {'id': 'ADJ_VIEJO',      'tipo': 'adjetivo_temporal',   'grounding_base': 0.85, 'variantes': ['vieja', 'viejos', 'viejas', 'antiguo', 'antigua']},
    'reciente':    {'id': 'ADJ_RECIENTE',   'tipo': 'adjetivo_temporal',   'grounding_base': 0.83, 'variantes': ['recientes']},
    'último':      {'id': 'ADJ_ULTIMO',     'tipo': 'adjetivo_temporal',   'grounding_base': 0.87, 'variantes': ['ultimo', 'última', 'ultima', 'últimos']},
    'primero':     {'id': 'ADJ_PRIMERO',    'tipo': 'adjetivo_temporal',   'grounding_base': 0.87, 'variantes': ['primer', 'primera', 'primeros', 'primeras']},
    'siguiente':   {'id': 'ADJ_SIGUIENTE',  'tipo': 'adjetivo_temporal',   'grounding_base': 0.83, 'variantes': ['siguientes', 'próximo', 'proximo']},
    'anterior':    {'id': 'ADJ_ANTERIOR',   'tipo': 'adjetivo_temporal',   'grounding_base': 0.82, 'variantes': ['anteriores', 'pasado', 'pasada']},

    # ── FÍSICOS ──────────────────────────────────
    'alto':        {'id': 'ADJ_ALTO',       'tipo': 'adjetivo_fisico',     'grounding_base': 0.85, 'variantes': ['alta', 'altos', 'altas']},
    'bajo':        {'id': 'ADJ_BAJO',       'tipo': 'adjetivo_fisico',     'grounding_base': 0.85, 'variantes': ['baja', 'bajos', 'bajas']},
    'delgado':     {'id': 'ADJ_DELGADO',    'tipo': 'adjetivo_fisico',     'grounding_base': 0.82, 'variantes': ['delgada', 'flaco', 'flaca']},
    'gordo':       {'id': 'ADJ_GORDO',      'tipo': 'adjetivo_fisico',     'grounding_base': 0.80, 'variantes': ['gorda', 'gordos', 'gordas', 'robusto']},
    'fuerte':      {'id': 'ADJ_FUERTE',     'tipo': 'adjetivo_fisico',     'grounding_base': 0.85, 'variantes': ['fuertes', 'resistente']},
    'débil':       {'id': 'ADJ_DEBIL',      'tipo': 'adjetivo_fisico',     'grounding_base': 0.83, 'variantes': ['debil', 'débiles']},
    'rápido':      {'id': 'ADJ_RAPIDO',     'tipo': 'adjetivo_fisico',     'grounding_base': 0.87, 'variantes': ['rapido', 'rápida', 'rapida', 'rápidos', 'veloz']},
    'lento':       {'id': 'ADJ_LENTO',      'tipo': 'adjetivo_fisico',     'grounding_base': 0.87, 'variantes': ['lenta', 'lentos', 'lentas']},
    'caliente':    {'id': 'ADJ_CALIENTE',   'tipo': 'adjetivo_fisico',     'grounding_base': 0.85, 'variantes': ['calientes', 'calor', 'cálido']},
    'frío':        {'id': 'ADJ_FRIO',       'tipo': 'adjetivo_fisico',     'grounding_base': 0.85, 'variantes': ['frio', 'fría', 'fria', 'frívolo']},
    'duro':        {'id': 'ADJ_DURO',       'tipo': 'adjetivo_fisico',     'grounding_base': 0.82, 'variantes': ['dura', 'duros', 'duras']},
    'suave':       {'id': 'ADJ_SUAVE',      'tipo': 'adjetivo_fisico',     'grounding_base': 0.82, 'variantes': ['suaves', 'blando', 'blanda']},
    'limpio':      {'id': 'ADJ_LIMPIO',     'tipo': 'adjetivo_fisico',     'grounding_base': 0.83, 'variantes': ['limpia', 'limpios', 'limpias']},
    'sucio':       {'id': 'ADJ_SUCIO',      'tipo': 'adjetivo_fisico',     'grounding_base': 0.82, 'variantes': ['sucia', 'sucios', 'sucias']},
    'lleno':       {'id': 'ADJ_LLENO',      'tipo': 'adjetivo_fisico',     'grounding_base': 0.83, 'variantes': ['llena', 'llenos', 'llenas']},
    'vacío':       {'id': 'ADJ_VACIO',      'tipo': 'adjetivo_fisico',     'grounding_base': 0.85, 'variantes': ['vacio', 'vacía', 'vacia', 'vacíos']},
    'abierto':     {'id': 'ADJ_ABIERTO',    'tipo': 'adjetivo_fisico',     'grounding_base': 0.83, 'variantes': ['abierta', 'abiertos']},
    'cerrado':     {'id': 'ADJ_CERRADO',    'tipo': 'adjetivo_fisico',     'grounding_base': 0.83, 'variantes': ['cerrada', 'cerrados']},
    'oscuro':      {'id': 'ADJ_OSCURO',     'tipo': 'adjetivo_fisico',     'grounding_base': 0.82, 'variantes': ['oscura', 'oscuros', 'oscuras']},
    'claro':       {'id': 'ADJ_CLARO',      'tipo': 'adjetivo_fisico',     'grounding_base': 0.83, 'variantes': ['clara', 'claros', 'claras']},

    # ── DIFICULTAD Y CAPACIDAD ───────────────────
    'fácil':       {'id': 'ADJ_FACIL',      'tipo': 'adjetivo_dificultad', 'grounding_base': 0.88, 'variantes': ['facil', 'fáciles', 'sencillo']},
    'difícil':     {'id': 'ADJ_DIFICIL',    'tipo': 'adjetivo_dificultad', 'grounding_base': 0.90, 'variantes': ['dificil', 'difíciles', 'complicado', 'complicada', 'complejo']},
    'imposible':   {'id': 'ADJ_IMPOSIBLE',  'tipo': 'adjetivo_dificultad', 'grounding_base': 0.87, 'variantes': ['imposibles']},
    'capaz':       {'id': 'ADJ_CAPAZ',      'tipo': 'adjetivo_capacidad',  'grounding_base': 0.87, 'variantes': ['capaces', 'capaz']},
    'listo':       {'id': 'ADJ_LISTO',      'tipo': 'adjetivo_capacidad',  'grounding_base': 0.85, 'variantes': ['lista', 'listos', 'preparado']},
    'inteligente': {'id': 'ADJ_INTELIGENTE','tipo': 'adjetivo_capacidad',  'grounding_base': 0.87, 'variantes': ['inteligentes', 'listo', 'lista']},

    # ── SOCIALES Y RELACIONALES ───────────────────
    'solo':        {'id': 'ADJ_SOLO',       'tipo': 'adjetivo_social',     'grounding_base': 0.88, 'variantes': ['sola', 'solos', 'solas', 'solito']},
    'junto':       {'id': 'ADJ_JUNTO',      'tipo': 'adjetivo_social',     'grounding_base': 0.83, 'variantes': ['junta', 'juntos', 'juntas']},
    'amable':      {'id': 'ADJ_AMABLE',     'tipo': 'adjetivo_social',     'grounding_base': 0.85, 'variantes': ['amables', 'amigable']},
    'honesto':     {'id': 'ADJ_HONESTO',    'tipo': 'adjetivo_social',     'grounding_base': 0.87, 'variantes': ['honesta', 'honestos', 'sincero', 'sincera']},
    'confiable':   {'id': 'ADJ_CONFIABLE',  'tipo': 'adjetivo_social',     'grounding_base': 0.87, 'variantes': ['confiables', 'de confianza']},
    'seguro':      {'id': 'ADJ_SEGURO',     'tipo': 'adjetivo_social',     'grounding_base': 0.85, 'variantes': ['segura', 'seguros']},

    # ── ESTADO ───────────────────────────────────
    'activo':      {'id': 'ADJ_ACTIVO',     'tipo': 'adjetivo_estado',     'grounding_base': 0.83, 'variantes': ['activa', 'activos']},
    'ocupado':     {'id': 'ADJ_OCUPADO',    'tipo': 'adjetivo_estado',     'grounding_base': 0.85, 'variantes': ['ocupada', 'ocupados']},
    'libre':       {'id': 'ADJ_LIBRE',      'tipo': 'adjetivo_estado',     'grounding_base': 0.85, 'variantes': ['libres', 'disponible']},
    'roto':        {'id': 'ADJ_ROTO',       'tipo': 'adjetivo_estado',     'grounding_base': 0.83, 'variantes': ['rota', 'rotos', 'dañado', 'dañada']},
    'funcionando': {'id': 'ADJ_FUNC',       'tipo': 'adjetivo_estado',     'grounding_base': 0.85, 'variantes': ['funcionando bien', 'andando']},
    'listo':       {'id': 'ADJ_LISTO2',     'tipo': 'adjetivo_estado',     'grounding_base': 0.85, 'variantes': ['lista', 'listos', 'terminado', 'terminada']},
    'perdido':     {'id': 'ADJ_PERDIDO',    'tipo': 'adjetivo_estado',     'grounding_base': 0.85, 'variantes': ['perdida', 'perdidos']},

    # ── CANTIDAD ─────────────────────────────────
    'completo':    {'id': 'ADJ_COMPLETO',   'tipo': 'adjetivo_cantidad',   'grounding_base': 0.85, 'variantes': ['completa', 'completos', 'entero', 'entera']},
    'parcial':     {'id': 'ADJ_PARCIAL',    'tipo': 'adjetivo_cantidad',   'grounding_base': 0.82, 'variantes': ['parciales', 'incompleto', 'incompleta']},
    'único':       {'id': 'ADJ_UNICO',      'tipo': 'adjetivo_cantidad',   'grounding_base': 0.85, 'variantes': ['unico', 'única', 'unica', 'únicos', 'solo']},
    'múltiple':    {'id': 'ADJ_MULTIPLE',   'tipo': 'adjetivo_cantidad',   'grounding_base': 0.82, 'variantes': ['multiple', 'múltiples', 'multiples', 'varios', 'varias']},
}
