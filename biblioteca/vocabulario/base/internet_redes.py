# biblioteca/vocabulario/base/internet_redes.py
# ================================================
# VOCABULARIO INTERNET, REDES SOCIALES Y MUNDO
# Bell entiende la vida digital y el mundo real
# ================================================

CONCEPTOS_INTERNET = {

    # ── Redes sociales ────────────────────────────
    'instagram': {
        'id': 'WEB_INSTAGRAM', 'tipo': 'red_social',
        'variantes': ['instagram','insta','el insta','las historias','reels','stories'],
        'grounding_base': 0.75,
    },
    'tiktok': {
        'id': 'WEB_TIKTOK', 'tipo': 'red_social',
        'variantes': ['tiktok','tik tok','los tiktoks','videos de tiktok'],
        'grounding_base': 0.75,
    },
    'youtube': {
        'id': 'WEB_YOUTUBE', 'tipo': 'plataforma',
        'variantes': ['youtube','un video','el video','ver videos','canal','youtuber'],
        'grounding_base': 0.75,
    },
    'twitter_x': {
        'id': 'WEB_TWITTER', 'tipo': 'red_social',
        'variantes': ['twitter','x','tweet','la x','tuiteé'],
        'grounding_base': 0.73,
    },
    'whatsapp': {
        'id': 'WEB_WHATSAPP', 'tipo': 'mensajeria',
        'variantes': ['whatsapp','wsp','wasap','el chat','me escribió','me mandó'],
        'grounding_base': 0.78,
    },
    'discord': {
        'id': 'WEB_DISCORD', 'tipo': 'plataforma',
        'variantes': ['discord','el discord','server de discord','servidor discord'],
        'grounding_base': 0.75,
    },
    'reddit': {
        'id': 'WEB_REDDIT', 'tipo': 'plataforma',
        'variantes': ['reddit','subreddit','vi en reddit','post de reddit'],
        'grounding_base': 0.72,
    },

    # ── Expresiones de internet ───────────────────
    'viral': {
        'id': 'WEB_VIRAL', 'tipo': 'expresion_internet',
        'variantes': ['viral','se hizo viral','está viral','es viral'],
        'grounding_base': 0.73,
    },
    'meme': {
        'id': 'WEB_MEME', 'tipo': 'expresion_internet',
        'variantes': ['meme','memes','el meme','ese meme','un meme'],
        'grounding_base': 0.73,
    },
    'hack': {
        'id': 'WEB_HACK', 'tipo': 'concepto_internet',
        'variantes': ['hack','hacker','hackearon','hackear','hackeado'],
        'grounding_base': 0.78,
    },

    # ── Mundo y actualidad ────────────────────────
    'noticias': {
        'id': 'MUN_NOTICIAS', 'tipo': 'actualidad',
        'variantes': ['noticias','la noticia','vi en las noticias','salió en noticias',
                      'lo que pasó','pasó algo','qué pasó'],
        'grounding_base': 0.73,
    },
    'politica': {
        'id': 'MUN_POLITICA', 'tipo': 'tema_mundo',
        'variantes': ['política','politica','el gobierno','los políticos','elecciones',
                      'presidente','el congreso'],
        'grounding_base': 0.72,
    },
    'economia': {
        'id': 'MUN_ECONOMIA', 'tipo': 'tema_mundo',
        'variantes': ['economía','economia','la inflación','el dólar','el mercado',
                      'los precios','todo caro','muy caro'],
        'grounding_base': 0.73,
    },
    'colombia_pais': {
        'id': 'MUN_COLOMBIA', 'tipo': 'lugar',
        'variantes': ['colombia','en colombia','aquí en colombia','este país'],
        'grounding_base': 0.78,
    },
    'bogota': {
        'id': 'MUN_BOGOTA', 'tipo': 'ciudad',
        'variantes': ['bogotá','bogota','en bogotá','la capital'],
        'grounding_base': 0.75,
    },

    # ── Clima ─────────────────────────────────────
    'lluvia': {
        'id': 'CLIM_LLUVIA', 'tipo': 'clima',
        'variantes': ['lluvia','está lloviendo','llueve','llovió','está mojado',
                      'aguacero','llovizna','diluvio'],
        'grounding_base': 0.72,
    },
    'calor': {
        'id': 'CLIM_CALOR', 'tipo': 'clima',
        'variantes': ['calor','hace calor','qué calor','está caliente','quema'],
        'grounding_base': 0.72,
    },
    'frio': {
        'id': 'CLIM_FRIO', 'tipo': 'clima',
        'variantes': ['frío','frio','hace frío','qué frío','está helado','está frío'],
        'grounding_base': 0.72,
    },
}


# ── Vocabulario de mundo y vida ──────────────────────────
CONCEPTOS_MUNDO = {

    # ── Transporte ────────────────────────────────
    'transporte': {
        'id': 'VID_TRANSPORTE', 'tipo': 'actividad',
        'variantes': ['bus','metro','transmilenio','uber','taxi','moto','carro','el carro',
                      'en bus','en metro','el trancón','trancón','tráfico','trancado'],
        'grounding_base': 0.72,
    },

    # ── Salud y bienestar ─────────────────────────
    'medico': {
        'id': 'VID_MEDICO', 'tipo': 'salud',
        'variantes': ['médico','medico','doctor','cita médica','hospital','clínica',
                      'pastilla','medicina','diagnóstico'],
        'grounding_base': 0.78,
    },
    'ejercicio': {
        'id': 'VID_EJERCICIO', 'tipo': 'bienestar',
        'variantes': ['ejercicio','gym','gimnasio','correr','entrenar','entrenamiento',
                      'hacer ejercicio','pesas','cardio'],
        'grounding_base': 0.73,
    },
    'meditacion': {
        'id': 'VID_MEDITACION', 'tipo': 'bienestar',
        'variantes': ['meditación','meditacion','meditar','respirar','calmarme',
                      'calmar la mente','relajarme'],
        'grounding_base': 0.73,
    },

    # ── Compras y dinero ──────────────────────────
    'compras': {
        'id': 'VID_COMPRAS', 'tipo': 'actividad',
        'variantes': ['comprar','compré','ir de compras','mercado','supermercado',
                      'tienda','lo compré','lo voy a comprar'],
        'grounding_base': 0.70,
    },
    'plata': {
        'id': 'VID_DINERO', 'tipo': 'recurso',
        'variantes': ['plata','dinero','no tengo plata','me quedé sin plata',
                      'debo','deuda','ahorrar','ahorro','caro','barato'],
        'grounding_base': 0.78,
    },

    # ── Naturaleza ────────────────────────────────
    'naturaleza': {
        'id': 'VID_NATURALEZA', 'tipo': 'entorno',
        'variantes': ['naturaleza','campo','montaña','mar','playa','río','lago',
                      'árboles','verde','parque'],
        'grounding_base': 0.70,
    },

    # ── Mascotas ──────────────────────────────────
    'mascota': {
        'id': 'VID_MASCOTA', 'tipo': 'ser_vivo',
        'variantes': ['perro','gato','mascota','mi perro','mi gato','el perro',
                      'la gata','el gato','mascotita'],
        'grounding_base': 0.72,
    },

    # ── Hogar ─────────────────────────────────────
    'casa': {
        'id': 'VID_CASA', 'tipo': 'lugar',
        'variantes': ['casa','en casa','mi casa','llegar a casa','estoy en casa',
                      'cuarto','habitación','pieza'],
        'grounding_base': 0.73,
    },

    # ── Sentido existencial ───────────────────────
    'vida': {
        'id': 'VID_VIDA', 'tipo': 'concepto_existencial',
        'variantes': ['la vida','mi vida','así es la vida','esto es la vida',
                      'vivir','quiero vivir','sentido de la vida'],
        'grounding_base': 0.83,
    },
    'tiempo_vida': {
        'id': 'VID_TIEMPO_ESCASO', 'tipo': 'concepto_existencial',
        'variantes': ['no tengo tiempo','se va el tiempo','el tiempo pasa',
                      'ya se me hizo tarde en','desperdicié','perdí tiempo'],
        'grounding_base': 0.78,
    },
    'felicidad': {
        'id': 'VID_FELICIDAD', 'tipo': 'concepto_existencial',
        'variantes': ['felicidad','ser feliz','quiero ser feliz','no soy feliz',
                      'buscar la felicidad','qué es la felicidad'],
        'grounding_base': 0.83,
    },
}