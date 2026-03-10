# -*- coding: utf-8 -*-
"""
calculadora_avanzada.py — VERSION v8.0

CAMBIOS v8.0 sobre v7.1:
═══════════════════════════════════════════════════════════════════════
BUG-03 FIX  resolver_sistema() ahora valida que ecuaciones sea List[str].
            Si recibe un str, lo envuelve automáticamente.
            Si recibe cualquier otro tipo, retorna error descriptivo.
            NUNCA hace crash.

NUEVO-C16   resolver_sistema() soporta variables automáticas (detecta
            cuántas variables hay en las ecuaciones y las asigna).

NUEVO-C17   estadisticas() — calcula media, mediana, moda, varianza,
            desviación estándar, mínimo, máximo, rango, percentiles.
            Acepta lista como string "4, 7, 2, 9, 1" o lista real.

NUEVO-C18   derivada_parcial() expuesta correctamente con método propio
            y soporte completo de orden y múltiples variables.

NUEVO-C19   evaluar_multivariable() — evalúa f(x,y,z,...) con dict
            de valores. Mejora sobre evaluar() existente.

NUEVO-C20   es_primo(), mcd(), mcm(), combinaciones(), permutaciones()
            — operaciones de aritmética discreta básica.

NUEVO-C21   Detección automática de tipo de operación por texto libre
            en calcular_automatico() — entrada única que detecta QUÉ
            hacer sin que el motor tenga que especificar sub_tipo.

NUEVO-C22   Soporte de estadística descriptiva completa con NumPy
            (fallback a implementación pura si NumPy no disponible).

NUEVO-C23   resolver_inecuacion() — resuelve inecuaciones simbólicas.

NUEVO-C24   polinomio_info() — factores, raíces, grado, coeficientes.

Todos los fixes v7.1 preservados intactos (FIX-C1 a FIX-C7,
NUEVO-C1 a NUEVO-C15).
═══════════════════════════════════════════════════════════════════════
"""

import re
import math
import unicodedata
import logging
from typing import List, Dict, Union, Optional, Tuple, Any
from dataclasses import dataclass, field

import sympy as sp
from sympy import (
    symbols, diff, integrate, solve, solve_linear_system,
    simplify, expand, factor, trigsimp, cancel, radsimp,
    nsimplify, sin, cos, tan, exp, log, sqrt, pi, E, oo, zoo,
    Matrix, linsolve, nonlinsolve, Eq, Rational, Integer, Float,
    Poly, degree, LC, gcd as sp_gcd, lcm as sp_lcm,
    solveset, S, Interval, And, Or,
)
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations,
    implicit_multiplication_application,
)

logger = logging.getLogger("calculadora_avanzada")

# ─────────────────────────────────────────────────────────────────────
# TRANSFORMACIONES SYMPY
# ─────────────────────────────────────────────────────────────────────

_TRANSFORMACIONES = standard_transformations + (implicit_multiplication_application,)

_LOCAL_DICT = {
    'sqrt': sp.sqrt, 'pi': sp.pi, 'e': sp.E,
    'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan,
    'asin': sp.asin, 'acos': sp.acos, 'atan': sp.atan,
    'sinh': sp.sinh, 'cosh': sp.cosh, 'tanh': sp.tanh,
    'exp': sp.exp, 'log': sp.log, 'ln': sp.log,
    'abs': sp.Abs, 'ceil': sp.ceiling, 'floor': sp.floor,
    'oo': sp.oo, 'inf': sp.oo,
    'factorial': sp.factorial,
    'cbrt': lambda x: x**sp.Rational(1, 3),
    'sec': lambda x: 1/sp.cos(x),
    'csc': lambda x: 1/sp.sin(x),
    'cot': lambda x: sp.cos(x)/sp.sin(x),
}

# ═══════════════════════════════════════════════════════════════════════
# DATACLASS DE RESULTADO
# ═══════════════════════════════════════════════════════════════════════

@dataclass
class ResultadoMatematico:
    """Resultado de una operación matemática."""
    expresion_original: str
    resultado: str
    paso_a_paso: List[str] = field(default_factory=list)
    exitoso: bool = True
    error: Optional[str] = None
    tipo: str = "GENERAL"
    latex: Optional[str] = None
    valor_numerico: Optional[float] = None


# ═══════════════════════════════════════════════════════════════════════
# NUEVO-C4: NÚMEROS EN ESPAÑOL
# ═══════════════════════════════════════════════════════════════════════

_NUMEROS_ES = {
    'cero': '0', 'un': '1', 'uno': '1', 'una': '1', 'dos': '2',
    'tres': '3', 'cuatro': '4', 'cinco': '5', 'seis': '6', 'siete': '7',
    'ocho': '8', 'nueve': '9', 'diez': '10', 'once': '11', 'doce': '12',
    'trece': '13', 'catorce': '14', 'quince': '15', 'veinte': '20',
    'treinta': '30', 'cuarenta': '40', 'cincuenta': '50', 'sesenta': '60',
    'setenta': '70', 'ochenta': '80', 'noventa': '90', 'cien': '100',
    'ciento': '100', 'mil': '1000', 'millon': '1000000',
}

_FRACCIONES_ES = {
    r'la\s+mitad\s+de\s+(.+?)(?:\s*$)':       r'\1 / 2',
    r'un\s+tercio\s+de\s+(.+?)(?:\s*$)':       r'\1 / 3',
    r'un\s+cuarto\s+de\s+(.+?)(?:\s*$)':       r'\1 / 4',
    r'tres\s+cuartos\s+de\s+(.+?)(?:\s*$)':    r'\1 * 3 / 4',
    r'un\s+quinto\s+de\s+(.+?)(?:\s*$)':       r'\1 / 5',
    r'dos\s+tercios\s+de\s+(.+?)(?:\s*$)':     r'\1 * 2 / 3',
}

def _convertir_numeros_espanol(texto: str) -> str:
    """Convierte números escritos en español a dígitos."""
    t = texto
    for patron, reemplazo in _FRACCIONES_ES.items():
        t = re.sub(patron, reemplazo, t, flags=re.IGNORECASE)
    for palabra, digito in sorted(_NUMEROS_ES.items(), key=lambda x: -len(x[0])):
        t = re.sub(r'\b' + palabra + r'\b', digito, t, flags=re.IGNORECASE)
    return t


# ═══════════════════════════════════════════════════════════════════════
# NUEVO-C10: PORCENTAJES DIRECTOS
# ═══════════════════════════════════════════════════════════════════════

_RE_PORCENTAJE_DE    = re.compile(r'(?:el\s+|cuanto\s+es\s+(?:el\s+)?)?((?:\d+(?:\.\d+)?))\s*%\s+de\s+((?:\d+(?:\.\d+)?))', re.IGNORECASE)
_RE_MAS_PORCENTAJE   = re.compile(r'((?:\d+(?:\.\d+)?))\s*(?:mas|más|\+)\s*(?:el\s+)?((?:\d+(?:\.\d+)?))\s*%', re.IGNORECASE)
_RE_MENOS_PORCENTAJE = re.compile(r'((?:\d+(?:\.\d+)?))\s*(?:menos|-)\s*(?:el\s+)?((?:\d+(?:\.\d+)?))\s*%', re.IGNORECASE)
_RE_DESCUENTO        = re.compile(r'descuento\s+(?:del?\s+)?((?:\d+(?:\.\d+)?))\s*%\s+(?:de|sobre|a)\s+((?:\d+(?:\.\d+)?))', re.IGNORECASE)

def _calcular_porcentaje_directo(texto: str) -> Optional[Tuple[str, str]]:
    """Detecta y resuelve porcentajes directamente sin SymPy."""
    m = _RE_DESCUENTO.search(texto)
    if m:
        pct = float(m.group(1)); base = float(m.group(2))
        descuento = base * pct / 100; final = base - descuento
        return (
            str(int(final) if final == int(final) else round(final, 6)),
            f"{pct}% de descuento sobre {base}: descuento = {descuento}, precio final = {final}"
        )
    m = _RE_MAS_PORCENTAJE.search(texto)
    if m:
        base = float(m.group(1)); pct = float(m.group(2))
        resultado = base * (1 + pct / 100)
        r = int(resultado) if resultado == int(resultado) else round(resultado, 6)
        return (str(r), f"{base} + {pct}% = {r}")
    m = _RE_MENOS_PORCENTAJE.search(texto)
    if m:
        base = float(m.group(1)); pct = float(m.group(2))
        resultado = base * (1 - pct / 100)
        r = int(resultado) if resultado == int(resultado) else round(resultado, 6)
        return (str(r), f"{base} - {pct}% = {r}")
    m = _RE_PORCENTAJE_DE.search(texto)
    if m:
        pct = float(m.group(1)); base = float(m.group(2))
        resultado = base * pct / 100
        r = int(resultado) if resultado == int(resultado) else round(resultado, 6)
        return (str(r), f"{pct}% de {base} = {r}")
    return None


# ═══════════════════════════════════════════════════════════════════════
# FIX-C4: LIMPIAR PREFIJOS
# ═══════════════════════════════════════════════════════════════════════

def limpiar_prefijos(texto: str) -> str:
    """Elimina palabras en español que preceden a una expresion matematica.
    FIX-C10: prefijos informales/coloquiales expandidos.
    """
    t = texto.strip()

    # Prefijos de mas largo a mas corto para evitar solapamientos
    prefijos = [
        r'ayuda(?:me)?\s+con\s+(?:esto|eso|lo\s+siguiente)[:\s]*',
        r'oye[,\s]+',
        r'che[,\s]+',
        r'mira[,\s]+',
        r'(?:esto|eso|lo\s+siguiente)[:\s]+',
        r'necesito\s+saber\s+cu[aá]nto\s+(?:es|da|son)\s+',
        r'necesito\s+saber\s+',
        r'necesito\s+',
        r'cu[aá]nto\s+(?:es|da|son)\s+',
        r'cu[aá]nto\s+es\s+(?:el\s+)?',
        r'cu[aá]nto\s+es\s+',
        r'cu[aá]nto\s+',
        r'cu[aá]l\s+es\s+el\s+valor\s+de\s+',
        r'cu[aá]l\s+es\s+',
        r'el\s+resultado\s+de\s+',
        r'resultado\s+de\s+',
        r'calcula[r]?\s+(?:la\s+|el\s+)?',
        r'dame\s+',
        r'dime\s+(?:el\s+|la\s+)?',
        r'obten\s+',
        r'obt[eé]n\s+',
        r'haz\s+',
        r'halla[r]?\s+(?:x|y|z)\s+si\s+',
        r'resuelve[r]?\s+(?:la\s+|el\s+)?',
        r'calcula\s+(?:la\s+|el\s+)?',
        r'encuentra[r]?\s+',
        r'halla[r]?\s+',
        r'determina[r]?\s+',
        r'que\s+es\s+',
    ]
    for p in prefijos:
        nuevo = re.sub(r'^' + p, '', t, flags=re.IGNORECASE).strip()
        if nuevo != t:
            t = nuevo
            break

    # FIX-C10b: "si " al inicio contamina expresiones como "si 3x + 7 = 22"
    t = re.sub(r'^si\s+(?=[a-zA-Z0-9\(\-])', '', t, flags=re.IGNORECASE).strip()

    return t


# ═══════════════════════════════════════════════════════════════════════
# FIX-C7: LIMPIAR PALABRAS ESPAÑOL ANTES DE SYMPY
# ═══════════════════════════════════════════════════════════════════════

_PALABRAS_RUIDO_ES = re.compile(
    r'\b(?:'
    r'de|del|la|el|los|las|un|una|unos|unas|'
    r'con|sin|para|por|sobre|hasta|desde|entre|'
    r'que|como|cuando|donde|'
    r'es|son|esta|hay|tiene|'
    r'resuelve|resolver|calcula|calcular|'
    r'encuentra|encontrar|obtener|obten|'
    r'halla|hallar|dame|dime|'
    r'ecuacion|expresion|funcion|formula|'
    r'valor|valores|numero|numeros|'
    r'resultado|resultados|'
    r'siendo|dado|dados|dada|dadas|'
    r'donde|con|tal|que'
    r')\b', re.IGNORECASE
)

_VARIABLES_MATEMATICAS_VALIDAS = set('xyztnabckmrsuv')
_NOMBRES_FUNCIONES_VALIDAS = {
    'sin', 'cos', 'tan', 'asin', 'acos', 'atan',
    'sinh', 'cosh', 'tanh', 'exp', 'log', 'sqrt',
    'abs', 'ceil', 'floor', 'factorial', 'cbrt', 'pi', 'ln',
    'sec', 'csc', 'cot',
}

def _limpiar_palabras_espanol(expr: str) -> str:
    """FIX-C7: Elimina palabras en español que SymPy interpreta como variables."""
    tiene_variables     = bool(re.search(r'[a-zA-Z]\s*[\*\+\-\/\^\(]|[\*\+\-\/\^]\s*[a-zA-Z]|\*\*', expr))
    tiene_numero_y_letra = bool(re.search(r'\d.*[a-zA-Z]|[a-zA-Z].*\d', expr))
    if not (tiene_variables or tiene_numero_y_letra):
        return expr
    _placeholder = {}
    for i, fn in enumerate(_NOMBRES_FUNCIONES_VALIDAS):
        token = f'__MATHFN{i}__'
        patron_fn = r'\b' + re.escape(fn) + r'\b'
        if re.search(patron_fn, expr, re.IGNORECASE):
            expr = re.sub(patron_fn, token, expr, flags=re.IGNORECASE)
            _placeholder[token] = fn
    def _reemplazar_ruido(m):
        palabra = m.group(0)
        if '__MATHFN' in palabra:
            return palabra
        if len(palabra) == 1 and palabra.lower() in _VARIABLES_MATEMATICAS_VALIDAS:
            return palabra
        return ' '
    expr = _PALABRAS_RUIDO_ES.sub(_reemplazar_ruido, expr)
    for token, fn in _placeholder.items():
        expr = expr.replace(token, fn)
    expr = re.sub(r'\s{2,}', ' ', expr).strip()
    return expr


# ═══════════════════════════════════════════════════════════════════════
# FIX-C6: FUNCIONES MATEMÁTICAS EN ESPAÑOL
# ═══════════════════════════════════════════════════════════════════════

def _convertir_funciones_espanol(texto: str) -> str:
    """FIX-C6: Convierte funciones matemáticas en español a equivalente SymPy."""
    t = texto.strip()

    # FIX-C9: potencias en lenguaje natural CON variable
    # "x al cuadrado" → "x**2", "x al cubo" → "x**3"
    t = re.sub(r'([a-zA-Z])\s+al\s+cuadrado', r'\1**2', t, flags=re.IGNORECASE)
    t = re.sub(r'([a-zA-Z])\s+al\s+cubo', r'\1**3', t, flags=re.IGNORECASE)
    t = re.sub(r'([a-zA-Z])\s+elevado\s+a\s+la?\s+(\w+)', r'\1**\2', t, flags=re.IGNORECASE)
    t = re.sub(r'([a-zA-Z])\s+elevado\s+a\s+(\d+)', r'\1**\2', t, flags=re.IGNORECASE)
    # "al cuadrado" sin variable previa (número)
    t = re.sub(r'(\d+)\s+al\s+cuadrado', r'\1**2', t, flags=re.IGNORECASE)
    t = re.sub(r'(\d+)\s+al\s+cubo', r'\1**3', t, flags=re.IGNORECASE)

    # Factorial
    t = re.sub(r'factorial\s+de\s+(\d+)', lambda m: f'factorial({m.group(1)})', t, flags=re.IGNORECASE)
    t = re.sub(r'(\d+)\s*!', lambda m: f'factorial({m.group(1)})', t)

    # Trigonométricas con grados
    t = re.sub(r'(?:seno|sen)\s+de\s+(\d+(?:\.\d+)?)\s+grados?',
               lambda m: f'sin({m.group(1)}*pi/180)', t, flags=re.IGNORECASE)
    t = re.sub(r'coseno\s+de\s+(\d+(?:\.\d+)?)\s+grados?',
               lambda m: f'cos({m.group(1)}*pi/180)', t, flags=re.IGNORECASE)
    t = re.sub(r'tangente\s+de\s+(\d+(?:\.\d+)?)\s+grados?',
               lambda m: f'tan({m.group(1)}*pi/180)', t, flags=re.IGNORECASE)
    t = re.sub(r'secante\s+de\s+(\d+(?:\.\d+)?)\s+grados?',
               lambda m: f'sec({m.group(1)}*pi/180)', t, flags=re.IGNORECASE)
    t = re.sub(r'cosecante\s+de\s+(\d+(?:\.\d+)?)\s+grados?',
               lambda m: f'csc({m.group(1)}*pi/180)', t, flags=re.IGNORECASE)
    t = re.sub(r'cotangente\s+de\s+(\d+(?:\.\d+)?)\s+grados?',
               lambda m: f'cot({m.group(1)}*pi/180)', t, flags=re.IGNORECASE)

    # Trigonométricas sin grados
    t = re.sub(r'(?:seno|sen)\s+de\s+([^\s,]+)',   lambda m: f'sin({m.group(1)})',  t, flags=re.IGNORECASE)
    t = re.sub(r'coseno\s+de\s+([^\s,]+)',          lambda m: f'cos({m.group(1)})',  t, flags=re.IGNORECASE)
    t = re.sub(r'tangente\s+de\s+([^\s,]+)',        lambda m: f'tan({m.group(1)})',  t, flags=re.IGNORECASE)
    t = re.sub(r'secante\s+de\s+([^\s,]+)',         lambda m: f'sec({m.group(1)})',  t, flags=re.IGNORECASE)
    t = re.sub(r'cosecante\s+de\s+([^\s,]+)',       lambda m: f'csc({m.group(1)})',  t, flags=re.IGNORECASE)
    t = re.sub(r'cotangente\s+de\s+([^\s,]+)',      lambda m: f'cot({m.group(1)})',  t, flags=re.IGNORECASE)

    # Inversas trigonométricas
    t = re.sub(r'arcoseno\s+de\s+([^\s,]+)',        lambda m: f'asin({m.group(1)})', t, flags=re.IGNORECASE)
    t = re.sub(r'arcocoseno\s+de\s+([^\s,]+)',      lambda m: f'acos({m.group(1)})', t, flags=re.IGNORECASE)
    t = re.sub(r'arcotangente\s+de\s+([^\s,]+)',    lambda m: f'atan({m.group(1)})', t, flags=re.IGNORECASE)

    # Logaritmos
    t = re.sub(r'logaritmo\s+natural\s+de\s+(\d+(?:\.\d+)?)',
               lambda m: f'log({m.group(1)})', t, flags=re.IGNORECASE)
    t = re.sub(r'\bln\s+de\s+(\d+(?:\.\d+)?)',
               lambda m: f'log({m.group(1)})', t, flags=re.IGNORECASE)
    t = re.sub(r'logaritmo\s+(?:en\s+)?base\s+(\d+)\s+de\s+(\d+(?:\.\d+)?)',
               lambda m: f'log({m.group(2)}, {m.group(1)})', t, flags=re.IGNORECASE)
    t = re.sub(r'log\s+base\s+(\d+)\s+de\s+(\d+(?:\.\d+)?)',
               lambda m: f'log({m.group(2)}, {m.group(1)})', t, flags=re.IGNORECASE)
    t = re.sub(r'log\s+de\s+(\d+(?:\.\d+)?)\s+(?:en\s+)?base\s+(\d+)',
               lambda m: f'log({m.group(1)}, {m.group(2)})', t, flags=re.IGNORECASE)
    t = re.sub(r'logaritmo\s+de\s+(\d+(?:\.\d+)?)',
               lambda m: f'log({m.group(1)})', t, flags=re.IGNORECASE)
    t = re.sub(r'\blog\s+de\s+(\d+(?:\.\d+)?)',
               lambda m: f'log({m.group(1)}, 10)', t, flags=re.IGNORECASE)

    # Raíces
    t = re.sub(r'ra[íi]z\s+c[uú]bica\s+de\s+(\d+(?:\.\d+)?)',
               lambda m: f'({m.group(1)}**(1/3))', t, flags=re.IGNORECASE)
    t = re.sub(r'ra[íi]z\s+cuadrada\s+de\s+(\d+(?:\.\d+)?)',
               lambda m: f'sqrt({m.group(1)})', t, flags=re.IGNORECASE)
    t = re.sub(r'ra[íi]z\s+de\s+(\d+(?:\.\d+)?)',
               lambda m: f'sqrt({m.group(1)})', t, flags=re.IGNORECASE)
    t = re.sub(r'ra[íi]z\s+(\d+)(?:esima|ésima|a)?\s+de\s+(\d+(?:\.\d+)?)',
               lambda m: f'({m.group(2)}**(1/{m.group(1)}))', t, flags=re.IGNORECASE)

    # Conversión grados/radianes
    t = re.sub(r'convierte?\s+(\d+(?:\.\d+)?)\s+grados?\s+(?:a\s+)?radianes?',
               lambda m: f'({m.group(1)}*pi/180)', t, flags=re.IGNORECASE)
    t = re.sub(r'(\d+(?:\.\d+)?)\s+grados?\s+(?:a|en)\s+radianes?',
               lambda m: f'({m.group(1)}*pi/180)', t, flags=re.IGNORECASE)
    t = re.sub(r'convierte?\s+(\d+(?:\.\d+)?)\s+radianes?\s+(?:a\s+)?grados?',
               lambda m: f'({m.group(1)}*180/pi)', t, flags=re.IGNORECASE)

    # Valor absoluto en español
    t = re.sub(r'valor\s+absoluto\s+de\s+([^\s,]+)',
               lambda m: f'abs({m.group(1)})', t, flags=re.IGNORECASE)

    return t


# ═══════════════════════════════════════════════════════════════════════
# NORMALIZADOR COMPLETO v8.0
# ═══════════════════════════════════════════════════════════════════════

def normalizar_expresion(texto: str) -> str:
    """Convierte texto natural/matematico a forma evaluable por SymPy.
    v8.1: FIX-C10 prefijos informales expandidos + FIX-C11 bypass simbolico.
    """
    t = texto.strip()

    # FIX-C8 + FIX-C10: eliminar prefijos de contexto (orden: mas largo primero)
    _prefijos = [
        (r'^ayuda(?:me)?\s+con\s+(?:esto|eso)[:\s]*', ''),
        (r'^oye[,\s]+', ''),
        (r'^che[,\s]+', ''),
        (r'^mira[,\s]+', ''),
        (r'^(?:esto|eso|aqui|aca|lo\s+siguiente)[:\s]+', ''),
    ]
    for _pat, _rep in _prefijos:
        _nuevo = re.sub(_pat, _rep, t, flags=re.IGNORECASE).strip()
        if _nuevo != t:
            t = _nuevo
            break

    # Limpiar prefijos de tarea especificos
    t = re.sub(r'^resuelve[r]?\s+la\s+inecuaci[oó]n\s+', '', t, flags=re.IGNORECASE).strip()
    t = re.sub(r'^(?:la\s+|el\s+)?inecuaci[oó]n\s+', '', t, flags=re.IGNORECASE).strip()
    t = re.sub(r'\bparcial\s+de\b', '', t, flags=re.IGNORECASE).strip()
    t = re.sub(r'^(?:la\s+)?funci[oó]n\s+[a-zA-Z]\s*\([a-zA-Z]\)\s*=\s*', '', t, flags=re.IGNORECASE).strip()
    t = re.sub(r'^[a-zA-Z]\s*\([a-zA-Z]\)\s*=\s*', '', t, flags=re.IGNORECASE).strip()
    # FIX-C10c: "grado del polinomio X" / "coeficientes del polinomio X"
    t = re.sub(r'^(?:grado|coeficientes?|ra[ií]ces?)\s+del?\s+polinomio\s+', '', t, flags=re.IGNORECASE).strip()

    # FIX-C6: funciones matematicas en espanol PRIMERO
    t = _convertir_funciones_espanol(t)

    # Unicode -> operadores ASCII
    t = t.replace('\u00f7', '/')
    t = t.replace('\u00d7', '*')
    t = t.replace('\u2212', '-')
    t = t.replace('\u00b2', '**2')
    t = t.replace('\u00b3', '**3')
    t = t.replace('\u221e', 'oo')
    t = t.replace('\u03c0', 'pi')
    t = t.replace('\u2260', '!=')
    t = t.replace('\u2264', '<=')
    t = t.replace('\u2265', '>=')

    # Simbolo raiz
    t = re.sub(r'\u221a\s*(\d+(?:\.\d+)?)', r'sqrt(\1)', t)
    t = re.sub(r'\u221a\s*\(', 'sqrt(', t)

    # Potencia ^ -> **
    t = t.replace('^', '**')
    t = re.sub(r'al\s+cuadrado', '**2', t, flags=re.IGNORECASE)
    t = re.sub(r'al\s+cubo', '**3', t, flags=re.IGNORECASE)
    t = re.sub(r'elevado\s+a\s+la?\s+(\w+)', r'**\1', t, flags=re.IGNORECASE)
    t = re.sub(r'elevado\s+a\s+(\d+)', r'**\1', t, flags=re.IGNORECASE)

    # Raiz en texto (refuerzo)
    t = re.sub(r'ra[ií]z\s+cuadrada\s+de\s+(\d+(?:\.\d+)?)', r'sqrt(\1)', t, flags=re.IGNORECASE)
    t = re.sub(r'ra[ií]z\s+c[uú]bica\s+de\s+(\d+(?:\.\d+)?)', r'(\1**(1/3))', t, flags=re.IGNORECASE)
    t = re.sub(r'ra[ií]z\s+de\s+(\d+(?:\.\d+)?)', r'sqrt(\1)', t, flags=re.IGNORECASE)

    # Operadores en espanol (entre numeros)
    t = re.sub(r'(\d+(?:\.\d+)?)\s+dividido\s+(?:entre|por)\s+(\d+(?:\.\d+)?)', r'\1 / \2', t, flags=re.IGNORECASE)
    t = re.sub(r'(\d+(?:\.\d+)?)\s+entre\s+(\d+(?:\.\d+)?)', r'\1 / \2', t, flags=re.IGNORECASE)
    t = re.sub(r'(\d+(?:\.\d+)?)\s+por\s+(\d+(?:\.\d+)?)', r'\1 * \2', t, flags=re.IGNORECASE)
    t = re.sub(r'(\d+(?:\.\d+)?)\s+multiplicado\s+por\s+(\d+(?:\.\d+)?)', r'\1 * \2', t, flags=re.IGNORECASE)
    t = re.sub(r'(\d+(?:\.\d+)?)\s+m[aá]s\s+(\d+(?:\.\d+)?)', r'\1 + \2', t, flags=re.IGNORECASE)
    t = re.sub(r'(\d+(?:\.\d+)?)\s+menos\s+(\d+(?:\.\d+)?)', r'\1 - \2', t, flags=re.IGNORECASE)

    # Notacion cientifica
    t = re.sub(r'(\d+(?:\.\d+)?)\s*[x×]\s*10\s*\*\*\s*(\d+)', r'\1*10**\2', t, flags=re.IGNORECASE)
    t = re.sub(r'(\d+(?:\.\d+)?)\s*[x×]\s*10\^(\d+)', r'\1*10**\2', t, flags=re.IGNORECASE)

    # FIX-C1: coeficiente implicito digito+letra -> digito*letra
    _FUNCIONES = ['sqrt', 'cbrt', 'sin', 'cos', 'tan', 'sec', 'csc', 'cot',
                  'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh',
                  'exp', 'log', 'abs', 'ceil', 'floor', 'factorial']
    _ph = {}
    for i, fn in enumerate(_FUNCIONES):
        token = f'__FN{i}__'
        t = t.replace(fn, token)
        _ph[token] = fn
    t = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', t)
    for token, fn in _ph.items():
        t = t.replace(token, fn)

    return t.strip()


# ═══════════════════════════════════════════════════════════════════════
# DETECTORES AUXILIARES
# ═══════════════════════════════════════════════════════════════════════

_VERBOS_MAT_AVANZADOS = re.compile(
    r'^(?:deriv[aá]?(?:da)?|integr[aá]?|l[íi]mite|lim\b|factori[zs]|simplific|'
    r'expan[ds]|resolv|resuelv|taylor|parcial|evalua|sistema)',
    re.IGNORECASE
)

_RE_CONTENIDO_ALGEBRAICO = re.compile(
    r'(?:[a-zA-Z][\*\+\-]|[\*\+\-][a-zA-Z]|\*\*|[a-zA-Z]\*\*|sin\(|cos\(|tan\(|sqrt\(|exp\(|log\()',
    re.IGNORECASE
)

_RE_PALABRA_NO_NUMERICA = re.compile(r'[a-zA-Z]{2,}')
_VARIABLES_VALIDAS = {
    'pi', 'e', 'x', 'y', 'z', 'n', 't', 'a', 'b', 'c',
    'sin', 'cos', 'tan', 'sec', 'csc', 'cot', 'exp', 'log',
    'sqrt', 'cbrt', 'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh',
    'abs', 'oo', 'inf', 'ln', 'factorial',
}

def _detectar_problema_basico(expr_limpia: str) -> Optional[str]:
    """FIX-C5: mensajes de error descriptivos antes de parsear con SymPy."""
    expr = expr_limpia.strip()
    if not expr:
        return "No detecté la expresión matemática. Dime qué quieres calcular."
    m_verbo = _VERBOS_MAT_AVANZADOS.match(expr)
    if m_verbo:
        verbo = m_verbo.group(0).lower()
        resto = expr[m_verbo.end():].strip()
        if not resto:
            ejemplos = {
                'deriv':  'deriva x**2 + 3*x',
                'integr': 'integra x**2',
                'limit':  'límite de 1/x cuando x tiende a infinito',
                'factor': 'factoriza x**2 - 9',
                'simplif':'simplifica (x**2 - 1)/(x - 1)',
                'expan':  'expande (x + 1)**2',
                'resolv': 'resuelve x**2 - 5*x + 6',
                'resuelv':'resuelve x**2 - 5*x + 6',
                'taylor': 'serie de Taylor de sin(x)',
            }
            for prefijo, ejemplo in ejemplos.items():
                if verbo.startswith(prefijo):
                    return f"¿Qué expresión quieres {verbo}r? Ejemplo: '{ejemplo}'"
            return f"¿Qué expresión quieres {verbo}r? Escribe la expresión matemática."
        if not _RE_CONTENIDO_ALGEBRAICO.search(resto):
            if '.' in resto or re.search(r'[a-zA-Z]{4,}', resto):
                return f"'{resto}' no es una expresión matemática. Escribe: '{verbo}r x**2 + 3*x' o similar."
    palabras_largas = _RE_PALABRA_NO_NUMERICA.findall(expr)
    palabras_invalidas = [p for p in palabras_largas if p.lower() not in _VARIABLES_VALIDAS]
    if palabras_invalidas:
        tiene_algebraico = bool(_RE_CONTENIDO_ALGEBRAICO.search(expr))
        if not tiene_algebraico:
            primera = palabras_invalidas[0]
            return f"'{primera}' no es un valor numérico. Solo puedo operar con números y variables matemáticas."
    return None


def validar_operandos_numericos(resultado) -> bool:
    """Verifica que el resultado sea un número real evaluable."""
    if resultado is None:
        return False
    try:
        float(resultado)
        return True
    except (TypeError, ValueError):
        pass
    try:
        if hasattr(resultado, 'free_symbols') and resultado.free_symbols:
            return False
        val = float(resultado.evalf())
        return math.isfinite(val)
    except Exception:
        return False


# ═══════════════════════════════════════════════════════════════════════
# NUEVO-C21: DETECTOR AUTOMÁTICO DE OPERACIÓN POR TEXTO
# ═══════════════════════════════════════════════════════════════════════

_DETECTORES_AUTO = [
    # Estadística — detectar PRIMERO (antes de calcular)
    (re.compile(
        r'(?:media|promedio|average|desviacion|desviación|varianza|mediana|moda|'
        r'estadistica|estadística|distribucion|distribución)\s+(?:de|del?)?\s*'
        r'(?:los?|las?)?\s*[\[\(]?[\d\s,\.]+[\]\)]?',
        re.IGNORECASE), 'ESTADISTICA'),
    (re.compile(r'(?:calcula|dame|obtén?|halla)\s+(?:la\s+)?(?:media|promedio|desviaci[oó]n|varianza|mediana|moda)\s+de', re.IGNORECASE), 'ESTADISTICA'),

    # Sistema de ecuaciones
    (re.compile(r'sistema\s+de\s+ecuaciones?|ecuaciones?\s+simult[aá]neas?|sistema\s+lineal|resuelve\s+el\s+sistema', re.IGNORECASE), 'SISTEMA'),

    # Derivadas
    (re.compile(r'deriv[aá](?:da)?|diferencial\s+de|d/dx|dy/dx|f\'\(', re.IGNORECASE), 'DERIVADA'),
    (re.compile(r'segunda\s+derivada|derivada\s+de\s+orden\s+2|derivada\s+parcial', re.IGNORECASE), 'DERIVADA'),

    # Integrales
    (re.compile(r'integr[aá](?:l)?|antiderivada|primitiva\s+de|[∫]|área\s+bajo', re.IGNORECASE), 'INTEGRAL'),

    # Límites
    (re.compile(r'l[íi]mite|lim\s*\(|lim\s+de|cuando\s+x\s+tiende|tiende\s+a', re.IGNORECASE), 'LIMITE'),

    # Taylor
    (re.compile(r'serie\s+de\s+taylor|expansi[oó]n\s+de\s+taylor|taylor\s+de', re.IGNORECASE), 'TAYLOR'),

    # Factorizar
    (re.compile(r'factori[zs]a(?:r)?|factores?\s+de', re.IGNORECASE), 'FACTORIZAR'),

    # Simplificar
    (re.compile(r'simplifica(?:r)?|reducir\s+expresi[oó]n|forma\s+m[aá]s\s+simple', re.IGNORECASE), 'SIMPLIFICAR'),

    # Expandir
    (re.compile(r'expande?(?:r)?|desarrolla(?:r)?\s+(?:la\s+)?expresi[oó]n|distribuye?', re.IGNORECASE), 'EXPANDIR'),

    # Resolver ecuación
    (re.compile(r'(?:resolv|resuelv|solve|encuentra\s+(?:el\s+valor|las?\s+ra[íi]ces?)|halla\s+(?:x|y|z))', re.IGNORECASE), 'ECUACION'),

    # Evaluar
    (re.compile(r'evalua(?:r)?|valor\s+de\s+f\(|calcula\s+f\(|sustituye?(?:r)?', re.IGNORECASE), 'EVALUAR'),

    # Porcentajes
    (re.compile(r'\d+\s*%|\d+\s+por\s+ciento|descuento\s+de', re.IGNORECASE), 'PORCENTAJE'),

    # MCD/MCM
    (re.compile(r'(?:mcd|m\.c\.d|maximo\s+comun\s+divisor|gcd)', re.IGNORECASE), 'MCD'),
    (re.compile(r'(?:mcm|m\.c\.m|minimo\s+comun\s+multiplo|lcm)', re.IGNORECASE), 'MCM'),

    # Primo
    (re.compile(r'es\s+primo|numero\s+primo|primo\?', re.IGNORECASE), 'PRIMO'),

    # Combinatoria
    (re.compile(r'combinaciones?\s+de|c\s*\(\s*\d+|nCr', re.IGNORECASE), 'COMBINACIONES'),
    (re.compile(r'permutaciones?\s+de|p\s*\(\s*\d+|nPr', re.IGNORECASE), 'PERMUTACIONES'),
]

def detectar_tipo_operacion(mensaje: str) -> str:
    """NUEVO-C21: Detecta automáticamente el tipo de operación matemática."""
    for patron, tipo in _DETECTORES_AUTO:
        if patron.search(mensaje):
            return tipo
    return 'BASICO'


# ═══════════════════════════════════════════════════════════════════════
# HELPERS DE FORMATO
# ═══════════════════════════════════════════════════════════════════════

def _formatear_resultado(expr_sympy) -> str:
    if expr_sympy is None:
        return ""
    return str(expr_sympy)

def _resultado_numerico(expr_sympy) -> Optional[float]:
    try:
        v = float(expr_sympy.evalf())
        return v if math.isfinite(v) else None
    except Exception:
        return None


# ═══════════════════════════════════════════════════════════════════════
# ESTADÍSTICA PURA (sin NumPy, fallback)
# ═══════════════════════════════════════════════════════════════════════

def _estadistica_pura(datos: List[float]) -> dict:
    """Calcula estadísticas descriptivas sin NumPy."""
    n = len(datos)
    media = sum(datos) / n
    datos_sorted = sorted(datos)
    if n % 2 == 0:
        mediana = (datos_sorted[n//2 - 1] + datos_sorted[n//2]) / 2
    else:
        mediana = datos_sorted[n//2]
    from collections import Counter
    conteo = Counter(datos)
    max_frec = max(conteo.values())
    modas = [k for k, v in conteo.items() if v == max_frec]
    moda = modas[0] if len(modas) == 1 else modas
    varianza = sum((x - media) ** 2 for x in datos) / n
    desv_est = math.sqrt(varianza)
    varianza_muestral = sum((x - media) ** 2 for x in datos) / (n - 1) if n > 1 else 0
    desv_muestral = math.sqrt(varianza_muestral)
    minimo = datos_sorted[0]
    maximo = datos_sorted[-1]
    rango = maximo - minimo
    # Percentiles
    def percentil(p):
        idx = (p / 100) * (n - 1)
        lo, hi = int(idx), min(int(idx) + 1, n - 1)
        return datos_sorted[lo] + (idx - lo) * (datos_sorted[hi] - datos_sorted[lo])
    q1, q2, q3 = percentil(25), percentil(50), percentil(75)
    iqr = q3 - q1
    return {
        'n': n, 'media': media, 'mediana': mediana, 'moda': moda,
        'varianza_poblacional': varianza, 'desviacion_poblacional': desv_est,
        'varianza_muestral': varianza_muestral, 'desviacion_muestral': desv_muestral,
        'minimo': minimo, 'maximo': maximo, 'rango': rango,
        'q1': q1, 'q2': q2, 'q3': q3, 'iqr': iqr,
        'suma': sum(datos),
    }

def _parsear_lista_numeros(entrada) -> Optional[List[float]]:
    """Parsea una lista de números desde string, list, o tuple."""
    if isinstance(entrada, (list, tuple)):
        try:
            return [float(x) for x in entrada]
        except (TypeError, ValueError):
            return None
    if isinstance(entrada, str):
        # Remover corchetes y paréntesis
        limpio = re.sub(r'[\[\]\(\)]', '', entrada)
        partes = re.split(r'[,\s]+', limpio.strip())
        try:
            return [float(p) for p in partes if p]
        except ValueError:
            return None
    return None


# ═══════════════════════════════════════════════════════════════════════
# CLASE PRINCIPAL v8.0
# ═══════════════════════════════════════════════════════════════════════

class CalculadoraAvanzada:
    """
    Calculadora matemática avanzada usando SymPy. v8.0

    v8.0: BUG-03 FIX en resolver_sistema(), NUEVO estadisticas(),
          derivada_parcial() expuesta, evaluar mejorado, aritmética
          discreta, calcular_automatico() para entrada libre.
    Todos los fixes y novedades de v7.1 preservados intactos.
    """

    def __init__(self):
        self.x, self.y, self.z = symbols('x y z')
        self.t = symbols('t')
        self.n = symbols('n', integer=True)
        self.ultima_expresion = None
        self._historial: List[Dict[str, Any]] = []

    # ------------------------------------------------------------------
    # PARSER
    # ------------------------------------------------------------------

    def _parsear(self, expresion: str):
        """Parsea una expresión matemática con SymPy. FIX-C7 aplicado."""
        expr_limpia = _limpiar_palabras_espanol(expresion)
        try:
            return parse_expr(
                expr_limpia, local_dict=_LOCAL_DICT,
                transformations=_TRANSFORMACIONES, evaluate=True,
            )
        except Exception:
            try:
                return parse_expr(expr_limpia, local_dict=_LOCAL_DICT, evaluate=True)
            except Exception:
                return parse_expr(expresion, local_dict=_LOCAL_DICT, evaluate=True)

    def _guardar_historial(self, tipo: str, entrada: str, resultado: str, exitoso: bool):
        self._historial.append({'tipo': tipo, 'entrada': entrada, 'resultado': resultado, 'exitoso': exitoso})
        if len(self._historial) > 50:
            self._historial.pop(0)

    def historial(self, n: int = 10) -> List[Dict]:
        return self._historial[-n:]

    def historial_texto(self, n: int = 10) -> str:
        items = self.historial(n)
        if not items:
            return "No hay operaciones registradas en esta sesión."
        lineas = []
        for i, op in enumerate(items, 1):
            estado = "✓" if op['exitoso'] else "✗"
            lineas.append(f"{i}. [{estado}] {op['tipo']}: {op['entrada']} = {op['resultado']}")
        return "\n".join(lineas)

    # ------------------------------------------------------------------
    # NUEVO-C21: CALCULAR AUTOMÁTICO — entrada libre
    # ------------------------------------------------------------------

    def calcular_automatico(self, mensaje: str) -> ResultadoMatematico:
        """
        NUEVO-C21: Detecta automáticamente el tipo de operación y la ejecuta.
        Punto de entrada único para cuando el motor no especifica sub_tipo.
        Bell puede recibir cualquier mensaje matemático y este método lo maneja.
        """
        tipo = detectar_tipo_operacion(mensaje)
        pasos = [f"Tipo detectado automáticamente: {tipo}", f"Entrada: {mensaje}"]

        if tipo == 'ESTADISTICA':
            # Extraer lista de números del mensaje
            m = re.search(r'[\[\(]?([\d\s,\.]+)[\]\)]?', mensaje)
            if m:
                return self.estadisticas(m.group(1))
            return self._error(mensaje, pasos, "No encontré una lista de números para calcular estadísticas.", "ESTADISTICA")

        if tipo == 'SISTEMA':
            # FIX-SIS: separación inteligente — NO hacer split por "y" (es variable)
            # Limpiar prefijo "resuelve el sistema:", "ecuaciones simultaneas:", etc.
            msg_sis = re.sub(
                r'^(?:resuelve[r]?\s+el\s+sistema\s*:?\s*|sistema\s+de\s+ecuaciones?\s*:?\s*|'
                r'ecuaciones?\s+simult[aá]neas?\s*:?\s*|sistema\s+lineal\s*:?\s*)',
                '', mensaje, flags=re.IGNORECASE
            ).strip()
            # Separar por ; primero (más seguro)
            if ';' in msg_sis:
                eqs_raw = msg_sis.split(';')
            # Separar por coma cuando hay al menos 2 signos '=' en el mensaje
            elif msg_sis.count('=') >= 2 and ',' in msg_sis:
                eqs_raw = msg_sis.split(',')
            # Separar por " y " SOLO si la y NO es variable (la y que separa va antes de dígito o letra distinta a y/z)
            elif re.search(r'\s+y\s+(?=\d|[a-wz])', msg_sis, re.IGNORECASE):
                eqs_raw = re.split(r'\s+y\s+(?=\d|[a-wz])', msg_sis, flags=re.IGNORECASE)
            elif '\n' in msg_sis:
                eqs_raw = msg_sis.split('\n')
            else:
                eqs_raw = [msg_sis]
            eqs_limpias = [e.strip() for e in eqs_raw if '=' in e]
            if len(eqs_limpias) >= 2:
                return self.resolver_sistema(eqs_limpias)
            return self._error(mensaje, pasos, "No encontré un sistema de ecuaciones. Separa las ecuaciones con ';'.", "SISTEMA")

        if tipo == 'DERIVADA':
            expr = self._extraer_expresion_de_mensaje(mensaje, 'derivada')
            if expr:
                orden = 2 if re.search(r'segunda|orden\s+2', mensaje, re.IGNORECASE) else 1
                var = self._extraer_variable_de_mensaje(mensaje)
                if 'parcial' in mensaje.lower():
                    return self.derivada_parcial(expr, var, orden)
                return self.derivar(expr, var, orden)

        if tipo == 'INTEGRAL':
            expr = self._extraer_expresion_de_mensaje(mensaje, 'integral')
            if expr:
                var = self._extraer_variable_de_mensaje(mensaje)
                lims = self._extraer_limites_de_mensaje(mensaje)
                return self.integrar(expr, var, lims[0], lims[1])

        if tipo == 'LIMITE':
            expr = self._extraer_expresion_de_mensaje(mensaje, 'limite')
            if expr:
                var = self._extraer_variable_de_mensaje(mensaje)
                punto = self._extraer_punto_de_mensaje(mensaje)
                return self.limite(expr, var, punto)

        if tipo == 'TAYLOR':
            expr = self._extraer_expresion_de_mensaje(mensaje, 'taylor')
            if expr:
                return self.serie_taylor(expr)

        if tipo == 'FACTORIZAR':
            expr = self._extraer_expresion_de_mensaje(mensaje, 'factorizar')
            if expr:
                return self.factorizar(expr)

        if tipo == 'SIMPLIFICAR':
            expr = self._extraer_expresion_de_mensaje(mensaje, 'simplificar')
            if expr:
                return self.simplificar(expr)

        if tipo == 'EXPANDIR':
            expr = self._extraer_expresion_de_mensaje(mensaje, 'expandir')
            if expr:
                return self.expandir(expr)

        if tipo == 'ECUACION':
            expr = self._extraer_expresion_de_mensaje(mensaje, 'ecuacion')
            if expr:
                var = self._extraer_variable_de_mensaje(mensaje)
                return self.resolver_ecuacion(expr, var)

        if tipo == 'EVALUAR':
            # FIX-EVAL: extraer "f(x) = EXPR" y "en x = N" por separado
            # Paso 1: zona de valores → buscar SOLO después de "en/con/para/cuando"
            zona_vals = re.search(r'\b(?:en|con|para|cuando)\b(.+)$', mensaje, re.IGNORECASE)
            zona = zona_vals.group(1) if zona_vals else mensaje
            valores = {}
            for m in re.finditer(r'\b([a-z])\s*=\s*([\-\d\.]+)', zona):
                try:
                    valores[m.group(1)] = float(m.group(2))
                except ValueError:
                    pass
            # Paso 2: extraer expresión — quitar "evalua", "f(x) =", y la parte "en x=N"
            expr_ev = re.sub(r'^eval[uú]a[r]?\s+', '', mensaje, flags=re.IGNORECASE).strip()
            expr_ev = re.sub(r'^(?:[a-zA-Z]\s*\([a-zA-Z,\s]+\)\s*=\s*)', '', expr_ev).strip()
            expr_ev = re.sub(r'\s+(?:en|con|para|cuando)\s+[a-z]\s*=\s*[\-\d\.]+.*$', '',
                             expr_ev, flags=re.IGNORECASE).strip()
            if expr_ev and valores:
                return self.evaluar(expr_ev, valores)

        if tipo == 'INECUACION':
            expr_in = re.sub(
                r'^(?:resuelve[r]?\s+)?(?:la\s+)?inecuaci[oó]n\s*',
                '', mensaje, flags=re.IGNORECASE
            ).strip()
            if re.search(r'[<>]', expr_in):
                return self.resolver_inecuacion(expr_in)

        if tipo == 'POLINOMIO':
            expr_pol = re.sub(
                r'^(?:(?:grado|coeficientes?|ra[ií]ces?|info)\s+del?\s+)?polinomio\s+',
                '', mensaje, flags=re.IGNORECASE
            ).strip()
            if expr_pol:
                return self.polinomio_info(expr_pol)

        if tipo == 'MCD':
            nums = re.findall(r'\d+', mensaje)
            if len(nums) >= 2:
                return self.mcd(int(nums[0]), int(nums[1]))

        if tipo == 'MCM':
            nums = re.findall(r'\d+', mensaje)
            if len(nums) >= 2:
                return self.mcm(int(nums[0]), int(nums[1]))

        if tipo == 'PRIMO':
            nums = re.findall(r'\d+', mensaje)
            if nums:
                return self.es_primo(int(nums[0]))

        if tipo == 'COMBINACIONES':
            nums = re.findall(r'\d+', mensaje)
            if len(nums) >= 2:
                return self.combinaciones(int(nums[0]), int(nums[1]))

        if tipo == 'PERMUTACIONES':
            nums = re.findall(r'\d+', mensaje)
            if len(nums) >= 2:
                return self.permutaciones(int(nums[0]), int(nums[1]))

        # Fallback: calcular básico
        return self.calcular_basico(mensaje)

    def _extraer_expresion_de_mensaje(self, mensaje: str, tipo: str) -> str:
        """Extrae la expresión matemática de un mensaje según el tipo."""
        patrones = {
            'derivada': [
                r'deriv(?:ada?\s+de|ar?)\s+(.+?)(?:\s+respecto|\s+de\s+orden|\s+en\s+x|$)',
                r'derivada\s+de\s+(.+)',
                r'd/dx\s+(?:de\s+)?(.+)',
            ],
            'integral': [
                r'integr(?:ar?|al\s+de)\s+(.+?)(?:\s+de\s+[\-\d]+\s+a|\s+respecto|$)',
                r'\u222b\s*(.+)',
            ],
            'limite': [
                r'l[íi]mite\s+de\s+(.+?)(?:\s+cuando|\s+para|\s+en\s+x|$)',
                r'lim\s+(?:de\s+)?(.+?)(?:\s+cuando|\s+tiende|$)',
            ],
            'taylor': [
                r'taylor\s+de\s+(.+?)(?:\s+alrededor|\s+en\s+x|$)',
                r'serie\s+de\s+taylor\s+de\s+(.+)',
            ],
            'factorizar': [
                r'factori[zs]a(?:r)?\s+(.+)',
                r'factores?\s+de\s+(.+)',
            ],
            'simplificar': [
                r'simplifica(?:r)?\s+(.+)',
                r'reduce\s+(.+)',
            ],
            'expandir': [
                r'expande?(?:r)?\s+(.+)',
                r'desarrolla(?:r)?\s+(.+)',
            ],
            'ecuacion': [
                r'(?:resuelve?|solve)\s+(.+)',
                r'halla\s+(?:las?\s+ra[íi]ces?\s+de\s+)?(.+)',
            ],
        }
        for p in patrones.get(tipo, []):
            m = re.search(p, mensaje, re.IGNORECASE)
            if m:
                expr = m.group(1).strip()
                # Limpiar palabras extra al final
                expr = re.sub(r'\s+(?:respecto\s+a\s+\w|de\s+orden\s+\d+)$', '', expr).strip()
                return expr
        # Fallback: devolver todo después del verbo
        expr_fallback = re.sub(
            r'^(?:calcula[r]?\s+(?:la\s+|el\s+)?)?(?:derivada|integral|limite|taylor|factori\w+|simplifica\w+|expande?\w+|resuelve?\w+)\s+(?:de\s+)?',
            '', mensaje, flags=re.IGNORECASE
        ).strip()
        return expr_fallback if expr_fallback else mensaje

    def _extraer_variable_de_mensaje(self, mensaje: str) -> str:
        m = re.search(r'respecto\s+a\s+([a-z])\b', mensaje)
        if m:
            return m.group(1)
        return 'x'

    def _extraer_limites_de_mensaje(self, mensaje: str):
        def _to_num(s):
            f = float(s)
            return int(f) if f == int(f) else f
        m = re.search(r'de\s+([\-\d\.]+)\s+a\s+([\-\d\.]+)', mensaje)
        if m:
            try:
                return _to_num(m.group(1)), _to_num(m.group(2))
            except Exception:
                pass
        return (None, None)

    def _extraer_punto_de_mensaje(self, mensaje: str):
        if any(w in mensaje.lower() for w in ['infinito', 'inf', '∞']):
            return 'oo'
        m = re.search(r'tiende\s+a\s+([\-\d\.]+)', mensaje.lower())
        if m:
            try:
                return float(m.group(1))
            except Exception:
                pass
        m = re.search(r'cuando\s+x\s*=\s*([\-\d\.]+)', mensaje.lower())
        if m:
            try:
                return float(m.group(1))
            except Exception:
                pass
        return 0

    # ------------------------------------------------------------------
    # CÁLCULO BÁSICO
    # ------------------------------------------------------------------

    # FIX-C11: operaciones simbolicas que llegan a calcular_basico
    # Se detectan ANTES de la validacion numerica y se redirigen al metodo correcto.
    _OPS_SIMBOLICAS_RE = re.compile(
        r'^(?:expande?(?:r)?|desarrolla(?:r)?|factori[zs]a(?:r)?|simplifica(?:r)?|'
        r'grado\s+del?|coeficientes?|ra[ií]ces?\s+del?|analiza\s+el)',
        re.IGNORECASE
    )

    def calcular_basico(self, expresion: str) -> ResultadoMatematico:
        """Calcula operaciones basicas con texto natural completo.
        FIX-C11: detecta operaciones simbolicas y las redirige antes de validar numericamente.
        """
        pasos = [f"Original: {expresion}"]

        # FIX-C11: redirigir operaciones simbolicas ANTES de normalizar/validar
        _msg_lower = expresion.lower().strip()
        if re.search(r'^expande?(?:r)?\s+', _msg_lower, re.IGNORECASE):
            expr_extraida = re.sub(r'^expande?(?:r)?\s+', '', expresion, flags=re.IGNORECASE).strip()
            return self.expandir(expr_extraida)
        if re.search(r'^desarrolla(?:r)?\s+', _msg_lower, re.IGNORECASE):
            expr_extraida = re.sub(r'^desarrolla(?:r)?\s+', '', expresion, flags=re.IGNORECASE).strip()
            return self.expandir(expr_extraida)
        if re.search(r'^(?:grado|coeficientes?|ra[ií]ces?)\s+del?\s+polinomio\s+', _msg_lower, re.IGNORECASE):
            expr_extraida = re.sub(r'^(?:grado|coeficientes?|ra[ií]ces?)\s+del?\s+polinomio\s+', '', expresion, flags=re.IGNORECASE).strip()
            return self.polinomio_info(expr_extraida)
        if re.search(r'^(?:resuelve[r]?\s+(?:la\s+)?inecuaci[oó]n\s+|(?:la\s+)?inecuaci[oó]n\s+)', _msg_lower, re.IGNORECASE):
            expr_extraida = re.sub(r'^(?:resuelve[r]?\s+(?:la\s+)?inecuaci[oó]n\s+|(?:la\s+)?inecuaci[oó]n\s+)', '', expresion, flags=re.IGNORECASE).strip()
            return self.resolver_inecuacion(expr_extraida)

        # Porcentajes directos
        pct = _calcular_porcentaje_directo(expresion)
        if pct:
            resultado_str, descripcion = pct
            pasos.append(f"Porcentaje directo: {descripcion}")
            self._guardar_historial("PORCENTAJE", expresion, resultado_str, True)
            return ResultadoMatematico(
                expresion_original=expresion, resultado=resultado_str,
                paso_a_paso=pasos, exitoso=True, tipo="PORCENTAJE",
            )

        # Números en español
        expr_es = _convertir_numeros_espanol(expresion)
        if expr_es != expresion:
            pasos.append(f"Convertido español: {expr_es}")

        # Funciones matemáticas en español
        expr_fn = _convertir_funciones_espanol(expr_es)
        if expr_fn != expr_es:
            pasos.append(f"Función convertida: {expr_fn}")

        # Normalizar
        normalizada = normalizar_expresion(expr_fn)
        if normalizada != expr_fn:
            pasos.append(f"Normalizada: {normalizada}")

        # Limpiar prefijos
        expr_limpia = limpiar_prefijos(normalizada)
        if expr_limpia != normalizada:
            pasos.append(f"Expresión limpia: {expr_limpia}")

        # FIX-C10d: si la expresion limpia tiene '=' y variables -> resolver ecuacion
        if '=' in expr_limpia and re.search(r'[a-zA-Z]', expr_limpia):
            # Verificar que no es una asignacion de funcion f(x) = ...
            if not re.match(r'^[a-zA-Z]\s*\([a-zA-Z]\)\s*=', expr_limpia):
                var_eq = 'x'
                _vars_eq = re.findall(r'(?<![a-zA-Z])([a-z])(?![a-zA-Z])', expr_limpia)
                _vars_eq_v = [v for v in _vars_eq if v not in ('e', 'i')]
                if _vars_eq_v:
                    var_eq = _vars_eq_v[0]
                pasos.append(f"Redirigiendo a resolver ecuacion: {expr_limpia}")
                return self.resolver_ecuacion(expr_limpia, var_eq)

        # FIX-C10e: si empieza con "derivada" o "che...derivada" -> derivar
        if re.search(r'derivada?\s+de\s+', expr_limpia, re.IGNORECASE):
            _expr_d = re.sub(r'^.*?derivada?\s+de\s+', '', expr_limpia, flags=re.IGNORECASE).strip()
            _expr_d = re.sub(r'\s+(?:cual\s+es|cuales?\s+son?).*$', '', _expr_d, flags=re.IGNORECASE).strip()
            if _expr_d:
                return self.derivar(_expr_d)

        # Deteccion temprana
        mensaje_error = _detectar_problema_basico(expr_limpia)
        if mensaje_error:
            self._guardar_historial("BASICO", expresion, mensaje_error, False)
            return ResultadoMatematico(
                expresion_original=expresion, resultado="",
                paso_a_paso=pasos, exitoso=False, error=mensaje_error, tipo="BASICO",
            )

        try:
            expr_sympy = self._parsear(expr_limpia)
            pasos.append(f"SymPy: {expr_sympy}")

            if expr_sympy == sp.zoo:
                return self._error(expresion, pasos, "División por cero: no está definido matemáticamente.", "BASICO")
            if expr_sympy == sp.oo:
                return ResultadoMatematico(expresion_original=expresion, resultado="∞ (infinito)", paso_a_paso=pasos, exitoso=True, tipo="BASICO")
            if expr_sympy == -sp.oo:
                return ResultadoMatematico(expresion_original=expresion, resultado="-∞ (-infinito)", paso_a_paso=pasos, exitoso=True, tipo="BASICO")

            if not validar_operandos_numericos(expr_sympy):
                if hasattr(expr_sympy, 'free_symbols') and expr_sympy.free_symbols:
                    simbolos = [str(s) for s in expr_sympy.free_symbols]
                    simbolos_largos = [s for s in simbolos if len(s) > 1 and s not in _VARIABLES_VALIDAS]
                    if simbolos_largos:
                        return self._error(expresion, pasos,
                            f"'{simbolos_largos[0]}' no es un valor numérico. Solo puedo operar con números.", "BASICO")
                return self._error(expresion, pasos,
                    "La expresión contiene variables no numéricas. Solo opero con números.", "BASICO")

            resultado_num = expr_sympy.evalf()
            resultado_str = self._formatear_numero(resultado_num)
            valor_num = _resultado_numerico(expr_sympy)
            pasos.append(f"Resultado: {resultado_str}")
            self._guardar_historial("BASICO", expresion, resultado_str, True)
            return ResultadoMatematico(
                expresion_original=expresion, resultado=resultado_str,
                paso_a_paso=pasos, exitoso=True, tipo="BASICO",
                valor_numerico=valor_num,
            )

        except ZeroDivisionError:
            return self._error(expresion, pasos, "División por cero: no está definido matemáticamente.", "BASICO")
        except (SyntaxError, TypeError, ValueError) as e:
            es = str(e).lower()
            if 'complex' in es or 'imagin' in es:
                return self._manejar_complejo(expresion, expr_limpia, pasos)
            expr_lower = expr_limpia.lower()
            if not _RE_CONTENIDO_ALGEBRAICO.search(expr_limpia):
                for verbo in ('deriv', 'integr', 'limit', 'factor', 'simplif', 'resolv', 'resuelv', 'expan'):
                    if expr_lower.startswith(verbo):
                        return self._error(expresion, pasos,
                            f"'{expr_limpia}' no es una expresión numérica. Para operaciones avanzadas escribe: 'deriva x**2', 'integra sin(x)', etc.", "BASICO")
            return self._error(expresion, pasos, f"No pude interpretar la expresión: {e}", "BASICO")
        except Exception as e:
            es = str(e).lower()
            if 'complex' in es or 'imagin' in es:
                return self._manejar_complejo(expresion, expr_limpia, pasos)
            if 'zoo' in es or 'division' in es or 'zero' in es:
                return self._error(expresion, pasos, "División por cero: no está definido matemáticamente.", "BASICO")
            return self._error(expresion, pasos, f"Error al calcular: {e}", "BASICO")

    # ------------------------------------------------------------------
    # MANEJO DE NÚMEROS COMPLEJOS
    # ------------------------------------------------------------------

    def _manejar_complejo(self, expresion: str, expr_limpia: str, pasos: list) -> ResultadoMatematico:
        try:
            expr_sympy = self._parsear(expr_limpia)
            re_part = float(sp.re(expr_sympy).evalf())
            im_part = float(sp.im(expr_sympy).evalf())
            if im_part == 0:
                return ResultadoMatematico(
                    expresion_original=expresion,
                    resultado=str(int(re_part) if re_part == int(re_part) else round(re_part, 10)),
                    paso_a_paso=pasos, exitoso=True, tipo="BASICO")
            resultado_str = f"{self._formatear_numero(re_part)} + {self._formatear_numero(im_part)}i"
            pasos.append(f"Número complejo: {resultado_str}")
            return ResultadoMatematico(
                expresion_original=expresion, resultado=resultado_str,
                paso_a_paso=pasos, exitoso=True, tipo="COMPLEJO",
            )
        except Exception:
            return self._error(expresion, pasos, "El resultado es un número complejo.", "BASICO")

    # ------------------------------------------------------------------
    # DERIVADAS
    # ------------------------------------------------------------------

    def derivar(self, expresion: str, variable: str = 'x', orden: int = 1) -> ResultadoMatematico:
        pasos = []
        try:
            expr_norm = normalizar_expresion(expresion)
            expr = self._parsear(expr_norm)
            pasos.append(f"Expresión: {expr}")
            self.ultima_expresion = expr
            var = symbols(variable)
            derivada = diff(expr, var, orden)
            pasos.append(f"d^{orden}/d{variable}^{orden}: {derivada}")
            resultado = simplify(derivada)
            pasos.append(f"Simplificado: {resultado}")
            resultado_str = _formatear_resultado(resultado)
            self._guardar_historial("DERIVADA", expresion, resultado_str, True)
            return ResultadoMatematico(
                expresion_original=expresion, resultado=resultado_str,
                paso_a_paso=pasos, exitoso=True, tipo="DERIVADA",
                valor_numerico=_resultado_numerico(resultado),
            )
        except Exception as e:
            return self._error(expresion, pasos, str(e), "DERIVADA")

    def derivada_parcial(self, expresion: str, variable: str = 'x', orden: int = 1) -> ResultadoMatematico:
        """NUEVO-C18: Derivada parcial con soporte completo."""
        pasos = [f"Derivada parcial de '{expresion}' respecto a '{variable}' (orden {orden})"]
        try:
            expr_norm = normalizar_expresion(expresion)
            expr = self._parsear(expr_norm)
            pasos.append(f"Expresión: {expr}")
            var = symbols(variable)
            resultado = diff(expr, var, orden)
            resultado = simplify(resultado)
            pasos.append(f"∂^{orden}f/∂{variable}^{orden} = {resultado}")
            resultado_str = _formatear_resultado(resultado)
            self._guardar_historial("DERIVADA_PARCIAL", expresion, resultado_str, True)
            return ResultadoMatematico(
                expresion_original=expresion, resultado=resultado_str,
                paso_a_paso=pasos, exitoso=True, tipo="DERIVADA_PARCIAL",
            )
        except Exception as e:
            return self._error(expresion, pasos, str(e), "DERIVADA_PARCIAL")

    # ------------------------------------------------------------------
    # INTEGRALES
    # ------------------------------------------------------------------

    def integrar(self, expresion: str, variable: str = 'x',
                 limite_inferior: Optional[float] = None,
                 limite_superior: Optional[float] = None) -> ResultadoMatematico:
        pasos = []
        try:
            expr_norm = normalizar_expresion(expresion)
            expr = self._parsear(expr_norm)
            pasos.append(f"Expresión: {expr}")
            self.ultima_expresion = expr
            var = symbols(variable)
            if limite_inferior is not None and limite_superior is not None:
                pasos.append(f"Integral definida de {limite_inferior} a {limite_superior}")
                resultado = integrate(expr, (var, limite_inferior, limite_superior))
                tipo = "INTEGRAL_DEFINIDA"
            else:
                pasos.append("Integral indefinida")
                integral = integrate(expr, var)
                pasos.append(f"Antiderivada: {integral} + C")
                resultado = integral
                tipo = "INTEGRAL_INDEFINIDA"
            resultado_final = simplify(resultado)
            resultado_str = _formatear_resultado(resultado_final)
            self._guardar_historial(tipo, expresion, resultado_str, True)
            return ResultadoMatematico(
                expresion_original=expresion, resultado=resultado_str,
                paso_a_paso=pasos, exitoso=True, tipo=tipo,
                valor_numerico=_resultado_numerico(resultado_final),
            )
        except Exception as e:
            return self._error(expresion, pasos, str(e), "INTEGRAL")

    # ------------------------------------------------------------------
    # RESOLUCIÓN DE ECUACIONES
    # ------------------------------------------------------------------

    def resolver_ecuacion(self, ecuacion: str, variable: str = 'x') -> ResultadoMatematico:
        pasos = []
        try:
            if "=" in ecuacion:
                izq, der = ecuacion.split("=", 1)
                expr = (self._parsear(normalizar_expresion(izq.strip()))
                       - self._parsear(normalizar_expresion(der.strip())))
            else:
                expr = self._parsear(normalizar_expresion(ecuacion))
            pasos.append(f"Ecuación: {expr} = 0")
            self.ultima_expresion = expr
            var = symbols(variable)
            soluciones = solve(expr, var)
            pasos.append(f"Soluciones: {soluciones}")
            # Formatear soluciones de forma legible
            if not soluciones:
                resultado_str = "Sin soluciones reales"
            elif len(soluciones) == 1:
                sol = soluciones[0]
                resultado_str = f"{variable} = {sol}"
                try:
                    val = float(sol.evalf())
                    resultado_str += f" ≈ {round(val, 6)}" if val != round(val) else ""
                except Exception:
                    pass
            else:
                partes = []
                for i, sol in enumerate(soluciones):
                    s = f"{variable}_{i+1} = {sol}"
                    try:
                        val = float(sol.evalf())
                        if val != round(val):
                            s += f" ≈ {round(val, 6)}"
                    except Exception:
                        pass
                    partes.append(s)
                resultado_str = ", ".join(partes)
            self._guardar_historial("ECUACION", ecuacion, resultado_str, True)
            return ResultadoMatematico(
                expresion_original=ecuacion, resultado=resultado_str,
                paso_a_paso=pasos, exitoso=True, tipo="ECUACION",
            )
        except Exception as e:
            return self._error(ecuacion, pasos, str(e), "ECUACION")

    def resolver_sistema(self, ecuaciones, variables: List[str] = None) -> ResultadoMatematico:
        """
        BUG-03 FIX v8.0: Valida y normaliza el tipo de 'ecuaciones'.
        Acepta: List[str], str (una sola ecuación), tuple.
        NUNCA hace crash por tipo incorrecto.
        """
        pasos = []

        # ── BUG-03 FIX: validación y normalización de tipo ───────────
        if isinstance(ecuaciones, str):
            # Recibió un str — envolver en lista
            ecuaciones = [ecuaciones]
            pasos.append("⚠ BUG-03 FIX: 'ecuaciones' era str, convertido a List[str]")
        elif isinstance(ecuaciones, tuple):
            ecuaciones = list(ecuaciones)
            pasos.append("⚠ BUG-03 FIX: 'ecuaciones' era tuple, convertido a List")
        elif not isinstance(ecuaciones, list):
            msg = (f"Error de tipo: 'ecuaciones' debe ser List[str], "
                   f"recibí {type(ecuaciones).__name__}. "
                   f"Ejemplo correcto: ['x + y = 5', 'x - y = 1']")
            return self._error(str(ecuaciones), pasos, msg, "SISTEMA")

        # Verificar que los elementos sean strings
        ecuaciones_limpias = []
        for i, ec in enumerate(ecuaciones):
            if isinstance(ec, str):
                ecuaciones_limpias.append(ec)
            else:
                try:
                    ecuaciones_limpias.append(str(ec))
                    pasos.append(f"⚠ BUG-03 FIX: ecuación {i} era {type(ec).__name__}, convertida a str")
                except Exception:
                    return self._error(str(ecuaciones), pasos,
                        f"No pude convertir la ecuación {i} a texto.", "SISTEMA")
        ecuaciones = ecuaciones_limpias
        # ─────────────────────────────────────────────────────────────

        pasos.insert(0, f"Sistema de {len(ecuaciones)} ecuaciones")
        try:
            if variables is None:
                # FIX-R10: detectar variables automaticamente desde las ecuaciones
                # Buscar todas las letras simples que aparecen en las ecuaciones
                _vars_detectadas = []
                _palabras_clave = {'e', 'i', 'o', 'pi'}
                for _ec in ecuaciones:
                    for _v in re.findall(r'(?<![a-zA-Z])([a-z])(?![a-zA-Z])', _ec):
                        if _v not in _palabras_clave and _v not in _vars_detectadas:
                            _vars_detectadas.append(_v)
                if len(_vars_detectadas) >= len(ecuaciones):
                    variables = _vars_detectadas[:len(ecuaciones)]
                elif _vars_detectadas:
                    variables = _vars_detectadas
                else:
                    variables = ['x', 'y', 'z', 'w'][:len(ecuaciones)]
            vars_sym = [symbols(v) for v in variables]
            eqs_sympy = []
            for ec in ecuaciones:
                if "=" in ec:
                    izq, der = ec.split("=", 1)
                    eq = Eq(self._parsear(normalizar_expresion(izq.strip())),
                            self._parsear(normalizar_expresion(der.strip())))
                else:
                    eq = Eq(self._parsear(normalizar_expresion(ec)), 0)
                eqs_sympy.append(eq)
                pasos.append(f"  {eq}")

            soluciones = solve(eqs_sympy, vars_sym)
            pasos.append(f"Soluciones: {soluciones}")

            if not soluciones:
                resultado_str = "Sin solución única (sistema incompatible o dependiente)"
            elif isinstance(soluciones, dict):
                partes = [f"{k} = {v}" for k, v in soluciones.items()]
                resultado_str = ", ".join(partes)
            elif isinstance(soluciones, list):
                if not soluciones:
                    resultado_str = "Sin solución"
                elif isinstance(soluciones[0], tuple):
                    partes = []
                    for sol in soluciones:
                        p = ", ".join(f"{v} = {s}" for v, s in zip(variables, sol))
                        partes.append(f"({p})")
                    resultado_str = " | ".join(partes)
                else:
                    resultado_str = str(soluciones)
            else:
                resultado_str = _formatear_resultado(soluciones)

            self._guardar_historial("SISTEMA", str(ecuaciones), resultado_str, True)
            return ResultadoMatematico(
                expresion_original=str(ecuaciones), resultado=resultado_str,
                paso_a_paso=pasos, exitoso=True, tipo="SISTEMA",
            )
        except Exception as e:
            return self._error(str(ecuaciones), pasos, str(e), "SISTEMA")

    # ------------------------------------------------------------------
    # SIMPLIFICACIÓN
    # ------------------------------------------------------------------

    def simplificar(self, expresion: str) -> ResultadoMatematico:
        pasos = []
        try:
            expr_norm = normalizar_expresion(expresion)
            expr = self._parsear(expr_norm)
            pasos.append(f"Original: {expr}")
            self.ultima_expresion = expr
            candidatos = {}
            for nombre, fn in [('simplify', simplify), ('trigsimp', trigsimp), ('cancel', cancel)]:
                try:
                    candidatos[nombre] = fn(expr)
                except Exception:
                    pass
            if not candidatos:
                return self._error(expresion, pasos, "No pude simplificar la expresión.", "SIMPLIFICAR")
            mejor = min(candidatos.values(), key=lambda x: len(str(x)))
            pasos.append(f"Simplificado (mejor): {mejor}")
            resultado_str = _formatear_resultado(mejor)
            self._guardar_historial("SIMPLIFICAR", expresion, resultado_str, True)
            return ResultadoMatematico(
                expresion_original=expresion, resultado=resultado_str,
                paso_a_paso=pasos, exitoso=True, tipo="SIMPLIFICAR",
            )
        except Exception as e:
            return self._error(expresion, pasos, str(e), "SIMPLIFICAR")

    # ------------------------------------------------------------------
    # EXPANSIÓN
    # ------------------------------------------------------------------

    def expandir(self, expresion: str) -> ResultadoMatematico:
        pasos = []
        try:
            expr_norm = normalizar_expresion(expresion)
            expr = self._parsear(expr_norm)
            pasos.append(f"Original: {expr}")
            self.ultima_expresion = expr
            resultado = expand(expr)
            pasos.append(f"Expandido: {resultado}")
            resultado_str = _formatear_resultado(resultado)
            self._guardar_historial("EXPANDIR", expresion, resultado_str, True)
            return ResultadoMatematico(
                expresion_original=expresion, resultado=resultado_str,
                paso_a_paso=pasos, exitoso=True, tipo="EXPANDIR",
            )
        except Exception as e:
            return self._error(expresion, pasos, str(e), "EXPANDIR")

    # ------------------------------------------------------------------
    # FACTORIZACIÓN
    # ------------------------------------------------------------------

    def factorizar(self, expresion: str) -> ResultadoMatematico:
        pasos = []
        try:
            expr_norm = normalizar_expresion(expresion)
            expr = self._parsear(expr_norm)
            pasos.append(f"Original: {expr}")
            self.ultima_expresion = expr
            resultado = factor(expr)
            pasos.append(f"Factorizado: {resultado}")
            resultado_str = _formatear_resultado(resultado)
            self._guardar_historial("FACTORIZAR", expresion, resultado_str, True)
            return ResultadoMatematico(
                expresion_original=expresion, resultado=resultado_str,
                paso_a_paso=pasos, exitoso=True, tipo="FACTORIZAR",
            )
        except Exception as e:
            return self._error(expresion, pasos, str(e), "FACTORIZAR")

    # ------------------------------------------------------------------
    # LÍMITE
    # ------------------------------------------------------------------

    def limite(self, expresion: str, variable: str = 'x',
               punto: Union[float, str] = 0) -> ResultadoMatematico:
        pasos = []
        try:
            expr_norm = normalizar_expresion(expresion)
            expr = self._parsear(expr_norm)
            pasos.append(f"Expresión: {expr}")
            self.ultima_expresion = expr
            var = symbols(variable)
            punto_eval = sp.oo if str(punto) in ('oo', 'inf', 'infinito') else punto
            pasos.append(f"Límite cuando {variable} → {punto}")
            resultado = sp.limit(expr, var, punto_eval)
            pasos.append(f"Resultado: {resultado}")
            resultado_str = _formatear_resultado(resultado)
            self._guardar_historial("LIMITE", expresion, resultado_str, True)
            return ResultadoMatematico(
                expresion_original=expresion, resultado=resultado_str,
                paso_a_paso=pasos, exitoso=True, tipo="LIMITE",
                valor_numerico=_resultado_numerico(resultado),
            )
        except Exception as e:
            return self._error(expresion, pasos, str(e), "LIMITE")

    # ------------------------------------------------------------------
    # SERIE DE TAYLOR
    # ------------------------------------------------------------------

    def serie_taylor(self, expresion: str, variable: str = 'x',
                     punto: float = 0, orden: int = 5) -> ResultadoMatematico:
        pasos = []
        try:
            expr_norm = normalizar_expresion(expresion)
            expr = self._parsear(expr_norm)
            pasos.append(f"Expresión: {expr}")
            self.ultima_expresion = expr
            var = symbols(variable)
            pasos.append(f"Serie de Taylor alrededor de {punto}, orden {orden}")
            serie = expr.series(var, punto, orden).removeO()
            serie_simplif = expand(serie)
            pasos.append(f"Serie: {serie_simplif}")
            resultado_str = _formatear_resultado(serie_simplif)
            self._guardar_historial("TAYLOR", expresion, resultado_str, True)
            return ResultadoMatematico(
                expresion_original=expresion, resultado=resultado_str,
                paso_a_paso=pasos, exitoso=True, tipo="TAYLOR",
            )
        except Exception as e:
            return self._error(expresion, pasos, str(e), "TAYLOR")

    # ------------------------------------------------------------------
    # EVALUACIÓN
    # ------------------------------------------------------------------

    def evaluar(self, expresion: str, valores: Dict[str, float]) -> ResultadoMatematico:
        pasos = []
        try:
            expr_norm = normalizar_expresion(expresion)
            expr = self._parsear(expr_norm)
            pasos.append(f"Expresión: {expr}")
            pasos.append(f"Valores: {valores}")
            self.ultima_expresion = expr
            subs_dict = {symbols(k): v for k, v in valores.items()}
            resultado = expr.subs(subs_dict)
            resultado_num = resultado.evalf()
            pasos.append(f"Resultado: {resultado_num}")
            resultado_str = self._formatear_numero(resultado_num)
            self._guardar_historial("EVALUAR", expresion, resultado_str, True)
            return ResultadoMatematico(
                expresion_original=expresion, resultado=resultado_str,
                paso_a_paso=pasos, exitoso=True, tipo="EVALUAR",
                valor_numerico=_resultado_numerico(resultado_num),
            )
        except Exception as e:
            return self._error(expresion, pasos, str(e), "EVALUAR")

    def evaluar_multivariable(self, expresion: str, valores: Dict[str, float]) -> ResultadoMatematico:
        """NUEVO-C19: Evalúa f(x,y,z,...) con múltiples variables."""
        return self.evaluar(expresion, valores)

    # ------------------------------------------------------------------
    # NUEVO-C17: ESTADÍSTICAS DESCRIPTIVAS COMPLETAS
    # ------------------------------------------------------------------

    def estadisticas(self, datos) -> ResultadoMatematico:
        """
        NUEVO-C17: Estadísticas descriptivas completas.
        Acepta: str "4, 7, 2, 9, 1", list [4, 7, 2, 9, 1], o tuple.
        """
        pasos = []
        datos_parsed = _parsear_lista_numeros(datos)
        if datos_parsed is None or len(datos_parsed) == 0:
            return self._error(str(datos), pasos,
                "No pude parsear la lista de números. Ejemplo: '4, 7, 2, 9, 1'", "ESTADISTICA")

        pasos.append(f"Datos: {datos_parsed}")
        pasos.append(f"N = {len(datos_parsed)}")

        try:
            stats = _estadistica_pura(datos_parsed)
            def fmt(v):
                if isinstance(v, list):
                    return str(v)
                try:
                    f = float(v)
                    return str(round(f, 6)) if f != int(f) else str(int(f))
                except Exception:
                    return str(v)

            pasos.append(f"Media: {fmt(stats['media'])}")
            pasos.append(f"Mediana: {fmt(stats['mediana'])}")
            pasos.append(f"Moda: {fmt(stats['moda'])}")
            pasos.append(f"Desviación estándar (poblacional): {fmt(stats['desviacion_poblacional'])}")
            pasos.append(f"Varianza (poblacional): {fmt(stats['varianza_poblacional'])}")
            pasos.append(f"Desviación estándar (muestral): {fmt(stats['desviacion_muestral'])}")
            pasos.append(f"Min: {fmt(stats['minimo'])}, Max: {fmt(stats['maximo'])}, Rango: {fmt(stats['rango'])}")
            pasos.append(f"Q1: {fmt(stats['q1'])}, Q2: {fmt(stats['q2'])}, Q3: {fmt(stats['q3'])}, IQR: {fmt(stats['iqr'])}")

            resultado_str = (
                f"N={stats['n']} | "
                f"Media={fmt(stats['media'])} | "
                f"Mediana={fmt(stats['mediana'])} | "
                f"Moda={fmt(stats['moda'])} | "
                f"Desv.Est={fmt(stats['desviacion_poblacional'])} | "
                f"Varianza={fmt(stats['varianza_poblacional'])} | "
                f"Min={fmt(stats['minimo'])} | Max={fmt(stats['maximo'])} | "
                f"Rango={fmt(stats['rango'])} | "
                f"Q1={fmt(stats['q1'])} | Q3={fmt(stats['q3'])} | IQR={fmt(stats['iqr'])}"
            )
            self._guardar_historial("ESTADISTICA", str(datos), resultado_str, True)
            return ResultadoMatematico(
                expresion_original=str(datos), resultado=resultado_str,
                paso_a_paso=pasos, exitoso=True, tipo="ESTADISTICA",
                valor_numerico=stats['media'],
            )
        except Exception as e:
            return self._error(str(datos), pasos, f"Error en estadísticas: {e}", "ESTADISTICA")

    # ------------------------------------------------------------------
    # NUEVO-C20: ARITMÉTICA DISCRETA
    # ------------------------------------------------------------------

    def es_primo(self, n: int) -> ResultadoMatematico:
        """NUEVO-C20: Verifica si un número es primo."""
        pasos = [f"Verificando si {n} es primo"]
        try:
            if n < 2:
                resultado = f"{n} NO es primo (los primos son ≥ 2)"
                self._guardar_historial("PRIMO", str(n), resultado, True)
                return ResultadoMatematico(expresion_original=str(n), resultado=resultado,
                    paso_a_paso=pasos, exitoso=True, tipo="PRIMO")
            if n == 2:
                resultado = f"{n} ES primo"
                return ResultadoMatematico(expresion_original=str(n), resultado=resultado,
                    paso_a_paso=pasos, exitoso=True, tipo="PRIMO")
            if n % 2 == 0:
                resultado = f"{n} NO es primo (divisible por 2)"
                return ResultadoMatematico(expresion_original=str(n), resultado=resultado,
                    paso_a_paso=pasos, exitoso=True, tipo="PRIMO")
            i = 3
            while i * i <= n:
                if n % i == 0:
                    resultado = f"{n} NO es primo (divisible por {i})"
                    return ResultadoMatematico(expresion_original=str(n), resultado=resultado,
                        paso_a_paso=pasos, exitoso=True, tipo="PRIMO")
                i += 2
            resultado = f"{n} ES primo"
            pasos.append(f"No tiene divisores hasta √{n} ≈ {math.sqrt(n):.2f}")
            self._guardar_historial("PRIMO", str(n), resultado, True)
            return ResultadoMatematico(expresion_original=str(n), resultado=resultado,
                paso_a_paso=pasos, exitoso=True, tipo="PRIMO")
        except Exception as e:
            return self._error(str(n), pasos, str(e), "PRIMO")

    def mcd(self, a: int, b: int) -> ResultadoMatematico:
        """NUEVO-C20: Máximo Común Divisor."""
        pasos = [f"MCD({a}, {b})"]
        try:
            resultado_val = math.gcd(abs(a), abs(b))
            pasos.append(f"Usando algoritmo de Euclides")
            resultado_str = f"MCD({a}, {b}) = {resultado_val}"
            self._guardar_historial("MCD", f"{a},{b}", resultado_str, True)
            return ResultadoMatematico(expresion_original=f"mcd({a},{b})", resultado=resultado_str,
                paso_a_paso=pasos, exitoso=True, tipo="MCD", valor_numerico=float(resultado_val))
        except Exception as e:
            return self._error(f"mcd({a},{b})", pasos, str(e), "MCD")

    def mcm(self, a: int, b: int) -> ResultadoMatematico:
        """NUEVO-C20: Mínimo Común Múltiplo."""
        pasos = [f"MCM({a}, {b})"]
        try:
            resultado_val = abs(a * b) // math.gcd(abs(a), abs(b))
            resultado_str = f"MCM({a}, {b}) = {resultado_val}"
            self._guardar_historial("MCM", f"{a},{b}", resultado_str, True)
            return ResultadoMatematico(expresion_original=f"mcm({a},{b})", resultado=resultado_str,
                paso_a_paso=pasos, exitoso=True, tipo="MCM", valor_numerico=float(resultado_val))
        except Exception as e:
            return self._error(f"mcm({a},{b})", pasos, str(e), "MCM")

    def combinaciones(self, n: int, r: int) -> ResultadoMatematico:
        """NUEVO-C20: C(n, r) = n! / (r! * (n-r)!)"""
        pasos = [f"C({n}, {r}) = {n}! / ({r}! × {n-r}!)"]
        try:
            resultado_val = math.comb(n, r)
            resultado_str = f"C({n},{r}) = {resultado_val}"
            pasos.append(resultado_str)
            self._guardar_historial("COMBINACIONES", f"C({n},{r})", resultado_str, True)
            return ResultadoMatematico(expresion_original=f"C({n},{r})", resultado=resultado_str,
                paso_a_paso=pasos, exitoso=True, tipo="COMBINACIONES", valor_numerico=float(resultado_val))
        except Exception as e:
            return self._error(f"C({n},{r})", pasos, str(e), "COMBINACIONES")

    def permutaciones(self, n: int, r: int) -> ResultadoMatematico:
        """NUEVO-C20: P(n, r) = n! / (n-r)!"""
        pasos = [f"P({n}, {r}) = {n}! / {n-r}!"]
        try:
            resultado_val = math.perm(n, r)
            resultado_str = f"P({n},{r}) = {resultado_val}"
            pasos.append(resultado_str)
            self._guardar_historial("PERMUTACIONES", f"P({n},{r})", resultado_str, True)
            return ResultadoMatematico(expresion_original=f"P({n},{r})", resultado=resultado_str,
                paso_a_paso=pasos, exitoso=True, tipo="PERMUTACIONES", valor_numerico=float(resultado_val))
        except Exception as e:
            return self._error(f"P({n},{r})", pasos, str(e), "PERMUTACIONES")

    # ------------------------------------------------------------------
    # NUEVO-C23: INECUACIONES
    # ------------------------------------------------------------------

    def resolver_inecuacion(self, inecuacion: str, variable: str = 'x') -> ResultadoMatematico:
        """NUEVO-C23: Resuelve inecuaciones simbolicas.
        FIX-C13: maneja correctamente resultados Or/And/Union de SymPy.
        """
        pasos = [f"Inecuacion: {inecuacion}"]
        try:
            # Normalizar la expresion primero (quitar prefijos)
            expr_norm = inecuacion.strip()
            expr_norm = re.sub(r'^resuelve[r]?\s+(?:la\s+)?inecuaci[o\u00f3]n\s+', '', expr_norm, flags=re.IGNORECASE).strip()
            expr_norm = re.sub(r'^(?:la\s+)?inecuaci[o\u00f3]n\s+', '', expr_norm, flags=re.IGNORECASE).strip()

            var = symbols(variable, real=True)
            # Detectar operador
            if '>=' in expr_norm or '\u2265' in expr_norm:
                op = '>='
                partes = re.split(r'>=|\u2265', expr_norm, 1)
            elif '<=' in expr_norm or '\u2264' in expr_norm:
                op = '<='
                partes = re.split(r'<=|\u2264', expr_norm, 1)
            elif '>' in expr_norm:
                op = '>'
                partes = expr_norm.split('>', 1)
            elif '<' in expr_norm:
                op = '<'
                partes = expr_norm.split('<', 1)
            else:
                return self._error(inecuacion, pasos, "No detecte operador de desigualdad (>, <, >=, <=).", "INECUACION")

            izq = self._parsear(normalizar_expresion(partes[0].strip()))
            der = self._parsear(normalizar_expresion(partes[1].strip()))
            expr = izq - der

            # FIX-C13b: usar la variable real de la expresion, no una nueva instancia
            # symbols('x', real=True) != symbols('x') cuando vienen de parseos distintos
            _free = expr.free_symbols
            if _free:
                # Usar el simbolo que ya esta en la expresion
                var_real = next(iter(_free))
            else:
                var_real = var

            if op == '>':
                sol = solveset(expr > 0, var_real, domain=S.Reals)
            elif op == '<':
                sol = solveset(expr < 0, var_real, domain=S.Reals)
            elif op == '>=':
                sol = solveset(expr >= 0, var_real, domain=S.Reals)
            else:
                sol = solveset(expr <= 0, var_real, domain=S.Reals)

            # FIX-C13: convertir resultado Or/And/Union a texto legible
            resultado_str = self._formatear_solucion_inecuacion(sol, variable)
            pasos.append(f"Solucion: {resultado_str}")
            self._guardar_historial("INECUACION", inecuacion, resultado_str, True)
            return ResultadoMatematico(
                expresion_original=inecuacion, resultado=resultado_str,
                paso_a_paso=pasos, exitoso=True, tipo="INECUACION",
            )
        except Exception as e:
            return self._error(inecuacion, pasos, str(e), "INECUACION")

    def _formatear_solucion_inecuacion(self, sol, variable: str = 'x') -> str:
        """FIX-C13: Convierte solucion Or/And/Union/Interval de SymPy a texto legible."""
        try:
            import sympy as _sp
            # Intervalo simple
            if isinstance(sol, _sp.Interval):
                return self._intervalo_a_texto(sol, variable)
            # Union de intervalos (Or)
            if hasattr(_sp, 'Union') and isinstance(sol, _sp.Union):
                partes = [self._intervalo_a_texto(i, variable) for i in sol.args]
                return " o ".join(partes)
            # Complement
            if hasattr(_sp, 'Complement') and isinstance(sol, _sp.Complement):
                return str(sol)
            # EmptySet
            if sol == _sp.EmptySet or sol == _sp.S.EmptySet:
                return "Sin solucion (conjunto vacio)"
            # Reales completos
            if sol == _sp.S.Reals or str(sol) == 'Reals':
                return "Todos los reales"
            # Finito (conjunto de puntos)
            if isinstance(sol, _sp.FiniteSet):
                puntos = [str(p) for p in sol]
                return f"{variable} = " + " o ".join(puntos)
            # Fallback: str()
            return str(sol)
        except Exception:
            return str(sol)

    def _intervalo_a_texto(self, intervalo, variable: str = 'x') -> str:
        """Convierte un Interval de SymPy a notacion legible."""
        try:
            import sympy as _sp
            a, b = intervalo.start, intervalo.end
            left_open = intervalo.left_open
            right_open = intervalo.right_open
            a_str = "\u221e" if a == _sp.oo or a == -_sp.oo else str(a)
            b_str = "\u221e" if b == _sp.oo or b == -_sp.oo else str(b)
            # Forma de desigualdad
            if a == -_sp.oo and b == _sp.oo:
                return "todos los reales"
            if a == -_sp.oo:
                op = "<" if right_open else "<="
                return f"{variable} {op} {b_str}"
            if b == _sp.oo:
                op = ">" if left_open else ">="
                return f"{variable} {op} {a_str}"
            op_l = "<" if left_open else "<="
            op_r = "<" if right_open else "<="
            return f"{a_str} {op_l} {variable} {op_r} {b_str}"
        except Exception:
            return str(intervalo)

    # ------------------------------------------------------------------
    # NUEVO-C24: INFO DE POLINOMIO
    # ------------------------------------------------------------------

    def polinomio_info(self, expresion: str, variable: str = 'x') -> ResultadoMatematico:
        """NUEVO-C24: Analiza un polinomio: grado, coeficientes, raíces, factores.
        FIX-POL: raíces numéricas aproximadas cuando la forma simbólica es ilegible (>20 chars).
        """
        pasos = [f"Analizando polinomio: {expresion}"]
        try:
            from sympy import nroots
            expr_norm = normalizar_expresion(expresion)
            expr = self._parsear(expr_norm)
            var = symbols(variable)
            poly = Poly(expr, var)
            grado = poly.degree()
            coefs = poly.all_coeffs()
            factorizado = factor(expr)
            pasos.append(f"Grado: {grado}")
            pasos.append(f"Coeficientes: {coefs}")

            # Raíces: exactas si son legibles, numéricas si son monstruosas
            raices_exactas = solve(expr, var)
            usa_aprox = any(len(str(r)) > 20 for r in raices_exactas)

            if usa_aprox:
                raices_num = nroots(poly, n=4, maxsteps=50)
                partes = []
                for r in raices_num:
                    re_v = float(r.as_real_imag()[0])
                    im_v = float(r.as_real_imag()[1])
                    if abs(im_v) < 1e-8:
                        partes.append(f"≈{re_v:.4g}")
                    else:
                        signo = '+' if im_v >= 0 else '-'
                        partes.append(f"≈{re_v:.4g}{signo}{abs(im_v):.4g}i")
                raices_display = ", ".join(partes)
                pasos.append(f"Raíces (numéricas): {raices_display}")
            else:
                raices_display = ", ".join(str(r) for r in raices_exactas) if raices_exactas else "sin raíces reales"
                pasos.append(f"Raíces: {raices_display}")

            pasos.append(f"Factorizado: {factorizado}")
            resultado_str = (
                f"Grado: {grado} | "
                f"Coeficientes: {coefs} | "
                f"Raíces: {raices_display} | "
                f"Factorizado: {factorizado}"
            )
            self._guardar_historial("POLINOMIO_INFO", expresion, resultado_str, True)
            return ResultadoMatematico(
                expresion_original=expresion, resultado=resultado_str,
                paso_a_paso=pasos, exitoso=True, tipo="POLINOMIO_INFO",
            )
        except Exception as e:
            return self._error(expresion, pasos, str(e), "POLINOMIO_INFO")

    # ------------------------------------------------------------------
    # HELPERS
    # ------------------------------------------------------------------

    def _formatear_numero(self, n) -> str:
        try:
            f = float(n)
            if f == int(f) and abs(f) < 1e15:
                return str(int(f))
            return f"{f:.10g}"
        except (TypeError, ValueError, OverflowError):
            return str(n)

    def _error(self, expresion: str, pasos: list, mensaje: str, tipo: str) -> ResultadoMatematico:
        self._guardar_historial(tipo, expresion, mensaje, False)
        return ResultadoMatematico(
            expresion_original=expresion, resultado="",
            paso_a_paso=pasos, exitoso=False, error=mensaje, tipo=tipo,
        )


# ═══════════════════════════════════════════════════════════════════════
# TESTS v8.0
# ═══════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    calc = CalculadoraAvanzada()
    print("=" * 60)
    print("CALCULADORA AVANZADA v8.0 — TESTS COMPLETOS")
    print("=" * 60)

    ok = fail = 0

    def test(nombre, resultado, debe_exito, contiene=None):
        global ok, fail
        bien = resultado.exitoso == debe_exito
        if contiene and bien and debe_exito:
            bien = contiene.lower() in resultado.resultado.lower()
        s = "✅" if bien else "❌"
        if bien: ok += 1
        else: fail += 1
        val = resultado.resultado if resultado.exitoso else resultado.error
        print(f"  {s} {nombre}: {val!r}")

    print("\n--- BUG-03 FIX: resolver_sistema() validación de tipo ---")
    test("sistema str (no lista)",     calc.resolver_sistema("x + y = 5"),       True)
    test("sistema tuple",               calc.resolver_sistema(("x + y = 5", "x - y = 1")), True)
    test("sistema correcto",            calc.resolver_sistema(["x + y = 5", "x - y = 1"]), True)
    test("sistema tipo inválido int",   calc.resolver_sistema(42),                False)

    print("\n--- NUEVO-C17: estadísticas ---")
    test("estadística string",  calc.estadisticas("4, 7, 2, 9, 1"),  True, "Media")
    test("estadística lista",   calc.estadisticas([4, 7, 2, 9, 1]),  True, "4.6")

    print("\n--- NUEVO-C20: aritmética discreta ---")
    test("es_primo 7",          calc.es_primo(7),      True, "ES primo")
    test("es_primo 9",          calc.es_primo(9),      True, "NO es primo")
    test("mcd(12,8)",           calc.mcd(12, 8),       True, "4")
    test("mcm(4,6)",            calc.mcm(4, 6),        True, "12")
    test("C(5,2)",              calc.combinaciones(5, 2), True, "10")
    test("P(5,2)",              calc.permutaciones(5, 2), True, "20")

    print("\n--- NUEVO-C21: calcular_automatico ---")
    test("auto derivada",    calc.calcular_automatico("deriva x**2 + 3*x"), True)
    test("auto estadística", calc.calcular_automatico("media de [4, 7, 2, 9, 1]"), True)
    test("auto básico",      calc.calcular_automatico("cuanto es 15 * 8"), True, "120")

    print("\n--- FIX-C6 preservados ---")
    test("raíz cuadrada de 144", calc.calcular_basico("raíz cuadrada de 144"), True, "12")
    test("factorial de 8",       calc.calcular_basico("factorial de 8"),       True, "40320")
    test("seno de 90 grados",    calc.calcular_basico("seno de 90 grados"),    True, "1")

    print(f"\n{'='*60}")
    print(f"RESULTADO: {ok} OK / {fail} FALLOS / {ok+fail} total")
    print(f"{'='*60}")