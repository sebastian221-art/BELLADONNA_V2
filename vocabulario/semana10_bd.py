"""
Vocabulario de Bases de Datos - Semana 10 (Fase 3 FINAL) - VERSIÓN CORREGIDA v3.
30 conceptos relacionados con SQLite y bases de datos.

═══════════════════════════════════════════════════════════════════════════════
CORRECCIONES FASE 4A:
- ✅ CONCEPTO_ROLLBACK: ELIMINADO "rollback", "revertir", "deshacer"
     (conflicto con CONCEPTO_ROLLBACK_PLAN de semana8_planificacion)
     Ahora usa: "rollback bd", "revertir transacción", "undo transaction"
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
    """Retorna 30 conceptos de bases de datos."""
    conceptos = []
    
    # ========== CONEXIÓN (3) ==========
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CONECTAR_BD",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["conectar base de datos", "abrir bd", "connect database"],
        operaciones={'ejecutar': lambda: cliente_sqlite.conectar() if cliente_sqlite else False},
        confianza_grounding=1.0,
        propiedades={'establece': 'conexión', 'necesario_para': 'operaciones'}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DESCONECTAR_BD",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["desconectar", "cerrar bd", "disconnect"],
        operaciones={'ejecutar': lambda: cliente_sqlite.desconectar() if cliente_sqlite else None},
        confianza_grounding=1.0,
        propiedades={'libera': 'recursos', 'finaliza': 'sesión'}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CONEXION",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["conexión", "connection", "sesión bd"],
        confianza_grounding=0.95,
        propiedades={'es': 'enlace con BD', 'permite': 'operaciones', 'debe': 'cerrarse'}
    ))
    
    # ========== TABLA (5) ==========
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TABLA",
        tipo=TipoConcepto.ENTIDAD_DIGITAL,
        palabras_español=["tabla", "table", "relación"],
        confianza_grounding=0.95,
        propiedades={'es': 'estructura de datos', 'contiene': ['filas', 'columnas'], 'almacena': 'registros'}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CREAR_TABLA",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["crear tabla", "create table", "nueva tabla"],
        operaciones={'ejecutar': lambda nombre, cols: cliente_sqlite.crear_tabla(nombre, cols) if cliente_sqlite else False},
        confianza_grounding=1.0,
        propiedades={'define': 'esquema', 'especifica': ['columnas', 'tipos'], 'puede': 'tener primary key'}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ELIMINAR_TABLA",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["eliminar tabla", "drop table", "borrar tabla"],
        operaciones={'ejecutar': lambda tabla: cliente_sqlite.eliminar_tabla(tabla) if cliente_sqlite else False},
        confianza_grounding=1.0,
        propiedades={'elimina': 'tabla y datos', 'irreversible': True, 'peligroso': True}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LISTAR_TABLAS",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["listar tablas", "show tables", "tablas existentes"],
        operaciones={'ejecutar': lambda: cliente_sqlite.listar_tablas() if cliente_sqlite else []},
        confianza_grounding=1.0,
        propiedades={'retorna': 'lista de nombres', 'consulta': 'metadata'}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ESQUEMA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["esquema", "schema", "estructura tabla"],
        confianza_grounding=0.9,
        propiedades={'define': 'columnas y tipos', 'describe': 'estructura', 'incluye': 'constraints'}
    ))
    
    # ========== CRUD (4) ==========
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INSERT",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["insert", "insertar", "agregar registro"],
        operaciones={'ejecutar': lambda tabla, datos: cliente_sqlite.insertar(tabla, datos) if cliente_sqlite else None},
        confianza_grounding=1.0,
        propiedades={'crea': 'nuevo registro', 'requiere': 'datos', 'puede': 'fallar si existe'}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SELECT",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["select", "seleccionar"],
        operaciones={'ejecutar': lambda tabla: cliente_sqlite.seleccionar(tabla) if cliente_sqlite else None},
        confianza_grounding=1.0,
        propiedades={'obtiene': 'datos', 'retorna': 'registros', 'puede': 'filtrar'}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_UPDATE",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["update", "actualizar registro"],
        operaciones={'ejecutar': lambda tabla, datos, where, params: cliente_sqlite.actualizar(tabla, datos, where, params) if cliente_sqlite else None},
        confianza_grounding=1.0,
        propiedades={'modifica': 'registros existentes', 'requiere': 'WHERE', 'afecta': 'múltiples filas'}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DELETE",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["delete", "borrar registro"],
        operaciones={'ejecutar': lambda tabla, where, params: cliente_sqlite.eliminar(tabla, where, params) if cliente_sqlite else None},
        confianza_grounding=1.0,
        propiedades={'elimina': 'registros', 'requiere': 'WHERE', 'irreversible': True}
    ))
    
    # ========== COLUMNAS Y TIPOS (4) ==========
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_COLUMNA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["columna", "column", "campo"],
        confianza_grounding=0.9,
        propiedades={'es': 'atributo', 'tiene': ['nombre', 'tipo'], 'almacena': 'valor específico'}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PRIMARY_KEY",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["primary key", "clave primaria", "pk"],
        confianza_grounding=0.95,
        propiedades={'es': 'identificador único', 'no_puede': 'ser NULL', 'identifica': 'registro'}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TIPO_DATO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["tipo de dato", "data type", "tipo dato"],
        confianza_grounding=0.9,
        propiedades={'ejemplos': ['INTEGER', 'TEXT', 'REAL', 'BLOB'], 'define': 'qué puede almacenar'}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NULL",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["null", "nulo", "sin valor"],
        confianza_grounding=0.9,
        propiedades={'es': 'ausencia de valor', 'diferente_de': 'cero o vacío', 'puede': 'prohibirse'}
    ))
    
    # ========== QUERIES (4) ==========
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_WHERE",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["where", "condición", "filtro"],
        confianza_grounding=0.95,
        propiedades={'filtra': 'registros', 'usa': 'condiciones lógicas', 'en': 'SELECT, UPDATE, DELETE'}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ORDER_BY",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["order by", "ordenar", "sort"],
        confianza_grounding=0.9,
        propiedades={'ordena': 'resultados', 'puede': 'ascendente o descendente', 'por': 'una o más columnas'}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LIMIT",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["limit", "límite consulta", "max results"],
        confianza_grounding=0.9,
        propiedades={'limita': 'número de resultados', 'útil_para': 'paginación', 'mejora': 'rendimiento'}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_COUNT",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["count", "contar", "total registros"],  # ← Este MANTIENE "count"
        operaciones={'ejecutar': lambda tabla: cliente_sqlite.contar(tabla) if cliente_sqlite else 0},
        confianza_grounding=1.0,
        propiedades={'retorna': 'número', 'cuenta': 'registros', 'puede': 'filtrar con WHERE'}
    ))
    
    # ========== TRANSACCIONES (3) ==========
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TRANSACCION",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["transacción", "transaction", "operación atómica"],
        confianza_grounding=0.95,
        propiedades={'es': 'conjunto de operaciones', 'garantiza': 'atomicidad', 'puede': 'revertirse'}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_COMMIT",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["commit", "confirmar", "guardar cambios"],
        operaciones={'ejecutar': lambda: gestor_bd.commit() if gestor_bd else None},
        confianza_grounding=1.0,
        propiedades={'confirma': 'transacción', 'hace': 'cambios permanentes', 'finaliza': 'transacción'}
    ))
    
    # ═══════════════════════════════════════════════════════════════════════
    # ✅ FIX: CONCEPTO_ROLLBACK - Palabras específicas para BD
    #    ELIMINADO: "rollback", "revertir", "deshacer" (conflicto con ROLLBACK_PLAN)
    # ═══════════════════════════════════════════════════════════════════════
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ROLLBACK",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "rollback bd",           # ← Específico para BD
            "revertir transacción",  # ← Específico para transacciones
            "undo transaction",      # ← En inglés, claro
            "cancelar transacción"   # ← Alternativa en español
        ],
        operaciones={'ejecutar': lambda: gestor_bd.rollback() if gestor_bd else None},
        confianza_grounding=1.0,
        propiedades={'revierte': 'cambios', 'cancela': 'transacción', 'restaura': 'estado anterior'}
    ))
    
    # ========== ÍNDICES (2) ==========
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INDICE",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["índice", "index", "indexación"],
        confianza_grounding=0.95,
        propiedades={'es': 'estructura de optimización', 'acelera': 'búsquedas', 'costo': 'espacio y tiempo de inserción'}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CREAR_INDICE",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["crear índice", "create index"],
        operaciones={'ejecutar': lambda nombre, tabla, cols: gestor_bd.crear_indice(nombre, tabla, cols) if gestor_bd else False},
        confianza_grounding=1.0,
        propiedades={'crea': 'índice', 'sobre': 'una o más columnas', 'puede': 'ser único'}
    ))
    
    # ========== OTROS (5) ==========
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SQLITE",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["sqlite", "base de datos embebida"],
        confianza_grounding=0.95,
        propiedades={'es': 'BD relacional', 'sin': 'servidor', 'archivo': 'único', 'usado_en': 'aplicaciones locales'}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SQL",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["sql", "structured query language", "lenguaje consultas"],
        confianza_grounding=0.95,
        propiedades={'es': 'lenguaje', 'para': 'bases de datos relacionales', 'incluye': ['DDL', 'DML', 'DCL']}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_REGISTRO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["registro", "fila", "row", "tupla"],
        confianza_grounding=0.9,
        propiedades={'es': 'fila de datos', 'contiene': 'valores de columnas', 'representa': 'entidad'}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RESULTADO_QUERY",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["resultado query", "resultset", "resultado consulta"],
        confianza_grounding=0.9,
        propiedades={'contiene': ['filas', 'columnas', 'metadata'], 'retornado_por': 'SELECT'}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RESPALDAR",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["respaldar", "backup", "copia de seguridad"],
        operaciones={'ejecutar': lambda ruta: gestor_bd.respaldar(ruta) if gestor_bd else False},
        confianza_grounding=1.0,
        propiedades={'crea': 'copia BD', 'preserva': 'datos', 'permite': 'recuperación'}
    ))
    
    return conceptos

if __name__ == '__main__':
    conceptos = obtener_conceptos_bd()
    print(f"✅ Vocabulario BD CORREGIDO v3: {len(conceptos)} conceptos")
    print(f"   ✅ CONCEPTO_ROLLBACK ahora usa palabras específicas para BD")
    print(f"   ✅ 'rollback/revertir/deshacer' → CONCEPTO_ROLLBACK_PLAN (planes)")
    
    con_grounding_1 = sum(1 for c in conceptos if c.confianza_grounding == 1.0)
    print(f"   - Grounding 1.0: {con_grounding_1}")
    print(f"   - Grounding promedio: {sum(c.confianza_grounding for c in conceptos) / len(conceptos):.2f}")