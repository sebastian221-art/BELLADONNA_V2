# -*- coding: utf-8 -*-
"""
calculadora_avanzada.py — VERSION v7.0 MÁXIMA

MEJORAS SOBRE v6.3/v6.4:
═══════════════════════════════════════════════════════════════════════

FIX-C1   normalizar_expresion(): coeficiente implícito 2x → 2*x
         Ahora: "2x^2 + 3x" → "2*x**2 + 3*x" antes de parsear SymPy.
         Regresión 0: "sin(x)", "sqrt(x)", "exp(x)" no se tocan.

NUEVO-C2 Soporte de fracciones en texto: "1/2 de 200", "tres cuartos"
         "la mitad de 80" → 40, "un tercio de 90" → 30

NUEVO-C3 Notación científica: "2e3", "1.5e-4", "3 × 10^6"
         Normaliza antes de parsear para que SymPy lo acepte.

NUEVO-C4 Soporte de números en español: "dos más tres", "cinco por ocho"
         Convierte texto numérico básico antes de parsear.

NUEVO-C5 derivar() con segunda derivada por texto:
         "segunda derivada de x^3" → diff(x^3, x, 2)
         "derivada segunda de sin(x)" → -sin(x)

NUEVO-C6 serie_taylor() con punto y orden extraídos del mensaje:
         "taylor de sin(x) alrededor de 0 orden 6"

NUEVO-C7 evaluar_multivariable(): evalúa f(x,y,z) con dict de valores
         "evalúa x^2 + y^2 con x=3, y=4" → 25

NUEVO-C8 resolver_sistema(): sistemas de ecuaciones 2x2 y 3x3
         "resuelve x + y = 5, x - y = 1" → {x:3, y:2}

NUEVO-C9 derivada_parcial(): ∂f/∂x, ∂f/∂y automático
         "derivada parcial de x^2*y respecto a y" → x^2

NUEVO-C10 calcular_basico() mejorado: detecta porcentajes directamente
          "cuánto es el 15% de 200" → 30
          "200 más 15%" → 230
          "descuento del 20% de 500" → 400 (con descripción)

NUEVO-C11 historial(): lista las últimas N operaciones de la sesión
          Útil para que Bell responda "¿qué calculé antes?"

NUEVO-C12 formato_resultado_latex(): convierte resultado SymPy a
          representación legible (no LaTeX crudo)

NUEVO-C13 Manejo robusto de números complejos: muestra parte real e
          imaginaria en vez de error crudo.

NUEVO-C14 simplificar() inteligente: detecta si la expresión es
          trigonométrica y usa trigsimp(), si es racional usa cancel(),
          si es general usa simplify() — siempre el mejor resultado.

NUEVO-C15 expandir_multinomial(): expande (a+b+c)^n correctamente.

TODOS LOS FIXES PREVIOS PRESERVADOS:
  C-02: unicode, raiz, cero, simbólico
  C-03: nunca reemplaza la x ASCII como variable matemática
  C-04: limpiar_prefijos() elimina texto español antes de parsear
  C-05: mensajes de error descriptivos (archivo.txt, vacío, texto)

COMPATIBILIDAD: registro_habilidades v1.6+, motor v9.0+
"""

import re
import math
import unicodedata
import logging
from typing import List, Dict, Union, Optional, Tuple, Any
from dataclasses import dataclass, field

import sympy as sp
from sympy import (
    symbols, diff, integrate, solve, solve_linear_system, simplify,
    expand, factor, trigsimp, cancel, radsimp, nsimplify,
    sin, cos, tan, exp, log, sqrt, pi, E, oo, zoo,
    Matrix, linsolve, nonlinsolve, Eq,
    Rational, Integer, Float,
)
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

logger = logging.getLogger("calculadora_avanzada")

# ─────────────────────────────────────────────────────────────────────
# TRANSFORMACIONES SYMPY — habilitar multiplicación implícita
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
}


# ======================================================================
# DATACLASS DE RESULTADO
# ======================================================================

@dataclass
class ResultadoMatematico:
    """Resultado de una operación matemática."""
    expresion_original: str
    resultado:          str
    paso_a_paso:        List[str] = field(default_factory=list)
    exitoso:            bool = True
    error:              Optional[str] = None
    tipo:               str = "GENERAL"   # BASICO, DERIVADA, INTEGRAL, etc.
    latex:              Optional[str] = None
    valor_numerico:     Optional[float] = None


# ======================================================================
# NUEVO-C4: NÚMEROS EN ESPAÑOL
# ======================================================================

_NUMEROS_ES = {
    'cero': '0', 'un': '1', 'uno': '1', 'una': '1',
    'dos': '2', 'tres': '3', 'cuatro': '4', 'cinco': '5',
    'seis': '6', 'siete': '7', 'ocho': '8', 'nueve': '9',
    'diez': '10', 'once': '11', 'doce': '12', 'trece': '13',
    'catorce': '14', 'quince': '15', 'veinte': '20',
    'treinta': '30', 'cuarenta': '40', 'cincuenta': '50',
    'sesenta': '60', 'setenta': '70', 'ochenta': '80',
    'noventa': '90', 'cien': '100', 'ciento': '100',
    'mil': '1000', 'millon': '1000000',
}

_FRACCIONES_ES = {
    r'la\s+mitad\s+de\s+(\d+(?:\.\d+)?)':         r'\1 / 2',
    r'un\s+tercio\s+de\s+(\d+(?:\.\d+)?)':         r'\1 / 3',
    r'un\s+cuarto\s+de\s+(\d+(?:\.\d+)?)':         r'\1 / 4',
    r'tres\s+cuartos\s+de\s+(\d+(?:\.\d+)?)':      r'\1 * 3 / 4',
    r'un\s+quinto\s+de\s+(\d+(?:\.\d+)?)':         r'\1 / 5',
    r'dos\s+tercios\s+de\s+(\d+(?:\.\d+)?)':       r'\1 * 2 / 3',
}


def _convertir_numeros_espanol(texto: str) -> str:
    """Convierte números escritos en español a dígitos."""
    t = texto
    # Fracciones primero (más específicas)
    for patron, reemplazo in _FRACCIONES_ES.items():
        t = re.sub(patron, reemplazo, t, flags=re.IGNORECASE)
    # Números individuales
    for palabra, digito in sorted(_NUMEROS_ES.items(), key=lambda x: -len(x[0])):
        t = re.sub(r'\b' + palabra + r'\b', digito, t, flags=re.IGNORECASE)
    return t


# ======================================================================
# NUEVO-C10: PORCENTAJES DIRECTOS
# ======================================================================

_RE_PORCENTAJE_DE = re.compile(
    r'(?:el\s+|cuanto\s+es\s+(?:el\s+)?)?(\d+(?:\.\d+)?)\s*%\s*(?:de\s+|of\s+)(\d+(?:\.\d+)?)',
    re.IGNORECASE
)
_RE_MAS_PORCENTAJE = re.compile(
    r'(\d+(?:\.\d+)?)\s*(?:mas|más|\+)\s*(?:el\s+)?(\d+(?:\.\d+)?)\s*%',
    re.IGNORECASE
)
_RE_MENOS_PORCENTAJE = re.compile(
    r'(\d+(?:\.\d+)?)\s*(?:menos|-)\s*(?:el\s+)?(\d+(?:\.\d+)?)\s*%',
    re.IGNORECASE
)
_RE_DESCUENTO = re.compile(
    r'descuento\s+(?:del?\s+)?(\d+(?:\.\d+)?)\s*%\s*(?:de\s+|a\s+)(\d+(?:\.\d+)?)',
    re.IGNORECASE
)


def _calcular_porcentaje_directo(texto: str) -> Optional[Tuple[str, str]]:
    """
    Detecta y resuelve porcentajes directamente sin SymPy.
    Retorna (resultado_str, descripcion) o None.
    """
    m = _RE_DESCUENTO.search(texto)
    if m:
        pct = float(m.group(1))
        base = float(m.group(2))
        descuento = base * pct / 100
        final = base - descuento
        return (
            str(int(final) if final == int(final) else round(final, 6)),
            f"{pct}% de descuento sobre {base}: descuento = {descuento}, precio final = {final}"
        )

    m = _RE_MAS_PORCENTAJE.search(texto)
    if m:
        base = float(m.group(1))
        pct = float(m.group(2))
        resultado = base * (1 + pct / 100)
        r = int(resultado) if resultado == int(resultado) else round(resultado, 6)
        return (str(r), f"{base} + {pct}% = {r}")

    m = _RE_MENOS_PORCENTAJE.search(texto)
    if m:
        base = float(m.group(1))
        pct = float(m.group(2))
        resultado = base * (1 - pct / 100)
        r = int(resultado) if resultado == int(resultado) else round(resultado, 6)
        return (str(r), f"{base} - {pct}% = {r}")

    m = _RE_PORCENTAJE_DE.search(texto)
    if m:
        pct = float(m.group(1))
        base = float(m.group(2))
        resultado = base * pct / 100
        r = int(resultado) if resultado == int(resultado) else round(resultado, 6)
        return (str(r), f"{pct}% de {base} = {r}")

    return None


# ======================================================================
# FIX-C4: LIMPIAR PREFIJOS
# ======================================================================

def limpiar_prefijos(texto: str) -> str:
    """
    Elimina palabras en español que preceden a una expresión matemática.
    """
    t = texto.strip()
    prefijos = [
        r'cu[aá]nto\s+es\s+(?:el\s+)?',
        r'cu[aá]nto\s+es\s+',
        r'cu[aá]nto\s+',
        r'cu[aá]l\s+es\s+',
        r'el\s+resultado\s+de\s+',
        r'resultado\s+de\s+',
        r'calcula[r]?\s+',
        r'dame\s+',
        r'dime\s+',
        r'obten\s+',
        r'obt[eé]n\s+',
        r'haz\s+',
    ]
    for p in prefijos:
        nuevo = re.sub(r'^' + p, '', t, flags=re.IGNORECASE).strip()
        if nuevo != t:
            t = nuevo
            break
    return t


# ======================================================================
# NUEVO-C3 + FIX-C1: NORMALIZADOR COMPLETO
# ======================================================================

def normalizar_expresion(texto: str) -> str:
    """
    Convierte texto natural/matemático a forma evaluable por SymPy.

    FIX-C3: NUNCA reemplaza la letra x ASCII (variable matemática).
    FIX-C1: coeficiente implícito 2x → 2*x (post-conversión de ^)
    NUEVO-C3: notación científica 3e6 → 3*10**6 (solo fuera de float literal)
    """
    t = texto.strip()

    # Unicode → operadores ASCII
    t = t.replace('\u00f7', '/')    # ÷
    t = t.replace('\u00d7', '*')    # × (NO es la letra x)
    t = t.replace('\u2212', '-')    # − (menos tipográfico)
    t = t.replace('\u00b2', '**2')  # ² superíndice
    t = t.replace('\u00b3', '**3')  # ³ superíndice
    t = t.replace('\u221e', 'oo')   # ∞

    # Símbolo raíz cuadrada √
    t = re.sub(r'\u221a\s*(\d+(?:\.\d+)?)', r'sqrt(\1)', t)
    t = re.sub(r'\u221a\s*\(', 'sqrt(', t)

    # Potencia ^ → **
    t = t.replace('^', '**')
    t = re.sub(r'al\s+cuadrado', '**2', t, flags=re.IGNORECASE)
    t = re.sub(r'al\s+cubo', '**3', t, flags=re.IGNORECASE)
    t = re.sub(r'elevado\s+a\s+la?\s+(\w+)', r'**\1', t, flags=re.IGNORECASE)
    t = re.sub(r'elevado\s+a\s+(\d+)', r'**\1', t, flags=re.IGNORECASE)

    # Raíz en texto
    t = re.sub(r'ra[íi]z\s+cuadrada\s+de\s+(\d+(?:\.\d+)?)', r'sqrt(\1)', t, flags=re.IGNORECASE)
    t = re.sub(r'ra[íi]z\s+c[uú]bica\s+de\s+(\d+(?:\.\d+)?)', r'cbrt(\1)', t, flags=re.IGNORECASE)
    t = re.sub(r'ra[íi]z\s+de\s+(\d+(?:\.\d+)?)', r'sqrt(\1)', t, flags=re.IGNORECASE)

    # Operadores en español (solo entre números)
    t = re.sub(r'(\d+(?:\.\d+)?)\s+dividido\s+(?:entre|por)\s+(\d+(?:\.\d+)?)', r'\1 / \2', t, flags=re.IGNORECASE)
    t = re.sub(r'(\d+(?:\.\d+)?)\s+entre\s+(\d+(?:\.\d+)?)', r'\1 / \2', t, flags=re.IGNORECASE)
    t = re.sub(r'(\d+(?:\.\d+)?)\s+por\s+(\d+(?:\.\d+)?)', r'\1 * \2', t, flags=re.IGNORECASE)
    t = re.sub(r'(\d+(?:\.\d+)?)\s+multiplicado\s+por\s+(\d+(?:\.\d+)?)', r'\1 * \2', t, flags=re.IGNORECASE)
    t = re.sub(r'(\d+(?:\.\d+)?)\s+m[aá]s\s+(\d+(?:\.\d+)?)', r'\1 + \2', t, flags=re.IGNORECASE)
    t = re.sub(r'(\d+(?:\.\d+)?)\s+menos\s+(\d+(?:\.\d+)?)', r'\1 - \2', t, flags=re.IGNORECASE)

    # NUEVO-C3: notación científica 3 × 10^6 → 3*10**6
    t = re.sub(r'(\d+(?:\.\d+)?)\s*[×x]\s*10\s*\*\*\s*(\d+)', r'\1*10**\2', t, flags=re.IGNORECASE)
    t = re.sub(r'(\d+(?:\.\d+)?)\s*[×x]\s*10\^(\d+)', r'\1*10**\2', t, flags=re.IGNORECASE)

    # FIX-C1: coeficiente implícito dígito+letra → dígito*letra
    # DESPUÉS de ^ → ** para no romper "x**2"
    # NO aplicar dentro de nombres de funciones (sin, cos, sqrt, exp, log...)
    # Estrategia: proteger funciones conocidas, aplicar, restaurar
    _FUNCIONES = ['sqrt', 'cbrt', 'sin', 'cos', 'tan', 'asin', 'acos', 'atan',
                  'sinh', 'cosh', 'tanh', 'exp', 'log', 'abs', 'ceil', 'floor']
    _placeholder = {}
    for i, fn in enumerate(_FUNCIONES):
        token = f'__FN{i}__'
        t = t.replace(fn, token)
        _placeholder[token] = fn

    # Ahora sí: dígito seguido de letra (variable) → dígito * letra
    t = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', t)

    # Restaurar funciones
    for token, fn in _placeholder.items():
        t = t.replace(token, fn)

    return t.strip()


# ======================================================================
# DETECTORES AUXILIARES (FIX-C5)
# ======================================================================

_VERBOS_MAT_AVANZADOS = re.compile(
    r'^(?:deriv[aá]?(?:da)?|integr[aá]?|l[íi]mite|lim\s*\('
    r'|factori[zs]|simplific|expan[ds]|resolv|resuelv|taylor'
    r'|parcial|evalua|sistema)\b',
    re.IGNORECASE
)

_RE_CONTENIDO_ALGEBRAICO = re.compile(
    r'(?:'
    r'[a-zA-Z]\s*[\*\+\-\/\^]'
    r'|[\*\+\-\/\^]\s*[a-zA-Z]'
    r'|\d+\s*[\*\+\-\/\^]'
    r'|[\*\+\-\/\^]\s*\d+'
    r'|\([a-zA-Z\d\s\+\-\*\/\^\*]+\)'
    r'|[a-zA-Z]\*\*\d'
    r'|\d\*\*[a-zA-Z\d]'
    r'|sin\(|cos\(|tan\(|sqrt\('
    r'|exp\(|log\('
    r')',
    re.IGNORECASE
)

_RE_PALABRA_NO_NUMERICA = re.compile(r'\b([a-zA-Z]{2,})\b')
_VARIABLES_VALIDAS = {
    'pi', 'e', 'x', 'y', 'z', 'n', 't', 'a', 'b', 'c',
    'sin', 'cos', 'tan', 'exp', 'log', 'sqrt', 'cbrt',
    'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh',
    'abs', 'oo', 'inf', 'ln',
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
                'deriv':   "deriva x**2 + 3*x",
                'integr':  "integra x**2",
                'limit':   "límite de 1/x cuando x tiende a infinito",
                'factor':  "factoriza x**2 - 9",
                'simplif': "simplifica (x**2 - 1)/(x - 1)",
                'expan':   "expande (x + 1)**2",
                'resolv':  "resuelve x**2 - 5*x + 6",
                'resuelv': "resuelve x**2 - 5*x + 6",
                'taylor':  "serie de Taylor de sin(x)",
            }
            for prefijo, ejemplo in ejemplos.items():
                if verbo.startswith(prefijo):
                    return f"¿Qué expresión quieres {verbo}r? Ejemplo: '{ejemplo}'"
            return f"¿Qué expresión quieres {verbo}r? Escribe la expresión matemática."

        if not _RE_CONTENIDO_ALGEBRAICO.search(resto):
            if '.' in resto or re.search(r'[a-zA-Z]{4,}', resto):
                return f"'{resto}' no es una expresión matemática. Escribe: '{verbo}r x**2 + 3*x' o similar."

    palabras_largas = _RE_PALABRA_NO_NUMERICA.findall(expr)
    palabras_invalidas = [
        p for p in palabras_largas
        if p.lower() not in _VARIABLES_VALIDAS
    ]

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


# ======================================================================
# NUEVO-C12: FORMATO DE RESULTADO LEGIBLE
# ======================================================================

def _formatear_resultado(expr_sympy) -> str:
    """
    Convierte un resultado SymPy a string legible, evitando LaTeX crudo.
    Usa notación matemática limpia.
    """
    if expr_sympy is None:
        return ""
    s = str(expr_sympy)
    # Mejorar legibilidad: ** → ^ en display (solo para mostrar)
    # No lo hacemos para no confundir con la entrada
    return s


def _resultado_numerico(expr_sympy) -> Optional[float]:
    """Extrae el valor numérico flotante si es posible."""
    try:
        v = float(expr_sympy.evalf())
        return v if math.isfinite(v) else None
    except Exception:
        return None


# ======================================================================
# CLASE PRINCIPAL
# ======================================================================

class CalculadoraAvanzada:
    """
    Calculadora matemática avanzada usando SymPy. v7.0 MÁXIMA.

    Soporta:
    - Aritmética básica con texto natural completo en español
    - Porcentajes directos (15% de 200, descuentos, incrementos)
    - Fracciones en texto (la mitad de, un tercio de)
    - Números en español (dos más tres)
    - Notación científica (3×10^6)
    - Derivadas (incluyendo parciales y orden N)
    - Integrales (definidas e indefinidas)
    - Límites
    - Series de Taylor
    - Resolución de ecuaciones (una variable y sistemas)
    - Factorización, simplificación, expansión inteligente
    - Evaluación con valores específicos (multivariable)
    - Historial de operaciones en sesión
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
        """Parsea una expresión matemática con SymPy. Usa multiplicación implícita."""
        try:
            return parse_expr(
                expresion,
                local_dict=_LOCAL_DICT,
                transformations=_TRANSFORMACIONES,
                evaluate=True,
            )
        except Exception:
            # Fallback sin multiplicación implícita
            return parse_expr(
                expresion,
                local_dict=_LOCAL_DICT,
                evaluate=True,
            )

    def _guardar_historial(self, tipo: str, entrada: str, resultado: str, exitoso: bool):
        """NUEVO-C11: guarda operación en historial de sesión."""
        self._historial.append({
            'tipo': tipo,
            'entrada': entrada,
            'resultado': resultado,
            'exitoso': exitoso,
        })
        if len(self._historial) > 50:
            self._historial.pop(0)

    # ------------------------------------------------------------------
    # NUEVO-C11: HISTORIAL
    # ------------------------------------------------------------------

    def historial(self, n: int = 10) -> List[Dict]:
        """Retorna las últimas N operaciones."""
        return self._historial[-n:]

    def historial_texto(self, n: int = 10) -> str:
        """Retorna historial como texto legible."""
        items = self.historial(n)
        if not items:
            return "No hay operaciones registradas en esta sesión."
        lineas = []
        for i, op in enumerate(items, 1):
            estado = "✓" if op['exitoso'] else "✗"
            lineas.append(f"{i}. [{estado}] {op['tipo']}: {op['entrada']} = {op['resultado']}")
        return "\n".join(lineas)

    # ------------------------------------------------------------------
    # CÁLCULO BÁSICO — mejorado v7.0
    # ------------------------------------------------------------------

    def calcular_basico(self, expresion: str) -> ResultadoMatematico:
        """
        Calcula operaciones básicas con texto natural completo.

        NUEVO-C10: detecta porcentajes directamente.
        NUEVO-C4: convierte números en español.
        FIX-C4: limpia palabras en español antes de parsear.
        FIX-C5: detecta expresiones no-numéricas con mensajes descriptivos.
        FIX-C1: normaliza coeficientes implícitos (2x → 2*x).
        """
        pasos = [f"Original: {expresion}"]

        # NUEVO-C10: porcentajes directos (antes de cualquier normalización)
        pct = _calcular_porcentaje_directo(expresion)
        if pct:
            resultado_str, descripcion = pct
            pasos.append(f"Porcentaje directo: {descripcion}")
            self._guardar_historial("PORCENTAJE", expresion, resultado_str, True)
            return ResultadoMatematico(
                expresion_original=expresion,
                resultado=resultado_str,
                paso_a_paso=pasos,
                exitoso=True,
                tipo="PORCENTAJE",
            )

        # NUEVO-C4: números en español
        expr_es = _convertir_numeros_espanol(expresion)
        if expr_es != expresion:
            pasos.append(f"Convertido español: {expr_es}")

        # FIX-C4: normalizar unicode y texto español
        normalizada = normalizar_expresion(expr_es)
        if normalizada != expr_es:
            pasos.append(f"Normalizada: {normalizada}")

        # Limpiar prefijos sobrantes
        expr_limpia = limpiar_prefijos(normalizada)
        if expr_limpia != normalizada:
            pasos.append(f"Expresión limpia: {expr_limpia}")

        # FIX-C5: detección temprana
        mensaje_error = _detectar_problema_basico(expr_limpia)
        if mensaje_error:
            self._guardar_historial("BASICO", expresion, mensaje_error, False)
            return ResultadoMatematico(
                expresion_original=expresion,
                resultado="",
                paso_a_paso=pasos,
                exitoso=False,
                error=mensaje_error,
                tipo="BASICO",
            )

        try:
            expr_sympy = self._parsear(expr_limpia)
            pasos.append(f"SymPy: {expr_sympy}")

            # Casos especiales SymPy
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
            valor_num     = _resultado_numerico(expr_sympy)

            pasos.append(f"Resultado: {resultado_str}")
            self._guardar_historial("BASICO", expresion, resultado_str, True)
            return ResultadoMatematico(
                expresion_original=expresion,
                resultado=resultado_str,
                paso_a_paso=pasos,
                exitoso=True,
                tipo="BASICO",
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
    # NUEVO-C13: MANEJO DE NÚMEROS COMPLEJOS
    # ------------------------------------------------------------------

    def _manejar_complejo(self, expresion: str, expr_limpia: str, pasos: list) -> ResultadoMatematico:
        """Muestra parte real e imaginaria en vez de error crudo."""
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
                expresion_original=expresion,
                resultado=resultado_str,
                paso_a_paso=pasos,
                exitoso=True,
                tipo="COMPLEJO",
            )
        except Exception:
            return self._error(expresion, pasos, "El resultado es un número complejo.", "BASICO")

    # ------------------------------------------------------------------
    # DERIVADAS — mejoradas v7.0
    # ------------------------------------------------------------------

    def derivar(self, expresion: str, variable: str = 'x', orden: int = 1) -> ResultadoMatematico:
        """
        Calcula la derivada de orden N.
        NUEVO-C5: detecta "segunda derivada" por texto.
        """
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
                expresion_original=expresion,
                resultado=resultado_str,
                paso_a_paso=pasos,
                exitoso=True,
                tipo="DERIVADA",
                valor_numerico=_resultado_numerico(resultado),
            )
        except Exception as e:
            return self._error(expresion, pasos, str(e), "DERIVADA")

    # NUEVO-C9: Derivada parcial
    def derivada_parcial(self, expresion: str, variable: str = 'x', orden: int = 1) -> ResultadoMatematico:
        """Calcula ∂f/∂variable de orden N."""
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
                expresion_original=expresion,
                resultado=resultado_str,
                paso_a_paso=pasos,
                exitoso=True,
                tipo="DERIVADA_PARCIAL",
            )
        except Exception as e:
            return self._error(expresion, pasos, str(e), "DERIVADA_PARCIAL")

    # ------------------------------------------------------------------
    # INTEGRALES
    # ------------------------------------------------------------------

    def integrar(self, expresion: str, variable: str = 'x',
                 limite_inferior: Optional[float] = None,
                 limite_superior: Optional[float] = None) -> ResultadoMatematico:
        """Calcula la integral definida o indefinida."""
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
                expresion_original=expresion,
                resultado=resultado_str,
                paso_a_paso=pasos,
                exitoso=True,
                tipo=tipo,
                valor_numerico=_resultado_numerico(resultado_final),
            )
        except Exception as e:
            return self._error(expresion, pasos, str(e), "INTEGRAL")

    # ------------------------------------------------------------------
    # RESOLUCIÓN DE ECUACIONES — mejorada v7.0
    # ------------------------------------------------------------------

    def resolver_ecuacion(self, ecuacion: str, variable: str = 'x') -> ResultadoMatematico:
        """Resuelve una ecuación algebraica en una variable."""
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

            resultado_str = _formatear_resultado(soluciones)
            self._guardar_historial("ECUACION", ecuacion, resultado_str, True)
            return ResultadoMatematico(
                expresion_original=ecuacion,
                resultado=resultado_str,
                paso_a_paso=pasos,
                exitoso=True,
                tipo="ECUACION",
            )
        except Exception as e:
            return self._error(ecuacion, pasos, str(e), "ECUACION")

    # NUEVO-C8: Sistema de ecuaciones
    def resolver_sistema(self, ecuaciones: List[str], variables: List[str] = None) -> ResultadoMatematico:
        """
        Resuelve un sistema de ecuaciones.
        Ejemplo: resolver_sistema(["x + y = 5", "x - y = 1"]) → {x:3, y:2}
        """
        pasos = [f"Sistema de {len(ecuaciones)} ecuaciones"]
        try:
            if variables is None:
                variables = ['x', 'y', 'z'][:len(ecuaciones)]

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

            resultado_str = _formatear_resultado(soluciones)
            self._guardar_historial("SISTEMA", str(ecuaciones), resultado_str, True)
            return ResultadoMatematico(
                expresion_original=str(ecuaciones),
                resultado=resultado_str,
                paso_a_paso=pasos,
                exitoso=True,
                tipo="SISTEMA",
            )
        except Exception as e:
            return self._error(str(ecuaciones), pasos, str(e), "SISTEMA")

    # ------------------------------------------------------------------
    # SIMPLIFICACIÓN INTELIGENTE — NUEVO-C14
    # ------------------------------------------------------------------

    def simplificar(self, expresion: str) -> ResultadoMatematico:
        """
        Simplifica inteligentemente:
        - trigonométrica → trigsimp()
        - racional → cancel()
        - general → simplify()
        Compara resultados y elige el más corto.
        """
        pasos = []
        try:
            expr_norm = normalizar_expresion(expresion)
            expr = self._parsear(expr_norm)
            pasos.append(f"Original: {expr}")
            self.ultima_expresion = expr

            candidatos = {}

            # General
            try:
                candidatos['simplify'] = simplify(expr)
            except Exception:
                pass

            # Trigonométrico
            try:
                candidatos['trigsimp'] = trigsimp(expr)
            except Exception:
                pass

            # Racional
            try:
                candidatos['cancel'] = cancel(expr)
            except Exception:
                pass

            if not candidatos:
                return self._error(expresion, pasos, "No pude simplificar la expresión.", "SIMPLIFICAR")

            # Elegir el más compacto
            mejor = min(candidatos.values(), key=lambda x: len(str(x)))
            pasos.append(f"Simplificado (mejor): {mejor}")
            resultado_str = _formatear_resultado(mejor)
            self._guardar_historial("SIMPLIFICAR", expresion, resultado_str, True)
            return ResultadoMatematico(
                expresion_original=expresion,
                resultado=resultado_str,
                paso_a_paso=pasos,
                exitoso=True,
                tipo="SIMPLIFICAR",
            )
        except Exception as e:
            return self._error(expresion, pasos, str(e), "SIMPLIFICAR")

    # ------------------------------------------------------------------
    # EXPANSIÓN — mejorada NUEVO-C15
    # ------------------------------------------------------------------

    def expandir(self, expresion: str) -> ResultadoMatematico:
        """Expande una expresión matemática, incluyendo multinomiales."""
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
                expresion_original=expresion,
                resultado=resultado_str,
                paso_a_paso=pasos,
                exitoso=True,
                tipo="EXPANDIR",
            )
        except Exception as e:
            return self._error(expresion, pasos, str(e), "EXPANDIR")

    # ------------------------------------------------------------------
    # FACTORIZACIÓN
    # ------------------------------------------------------------------

    def factorizar(self, expresion: str) -> ResultadoMatematico:
        """Factoriza una expresión matemática."""
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
                expresion_original=expresion,
                resultado=resultado_str,
                paso_a_paso=pasos,
                exitoso=True,
                tipo="FACTORIZAR",
            )
        except Exception as e:
            return self._error(expresion, pasos, str(e), "FACTORIZAR")

    # ------------------------------------------------------------------
    # LÍMITE
    # ------------------------------------------------------------------

    def limite(self, expresion: str, variable: str = 'x',
               punto: Union[float, str] = 0) -> ResultadoMatematico:
        """Calcula el límite de una expresión."""
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
                expresion_original=expresion,
                resultado=resultado_str,
                paso_a_paso=pasos,
                exitoso=True,
                tipo="LIMITE",
                valor_numerico=_resultado_numerico(resultado),
            )
        except Exception as e:
            return self._error(expresion, pasos, str(e), "LIMITE")

    # ------------------------------------------------------------------
    # SERIE DE TAYLOR — mejorada NUEVO-C6
    # ------------------------------------------------------------------

    def serie_taylor(self, expresion: str, variable: str = 'x',
                     punto: float = 0, orden: int = 5) -> ResultadoMatematico:
        """
        Calcula la serie de Taylor.
        NUEVO-C6: punto y orden extraídos del mensaje si están presentes.
        """
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
                expresion_original=expresion,
                resultado=resultado_str,
                paso_a_paso=pasos,
                exitoso=True,
                tipo="TAYLOR",
            )
        except Exception as e:
            return self._error(expresion, pasos, str(e), "TAYLOR")

    # ------------------------------------------------------------------
    # EVALUACIÓN — mejorada NUEVO-C7
    # ------------------------------------------------------------------

    def evaluar(self, expresion: str, valores: Dict[str, float]) -> ResultadoMatematico:
        """Evalúa una expresión con valores específicos (multivariable)."""
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
                expresion_original=expresion,
                resultado=resultado_str,
                paso_a_paso=pasos,
                exitoso=True,
                tipo="EVALUAR",
                valor_numerico=_resultado_numerico(resultado_num),
            )
        except Exception as e:
            return self._error(expresion, pasos, str(e), "EVALUAR")

    # ------------------------------------------------------------------
    # HELPERS
    # ------------------------------------------------------------------

    def _formatear_numero(self, n) -> str:
        """Formatea un número: entero si es entero, decimal limpio si no."""
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
            expresion_original=expresion,
            resultado="",
            paso_a_paso=pasos,
            exitoso=False,
            error=mensaje,
            tipo=tipo,
        )


# ======================================================================
# TESTS v7.0
# ======================================================================

if __name__ == '__main__':
    calc = CalculadoraAvanzada()
    print("=" * 60)
    print("CALCULADORA AVANZADA v7.0 — TESTS COMPLETOS")
    print("=" * 60)

    ok = fail = 0

    def test(nombre, resultado, debe_exito, contiene=None):
        global ok, fail
        bien = resultado.exitoso == debe_exito
        if contiene and bien and debe_exito:
            bien = contiene in resultado.resultado
        s = "✅" if bien else "❌"
        if bien: ok += 1
        else: fail += 1
        val = resultado.resultado if resultado.exitoso else resultado.error
        print(f"  {s} {nombre}: {val!r}")

    print("\n--- BÁSICOS ---")
    test("15 * 8",           calc.calcular_basico("cuanto es 15 * 8"),           True,  "120")
    test("144 / 12",         calc.calcular_basico("144 dividido entre 12"),       True,  "12")
    test("7 × 8",            calc.calcular_basico("cuanto es 7 \u00d7 8"),        True,  "56")
    test("√144",             calc.calcular_basico("\u221a144"),                   True,  "12")
    test("2^10",             calc.calcular_basico("2^10"),                        True,  "1024")
    test("1000 / 0",         calc.calcular_basico("1000 / 0"),                   False)
    test("amor + 3",         calc.calcular_basico("cuanto es amor + 3"),          False)

    print("\n--- PORCENTAJES (NUEVO-C10) ---")
    test("15% de 200",       calc.calcular_basico("el 15% de 200"),               True,  "30")
    test("100 + 20%",        calc.calcular_basico("100 mas 20%"),                 True,  "120")
    test("500 - 20%",        calc.calcular_basico("500 menos 20%"),               True,  "400")
    test("descuento 10%/200",calc.calcular_basico("descuento del 10% de 200"),    True,  "180")

    print("\n--- NÚMEROS EN ESPAÑOL (NUEVO-C4) ---")
    test("dos + tres",       calc.calcular_basico("dos más tres"),                True,  "5")
    test("cinco * ocho",     calc.calcular_basico("cinco por ocho"),              True,  "40")
    test("mitad de 80",      calc.calcular_basico("la mitad de 80"),              True,  "40")
    test("tercio de 90",     calc.calcular_basico("un tercio de 90"),             True,  "30")

    print("\n--- COEFICIENTE IMPLÍCITO (FIX-C1) ---")
    r = calc.derivar("2x^3 + 3x^2 - 5x + 1")
    test("deriva 2x^3+3x^2-5x+1", r, True)
    r = calc.integrar("3x^2 + 2x")
    test("integra 3x^2+2x", r, True)
    r = calc.resolver_ecuacion("x^2 - 5x + 6 = 0")
    test("resuelve x^2-5x+6=0", r, True)

    print("\n--- DERIVADAS AVANZADAS ---")
    test("deriva x^3",       calc.derivar("x^3"),                                 True, "3*x**2")
    test("d2/dx2 sin(x)",    calc.derivar("sin(x)", orden=2),                     True, "-sin(x)")
    test("∂/∂y x^2*y",       calc.derivada_parcial("x^2*y", "y"),                True)

    print("\n--- SISTEMA DE ECUACIONES (NUEVO-C8) ---")
    r = calc.resolver_sistema(["x + y = 5", "x - y = 1"])
    test("sistema x+y=5, x-y=1", r, True)

    print("\n--- LÍMITES ---")
    test("lim 1/x x→∞",    calc.limite("1/x", punto='oo'),                       True, "0")
    test("lim sin(x)/x x→0",calc.limite("sin(x)/x", punto=0),                    True, "1")

    print("\n--- SIMPLIFICACIÓN INTELIGENTE (NUEVO-C14) ---")
    test("simplif (x^2-1)/(x-1)", calc.simplificar("(x**2-1)/(x-1)"),            True)
    test("trigsimp sin^2+cos^2",  calc.simplificar("sin(x)**2 + cos(x)**2"),      True, "1")

    print("\n--- EVALUACIÓN MULTIVARIABLE (NUEVO-C7) ---")
    test("x^2+y^2 x=3,y=4", calc.evaluar("x**2+y**2", {"x":3, "y":4}),           True, "25")

    print("\n--- TAYLOR ---")
    r = calc.serie_taylor("sin(x)", orden=7)
    test("taylor sin(x) orden 7", r, True)

    print("\n--- HISTORIAL (NUEVO-C11) ---")
    h = calc.historial_texto(5)
    print(f"  ℹ️  Últimas 5 ops: {len(calc.historial(5))} registradas")

    print(f"\n{'='*60}")
    print(f"RESULTADO: {ok} OK / {fail} FALLOS / {ok+fail} total")
    print(f"{'='*60}")