# biblioteca/vocabulario/base/colombia.py
# ================================================
# VOCABULARIO COLOMBIANO — expresiones locales
# Bell entiende como habla Sebastian de verdad
# ================================================

CONCEPTOS_COLOMBIA = {

    # ── Saludos y apelaciones ─────────────────────
    'parce': {
        'id': 'COL_PARCE', 'tipo': 'apelacion_cercana',
        'variantes': ['parce','parcero','parcera','llave','llavecita'],
        'grounding_base': 0.80,
        'contexto': 'apelacion_afectiva',
    },
    'marica': {
        'id': 'COL_MARICA', 'tipo': 'apelacion_cercana',
        'variantes': ['marica','marica no','marica sí','ay marica'],
        'grounding_base': 0.80,
        'contexto': 'apelacion_informal',
    },
    'mane': {
        'id': 'COL_MANE', 'tipo': 'apelacion_cercana',
        'variantes': ['mane','man','ese man','ese mane'],
        'grounding_base': 0.78,
    },
    'chino': {
        'id': 'COL_CHINO', 'tipo': 'apelacion',
        'variantes': ['chino','china','el chino','la china'],
        'grounding_base': 0.75,
    },
    'cucho': {
        'id': 'COL_CUCHO', 'tipo': 'familiar',
        'variantes': ['cucho','cucha','mi cucho','mi cucha'],
        'grounding_base': 0.78,
        'contexto': 'referencia_a_padres',
    },
    'hemano': {
        'id': 'COL_HERMANO', 'tipo': 'apelacion_cercana',
        'variantes': ['hermano','hermana','mi hermano','bro'],
        'grounding_base': 0.78,
    },

    # ── Expresiones positivas ─────────────────────
    'bacano': {
        'id': 'COL_BACANO', 'tipo': 'expresion_positiva',
        'variantes': ['bacano','bacana','qué bacano','está bacano','estuvo bacano'],
        'grounding_base': 0.82,
        'emocion': 'entusiasmo',
    },
    'chevere': {
        'id': 'COL_CHEVERE', 'tipo': 'expresion_positiva',
        'variantes': ['chévere','chevere','qué chévere','está chévere','muy chévere'],
        'grounding_base': 0.82,
        'emocion': 'entusiasmo',
    },
    'de_una': {
        'id': 'COL_DE_UNA', 'tipo': 'expresion_acuerdo',
        'variantes': ['de una','de una vez','dale de una','vamos de una'],
        'grounding_base': 0.85,
        'contexto': 'confirmacion_entusiasta',
    },
    'qué_nota': {
        'id': 'COL_QUE_NOTA', 'tipo': 'expresion_positiva',
        'variantes': ['qué nota','es una nota','nota','estuvo nota','de nota'],
        'grounding_base': 0.80,
        'emocion': 'entusiasmo',
    },
    'brillante': {
        'id': 'COL_BRILLANTE', 'tipo': 'expresion_positiva',
        'variantes': ['brillante','qué brillante','es brillante','estuvo brillante'],
        'grounding_base': 0.78,
    },
    'chimba': {
        'id': 'COL_CHIMBA', 'tipo': 'expresion_positiva',
        'variantes': ['chimba','es una chimba','qué chimba','chimbita'],
        'grounding_base': 0.80,
        'emocion': 'entusiasmo',
    },

    # ── Expresiones negativas ─────────────────────
    'mamado': {
        'id': 'COL_MAMADO', 'tipo': 'expresion_negativa',
        'variantes': ['mamado','mamada','me tiene mamado','estoy mamado','ya me mamé'],
        'grounding_base': 0.82,
        'emocion': 'frustracion',
    },
    'jartera': {
        'id': 'COL_JARTERA', 'tipo': 'expresion_negativa',
        'variantes': ['jartera','qué jartera','es una jartera','me da jartera'],
        'grounding_base': 0.80,
        'emocion': 'frustracion',
    },
    'mamera': {
        'id': 'COL_MAMERA', 'tipo': 'expresion_negativa',
        'variantes': ['mamera','qué mamera','me da mamera','es una mamera'],
        'grounding_base': 0.80,
        'emocion': 'pereza',
    },
    'qué_oso': {
        'id': 'COL_QUE_OSO', 'tipo': 'expresion_verguenza',
        'variantes': ['qué oso','oso','pasé el oso','qué oso tan grande'],
        'grounding_base': 0.80,
        'emocion': 'verguenza',
    },

    # ── Actividades sociales ──────────────────────
    'rumba': {
        'id': 'COL_RUMBA', 'tipo': 'actividad_social',
        'variantes': ['rumba','rumbear','salir de rumba','fuimos a rumbear',
                      'rumba anoche','de rumba'],
        'grounding_base': 0.75,
    },
    'parche': {
        'id': 'COL_PARCHE', 'tipo': 'actividad_social',
        'variantes': ['parche','el parche','con el parche','con mi parche',
                      'hacer parche','vamos al parche'],
        'grounding_base': 0.75,
        'contexto': 'grupo_amigos',
    },
    'camellar': {
        'id': 'COL_CAMELLAR', 'tipo': 'accion',
        'variantes': ['camellar','camellando','camellé','a camellar',
                      'toca camellar'],
        'grounding_base': 0.75,
        'contexto': 'trabajar',
    },

    # ── Expresiones de acuerdo/desacuerdo ─────────
    'listo_col': {
        'id': 'COL_LISTO', 'tipo': 'confirmacion',
        'variantes': ['listo','ya listo','todo listo','quedó listo'],
        'grounding_base': 0.85,
    },
    'no_le_para': {
        'id': 'COL_NO_LE_PARA', 'tipo': 'expresion',
        'variantes': ['no le para','no para bolas','ni le para','sin darle bolas'],
        'grounding_base': 0.75,
        'contexto': 'ignorar_algo',
    },
    'pillar': {
        'id': 'COL_PILLAR', 'tipo': 'verbo',
        'variantes': ['pillar','lo pillé','pilla','pillé','no la pillé','pilas'],
        'grounding_base': 0.78,
        'contexto': 'entender_o_ver',
    },

    # ── Expresiones de cantidad/intensidad ────────
    'tenaz': {
        'id': 'COL_TENAZ', 'tipo': 'intensificador',
        'variantes': ['tenaz','está tenaz','es tenaz','qué tenaz'],
        'grounding_base': 0.78,
        'contexto': 'algo_intenso_o_dificil',
    },
    'full': {
        'id': 'COL_FULL', 'tipo': 'intensificador',
        'variantes': ['full','full de','estoy full','tengo full','a full'],
        'grounding_base': 0.75,
    },
    'mono': {
        'id': 'COL_MONO', 'tipo': 'calificativo',
        'variantes': ['qué mono','está mono','eso está mono'],
        'grounding_base': 0.72,
        'contexto': 'algo_bonito_o_gracioso',
    },
}