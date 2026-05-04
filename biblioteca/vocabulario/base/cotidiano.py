# biblioteca/vocabulario/base/cotidiano.py
# ================================================
# VOCABULARIO COTIDIANO — vida diaria completa
# ================================================

CONCEPTOS_COTIDIANO = {

    # ── Rutinas ──────────────────────────────────
    'dormir': {
        'id': 'COTI_DORMIR', 'tipo': 'accion_cotidiana',
        'variantes': ['dormir','duermo','dormí','dormiste','no dormí','no pude dormir',
                      'me quedé dormido','me acosté','a dormir','hora de dormir'],
        'grounding_base': 0.75,
    },
    'comer': {
        'id': 'COTI_COMER', 'tipo': 'accion_cotidiana',
        'variantes': ['comer','comí','almorzar','almorcé','desayunar','desayuné',
                      'cenar','cené','no he comido','tengo hambre','hambre'],
        'grounding_base': 0.75,
    },
    'despertar': {
        'id': 'COTI_DESPERTAR', 'tipo': 'accion_cotidiana',
        'variantes': ['desperté','me desperté','me levanté','acabo de despertar',
                      'recién me levanto','me acabo de levantar','buenos días'],
        'grounding_base': 0.75,
    },
    'trabajar': {
        'id': 'COTI_TRABAJAR', 'tipo': 'accion_cotidiana',
        'variantes': ['trabajando','trabajé','trabajo','estoy en el trabajo','en la oficina',
                      'jornada','turno','reunión','meeting','entrega','deadline'],
        'grounding_base': 0.78,
    },
    'estudiar': {
        'id': 'COTI_ESTUDIAR', 'tipo': 'accion_cotidiana',
        'variantes': ['estudiar','estudiando','estudiando','estudié','examen','parcial',
                      'tarea','trabajo escolar','clase','clases','universidad','colegio'],
        'grounding_base': 0.78,
    },
    'salir': {
        'id': 'COTI_SALIR', 'tipo': 'accion_cotidiana',
        'variantes': ['salir','salgo','salí','voy a salir','voy a salir','afuera',
                      'calle','por fuera'],
        'grounding_base': 0.72,
    },
    'llegar': {
        'id': 'COTI_LLEGAR', 'tipo': 'accion_cotidiana',
        'variantes': ['llegué','llegué a','acabo de llegar','ya llegué','llegando'],
        'grounding_base': 0.72,
    },

    # ── Tiempo libre ─────────────────────────────
    'descansar': {
        'id': 'COTI_DESCANSAR', 'tipo': 'accion_cotidiana',
        'variantes': ['descansar','descansando','descansé','me voy a descansar',
                      'tomar aire','un rato','pausa','break'],
        'grounding_base': 0.73,
    },
    'ver_series': {
        'id': 'COTI_SERIES', 'tipo': 'accion_cotidiana',
        'variantes': ['ver series','netflix','ver películas','serie','pelicula','película',
                      'show','episodio','capitulo','capítulo'],
        'grounding_base': 0.70,
    },
    'escuchar_musica': {
        'id': 'COTI_MUSICA', 'tipo': 'accion_cotidiana',
        'variantes': ['música','musica','canción','cancion','escuchando','spotify',
                      'playlist','song'],
        'grounding_base': 0.70,
    },

    # ── Estados físicos ───────────────────────────
    'dolor': {
        'id': 'COTI_DOLOR', 'tipo': 'estado_fisico',
        'variantes': ['dolor','me duele','duele','tengo dolor','me duelen','molestia'],
        'grounding_base': 0.80,
    },
    'enfermo': {
        'id': 'COTI_ENFERMO', 'tipo': 'estado_fisico',
        'variantes': ['enfermo','enferma','gripa','gripe','resfriado','fiebre',
                      'mal físico','no me siento bien','nauseas','mareo'],
        'grounding_base': 0.82,
    },
    'sin_sueno': {
        'id': 'COTI_SIN_SUENO', 'tipo': 'estado_fisico',
        'variantes': ['sin sueño','no tengo sueño','desvelado','trasnochado',
                      'me trasnoché','no dormí nada','no pegué el ojo'],
        'grounding_base': 0.78,
    },

    # ── Situaciones cotidianas ────────────────────
    'tarde': {
        'id': 'COTI_TARDE', 'tipo': 'situacion',
        'variantes': ['tarde','se me hizo tarde','llegué tarde','voy tarde',
                      'estoy atrasado','atrasada','no llegué'],
        'grounding_base': 0.73,
    },
    'estres': {
        'id': 'COTI_ESTRES', 'tipo': 'estado_emocional',
        'variantes': ['estrés','estres','estresado','estresada','con mil cosas',
                      'demasiado','saturado','saturada','mucho encima'],
        'grounding_base': 0.82,
    },
    'aburrido': {
        'id': 'COTI_ABURRIDO', 'tipo': 'estado_emocional',
        'variantes': ['aburrido','aburrida','aburrimiento','no tengo nada que hacer',
                      'qué pereza','qué aburrición','que aburricion','no sé qué hacer'],
        'grounding_base': 0.73,
    },
    'motivado': {
        'id': 'COTI_MOTIVADO', 'tipo': 'estado_emocional',
        'variantes': ['motivado','motivada','con ganas','con energía','activo','activa',
                      'listo para','lista para','arrancando','de una'],
        'grounding_base': 0.75,
    },
}