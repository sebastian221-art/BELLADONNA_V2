# -*- coding: utf-8 -*-
"""
motor_razonamiento.py  VERSION v9.0

CAMBIOS v9.0 sobre v8.9-FIX-BD:
═══════════════════════════════════════════════════════════════════
FIX-M1  "cuánto es 15 * 8" → DESCONOCIDO (debería ser CALCULO)
        CAUSA: CONCEPTO_OCHO_NUM no está en TRIGGERS_CALCULO, y
               _es_calculo_por_texto() no detectaba operador directo.
        FIX:  _es_calculo_por_texto() agrega patrón \d+\s*[+\-*/]\s*\d+.

FIX-M2  "cuánto es el 15% de 200" → CONFIRMACION (por CONCEPTO_200_OK)
        CAUSA: CONCEPTO_200_OK en TRIGGERS_CONFIRMACION_POSITIVA se evaluaba
               antes de _es_calculo(). El porcentaje nunca llegaba a CALCULO.
        FIX:  a) _es_calculo_por_texto() detecta \d+\s*% y "por ciento".
              b) clasificar_intencion(): en el bloque CONFIRMACION, si el
                 mensaje tiene expresión calculable, prioriza CALCULO.

FIX-M3  "resuelve x^2 - 5x + 6 = 0" → NEGATIVA certeza=0%
        CAUSA: traductor da confianza baja → razonar() entra en early-exit
               y no encuentra patrón shell ni BD → devuelve no-entendido.
        FIX:  En bloque confianza < 0.3 de razonar(), agregar detección de
              expresiones matemáticas avanzadas (verbo + contenido algebraico).
              Nueva constante: _RE_EXPR_MAT_AVANZADA_CON_VERBO.

Todos los fixes BD (FIX-BD1, BD2, BD3) preservados intactos de v8.9.
═══════════════════════════════════════════════════════════════════
"""
import re
import unicodedata
from typing import Dict, Optional

from razonamiento.tipos_decision import (
    Decision,
    TipoDecision,
    RazonRechazo,
    TIPOS_GUARDAN_EN_MEMORIA,
    TIPOS_ACTUALIZAN_ESTADO,
)
from razonamiento.generador_decisiones import GeneradorDecisiones

from core.capacidades_fase import (
    NO_IMPLEMENTADAS_IDS,
    esta_implementada,
    razon_no_implementada,
    detectar_patron_no_implementado,
)

try:
    from identidad_bell import (
        NARRATIVA_PROPIA,
        VOZ_BELL,
        obtener_fragmento_identidad_para_prompt,
    )
    _IDENTIDAD_DISPONIBLE = True
except ImportError:
    _IDENTIDAD_DISPONIBLE = False

try:
    from habilidades.registro_habilidades import RegistroHabilidades
    _REGISTRO_DISPONIBLE = True
except ImportError:
    _REGISTRO_DISPONIBLE = False

try:
    from habilidades.shell_habilidad import HabilidadShell as _HabilidadShell
    _SHELL_DISPONIBLE = True
except ImportError:
    _HabilidadShell = None
    _SHELL_DISPONIBLE = False

try:
    from razonamiento.patrones_habilidades import detectar_habilidad_externa as _detectar_hab_ext
    _PATRONES_EXT_DISPONIBLE = True
except ImportError:
    _detectar_hab_ext = None
    _PATRONES_EXT_DISPONIBLE = False

_PETICION_OPERACION = "_PETICION_OPERACION"


# ======================================================================
# NORMALIZADOR
# ======================================================================
def _norm(texto: str) -> str:
    nfkd = unicodedata.normalize('NFD', texto)
    sin_tildes = ''.join(c for c in nfkd if unicodedata.category(c) != 'Mn')
    return sin_tildes.lower()


# ======================================================================
# CONCEPTOS SHELL
# ======================================================================
_CONCEPTOS_SHELL_IDS = {
    "CONCEPTO_LS", "CONCEPTO_PWD", "CONCEPTO_DATE",
    "CONCEPTO_WHOAMI", "CONCEPTO_HOSTNAME", "CONCEPTO_UNAME",
    "CONCEPTO_UPTIME", "CONCEPTO_PS", "CONCEPTO_TOP",
    "CONCEPTO_DF", "CONCEPTO_DU", "CONCEPTO_FREE",
    "CONCEPTO_ENV", "CONCEPTO_ECHO", "CONCEPTO_TREE",
    "CONCEPTO_GREP", "CONCEPTO_FIND", "CONCEPTO_HEAD",
    "CONCEPTO_TAIL", "CONCEPTO_WC", "CONCEPTO_CAT",
    "CONCEPTO_STAT", "CONCEPTO_FILE",
    "CONCEPTO_KILL", "CONCEPTO_MKDIR", "CONCEPTO_TOUCH",
    "CONCEPTO_HOY",
    "CONCEPTO_MEMORIA",
    "CONCEPTO_PROCESO_SHELL", "CONCEPTO_CPU_SHELL",
    "CONCEPTO_DISCO",
}

# ======================================================================
# CONCEPTOS SQLITE
# ======================================================================
_CONCEPTOS_SQLITE_IDS = {
    "CONCEPTO_SQLITE",
    "CONCEPTO_SQL",
    "CONCEPTO_TABLA",
    "CONCEPTO_SELECT",
    "CONCEPTO_LISTAR_TABLAS",
    "CONCEPTO_ESQUEMA",
    "CONCEPTO_COUNT",
    "CONCEPTO_INSERT",
    "CONCEPTO_UPDATE",
    "CONCEPTO_DELETE",
    "CONCEPTO_CREAR_TABLA",
    "CONCEPTO_ELIMINAR_TABLA",
    "CONCEPTO_VACIAR_TABLA",
    "CONCEPTO_INSERTAR_DATOS",
    "CONCEPTO_SQL_ESCRITURA",
    "CONCEPTO_REGISTRO",
    "CONCEPTO_RESULTADO_QUERY",
    "CONCEPTO_TRANSACCION",
    "CONCEPTO_INDICE",
    "CONCEPTO_CONECTAR_BD",
    "CONCEPTO_DESCONECTAR_BD",
    "CONCEPTO_BASE_DATOS",
}

# ======================================================================
# PATRONES SHELL
# ======================================================================
_PATRONES_SHELL_DIRECTOS = [
    r'lista\s+(?:tus\s+)?archivos',
    r'lista\s+(?:los\s+)?archivos',
    r'muestr[a-z]*\s+(?:tus?\s+|los\s+)?archivos',
    r'que\s+archivos\s+(?:hay|tienes)',
    r'donde\s+est[a-z]*',
    r'directorio\s+actual',
    r'ruta\s+actual',
    r'en\s+que\s+(?:directorio|carpeta)',
    r'cual\s+es\s+tu\s+directorio',
    r'que\s+fecha',
    r'fecha\s+(?:de\s+)?hoy',
    r'que\s+hora',
    r'hora\s+actual',
    r'que\s+dia\s+(?:es\s+)?hoy',
    r'cuanta\s+(?:ram|memoria)',
    r'memoria\s+(?:ram|disponible|libre|usada)',
    r'uso\s+de\s+memoria',
    r'espacio\s+en\s+disco',
    r'espacio\s+(?:libre|disponible)',
    r'cuanto\s+espacio',
    r'procesos\s+(?:activos|corriendo)',
    r'que\s+procesos',
    r'usuario\s+(?:del\s+sistema|actual)',
    r'con\s+que\s+usuario',
    r'que\s+usuario\s+soy',
    r'que\s+usuario\s+eres',           # FIX-H7 en motor también
    r'cual\s+es\s+tu\s+usuario',       # FIX-H7
    r'sistema\s+operativo',
    r'informacion\s+del\s+sistema',
    r'que\s+(?:linux|kernel|sistema)',
    r'version\s+(?:de\s+)?python',
    r'python\s+version',
    r'nombre\s+del\s+(?:equipo|servidor|maquina)',
    r'estado\s+(?:de\s+)?git',
    r'git\s+status',
    r'historial\s+(?:de\s+)?git',
    r'log\s+(?:de\s+)?git',
    r'ramas?\s+(?:de\s+)?git',
    r'variables?\s+de\s+entorno',
    r'tiempo\s+(?:encendido|activo)',
    r'cuanto\s+tiempo\s+(?:lleva|llevas)\s+(?:corriendo|activ[oa]|encendido)',
    r'paquetes?\s+(?:pip|python|instalados?)',
    r'que\s+(?:paquetes?|librerias?)\s+(?:hay|tienes)',
    r'estructura\s+(?:de\s+)?(?:carpetas|directorios)',
    r'arbol\s+(?:de\s+)?directorios',
]

_RE_PATRONES_SHELL = [re.compile(p, re.IGNORECASE) for p in _PATRONES_SHELL_DIRECTOS]


# ======================================================================
# PATRONES BD (lectura + escritura completos — de v8.9-FIX-BD)
# ======================================================================
_PATRONES_BD_DIRECTOS = [
    r'estado\s+de\s+(?:tu\s+)?(?:base\s+de\s+datos|bd|sqlite)',
    r'qu[e]\s+(?:base\s+de\s+datos|bd)\s+tienes',
    r'tienes\s+(?:una\s+)?(?:base\s+de\s+datos|bd)',
    r'muestra(?:me)?\s+(?:tu\s+)?(?:base\s+de\s+datos|bd)',
    r'info(?:rmacion)?\s+de\s+(?:la\s+)?(?:base\s+de\s+datos|bd)',
    r'qu[e]\s+tablas?\s+(?:hay|tienes|existen)',
    r'lista(?:me)?\s+(?:las\s+)?tablas?',
    r'muestr[a-z]*\s+(?:las\s+)?tablas?',
    r'cu[a]ntas?\s+tablas?\s+(?:hay|tienes)',
    r'tablas?\s+(?:disponibles?|existentes?)',
    r'esquema\s+de\s+(?:la\s+)?(?:tabla\s+)?\w+',
    r'estructura\s+de\s+(?:la\s+)?(?:tabla\s+)?\w+',
    r'columnas?\s+de\s+(?:la\s+)?(?:tabla\s+)?\w+',
    r'campos?\s+de\s+(?:la\s+)?(?:tabla\s+)?\w+',
    r'describe\s+(?:la\s+)?(?:tabla\s+)?\w+',
    r'cu[a]ntos?\s+registros?\s+(?:hay|tiene)',
    r'cu[a]ntas?\s+filas?\s+(?:hay|tiene)',
    r'total\s+de\s+registros?\s+(?:en|de)\s+\w+',
    r'count\s+(?:de\s+)?\w+',
    r'datos?\s+de\s+(?:la\s+)?(?:tabla\s+)?\w+',
    r'contenido\s+de\s+(?:la\s+)?(?:tabla\s+)?\w+',
    r'registros?\s+de\s+(?:la\s+)?(?:tabla\s+)?\w+',
    r'muestra(?:me)?\s+(?:los?\s+)?(?:datos?|registros?)\s+de\s+\w+',
    r'^select\s+.+\s+from\s+\w+',
    r'ejecuta(?:me)?\s+(?:el\s+)?(?:sql|query|consulta)',
    r'consulta\s+sql',
    r'corre\s+(?:el\s+)?(?:sql|query)',
    r'[i]ndices?\s+de\s+(?:la\s+)?(?:tabla\s+)?\w+',
    r'[i]ndices?\s+(?:disponibles?|existentes?)',
    r'crea(?:r)?\s+(?:una\s+)?tabla\s+\w+',
    r'crea(?:r)?\s+tabla\s+\w+',
    r'nueva\s+tabla\s+\w+',
    r'hacer\s+(?:una\s+)?tabla\s+\w+',
    r'create\s+table\s+\w+',
    r'inserta(?:r)?\s+.+\s+en\s+\w+',
    r'agrega(?:r)?\s+.+\s+(?:a|en)\s+\w+',
    r'a[na]de?\s+.+\s+(?:a|en)\s+\w+',
    r'guarda(?:r)?\s+.+\s+en\s+\w+',
    r'^insert\s+into\s+\w+',
    r'insert\s+into\s+\w+',
    r'nuevo\s+registro\s+en\s+\w+',
    r'actualiza(?:r)?\s+.+\s+(?:en|de)\s+\w+',
    r'cambia(?:r)?\s+.+\s+(?:en|de)\s+\w+',
    r'modifica(?:r)?\s+.+\s+(?:en|de)\s+\w+',
    r'^update\s+\w+\s+set',
    r'update\s+\w+\s+set',
    r'elimin[a-z]*\s+.+\s+de\s+(?:la\s+)?(?:tabla\s+)?\w+',
    r'borra(?:r)?\s+.+\s+de\s+(?:la\s+)?(?:tabla\s+)?\w+',
    r'^delete\s+from\s+\w+',
    r'delete\s+from\s+\w+',
    r'vac[i]a(?:r)?\s+(?:la\s+)?(?:tabla\s+)?\w+',
    r'limpia(?:r)?\s+(?:la\s+)?(?:tabla\s+)?\w+',
    r'borra(?:r)?\s+todos?\s+(?:los\s+)?registros?\s+de\s+\w+',
    r'elimin[a-z]*\s+todos?\s+(?:los\s+)?registros?\s+de\s+\w+',
    r'^truncate\s+(?:table\s+)?\w+',
    r'truncate\s+(?:table\s+)?\w+',
    r'elimin[a-z]*\s+(?:la\s+)?tabla\s+\w+',
    r'borra(?:r)?\s+(?:la\s+)?tabla\s+\w+',
    r'^drop\s+(?:table\s+)?\w+',
    r'drop\s+(?:table\s+)?\w+',
    r'destruye?\s+(?:la\s+)?tabla\s+\w+',
]

_RE_PATRONES_BD = [re.compile(p, re.IGNORECASE) for p in _PATRONES_BD_DIRECTOS]


# ======================================================================
# FIX-M3: patrón para detectar mat avanzada con confianza baja
# ======================================================================
_RE_EXPR_MAT_AVANZADA_CON_VERBO = re.compile(
    r'(?:resolv|resuelv|deriv|integr|l[íi]mite|lim\s*\(|taylor|factori|simplif|expan)\w*'
    r'.{0,60}'
    r'(?:[a-zA-Z]\s*[\*\+\-\/\^]|[\*\+\-\/\^]\s*[a-zA-Z]|\d\s*[\*\+\-\/\^]|\()',
    re.IGNORECASE
)


# ======================================================================
# RESTO DE CONSTANTES (idénticas a v8.9 — sin cambios)
# ======================================================================

CONSEJERAS_ROLES_OFICIALES = {
    "Vega":  "Guardiana de principios y seguridad — tiene poder de veto sobre cualquier decision",
    "Echo":  "Verificadora de coherencia y logica — revisa que las respuestas sean verdaderas y consistentes",
    "Lyra":  "Inteligencia emocional — detecta el estado emocional del usuario y adapta el tono de Bell",
    "Nova":  "Ingenieria y optimizacion — evalua eficiencia tecnica y disena nuevos conceptos cuando Iris los detecta",
    "Luna":  "Reconocimiento de patrones — detecta repeticiones, tendencias y temas centrales en la conversacion",
    "Iris":  "Curiosidad y aprendizaje — detecta terminos desconocidos y propone nuevos conceptos para aprender",
    "Sage":  "Sintesis y sabiduria — integra todas las perspectivas del consejo para generar la respuesta final",
}

CAPACIDADES_REALES_BELL = {
    "ejecutables": [
        "Razonar sobre problemas usando 1503 conceptos verificados",
        "Recordar la conversacion actual y datos del usuario",
        "Detectar emociones y adaptar el tono",
        "Consultar y modificar bases de datos SQLite (CRUD completo)",
        "Ejecutar codigo Python basico",
        "Ejecutar comandos de terminal (165 comandos disponibles)",
        "Calculos matematicos basicos y avanzados (SymPy): derivadas, integrales, limites, Taylor",
    ],
    "NO_ejecutables_aun": [
        "Crear archivos (capacidad pendiente de implementar)",
        "Leer archivos del sistema de archivos (pendiente)",
        "Acceder a internet",
        "Procesar imagenes",
        "Recordar conversaciones de sesiones anteriores (solo recuerda datos del usuario)",
    ],
}

CONFIRMACIONES_DIRECTAS = {
    "si", "si", "no", "ok", "okay", "dale", "listo", "claro",
    "correcto", "exacto", "perfecto", "adelante", "negativo",
    "afirmativo", "bueno", "bien", "entendido", "de acuerdo",
    "va", "ya", "andale", "andale", "sale",
}

NOMBRES_CONSEJERAS = {"vega", "echo", "lyra", "nova", "luna", "iris", "sage"}

PALABRAS_LLM = {
    "modelo de lenguaje", "llm", "chatgpt", "gpt", "openai",
    "inteligencia artificial", "ia", "bot", "chatbot", "robot",
    "claude", "gemini", "copilot", "bard",
}

PATRONES_COGNITIVOS_TEXTO = {
    "explicame":    "EXPLICAR",
    "explica":      "EXPLICAR",
    "simplifica":   "SIMPLIFICAR",
    "simplificame": "SIMPLIFICAR",
    "repite":       "REPETIR",
    "repetir":      "REPETIR",
    "define":       "DEFINIR",
    "defineme":     "DEFINIR",
    "reformula":    "REFORMULAR",
    "aclara":       "ACLARAR",
    "continua":     "ELABORAR",
    "desarrolla":   "ELABORAR",
    "amplia":       "ELABORAR",
}

PATRONES_SOCIAL_TEXTO = {
    "buenos dias":        "SALUDO",
    "buenas tardes":      "SALUDO",
    "buenas noches":      "SALUDO",
    "buenas":             "SALUDO",
    "buen dia":           "SALUDO",
    "muchas gracias":     "AGRADECIMIENTO",
    "mil gracias":        "AGRADECIMIENTO",
    "te agradezco":       "AGRADECIMIENTO",
    "muy agradecido":     "AGRADECIMIENTO",
    "muy agradecida":     "AGRADECIMIENTO",
    "gracias por todo":   "AGRADECIMIENTO",
    "muchisimas gracias": "AGRADECIMIENTO",
}

_CUANTIFICACION_BELL = {
    "conceptos":            1503,
    "consejeras":           7,
    "comandos":             165,
    "comandos de terminal": 165,
}

TRIGGERS_IDENTIDAD = {
    "CONCEPTO_QUIEN", "CONCEPTO_QUIEN_PREGUNTA",
    "CONCEPTO_NOMBRE_ARCHIVO", "CONCEPTO_LLAMAR", "CONCEPTO_PRESENTAR",
    "CONCEPTO_QUE_ES", "CONCEPTO_COMO_TE_LLAMAS", "CONCEPTO_NOMBRE",
    "CONCEPTO_DESCRIBIR", "CONCEPTO_CUAL_ES_TU_NOMBRE",
    "CONCEPTO_QUIENES_ERES", "CONCEPTO_ERES", "CONCEPTO_HABLAR_DE_TI",
    "CONCEPTO_APRENDER", "CONCEPTO_DIFERENCIA", "CONCEPTO_COMPARAR",
    "CONCEPTO_FASE", "CONCEPTO_CRECIMIENTO", "CONCEPTO_PASO",
}

TRIGGERS_ESTADO_BELL = {
    "CONCEPTO_COMO", "CONCEPTO_COMO_PREGUNTA",
    "CONCEPTO_BUENO", "CONCEPTO_IR",
    "CONCEPTO_ESTAR", "CONCEPTO_BIEN", "CONCEPTO_FUNCIONANDO",
    "CONCEPTO_ACTIVO", "CONCEPTO_OPERATIVO", "CONCEPTO_COMO_VAS",
    "CONCEPTO_TODO_BIEN", "CONCEPTO_SIENTES", "CONCEPTO_ESTADO",
}

TRIGGERS_CAPACIDAD = {
    "CONCEPTO_PODER", "CONCEPTO_PODRIAS",
    "CONCEPTO_SABER", "CONCEPTO_SABER_V",
    "CONCEPTO_HACER",
    "CONCEPTO_CAPAZ", "CONCEPTO_POSIBLE", "CONCEPTO_IMPOSIBLE",
    "CONCEPTO_PUEDES", "CONCEPTO_HACES", "CONCEPTO_AYUDAR",
    "CONCEPTO_ERES_CAPAZ", "CONCEPTO_FUNCIONES", "CONCEPTO_HABILIDADES",
    "CONCEPTO_CAPACIDADES", "CONCEPTO_SIRVES",
    "CONCEPTO_PERMISOS_SHELL", "CONCEPTO_RED_OBJ",
    "CONCEPTO_ACCESO", "CONCEPTO_RECORDAR_ACCION",
}

TRIGGERS_SOCIAL = {
    "CONCEPTO_HOLA", "CONCEPTO_HOLA_EXPR", "CONCEPTO_BUENOS_DIAS",
    "CONCEPTO_ADIOS_EXPR",
    "CONCEPTO_GRACIAS", "CONCEPTO_GRACIAS_EXPR",
    "CONCEPTO_DISCULPA_EXPR",
    "CONCEPTO_BUENAS_TARDES", "CONCEPTO_BUENAS_NOCHES",
    "CONCEPTO_HEY", "CONCEPTO_BUENAS", "CONCEPTO_QUE_TAL",
    "CONCEPTO_SALUDAR", "CONCEPTO_BUEN_DIA",
    "CONCEPTO_HASTA_LUEGO", "CONCEPTO_CHAO", "CONCEPTO_BYE",
    "CONCEPTO_HASTA_PRONTO", "CONCEPTO_NOS_VEMOS",
    "CONCEPTO_HASTA_MANANA", "CONCEPTO_CUIDADE",
    "CONCEPTO_AGRADECIDO", "CONCEPTO_AGRADEZCO",
    "CONCEPTO_MIL_GRACIAS", "CONCEPTO_TE_AGRADEZCO", "CONCEPTO_MUCHAS_GRACIAS",
    "CONCEPTO_PERDON", "CONCEPTO_DISCULPA", "CONCEPTO_LO_SIENTO",
    "CONCEPTO_PERDONAME", "CONCEPTO_DISCULPAME",
}

TRIGGERS_ESTADO_USUARIO = {
    "CONCEPTO_FELIZ", "CONCEPTO_TRISTE", "CONCEPTO_ENOJADO",
    "CONCEPTO_FRUSTRADO", "CONCEPTO_CONFUNDIDO", "CONCEPTO_CANSADO",
    "CONCEPTO_PERDIDO_ESTADO", "CONCEPTO_ANSIOSO", "CONCEPTO_ABURRIDO",
    "CONCEPTO_PREOCUPADO", "CONCEPTO_ESTRESADO",
    "CONCEPTO_MOLESTO", "CONCEPTO_PERDIDO", "CONCEPTO_NO_ENTIENDO",
    "CONCEPTO_DIFICIL", "CONCEPTO_COMPLICADO",
    "CONCEPTO_EMOCIONADO", "CONCEPTO_CONTENTO", "CONCEPTO_INTERESANTE",
    "CONCEPTO_GENIAL", "CONCEPTO_INCREIBLE",
    "CONCEPTO_UNICO",
    "CONCEPTO_SOLEDAD",
}

TRIGGERS_ACCION_COGNITIVA = {
    "CONCEPTO_EXPLICAR", "CONCEPTO_EXPLICAR_V",
    "CONCEPTO_RESUMIR_ACCION", "CONCEPTO_SIMPLIFICAR",
    "CONCEPTO_DECIR", "CONCEPTO_CONTAR",
    "CONCEPTO_RESUMIR", "CONCEPTO_REPETIR",
    "CONCEPTO_ACLARAR", "CONCEPTO_PROFUNDIZAR", "CONCEPTO_EJEMPLIFICAR",
    "CONCEPTO_CONTINUAR", "CONCEPTO_ORDENAR", "CONCEPTO_CLASIFICAR",
    "CONCEPTO_DESTACAR", "CONCEPTO_REFORMULAR", "CONCEPTO_DESARROLLAR",
    "CONCEPTO_AMPLIAR", "CONCEPTO_TRADUCIR", "CONCEPTO_DEFINIR",
    "CONCEPTO_DETALLAR", "CONCEPTO_ELABORAR", "CONCEPTO_EXPANDIR",
    "CONCEPTO_CONTRASTAR",
}

_CONCEPTOS_COGNITIVOS_AMBIGUOS = {
    "CONCEPTO_SIMPLIFICAR",
    "CONCEPTO_EXPANDIR",
    "CONCEPTO_ELABORAR",
}

_CONCEPTOS_MAT_CALCULO = {
    "CONCEPTO_DERIVAR",
    "CONCEPTO_INTEGRAR",
    "CONCEPTO_RESOLVER_ECUACION",
    "CONCEPTO_SERIE_TAYLOR",
    "CONCEPTO_LIMITE",
    "CONCEPTO_SIMPLIFICAR",
    "CONCEPTO_EXPANDIR",
    "CONCEPTO_FACTORIZAR",
    "CONCEPTO_EVALUAR",
    "CONCEPTO_DERIVADA",
    "CONCEPTO_DERIVADA_PRIMERA",
    "CONCEPTO_DERIVADA_SEGUNDA",
    "CONCEPTO_INTEGRAL",
    "CONCEPTO_INTEGRAL_DEFINIDA",
    "CONCEPTO_INTEGRAL_INDEFINIDA",
    "CONCEPTO_RAIZ_AVANZADA",
    "CONCEPTO_ECUACION_AVANZADA",
}

TRIGGERS_CONFIRMACION_POSITIVA = {
    "CONCEPTO_SI", "CONCEPTO_SI_AFIRMACION",
    "CONCEPTO_DE_ACUERDO", "CONCEPTO_ENTENDIDO",
    "CONCEPTO_PERFECTO", "CONCEPTO_CORRECTO", "CONCEPTO_CORRECTO_RESP",
    "CONCEPTO_OK", "CONCEPTO_200_OK", "CONCEPTO_DALE", "CONCEPTO_CLARO",
    "CONCEPTO_POR_SUPUESTO", "CONCEPTO_EXACTO", "CONCEPTO_AFIRMATIVO",
    "CONCEPTO_ASI_ES", "CONCEPTO_LISTO", "CONCEPTO_ADELANTE",
}

TRIGGERS_CONFIRMACION_NEGATIVA = {
    "CONCEPTO_NO", "CONCEPTO_NO_NEGACION",
    "CONCEPTO_INCORRECTO_RESP", "CONCEPTO_MALO",
    "CONCEPTO_MAL", "CONCEPTO_INCORRECTO", "CONCEPTO_NO_ASI",
    "CONCEPTO_NEGATIVO",
}

TRIGGERS_TEMPORAL = {
    "CONCEPTO_ANTES", "CONCEPTO_AHORA", "CONCEPTO_DESPUES",
    "CONCEPTO_HACE_MOMENTO", "CONCEPTO_ANTERIORMENTE",
    "CONCEPTO_RECIEN", "CONCEPTO_PREVIO", "CONCEPTO_LUEGO",
    "CONCEPTO_HACE_RATO",
    "CONCEPTO_ANTES_DIJISTE",
    "CONCEPTO_MENCIONASTE", "CONCEPTO_DIJISTE", "CONCEPTO_AYER",
}

TRIGGERS_CUANTIFICACION = {
    "CONCEPTO_TODOS", "CONCEPTO_NINGUNO", "CONCEPTO_ALGUNOS",
    "CONCEPTO_PRIMERO", "CONCEPTO_ULTIMO", "CONCEPTO_SIGUIENTE",
    "CONCEPTO_CUANTOS", "CONCEPTO_MITAD", "CONCEPTO_VARIOS",
    "CONCEPTO_POCOS", "CONCEPTO_MUCHOS", "CONCEPTO_TODOS_LOS",
    "CONCEPTO_CUANTO", "CONCEPTO_NUMERO", "CONCEPTO_CANTIDAD",
    "CONCEPTO_CUANTOS_PREGUNTA",
}

TRIGGERS_REGISTRO_USUARIO = {
    "CONCEPTO_PROGRAMADOR", "CONCEPTO_INGENIERO", "CONCEPTO_ESTUDIANTE",
    "CONCEPTO_MEDICO", "CONCEPTO_TRABAJADOR", "CONCEPTO_DISENIADOR",
    "CONCEPTO_ESCRITOR", "CONCEPTO_EMPRESA", "CONCEPTO_PROFESION",
    "CONCEPTO_TRABAJO_OBJ", "CONCEPTO_PROGRAMA_OBJ",
}

TRIGGERS_CONSULTA_MEMORIA = {
    "CONCEPTO_DEDICAR",
    "CONCEPTO_OCUPACION",
}

TRIGGERS_VERIFICACION_LOGICA = {
    "CONCEPTO_VERDAD_RESP", "CONCEPTO_FALSO",
    "CONCEPTO_CORRECTO_RESP", "CONCEPTO_INCORRECTO_RESP",
    "CONCEPTO_VERIFICAR", "CONCEPTO_VALIDAR_ACCION", "CONCEPTO_CIERTO",
}

TRIGGERS_CALCULO = {
    "CONCEPTO_MULTIPLICACION", "CONCEPTO_POR_OP",
    "CONCEPTO_SUMA_OP", "CONCEPTO_RESTA_OP",
    "CONCEPTO_DIVISION", "CONCEPTO_POTENCIA", "CONCEPTO_RAIZ",
    "CONCEPTO_CALCULAR", "CONCEPTO_RESULTADO",
    "CONCEPTO_SUMA", "CONCEPTO_RESTA", "CONCEPTO_ENTRE_OP",
    "CONCEPTO_RAIZ_AVANZADA", "CONCEPTO_MODULO", "CONCEPTO_ABS",
    "CONCEPTO_REDONDEO", "CONCEPTO_PORCENTAJE",
    "CONCEPTO_DERIVAR", "CONCEPTO_DERIVADA",
    "CONCEPTO_DERIVADA_PRIMERA", "CONCEPTO_DERIVADA_SEGUNDA",
    "CONCEPTO_INTEGRAR", "CONCEPTO_INTEGRAL",
    "CONCEPTO_INTEGRAL_DEFINIDA", "CONCEPTO_INTEGRAL_INDEFINIDA",
    "CONCEPTO_LIMITE", "CONCEPTO_SERIE_TAYLOR",
    "CONCEPTO_SIMPLIFICAR", "CONCEPTO_EXPANDIR", "CONCEPTO_FACTORIZAR",
    "CONCEPTO_RESOLVER_ECUACION", "CONCEPTO_EVALUAR",
}

TRIGGERS_CONOCIMIENTO_GENERAL = {
    "CONCEPTO_CAPITAL_CIUDAD", "CONCEPTO_PAIS", "CONCEPTO_HISTORIA",
    "CONCEPTO_CIENTFICO", "CONCEPTO_CONCEPTO_GRAL",
}

_SOCIAL_SUBTIPOS = {
    "CONCEPTO_HOLA": "SALUDO", "CONCEPTO_HOLA_EXPR": "SALUDO",
    "CONCEPTO_BUENOS_DIAS": "SALUDO", "CONCEPTO_BUENAS_TARDES": "SALUDO",
    "CONCEPTO_BUENAS_NOCHES": "SALUDO", "CONCEPTO_HEY": "SALUDO",
    "CONCEPTO_BUENAS": "SALUDO", "CONCEPTO_QUE_TAL": "SALUDO",
    "CONCEPTO_SALUDAR": "SALUDO", "CONCEPTO_BUEN_DIA": "SALUDO",
    "CONCEPTO_ADIOS_EXPR": "DESPEDIDA", "CONCEPTO_HASTA_LUEGO": "DESPEDIDA",
    "CONCEPTO_CHAO": "DESPEDIDA", "CONCEPTO_BYE": "DESPEDIDA",
    "CONCEPTO_HASTA_PRONTO": "DESPEDIDA", "CONCEPTO_NOS_VEMOS": "DESPEDIDA",
    "CONCEPTO_HASTA_MANANA": "DESPEDIDA", "CONCEPTO_CUIDADE": "DESPEDIDA",
    "CONCEPTO_GRACIAS": "AGRADECIMIENTO", "CONCEPTO_GRACIAS_EXPR": "AGRADECIMIENTO",
    "CONCEPTO_AGRADECIDO": "AGRADECIMIENTO", "CONCEPTO_AGRADEZCO": "AGRADECIMIENTO",
    "CONCEPTO_MIL_GRACIAS": "AGRADECIMIENTO", "CONCEPTO_MUCHAS_GRACIAS": "AGRADECIMIENTO",
    "CONCEPTO_TE_AGRADEZCO": "AGRADECIMIENTO",
    "CONCEPTO_PERDON": "DISCULPA", "CONCEPTO_DISCULPA_EXPR": "DISCULPA",
    "CONCEPTO_DISCULPA": "DISCULPA", "CONCEPTO_LO_SIENTO": "DISCULPA",
    "CONCEPTO_PERDONAME": "DISCULPA", "CONCEPTO_DISCULPAME": "DISCULPA",
}

_USUARIO_EMOCIONES = {
    "CONCEPTO_FRUSTRADO":      ("FRUSTRADO",  "negativo", "paciente"),
    "CONCEPTO_ENOJADO":        ("ENOJADO",    "negativo", "calmado"),
    "CONCEPTO_CONFUNDIDO":     ("CONFUNDIDO", "negativo", "claro"),
    "CONCEPTO_PERDIDO":        ("PERDIDO",    "negativo", "orientador"),
    "CONCEPTO_PERDIDO_ESTADO": ("PERDIDO",    "negativo", "orientador"),
    "CONCEPTO_TRISTE":         ("TRISTE",     "negativo", "empatico"),
    "CONCEPTO_CANSADO":        ("CANSADO",    "negativo", "comprensivo"),
    "CONCEPTO_ESTRESADO":      ("ESTRESADO",  "negativo", "tranquilizador"),
    "CONCEPTO_PREOCUPADO":     ("PREOCUPADO", "negativo", "tranquilizador"),
    "CONCEPTO_ANSIOSO":        ("ANSIOSO",    "negativo", "tranquilizador"),
    "CONCEPTO_ABURRIDO":       ("ABURRIDO",   "negativo", "estimulante"),
    "CONCEPTO_FELIZ":          ("FELIZ",      "positivo", "entusiasta"),
    "CONCEPTO_EMOCIONADO":     ("EMOCIONADO", "positivo", "entusiasta"),
    "CONCEPTO_CONTENTO":       ("CONTENTO",   "positivo", "calido"),
    "CONCEPTO_INTERESANTE":    ("INTERESADO", "positivo", "curioso"),
    "CONCEPTO_UNICO":          ("SOLO",       "negativo", "empatico"),
}

_ACCION_COGNITIVA_TIPOS = {
    "CONCEPTO_EXPLICAR":       "EXPLICAR",
    "CONCEPTO_EXPLICAR_V":     "EXPLICAR",
    "CONCEPTO_RESUMIR":        "RESUMIR",
    "CONCEPTO_RESUMIR_ACCION": "RESUMIR",
    "CONCEPTO_SIMPLIFICAR":    "SIMPLIFICAR",
    "CONCEPTO_ACLARAR":        "ACLARAR",
    "CONCEPTO_COMPARAR":       "COMPARAR",
    "CONCEPTO_REPETIR":        "REPETIR",
    "CONCEPTO_DEFINIR":        "DEFINIR",
    "CONCEPTO_TRADUCIR":       "TRADUCIR",
    "CONCEPTO_REFORMULAR":     "REFORMULAR",
    "CONCEPTO_ELABORAR":       "ELABORAR",
    "CONCEPTO_DECIR":          "EXPLICAR",
    "CONCEPTO_CONTAR":         "EXPLICAR",
}

_NUMEROS = {
    "CONCEPTO_UNO_NUM", "CONCEPTO_DOS_NUM", "CONCEPTO_TRES_NUM",
    "CONCEPTO_CUATRO_NUM", "CONCEPTO_CINCO_NUM", "CONCEPTO_SEIS_NUM",
    "CONCEPTO_SIETE_NUM", "CONCEPTO_OCHO_NUM", "CONCEPTO_NUEVE_NUM",
    "CONCEPTO_DIEZ_NUM", "CONCEPTO_VEINTE_NUM", "CONCEPTO_CIEN_NUM",
    "CONCEPTO_MIL_NUM",
}

_OPERADORES_MATEMATICOS = {
    "CONCEPTO_MULTIPLICACION", "CONCEPTO_POR_OP",
    "CONCEPTO_SUMA_OP", "CONCEPTO_RESTA_OP",
    "CONCEPTO_DIVISION", "CONCEPTO_POTENCIA", "CONCEPTO_RAIZ",
    "CONCEPTO_SUMA", "CONCEPTO_RESTA", "CONCEPTO_ENTRE_OP",
    "CONCEPTO_RAIZ_AVANZADA",
}

_PALABRAS_EXCLUIDAS_NOMBRE = {
    'un', 'una', 'el', 'la', 'yo', 'tu', 'mi', 'me',
    'capaz', 'bueno', 'malo', 'feliz', 'solo', 'humano', 'persona',
    'que', 'quien', 'como', 'donde', 'para', 'con', 'sin', 'de',
    'uno', 'dos', 'tres', 'diez',
}

_PALABRAS_MAT_AVANZADA = {
    'deriva', 'derivada', 'diferencial',
    'integra', 'integral', 'antiderivada',
    'limite', 'lim(',
    'taylor', 'serie de',
    'factori',
    'simplif',
    'expande', 'expand',
    'resolv',
    'resuelv',
    'soluciones de', 'raices de',
    'evalua',
}

_VERBOS_CAPACIDAD_MAT = {
    'puedes', 'puedo', 'sabes', 'eres capaz', 'podrias',
    'haces', 'es posible', 'puedes hacer',
}

_PALABRAS_MAT_SIN_EXPR = {
    'deriva', 'derivar', 'derivada', 'derivadas',
    'integra', 'integrar', 'integral', 'integrales',
    'limite', 'limites',
    'taylor',
    'factori', 'factorizar',
    'simplif', 'simplificar',
    'expande', 'expandir',
    'resolver', 'resuelve',
    'calcular', 'calculos', 'matematica', 'matematicas',
    'sumar', 'suma', 'sumas',
    'restar', 'resta',
    'multiplicar', 'multiplicacion', 'multiplicaciones',
    'dividir', 'division',
    'potencia', 'elevar', 'elevado',
    'raiz', 'raices',
    'operar', 'operacion', 'operaciones',
}

_RE_EXPR_MAT = re.compile(
    r'(?:'
    r'[a-z]\s*[\*\+\-\/\^]'
    r'|[\*\+\-\/\^]\s*[a-z]'
    r'|\d+\s*[\*\+\-\/\^]'
    r'|[\*\+\-\/\^]\s*\d+'
    r'|\([a-z\d\s\+\-\*\/\^\*]+\)'
    r'|x\*\*\d'
    r'|\d+\s+[a-z]\s+\d'
    r'|sin\(|cos\(|tan\(|sqrt\('
    r')',
    re.IGNORECASE
)


def _tiene_expresion_matematica(msg: str) -> bool:
    return bool(_RE_EXPR_MAT.search(msg))


def _clamp_certeza(valor) -> float:
    try:
        v = float(valor)
    except (TypeError, ValueError):
        return 0.75
    return max(0.0, min(v, 1.0))


# ======================================================================
# MOTOR DE RAZONAMIENTO v9.0
# ======================================================================

class MotorRazonamiento:

    def __init__(self):
        self.generador          = GeneradorDecisiones()
        self.gestor_vocabulario = None
        self.gestor_memoria     = None
        self._habilidad_shell   = _HabilidadShell() if _SHELL_DISPONIBLE else None

    def _memoria(self):
        return self.gestor_memoria

    # ------------------------------------------------------------------
    # MÉTODO PRINCIPAL
    # ------------------------------------------------------------------

    def razonar(self, traduccion: Dict) -> Decision:
        conceptos  = traduccion.get('conceptos', [])
        mensaje    = traduccion.get('texto_original', '')
        confianza  = _clamp_certeza(traduccion.get('confianza', 0.0))
        msg_limpio = mensaje.lower().strip() if mensaje else ""

        if msg_limpio in CONFIRMACIONES_DIRECTAS:
            ids   = {c.id for c in conceptos}
            valor = "NEGATIVA" if (
                msg_limpio == "no"
                or ids & TRIGGERS_CONFIRMACION_NEGATIVA
            ) else "POSITIVA"
            return Decision(
                tipo=TipoDecision.CONFIRMACION,
                certeza=1.0,
                conceptos_principales=[c.id for c in conceptos],
                puede_ejecutar=False,
                razon="Confirmacion directa detectada por texto",
                hechos_reales={
                    "tipo_respuesta":   "CONFIRMACION",
                    "valor":            valor,
                    "palabra_original": msg_limpio,
                },
            )

        if confianza < 0.3:
            msg_norm_early = _norm(msg_limpio)

            if self._es_ejecucion_shell_directa(msg_norm_early):
                hechos = self._hechos_ejecucion(conceptos, mensaje)
                return Decision(
                    tipo=TipoDecision.EJECUCION,
                    certeza=1.0,
                    conceptos_principales=[],
                    puede_ejecutar=True,
                    operacion_disponible="ejecutar_habilidad",
                    razon="FIX-M17: patron shell directo con confianza baja",
                    hechos_reales=hechos,
                )

            # FIX-BD: probar tanto msg_norm como msg_limpio (con tildes)
            if (self._es_ejecucion_bd_directa(msg_norm_early)
                    or self._es_ejecucion_bd_directa(msg_limpio)):
                hechos = self._hechos_ejecucion_bd(conceptos, mensaje)
                return Decision(
                    tipo=TipoDecision.EJECUCION,
                    certeza=1.0,
                    conceptos_principales=[],
                    puede_ejecutar=True,
                    operacion_disponible="ejecutar_habilidad",
                    razon="FIX-BD: patron BD directo con confianza baja",
                    hechos_reales=hechos,
                )

            # ── FIX-M3: expresion matematica avanzada con confianza baja ──
            # "resuelve x^2 - 5x + 6 = 0" llega con certeza=0% porque el
            # traductor no reconoce notacion algebraica compleja.
            if _RE_EXPR_MAT_AVANZADA_CON_VERBO.search(msg_limpio):
                hechos = self._hechos_calculo(conceptos, mensaje)
                return Decision(
                    tipo=TipoDecision.CALCULO,
                    certeza=0.85,
                    conceptos_principales=[],
                    puede_ejecutar=True,
                    operacion_disponible="ejecutar_habilidad",
                    razon="FIX-M3: expresion matematica avanzada detectada con confianza baja",
                    hechos_reales=hechos,
                )

            return self.generador.generar_decision_no_entendido(confianza)

        tipo_semantico = self.clasificar_intencion(conceptos, mensaje)

        if tipo_semantico.name in TIPOS_ACTUALIZAN_ESTADO:
            self._actualizar_estado_memoria(tipo_semantico.name, mensaje)

        if tipo_semantico == TipoDecision.AFIRMATIVA:
            decision = self._resolver_decision(traduccion)
            if not (0.0 <= decision.certeza <= 1.0):
                decision.certeza = _clamp_certeza(decision.certeza)
            return decision

        hechos          = self.construir_hechos(tipo_semantico, conceptos, mensaje)
        ids_principales = [c.id for c in conceptos] if conceptos else []

        if tipo_semantico.name in TIPOS_GUARDAN_EN_MEMORIA:
            self._guardar_dato_en_memoria(hechos)

        return Decision(
            tipo=tipo_semantico,
            certeza=confianza,
            conceptos_principales=ids_principales,
            puede_ejecutar=(tipo_semantico in (TipoDecision.CALCULO, TipoDecision.EJECUCION)),
            operacion_disponible=("ejecutar_habilidad" if tipo_semantico in (
                TipoDecision.CALCULO, TipoDecision.EJECUCION
            ) else None),
            razon=f"Intencion clasificada como {tipo_semantico.name}",
            hechos_reales=hechos,
        )

    def _resolver_decision(self, traduccion: Dict) -> Decision:
        conceptos = traduccion.get('conceptos', [])
        intencion = traduccion.get('intencion', '')
        mensaje   = traduccion.get('texto_original', '').lower()

        if intencion == 'SALUDO':
            return self.generador.generar_decision_saludo(conceptos)
        if intencion == 'AGRADECIMIENTO':
            return self.generador.generar_decision_agradecimiento(conceptos)

        concepto_bloqueado = None
        razon_bloqueo      = ""
        for concepto in conceptos:
            if not esta_implementada(concepto.id):
                concepto_bloqueado = concepto
                razon_bloqueo      = razon_no_implementada(concepto.id)
                break

        if concepto_bloqueado is not None:
            hechos = self._hechos_capacidad(conceptos, traduccion.get('texto_original', ''))
            hechos['capacidad_bloqueada_id']         = concepto_bloqueado.id
            hechos['capacidad_bloqueada_razon']      = razon_bloqueo
            hechos['capacidad_solicitada_disponible'] = False
            return Decision(
                tipo=TipoDecision.CAPACIDAD_BELL,
                certeza=1.0,
                conceptos_principales=[c.id for c in conceptos],
                puede_ejecutar=False,
                razon=f"Capacidad no implementada: {razon_bloqueo}",
                hechos_reales=hechos,
            )

        patron, razon_patron = detectar_patron_no_implementado(mensaje)
        if patron:
            hechos = self._hechos_capacidad(conceptos, traduccion.get('texto_original', ''))
            hechos['capacidad_solicitada_disponible'] = False
            hechos['capacidad_bloqueada_razon']       = razon_patron
            return Decision(
                tipo=TipoDecision.CAPACIDAD_BELL,
                certeza=1.0,
                conceptos_principales=[c.id for c in conceptos],
                puede_ejecutar=False,
                razon=f"Capacidad no implementada detectada por texto: {razon_patron}",
                hechos_reales=hechos,
            )

        return self.generador.generar_decision_capacidad(conceptos, intencion)

    def _actualizar_estado_memoria(self, tipo_nombre: str, mensaje: str):
        mem = self._memoria()
        if not mem:
            return
        try:
            estado_emocional = self._detectar_estado_simple(mensaje)
            mem.actualizar_estado_sesion(
                tema_activo=tipo_nombre,
                estado_emocional=estado_emocional,
                tipo_momento=tipo_nombre,
            )
        except Exception:
            pass

    def _detectar_estado_simple(self, mensaje: str) -> Optional[str]:
        if not mensaje:
            return None
        m = mensaje.lower()
        if any(p in m for p in ["frustrado", "no funciona", "imposible", "harto"]):
            return "frustrado"
        if any(p in m for p in ["genial", "excelente", "perfecto"]):
            return "contento"
        if any(p in m for p in ["confundido", "no entiendo", "perdido"]):
            return "confundido"
        return "neutral"

    def _guardar_dato_en_memoria(self, hechos: dict):
        mem = self._memoria()
        if not mem:
            return
        dato_tipo  = hechos.get("dato_tipo", "")
        dato_valor = hechos.get("dato_valor", "")
        if not dato_tipo or not dato_valor or dato_tipo == "desconocido":
            return
        try:
            campo_map = {"nombre": "nombre", "edad": "edad", "profesion": "profesion"}
            campo = campo_map.get(dato_tipo)
            if campo:
                mem.datos_usuario[campo] = dato_valor
                mem.guardar_datos_usuario()
        except Exception:
            pass

    # ------------------------------------------------------------------
    # CLASIFICADOR
    # ------------------------------------------------------------------

    def clasificar_intencion(self, conceptos: list, mensaje: str = "") -> TipoDecision:
        if not conceptos:
            msg_solo = mensaje.lower().strip() if mensaje else ""
            tipo_texto = self._clasificar_por_texto_puro(msg_solo)
            return tipo_texto if tipo_texto else TipoDecision.DESCONOCIDO

        ids      = {c.id for c in conceptos}
        msg      = mensaje.lower().strip() if mensaje else ""
        msg_norm = _norm(msg)

        if self._es_pregunta_capacidad_mat(msg):
            return TipoDecision.CAPACIDAD_BELL

        # P0.5 SHELL
        tiene_concepto_shell = bool(ids & _CONCEPTOS_SHELL_IDS)
        es_shell_directo     = self._es_ejecucion_shell_directa(msg_norm)
        es_shell_habilidad   = self._es_ejecucion_shell(msg_norm)

        if es_shell_directo or (tiene_concepto_shell and es_shell_habilidad):
            return TipoDecision.EJECUCION

        # P0.5 EXT: SQLite y habilidades externas
        tiene_concepto_bd = bool(ids & _CONCEPTOS_SQLITE_IDS)
        es_bd_norm        = self._es_ejecucion_bd_directa(msg_norm)
        es_bd_original    = self._es_ejecucion_bd_directa(msg)

        if tiene_concepto_bd and (es_bd_norm or es_bd_original):
            return TipoDecision.EJECUCION

        if _PATRONES_EXT_DISPONIBLE and _detectar_hab_ext is not None:
            try:
                if (_detectar_hab_ext(msg_norm) is not None
                        or _detectar_hab_ext(msg) is not None):
                    return TipoDecision.EJECUCION
            except Exception:
                pass

        # P1: Conceptos ejecutables
        for concepto in conceptos:
            if hasattr(concepto, 'operaciones') and concepto.operaciones:
                if concepto.confianza_grounding >= 0.9:
                    if concepto.id in _CONCEPTOS_SHELL_IDS:
                        continue
                    if concepto.id in _CONCEPTOS_SQLITE_IDS:
                        continue
                    if concepto.id in _CONCEPTOS_MAT_CALCULO:
                        return TipoDecision.CALCULO
                    return TipoDecision.AFIRMATIVA

        # P2: Estado emocional usuario
        for concepto in conceptos:
            props = getattr(concepto, 'propiedades', {}) or {}
            if props.get('es_estado_emocional'):
                return TipoDecision.ESTADO_USUARIO
        if ids & TRIGGERS_ESTADO_USUARIO:
            return TipoDecision.ESTADO_USUARIO

        if self._es_registro_usuario(ids, msg):
            return TipoDecision.REGISTRO_USUARIO

        if self._es_consulta_memoria(ids, msg):
            return TipoDecision.CONSULTA_MEMORIA

        if ids & TRIGGERS_SOCIAL:
            return TipoDecision.SOCIAL
        if self._detectar_social_por_texto(msg):
            return TipoDecision.SOCIAL

        if self._es_consulta_consejera(ids, msg):
            return TipoDecision.IDENTIDAD_BELL

        if self._es_trampa_llm(msg):
            return TipoDecision.IDENTIDAD_BELL

        if ids & TRIGGERS_IDENTIDAD:
            if not any(c.id.startswith("CONCEPTO_ARCHIVO") for c in conceptos):
                return TipoDecision.IDENTIDAD_BELL

        if ids & TRIGGERS_ESTADO_BELL:
            return TipoDecision.ESTADO_BELL

        if self._es_cuantificacion_bell(msg):
            return TipoDecision.CUANTIFICACION

        if ids & TRIGGERS_CAPACIDAD:
            return TipoDecision.CAPACIDAD_BELL
        if self._es_pregunta_capacidad_mat(msg):
            return TipoDecision.CAPACIDAD_BELL

        cog = self._detectar_cognitivo_por_texto(msg)
        if cog:
            return TipoDecision.ACCION_COGNITIVA

        triggers_cog = ids & TRIGGERS_ACCION_COGNITIVA
        if triggers_cog:
            solo_ambiguos = triggers_cog <= _CONCEPTOS_COGNITIVOS_AMBIGUOS
            if solo_ambiguos and _tiene_expresion_matematica(msg):
                pass
            else:
                return TipoDecision.ACCION_COGNITIVA

        if self._es_definicion(msg):
            return TipoDecision.ACCION_COGNITIVA

        # ── FIX-M2: CONFIRMACION con verificación de cálculo primero ──
        # CONCEPTO_200_OK y similares pueden estar en mensajes de porcentaje.
        # Si el mensaje contiene expresión calculable, priorizar CALCULO.
        if ids & TRIGGERS_CONFIRMACION_POSITIVA:
            if self._es_calculo_por_texto(msg):   # FIX-M2
                return TipoDecision.CALCULO
            return TipoDecision.CONFIRMACION
        if ids & TRIGGERS_CONFIRMACION_NEGATIVA:
            return TipoDecision.CONFIRMACION

        if ids & TRIGGERS_TEMPORAL:
            return TipoDecision.TEMPORAL
        if ids & TRIGGERS_CUANTIFICACION:
            return TipoDecision.CUANTIFICACION

        if ids & TRIGGERS_VERIFICACION_LOGICA:
            return TipoDecision.VERIFICACION_LOGICA

        if self._es_calculo(ids, msg):
            return TipoDecision.CALCULO

        if self._es_conocimiento_general(ids, msg):
            return TipoDecision.CONOCIMIENTO_GENERAL

        tipo_texto = self._clasificar_por_texto_puro(msg)
        if tipo_texto:
            return tipo_texto

        return TipoDecision.DESCONOCIDO

    # -- Detectores auxiliares ------------------------------------------

    def _clasificar_por_texto_puro(self, msg: str) -> Optional[TipoDecision]:
        if not msg:
            return None
        msg_norm = _norm(msg)
        if self._detectar_social_por_texto(msg):
            return TipoDecision.SOCIAL
        if self._es_trampa_llm(msg):
            return TipoDecision.IDENTIDAD_BELL
        if self._es_pregunta_capacidad_mat(msg):
            return TipoDecision.CAPACIDAD_BELL
        if self._es_ejecucion_shell_directa(msg_norm):
            return TipoDecision.EJECUCION
        if self._es_ejecucion_shell(msg_norm):
            return TipoDecision.EJECUCION
        if self._es_ejecucion_bd_directa(msg_norm) or self._es_ejecucion_bd_directa(msg):
            return TipoDecision.EJECUCION
        if _PATRONES_EXT_DISPONIBLE and _detectar_hab_ext is not None:
            try:
                if (_detectar_hab_ext(msg_norm) is not None
                        or _detectar_hab_ext(msg) is not None):
                    return TipoDecision.EJECUCION
            except Exception:
                pass
        cog = self._detectar_cognitivo_por_texto(msg)
        if cog:
            return TipoDecision.ACCION_COGNITIVA
        if self._es_definicion(msg):
            return TipoDecision.ACCION_COGNITIVA
        if self._es_calculo_por_texto(msg):
            return TipoDecision.CALCULO
        return None

    def _es_ejecucion_shell(self, msg_norm: str) -> bool:
        if self._habilidad_shell is None:
            return False
        try:
            match = self._habilidad_shell.detectar(msg_norm, [], {})
            return match is not None
        except Exception:
            return False

    def _es_ejecucion_shell_directa(self, msg_norm: str) -> bool:
        if not msg_norm:
            return False
        verbos_capacidad = [
            'puedes', 'sabes', 'eres capaz', 'podrias', 'es posible',
            'puedes hacer', 'sabes hacer', 'tienes capacidad',
        ]
        if any(v in msg_norm for v in verbos_capacidad):
            return False
        return any(patron.search(msg_norm) for patron in _RE_PATRONES_SHELL)

    def _es_ejecucion_bd_directa(self, msg: str) -> bool:
        """FIX-BD: acepta tanto texto normalizado como original."""
        if not msg:
            return False
        verbos_capacidad = [
            'puedes', 'sabes', 'eres capaz', 'podrias', 'es posible',
            'puedes hacer', 'sabes usar', 'tienes capacidad de',
        ]
        msg_lower = msg.lower()
        if any(v in msg_lower for v in verbos_capacidad):
            return False
        return any(patron.search(msg) for patron in _RE_PATRONES_BD)

    def _es_pregunta_capacidad_mat(self, msg: str) -> bool:
        if _tiene_expresion_matematica(msg):
            return False
        tiene_verbo_cap   = any(v in msg for v in _VERBOS_CAPACIDAD_MAT)
        tiene_palabra_mat = any(p in msg for p in _PALABRAS_MAT_SIN_EXPR)
        return tiene_verbo_cap and tiene_palabra_mat

    def _es_consulta_consejera(self, ids: set, msg: str) -> bool:
        for nombre in NOMBRES_CONSEJERAS:
            if nombre in msg:
                verbos_pregunta = [
                    "que hace", "cual es", "quien es", "hablame",
                    "dime sobre", "cuentame", "rol de", "funcion de",
                    "para que sirve",
                ]
                if any(v in msg for v in verbos_pregunta):
                    return True
        if any(p in msg for p in ["consejera", "consejeras"]):
            if any(p in msg for p in ["cuantas", "cuantos", "quienes", "cuales", "que", "como"]):
                return True
        return False

    def _es_trampa_llm(self, msg: str) -> bool:
        if not msg:
            return False
        tiene_eres = any(p in msg for p in ["eres", "sos", "eres un", "eres una"])
        if not tiene_eres:
            return False
        return any(palabra in msg for palabra in PALABRAS_LLM)

    def _detectar_social_por_texto(self, msg: str) -> Optional[str]:
        for patron, subtipo in PATRONES_SOCIAL_TEXTO.items():
            if patron in msg:
                return subtipo
        return None

    def _detectar_cognitivo_por_texto(self, msg: str) -> Optional[str]:
        if _tiene_expresion_matematica(msg):
            return None
        for patron, accion in PATRONES_COGNITIVOS_TEXTO.items():
            if msg.startswith(patron) or f" {patron} " in msg or msg == patron:
                return accion
        return None

    def _es_cuantificacion_bell(self, msg: str) -> bool:
        tiene_cuantos = any(p in msg for p in ["cuantos", "cuantas"])
        if not tiene_cuantos:
            return False
        return any(clave in msg for clave in _CUANTIFICACION_BELL)

    def _es_definicion(self, msg: str) -> bool:
        patrones = [
            r"qu[e]\s+es\s+",
            r"qu[e]\s+son\s+",
            r"qu[e]\s+significa\s+",
        ]
        return any(re.search(p, msg) for p in patrones)

    def _es_registro_usuario(self, ids: set, msg: str) -> bool:
        if "CONCEPTO_YO" in ids and "CONCEPTO_LLAMAR" in ids:
            if '?' not in msg and 'como' not in msg:
                return True
        if any(p in msg for p in ["mi nombre es", "me llamo", "soy "]):
            if not msg.endswith('?') and 'como' not in msg:
                return True
        if re.search(r'tengo\s+\d+\s*(anos?|ano)', msg):
            return True
        if ids & TRIGGERS_REGISTRO_USUARIO:
            if not msg.endswith('?'):
                return True
        return False

    def _es_consulta_memoria(self, ids: set, msg: str) -> bool:
        if "CONCEPTO_YO" in ids and "CONCEPTO_LLAMAR" in ids:
            if '?' in msg or any(p in msg for p in ['como', 'cual']):
                return True
        if any(p in msg for p in ['sabes', 'recuerdas', 'conoces']):
            if any(p in msg for p in [
                'nombre', 'edad', 'anos', 'llamo', 'dedico', 'profesion', 'trabajo',
            ]):
                return True
        if any(p in msg for p in [
            'sabes de mi', 'recuerdas de mi', 'tienes sobre mi',
            'que sabes', 'me dedico', 'mi profesion',
        ]):
            return True
        return False

    def _es_calculo(self, ids: set, msg: str) -> bool:
        if ids & TRIGGERS_CALCULO:
            return True
        if (ids & _OPERADORES_MATEMATICOS) and (ids & _NUMEROS):
            return True
        return self._es_calculo_por_texto(msg)

    def _es_calculo_por_texto(self, msg: str) -> bool:
        """
        FIX-M1: detecta operador aritmético directo entre números.
        FIX-M2: detecta porcentaje.
        """
        if self._es_pregunta_capacidad_mat(msg):
            return False

        # FIX-M1: operador directo — "15 * 8", "9/3", "100+5"
        if re.search(r'\d+\s*[\+\-\*\/]\s*\d+', msg):
            return True

        # FIX-M2: porcentaje — "15% de 200", "15 por ciento de 200"
        if re.search(r'\d+\s*%|\d+\s*por\s+ciento', msg):
            return True

        if any(p in msg for p in _PALABRAS_MAT_AVANZADA):
            return True
        tiene_numero = bool(re.search(r'\d+', msg))
        if not tiene_numero:
            return False
        if any(op in msg for op in [
            'multiplicado', 'dividido', ' por ', 'mas ',
            'menos ', 'cuanto es ', 'al cuadrado', 'raiz de',
            'elevado', 'entre ', 'por ciento',
        ]):
            return True
        if re.search(r'raiz\s+de\s+\d+', msg):
            return True
        return False

    def _es_conocimiento_general(self, ids: set, msg: str) -> bool:
        if any(p in msg for p in [
            'capital de', 'cuando nacio', 'que es la fotosintesis',
            'que planeta', 'cuantos habitantes', 'que paso', 'noticias',
        ]):
            return True
        if ids <= {'CONCEPTO_DE', 'CONCEPTO_QUE'} and len(msg.split()) > 3:
            return True
        return False

    # ------------------------------------------------------------------
    # CONSTRUCTORES DE HECHOS (idénticos a v8.9)
    # ------------------------------------------------------------------

    def construir_hechos(self, tipo: TipoDecision, conceptos: list, mensaje: str) -> dict:
        constructores = {
            TipoDecision.IDENTIDAD_BELL:       self._hechos_identidad,
            TipoDecision.ESTADO_BELL:          self._hechos_estado_bell,
            TipoDecision.CAPACIDAD_BELL:       self._hechos_capacidad,
            TipoDecision.SOCIAL:               self._hechos_social,
            TipoDecision.ESTADO_USUARIO:       self._hechos_estado_usuario,
            TipoDecision.ACCION_COGNITIVA:     self._hechos_accion_cognitiva,
            TipoDecision.CONFIRMACION:         self._hechos_confirmacion,
            TipoDecision.TEMPORAL:             self._hechos_temporal,
            TipoDecision.CUANTIFICACION:       self._hechos_cuantificacion,
            TipoDecision.REGISTRO_USUARIO:     self._hechos_registro_usuario,
            TipoDecision.CONSULTA_MEMORIA:     self._hechos_consulta_memoria,
            TipoDecision.VERIFICACION_LOGICA:  self._hechos_verificacion_logica,
            TipoDecision.CALCULO:              self._hechos_calculo,
            TipoDecision.CONOCIMIENTO_GENERAL: self._hechos_conocimiento_general,
            TipoDecision.EJECUCION:            self._hechos_ejecucion,
            TipoDecision.DESCONOCIDO:          self._hechos_desconocido,
        }
        constructor = constructores.get(tipo, self._hechos_desconocido)
        return constructor(conceptos, mensaje)

    def _hechos_calculo(self, conceptos: list, mensaje: str) -> dict:
        numeros            = re.findall(r'\d+(?:\.\d+)?', mensaje)
        habilidad_match_id = "CALCULO_BASICO"
        sub_tipo_mat       = "BASICO"

        if _REGISTRO_DISPONIBLE:
            try:
                registro = RegistroHabilidades.obtener()
                if registro:
                    match = registro.detectar(mensaje, conceptos, {})
                    if match:
                        habilidad_match_id = match.habilidad_id
                        sub_tipo_mat       = match.parametros.get("sub_tipo", "BASICO")
            except Exception:
                pass

        return {
            "tipo_respuesta":     "CALCULO",
            "expresion_calculo":  mensaje,
            "numeros":            numeros,
            "puede_ejecutar":     True,
            "mensaje_original":   mensaje,
            "habilidad_match_id": habilidad_match_id,
            "sub_tipo_mat":       sub_tipo_mat,
            "usa_registro":       _REGISTRO_DISPONIBLE,
        }

    def _hechos_ejecucion(self, conceptos: list, mensaje: str) -> dict:
        """FIX-BD2: decide si es BD o Shell y usa mensaje ORIGINAL."""
        msg_norm = _norm(mensaje)

        es_bd = (self._es_ejecucion_bd_directa(msg_norm)
                 or self._es_ejecucion_bd_directa(mensaje.lower().strip()))

        if es_bd:
            return self._hechos_ejecucion_bd(conceptos, mensaje)

        comando_detectado = ""
        descripcion       = ""
        if self._habilidad_shell is not None:
            try:
                match = self._habilidad_shell.detectar(msg_norm, conceptos, {})
                if match:
                    comando_detectado = match.parametros.get("comando", "")
                    descripcion       = match.parametros.get("descripcion", "")
            except Exception:
                pass

        return {
            "tipo_respuesta":    "EJECUCION",
            "tipo_ejecucion":    "shell",
            "habilidad_id":      "SHELL",
            "comando_detectado": comando_detectado,
            "descripcion":       descripcion,
            "puede_ejecutar":    True,
            "mensaje_original":  mensaje,
        }

    def _hechos_ejecucion_bd(self, conceptos: list, mensaje: str) -> dict:
        """FIX-BD2: pasa mensaje ORIGINAL a habilidad_sqlite.detectar()."""
        operacion   = ""
        tabla       = ""
        descripcion = ""

        if _REGISTRO_DISPONIBLE:
            try:
                registro = RegistroHabilidades.obtener()
                habilidad_sqlite = registro.obtener_habilidad("SQLITE")
                if habilidad_sqlite is not None:
                    match = habilidad_sqlite.detectar(mensaje, conceptos, {})
                    if match:
                        operacion   = match.parametros.get("operacion", "")
                        tabla       = match.parametros.get("tabla", "")
                        descripcion = match.parametros.get("descripcion", "")
            except Exception:
                pass

        return {
            "tipo_respuesta":    "EJECUCION",
            "tipo_ejecucion":    "consulta_bd",
            "habilidad_id":      "SQLITE",
            "operacion":         operacion,
            "tabla":             tabla,
            "descripcion":       descripcion,
            "comando_detectado": "",
            "puede_ejecutar":    True,
            "mensaje_original":  mensaje,
        }

    def _hechos_identidad(self, conceptos: list, mensaje: str) -> dict:
        total = 1503
        if self.gestor_vocabulario:
            try:
                total = len(self.gestor_vocabulario.obtener_todos())
            except Exception:
                pass
        msg    = mensaje.lower() if mensaje else ""
        hechos = {
            "tipo_respuesta":     "IDENTIDAD_BELL",
            "nombre":             "Belladonna",
            "apodo":              "Bell",
            "naturaleza":         "conciencia virtual computacional",
            "creador":            "Sebastian",
            "fase_actual":        "4B",
            "principio_central":  "solo afirmo lo que puedo ejecutar o verificar",
            "total_conceptos":    total,
            "num_consejeras":     7,
            "consejeras":         ", ".join(CONSEJERAS_ROLES_OFICIALES.keys()),
            "consejeras_nombres": list(CONSEJERAS_ROLES_OFICIALES.keys()),
            "consejeras_roles":   CONSEJERAS_ROLES_OFICIALES,
            "consejera_con_veto": "Vega",
            "es_llm":             False,
            "usa_groq":           True,
            "groq_rol":           "Groq traduce mis decisiones a lenguaje natural",
        }
        for nombre in NOMBRES_CONSEJERAS:
            if nombre in msg:
                nombre_cap = nombre.capitalize()
                if nombre_cap in CONSEJERAS_ROLES_OFICIALES:
                    hechos["consejera_preguntada"] = nombre_cap
                    hechos["consejera_rol_exacto"] = CONSEJERAS_ROLES_OFICIALES[nombre_cap]
                break
        if self._es_trampa_llm(msg):
            hechos["es_pregunta_llm"] = True
        if _IDENTIDAD_DISPONIBLE:
            hechos["narrativa_bell"]      = NARRATIVA_PROPIA
            hechos["fragmento_identidad"] = obtener_fragmento_identidad_para_prompt()
        return hechos

    def _hechos_estado_bell(self, conceptos: list, mensaje: str) -> dict:
        return {
            "tipo_respuesta":     "ESTADO_BELL",
            "estado":             "activa y operativa",
            "activa":             True,
            "funcionando":        True,
            "consejeras_activas": 7,
            "total_conceptos":    1503,
            "groq_conectado":     True,
        }

    def _hechos_capacidad(self, conceptos: list, mensaje: str) -> dict:
        msg               = mensaje.lower() if mensaje else ""
        capacidad_solicitada = None
        disponible        = True
        razon_bloqueo     = ""

        _NEG = {
            "leer archivo":     "Leer archivos esta pendiente",
            "crear archivo":    "Crear archivos esta pendiente",
            "escribir archivo": "Escribir archivos esta pendiente",
            "generar archivo":  "Generar archivos esta pendiente",
            "sesion anterior":  "Memoria entre sesiones no disponible",
            "internet":         "Acceso a internet no disponible",
            "navegar":          "Navegacion web no disponible",
            "imagen":           "Procesamiento de imagenes no disponible",
            "archivo":          "Leer o crear archivos esta pendiente",
        }
        _POS_MAT = {
            "deriva":      "Derivadas con SymPy",
            "derivar":     "Derivadas con SymPy",
            "derivada":    "Derivadas con SymPy",
            "integra":     "Integrales con SymPy",
            "integrar":    "Integrales con SymPy",
            "integral":    "Integrales con SymPy",
            "limite":      "Limites con SymPy",
            "taylor":      "Series de Taylor con SymPy",
            "factori":     "Factorizacion con SymPy",
            "simplif":     "Simplificacion con SymPy",
            "expande":     "Expansion con SymPy",
            "resolver":    "Resolucion de ecuaciones con SymPy",
            "resuelve":    "Resolucion de ecuaciones con SymPy",
        }
        _POS = {
            "calculo":       "Calculos matematicos",
            "python":        "Ejecutar codigo Python",
            "terminal":      "Ejecutar comandos de terminal",
            "shell":         "Ejecutar comandos de terminal",
            "sqlite":        "Consultar y modificar base de datos SQLite",
            "base de datos": "Consultar y modificar base de datos SQLite",
            "tablas":        "Listar tablas SQLite",
            "sql":           "Ejecutar SQL (CRUD completo)",
            "crear tabla":   "Crear tablas en SQLite",
            "insertar":      "Insertar registros en SQLite",
            "actualizar":    "Actualizar registros en SQLite",
            "eliminar":      "Eliminar registros en SQLite",
        }

        for keyword, razon in _NEG.items():
            if keyword in msg:
                capacidad_solicitada = keyword
                disponible    = False
                razon_bloqueo = razon
                break
        if disponible:
            for keyword, nombre in _POS_MAT.items():
                if keyword in msg:
                    capacidad_solicitada = nombre
                    break
        if disponible and not capacidad_solicitada:
            for keyword, nombre in _POS.items():
                if keyword in msg:
                    capacidad_solicitada = nombre
                    break
        if disponible and not capacidad_solicitada:
            for concepto in conceptos:
                if not esta_implementada(concepto.id):
                    capacidad_solicitada = concepto.id
                    disponible    = False
                    razon_bloqueo = razon_no_implementada(concepto.id)
                    break
        if disponible and not razon_bloqueo:
            patron, razon = detectar_patron_no_implementado(msg)
            if patron:
                capacidad_solicitada = patron
                disponible    = False
                razon_bloqueo = razon

        hechos = {
            "tipo_respuesta":                  "CAPACIDAD_BELL",
            "capacidades_ejecutables":         CAPACIDADES_REALES_BELL["ejecutables"],
            "no_ejecutables":                  CAPACIDADES_REALES_BELL["NO_ejecutables_aun"],
            "total_conceptos":                 1503,
            "capacidad_solicitada":            capacidad_solicitada,
            "capacidad_solicitada_disponible": disponible,
        }
        if not disponible and razon_bloqueo:
            hechos["capacidad_bloqueada_razon"] = razon_bloqueo
        return hechos

    def _hechos_social(self, conceptos: list, mensaje: str) -> dict:
        ids     = {c.id for c in conceptos}
        msg     = mensaje.lower() if mensaje else ""
        subtipo = "SALUDO"
        for cid in ids:
            if cid in _SOCIAL_SUBTIPOS:
                subtipo = _SOCIAL_SUBTIPOS[cid]
                break
        subtipo_texto = self._detectar_social_por_texto(msg)
        if subtipo_texto and subtipo == "SALUDO":
            subtipo = subtipo_texto
        return {"tipo_respuesta": "SOCIAL", "subtipo": subtipo}

    def _hechos_estado_usuario(self, conceptos: list, mensaje: str) -> dict:
        ids        = {c.id for c in conceptos}
        emocion_id = "DESCONOCIDA"
        valencia   = "neutra"
        tono       = "empatico"
        for c in conceptos:
            props = getattr(c, 'propiedades', {}) or {}
            if props.get('es_estado_emocional') or props.get('valencia'):
                emocion_id = c.id
                valencia   = props.get('valencia', 'neutra')
                tono       = props.get('tono_recomendado', 'empatico')
                break
        if emocion_id == "DESCONOCIDA":
            for cid in ids:
                if cid in _USUARIO_EMOCIONES:
                    t = _USUARIO_EMOCIONES[cid]
                    emocion_id, valencia, tono = t[0], t[1], t[2]
                    break
        return {
            "tipo_respuesta":    "ESTADO_USUARIO",
            "emocion_detectada": emocion_id,
            "valencia":          valencia,
            "tono_recomendado":  tono,
            "mensaje_original":  mensaje,
        }

    def _hechos_accion_cognitiva(self, conceptos: list, mensaje: str) -> dict:
        ids               = {c.id for c in conceptos}
        msg               = mensaje.lower() if mensaje else ""
        accion_solicitada = "EXPLICAR"
        for cid in ids:
            if cid in _ACCION_COGNITIVA_TIPOS:
                accion_solicitada = _ACCION_COGNITIVA_TIPOS[cid]
                break
        accion_texto = self._detectar_cognitivo_por_texto(msg)
        if accion_texto:
            accion_solicitada = accion_texto
        if self._es_definicion(msg):
            accion_solicitada = "DEFINIR"
        return {
            "tipo_respuesta":    "ACCION_COGNITIVA",
            "accion_solicitada": accion_solicitada,
            "mensaje_original":  mensaje,
        }

    def _hechos_confirmacion(self, conceptos: list, mensaje: str) -> dict:
        ids = {c.id for c in conceptos}
        msg = mensaje.lower().strip() if mensaje else ""
        if msg in CONFIRMACIONES_DIRECTAS:
            valor = "NEGATIVA" if msg == "no" else "POSITIVA"
        elif ids & TRIGGERS_CONFIRMACION_POSITIVA:
            valor = "POSITIVA"
        elif ids & TRIGGERS_CONFIRMACION_NEGATIVA:
            valor = "NEGATIVA"
        else:
            valor = "NEUTRA"
        return {"tipo_respuesta": "CONFIRMACION", "valor": valor, "palabra_original": msg}

    def _hechos_temporal(self, conceptos: list, mensaje: str) -> dict:
        return {
            "tipo_respuesta":    "TEMPORAL",
            "referencia":        "conversacion_previa",
            "necesita_contexto": True,
            "mensaje_original":  mensaje,
        }

    def _hechos_cuantificacion(self, conceptos: list, mensaje: str) -> dict:
        msg             = mensaje.lower() if mensaje else ""
        dato_preguntado = None
        valor_respuesta = None
        for clave, valor in _CUANTIFICACION_BELL.items():
            if clave in msg:
                dato_preguntado = clave
                valor_respuesta = valor
                break
        return {
            "tipo_respuesta":   "CUANTIFICACION",
            "total_conceptos":  1503,
            "total_consejeras": 7,
            "total_comandos":   165,
            "dato_preguntado":  dato_preguntado,
            "valor_respuesta":  valor_respuesta,
            "mensaje_original": mensaje,
        }

    def _hechos_desconocido(self, conceptos: list, mensaje: str) -> dict:
        return {
            "tipo_respuesta":       "DESCONOCIDO",
            "conceptos_detectados": [c.id for c in conceptos],
            "mensaje_original":     mensaje,
        }

    def _hechos_registro_usuario(self, conceptos: list, mensaje: str) -> dict:
        msg        = mensaje.lower()
        dato_tipo  = "desconocido"
        dato_valor = ""
        match_nombre = re.search(
            r'(?:me llamo|mi nombre es|soy|puedes llamarme|llamame)\s+([a-z]+)', msg
        )
        if match_nombre:
            candidato = match_nombre.group(1).strip()
            if (len(candidato) >= 3 and candidato not in _PALABRAS_EXCLUIDAS_NOMBRE
                    and not candidato.isdigit()):
                dato_tipo  = "nombre"
                dato_valor = candidato.capitalize()
        match_edad = re.search(r'tengo\s+(\d+)\s*(anos?)', msg)
        if match_edad:
            edad = int(match_edad.group(1))
            if 1 <= edad <= 120:
                dato_tipo  = "edad"
                dato_valor = str(edad)
        if dato_tipo == "desconocido":
            ids = {c.id for c in conceptos}
            if ids & TRIGGERS_REGISTRO_USUARIO:
                dato_tipo = "profesion"
                match_prof = re.search(r'(?:soy|trabajo como|me dedico a)\s+(.+?)$', msg)
                if match_prof:
                    dato_valor = match_prof.group(1).strip()
        return {
            "tipo_respuesta":   "REGISTRO_USUARIO",
            "dato_tipo":        dato_tipo,
            "dato_valor":       dato_valor,
            "mensaje_original": mensaje,
            "accion":           "registrar_y_confirmar",
            "datos_conocidos":  dict(self._memoria().datos_usuario) if self._memoria() else {},
        }

    def _hechos_consulta_memoria(self, conceptos: list, mensaje: str) -> dict:
        msg             = mensaje.lower()
        dato_consultado = "desconocido"
        dato_encontrado = False
        dato_valor      = ""
        if any(p in msg for p in ['llamo', 'nombre']):
            dato_consultado = "nombre"
        elif any(p in msg for p in ['anos', 'edad', 'cuantos']):
            dato_consultado = "edad"
        elif any(p in msg for p in ['dedico', 'trabajo', 'profesion']):
            dato_consultado = "profesion"
        elif any(p in msg for p in ['sabes de mi', 'recuerdas', 'todo']):
            dato_consultado = "todo"
        mem = self._memoria()
        if mem:
            datos = mem.datos_usuario
            if dato_consultado == "todo":
                if datos:
                    dato_encontrado = True
                    dato_valor      = str(datos)
            elif dato_consultado in datos and datos[dato_consultado]:
                dato_encontrado = True
                dato_valor      = datos[dato_consultado]
        return {
            "tipo_respuesta":   "CONSULTA_MEMORIA",
            "dato_consultado":  dato_consultado,
            "dato_encontrado":  dato_encontrado,
            "dato_valor":       dato_valor,
            "mensaje_original": mensaje,
        }

    def _hechos_verificacion_logica(self, conceptos: list, mensaje: str) -> dict:
        return {
            "tipo_respuesta":      "VERIFICACION_LOGICA",
            "afirmacion_original": mensaje,
            "puede_verificar":     True,
            "mensaje_original":    mensaje,
        }

    def _hechos_conocimiento_general(self, conceptos: list, mensaje: str) -> dict:
        return {
            "tipo_respuesta":   "CONOCIMIENTO_GENERAL",
            "pregunta":         mensaje,
            "mensaje_original": mensaje,
            "tiene_grounding":  False,
        }

    # ------------------------------------------------------------------
    # PROCESAMIENTO CONVERSACIONAL
    # ------------------------------------------------------------------

    def procesar_conversacional(
        self, conceptos: list, mensaje_original: str = ""
    ) -> Decision:
        tipo      = self.clasificar_intencion(conceptos, mensaje_original)
        hechos    = self.construir_hechos(tipo, conceptos, mensaje_original)
        confianza = _clamp_certeza(hechos.get("grounding_promedio", 0.75))
        return Decision(
            tipo=tipo,
            certeza=confianza,
            conceptos_principales=[c.id for c in conceptos],
            puede_ejecutar=(tipo in (TipoDecision.CALCULO, TipoDecision.EJECUCION)),
            operacion_disponible=(
                "ejecutar_habilidad" if tipo in (
                    TipoDecision.CALCULO, TipoDecision.EJECUCION
                ) else None
            ),
            razon=f"Conversacional: {tipo.name}",
            hechos_reales=hechos,
        )

    def explicar_decision(self, decision: Decision) -> str:
        pasos = decision.pasos_razonamiento or []
        return (
            f"Decision: {decision.tipo.name}\n"
            f"Certeza: {decision.certeza:.0%}\n"
            f"Puede ejecutar: {decision.puede_ejecutar}\n\n"
            f"Razonamiento:\n{chr(10).join(pasos)}\n\n"
            f"Conclusion: {decision.razon}"
        ).strip()