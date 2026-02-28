"""
Tests para CalculadoraAvanzada.
FASE 3 - Tests de matemáticas avanzadas.
"""

import pytest
from pathlib import Path
import sys

# Importar la calculadora
proyecto_path = Path(__file__).parent.parent
sys.path.insert(0, str(proyecto_path))

from matematicas.calculadora_avanzada import CalculadoraAvanzada, ResultadoMatematico


class TestCalculadoraDerivadas:
    """Tests de derivadas."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.calc = CalculadoraAvanzada()
    
    def test_derivada_simple(self):
        """Test: derivada de x**2."""
        resultado = self.calc.derivar("x**2")
        
        assert resultado.exitoso is True
        assert "2*x" in resultado.resultado
    
    def test_derivada_polinomio(self):
        """Test: derivada de polinomio."""
        resultado = self.calc.derivar("x**3 + 2*x**2 + 3*x + 4")
        
        assert resultado.exitoso is True
        # Debería contener 3*x**2 + 4*x + 3
        assert resultado.exitoso
    
    def test_derivada_trigonometrica(self):
        """Test: derivada de sin(x)."""
        resultado = self.calc.derivar("sin(x)")
        
        assert resultado.exitoso is True
        assert "cos(x)" in resultado.resultado
    
    def test_derivada_segunda(self):
        """Test: segunda derivada."""
        resultado = self.calc.derivar("x**3", orden=2)
        
        assert resultado.exitoso is True
        assert "6*x" in resultado.resultado
    
    def test_derivada_variable_diferente(self):
        """Test: derivar respecto a y."""
        resultado = self.calc.derivar("y**2 + 3*y", variable='y')
        
        assert resultado.exitoso is True
        assert "y" in resultado.resultado


class TestCalculadoraIntegrales:
    """Tests de integrales."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.calc = CalculadoraAvanzada()
    
    def test_integral_simple(self):
        """Test: integral de x."""
        resultado = self.calc.integrar("x")
        
        assert resultado.exitoso is True
        assert "x**2" in resultado.resultado
    
    def test_integral_polinomio(self):
        """Test: integral de x**2."""
        resultado = self.calc.integrar("x**2")
        
        assert resultado.exitoso is True
        assert "x**3" in resultado.resultado
    
    def test_integral_definida(self):
        """Test: integral definida de x**2 de 0 a 1."""
        resultado = self.calc.integrar("x**2", limite_inferior=0, limite_superior=1)
        
        assert resultado.exitoso is True
        # El resultado debería ser 1/3
        assert "1/3" in resultado.resultado or "0.333" in resultado.resultado
    
    def test_integral_trigonometrica(self):
        """Test: integral de cos(x)."""
        resultado = self.calc.integrar("cos(x)")
        
        assert resultado.exitoso is True
        assert "sin(x)" in resultado.resultado


class TestCalculadoraEcuaciones:
    """Tests de resolver ecuaciones."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.calc = CalculadoraAvanzada()
    
    def test_resolver_lineal(self):
        """Test: resolver 2*x + 3 = 7."""
        resultado = self.calc.resolver_ecuacion("2*x + 3 = 7")
        
        assert resultado.exitoso is True
        assert "2" in resultado.resultado
    
    def test_resolver_cuadratica(self):
        """Test: resolver x**2 - 4."""
        resultado = self.calc.resolver_ecuacion("x**2 - 4")
        
        assert resultado.exitoso is True
        # Soluciones: -2, 2
        assert "-2" in resultado.resultado
        assert "2" in resultado.resultado
    
    def test_resolver_sin_solucion_real(self):
        """Test: x**2 + 1 = 0 tiene soluciones complejas."""
        resultado = self.calc.resolver_ecuacion("x**2 + 1")
        
        assert resultado.exitoso is True
        # Debería tener I (imaginario)
        assert "I" in resultado.resultado or "i" in resultado.resultado.lower()


class TestCalculadoraSimplificacion:
    """Tests de simplificación."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.calc = CalculadoraAvanzada()
    
    def test_simplificar_basico(self):
        """Test: simplificar x + x."""
        resultado = self.calc.simplificar("x + x")
        
        assert resultado.exitoso is True
        assert "2*x" in resultado.resultado
    
    def test_simplificar_trigonometrico(self):
        """Test: simplificar sin(x)**2 + cos(x)**2."""
        resultado = self.calc.simplificar("sin(x)**2 + cos(x)**2")
        
        assert resultado.exitoso is True
        # Debería dar 1
        assert "1" in resultado.resultado


class TestCalculadoraExpansion:
    """Tests de expansión."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.calc = CalculadoraAvanzada()
    
    def test_expandir_cuadrado(self):
        """Test: expandir (x + 1)**2."""
        resultado = self.calc.expandir("(x + 1)**2")
        
        assert resultado.exitoso is True
        # Debería ser x**2 + 2*x + 1
        assert "x**2" in resultado.resultado
        assert "2*x" in resultado.resultado
        assert "1" in resultado.resultado
    
    def test_expandir_producto(self):
        """Test: expandir (x + 2)*(x + 3)."""
        resultado = self.calc.expandir("(x + 2)*(x + 3)")
        
        assert resultado.exitoso is True
        assert "x**2" in resultado.resultado


class TestCalculadoraFactorizacion:
    """Tests de factorización."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.calc = CalculadoraAvanzada()
    
    def test_factorizar_diferencia_cuadrados(self):
        """Test: factorizar x**2 - 4."""
        resultado = self.calc.factorizar("x**2 - 4")
        
        assert resultado.exitoso is True
        # Debería ser (x - 2)*(x + 2)
        assert "x - 2" in resultado.resultado or "x + 2" in resultado.resultado
    
    def test_factorizar_simple(self):
        """Test: factorizar x**2 + 2*x."""
        resultado = self.calc.factorizar("x**2 + 2*x")
        
        assert resultado.exitoso is True
        # Debería tener x como factor
        assert "x" in resultado.resultado


class TestCalculadoraLimites:
    """Tests de límites."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.calc = CalculadoraAvanzada()
    
    def test_limite_simple(self):
        """Test: límite de x cuando x->0."""
        resultado = self.calc.limite("x", punto=0)
        
        assert resultado.exitoso is True
        assert "0" in resultado.resultado
    
    def test_limite_infinito(self):
        """Test: límite de 1/x cuando x->oo."""
        resultado = self.calc.limite("1/x", punto='oo')
        
        assert resultado.exitoso is True
        assert "0" in resultado.resultado
    
    def test_limite_indeterminado(self):
        """Test: límite de (x**2 - 1)/(x - 1) cuando x->1."""
        resultado = self.calc.limite("(x**2 - 1)/(x - 1)", punto=1)
        
        assert resultado.exitoso is True
        # Debería dar 2
        assert "2" in resultado.resultado


class TestCalculadoraSerieTaylor:
    """Tests de serie de Taylor."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.calc = CalculadoraAvanzada()
    
    def test_serie_taylor_exp(self):
        """Test: serie de Taylor de exp(x)."""
        resultado = self.calc.serie_taylor("exp(x)", orden=4)
        
        assert resultado.exitoso is True
        # Debería contener 1 + x + x**2/2 + x**3/6
        assert "x" in resultado.resultado
    
    def test_serie_taylor_sin(self):
        """Test: serie de Taylor de sin(x)."""
        resultado = self.calc.serie_taylor("sin(x)", orden=4)
        
        assert resultado.exitoso is True
        assert "x" in resultado.resultado


class TestCalculadoraEvaluacion:
    """Tests de evaluación."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.calc = CalculadoraAvanzada()
    
    def test_evaluar_simple(self):
        """Test: evaluar x**2 con x=2."""
        resultado = self.calc.evaluar("x**2", {"x": 2})
        
        assert resultado.exitoso is True
        assert "4" in resultado.resultado
    
    def test_evaluar_multiples_variables(self):
        """Test: evaluar x + y con x=2, y=3."""
        resultado = self.calc.evaluar("x + y", {"x": 2, "y": 3})
        
        assert resultado.exitoso is True
        assert "5" in resultado.resultado
    
    def test_evaluar_trigonometrica(self):
        """Test: evaluar sin(0)."""
        resultado = self.calc.evaluar("sin(x)", {"x": 0})
        
        assert resultado.exitoso is True
        assert "0" in resultado.resultado


class TestResultadoMatematico:
    """Tests de ResultadoMatematico."""
    
    def test_crear_resultado_exitoso(self):
        """Test: crear resultado exitoso."""
        resultado = ResultadoMatematico(
            expresion_original="x**2",
            resultado="2*x",
            paso_a_paso=["paso 1", "paso 2"],
            exitoso=True
        )
        
        assert resultado.exitoso is True
        assert resultado.error is None
    
    def test_crear_resultado_con_error(self):
        """Test: crear resultado con error."""
        resultado = ResultadoMatematico(
            expresion_original="invalido",
            resultado="",
            paso_a_paso=[],
            exitoso=False,
            error="Syntax Error"
        )
        
        assert resultado.exitoso is False
        assert resultado.error == "Syntax Error"


class TestCalculadoraExpresionesComplejas:
    """Tests de expresiones complejas."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.calc = CalculadoraAvanzada()
    
    def test_derivada_producto(self):
        """Test: derivada de x*sin(x)."""
        resultado = self.calc.derivar("x*sin(x)")
        
        assert resultado.exitoso is True
        # d/dx[x*sin(x)] = sin(x) + x*cos(x)
        assert "sin" in resultado.resultado and "cos" in resultado.resultado
    
    def test_integral_compuesta(self):
        """Test: integral de x*exp(x)."""
        resultado = self.calc.integrar("x*exp(x)")
        
        assert resultado.exitoso is True
        assert "exp" in resultado.resultado
    
    def test_simplificar_complejo(self):
        """Test: simplificar (x**2 - 1)/(x - 1)."""
        resultado = self.calc.simplificar("(x**2 - 1)/(x - 1)")
        
        assert resultado.exitoso is True
        # Debería simplificar a x + 1
        assert "x" in resultado.resultado


if __name__ == '__main__':
    # Ejecutar tests
    pytest.main([__file__, '-v', '--tb=short'])