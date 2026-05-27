# capas/capa7/detector_habilidad.py
# ================================================
# DETECTOR DE HABILIDAD — v2 con PYTHON_COMPLETO
# ================================================

import re
# clasificador_habilidad_groq reemplazado por clasificador_bell (C3 provee habilidad_req)

def _podria_ser_autoanalisis_semantico(texto_lower: str) -> bool:
    """Universal: detecta si la pregunta es sobre la arquitectura interna de Bell."""
    _COMPONENTES = [
        'capa', 'capas', 'archivo', 'archivos', 'código', 'modulo', 'módulo',
        'habilidad', 'habilidades', 'consejera', 'consejeras', 'vocabulario',
        'interfaz', 'biblioteca', 'arquitectura', 'estructura', 'capacidad', 'capacidades',
    ]
    _BELL_SELF = ['tuyo', 'tuya', 'tuyos', 'tuyas', 'tu ', 'tus ', ' te ', ' ti ',
        'de ti', 'contigo', 'eres', 'tienes', 'estás']
    _ANALISIS = [
        'analiza', 'describe', 'cuéntame', 'muéstrame', 'dime', 'lista',
        'qué hay', 'cuánto', 'cuántos', 'cuántas', 'qué te falta', 'faltan',
        'más grande', 'más largo', 'más complejo', 'incompleto', 'pendiente',
        'deuda', 'urgente', 'mejorar', 'crecieron', 'qué tan grande',
    ]
    _FRASES = [
        'cuáles son tus', 'describe tu', 'muéstrame tu', 'explícame tu',
        'analízate', 'cuánto mides', 'cuánto pesas', 'qué tan grande eres',
    ]
    tiene_componente = any(c in texto_lower for c in _COMPONENTES)
    tiene_self = any(s in texto_lower for s in _BELL_SELF)
    tiene_analisis = any(v in texto_lower for v in _ANALISIS)
    if tiene_componente and tiene_self: return True
    if tiene_analisis and tiene_self: return True
    if any(f in texto_lower for f in _FRASES): return True
    return False


HABILIDADES = {
    'CALCULO': {
        'disponible':  False,
        'descripcion': 'Cálculo matemático con SymPy',
        'patrones': [
            r'\bcalcula\b', r'\bcuánto\s+es\b', r'\bcuanto\s+es\b',
            r'\bresuelve\b', r'\bintegral\b', r'\bderivada\b',
            r'\braíz\s+de\b', r'\braiz\s+de\b', r'\bpotencia\b',
            r'\bmultiplica\b', r'\bdivide\b',
            r'\b\d+\s*[\+\-\*\/\^]\s*\d+\b',
            r'\bpromedio\b', r'\bdesviaci[oó]n\b',
            r'\bfactorial\b', r'\blogaritmo\b',
            r'\bcu[aá]nto\s+(?:da|vale|son)\b',
            r'\b\d+\s*%\s+de\b',
        ],
    },
    # ── AUTO-ANÁLISIS TOTAL — Bell se conoce a sí misma ─────────────
    'AUTO_ANALISIS_TOTAL': {
        'disponible': False,  # DESACTIVADA — rediseño pendiente
        'descripcion': 'Bell lee su propia arquitectura, archivos, habilidades y estado',
        'patrones': [
            r'\bqu[eé]\s+(?:archivos?|habilidades?|capas?|consejeras?)\s+(?:tienes?|tenés|hay)\b',
            r'\bqu[eé]\s+tienes\b',
            r'\bcómo\s+est[aá]s\s+(?:organizada|estructurada|construida|hecha)\b',
            r'\bdescríbete\b',
            r'\bcu[aá]ntos?\s+archivos?\b',
            r'\bcu[aá]ntas?\s+l[ií]neas?\b',
            r'\bqu[eé]\s+hay\s+en\s+(?:tu\s+)?capa\s*[1-9]\b',
            r'\bqu[eé]\s+hace\s+(?:tu\s+)?capa\s*[1-9]\b',
            r'\bqu[eé]\s+habilidades?\s+(?:tienes?|tenés|activas?|funcionan?)\b',
            r'\bqu[eé]\s+consejeras?\s+(?:tienes?|tenés)\b',
            r'\bqu[eé]\s+archivos?\s+(?:python|javascript|js|css|html)\s+tienes?\b',
            r'\bcu[aá]nto\s+vocabulario\b',
            r'\bqu[eé]\s+hay\s+en\s+(?:tu\s+)?(?:interfaz|frontend|biblioteca)\b',
            r'\bdescribe\s+(?:tu\s+)?arquitectura\b',
            r'\bqu[eé]\s+(?:tiene|hay|tienes?)\s+(?:tu\s+)?(?:capa|biblioteca|interfaz)\b',
            r'\bcómo\s+est[aá]s\s+(?:por\s+dentro|internamente)\b',
            r'\bqu[eé]\s+puedes?\s+hacer\s+(?:ahora|actualmente|hoy)\b',
            r'\bcu[aá]nto\s+(?:pesas?|ocupas?|mides?)\b',
            r'\bqu[eé]\s+hace\s+\w[\w_]*\.(?:py|js|css|html|json|md)\b',
            r'\bqu[eé]\s+(?:es|hace|contiene)\s+(?:tu\s+)?\w[\w_]*\.(?:py|js)\b',
            # Nivel 2 — análisis propio e introspección
            r'\banaliza\s+(?:tu\s+)?(?:todo\s+)?(?:tu\s+)?c[oó]digo\b',
            r'\banaliza\s+(?:tu\s+)?propio\b',
            r'\bqu[eé]\s+mejorar[ií]as?\b',
            r'\bqu[eé]\s+cambiar[ií]as?\s+de\s+ti\b',
            r'\bprop[oó]n\s+mejoras?\b',
            r'\bqu[eé]\s+est[aá]\s+mal\s+en\s+ti\b',
            r'\bdeuda\s+t[eé]cnica\b',
            r'\bqu[eé]\s+te\s+falta\b',
            r'\bcuáles?\s+son\s+tus\s+limitaciones?\b',
            r'\banalízate\b',
            r'\bautoanalisis\b',
            r'\bqu[eé]\s+falla\s+en\s+ti\b',
            r'\bqu[eé]\s+necesitas?\s+mejorar\b',
            r'\bqu[eé]\s+har[ií]as?\s+diferente\b',
            r'\bhabilidades?\s+(?:incompletas?|pendientes?|faltantes?)\b',
            r'\bcu[aá]les?\s+son\s+tus\s+(?:limitaciones?|debilidades?)\b',
            r'\bqu[eé]\s+archivos?\s+est[aá]n?\s+creciendo\b',
        ],
    },
    # ── NAVEGADOR WEB — Bell controla el browser ───────────────────
    'NAVEGADOR_WEB': {
        'disponible': True,
        'descripcion': 'Bell controla el browser: YouTube, Instagram, GitHub, Gmail, cualquier web',
        'patrones': [
            # ── Videos / YouTube ─────────────────────────
            r'\bponme\b', r'\bpon\s+el\s+video\b', r'\breproduce\b',
            r'\babre\s+youtube\b', r'\bbusca\s+en\s+youtube\b',
            r'\bvideo\s+de\b', r'\bcanal\s+de\b',
            # ── Instagram ────────────────────────────────
            r'\binstagram\b', r'\binsta\b',
            r'\bescr[ií]bele\b', r'\bmanda\s+(?:un\s+)?mensaje\b',
            r'\bmensaje\s+a\b', r'\benvía?\s+(?:un\s+)?mensaje\b',
            # ── GitHub ───────────────────────────────────
            r'\bgithub\b', r'\brepositorio\b', r'\brepositoios\b',
            r'\bmis\s+repos\b', r'\burl\s+del\s+repo\b',
            # ── Gmail ────────────────────────────────────
            r'\bgmail\b', r'\bcorreos\s+de\b', r'\bemails\s+de\b',
            # ── Acciones generales de browser ────────────
            r'\babre\s+(?:el\s+)?(?:navegador|browser|chrome)\b',
            r'\bnavega\s+a\b', r'\bve\s+a\s+(?:la\s+)?p[aá]gina\b',
            r'\blee\s+(?:esta\s+)?p[aá]gina\b',
            r'\bleer\s+(?:la\s+)?web\b', r'\bextr[aá]e\s+(?:de\s+)?(?:la\s+)?web\b',
            r'\binicia\s+sesi[oó]n\b', r'\blog(?:ue)?a(?:te)?\b',
            r'\bdescarga\b', r'\bdescargar\b',
            r'\bllena\s+(?:el\s+)?formulario\b',
            # ── URL directa ──────────────────────────────
            r'https?://',
        ],
    },

    # ── BÚSQUEDA EN INTERNET ─────────────────────────────────────────
    'BUSQUEDA_INTERNET': {
        'disponible': False,  # DESACTIVADA — rediseño pendiente
        'descripcion': 'Bell busca en internet, lee páginas y responde con información real',
        'patrones': [
            # ── QUÉ ES / SON / SIGNIFICA ─────────────────────────
            r'\bqu[eé]\s+es\b',
            r'\bqu[eé]\s+son\b',
            r'\bqu[eé]\s+significa\b',
            r'\bqu[eé]\s+quiere\s+decir\b',
            r'\bqu[eé]\s+fue\b',
            r'\bqu[eé]\s+era\b',
            r'\bqu[eé]\s+hace\b',
            r'\bqu[eé]\s+hizo\b',
            r'\bqu[eé]\s+tiene\b',
            r'\bqu[eé]\s+hay\b',
            r'\bqu[eé]\s+pas[oó]\b',
            r'\bqu[eé]\s+pas[aá]\b',
            r'\bcu[aá]les\s+son\b',
            r'\bcu[aá]l\s+es\b',
            # ── QUIÉN / QUIÉNES ──────────────────────────────────
            r'\bqui[eé]n\s+es\b',
            r'\bqui[eé]n\s+fue\b',
            r'\bqui[eé]n\s+era\b',
            r'\bqui[eé]nes\s+son\b',
            r'\bqui[eé]n\s+cre[oó]\b',
            r'\bqui[eé]n\s+invent[oó]\b',
            r'\bqui[eé]n\s+fund[oó]\b',
            r'\bqui[eé]n\s+escribi[oó]\b',
            r'\bqui[eé]n\s+gan[oó]\b',
            r'\bqui[eé]n\s+mat[oó]\b',
            r'\bqui[eé]n\s+dirige\b',
            r'\bqui[eé]n\s+gobierna\b',
            # ── DÓNDE ────────────────────────────────────────────
            r'\bd[oó]nde\s+queda\b',
            r'\bd[oó]nde\s+est[aá]\b',
            r'\bd[oó]nde\s+vive\b',
            r'\bd[oó]nde\s+naci[oó]\b',
            r'\bd[oó]nde\s+se\s+encuentra\b',
            r'\bd[oó]nde\s+puedo\b',
            r'\bd[oó]nde\s+fue\b',
            r'\bd[oó]nde\s+ocurri[oó]\b',
            # ── CUÁNDO ───────────────────────────────────────────
            r'\bcu[aá]ndo\s+fue\b',
            r'\bcu[aá]ndo\s+naci[oó]\b',
            r'\bcu[aá]ndo\s+muri[oó]\b',
            r'\bcu[aá]ndo\s+sali[oó]\b',
            r'\bcu[aá]ndo\s+se\s+cre[oó]\b',
            r'\bcu[aá]ndo\s+se\s+fund[oó]\b',
            r'\bcu[aá]ndo\s+empieza\b',
            r'\bcu[aá]ndo\s+termina\b',
            r'\bcu[aá]ndo\s+es\b',
            r'\bcu[aá]ndo\s+ocurri[oó]\b',
            # ── CÓMO ─────────────────────────────────────────────
            r'\bc[oó]mo\s+funciona\b',
            r'\bc[oó]mo\s+se\s+hace\b',
            r'\bc[oó]mo\s+se\s+llama\b',
            r'\bc[oó]mo\s+se\s+usa\b',
            r'\bc[oó]mo\s+se\s+crea\b',
            r'\bc[oó]mo\s+se\s+instala\b',
            r'\bc[oó]mo\s+se\s+juega\b',
            r'\bc[oó]mo\s+se\s+dice\b',
            r'\bc[oó]mo\s+es\b',
            r'\bc[oó]mo\s+fue\b',
            r'\bc[oó]mo\s+lo\s+hago\b',
            r'\bc[oó]mo\s+puedo\b',
            r'\bc[oó]mo\s+funciona\b',
            # ── CUÁNTO / CUÁNTOS ─────────────────────────────────
            r'\bcu[aá]nto\s+cuesta\b',
            r'\bcu[aá]nto\s+vale\b',
            r'\bcu[aá]ntos\s+hay\b',
            r'\bcu[aá]ntos\s+tiene\b',
            r'\bcu[aá]nta\s+gente\b',
            r'\bcu[aá]ntos\s+habitantes\b',
            r'\bcu[aá]ntos\s+a[nñ]os\b',
            # ── PARA QUÉ / POR QUÉ ───────────────────────────────
            r'\bpara\s+qu[eé]\s+sirve\b',
            r'\bpara\s+qu[eé]\s+es\b',
            r'\bpor\s+qu[eé]\s+es\b',
            r'\bpor\s+qu[eé]\s+se\b',
            r'\bpor\s+qu[eé]\s+fue\b',
            # ── BUSCAR EXPLÍCITO ─────────────────────────────────
            r'\bbusca\b',
            r'\bbuscame\b',
            r'\bb[uú]scame\b',
            r'\bgooglea\b',
            r'\bsearch\b',
            r'\binvestiga\b',
            r'\baverigua\b',
            r'\bconsulta\b',
            # ── INFORMACIÓN / DEFINICIÓN ─────────────────────────
            r'\binformaci[oó]n\s+(sobre|de|acerca)\b',
            r'\bdefinici[oó]n\s+de\b',
            r'\bdefine\s+\w',
            r'\bqu[eé]\s+significa\b',
            r'\bbiograf[ií]a\s+de\b',
            r'\bhistoria\s+de\b',
            r'\bde\s+d[oó]nde\s+viene\b',
            r'\bor[ií]gen\s+de\b',
            # ── CUÉNTAME / EXPLÍCAME / HÁBLAME ───────────────────
            r'\bcu[eé]ntame\s+(sobre|de|acerca)\b',
            r'\bexpl[ií]came\b',
            r'\bh[aá]blame\s+de\b',
            r'\bdime\s+(sobre|qu[eé]\s+es|qui[eé]n\s+es)\b',
            r'\bquiero\s+saber\b',
            r'\bnecesito\s+saber\b',
            r'\bquiero\s+entender\b',
            # ── NOTICIAS / ACTUALIDAD ────────────────────────────
            r'\bnoticias\s+(de|sobre|acerca)\b',
            r'\b[uú]ltimas\s+noticias\b',
            r'\bqu[eé]\s+hay\s+de\s+nuevo\b',
            r'\bactualidad\s+(de|sobre)\b',
            r'\bqu[eé]\s+pas[oó]\s+con\b',
            r'\bnovedades\s+(de|sobre)\b',
            # ── COMPARAR / DIFERENCIA ────────────────────────────
            r'\bdiferencia\s+(entre|de)\b',
            r'\bcompara\b',
            r'\bqu[eé]\s+es\s+mejor\b',
            r'\bvs\b',
            r'\bversus\b',
            # ── PRECIO / LUGAR / CAPITAL ─────────────────────────
            r'\bprecio\s+de\b',
            r'\bcu[aá]nto\s+cuesta\b',
            r'\bcapital\s+de\b',
            r'\bpa[ií]s\s+de\b',
            r'\bciudad\s+de\b',
            r'\bpoblaci[oó]n\s+de\b',
        ],
    },
    # ── PYTHON COMPLETO — 5 modos ──────────────────────────────────
    'PYTHON_COMPLETO': {
        'disponible':  True,
        'descripcion': 'Análisis, generación, explicación, debug y auto-análisis Python',
        # Modo analisis
        'patrones_analisis': [
            r'\banaliza\s+(?:este|el|mi)\s+c[oó]digo\b',
            r'\brevisa\s+(?:este|el|mi)\s+c[oó]digo\b',
            r'\bqu[eé]\s+hace\s+(?:este|el|esta)\b',
            r'\bqu[eé]\s+(?:errores|bugs|problemas)\s+(?:tiene|hay)\b',
            r'\bc[oó]mo\s+(?:mejoro|optimizo|refactorizo)\b',
            r'\bmalas\s+pr[aá]cticas\b',
            r'\bretroalimentaci[oó]n\b',
        ],
        # Modo generacion
        'patrones_generacion': [
            # Español
            r'\bcrea\s+(?:un?a?\s+)?(?:script|funci[oó]n|clase|m[oé]todo|endpoint|decorador|servidor)\b',
            r'\beschribe\s+(?:el|un?a?\s+)?c[oó]digo\b',
            r'\bhazme\s+(?:el|un?a?\s+)?(?:c[oó]digo|script|funci[oó]n|endpoint|clase|decorador|api)\b',
            r'\bgenera\s+(?:el|un?a?\s+)?c[oó]digo\b',
            r'\bnecesito\s+(?:un?a?\s+)?(?:script|funci[oó]n|clase|endpoint|decorador)\b',
            r'\bc[oó]digo\s+que\s+haga\b',
            r'\bfunci[oó]n\s+que\b',
            r'\bendpoint\s+(?:de|con|para|flask)\b',
            r'\bescribe\s+(?:el|un?a?\s+)?c[oó]digo\s+para\b',
            r'\bescribe\s+(?:el\s+)?c[oó]digo\s+(?:para|de|que)\b',
            r'\bprograma\s+que\b',
            r'\bscript\s+que\b',
            # Patrones de sistemas complejos
            r'\bcircuit\s*breaker\b',
            r'\bworker\s*pool\b',
            r'\bsistema\s+de\s+(?:configuraci[oó]n|eventos|cach[eé]|workers|retry)\b',
            r'\bpool\s+de\s+conexiones\b',
            r'\bquery\s+builder\b',
            r'\bpipeline\s+de\b',
            r'\bevent\s*bus\b',
            r'\brate\s*limit(?:er)?\b',
            # Inglés
            r'\bcreate\s+(?:a\s+)?(?:function|class|decorator|endpoint|script)\b',
            r'\bwrite\s+(?:a\s+)?(?:function|class|script|code)\b',
            r'\bmake\s+(?:a\s+)?(?:function|class|decorator|endpoint)\b',
            r'\bcreate\s+(?:a\s+)?(?:circuit|worker|pool|cache|queue|pipeline)\b',
        ],
        # Modo explicacion
        'patrones_explicacion': [
            # Español
            r'\bqu[eé]\s+es\s+(?:un?a?\s+)?(?:decorador|generador|lambda|yield|async|await|context\s+manager|type\s+hint|dataclass)\b',
            r'\bc[oó]mo\s+funciona\s+(?:async|await|with|flask|django|socketio|git|gil|el\s+gil)\b',
            r'\bc[oó]mo\s+hago\s+(?:un?a?\s+)?(?:bucle|loop|funci[oó]n|clase|decorador|generador|commit|push|branch)\b',
            r'\bexpl[ií]came\b',
            r'\bno\s+entiendo\s+(?:c[oó]mo|qu[eé])\b',
            r'\bqu[eé]\s+es\s+(?:pip|venv|virtualenv|pytest|unittest|pydantic|yield|generador)\b',
            r'\bqu[eé]\s+son\s+(?:los?\s+)?(?:generadores?|type\s+hints?|decoradores?)\b',
            r'\bc[oó]mo\s+(?:hago|funciona)\s+(?:un?a?\s+)?commit\b',
            r'\bdiferencia\s+(?:entre|hay)\b',
            r'\bcu[aá]ndo\s+(?:usar|uso|debo)\b',
            # Inglés — todos los conceptos Python
            r'\bgenerators?\b',
            r'\byield\b',
            r'\bcontext\s+managers?\b',
            r'\bdeep\s*copy\b',
            r'\bshallow\s+copy\b',
            r'\bthe\s+gil\b',
            r'\bglobal\s+interpreter\s+lock\b',
            r'\blist\s+comprehension\b',
            r'\bdict\s+comprehension\b',
            r'\bgenerator\s+expression\b',
            r'\bmetaclass\b',
            r'\bdescriptor\b',
            r'\bmethod\s+resolution\s+order\b',
            r'\bdataclass\b',
            r'\bprotocol\b',
            r'\babstract\s+class\b',
            r'\bproperty\s+decorator\b',
            r'\bstaticmethod\b',
            r'\bclassmethod\b',
            r'\bthreading\b',
            r'\bmultiprocessing\b',
            r'\basyncio\b',
            r'\bcoroutine\b',
            r'\biterator\b',
            r'\biterable\b',
            r'\bhow\s+does\b',
            r'\bwhat\s+is\b',
            r'\bwhat\s+are\b',
            r'\bexplain\b',
            r'\bdifference\s+between\b',
            r'\bwhen\s+to\s+use\b',
            r'\bhow\s+to\s+use\b',
        ],
        # Modo debug
        'patrones_debug': [
            r'\btengo\s+(?:este\s+|un\s+)?error\b',
            r'\bme\s+(?:sale|da|aparece)\s+(?:este\s+|un\s+)?error\b',
            r'\b(?:Traceback|traceback)\b',
            r'\b\w+Error:\s*\w*',
            r'\bpor\s+qu[eé]\s+(?:falla|no\s+funciona|no\s+corre)\b',
            r'\bc[oó]mo\s+(?:arreglo|soluciono|debugueo)\b',
            r'\bdebugueo\b', r'\bdebug\b',
            r'\berror\s+de\s+importaci[oó]n\b',
            r'\bModuleNotFoundError\b', r'\bImportError\b',
            r'\bno\s+corre\b', r'\bno\s+arranca\b',
        ],
        # Modo auto-analisis
        'patrones_auto': [
            r'\banaliza\s+tu\s+(?:propio\s+)?c[oó]digo\b',
            r'\banaliza\s+tus\s+archivos\b',
            r'\banaliza\s+(?:la\s+)?capa\s+\d+\b',
            r'\bqu[eé]\s+puedes\s+mejorar\s+de\s+ti\b',
            r'\btienes\s+bugs\b',
            r'\banaliza\s+belladonna\b',
            r'\banaliza\s+tu\s+arquitectura\b',
            r'\brevis[ae]\s+tu\s+(?:propio\s+)?c[oó]digo\b',
            # Patrones: "analiza tu [archivo]" — cualquier cosa después de "analiza tu"
            r'\banaliza\s+tu\s+\w+\b',
            r'\banaliza\s+(?:tu\s+)?capa\d+\b',
            r'\banaliza\s+(?:el\s+)?generador\b',
            r'\banaliza\s+(?:el\s+)?constructor\b',
            r'\bqu[eé]\s+puedes\s+mejorar\s+de\s+tu\b',
            r'\bmejorar\s+(?:tu|de\s+tu)\s+(?:propio\s+)?c[oó]digo\b',
        ],
        # Patrones generales Python
        'patrones': [
            r'\bdef\s+\w+\(',
            r'\bclass\s+\w+',
            r'^\s*import\s+\w+',
            r'^\s*from\s+\w+\s+import\b',
            r'\bpython\b',
            r'\.py\b',
        ],
    },
    'SHELL': {
        'disponible':  False,
        'descripcion': 'Comandos del sistema operativo',
        'patrones': [
            r'\bejecuta\s+(?:el\s+)?comando\b',
            r'\bcorre\s+el\s+comando\b',
            r'\blistar?\s+archivos\b',
            r'\b(?:ls|dir|pwd|mkdir|rmdir|rm|cp|mv|cat|grep|find)\b',
            r'\bgit\s+(?:init|add|commit|push|pull|clone|status)\b',
            r'\bnpm\s+(?:install|start|run|build|test)\b',
            r'\bpip\s+install\b',
        ],
    },
    'MEMORIA': {
        'disponible': True,
        'descripcion': 'Bell recuerda conversaciones previas, perfil de Sebastian y su propia historia',
        'patrones': [
            r'\brecuerdas\b', r'\brecuerda\b',
            r'\bqu[eé]\s+recuerdas\b',
            r'\bqu[eé]\s+sabes\s+de\s+m[ií]\b',
            r'\bqu[eé]\s+sabes\s+de\s+ti\b',
            r'\bmi\s+perfil\b',
            r'\bhistoria\s+(?:de\s+)?(?:nuestras?|mis)\s+conversaci[oó]n',
            r'\bqu[eé]\s+me\s+dijiste\b',
            r'\bhablamos\s+de\b',
            r'\barchivos\s+(?:que\s+has|analizados?)\b',
            r'\bcu[aá]ntas?\s+conversaciones\b',
            r'\bcu[aá]nto\s+llevamos\b',
        ],
    },
    'SQLITE': {
        'disponible':  False,
        'descripcion': 'Base de datos SQLite',
        'patrones': [
            r'\bbase\s+de\s+datos\b',
            r'\bcrea\s+(?:una?\s+)?tabla\b',
            r'\bguarda\s+(?:en|esto|eso)\b',
            r'\binserta\s+(?:en\s+)?\b',
            r'\bconsulta\s+(?:la\s+)?(?:base|tabla)\b',
            r'\b(?:select|insert|update|delete|create\s+table|drop\s+table)\b',
            r'\bpon\s+(?:en\s+)?(?:la\s+)?(?:base|tabla)\b',
        ],
    },
}

# ── Palabras de verbosidad para detectar en el texto ──────────────
_VERBOSIDAD_SIMPLE = [
    'más simple', 'mas simple', 'más sencillo', 'mas sencillo',
    'resúmelo', 'resumelo', 'brevemente', 'en pocas palabras',
    'resumido', 'breve', 'corto', 'simplifica', 'sin tecnicismos',
    'más corto', 'mas corto', 'no tan técnico', 'no tan tecnico',
    'sin tanto detalle',
]
_VERBOSIDAD_DETALLADA = [
    'más detallado', 'mas detallado', 'con más detalle', 'profundo',
    'explícame bien', 'completo', 'todo lo que puedas', 'a fondo',
    'explica cada parte', 'técnicamente', 'con tecnicismos',
    'análisis completo', 'analisis completo',
]


class DetectorHabilidad:

    # Temas que Bell ya conoce — no buscar en internet
    _TEMAS_INTERNOS = {
        'bell', 'belladonna', 'grounding', 'capa', 'capas',
        'consejera', 'consejeras', 'habilidad', 'habilidades',
        'motor', 'pipeline', 'bell_core', 'bellcore',
        'vega', 'echo', 'lyra', 'nova', 'luna', 'iris', 'sage', 'soma',
        'mente pura', 'arquitectura', 'zona de desconocimiento',
        'vocabulario', 'neurona', 'nodo', 'sebastian', 'sebas',
        'jelcon', 'uniminuto', 'bucaramanga',
    }

    def detectar(self, texto: str, decision_final: dict,
                 tipo_respuesta: str = 'conversacional') -> dict:
        texto_lower = texto.lower().strip()

        # ── FIX 2: plan de navegación pausado → todo va al navegador ──
        # Si Bell pausó esperando una respuesta (credenciales, confirmación),
        # el siguiente mensaje retoma ese plan, sin reclasificar.
        try:
            from biblioteca.habilidades.navegador.planificador import EstadoPausa
            if EstadoPausa.esta_activo():
                return {
                    'necesita_habilidad': True,
                    'habilidad_id':       'NAVEGADOR_WEB',
                    'disponible':         True,
                    'texto_original':     texto,
                    'verbosidad':         'normal',
                    'fuente_deteccion':   'pausa_navegador',
                }
        except Exception:
            pass

        # ── NAVEGADOR: contexto de navegación gana sobre Python/emocional ──
        # (FIX 1 + 2) Si hay sitio web + verbo de navegación (o C3 ya lo marcó),
        # va a NAVEGADOR_WEB antes de la detección de Python.
        _SITIOS_NAV = [
            'youtube', 'instagram', 'github', 'gmail', 'twitter', 'x.com',
            'spotify', 'crunchyroll', 'netflix', 'twitch', 'linkedin',
            'facebook', 'tiktok', 'reddit', 'wikipedia', 'stackoverflow',
            'amazon', 'mercadolibre',
        ]
        _VERBOS_NAV = [
            'busca en', 'abre ', 'navega a', 've a', 'ponme', 'reproduce',
            'inicia sesion', 'inicia sesión', 'escríbele', 'escribele',
            'manda un mensaje', 'envíale', 'dame la url',
            'mis repos', 'mis repositorios', 'lee http', 'descarga el',
        ]
        _hab_c3_nav      = decision_final.get('habilidad_req', '') == 'NAVEGADOR_WEB'
        _tiene_sitio_nav = any(s in texto_lower for s in _SITIOS_NAV)
        _tiene_verbo_nav = any(v in texto_lower for v in _VERBOS_NAV)
        # FIX/CAMBIO 5: investigación NO va al navegador (no abrir Chrome) →
        # va a BUSQUEDA_INTERNET con respuesta detallada.
        _KW_INVESTIGACION = ['investiga ', 'investigar ', 'dame todo sobre',
                             'explícame a fondo', 'explicame a fondo', 'explícame todo']
        _es_investigacion = any(k in texto_lower for k in _KW_INVESTIGACION)
        if _es_investigacion:
            cfg_b = HABILIDADES.get('BUSQUEDA_INTERNET', {})
            return {
                'necesita_habilidad': True,
                'habilidad_id':       'BUSQUEDA_INTERNET',
                'modo':               None,
                'disponible':         cfg_b.get('disponible', False),
                'descripcion':        cfg_b.get('descripcion', ''),
                'texto_original':     texto,
                'verbosidad':         'detallado',
                'fuente_deteccion':   'investigacion',
            }
        if ((_hab_c3_nav
             or (_tiene_sitio_nav and (_tiene_verbo_nav or 'http' in texto_lower)))
                and HABILIDADES.get('NAVEGADOR_WEB', {}).get('disponible')
                and '```' not in texto):
            return {
                'necesita_habilidad': True,
                'habilidad_id':       'NAVEGADOR_WEB',
                'modo':               None,
                'disponible':         True,
                'descripcion':        HABILIDADES['NAVEGADOR_WEB'].get('descripcion', ''),
                'texto_original':     texto,
                'verbosidad':         'normal',
                'fuente_deteccion':   'nav_contexto',
            }

        # Tipos emocionales puros → nunca necesitan habilidad
        _BYPASS = {
            'emocional', 'matematica_python',
            'honestidad_limitacion', 'veto_respuesta',
        }
        # 'conversacional' solo hace bypass si NO tiene palabras de búsqueda
        # y NO tiene patrones de memoria
        _KW_BUSQUEDA_C7 = [
            'qué es ', 'que es ', 'quién es ', 'quien es ',
            'diferencia entre', 'compara ', 'cómo funciona', 'como funciona',
            'precio del', 'precio de ', 'cuánto cuesta', 'cuanto cuesta',
            'hoy ', 'hoy?', 'noticias', 'fyi:', 'fyi ',
            'busca ', 'buscar ', 'dónde', 'donde ', 'cuándo', 'cuando ',
            'cómo se', 'como se', 'qué son', 'que son',
            'capital de', 'cuándo fue', 'cuando fue', 'historia de',
            'cuándo nació', 'cuando nacio', 'quién inventó', 'quien invento',
            'cómo instalar', 'como instalar', 'tutorial', 'guía', 'guia',
            'sabías que', 'sabias que', 'dato:', 'tip:',
            # ── Navegador Web ────────────────────────────────────
            'ponme', 'pon el video', 'reproduce', 'abre youtube', 'abre el video',
            'youtube', 'instagram', 'github', 'gmail', 'twitter',
            'lee http', 'lee https', 'navega a', 'abre la pagina', 'abre la página',
            'escríbele', 'escribele', 'manda un mensaje', 'envíale', 'enviame',
            'dame la url', 'url del repo', 'url del repositorio',
            'repositorio de', 'mis repos', 'mis repositorios',
            'inicia sesion', 'inicia sesión', 'loguéate', 'logueate',
            'descarga el', 'descargar el', 'llena el formulario',
            'video de ', 'último video', 'ultimo video', 'canal de ',
            'busca en youtube', 'busca en instagram', 'busca en github',
            've a la pagina', 've a la página', 'abre chrome',
            'spotify', 'crunchyroll', 'netflix', 'twitch',
        ]
        # Palabra sola desconocida que podría ser búsqueda (rust, vue, kotlin...)
        # Si es una sola palabra sin puntuación y no está en vocab Bell → buscar
        _es_palabra_sola = (len(texto_lower.split()) <= 3 and
                            '```' not in texto and
                            not any(c in texto_lower for c in ['def ', 'class ', 'import ']))
        _KW_MEM_C7 = [
            'recuerdas', 'hablamos de', 'me dijiste', 'sabes de mí', 'sabes de mi',
            'mi perfil', 'qué sabes', 'que sabes', 'en qué quedamos', 'en que quedamos',
            'la última vez', 'la ultima vez', 'quedamos en', 'me contaste',
            'cuánto llevamos', 'cuanto llevamos', 'cuántas conversaciones',
            'qué aprendiste', 'que aprendiste', 'qué conoces', 'que conoces',
            'qué recuerdas de', 'que recuerdas de',
        ]
        es_info = any(k in texto_lower for k in _KW_BUSQUEDA_C7) or _es_palabra_sola
        es_mem  = any(k in texto_lower for k in _KW_MEM_C7)

        # Early-exit C3 desactivado — habilidades búsqueda/memoria/auto en rediseño

        if tipo_respuesta in _BYPASS:
            return {
                'necesita_habilidad': False,
                'habilidad_id': None,
                'disponible': False,
                'texto_original': texto,
                'verbosidad': 'normal',
            }

        # ── MEMORIA: consultas de memoria van a la habilidad ───────
        # Antes del guard conversacional y de _NO_BUSCAR_TIPOS, para que
        # "¿qué sabes de mí?" no lo intercepte el path pregunta_sebastian.
        if es_mem and HABILIDADES.get('MEMORIA', {}).get('disponible'):
            return {
                'necesita_habilidad': True,
                'habilidad_id':       'MEMORIA',
                'modo':               None,
                'disponible':         True,
                'descripcion':        HABILIDADES['MEMORIA']['descripcion'],
                'texto_original':     texto,
                'verbosidad':         'normal',
                'fuente_deteccion':   'kw_memoria',
            }

        if tipo_respuesta == 'conversacional' and not es_info and not es_mem:
            # GUARD: no salir si el texto pide código Python aunque no tenga bloque
            _KW_CREACION_PY = [
                'en python', 'en Python',
                'crea una clase', 'crea un clase', 'crea una funcion',
                'crea una función', 'crea un metodo', 'crea un método',
                'crea una función', 'escribe una clase', 'escribe una función',
                'implementa una clase', 'implementa una función',
                'haz una función', 'haz una clase',
                'crea el código', 'escribe el código',
                'que tenga:', 'que tenga estado', 'que tenga nivel',
                'método activar', 'método procesar', 'metodo activar',
            ]
            _pide_python = any(kw.lower() in texto_lower for kw in _KW_CREACION_PY)
            if not _pide_python:
                return {
                    'necesita_habilidad': False,
                    'habilidad_id': None,
                    'disponible': False,
                    'texto_original': texto,
                    'verbosidad': 'normal',
                }
            # Si sí pide Python → continuar hacia detección de habilidad

        # Si el texto es sobre Bell/Sebastian → Bell lo responde sola
        _es_tema_interno = any(t in texto_lower for t in self._TEMAS_INTERNOS)
        _NO_BUSCAR_TIPOS = {
            'pregunta_identidad_bell', 'pregunta_estado_bell',
            'pregunta_arquitectura_bell', 'pregunta_accion_bell',
            'pregunta_sebastian', 'pregunta_capacidad_bell',
        }
        if tipo_respuesta in _NO_BUSCAR_TIPOS:
            return {
                'necesita_habilidad': False,
                'habilidad_id': None,
                'disponible': False,
                'texto_original': texto,
                'verbosidad': 'normal',
            }

        # Si el texto pregunta por un archivo específico → AUTO_ANALISIS gana
        import re as _re_det
        _es_pregunta_archivo = bool(_re_det.search(
            r'\bqu[eé]\s+(?:hace|es|contiene|tiene)\s+(?:el\s+|tu\s+)?\w[\w_]*\.(?:py|js|css|html|json|md)\b'
            r'|c[oó]mo\s+est[aá]\s+\w[\w_]*\.(?:py|js|css|html|json|md)\b'
            r'|c[oó]mo\s+funciona\s+\w[\w_]*\.(?:py|js)\b'
            r'|analiza\s+(?:el\s+)?\w[\w_]*\.(?:py|js)\b',
            texto_lower
        )) and '```' not in texto and not re.search(r'def\s+\w+\(', texto)
        if _es_pregunta_archivo and 'AUTO_ANALISIS_TOTAL' in HABILIDADES:
            cfg_aa = HABILIDADES['AUTO_ANALISIS_TOTAL']
            if cfg_aa.get('disponible'):
                return {
                    'necesita_habilidad': True,
                    'habilidad_id': 'AUTO_ANALISIS_TOTAL',
                    'disponible': True,
                    'modo': 'archivo_especifico',
                    'texto_original': texto,
                    'verbosidad': 'normal',
                }

        # Si el texto empieza con crea/hazme/implementa → es generacion, NUNCA debug
        _es_generacion = bool(re.match(
            r'^\s*(crea|hazme|implementa|escribe|diseña|construye|genera|haz\s+(?:un|una))',
            texto_lower
        ))

        # ── Detectar verbosidad ────────────────────────────────────
        verbosidad = 'normal'
        if any(v in texto_lower for v in _VERBOSIDAD_SIMPLE):
            verbosidad = 'simple'
        elif any(v in texto_lower for v in _VERBOSIDAD_DETALLADA):
            verbosidad = 'detallado'

        # ── AUTO_ANALISIS: interceptar ANTES de Python ─────────────
        # "cómo está X.py" / "qué hace X.py" sin bloque de código → Bell analiza su propio archivo
        _pregunta_archivo_bell = bool(re.search(
            r'(?:cómo|como)\s+est[aá]\s+\w[\w_]*\.(?:py|js|css|html|json|md)'
            r'|(?:qué|que)\s+(?:hace|es|contiene|tiene)\s+\w[\w_]*\.(?:py|js|css|html|json|md)'
            r'|analiza\s+(?:el\s+)?\w[\w_]*\.(?:py|js)'
            r'|cómo\s+funciona\s+\w[\w_]*\.(?:py|js)',
            texto_lower
        ))
        _tiene_bloque_codigo = '```' in texto or bool(re.search(r'def\s+\w+\(|class\s+\w+', texto))
        if _pregunta_archivo_bell and not _tiene_bloque_codigo:
            return {
                'necesita_habilidad': True,
                'habilidad_id':       'AUTO_ANALISIS_TOTAL',
                'modo':               None,
                'disponible':         HABILIDADES['AUTO_ANALISIS_TOTAL']['disponible'],
                'descripcion':        HABILIDADES['AUTO_ANALISIS_TOTAL']['descripcion'],
                'texto_original':     texto,
                'verbosidad':         'normal',
            }

        # ── Detectar PYTHON primero — es la habilidad prioritaria ──
        cfg_py = HABILIDADES['PYTHON_COMPLETO']
        modo_python = self._detectar_modo_python(texto_lower, texto, cfg_py, _es_generacion)

        # Si C3 ya detectó que se necesita Python pero los patrones de C7 no lo vieron,
        # confiar en C3 — tiene más contexto semántico
        if not modo_python:
            habilidad_c3 = decision_final.get('habilidad_req', '')
            if habilidad_c3 == 'PYTHON_COMPLETO':
                modo_python = decision_final.get('modo_python', 'explicacion')

        if modo_python:
            # Guard: si hay URL externa en el texto → es NAVEGADOR, no Python
            import re as _re_nav
            _tiene_url_externa = bool(_re_nav.search(r'https?://', texto))
            _verbos_navegacion = ['lee ', 'leer ', 'abre ', 'navega', 've a']
            _es_peticion_web = _tiene_url_externa and any(v in texto_lower for v in _verbos_navegacion)
            if not _es_peticion_web:
                return {
                    'necesita_habilidad': True,
                    'habilidad_id':       'PYTHON_COMPLETO',
                    'modo':               modo_python,
                    'disponible':         cfg_py['disponible'],
                    'descripcion':        cfg_py['descripcion'],
                    'texto_original':     texto,
                    'verbosidad':         verbosidad,
                }
            # Si es petición web con URL → dejar que NAVEGADOR_WEB lo tome en el loop

        # ── Resto de habilidades ───────────────────────────────────
        for habilidad_id, config in HABILIDADES.items():
            if habilidad_id == 'PYTHON_COMPLETO':
                continue
            for patron in config.get('patrones', []):
                if re.search(patron, texto_lower, re.IGNORECASE):
                    # Si es BUSQUEDA pero habla de temas internos → no buscar
                    if habilidad_id == 'BUSQUEDA_INTERNET' and _es_tema_interno:
                        continue
                    return {
                        'necesita_habilidad': True,
                        'habilidad_id':       habilidad_id,
                        'modo':               None,
                        'disponible':         config['disponible'],
                        'descripcion':        config['descripcion'],
                        'texto_original':     texto,
                        'verbosidad':         verbosidad,
                    }

        # ── FALLBACK SEMÁNTICO: pregunta + palabras desconocidas → buscar ──
        # Si el usuario pregunta algo con palabras que Bell no reconoce
        # es muy probable que sea una búsqueda de información externa.
        _NODOS_PREGUNTA = {
            'PREG_QUE', 'PREG_QUIEN', 'PREG_DONDE', 'PREG_CUANDO',
            'PREG_COMO', 'PREG_CUANTO', 'PREG_CUAL', 'PRON_INTERR_QUE',
            'PRON_INTERR_QUIEN', 'PRON_INTERR_CUANT', 'PREG_CUALES',
        }
        _PALABRAS_PREGUNTA = [
            'qué', 'que', 'quién', 'quien', 'dónde', 'donde',
            'cuándo', 'cuando', 'cómo', 'como', 'cuál', 'cual',
            'cuánto', 'cuanto', 'para qué', 'por qué',
            'háblame', 'hablame', 'cuéntame', 'cuentame',
            'explícame', 'explicame', 'busca', 'investiga',
        ]
        _NO_BELL = ['bell', 'belladonna', 'capa', 'consejera', 'habilidad',
                    'vocabulario', 'archivo', 'groq']
        # decision_final trae conceptos de C1 y nodos de C2
        _conceptos_activos = decision_final.get('conceptos_activados', []) or []
        _desconocidos = decision_final.get('desconocidos', []) or []
        tiene_pregunta = (
            bool(set(_conceptos_activos) & _NODOS_PREGUNTA) or
            any(p in texto_lower for p in _PALABRAS_PREGUNTA)
        )
        es_sobre_bell = any(p in texto_lower for p in _NO_BELL)
        # Palabra sola desconocida (ej: "rust", "vue", "kotlin") → buscar
        _texto_corto = len(texto_lower.split()) <= 3
        if (_texto_corto and _desconocidos and not es_sobre_bell):
            return {
                'necesita_habilidad': True,
                'habilidad_id':       'BUSQUEDA_INTERNET',
                'disponible':         True,
                'texto_original':     texto,
                'verbosidad':         'normal',
                'fuente':             'semantico_palabra_desconocida',
            }
        if (tiene_pregunta and _desconocidos and not es_sobre_bell):
            return {
                'necesita_habilidad': True,
                'habilidad_id':       'BUSQUEDA_INTERNET',
                'disponible':         True,
                'fuente':             'semantico_pregunta_desconocida',
            }

        # ── FALLBACK UNIVERSAL: detectar preguntas sobre Bell que no matchearon ──
        if _podria_ser_autoanalisis_semantico(texto_lower):
            return {
                'necesita_habilidad': True,
                'habilidad_id':       'AUTO_ANALISIS_TOTAL',
                'disponible':         True,
                'modo':               'resumen_general',
                'texto_original':     texto,
                'verbosidad':         verbosidad,
            }

        # ── CLASIFICADOR BELL — usa habilidad_req de C3 ─────────
        # C3 ya entregó habilidad_req en decision_final.
        # Si llegamos aquí, lo leemos directamente sin API.
        hab_c3 = decision_final.get('habilidad_req', '')
        if hab_c3 in ('BUSQUEDA_INTERNET', 'PYTHON_COMPLETO', 'AUTO_ANALISIS_TOTAL', 'MEMORIA', 'NAVEGADOR_WEB'):
            cfg_b = HABILIDADES.get(hab_c3, {})
            print(f'  [C7 Bell] {hab_c3} ← habilidad_req de C3')
            return {
                'necesita_habilidad': True,
                'habilidad_id':       hab_c3,
                'modo':               cfg_b.get('modo_default', None),
                'disponible':         cfg_b.get('disponible', True),
                'descripcion':        cfg_b.get('descripcion', ''),
                'texto_original':     texto,
                'verbosidad':         verbosidad,
                'fuente_deteccion':   'clasificador_bell',
            }

        return {
            'necesita_habilidad': False,
            'habilidad_id':       None,
            'modo':               None,
            'disponible':         False,
            'descripcion':        '',
            'texto_original':     texto,
            'verbosidad':         verbosidad,
        }

    def _detectar_modo_python(self, tl: str, texto_orig: str, cfg: dict, es_generacion: bool = False) -> str:
        """Detecta cuál de los 5 modos Python se necesita."""
        # Ejecutar tiene prioridad si pide correr/ejecutar código
        _KW_EJECUTAR = ['ejecuta esto', 'ejecuta el', 'corre esto', 'corre el', 'prueba esto', 'ejecuta ']
        if any(k in tl for k in _KW_EJECUTAR):
            return 'ejecutar'

        # Debug tiene prioridad si hay traceback o error explícito
        for pat in cfg.get('patrones_debug', []):
            if re.search(pat, texto_orig, re.IGNORECASE | re.MULTILINE):
                if not es_generacion:   # nunca debug si empieza con crea/hazme
                    return 'debug'

        # Auto-análisis
        for pat in cfg.get('patrones_auto', []):
            if re.search(pat, tl, re.IGNORECASE):
                return 'auto_analisis'

        # Análisis de código ajeno
        for pat in cfg.get('patrones_analisis', []):
            if re.search(pat, tl, re.IGNORECASE):
                return 'analisis'

        # Generación
        for pat in cfg.get('patrones_generacion', []):
            if re.search(pat, tl, re.IGNORECASE):
                return 'generacion'

        # Explicación
        _KW_PYTHON_EXPL = [
            'async', 'await', 'yield', 'lambda', 'decorator', 'decorador',
            'generator', 'generador', 'list comprehension', 'dict comprehension',
            'threading', 'multiprocessing', 'asyncio', 'coroutine', 'coroutina',
            'dataclass', 'metaclass', 'descriptor', 'protocol', 'abc',
            'flask', 'django', 'numpy', 'pandas', 'pytorch', 'tensorflow',
            'pip', 'venv', 'pytest', 'type hint', 'type hints', 'typing',
            'context manager', 'with statement', 'dunder', 'magic method',
            'gil', 'global interpreter', 'bytecode', 'cpython',
            'list', 'dict', 'tuple', 'set ', 'frozenset',
        ]
        for pat in cfg.get('patrones_explicacion', []):
            if re.search(pat, tl, re.IGNORECASE):
                # Guard: "diferencia entre X y Y" sin concepto Python → es BUSQUEDA
                if re.search(r'\bdiferencia\s+entre\b', tl):
                    if not any(kw in tl for kw in _KW_PYTHON_EXPL):
                        continue  # No es diferencia entre conceptos Python
                return 'explicacion'

        # Patrones generales Python (código pegado directamente)
        for pat in cfg.get('patrones', []):
            if re.search(pat, texto_orig, re.IGNORECASE | re.MULTILINE):
                # Si el texto tiene estructura de código real → análisis
                if any(k in texto_orig for k in ['def ', 'class ', 'import ', 'Traceback']):
                    return 'analisis'
                return 'explicacion'

        return ''

    def estado(self) -> dict:
        return {
            hid: {
                'disponible':  cfg['disponible'],
                'descripcion': cfg['descripcion'],
            }
            for hid, cfg in HABILIDADES.items()
        }