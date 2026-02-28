"""
Gestor avanzado de bases de datos SQLite.
FASE 3 - Semana 8 (VERSIÓN DEFINITIVA)
"""

from typing import List, Dict, Any, Optional, Callable
from pathlib import Path
import sqlite3
from .cliente_sqlite import ClienteSQLite, ResultadoQuery


class GestorBD:
    """
    Gestor avanzado de bases de datos.
    
    Añade sobre ClienteSQLite:
    - Transacciones
    - Migraciones
    - Respaldos
    - Validaciones
    - Indices
    - Queries complejas
    """
    
    def __init__(self, db_path: str = ":memory:"):
        """
        Inicializa el gestor.
        
        Args:
            db_path: Ruta a la base de datos
        """
        self.cliente = ClienteSQLite(db_path)
        self.en_transaccion = False
    
    def conectar(self) -> bool:
        """Conecta a la base de datos."""
        return self.cliente.conectar()
    
    def desconectar(self):
        """Desconecta de la base de datos."""
        self.cliente.desconectar()
    
    # ==================== TRANSACCIONES ====================
    
    def iniciar_transaccion(self):
        """Inicia una transacción."""
        if not self.en_transaccion:
            # Deshabilitar auto-commit
            self.cliente.auto_commit_enabled = False
            self.cliente.ejecutar_sql("BEGIN TRANSACTION")
            self.en_transaccion = True
    
    def commit(self):
        """Confirma la transacción."""
        if self.en_transaccion:
            self.cliente.conexion.commit()
            self.en_transaccion = False
            # Rehabilitar auto-commit
            self.cliente.auto_commit_enabled = True
    
    def rollback(self):
        """Revierte la transacción."""
        if self.en_transaccion:
            self.cliente.conexion.rollback()
            self.en_transaccion = False
            # Rehabilitar auto-commit
            self.cliente.auto_commit_enabled = True
    
    def ejecutar_transaccion(
        self,
        operaciones: List[Callable]
    ) -> tuple[bool, Optional[str]]:
        """
        Ejecuta múltiples operaciones en una transacción.
        
        Args:
            operaciones: Lista de funciones a ejecutar
            
        Returns:
            (exitoso, error)
            
        Example:
            >>> def op1():
            ...     cliente.insertar("usuarios", {"nombre": "Bell"})
            >>> def op2():
            ...     cliente.insertar("usuarios", {"nombre": "Lyra"})
            >>> gestor.ejecutar_transaccion([op1, op2])
        """
        try:
            self.iniciar_transaccion()
            
            for operacion in operaciones:
                resultado = operacion()
                
                # Verificar si la operación retornó ResultadoQuery con error
                if resultado is not None and hasattr(resultado, 'exitoso'):
                    if not resultado.exitoso:
                        self.rollback()
                        return (False, resultado.error)
            
            self.commit()
            return (True, None)
            
        except Exception as e:
            self.rollback()
            return (False, str(e))
    
    # ==================== INDICES ====================
    
    def crear_indice(
        self,
        nombre: str,
        tabla: str,
        columnas: List[str],
        unico: bool = False
    ) -> bool:
        """
        Crea un índice.
        
        Args:
            nombre: Nombre del índice
            tabla: Tabla
            columnas: Columnas a indexar
            unico: Si es índice único
            
        Returns:
            True si exitoso
        """
        unique_clause = "UNIQUE " if unico else ""
        cols = ', '.join(columnas)
        
        sql = f"CREATE {unique_clause}INDEX IF NOT EXISTS {nombre} ON {tabla} ({cols})"
        
        resultado = self.cliente.ejecutar_sql(sql)
        return resultado.exitoso
    
    def eliminar_indice(self, nombre: str) -> bool:
        """
        Elimina un índice.
        
        Args:
            nombre: Nombre del índice
            
        Returns:
            True si exitoso
        """
        sql = f"DROP INDEX IF EXISTS {nombre}"
        resultado = self.cliente.ejecutar_sql(sql)
        return resultado.exitoso
    
    def listar_indices(self, tabla: str) -> List[str]:
        """
        Lista índices de una tabla.
        
        Args:
            tabla: Nombre de la tabla
            
        Returns:
            Lista de nombres de índices
        """
        sql = f"SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='{tabla}'"
        resultado = self.cliente.ejecutar_sql(sql)
        
        if resultado.exitoso:
            return [fila[0] for fila in resultado.filas]
        
        return []
    
    # ==================== RESPALDOS ====================
    
    def respaldar(self, ruta_respaldo: str) -> bool:
        """
        Crea un respaldo de la base de datos.
        
        Args:
            ruta_respaldo: Ruta del archivo de respaldo
            
        Returns:
            True si exitoso
        """
        try:
            respaldo_conn = sqlite3.connect(ruta_respaldo)
            self.cliente.conexion.backup(respaldo_conn)
            respaldo_conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error en respaldo: {e}")
            return False
    
    def restaurar(self, ruta_respaldo: str) -> bool:
        """
        Restaura desde un respaldo.
        
        Args:
            ruta_respaldo: Ruta del archivo de respaldo
            
        Returns:
            True si exitoso
        """
        try:
            respaldo_conn = sqlite3.connect(ruta_respaldo)
            respaldo_conn.backup(self.cliente.conexion)
            respaldo_conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error restaurando: {e}")
            return False
    
    # ==================== VALIDACIONES ====================
    
    def validar_datos(
        self,
        datos: Dict[str, Any],
        reglas: Dict[str, Callable]
    ) -> tuple[bool, List[str]]:
        """
        Valida datos según reglas.
        
        Args:
            datos: Datos a validar
            reglas: Dict {campo: funcion_validacion}
            
        Returns:
            (valido, errores)
            
        Example:
            >>> def validar_edad(valor):
            ...     return valor >= 0 and valor <= 150
            >>> gestor.validar_datos(
            ...     {"edad": 200},
            ...     {"edad": validar_edad}
            ... )
            (False, ['edad: validación falló'])
        """
        errores = []
        
        for campo, funcion in reglas.items():
            if campo in datos:
                try:
                    if not funcion(datos[campo]):
                        errores.append(f"{campo}: validación falló")
                except Exception as e:
                    errores.append(f"{campo}: error en validación - {e}")
        
        return (len(errores) == 0, errores)
    
    # ==================== QUERIES COMPLEJAS ====================
    
    def buscar(
        self,
        tabla: str,
        termino: str,
        columnas: List[str]
    ) -> ResultadoQuery:
        """
        Busca un término en múltiples columnas.
        
        Args:
            tabla: Tabla
            termino: Término a buscar
            columnas: Columnas donde buscar
            
        Returns:
            ResultadoQuery
        """
        condiciones = ' OR '.join([f"{col} LIKE ?" for col in columnas])
        parametros = tuple([f"%{termino}%" for _ in columnas])
        
        sql = f"SELECT * FROM {tabla} WHERE {condiciones}"
        
        return self.cliente.ejecutar_sql(sql, parametros)
    
    def agrupar(
        self,
        tabla: str,
        columna_agrupar: str,
        agregacion: str = "COUNT(*)"
    ) -> ResultadoQuery:
        """
        Agrupa y agrega datos.
        
        Args:
            tabla: Tabla
            columna_agrupar: Columna para GROUP BY
            agregacion: Función de agregación
            
        Returns:
            ResultadoQuery
            
        Example:
            >>> gestor.agrupar("usuarios", "ciudad", "COUNT(*)")
        """
        sql = f"SELECT {columna_agrupar}, {agregacion} as total FROM {tabla} GROUP BY {columna_agrupar}"
        
        return self.cliente.ejecutar_sql(sql)
    
    def unir_tablas(
        self,
        tabla1: str,
        tabla2: str,
        columna_union: str,
        tipo_join: str = "INNER"
    ) -> ResultadoQuery:
        """
        Une dos tablas.
        
        Args:
            tabla1: Primera tabla
            tabla2: Segunda tabla
            columna_union: Columna para unir
            tipo_join: Tipo de JOIN (INNER, LEFT, RIGHT)
            
        Returns:
            ResultadoQuery
        """
        sql = f"""
        SELECT * FROM {tabla1}
        {tipo_join} JOIN {tabla2}
        ON {tabla1}.{columna_union} = {tabla2}.{columna_union}
        """
        
        return self.cliente.ejecutar_sql(sql)
    
    # ==================== ESTADÍSTICAS ====================
    
    def obtener_estadisticas(self, tabla: str) -> Dict[str, Any]:
        """
        Obtiene estadísticas de una tabla.
        
        Args:
            tabla: Nombre de la tabla
            
        Returns:
            Dict con estadísticas
        """
        stats = {}
        
        # Total de registros
        stats['total_registros'] = self.cliente.contar(tabla)
        
        # Esquema
        esquema = self.cliente.obtener_esquema(tabla)
        stats['columnas'] = len(esquema)
        stats['nombre_columnas'] = [col['nombre'] for col in esquema]
        
        # Índices
        stats['indices'] = len(self.listar_indices(tabla))
        
        return stats
    
    def obtener_estadisticas_bd(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas generales de la BD.
        
        Returns:
            Dict con estadísticas
        """
        stats = {}
        
        # Tablas
        tablas = self.cliente.listar_tablas()
        stats['total_tablas'] = len(tablas)
        stats['tablas'] = tablas
        
        # Tamaño (si es archivo)
        if self.cliente.db_path != ":memory:":
            try:
                path = Path(self.cliente.db_path)
                if path.exists():
                    stats['tamaño_bytes'] = path.stat().st_size
                    stats['tamaño_mb'] = round(stats['tamaño_bytes'] / (1024 * 1024), 2)
            except:
                pass
        
        return stats
    
    # ==================== MIGRACIONES ====================
    
    def agregar_columna(
        self,
        tabla: str,
        nombre_columna: str,
        tipo: str,
        default: Optional[Any] = None
    ) -> bool:
        """
        Agrega una columna a una tabla existente.
        
        Args:
            tabla: Nombre de la tabla
            nombre_columna: Nombre de la nueva columna
            tipo: Tipo de dato
            default: Valor por defecto
            
        Returns:
            True si exitoso
        """
        default_clause = f" DEFAULT {default}" if default is not None else ""
        sql = f"ALTER TABLE {tabla} ADD COLUMN {nombre_columna} {tipo}{default_clause}"
        
        resultado = self.cliente.ejecutar_sql(sql)
        return resultado.exitoso
    
    def renombrar_tabla(self, nombre_actual: str, nombre_nuevo: str) -> bool:
        """
        Renombra una tabla.
        
        Args:
            nombre_actual: Nombre actual
            nombre_nuevo: Nombre nuevo
            
        Returns:
            True si exitoso
        """
        sql = f"ALTER TABLE {nombre_actual} RENAME TO {nombre_nuevo}"
        resultado = self.cliente.ejecutar_sql(sql)
        return resultado.exitoso


# Ejemplo de uso
if __name__ == '__main__':
    gestor = GestorBD(":memory:")
    gestor.conectar()
    
    # Crear tabla
    gestor.cliente.crear_tabla(
        "usuarios",
        {"id": "INTEGER", "nombre": "TEXT", "edad": "INTEGER"},
        primary_key="id"
    )
    
    # Usar transacciones
    print("📦 Transacción...")
    def op1():
        gestor.cliente.insertar("usuarios", {"id": 1, "nombre": "Bell", "edad": 1})
    
    def op2():
        gestor.cliente.insertar("usuarios", {"id": 2, "nombre": "Lyra", "edad": 25})
    
    exitoso, error = gestor.ejecutar_transaccion([op1, op2])
    print(f"   Exitoso: {exitoso}")
    
    # Crear índice
    gestor.crear_indice("idx_nombre", "usuarios", ["nombre"])
    print(f"📊 Índices: {gestor.listar_indices('usuarios')}")
    
    # Estadísticas
    stats = gestor.obtener_estadisticas("usuarios")
    print(f"📈 Estadísticas: {stats}")
    
    gestor.desconectar()