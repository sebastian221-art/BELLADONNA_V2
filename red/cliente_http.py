"""
Cliente HTTP para realizar requests.
FASE 3 - Semana 7
"""

from typing import Dict, Optional, Any
from dataclasses import dataclass
import urllib.request
import urllib.parse
import urllib.error
import json
import time


@dataclass
class Respuesta:
    """Respuesta de un request HTTP."""
    codigo_estado: int
    contenido: str
    headers: Dict[str, str]
    url: str
    exitoso: bool
    tiempo_respuesta: float
    error: Optional[str] = None


class ClienteHTTP:
    """
    Cliente HTTP simple usando urllib (sin dependencias externas).
    
    Capacidades:
    - GET, POST, PUT, DELETE
    - Headers personalizados
    - Query parameters
    - JSON automático
    - Timeouts
    - Reintentos
    """
    
    def __init__(self, timeout: int = 30, max_reintentos: int = 3):
        """
        Inicializa el cliente HTTP.
        
        Args:
            timeout: Timeout en segundos
            max_reintentos: Número máximo de reintentos
        """
        self.timeout = timeout
        self.max_reintentos = max_reintentos
        self.headers_default = {
            'User-Agent': 'Belladonna-HTTP-Client/1.0',
            'Accept': 'application/json, text/plain, */*'
        }
    
    def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Respuesta:
        """
        Realiza un request GET.
        
        Args:
            url: URL del recurso
            params: Parámetros de query
            headers: Headers adicionales
            
        Returns:
            Respuesta
            
        Example:
            >>> cliente = ClienteHTTP()
            >>> respuesta = cliente.get("https://api.github.com/users/github")
            >>> print(respuesta.codigo_estado)  # 200
        """
        if params:
            url = self._agregar_params(url, params)
        
        return self._hacer_request('GET', url, headers=headers)
    
    def post(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Respuesta:
        """
        Realiza un request POST.
        
        Args:
            url: URL del recurso
            data: Datos form-encoded
            json_data: Datos JSON
            headers: Headers adicionales
            
        Returns:
            Respuesta
        """
        body = None
        headers_merged = self._merge_headers(headers)
        
        if json_data:
            body = json.dumps(json_data).encode('utf-8')
            headers_merged['Content-Type'] = 'application/json'
        elif data:
            body = urllib.parse.urlencode(data).encode('utf-8')
            headers_merged['Content-Type'] = 'application/x-www-form-urlencoded'
        
        return self._hacer_request('POST', url, body=body, headers=headers_merged)
    
    def put(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Respuesta:
        """
        Realiza un request PUT.
        
        Args:
            url: URL del recurso
            data: Datos form-encoded
            json_data: Datos JSON
            headers: Headers adicionales
            
        Returns:
            Respuesta
        """
        body = None
        headers_merged = self._merge_headers(headers)
        
        if json_data:
            body = json.dumps(json_data).encode('utf-8')
            headers_merged['Content-Type'] = 'application/json'
        elif data:
            body = urllib.parse.urlencode(data).encode('utf-8')
            headers_merged['Content-Type'] = 'application/x-www-form-urlencoded'
        
        return self._hacer_request('PUT', url, body=body, headers=headers_merged)
    
    def delete(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None
    ) -> Respuesta:
        """
        Realiza un request DELETE.
        
        Args:
            url: URL del recurso
            headers: Headers adicionales
            
        Returns:
            Respuesta
        """
        return self._hacer_request('DELETE', url, headers=headers)
    
    def _hacer_request(
        self,
        method: str,
        url: str,
        body: Optional[bytes] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Respuesta:
        """
        Realiza el request HTTP con reintentos.
        
        Args:
            method: Método HTTP
            url: URL
            body: Cuerpo del request
            headers: Headers
            
        Returns:
            Respuesta
        """
        headers_merged = self._merge_headers(headers)
        
        for intento in range(self.max_reintentos):
            try:
                tiempo_inicio = time.time()
                
                # Crear request
                req = urllib.request.Request(
                    url,
                    data=body,
                    headers=headers_merged,
                    method=method
                )
                
                # Ejecutar request
                with urllib.request.urlopen(req, timeout=self.timeout) as response:
                    contenido = response.read().decode('utf-8')
                    codigo = response.status
                    headers_resp = dict(response.headers)
                
                tiempo_respuesta = time.time() - tiempo_inicio
                
                return Respuesta(
                    codigo_estado=codigo,
                    contenido=contenido,
                    headers=headers_resp,
                    url=url,
                    exitoso=200 <= codigo < 300,
                    tiempo_respuesta=tiempo_respuesta
                )
                
            except urllib.error.HTTPError as e:
                tiempo_respuesta = time.time() - tiempo_inicio
                contenido = e.read().decode('utf-8') if e.fp else ""
                
                return Respuesta(
                    codigo_estado=e.code,
                    contenido=contenido,
                    headers=dict(e.headers) if e.headers else {},
                    url=url,
                    exitoso=False,
                    tiempo_respuesta=tiempo_respuesta,
                    error=f"HTTP Error {e.code}: {e.reason}"
                )
                
            except urllib.error.URLError as e:
                if intento < self.max_reintentos - 1:
                    time.sleep(1)  # Esperar antes de reintentar
                    continue
                
                return Respuesta(
                    codigo_estado=0,
                    contenido="",
                    headers={},
                    url=url,
                    exitoso=False,
                    tiempo_respuesta=0.0,
                    error=f"URL Error: {str(e.reason)}"
                )
                
            except Exception as e:
                return Respuesta(
                    codigo_estado=0,
                    contenido="",
                    headers={},
                    url=url,
                    exitoso=False,
                    tiempo_respuesta=0.0,
                    error=f"Error: {str(e)}"
                )
        
        # Si llegamos aquí, todos los intentos fallaron
        return Respuesta(
            codigo_estado=0,
            contenido="",
            headers={},
            url=url,
            exitoso=False,
            tiempo_respuesta=0.0,
            error="Máximo de reintentos alcanzado"
        )
    
    def _agregar_params(self, url: str, params: Dict[str, Any]) -> str:
        """
        Agrega parámetros de query a la URL.
        
        Args:
            url: URL base
            params: Parámetros
            
        Returns:
            URL con parámetros
        """
        query_string = urllib.parse.urlencode(params)
        separator = '&' if '?' in url else '?'
        return f"{url}{separator}{query_string}"
    
    def _merge_headers(self, headers: Optional[Dict[str, str]]) -> Dict[str, str]:
        """
        Combina headers default con headers personalizados.
        
        Args:
            headers: Headers personalizados
            
        Returns:
            Headers combinados
        """
        merged = self.headers_default.copy()
        if headers:
            merged.update(headers)
        return merged
    
    def get_json(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> tuple[bool, Any]:
        """
        Realiza GET y parsea respuesta como JSON.
        
        Args:
            url: URL
            params: Parámetros
            headers: Headers
            
        Returns:
            (exitoso, datos_json)
        """
        respuesta = self.get(url, params=params, headers=headers)
        
        if not respuesta.exitoso:
            return (False, None)
        
        try:
            datos = json.loads(respuesta.contenido)
            return (True, datos)
        except json.JSONDecodeError:
            return (False, None)
    
    def post_json(
        self,
        url: str,
        json_data: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None
    ) -> tuple[bool, Any]:
        """
        Realiza POST con JSON y parsea respuesta.
        
        Args:
            url: URL
            json_data: Datos a enviar
            headers: Headers
            
        Returns:
            (exitoso, datos_json)
        """
        respuesta = self.post(url, json_data=json_data, headers=headers)
        
        if not respuesta.exitoso:
            return (False, None)
        
        try:
            datos = json.loads(respuesta.contenido)
            return (True, datos)
        except json.JSONDecodeError:
            return (True, respuesta.contenido)


# Ejemplo de uso
if __name__ == '__main__':
    cliente = ClienteHTTP()
    
    # GET simple
    print("GET a JSONPlaceholder...")
    respuesta = cliente.get("https://jsonplaceholder.typicode.com/todos/1")
    print(f"Status: {respuesta.codigo_estado}")
    print(f"Exitoso: {respuesta.exitoso}")
    print(f"Contenido: {respuesta.contenido[:100]}...")
    
    # GET con JSON
    print("\nGET con JSON parsing...")
    exitoso, datos = cliente.get_json("https://jsonplaceholder.typicode.com/todos/1")
    if exitoso:
        print(f"Todo ID: {datos.get('id')}")
        print(f"Title: {datos.get('title')}")
    
    # POST
    print("\nPOST con JSON...")
    nuevo_todo = {
        "title": "Test desde Belladonna",
        "completed": False,
        "userId": 1
    }
    respuesta = cliente.post(
        "https://jsonplaceholder.typicode.com/todos",
        json_data=nuevo_todo
    )
    print(f"Status: {respuesta.codigo_estado}")
    print(f"Creado: {respuesta.exitoso}")