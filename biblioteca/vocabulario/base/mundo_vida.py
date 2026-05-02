# biblioteca/vocabulario/base/mundo_vida.py
# ================================================
# VOCABULARIO MUNDO Y VIDA — completo standalone
# ================================================

CONCEPTOS_MUNDO = {

    # ── Transporte ────────────────────────────────
    'bus': {
        'id': 'VID_BUS', 'tipo': 'transporte',
        'variantes': ['bus','buseta','el bus','en bus','transmilenio','metro','el metro'],
        'grounding_base': 0.72,
    },
    'carro': {
        'id': 'VID_CARRO', 'tipo': 'transporte',
        'variantes': ['carro','auto','el carro','mi carro','en carro','uber','taxi','moto'],
        'grounding_base': 0.72,
    },
    'trancon': {
        'id': 'VID_TRANCON', 'tipo': 'situacion',
        'variantes': ['trancón','trancon','trancado','tráfico','trafico',
                      'embotellamiento','no avanza','pegado en el tráfico'],
        'grounding_base': 0.75,
    },

    # ── Salud ─────────────────────────────────────
    'medico': {
        'id': 'VID_MEDICO', 'tipo': 'salud',
        'variantes': ['médico','medico','doctor','cita','cita médica',
                      'hospital','clínica','clinica','urgencias'],
        'grounding_base': 0.78,
    },
    'enfermedad': {
        'id': 'VID_ENFERMEDAD', 'tipo': 'salud',
        'variantes': ['enfermedad','gripa','gripe','resfriado','fiebre',
                      'tos','dolor de cabeza','migraña','migrana'],
        'grounding_base': 0.80,
    },
    'pastilla': {
        'id': 'VID_MEDICAMENTO', 'tipo': 'salud',
        'variantes': ['pastilla','medicamento','medicina','remedio',
                      'antibiótico','tableta','jarabe'],
        'grounding_base': 0.77,
    },
    'ejercicio': {
        'id': 'VID_EJERCICIO', 'tipo': 'bienestar',
        'variantes': ['ejercicio','gym','gimnasio','correr','trotar','entrenar',
                      'entrenamiento','pesas','cardio','rutina'],
        'grounding_base': 0.73,
    },
    'insomnio': {
        'id': 'VID_INSOMNIO', 'tipo': 'salud',
        'variantes': ['no pude dormir','insomnio','desvelado','desvelada',
                      'trasnoche','me trasnoché','no pegué el ojo'],
        'grounding_base': 0.78,
    },

    # ── Hogar ─────────────────────────────────────
    'casa': {
        'id': 'VID_CASA', 'tipo': 'lugar',
        'variantes': ['casa','en casa','mi casa','llegar a casa','estoy en casa',
                      'cuarto','habitación','habitacion','pieza','apartamento','apto'],
        'grounding_base': 0.73,
    },
    'limpiar': {
        'id': 'VID_LIMPIAR', 'tipo': 'actividad_hogar',
        'variantes': ['ordenar','limpiar','limpiar la casa','asear','tender la cama',
                      'lavar','cocinar','barrer'],
        'grounding_base': 0.70,
    },

    # ── Dinero ────────────────────────────────────
    'plata': {
        'id': 'VID_DINERO', 'tipo': 'recurso',
        'variantes': ['plata','dinero','lucas','billete',
                      'no tengo plata','me quedé sin plata','sin un peso'],
        'grounding_base': 0.80,
    },
    'deuda': {
        'id': 'VID_DEUDA', 'tipo': 'situacion_financiera',
        'variantes': ['deuda','debo','préstamo','prestamo','crédito','credito','cuota'],
        'grounding_base': 0.78,
    },
    'ahorro': {
        'id': 'VID_AHORRO', 'tipo': 'accion_financiera',
        'variantes': ['ahorrar','ahorrando','ahorré','mis ahorros','guardar plata'],
        'grounding_base': 0.75,
    },
    'compras': {
        'id': 'VID_COMPRAS', 'tipo': 'actividad',
        'variantes': ['comprar','compré','ir de compras','mercado','supermercado',
                      'tienda','lo compré'],
        'grounding_base': 0.70,
    },

    # ── Naturaleza y clima ────────────────────────
    'naturaleza': {
        'id': 'VID_NATURALEZA', 'tipo': 'entorno',
        'variantes': ['naturaleza','campo','montaña','mar','playa','río','rio',
                      'lago','bosque','parque'],
        'grounding_base': 0.70,
    },
    'lluvia': {
        'id': 'VID_LLUVIA', 'tipo': 'clima',
        'variantes': ['lluvia','está lloviendo','llueve','llovió','llovio',
                      'aguacero','llovizna','diluvio'],
        'grounding_base': 0.72,
    },
    'calor': {
        'id': 'VID_CALOR', 'tipo': 'clima',
        'variantes': ['calor','hace calor','qué calor','está caliente','bochorno'],
        'grounding_base': 0.72,
    },
    'frio': {
        'id': 'VID_FRIO', 'tipo': 'clima',
        'variantes': ['frío','frio','hace frío','qué frío','está helado'],
        'grounding_base': 0.72,
    },

    # ── Mascotas ──────────────────────────────────
    'perro': {
        'id': 'VID_PERRO', 'tipo': 'mascota',
        'variantes': ['perro','perrita','mi perro','el perro','la perra','cachorro'],
        'grounding_base': 0.72,
    },
    'gato': {
        'id': 'VID_GATO', 'tipo': 'mascota',
        'variantes': ['gato','gatito','mi gato','el gato','la gata','michi'],
        'grounding_base': 0.72,
    },

    # ── Colombia y ciudades ───────────────────────
    'colombia': {
        'id': 'VID_COLOMBIA', 'tipo': 'lugar',
        'variantes': ['colombia','en colombia','aquí en colombia','este país',
                      'colombiano','colombiana'],
        'grounding_base': 0.78,
    },
    'bogota': {
        'id': 'VID_BOGOTA', 'tipo': 'ciudad',
        'variantes': ['bogotá','bogota','en bogotá','la capital','bogotano'],
        'grounding_base': 0.75,
    },
    'medellin': {
        'id': 'VID_MEDELLIN', 'tipo': 'ciudad',
        'variantes': ['medellín','medellin','en medellín','paisa','los paisas'],
        'grounding_base': 0.75,
    },
    'cali': {
        'id': 'VID_CALI', 'tipo': 'ciudad',
        'variantes': ['cali','en cali','caleño','caleña'],
        'grounding_base': 0.73,
    },
    'bucaramanga': {
        'id': 'VID_BUCARAMANGA', 'tipo': 'ciudad',
        'variantes': ['bucaramanga','en bucaramanga','bumangués','bumanguesa','la ciudad bonita'],
        'grounding_base': 0.75,
    },

    # ── Deportes ──────────────────────────────────
    'futbol': {
        'id': 'VID_FUTBOL', 'tipo': 'deporte',
        'variantes': ['fútbol','futbol','el partido','ver el partido','la selección',
                      'gol','nacional','millos','america de cali','junior'],
        'grounding_base': 0.73,
    },

    # ── Existencial ───────────────────────────────
    'vida': {
        'id': 'VID_VIDA', 'tipo': 'concepto_existencial',
        'variantes': ['la vida','mi vida','así es la vida','vivir',
                      'sentido de la vida','para qué vivir'],
        'grounding_base': 0.85,
    },
    'felicidad': {
        'id': 'VID_FELICIDAD', 'tipo': 'concepto_existencial',
        'variantes': ['felicidad','ser feliz','quiero ser feliz','no soy feliz',
                      'qué es la felicidad','momentos felices'],
        'grounding_base': 0.83,
    },
    'tiempo_escaso': {
        'id': 'VID_TIEMPO_ESCASO', 'tipo': 'situacion',
        'variantes': ['no tengo tiempo','se va el tiempo','el tiempo pasa',
                      'perdí tiempo','no me alcanza el tiempo'],
        'grounding_base': 0.78,
    },
    'exito': {
        'id': 'VID_EXITO', 'tipo': 'concepto',
        'variantes': ['éxito','exito','ser exitoso','quiero tener éxito','triunfar'],
        'grounding_base': 0.78,
    },
    'suenos_vida': {
        'id': 'VID_SUENOS', 'tipo': 'aspiracion',
        'variantes': ['mis sueños','sueño con','siempre quise','quiero llegar a ser',
                      'algún día quiero','mi propósito en la vida'],
        'grounding_base': 0.82,
    },

    # ── Música y cultura ──────────────────────────
    'musica': {
        'id': 'VID_MUSICA', 'tipo': 'cultura',
        'variantes': ['música','musica','canción','cancion','spotify',
                      'playlist','reggaeton','salsa','rap','trap'],
        'grounding_base': 0.70,
    },
    'cine': {
        'id': 'VID_CINE', 'tipo': 'cultura',
        'variantes': ['película','pelicula','cine','netflix','serie','series',
                      'una serie','episodio','temporada'],
        'grounding_base': 0.70,
    },
    'libro': {
        'id': 'VID_LIBRO', 'tipo': 'cultura',
        'variantes': ['libro','leer','estoy leyendo','leí','novela','cuento'],
        'grounding_base': 0.72,
    },

    # ── Actualidad ────────────────────────────────
    'noticias': {
        'id': 'VID_NOTICIAS', 'tipo': 'actualidad',
        'variantes': ['noticias','la noticia','vi en las noticias','lo que pasó',
                      'pasó algo','qué pasó','última hora'],
        'grounding_base': 0.73,
    },
    'politica': {
        'id': 'VID_POLITICA', 'tipo': 'actualidad',
        'variantes': ['política','politica','el gobierno','los políticos',
                      'elecciones','presidente','el congreso'],
        'grounding_base': 0.72,
    },
    'economia': {
        'id': 'VID_ECONOMIA', 'tipo': 'actualidad',
        'variantes': ['economía','economia','inflación','inflacion','el dólar',
                      'los precios','todo está caro'],
        'grounding_base': 0.73,
    },
}