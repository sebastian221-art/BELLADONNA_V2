"""
Demo de Bases de Datos - Fase 3 Semana 8 (CORREGIDO).
Muestra capacidades de SQLite de Bell.
"""

import sys
from pathlib import Path

proyecto_path = Path(__file__).parent.parent
sys.path.insert(0, str(proyecto_path))

from base_datos.cliente_sqlite import ClienteSQLite
from base_datos.gestor_bd import GestorBD
from vocabulario.semana10_bd import obtener_conceptos_bd, configurar_bd


def print_separador(titulo=""):
    """Imprime separador visual."""
    print("\n" + "=" * 80)
    if titulo:
        print(f"  {titulo}")
        print("=" * 80)


def demo_conexion():
    """Demo 1: Conectar a BD."""
    print_separador("DEMO 1: CONECTAR A BASE DE DATOS")
    
    # BD en memoria
    cliente = ClienteSQLite(":memory:")
    
    print("\n🗄️  Conectando a base de datos en memoria...")
    if cliente.conectar():
        print("   ✅ Conectado exitosamente")
        print(f"   📍 Path: {cliente.db_path}")
        print(f"   🔗 Conexión activa: {cliente.conexion is not None}")
        
        cliente.desconectar()
        print("\n   ✅ Desconectado")
    else:
        print("   ❌ Error al conectar")


def demo_crear_tabla():
    """Demo 2: Crear tablas."""
    print_separador("DEMO 2: CREAR TABLAS")
    
    cliente = ClienteSQLite(":memory:")
    cliente.conectar()
    
    print("\n📋 Creando tabla 'usuarios'...")
    exitoso = cliente.crear_tabla(
        "usuarios",
        {
            "id": "INTEGER",
            "nombre": "TEXT",
            "edad": "INTEGER",
            "email": "TEXT"
        },
        primary_key="id"
    )
    
    print(f"   ✅ Tabla creada: {exitoso}")
    
    # Verificar esquema
    print("\n📊 ESQUEMA DE LA TABLA:")
    esquema = cliente.obtener_esquema("usuarios")
    for col in esquema:
        pk = " (PK)" if col['pk'] else ""
        print(f"   • {col['nombre']}: {col['tipo']}{pk}")
    
    # Listar todas las tablas
    print("\n📋 TABLAS EN LA BD:")
    for tabla in cliente.listar_tablas():
        print(f"   • {tabla}")
    
    cliente.desconectar()


def demo_crud():
    """Demo 3: Operaciones CRUD."""
    print_separador("DEMO 3: CRUD (CREATE, READ, UPDATE, DELETE)")
    
    cliente = ClienteSQLite(":memory:")
    cliente.conectar()
    
    # Crear tabla
    cliente.crear_tabla(
        "usuarios",
        {"id": "INTEGER", "nombre": "TEXT", "edad": "INTEGER"},
        primary_key="id"
    )
    
    # CREATE (INSERT)
    print("\n➕ INSERT:")
    cliente.insertar("usuarios", {"id": 1, "nombre": "Bell", "edad": 1})
    cliente.insertar("usuarios", {"id": 2, "nombre": "Lyra", "edad": 25})
    cliente.insertar("usuarios", {"id": 3, "nombre": "Nova", "edad": 30})
    print("   ✅ 3 usuarios insertados")
    
    # READ (SELECT)
    print("\n📖 SELECT:")
    resultado = cliente.seleccionar("usuarios")
    print(f"   Total: {len(resultado.filas)} registros")
    for fila in resultado.filas:
        print(f"   • ID: {fila[0]}, Nombre: {fila[1]}, Edad: {fila[2]}")
    
    # UPDATE
    print("\n✏️  UPDATE:")
    resultado = cliente.actualizar(
        "usuarios",
        {"edad": 2},
        "nombre = 'Bell'"
    )
    print(f"   ✅ {resultado.filas_afectadas} registro(s) actualizado(s)")
    
    # Verificar cambio
    resultado = cliente.seleccionar("usuarios", where="nombre = 'Bell'")
    print(f"   Nueva edad de Bell: {resultado.filas[0][2]}")
    
    # DELETE
    print("\n🗑️  DELETE:")
    resultado = cliente.eliminar("usuarios", "id = 3")
    print(f"   ✅ {resultado.filas_afectadas} registro(s) eliminado(s)")
    
    # Verificar
    total = cliente.contar("usuarios")
    print(f"\n📊 Total final: {total} usuarios")
    
    cliente.desconectar()


def demo_queries_avanzadas():
    """Demo 4: Queries avanzadas."""
    print_separador("DEMO 4: QUERIES AVANZADAS")
    
    cliente = ClienteSQLite(":memory:")
    cliente.conectar()
    
    # Crear tabla y datos
    cliente.crear_tabla(
        "productos",
        {"id": "INTEGER", "nombre": "TEXT", "precio": "REAL", "stock": "INTEGER"},
        primary_key="id"
    )
    
    productos = [
        {"id": 1, "nombre": "Laptop", "precio": 999.99, "stock": 5},
        {"id": 2, "nombre": "Mouse", "precio": 29.99, "stock": 50},
        {"id": 3, "nombre": "Teclado", "precio": 79.99, "stock": 30},
        {"id": 4, "nombre": "Monitor", "precio": 299.99, "stock": 15},
        {"id": 5, "nombre": "USB", "precio": 9.99, "stock": 100}
    ]
    
    for p in productos:
        cliente.insertar("productos", p)
    
    print("\n📦 Productos insertados: 5")
    
    # WHERE
    print("\n🔍 WHERE (precio > 50):")
    resultado = cliente.seleccionar(
        "productos",
        where="precio > 50"
    )
    for fila in resultado.filas:
        print(f"   • {fila[1]}: ${fila[2]}")
    
    # ORDER BY
    print("\n📊 ORDER BY precio DESC:")
    resultado = cliente.seleccionar(
        "productos",
        order_by="precio DESC",
        limit=3
    )
    for fila in resultado.filas:
        print(f"   • {fila[1]}: ${fila[2]}")
    
    # COUNT
    print("\n🔢 COUNT:")
    total = cliente.contar("productos")
    caros = cliente.contar("productos", where="precio > 100")
    print(f"   Total productos: {total}")
    print(f"   Productos >$100: {caros}")
    
    cliente.desconectar()


def demo_transacciones():
    """Demo 5: Transacciones."""
    print_separador("DEMO 5: TRANSACCIONES")
    
    gestor = GestorBD(":memory:")
    gestor.conectar()
    
    # Crear tabla
    gestor.cliente.crear_tabla(
        "cuentas",
        {"id": "INTEGER", "titular": "TEXT", "saldo": "REAL"},
        primary_key="id"
    )
    
    # Insertar datos iniciales
    gestor.cliente.insertar("cuentas", {"id": 1, "titular": "Alice", "saldo": 1000})
    gestor.cliente.insertar("cuentas", {"id": 2, "titular": "Bob", "saldo": 500})
    
    print("\n💰 SALDOS INICIALES:")
    resultado = gestor.cliente.seleccionar("cuentas")
    for fila in resultado.filas:
        print(f"   • {fila[1]}: ${fila[2]}")
    
    # Transacción: Transferir $200 de Alice a Bob
    print("\n💸 TRANSACCIÓN: Transferir $200 de Alice a Bob...")
    
    def transferir():
        gestor.cliente.actualizar(
            "cuentas",
            {"saldo": 800},
            "id = 1"
        )
        gestor.cliente.actualizar(
            "cuentas",
            {"saldo": 700},
            "id = 2"
        )
    
    exitoso, error = gestor.ejecutar_transaccion([transferir])
    
    if exitoso:
        print("   ✅ Transacción exitosa")
        
        print("\n💰 SALDOS FINALES:")
        resultado = gestor.cliente.seleccionar("cuentas")
        for fila in resultado.filas:
            print(f"   • {fila[1]}: ${fila[2]}")
    else:
        print(f"   ❌ Error: {error}")
    
    gestor.desconectar()


def demo_indices():
    """Demo 6: Índices."""
    print_separador("DEMO 6: ÍNDICES")
    
    gestor = GestorBD(":memory:")
    gestor.conectar()
    
    # Crear tabla
    gestor.cliente.crear_tabla(
        "usuarios",
        {"id": "INTEGER", "nombre": "TEXT", "email": "TEXT"},
        primary_key="id"
    )
    
    print("\n📋 Tabla 'usuarios' creada")
    
    # Crear índice
    print("\n🔍 Creando índice en columna 'email'...")
    exitoso = gestor.crear_indice("idx_email", "usuarios", ["email"], unico=True)
    print(f"   ✅ Índice creado: {exitoso}")
    
    # Crear índice compuesto
    print("\n🔍 Creando índice compuesto (nombre, email)...")
    exitoso = gestor.crear_indice("idx_nombre_email", "usuarios", ["nombre", "email"])
    print(f"   ✅ Índice creado: {exitoso}")
    
    # Listar índices
    print("\n📊 ÍNDICES DE LA TABLA:")
    indices = gestor.listar_indices("usuarios")
    for idx in indices:
        print(f"   • {idx}")
    
    gestor.desconectar()


def demo_estadisticas():
    """Demo 7: Estadísticas."""
    print_separador("DEMO 7: ESTADÍSTICAS")
    
    gestor = GestorBD(":memory:")
    gestor.conectar()
    
    # Crear tablas y datos
    gestor.cliente.crear_tabla("usuarios", {"id": "INTEGER", "nombre": "TEXT"})
    gestor.cliente.crear_tabla("posts", {"id": "INTEGER", "titulo": "TEXT"})
    
    for i in range(10):
        gestor.cliente.insertar("usuarios", {"id": i, "nombre": f"Usuario{i}"})
    
    for i in range(20):
        gestor.cliente.insertar("posts", {"id": i, "titulo": f"Post {i}"})
    
    # Estadísticas de tabla
    print("\n📊 ESTADÍSTICAS DE 'usuarios':")
    stats = gestor.obtener_estadisticas("usuarios")
    print(f"   Total registros: {stats['total_registros']}")
    print(f"   Columnas: {stats['columnas']}")
    print(f"   Nombres: {', '.join(stats['nombre_columnas'])}")
    
    # Estadísticas generales
    print("\n📊 ESTADÍSTICAS GENERALES:")
    stats = gestor.obtener_estadisticas_bd()
    print(f"   Total tablas: {stats['total_tablas']}")
    print(f"   Tablas: {', '.join(stats['tablas'])}")
    
    gestor.desconectar()


def demo_vocabulario():
    """Demo 8: Vocabulario de BD."""
    print_separador("DEMO 8: VOCABULARIO DE BASES DE DATOS")
    
    conceptos = obtener_conceptos_bd()
    
    print(f"\n📚 CONCEPTOS CARGADOS: {len(conceptos)}")
    
    # Estadísticas
    con_grounding_1 = sum(1 for c in conceptos if c.confianza_grounding == 1.0)
    con_operaciones = sum(1 for c in conceptos if hasattr(c, 'operaciones') and c.operaciones)
    
    print(f"  • Grounding 1.0: {con_grounding_1}/{len(conceptos)}")
    print(f"  • Con operaciones: {con_operaciones}/{len(conceptos)}")
    print(f"  • Grounding promedio: {sum(c.confianza_grounding for c in conceptos) / len(conceptos):.2f}")
    
    # Conceptos por categoría
    print("\n📊 CONCEPTOS POR CATEGORÍA:")
    categorias = {
        'Conexión': ['conectar', 'desconectar', 'conexión'],
        'Tablas': ['tabla', 'crear tabla', 'eliminar tabla', 'esquema'],
        'CRUD': ['insert', 'select', 'update', 'delete'],
        'Queries': ['where', 'order by', 'limit', 'count'],
        'Transacciones': ['transacción', 'commit', 'rollback'],
        'Índices': ['índice', 'crear índice'],
        'Otros': ['sql', 'sqlite', 'registro', 'columna']
    }
    
    for cat, palabras in categorias.items():
        count = sum(1 for c in conceptos
                   if any(p in ' '.join(c.palabras_español).lower()
                         for p in palabras))
        print(f"  • {cat}: {count}")


def demo_integracion():
    """Demo 9: Integración completa."""
    print_separador("DEMO 9: INTEGRACIÓN COMPLETA")
    
    # Configurar todo
    cliente = ClienteSQLite(":memory:")
    gestor = GestorBD(":memory:")
    
    cliente.conectar()
    gestor.conectar()
    
    configurar_bd(cliente, gestor)
    
    print("\n✅ Sistema de BD configurado")
    print(f"   Cliente: {type(cliente).__name__}")
    print(f"   Gestor: {type(gestor).__name__}")
    
    # Crear sistema de blog
    print("\n📝 Creando sistema de blog...")
    
    # Tabla usuarios
    gestor.cliente.crear_tabla(
        "usuarios",
        {"id": "INTEGER", "username": "TEXT", "email": "TEXT"},
        primary_key="id"
    )
    
    # Tabla posts
    gestor.cliente.crear_tabla(
        "posts",
        {"id": "INTEGER", "user_id": "INTEGER", "titulo": "TEXT", "contenido": "TEXT"},
        primary_key="id"
    )
    
    print("   ✅ Tablas creadas")
    
    # Insertar datos
    gestor.cliente.insertar("usuarios", {"id": 1, "username": "bell", "email": "bell@ai.com"})
    gestor.cliente.insertar("usuarios", {"id": 2, "username": "lyra", "email": "lyra@ai.com"})
    
    gestor.cliente.insertar("posts", {
        "id": 1,
        "user_id": 1,
        "titulo": "Mi primer post",
        "contenido": "Hola mundo desde Bell!"
    })
    
    print("   ✅ Datos insertados")
    
    # Crear índices
    gestor.crear_indice("idx_username", "usuarios", ["username"], unico=True)
    gestor.crear_indice("idx_user_posts", "posts", ["user_id"])
    
    print("   ✅ Índices creados")
    
    # Query compleja: Posts con info de usuario
    print("\n📊 POSTS CON INFORMACIÓN DE USUARIO:")
    resultado = gestor.unir_tablas("posts", "usuarios", "user_id", "INNER")
    
    if resultado.exitoso:
        for fila in resultado.filas:
            print(f"   • Post: '{fila[2]}' por @{fila[5]}")
    
    # Estadísticas finales
    print("\n📈 ESTADÍSTICAS:")
    stats = gestor.obtener_estadisticas_bd()
    print(f"   Tablas: {stats['total_tablas']}")
    
    for tabla in stats['tablas']:
        total = gestor.cliente.contar(tabla)
        print(f"   • {tabla}: {total} registros")
    
    cliente.desconectar()
    gestor.desconectar()


def main():
    """Ejecuta todas las demos."""
    print("\n" + "🗄️" * 40)
    print("  BELLADONNA - FASE 3 COMPLETA: BASES DE DATOS")
    print("  Semana 8: SQLite + Gestor BD (FINAL)")
    print("🗄️" * 40)
    
    try:
        # Demo 1
        demo_conexion()
        
        # Demo 2
        demo_crear_tabla()
        
        # Demo 3
        demo_crud()
        
        # Demo 4
        demo_queries_avanzadas()
        
        # Demo 5
        demo_transacciones()
        
        # Demo 6
        demo_indices()
        
        # Demo 7
        demo_estadisticas()
        
        # Demo 8
        demo_vocabulario()
        
        # Demo 9
        demo_integracion()
        
        # Resumen final
        print_separador("✨ FASE 3 COMPLETADA ✨")
        print("""
🎉🎉🎉 ¡BELLADONNA FASE 3 COMPLETA! 🎉🎉🎉

✅ Semana 1-2: Sistema de Operaciones (40 conceptos)
✅ Semana 3-4: Análisis de Código (50 conceptos)
✅ Semana 5: Matemáticas Avanzadas (45 conceptos)
✅ Semana 6: Planificación Multi-Paso (40 conceptos)
✅ Semana 7: Red y APIs (35 conceptos)
✅ Semana 8: Bases de Datos (30 conceptos)

📊 ESTADÍSTICAS TOTALES FASE 3:
  • Conceptos nuevos: 240
  • Tests nuevos: 150+
  • Módulos: 8
  • Grounding promedio: 0.94

🎯 VOCABULARIO TOTAL BELLADONNA:
  • Fase 1+2: 225 conceptos
  • Fase 3: +240 conceptos
  • TOTAL: 465 CONCEPTOS 🚀

🌟 CAPACIDADES ACTUALES DE BELL:
  ✓ Sistema de archivos y comandos shell
  ✓ Análisis de código Python
  ✓ Matemáticas avanzadas
  ✓ Planificación multi-paso
  ✓ Networking y APIs HTTP
  ✓ Bases de datos SQLite

🎓 PRÓXIMO: FASE 4 - Autonomía y Aprendizaje Continuo
        """)
        
    except Exception as e:
        print(f"\n❌ Error en demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()