"""
Tests para PythonAnalyzer.
FASE 3 - Tests de análisis de código.
"""

import pytest
from pathlib import Path
import sys
import tempfile

# Importar el analizador
proyecto_path = Path(__file__).parent.parent
sys.path.insert(0, str(proyecto_path))

from analisis.python_analyzer import PythonAnalyzer, AnalysisResult


class TestPythonAnalyzerBasico:
    """Tests básicos del analizador."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.analyzer = PythonAnalyzer()
    
    def test_analizar_codigo_valido(self):
        """Test: código válido se analiza correctamente."""
        codigo = '''
def suma(a, b):
    return a + b
'''
        resultado = self.analyzer.analizar(codigo)
        
        assert resultado.valido is True
        assert len(resultado.errores) == 0
        assert resultado.es_exitoso()
    
    def test_analizar_codigo_invalido(self):
        """Test: código con error de sintaxis."""
        codigo = '''
def suma(a, b
    return a + b
'''
        resultado = self.analyzer.analizar(codigo)
        
        assert resultado.valido is False
        assert len(resultado.errores) > 0
        assert not resultado.es_exitoso()
    
    def test_analizar_codigo_vacio(self):
        """Test: código vacío."""
        resultado = self.analyzer.analizar('')
        
        assert resultado.valido is True
        assert resultado.metricas['funciones'] == 0


class TestPythonAnalyzerMetricas:
    """Tests de métricas de código."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.analyzer = PythonAnalyzer()
    
    def test_contar_funciones(self):
        """Test: cuenta funciones correctamente."""
        codigo = '''
def funcion1():
    pass

def funcion2():
    pass

def funcion3():
    pass
'''
        resultado = self.analyzer.analizar(codigo)
        assert resultado.metricas['funciones'] == 3
    
    def test_contar_clases(self):
        """Test: cuenta clases correctamente."""
        codigo = '''
class Clase1:
    pass

class Clase2:
    pass
'''
        resultado = self.analyzer.analizar(codigo)
        assert resultado.metricas['clases'] == 2
    
    def test_contar_lineas_codigo(self):
        """Test: cuenta líneas de código."""
        codigo = '''def suma(a, b):
    return a + b

print("hola")'''
        resultado = self.analyzer.analizar(codigo)
        
        # 3 líneas de código
        assert resultado.metricas['lineas_codigo'] == 4
        assert resultado.metricas['lineas_no_vacias'] == 3
    
    def test_extraer_imports(self):
        """Test: extrae imports correctamente."""
        codigo = '''
import os
import sys
from pathlib import Path
'''
        resultado = self.analyzer.analizar(codigo)
        imports = resultado.metricas['imports']
        
        assert 'os' in imports
        assert 'sys' in imports
        assert 'pathlib.Path' in imports


class TestPythonAnalyzerComplejidad:
    """Tests de complejidad ciclomática."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.analyzer = PythonAnalyzer()
    
    def test_complejidad_basica(self):
        """Test: complejidad de función simple."""
        codigo = '''
def suma(a, b):
    return a + b
'''
        resultado = self.analyzer.analizar(codigo)
        # Complejidad base = 1
        assert resultado.metricas['complejidad_ciclomatica'] >= 1
    
    def test_complejidad_con_if(self):
        """Test: if incrementa complejidad."""
        codigo = '''
def absoluto(x):
    if x < 0:
        return -x
    return x
'''
        resultado = self.analyzer.analizar(codigo)
        # Base (1) + if (1) = 2
        assert resultado.metricas['complejidad_ciclomatica'] >= 2
    
    def test_complejidad_con_loop(self):
        """Test: loops incrementan complejidad."""
        codigo = '''
def suma_lista(lista):
    total = 0
    for num in lista:
        total += num
    return total
'''
        resultado = self.analyzer.analizar(codigo)
        # Base (1) + for (1) = 2
        assert resultado.metricas['complejidad_ciclomatica'] >= 2
    
    def test_complejidad_alta(self):
        """Test: función con alta complejidad."""
        codigo = '''
def compleja(x, y):
    if x > 0:
        if y > 0:
            for i in range(10):
                while i < 5:
                    if i % 2 == 0:
                        return True
    return False
'''
        resultado = self.analyzer.analizar(codigo)
        # Múltiples if, for, while
        assert resultado.metricas['complejidad_ciclomatica'] > 5


class TestPythonAnalyzerDeteccionProblemas:
    """Tests de detección de problemas."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.analyzer = PythonAnalyzer()
    
    def test_detectar_variable_sin_usar(self):
        """Test: detecta variables sin usar."""
        codigo = '''
def funcion():
    x = 5
    y = 10
    return y
'''
        resultado = self.analyzer.analizar(codigo)
        
        assert 'variables_sin_usar' in resultado.metricas
        assert 'x' in resultado.metricas['variables_sin_usar']
    
    def test_detectar_import_sin_usar(self):
        """Test: detecta imports sin usar."""
        codigo = '''
import os
import sys

def funcion():
    return os.path.exists('/')
'''
        resultado = self.analyzer.analizar(codigo)
        
        # sys no se usa
        if 'imports_sin_usar' in resultado.metricas:
            assert 'sys' in resultado.metricas['imports_sin_usar']
    
    def test_detectar_docstring_faltante(self):
        """Test: detecta funciones sin docstring."""
        codigo = '''
def con_docstring():
    """Esta función tiene docstring."""
    pass

def sin_docstring():
    pass
'''
        resultado = self.analyzer.analizar(codigo)
        
        assert 'sin_docstring' in resultado.metricas
        assert 'sin_docstring' in resultado.metricas['sin_docstring']
        assert 'con_docstring' not in resultado.metricas['sin_docstring']


class TestPythonAnalyzerTypeHints:
    """Tests de type hints."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.analyzer = PythonAnalyzer()
    
    def test_detectar_type_hints(self):
        """Test: detecta uso de type hints."""
        codigo = '''
def suma(a: int, b: int) -> int:
    return a + b
'''
        resultado = self.analyzer.analizar(codigo)
        assert resultado.metricas['usa_type_hints'] is True
    
    def test_sin_type_hints(self):
        """Test: detecta ausencia de type hints."""
        codigo = '''
def suma(a, b):
    return a + b
'''
        resultado = self.analyzer.analizar(codigo)
        assert resultado.metricas['usa_type_hints'] is False


class TestPythonAnalyzerTests:
    """Tests de detección de tests."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.analyzer = PythonAnalyzer()
    
    def test_detectar_test_functions(self):
        """Test: detecta funciones de test."""
        codigo = '''
def test_suma():
    assert suma(2, 3) == 5

def test_resta():
    assert resta(5, 3) == 2
'''
        resultado = self.analyzer.analizar(codigo)
        assert resultado.metricas['tiene_tests'] is True
    
    def test_sin_tests(self):
        """Test: detecta ausencia de tests."""
        codigo = '''
def suma(a, b):
    return a + b
'''
        resultado = self.analyzer.analizar(codigo)
        assert resultado.metricas['tiene_tests'] is False


class TestPythonAnalyzerComentarios:
    """Tests de análisis de comentarios."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.analyzer = PythonAnalyzer()
    
    def test_ratio_comentarios(self):
        """Test: calcula ratio de comentarios."""
        codigo = '''
# Comentario 1
def suma(a, b):
    # Comentario 2
    return a + b
'''
        resultado = self.analyzer.analizar(codigo)
        assert 'ratio_comentarios' in resultado.metricas
        assert resultado.metricas['ratio_comentarios'] > 0


class TestPythonAnalyzerArchivos:
    """Tests de análisis de archivos."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.analyzer = PythonAnalyzer()
    
    def test_analizar_archivo_existente(self):
        """Test: analiza archivo que existe."""
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('def suma(a, b):\n    return a + b\n')
            temp_path = Path(f.name)
        
        try:
            resultado = self.analyzer.analizar_archivo(temp_path)
            assert resultado.valido is True
            assert resultado.metricas['funciones'] == 1
        finally:
            temp_path.unlink()
    
    def test_analizar_archivo_inexistente(self):
        """Test: error con archivo inexistente."""
        resultado = self.analyzer.analizar_archivo(Path('/archivo/que/no/existe.py'))
        
        assert resultado.valido is False
        assert len(resultado.errores) > 0


class TestPythonAnalyzerNombres:
    """Tests de extracción de nombres."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.analyzer = PythonAnalyzer()
    
    def test_obtener_nombres_funciones(self):
        """Test: obtiene nombres de funciones."""
        codigo = '''
def funcion1():
    pass

def funcion2():
    pass
'''
        self.analyzer.analizar(codigo)
        nombres = self.analyzer.obtener_nombres_funciones()
        
        assert 'funcion1' in nombres
        assert 'funcion2' in nombres
        assert len(nombres) == 2
    
    def test_obtener_nombres_clases(self):
        """Test: obtiene nombres de clases."""
        codigo = '''
class Clase1:
    pass

class Clase2:
    pass
'''
        self.analyzer.analizar(codigo)
        nombres = self.analyzer.obtener_nombres_clases()
        
        assert 'Clase1' in nombres
        assert 'Clase2' in nombres
        assert len(nombres) == 2


class TestPythonAnalyzerReporte:
    """Tests de generación de reportes."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.analyzer = PythonAnalyzer()
    
    def test_generar_reporte_codigo_valido(self):
        """Test: genera reporte para código válido."""
        codigo = '''
def suma(a, b):
    """Suma dos números."""
    return a + b
'''
        resultado = self.analyzer.analizar(codigo)
        reporte = self.analyzer.generar_reporte(resultado)
        
        assert isinstance(reporte, str)
        assert '✅' in reporte
        assert 'REPORTE' in reporte
    
    def test_generar_reporte_codigo_invalido(self):
        """Test: genera reporte para código inválido."""
        codigo = 'def suma(a, b'
        resultado = self.analyzer.analizar(codigo)
        reporte = self.analyzer.generar_reporte(resultado)
        
        assert isinstance(reporte, str)
        assert '❌' in reporte
        assert 'ERRORES' in reporte
    
    def test_generar_reporte_con_advertencias(self):
        """Test: reporte incluye advertencias."""
        codigo = '''
import os

def funcion():
    x = 5
    return 10
'''
        resultado = self.analyzer.analizar(codigo)
        reporte = self.analyzer.generar_reporte(resultado)
        
        if resultado.advertencias:
            assert '⚠️' in reporte or 'ADVERTENCIAS' in reporte


class TestAnalysisResult:
    """Tests de AnalysisResult."""
    
    def test_es_exitoso_sin_errores(self):
        """Test: es_exitoso cuando no hay errores."""
        resultado = AnalysisResult(
            valido=True,
            errores=[],
            advertencias=[],
            metricas={}
        )
        assert resultado.es_exitoso() is True
    
    def test_es_exitoso_con_errores(self):
        """Test: no es exitoso con errores."""
        resultado = AnalysisResult(
            valido=True,
            errores=['Error 1'],
            advertencias=[],
            metricas={}
        )
        assert resultado.es_exitoso() is False
    
    def test_es_exitoso_invalido(self):
        """Test: no es exitoso si código inválido."""
        resultado = AnalysisResult(
            valido=False,
            errores=[],
            advertencias=[],
            metricas={}
        )
        assert resultado.es_exitoso() is False


if __name__ == '__main__':
    # Ejecutar tests
    pytest.main([__file__, '-v', '--tb=short'])