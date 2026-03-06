# -*- coding: utf-8 -*-
"""
habilidades/sqlite_habilidad.py — VERSION v2.0

CAMBIOS v2.0 sobre v1.0:
════════════════════════════════════════════════════════════════════
FASE 4B — BD AL 100%: Bell puede crear, leer, escribir y eliminar.

NUEVAS OPERACIONES:
  ✅ crear_tabla       — "crea una tabla usuarios con nombre y edad"
  ✅ insertar          — "inserta a Juan con 25 años en usuarios"
  ✅ actualizar        — "actualiza edad=26 donde nombre=Juan en usuarios"
  ✅ eliminar_registro — "elimina a Juan de usuarios" (con WHERE específico)
  ✅ vaciar_tabla      — "vacía la tabla usuarios" (advertencia de Vega)
  ✅ eliminar_tabla    — "elimina la tabla usuarios" (advertencia de Vega)
  ✅ sql_escritura     — INSERT/UPDATE/DELETE directo con análisis de riesgo

OPERACIONES QUE YA EXISTÍAN (preservadas intactas v1.0):
  ✅ estadisticas_bd   — estado general de la BD
  ✅ listar_tablas     — qué tablas hay
  ✅ esquema_tabla     — estructura de una tabla
  ✅ contar_registros  — cuántos registros hay en X
  ✅ select_simple     — muestra los datos de X
  ✅ sql_directo       — SELECT directo (solo lectura)
  ✅ listar_indices    — índices de una tabla

NUEVA LÓGICA DE VEGA (reemplaza bloqueo total):
  VETA (no ejecuta):
    - DELETE/DROP sin WHERE y sin nombre de tabla específico
    - "elimina todos" sin contexto claro
  ADVIERTE (ejecuta con nota):
    - vaciar_tabla, eliminar_tabla → Bell avisa antes de ejecutar
    - DELETE con WHERE → ejecuta normalmente
  APRUEBA sin comentario:
    - INSERT, UPDATE, CREATE TABLE, SELECT

ESCALABILIDAD — para agregar una operación nueva:
  1. Agregar tupla a _MAPA_SQLITE
  2. Agregar elif en _ejecutar_operacion()
  3. Listo.
"""

import re
import logging
from typing import Optional, Any, Dict, Tuple, List

from habilidades.registro_habilidades import (
    BaseHabilidad,
    HabilidadMatch,
    ResultadoHabilidad,
)

logger = logging.getLogger("habilidades.sqlite")


# ======================================================================
# MAPA DE INTENCIÓN → OPERACIÓN SQLite
# Formato: (lista_patrones, operacion_id, descripcion)
# ======================================================================

_MAPA_SQLITE: list = [

    # ── Estado general de la BD ───────────────────────────────────────
    (
        [r'estado\s+de\s+(?:tu\s+)?(?:base\s+de\s+datos|bd|sqlite)',
         r'info(?:rmaci[oó]n)?\s+de\s+(?:la\s+)?(?:base\s+de\s+datos|bd)',
         r'c[oó]mo\s+est[aá]\s+(?:tu\s+)?(?:base\s+de\s+datos|bd)',
         r'resumen\s+de\s+(?:la\s+)?(?:base\s+de\s+datos|bd)',
         r'qu[eé]\s+(?:base\s+de\s+datos|bd)\s+tienes',
         r'tienes\s+(?:una\s+)?(?:base\s+de\s+datos|bd)',
         r'muestra(?:me)?\s+(?:tu\s+)?(?:base\s+de\s+datos|bd)'],
        "estadisticas_bd",
        "Estado de la base de datos",
    ),

    # ── Listar tablas ─────────────────────────────────────────────────
    (
        [r'qu[eé]\s+tablas?\s+(?:hay|tienes|existen)',
         r'lista(?:me)?\s+(?:las\s+)?tablas?',
         r'muestr[a-z]*\s+(?:las\s+)?tablas?',
         r'tablas?\s+(?:disponibles?|existentes?)',
         r'cu[aá]ntas?\s+tablas?\s+(?:hay|tienes)',
         r'tus\s+tablas?',
         r'nombre\s+de\s+(?:las\s+)?tablas?'],
        "listar_tablas",
        "Tablas en la base de datos",
    ),

    # ── Esquema de tabla ──────────────────────────────────────────────
    (
        [r'esquema\s+(?:de\s+(?:la\s+)?(?:tabla\s+)?)?(\w+)',
         r'columnas?\s+de\s+(?:la\s+(?:tabla\s+)?)?(\w+)',
         r'estructura\s+de\s+(?:la\s+(?:tabla\s+)?)?(\w+)',
         r'c[oó]mo\s+es\s+(?:la\s+(?:tabla\s+)?)?(\w+)',
         r'campos?\s+de\s+(?:la\s+(?:tabla\s+)?)?(\w+)',
         r'describe\s+(?:la\s+(?:tabla\s+)?)?(\w+)'],
        "esquema_tabla",
        "Esquema de tabla",
    ),

    # ── Contar registros ──────────────────────────────────────────────
    (
        [r'cu[aá]ntos?\s+registros?\s+(?:hay\s+en|tiene)\s+(\w+)',
         r'total\s+de\s+(?:registros?\s+en\s+)?(\w+)',
         r'cu[aá]ntas?\s+filas?\s+(?:hay\s+en|tiene)\s+(\w+)',
         r'cuenta\s+(?:los\s+registros?\s+de\s+)?(\w+)',
         r'contar\s+(?:registros?\s+de\s+)?(\w+)',
         r'count\s+(?:de\s+)?(\w+)'],
        "contar_registros",
        "Contar registros en tabla",
    ),

    # ── Crear tabla ───────────────────────────────────────────────────
    (
        [r'crea(?:r)?\s+(?:una\s+)?tabla\s+(\w+)',
         r'nueva\s+tabla\s+(\w+)',
         r'crea(?:r)?\s+tabla\s+(\w+)',
         r'hacer\s+(?:una\s+)?tabla\s+(\w+)',
         r'crea(?:me)?\s+(?:una\s+)?tabla\s+(?:llamada?\s+)?(\w+)',
         r'create\s+table\s+(?:if\s+not\s+exists\s+)?(\w+)'],
        "crear_tabla",
        "Crear tabla en la base de datos",
    ),

    # ── Insertar registro ─────────────────────────────────────────────
    (
        [r'inserta(?:r)?\s+(?:a\s+)?(.+?)\s+en\s+(?:la\s+(?:tabla\s+)?)?(\w+)',
         r'agrega(?:r)?\s+(?:a\s+)?(.+?)\s+(?:a|en)\s+(?:la\s+(?:tabla\s+)?)?(\w+)',
         r'a[nñ]ade?\s+(?:a\s+)?(.+?)\s+(?:a|en)\s+(?:la\s+(?:tabla\s+)?)?(\w+)',
         r'guarda(?:r)?\s+(?:a\s+)?(.+?)\s+en\s+(?:la\s+(?:tabla\s+)?)?(\w+)',
         r'insert\s+into\s+(\w+)',
         r'nuevo\s+registro\s+en\s+(\w+)',
         r'a[nñ]ade?\s+registro\s+(?:a|en)\s+(\w+)'],
        "insertar",
        "Insertar registro en tabla",
    ),

    # ── Actualizar registro ───────────────────────────────────────────
    (
        [r'actualiza(?:r)?\s+(?:el\s+)?(\w+)\s+(?:a|=|por)\s+(.+?)\s+(?:donde|en|de)\s+(\w+)',
         r'cambia(?:r)?\s+(?:el\s+)?(\w+)\s+(?:a|=|por)\s+(.+?)\s+(?:en|de)\s+(\w+)',
         r'modifica(?:r)?\s+(?:el\s+)?(\w+)\s+(?:a|=|por)\s+(.+?)\s+(?:en|de)\s+(\w+)',
         r'update\s+(\w+)\s+set',
         r'actualiza(?:r)?\s+(?:en\s+)?(\w+)\s+(?:set\s+)?(\w+)\s*=\s*(.+)',
         # FIX: "actualiza campo=val donde campo=val en tabla"
         r'actualiza(?:r)?\s+\w+=\S+\s+(?:donde|where)\s+.+\s+en\s+(\w+)',
         r'actualiza(?:r)?\s+.+\s+en\s+(\w+)',
         r'cambia(?:r)?\s+.+\s+en\s+(\w+)',
         r'modifica(?:r)?\s+.+\s+en\s+(\w+)'],
        "actualizar",
        "Actualizar registro en tabla",
    ),

    # ── Eliminar registro (con WHERE) ─────────────────────────────────
    (
        [r'elimin[a-z]*\s+(?:al?\s+|a\s+la\s+)?(.+?)\s+de\s+(?:la\s+(?:tabla\s+)?)?(\w+)',
         r'borra(?:r)?\s+(?:al?\s+|a\s+la\s+)?(.+?)\s+de\s+(?:la\s+(?:tabla\s+)?)?(\w+)',
         r'quita(?:r)?\s+(?:al?\s+|a\s+la\s+)?(.+?)\s+de\s+(?:la\s+(?:tabla\s+)?)?(\w+)',
         r'delete\s+from\s+(\w+)\s+where\s+(.+)',
         r'delete\s+from\s+(\w+)'],
        "eliminar_registro",
        "Eliminar registro de tabla",
    ),

    # ── Vaciar tabla ──────────────────────────────────────────────────
    (
        [r'vac[ií]a(?:r)?\s+(?:la\s+(?:tabla\s+)?)?(\w+)',
         r'limpia(?:r)?\s+(?:la\s+(?:tabla\s+)?)?(\w+)',
         r'borra(?:r)?\s+todos?\s+(?:los\s+)?registros?\s+de\s+(?:la\s+(?:tabla\s+)?)?(\w+)',
         r'elimin[a-z]*\s+todos?\s+(?:los\s+)?registros?\s+de\s+(?:la\s+(?:tabla\s+)?)?(\w+)',
         r'truncate\s+(?:table\s+)?(\w+)',
         r'delete\s+from\s+(\w+)\s*$'],
        "vaciar_tabla",
        "Vaciar todos los registros de una tabla",
    ),

    # ── Eliminar tabla (DROP) ─────────────────────────────────────────
    (
        [r'elimin[a-z]*\s+(?:la\s+)?tabla\s+(\w+)',
        r'borra(?:r)?\s+(?:la\s+)?tabla\s+(\w+)',
        r'drop\s+(?:table\s+)?(?:if\s+exists\s+)?(\w+)',
        r'destruye?\s+(?:la\s+)?tabla\s+(\w+)',
        r'quita(?:r)?\s+(?:la\s+)?tabla\s+(\w+)'],
        "eliminar_tabla",
        "Eliminar tabla de la base de datos",
    ),

    # ── SELECT simple (mostrar datos) ─────────────────────────────────
    (
        [r'muestr[a-z]*\s+(?:los\s+datos\s+de\s+)?(?:la\s+(?:tabla\s+)?)?(\w+)',
         r'qu[eé]\s+hay\s+en\s+(?:la\s+(?:tabla\s+)?)?(\w+)',
         r'datos?\s+de\s+(?:la\s+(?:tabla\s+)?)?(\w+)',
         r'contenido\s+de\s+(?:la\s+(?:tabla\s+)?)?(\w+)',
         r'ver\s+(?:la\s+(?:tabla\s+)?)?(\w+)',
         r'registros?\s+de\s+(?:la\s+(?:tabla\s+)?)?(\w+)',
         r'select\s+\*\s+from\s+(\w+)'],
        "select_simple",
        "Mostrar datos de tabla",
    ),

    # ── SQL directo (SELECT) ──────────────────────────────────────────
    (
        [r'^select\s+.+\s+from\s+\w+',
         r'ejecuta(?:me)?\s+(?:el\s+)?(?:sql|query|consulta)[:\s]+(.+)',
         r'corre\s+(?:este\s+)?(?:sql|query)[:\s]+(.+)',
         r'consulta\s+sql[:\s]+(.+)'],
        "sql_directo",
        "Ejecutar consulta SQL SELECT",
    ),

    # ── SQL escritura directa (INSERT/UPDATE/DELETE) ──────────────────
    (
        [r'^insert\s+into\s+\w+',
         r'^update\s+\w+\s+set',
         r'^delete\s+from\s+\w+',
         r'ejecuta(?:me)?\s+(?:este\s+)?(?:sql|query)[:\s]+((?:insert|update|delete).+)',
         r'corre\s+(?:este\s+)?(?:insert|update|delete)[:\s]+(.+)'],
        "sql_escritura",
        "Ejecutar SQL de escritura",
    ),

    # ── Índices ───────────────────────────────────────────────────────
    (
        [r'[ií]ndices?\s+de\s+(?:la\s+(?:tabla\s+)?)?(\w+)',
         r'qu[eé]\s+[ií]ndices?\s+tiene\s+(\w+)',
         r'[ií]ndices?\s+(?:disponibles?|existentes?)',
         r'indices\s+de\s+la\s+bd'],
        "listar_indices",
        "Índices de tabla",
    ),
]

# Palabras que no son nombres de tabla aunque el regex las capture
_NO_SON_TABLAS = frozenset({
    'sql', 'query', 'consulta', 'datos', 'la', 'el', 'una', 'un',
    'los', 'las', 'me', 'te', 'se', 'de', 'en', 'por', 'con',
    'tabla', 'base', 'bd', 'sqlite', 'hay', 'tiene', 'tienes',
    'todos', 'todas', 'todo', 'where', 'set', 'from', 'into',
    'registros', 'registro', 'columna', 'columnas',
})

# Verbos que indican pregunta de capacidad → no ejecutar
_VERBOS_CAPACIDAD = frozenset({
    'puedes', 'sabes', 'eres capaz', 'podrias', 'es posible',
    'puedes hacer', 'sabes usar', 'tienes capacidad de',
    'puedes consultar', 'sabes manejar',
})

# Tipos de columnas SQLite comunes
_TIPOS_COLUMNA = {
    'texto': 'TEXT', 'text': 'TEXT', 'cadena': 'TEXT', 'string': 'TEXT',
    'nombre': 'TEXT', 'email': 'TEXT', 'correo': 'TEXT',
    'numero': 'INTEGER', 'number': 'INTEGER', 'entero': 'INTEGER',
    'integer': 'INTEGER', 'int': 'INTEGER', 'edad': 'INTEGER',
    'cantidad': 'INTEGER', 'id': 'INTEGER',
    'decimal': 'REAL', 'real': 'REAL', 'float': 'REAL', 'precio': 'REAL',
    'fecha': 'TEXT', 'date': 'TEXT', 'datetime': 'TEXT',
    'bool': 'INTEGER', 'booleano': 'INTEGER',
}


# ======================================================================
# DETECTORES AUXILIARES
# ======================================================================

def _detectar_operacion(msg: str) -> Optional[tuple]:
    """
    Busca la primera operación que hace match con el mensaje.
    Retorna (operacion_id, descripcion, tabla_extraida) o None.
    """
    for patrones, operacion_id, descripcion in _MAPA_SQLITE:
        for patron in patrones:
            m = re.search(patron, msg, re.IGNORECASE)
            if m:
                tabla = ""
                if m.lastindex and m.lastindex >= 1 and m.group(1):
                    candidato = m.group(1).strip()
                    if candidato and candidato.lower() not in _NO_SON_TABLAS:
                        tabla = candidato
                return (operacion_id, descripcion, tabla)
    return None


def _analizar_riesgo_sql(sql: str) -> Tuple[str, str]:
    """
    Analiza el nivel de riesgo de una operación SQL.
    Retorna (nivel, descripcion):
      - "BLOQUEAR"  → no ejecutar (destructivo masivo sin contexto)
      - "ADVERTIR"  → ejecutar con nota de advertencia
      - "OK"        → ejecutar normalmente
    """
    sql_upper = sql.strip().upper()
    sql_limpio = sql.strip()

    # SELECT siempre OK
    if sql_upper.startswith("SELECT"):
        return ("OK", "")

    # DROP TABLE sin nombre específico → bloquear
    if re.match(r'DROP\s+TABLE\s*$', sql_upper):
        return ("BLOQUEAR", "DROP TABLE sin especificar qué tabla eliminar.")

    # DROP TABLE con nombre → advertir
    if sql_upper.startswith("DROP"):
        m = re.search(r'DROP\s+(?:TABLE\s+)?(?:IF\s+EXISTS\s+)?(\w+)', sql_upper)
        nombre = m.group(1) if m else "desconocida"
        return ("ADVERTIR", f"Eliminará permanentemente la tabla '{nombre}' y todos sus datos.")

    # DELETE sin WHERE → bloquear (masivo sin filtro)
    if sql_upper.startswith("DELETE"):
        tiene_where = bool(re.search(r'\bWHERE\b', sql_upper))
        if not tiene_where:
            return ("BLOQUEAR",
                "DELETE sin WHERE eliminaría TODOS los registros. "
                "Usa 'vacía la tabla X' si eso es lo que quieres.")
        return ("OK", "")

    # TRUNCATE → advertir
    if sql_upper.startswith("TRUNCATE"):
        return ("ADVERTIR", "TRUNCATE eliminará todos los registros de la tabla.")

    # INSERT, UPDATE, CREATE TABLE → OK
    if sql_upper.startswith(("INSERT", "UPDATE", "CREATE", "ALTER")):
        return ("OK", "")

    return ("BLOQUEAR", f"Operación no reconocida: '{sql_limpio[:30]}'")


def _parsear_columnas_desde_mensaje(mensaje: str) -> Dict[str, str]:
    """
    Intenta extraer columnas y tipos de un mensaje en lenguaje natural.
    Ej: "con nombre y edad" → {"nombre": "TEXT", "edad": "INTEGER"}
    Ej: "con id entero, nombre texto y precio decimal" → {...}
    """
    columnas = {}

    # Primero intentar formato "columna tipo, columna tipo"
    patron_explicito = re.findall(
        r'(\w+)\s+(?:de\s+tipo\s+)?'
        r'(texto|text|integer|int|entero|numero|real|decimal|float|fecha|date|bool|booleano)',
        mensaje, re.IGNORECASE
    )
    for nombre_col, tipo_col in patron_explicito:
        if nombre_col.lower() not in _NO_SON_TABLAS:
            columnas[nombre_col] = _TIPOS_COLUMNA.get(tipo_col.lower(), 'TEXT')

    if columnas:
        return columnas

    # Si no hay tipos explícitos, extraer nombres y asignar tipo por nombre
    # Buscar "con X, Y y Z" o "con X e Y"
    m = re.search(r'con\s+(.+?)(?:\s*$|\s+en\s+|\s+\()', mensaje, re.IGNORECASE)
    if m:
        parte = m.group(1)
        # Separar por comas, "y", "e"
        nombres = re.split(r'[,\s]+(?:y|e)\s+|,\s*', parte)
        for nombre in nombres:
            nombre = nombre.strip().split()[0] if nombre.strip() else ""
            if nombre and len(nombre) >= 2 and nombre.lower() not in _NO_SON_TABLAS:
                # Asignar tipo por nombre conocido o TEXT por defecto
                tipo = _TIPOS_COLUMNA.get(nombre.lower(), 'TEXT')
                columnas[nombre] = tipo

    # Si nada, columnas básicas mínimas
    if not columnas:
        columnas = {"id": "INTEGER", "nombre": "TEXT"}

    return columnas


def _parsear_datos_insercion(mensaje: str, tabla: str, esquema: list) -> Dict[str, Any]:
    """
    Extrae datos a insertar desde un mensaje en lenguaje natural.
    Usa el esquema de la tabla si está disponible.
    Ej: "inserta a Juan con 25 años en usuarios" → {"nombre": "Juan", "edad": 25}
    """
    datos = {}

    if not esquema:
        # Sin esquema: intentar extraer pares clave=valor
        pares = re.findall(r'(\w+)\s*[=:]\s*([^\s,]+)', mensaje)
        for clave, valor in pares:
            if clave.lower() not in _NO_SON_TABLAS:
                datos[clave] = _convertir_valor(valor)
        return datos

    cols = [col['nombre'] for col in esquema if not col.get('pk') or col.get('tipo') != 'INTEGER']
    msg_lower = mensaje.lower()

    # Buscar valores por posición o por nombre de columna en el mensaje
    for col_info in esquema:
        col = col_info['nombre']
        tipo = col_info['tipo']

        # Buscar "col=valor" o "col: valor"
        m = re.search(rf'{re.escape(col)}\s*[=:]\s*([^\s,]+)', mensaje, re.IGNORECASE)
        if m:
            datos[col] = _convertir_valor(m.group(1), tipo)
            continue

        # Para columnas de tipo TEXT: buscar palabras que parezcan nombres
        if tipo == 'TEXT' and col.lower() in ('nombre', 'name', 'titulo', 'title'):
            # Buscar "a Juan", "llamado Juan", etc.
            m = re.search(
                r'(?:a\s+|llamad[oa]\s+|nombre\s+)([A-Z][a-záéíóúñ]+)',
                mensaje
            )
            if m and m.group(1).lower() not in _NO_SON_TABLAS:
                datos[col] = m.group(1)
                continue

        # Para columnas de tipo INTEGER con "X años"
        if tipo == 'INTEGER' and col.lower() in ('edad', 'age', 'años'):
            m = re.search(r'(\d+)\s+a[ñn]os?', msg_lower)
            if m:
                datos[col] = int(m.group(1))
                continue

        # Números sueltos para columnas INTEGER
        if tipo in ('INTEGER', 'REAL'):
            m = re.search(r'\b(\d+(?:\.\d+)?)\b', mensaje)
            if m and col not in datos:
                datos[col] = _convertir_valor(m.group(1), tipo)

    return datos


def _convertir_valor(valor_str: str, tipo: str = None) -> Any:
    """Convierte string a tipo Python apropiado."""
    if tipo in ('INTEGER', 'INT'):
        try:
            return int(valor_str)
        except (ValueError, TypeError):
            pass
    if tipo in ('REAL', 'FLOAT', 'DECIMAL'):
        try:
            return float(valor_str)
        except (ValueError, TypeError):
            pass
    # Auto-detectar
    try:
        return int(valor_str)
    except (ValueError, TypeError):
        pass
    try:
        return float(valor_str)
    except (ValueError, TypeError):
        pass
    # Quitar comillas si las tiene
    return valor_str.strip("'\"")


# ======================================================================
# HABILIDAD SQLITE v2.0
# ======================================================================

class HabilidadSQLite(BaseHabilidad):
    """
    Habilidad SQLite completa para Bell v2.0.

    Vega analiza el riesgo real:
    - BLOQUEA: operaciones masivas sin filtro (DELETE sin WHERE)
    - ADVIERTE: operaciones reversibles con nombre específico (DROP TABLE X)
    - APRUEBA: INSERT, UPDATE con WHERE, CREATE, SELECT
    """

    def __init__(self):
        self._cliente = None
        self._gestor  = None

    @property
    def id(self) -> str:
        return "SQLITE"

    @property
    def descripcion_para_bell(self) -> str:
        return (
            "Base de datos SQLite completa: crear tablas, insertar, "
            "actualizar, eliminar registros, consultar, ver esquemas. "
            "Vega analiza el riesgo real en vez de bloquear todo."
        )

    @property
    def consejeras_requeridas(self) -> list:
        return ["Vega", "Echo"]

    # ------------------------------------------------------------------
    # INYECCIÓN
    # ------------------------------------------------------------------

    def configurar_cliente(self, cliente, gestor=None):
        self._cliente = cliente
        self._gestor  = gestor
        logger.info("HabilidadSQLite v2.0: ClienteSQLite inyectado")

    def _obtener_cliente(self):
        if self._cliente is not None:
            return self._cliente
        try:
            from base_datos.cliente_sqlite import ClienteSQLite
            cliente = ClienteSQLite(":memory:")
            cliente.conectar()
            self._cliente = cliente
            logger.info("HabilidadSQLite: ClienteSQLite creado en memoria (fallback)")
            return cliente
        except ImportError:
            logger.warning("ClienteSQLite no disponible")
            return None

    # ------------------------------------------------------------------
    # DETECCIÓN
    # ------------------------------------------------------------------

    def detectar(self, mensaje: str, conceptos: list, hechos: dict) -> Optional[HabilidadMatch]:
        msg = mensaje.lower().strip() if mensaje else ""
        if not msg:
            return None
        if any(v in msg for v in _VERBOS_CAPACIDAD):
            return None

        resultado = _detectar_operacion(msg)
        if resultado is None:
            return None

        operacion_id, descripcion, tabla = resultado

        return HabilidadMatch(
            habilidad_id="SQLITE",
            confianza=0.90,
            parametros={
                "operacion":   operacion_id,
                "descripcion": descripcion,
                "tabla":       tabla,
                "mensaje":     mensaje,
            },
            habilidad=self,
        )

    # ------------------------------------------------------------------
    # EJECUCIÓN
    # ------------------------------------------------------------------

    def ejecutar(self, match: HabilidadMatch, nombre_usuario: str = "") -> ResultadoHabilidad:
        operacion   = match.parametros.get("operacion", "")
        descripcion = match.parametros.get("descripcion", "")
        tabla       = match.parametros.get("tabla", "")
        mensaje     = match.parametros.get("mensaje", "")

        if not operacion:
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error="No se determinó la operación a ejecutar.",
                tipo_habilidad="SQLITE",
            )

        cliente = self._obtener_cliente()
        if cliente is None:
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error="Base de datos SQLite no disponible.",
                tipo_habilidad="SQLITE",
            )

        if not self._verificar_conexion(cliente):
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error="No hay conexión activa a la base de datos.",
                tipo_habilidad="SQLITE",
            )

        return self._ejecutar_operacion(operacion, descripcion, tabla, mensaje, cliente)

    def _verificar_conexion(self, cliente) -> bool:
        try:
            return cliente.conexion is not None
        except Exception:
            return False

    def _ejecutar_operacion(
        self,
        operacion:   str,
        descripcion: str,
        tabla:       str,
        mensaje:     str,
        cliente:     Any,
    ) -> ResultadoHabilidad:
        try:
            # ── Operaciones de lectura (v1.0) ──────────────────────────
            if operacion == "estadisticas_bd":
                return self._op_estadisticas_bd(cliente)
            elif operacion == "listar_tablas":
                return self._op_listar_tablas(cliente)
            elif operacion == "esquema_tabla":
                return self._op_esquema_tabla(cliente, tabla, mensaje)
            elif operacion == "contar_registros":
                return self._op_contar_registros(cliente, tabla, mensaje)
            elif operacion == "select_simple":
                return self._op_select_simple(cliente, tabla, mensaje)
            elif operacion == "sql_directo":
                return self._op_sql_directo(cliente, mensaje)
            elif operacion == "listar_indices":
                return self._op_listar_indices(cliente, tabla, mensaje)

            # ── Operaciones de escritura (v2.0) ────────────────────────
            elif operacion == "crear_tabla":
                return self._op_crear_tabla(cliente, tabla, mensaje)
            elif operacion == "insertar":
                return self._op_insertar(cliente, tabla, mensaje)
            elif operacion == "actualizar":
                return self._op_actualizar(cliente, tabla, mensaje)
            elif operacion == "eliminar_registro":
                return self._op_eliminar_registro(cliente, tabla, mensaje)
            elif operacion == "vaciar_tabla":
                return self._op_vaciar_tabla(cliente, tabla, mensaje)
            elif operacion == "eliminar_tabla":
                return self._op_eliminar_tabla(cliente, tabla, mensaje)
            elif operacion == "sql_escritura":
                return self._op_sql_escritura(cliente, mensaje)

            else:
                return ResultadoHabilidad(
                    exitoso=False, valor="", descripcion="",
                    error=f"Operación '{operacion}' no implementada.",
                    tipo_habilidad="SQLITE",
                )
        except Exception as e:
            logger.error(f"HabilidadSQLite._ejecutar_operacion error: {e}")
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error=f"Error inesperado: {e}",
                tipo_habilidad="SQLITE",
            )

    # ------------------------------------------------------------------
    # OPERACIONES DE LECTURA (idénticas a v1.0)
    # ------------------------------------------------------------------

    def _op_estadisticas_bd(self, cliente) -> ResultadoHabilidad:
        _TABLAS_INTERNAS = {'sqlite_sequence', 'sqlite_stat1', 'sqlite_stat2',
                            'sqlite_stat3', 'sqlite_stat4', 'sqlite_master'}
        tablas = [t for t in cliente.listar_tablas() if t not in _TABLAS_INTERNAS]
        if not tablas:
            return ResultadoHabilidad(
                exitoso=True,
                valor="La base de datos está vacía (sin tablas creadas todavía).",
                descripcion="Estado de la base de datos",
                pasos=["SELECT name FROM sqlite_master WHERE type='table'"],
                tipo_habilidad="SQLITE", aprobado_vega=True,
            )
        lineas = [f"Base de datos SQLite — {len(tablas)} tabla(s):"]
        for tabla in tablas:
            try:
                total   = cliente.contar(tabla)
                esquema = cliente.obtener_esquema(tabla)
                cols    = len(esquema)
                lineas.append(f"  • {tabla}: {total} registro(s), {cols} columna(s)")
            except Exception:
                lineas.append(f"  • {tabla}: (sin info)")
        return ResultadoHabilidad(
            exitoso=True, valor="\n".join(lineas),
            descripcion="Estado de la base de datos",
            pasos=["listar_tablas()", "contar() + obtener_esquema()"],
            tipo_habilidad="SQLITE", aprobado_vega=True,
        )

    def _op_listar_tablas(self, cliente) -> ResultadoHabilidad:
        # FIX: filtrar tablas internas de SQLite
        _TABLAS_INTERNAS = {'sqlite_sequence', 'sqlite_stat1', 'sqlite_stat2',
                            'sqlite_stat3', 'sqlite_stat4', 'sqlite_master'}
        tablas = [t for t in cliente.listar_tablas() if t not in _TABLAS_INTERNAS]
        if not tablas:
            valor = "No hay tablas en la base de datos todavía."
        else:
            lista = "\n".join(f"  {i+1}. {t}" for i, t in enumerate(tablas))
            valor = f"Tablas en la base de datos ({len(tablas)}):\n{lista}"
        return ResultadoHabilidad(
            exitoso=True, valor=valor,
            descripcion="Tablas en la base de datos",
            pasos=["SELECT name FROM sqlite_master WHERE type='table'"],
            tipo_habilidad="SQLITE", aprobado_vega=True,
        )

    def _op_esquema_tabla(self, cliente, tabla: str, mensaje: str) -> ResultadoHabilidad:
        tabla = self._resolver_tabla(tabla, mensaje, cliente)
        if not tabla:
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error="No identifiqué el nombre de la tabla. Escribe: 'esquema de [tabla]'",
                tipo_habilidad="SQLITE",
            )
        if not cliente.existe_tabla(tabla):
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error=f"La tabla '{tabla}' no existe.{self._sugerir_tablas(cliente)}",
                tipo_habilidad="SQLITE",
            )
        esquema = cliente.obtener_esquema(tabla)
        if not esquema:
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error=f"No pude obtener el esquema de '{tabla}'.",
                tipo_habilidad="SQLITE",
            )
        lineas = [f"Esquema de '{tabla}':"]
        for col in esquema:
            pk      = " [PK]"                      if col.get('pk')      else ""
            nn      = " NOT NULL"                  if col.get('notnull') else ""
            default = f" DEFAULT {col['default']}" if col.get('default') else ""
            lineas.append(f"  • {col['nombre']}: {col['tipo']}{pk}{nn}{default}")
        return ResultadoHabilidad(
            exitoso=True, valor="\n".join(lineas),
            descripcion=f"Esquema de '{tabla}'",
            pasos=[f"PRAGMA table_info({tabla})"],
            tipo_habilidad="SQLITE", aprobado_vega=True,
        )

    def _op_contar_registros(self, cliente, tabla: str, mensaje: str) -> ResultadoHabilidad:
        tabla = self._resolver_tabla(tabla, mensaje, cliente)
        if not tabla:
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error="No identifiqué el nombre de la tabla.",
                tipo_habilidad="SQLITE",
            )
        if not cliente.existe_tabla(tabla):
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error=f"La tabla '{tabla}' no existe.{self._sugerir_tablas(cliente)}",
                tipo_habilidad="SQLITE",
            )
        total = cliente.contar(tabla)
        return ResultadoHabilidad(
            exitoso=True, valor=f"La tabla '{tabla}' tiene {total} registro(s).",
            descripcion=f"Total en '{tabla}'",
            pasos=[f"SELECT COUNT(*) FROM {tabla}"],
            tipo_habilidad="SQLITE", aprobado_vega=True,
        )

    def _op_select_simple(self, cliente, tabla: str, mensaje: str) -> ResultadoHabilidad:
        tabla = self._resolver_tabla(tabla, mensaje, cliente)
        if not tabla:
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error="No identifiqué el nombre de la tabla.",
                tipo_habilidad="SQLITE",
            )
        if not cliente.existe_tabla(tabla):
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error=f"La tabla '{tabla}' no existe.{self._sugerir_tablas(cliente)}",
                tipo_habilidad="SQLITE",
            )
        resultado = cliente.seleccionar(tabla, limit=20)
        if not resultado.exitoso:
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error=f"Error al consultar '{tabla}': {resultado.error}",
                tipo_habilidad="SQLITE",
            )
        if not resultado.filas:
            valor = f"La tabla '{tabla}' está vacía (0 registros)."
        else:
            columnas   = resultado.columnas or [f"col{i}" for i in range(len(resultado.filas[0]))]
            encabezado = " | ".join(columnas)
            separador  = "-" * len(encabezado)
            filas_str  = "\n".join(" | ".join(str(v) for v in fila) for fila in resultado.filas[:20])
            total      = cliente.contar(tabla)
            nota       = f"\n(mostrando {min(20, total)} de {total})" if total > 20 else ""
            valor      = f"Tabla '{tabla}':\n{encabezado}\n{separador}\n{filas_str}{nota}"
        return ResultadoHabilidad(
            exitoso=True, valor=valor,
            descripcion=f"Datos de '{tabla}'",
            pasos=[f"SELECT * FROM {tabla} LIMIT 20"],
            tipo_habilidad="SQLITE", aprobado_vega=True,
        )

    def _op_sql_directo(self, cliente, mensaje: str) -> ResultadoHabilidad:
        sql = self._extraer_sql_select(mensaje)
        if not sql:
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error="No pude extraer la consulta SQL SELECT.",
                tipo_habilidad="SQLITE",
            )
        nivel, razon = _analizar_riesgo_sql(sql)
        if nivel == "BLOQUEAR":
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error=f"Vega bloqueó la consulta: {razon}",
                tipo_habilidad="SQLITE", aprobado_vega=False,
            )
        resultado = cliente.ejecutar_sql(sql)
        if not resultado.exitoso:
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error=f"Error SQL: {resultado.error}",
                tipo_habilidad="SQLITE",
            )
        if not resultado.filas:
            valor = f"Consulta ejecutada. Sin resultados.\nSQL: {sql}"
        else:
            columnas   = resultado.columnas or [f"col{i}" for i in range(len(resultado.filas[0]))]
            encabezado = " | ".join(columnas)
            separador  = "-" * len(encabezado)
            filas_str  = "\n".join(" | ".join(str(v) for v in fila) for fila in resultado.filas[:50])
            valor      = f"Resultado:\n{encabezado}\n{separador}\n{filas_str}\n({len(resultado.filas)} fila(s))"
        return ResultadoHabilidad(
            exitoso=True, valor=valor,
            descripcion="Resultado de consulta SQL",
            pasos=[f"SQL: {sql}"],
            tipo_habilidad="SQLITE", aprobado_vega=True,
        )

    def _op_listar_indices(self, cliente, tabla: str, mensaje: str) -> ResultadoHabilidad:
        tabla = self._resolver_tabla(tabla, mensaje, cliente)
        try:
            if tabla and cliente.existe_tabla(tabla):
                sql      = f"SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='{tabla}'"
                contexto = f" en '{tabla}'"
            else:
                sql      = "SELECT name, tbl_name FROM sqlite_master WHERE type='index'"
                contexto = ""
            resultado = cliente.ejecutar_sql(sql)
            if not resultado.exitoso:
                return ResultadoHabilidad(
                    exitoso=False, valor="", descripcion="",
                    error=f"Error obteniendo índices: {resultado.error}",
                    tipo_habilidad="SQLITE",
                )
            if not resultado.filas:
                valor = f"No hay índices definidos{contexto}."
            else:
                lista = "\n".join(f"  • {fila[0]}" for fila in resultado.filas)
                valor = f"Índices{contexto} ({len(resultado.filas)}):\n{lista}"
            return ResultadoHabilidad(
                exitoso=True, valor=valor, descripcion="Índices",
                pasos=[sql], tipo_habilidad="SQLITE", aprobado_vega=True,
            )
        except Exception as e:
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error=f"Error listando índices: {e}", tipo_habilidad="SQLITE",
            )

    # ------------------------------------------------------------------
    # OPERACIONES DE ESCRITURA (nuevas en v2.0)
    # ------------------------------------------------------------------

    def _op_crear_tabla(self, cliente, tabla: str, mensaje: str) -> ResultadoHabilidad:
        """
        Crea una tabla nueva.
        Detecta columnas desde el mensaje:
          "crea una tabla usuarios con nombre y edad"
          "crea tabla productos con nombre texto, precio decimal e id entero"
        """
        tabla = self._resolver_tabla_escritura(tabla, mensaje)
        if not tabla:
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error="No identifiqué el nombre de la tabla. Escribe: 'crea tabla [nombre] con [columnas]'",
                tipo_habilidad="SQLITE",
            )

        if cliente.existe_tabla(tabla):
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error=f"La tabla '{tabla}' ya existe.{self._sugerir_tablas(cliente)}",
                tipo_habilidad="SQLITE",
            )

        columnas = _parsear_columnas_desde_mensaje(mensaje)

        # Agregar id autoincrement si no está
        columnas_final = {}
        if 'id' not in {k.lower() for k in columnas}:
            columnas_final['id'] = 'INTEGER'

        columnas_final.update(columnas)

        # Construir SQL
        partes_col = []
        for nombre_col, tipo_col in columnas_final.items():
            if nombre_col.lower() == 'id':
                partes_col.append(f"{nombre_col} INTEGER PRIMARY KEY AUTOINCREMENT")
            else:
                partes_col.append(f"{nombre_col} {tipo_col}")

        sql = f"CREATE TABLE IF NOT EXISTS {tabla} ({', '.join(partes_col)})"
        resultado = cliente.ejecutar_sql(sql)

        if not resultado.exitoso:
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error=f"Error creando tabla: {resultado.error}",
                tipo_habilidad="SQLITE",
            )

        # Mostrar esquema creado
        lineas = [f"Tabla '{tabla}' creada con {len(columnas_final)} columna(s):"]
        for nombre_col, tipo_col in columnas_final.items():
            pk = " [PK AUTO]" if nombre_col.lower() == 'id' else ""
            lineas.append(f"  • {nombre_col}: {tipo_col}{pk}")

        return ResultadoHabilidad(
            exitoso=True, valor="\n".join(lineas),
            descripcion=f"Tabla '{tabla}' creada",
            pasos=[sql],
            tipo_habilidad="SQLITE", aprobado_vega=True,
        )

    def _op_insertar(self, cliente, tabla: str, mensaje: str) -> ResultadoHabilidad:
        """
        Inserta un registro.
        "inserta a Juan con 25 años en usuarios"
        "agrega nombre=Pedro edad=30 en empleados"
        """
        tabla = self._resolver_tabla_escritura(tabla, mensaje)
        if not tabla:
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error="No identifiqué la tabla destino. Escribe: 'inserta [datos] en [tabla]'",
                tipo_habilidad="SQLITE",
            )

        if not cliente.existe_tabla(tabla):
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error=f"La tabla '{tabla}' no existe.{self._sugerir_tablas(cliente)}\n"
                      f"Primero créala con: 'crea tabla {tabla} con [columnas]'",
                tipo_habilidad="SQLITE",
            )

        esquema = cliente.obtener_esquema(tabla)
        datos = _parsear_datos_insercion(mensaje, tabla, esquema)

        # Quitar id si es AUTOINCREMENT
        datos_sin_pk = {k: v for k, v in datos.items()
                       if not any(c['nombre'] == k and c.get('pk') and c.get('tipo') == 'INTEGER'
                                  for c in esquema)}

        if not datos_sin_pk:
            cols_disponibles = [c['nombre'] for c in esquema if not (c.get('pk') and c.get('tipo') == 'INTEGER')]
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error=f"No pude extraer los datos a insertar. "
                      f"Columnas disponibles: {', '.join(cols_disponibles)}. "
                      f"Ejemplo: 'inserta nombre=Juan edad=25 en {tabla}'",
                tipo_habilidad="SQLITE",
            )

        resultado = cliente.insertar(tabla, datos_sin_pk)

        if not resultado.exitoso:
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error=f"Error insertando: {resultado.error}",
                tipo_habilidad="SQLITE",
            )

        total = cliente.contar(tabla)
        valores_str = ", ".join(f"{k}={v}" for k, v in datos_sin_pk.items())
        return ResultadoHabilidad(
            exitoso=True,
            valor=f"Registro insertado en '{tabla}':\n  {valores_str}\n  Total ahora: {total} registro(s).",
            descripcion=f"Registro insertado en '{tabla}'",
            pasos=[f"INSERT INTO {tabla} ({', '.join(datos_sin_pk.keys())}) VALUES (...)"],
            tipo_habilidad="SQLITE", aprobado_vega=True,
        )

    def _op_actualizar(self, cliente, tabla: str, mensaje: str) -> ResultadoHabilidad:
        """
        Actualiza registros con WHERE.
        "actualiza edad=26 donde nombre=Juan en usuarios"
        "cambia el precio a 99.9 donde id=1 en productos"
        """
        tabla = self._resolver_tabla_escritura(tabla, mensaje)
        if not tabla:
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error="No identifiqué la tabla. Escribe: 'actualiza [col=val] donde [col=val] en [tabla]'",
                tipo_habilidad="SQLITE",
            )

        if not cliente.existe_tabla(tabla):
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error=f"La tabla '{tabla}' no existe.{self._sugerir_tablas(cliente)}",
                tipo_habilidad="SQLITE",
            )

        # Extraer SET y WHERE del mensaje
        datos_set, where_clause = self._extraer_set_where(mensaje)

        if not datos_set:
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error="No identifiqué qué actualizar. "
                      "Ejemplo: 'actualiza edad=26 donde nombre=Juan en usuarios'",
                tipo_habilidad="SQLITE",
            )

        if not where_clause:
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error="Necesito saber QUÉ registros actualizar (cláusula WHERE). "
                      "Ejemplo: 'actualiza edad=26 donde nombre=Juan en usuarios'",
                tipo_habilidad="SQLITE",
            )

        resultado = cliente.actualizar(tabla, datos_set, where_clause)

        if not resultado.exitoso:
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error=f"Error actualizando: {resultado.error}",
                tipo_habilidad="SQLITE",
            )

        afectados = resultado.filas_afectadas if resultado.filas_afectadas >= 0 else "?"
        valores_str = ", ".join(f"{k}={v}" for k, v in datos_set.items())
        return ResultadoHabilidad(
            exitoso=True,
            valor=f"Actualización en '{tabla}':\n  SET {valores_str}\n  WHERE {where_clause}\n  Registros afectados: {afectados}",
            descripcion=f"Registros actualizados en '{tabla}'",
            pasos=[f"UPDATE {tabla} SET {valores_str} WHERE {where_clause}"],
            tipo_habilidad="SQLITE", aprobado_vega=True,
        )

    def _op_eliminar_registro(self, cliente, tabla: str, mensaje: str) -> ResultadoHabilidad:
        """
        Elimina registros específicos con WHERE.
        "elimina a Juan de usuarios"
        "borra el registro donde id=5 de productos"
        """
        tabla = self._resolver_tabla_escritura(tabla, mensaje)
        if not tabla:
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error="No identifiqué la tabla. Escribe: 'elimina [condición] de [tabla]'",
                tipo_habilidad="SQLITE",
            )

        if not cliente.existe_tabla(tabla):
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error=f"La tabla '{tabla}' no existe.{self._sugerir_tablas(cliente)}",
                tipo_habilidad="SQLITE",
            )

        where_clause = self._extraer_where_eliminacion(mensaje, tabla, cliente)

        if not where_clause:
            total = cliente.contar(tabla)
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error=f"No identifiqué QUÉ eliminar de '{tabla}' ({total} registros). "
                      f"Sé más específico: 'elimina donde nombre=Juan de {tabla}' "
                      f"o usa 'vacía la tabla {tabla}' para eliminar todo.",
                tipo_habilidad="SQLITE",
            )

        # Contar antes
        total_antes = cliente.contar(tabla)
        resultado = cliente.eliminar(tabla, where_clause)

        if not resultado.exitoso:
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error=f"Error eliminando: {resultado.error}",
                tipo_habilidad="SQLITE",
            )

        total_despues = cliente.contar(tabla)
        eliminados = total_antes - total_despues

        return ResultadoHabilidad(
            exitoso=True,
            valor=f"Eliminación en '{tabla}':\n  WHERE {where_clause}\n  Registros eliminados: {eliminados}\n  Quedan: {total_despues} registro(s).",
            descripcion=f"Registros eliminados de '{tabla}'",
            pasos=[f"DELETE FROM {tabla} WHERE {where_clause}"],
            tipo_habilidad="SQLITE", aprobado_vega=True,
        )

    def _op_vaciar_tabla(self, cliente, tabla: str, mensaje: str) -> ResultadoHabilidad:
        """
        Vacía todos los registros de una tabla (ejecuta con nota de advertencia).
        Vega advierte pero NO bloquea — el usuario lo pidió explícitamente.
        """
        tabla = self._resolver_tabla_escritura(tabla, mensaje)
        if not tabla:
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error="No identifiqué la tabla a vaciar.",
                tipo_habilidad="SQLITE",
            )

        if not cliente.existe_tabla(tabla):
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error=f"La tabla '{tabla}' no existe.{self._sugerir_tablas(cliente)}",
                tipo_habilidad="SQLITE",
            )

        total_antes = cliente.contar(tabla)
        exitoso = cliente.vaciar_tabla(tabla)

        if not exitoso:
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error=f"Error vaciando la tabla '{tabla}'.",
                tipo_habilidad="SQLITE",
            )

        return ResultadoHabilidad(
            exitoso=True,
            valor=f"Tabla '{tabla}' vaciada.\n  Se eliminaron {total_antes} registro(s).\n  La tabla sigue existiendo (con 0 registros).",
            descripcion=f"Tabla '{tabla}' vaciada",
            pasos=[f"DELETE FROM {tabla}  -- {total_antes} registros eliminados"],
            tipo_habilidad="SQLITE", aprobado_vega=True,
        )

    def _op_eliminar_tabla(self, cliente, tabla: str, mensaje: str) -> ResultadoHabilidad:
        """
        Elimina una tabla completa (DROP TABLE).
        Ejecuta con nota de advertencia — es irreversible.
        """
        tabla = self._resolver_tabla_escritura(tabla, mensaje)
        if not tabla:
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error="No identifiqué el nombre de la tabla a eliminar.",
                tipo_habilidad="SQLITE",
            )

        if not cliente.existe_tabla(tabla):
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error=f"La tabla '{tabla}' no existe.{self._sugerir_tablas(cliente)}",
                tipo_habilidad="SQLITE",
            )

        total = cliente.contar(tabla)
        exitoso = cliente.eliminar_tabla(tabla)

        if not exitoso:
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error=f"Error eliminando la tabla '{tabla}'.",
                tipo_habilidad="SQLITE",
            )

        return ResultadoHabilidad(
            exitoso=True,
            valor=f"Tabla '{tabla}' eliminada permanentemente.\n  Tenía {total} registro(s). Esta operación es irreversible.",
            descripcion=f"Tabla '{tabla}' eliminada",
            pasos=[f"DROP TABLE IF EXISTS {tabla}"],
            tipo_habilidad="SQLITE", aprobado_vega=True,
        )

    def _op_sql_escritura(self, cliente, mensaje: str) -> ResultadoHabilidad:
        """
        Ejecuta SQL de escritura directo (INSERT/UPDATE/DELETE) con análisis de riesgo.
        """
        sql = self._extraer_sql_completo(mensaje)
        if not sql:
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error="No pude extraer el SQL. Escribe directamente: INSERT INTO..., UPDATE..., DELETE FROM...",
                tipo_habilidad="SQLITE",
            )

        nivel, razon = _analizar_riesgo_sql(sql)

        if nivel == "BLOQUEAR":
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error=f"Vega bloqueó esa operación: {razon}",
                tipo_habilidad="SQLITE", aprobado_vega=False,
            )

        resultado = cliente.ejecutar_sql(sql)

        if not resultado.exitoso:
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error=f"Error SQL: {resultado.error}",
                tipo_habilidad="SQLITE",
            )

        afectados = resultado.filas_afectadas if resultado.filas_afectadas >= 0 else "?"

        if nivel == "ADVERTIR":
            nota = f"\n⚠ Nota: {razon}"
        else:
            nota = ""

        valor = f"SQL ejecutado correctamente.\n  Filas afectadas: {afectados}\n  SQL: {sql[:100]}{nota}"

        return ResultadoHabilidad(
            exitoso=True, valor=valor,
            descripcion="SQL ejecutado",
            pasos=[f"SQL: {sql}"],
            tipo_habilidad="SQLITE", aprobado_vega=True,
        )

    # ------------------------------------------------------------------
    # HELPERS DE ESCRITURA (nuevos en v2.0)
    # ------------------------------------------------------------------

    def _resolver_tabla_escritura(self, tabla: str, mensaje: str) -> str:
        """
        Extrae el nombre de tabla para operaciones de escritura.
        Más agresivo que _resolver_tabla() — no necesita cliente BD.
        """
        if tabla and tabla.isidentifier() and tabla.lower() not in _NO_SON_TABLAS:
            return tabla

        # Buscar "en [tabla]", "de [tabla]", "tabla [tabla]"
        patrones = [
            r'(?:en|de|la\s+tabla|tabla)\s+(\w+)\s*$',
            r'(?:en|de|la\s+tabla|tabla)\s+(\w+)',
            r'(\w+)\s*$',
        ]
        msg_lower = mensaje.lower()
        for patron in patrones:
            m = re.search(patron, msg_lower)
            if m:
                candidato = m.group(1)
                if (candidato and candidato.isidentifier()
                        and candidato.lower() not in _NO_SON_TABLAS
                        and len(candidato) >= 2):
                    return candidato

        return ""

    def _extraer_set_where(self, mensaje: str) -> Tuple[Dict[str, Any], str]:
        """
        Extrae datos SET y cláusula WHERE de un mensaje de actualización.
        "actualiza edad=26 donde nombre=Juan en usuarios"
        → datos={"edad": 26}, where="nombre = 'Juan'"
        """
        datos_set = {}
        where_clause = ""

        # Normalizar separadores
        msg = mensaje.lower()

        # Buscar "donde" o "where" como separador
        separador = re.search(r'\b(?:donde|where)\b', msg, re.IGNORECASE)
        if separador:
            parte_set   = mensaje[:separador.start()]
            parte_where = mensaje[separador.end():]
        else:
            parte_set   = mensaje
            parte_where = ""

        # Extraer pares clave=valor del SET
        pares_set = re.findall(r'(\w+)\s*=\s*([^\s,]+)', parte_set)
        for clave, valor in pares_set:
            if clave.lower() not in _NO_SON_TABLAS:
                datos_set[clave] = _convertir_valor(valor)

        # Extraer WHERE
        if parte_where:
            pares_where = re.findall(r'(\w+)\s*=\s*([^\s,]+)', parte_where)
            condiciones = []
            for clave, valor in pares_where:
                if clave.lower() not in _NO_SON_TABLAS:
                    # Decidir si va con comillas
                    try:
                        int(valor)
                        condiciones.append(f"{clave} = {valor}")
                    except ValueError:
                        try:
                            float(valor)
                            condiciones.append(f"{clave} = {valor}")
                        except ValueError:
                            condiciones.append(f"{clave} = '{valor}'")
            where_clause = " AND ".join(condiciones)

        return datos_set, where_clause

    def _extraer_where_eliminacion(self, mensaje: str, tabla: str, cliente) -> str:
        """
        Extrae la cláusula WHERE para DELETE desde lenguaje natural.
        "elimina a Juan de usuarios" → "nombre = 'Juan'"
        "borra donde id=5 de productos" → "id = 5"
        """
        msg = mensaje.lower()

        # Formato explícito: "donde col=val"
        m = re.search(r'(?:donde|where)\s+(\w+)\s*=\s*([^\s]+)', mensaje, re.IGNORECASE)
        if m:
            clave, valor = m.group(1), m.group(2)
            try:
                int(valor)
                return f"{clave} = {valor}"
            except ValueError:
                return f"{clave} = '{valor}'"

        # Formato "col=val"
        m = re.search(r'(\w+)\s*=\s*([^\s,]+)', mensaje)
        if m:
            clave, valor = m.group(1), m.group(2)
            if clave.lower() not in _NO_SON_TABLAS:
                try:
                    int(valor)
                    return f"{clave} = {valor}"
                except ValueError:
                    return f"{clave} = '{valor}'"

        # Intentar "elimina a [Nombre]" → buscar columna TEXT principal
        esquema = cliente.obtener_esquema(tabla)
        col_texto = next(
            (c['nombre'] for c in esquema
             if c['tipo'] == 'TEXT' and not c.get('pk')),
            None
        )
        if col_texto:
            # Buscar nombre propio o valor después de "a "
            m = re.search(r'\ba\s+(\w+)', mensaje, re.IGNORECASE)
            if m:
                valor = m.group(1)
                if valor.lower() not in _NO_SON_TABLAS:
                    return f"{col_texto} = '{valor}'"

        return ""

    def _extraer_sql_select(self, mensaje: str) -> str:
        """Extrae SQL SELECT del mensaje."""
        m = re.search(
            r'(?:ejecuta(?:me)?|corre|consulta\s+sql)[:\s]+(.+)',
            mensaje, re.IGNORECASE | re.DOTALL
        )
        if m:
            return m.group(1).strip()
        msg_strip = mensaje.strip()
        if msg_strip.upper().startswith("SELECT"):
            return msg_strip
        return ""

    def _extraer_sql_completo(self, mensaje: str) -> str:
        """Extrae cualquier SQL del mensaje (INSERT/UPDATE/DELETE/SELECT)."""
        # Buscar prefijos de extracción
        m = re.search(
            r'(?:ejecuta(?:me)?|corre)[:\s]+(.+)',
            mensaje, re.IGNORECASE | re.DOTALL
        )
        if m:
            return m.group(1).strip()

        # SQL directo al inicio del mensaje
        msg_strip = mensaje.strip()
        sql_upper = msg_strip.upper()
        for prefix in ("INSERT", "UPDATE", "DELETE", "SELECT", "CREATE", "DROP", "ALTER"):
            if sql_upper.startswith(prefix):
                return msg_strip

        return ""

    # ------------------------------------------------------------------
    # HELPERS COMPARTIDOS
    # ------------------------------------------------------------------

    def _resolver_tabla(self, tabla: str, mensaje: str, cliente) -> str:
        """Para operaciones de lectura — igual que v1.0."""
        if tabla and tabla.isidentifier() and tabla.lower() not in _NO_SON_TABLAS:
            return tabla
        if mensaje:
            m = re.search(r'\b(\w{2,})\s*$', mensaje.lower())
            if m:
                candidato = m.group(1)
                if candidato not in _NO_SON_TABLAS and candidato.isidentifier():
                    return candidato
        try:
            tablas = cliente.listar_tablas()
            if len(tablas) == 1:
                return tablas[0]
        except Exception:
            pass
        return ""

    def _sugerir_tablas(self, cliente) -> str:
        try:
            tablas = cliente.listar_tablas()
            if tablas:
                return f" Tablas disponibles: {', '.join(tablas)}."
        except Exception:
            pass
        return ""

    # ------------------------------------------------------------------
    # FORMATEO
    # ------------------------------------------------------------------

    def formatear_respuesta(self, resultado: ResultadoHabilidad, nombre_usuario: str = "") -> str:
        n = f", {nombre_usuario}" if nombre_usuario else ""
        if resultado.exitoso:
            valor = resultado.valor or resultado.descripcion
            return f"{valor}{n}."
        else:
            error = resultado.error or "Error desconocido al operar la base de datos."
            return f"No pude ejecutar esa operación{n}: {error}"


# Necesario para _parsear_datos_insercion
from typing import Any