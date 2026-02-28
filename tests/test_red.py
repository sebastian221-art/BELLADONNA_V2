"""
Tests para Cliente HTTP y Manejador de Requests.
FASE 3 - Tests de red y APIs.
"""

import pytest
from pathlib import Path
import sys
import json

proyecto_path = Path(__file__).parent.parent
sys.path.insert(0, str(proyecto_path))

from red.cliente_http import ClienteHTTP, Respuesta
from red.manejador_requests import ManejadorRequests, ConfiguracionAPI


class TestClienteHTTP:
    """Tests del cliente HTTP básico."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.cliente = ClienteHTTP(timeout=10)
    
    def test_crear_cliente(self):
        """Test: crear cliente HTTP."""
        assert self.cliente is not None
        assert self.cliente.timeout == 10
        assert self.cliente.max_reintentos == 3
    
    def test_get_simple(self):
        """Test: GET request simple."""
        # Usar JSONPlaceholder (API pública de prueba)
        respuesta = self.cliente.get("https://jsonplaceholder.typicode.com/todos/1")
        
        assert respuesta.codigo_estado == 200
        assert respuesta.exitoso is True
        assert len(respuesta.contenido) > 0
    
    def test_get_con_params(self):
        """Test: GET con query parameters."""
        respuesta = self.cliente.get(
            "https://jsonplaceholder.typicode.com/comments",
            params={'postId': 1}
        )
        
        assert respuesta.exitoso is True
        assert "postId" in respuesta.url or "postId=1" in respuesta.url
    
    def test_get_json(self):
        """Test: GET con parseo JSON."""
        exitoso, datos = self.cliente.get_json(
            "https://jsonplaceholder.typicode.com/todos/1"
        )
        
        assert exitoso is True
        assert isinstance(datos, dict)
        assert 'id' in datos
        assert 'title' in datos
    
    def test_post_json(self):
        """Test: POST con JSON."""
        datos = {
            'title': 'Test',
            'body': 'Test body',
            'userId': 1
        }
        
        respuesta = self.cliente.post(
            "https://jsonplaceholder.typicode.com/posts",
            json_data=datos
        )
        
        assert respuesta.codigo_estado == 201
        assert respuesta.exitoso is True
    
    def test_put_request(self):
        """Test: PUT request."""
        datos = {
            'id': 1,
            'title': 'Updated',
            'body': 'Updated body',
            'userId': 1
        }
        
        respuesta = self.cliente.put(
            "https://jsonplaceholder.typicode.com/posts/1",
            json_data=datos
        )
        
        assert respuesta.codigo_estado == 200
        assert respuesta.exitoso is True
    
    def test_delete_request(self):
        """Test: DELETE request."""
        respuesta = self.cliente.delete(
            "https://jsonplaceholder.typicode.com/posts/1"
        )
        
        assert respuesta.codigo_estado == 200
        assert respuesta.exitoso is True
    
    def test_headers_personalizados(self):
        """Test: headers personalizados."""
        headers = {
            'X-Custom-Header': 'test-value'
        }
        
        respuesta = self.cliente.get(
            "https://jsonplaceholder.typicode.com/todos/1",
            headers=headers
        )
        
        assert respuesta.exitoso is True
    
    def test_url_inexistente(self):
        """Test: manejo de URL inexistente."""
        respuesta = self.cliente.get(
            "https://jsonplaceholder.typicode.com/noexiste"
        )
        
        assert respuesta.codigo_estado == 404
        assert respuesta.exitoso is False


class TestRespuesta:
    """Tests de la clase Respuesta."""
    
    def test_respuesta_exitosa(self):
        """Test: respuesta exitosa."""
        resp = Respuesta(
            codigo_estado=200,
            contenido='{"test": true}',
            headers={'Content-Type': 'application/json'},
            url='https://test.com',
            exitoso=True,
            tiempo_respuesta=0.5
        )
        
        assert resp.codigo_estado == 200
        assert resp.exitoso is True
        assert resp.error is None
    
    def test_respuesta_con_error(self):
        """Test: respuesta con error."""
        resp = Respuesta(
            codigo_estado=500,
            contenido='',
            headers={},
            url='https://test.com',
            exitoso=False,
            tiempo_respuesta=1.0,
            error='Server Error'
        )
        
        assert resp.codigo_estado == 500
        assert resp.exitoso is False
        assert resp.error is not None


class TestManejadorRequests:
    """Tests del manejador de requests."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.manejador = ManejadorRequests()
    
    def test_crear_manejador(self):
        """Test: crear manejador."""
        assert self.manejador is not None
        assert len(self.manejador.configuraciones) == 0
    
    def test_configurar_api(self):
        """Test: configurar una API."""
        self.manejador.configurar_api(
            "test_api",
            "https://api.test.com",
            headers={'Authorization': 'Bearer token'}
        )
        
        assert "test_api" in self.manejador.configuraciones
        config = self.manejador.configuraciones["test_api"]
        assert config.base_url == "https://api.test.com"
        assert 'Authorization' in config.headers
    
    def test_request_api(self):
        """Test: hacer request a API configurada."""
        self.manejador.configurar_api(
            "jsonplaceholder",
            "https://jsonplaceholder.typicode.com"
        )
        
        respuesta = self.manejador.request_api(
            "jsonplaceholder",
            "/todos/1",
            method='GET'
        )
        
        assert respuesta.exitoso is True
        assert respuesta.codigo_estado == 200
    
    def test_api_no_configurada(self):
        """Test: error con API no configurada."""
        with pytest.raises(ValueError):
            self.manejador.request_api("no_existe", "/test")
    
    def test_cache_respuestas(self):
        """Test: caché de respuestas."""
        url = "https://jsonplaceholder.typicode.com/todos/1"
        
        # Primera llamada
        resp1 = self.manejador.get_con_cache(url)
        
        # Segunda llamada (debería venir del caché)
        resp2 = self.manejador.get_con_cache(url)
        
        assert resp1.codigo_estado == resp2.codigo_estado
        assert len(self.manejador.cache) > 0
    
    def test_limpiar_cache(self):
        """Test: limpiar caché."""
        url = "https://jsonplaceholder.typicode.com/todos/1"
        
        self.manejador.get_con_cache(url)
        assert len(self.manejador.cache) > 0
        
        self.manejador.limpiar_cache()
        assert len(self.manejador.cache) == 0
    
    def test_validar_respuesta_exitosa(self):
        """Test: validar respuesta exitosa."""
        resp = Respuesta(
            codigo_estado=200,
            contenido='test',
            headers={},
            url='https://test.com',
            exitoso=True,
            tiempo_respuesta=0.1
        )
        
        valida, errores = self.manejador.validar_respuesta(resp)
        
        assert valida is True
        assert len(errores) == 0
    
    def test_validar_respuesta_fallida(self):
        """Test: validar respuesta fallida."""
        resp = Respuesta(
            codigo_estado=500,
            contenido='',
            headers={},
            url='https://test.com',
            exitoso=False,
            tiempo_respuesta=0.1,
            error='Server Error'
        )
        
        valida, errores = self.manejador.validar_respuesta(resp)
        
        assert valida is False
        assert len(errores) > 0
    
    def test_validaciones_custom(self):
        """Test: validaciones personalizadas."""
        resp = Respuesta(
            codigo_estado=200,
            contenido='test',
            headers={},
            url='https://test.com',
            exitoso=True,
            tiempo_respuesta=0.1
        )
        
        def validar_contenido(r):
            return len(r.contenido) > 0
        
        valida, errores = self.manejador.validar_respuesta(
            resp,
            validaciones={'tiene_contenido': validar_contenido}
        )
        
        assert valida is True
    
    def test_parsear_json(self):
        """Test: parsear JSON de respuesta."""
        resp = Respuesta(
            codigo_estado=200,
            contenido='{"test": true}',
            headers={},
            url='https://test.com',
            exitoso=True,
            tiempo_respuesta=0.1
        )
        
        exitoso, datos = self.manejador.parsear_json_respuesta(resp)
        
        assert exitoso is True
        assert isinstance(datos, dict)
        assert datos['test'] is True
    
    def test_parsear_json_invalido(self):
        """Test: parsear JSON inválido."""
        resp = Respuesta(
            codigo_estado=200,
            contenido='invalid json',
            headers={},
            url='https://test.com',
            exitoso=True,
            tiempo_respuesta=0.1
        )
        
        exitoso, datos = self.manejador.parsear_json_respuesta(resp)
        
        assert exitoso is False
    
    def test_estadisticas(self):
        """Test: obtener estadísticas."""
        self.manejador.configurar_api(
            "jsonplaceholder",
            "https://jsonplaceholder.typicode.com"
        )
        
        # Hacer varios requests
        self.manejador.request_api("jsonplaceholder", "/todos/1")
        self.manejador.request_api("jsonplaceholder", "/todos/2")
        
        stats = self.manejador.obtener_estadisticas()
        
        assert stats['total_requests'] == 2
        assert stats['exitosos'] >= 0
        assert 'tiempo_promedio' in stats
    
    def test_historial(self):
        """Test: historial de requests."""
        self.manejador.configurar_api(
            "jsonplaceholder",
            "https://jsonplaceholder.typicode.com"
        )
        
        self.manejador.request_api("jsonplaceholder", "/todos/1")
        
        assert len(self.manejador.historial_requests) == 1
        
        self.manejador.limpiar_historial()
        assert len(self.manejador.historial_requests) == 0


class TestBatchRequests:
    """Tests de requests en batch."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.manejador = ManejadorRequests()
    
    def test_batch_get(self):
        """Test: múltiples GET en batch."""
        requests = [
            {'url': 'https://jsonplaceholder.typicode.com/todos/1', 'method': 'GET'},
            {'url': 'https://jsonplaceholder.typicode.com/todos/2', 'method': 'GET'},
        ]
        
        respuestas = self.manejador.hacer_batch_requests(requests)
        
        assert len(respuestas) == 2
        assert all(r.exitoso for r in respuestas)


class TestConfiguracionAPI:
    """Tests de configuración de API."""
    
    def test_crear_configuracion(self):
        """Test: crear configuración."""
        config = ConfiguracionAPI(
            base_url="https://api.test.com",
            headers={'Auth': 'token'},
            timeout=60
        )
        
        assert config.base_url == "https://api.test.com"
        assert config.timeout == 60
        assert 'Auth' in config.headers


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])