# -*- coding: utf-8 -*-
"""
razonamiento/patrones_habilidades.py  VERSION v3.1

CAMBIOS v3.1 sobre v3.0:
════════════════════════════════════════════════════════════════════
FIX-P1  "métricas de Bell", "estadísticas de Bell", "score de Bell"
        → motor detectaba ANALISIS_PYTHON pero _MAPA_ANALISIS en
          analizador_habilidad.py no cubría esas frases → operación vacía.
        FIX: Agregar los patrones que faltan al bloque
             metricas_generales de _PATRONES_ANALISIS_PYTHON para
             que la detección en el motor y en la habilidad sean
             consistentes.

FIX-P2  Consejeras individuales: "analiza nova", "analiza vega",
        "analiza lyra", "analiza luna", "analiza iris", "analiza sage"
        → v3.0 solo tenía nova, vega, echo. Faltaban lyra, luna, iris, sage.
        FIX: Unificar las 7 consejeras en un solo patrón.

FIX-P3  Ruta absoluta Windows/Linux para analizar_archivo:
        "analiza C:\ruta\archivo.py" o "analiza /home/user/archivo.py"
        → v3.0 no tenía estos patrones en _PATRONES_ANALISIS_PYTHON.
        FIX: Agregar patrones de ruta absoluta.

Todo lo demás de v3.0 preservado intacto (SQLITE completo).
════════════════════════════════════════════════════════════════════
"""
import re
from typing import Optional, Tuple, List


# ======================================================================
# HABILIDAD: SQLITE — patrones completos v2.0 (sin cambios)
# ======================================================================

_PATRONES_SQLITE: List[str] = [
    # ── Estado general de la BD ────────────────────────────────────────
    r'estado\s+de\s+(?:tu\s+)?(?:base\s+de\s+datos|bd|sqlite)',
    r'qu[eé]\s+(?:base\s+de\s+datos|bd)\s+tienes',
    r'tienes\s+(?:una\s+)?(?:base\s+de\s+datos|bd)',
    r'muestra(?:me)?\s+(?:tu\s+)?(?:base\s+de\s+datos|bd)',
    r'informacion\s+(?:de\s+)?(?:tu\s+)?(?:base\s+de\s+datos|bd)',

    # ── Listar tablas ──────────────────────────────────────────────────
    r'qu[eé]\s+tablas?\s+(?:hay|tienes|existen)',
    r'lista(?:me)?\s+(?:las\s+)?tablas?',
    r'muestr[a-z]*\s+(?:las\s+)?tablas?',
    r'cu[aá]ntas?\s+tablas?\s+(?:hay|tienes)',
    r'tablas?\s+(?:disponibles?|existentes?)',

    # ── Esquema de tabla ───────────────────────────────────────────────
    r'esquema\s+de\s+(?:la\s+)?(?:tabla\s+)?\w+',
    r'estructura\s+de\s+(?:la\s+)?(?:tabla\s+)?\w+',
    r'columnas?\s+de\s+(?:la\s+)?(?:tabla\s+)?\w+',
    r'campos?\s+de\s+(?:la\s+)?(?:tabla\s+)?\w+',
    r'describe\s+(?:la\s+)?(?:tabla\s+)?\w+',

    # ── Contar registros ───────────────────────────────────────────────
    r'cu[aá]ntos?\s+registros?\s+(?:hay|tiene)',
    r'cu[aá]ntas?\s+filas?\s+(?:hay|tiene)',
    r'total\s+de\s+registros?\s+(?:en|de)\s+\w+',
    r'count\s+(?:de\s+)?\w+',

    # ── Mostrar datos ──────────────────────────────────────────────────
    r'datos?\s+de\s+(?:la\s+)?(?:tabla\s+)?\w+',
    r'contenido\s+de\s+(?:la\s+)?(?:tabla\s+)?\w+',
    r'registros?\s+de\s+(?:la\s+)?(?:tabla\s+)?\w+',
    r'muestra(?:me)?\s+(?:los?\s+)?(?:datos?|registros?)\s+de\s+\w+',

    # ── SQL SELECT ─────────────────────────────────────────────────────
    r'^select\s+.+\s+from\s+\w+',
    r'ejecuta(?:me)?\s+(?:el\s+)?(?:sql|query|consulta)',
    r'consulta\s+sql',
    r'corre\s+(?:el\s+)?(?:sql|query)',

    # ── Índices ────────────────────────────────────────────────────────
    r'[íi]ndices?\s+de\s+(?:la\s+)?(?:tabla\s+)?\w+',
    r'[íi]ndices?\s+(?:disponibles?|existentes?)',

    # ── Crear tabla ────────────────────────────────────────────────────
    r'crea(?:r)?\s+(?:una\s+)?tabla\s+\w+',
    r'nueva\s+tabla\s+\w+',
    r'hacer\s+(?:una\s+)?tabla\s+\w+',
    r'create\s+table\s+\w+',

    # ── Insertar ───────────────────────────────────────────────────────
    r'inserta(?:r)?\s+.+\s+en\s+\w+',
    r'agrega(?:r)?\s+.+\s+(?:a|en)\s+\w+',
    r'a[nñ]ade?\s+.+\s+(?:a|en)\s+\w+',
    r'guarda(?:r)?\s+.+\s+en\s+\w+',
    r'^insert\s+into\s+\w+',
    r'nuevo\s+registro\s+en\s+\w+',

    # ── Actualizar ─────────────────────────────────────────────────────
    r'actualiza(?:r)?\s+.+\s+(?:en|de)\s+\w+',
    r'cambia(?:r)?\s+.+\s+(?:en|de)\s+\w+',
    r'modifica(?:r)?\s+.+\s+(?:en|de)\s+\w+',
    r'^update\s+\w+\s+set',

    # ── Eliminar registro ──────────────────────────────────────────────
    r'elimin[a-z]*\s+.+\s+de\s+(?:la\s+)?(?:tabla\s+)?\w+',
    r'borra(?:r)?\s+.+\s+de\s+(?:la\s+)?(?:tabla\s+)?\w+',
    r'quita(?:r)?\s+.+\s+de\s+(?:la\s+)?(?:tabla\s+)?\w+',
    r'^delete\s+from\s+\w+\s+where',
    r'^delete\s+from\s+\w+',

    # ── Vaciar tabla ───────────────────────────────────────────────────
    r'vac[ií]a(?:r)?\s+(?:la\s+)?(?:tabla\s+)?\w+',
    r'limpia(?:r)?\s+(?:la\s+)?(?:tabla\s+)?\w+',
    r'borra(?:r)?\s+todos?\s+(?:los\s+)?registros?\s+de\s+\w+',
    r'elimin[a-z]*\s+todos?\s+(?:los\s+)?registros?\s+de\s+\w+',
    r'^truncate\s+(?:table\s+)?\w+',

    # ── Eliminar tabla ─────────────────────────────────────────────────
    r'elimin[a-z]*\s+(?:la\s+)?tabla\s+\w+',
    r'borra(?:r)?\s+(?:la\s+)?tabla\s+\w+',
    r'^drop\s+(?:table\s+)?\w+',
    r'destruye?\s+(?:la\s+)?tabla\s+\w+',
]

_CONCEPTOS_SQLITE: List[str] = [
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
    "CONCEPTO_REGISTRO",
    "CONCEPTO_RESULTADO_QUERY",
    "CONCEPTO_TRANSACCION",
    "CONCEPTO_INDICE",
    "CONCEPTO_CONECTAR_BD",
    "CONCEPTO_DESCONECTAR_BD",
]


# ======================================================================
# HABILIDAD: ANALISIS_PYTHON — patrones v3.1
# ======================================================================

_PATRONES_ANALISIS_PYTHON: List[str] = [

    # ── Análisis completo de Bell ──────────────────────────────────────
    r'anali[sz]a(?:r)?\s+(?:tu\s+)?(?:propio\s+)?c[oó]digo',
    r'anali[sz]a(?:r)?\s+(?:a\s+)?bell\b',
    r'anali[sz]a(?:r)?\s+(?:todo\s+)?(?:el\s+)?sistema',
    r'revisa(?:r)?\s+(?:tu\s+)?c[oó]digo',
    r'inspecci[oó]n\s+(?:de\s+)?bell',
    r'c[oó]mo\s+est[aá]\s+(?:tu\s+)?c[oó]digo',
    r'qu[eé]\s+tal\s+(?:tu\s+)?c[oó]digo',
    r'qu[eé]\s+tal\s+est[aá]\s+(?:tu\s+)?c[oó]digo',

    # ── Las 7 consejeras — FIX-P2 ─────────────────────────────────────
    # v3.0 tenía solo nova, vega, echo como patrones separados.
    # v3.1: un solo patrón unificado con todos los nombres.
    r'anali[sz]a(?:r)?\s+(?:la\s+)?(?:consejera\s+)?(nova|vega|echo|lyra|luna|iris|sage)\b',
    r'revisa(?:r)?\s+(?:la\s+)?(?:consejera\s+)?(nova|vega|echo|lyra|luna|iris|sage)\b',
    r'c[oó]mo\s+est[aá]\s+(?:la\s+)?(nova|vega|echo|lyra|luna|iris|sage)\b',
    r'qu[eé]\s+hace\s+(?:la\s+)?(nova|vega|echo|lyra|luna|iris|sage)\b',

    # ── Módulo Bell específico (no-consejera) ──────────────────────────
    r'anali[sz]a(?:r)?\s+(?:el\s+)?motor(?:_razonamiento)?',
    r'anali[sz]a(?:r)?\s+(?:el\s+)?generador(?:_salida|_ejecutores)?',
    r'anali[sz]a(?:r)?\s+(?:el\s+)?registro(?:_habilidades)?',
    r'anali[sz]a(?:r)?\s+(?:el\s+)?m[oó]dulo\s+\w+',
    r'anali[sz]a(?:r)?\s+(?:la\s+)?habilidad\s+\w+',
    r'qu[eé]\s+hace\s+(?:el\s+)?motor',
    r'estructura\s+del?\s+motor',
    r'c[oó]mo\s+est[aá]\s+(?:el\s+)?m[oó]dulo\s+\w+',
    r'qu[eé]\s+contiene\s+(?:el\s+)?m[oó]dulo\s+\w+',
    r'anali[sz]a(?:r)?\s+(?:el\s+)?main',

    # ── Archivo .py por nombre simple ─────────────────────────────────
    r'anali[sz]a(?:r)?\s+\w+\.py',
    r'revisa(?:r)?\s+\w+\.py',
    r'qu[eé]\s+problemas?\s+(?:tiene|hay\s+en)\s+\w+\.py',
    r'complejidad\s+de\s+\w+\.py',
    r'calidad\s+de\s+\w+\.py',
    r'metricas?\s+de\s+\w+\.py',
    r'c[oó]mo\s+est[aá]\s+\w+\.py',
    r'errores?\s+en\s+\w+\.py',
    r'score\s+de\s+\w+\.py',

    # ── Archivo por ruta absoluta — FIX-P3 ────────────────────────────
    # Windows: "analiza C:\ruta\archivo.py"
    r'anali[sz]a(?:r)?\s+[A-Za-z]:\\[^\s]+\.py',
    r'revisa(?:r)?\s+[A-Za-z]:\\[^\s]+\.py',
    # Linux/Mac: "analiza /home/user/archivo.py"
    r'anali[sz]a(?:r)?\s+/[^\s]+\.py',
    r'revisa(?:r)?\s+/[^\s]+\.py',

    # ── Código inline ──────────────────────────────────────────────────
    r'anali[sz]a(?:r)?\s+(?:este\s+)?c[oó]digo',
    r'revisa(?:r)?\s+(?:este\s+)?c[oó]digo',
    r'qu[eé]\s+(?:problemas?|errores?)\s+tiene\s+(?:este\s+)?c[oó]digo',
    r'qu[eé]\s+est[aá]\s+mal\s+(?:en\s+)?(?:este\s+)?c[oó]digo',
    r'qu[eé]\s+piensas?\s+(?:de\s+)?(?:este\s+)?c[oó]digo',
    r'mejora(?:r)?\s+(?:este\s+)?c[oó]digo',
    r'c[oó]mo\s+mejorar[ií]as?\s+(?:este\s+)?c[oó]digo',
    r'analiza\s+(?:el\s+)?siguiente\s+c[oó]digo',
    r'revisa\s+(?:el\s+)?siguiente\s+c[oó]digo',
    r'```python',

    # ── Métricas generales Bell — FIX-P1 ──────────────────────────────
    # v3.0 no cubría "métricas de Bell", "estadísticas de Bell",
    # "score de Bell", "tamaño de Bell". Solo cubría frases con "código".
    r'metricas?\s+(?:del?\s+|de\s+tu\s+)?c[oó]digo',
    r'metricas?\s+de\s+bell',                           # FIX-P1
    r'calidad\s+del?\s+c[oó]digo',
    r'complejidad\s+(?:del?\s+c[oó]digo|de\s+bell)',
    r'qu[eé]\s+tan\s+(?:bueno|complejo|grande)\s+es\s+(?:tu\s+)?c[oó]digo',
    r'qu[eé]\s+tan\s+grande\s+es\s+bell',              # FIX-P1
    r'cu[aá]ntas?\s+l[ií]neas?\s+(?:tiene|tienes)',
    r'cu[aá]ntas?\s+funciones?\s+(?:tiene|tienes)',
    r'cu[aá]ntas?\s+clases?\s+(?:tiene|tienes)',
    r'tama[nñ]o\s+(?:de\s+)?bell',
    r'estad[ií]sticas?\s+(?:de\s+)?bell',              # FIX-P1
    r'estad[ií]sticas?\s+del?\s+c[oó]digo',
    r'resumen\s+del?\s+c[oó]digo',
    r'score\s+(?:de\s+)?bell',                         # FIX-P1
    r'score\s+(?:del?\s+)?c[oó]digo',
    r'cu[aá]nto\s+c[oó]digo\s+(?:tiene|tienes)',       # FIX-P1
    r'cu[aá]ntas?\s+l[ií]neas?\s+(?:tiene|tienes)\s+bell',  # FIX-P1
]

_CONCEPTOS_ANALISIS_PYTHON: List[str] = [
    "CONCEPTO_ANALISIS_CODIGO",
    "CONCEPTO_ANALISIS_PYTHON",
    "CONCEPTO_COMPLEJIDAD_CODIGO",
    "CONCEPTO_CALIDAD_CODIGO",
    "CONCEPTO_METRICAS_CODIGO",
    "CONCEPTO_FUNCION_CODIGO",
    "CONCEPTO_CLASE_CODIGO",
    "CONCEPTO_DOCSTRING",
    "CONCEPTO_IMPORT_CODIGO",
    "CONCEPTO_REFACTORIZAR",
    "CONCEPTO_INTROSPECCION_BELL",
    "CONCEPTO_SCORE_CALIDAD",
    "CONCEPTO_COMPLEJIDAD_MCCABE",
]


# ======================================================================
# REGISTRO CENTRAL DE PATRONES EXTERNOS
# ======================================================================

PATRONES_EXTERNOS: List[dict] = [
    {
        "habilidad_id":   "SQLITE",
        "tipo_ejecucion": "consulta_bd",
        "patrones":       _PATRONES_SQLITE,
        "conceptos_ids":  _CONCEPTOS_SQLITE,
    },
    {
        "habilidad_id":   "ANALISIS_PYTHON",
        "tipo_ejecucion": "analisis_codigo",
        "patrones":       _PATRONES_ANALISIS_PYTHON,
        "conceptos_ids":  _CONCEPTOS_ANALISIS_PYTHON,
    },
    # ── Futuras habilidades van aquí ──────────────────────────────────
]


# ======================================================================
# CACHÉ COMPILADA
# ======================================================================

_CACHE_COMPILADA: List[Tuple[re.Pattern, str, str]] = []


def _compilar_cache() -> None:
    _CACHE_COMPILADA.clear()
    for entrada in PATRONES_EXTERNOS:
        hid  = entrada["habilidad_id"]
        tipo = entrada["tipo_ejecucion"]
        for patron_str in entrada["patrones"]:
            try:
                _CACHE_COMPILADA.append(
                    (re.compile(patron_str, re.IGNORECASE), hid, tipo)
                )
            except re.error:
                pass


_compilar_cache()


# ======================================================================
# API PÚBLICA — idéntica a v3.0
# ======================================================================

def detectar_habilidad_externa(
    msg_norm: str,
) -> Optional[Tuple[str, str]]:
    """
    Detecta si msg_norm coincide con algún patrón de habilidad externa.
    Retorna (habilidad_id, tipo_ejecucion) o None.

    ORDEN DE PRIORIDAD: el primer match gana.
    SQLITE tiene prioridad sobre ANALISIS_PYTHON.
    """
    if not msg_norm:
        return None
    for patron, hid, tipo in _CACHE_COMPILADA:
        if patron.search(msg_norm):
            return (hid, tipo)
    return None


def obtener_todos_los_patrones() -> List[Tuple[re.Pattern, str, str]]:
    return list(_CACHE_COMPILADA)


def obtener_patrones_por_habilidad(habilidad_id: str) -> List[re.Pattern]:
    return [p for p, hid, _ in _CACHE_COMPILADA if hid == habilidad_id]


def obtener_conceptos_por_habilidad(habilidad_id: str) -> List[str]:
    for entrada in PATRONES_EXTERNOS:
        if entrada["habilidad_id"] == habilidad_id:
            return list(entrada["conceptos_ids"])
    return []


def listar_habilidades_registradas() -> List[str]:
    return [entrada["habilidad_id"] for entrada in PATRONES_EXTERNOS]