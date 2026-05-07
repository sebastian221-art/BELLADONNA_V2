# capas/capa7/detector_habilidad.py
# ================================================
# DETECTOR DE HABILIDAD — v2 con PYTHON_COMPLETO
# ================================================

import re

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

    def detectar(self, texto: str, decision_final: dict) -> dict:
        texto_lower = texto.lower().strip()

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
            return {
                'necesita_habilidad': True,
                'habilidad_id':       'PYTHON_COMPLETO',
                'modo':               modo_python,
                'disponible':         cfg_py['disponible'],
                'descripcion':        cfg_py['descripcion'],
                'texto_original':     texto,
                'verbosidad':         verbosidad,
            }

        # ── Resto de habilidades ───────────────────────────────────
        for habilidad_id, config in HABILIDADES.items():
            if habilidad_id == 'PYTHON_COMPLETO':
                continue
            for patron in config.get('patrones', []):
                if re.search(patron, texto_lower, re.IGNORECASE):
                    return {
                        'necesita_habilidad': True,
                        'habilidad_id':       habilidad_id,
                        'modo':               None,
                        'disponible':         config['disponible'],
                        'descripcion':        config['descripcion'],
                        'texto_original':     texto,
                        'verbosidad':         verbosidad,
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
        for pat in cfg.get('patrones_explicacion', []):
            if re.search(pat, tl, re.IGNORECASE):
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