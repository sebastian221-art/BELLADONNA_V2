# biblioteca/vocabulario/base/conversacion_profunda.py
# ================================================
# VOCABULARIO CONVERSACIÓN PROFUNDA + RELACIONES
# Bell entiende cuando Sebastian reflexiona,
# habla de su vida, sus vínculos y sus metas
# ================================================

CONCEPTOS_PROFUNDO = {

    # ── Reflexión y pensamiento ───────────────────
    'pensar': {
        'id': 'PROF_PENSAR', 'tipo': 'accion_cognitiva',
        'variantes': ['pensar','pensando','pensé','me puse a pensar','estaba pensando',
                      'estoy pensando','me quedé pensando','reflexionando','reflexioné'],
        'grounding_base': 0.82,
    },
    'duda': {
        'id': 'PROF_DUDA', 'tipo': 'estado_cognitivo',
        'variantes': ['duda','dudas','no sé si','tengo dudas','no estoy seguro',
                      'no estoy segura','no sé bien','estoy indeciso','indecisa'],
        'grounding_base': 0.83,
    },
    'idea': {
        'id': 'PROF_IDEA', 'tipo': 'concepto',
        'variantes': ['idea','una idea','se me ocurrió','tengo una idea','mi idea',
                      'la idea','buena idea','mala idea'],
        'grounding_base': 0.80,
    },
    'decision': {
        'id': 'PROF_DECISION', 'tipo': 'accion',
        'variantes': ['decisión','decision','decidir','decidí','tengo que decidir',
                      'no sé qué decidir','tomé una decisión'],
        'grounding_base': 0.83,
    },
    'miedo': {
        'id': 'PROF_MIEDO', 'tipo': 'emocion',
        'variantes': ['miedo','con miedo','me da miedo','tengo miedo','le temo',
                      'le tengo miedo','miedo de','miedo a','temo que'],
        'grounding_base': 0.85,
    },
    'esperanza': {
        'id': 'PROF_ESPERANZA', 'tipo': 'emocion',
        'variantes': ['esperanza','espero que','ojalá','ojalá que','quiero creer',
                      'puede que','tal vez','a ver si','tengo fe'],
        'grounding_base': 0.78,
    },
    'proposito': {
        'id': 'PROF_PROPOSITO', 'tipo': 'concepto_existencial',
        'variantes': ['propósito','proposito','para qué','sentido','qué sentido',
                      'sin sentido','con sentido','mi propósito','mi misión'],
        'grounding_base': 0.85,
    },
    'futuro': {
        'id': 'PROF_FUTURO', 'tipo': 'concepto_temporal',
        'variantes': ['futuro','el futuro','qué va a pasar','qué pasará','más adelante',
                      'a largo plazo','en unos años','cuando sea grande'],
        'grounding_base': 0.80,
    },
    'pasado': {
        'id': 'PROF_PASADO', 'tipo': 'concepto_temporal',
        'variantes': ['pasado','antes','cuando era','de pequeño','de pequeña',
                      'en el pasado','hace tiempo','años atrás','lo que fue'],
        'grounding_base': 0.78,
    },
    'cambiar': {
        'id': 'PROF_CAMBIAR', 'tipo': 'accion',
        'variantes': ['cambiar','cambio','quiero cambiar','necesito cambiar',
                      'cambié','todo cambió','las cosas cambiaron'],
        'grounding_base': 0.80,
    },
    'crecer': {
        'id': 'PROF_CRECER', 'tipo': 'accion',
        'variantes': ['crecer','creciendo','crecí','quiero crecer','he crecido',
                      'crecimiento','madurar','madurando','maduré'],
        'grounding_base': 0.80,
    },

    # ── Relaciones ────────────────────────────────
    'amigo': {
        'id': 'REL_AMIGO', 'tipo': 'relacion',
        'variantes': ['amigo','amiga','amigos','amigas','mi mejor amigo','mi mejor amiga',
                      'mi amigo','mi amiga','un amigo','una amiga'],
        'grounding_base': 0.80,
    },
    'familia': {
        'id': 'REL_FAMILIA', 'tipo': 'relacion',
        'variantes': ['familia','mi familia','los de mi casa','mi gente','los míos'],
        'grounding_base': 0.82,
    },
    'papa': {
        'id': 'REL_PAPA', 'tipo': 'relacion',
        'variantes': ['papá','papa','mi papá','mi papa','mi viejo','el viejo','papi'],
        'grounding_base': 0.82,
    },
    'mama': {
        'id': 'REL_MAMA', 'tipo': 'relacion',
        'variantes': ['mamá','mama','mi mamá','mi mama','mi vieja','la vieja','mami'],
        'grounding_base': 0.82,
    },
    'hermano': {
        'id': 'REL_HERMANO', 'tipo': 'relacion',
        'variantes': ['hermano','hermana','mi hermano','mi hermana','los hermanos'],
        'grounding_base': 0.80,
    },
    'pareja': {
        'id': 'REL_PAREJA', 'tipo': 'relacion',
        'variantes': ['novia','novio','pareja','mi novia','mi novio','mi pareja',
                      'la novia','el novio','saliendo con','estoy con'],
        'grounding_base': 0.83,
    },

    # ── Metas y sueños ────────────────────────────
    'sueno': {
        'id': 'PROF_SUENO', 'tipo': 'aspiracion',
        'variantes': ['sueño','sueños','mi sueño','sueño con','siempre quise',
                      'quiero llegar a','algún día','mi meta','mis metas'],
        'grounding_base': 0.82,
    },
    'logro': {
        'id': 'PROF_LOGRO', 'tipo': 'evento_positivo',
        'variantes': ['logré','lo logré','lo hice','por fin','terminé','conseguí',
                      'obtuve','alcancé','cumplí','completé','funcionó'],
        'grounding_base': 0.83,
    },
    'fracaso': {
        'id': 'PROF_FRACASO', 'tipo': 'evento_negativo',
        'variantes': ['fallé','fracasé','no lo logré','no pude','me salió mal',
                      'no funcionó','fue un error','me equivoqué en todo'],
        'grounding_base': 0.83,
    },

    # ── Estados complejos ─────────────────────────
    'confundido_tranquilo': {
        'id': 'PROF_CONF_TRANQ', 'tipo': 'estado_mixto',
        'variantes': ['confundido pero bien','confundida pero bien',
                      'no sé pero estoy bien','perdido pero tranquilo'],
        'grounding_base': 0.80,
    },
    'cansado_motivado': {
        'id': 'PROF_CANS_MOTIV', 'tipo': 'estado_mixto',
        'variantes': ['cansado pero motivado','cansada pero motivada',
                      'agotado pero sigo','sin fuerzas pero voy'],
        'grounding_base': 0.82,
    },
    'solo_bien': {
        'id': 'PROF_SOLO_BIEN', 'tipo': 'estado_mixto',
        'variantes': ['solo pero bien','sola pero bien','prefiero estar solo',
                      'necesito tiempo solo','necesito mi espacio'],
        'grounding_base': 0.80,
    },

    # ── Pedir consejo / opinión ───────────────────
    'pedir_consejo': {
        'id': 'PROF_CONSEJO', 'tipo': 'solicitud',
        'variantes': ['qué harías','qué haría','qué me recomiendas','qué piensas',
                      'qué crees','dame tu opinión','me aconsejas','qué harías tú',
                      'tú qué harías','debería','debo','qué me dices'],
        'grounding_base': 0.87,
    },
    'contar_algo': {
        'id': 'PROF_CONTAR', 'tipo': 'accion_comunicativa',
        'variantes': ['te cuento','tengo que contarte','quiero contarte','escucha',
                      'oye','mira','fíjate','imagínate','te digo algo'],
        'grounding_base': 0.80,
    },
    'desahogo': {
        'id': 'PROF_DESAHOGO', 'tipo': 'necesidad',
        'variantes': ['necesito hablar','quiero hablar','necesito desahogarme',
                      'necesito contarte','quiero contarte algo','estoy mal'],
        'grounding_base': 0.88,
    },
}