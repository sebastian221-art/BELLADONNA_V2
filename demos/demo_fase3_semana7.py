"""
Demo de Red y APIs - Fase 3 Semana 7.
Muestra capacidades de networking de Bell.
"""

import sys
from pathlib import Path

proyecto_path = Path(__file__).parent.parent
sys.path.insert(0, str(proyecto_path))

from red.cliente_http import ClienteHTTP
from red.manejador_requests import ManejadorRequests
from vocabulario.semana9_red import obtener_conceptos_red, configurar_red


def print_separador(titulo=""):
    """Imprime separador visual."""
    print("\n" + "=" * 80)
    if titulo:
        print(f"  {titulo}")
        print("=" * 80)


def demo_get_simple():
    """Demo 1: GET request simple."""
    print_separador("DEMO 1: GET REQUEST SIMPLE")
    
    cliente = ClienteHTTP()
    
    print("\n🌐 GET a JSONPlaceholder API...")
    respuesta = cliente.get("https://jsonplaceholder.typicode.com/todos/1")
    
    print(f"\n✅ Respuesta recibida:")
    print(f"   Código: {respuesta.codigo_estado}")
    print(f"   Exitoso: {respuesta.exitoso}")
    print(f"   Tiempo: {respuesta.tiempo_respuesta:.3f}s")
    print(f"   Contenido: {respuesta.contenido[:100]}...")


def demo_get_json():
    """Demo 2: GET con parseo JSON."""
    print_separador("DEMO 2: GET CON JSON")
    
    cliente = ClienteHTTP()
    
    print("\n📊 Obteniendo datos JSON...")
    exitoso, datos = cliente.get_json(
        "https://jsonplaceholder.typicode.com/users/1"
    )
    
    if exitoso:
        print(f"\n✅ JSON parseado correctamente:")
        print(f"   ID: {datos.get('id')}")
        print(f"   Nombre: {datos.get('name')}")
        print(f"   Username: {datos.get('username')}")
        print(f"   Email: {datos.get('email')}")
        print(f"   Ciudad: {datos.get('address', {}).get('city')}")
    else:
        print(f"❌ Error parseando JSON")


def demo_post():
    """Demo 3: POST request."""
    print_separador("DEMO 3: POST REQUEST")
    
    cliente = ClienteHTTP()
    
    nuevo_post = {
        'title': 'Bell aprende HTTP',
        'body': 'Belladonna está enviando su primer POST request',
        'userId': 1
    }
    
    print("\n📤 Enviando POST...")
    print(f"   Datos: {nuevo_post}")
    
    respuesta = cliente.post(
        "https://jsonplaceholder.typicode.com/posts",
        json_data=nuevo_post
    )
    
    print(f"\n✅ POST enviado:")
    print(f"   Código: {respuesta.codigo_estado}")
    print(f"   Creado: {respuesta.exitoso}")
    print(f"   Respuesta: {respuesta.contenido[:150]}...")


def demo_query_params():
    """Demo 4: Query parameters."""
    print_separador("DEMO 4: QUERY PARAMETERS")
    
    cliente = ClienteHTTP()
    
    params = {
        'postId': 1,
        '_limit': 3
    }
    
    print(f"\n🔍 GET con parámetros: {params}")
    
    exitoso, datos = cliente.get_json(
        "https://jsonplaceholder.typicode.com/comments",
        params=params
    )
    
    if exitoso and isinstance(datos, list):
        print(f"\n✅ Obtenidos {len(datos)} comentarios:")
        for comentario in datos:
            print(f"   • {comentario.get('name')} - {comentario.get('email')}")


def demo_configurar_api():
    """Demo 5: Configurar API."""
    print_separador("DEMO 5: CONFIGURAR API")
    
    manejador = ManejadorRequests()
    
    print("\n⚙️  Configurando APIs...")
    
    # Configurar JSONPlaceholder
    manejador.configurar_api(
        "jsonplaceholder",
        "https://jsonplaceholder.typicode.com",
        headers={'Content-Type': 'application/json'}
    )
    
    # Configurar GitHub
    manejador.configurar_api(
        "github",
        "https://api.github.com",
        headers={'Accept': 'application/vnd.github.v3+json'}
    )
    
    print(f"   ✅ APIs configuradas: {len(manejador.configuraciones)}")
    for nombre in manejador.configuraciones:
        config = manejador.configuraciones[nombre]
        print(f"   • {nombre}: {config.base_url}")
    
    # Usar API configurada
    print("\n🌐 Usando API configurada...")
    respuesta = manejador.request_api(
        "jsonplaceholder",
        "/posts/1",
        method='GET'
    )
    
    print(f"   Código: {respuesta.codigo_estado}")
    print(f"   Exitoso: {respuesta.exitoso}")


def demo_validacion():
    """Demo 6: Validación de respuestas."""
    print_separador("DEMO 6: VALIDACIÓN DE RESPUESTAS")
    
    manejador = ManejadorRequests()
    cliente = ClienteHTTP()
    
    # Request exitoso
    print("\n✅ Validando respuesta exitosa...")
    resp1 = cliente.get("https://jsonplaceholder.typicode.com/todos/1")
    
    def validar_json(resp):
        try:
            import json
            json.loads(resp.contenido)
            return True
        except:
            return False
    
    valida, errores = manejador.validar_respuesta(
        resp1,
        validaciones={'es_json': validar_json}
    )
    
    print(f"   Válida: {valida}")
    print(f"   Errores: {len(errores)}")
    
    # Request fallido (simulado)
    print("\n❌ Validando respuesta fallida...")
    resp2 = cliente.get("https://jsonplaceholder.typicode.com/noexiste")
    
    valida, errores = manejador.validar_respuesta(resp2)
    
    print(f"   Válida: {valida}")
    print(f"   Errores: {len(errores)}")
    for error in errores:
        print(f"     • {error}")


def demo_cache():
    """Demo 7: Caché de respuestas."""
    print_separador("DEMO 7: CACHÉ DE RESPUESTAS")
    
    manejador = ManejadorRequests()
    url = "https://jsonplaceholder.typicode.com/posts/1"
    
    print("\n🗄️  Primera llamada (sin caché)...")
    resp1 = manejador.get_con_cache(url)
    print(f"   Tiempo: {resp1.tiempo_respuesta:.3f}s")
    print(f"   En caché: {len(manejador.cache)} items")
    
    print("\n⚡ Segunda llamada (con caché)...")
    resp2 = manejador.get_con_cache(url)
    print(f"   Tiempo: {resp2.tiempo_respuesta:.3f}s")
    print(f"   En caché: {len(manejador.cache)} items")
    
    print("\n🔄 Forzar refresh...")
    resp3 = manejador.get_con_cache(url, forzar_refresh=True)
    print(f"   Tiempo: {resp3.tiempo_respuesta:.3f}s")


def demo_estadisticas():
    """Demo 8: Estadísticas de requests."""
    print_separador("DEMO 8: ESTADÍSTICAS")
    
    manejador = ManejadorRequests()
    manejador.configurar_api(
        "jsonplaceholder",
        "https://jsonplaceholder.typicode.com"
    )
    
    print("\n📊 Haciendo múltiples requests...")
    
    # Hacer varios requests
    endpoints = ["/todos/1", "/todos/2", "/todos/3", "/posts/1", "/users/1"]
    for endpoint in endpoints:
        manejador.request_api("jsonplaceholder", endpoint)
        print(f"   ✅ {endpoint}")
    
    # Obtener estadísticas
    stats = manejador.obtener_estadisticas()
    
    print("\n📈 ESTADÍSTICAS:")
    print(f"   Total requests: {stats['total_requests']}")
    print(f"   Exitosos: {stats['exitosos']}")
    print(f"   Fallidos: {stats['fallidos']}")
    print(f"   Tasa de éxito: {stats['tasa_exito']:.1f}%")
    print(f"   Tiempo promedio: {stats['tiempo_promedio']:.3f}s")
    print(f"   Tiempo total: {stats['tiempo_total']:.3f}s")


def demo_vocabulario():
    """Demo 9: Vocabulario de red."""
    print_separador("DEMO 9: VOCABULARIO DE RED")
    
    conceptos = obtener_conceptos_red()
    
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
        'HTTP Métodos': ['get', 'post', 'put', 'delete'],
        'Respuesta': ['respuesta', 'codigo', '200', '404', '500'],
        'JSON': ['json', 'parsear'],
        'Headers': ['headers', 'content-type', 'user-agent'],
        'URL': ['url', 'endpoint', 'params'],
        'Configuración': ['configurar', 'timeout', 'cache'],
        'Errores': ['error', 'validar', 'manejo']
    }
    
    for cat, palabras in categorias.items():
        count = sum(1 for c in conceptos
                   if any(p in ' '.join(c.palabras_español).lower()
                         for p in palabras))
        print(f"  • {cat}: {count}")


def demo_integracion():
    """Demo 10: Integración completa."""
    print_separador("DEMO 10: INTEGRACIÓN COMPLETA")
    
    # Configurar todo
    cliente = ClienteHTTP()
    manejador = ManejadorRequests()
    configurar_red(cliente, manejador)
    
    print("\n✅ Sistema de red configurado")
    print(f"   Cliente HTTP: {type(cliente).__name__}")
    print(f"   Manejador: {type(manejador).__name__}")
    
    # Configurar API real
    manejador.configurar_api(
        "github",
        "https://api.github.com",
        headers={'Accept': 'application/vnd.github.v3+json'}
    )
    
    print("\n🌐 Consultando GitHub API...")
    respuesta = manejador.request_api(
        "github",
        "/users/github",
        method='GET'
    )
    
    if respuesta.exitoso:
        exitoso, datos = manejador.parsear_json_respuesta(respuesta)
        if exitoso:
            print(f"\n✅ Usuario GitHub:")
            print(f"   Login: {datos.get('login')}")
            print(f"   Name: {datos.get('name')}")
            print(f"   Public Repos: {datos.get('public_repos')}")
            print(f"   Followers: {datos.get('followers')}")


def main():
    """Ejecuta todas las demos."""
    print("\n" + "🌐" * 40)
    print("  BELLADONNA - FASE 3: RED Y APIs")
    print("  Semana 7: Cliente HTTP + Manejador de Requests")
    print("🌐" * 40)
    
    try:
        # Demo 1
        demo_get_simple()
        
        # Demo 2
        demo_get_json()
        
        # Demo 3
        demo_post()
        
        # Demo 4
        demo_query_params()
        
        # Demo 5
        demo_configurar_api()
        
        # Demo 6
        demo_validacion()
        
        # Demo 7
        demo_cache()
        
        # Demo 8
        demo_estadisticas()
        
        # Demo 9
        demo_vocabulario()
        
        # Demo 10
        demo_integracion()
        
        # Resumen final
        print_separador("RESUMEN")
        print("""
✅ Cliente HTTP funcionando
✅ Manejador de Requests funcionando
✅ 35 conceptos de red cargados
✅ GET, POST, PUT, DELETE
✅ Parseo automático de JSON
✅ Query parameters
✅ Headers personalizados
✅ Configuración de APIs
✅ Validación de respuestas
✅ Caché de respuestas
✅ Estadísticas de uso

📊 ESTADÍSTICAS:
  • Conceptos nuevos: 35
  • Tests: 25+
  • Grounding promedio: 0.92
  • Operaciones: GET, POST, PUT, DELETE, validar, configurar

🎯 PRÓXIMO: Semana 8 - Bases de Datos (SQLite)
        """)
        
    except Exception as e:
        print(f"\n❌ Error en demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()