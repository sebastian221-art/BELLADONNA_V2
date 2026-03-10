# -*- coding: utf-8 -*-
"""
motor_razonamiento.py — VERSION v10.0

CAMBIOS v10.0 sobre v9.2:
═══════════════════════════════════════════════════════════════════════
FIX-M-MAT1  Detección matemática UNIVERSAL — Bell detecta matemáticas
            sin importar cómo se formulen. Se agregaron:
            · _PALABRAS_MAT_UNIVERSAL: 120+ palabras que identifican
              intención matemática en lenguaje coloquial
            · _es_matematica_universal(): detector que captura TODA
              pregunta matemática antes de llegar a DESCONOCIDO
            · _PATRONES_MAT_LENGUAJE_NATURAL: 30+ regex para formas
              coloquiales ("cuánto es X por Y", "factorial de", etc.)

FIX-M-MAT2  _CONCEPTOS_MAT_CALCULO ampliado con todos los conceptos
            nuevos de semana7 v4.0: CONCEPTO_SISTEMA_LINEAL,
            CONCEPTO_ESTADISTICA, CONCEPTO_DERIVADA_PARCIAL,
            CONCEPTO_INECUACION, CONCEPTO_MCD, CONCEPTO_MCM,
            CONCEPTO_NUMERO_PRIMO, CONCEPTO_COMBINATORIA,
            CONCEPTO_POLINOMIO_INFO, CONCEPTO_FUNCION_TRIGONOMETRICA,
            CONCEPTO_LOGARITMO, CONCEPTO_EVALUAR_FUNCION.

FIX-M-MAT3  TRIGGERS_CALCULO ampliado para incluir los mismos conceptos
            nuevos. clasificar_intencion() los mapea a CALCULO.

FIX-M-MAT4  _es_calculo_por_texto() ampliado masivamente:
            estadística, sistema ecuaciones, MCD/MCM, primos,
            combinatoria, trigonometría, logaritmos, inecuaciones,
            evaluación de funciones.

FIX-M-MAT5  _hechos_calculo() incluye 'tipo_operacion_detectada'
            con el tipo específico (ESTADISTICA, SISTEMA, PRIMO...).

FIX-M-MAT6  Fallback final en clasificar_intencion(): antes de
            retornar DESCONOCIDO llama _es_matematica_universal().
            Bell NUNCA responde DESCONOCIDO a una pregunta matemática.

FIX-BUG7    FASE_ACTUAL unificada — leída desde core.capacidades_fase.

Todos los fixes de v9.2 preservados (FIX-BD-BUG1, FIX-BD-BUG8,
FIX-M4, FIX-M3, etc.).
═══════════════════════════════════════════════════════════════════════
"""

import re
import unicodedata
from typing import Dict, List, Optional, Set

from razonamiento.tipos_decision import (
    Decision, TipoDecision, RazonRechazo,
    TIPOS_GUARDAN_EN_MEMORIA, TIPOS_ACTUALIZAN_ESTADO,
)
from razonamiento.generador_decisiones import GeneradorDecisiones

from core.capacidades_fase import (
    FASE_ACTUAL,
    NO_IMPLEMENTADAS_IDS,
    esta_implementada,
    razon_no_implementada,
    detectar_patron_no_implementado,
)

try:
    from identidad_bell import (
        NARRATIVA_PROPIA, VOZ_BELL,
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


# ═══════════════════════════════════════════════════════════════════════
# NORMALIZADOR
# ═══════════════════════════════════════════════════════════════════════

def _norm(texto: str) -> str:
    nfkd = unicodedata.normalize('NFD', texto)
    sin_tildes = ''.join(c for c in nfkd if unicodedata.category(c) != 'Mn')
    return sin_tildes.lower()


# ═══════════════════════════════════════════════════════════════════════
# CONCEPTOS SHELL / SQLITE
# ═══════════════════════════════════════════════════════════════════════

_CONCEPTOS_SHELL_IDS = {
    "CONCEPTO_LS", "CONCEPTO_PWD", "CONCEPTO_DATE", "CONCEPTO_WHOAMI",
    "CONCEPTO_HOSTNAME", "CONCEPTO_UNAME", "CONCEPTO_UPTIME", "CONCEPTO_PS",
    "CONCEPTO_TOP", "CONCEPTO_DF", "CONCEPTO_DU", "CONCEPTO_FREE",
    "CONCEPTO_ENV", "CONCEPTO_ECHO", "CONCEPTO_TREE", "CONCEPTO_GREP",
    "CONCEPTO_FIND", "CONCEPTO_HEAD", "CONCEPTO_TAIL", "CONCEPTO_WC",
    "CONCEPTO_CAT", "CONCEPTO_STAT", "CONCEPTO_FILE", "CONCEPTO_KILL",
    "CONCEPTO_MKDIR", "CONCEPTO_TOUCH", "CONCEPTO_HOY", "CONCEPTO_MEMORIA",
    "CONCEPTO_PROCESO_SHELL", "CONCEPTO_CPU_SHELL", "CONCEPTO_DISCO",
    # FIX-M1: conceptos que también deben disparar ejecución shell
    "CONCEPTO_NPROC",          # "cuántos núcleos" → nproc
    "CONCEPTO_BUSCAR",         # "busca el archivo X" → find
    "CONCEPTO_PATH",           # "cuál es el PATH" → echo $PATH
    "CONCEPTO_VERSION",        # "versión de Python" → python3 --version
    "CONCEPTO_PACKAGE",        # "paquetes pip" → pip3 list
    "CONCEPTO_GIT",            # "qué cambié en git" → git diff
    "CONCEPTO_LOG",            # "historial de git" → git log
    "CONCEPTO_CONEXION",       # "conexiones activas" → ss -tuln
    "CONCEPTO_CONNECTION",     # variante en inglés
    "CONCEPTO_ABIERTO_ADJ",    # "puertos abiertos" → ss -tuln
}

_CONCEPTOS_SQLITE_IDS = {
    "CONCEPTO_SQLITE", "CONCEPTO_SQL", "CONCEPTO_TABLA", "CONCEPTO_SELECT",
    "CONCEPTO_LISTAR_TABLAS", "CONCEPTO_ESQUEMA", "CONCEPTO_COUNT",
    "CONCEPTO_INSERT", "CONCEPTO_UPDATE", "CONCEPTO_DELETE",
    "CONCEPTO_CREAR_TABLA", "CONCEPTO_ELIMINAR_TABLA", "CONCEPTO_VACIAR_TABLA",
    "CONCEPTO_INSERTAR_DATOS", "CONCEPTO_SQL_ESCRITURA", "CONCEPTO_REGISTRO",
    "CONCEPTO_RESULTADO_QUERY", "CONCEPTO_TRANSACCION", "CONCEPTO_INDICE",
    "CONCEPTO_CONECTAR_BD", "CONCEPTO_DESCONECTAR_BD", "CONCEPTO_BASE_DATOS",
}


# ═══════════════════════════════════════════════════════════════════════
# PATRONES SHELL
# ═══════════════════════════════════════════════════════════════════════

_PATRONES_SHELL_DIRECTOS = [
    r'lista\s+(?:tus\s+)?archivos', r'lista\s+(?:los\s+)?archivos',
    r'muestr[a-z]+\s+(?:tus?\s+|los\s+)?archivos', r'que\s+archivos\s+(?:hay|tienes)',
    r'donde\s+est[a-z]+', r'directorio\s+actual', r'ruta\s+actual',
    r'en\s+que\s+(?:directorio|carpeta)', r'cual\s+es\s+tu\s+directorio',
    r'que\s+fecha', r'fecha\s+(?:de\s+)?hoy', r'que\s+hora', r'hora\s+actual',
    r'que\s+dia\s+(?:es\s+)?hoy', r'cuanta\s+(?:ram|memoria)',
    r'memoria\s+(?:ram|disponible|libre|usada)', r'uso\s+de\s+memoria',
    r'espacio\s+en\s+disco', r'espacio\s+(?:libre|disponible)', r'cuanto\s+espacio',
    r'procesos\s+(?:activos|corriendo)', r'que\s+procesos',
    r'usuario\s+(?:del\s+sistema|actual)', r'con\s+que\s+usuario',
    r'que\s+usuario\s+soy', r'que\s+usuario\s+eres', r'cual\s+es\s+tu\s+usuario',
    r'sistema\s+operativo', r'informacion\s+del\s+sistema',
    r'que\s+(?:linux|kernel|sistema)', r'version\s+(?:de\s+)?python',
    r'python\s+version', r'nombre\s+del\s+(?:equipo|servidor|maquina)',
    r'estado\s+(?:de\s+)?git', r'git\s+status', r'historial\s+(?:de\s+)?git',
    r'log\s+(?:de\s+)?git', r'ramas?\s+(?:de\s+)?git', r'variables?\s+de\s+entorno',
    r'tiempo\s+(?:encendido|activo)',
    r'cuanto\s+tiempo\s+(?:lleva|llevas)\s+(?:corriendo|activ[oa]|encendido)',
    r'paquetes?\s+(?:pip|python|instalados?)',
    r'que\s+(?:paquetes?|librerias?)\s+(?:hay|tienes)',
    r'estructura\s+(?:de\s+)?(?:carpetas|directorios)',
    r'arbol\s+(?:de\s+)?directorios',
    # FIX-M2: patrones faltantes detectados en pruebas
    r'como\s+se\s+llama\s+(?:esta?\s+)?(?:maquina|equipo|pc|computadora|servidor)',
    r'nombre\s+(?:de\s+(?:esta?\s+)?)?(?:maquina|equipo|pc|computadora)',
    r'hostname', r'nombre\s+del\s+host',
    r'cuantos?\s+(?:nucleos|cores?|procesadores?)',
    r'info(?:rmacion)?\s+(?:del?\s+)?(?:cpu|procesador)',
    r'detalles?\s+(?:del?\s+)?(?:cpu|procesador)',
    r'cuanto\s+pesa\s+(?:esta?\s+)?(?:carpeta|directorio)',
    r'archivos?\s+(?:de\s+)?log', r'logs?\s+del?\s+sistema',
    r'archivos?\s+(?:mas\s+)?(?:grandes?|pesados?)',
    r'archivos?\s+\.\w+', r'que\s+archivos?\s+\.\w+',
    r'busca(?:r)?\s+(?:el\s+|la\s+)?archivo',
    r'donde\s+esta\s+(?:el\s+|la\s+)?(?:archivo|python|pip)',
    r'primeras?\s+lineas?\s+(?:del?\s+)?archivo',
    r'ultimas?\s+lineas?\s+(?:del?\s+)?(?:archivo|\w+\.\w+)',
    r'que\s+cambie\s+en\s+git', r'cambios?\s+(?:en\s+|de\s+)?git',
    r'git\s+diff', r'git\s+stash', r'git\s+log', r'git\s+\w+',
    r'carga\s+del\s+sistema', r'carga\s+(?:del?\s+)?cpu',
    r'archivos?\s+modificados?\s+(?:hoy|reciente)',
    r'muestr[a-z]+\s+(?:el\s+)?archivo\s+\S+',
    r'cuantas?\s+lineas?\s+(?:tiene|hay)',
]

_RE_PATRONES_SHELL = [re.compile(p, re.IGNORECASE) for p in _PATRONES_SHELL_DIRECTOS]


# ═══════════════════════════════════════════════════════════════════════
# PATRONES BD (FIX-BD-BUG1 v9.2 preservados)
# ═══════════════════════════════════════════════════════════════════════

_PATRONES_BD_DIRECTOS = [
    r'estado\s+de\s+(?:tu\s+)?(?:base\s+de\s+datos|bd|sqlite)',
    r'qu[e]+\s+(?:base\s+de\s+datos|bd)\s+tienes',
    r'tienes\s+(?:una\s+)?(?:base\s+de\s+datos|bd)',
    r'muestra(?:me)?\s+(?:tu\s+)?(?:base\s+de\s+datos|bd)',
    r'info(?:rmacion)?\s+de\s+(?:la\s+)?(?:base\s+de\s+datos|bd)',
    r'qu[e]+\s+tablas?\s+(?:hay|tienes|existen)',
    r'lista(?:me)?\s+(?:las\s+)?tablas?', r'muestr[a-z]+\s+(?:las\s+)?tablas?',
    r'cu[a]ntas?\s+tablas?\s+(?:hay|tienes)',
    r'tablas?\s+(?:disponibles?|existentes?)',
    r'esquema\s+de\s+(?:la\s+)?(?:tabla\s+)?\w+',
    r'estructura\s+de\s+(?:la\s+)?(?:tabla\s+)(?:\w+)|estructura\s+de\s+(?:la\s+)(?:tabla|base|bd)\s*',
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
    r'consulta\s+sql', r'corre\s+(?:el\s+)?(?:sql|query)',
    r'[íi]ndices?\s+de\s+(?:la\s+)?(?:tabla\s+)?\w+',
    r'[íi]ndices?\s+(?:disponibles?|existentes?)',
    r'crea(?:r)?\s+(?:una\s+)?tabla\s+\w+',
    r'nueva\s+tabla\s+\w+', r'hacer\s+(?:una\s+)?tabla\s+\w+',
    r'create\s+table\s+\w+',
    r'inserta(?:r)?\s+.+\s+en\s+\w+', r'agrega(?:r)?\s+.+\s+(?:a|en)\s+\w+',
    r'a[nñ]ade?\s+.+\s+(?:a|en)\s+\w+', r'guarda(?:r)?\s+.+\s+en\s+\w+',
    r'^insert\s+into\s+\w+', r'nuevo\s+registro\s+en\s+\w+',
    r'actualiza(?:r)?\s+.+\s+(?:en|de)\s+\w+',
    r'cambia(?:r)?\s+.+\s+(?:en|de)\s+\w+',
    r'modifica(?:r)?\s+.+\s+(?:en|de)\s+\w+',
    r'^update\s+\w+\s+set',
    r'elimin[a-z]*\s+.+\s+de\s+(?:la\s+)?(?:tabla\s+)?\w+',
    r'borra(?:r)?\s+.+\s+de\s+(?:la\s+)?(?:tabla\s+)?\w+',
    r'^delete\s+from\s+\w+\s+where', r'^delete\s+from\s+\w+',
    r'vac[ií]a(?:r)?\s+(?:la\s+)?(?:tabla\s+)?\w+',
    r'limpia(?:r)?\s+(?:la\s+)?(?:tabla\s+)?\w+',
    r'borra(?:r)?\s+todos?\s+(?:los\s+)?registros?\s+de\s+\w+',
    r'elimin[a-z]+\s+todos?\s+(?:los\s+)?registros?\s+de\s+\w+',
    r'^truncate\s+(?:table\s+)?\w+',
    r'elimin[a-z]+\s+(?:la\s+)?tabla\s+\w+',
    r'borra(?:r)?\s+(?:la\s+)?tabla\s+\w+',
    r'^drop\s+(?:table\s+)?\w+',
    r'destruye?\s+(?:la\s+)?tabla\s+\w+',
    # FIX-BD-BUG1 v9.2: patrones permisivos
    r'inserta(?:r)?\s+(?:un|una|el|la|al|a)?\s*\w+',
    r'agrega(?:r)?\s+(?:un|una|el|la|al|a)?\s*\w+',
    r'muestr[a-z]*\s+todos?\s+(?:los?\s+)?\w+',
    r'elimin[a-z]*\s+(?:el|la|al|a\s+la|un|una)\s+\w+',
    r'borra(?:r)?\s+(?:el|la|al|un|una)\s+\w+',
    r'cu[aá]l\s+es\s+el\s+(?:\w+\s+)?m[aá]s\s+\w+',
    r'(?:el|la)\s+\w+\s+m[aá]s\s+\w+',
    r'todos?\s+los?\s+(?:productos?|registros?|usuarios?|clientes?|items?|elementos?)',
]

_RE_PATRONES_BD = [re.compile(p, re.IGNORECASE) for p in _PATRONES_BD_DIRECTOS]


# ═══════════════════════════════════════════════════════════════════════
# FIX-M3: patrón mat avanzada con confianza baja
# ═══════════════════════════════════════════════════════════════════════

_RE_EXPR_MAT_AVANZADA_CON_VERBO = re.compile(
    r'(?:resolv|resuelv|deriv|integr|l[íi]mite|lim\b|taylor|factori|simplif|expan)'
    r'.{0,60}'
    r'(?:[a-zA-Z]|[*+-/^]|\()',
    re.IGNORECASE
)


# ═══════════════════════════════════════════════════════════════════════
# FIX-M-MAT1: DETECTOR MATEMÁTICO UNIVERSAL
# ═══════════════════════════════════════════════════════════════════════

_PALABRAS_MAT_UNIVERSAL = {
    'suma', 'sumar', 'resta', 'restar', 'multiplica', 'multiplicar',
    'dividir', 'division', 'producto', 'cociente',
    'mas', 'menos', 'por', 'entre',
    'potencia', 'elevado', 'cuadrado', 'cubo', 'raiz', 'sqrt', 'cbrt', 'exponente',
    'derivar', 'deriva', 'derivada', 'derivadas', 'diferencial',
    'integrar', 'integra', 'integral', 'integrales', 'antiderivada',
    'limite', 'limites', 'lim',
    'taylor', 'serie', 'convergencia', 'divergencia',
    'factorizar', 'factoriza', 'factor', 'factores',
    'simplificar', 'simplifica', 'simplify',
    'expandir', 'expande', 'expand', 'desarrollar',
    'resolver', 'resuelve', 'solve', 'ecuacion', 'sistema', 'polinomio',
    'seno', 'coseno', 'tangente', 'secante', 'cosecante', 'cotangente',
    'sin', 'cos', 'tan', 'sec', 'csc', 'cot',
    'arcoseno', 'arcocoseno', 'arcotangente', 'grados', 'radianes',
    'logaritmo', 'ln', 'log',
    'media', 'promedio', 'mediana', 'moda', 'varianza',
    'desviacion', 'percentil', 'estadistica',
    'factorial', 'primo', 'mcd', 'mcm', 'divisor', 'multiplo',
    'combinaciones', 'permutaciones', 'combinatoria',
    'porcentaje', 'porciento', 'descuento',
    'area', 'perimetro', 'volumen', 'pi',
    'inecuacion', 'desigualdad',
    'calcula', 'calcular', 'calculo',
    'resultado', 'operacion', 'matematica', 'matematicas',
    'algebra', 'aritmetica',
    'numero', 'valor', 'evalua', 'modulo', 'absoluto',
    'halla', 'hallar', 'encuentra', 'encontrar', 'despeja', 'despejar',
}

_PATRONES_MAT_LENGUAJE_NATURAL = [
    re.compile(r'\d+\s*[\+\-\*\/×÷]\s*\d+'),
    re.compile(r'\d+\s+(?:mas|menos|por|entre|dividido)\s+\d+', re.IGNORECASE),
    re.compile(r'(?:cuanto\s+(?:es|da|son)|dame|dime|calcula)\s+\d+', re.IGNORECASE),
    re.compile(r'\d+\s+(?:al\s+)?(?:cuadrado|cubo|elevado)', re.IGNORECASE),
    re.compile(r'(?:raiz|raiz)\s+(?:cuadrada\s+)?de\s+\d+', re.IGNORECASE),
    re.compile(r'(?:seno|coseno|tangente|sen)\s+de\s+\d+', re.IGNORECASE),
    re.compile(r'(?:sin|cos|tan)\s*\(?\s*\d+', re.IGNORECASE),
    re.compile(r'(?:logaritmo|log|ln)\s+(?:de\s+|natural\s+de\s+)?\d+', re.IGNORECASE),
    re.compile(r'factorial\s+de\s+\d+|\d+\s*!', re.IGNORECASE),
    re.compile(r'\d+\s*%|\d+\s+por\s+ciento', re.IGNORECASE),
    re.compile(r'(?:media|promedio|mediana|moda|varianza|desviaci[oó]n)\s+de', re.IGNORECASE),
    re.compile(r'calcula\s+(?:la\s+)?(?:media|promedio|mediana|moda|varianza)', re.IGNORECASE),
    re.compile(r'estadist\w*\s+de', re.IGNORECASE),
    re.compile(r'sistema\s+de\s+ecuaciones?', re.IGNORECASE),
    re.compile(r'ecuaciones?\s+simult[aá]neas?', re.IGNORECASE),
    re.compile(r'deriv[aá](?:da)?\s+de\s+[a-zA-Z]', re.IGNORECASE),
    re.compile(r'integr[aá](?:l)?\s+de\s+[a-zA-Z]', re.IGNORECASE),
    re.compile(r'l[íi]mite\s+(?:de\s+)?[a-zA-Z].*(?:tiende|cuando)', re.IGNORECASE),
    re.compile(r'(?:m\.?c\.?d\.?|m\.?c\.?m\.?|m[aá]ximo\s+com[uú]n|m[ií]nimo\s+com[uú]n)\s+(?:de\s+)?\d+', re.IGNORECASE),
    re.compile(r'\d+\s+(?:es\s+)?primo\??|es\s+primo\s+\d+', re.IGNORECASE),
    re.compile(r'(?:combinaciones?|permutaciones?)\s+de\s+\d+', re.IGNORECASE),
    re.compile(r'C\s*\(\s*\d+\s*,\s*\d+\s*\)|P\s*\(\s*\d+\s*,\s*\d+\s*\)'),
    re.compile(r'[a-zA-Z]\s*(?:>|<|>=|<=|≥|≤)\s*\d+'),
    re.compile(r'inecuaci[oó]n', re.IGNORECASE),
    re.compile(r'eval[uú]a(?:r)?\s+(?:f\s*\(|la\s+funci[oó]n)', re.IGNORECASE),
    re.compile(r'la\s+mitad\s+de\s+\d+|un\s+tercio\s+de\s+\d+|un\s+cuarto\s+de\s+\d+', re.IGNORECASE),
    re.compile(r'redonde[ao]\s+\d+', re.IGNORECASE),
    re.compile(r'valor\s+absoluto\s+de\s+[\d\-]', re.IGNORECASE),
    re.compile(r'\d+[a-zA-Z][\+\-\*\/]|[a-zA-Z]\*\*\d+|[a-zA-Z]\^\d+'),
    # FIX-M-MAT8: patrones adicionales de ecuación y división natural
    re.compile(r'halla[r]?\s+[a-z]\s+(?:si|cuando|donde|tal\s+que)', re.IGNORECASE),
    re.compile(r'\d+\s+entre\s+\d+', re.IGNORECASE),
    re.compile(r'cuanto\s+(?:da|es|son)\s+\d+\s+(?:entre|dividido|por|mas|menos)\s+\d+', re.IGNORECASE),
    re.compile(r'(?:mitad|tercio|cuarto|doble|triple)\s+de\s+\d+', re.IGNORECASE),
]


def _es_matematica_universal(msg: str) -> bool:
    """FIX-M-MAT1: Retorna True si el mensaje tiene intención matemática."""
    if not msg:
        return False
    msg_norm = _norm(msg)
    palabras_msg = re.findall(r'\b\w+\b', msg_norm)
    for palabra in palabras_msg:
        if palabra in _PALABRAS_MAT_UNIVERSAL:
            return True
    for patron in _PATRONES_MAT_LENGUAJE_NATURAL:
        if patron.search(msg):
            return True
    if re.search(r'[a-zA-Z]\s*[\+\-\*\/\^]\s*[a-zA-Z0-9]|[a-zA-Z0-9]\s*[\+\-\*\/\^]\s*[a-zA-Z]', msg):
        if re.search(r'\d', msg) or re.search(r'[a-zA-Z]\*\*', msg):
            return True
    return False


def _detectar_tipo_mat_especifico(msg: str) -> str:
    """FIX-M-MAT5: Detecta el sub-tipo específico de operación matemática."""
    msg_l = msg.lower()
    if re.search(r'sistema\s+de\s+ecuaciones?|ecuaciones?\s+simult[aá]neas?', msg_l): return 'SISTEMA'
    if re.search(r'estadist\w*|media\s+de|promedio\s+de|desviaci[oó]n|varianza\s+de|mediana\s+de|moda\s+de', msg_l): return 'ESTADISTICA'
    if re.search(r'deriv[aá](?:da)?\s+parcial|parcial\s+de|∂', msg_l): return 'DERIVADA_PARCIAL'
    if re.search(r'deriv[aá](?:da)?|d/dx|dy/dx', msg_l): return 'DERIVADA'
    if re.search(r'integr[aá](?:l)?|antiderivada|primitiva\s+de|[∫]', msg_l): return 'INTEGRAL'
    if re.search(r'l[íi]mite\s+(?:de|cuando)|lim\s*[\(\s]|tiende\s+a', msg_l): return 'LIMITE'
    if re.search(r'serie\s+de\s+taylor|taylor\s+de|expansi[oó]n\s+de\s+taylor', msg_l): return 'TAYLOR'
    if re.search(r'factori[zs](?:a(?:r)?)?', msg_l): return 'FACTORIZAR'
    if re.search(r'simplif[ií]c(?:a(?:r)?)?|forma\s+m[aá]s\s+simple', msg_l): return 'SIMPLIFICAR'
    if re.search(r'expan[ds](?:e(?:r)?)?|desarrolla(?:r)?', msg_l): return 'EXPANDIR'
    if re.search(r'inecuaci[oó]n|[a-zA-Z]\s*(?:>|<|>=|<=|≥|≤)', msg_l): return 'INECUACION'
    if re.search(r'm\.?c\.?d\.?|m[aá]ximo\s+com[uú]n\s+divisor', msg_l): return 'MCD'
    if re.search(r'm\.?c\.?m\.?|m[ií]nimo\s+com[uú]n\s+m[uú]ltiplo', msg_l): return 'MCM'
    if re.search(r'\d+\s+es\s+primo|es\s+primo|n[uú]mero\s+primo', msg_l): return 'PRIMO'
    if re.search(r'combinaciones?\s+de\s+\d+|C\s*\(\s*\d+', msg_l): return 'COMBINACIONES'
    if re.search(r'permutaciones?\s+de\s+\d+|P\s*\(\s*\d+', msg_l): return 'PERMUTACIONES'
    if re.search(r'grado\s+del?\s+polinomio|coeficientes?\s+del?\s+polinomio', msg_l): return 'POLINOMIO'
    if re.search(r'eval[uú]a(?:r)?|sustituye?\s+[a-z]\s*=|valor\s+de\s+f\s*\(', msg_l): return 'EVALUAR'
    if re.search(r'resolv|resuelv|solve|halla\s+[a-z]', msg_l): return 'ECUACION'
    return 'BASICO'


# ═══════════════════════════════════════════════════════════════════════
# CONSTANTES
# ═══════════════════════════════════════════════════════════════════════

CONSEJERAS_ROLES_OFICIALES = {
    "Vega":  "Guardiana de principios y seguridad — veto sobre cualquier decision",
    "Echo":  "Verificadora de coherencia y logica — revisa verdad y consistencia",
    "Lyra":  "Inteligencia emocional — detecta estado emocional y adapta el tono",
    "Nova":  "Ingenieria y optimizacion — eficiencia tecnica y nuevos conceptos",
    "Luna":  "Reconocimiento de patrones — detecta repeticiones y tendencias",
    "Iris":  "Curiosidad y aprendizaje — detecta terminos desconocidos",
    "Sage":  "Sintesis y sabiduria — integra perspectivas del consejo",
}

CAPACIDADES_REALES_BELL = {
    "ejecutables": [
        "Razonar con 1503 conceptos verificados",
        "Recordar la conversacion actual y datos del usuario",
        "Detectar emociones y adaptar el tono",
        "Consultar y modificar bases de datos SQLite (CRUD completo)",
        "Ejecutar codigo Python basico",
        "Ejecutar comandos de terminal (165 comandos)",
        "Calculos matematicos basicos y avanzados (SymPy): derivadas, integrales, limites, Taylor, "
        "sistemas de ecuaciones, estadistica, MCD, MCM, primos, combinatoria, inecuaciones",
        "Analizar codigo Python: metricas, complejidad, calidad (Nova)",
    ],
    "NO_ejecutables_aun": [
        "Crear archivos (pendiente)",
        "Leer archivos del sistema (pendiente)",
        "Acceder a internet",
        "Procesar imagenes",
        "Recordar conversaciones de sesiones anteriores",
    ],
}

CONFIRMACIONES_DIRECTAS = {
    "si", "sí", "no", "ok", "okay", "dale", "listo", "claro", "correcto",
    "exacto", "perfecto", "adelante", "negativo", "afirmativo", "bueno",
    "bien", "entendido", "de acuerdo", "va", "ya", "andale", "ándale", "sale",
}

NOMBRES_CONSEJERAS = {"vega", "echo", "lyra", "nova", "luna", "iris", "sage"}

PALABRAS_LLM = {
    "modelo de lenguaje", "llm", "chatgpt", "gpt", "openai",
    "inteligencia artificial", "ia", "bot", "chatbot", "robot",
    "claude", "gemini", "copilot", "bard",
}

PATRONES_COGNITIVOS_TEXTO = {
    "explicame": "EXPLICAR", "explica": "EXPLICAR",
    "simplifica": "SIMPLIFICAR", "simplificame": "SIMPLIFICAR",
    "repite": "REPETIR", "repetir": "REPETIR",
    "define": "DEFINIR", "defineme": "DEFINIR",
    "reformula": "REFORMULAR", "aclara": "ACLARAR",
    "continua": "ELABORAR", "desarrolla": "ELABORAR", "amplia": "ELABORAR",
}

PATRONES_SOCIAL_TEXTO = {
    "buenos dias": "SALUDO", "buenas tardes": "SALUDO",
    "buenas noches": "SALUDO", "buenas": "SALUDO", "buen dia": "SALUDO",
    "muchas gracias": "AGRADECIMIENTO", "mil gracias": "AGRADECIMIENTO",
    "te agradezco": "AGRADECIMIENTO", "muy agradecido": "AGRADECIMIENTO",
    "muy agradecida": "AGRADECIMIENTO", "gracias por todo": "AGRADECIMIENTO",
    "muchisimas gracias": "AGRADECIMIENTO",
}

_CUANTIFICACION_BELL = {
    "conceptos": 1503, "consejeras": 7,
    "comandos": 165, "comandos de terminal": 165,
}

TRIGGERS_IDENTIDAD = {
    "CONCEPTO_QUIEN", "CONCEPTO_QUIEN_PREGUNTA", "CONCEPTO_NOMBRE_ARCHIVO",
    "CONCEPTO_LLAMAR", "CONCEPTO_PRESENTAR", "CONCEPTO_QUE_ES",
    "CONCEPTO_COMO_TE_LLAMAS", "CONCEPTO_NOMBRE", "CONCEPTO_DESCRIBIR",
    "CONCEPTO_CUAL_ES_TU_NOMBRE", "CONCEPTO_QUIENES_ERES", "CONCEPTO_ERES",
    "CONCEPTO_HABLAR_DE_TI", "CONCEPTO_APRENDER", "CONCEPTO_DIFERENCIA",
    "CONCEPTO_COMPARAR", "CONCEPTO_FASE", "CONCEPTO_CRECIMIENTO", "CONCEPTO_PASO",
}

TRIGGERS_ESTADO_BELL = {
    "CONCEPTO_COMO", "CONCEPTO_COMO_PREGUNTA", "CONCEPTO_BUENO",
    "CONCEPTO_IR", "CONCEPTO_ESTAR", "CONCEPTO_BIEN", "CONCEPTO_FUNCIONANDO",
    "CONCEPTO_ACTIVO", "CONCEPTO_OPERATIVO", "CONCEPTO_COMO_VAS",
    "CONCEPTO_TODO_BIEN", "CONCEPTO_SIENTES", "CONCEPTO_ESTADO",
}

TRIGGERS_CAPACIDAD = {
    "CONCEPTO_PODER", "CONCEPTO_PODRIAS", "CONCEPTO_SABER", "CONCEPTO_SABER_V",
    "CONCEPTO_HACER", "CONCEPTO_CAPAZ", "CONCEPTO_POSIBLE", "CONCEPTO_IMPOSIBLE",
    "CONCEPTO_PUEDES", "CONCEPTO_HACES", "CONCEPTO_AYUDAR", "CONCEPTO_ERES_CAPAZ",
    "CONCEPTO_FUNCIONES", "CONCEPTO_HABILIDADES", "CONCEPTO_CAPACIDADES",
    "CONCEPTO_SIRVES", "CONCEPTO_PERMISOS_SHELL", "CONCEPTO_RED_OBJ",
    "CONCEPTO_ACCESO", "CONCEPTO_RECORDAR_ACCION",
}

TRIGGERS_SOCIAL = {
    "CONCEPTO_HOLA", "CONCEPTO_HOLA_EXPR", "CONCEPTO_BUENOS_DIAS",
    "CONCEPTO_ADIOS_EXPR", "CONCEPTO_GRACIAS", "CONCEPTO_GRACIAS_EXPR",
    "CONCEPTO_DISCULPA_EXPR", "CONCEPTO_BUENAS_TARDES", "CONCEPTO_BUENAS_NOCHES",
    "CONCEPTO_HEY", "CONCEPTO_BUENAS", "CONCEPTO_QUE_TAL", "CONCEPTO_SALUDAR",
    "CONCEPTO_BUEN_DIA", "CONCEPTO_HASTA_LUEGO", "CONCEPTO_CHAO",
    "CONCEPTO_BYE", "CONCEPTO_HASTA_PRONTO", "CONCEPTO_NOS_VEMOS",
    "CONCEPTO_HASTA_MANANA", "CONCEPTO_CUIDADE", "CONCEPTO_AGRADECIDO",
    "CONCEPTO_AGRADEZCO", "CONCEPTO_MIL_GRACIAS", "CONCEPTO_TE_AGRADEZCO",
    "CONCEPTO_MUCHAS_GRACIAS", "CONCEPTO_PERDON", "CONCEPTO_DISCULPA",
    "CONCEPTO_LO_SIENTO", "CONCEPTO_PERDONAME", "CONCEPTO_DISCULPAME",
}

TRIGGERS_ESTADO_USUARIO = {
    "CONCEPTO_FELIZ", "CONCEPTO_TRISTE", "CONCEPTO_ENOJADO",
    "CONCEPTO_FRUSTRADO", "CONCEPTO_CONFUNDIDO", "CONCEPTO_CANSADO",
    "CONCEPTO_PERDIDO_ESTADO", "CONCEPTO_ANSIOSO", "CONCEPTO_ABURRIDO",
    "CONCEPTO_PREOCUPADO", "CONCEPTO_ESTRESADO", "CONCEPTO_MOLESTO",
    "CONCEPTO_PERDIDO", "CONCEPTO_NO_ENTIENDO", "CONCEPTO_DIFICIL",
    "CONCEPTO_COMPLICADO", "CONCEPTO_EMOCIONADO", "CONCEPTO_CONTENTO",
    "CONCEPTO_INTERESANTE", "CONCEPTO_GENIAL", "CONCEPTO_INCREIBLE",
    "CONCEPTO_UNICO", "CONCEPTO_SOLEDAD",
}

TRIGGERS_ACCION_COGNITIVA = {
    "CONCEPTO_EXPLICAR", "CONCEPTO_EXPLICAR_V", "CONCEPTO_RESUMIR_ACCION",
    "CONCEPTO_SIMPLIFICAR", "CONCEPTO_DECIR", "CONCEPTO_CONTAR",
    "CONCEPTO_RESUMIR", "CONCEPTO_REPETIR", "CONCEPTO_ACLARAR",
    "CONCEPTO_PROFUNDIZAR", "CONCEPTO_EJEMPLIFICAR", "CONCEPTO_CONTINUAR",
    "CONCEPTO_ORDENAR", "CONCEPTO_CLASIFICAR", "CONCEPTO_DESTACAR",
    "CONCEPTO_REFORMULAR", "CONCEPTO_DESARROLLAR", "CONCEPTO_AMPLIAR",
    "CONCEPTO_TRADUCIR", "CONCEPTO_DEFINIR", "CONCEPTO_DETALLAR",
    "CONCEPTO_ELABORAR", "CONCEPTO_EXPANDIR", "CONCEPTO_CONTRASTAR",
}

_CONCEPTOS_COGNITIVOS_AMBIGUOS = {
    "CONCEPTO_SIMPLIFICAR", "CONCEPTO_EXPANDIR", "CONCEPTO_ELABORAR",
}

# FIX-M-MAT2: ampliado con todos los conceptos nuevos de semana7 v4.0
_CONCEPTOS_MAT_CALCULO = {
    "CONCEPTO_DERIVAR", "CONCEPTO_INTEGRAR", "CONCEPTO_RESOLVER_ECUACION",
    "CONCEPTO_SERIE_TAYLOR", "CONCEPTO_LIMITE", "CONCEPTO_SIMPLIFICAR",
    "CONCEPTO_EXPANDIR", "CONCEPTO_FACTORIZAR", "CONCEPTO_EVALUAR",
    "CONCEPTO_DERIVADA", "CONCEPTO_DERIVADA_PRIMERA", "CONCEPTO_DERIVADA_SEGUNDA",
    "CONCEPTO_INTEGRAL", "CONCEPTO_INTEGRAL_DEFINIDA", "CONCEPTO_INTEGRAL_INDEFINIDA",
    "CONCEPTO_RAIZ_AVANZADA", "CONCEPTO_ECUACION_AVANZADA",
    # FIX-M-MAT2 NUEVO: semana7 v4.0
    "CONCEPTO_SISTEMA_LINEAL",
    "CONCEPTO_ESTADISTICA",
    "CONCEPTO_DERIVADA_PARCIAL",
    "CONCEPTO_INECUACION",
    "CONCEPTO_MCD",
    "CONCEPTO_MCM",
    "CONCEPTO_NUMERO_PRIMO",
    "CONCEPTO_COMBINATORIA",
    "CONCEPTO_POLINOMIO_INFO",
    "CONCEPTO_FUNCION_TRIGONOMETRICA",
    "CONCEPTO_LOGARITMO",
    "CONCEPTO_EVALUAR_FUNCION",
    "CONCEPTO_SISTEMA_ECUACIONES",
    "CONCEPTO_ECUACION_CUADRATICA",
}

TRIGGERS_CONFIRMACION_POSITIVA = {
    "CONCEPTO_SI", "CONCEPTO_SI_AFIRMACION", "CONCEPTO_DE_ACUERDO",
    "CONCEPTO_ENTENDIDO", "CONCEPTO_PERFECTO", "CONCEPTO_CORRECTO",
    "CONCEPTO_CORRECTO_RESP", "CONCEPTO_OK", "CONCEPTO_200_OK",
    "CONCEPTO_DALE", "CONCEPTO_CLARO", "CONCEPTO_POR_SUPUESTO",
    "CONCEPTO_EXACTO", "CONCEPTO_AFIRMATIVO", "CONCEPTO_ASI_ES",
    "CONCEPTO_LISTO", "CONCEPTO_ADELANTE",
}

TRIGGERS_CONFIRMACION_NEGATIVA = {
    "CONCEPTO_NO", "CONCEPTO_NO_NEGACION", "CONCEPTO_INCORRECTO_RESP",
    "CONCEPTO_MALO", "CONCEPTO_MAL", "CONCEPTO_INCORRECTO",
    "CONCEPTO_NO_ASI", "CONCEPTO_NEGATIVO",
}

TRIGGERS_TEMPORAL = {
    "CONCEPTO_ANTES", "CONCEPTO_AHORA", "CONCEPTO_DESPUES",
    "CONCEPTO_HACE_MOMENTO", "CONCEPTO_ANTERIORMENTE", "CONCEPTO_RECIEN",
    "CONCEPTO_PREVIO", "CONCEPTO_LUEGO", "CONCEPTO_HACE_RATO",
    "CONCEPTO_ANTES_DIJISTE", "CONCEPTO_MENCIONASTE", "CONCEPTO_DIJISTE",
    "CONCEPTO_AYER",
}

TRIGGERS_CUANTIFICACION = {
    "CONCEPTO_TODOS", "CONCEPTO_NINGUNO", "CONCEPTO_ALGUNOS",
    "CONCEPTO_PRIMERO", "CONCEPTO_ULTIMO", "CONCEPTO_SIGUIENTE",
    "CONCEPTO_CUANTOS", "CONCEPTO_VARIOS",
    "CONCEPTO_POCOS", "CONCEHOS_MUCHOS", "CONCEPTO_TODOS_LOS",
    "CONCEPTO_CUANTO", "CONCEPTO_NUMERO", "CONCEPTO_CANTIDAD",
    "CONCEPTO_CUANTOS_PREGUNTA",
    # NOTA: CONCEPTO_MITAD fue movido a TRIGGERS_CALCULO (FIX-M-MAT6)
    # "la mitad de 980" es matemáticas, no cuantificación de Bell
}

TRIGGERS_REGISTRO_USUARIO = {
    "CONCEPTO_PROGRAMADOR", "CONCEPTO_INGENIERO", "CONCEPTO_ESTUDIANTE",
    "CONCEPTO_MEDICO", "CONCEPTO_TRABAJADOR", "CONCEPTO_DISENIADOR",
    "CONCEPTO_ESCRITOR", "CONCEPTO_EMPRESA", "CONCEPTO_PROFESION",
    "CONCEPTO_TRABAJO_OBJ", "CONCEPTO_PROGRAMA_OBJ",
}

TRIGGERS_CONSULTA_MEMORIA = {"CONCEPTO_DEDICAR", "CONCEPTO_OCUPACION"}

TRIGGERS_VERIFICACION_LOGICA = {
    "CONCEPTO_VERDAD_RESP", "CONCEPTO_FALSO", "CONCEPTO_CORRECTO_RESP",
    "CONCEPTO_INCORRECTO_RESP", "CONCEPTO_VERIFICAR",
    "CONCEPTO_VALIDAR_ACCION", "CONCEPTO_CIERTO",
}

# FIX-M-MAT3: TRIGGERS_CALCULO ampliado
TRIGGERS_CALCULO = {
    "CONCEPTO_MULTIPLICACION", "CONCEPTO_POR_OP", "CONCEPTO_SUMA_OP",
    "CONCEPTO_RESTA_OP", "CONCEPTO_DIVISION", "CONCEPTO_POTENCIA",
    "CONCEPTO_RAIZ", "CONCEPTO_CALCULAR", "CONCEPTO_RESULTADO",
    "CONCEPTO_SUMA", "CONCEPTO_RESTA", "CONCEPTO_ENTRE_OP",
    "CONCEPTO_RAIZ_AVANZADA", "CONCEPTO_MODULO", "CONCEPTO_ABS",
    "CONCEPTO_REDONDEO", "CONCEPTO_PORCENTAJE",
    "CONCEPTO_DERIVAR", "CONCEPTO_DERIVADA", "CONCEPTO_DERIVADA_PRIMERA",
    "CONCEPTO_DERIVADA_SEGUNDA", "CONCEPTO_INTEGRAR", "CONCEPTO_INTEGRAL",
    "CONCEPTO_INTEGRAL_DEFINIDA", "CONCEPTO_INTEGRAL_INDEFINIDA",
    "CONCEPTO_LIMITE", "CONCEPTO_SERIE_TAYLOR", "CONCEPTO_SIMPLIFICAR",
    "CONCEPTO_EXPANDIR", "CONCEPTO_FACTORIZAR", "CONCEPTO_RESOLVER_ECUACION",
    "CONCEPTO_EVALUAR",
    # FIX-M-MAT3 NUEVO
    "CONCEPTO_SISTEMA_LINEAL", "CONCEPTO_ESTADISTICA",
    "CONCEPTO_DERIVADA_PARCIAL", "CONCEPTO_INECUACION",
    "CONCEPTO_MCD", "CONCEPTO_MCM", "CONCEPTO_NUMERO_PRIMO",
    "CONCEPTO_COMBINATORIA", "CONCEPTO_POLINOMIO_INFO",
    "CONCEPTO_FUNCION_TRIGONOMETRICA", "CONCEPTO_LOGARITMO",
    "CONCEPTO_EVALUAR_FUNCION", "CONCEPTO_FACTORIAL",
    "CONCEPTO_ECUACION_CUADRATICA",
    # FIX-M-MAT6: fracciones y proporciones en lenguaje natural
    "CONCEPTO_MITAD", "CONCEPTO_TERCIO", "CONCEPTO_CUARTO",
    "CONCEPTO_PROMEDIO", "CONCEPTO_FRACCION", "CONCEPTO_FRACCION_OP",
    "CONCEPTO_PROPORCION", "CONCEPTO_DOBLE", "CONCEPTO_TRIPLE",
    "CONCEPTO_CALCULAR_ACCION",
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
    "CONCEPTO_EXPLICAR": "EXPLICAR", "CONCEPTO_EXPLICAR_V": "EXPLICAR",
    "CONCEPTO_RESUMIR": "RESUMIR", "CONCEPTO_RESUMIR_ACCION": "RESUMIR",
    "CONCEPTO_SIMPLIFICAR": "SIMPLIFICAR", "CONCEPTO_ACLARAR": "ACLARAR",
    "CONCEPTO_COMPARAR": "COMPARAR", "CONCEPTO_REPETIR": "REPETIR",
    "CONCEPTO_DEFINIR": "DEFINIR", "CONCEPTO_TRADUCIR": "TRADUCIR",
    "CONCEPTO_REFORMULAR": "REFORMULAR", "CONCEPTO_ELABORAR": "ELABORAR",
    "CONCEPTO_DECIR": "EXPLICAR", "CONCEPTO_CONTAR": "EXPLICAR",
}

_NUMEROS = {
    "CONCEPTO_UNO_NUM", "CONCEPTO_DOS_NUM", "CONCEPTO_TRES_NUM",
    "CONCEPTO_CUATRO_NUM", "CONCEPTO_CINCO_NUM", "CONCEPTO_SEIS_NUM",
    "CONCEPTO_SIETE_NUM", "CONCEPTO_OCHO_NUM", "CONCEPTO_NUEVE_NUM",
    "CONCEPTO_DIEZ_NUM", "CONCEPTO_VEINTE_NUM", "CONCEPTO_CIEN_NUM",
    "CONCEPTO_MIL_NUM",
}

_OPERADORES_MATEMATICOS = {
    "CONCEPTO_MULTIPLICACION", "CONCEPTO_POR_OP", "CONCEPTO_SUMA_OP",
    "CONCEPTO_RESTA_OP", "CONCEPTO_DIVISION", "CONCEPTO_POTENCIA",
    "CONCEPTO_RAIZ", "CONCEPTO_SUMA", "CONCEPTO_RESTA",
    "CONCEPTO_ENTRE_OP", "CONCEPTO_RAIZ_AVANZADA",
}

_PALABRAS_MAT_AVANZADA = {
    'deriva', 'derivada', 'diferencial', 'integra', 'integral',
    'antiderivada', 'limite', 'lim(', 'taylor', 'serie de',
    'factori', 'simplif', 'expande', 'expand', 'resolv', 'resuelv',
    'soluciones de', 'raices de', 'evalua',
    'estadistica', 'estadística', 'media de', 'promedio de',
    'sistema de ecuaciones', 'mcd', 'mcm', 'primo', 'combinaciones',
    'permutaciones', 'inecuacion', 'inecuación',
}

_VERBOS_CAPACIDAD_MAT = {
    'puedes', 'puedo', 'sabes', 'eres capaz', 'podrias', 'haces',
    'es posible', 'puedes hacer',
}

_PALABRAS_MAT_SIN_EXPR = {
    'deriva', 'derivar', 'derivada', 'derivadas',
    'integra', 'integrar', 'integral', 'integrales',
    'limite', 'limites', 'taylor',
    'factori', 'factorizar', 'simplif', 'simplificar',
    'expande', 'expandir', 'resolver', 'resuelve',
    'calcular', 'calculos', 'matematica', 'matematicas',
    'sumar', 'suma', 'restar', 'resta', 'multiplicar', 'dividir',
    'potencia', 'elevar', 'elevado', 'raiz', 'raices',
    'operar', 'operacion', 'operaciones',
    'estadistica', 'estadísticas', 'media', 'promedio',
    'sistema de ecuaciones', 'mcd', 'mcm',
    'primo', 'combinaciones', 'permutaciones',
    'inecuacion', 'logaritmo', 'logaritmos',
}

_RE_EXPR_MAT = re.compile(
    r'(?:[a-z][\*\+\-]|[\*\+\-][a-z]|\*\*|[a-z]\*\*|sin\(|cos\(|tan\(|sqrt\(|exp\(|log\()',
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


# ═══════════════════════════════════════════════════════════════════════
# MOTOR DE RAZONAMIENTO v10.0
# ═══════════════════════════════════════════════════════════════════════

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
        conceptos = traduccion.get('conceptos', [])
        mensaje   = traduccion.get('texto_original', '')
        confianza = _clamp_certeza(traduccion.get('confianza', 0.0))
        msg_limpio = mensaje.lower().strip() if mensaje else ""

        # Confirmación directa
        if msg_limpio in CONFIRMACIONES_DIRECTAS:
            ids   = {c.id for c in conceptos}
            valor = "NEGATIVA" if (msg_limpio == "no" or ids & TRIGGERS_CONFIRMACION_NEGATIVA) else "POSITIVA"
            return Decision(
                tipo=TipoDecision.CONFIRMACION, certeza=1.0,
                conceptos_principales=[c.id for c in conceptos],
                puede_ejecutar=False,
                razon="Confirmacion directa detectada por texto",
                hechos_reales={
                    "tipo_respuesta": "CONFIRMACION",
                    "valor": valor,
                    "palabra_original": msg_limpio,
                },
            )

        if confianza < 0.3:
            msg_norm_early = _norm(msg_limpio)

            if self._es_ejecucion_shell_directa(msg_norm_early):
                return Decision(
                    tipo=TipoDecision.EJECUCION, certeza=1.0,
                    conceptos_principales=[], puede_ejecutar=True,
                    operacion_disponible="ejecutar_habilidad",
                    razon="patron shell directo con confianza baja",
                    hechos_reales=self._hechos_ejecucion(conceptos, mensaje),
                )

            if self._es_ejecucion_bd_directa(msg_norm_early) or self._es_ejecucion_bd_directa(msg_limpio):
                return Decision(
                    tipo=TipoDecision.EJECUCION, certeza=1.0,
                    conceptos_principales=[], puede_ejecutar=True,
                    operacion_disponible="ejecutar_habilidad",
                    razon="patron BD directo con confianza baja",
                    hechos_reales=self._hechos_ejecucion_bd(conceptos, mensaje),
                )

            if _RE_EXPR_MAT_AVANZADA_CON_VERBO.search(msg_limpio):
                return Decision(
                    tipo=TipoDecision.CALCULO, certeza=0.85,
                    conceptos_principales=[], puede_ejecutar=True,
                    operacion_disponible="ejecutar_habilidad",
                    razon="FIX-M3: expresion matematica avanzada con confianza baja",
                    hechos_reales=self._hechos_calculo(conceptos, mensaje),
                )

            # FIX-M-MAT1: universal con confianza baja
            if _es_matematica_universal(msg_limpio):
                return Decision(
                    tipo=TipoDecision.CALCULO, certeza=0.85,
                    conceptos_principales=[], puede_ejecutar=True,
                    operacion_disponible="ejecutar_habilidad",
                    razon="FIX-M-MAT1: matematica universal detectada con confianza baja",
                    hechos_reales=self._hechos_calculo(conceptos, mensaje),
                )

            if _PATRONES_EXT_DISPONIBLE and _detectar_hab_ext is not None:
                try:
                    resultado_ext = _detectar_hab_ext(msg_norm_early) or _detectar_hab_ext(msg_limpio)
                    if resultado_ext is not None:
                        habilidad_ext_id, tipo_ext = resultado_ext
                        return Decision(
                            tipo=TipoDecision.EJECUCION, certeza=1.0,
                            conceptos_principales=[], puede_ejecutar=True,
                            operacion_disponible="ejecutar_habilidad",
                            razon=f"habilidad externa '{habilidad_ext_id}' con confianza baja",
                            hechos_reales=self._hechos_ejecucion_externa(habilidad_ext_id, tipo_ext, conceptos, mensaje),
                        )
                except Exception:
                    pass

            return self.generador.generar_decision_no_entendido(confianza)

        tipo_semantico = self.clasificar_intencion(conceptos, mensaje)

        if tipo_semantico.name in TIPOS_ACTUALIZAN_ESTADO:
            self._actualizar_estado_memoria(tipo_semantico.name, mensaje)

        if tipo_semantico == TipoDecision.AFIRMATIVA:
            decision = self._resolver_decision(traduccion)
            if not (0.0 <= decision.certeza <= 1.0):
                decision.certeza = _clamp_certeza(decision.certeza)
            return decision

        hechos = self.construir_hechos(tipo_semantico, conceptos, mensaje)
        ids_principales = [c.id for c in conceptos] if conceptos else []

        if tipo_semantico.name in TIPOS_GUARDAN_EN_MEMORIA:
            self._guardar_dato_en_memoria(hechos)

        return Decision(
            tipo=tipo_semantico,
            certeza=confianza,
            conceptos_principales=ids_principales,
            puede_ejecutar=(tipo_semantico in (TipoDecision.CALCULO, TipoDecision.EJECUCION)),
            operacion_disponible=("ejecutar_habilidad" if tipo_semantico in (
                TipoDecision.CALCULO, TipoDecision.EJECUCION) else None),
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
        razon_bloqueo = ""
        for concepto in conceptos:
            if not esta_implementada(concepto.id):
                concepto_bloqueado = concepto
                razon_bloqueo = razon_no_implementada(concepto.id)
                break

        if concepto_bloqueado is not None:
            hechos = self._hechos_capacidad(conceptos, traduccion.get('texto_original', ''))
            hechos['capacidad_bloqueada_id']          = concepto_bloqueado.id
            hechos['capacidad_bloqueada_razon']       = razon_bloqueo
            hechos['capacidad_solicitada_disponible'] = False
            return Decision(
                tipo=TipoDecision.CAPACIDAD_BELL, certeza=1.0,
                conceptos_principales=[c.id for c in conceptos],
                puede_ejecutar=False,
                razon=f"Capacidad no implementada: {razon_bloqueo}",
                hechos_reales=hechos,
            )

        patron, razon_patron = detectar_patron_no_implementado(mensaje)
        if patron:
            hechos = self._hechos_capacidad(conceptos, traduccion.get('texto_original', ''))
            hechos['capacidad_solicitada_disponible'] = False
            hechos['capacidad_bloqueada_razon'] = razon_patron
            return Decision(
                tipo=TipoDecision.CAPACIDAD_BELL, certeza=1.0,
                conceptos_principales=[c.id for c in conceptos],
                puede_ejecutar=False,
                razon=f"Capacidad no implementada por texto: {razon_patron}",
                hechos_reales=hechos,
            )

        return self.generador.generar_decision_capacidad(conceptos, intencion)

    def _actualizar_estado_memoria(self, tipo_nombre: str, mensaje: str):
        mem = self._memoria()
        if not mem:
            return
        try:
            estado = self._detectar_estado_simple(mensaje)
            mem.actualizar_estado_sesion(
                tema_activo=tipo_nombre,
                estado_emocional=estado,
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

        ids  = {c.id for c in conceptos}
        msg  = mensaje.lower().strip() if mensaje else ""
        msg_norm = _norm(msg)

        if self._es_pregunta_capacidad_mat(msg):
            return TipoDecision.CAPACIDAD_BELL

        # FIX-M4: Seguridad — rechazar mensajes con inyección antes de cualquier ejecución shell
        # "lista archivos || echo INYECCION" → DESCONOCIDO (no extraer solo el comando seguro)
        _INYECCION_SHELL = ('||', '&&', '; ', '`', '$(')
        if any(tok in mensaje for tok in _INYECCION_SHELL):
            return TipoDecision.DESCONOCIDO

        tiene_concepto_shell = bool(ids & _CONCEPTOS_SHELL_IDS)
        es_shell_directo     = self._es_ejecucion_shell_directa(msg_norm)
        es_shell_habilidad   = self._es_ejecucion_shell(msg_norm)
        # FIX-M5: si hay verbo de capacidad junto a concepto shell → CAPACIDAD_BELL
        # "eres capaz de ver el disco?" → CAPACIDAD_BELL, no EJECUCION
        if tiene_concepto_shell and (ids & TRIGGERS_CAPACIDAD):
            if not es_shell_directo:
                return TipoDecision.CAPACIDAD_BELL
        if es_shell_directo or (tiene_concepto_shell and es_shell_habilidad):
            return TipoDecision.EJECUCION

        tiene_concepto_bd = bool(ids & _CONCEPTOS_SQLITE_IDS)
        es_bd = self._es_ejecucion_bd_directa(msg_norm) or self._es_ejecucion_bd_directa(msg)
        if tiene_concepto_bd and es_bd:
            return TipoDecision.EJECUCION

        if _PATRONES_EXT_DISPONIBLE and _detectar_hab_ext is not None:
            try:
                if _detectar_hab_ext(msg_norm) is not None or _detectar_hab_ext(msg) is not None:
                    return TipoDecision.EJECUCION
            except Exception:
                pass

        for concepto in conceptos:
            if hasattr(concepto, 'operaciones') and concepto.operaciones:
                if concepto.confianza_grounding >= 0.9:
                    if concepto.id in _CONCEPTOS_SHELL_IDS or concepto.id in _CONCEPTOS_SQLITE_IDS:
                        continue
                    if concepto.id in _CONCEPTOS_MAT_CALCULO:
                        return TipoDecision.CALCULO
                    return TipoDecision.AFIRMATIVA

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
        if ids & TRIGGERS_SOCIAL or self._detectar_social_por_texto(msg):
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

        # FIX-M-MAT7: si hay expresión matemática con números, CALCULO gana sobre CAPACIDAD_BELL
        # "necesito saber cuanto da 7 entre 2" → hay números y "entre" → CALCULO
        if _es_matematica_universal(msg):
            return TipoDecision.CALCULO
        if self._es_calculo_por_texto(msg):
            return TipoDecision.CALCULO

        if ids & TRIGGERS_CAPACIDAD or self._es_pregunta_capacidad_mat(msg):
            return TipoDecision.CAPACIDAD_BELL

        cog = self._detectar_cognitivo_por_texto(msg)
        if cog:
            return TipoDecision.ACCION_COGNITIVA

        triggers_cog = ids & TRIGGERS_ACCION_COGNITIVA
        if triggers_cog:
            solo_ambiguos = triggers_cog <= _CONCEPTOS_COGNITIVOS_AMBIGUOS
            if not (solo_ambiguos and _tiene_expresion_matematica(msg)):
                return TipoDecision.ACCION_COGNITIVA

        if self._es_definicion(msg):
            return TipoDecision.ACCION_COGNITIVA

        if ids & TRIGGERS_CONFIRMACION_POSITIVA:
            if self._es_calculo_por_texto(msg):
                return TipoDecision.CALCULO
            return TipoDecision.CONFIRMACION
        if ids & TRIGGERS_CONFIRMACION_NEGATIVA:
            return TipoDecision.CONFIRMACION
        if ids & TRIGGERS_TEMPORAL:
            return TipoDecision.TEMPORAL
        # FIX-M-MAT7: CALCULO antes de CUANTIFICACION cuando hay matemáticas
        if self._es_calculo(ids, msg):
            return TipoDecision.CALCULO
        if ids & TRIGGERS_CUANTIFICACION:
            # FIX-M3: si hay concepto shell, no ceder a CUANTIFICACION
            # "cuántos núcleos" → EJECUCION, no CUANTIFICACION
            if not (ids & _CONCEPTOS_SHELL_IDS):
                return TipoDecision.CUANTIFICACION
        if ids & TRIGGERS_VERIFICACION_LOGICA:
            return TipoDecision.VERIFICACION_LOGICA
        if self._es_conocimiento_general(ids, msg):
            return TipoDecision.CONOCIMIENTO_GENERAL

        tipo_texto = self._clasificar_por_texto_puro(msg)
        if tipo_texto:
            return tipo_texto

        # FIX-M-MAT6: fallback matemático universal ANTES de DESCONOCIDO
        if _es_matematica_universal(msg):
            return TipoDecision.CALCULO

        return TipoDecision.DESCONOCIDO

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
                if _detectar_hab_ext(msg_norm) is not None or _detectar_hab_ext(msg) is not None:
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
        # FIX-M-MAT6: última oportunidad
        if _es_matematica_universal(msg):
            return TipoDecision.CALCULO
        return None

    def _es_ejecucion_shell(self, msg_norm: str) -> bool:
        if self._habilidad_shell is None:
            return False
        try:
            return self._habilidad_shell.detectar(msg_norm, [], {}) is not None
        except Exception:
            return False

    def _es_ejecucion_shell_directa(self, msg_norm: str) -> bool:
        if not msg_norm:
            return False
        verbos_cap = ['puedes', 'sabes', 'eres capaz', 'podrias', 'es posible', 'puedes hacer', 'sabes hacer', 'tienes capacidad']
        if any(v in msg_norm for v in verbos_cap):
            return False
        return any(p.search(msg_norm) for p in _RE_PATRONES_SHELL)

    def _es_ejecucion_bd_directa(self, msg: str) -> bool:
        if not msg:
            return False
        verbos_cap = ['puedes', 'sabes', 'eres capaz', 'podrias', 'es posible', 'puedes hacer', 'sabes usar', 'tienes capacidad de']
        msg_lower = msg.lower()
        if any(v in msg_lower for v in verbos_cap):
            return False
        return any(p.search(msg) for p in _RE_PATRONES_BD)

    def _es_pregunta_capacidad_mat(self, msg: str) -> bool:
        if _tiene_expresion_matematica(msg):
            return False
        tiene_verbo_cap = any(v in msg for v in _VERBOS_CAPACIDAD_MAT)
        tiene_palabra_mat = any(p in msg for p in _PALABRAS_MAT_SIN_EXPR)
        return tiene_verbo_cap and tiene_palabra_mat

    def _es_consulta_consejera(self, ids: set, msg: str) -> bool:
        for nombre in NOMBRES_CONSEJERAS:
            if nombre in msg:
                verbos = ["que hace", "cual es", "quien es", "hablame", "dime sobre", "cuentame", "rol de", "funcion de", "para que sirve"]
                if any(v in msg for v in verbos):
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
        _PALABRAS_BD_CUANT = {"tabla", "tablas", "registro", "registros", "fila", "filas",
                               "producto", "productos", "usuario", "usuarios", "cliente", "clientes",
                               "elemento", "elementos", "item", "items", "base de datos", "bd",
                               "columna", "columnas", "campo", "campos"}
        if any(p in msg for p in _PALABRAS_BD_CUANT):
            return False
        return any(clave in msg for clave in _CUANTIFICACION_BELL)

    def _es_definicion(self, msg: str) -> bool:
        patrones = [r"qu[e]\s+es\s+", r"qu[e]\s+son\s+", r"qu[e]\s+significa\s+"]
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
        if ids & TRIGGERS_REGISTRO_USUARIO and not msg.endswith('?'):
            return True
        return False

    def _es_consulta_memoria(self, ids: set, msg: str) -> bool:
        if "CONCEPTO_YO" in ids and "CONCEPTO_LLAMAR" in ids:
            if '?' in msg or any(p in msg for p in ['como', 'cual']):
                return True
        if any(p in msg for p in ['sabes', 'recuerdas', 'conoces']):
            if any(p in msg for p in ['nombre', 'edad', 'anos', 'llamo', 'dedico', 'profesion', 'trabajo']):
                return True
        if any(p in msg for p in ['sabes de mi', 'recuerdas de mi', 'tienes sobre mi', 'que sabes', 'me dedico', 'mi profesion']):
            return True
        return False

    def _es_calculo(self, ids: set, msg: str) -> bool:
        if ids & TRIGGERS_CALCULO:
            return True
        if (ids & _OPERADORES_MATEMATICOS) and (ids & _NUMEROS):
            return True
        return self._es_calculo_por_texto(msg)

    def _es_calculo_por_texto(self, msg: str) -> bool:
        """FIX-M-MAT4: ampliado masivamente."""
        if self._es_pregunta_capacidad_mat(msg):
            return False
        if re.search(r'\d+\s*[\+\-\*\/]\s*\d+', msg):
            return True
        if re.search(r'\d+\s*%|\d+\s*por\s+ciento', msg):
            return True
        if any(p in msg for p in _PALABRAS_MAT_AVANZADA):
            return True
        tiene_numero = bool(re.search(r'\d+', msg))
        if tiene_numero:
            ops = ['multiplicado', 'dividido', ' por ', 'mas ', 'menos ', 'cuanto es ', 'al cuadrado',
                   'raiz de', 'elevado', 'entre ', 'por ciento', 'raiz cuadrada', 'factorial de',
                   'seno de', 'coseno de', 'tangente de', 'logaritmo', 'al cubo', 'grados a radianes',
                   'raiz cubica', 'valor absoluto', 'redondea']
            if any(op in msg for op in ops):
                return True
            if re.search(r'raiz\s+de\s+\d+', msg):
                return True
        if re.search(r'(?:media|promedio|mediana|moda|varianza|desviaci[oó]n)\s+de', msg):
            return True
        if re.search(r'calcula\s+(?:la\s+)?(?:media|promedio|mediana|moda|varianza|desviaci[oó]n)', msg):
            return True
        if re.search(r'estadist\w*\s+de', msg):
            return True
        if re.search(r'sistema\s+de\s+ecuaciones?|ecuaciones?\s+simult[aá]neas?', msg):
            return True
        if re.search(r'm\.?c\.?d\.?\s+de\s+\d+|m\.?c\.?m\.?\s+de\s+\d+|'
                     r'm[aá]ximo\s+com[uú]n\s+divisor|m[ií]nimo\s+com[uú]n\s+m[uú]ltiplo', msg):
            return True
        if re.search(r'\d+\s+es\s+primo|es\s+primo\s+\d+|verifica\s+si\s+\d+\s+es\s+primo', msg):
            return True
        if re.search(r'combinaciones?\s+de\s+\d+|permutaciones?\s+de\s+\d+|'
                     r'C\s*\(\s*\d+\s*,\s*\d+\s*\)|P\s*\(\s*\d+\s*,\s*\d+\s*\)', msg):
            return True
        if re.search(r'[a-zA-Z]\s*(?:>|<|>=|<=|≥|≤)\s*\d+|inecuaci[oó]n', msg):
            return True
        if re.search(r'(?:seno|coseno|tangente|secante|cosecante|cotangente)\s+de', msg):
            return True
        if re.search(r'(?:sin|cos|tan)\s*\([^)]+\)', msg):
            return True
        if re.search(r'logaritmo\s+(?:de|natural|base)|ln\s+de\s+|log\s+de\s+', msg):
            return True
        if re.search(r'eval[uú]a[r]?\s+(?:f\s*\(|la\s+funci[oó]n)|'
                     r'valor\s+de\s+f\s*\(|sustituye?\s+[a-z]\s*=', msg):
            return True
        if re.search(r'la\s+mitad\s+de\s+\d+|un\s+tercio\s+de\s+\d+|'
                     r'un\s+cuarto\s+de\s+\d+|tres\s+cuartos\s+de\s+\d+', msg):
            return True
        return False

    def _es_conocimiento_general(self, ids: set, msg: str) -> bool:
        if any(p in msg for p in ['capital de', 'cuando nacio', 'que es la fotosintesis',
                                   'que planeta', 'cuantos habitantes', 'que paso', 'noticias']):
            return True
        if ids <= {'CONCEPTO_DE', 'CONCEPTO_QUE'} and len(msg.split()) > 3:
            return True
        return False

    # ------------------------------------------------------------------
    # CONSTRUCTORES DE HECHOS
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
        """FIX-M-MAT5: incluye tipo_operacion_detectada."""
        numeros = re.findall(r'\d+(?:\.\d+)?', mensaje)
        habilidad_match_id = "CALCULO_BASICO"
        sub_tipo_mat = "BASICO"
        tipo_operacion = _detectar_tipo_mat_especifico(mensaje.lower())

        if _REGISTRO_DISPONIBLE:
            try:
                registro = RegistroHabilidades.obtener()
                if registro:
                    match = registro.detectar(mensaje, conceptos, {})
                    if match:
                        habilidad_match_id = match.habilidad_id
                        sub_tipo_mat = match.parametros.get("sub_tipo", "BASICO")
            except Exception:
                pass

        return {
            "tipo_respuesta":           "CALCULO",
            "expresion_calculo":        mensaje,
            "numeros":                  numeros,
            "puede_ejecutar":           True,
            "mensaje_original":         mensaje,
            "habilidad_match_id":       habilidad_match_id,
            "sub_tipo_mat":             sub_tipo_mat,
            "tipo_operacion_detectada": tipo_operacion,
            "usa_registro":             _REGISTRO_DISPONIBLE,
        }

    def _hechos_ejecucion(self, conceptos: list, mensaje: str) -> dict:
        msg_norm = _norm(mensaje)
        es_bd = self._es_ejecucion_bd_directa(msg_norm) or self._es_ejecucion_bd_directa(mensaje.lower().strip())
        if es_bd:
            return self._hechos_ejecucion_bd(conceptos, mensaje)
        if _PATRONES_EXT_DISPONIBLE and _detectar_hab_ext is not None:
            try:
                resultado_ext = _detectar_hab_ext(msg_norm) or _detectar_hab_ext(mensaje.lower().strip())
                if resultado_ext is not None:
                    habilidad_ext_id, tipo_ext = resultado_ext
                    if habilidad_ext_id != "SQLITE":
                        return self._hechos_ejecucion_externa(habilidad_ext_id, tipo_ext, conceptos, mensaje)
            except Exception:
                pass
        comando_detectado = ""
        descripcion = ""
        if self._habilidad_shell is not None:
            try:
                match = self._habilidad_shell.detectar(msg_norm, conceptos, {})
                if match:
                    comando_detectado = match.parametros.get("comando", "")
                    descripcion = match.parametros.get("descripcion", "")
            except Exception:
                pass
        return {
            "tipo_respuesta": "EJECUCION", "tipo_ejecucion": "shell",
            "habilidad_id": "SHELL", "comando_detectado": comando_detectado,
            "descripcion": descripcion, "puede_ejecutar": True, "mensaje_original": mensaje,
        }

    def _hechos_ejecucion_externa(self, habilidad_id, tipo_ejecucion, conceptos, mensaje) -> dict:
        operacion = ""
        descripcion = ""
        extra = {}
        if _REGISTRO_DISPONIBLE:
            try:
                registro = RegistroHabilidades.obtener()
                habilidad = registro.obtener_habilidad(habilidad_id)
                if habilidad is not None:
                    match = habilidad.detectar(mensaje, conceptos, {})
                    if match:
                        operacion = match.parametros.get("operacion", "")
                        descripcion = match.parametros.get("descripcion", "")
                        extra = {k: v for k, v in match.parametros.items() if k not in ("operacion", "descripcion", "mensaje")}
            except Exception:
                pass
        hechos = {
            "tipo_respuesta": "EJECUCION", "tipo_ejecucion": tipo_ejecucion,
            "habilidad_id": habilidad_id, "operacion": operacion,
            "descripcion": descripcion, "comando_detectado": "",
            "puede_ejecutar": True, "mensaje_original": mensaje,
        }
        hechos.update(extra)
        return hechos

    def _hechos_ejecucion_bd(self, conceptos: list, mensaje: str) -> dict:
        operacion = tabla = descripcion = ""
        if _REGISTRO_DISPONIBLE:
            try:
                registro = RegistroHabilidades.obtener()
                habilidad_sqlite = registro.obtener_habilidad("SQLITE")
                if habilidad_sqlite is not None:
                    match = habilidad_sqlite.detectar(mensaje, conceptos, {})
                    if match:
                        operacion = match.parametros.get("operacion", "")
                        tabla = match.parametros.get("tabla", "")
                        descripcion = match.parametros.get("descripcion", "")
            except Exception:
                pass
        return {
            "tipo_respuesta": "EJECUCION", "tipo_ejecucion": "consulta_bd",
            "habilidad_id": "SQLITE", "operacion": operacion, "tabla": tabla,
            "descripcion": descripcion, "comando_detectado": "",
            "puede_ejecutar": True, "mensaje_original": mensaje,
        }

    def _hechos_identidad(self, conceptos: list, mensaje: str) -> dict:
        # FIX-BUG7: FASE_ACTUAL leído desde capacidades_fase (fuente única)
        total = 1503
        if self.gestor_vocabulario:
            try:
                total = len(self.gestor_vocabulario.obtener_todos())
            except Exception:
                pass
        msg = mensaje.lower() if mensaje else ""
        hechos = {
            "tipo_respuesta":     "IDENTIDAD_BELL",
            "nombre":             "Belladonna",
            "apodo":              "Bell",
            "naturaleza":         "conciencia virtual computacional",
            "creador":            "Sebastian",
            "fase_actual":        FASE_ACTUAL,
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
            "tipo_respuesta": "ESTADO_BELL", "estado": "activa y operativa",
            "activa": True, "funcionando": True, "consejeras_activas": 7,
            "total_conceptos": 1503, "groq_conectado": True,
        }

    def _hechos_capacidad(self, conceptos: list, mensaje: str) -> dict:
        msg = mensaje.lower() if mensaje else ""
        capacidad_solicitada = None
        disponible = True
        razon_bloqueo = ""

        _NEG = {
            "leer archivo": "Leer archivos esta pendiente",
            "crear archivo": "Crear archivos esta pendiente",
            "escribir archivo": "Escribir archivos esta pendiente",
            "generar archivo": "Generar archivos esta pendiente",
            "sesion anterior": "Memoria entre sesiones no disponible",
            "internet": "Acceso a internet no disponible",
            "navegar": "Navegacion web no disponible",
            "imagen": "Procesamiento de imagenes no disponible",
            "archivo": "Leer o crear archivos esta pendiente",
            "descarga": "Descargar archivos de internet no esta implementado",
            "descargar": "Descargar archivos de internet no esta implementado",
        }
        _POS_MAT = {
            "deriva": "Derivadas con SymPy", "derivar": "Derivadas con SymPy",
            "derivada": "Derivadas con SymPy", "integra": "Integrales con SymPy",
            "integrar": "Integrales con SymPy", "integral": "Integrales con SymPy",
            "limite": "Limites con SymPy", "taylor": "Series de Taylor con SymPy",
            "factori": "Factorizacion con SymPy", "simplif": "Simplificacion con SymPy",
            "expande": "Expansion con SymPy", "resolver": "Resolucion de ecuaciones con SymPy",
            "estadistic": "Estadistica descriptiva completa",
            "promedio": "Media, mediana, moda, varianza, desviacion",
            "media": "Media, mediana, moda, varianza, desviacion",
            "mcd": "Maximo comun divisor", "mcm": "Minimo comun multiplo",
            "primo": "Verificacion de numeros primos",
            "combinacion": "Combinaciones C(n,r)", "permutacion": "Permutaciones P(n,r)",
            "inecuacion": "Inecuaciones con SymPy",
        }
        _POS = {
            "calculo": "Calculos matematicos", "python": "Ejecutar codigo Python",
            "terminal": "Ejecutar comandos de terminal", "shell": "Ejecutar comandos de terminal",
            "sqlite": "Consultar y modificar base de datos SQLite",
            "base de datos": "Consultar y modificar base de datos SQLite",
            "tablas": "Listar tablas SQLite", "sql": "Ejecutar SQL (CRUD completo)",
        }

        for keyword, razon in _NEG.items():
            if keyword in msg:
                capacidad_solicitada = keyword
                disponible = False
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
                    disponible = False
                    razon_bloqueo = razon_no_implementada(concepto.id)
                    break
        if disponible and not razon_bloqueo:
            patron, razon = detectar_patron_no_implementado(msg)
            if patron:
                capacidad_solicitada = patron
                disponible = False
                razon_bloqueo = razon

        hechos = {
            "tipo_respuesta": "CAPACIDAD_BELL",
            "capacidades_ejecutables": CAPACIDADES_REALES_BELL["ejecutables"],
            "no_ejecutables": CAPACIDADES_REALES_BELL["NO_ejecutables_aun"],
            "total_conceptos": 1503,
            "capacidad_solicitada": capacidad_solicitada,
            "capacidad_solicitada_disponible": disponible,
        }
        if not disponible and razon_bloqueo:
            hechos["capacidad_bloqueada_razon"] = razon_bloqueo
        return hechos

    def _hechos_social(self, conceptos: list, mensaje: str) -> dict:
        ids = {c.id for c in conceptos}
        msg = mensaje.lower() if mensaje else ""
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
        ids = {c.id for c in conceptos}
        emocion_id = "DESCONOCIDA"
        valencia = "neutra"
        tono = "empatico"
        for c in conceptos:
            props = getattr(c, 'propiedades', {}) or {}
            if props.get('es_estado_emocional') or props.get('valencia'):
                emocion_id = c.id
                valencia = props.get('valencia', 'neutra')
                tono = props.get('tono_recomendado', 'empatico')
                break
        if emocion_id == "DESCONOCIDA":
            for cid in ids:
                if cid in _USUARIO_EMOCIONES:
                    t = _USUARIO_EMOCIONES[cid]
                    emocion_id, valencia, tono = t[0], t[1], t[2]
                    break
        return {
            "tipo_respuesta": "ESTADO_USUARIO", "emocion_detectada": emocion_id,
            "valencia": valencia, "tono_recomendado": tono, "mensaje_original": mensaje,
        }

    def _hechos_accion_cognitiva(self, conceptos: list, mensaje: str) -> dict:
        ids = {c.id for c in conceptos}
        msg = mensaje.lower() if mensaje else ""
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
            "tipo_respuesta": "ACCION_COGNITIVA",
            "accion_solicitada": accion_solicitada,
            "mensaje_original": mensaje,
        }

    def _hechos_confirmacion(self, conceptos: list, mensaje: str) -> dict:
        ids = {c.id for c in conceptos}
        valor = "NEGATIVA" if ids & TRIGGERS_CONFIRMACION_NEGATIVA else "POSITIVA"
        return {
            "tipo_respuesta": "CONFIRMACION",
            "valor": valor,
            "mensaje_original": mensaje,
        }

    def _hechos_temporal(self, conceptos: list, mensaje: str) -> dict:
        return {
            "tipo_respuesta": "TEMPORAL",
            "mensaje_original": mensaje,
            "conceptos_temporales": [c.id for c in conceptos if c.id in TRIGGERS_TEMPORAL],
        }

    def _hechos_cuantificacion(self, conceptos: list, mensaje: str) -> dict:
        msg = mensaje.lower() if mensaje else ""
        dato_preguntado = "desconocido"
        valor_real = None
        for clave, valor in _CUANTIFICACION_BELL.items():
            if clave in msg:
                dato_preguntado = clave
                valor_real = valor
                break
        return {
            "tipo_respuesta": "CUANTIFICACION",
            "dato_preguntado": dato_preguntado,
            "valor_real": valor_real,
            "mensaje_original": mensaje,
        }

    def _hechos_registro_usuario(self, conceptos: list, mensaje: str) -> dict:
        msg = mensaje.lower() if mensaje else ""
        dato_tipo = "desconocido"
        dato_valor = ""
        m = re.search(r'(?:me llamo|mi nombre es|soy)\s+([A-Za-záéíóúñÁÉÍÓÚÑ]{2,})', msg)
        if m:
            dato_tipo = "nombre"
            dato_valor = m.group(1).capitalize()
        m_edad = re.search(r'tengo\s+(\d+)\s*(?:anos?|año)', msg)
        if m_edad:
            dato_tipo = "edad"
            dato_valor = m_edad.group(1)
        return {
            "tipo_respuesta": "REGISTRO_USUARIO",
            "dato_tipo": dato_tipo,
            "dato_valor": dato_valor,
            "mensaje_original": mensaje,
        }

    def _hechos_consulta_memoria(self, conceptos: list, mensaje: str) -> dict:
        return {
            "tipo_respuesta": "CONSULTA_MEMORIA",
            "mensaje_original": mensaje,
        }

    def _hechos_verificacion_logica(self, conceptos: list, mensaje: str) -> dict:
        return {
            "tipo_respuesta": "VERIFICACION_LOGICA",
            "mensaje_original": mensaje,
            "conceptos": [c.id for c in conceptos],
        }

    def _hechos_conocimiento_general(self, conceptos: list, mensaje: str) -> dict:
        return {
            "tipo_respuesta": "CONOCIMIENTO_GENERAL",
            "mensaje_original": mensaje,
        }

    def _hechos_desconocido(self, conceptos: list, mensaje: str) -> dict:
        return {
            "tipo_respuesta": "DESCONOCIDO",
            "mensaje_original": mensaje,
            "conceptos_encontrados": [c.id for c in conceptos],
        }