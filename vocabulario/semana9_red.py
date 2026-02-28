"""
Vocabulario de Red y APIs - Semana 9 (Fase 3) - VERSIÓN CORREGIDA v2.
35 conceptos relacionados con networking y HTTP.

═══════════════════════════════════════════════════════════════════════════════
CORRECCIONES FASE 4A v2:
- ✅ CONCEPTO_HTTP_PUT: Sin "reemplazar" (conflicto con CONCEPTO_REEMPLAZAR)
     Ahora usa: "put request", "actualizar completo", "update http"
═══════════════════════════════════════════════════════════════════════════════
"""

from pathlib import Path
import sys

proyecto_path = Path(__file__).parent.parent
sys.path.insert(0, str(proyecto_path))

from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto

# Importar cliente y manejador
cliente_http = None
manejador_requests = None

def configurar_red(cliente, manejador):
    """Configura cliente y manejador para los conceptos."""
    global cliente_http, manejador_requests
    cliente_http = cliente
    manejador_requests = manejador

def obtener_conceptos_red():
    """Retorna 35 conceptos de red y APIs."""
    conceptos = []
    
    # ========== HTTP MÉTODOS (5) ==========
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_HTTP_GET",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["get request", "obtener", "consultar", "leer http"],
        operaciones={'ejecutar': lambda url: cliente_http.get(url) if cliente_http else None},
        confianza_grounding=1.0,
        propiedades={'metodo': 'GET', 'idempotente': True, 'seguro': True}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_HTTP_POST",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["post request", "enviar", "publicar", "crear recurso"],
        operaciones={'ejecutar': lambda url, data: cliente_http.post(url, json_data=data) if cliente_http else None},
        confianza_grounding=1.0,
        propiedades={'metodo': 'POST', 'idempotente': False, 'seguro': False}
    ))
    
    # ═══════════════════════════════════════════════════════════════════════
    # ✅ FIX: CONCEPTO_HTTP_PUT - Sin "reemplazar"
    #    "reemplazar" está en CONCEPTO_REEMPLAZAR (semana3_sistema_avanzado)
    # ═══════════════════════════════════════════════════════════════════════
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_HTTP_PUT",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "put request",         # ← Principal
            "actualizar completo", # ← Descripción semántica
            "update http",         # ← Técnico
            "sobrescribir recurso" # ← Alternativa
            # "reemplazar" ELIMINADO → CONCEPTO_REEMPLAZAR
        ],
        operaciones={'ejecutar': lambda url, data: cliente_http.put(url, json_data=data) if cliente_http else None},
        confianza_grounding=1.0,
        propiedades={'metodo': 'PUT', 'idempotente': True}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_HTTP_DELETE",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["delete request", "borrar recurso", "eliminar http"],
        operaciones={'ejecutar': lambda url: cliente_http.delete(url) if cliente_http else None},
        confianza_grounding=1.0,
        propiedades={'metodo': 'DELETE', 'idempotente': True}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_REQUEST",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["request", "petición", "solicitud http"],
        confianza_grounding=0.95,
        propiedades={'es': 'solicitud HTTP', 'contiene': ['método', 'url', 'headers', 'body']}
    ))
    
    # ========== RESPUESTA (6) ==========
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RESPUESTA_HTTP",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["respuesta http", "response", "resultado http"],
        confianza_grounding=0.95,
        propiedades={'contiene': ['código', 'contenido', 'headers'], 'de': 'servidor'}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CODIGO_ESTADO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["código de estado", "status code", "código http"],
        confianza_grounding=0.9,
        propiedades={'ejemplos': [200, 404, 500], 'indica': 'resultado del request'}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_200_OK",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["200", "ok", "éxito"],
        confianza_grounding=0.9,
        propiedades={'codigo': 200, 'significa': 'request exitoso'}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_404_NOT_FOUND",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["404", "not found", "no encontrado"],
        confianza_grounding=0.9,
        propiedades={'codigo': 404, 'significa': 'recurso no existe'}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_500_ERROR",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["500", "server error", "error servidor"],
        confianza_grounding=0.9,
        propiedades={'codigo': 500, 'significa': 'error en servidor'}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CONTENIDO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["contenido", "body", "cuerpo respuesta"],
        confianza_grounding=0.9,
        propiedades={'es': 'datos de respuesta', 'puede_ser': ['JSON', 'HTML', 'texto']}
    ))
    
    # ========== JSON (4) ==========
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_JSON",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["json", "javascript object notation"],
        confianza_grounding=0.95,
        propiedades={'es': 'formato de datos', 'basado_en': 'texto', 'estructura': 'clave-valor'}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PARSEAR_JSON",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["parsear json", "decodificar json", "convertir json"],
        confianza_grounding=1.0,
        propiedades={'convierte': 'string a objeto', 'puede_fallar': True}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_GET_JSON",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["get json", "obtener json", "consultar json"],
        operaciones={'ejecutar': lambda url: cliente_http.get_json(url) if cliente_http else (False, None)},
        confianza_grounding=1.0,
        propiedades={'hace': 'GET + parseo JSON automático'}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_POST_JSON",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["post json", "enviar json", "crear con json"],
        operaciones={'ejecutar': lambda url, data: cliente_http.post_json(url, data) if cliente_http else (False, None)},
        confianza_grounding=1.0,
        propiedades={'hace': 'POST con JSON + parseo respuesta'}
    ))
    
    # ========== HEADERS (4) ==========
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_HEADERS",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["headers", "cabeceras", "encabezados http"],
        confianza_grounding=0.9,
        propiedades={'son': 'metadatos del request/respuesta', 'formato': 'clave: valor'}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CONTENT_TYPE",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["content-type", "tipo de contenido"],
        confianza_grounding=0.9,
        propiedades={'indica': 'tipo de datos', 'ejemplos': ['application/json', 'text/html']}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_USER_AGENT",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["user-agent", "agente usuario"],
        confianza_grounding=0.9,
        propiedades={'identifica': 'cliente', 'ejemplo': 'Mozilla/5.0'}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_AUTHORIZATION",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["authorization", "autorización", "auth header"],
        confianza_grounding=0.9,
        propiedades={'para': 'autenticación', 'tipos': ['Bearer', 'Basic']}
    ))
    
    # ========== URL y PARAMS (4) ==========
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_URL",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["url", "dirección web", "uniform resource locator"],
        confianza_grounding=0.95,
        propiedades={'partes': ['protocolo', 'dominio', 'path', 'query'], 'ejemplo': 'https://api.com/users?id=1'}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ENDPOINT",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["endpoint", "ruta api", "punto acceso"],
        confianza_grounding=0.9,
        propiedades={'es': 'punto de acceso de API', 'ejemplo': '/users/123'}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_QUERY_PARAMS",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["query parameters", "parámetros url", "params"],
        confianza_grounding=0.9,
        propiedades={'formato': 'key=value', 'separan': '&', 'ejemplo': '?page=1&limit=10'}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_BASE_URL",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["base url", "url base", "dominio api"],
        confianza_grounding=0.9,
        propiedades={'es': 'URL raíz de API', 'ejemplo': 'https://api.github.com'}
    ))
    
    # ========== CONFIGURACIÓN (4) ==========
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CONFIGURAR_API",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["configurar api", "setup api", "definir api"],
        operaciones={'ejecutar': lambda nombre, url: manejador_requests.configurar_api(nombre, url) if manejador_requests else None},
        confianza_grounding=1.0,
        propiedades={'define': 'configuración reutilizable', 'incluye': ['base_url', 'headers', 'timeout']}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TIMEOUT",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["timeout", "tiempo límite", "expiración"],
        confianza_grounding=0.9,
        propiedades={'es': 'tiempo máximo de espera', 'unidad': 'segundos', 'previene': 'espera infinita'}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_REINTENTOS_HTTP",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["reintentos http", "retry http", "intentos http"],
        confianza_grounding=0.9,
        propiedades={'es': 'volver a intentar', 'cuando': 'falla temporal', 'tiene': 'límite máximo'}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CACHE",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["cache", "caché", "almacenar respuestas"],
        confianza_grounding=0.9,
        propiedades={'es': 'almacenamiento temporal', 'reduce': 'requests redundantes', 'mejora': 'velocidad'}
    ))
    
    # ========== MANEJO DE ERRORES (4) ==========
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ERROR_RED",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["error de red", "network error", "fallo conexión"],
        confianza_grounding=0.9,
        propiedades={'ocurre_cuando': 'no hay conexión', 'ejemplos': ['timeout', 'DNS failure', 'connection refused']}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_HTTP_ERROR",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["error http", "http error", "status error"],
        confianza_grounding=0.9,
        propiedades={'es': 'código 4xx o 5xx', 'indica': 'request no exitoso'}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_VALIDAR_RESPUESTA",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["validar respuesta", "verificar respuesta", "comprobar respuesta"],
        operaciones={'ejecutar': lambda resp: manejador_requests.validar_respuesta(resp) if manejador_requests else (False, [])},
        confianza_grounding=1.0,
        propiedades={'verifica': 'corrección de respuesta', 'retorna': '(válida, errores)'}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MANEJO_ERRORES",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["manejo de errores", "error handling", "gestión errores"],
        confianza_grounding=0.9,
        propiedades={'incluye': ['try/catch', 'reintentos', 'fallback'], 'previene': 'crashes'}
    ))
    
    # ========== API (4) ==========
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_API",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["api", "application programming interface", "interfaz"],
        confianza_grounding=0.95,
        propiedades={'es': 'interfaz de programación', 'permite': 'comunicación entre sistemas'}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_REST_API",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["rest api", "restful", "api rest"],
        confianza_grounding=0.95,
        propiedades={'es': 'arquitectura API', 'usa': 'HTTP', 'basada_en': 'recursos'}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RECURSO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["recurso", "resource", "entidad api"],
        confianza_grounding=0.9,
        propiedades={'es': 'objeto en API', 'ejemplos': ['user', 'post', 'comment'], 'tiene': 'URL única'}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CLIENTE_HTTP",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["cliente http", "http client"],
        confianza_grounding=1.0,
        propiedades={'es': 'componente para requests', 'soporta': ['GET', 'POST', 'PUT', 'DELETE']}
    ))
    
    return conceptos

if __name__ == '__main__':
    conceptos = obtener_conceptos_red()
    print(f"✅ Vocabulario Red CORREGIDO v2: {len(conceptos)} conceptos")
    print(f"   ✅ CONCEPTO_HTTP_PUT sin 'reemplazar'")
    con_grounding_1 = sum(1 for c in conceptos if c.confianza_grounding == 1.0)
    print(f"   - Grounding 1.0: {con_grounding_1}")
    print(f"   - Grounding promedio: {sum(c.confianza_grounding for c in conceptos) / len(conceptos):.2f}")