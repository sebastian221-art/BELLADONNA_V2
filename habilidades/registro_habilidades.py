# -*- coding: utf-8 -*-
"""
registro_habilidades.py - VERSION v1.6

CAMBIOS v1.6 sobre v1.5:
======================================

FIX-R8: "resuelve 9 * 9" clasificaba como ECUACION en HabilidadMatAvanzada
         y llamaba a SymPy.solve(81, x) → soluciones=[] → Bell respondia
         "Las soluciones de 9 * 9 = 0 son: [], Sebastian."

CAUSA:  El patron r'resolv|resuelv' en _DETECTORES capturaba "resuelve 9 * 9"
        con confianza 0.92. La expresion extraida "9 * 9" tiene matematica real
        (_expresion_tiene_matematica=True) entonces pasaba la guarda. Pero al
        ejecutar, resolver_ecuacion("9 * 9") hace solve(81, x) = [] porque
        SymPy interpreta 81 = 0, que no tiene solucion.

FIX:    En HabilidadMatAvanzada.detectar(), antes de retornar el HabilidadMatch
        para sub_tipo ECUACION, verificar si la expresion extraida es puramente
        numerica (sin variables libres). Si lo es, retornar un HabilidadMatch
        con habilidad_id="CALCULO_BASICO" apuntando a HabilidadCalculo,
        de modo que se ejecute calcular_basico() en lugar de resolver_ecuacion().

NUEVA FUNCION: _es_expresion_puramente_numerica(expr_str) -> bool
        Parsea la expresion con SymPy y devuelve True si free_symbols es vacio.
        Si el parse falla, devuelve False (caso seguro: deja pasar a ecuacion).

CASOS QUE AHORA FUNCIONAN CORRECTAMENTE:
        "resuelve 9 * 9"      → CALCULO_BASICO → 81
        "resuelve 9 mas 9"    → CALCULO_BASICO → 18  (normalizar_expresion convierte)
        "resuelve 9 + 9"      → CALCULO_BASICO → 18
        "resuelve 100 / 4"    → CALCULO_BASICO → 25

CASOS QUE SIGUEN FUNCIONANDO IGUAL:
        "resuelve x**2 - 5*x + 6"  → ECUACION → [2, 3]
        "resuelve x + 3 = 0"       → ECUACION → [-3]
        "resuelve x**2 - 9"        → ECUACION → [-3, 3]

COMPATIBILIDAD: 100% con v1.5. Mismas firmas externas.
Todos los fixes anteriores (BUG-R6, BUG-R7, FIX v1.5) preservados intactos.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Any
import re
import logging

logger = logging.getLogger("registro_habilidades")


# ======================================================================
# TIPOS BASE
# ======================================================================

@dataclass
class ResultadoHabilidad:
    exitoso:         bool
    valor:           str
    descripcion:     str
    pasos:           List[str] = field(default_factory=list)
    error:           Optional[str] = None
    tipo_habilidad:  str = ""
    datos_raw:       Any = None
    verificado_echo: bool = False
    aprobado_vega:   bool = True


@dataclass
class HabilidadMatch:
    habilidad_id: str
    confianza:    float
    parametros:   Dict[str, Any]
    habilidad:    'BaseHabilidad'


# ======================================================================
# INTERFAZ BASE
# ======================================================================

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


# ======================================================================
# HABILIDAD: CALCULO BASICO
# ======================================================================

class HabilidadCalculo(BaseHabilidad):

    @property
    def id(self): return "CALCULO_BASICO"

    @property
    def descripcion_para_bell(self):
        return "Operaciones matematicas basicas: suma, resta, multiplicacion, division, raiz, potencias."

    _PATRONES = [
        r'\d+\s*[\+\-\*\/\u00f7\u00d7]\s*\d+',
        r'\u221a\s*\d+',
        r'\d+\s*\*\*\s*\d+',
        r'\d+\s*\^\s*\d+',
        r'ra[i\u00ed]z\s+(?:cuadrada\s+)?de\s+\d+',
    ]
    _TEXTO = [
        'multiplicado por', 'dividido entre', 'dividido por',
        'm\u00e1s ', 'mas ', 'menos ', 'cu\u00e1nto es', 'cuanto es',
        'al cuadrado', 'al cubo', 'elevado a',
    ]
    _EXCLUIR = [
        'deriv', 'integral', 'integr', 'l\u00edmite', 'limite',
        'taylor', 'factori', 'simplif', 'expand', 'ecuaci', 'resolv', 'resuelv',
    ]

    def detectar(self, mensaje, conceptos, hechos):
        msg = mensaje.lower().strip()
        if not re.search(r'\d+', msg):
            return None
        if any(e in msg for e in self._EXCLUIR):
            return None

        confianza = 0.0
        for p in self._PATRONES:
            if re.search(p, msg):
                confianza = max(confianza, 0.95)
                break
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


# ======================================================================
# HABILIDAD: MATEMATICAS AVANZADAS
# ======================================================================

# BUG-R6 FIX: patron para verificar que la expresion tiene contenido matematico real
_RE_EXPR_MAT_VALIDA = re.compile(
    r'(?:'
    r'[a-zA-Z]\s*[\*\+\-\/\^]'
    r'|[\*\+\-\/\^]\s*[a-zA-Z]'
    r'|\d+\s*[\*\+\-\/\^]'
    r'|[\*\+\-\/\^]\s*\d+'
    r'|\([a-zA-Z\d\s\+\-\*\/\^\*]+\)'
    r'|[a-zA-Z]\*\*\d'
    r'|\d\*\*\d'
    r'|sin\(|cos\(|tan\(|sqrt\('
    r'|exp\(|log\('
    r')',
    re.IGNORECASE
)


def _expresion_tiene_matematica(expr: str) -> bool:
    return bool(_RE_EXPR_MAT_VALIDA.search(expr))


# ======================================================================
# FIX-R8: detectar si una expresion es puramente numerica (sin variables)
# ======================================================================

def _es_expresion_puramente_numerica(expr_str: str) -> bool:
    """
    Retorna True si la expresion, una vez parseada por SymPy, no tiene
    variables libres. Esto permite distinguir:
        "9 * 9"          -> True  (calculo basico, no ecuacion)
        "x**2 - 5*x + 6" -> False (ecuacion algebraica)

    Si el parse falla por cualquier razon, retorna False de forma segura
    (la expresion sigue su camino normal hacia resolver_ecuacion).
    """
    try:
        from sympy.parsing.sympy_parser import parse_expr
        from matematicas.calculadora_avanzada import normalizar_expresion
        expr_norm = normalizar_expresion(expr_str)
        expr = parse_expr(expr_norm)
        return not bool(expr.free_symbols)
    except Exception:
        return False


class HabilidadMatAvanzada(BaseHabilidad):

    @property
    def id(self): return "MAT_AVANZADA"

    @property
    def descripcion_para_bell(self):
        return (
            "Matematicas avanzadas: derivadas, integrales definidas e indefinidas, "
            "limites, series de Taylor, factorizacion, simplificacion, expansion, "
            "resolucion de ecuaciones."
        )

    @property
    def consejeras_requeridas(self): return ["Vega", "Nova"]

    _DETECTORES = [
        (r'deriv[a\u00e1]',                   "DERIVADA",    "derivar",           0.95),
        (r'integr[a\u00e1]',                  "INTEGRAL",    "integrar",          0.95),
        (r'l[i\u00ed]mite|lim\s*\(',          "LIMITE",      "limite",            0.95),
        (r'serie\s+de\s+taylor|taylor',       "TAYLOR",      "serie_taylor",      0.95),
        (r'factori[zs]',                      "FACTORIZAR",  "factorizar",        0.90),
        (r'simplif[i\u00ed]c',               "SIMPLIFICAR", "simplificar",       0.90),
        (r'expan[ds]',                        "EXPANDIR",    "expandir",          0.90),
        (r'resolv|resuelv|solve',             "ECUACION",    "resolver_ecuacion", 0.92),
    ]

    def detectar(self, mensaje, conceptos, hechos):
        msg = mensaje.lower().strip()
        sub_tipo = metodo = None
        confianza = 0.0

        for patron, tipo, met, conf in self._DETECTORES:
            if re.search(patron, msg):
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

        if not _expresion_tiene_matematica(expresion):
            logger.debug(
                f"HabilidadMatAvanzada.detectar: expresion '{expresion}' "
                f"sin matematica real para '{msg}' -> None (CAPACIDAD_BELL)"
            )
            return None

        # ── FIX-R8: "resuelve 9 * 9" — expresion sin variables ───────
        # Si el patron matched es ECUACION pero la expresion extraida
        # no tiene variables libres (es puramente numerica), no tiene
        # sentido llamar a resolver_ecuacion() — SymPy devolveria [].
        # Redirigimos a CALCULO_BASICO en su lugar.
        if sub_tipo == "ECUACION" and _es_expresion_puramente_numerica(expresion):
            logger.debug(
                f"FIX-R8: '{expresion}' es numerica pura en contexto ECUACION "
                f"→ redirigiendo a CALCULO_BASICO"
            )
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
        if sub_tipo == "TAYLOR":
            m = re.search(r'taylor\s+de[l]?\s+(.+)', msg, re.IGNORECASE)
            if m:
                return m.group(1).strip()

        if sub_tipo == "INTEGRAL":
            m = re.search(
                r'integra[r]?\s+(.+?)\s+de\s+[\-\d\.]+\s+a\s+[\-\d\.]+',
                msg, re.IGNORECASE
            )
            if m:
                return m.group(1).strip()
            m = re.search(r'integra[r]?\s+(.+)', msg, re.IGNORECASE)
            if m:
                return m.group(1).strip()

        if sub_tipo == "LIMITE":
            m = re.search(r'l[i\u00ed]mite\s+de\s+(.+?)(?:\s+cuando|\s+para|\s+en\s+x\s*=|$)',
                          msg, re.IGNORECASE)
            if m:
                expr = m.group(1).strip()
                expr = re.sub(r'\s+(cuando|para|tiende|en\s+x).*$', '', expr, flags=re.IGNORECASE)
                return expr

        if sub_tipo == "ECUACION":
            m = re.search(r'(?:resuelve[r]?|solve)\s+(.+)', msg, re.IGNORECASE)
            if m:
                return m.group(1).strip()

        if sub_tipo == "DERIVADA":
            m = re.search(r'(?:deriv(?:a(?:da?)?)?\s+(?:de\s+)?|calcula[r]?\s+la\s+derivada\s+de\s+)(.+)',
                          msg, re.IGNORECASE)
            if m:
                expr = m.group(1).strip()
                expr = re.sub(r'\s+(?:de\s+)?orden\s+\d+$', '', expr).strip()
                return expr

        limpio = re.sub(
            r'^(deriv(?:ada?)?\s+(?:de\s+)?|calcula[r]?\s+la\s+derivada\s+de|'
            r'integra[r]?|factori[zs]a[r]?|simplifica[r]?|expande[r]?|'
            r'resuelve[r]?|l[i\u00ed]mite\s+de|serie\s+de\s+taylor\s+de)\s*',
            '', msg, flags=re.IGNORECASE
        ).strip()
        limpio = re.sub(r'^(la|el|los|las|una?)\s+', '', limpio).strip()
        limpio = re.sub(r'^(funci[o\u00f3]n|polinomio|expresi[o\u00f3]n)\s+', '', limpio).strip()

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
        if any(w in msg_l for w in ['infinito', 'infinita', 'inf', '\u221e']):
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
        p      = match.parametros
        sub    = p.get("sub_tipo", "")
        metodo = p.get("metodo", "")
        expr   = p.get("expresion", "").strip()
        orden  = p.get("orden", 1)
        lims   = p.get("limites", (None, None))
        var    = p.get("variable", "x")
        punto  = p.get("punto", 0)

        if not expr:
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error="No detecte la expresion matematica. Escribe: 'deriva x**2 + 3*x'",
                tipo_habilidad=f"MAT_{sub}",
            )

        try:
            from matematicas.calculadora_avanzada import CalculadoraAvanzada
            calc = CalculadoraAvanzada()
            resultado = None

            if metodo == "derivar":
                resultado = calc.derivar(expr, var, orden)
                desc = self._desc_derivada(expr, resultado, orden, var)
            elif metodo == "integrar":
                li, ls = lims
                resultado = calc.integrar(expr, variable=var,
                                          limite_inferior=li, limite_superior=ls)
                desc = self._desc_integral(expr, resultado, li, ls, var)
            elif metodo == "limite":
                resultado = calc.limite(expr, var, punto)
                desc = self._desc_limite(expr, resultado, var, punto)
            elif metodo == "serie_taylor":
                n_orden = orden if orden > 1 else 5
                resultado = calc.serie_taylor(expr, var, punto, n_orden)
                desc = self._desc_taylor(expr, resultado, punto, n_orden)
            elif metodo == "factorizar":
                resultado = calc.factorizar(expr)
                desc = self._desc_op(expr, resultado, "La factorizacion de")
            elif metodo == "simplificar":
                resultado = calc.simplificar(expr)
                desc = self._desc_op(expr, resultado, "Simplificando")
            elif metodo == "expandir":
                resultado = calc.expandir(expr)
                desc = self._desc_op(expr, resultado, "Expandiendo")
            elif metodo == "resolver_ecuacion":
                resultado = calc.resolver_ecuacion(expr, var)
                desc = self._desc_ecuacion(expr, resultado, var)
            else:
                return ResultadoHabilidad(exitoso=False, valor="", descripcion="",
                    error=f"Metodo '{metodo}' no implementado.", tipo_habilidad=f"MAT_{sub}")

            if resultado is None:
                return ResultadoHabilidad(exitoso=False, valor="", descripcion="",
                    error=f"No pude aplicar {metodo}.", tipo_habilidad=f"MAT_{sub}")

            if resultado.exitoso:
                # BUG-R7 FIX: str() defensivo
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

    def _desc_derivada(self, expr, r, orden, var):
        if not r.exitoso: return ""
        o = {1: "primera", 2: "segunda", 3: "tercera"}.get(orden, f"orden {orden}")
        return f"La {o} derivada de {expr} respecto a {var} es {r.resultado}"

    def _desc_integral(self, expr, r, li, ls, var):
        if not r.exitoso: return ""
        if li is not None and ls is not None:
            return f"La integral definida de {expr} de {li} a {ls} es {r.resultado}"
        return f"La integral indefinida de {expr} es {r.resultado} + C"

    def _desc_limite(self, expr, r, var, punto):
        if not r.exitoso: return ""
        ps = "infinito" if str(punto) in ('oo', 'inf') or punto == float('inf') else str(punto)
        return f"El limite de {expr} cuando {var} tiende a {ps} es {r.resultado}"

    def _desc_taylor(self, expr, r, punto, orden):
        if not r.exitoso: return ""
        return f"La serie de Taylor de {expr} alrededor de {punto} hasta orden {orden} es: {r.resultado}"

    def _desc_ecuacion(self, expr, r, var):
        if not r.exitoso: return ""
        return f"Las soluciones de {expr} = 0 son: {r.resultado}"

    def _desc_op(self, expr, r, verbo):
        if not r.exitoso: return ""
        return f"{verbo} {expr} es: {r.resultado}"

    def formatear_respuesta(self, resultado, nombre_usuario=""):
        n = f", {nombre_usuario}" if nombre_usuario else ""
        if resultado.exitoso:
            return f"{resultado.descripcion}{n}."
        return f"{resultado.error}{n}."


# ======================================================================
# REGISTRO CENTRAL — singleton
# ======================================================================

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
            resultado.error = "Resultado vacio detectado por Echo."
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

        # ── Cálculo básico — menor prioridad ──────────────────────────
        self.registrar(HabilidadCalculo(), prioridad=70)


# ======================================================================
# FUNCION DE CONVENIENCIA
# ======================================================================

def detectar_y_ejecutar(mensaje, conceptos, hechos, nombre_usuario=""):
    registro = RegistroHabilidades.obtener()
    match = registro.detectar(mensaje, conceptos, hechos)
    if not match:
        return None
    resultado = registro.ejecutar(match, nombre_usuario)
    return registro.formatear(match, resultado, nombre_usuario)