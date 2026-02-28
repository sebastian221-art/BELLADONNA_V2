"""
Manejador de Requests HTTP.
FASE 3 - Semana 7
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
import json
from .cliente_http import ClienteHTTP, Respuesta


@dataclass
class ConfiguracionAPI:
    """Configuración para una API específica."""
    base_url: str
    headers: Dict[str, str] = field(default_factory=dict)
    timeout: int = 30
    autenticacion: Optional[Dict[str, str]] = None


class ManejadorRequests:
    """
    Maneja requests HTTP con configuraciones por API.
    
    Capacidades:
    - Configuraciones por API
    - Rate limiting (simulado)
    - Caché de respuestas
    - Validación de respuestas
    - Manejo de errores
    """
    
    def __init__(self):
        """Inicializa el manejador."""
        self.cliente = ClienteHTTP()
        self.configuraciones: Dict[str, ConfiguracionAPI] = {}
        self.cache: Dict[str, Respuesta] = {}
        self.historial_requests: List[Dict] = []
        self.max_cache = 100
    
    def configurar_api(
        self,
        nombre: str,
        base_url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 30
    ):
        """
        Configura una API para uso posterior.
        
        Args:
            nombre: Nombre de la API
            base_url: URL base
            headers: Headers por defecto
            timeout: Timeout
            
        Example:
            >>> manejador = ManejadorRequests()
            >>> manejador.configurar_api(
            ...     "github",
            ...     "https://api.github.com",
            ...     headers={"Accept": "application/vnd.github.v3+json"}
            ... )
        """
        config = ConfiguracionAPI(
            base_url=base_url,
            headers=headers or {},
            timeout=timeout
        )
        self.configuraciones[nombre] = config
    
    def request_api(
        self,
        nombre_api: str,
        endpoint: str,
        method: str = 'GET',
        **kwargs
    ) -> Respuesta:
        """
        Hace request a una API configurada.
        
        Args:
            nombre_api: Nombre de la API configurada
            endpoint: Endpoint (ej: "/users/github")
            method: Método HTTP
            **kwargs: Argumentos adicionales
            
        Returns:
            Respuesta
        """
        if nombre_api not in self.configuraciones:
            raise ValueError(f"API '{nombre_api}' no configurada")
        
        config = self.configuraciones[nombre_api]
        url = f"{config.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        # Merge headers
        headers = config.headers.copy()
        if 'headers' in kwargs:
            headers.update(kwargs['headers'])
            kwargs['headers'] = headers
        else:
            kwargs['headers'] = headers
        
        # Hacer request según método
        if method.upper() == 'GET':
            respuesta = self.cliente.get(url, **kwargs)
        elif method.upper() == 'POST':
            respuesta = self.cliente.post(url, **kwargs)
        elif method.upper() == 'PUT':
            respuesta = self.cliente.put(url, **kwargs)
        elif method.upper() == 'DELETE':
            respuesta = self.cliente.delete(url, **kwargs)
        else:
            raise ValueError(f"Método '{method}' no soportado")
        
        # Guardar en historial
        self._agregar_historial(nombre_api, endpoint, method, respuesta)
        
        return respuesta
    
    def get_con_cache(
        self,
        url: str,
        forzar_refresh: bool = False,
        **kwargs
    ) -> Respuesta:
        """
        GET con caché de respuestas.
        
        Args:
            url: URL
            forzar_refresh: Si forzar actualización
            **kwargs: Argumentos adicionales
            
        Returns:
            Respuesta (del caché o nueva)
        """
        cache_key = self._generar_cache_key(url, kwargs)
        
        if not forzar_refresh and cache_key in self.cache:
            return self.cache[cache_key]
        
        respuesta = self.cliente.get(url, **kwargs)
        
        if respuesta.exitoso:
            self._guardar_en_cache(cache_key, respuesta)
        
        return respuesta
    
    def validar_respuesta(
        self,
        respuesta: Respuesta,
        validaciones: Dict[str, Callable] = None
    ) -> tuple[bool, List[str]]:
        """
        Valida una respuesta según criterios.
        
        Args:
            respuesta: Respuesta a validar
            validaciones: Dict de validaciones custom
            
        Returns:
            (es_valida, errores)
        """
        errores = []
        
        # Validaciones básicas
        if not respuesta.exitoso:
            errores.append(f"Request falló: {respuesta.error}")
        
        if respuesta.codigo_estado == 0:
            errores.append("No se pudo conectar al servidor")
        
        # Validaciones custom
        if validaciones:
            for nombre, funcion in validaciones.items():
                try:
                    if not funcion(respuesta):
                        errores.append(f"Validación '{nombre}' falló")
                except Exception as e:
                    errores.append(f"Error en validación '{nombre}': {e}")
        
        return (len(errores) == 0, errores)
    
    def parsear_json_respuesta(
        self,
        respuesta: Respuesta
    ) -> tuple[bool, Optional[Any]]:
        """
        Parsea respuesta JSON con manejo de errores.
        
        Args:
            respuesta: Respuesta HTTP
            
        Returns:
            (exitoso, datos)
        """
        if not respuesta.exitoso:
            return (False, None)
        
        try:
            datos = json.loads(respuesta.contenido)
            return (True, datos)
        except json.JSONDecodeError as e:
            return (False, f"Error parseando JSON: {e}")
    
    def hacer_batch_requests(
        self,
        requests: List[Dict[str, Any]],
        paralelo: bool = False
    ) -> List[Respuesta]:
        """
        Hace múltiples requests.
        
        Args:
            requests: Lista de configs de requests
            paralelo: Si ejecutar en paralelo (futuro)
            
        Returns:
            Lista de respuestas
        """
        respuestas = []
        
        for req_config in requests:
            url = req_config['url']
            method = req_config.get('method', 'GET')
            
            if method == 'GET':
                resp = self.cliente.get(url, **req_config.get('kwargs', {}))
            elif method == 'POST':
                resp = self.cliente.post(url, **req_config.get('kwargs', {}))
            else:
                raise ValueError(f"Método '{method}' no soportado en batch")
            
            respuestas.append(resp)
        
        return respuestas
    
    def _generar_cache_key(self, url: str, kwargs: Dict) -> str:
        """Genera clave de caché."""
        params = kwargs.get('params', {})
        params_str = json.dumps(params, sort_keys=True)
        return f"{url}?{params_str}"
    
    def _guardar_en_cache(self, key: str, respuesta: Respuesta):
        """Guarda respuesta en caché."""
        if len(self.cache) >= self.max_cache:
            # Eliminar entrada más antigua (FIFO simple)
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
        
        self.cache[key] = respuesta
    
    def _agregar_historial(
        self,
        api: str,
        endpoint: str,
        method: str,
        respuesta: Respuesta
    ):
        """Agrega request al historial."""
        entrada = {
            'api': api,
            'endpoint': endpoint,
            'method': method,
            'codigo': respuesta.codigo_estado,
            'exitoso': respuesta.exitoso,
            'tiempo': respuesta.tiempo_respuesta
        }
        self.historial_requests.append(entrada)
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de requests.
        
        Returns:
            Dict con estadísticas
        """
        if not self.historial_requests:
            return {'total': 0}
        
        total = len(self.historial_requests)
        exitosos = sum(1 for r in self.historial_requests if r['exitoso'])
        tiempo_total = sum(r['tiempo'] for r in self.historial_requests)
        tiempo_promedio = tiempo_total / total if total > 0 else 0
        
        return {
            'total_requests': total,
            'exitosos': exitosos,
            'fallidos': total - exitosos,
            'tasa_exito': (exitosos / total * 100) if total > 0 else 0,
            'tiempo_promedio': tiempo_promedio,
            'tiempo_total': tiempo_total
        }
    
    def limpiar_cache(self):
        """Limpia el caché de respuestas."""
        self.cache.clear()
    
    def limpiar_historial(self):
        """Limpia el historial de requests."""
        self.historial_requests.clear()


# Ejemplo de uso
if __name__ == '__main__':
    manejador = ManejadorRequests()
    
    # Configurar API
    manejador.configurar_api(
        "jsonplaceholder",
        "https://jsonplaceholder.typicode.com",
        headers={"Content-Type": "application/json"}
    )
    
    # Hacer request
    print("Request a API configurada...")
    respuesta = manejador.request_api(
        "jsonplaceholder",
        "/todos/1",
        method='GET'
    )
    print(f"Status: {respuesta.codigo_estado}")
    print(f"Contenido: {respuesta.contenido[:100]}...")
    
    # Validar respuesta
    def validar_json(resp):
        try:
            json.loads(resp.contenido)
            return True
        except:
            return False
    
    valida, errores = manejador.validar_respuesta(
        respuesta,
        validaciones={'es_json': validar_json}
    )
    print(f"\nValidación: {'✅' if valida else '❌'}")
    
    # Estadísticas
    stats = manejador.obtener_estadisticas()
    print(f"\nEstadísticas:")
    print(f"  Total requests: {stats['total_requests']}")
    print(f"  Tasa de éxito: {stats['tasa_exito']:.1f}%")