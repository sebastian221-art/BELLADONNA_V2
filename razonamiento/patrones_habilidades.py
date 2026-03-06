# -*- coding: utf-8 -*-
"""
razonamiento/patrones_habilidades.py  VERSION v2.0

CAMBIOS v2.0 sobre v1.0:
════════════════════════════════════════════════════════════════════
FASE 4B — BD AL 100%: patrones para operaciones de escritura.

NUEVOS PATRONES SQLITE:
  ✅ crear_tabla       — "crea una tabla X", "CREATE TABLE X"
  ✅ insertar          — "inserta a X en Y", "INSERT INTO X"
  ✅ actualizar        — "actualiza X=Y en Z", "UPDATE X SET"
  ✅ eliminar_registro — "elimina a X de Y", "DELETE FROM X WHERE"
  ✅ vaciar_tabla      — "vacía la tabla X", "DELETE FROM X"
  ✅ eliminar_tabla    — "elimina la tabla X", "DROP TABLE X"
  ✅ sql_escritura     — INSERT/UPDATE/DELETE directo

Todo lo demás de v1.0 preservado intacto.

COMPATIBILIDAD: motor_razonamiento v8.9+, generador_salida v8.5+
"""
import re
from typing import Optional, Tuple, List


# ======================================================================
# HABILIDAD: SQLITE — patrones completos v2.0
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

    # ── NUEVO v2.0: Crear tabla ────────────────────────────────────────
    r'crea(?:r)?\s+(?:una\s+)?tabla\s+\w+',
    r'nueva\s+tabla\s+\w+',
    r'hacer\s+(?:una\s+)?tabla\s+\w+',
    r'create\s+table\s+\w+',

    # ── NUEVO v2.0: Insertar ───────────────────────────────────────────
    r'inserta(?:r)?\s+.+\s+en\s+\w+',
    r'agrega(?:r)?\s+.+\s+(?:a|en)\s+\w+',
    r'a[nñ]ade?\s+.+\s+(?:a|en)\s+\w+',
    r'guarda(?:r)?\s+.+\s+en\s+\w+',
    r'^insert\s+into\s+\w+',
    r'nuevo\s+registro\s+en\s+\w+',

    # ── NUEVO v2.0: Actualizar ─────────────────────────────────────────
    r'actualiza(?:r)?\s+.+\s+(?:en|de)\s+\w+',
    r'cambia(?:r)?\s+.+\s+(?:en|de)\s+\w+',
    r'modifica(?:r)?\s+.+\s+(?:en|de)\s+\w+',
    r'^update\s+\w+\s+set',

    # ── NUEVO v2.0: Eliminar registro ──────────────────────────────────
    r'elimin[a-z]*\s+.+\s+de\s+(?:la\s+)?(?:tabla\s+)?\w+',
    r'borra(?:r)?\s+.+\s+de\s+(?:la\s+)?(?:tabla\s+)?\w+',
    r'quita(?:r)?\s+.+\s+de\s+(?:la\s+)?(?:tabla\s+)?\w+',
    r'^delete\s+from\s+\w+\s+where',
    r'^delete\s+from\s+\w+',

    # ── NUEVO v2.0: Vaciar tabla ───────────────────────────────────────
    r'vac[ií]a(?:r)?\s+(?:la\s+)?(?:tabla\s+)?\w+',
    r'limpia(?:r)?\s+(?:la\s+)?(?:tabla\s+)?\w+',
    r'borra(?:r)?\s+todos?\s+(?:los\s+)?registros?\s+de\s+\w+',
    r'elimin[a-z]*\s+todos?\s+(?:los\s+)?registros?\s+de\s+\w+',
    r'^truncate\s+(?:table\s+)?\w+',

    # ── NUEVO v2.0: Eliminar tabla ─────────────────────────────────────
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
# REGISTRO CENTRAL DE PATRONES EXTERNOS
# Agregar una nueva habilidad = agregar una entrada aquí.
# Motor y generador NO necesitan modificarse.
# ======================================================================

PATRONES_EXTERNOS: List[dict] = [
    {
        "habilidad_id":   "SQLITE",
        "tipo_ejecucion": "consulta_bd",
        "patrones":       _PATRONES_SQLITE,
        "conceptos_ids":  _CONCEPTOS_SQLITE,
    },
    # ── Futuras habilidades van aquí ──────────────────────────────────
    # {
    #     "habilidad_id":   "PYTHON_RUNNER",
    #     "tipo_ejecucion": "ejecucion_python",
    #     "patrones":       _PATRONES_PYTHON,
    #     "conceptos_ids":  _CONCEPTOS_PYTHON,
    # },
]


# ======================================================================
# CACHÉ COMPILADA — se construye UNA VEZ al importar
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
# API PÚBLICA — idéntica a v1.0 (motor no necesita cambios)
# ======================================================================

def detectar_habilidad_externa(
    msg_norm: str,
) -> Optional[Tuple[str, str]]:
    """
    Detecta si msg_norm coincide con algún patrón de habilidad externa.
    Retorna (habilidad_id, tipo_ejecucion) o None.
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