"""
Calculadora Avanzada con SymPy.
FASE 3 - Semana 5
"""

import sympy as sp
from sympy import symbols, sympify, diff, integrate, solve, simplify, expand, factor
from sympy import sin, cos, tan, exp, log, sqrt, pi, E
from sympy.parsing.sympy_parser import parse_expr
from typing import List, Dict, Union, Optional
from dataclasses import dataclass


@dataclass
class ResultadoMatematico:
    """Resultado de una operación matemática."""
    expresion_original: str
    resultado: str
    paso_a_paso: List[str]
    exitoso: bool
    error: Optional[str] = None


class CalculadoraAvanzada:
    """
    Calculadora matemática avanzada usando SymPy.
    
    Capacidades:
    - Derivadas simbólicas
    - Integrales (definidas e indefinidas)
    - Resolver ecuaciones
    - Simplificar expresiones
    - Expandir y factorizar
    - Límites
    - Series de Taylor
    - Álgebra matricial
    """
    
    def __init__(self):
        """Inicializa la calculadora."""
        self.x, self.y, self.z = symbols('x y z')
        self.n = symbols('n', integer=True)
        self.ultima_expresion = None
    
    def derivar(
        self, 
        expresion: str, 
        variable: str = 'x',
        orden: int = 1
    ) -> ResultadoMatematico:
        """
        Calcula la derivada de una expresión.
        
        Args:
            expresion: Expresión matemática como string
            variable: Variable respecto a la cual derivar
            orden: Orden de la derivada (1 = primera, 2 = segunda, etc.)
            
        Returns:
            ResultadoMatematico con la derivada
            
        Examples:
            >>> calc.derivar("x**2 + 3*x + 2")
            "2*x + 3"
            
            >>> calc.derivar("sin(x)", orden=2)
            "-sin(x)"
        """
        pasos = []
        
        try:
            # Parsear expresión
            expr = parse_expr(expresion)
            pasos.append(f"Expresión: {expr}")
            self.ultima_expresion = expr
            
            # Obtener símbolo de la variable
            var = symbols(variable)
            
            # Derivar
            derivada = diff(expr, var, orden)
            pasos.append(f"Derivada de orden {orden}: {derivada}")
            
            # Simplificar
            resultado = simplify(derivada)
            pasos.append(f"Simplificado: {resultado}")
            
            return ResultadoMatematico(
                expresion_original=expresion,
                resultado=str(resultado),
                paso_a_paso=pasos,
                exitoso=True
            )
            
        except Exception as e:
            return ResultadoMatematico(
                expresion_original=expresion,
                resultado="",
                paso_a_paso=pasos,
                exitoso=False,
                error=str(e)
            )
    
    def integrar(
        self,
        expresion: str,
        variable: str = 'x',
        limite_inferior: Optional[float] = None,
        limite_superior: Optional[float] = None
    ) -> ResultadoMatematico:
        """
        Calcula la integral de una expresión.
        
        Args:
            expresion: Expresión matemática
            variable: Variable de integración
            limite_inferior: Límite inferior (None = indefinida)
            limite_superior: Límite superior (None = indefinida)
            
        Returns:
            ResultadoMatematico con la integral
            
        Examples:
            >>> calc.integrar("x**2")
            "x**3/3"
            
            >>> calc.integrar("x**2", limite_inferior=0, limite_superior=1)
            "1/3"
        """
        pasos = []
        
        try:
            # Parsear expresión
            expr = parse_expr(expresion)
            pasos.append(f"Expresión: {expr}")
            self.ultima_expresion = expr
            
            # Obtener símbolo de la variable
            var = symbols(variable)
            
            # Integral definida o indefinida
            if limite_inferior is not None and limite_superior is not None:
                pasos.append(f"Integral definida de {limite_inferior} a {limite_superior}")
                integral = integrate(expr, (var, limite_inferior, limite_superior))
                pasos.append(f"Resultado: {integral}")
                resultado = integral
            else:
                pasos.append("Integral indefinida")
                integral = integrate(expr, var)
                pasos.append(f"Resultado: {integral} + C")
                resultado = integral
            
            # Simplificar
            resultado_final = simplify(resultado)
            
            return ResultadoMatematico(
                expresion_original=expresion,
                resultado=str(resultado_final),
                paso_a_paso=pasos,
                exitoso=True
            )
            
        except Exception as e:
            return ResultadoMatematico(
                expresion_original=expresion,
                resultado="",
                paso_a_paso=pasos,
                exitoso=False,
                error=str(e)
            )
    
    def resolver_ecuacion(
        self,
        ecuacion: str,
        variable: str = 'x'
    ) -> ResultadoMatematico:
        """
        Resuelve una ecuación algebraica.
        
        Args:
            ecuacion: Ecuación a resolver (ej: "x**2 - 4 = 0")
            variable: Variable a resolver
            
        Returns:
            ResultadoMatematico con las soluciones
            
        Examples:
            >>> calc.resolver_ecuacion("x**2 - 4")
            "[-2, 2]"
            
            >>> calc.resolver_ecuacion("2*x + 3 = 7")
            "[2]"
        """
        pasos = []
        
        try:
            # Si tiene "=", separar
            if "=" in ecuacion:
                izq, der = ecuacion.split("=")
                expr = parse_expr(izq) - parse_expr(der)
            else:
                expr = parse_expr(ecuacion)
            
            pasos.append(f"Ecuación: {expr} = 0")
            self.ultima_expresion = expr
            
            # Obtener símbolo de la variable
            var = symbols(variable)
            
            # Resolver
            soluciones = solve(expr, var)
            pasos.append(f"Soluciones: {soluciones}")
            
            return ResultadoMatematico(
                expresion_original=ecuacion,
                resultado=str(soluciones),
                paso_a_paso=pasos,
                exitoso=True
            )
            
        except Exception as e:
            return ResultadoMatematico(
                expresion_original=ecuacion,
                resultado="",
                paso_a_paso=pasos,
                exitoso=False,
                error=str(e)
            )
    
    def simplificar(self, expresion: str) -> ResultadoMatematico:
        """
        Simplifica una expresión matemática.
        
        Args:
            expresion: Expresión a simplificar
            
        Returns:
            ResultadoMatematico con la expresión simplificada
        """
        pasos = []
        
        try:
            expr = parse_expr(expresion)
            pasos.append(f"Original: {expr}")
            self.ultima_expresion = expr
            
            resultado = simplify(expr)
            pasos.append(f"Simplificado: {resultado}")
            
            return ResultadoMatematico(
                expresion_original=expresion,
                resultado=str(resultado),
                paso_a_paso=pasos,
                exitoso=True
            )
            
        except Exception as e:
            return ResultadoMatematico(
                expresion_original=expresion,
                resultado="",
                paso_a_paso=pasos,
                exitoso=False,
                error=str(e)
            )
    
    def expandir(self, expresion: str) -> ResultadoMatematico:
        """
        Expande una expresión matemática.
        
        Args:
            expresion: Expresión a expandir
            
        Returns:
            ResultadoMatematico con la expresión expandida
            
        Examples:
            >>> calc.expandir("(x + 1)**2")
            "x**2 + 2*x + 1"
        """
        pasos = []
        
        try:
            expr = parse_expr(expresion)
            pasos.append(f"Original: {expr}")
            self.ultima_expresion = expr
            
            resultado = expand(expr)
            pasos.append(f"Expandido: {resultado}")
            
            return ResultadoMatematico(
                expresion_original=expresion,
                resultado=str(resultado),
                paso_a_paso=pasos,
                exitoso=True
            )
            
        except Exception as e:
            return ResultadoMatematico(
                expresion_original=expresion,
                resultado="",
                paso_a_paso=pasos,
                exitoso=False,
                error=str(e)
            )
    
    def factorizar(self, expresion: str) -> ResultadoMatematico:
        """
        Factoriza una expresión matemática.
        
        Args:
            expresion: Expresión a factorizar
            
        Returns:
            ResultadoMatematico con la expresión factorizada
            
        Examples:
            >>> calc.factorizar("x**2 - 4")
            "(x - 2)*(x + 2)"
        """
        pasos = []
        
        try:
            expr = parse_expr(expresion)
            pasos.append(f"Original: {expr}")
            self.ultima_expresion = expr
            
            resultado = factor(expr)
            pasos.append(f"Factorizado: {resultado}")
            
            return ResultadoMatematico(
                expresion_original=expresion,
                resultado=str(resultado),
                paso_a_paso=pasos,
                exitoso=True
            )
            
        except Exception as e:
            return ResultadoMatematico(
                expresion_original=expresion,
                resultado="",
                paso_a_paso=pasos,
                exitoso=False,
                error=str(e)
            )
    
    def limite(
        self,
        expresion: str,
        variable: str = 'x',
        punto: Union[float, str] = 0
    ) -> ResultadoMatematico:
        """
        Calcula el límite de una expresión.
        
        Args:
            expresion: Expresión matemática
            variable: Variable
            punto: Punto al que tiende (puede ser 'oo' para infinito)
            
        Returns:
            ResultadoMatematico con el límite
        """
        pasos = []
        
        try:
            expr = parse_expr(expresion)
            pasos.append(f"Expresión: {expr}")
            self.ultima_expresion = expr
            
            var = symbols(variable)
            
            # Convertir 'oo' a infinito
            if punto == 'oo' or punto == 'inf':
                punto_eval = sp.oo
            else:
                punto_eval = punto
            
            pasos.append(f"Límite cuando {variable} → {punto}")
            
            resultado = sp.limit(expr, var, punto_eval)
            pasos.append(f"Resultado: {resultado}")
            
            return ResultadoMatematico(
                expresion_original=expresion,
                resultado=str(resultado),
                paso_a_paso=pasos,
                exitoso=True
            )
            
        except Exception as e:
            return ResultadoMatematico(
                expresion_original=expresion,
                resultado="",
                paso_a_paso=pasos,
                exitoso=False,
                error=str(e)
            )
    
    def serie_taylor(
        self,
        expresion: str,
        variable: str = 'x',
        punto: float = 0,
        orden: int = 5
    ) -> ResultadoMatematico:
        """
        Calcula la serie de Taylor de una expresión.
        
        Args:
            expresion: Expresión matemática
            variable: Variable
            punto: Punto alrededor del cual expandir
            orden: Orden de la serie
            
        Returns:
            ResultadoMatematico con la serie de Taylor
        """
        pasos = []
        
        try:
            expr = parse_expr(expresion)
            pasos.append(f"Expresión: {expr}")
            self.ultima_expresion = expr
            
            var = symbols(variable)
            
            pasos.append(f"Serie de Taylor alrededor de {punto}, orden {orden}")
            
            serie = expr.series(var, punto, orden).removeO()
            pasos.append(f"Serie: {serie}")
            
            return ResultadoMatematico(
                expresion_original=expresion,
                resultado=str(serie),
                paso_a_paso=pasos,
                exitoso=True
            )
            
        except Exception as e:
            return ResultadoMatematico(
                expresion_original=expresion,
                resultado="",
                paso_a_paso=pasos,
                exitoso=False,
                error=str(e)
            )
    
    def evaluar(
        self,
        expresion: str,
        valores: Dict[str, float]
    ) -> ResultadoMatematico:
        """
        Evalúa una expresión con valores específicos.
        
        Args:
            expresion: Expresión matemática
            valores: Diccionario de valores {variable: valor}
            
        Returns:
            ResultadoMatematico con el valor numérico
            
        Examples:
            >>> calc.evaluar("x**2 + y", {"x": 2, "y": 3})
            "7"
        """
        pasos = []
        
        try:
            expr = parse_expr(expresion)
            pasos.append(f"Expresión: {expr}")
            pasos.append(f"Valores: {valores}")
            self.ultima_expresion = expr
            
            # Convertir valores a símbolos
            subs_dict = {symbols(k): v for k, v in valores.items()}
            
            resultado = expr.subs(subs_dict)
            pasos.append(f"Resultado: {resultado}")
            
            return ResultadoMatematico(
                expresion_original=expresion,
                resultado=str(resultado),
                paso_a_paso=pasos,
                exitoso=True
            )
            
        except Exception as e:
            return ResultadoMatematico(
                expresion_original=expresion,
                resultado="",
                paso_a_paso=pasos,
                exitoso=False,
                error=str(e)
            )


# Ejemplo de uso
if __name__ == '__main__':
    calc = CalculadoraAvanzada()
    
    print("=== CALCULADORA AVANZADA ===\n")
    
    # Derivada
    resultado = calc.derivar("x**2 + 3*x + 2")
    print(f"Derivada de {resultado.expresion_original}:")
    print(f"  → {resultado.resultado}\n")
    
    # Integral
    resultado = calc.integrar("x**2", limite_inferior=0, limite_superior=1)
    print(f"Integral de x**2 de 0 a 1:")
    print(f"  → {resultado.resultado}\n")
    
    # Resolver ecuación
    resultado = calc.resolver_ecuacion("x**2 - 4")
    print(f"Resolver x**2 - 4 = 0:")
    print(f"  → {resultado.resultado}\n")