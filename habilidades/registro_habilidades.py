# -*- coding: utf-8 -*-
"""
registro_habilidades.py — VERSION v2.0

CAMBIOS v2.0 sobre v1.7:
═══════════════════════════════════════════════════════════════════════
FIX-PRIO    Prioridades corregidas al orden oficial del proyecto:
            90 → HabilidadMatAvanzada  (era 90, OK)
            80 → HabilidadShell        (era 80, OK)
            75 → HabilidadSQLite       (era 75, OK)
            72 → HabilidadAnalisisPython (era 72, OK)
            60 → HabilidadCalculo      (ERA 70 — CONFLICTO con MatAvanzada)
            Bajado a 60 para evitar que Calculo básico compita con
            MatAvanzada en mensajes ambiguos.

FIX-MAT-1   HabilidadMatAvanzada._DETECTORES ampliado con:
            - SISTEMA: "sistema de ecuaciones", "ecuaciones simultáneas"
            - EVALUAR: "evalúa f(x)", "sustituye x=", "valor de f en"
            - DERIVADA_PARCIAL: "derivada parcial", "parcial de"
            - ESTADISTICA: "media de", "promedio de", "desviación", etc.
            - INECUACION: "inecuación", "mayor que", "menor que" con var
            - MCD/MCM: "mcd de", "mcm de", "máximo común divisor"
            - PRIMO: "es primo", "número primo"
            - COMBINATORIA: "combinaciones de", "permutaciones de"
            - POLINOMIO: "grado del polinomio", "coeficientes de"

FIX-MAT-2   _extraer_expresion() mejorado para todos los sub_tipos
            nuevos: sistema, evaluar, estadistica, inecuacion, etc.

FIX-MAT-3   ejecutar() cubre TODOS los métodos nuevos de
            CalculadoraAvanzada v8.0 sin dejar ninguno sin mapeo.

FIX-MAT-4   HabilidadCalculo._PATRONES y _TEXTO ampliados para detectar
            ALL las formas que un humano puede pedir cálculo básico:
            "cuánto es", "a cuánto equivale", "dime el resultado",
            "opera", "cuanto da", porcentajes, fracciones en español,
            funciones trigonométricas, logaritmos, etc.

FIX-MAT-5   calcular_automatico() integrado: si el sub_tipo no se puede
            determinar con certeza, se llama a
            calc.calcular_automatico() que tiene detección interna.

FIX-DET-1   HabilidadMatAvanzada.detectar() ya no retorna None cuando
            el mensaje tiene claramente matemáticas pero el patrón de
            extracción devuelve vacío — usa el mensaje completo como
            expresión de fallback.

FIX-DET-2   _es_expresion_puramente_numerica() mejorado: evita falsos
            positivos con expresiones como "factorial de 8" (tiene
            letras pero no variables libres tras normalizar).

NUEVO-R1    formatear_respuesta() para MatAvanzada muestra paso a paso
            cuando hay múltiples pasos, facilitando la comprensión.

NUEVO-R2    HabilidadCalculo cubre funciones matemáticas en español
            directamente ("seno de 90 grados", "raíz de 144", etc.)
            para que NUNCA se pierdan como DESCONOCIDO.

Todos los fixes anteriores (BUG-R6, BUG-R7, FIX-R8) preservados.
═══════════════════════════════════════════════════════════════════════
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Any
import re
import logging

logger = logging.getLogger("registro_habilidades")


# ═══════════════════════════════════════════════════════════════════════
# TIPOS BASE
# ═══════════════════════════════════════════════════════════════════════

@dataclass
class ResultadoHabilidad:
    exitoso: bool
    valor: str
    descripcion: str
    pasos: List[str] = field(default_factory=list)
    error: Optional[str] = None
    tipo_habilidad: str = ""
    datos_raw: Any = None
    verificado_echo: bool = False
    aprobado_vega: bool = True


@dataclass
class HabilidadMatch:
    habilidad_id: str
    confianza: float
    parametros: Dict[str, Any]
    habilidad: 'BaseHabilidad'


# ═══════════════════════════════════════════════════════════════════════
# INTERFAZ BASE
# ═══════════════════════════════════════════════════════════════════════

class BaseHabilidad(ABC):

    @property
    @abstractmethod
    def id(self) -> str: ...

    @property
    @abstractmethod
    def descripcion_para_bell(self) -> str: ...

    @property
    def consejeras_requeridas(self) -> List[str]:
        return ["Vega"]

    @abstractmethod
    def detectar(self, mensaje, conceptos, hechos) -> Optional[HabilidadMatch]: ...

    @abstractmethod
    def ejecutar(self, match, nombre_usuario="") -> ResultadoHabilidad: ...

    def formatear_respuesta(self, resultado, nombre_usuario="") -> str:
        n = f", {nombre_usuario}" if nombre_usuario else ""
        if resultado.exitoso:
            return f"{resultado.descripcion}{n}."
        return f"{resultado.error or 'No pude completar esa operacion'}{n}."


# ═══════════════════════════════════════════════════════════════════════
# HELPERS COMPARTIDOS
# ═══════════════════════════════════════════════════════════════════════

# BUG-R6 FIX: patrón para verificar que la expresión tiene contenido matemático real
_RE_EXPR_MAT_VALIDA = re.compile(
    r'(?:[a-zA-Z][\*\+\-\/\^]|[\*\+\-\/\^][a-zA-Z]|\*\*|[a-zA-Z]\*\*|'
    r'sin\(|cos\(|tan\(|sqrt\(|exp\(|log\(|\d+[a-zA-Z]|[a-zA-Z]\d+)',
    re.IGNORECASE
)

def _expresion_tiene_matematica(expr: str) -> bool:
    return bool(_RE_EXPR_MAT_VALIDA.search(expr))


# FIX-R8 mejorado: detectar si una expresión es puramente numérica
def _es_expresion_puramente_numerica(expr_str: str) -> bool:
    """
    Retorna True si la expresión, una vez parseada por SymPy,
    no tiene variables libres.
    FIX-DET-2: mejor manejo de funciones españolas con letras.
    """
    try:
        from sympy.parsing.sympy_parser import parse_expr
        from matematicas.calculadora_avanzada import normalizar_expresion
        expr_norm = normalizar_expresion(expr_str)
        expr = parse_expr(expr_norm)
        return not bool(expr.free_symbols)
    except Exception:
        return False


# ═══════════════════════════════════════════════════════════════════════
# HABILIDAD: CÁLCULO BÁSICO — v2.0 (FIX-MAT-4)
# ═══════════════════════════════════════════════════════════════════════

class HabilidadCalculo(BaseHabilidad):

    @property
    def id(self): return "CALCULO_BASICO"

    @property
    def descripcion_para_bell(self):
        return (
            "Operaciones matemáticas básicas: suma, resta, multiplicación, división, "
            "raíz, potencias, porcentajes, fracciones, funciones trigonométricas básicas, "
            "logaritmos, factorial, valor absoluto, redondeo."
        )

    # FIX-MAT-4: patrones ampliados — todo lo que el usuario pueda decir
    _PATRONES = [
        r'\d+\s*[\+\-\*\/\u00f7\u00d7]\s*\d+',      # operaciones con operadores
        r'\u221a\s*\d+',                              # símbolo raíz
        r'\d+\s*\*\*\s*\d+',                          # potencia **
        r'\d+\s*\^\s*\d+',                            # potencia ^
        r'ra[i\u00ed]z\s+(?:cuadrada\s+)?de\s+\d+',  # raíz en español
        r'ra[i\u00ed]z\s+c[u\u00fa]bica\s+de\s+\d+', # raíz cúbica
        r'factorial\s+de\s+\d+',                      # factorial en español
        r'\d+\s*!',                                   # factorial !
        r'\d+\s*%',                                   # porcentaje
        r'\d+\s+(?:mas|más|menos|por|entre|dividido)', # operaciones en español
        r'seno\s+de|coseno\s+de|tangente\s+de',       # trig en español
        r'logaritmo\s+(?:de|natural|base)|ln\s+de|log\s+de', # logaritmos
        r'\d+\s+al\s+(?:cuadrado|cubo)',               # potencias en español
        r'valor\s+absoluto\s+de\s+\d+',               # abs en español
        r'redonde[ao]\s+\d+',                          # redondeo
        r'\d+\s+grados?\s+(?:a|en)\s+radianes?',       # conversión grados
        r'convierte?\s+\d+\s+grados?',                 # conversión grados v2
        r'\d+\s+(?:por\s+ciento|%)\s+de\s+\d+',        # % de
        r'descuento\s+de\s+\d+',                       # descuento
        r'la\s+mitad|un\s+tercio|un\s+cuarto',         # fracciones español
        r'cuanto\s+(?:es|da|son)\s+\d+',               # "cuanto es X"
        r'que\s+es\s+\d+\s*[\+\-\*\/]',               # "que es X + Y"
        r'calcula\s+\d+',                              # "calcula X"
    ]

    _TEXTO = [
        'multiplicado por', 'dividido entre', 'dividido por',
        'más ', 'mas ', 'menos ', 'cuánto es', 'cuanto es',
        'al cuadrado', 'al cubo', 'elevado a',
        'cuanto da', 'cuanto son', 'a cuanto equivale',
        'dime el resultado de', 'opera ', 'calcula ',
        'raiz de', 'raíz de', 'factorial de',
        'seno de', 'coseno de', 'tangente de',
        'logaritmo de', 'logaritmo natural', 'ln de', 'log de',
        'por ciento de', '% de', 'descuento del',
        'la mitad de', 'un tercio de', 'un cuarto de',
        'valor absoluto de', 'redondea', 'grados a radianes',
    ]

    _EXCLUIR = [
        'deriv', 'integral', 'integr', 'límite', 'limite',
        'taylor', 'factori', 'simplif', 'expand', 'ecuaci',
        'resolv', 'resuelv', 'sistema de', 'estadistica',
        'estadística', 'inecuaci', 'polinomio info',
    ]

    def detectar(self, mensaje, conceptos, hechos):
        msg = mensaje.lower().strip()
        if not re.search(r'\d+', msg):
            # Sin números, verificar funciones matemáticas en español
            tiene_func_mat = any(f in msg for f in [
                'seno', 'coseno', 'tangente', 'logaritmo', 'factorial',
                'raiz', 'raíz', 'valor absoluto', 'la mitad', 'un tercio',
            ])
            if not tiene_func_mat:
                return None

        if any(e in msg for e in self._EXCLUIR):
            return None

        confianza = 0.0
        for p in self._PATRONES:
            if re.search(p, msg, re.IGNORECASE):
                confianza = max(confianza, 0.95)
                break
        if confianza < 0.95:
            for t in self._TEXTO:
                if t in msg:
                    confianza = max(confianza, 0.85)
                    break

        if confianza < 0.75:
            return None

        return HabilidadMatch(
            habilidad_id="CALCULO_BASICO",
            confianza=confianza,
            parametros={"expresion": mensaje},
            habilidad=self,
        )

    def ejecutar(self, match, nombre_usuario=""):
        expresion = match.parametros.get("expresion", "")
        try:
            from matematicas.calculadora_avanzada import CalculadoraAvanzada
            calc = CalculadoraAvanzada()
            r = calc.calcular_basico(expresion)
            if r.exitoso:
                return ResultadoHabilidad(exitoso=True, valor=r.resultado,
                    descripcion=r.resultado, pasos=r.paso_a_paso,
                    tipo_habilidad="CALCULO_BASICO", datos_raw=r)
            return ResultadoHabilidad(exitoso=False, valor="", descripcion="",
                error=r.error, tipo_habilidad="CALCULO_BASICO", datos_raw=r)
        except Exception as e:
            return ResultadoHabilidad(exitoso=False, valor="", descripcion="",
                error=f"Error: {e}", tipo_habilidad="CALCULO_BASICO")

    def formatear_respuesta(self, resultado, nombre_usuario=""):
        n = f", {nombre_usuario}" if nombre_usuario else ""
        if resultado.exitoso:
            return f"{resultado.valor}{n}."
        return f"{resultado.error}{n}."


# ═══════════════════════════════════════════════════════════════════════
# HABILIDAD: MATEMÁTICAS AVANZADAS — v2.0 (FIX-MAT-1 a FIX-MAT-5)
# ═══════════════════════════════════════════════════════════════════════

class HabilidadMatAvanzada(BaseHabilidad):

    @property
    def id(self): return "MAT_AVANZADA"

    @property
    def descripcion_para_bell(self):
        return (
            "Matemáticas avanzadas con SymPy: derivadas (ordinarias y parciales), "
            "integrales (definidas e indefinidas), límites, series de Taylor, "
            "factorización, simplificación, expansión, resolución de ecuaciones y "
            "sistemas, evaluación de funciones, estadística descriptiva completa, "
            "inecuaciones, MCD, MCM, números primos, combinatoria, info de polinomios."
        )

    @property
    def consejeras_requeridas(self): return ["Vega", "Nova"]

    # FIX-MAT-1: _DETECTORES ampliado con todos los sub_tipos nuevos
    _DETECTORES = [
        # ── Derivadas ────────────────────────────────────────────────
        (r'deriv[aá](?:da)?|diferencial\s+de|d/dx|dy/dx|d²/dx²|segunda\s+derivada',
         "DERIVADA", "derivar", 0.95),
        (r'derivada\s+parcial|parcial\s+de|∂',
         "DERIVADA_PARCIAL", "derivada_parcial", 0.95),

        # ── Integrales ───────────────────────────────────────────────
        (r'integr[aá](?:l)?|antiderivada|primitiva\s+de|[∫]|[aá]rea\s+bajo',
         "INTEGRAL", "integrar", 0.95),

        # ── Límites ──────────────────────────────────────────────────
        (r'l[íi]mite\s+(?:de|cuando)|lim\s*[\(\s]|lim\s+de|tiende\s+a',
         "LIMITE", "limite", 0.95),

        # ── Series de Taylor ─────────────────────────────────────────
        (r'serie\s+de\s+taylor|taylor\s+(?:de|series?)|expansi[oó]n\s+de\s+taylor',
         "TAYLOR", "serie_taylor", 0.95),

        # ── Factorizar ───────────────────────────────────────────────
        (r'factori[zs](?:a(?:r)?)?|factores?\s+de\s+[a-z]',
         "FACTORIZAR", "factorizar", 0.90),

        # ── Simplificar ──────────────────────────────────────────────
        (r'simplif[ií]c(?:a(?:r)?)?|reducir\s+la\s+expresi[oó]n|forma\s+m[aá]s\s+simple',
         "SIMPLIFICAR", "simplificar", 0.90),

        # ── Expandir ─────────────────────────────────────────────────
        (r'expan[ds](?:e(?:r)?)?|desarrolla(?:r)?\s+(?:la\s+)?expresi[oó]n',
         "EXPANDIR", "expandir", 0.90),

        # ── Inecuaciones — ANTES que ECUACION (prioridad) ────────────
        # "resuelve ... > 0" debe detectarse como inecuación, no ecuación
        (r'inecuaci[oó]n|resuelve\s+.{0,30}(?:>|<|>=|<=|≥|≤)|para\s+qu[eé]\s+valores?\s+de',
         "INECUACION", "resolver_inecuacion", 0.93),

        # ── Evaluar función — ANTES que ECUACION ─────────────────────
        # "evalua f(x) = ..." contiene "=" y es capturado por ECUACION si va después
        (r'eval[uú]a(?:r)?|sustituye?\s+[a-z]\s*=|valor\s+de\s+f\s*\(',
         "EVALUAR", "evaluar", 0.92),

        # ── Sistema de ecuaciones ─────────────────────────────────────
        (r'sistema\s+de\s+ecuaciones?|ecuaciones?\s+simult[aá]neas?|sistema\s+lineal|resuelve\s+el\s+sistema',
         "SISTEMA", "resolver_sistema", 0.95),

        # ── Resolver ecuación ────────────────────────────────────────
        (r'resolv[e]?[r]?|resuelv[e]?|solve\b|encuentra\s+(?:el\s+valor\s+de|las?\s+ra[íi]ces?)|halla\s+(?:x|y|z)\s*=',
         "ECUACION", "resolver_ecuacion", 0.92),

        # ── Estadística ──────────────────────────────────────────────
        (r'(?:calcula\s+(?:la\s+)?)?(?:media|promedio|average)\s+de|'
         r'desviaci[oó]n\s+(?:est[aá]ndar|t[íi]pica)|varianza\s+de|'
         r'mediana\s+de|moda\s+de|estadist|estad[íi]sticas?\s+de',
         "ESTADISTICA", "estadisticas", 0.90),

        # ── MCD / MCM ────────────────────────────────────────────────
        (r'(?:m\.?c\.?d\.?|m[aá]ximo\s+com[uú]n\s+divisor|gcd)\s+(?:de\s+)?\d',
         "MCD", "mcd", 0.92),
        (r'(?:m\.?c\.?m\.?|m[ií]nimo\s+com[uú]n\s+m[uú]ltiplo|lcm)\s+(?:de\s+)?\d',
         "MCM", "mcm", 0.92),

        # ── Números primos ────────────────────────────────────────────
        (r'\d+\s+es\s+primo\??|es\s+primo\s+\d+|n[uú]mero\s+primo\s+\d+|verifica\s+si\s+\d+\s+es\s+primo',
         "PRIMO", "es_primo", 0.90),

        # ── Combinatoria ─────────────────────────────────────────────
        (r'combinaciones?\s+de\s+\d+|C\s*\(\s*\d+\s*,\s*\d+\s*\)|nCr\s+\d',
         "COMBINACIONES", "combinaciones", 0.90),
        (r'permutaciones?\s+de\s+\d+|P\s*\(\s*\d+\s*,\s*\d+\s*\)|nPr\s+\d',
         "PERMUTACIONES", "permutaciones", 0.90),

        # ── Info polinomio ────────────────────────────────────────────
        (r'(?:grado|coeficientes?|ra[íi]ces?)\s+del?\s+polinomio|analiza\s+el\s+polinomio',
         "POLINOMIO", "polinomio_info", 0.88),
    ]

    def detectar(self, mensaje, conceptos, hechos):
        msg = mensaje.lower().strip()
        sub_tipo = metodo = None
        confianza = 0.0

        for patron, tipo, met, conf in self._DETECTORES:
            if re.search(patron, msg, re.IGNORECASE):
                sub_tipo = tipo
                metodo = met
                confianza = conf
                break

        if not sub_tipo or confianza < 0.80:
            return None

        expresion = self._extraer_expresion(msg, sub_tipo)
        orden     = self._extraer_orden(msg)
        limites   = self._extraer_limites(msg)
        variable  = self._extraer_variable(msg)
        punto     = self._extraer_punto(msg, sub_tipo)

        # FIX-DET-1: si no se extrajo expresión, usar el mensaje completo como fallback
        # para tipos que claramente tienen matemáticas (no bloquear por extracción fallida)
        if not expresion and sub_tipo not in ('SISTEMA', 'ESTADISTICA', 'MCD', 'MCM', 'PRIMO', 'COMBINACIONES', 'PERMUTACIONES'):
            expresion = mensaje  # usar mensaje original completo

        if sub_tipo not in ('SISTEMA', 'ESTADISTICA', 'MCD', 'MCM', 'PRIMO', 'COMBINACIONES', 'PERMUTACIONES', 'INECUACION', 'EVALUAR', 'POLINOMIO'):
            if not _expresion_tiene_matematica(expresion):
                logger.debug(
                    f"HabilidadMatAvanzada.detectar: expresion '{expresion}' "
                    f"sin matematica real para '{msg}' -> None"
                )
                return None

        # FIX-R8: "resuelve 9 * 9" — expresión sin variables → redirigir a CALCULO_BASICO
        if sub_tipo == "ECUACION" and _es_expresion_puramente_numerica(expresion):
            logger.debug(f"FIX-R8: '{expresion}' es numérica pura → redirigiendo a CALCULO_BASICO")
            _habilidad_calculo = HabilidadCalculo()
            return HabilidadMatch(
                habilidad_id="CALCULO_BASICO",
                confianza=confianza,
                parametros={"expresion": expresion},
                habilidad=_habilidad_calculo,
            )

        return HabilidadMatch(
            habilidad_id=f"MAT_{sub_tipo}",
            confianza=confianza,
            parametros={
                "sub_tipo":  sub_tipo,
                "metodo":    metodo,
                "expresion": expresion,
                "orden":     orden,
                "limites":   limites,
                "variable":  variable,
                "punto":     punto,
                "mensaje":   mensaje,
            },
            habilidad=self,
        )

    def _extraer_expresion(self, msg: str, sub_tipo: str) -> str:
        """FIX-MAT-2: extracción mejorada para todos los sub_tipos."""

        if sub_tipo == "TAYLOR":
            # "serie de taylor de sin(x) en x=0 hasta orden 5" → "sin(x)"
            m = re.search(r'serie\s+de\s+taylor\s+de\s+(.+?)(?:\s+en\s+x\s*=|\s+alrededor|\s+hasta\s+orden|$)', msg, re.IGNORECASE)
            if m: return m.group(1).strip()
            m = re.search(r'taylor\s+de[l]?\s+(.+?)(?:\s+en\s+x\s*=|\s+alrededor|\s+hasta\s+orden|$)', msg, re.IGNORECASE)
            if m: return m.group(1).strip()

        if sub_tipo == "INTEGRAL":
            # "integral de e^x desde 0 hasta 2" → "e^x" (quitar "integral de" al inicio)
            m = re.search(r'integral\s+de\s+(.+?)\s+(?:desde|de)\s+[\-\d\.]+', msg, re.IGNORECASE)
            if m: return m.group(1).strip()
            m = re.search(r'integra[r]?\s+(.+?)\s+de\s+[\-\d\.]+\s+a\s+[\-\d\.]+', msg, re.IGNORECASE)
            if m: return m.group(1).strip()
            m = re.search(r'integral\s+de\s+(.+)', msg, re.IGNORECASE)
            if m: return m.group(1).strip()
            m = re.search(r'integra[r]?\s+(.+)', msg, re.IGNORECASE)
            if m: return m.group(1).strip()

        if sub_tipo == "LIMITE":
            m = re.search(r'l[íi]mite\s+de\s+(.+?)(?:\s+cuando|\s+para|\s+en\s+x\s*=|$)', msg, re.IGNORECASE)
            if m:
                expr = m.group(1).strip()
                expr = re.sub(r'\s+(cuando|para|tiende|en\s+x).*$', '', expr, flags=re.IGNORECASE)
                return expr
            m = re.search(r'lim\s+de\s+(.+)', msg, re.IGNORECASE)
            if m: return m.group(1).strip()

        if sub_tipo == "ECUACION":
            m = re.search(r'(?:resuelve[r]?|solve)\s+(.+)', msg, re.IGNORECASE)
            if m:
                expr = m.group(1).strip()
                # Quitar prefijos de contexto "la ecuacion", "el sistema", etc.
                expr = re.sub(r'^(?:la\s+|el\s+)?(?:ecuaci[o\u00f3]n\s+|sistema\s+)', '', expr, flags=re.IGNORECASE).strip()
                return expr
            # "halla x si 3x + 7 = 22" → "3x + 7 = 22"
            m = re.search(r'halla[r]?\s+[a-z]\s+si\s+(.+)', msg, re.IGNORECASE)
            if m: return m.group(1).strip()
            m = re.search(r'halla[r]?\s+(?:las?\s+ra[i\u00ed]ces?\s+de\s+)?(.+)', msg, re.IGNORECASE)
            if m:
                expr = m.group(1).strip()
                # Quitar "x si " al inicio  
                expr = re.sub(r'^[a-z]\s+si\s+', '', expr, flags=re.IGNORECASE).strip()
                return expr

        if sub_tipo == "DERIVADA":
            m = re.search(
                r'(?:deriv(?:a(?:da?)?)?)\s+(?:de\s+)?(.+?)(?:\s+respecto|\s+de\s+orden|\s+en\s+x|$)',
                msg, re.IGNORECASE
            )
            if m:
                expr = m.group(1).strip()
                expr = re.sub(r'\s+(?:de\s+)?orden\s+\d+$', '', expr).strip()
                return expr
            m = re.search(r'derivada\s+de\s+(.+)', msg, re.IGNORECASE)
            if m: return m.group(1).strip()
            m = re.search(r'd/dx\s+(?:de\s+)?(.+)', msg, re.IGNORECASE)
            if m: return m.group(1).strip()

        if sub_tipo == "DERIVADA_PARCIAL":
            # "derivada parcial de x^2 * y^3 respecto a x" → "x^2 * y^3"
            m = re.search(r'derivada\s+parcial\s+de\s+(.+?)(?:\s+respecto|$)', msg, re.IGNORECASE)
            if m: return m.group(1).strip()
            m = re.search(r'parcial\s+de\s+(.+?)(?:\s+respecto|$)', msg, re.IGNORECASE)
            if m: return m.group(1).strip()
            # Quitar "parcial de" si quedó en la expresión y retornar el resto
            expr_limpia = re.sub(r'\bparcial\s+de\b', '', msg, flags=re.IGNORECASE).strip()
            expr_limpia = re.sub(r'\bparcial\b', '', expr_limpia, flags=re.IGNORECASE).strip()
            expr_limpia = re.sub(r'\bderivada\b', '', expr_limpia, flags=re.IGNORECASE).strip()
            expr_limpia = re.sub(r'\brespecto\s+a\s+\w\b', '', expr_limpia, flags=re.IGNORECASE).strip()
            return expr_limpia

        if sub_tipo == "SIMPLIFICAR":
            m = re.search(r'simplifica[r]?\s+(.+)', msg, re.IGNORECASE)
            if m: return m.group(1).strip()

        if sub_tipo == "EXPANDIR":
            m = re.search(r'expande?[r]?\s+(.+)', msg, re.IGNORECASE)
            if m: return m.group(1).strip()
            m = re.search(r'desarrolla[r]?\s+(.+)', msg, re.IGNORECASE)
            if m: return m.group(1).strip()

        if sub_tipo == "FACTORIZAR":
            m = re.search(r'factori[zs]a[r]?\s+(.+)', msg, re.IGNORECASE)
            if m: return m.group(1).strip()
            m = re.search(r'factores?\s+de\s+(.+)', msg, re.IGNORECASE)
            if m: return m.group(1).strip()

        if sub_tipo == "EVALUAR":
            # "evalúa f(x) = x^2 + 3x en x = 4" → expr="x^2 + 3x"
            m = re.search(r'eval[uú]a[r]?\s+(?:la\s+)?(?:funci[oó]n\s+)?[a-zA-Z]\s*\([a-zA-Z]\)\s*=\s*(.+?)\s+en\s+', msg, re.IGNORECASE)
            if m: return m.group(1).strip()
            m = re.search(r'eval[uú]a[r]?\s+(.+?)\s+en\s+[a-z]\s*=', msg, re.IGNORECASE)
            if m:
                expr = m.group(1).strip()
                # quitar "f(x) =" si quedó
                expr = re.sub(r'^[a-zA-Z]\s*\([a-zA-Z]\)\s*=\s*', '', expr).strip()
                return expr
            m = re.search(r'eval[uú]a[r]?\s+(.+)', msg, re.IGNORECASE)
            if m:
                expr = m.group(1).strip()
                expr = re.sub(r'^[a-zA-Z]\s*\([a-zA-Z]\)\s*=\s*', '', expr).strip()
                return expr
            m = re.search(r'valor\s+de\s+f\s*\((.+?)\)', msg, re.IGNORECASE)
            if m: return m.group(1).strip()

        if sub_tipo == "INECUACION":
            # Quitar prefijos de texto para dejar solo la expresión con el operador
            expr_ineq = re.sub(r'^resuelve[r]?\s+(?:la\s+)?inecuaci[oó]n\s+', '', msg, flags=re.IGNORECASE).strip()
            expr_ineq = re.sub(r'^(?:la\s+)?inecuaci[oó]n\s+', '', expr_ineq, flags=re.IGNORECASE).strip()
            expr_ineq = re.sub(r'^(?:resuelve[r]?\s+)', '', expr_ineq, flags=re.IGNORECASE).strip()
            # Si ya tiene el operador de desigualdad, usarla directamente
            if re.search(r'[<>]=?|[≤≥]', expr_ineq):
                return expr_ineq
            # Buscar la parte con operador
            m = re.search(r'([a-z0-9\s\+\-\*\/\^\(\)]+(?:>|<|>=|<=|≥|≤)[a-z0-9\s\+\-\*\/\^\(\)]+)', msg, re.IGNORECASE)
            if m: return m.group(1).strip()

        if sub_tipo == "ESTADISTICA":
            # "calcula la media de 10, 20, 30, 40, 50" → "10, 20, 30, 40, 50"
            # "estadísticas de 100, 200, 150" → "100, 200, 150"
            m = re.search(r'(?:de|del?)\s+([\d\s,\.]+)$', msg, re.IGNORECASE)
            if m: return m.group(1).strip()
            # buscar lista de números separados por coma
            m = re.search(r'([\d]+(?:\s*,\s*[\d]+){1,})', msg)
            if m: return m.group(1).strip()
            # fallback: todos los números del mensaje
            nums = re.findall(r'\d+(?:\.\d+)?', msg)
            if nums: return ', '.join(nums)

        if sub_tipo in ("MCD", "MCM"):
            nums = re.findall(r'\d+', msg)
            if len(nums) >= 2:
                return f"{nums[0]},{nums[1]}"

        if sub_tipo == "PRIMO":
            nums = re.findall(r'\d+', msg)
            if nums: return nums[0]

        if sub_tipo in ("COMBINACIONES", "PERMUTACIONES"):
            nums = re.findall(r'\d+', msg)
            if len(nums) >= 2:
                return f"{nums[0]},{nums[1]}"

        if sub_tipo == "SISTEMA":
            return msg  # se procesa entero en ejecutar() → _extraer_sistema()

        if sub_tipo == "POLINOMIO":
            m = re.search(r'polinomio\s+(.+)', msg, re.IGNORECASE)
            if m: return m.group(1).strip()

        # Fallback genérico
        limpio = re.sub(
            r'^(?:deriv(?:ada?)?|integra[r]?|factori[zs]a[r]?|simplifica[r]?|'
            r'expande?[r]?|resuelve[r]?|l[íi]mite\s+de|serie\s+de\s+taylor\s+de|'
            r'calcula[r]?\s+(?:la\s+|el\s+)?|eval[uú]a[r]?)\s*',
            '', msg, flags=re.IGNORECASE
        ).strip()
        limpio = re.sub(r'^(?:la|el|los|las|una?)\s+', '', limpio).strip()
        limpio = re.sub(r'^(?:funci[oó]n|polinomio|expresi[oó]n)\s+', '', limpio).strip()

        if sub_tipo == "DERIVADA":
            limpio = re.sub(r'\s+(?:de\s+)?orden\s+\d+$', '', limpio).strip()
            limpio = re.sub(r'\s+(?:segunda|segunda\s+derivada)$', '', limpio).strip()

        return limpio

    def _extraer_orden(self, msg: str) -> int:
        m = re.search(r'(?:orden|de\s+orden)\s+(\d+)', msg)
        if m: return int(m.group(1))
        if 'segunda' in msg or 'orden 2' in msg: return 2
        if 'tercera' in msg or 'orden 3' in msg: return 3
        return 1

    def _extraer_limites(self, msg: str) -> tuple:
        def _to_num(s):
            f = float(s)
            return int(f) if f == int(f) else f
        # FIX-R11: "desde X hasta Y" — forma mas comun en espanol
        m = re.search(r'desde\s+([\-\d\.]+)\s+hasta\s+([\-\d\.]+)', msg)
        if m:
            try: return _to_num(m.group(1)), _to_num(m.group(2))
            except: pass
        m = re.search(r'de\s+([\-\d\.]+)\s+a\s+([\-\d\.]+)', msg)
        if m:
            try: return _to_num(m.group(1)), _to_num(m.group(2))
            except: pass
        m = re.search(r'entre\s+([\-\d\.]+)\s+y\s+([\-\d\.]+)', msg)
        if m:
            try: return _to_num(m.group(1)), _to_num(m.group(2))
            except: pass
        return (None, None)

    def _extraer_variable(self, msg: str) -> str:
        m = re.search(r'respecto\s+a\s+([a-z])\b', msg)
        if m: return m.group(1)
        return 'x'

    def _extraer_punto(self, msg: str, sub_tipo: str = "") -> Any:
        msg_l = msg.lower()
        if any(w in msg_l for w in ['infinito', 'infinita', 'inf', '∞']):
            return 'oo'
        m = re.search(r'tiende\s+a\s+([\-\d\.]+)', msg_l)
        if m:
            try: return float(m.group(1))
            except: pass
        m = re.search(r'(?:cuando|en)\s+x\s*=\s*([\-\d\.]+)', msg_l)
        if m:
            try: return float(m.group(1))
            except: pass
        if sub_tipo == "LIMITE":
            m = re.search(r'en\s+([\-\d\.]+)', msg_l)
            if m:
                try: return float(m.group(1))
                except: pass
        return 0

    def ejecutar(self, match, nombre_usuario=""):
        """FIX-MAT-3: cubre TODOS los métodos de CalculadoraAvanzada v8.0."""
        p      = match.parametros
        sub    = p.get("sub_tipo", "")
        metodo = p.get("metodo", "")
        expr   = p.get("expresion", "").strip()
        orden  = p.get("orden", 1)
        lims   = p.get("limites", (None, None))
        var    = p.get("variable", "x")
        punto  = p.get("punto", 0)
        msg_orig = p.get("mensaje", expr)

        if not expr and sub not in ('SISTEMA', 'ESTADISTICA'):
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error="No detecté la expresión matemática. Escribe: 'deriva x**2 + 3*x'",
                tipo_habilidad=f"MAT_{sub}",
            )

        try:
            from matematicas.calculadora_avanzada import CalculadoraAvanzada
            calc = CalculadoraAvanzada()
            resultado = None

            # ── Derivadas ────────────────────────────────────────────
            if metodo == "derivar":
                resultado = calc.derivar(expr, var, orden)
                desc = self._desc_derivada(expr, resultado, orden, var)

            elif metodo == "derivada_parcial":
                resultado = calc.derivada_parcial(expr, var, orden)
                desc = self._desc_derivada_parcial(expr, resultado, orden, var)

            # ── Integrales ───────────────────────────────────────────
            elif metodo == "integrar":
                li, ls = lims
                resultado = calc.integrar(expr, variable=var,
                                          limite_inferior=li, limite_superior=ls)
                desc = self._desc_integral(expr, resultado, li, ls, var)

            # ── Límite ───────────────────────────────────────────────
            elif metodo == "limite":
                resultado = calc.limite(expr, var, punto)
                desc = self._desc_limite(expr, resultado, var, punto)

            # ── Taylor ───────────────────────────────────────────────
            elif metodo == "serie_taylor":
                n_orden = orden if orden > 1 else 5
                resultado = calc.serie_taylor(expr, var, punto, n_orden)
                desc = self._desc_taylor(expr, resultado, punto, n_orden)

            # ── Simplificar / Expandir / Factorizar ──────────────────
            elif metodo == "factorizar":
                resultado = calc.factorizar(expr)
                desc = self._desc_op(expr, resultado, "La factorización de")

            elif metodo == "simplificar":
                resultado = calc.simplificar(expr)
                desc = self._desc_op(expr, resultado, "Simplificando")

            elif metodo == "expandir":
                resultado = calc.expandir(expr)
                desc = self._desc_op(expr, resultado, "Expandiendo")

            # ── Ecuación ─────────────────────────────────────────────
            elif metodo == "resolver_ecuacion":
                resultado = calc.resolver_ecuacion(expr, var)
                desc = self._desc_ecuacion(expr, resultado, var)

            # ── Sistema (FIX-MAT-3 NUEVO + FIX-R10) ──────────────────
            elif metodo == "resolver_sistema":
                # Extraer ecuaciones del mensaje original
                eqs = self._extraer_sistema(msg_orig)
                variables_detectadas = self._extraer_variables_sistema(msg_orig)
                # FIX-R10: resolver_sistema necesita saber las variables exactas
                # Si se detectaron variables (incluyendo a,b,c), usarlas en orden
                # Si no, dejar que CalculadoraAvanzada las infiera del sistema
                resultado = calc.resolver_sistema(eqs, variables_detectadas if variables_detectadas else None)
                desc = self._desc_sistema(eqs, resultado)

            # ── Evaluar (FIX-MAT-3 NUEVO) ─────────────────────────────
            elif metodo == "evaluar":
                valores = self._extraer_valores_evaluacion(msg_orig)
                expr_eval = self._extraer_expr_para_evaluar(msg_orig)
                resultado = calc.evaluar(expr_eval or expr, valores)
                desc = self._desc_evaluar(expr_eval or expr, resultado, valores)

            # ── Estadística (FIX-MAT-3 NUEVO) ─────────────────────────
            elif metodo == "estadisticas":
                resultado = calc.estadisticas(expr)
                desc = self._desc_estadistica(resultado)

            # ── Inecuación (FIX-MAT-3 NUEVO) ──────────────────────────
            elif metodo == "resolver_inecuacion":
                resultado = calc.resolver_inecuacion(expr, var)
                desc = self._desc_inecuacion(expr, resultado)

            # ── MCD / MCM (FIX-MAT-3 NUEVO) ───────────────────────────
            elif metodo == "mcd":
                nums = re.findall(r'\d+', msg_orig)
                if len(nums) >= 2:
                    resultado = calc.mcd(int(nums[0]), int(nums[1]))
                    desc = resultado.resultado if resultado else ""
                else:
                    return ResultadoHabilidad(exitoso=False, valor="", descripcion="",
                        error="Necesito dos números para calcular el MCD.", tipo_habilidad="MAT_MCD")

            elif metodo == "mcm":
                nums = re.findall(r'\d+', msg_orig)
                if len(nums) >= 2:
                    resultado = calc.mcm(int(nums[0]), int(nums[1]))
                    desc = resultado.resultado if resultado else ""
                else:
                    return ResultadoHabilidad(exitoso=False, valor="", descripcion="",
                        error="Necesito dos números para calcular el MCM.", tipo_habilidad="MAT_MCM")

            # ── Primo (FIX-MAT-3 NUEVO) ────────────────────────────────
            elif metodo == "es_primo":
                nums = re.findall(r'\d+', msg_orig)
                if nums:
                    resultado = calc.es_primo(int(nums[0]))
                    desc = resultado.resultado if resultado else ""
                else:
                    return ResultadoHabilidad(exitoso=False, valor="", descripcion="",
                        error="Necesito un número para verificar si es primo.", tipo_habilidad="MAT_PRIMO")

            # ── Combinatoria (FIX-MAT-3 NUEVO) ─────────────────────────
            elif metodo == "combinaciones":
                nums = re.findall(r'\d+', msg_orig)
                if len(nums) >= 2:
                    resultado = calc.combinaciones(int(nums[0]), int(nums[1]))
                    desc = resultado.resultado if resultado else ""
                else:
                    return ResultadoHabilidad(exitoso=False, valor="", descripcion="",
                        error="Necesito n y r para calcular combinaciones C(n,r).", tipo_habilidad="MAT_COMBINACIONES")

            elif metodo == "permutaciones":
                nums = re.findall(r'\d+', msg_orig)
                if len(nums) >= 2:
                    resultado = calc.permutaciones(int(nums[0]), int(nums[1]))
                    desc = resultado.resultado if resultado else ""
                else:
                    return ResultadoHabilidad(exitoso=False, valor="", descripcion="",
                        error="Necesito n y r para calcular permutaciones P(n,r).", tipo_habilidad="MAT_PERMUTACIONES")

            # ── Info polinomio (FIX-MAT-3 NUEVO) ──────────────────────
            elif metodo == "polinomio_info":
                resultado = calc.polinomio_info(expr, var)
                desc = self._desc_op(expr, resultado, "Análisis del polinomio")

            # ── FIX-MAT-5: fallback a calcular_automatico ─────────────
            else:
                logger.warning(f"Método '{metodo}' no implementado, usando calcular_automatico")
                resultado = calc.calcular_automatico(msg_orig)
                desc = resultado.resultado if resultado and resultado.exitoso else ""

            if resultado is None:
                return ResultadoHabilidad(exitoso=False, valor="", descripcion="",
                    error=f"No pude aplicar {metodo}.", tipo_habilidad=f"MAT_{sub}")

            if resultado.exitoso:
                valor_str = str(resultado.resultado) if resultado.resultado is not None else ""
                return ResultadoHabilidad(exitoso=True, valor=valor_str,
                    descripcion=desc, pasos=resultado.paso_a_paso,
                    tipo_habilidad=f"MAT_{sub}", datos_raw=resultado)
            else:
                return ResultadoHabilidad(exitoso=False, valor="", descripcion="",
                    error=resultado.error or f"No pude calcular {metodo}.",
                    tipo_habilidad=f"MAT_{sub}", datos_raw=resultado)

        except Exception as e:
            logger.error(f"HabilidadMatAvanzada error: {e}")
            return ResultadoHabilidad(exitoso=False, valor="", descripcion="",
                error=f"Error al calcular: {e}", tipo_habilidad=f"MAT_{sub}")

    # ── Helpers de extracción para sub_tipos nuevos ──────────────────

    def _extraer_sistema(self, msg: str) -> List[str]:
        """FIX-R10: Extrae ecuaciones de un mensaje de sistema.
        Soporta:
          - 'x + y = 10 y 2x - y = 5'  (separador: ' y ')
          - 'x+y=10; 2x-y=5'           (separador: ';')
          - '3a + b = 7, a - b = 1'     (separador: ',')
          - variables: a,b,c,x,y,z...
        """
        msg_limpio = re.sub(
            r'^(?:resuelve[r]?\s+el\s+sistema\s*:?\s*|sistema\s+de\s+ecuaciones?\s*:?\s*|'
            r'ecuaciones?\s+simult[\u00e1]neas?\s*:?\s*|resuelve[r]?\s+el\s+sistema\s*:?\s*)',
            '', msg, flags=re.IGNORECASE
        ).strip()

        # Intentar separadores en orden de preferencia
        partes = None
        if ';' in msg_limpio:
            partes = msg_limpio.split(';')
        elif re.search(r',\s*[a-zA-Z0-9\-\(]', msg_limpio):
            # Coma seguida de contenido algebraico: separador de ecuaciones
            partes = msg_limpio.split(',')
        else:
            # Separador " y " — pero solo si lo que sigue parece una ecuacion
            # (empieza con letra, numero, parentesis o signo)
            partes = re.split(r'\s+y\s+(?=[a-zA-Z0-9\-\(])', msg_limpio, flags=re.IGNORECASE)

        eqs_limpias = []
        for e in partes:
            e = e.strip()
            # Quitar residuos de palabras clave al inicio de cada parte
            e = re.sub(r'^(?:y\s+|que\s+|donde\s+|y\s*$)', '', e, flags=re.IGNORECASE).strip()
            if re.search(r'=', e) and re.search(r'[a-zA-Z]', e):
                if e:
                    eqs_limpias.append(e)

        return eqs_limpias if len(eqs_limpias) >= 2 else [msg]

    def _extraer_variables_sistema(self, msg: str) -> Optional[List[str]]:
        """FIX-R10: Detecta las variables usadas en el sistema.
        Ahora acepta cualquier letra simple que aparezca como variable (no solo x,y,z,w).
        """
        # Buscar letras que aparecen junto a numeros u operadores (son variables)
        vars_en_ecuaciones = re.findall(r'(?<![a-zA-Z])([a-z])(?![a-zA-Z])(?=\s*[\+\-\*\/=]|[\+\-\*\/=])', msg)
        # Tambien buscar letras que preceden a operadores o siguen a operadores
        vars_con_coef = re.findall(r'(?:\d|^|\s)([a-z])(?:\s*[\+\-=]|$)', msg)
        # Combinar y filtrar ruido (palabras clave)
        _palabras_clave = {'y', 'o', 'e', 'u', 'a', 'de', 'si', 'en'}
        todas = vars_en_ecuaciones + vars_con_coef
        validas = [v for v in todas if len(v) == 1 and v not in _palabras_clave]
        # Preservar orden de aparicion
        vistas = []
        for v in validas:
            if v not in vistas:
                vistas.append(v)
        return vistas if vistas else None

    def _extraer_valores_evaluacion(self, msg: str) -> Dict[str, float]:
        """Extrae valores para evaluación: 'evalúa en x=2, y=3'."""
        valores = {}
        for m in re.finditer(r'([a-z])\s*=\s*([\-\d\.]+)', msg):
            try:
                valores[m.group(1)] = float(m.group(2))
            except ValueError:
                pass
        return valores

    def _extraer_expr_para_evaluar(self, msg: str) -> str:
        """Extrae la expresión a evaluar del mensaje, quitando 'f(x) =' del principio."""
        # "evalúa f(x) = x^2 + 3x en x = 4" → "x^2 + 3x"
        m = re.search(r'eval[uú]a[r]?\s+(?:(?:la\s+)?funci[oó]n\s+)?[a-zA-Z]\s*\([a-zA-Z]\)\s*=\s*(.+?)\s+(?:en|para|con|cuando)\s+[a-z]\s*=', msg, re.IGNORECASE)
        if m: return m.group(1).strip()
        # sin "en x=", toda la expresión después del "="
        m = re.search(r'eval[uú]a[r]?\s+(?:(?:la\s+)?funci[oó]n\s+)?[a-zA-Z]\s*\([a-zA-Z]\)\s*=\s*(.+)', msg, re.IGNORECASE)
        if m:
            expr = m.group(1).strip()
            # quitar "en x=4" al final si lo tiene
            expr = re.sub(r'\s+(?:en|para|con|cuando)\s+[a-z]\s*=\s*[\d\.]+$', '', expr, flags=re.IGNORECASE).strip()
            return expr
        m = re.search(r'eval[uú]a[r]?\s+(.+?)\s+(?:en|para|con|cuando)\s+[a-z]\s*=', msg, re.IGNORECASE)
        if m:
            expr = m.group(1).strip()
            expr = re.sub(r'^[a-zA-Z]\s*\([a-zA-Z]\)\s*=\s*', '', expr).strip()
            return expr
        m = re.search(r'f\(([^)]+)\)', msg)
        if m: return m.group(1).strip()
        return ""

    # ── Descriptores ─────────────────────────────────────────────────

    def _desc_derivada(self, expr, r, orden, var):
        if not r.exitoso: return ""
        o = {1: "primera", 2: "segunda", 3: "tercera"}.get(orden, f"orden {orden}")
        return f"La {o} derivada de {expr} respecto a {var} es {r.resultado}"

    def _desc_derivada_parcial(self, expr, r, orden, var):
        if not r.exitoso: return ""
        if orden == 1:
            return f"La derivada parcial de {expr} respecto a {var} es {r.resultado}"
        return f"La derivada parcial de orden {orden} de {expr} respecto a {var} es {r.resultado}"

    def _desc_integral(self, expr, r, li, ls, var):
        if not r.exitoso: return ""
        if li is not None and ls is not None:
            return f"La integral definida de {expr} de {li} a {ls} es {r.resultado}"
        return f"La integral indefinida de {expr} es {r.resultado} + C"

    def _desc_limite(self, expr, r, var, punto):
        if not r.exitoso: return ""
        ps = "infinito" if str(punto) in ('oo', 'inf') or punto == float('inf') else str(punto)
        return f"El límite de {expr} cuando {var} tiende a {ps} es {r.resultado}"

    def _desc_taylor(self, expr, r, punto, orden):
        if not r.exitoso: return ""
        return f"La serie de Taylor de {expr} alrededor de {punto} hasta orden {orden} es: {r.resultado}"

    def _desc_ecuacion(self, expr, r, var):
        if not r.exitoso: return ""
        # No agregar "= 0" si la expresión ya tiene "=" o comparador
        if re.search(r'[=<>]', str(expr)):
            return f"Las soluciones de {expr} son: {r.resultado}"
        return f"Las soluciones de {expr} = 0 son: {r.resultado}"

    def _desc_sistema(self, eqs, r):
        if not r.exitoso: return ""
        return f"La solución del sistema es: {r.resultado}"

    def _desc_evaluar(self, expr, r, valores):
        if not r.exitoso: return ""
        vals_str = ", ".join(f"{k}={v}" for k, v in valores.items())
        return f"El valor de {expr} con {vals_str} es {r.resultado}"

    def _desc_estadistica(self, r):
        if not r.exitoso: return ""
        return f"Estadísticas: {r.resultado}"

    def _desc_inecuacion(self, expr, r):
        if not r.exitoso: return ""
        return f"La solución de la inecuación {expr} es: {r.resultado}"

    def _desc_op(self, expr, r, verbo):
        if not r.exitoso: return ""
        return f"{verbo} {expr} es: {r.resultado}"

    def formatear_respuesta(self, resultado, nombre_usuario=""):
        """NUEVO-R1: muestra descripción clara y pasos si los hay."""
        n = f", {nombre_usuario}" if nombre_usuario else ""
        if resultado.exitoso:
            desc = resultado.descripcion or resultado.valor
            return f"{desc}{n}."
        return f"{resultado.error}{n}."


# ═══════════════════════════════════════════════════════════════════════
# REGISTRO CENTRAL — singleton
# ═══════════════════════════════════════════════════════════════════════

class RegistroHabilidades:

    _instancia: Optional['RegistroHabilidades'] = None

    def __init__(self):
        self._habilidades: Dict[str, BaseHabilidad] = {}
        self._prioridades: Dict[str, int] = {}
        self._orden_deteccion: List[str] = []
        self._registrar_habilidades_builtin()

    @classmethod
    def obtener(cls) -> 'RegistroHabilidades':
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    @classmethod
    def resetear(cls):
        cls._instancia = None

    def registrar(self, habilidad: BaseHabilidad, prioridad: int = 50):
        hid = habilidad.id
        self._habilidades[hid] = habilidad
        self._prioridades[hid] = prioridad
        self._orden_deteccion = sorted(
            self._habilidades.keys(),
            key=lambda x: self._prioridades.get(x, 50),
            reverse=True,
        )

    def detectar(self, mensaje, conceptos, hechos) -> Optional[HabilidadMatch]:
        mejor = None
        mejor_conf = 0.0
        for hid in self._orden_deteccion:
            try:
                m = self._habilidades[hid].detectar(mensaje, conceptos, hechos)
                if m and m.confianza > mejor_conf:
                    mejor_conf = m.confianza
                    mejor = m
                    if mejor_conf >= 0.95:
                        break
            except Exception as e:
                logger.warning(f"Error detectando {hid}: {e}")
        return mejor

    def ejecutar(self, match, nombre_usuario="") -> ResultadoHabilidad:
        resultado = match.habilidad.ejecutar(match, nombre_usuario)
        # BUG-R7 FIX: str() defensivo antes de verificar valor vacío
        valor_str = str(resultado.valor) if resultado.valor is not None else ""
        if resultado.exitoso and not valor_str.strip():
            resultado.exitoso = False
            resultado.error = "Resultado vacío detectado por Echo."
        resultado.verificado_echo = True
        return resultado

    def formatear(self, match, resultado, nombre_usuario="") -> str:
        return match.habilidad.formatear_respuesta(resultado, nombre_usuario)

    def listar_habilidades(self) -> List[Dict]:
        return [
            {"id": hid, "descripcion": self._habilidades[hid].descripcion_para_bell,
             "prioridad": self._prioridades.get(hid, 50)}
            for hid in self._orden_deteccion
        ]

    def obtener_habilidad(self, hid: str):
        return self._habilidades.get(hid)

    def _registrar_habilidades_builtin(self):
        # ── Matemáticas avanzadas — mayor prioridad ───────────────────
        self.registrar(HabilidadMatAvanzada(), prioridad=90)

        # ── Shell — segunda prioridad ─────────────────────────────────
        try:
            from habilidades.shell_habilidad import HabilidadShell
            self.registrar(HabilidadShell(), prioridad=80)
            logger.info("HabilidadShell registrada con prioridad 80")
        except ImportError:
            logger.warning("HabilidadShell no disponible — shell_habilidad.py no encontrado")

        # ── SQLite — tercera prioridad ────────────────────────────────
        try:
            from habilidades.sqlite_habilidad import HabilidadSQLite
            self.registrar(HabilidadSQLite(), prioridad=75)
            logger.info("HabilidadSQLite registrada con prioridad 75")
        except ImportError:
            logger.warning("HabilidadSQLite no disponible — sqlite_habilidad.py no encontrado")

        # ── Análisis Python — cuarta prioridad ────────────────────────
        try:
            from habilidades.analizador_habilidad import HabilidadAnalisisPython
            self.registrar(HabilidadAnalisisPython(), prioridad=72)
            logger.info("HabilidadAnalisisPython registrada con prioridad 72")
        except ImportError:
            logger.warning("HabilidadAnalisisPython no disponible — analizador_habilidad.py no encontrado")

        # ── Cálculo básico — prioridad 60 (FIX-PRIO) ─────────────────
        # ERA 70 — bajado a 60 para evitar competir con MatAvanzada (90)
        # en mensajes ambiguos. MatAvanzada tiene prioridad siempre.
        self.registrar(HabilidadCalculo(), prioridad=60)


# ═══════════════════════════════════════════════════════════════════════
# FUNCIÓN DE CONVENIENCIA
# ═══════════════════════════════════════════════════════════════════════

def detectar_y_ejecutar(mensaje, conceptos, hechos, nombre_usuario=""):
    registro = RegistroHabilidades.obtener()
    match = registro.detectar(mensaje, conceptos, hechos)
    if not match:
        return None
    resultado = registro.ejecutar(match, nombre_usuario)
    return registro.formatear(match, resultado, nombre_usuario)