"""
Calculadora Avanzada con SymPy.
FASE 3 - Semana 5

CAMBIOS v6 (diagnóstico 02/03/2026):
═══════════════════════════════════════════════════════════════════════

FIX C-02 — BUGS DE CÁLCULO BÁSICO
───────────────────────────────────
  Problemas detectados en diagnóstico:

  1. 100÷4 = '1004'  (concatenación de strings, no división)
     Causa: eval() recibía "100÷4" con el símbolo unicode ÷ y lo
     evaluaba como concatenación o lanzaba SyntaxError silencioso.
     Fix: normalizar_expresion() convierte ÷ → / antes de eval.

  2. √144 = '144'  (no calculaba raíz)
     Causa: "√144" o "raíz de 144" no llegaba a sqrt().
     Fix: normalizar_expresion() convierte √N → sqrt(N).

  3. 1000÷0 = '10000'  (sin manejo de división por cero)
     Causa: ZeroDivisionError no se capturaba correctamente.
     Fix: captura explícita de ZeroDivisionError con mensaje claro.

  4. "amor+3 = 3"  (operandos no numéricos no rechazados)
     Causa: SymPy acepta símbolos literales y devuelve expresiones
     simbólicas en vez de error.
     Fix: validar_operandos_numericos() verifica que el resultado
     sea un número real, no una expresión simbólica.

  Nuevo método: calcular_basico() para operaciones simples del tipo
  "cuánto es X + Y". Maneja texto natural (español e inglés) antes de
  pasarlo a SymPy.
═══════════════════════════════════════════════════════════════════════
"""

import re
import math
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


# ══════════════════════════════════════════════════════════════════════
# FIX C-02: Normalización y validación de expresiones
# ══════════════════════════════════════════════════════════════════════

def normalizar_expresion(texto: str) -> str:
    """
    FIX C-02: Convierte expresión en texto natural a forma evaluable.

    Conversiones aplicadas:
      ÷  →  /          (símbolo unicode división)
      ×  →  *          (símbolo unicode multiplicación)
      √N →  sqrt(N)    (símbolo raíz cuadrada)
      ^  →  **         (potencia en notación matemática común)
      "dividido entre" → /
      "dividido por"   → /
      "entre"          → /  (solo si entre números)
      "por"            → *  (solo si entre números)
      "elevado a"      → **
      "al cuadrado"    → **2
      "al cubo"        → **3
      "raíz de"        → sqrt(
      "raíz cuadrada de" → sqrt(
    """
    t = texto.strip()

    # ── Símbolos unicode ─────────────────────────────────────────────
    t = t.replace('÷', '/').replace('×', '*').replace('x', '*') \
         if re.fullmatch(r'[\d\s×x÷+\-*/().]+', t, re.IGNORECASE) else t
    t = t.replace('÷', '/')
    t = t.replace('×', '*')

    # ── Símbolo √ con número ─────────────────────────────────────────
    # √144 → sqrt(144)
    t = re.sub(r'√\s*(\d+(?:\.\d+)?)', r'sqrt(\1)', t)
    # √(expr) → sqrt(expr)
    t = re.sub(r'√\s*\(', 'sqrt(', t)

    # ── Potencia ─────────────────────────────────────────────────────
    t = t.replace('^', '**')
    t = re.sub(r'al\s+cuadrado', '**2', t, flags=re.IGNORECASE)
    t = re.sub(r'al\s+cubo', '**3', t, flags=re.IGNORECASE)
    t = re.sub(r'elevado\s+a\s+la?\s+(\w+)', r'**\1', t, flags=re.IGNORECASE)
    t = re.sub(r'elevado\s+a\s+(\d+)', r'**\1', t, flags=re.IGNORECASE)

    # ── Raíz cuadrada en texto ────────────────────────────────────────
    # "raíz cuadrada de 144" → "sqrt(144)"
    t = re.sub(
        r'ra[íi]z\s+cuadrada\s+de\s+(\d+(?:\.\d+)?)',
        r'sqrt(\1)', t, flags=re.IGNORECASE
    )
    # "raíz de 144" → "sqrt(144)"
    t = re.sub(
        r'ra[íi]z\s+de\s+(\d+(?:\.\d+)?)',
        r'sqrt(\1)', t, flags=re.IGNORECASE
    )

    # ── Operadores en español entre números ──────────────────────────
    # "100 dividido entre 4" → "100 / 4"
    t = re.sub(
        r'(\d+(?:\.\d+)?)\s+dividido\s+(?:entre|por)\s+(\d+(?:\.\d+)?)',
        r'\1 / \2', t, flags=re.IGNORECASE
    )
    # "100 entre 4"
    t = re.sub(
        r'(\d+(?:\.\d+)?)\s+entre\s+(\d+(?:\.\d+)?)',
        r'\1 / \2', t, flags=re.IGNORECASE
    )
    # "7 por 8"
    t = re.sub(
        r'(\d+(?:\.\d+)?)\s+por\s+(\d+(?:\.\d+)?)',
        r'\1 * \2', t, flags=re.IGNORECASE
    )
    # "7 multiplicado por 8"
    t = re.sub(
        r'(\d+(?:\.\d+)?)\s+multiplicado\s+por\s+(\d+(?:\.\d+)?)',
        r'\1 * \2', t, flags=re.IGNORECASE
    )
    # "7 más 8"
    t = re.sub(
        r'(\d+(?:\.\d+)?)\s+m[aá]s\s+(\d+(?:\.\d+)?)',
        r'\1 + \2', t, flags=re.IGNORECASE
    )
    # "7 menos 8"
    t = re.sub(
        r'(\d+(?:\.\d+)?)\s+menos\s+(\d+(?:\.\d+)?)',
        r'\1 - \2', t, flags=re.IGNORECASE
    )

    return t.strip()


def validar_operandos_numericos(resultado) -> bool:
    """
    FIX C-02: Verifica que el resultado sea un número real,
    no una expresión simbólica como 'amor + 3'.

    SymPy acepta variables libres y retorna expresiones simbólicas.
    Esta función detecta eso y retorna False para rechazarlo.
    """
    if resultado is None:
        return False
    try:
        # Intentar convertir a float
        float(resultado)
        return True
    except (TypeError, ValueError):
        pass
    try:
        # SymPy: verificar si tiene variables libres
        if hasattr(resultado, 'free_symbols') and resultado.free_symbols:
            return False  # Tiene variables → no es numérico puro
        # Intentar evaluar numéricamente
        val = float(resultado.evalf())
        return math.isfinite(val)
    except Exception:
        return False


class CalculadoraAvanzada:
    """
    Calculadora matemática avanzada usando SymPy.

    v6: agrega calcular_basico() para operaciones simples con
    texto natural, y aplica normalizar_expresion() en todos los
    métodos para manejar símbolos unicode y texto en español.
    """

    def __init__(self):
        self.x, self.y, self.z = symbols('x y z')
        self.n = symbols('n', integer=True)
        self.ultima_expresion = None

    # ══════════════════════════════════════════════════════════════════
    # FIX C-02: Método principal para cálculo básico
    # ══════════════════════════════════════════════════════════════════

    def calcular_basico(self, expresion: str) -> ResultadoMatematico:
        """
        FIX C-02: Calcula operaciones básicas con texto natural.

        Maneja los 4 bugs del diagnóstico:
          1. 100÷4      → 25.0   (no concatenación)
          2. √144        → 12.0   (no devuelve 144)
          3. 1000÷0      → error honesto
          4. amor+3      → error honesto (no numérico)

        Flujo:
          1. Normalizar expresión (símbolos unicode, texto español)
          2. Evaluar con SymPy
          3. Verificar que resultado es numérico (no simbólico)
          4. Manejar división por cero explícitamente
        """
        pasos = []
        pasos.append(f"Expresión original: {expresion}")

        # Paso 1: Normalizar
        expr_normalizada = normalizar_expresion(expresion)
        if expr_normalizada != expresion:
            pasos.append(f"Normalizada: {expr_normalizada}")

        try:
            # Paso 2: Parsear con SymPy
            expr_sympy = parse_expr(
                expr_normalizada,
                local_dict={
                    'sqrt': sp.sqrt,
                    'pi': sp.pi,
                    'e': sp.E,
                },
                evaluate=True,
            )
            pasos.append(f"Expresión SymPy: {expr_sympy}")

            # Paso 3: Verificar que es numérico (FIX operandos no numéricos)
            if not validar_operandos_numericos(expr_sympy):
                return ResultadoMatematico(
                    expresion_original=expresion,
                    resultado="",
                    paso_a_paso=pasos,
                    exitoso=False,
                    error=(
                        f"La expresión contiene variables no numéricas. "
                        f"Solo puedo calcular operaciones con números."
                    )
                )

            # Paso 4: Evaluar numéricamente
            resultado_num = expr_sympy.evalf()

            # Si es entero exacto, mostrar sin decimales
            try:
                resultado_int = int(resultado_num)
                if abs(float(resultado_num) - resultado_int) < 1e-10:
                    resultado_str = str(resultado_int)
                else:
                    # Redondear a 10 decimales significativos
                    resultado_str = f"{float(resultado_num):.10g}"
            except (ValueError, OverflowError):
                resultado_str = str(resultado_num)

            pasos.append(f"Resultado: {resultado_str}")

            return ResultadoMatematico(
                expresion_original=expresion,
                resultado=resultado_str,
                paso_a_paso=pasos,
                exitoso=True
            )

        except ZeroDivisionError:
            # FIX C-02: división por cero honesta
            return ResultadoMatematico(
                expresion_original=expresion,
                resultado="",
                paso_a_paso=pasos,
                exitoso=False,
                error="División por cero: esa operación no está definida matemáticamente."
            )
        except sp.core.numbers.ComplexNumber:
            return ResultadoMatematico(
                expresion_original=expresion,
                resultado="",
                paso_a_paso=pasos,
                exitoso=False,
                error="El resultado es un número complejo (no real)."
            )
        except (SyntaxError, TypeError, ValueError) as e:
            return ResultadoMatematico(
                expresion_original=expresion,
                resultado="",
                paso_a_paso=pasos,
                exitoso=False,
                error=f"No pude interpretar la expresión: {e}"
            )
        except Exception as e:
            # Verificar si es zoo (infinito complejo de SymPy = div/0)
            err_str = str(e).lower()
            if 'zoo' in err_str or 'division' in err_str or 'zero' in err_str:
                return ResultadoMatematico(
                    expresion_original=expresion,
                    resultado="",
                    paso_a_paso=pasos,
                    exitoso=False,
                    error="División por cero: esa operación no está definida matemáticamente."
                )
            return ResultadoMatematico(
                expresion_original=expresion,
                resultado="",
                paso_a_paso=pasos,
                exitoso=False,
                error=f"Error al calcular: {e}"
            )

    # ══════════════════════════════════════════════════════════════════
    # Métodos avanzados — sin cambios de lógica, con normalización
    # ══════════════════════════════════════════════════════════════════

    def derivar(
        self,
        expresion: str,
        variable: str = 'x',
        orden: int = 1
    ) -> ResultadoMatematico:
        """Calcula la derivada de una expresión."""
        pasos = []
        try:
            expr = parse_expr(normalizar_expresion(expresion))
            pasos.append(f"Expresión: {expr}")
            self.ultima_expresion = expr
            var = symbols(variable)
            derivada = diff(expr, var, orden)
            pasos.append(f"Derivada de orden {orden}: {derivada}")
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
        """Calcula la integral de una expresión."""
        pasos = []
        try:
            expr = parse_expr(normalizar_expresion(expresion))
            pasos.append(f"Expresión: {expr}")
            self.ultima_expresion = expr
            var = symbols(variable)
            if limite_inferior is not None and limite_superior is not None:
                pasos.append(f"Integral definida de {limite_inferior} a {limite_superior}")
                integral = integrate(expr, (var, limite_inferior, limite_superior))
                resultado = integral
            else:
                pasos.append("Integral indefinida")
                integral = integrate(expr, var)
                pasos.append(f"Resultado: {integral} + C")
                resultado = integral
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
        """Resuelve una ecuación algebraica."""
        pasos = []
        try:
            if "=" in ecuacion:
                izq, der = ecuacion.split("=")
                expr = parse_expr(normalizar_expresion(izq)) \
                     - parse_expr(normalizar_expresion(der))
            else:
                expr = parse_expr(normalizar_expresion(ecuacion))
            pasos.append(f"Ecuación: {expr} = 0")
            self.ultima_expresion = expr
            var = symbols(variable)
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
        """Simplifica una expresión matemática."""
        pasos = []
        try:
            expr = parse_expr(normalizar_expresion(expresion))
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
        """Expande una expresión matemática."""
        pasos = []
        try:
            expr = parse_expr(normalizar_expresion(expresion))
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
        """Factoriza una expresión matemática."""
        pasos = []
        try:
            expr = parse_expr(normalizar_expresion(expresion))
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
        """Calcula el límite de una expresión."""
        pasos = []
        try:
            expr = parse_expr(normalizar_expresion(expresion))
            pasos.append(f"Expresión: {expr}")
            self.ultima_expresion = expr
            var = symbols(variable)
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
        """Calcula la serie de Taylor de una expresión."""
        pasos = []
        try:
            expr = parse_expr(normalizar_expresion(expresion))
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
        """Evalúa una expresión con valores específicos."""
        pasos = []
        try:
            expr = parse_expr(normalizar_expresion(expresion))
            pasos.append(f"Expresión: {expr}")
            pasos.append(f"Valores: {valores}")
            self.ultima_expresion = expr
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


# ══════════════════════════════════════════════════════════════════════
# Test de fixes C-02
# ══════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    calc = CalculadoraAvanzada()

    print("=== TEST FIX C-02 ===\n")

    casos = [
        # (descripción, expresión, resultado_esperado, debe_exitoso)
        ("División unicode",     "100÷4",       "25",    True),
        ("Raíz cuadrada √",      "√144",        "12",    True),
        ("División por cero",    "1000÷0",      "",      False),
        ("Operandos no numéricos","amor+3",      "",      False),
        ("Multiplicación ×",     "7×8",         "56",    True),
        ("División texto",       "100 dividido entre 4", "25", True),
        ("Raíz texto",           "raíz de 144",  "12",   True),
        ("Suma básica",          "15+27",        "42",   True),
        ("Potencia ^",           "2^10",         "1024", True),
        ("Pi",                   "3.14*2",       "6.28", True),
    ]

    ok = 0
    fail = 0
    for desc, expr, esperado, debe_exitoso in casos:
        r = calc.calcular_basico(expr)
        exito_ok = r.exitoso == debe_exitoso
        resultado_ok = (not debe_exitoso) or (r.resultado == esperado)
        status = "✅" if (exito_ok and resultado_ok) else "❌"
        if exito_ok and resultado_ok:
            ok += 1
        else:
            fail += 1
        print(f"{status} {desc}: '{expr}' → '{r.resultado}' (error: {r.error})")

    print(f"\n{ok}/{ok+fail} tests pasaron")

    print("\n=== CALCULADORA AVANZADA ===\n")

    resultado = calc.derivar("x**2 + 3*x + 2")
    print(f"Derivada de {resultado.expresion_original}: {resultado.resultado}")

    resultado = calc.integrar("x**2", limite_inferior=0, limite_superior=1)
    print(f"Integral x**2 de 0 a 1: {resultado.resultado}")

    resultado = calc.resolver_ecuacion("x**2 - 4")
    print(f"Resolver x**2-4=0: {resultado.resultado}")