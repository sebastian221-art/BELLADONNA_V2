"""
Tests para Cliente SQLite y Gestor BD - CORREGIDOS.
FASE 3 - Tests de bases de datos.
"""

import pytest
from pathlib import Path
import sys

proyecto_path = Path(__file__).parent.parent
sys.path.insert(0, str(proyecto_path))

from base_datos.cliente_sqlite import ClienteSQLite, ResultadoQuery
from base_datos.gestor_bd import GestorBD


class TestClienteSQLite:
    """Tests del cliente SQLite básico."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.cliente = ClienteSQLite(":memory:")
        self.cliente.conectar()
    
    def teardown_method(self):
        """Cleanup después de cada test."""
        self.cliente.desconectar()
    
    def test_conectar(self):
        """Test: conectar a BD."""
        cliente = ClienteSQLite(":memory:")
        assert cliente.conectar() is True
        cliente.desconectar()
    
    def test_crear_tabla(self):
        """Test: crear tabla."""
        exitoso = self.cliente.crear_tabla(
            "usuarios",
            {"id": "INTEGER", "nombre": "TEXT"},
            primary_key="id"
        )
        
        assert exitoso is True
        assert "usuarios" in self.cliente.listar_tablas()
    
    def test_insertar(self):
        """Test: insertar registro."""
        self.cliente.crear_tabla(
            "usuarios",
            {"id": "INTEGER", "nombre": "TEXT"}
        )
        
        resultado = self.cliente.insertar(
            "usuarios",
            {"id": 1, "nombre": "Bell"}
        )
        
        assert resultado.exitoso is True
        assert resultado.filas_afectadas == 1
    
    def test_seleccionar_todos(self):
        """Test: seleccionar todos los registros."""
        self.cliente.crear_tabla(
            "usuarios",
            {"id": "INTEGER", "nombre": "TEXT"}
        )
        
        self.cliente.insertar("usuarios", {"id": 1, "nombre": "Bell"})
        self.cliente.insertar("usuarios", {"id": 2, "nombre": "Lyra"})
        
        resultado = self.cliente.seleccionar("usuarios")
        
        assert resultado.exitoso is True
        assert len(resultado.filas) == 2
    
    def test_seleccionar_con_where(self):
        """Test: seleccionar con filtro WHERE."""
        self.cliente.crear_tabla(
            "usuarios",
            {"id": "INTEGER", "nombre": "TEXT", "edad": "INTEGER"}
        )
        
        self.cliente.insertar("usuarios", {"id": 1, "nombre": "Bell", "edad": 1})
        self.cliente.insertar("usuarios", {"id": 2, "nombre": "Lyra", "edad": 25})
        
        # Usar WHERE con valor directo
        resultado = self.cliente.seleccionar(
            "usuarios",
            where="edad > 10"
        )
        
        assert resultado.exitoso is True
        assert len(resultado.filas) == 1
        assert resultado.filas[0][1] == "Lyra"
    
    def test_seleccionar_con_order_by(self):
        """Test: seleccionar con ORDER BY."""
        self.cliente.crear_tabla(
            "usuarios",
            {"id": "INTEGER", "nombre": "TEXT"}
        )
        
        self.cliente.insertar("usuarios", {"id": 2, "nombre": "Lyra"})
        self.cliente.insertar("usuarios", {"id": 1, "nombre": "Bell"})
        
        resultado = self.cliente.seleccionar(
            "usuarios",
            order_by="id ASC"
        )
        
        assert resultado.filas[0][0] == 1  # Primer ID debe ser 1
    
    def test_seleccionar_con_limit(self):
        """Test: seleccionar con LIMIT."""
        self.cliente.crear_tabla(
            "usuarios",
            {"id": "INTEGER", "nombre": "TEXT"}
        )
        
        for i in range(5):
            self.cliente.insertar("usuarios", {"id": i, "nombre": f"Usuario{i}"})
        
        resultado = self.cliente.seleccionar("usuarios", limit=3)
        
        assert len(resultado.filas) == 3
    
    def test_actualizar(self):
        """Test: actualizar registro."""
        self.cliente.crear_tabla(
            "usuarios",
            {"id": "INTEGER", "nombre": "TEXT", "edad": "INTEGER"}
        )
        
        self.cliente.insertar("usuarios", {"id": 1, "nombre": "Bell", "edad": 1})
        
        # WHERE con valor directo
        resultado = self.cliente.actualizar(
            "usuarios",
            {"edad": 2},
            "id = 1"
        )
        
        assert resultado.exitoso is True
        assert resultado.filas_afectadas == 1
        
        # Verificar cambio
        verificacion = self.cliente.seleccionar("usuarios", where="id = 1")
        assert verificacion.filas[0][2] == 2  # Nueva edad
    
    def test_eliminar(self):
        """Test: eliminar registro."""
        self.cliente.crear_tabla(
            "usuarios",
            {"id": "INTEGER", "nombre": "TEXT"}
        )
        
        self.cliente.insertar("usuarios", {"id": 1, "nombre": "Bell"})
        self.cliente.insertar("usuarios", {"id": 2, "nombre": "Lyra"})
        
        resultado = self.cliente.eliminar("usuarios", "id = 1")
        
        assert resultado.exitoso is True
        assert resultado.filas_afectadas == 1
        
        # Verificar eliminación
        verificacion = self.cliente.seleccionar("usuarios")
        assert len(verificacion.filas) == 1
    
    def test_contar(self):
        """Test: contar registros."""
        self.cliente.crear_tabla(
            "usuarios",
            {"id": "INTEGER", "nombre": "TEXT"}
        )
        
        for i in range(5):
            self.cliente.insertar("usuarios", {"id": i, "nombre": f"Usuario{i}"})
        
        total = self.cliente.contar("usuarios")
        
        assert total == 5
    
    def test_contar_con_where(self):
        """Test: contar con filtro."""
        self.cliente.crear_tabla(
            "usuarios",
            {"id": "INTEGER", "edad": "INTEGER"}
        )
        
        self.cliente.insertar("usuarios", {"id": 1, "edad": 10})
        self.cliente.insertar("usuarios", {"id": 2, "edad": 20})
        self.cliente.insertar("usuarios", {"id": 3, "edad": 30})
        
        total = self.cliente.contar("usuarios", where="edad >= 20")
        
        assert total == 2
    
    def test_listar_tablas(self):
        """Test: listar tablas."""
        self.cliente.crear_tabla("usuarios", {"id": "INTEGER"})
        self.cliente.crear_tabla("posts", {"id": "INTEGER"})
        
        tablas = self.cliente.listar_tablas()
        
        assert "usuarios" in tablas
        assert "posts" in tablas
    
    def test_obtener_esquema(self):
        """Test: obtener esquema de tabla."""
        self.cliente.crear_tabla(
            "usuarios",
            {"id": "INTEGER", "nombre": "TEXT", "edad": "INTEGER"},
            primary_key="id"
        )
        
        esquema = self.cliente.obtener_esquema("usuarios")
        
        assert len(esquema) == 3
        assert esquema[0]['nombre'] == 'id'
        assert esquema[0]['pk'] == 1  # Es primary key
    
    def test_existe_tabla(self):
        """Test: verificar si tabla existe."""
        assert self.cliente.existe_tabla("usuarios") is False
        
        self.cliente.crear_tabla("usuarios", {"id": "INTEGER"})
        
        assert self.cliente.existe_tabla("usuarios") is True
    
    def test_eliminar_tabla(self):
        """Test: eliminar tabla."""
        self.cliente.crear_tabla("usuarios", {"id": "INTEGER"})
        
        assert self.cliente.eliminar_tabla("usuarios") is True
        assert "usuarios" not in self.cliente.listar_tablas()
    
    def test_vaciar_tabla(self):
        """Test: vaciar tabla."""
        self.cliente.crear_tabla("usuarios", {"id": "INTEGER"})
        
        for i in range(5):
            self.cliente.insertar("usuarios", {"id": i})
        
        assert self.cliente.vaciar_tabla("usuarios") is True
        assert self.cliente.contar("usuarios") == 0


class TestGestorBD:
    """Tests del gestor avanzado."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.gestor = GestorBD(":memory:")
        self.gestor.conectar()
    
    def teardown_method(self):
        """Cleanup después de cada test."""
        self.gestor.desconectar()
    
    def test_transaccion_exitosa(self):
        """Test: transacción exitosa."""
        self.gestor.cliente.crear_tabla(
            "usuarios",
            {"id": "INTEGER", "nombre": "TEXT"}
        )
        
        def op1():
            self.gestor.cliente.insertar("usuarios", {"id": 1, "nombre": "Bell"})
        
        def op2():
            self.gestor.cliente.insertar("usuarios", {"id": 2, "nombre": "Lyra"})
        
        exitoso, error = self.gestor.ejecutar_transaccion([op1, op2])
        
        assert exitoso is True
        assert error is None
        assert self.gestor.cliente.contar("usuarios") == 2
    
    def test_transaccion_con_error(self):
        """Test: transacción con error hace rollback."""
        self.gestor.cliente.crear_tabla(
            "usuarios",
            {"id": "INTEGER", "nombre": "TEXT"}
        )
        
        def op1():
            return self.gestor.cliente.insertar("usuarios", {"id": 1, "nombre": "Bell"})
        
        def op2():
            # Forzar un error SQL real: tabla inexistente
            return self.gestor.cliente.ejecutar_sql("SELECT * FROM tabla_inexistente")
        
        exitoso, error = self.gestor.ejecutar_transaccion([op1, op2])
        
        # La transacción debe fallar
        assert exitoso is False
        assert error is not None
        
        # Verificar rollback: NO debe haber ningún registro
        total = self.gestor.cliente.contar("usuarios")
        assert total == 0, f"Rollback falló: hay {total} registro(s)"
    
    def test_crear_indice(self):
        """Test: crear índice."""
        self.gestor.cliente.crear_tabla(
            "usuarios",
            {"id": "INTEGER", "nombre": "TEXT"}
        )
        
        exitoso = self.gestor.crear_indice(
            "idx_nombre",
            "usuarios",
            ["nombre"]
        )
        
        assert exitoso is True
        assert "idx_nombre" in self.gestor.listar_indices("usuarios")
    
    def test_eliminar_indice(self):
        """Test: eliminar índice."""
        self.gestor.cliente.crear_tabla("usuarios", {"id": "INTEGER", "nombre": "TEXT"})
        
        self.gestor.crear_indice("idx_nombre", "usuarios", ["nombre"])
        assert self.gestor.eliminar_indice("idx_nombre") is True
    
    def test_validar_datos(self):
        """Test: validar datos."""
        def validar_edad(valor):
            return 0 <= valor <= 150
        
        datos_validos = {"nombre": "Bell", "edad": 25}
        datos_invalidos = {"nombre": "Bell", "edad": 200}
        
        valido, errores = self.gestor.validar_datos(
            datos_validos,
            {"edad": validar_edad}
        )
        assert valido is True
        
        valido, errores = self.gestor.validar_datos(
            datos_invalidos,
            {"edad": validar_edad}
        )
        assert valido is False
        assert len(errores) > 0
    
    def test_buscar(self):
        """Test: buscar en múltiples columnas."""
        self.gestor.cliente.crear_tabla(
            "usuarios",
            {"id": "INTEGER", "nombre": "TEXT", "email": "TEXT"}
        )
        
        self.gestor.cliente.insertar("usuarios", {"id": 1, "nombre": "Bell", "email": "bell@ai.com"})
        self.gestor.cliente.insertar("usuarios", {"id": 2, "nombre": "Lyra", "email": "lyra@ai.com"})
        
        resultado = self.gestor.buscar("usuarios", "Bell", ["nombre", "email"])
        
        assert resultado.exitoso is True
        assert len(resultado.filas) >= 1
    
    def test_agrupar(self):
        """Test: agrupar datos."""
        self.gestor.cliente.crear_tabla(
            "ventas",
            {"id": "INTEGER", "ciudad": "TEXT", "monto": "INTEGER"}
        )
        
        self.gestor.cliente.insertar("ventas", {"id": 1, "ciudad": "Madrid", "monto": 100})
        self.gestor.cliente.insertar("ventas", {"id": 2, "ciudad": "Madrid", "monto": 200})
        self.gestor.cliente.insertar("ventas", {"id": 3, "ciudad": "Barcelona", "monto": 150})
        
        resultado = self.gestor.agrupar("ventas", "ciudad", "SUM(monto)")
        
        assert resultado.exitoso is True
        assert len(resultado.filas) == 2
    
    def test_obtener_estadisticas_tabla(self):
        """Test: obtener estadísticas de tabla."""
        self.gestor.cliente.crear_tabla(
            "usuarios",
            {"id": "INTEGER", "nombre": "TEXT", "edad": "INTEGER"}
        )
        
        for i in range(10):
            self.gestor.cliente.insertar("usuarios", {"id": i, "nombre": f"Usuario{i}", "edad": 20+i})
        
        stats = self.gestor.obtener_estadisticas("usuarios")
        
        assert stats['total_registros'] == 10
        assert stats['columnas'] == 3
        assert 'nombre' in stats['nombre_columnas']
    
    def test_obtener_estadisticas_bd(self):
        """Test: obtener estadísticas generales."""
        self.gestor.cliente.crear_tabla("usuarios", {"id": "INTEGER"})
        self.gestor.cliente.crear_tabla("posts", {"id": "INTEGER"})
        
        stats = self.gestor.obtener_estadisticas_bd()
        
        assert stats['total_tablas'] == 2
        assert 'usuarios' in stats['tablas']
        assert 'posts' in stats['tablas']
    
    def test_agregar_columna(self):
        """Test: agregar columna a tabla existente."""
        self.gestor.cliente.crear_tabla("usuarios", {"id": "INTEGER", "nombre": "TEXT"})
        
        exitoso = self.gestor.agregar_columna("usuarios", "edad", "INTEGER", default=0)
        
        assert exitoso is True
        
        esquema = self.gestor.cliente.obtener_esquema("usuarios")
        nombres_cols = [col['nombre'] for col in esquema]
        assert 'edad' in nombres_cols
    
    def test_renombrar_tabla(self):
        """Test: renombrar tabla."""
        self.gestor.cliente.crear_tabla("usuarios", {"id": "INTEGER"})
        
        exitoso = self.gestor.renombrar_tabla("usuarios", "users")
        
        assert exitoso is True
        assert "users" in self.gestor.cliente.listar_tablas()
        assert "usuarios" not in self.gestor.cliente.listar_tablas()


class TestResultadoQuery:
    """Tests de la clase ResultadoQuery."""
    
    def test_crear_resultado_exitoso(self):
        """Test: crear resultado exitoso."""
        resultado = ResultadoQuery(
            exitoso=True,
            filas=[(1, "Bell")],
            filas_afectadas=1,
            columnas=["id", "nombre"]
        )
        
        assert resultado.exitoso is True
        assert len(resultado.filas) == 1
        assert resultado.error is None
    
    def test_crear_resultado_con_error(self):
        """Test: crear resultado con error."""
        resultado = ResultadoQuery(
            exitoso=False,
            filas=[],
            filas_afectadas=0,
            columnas=[],
            error="Error de prueba"
        )
        
        assert resultado.exitoso is False
        assert resultado.error == "Error de prueba"


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])