"""
vocabulario/semana10_base_datos.py — VERSION v4
Vocabulario de Bases de Datos — Fase 4B (COMPLETO Y MAXIMIZADO)

═══════════════════════════════════════════════════════════════════════════════
CAMBIOS v4 sobre v3:

CONCEPTOS MAXIMIZADOS (más palabras para mejor detección):
  ✅ CONCEPTO_INSERT       — +8 palabras: "insert into", "agrega", "añade", etc.
  ✅ CONCEPTO_DELETE       — +6 palabras: "delete from", "eliminar registro de", etc.
  ✅ CONCEPTO_UPDATE       — +6 palabras: "update set", "actualizar en tabla", etc.
  ✅ CONCEPTO_CREAR_TABLA  — +5 palabras: "crea tabla", "hacer tabla", etc.
  ✅ CONCEPTO_SELECT       — +4 palabras: "select from", "consultar tabla", etc.

CONCEPTOS NUEVOS (v4):
  ✅ CONCEPTO_VACIAR_TABLA    — "vaciar tabla", "limpiar tabla", "truncate"
  ✅ CONCEPTO_ELIMINAR_TABLA  — "drop table", "eliminar tabla", "borrar tabla"
  ✅ CONCEPTO_SQL_ESCRITURA   — INSERT/UPDATE/DELETE directo en SQL
  ✅ CONCEPTO_WHERE           — "where", "condición", "filtrar donde"
  ✅ CONCEPTO_INSERTAR_DATOS  — alias natural para insertar

CORRECCIONES v3 PRESERVADAS:
  ✅ CONCEPTO_ROLLBACK: usa "rollback bd", "revertir transacción" 
     (sin conflicto con CONCEPTO_ROLLBACK_PLAN de semana8_planificacion)

TOTAL: 35 conceptos (antes 30)
═══════════════════════════════════════════════════════════════════════════════
"""

from pathlib import Path
import sys

proyecto_path = Path(__file__).parent.parent
sys.path.insert(0, str(proyecto_path))

from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto

cliente_sqlite = None
gestor_bd = None


def configurar_bd(cliente, gestor):
    """Configura cliente y gestor para los conceptos."""
    global cliente_sqlite, gestor_bd
    cliente_sqlite = cliente
    gestor_bd = gestor


def obtener_conceptos_bd():
    """Retorna 35 conceptos de bases de datos — maximizados para Fase 4B."""
    conceptos = []

    # ═══════════════════════════════════════════════════════════════════
    # CONEXIÓN (3)
    # ═══════════════════════════════════════════════════════════════════

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CONECTAR_BD",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "conectar base de datos", "abrir bd", "connect database",
            "iniciar conexión bd", "abrir base de datos", "conectarse a bd",
        ],
        operaciones={'ejecutar': lambda: cliente_sqlite.conectar() if cliente_sqlite else False},
        confianza_grounding=1.0,
        propiedades={'establece': 'conexión', 'necesario_para': 'operaciones'}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DESCONECTAR_BD",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "desconectar", "cerrar bd", "disconnect",
            "cerrar base de datos", "cerrar conexión bd",
        ],
        operaciones={'ejecutar': lambda: cliente_sqlite.desconectar() if cliente_sqlite else None},
        confianza_grounding=1.0,
        propiedades={'libera': 'recursos', 'finaliza': 'sesión'}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CONEXION",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "conexión", "connection", "sesión bd",
            "enlace base de datos", "conexión activa",
        ],
        confianza_grounding=0.95,
        propiedades={'es': 'enlace con BD', 'permite': 'operaciones', 'debe': 'cerrarse'}
    ))

    # ═══════════════════════════════════════════════════════════════════
    # TABLA — ESTRUCTURA (6)
    # ═══════════════════════════════════════════════════════════════════

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TABLA",
        tipo=TipoConcepto.ENTIDAD_DIGITAL,
        palabras_español=[
            "tabla", "table", "relación",
            "tabla de datos", "tabla bd", "tabla sql",
        ],
        confianza_grounding=0.95,
        propiedades={'es': 'estructura de datos', 'contiene': ['filas', 'columnas'], 'almacena': 'registros'}
    ))

    # ✅ MAXIMIZADO v4
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CREAR_TABLA",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "crear tabla", "create table", "nueva tabla",
            "crea tabla", "crea una tabla", "hacer tabla",
            "generar tabla", "definir tabla", "crea la tabla",
            "nueva tabla en bd", "create table if not exists",
        ],
        operaciones={'ejecutar': lambda nombre, cols: cliente_sqlite.crear_tabla(nombre, cols) if cliente_sqlite else False},
        confianza_grounding=1.0,
        propiedades={'define': 'esquema', 'especifica': ['columnas', 'tipos'], 'puede': 'tener primary key'}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ELIMINAR_TABLA",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "eliminar tabla", "drop table", "borrar tabla",
            "elimina la tabla", "borra la tabla", "destruir tabla",
            "drop table if exists", "quitar tabla",
        ],
        operaciones={'ejecutar': lambda tabla: cliente_sqlite.eliminar_tabla(tabla) if cliente_sqlite else False},
        confianza_grounding=1.0,
        propiedades={'elimina': 'tabla y todos sus datos', 'irreversible': True, 'peligroso': True}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LISTAR_TABLAS",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "listar tablas", "show tables", "tablas existentes",
            "qué tablas hay", "qué tablas tienes", "mostrar tablas",
            "ver tablas", "tablas disponibles", "nombre de las tablas",
        ],
        operaciones={'ejecutar': lambda: cliente_sqlite.listar_tablas() if cliente_sqlite else []},
        confianza_grounding=1.0,
        propiedades={'retorna': 'lista de nombres', 'consulta': 'metadata'}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ESQUEMA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "esquema", "schema", "estructura tabla",
            "columnas de tabla", "campos de tabla",
            "describe tabla", "cómo es la tabla",
        ],
        confianza_grounding=0.9,
        propiedades={'define': 'columnas y tipos', 'describe': 'estructura', 'incluye': 'constraints'}
    ))

    # ✅ NUEVO v4
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_VACIAR_TABLA",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "vaciar tabla", "limpiar tabla", "vacía tabla",
            "borrar todos los registros", "eliminar todos los registros",
            "truncate", "truncate table", "dejar tabla vacía",
            "vacía la tabla", "limpia la tabla",
        ],
        operaciones={'ejecutar': lambda tabla: cliente_sqlite.vaciar_tabla(tabla) if cliente_sqlite else False},
        confianza_grounding=1.0,
        propiedades={'elimina': 'todos los registros', 'mantiene': 'estructura tabla', 'irreversible': True}
    ))

    # ═══════════════════════════════════════════════════════════════════
    # CRUD COMPLETO (6)
    # ═══════════════════════════════════════════════════════════════════

    # ✅ MAXIMIZADO v4
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INSERT",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "insert", "insertar", "insert into",
            "agregar registro", "agrega registro",
            "añadir registro", "añade registro",
            "nuevo registro", "guardar en tabla",
            "inserta en", "inserta a", "agrega a",
            "guardar dato en bd", "agregar a tabla",
        ],
        operaciones={'ejecutar': lambda tabla, datos: cliente_sqlite.insertar(tabla, datos) if cliente_sqlite else None},
        confianza_grounding=1.0,
        propiedades={'crea': 'nuevo registro', 'requiere': 'datos', 'puede': 'fallar si existe'}
    ))

    # ✅ NUEVO v4 — alias más natural para insertar
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INSERTAR_DATOS",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "inserta datos", "insertar datos", "cargar datos",
            "guardar datos en tabla", "poblar tabla",
            "llenar tabla", "meter datos", "poner datos en tabla",
        ],
        operaciones={'ejecutar': lambda tabla, datos: cliente_sqlite.insertar(tabla, datos) if cliente_sqlite else None},
        confianza_grounding=1.0,
        propiedades={'crea': 'registros', 'requiere': 'datos y tabla destino'}
    ))

    # ✅ MAXIMIZADO v4
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SELECT",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "select", "seleccionar", "select from",
            "consultar tabla", "ver datos", "mostrar datos",
            "qué hay en tabla", "datos de tabla",
            "listar registros", "ver registros",
        ],
        operaciones={'ejecutar': lambda tabla: cliente_sqlite.seleccionar(tabla) if cliente_sqlite else None},
        confianza_grounding=1.0,
        propiedades={'obtiene': 'datos', 'retorna': 'registros', 'puede': 'filtrar'}
    ))

    # ✅ MAXIMIZADO v4
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_UPDATE",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "update", "actualizar registro", "update set",
            "actualizar en tabla", "modificar registro",
            "cambiar valor en tabla", "editar registro",
            "actualiza en", "cambia en tabla",
            "actualizar datos", "modifica registro",
        ],
        operaciones={'ejecutar': lambda tabla, datos, where: cliente_sqlite.actualizar(tabla, datos, where) if cliente_sqlite else None},
        confianza_grounding=1.0,
        propiedades={'modifica': 'registros existentes', 'requiere': 'WHERE', 'afecta': 'múltiples filas'}
    ))

    # ✅ MAXIMIZADO v4
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DELETE",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "delete", "delete from", "borrar registro",
            "eliminar registro", "eliminar de tabla",
            "elimina de", "borra de tabla",
            "quitar de tabla", "remover registro",
            "elimina registro", "borrar de bd",
        ],
        operaciones={'ejecutar': lambda tabla, where: cliente_sqlite.eliminar(tabla, where) if cliente_sqlite else None},
        confianza_grounding=1.0,
        propiedades={'elimina': 'registros', 'requiere': 'WHERE recomendado', 'irreversible': True}
    ))

    # ✅ NUEVO v4 — SQL de escritura directo
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SQL_ESCRITURA",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "insert into", "update table", "delete from",
            "sql escritura", "sql de modificación",
            "ejecutar insert", "ejecutar update", "ejecutar delete",
            "correr insert", "correr update", "correr delete",
        ],
        operaciones={'ejecutar': lambda sql: cliente_sqlite.ejecutar_sql(sql) if cliente_sqlite else None},
        confianza_grounding=1.0,
        propiedades={'ejecuta': 'SQL de escritura', 'modifica': 'datos BD', 'requiere': 'análisis Vega'}
    ))

    # ═══════════════════════════════════════════════════════════════════
    # COLUMNAS Y TIPOS (4)
    # ═══════════════════════════════════════════════════════════════════

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_COLUMNA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "columna", "column", "campo",
            "atributo tabla", "campo de tabla",
        ],
        confianza_grounding=0.9,
        propiedades={'es': 'atributo', 'tiene': ['nombre', 'tipo'], 'almacena': 'valor específico'}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PRIMARY_KEY",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "primary key", "clave primaria", "pk",
            "llave primaria", "identificador único tabla",
        ],
        confianza_grounding=0.95,
        propiedades={'es': 'identificador único', 'no_puede': 'ser NULL', 'identifica': 'registro'}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TIPO_DATO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "tipo de dato", "data type", "tipo dato",
            "tipo columna", "tipo campo",
        ],
        confianza_grounding=0.9,
        propiedades={'ejemplos': ['INTEGER', 'TEXT', 'REAL', 'BLOB'], 'define': 'qué puede almacenar'}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NULL",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "null", "nulo", "sin valor",
            "valor nulo", "campo vacío bd",
        ],
        confianza_grounding=0.9,
        propiedades={'es': 'ausencia de valor', 'diferente_de': 'cero o vacío', 'puede': 'prohibirse'}
    ))

    # ═══════════════════════════════════════════════════════════════════
    # QUERIES Y FILTROS (5)
    # ═══════════════════════════════════════════════════════════════════

    # ✅ MAXIMIZADO v4
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_WHERE",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "where", "condición", "filtro",
            "donde", "filtrar donde", "condición where",
            "filtrar por", "con condición", "donde sea igual",
        ],
        confianza_grounding=0.95,
        propiedades={'filtra': 'registros', 'usa': 'condiciones lógicas', 'en': 'SELECT, UPDATE, DELETE'}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ORDER_BY",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "order by", "ordenar", "sort",
            "ordenar por", "ordenado por",
        ],
        confianza_grounding=0.9,
        propiedades={'ordena': 'resultados', 'puede': 'ascendente o descendente', 'por': 'una o más columnas'}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LIMIT",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "limit", "límite consulta", "max results",
            "limitar resultados", "máximo de filas",
        ],
        confianza_grounding=0.9,
        propiedades={'limita': 'número de resultados', 'útil_para': 'paginación', 'mejora': 'rendimiento'}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_COUNT",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "count", "contar", "total registros",
            "cuántos registros", "cuántas filas",
            "contar filas", "count de tabla",
        ],
        operaciones={'ejecutar': lambda tabla: cliente_sqlite.contar(tabla) if cliente_sqlite else 0},
        confianza_grounding=1.0,
        propiedades={'retorna': 'número', 'cuenta': 'registros', 'puede': 'filtrar con WHERE'}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RESULTADO_QUERY",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "resultado query", "resultset", "resultado consulta",
            "filas resultado", "resultado sql",
        ],
        confianza_grounding=0.9,
        propiedades={'contiene': ['filas', 'columnas', 'metadata'], 'retornado_por': 'SELECT'}
    ))

    # ═══════════════════════════════════════════════════════════════════
    # TRANSACCIONES (3)
    # ═══════════════════════════════════════════════════════════════════

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TRANSACCION",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "transacción", "transaction", "operación atómica",
            "bloque de operaciones bd", "transacción sql",
        ],
        confianza_grounding=0.95,
        propiedades={'es': 'conjunto de operaciones', 'garantiza': 'atomicidad', 'puede': 'revertirse'}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_COMMIT",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "commit", "confirmar", "guardar cambios",
            "confirmar transacción", "commit bd", "aplicar cambios bd",
        ],
        operaciones={'ejecutar': lambda: gestor_bd.commit() if gestor_bd else None},
        confianza_grounding=1.0,
        propiedades={'confirma': 'transacción', 'hace': 'cambios permanentes', 'finaliza': 'transacción'}
    ))

    # ✅ FIX v3 PRESERVADO: palabras específicas para BD (sin conflicto con ROLLBACK_PLAN)
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ROLLBACK",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "rollback bd",
            "revertir transacción",
            "undo transaction",
            "cancelar transacción",
            "deshacer cambios bd",
            "revertir cambios de base de datos",
        ],
        operaciones={'ejecutar': lambda: gestor_bd.rollback() if gestor_bd else None},
        confianza_grounding=1.0,
        propiedades={'revierte': 'cambios', 'cancela': 'transacción', 'restaura': 'estado anterior'}
    ))

    # ═══════════════════════════════════════════════════════════════════
    # ÍNDICES (2)
    # ═══════════════════════════════════════════════════════════════════

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INDICE",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "índice", "index", "indexación",
            "índice de tabla", "índice sql", "índices disponibles",
        ],
        confianza_grounding=0.95,
        propiedades={'es': 'estructura de optimización', 'acelera': 'búsquedas', 'costo': 'espacio y tiempo de inserción'}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CREAR_INDICE",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "crear índice", "create index",
            "nuevo índice", "indexar columna",
        ],
        operaciones={'ejecutar': lambda nombre, tabla, cols: gestor_bd.crear_indice(nombre, tabla, cols) if gestor_bd else False},
        confianza_grounding=1.0,
        propiedades={'crea': 'índice', 'sobre': 'una o más columnas', 'puede': 'ser único'}
    ))

    # ═══════════════════════════════════════════════════════════════════
    # SQLITE Y SQL GENERAL (5)
    # ═══════════════════════════════════════════════════════════════════

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SQLITE",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "sqlite", "base de datos embebida",
            "base de datos sqlite", "bd sqlite", "sqlite3",
        ],
        confianza_grounding=0.95,
        propiedades={'es': 'BD relacional', 'sin': 'servidor', 'archivo': 'único', 'usado_en': 'aplicaciones locales'}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SQL",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "sql", "structured query language", "lenguaje consultas",
            "consulta sql", "query sql", "lenguaje sql",
        ],
        confianza_grounding=0.95,
        propiedades={'es': 'lenguaje', 'para': 'bases de datos relacionales', 'incluye': ['DDL', 'DML', 'DCL']}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_REGISTRO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "registro", "fila", "row", "tupla",
            "entrada bd", "dato en tabla",
        ],
        confianza_grounding=0.9,
        propiedades={'es': 'fila de datos', 'contiene': 'valores de columnas', 'representa': 'entidad'}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RESPALDAR",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "respaldar", "backup", "copia de seguridad",
            "respaldo bd", "backup bd", "copia bd",
        ],
        operaciones={'ejecutar': lambda ruta: gestor_bd.respaldar(ruta) if gestor_bd else False},
        confianza_grounding=1.0,
        propiedades={'crea': 'copia BD', 'preserva': 'datos', 'permite': 'recuperación'}
    ))

    # ✅ NUEVO v4 — cubre "base de datos" como concepto general
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_BASE_DATOS",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "base de datos", "bd", "database",
            "mi base de datos", "tu base de datos",
            "estado de la bd", "qué bd tienes",
        ],
        confianza_grounding=0.95,
        propiedades={'es': 'sistema de almacenamiento', 'contiene': 'tablas', 'tipo': 'SQLite en Bell'}
    ))

    return conceptos


if __name__ == '__main__':
    conceptos = obtener_conceptos_bd()
    print(f"✅ Vocabulario BD v4: {len(conceptos)} conceptos")  # 34

    con_operacion = sum(1 for c in conceptos if hasattr(c, 'operaciones') and c.operaciones)
    con_grounding_1 = sum(1 for c in conceptos if c.confianza_grounding == 1.0)
    grounding_prom = sum(c.confianza_grounding for c in conceptos) / len(conceptos)

    print(f"   Con operación ejecutable : {con_operacion}")
    print(f"   Grounding 1.0            : {con_grounding_1}")
    print(f"   Grounding promedio       : {grounding_prom:.2f}")
    print()
    print("   Conceptos nuevos en v4:")
    nuevos = [
        "CONCEPTO_VACIAR_TABLA", "CONCEPTO_ELIMINAR_TABLA",
        "CONCEPTO_SQL_ESCRITURA", "CONCEPTO_INSERTAR_DATOS",
        "CONCEPTO_BASE_DATOS",
    ]
    for n in nuevos:
        print(f"   ✅ {n}")
    print()
    print("   Conceptos maximizados en v4:")
    maximizados = [
        "CONCEPTO_INSERT", "CONCEPTO_DELETE", "CONCEPTO_UPDATE",
        "CONCEPTO_CREAR_TABLA", "CONCEPTO_SELECT", "CONCEPTO_WHERE",
    ]
    for m in maximizados:
        print(f"   ✅ {m}")