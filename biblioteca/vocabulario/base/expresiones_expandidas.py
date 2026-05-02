# biblioteca/vocabulario/base/expresiones_expandidas.py
# ================================================
# EXPRESIONES EXPANDIDAS — intensificadores,
# conectores, afirmaciones, negaciones y más
# ================================================

CONCEPTOS_EXPRESIONES = {

    # ── Intensificadores ──────────────────────────
    'muy': {
        'id': 'EXP_MUY', 'tipo': 'intensificador',
        'variantes': ['muy','demasiado','súper','super','re','requete',
                      'hiper','mega','ultra','extremadamente'],
        'grounding_base': 0.68,
    },
    'poco': {
        'id': 'EXP_POCO', 'tipo': 'cuantificador',
        'variantes': ['poco','poquito','algo','un poco','apenas','casi nada'],
        'grounding_base': 0.68,
    },
    'nada': {
        'id': 'EXP_NADA', 'tipo': 'negacion_total',
        'variantes': ['nada','para nada','absolutamente nada','cero','ni pizca'],
        'grounding_base': 0.73,
    },
    'siempre': {
        'id': 'EXP_SIEMPRE', 'tipo': 'temporalidad',
        'variantes': ['siempre','todo el tiempo','constantemente','sin parar',
                      'toda la vida'],
        'grounding_base': 0.72,
    },
    'nunca': {
        'id': 'EXP_NUNCA', 'tipo': 'temporalidad',
        'variantes': ['nunca','jamás','jamas','ni una vez','en mi vida'],
        'grounding_base': 0.72,
    },

    # ── Afirmaciones ──────────────────────────────
    'claro': {
        'id': 'EXP_CLARO', 'tipo': 'afirmacion',
        'variantes': ['claro','claro que sí','obvio','por supuesto',
                      'efectivamente','exactamente','exacto','correcto','así es'],
        'grounding_base': 0.80,
    },
    'dale': {
        'id': 'EXP_DALE', 'tipo': 'afirmacion_informal',
        'variantes': ['dale','dale pues','listo','ok','okay','sí','si','venga','va'],
        'grounding_base': 0.83,
    },

    # ── Negaciones ────────────────────────────────
    'no_way': {
        'id': 'EXP_NO_WAY', 'tipo': 'negacion_enfatica',
        'variantes': ['no way','de ninguna manera','imposible','qué va',
                      'para nada','ni de chiste','ni loco','ni loca'],
        'grounding_base': 0.78,
    },

    # ── Sorpresa ──────────────────────────────────
    'sorpresa': {
        'id': 'EXP_SORPRESA', 'tipo': 'emocion_expresion',
        'variantes': ['no me digas','en serio','enserio','no puede ser',
                      'de verdad','qué','wow','wao','increíble','no lo puedo creer'],
        'grounding_base': 0.75,
    },

    # ── Duda ─────────────────────────────────────
    'quizas': {
        'id': 'EXP_QUIZAS', 'tipo': 'incertidumbre',
        'variantes': ['quizás','quizas','tal vez','a lo mejor','puede que',
                      'capaz','capaz que sí','no sé si','depende'],
        'grounding_base': 0.73,
    },

    # ── Tiempo ────────────────────────────────────
    'ahora': {
        'id': 'EXP_AHORA', 'tipo': 'tiempo',
        'variantes': ['ahora','ahorita','ya','en este momento','ahora mismo','de una vez'],
        'grounding_base': 0.75,
    },
    'despues': {
        'id': 'EXP_DESPUES', 'tipo': 'tiempo',
        'variantes': ['después','despues','luego','más tarde','más adelante',
                      'en un rato','cuando pueda'],
        'grounding_base': 0.72,
    },
    'hoy': {
        'id': 'EXP_HOY', 'tipo': 'tiempo',
        'variantes': ['hoy','este día','hoy en la mañana','hoy en la tarde','hoy en la noche'],
        'grounding_base': 0.75,
    },
    'ayer': {
        'id': 'EXP_AYER', 'tipo': 'tiempo',
        'variantes': ['ayer','el día de ayer','ayer en la noche','ayer en la tarde'],
        'grounding_base': 0.73,
    },
    'manana': {
        'id': 'EXP_MANANA', 'tipo': 'tiempo',
        'variantes': ['mañana','manana','el día de mañana','para mañana'],
        'grounding_base': 0.73,
    },

    # ── Conectores ────────────────────────────────
    'por_cierto': {
        'id': 'EXP_POR_CIERTO', 'tipo': 'conector',
        'variantes': ['por cierto','a propósito','hablando de eso',
                      'cambiando el tema','otra cosa'],
        'grounding_base': 0.75,
    },
    'o_sea': {
        'id': 'EXP_O_SEA', 'tipo': 'conector',
        'variantes': ['o sea','osea','es decir','o sea que','quiero decir'],
        'grounding_base': 0.73,
    },
    'bueno': {
        'id': 'EXP_BUENO', 'tipo': 'conector',
        'variantes': ['bueno','pues','pues bien','entonces','así que'],
        'grounding_base': 0.70,
    },

    # ── Acuerdo ───────────────────────────────────
    'de_acuerdo': {
        'id': 'EXP_ACUERDO', 'tipo': 'acuerdo',
        'variantes': ['de acuerdo','entendido','entiendo','ya veo',
                      'tiene sentido','tienes razón','sí sí'],
        'grounding_base': 0.78,
    },

    # ── Pedir aclaración ──────────────────────────
    'no_entendi': {
        'id': 'EXP_NO_ENTENDI', 'tipo': 'solicitud_aclaracion',
        'variantes': ['no entendí','no entendi','no entiendo',
                      'me puedes explicar','no me quedó claro',
                      'cómo así','como así'],
        'grounding_base': 0.80,
    },

    # ── Expresiones comunes ───────────────────────
    'en_serio': {
        'id': 'EXP_EN_SERIO', 'tipo': 'expresion',
        'variantes': ['en serio','enserio','de verdad','de verdad verdad',
                      'literalmente','literal'],
        'grounding_base': 0.73,
    },
    'ya_se': {
        'id': 'EXP_YA_SE', 'tipo': 'expresion',
        'variantes': ['ya sé','ya se','ya lo sé','sí ya sé','ya lo sabía'],
        'grounding_base': 0.73,
    },
}