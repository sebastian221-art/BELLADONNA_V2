# biblioteca/vocabulario/base/gastronomia.py
# ================================================
# VOCABULARIO GASTRONOMÍA Y COMIDA
# ================================================

CONCEPTOS_GASTRONOMIA = {

    # ── Comidas colombianas ───────────────────────
    'arepas': {
        'id': 'GAS_AREPAS', 'tipo': 'comida',
        'variantes': ['arepa','arepas','arepa de choclo','arepa de maíz'],
        'grounding_base': 0.72,
    },
    'bandeja': {
        'id': 'GAS_BANDEJA', 'tipo': 'comida',
        'variantes': ['bandeja paisa','bandeja','frijoles','chicharrón'],
        'grounding_base': 0.72,
    },
    'empanadas': {
        'id': 'GAS_EMPANADAS', 'tipo': 'comida',
        'variantes': ['empanada','empanadas','empanadicta'],
        'grounding_base': 0.72,
    },
    'cafe': {
        'id': 'GAS_CAFE', 'tipo': 'bebida',
        'variantes': ['café','cafe','tinto','un tinto','tomando café','café colombiano'],
        'grounding_base': 0.75,
    },

    # ── Comidas generales ─────────────────────────
    'pizza': {
        'id': 'GAS_PIZZA', 'tipo': 'comida',
        'variantes': ['pizza','una pizza','pedir pizza','pedí pizza'],
        'grounding_base': 0.70,
    },
    'hamburguesa': {
        'id': 'GAS_HAMBURGUESA', 'tipo': 'comida',
        'variantes': ['hamburguesa','burger','una hamburguesa'],
        'grounding_base': 0.70,
    },
    'domicilio': {
        'id': 'GAS_DOMICILIO', 'tipo': 'servicio',
        'variantes': ['domicilio','pedir domicilio','rappi','ifood','pedí comida',
                      'voy a pedir','qué pido'],
        'grounding_base': 0.73,
    },
    'hambre': {
        'id': 'GAS_HAMBRE', 'tipo': 'estado',
        'variantes': ['hambre','tengo hambre','muero de hambre','estoy con hambre',
                      'no he comido','no comí'],
        'grounding_base': 0.80,
    },
    'agua': {
        'id': 'GAS_AGUA', 'tipo': 'bebida',
        'variantes': ['agua','tomar agua','un vaso de agua','sed','tengo sed'],
        'grounding_base': 0.73,
    },
}


# ── Expresiones expandidas ────────────────────────────────

CONCEPTOS_EXPRESIONES = {

    # ── Intensificadores ──────────────────────────
    'muy': {
        'id': 'EXP_MUY', 'tipo': 'intensificador',
        'variantes': ['muy','demasiado','súper','super','re','requete','hiper',
                      'mega','ultra','extremadamente'],
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
                      'de siempre','toda la vida'],
        'grounding_base': 0.72,
    },
    'nunca': {
        'id': 'EXP_NUNCA', 'tipo': 'temporalidad',
        'variantes': ['nunca','jamás','jamas','ni una vez','en mi vida'],
        'grounding_base': 0.72,
    },

    # ── Afirmaciones expandidas ───────────────────
    'claro': {
        'id': 'EXP_CLARO', 'tipo': 'afirmacion',
        'variantes': ['claro','claro que sí','claro que si','obvio','por supuesto',
                      'efectivamente','exactamente','exacto','correcto','así es'],
        'grounding_base': 0.80,
    },
    'dale': {
        'id': 'EXP_DALE', 'tipo': 'afirmacion_informal',
        'variantes': ['dale','dale pues','listo','ok','okay','sí','si','venga','va'],
        'grounding_base': 0.83,
    },

    # ── Negaciones expandidas ─────────────────────
    'no_way': {
        'id': 'EXP_NO_WAY', 'tipo': 'negacion_enfatica',
        'variantes': ['no way','de ninguna manera','imposible','qué va','qué va pues',
                      'para nada','ni de chiste','ni loco','ni loca'],
        'grounding_base': 0.78,
    },

    # ── Expresiones de sorpresa ───────────────────
    'sorpresa': {
        'id': 'EXP_SORPRESA', 'tipo': 'emocion_expresion',
        'variantes': ['no me digas','en serio','enserio','no puede ser','de verdad',
                      'qué','wow','wao','increíble','increible','no lo puedo creer'],
        'grounding_base': 0.75,
    },

    # ── Expresiones de duda ───────────────────────
    'quizas': {
        'id': 'EXP_QUIZAS', 'tipo': 'incertidumbre',
        'variantes': ['quizás','quizas','tal vez','a lo mejor','puede que','capaz',
                      'capaz que sí','no sé si','depende'],
        'grounding_base': 0.73,
    },

    # ── Expresiones temporales cotidianas ─────────
    'ahora': {
        'id': 'EXP_AHORA', 'tipo': 'tiempo',
        'variantes': ['ahora','ahorita','ya','en este momento','en este rato',
                      'ahora mismo','de una vez'],
        'grounding_base': 0.75,
    },
    'despues': {
        'id': 'EXP_DESPUES', 'tipo': 'tiempo',
        'variantes': ['después','despues','luego','más tarde','más adelante',
                      'en un rato','cuando pueda','ahorita más tarde'],
        'grounding_base': 0.72,
    },
    'hoy': {
        'id': 'EXP_HOY', 'tipo': 'tiempo',
        'variantes': ['hoy','este día','hoy en el día','hoy en la mañana',
                      'hoy en la tarde','hoy en la noche'],
        'grounding_base': 0.75,
    },
    'ayer': {
        'id': 'EXP_AYER', 'tipo': 'tiempo',
        'variantes': ['ayer','el día de ayer','ayer en la noche','ayer en la tarde'],
        'grounding_base': 0.73,
    },
    'manana_tiempo': {
        'id': 'EXP_MANANA', 'tipo': 'tiempo',
        'variantes': ['mañana','manana','el día de mañana','para mañana'],
        'grounding_base': 0.73,
    },

    # ── Conectores de conversación ────────────────
    'por_cierto': {
        'id': 'EXP_POR_CIERTO', 'tipo': 'conector',
        'variantes': ['por cierto','a propósito','a proposito','hablando de eso',
                      'ya que hablamos','cambiando el tema','otra cosa'],
        'grounding_base': 0.75,
    },
    'o_sea': {
        'id': 'EXP_O_SEA', 'tipo': 'conector',
        'variantes': ['o sea','osea','es decir','o sea que','quiero decir'],
        'grounding_base': 0.73,
    },
    'bueno': {
        'id': 'EXP_BUENO', 'tipo': 'conector',
        'variantes': ['bueno','pues','pues bien','entonces','así que','así'],
        'grounding_base': 0.70,
    },

    # ── Expresiones de acuerdo parcial ───────────
    'de_acuerdo': {
        'id': 'EXP_ACUERDO', 'tipo': 'acuerdo',
        'variantes': ['de acuerdo','entendido','entiendo','ya veo','ya entiendo',
                      'tiene sentido','tiene razón','tienes razón','sí, sí'],
        'grounding_base': 0.78,
    },

    # ── Pedir aclaración ──────────────────────────
    'no_entendi': {
        'id': 'EXP_NO_ENTENDI', 'tipo': 'solicitud_aclaracion',
        'variantes': ['no entendí','no entendi','no entiendo','me puedes explicar',
                      'no me quedó claro','qué quisiste decir','cómo así','como así'],
        'grounding_base': 0.80,
    },

    # ── Expresiones de cansancio conversacional ───
    'ya_se': {
        'id': 'EXP_YA_SE', 'tipo': 'expresion',
        'variantes': ['ya sé','ya se','ya lo sé','sí ya sé','ya lo sabía'],
        'grounding_base': 0.73,
    },
    'en_serio': {
        'id': 'EXP_EN_SERIO', 'tipo': 'expresion',
        'variantes': ['en serio','enserio','de verdad','de verdad verdad',
                      'literalmente','literal'],
        'grounding_base': 0.73,
    },
}