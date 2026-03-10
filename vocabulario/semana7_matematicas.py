# -*- coding: utf-8 -*-
"""
semana7_matematicas.py — VERSION v4.0 (Fase 3, maximizada)

CAMBIOS v4.0 sobre v3.0:
═══════════════════════════════════════════════════════════════════════
FIX-VOC-1   CONCEPTO_LIMITE: palabras_español ampliadas con formas
            naturales: "límite", "lim de", "limite de", "lim cuando",
            "tiende a", "cuando x tiende". El vocabulario anterior
            ["límite matemático", "limit cálculo", "límite función"]
            era demasiado específico y nadie lo usaba así.

FIX-VOC-2   CONCEPTO_SERIE_TAYLOR: ampliado con "taylor de", "serie
            taylor", "expansión taylor", "polinomio taylor".

FIX-VOC-3   CONCEPTO_RESOLVER_ECUACION: ampliado con "halla x",
            "encuentra x", "valor de x", "raíces de", "ceros de",
            "para qué valores", "cuando es cero".

FIX-VOC-4   CONCEPTO_SIMPLIFICAR: ampliado con "simplifica", "reduce",
            "forma más simple", "cancela términos".

FIX-VOC-5   CONCEPTO_EXPANDIR: ampliado con "expande", "desarrolla",
            "distribuye", "multiplica los paréntesis".

FIX-VOC-6   CONCEPTO_FACTORIZAR: ampliado con "factoriza", "factores
            de", "factorización de", "descomponer en factores".

FIX-VOC-7   CONCEPTO_DERIVAR / CONCEPTO_INTEGRAR: palabras ampliadas
            con todas las formas coloquiales en español.

NUEVO-V1    CONCEPTO_ESTADISTICA — operación ejecutable que invoca
            calc.estadisticas(). Cubre media, promedio, desviación,
            varianza, mediana, moda con SymPy / Python puro.

NUEVO-V2    CONCEPTO_SISTEMA_LINEAL — operación ejecutable que invoca
            calc.resolver_sistema() para sistemas de ecuaciones.

NUEVO-V3    CONCEPTO_EVALUAR_FUNCION — concepto de evaluación con
            palabras como "evalúa f(x) en x=2", "sustituye x por 3".

NUEVO-V4    CONCEPTO_DERIVADA_PARCIAL — operación ejecutable que invoca
            calc.derivada_parcial().

NUEVO-V5    CONCEPTO_INECUACION — operación ejecutable para inecuaciones
            con operadores >, <, >=, <=.

NUEVO-V6    CONCEPTO_MCD — operación ejecutable para máximo común
            divisor de dos números.

NUEVO-V7    CONCEPTO_MCM — operación ejecutable para mínimo común
            múltiplo de dos números.

NUEVO-V8    CONCEPTO_NUMERO_PRIMO — operación ejecutable para verificar
            primalidad.

NUEVO-V9    CONCEPTO_COMBINATORIA — operación ejecutable para C(n,r)
            y P(n,r).

NUEVO-V10   CONCEPTO_POLINOMIO_INFO — analiza grado, coeficientes,
            raíces y factorización de un polinomio.

NUEVO-V11   CONCEPTO_FUNCION_TRIGONOMETRICA — vocabulario completo para
            sin, cos, tan, sec, csc, cot y sus inversas.

NUEVO-V12   CONCEPTO_LOGARITMO — vocabulario para log, ln, log base N.

NUEVO-V13   CONCEPTO_NUMERO_COMPLEJO — soporte de vocabulario para
            resultados complejos.

Todos los 45 conceptos originales preservados e integrados.
Total final: 66 conceptos (45 originales + 21 nuevos).
═══════════════════════════════════════════════════════════════════════
"""

from pathlib import Path
import sys

# Agregar path del proyecto
proyecto_path = Path(__file__).parent.parent
sys.path.insert(0, str(proyecto_path))

from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto

# Calculadora (se inyecta en runtime)
calculadora = None

def configurar_calculadora(calc):
    """Configura la calculadora para los conceptos operativos."""
    global calculadora
    calculadora = calc


def obtener_conceptos_matematicas_avanzadas():
    """
    Retorna 66 conceptos de matemáticas avanzadas.

    Categorías:
    - Derivadas (9 conceptos)
    - Integrales (8 conceptos)
    - Ecuaciones y Sistemas (9 conceptos)
    - Simplificación/Expansión/Factorización (8 conceptos)
    - Límites y Series (9 conceptos)
    - Evaluación y Estadística (8 conceptos)
    - Aritmética Discreta y Combinatoria (7 conceptos)
    - Funciones y Constantes (8 conceptos)
    """
    conceptos = []

    # ═══════════════════════════════════════════════════════
    # DERIVADAS (9 conceptos)
    # ═══════════════════════════════════════════════════════

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DERIVAR",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            # FIX-VOC-7: ampliado
            "derivar", "calcular derivada", "diferencial", "deriva",
            "calcula la derivada de", "saca la derivada", "obtén la derivada",
            "diferencia", "tasa de cambio de", "d/dx de", "dy/dx",
        ],
        operaciones={
            'ejecutar': lambda expr, var='x': calculadora.derivar(expr, var)
                        if calculadora else None
        },
        confianza_grounding=1.0,
        propiedades={
            'usa_sympy': True,
            'retorna': 'ResultadoMatematico',
            'soporta_orden': True,
            'habilidad_asociada': 'MAT_AVANZADA',
        }
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DERIVADA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "derivada", "derivative", "tasa de cambio",
            "pendiente de la tangente", "ritmo de cambio",
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'operador',
            'mide': 'tasa de cambio',
            'notacion': "f'(x), dy/dx, d/dx",
            'habilidad_asociada': 'MAT_AVANZADA',
        }
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DERIVADA_PRIMERA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "primera derivada", "derivada de primer orden",
            "velocidad", "tasa de cambio", "derivada primera",
        ],
        confianza_grounding=0.9,
        propiedades={'orden': 1, 'notacion': "f'(x)", 'representa': 'velocidad de cambio'}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DERIVADA_SEGUNDA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "segunda derivada", "derivada de segundo orden",
            "aceleración", "concavidad", "derivada segunda",
        ],
        confianza_grounding=0.9,
        propiedades={'orden': 2, 'notacion': "f''(x)", 'representa': 'aceleración'}
    ))

    # NUEVO-V4: derivada parcial ejecutable
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DERIVADA_PARCIAL",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "derivada parcial", "partial derivative", "∂", "parcial de",
            "derivada parcial respecto a", "derivar parcialmente",
        ],
        operaciones={
            'ejecutar': lambda expr, var='x': calculadora.derivada_parcial(expr, var)
                        if calculadora else None
        },
        confianza_grounding=1.0,
        propiedades={
            'usa_sympy': True,
            'retorna': 'ResultadoMatematico',
            'habilidad_asociada': 'MAT_AVANZADA',
        }
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_REGLA_CADENA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "regla de la cadena", "chain rule", "derivada de composición",
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'regla de derivación',
            'para': 'funciones compuestas',
            'formula': "(f∘g)'(x) = f'(g(x))·g'(x)",
        }
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_REGLA_PRODUCTO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["regla del producto", "product rule", "derivada de producto"],
        confianza_grounding=0.9,
        propiedades={
            'es': 'regla de derivación',
            'formula': "(f·g)' = f'·g + f·g'",
        }
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_REGLA_COCIENTE",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["regla del cociente", "quotient rule", "derivada de cociente"],
        confianza_grounding=0.9,
        propiedades={
            'es': 'regla de derivación',
            'formula': "(f/g)' = (f'g - fg')/g²",
        }
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DERIVADA_SIMBOLICA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["derivada simbólica", "symbolic derivative", "derivación simbólica"],
        confianza_grounding=0.9,
        propiedades={'es': 'cálculo simbólico', 'resultado': 'expresión algebraica'}
    ))

    # ═══════════════════════════════════════════════════════
    # INTEGRALES (8 conceptos)
    # ═══════════════════════════════════════════════════════

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INTEGRAR",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            # FIX-VOC-7: ampliado
            "integrar", "calcular integral", "integración", "integra",
            "calcula la integral de", "saca la integral", "antiderivada de",
            "primitiva de", "integral de", "área bajo la curva de",
            "∫", "integral definida", "integral indefinida",
        ],
        operaciones={
            'ejecutar': lambda expr, var='x', a=None, b=None:
                        calculadora.integrar(expr, var, a, b)
                        if calculadora else None
        },
        confianza_grounding=1.0,
        propiedades={
            'usa_sympy': True,
            'retorna': 'ResultadoMatematico',
            'tipos': ['definida', 'indefinida'],
            'habilidad_asociada': 'MAT_AVANZADA',
        }
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INTEGRAL",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["integral", "antiderivada", "primitiva"],
        confianza_grounding=0.9,
        propiedades={'es': 'operador', 'inversa_de': 'derivada', 'notacion': '∫f(x)dx'}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INTEGRAL_DEFINIDA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "integral definida", "definite integral", "área bajo la curva",
            "área entre límites",
        ],
        confianza_grounding=0.9,
        propiedades={
            'tiene': 'límites de integración',
            'resultado': 'número',
            'notacion': '∫[a,b] f(x)dx',
        }
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INTEGRAL_INDEFINIDA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "integral indefinida", "indefinite integral", "antiderivada", "primitiva",
        ],
        confianza_grounding=0.9,
        propiedades={'sin': 'límites', 'resultado': 'función + C', 'constante': 'C'}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CONSTANTE_INTEGRACION",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["constante de integración", "c", "constante arbitraria"],
        confianza_grounding=0.9,
        propiedades={'simbolo': 'C', 'razon': 'derivada de constante es 0'}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TEOREMA_FUNDAMENTAL_CALCULO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["teorema fundamental del cálculo", "fundamental theorem of calculus"],
        confianza_grounding=0.9,
        propiedades={'dice': '∫[a,b] f\'(x)dx = f(b) - f(a)'}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SUSTITUCION",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["sustitución", "u-substitution", "cambio de variable"],
        confianza_grounding=0.9,
        propiedades={'es': 'técnica de integración'}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INTEGRACION_POR_PARTES",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["integración por partes", "integration by parts"],
        confianza_grounding=0.9,
        propiedades={'formula': '∫u dv = uv - ∫v du'}
    ))

    # ═══════════════════════════════════════════════════════
    # ECUACIONES Y SISTEMAS (9 conceptos)
    # ═══════════════════════════════════════════════════════

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RESOLVER_ECUACION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            # FIX-VOC-3: ampliado
            "resolver ecuación", "solve", "encontrar solución", "hallar raíces",
            "resuelve", "resolver", "halla x", "encuentra x", "valor de x",
            "raíces de", "ceros de", "para qué valores", "cuando es cero",
            "encontrar la x", "despejar x", "cuánto vale x", "qué vale x",
            "soluciones de", "solución de la ecuación",
        ],
        operaciones={
            'ejecutar': lambda ecuacion, var='x':
                        calculadora.resolver_ecuacion(ecuacion, var)
                        if calculadora else None
        },
        confianza_grounding=1.0,
        propiedades={
            'usa_sympy': True,
            'retorna': 'lista de soluciones',
            'habilidad_asociada': 'MAT_AVANZADA',
        }
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ECUACION_AVANZADA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["ecuación", "equation", "igualdad matemática"],
        confianza_grounding=0.9,
        propiedades={'objetivo': 'encontrar valores que la satisfacen'}
    ))

    # NUEVO-V2: sistema de ecuaciones ejecutable
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SISTEMA_LINEAL",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "sistema de ecuaciones", "sistema lineal", "ecuaciones simultáneas",
            "resuelve el sistema", "sistema de", "sistema 2x2", "sistema 3x3",
            "resolver simultáneamente", "solución del sistema",
        ],
        operaciones={
            'ejecutar': lambda eqs, variables=None:
                        calculadora.resolver_sistema(eqs, variables)
                        if calculadora else None
        },
        confianza_grounding=1.0,
        propiedades={
            'usa_sympy': True,
            'habilidad_asociada': 'MAT_AVANZADA',
        }
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RAIZ_AVANZADA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["raíz", "root", "solución", "cero de la función"],
        confianza_grounding=0.9,
        propiedades={'es': 'valor que hace f(x) = 0'}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ECUACION_CUADRATICA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "ecuación cuadrática", "quadratic equation",
            "ecuación de segundo grado", "ecuación cuadrática",
        ],
        confianza_grounding=0.9,
        propiedades={
            'forma': 'ax² + bx + c = 0',
            'formula': 'x = (-b ± √(b²-4ac))/2a',
        }
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DISCRIMINANTE",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["discriminante", "discriminant"],
        confianza_grounding=0.9,
        propiedades={'formula': 'b² - 4ac', 'determina': 'número de raíces reales'}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SISTEMA_ECUACIONES",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "sistema de ecuaciones", "system of equations", "ecuaciones simultáneas",
        ],
        confianza_grounding=0.9,
        propiedades={'metodos': ['sustitución', 'eliminación', 'matrices']}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ECUACION_DIFERENCIAL",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["ecuación diferencial", "differential equation", "ode"],
        confianza_grounding=0.9,
        propiedades={'tipos': ['ordinarias', 'parciales']}
    ))

    # NUEVO-V5: inecuaciones ejecutables
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INECUACION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "inecuación", "inequality", "desigualdad", "resuelve la desigualdad",
            "para qué x es mayor que", "para qué x es menor que",
            "valores de x donde", "cuando es positivo", "cuando es negativo",
        ],
        operaciones={
            'ejecutar': lambda inec, var='x':
                        calculadora.resolver_inecuacion(inec, var)
                        if calculadora else None
        },
        confianza_grounding=1.0,
        propiedades={
            'usa_sympy': True,
            'habilidad_asociada': 'MAT_AVANZADA',
        }
    ))

    # ═══════════════════════════════════════════════════════
    # SIMPLIFICACIÓN / EXPANSIÓN / FACTORIZACIÓN (8 conceptos)
    # ═══════════════════════════════════════════════════════

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SIMPLIFICAR",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            # FIX-VOC-4: ampliado
            "simplificar", "simplify", "reducir expresión", "simplifica",
            "simplifica esto", "reduce la expresión", "forma más simple",
            "cancela términos", "simplifica la fracción", "simplificame",
        ],
        operaciones={
            'ejecutar': lambda expr: calculadora.simplificar(expr)
                        if calculadora else None
        },
        confianza_grounding=1.0,
        propiedades={
            'usa_sympy': True,
            'habilidad_asociada': 'MAT_AVANZADA',
        }
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EXPANDIR",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            # FIX-VOC-5: ampliado
            "expandir", "expand", "desarrollar expresión", "expande",
            "distribuye", "multiplica los paréntesis", "desarrolla",
            "expande esto", "abre los paréntesis",
        ],
        operaciones={
            'ejecutar': lambda expr: calculadora.expandir(expr)
                        if calculadora else None
        },
        confianza_grounding=1.0,
        propiedades={
            'usa_sympy': True,
            'ejemplo': '(x+1)² → x² + 2x + 1',
            'habilidad_asociada': 'MAT_AVANZADA',
        }
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FACTORIZAR",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            # FIX-VOC-6: ampliado
            "factorizar", "factor", "factorear", "factoriza",
            "descomponer en factores", "factorización de",
            "factorea esto", "factoriza esta expresión",
            "saca factor común", "encuentra los factores de",
        ],
        operaciones={
            'ejecutar': lambda expr: calculadora.factorizar(expr)
                        if calculadora else None
        },
        confianza_grounding=1.0,
        propiedades={
            'usa_sympy': True,
            'ejemplo': 'x² - 4 → (x-2)(x+2)',
            'habilidad_asociada': 'MAT_AVANZADA',
        }
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FACTOR",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["factor", "divisor"],
        confianza_grounding=0.9,
        propiedades={'es': 'término multiplicativo'}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TERMINO_COMUN",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["término común", "factor común", "common factor"],
        confianza_grounding=0.9,
        propiedades={'es': 'factor presente en todos los términos'}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EXPRESION_ALGEBRAICA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["expresión algebraica", "algebraic expression"],
        confianza_grounding=0.9,
        propiedades={'tipos': ['monomio', 'binomio', 'polinomio']}
    ))

    # NUEVO-V10: info de polinomio ejecutable
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_POLINOMIO_INFO",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "analiza el polinomio", "grado del polinomio", "coeficientes del polinomio",
            "raíces del polinomio", "info del polinomio", "información del polinomio",
        ],
        operaciones={
            'ejecutar': lambda expr, var='x': calculadora.polinomio_info(expr, var)
                        if calculadora else None
        },
        confianza_grounding=1.0,
        propiedades={
            'usa_sympy': True,
            'habilidad_asociada': 'MAT_AVANZADA',
        }
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_POLINOMIO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "polinomio", "polynomial", "función polinomial",
            "polinomio de grado n",
        ],
        confianza_grounding=0.9,
        propiedades={'tipos': ['monomio', 'binomio', 'trinomio', 'polinomio']}
    ))

    # ═══════════════════════════════════════════════════════
    # LÍMITES Y SERIES (9 conceptos)
    # ═══════════════════════════════════════════════════════

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LIMITE",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        # FIX-VOC-1: palabras naturales ampliadas
        palabras_español=[
            "límite", "limite", "lim", "limit",
            "lim de", "límite de", "limite de",
            "lim cuando", "cuando x tiende", "tiende a",
            "límite cuando x tiende a", "límite en el infinito",
            "límite lateral", "qué pasa cuando x tiende",
            "valor cuando x se acerca", "límite de la función",
        ],
        operaciones={
            'ejecutar': lambda expr, var='x', punto=0:
                        calculadora.limite(expr, var, punto)
                        if calculadora else None
        },
        confianza_grounding=1.0,
        propiedades={
            'usa_sympy': True,
            'notacion': 'lim[x→a] f(x)',
            'soporta': 'infinito',
            'habilidad_asociada': 'MAT_AVANZADA',
        }
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INFINITO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["infinito", "infinity", "∞", "tiende a infinito", "sin límite"],
        confianza_grounding=0.9,
        propiedades={'simbolo': '∞', 'no_es': 'número'}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CONTINUIDAD",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["continuidad", "continuous", "función continua", "es continua"],
        confianza_grounding=0.9,
        propiedades={'condicion': 'lim[x→a] f(x) = f(a)'}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SERIE_TAYLOR",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        # FIX-VOC-2: ampliado
        palabras_español=[
            "serie de taylor", "taylor series", "expansión de taylor",
            "taylor de", "serie taylor", "polinomio de taylor",
            "aproximación de taylor", "expansión taylor",
            "desarrollo de taylor", "taylor alrededor de",
        ],
        operaciones={
            'ejecutar': lambda expr, var='x', punto=0, orden=5:
                        calculadora.serie_taylor(expr, var, punto, orden)
                        if calculadora else None
        },
        confianza_grounding=1.0,
        propiedades={
            'usa_sympy': True,
            'aproxima': 'función como serie',
            'habilidad_asociada': 'MAT_AVANZADA',
        }
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SERIE",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["serie", "series", "suma infinita", "sucesión de sumas"],
        confianza_grounding=0.9,
        propiedades={'tipos': ['geométrica', 'armónica', 'potencias']}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CONVERGENCIA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["convergencia", "convergent", "converge", "converge a"],
        confianza_grounding=0.9,
        propiedades={'significa': 'tiende a un valor finito'}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DIVERGENCIA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["divergencia", "divergent", "diverge", "no converge"],
        confianza_grounding=0.9,
        propiedades={'significa': 'no converge a valor finito'}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_APROXIMACION",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["aproximación", "approximation", "valor aproximado", "aproximadamente"],
        confianza_grounding=0.9,
        propiedades={'metodos': ['Taylor', 'numérico', 'lineal']}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ASINTOTA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "asíntota", "asymptote", "asíntota vertical", "asíntota horizontal",
            "asíntota oblicua",
        ],
        confianza_grounding=0.9,
        propiedades={'es': 'línea a la que se acerca la función sin tocarla'}
    ))

    # ═══════════════════════════════════════════════════════
    # EVALUACIÓN Y ESTADÍSTICA (8 conceptos)
    # ═══════════════════════════════════════════════════════

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EVALUAR",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "evaluar", "evaluate", "calcular valor", "sustituir",
            "evalúa", "evalúa f(x)", "sustituye x", "valor de f en",
            "calcula f(", "plug in", "reemplaza x por", "f de",
        ],
        operaciones={
            'ejecutar': lambda expr, valores: calculadora.evaluar(expr, valores)
                        if calculadora else None
        },
        confianza_grounding=1.0,
        propiedades={
            'usa_sympy': True,
            'requiere': 'valores para variables',
            'habilidad_asociada': 'MAT_AVANZADA',
        }
    ))

    # NUEVO-V3: evaluar función
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EVALUAR_FUNCION",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "evalúa la función", "calcula f(x) en", "sustituye x=",
            "valor de la función en", "f evaluada en",
        ],
        confianza_grounding=0.9,
        propiedades={'habilidad_asociada': 'MAT_AVANZADA'}
    ))

    # NUEVO-V1: estadística ejecutable
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ESTADISTICA",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "estadística", "estadísticas de", "media de", "promedio de",
            "calcula la media", "calcula el promedio", "desviación estándar",
            "desviación típica", "varianza de", "mediana de", "moda de",
            "estadísticas descriptivas", "analiza los datos", "dispersión de",
            "distribución de", "calcula estadísticas", "analiza esta muestra",
            "calcula la desviación", "promedio aritmético",
        ],
        operaciones={
            'ejecutar': lambda datos: calculadora.estadisticas(datos)
                        if calculadora else None
        },
        confianza_grounding=1.0,
        propiedades={
            'usa_python': True,
            'calcula': ['media', 'mediana', 'moda', 'varianza', 'desv_est', 'min', 'max', 'rango', 'percentiles'],
            'habilidad_asociada': 'MAT_AVANZADA',
        }
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SUSTITUCION_AVANZADA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["sustitución", "substitution", "reemplazo", "reemplaza"],
        confianza_grounding=0.9,
        propiedades={'notacion': 'f(x)|[x=a]'}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_VARIABLE_MATEMATICA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["variable matemática", "incógnita", "x variable", "la x", "la y"],
        confianza_grounding=0.9,
        propiedades={'comunes': 'x, y, z, t, n'}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EXPRESION",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["expresión matemática", "expression", "fórmula", "la expresión"],
        confianza_grounding=0.9,
        propiedades={'tipos': ['numérica', 'algebraica', 'lógica']}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SIMBOLICO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["simbólico", "symbolic", "algebraico", "cálculo simbólico"],
        confianza_grounding=0.9,
        propiedades={'usa': 'símbolos en lugar de números'}
    ))

    # ═══════════════════════════════════════════════════════
    # ARITMÉTICA DISCRETA Y COMBINATORIA (7 conceptos)
    # ═══════════════════════════════════════════════════════

    # NUEVO-V6: MCD ejecutable
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MCD",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "mcd", "máximo común divisor", "m.c.d", "gcd",
            "máximo común divisor de", "mayor divisor común",
        ],
        operaciones={
            'ejecutar': lambda a, b: calculadora.mcd(a, b)
                        if calculadora else None
        },
        confianza_grounding=1.0,
        propiedades={
            'usa_python': True,
            'algoritmo': 'Euclides',
            'habilidad_asociada': 'MAT_AVANZADA',
        }
    ))

    # NUEVO-V7: MCM ejecutable
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MCM",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "mcm", "mínimo común múltiplo", "m.c.m", "lcm",
            "mínimo común múltiplo de", "menor múltiplo común",
        ],
        operaciones={
            'ejecutar': lambda a, b: calculadora.mcm(a, b)
                        if calculadora else None
        },
        confianza_grounding=1.0,
        propiedades={
            'usa_python': True,
            'habilidad_asociada': 'MAT_AVANZADA',
        }
    ))

    # NUEVO-V8: número primo ejecutable
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NUMERO_PRIMO",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "número primo", "es primo", "primo", "prime number",
            "verifica si es primo", "¿es primo?", "es número primo",
        ],
        operaciones={
            'ejecutar': lambda n: calculadora.es_primo(n)
                        if calculadora else None
        },
        confianza_grounding=1.0,
        propiedades={
            'usa_python': True,
            'habilidad_asociada': 'MAT_AVANZADA',
        }
    ))

    # NUEVO-V9: combinatoria ejecutable
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_COMBINATORIA",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "combinaciones", "combinaciones de", "C(n,r)", "nCr",
            "permutaciones", "permutaciones de", "P(n,r)", "nPr",
            "cuántas formas hay", "cuántas combinaciones", "cuántas permutaciones",
        ],
        operaciones={
            'ejecutar_combinaciones': lambda n, r: calculadora.combinaciones(n, r)
                                       if calculadora else None,
            'ejecutar_permutaciones': lambda n, r: calculadora.permutaciones(n, r)
                                       if calculadora else None,
        },
        confianza_grounding=1.0,
        propiedades={
            'usa_python': True,
            'habilidad_asociada': 'MAT_AVANZADA',
        }
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FACTORIAL",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["factorial", "n!", "factorial de", "producto de enteros"],
        confianza_grounding=0.9,
        propiedades={'formula': 'n! = n × (n-1) × ... × 1', 'base': '0! = 1'}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DIVISIBILIDAD",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "divisibilidad", "divisible", "múltiplo de", "divisor de",
            "divide a", "es divisible por",
        ],
        confianza_grounding=0.9,
        propiedades={'habilidad_asociada': 'MAT_AVANZADA'}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MODULO_ARITMETICO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "módulo aritmético", "aritmética modular", "congruencia",
            "resto de la división", "residuo",
        ],
        confianza_grounding=0.9,
        propiedades={'notacion': 'a ≡ b (mod n)'}
    ))

    # ═══════════════════════════════════════════════════════
    # FUNCIONES Y CONSTANTES (8 conceptos)
    # ═══════════════════════════════════════════════════════

    # NUEVO-V11: funciones trigonométricas
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FUNCION_TRIGONOMETRICA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "seno", "coseno", "tangente", "secante", "cosecante", "cotangente",
            "sin", "cos", "tan", "sec", "csc", "cot",
            "arcoseno", "arcocoseno", "arcotangente",
            "asin", "acos", "atan", "trigonometría", "trigonométrica",
            "función trigonométrica",
        ],
        confianza_grounding=0.9,
        propiedades={
            'unidades': 'radianes o grados',
            'habilidad_asociada': 'MAT_AVANZADA',
        }
    ))

    # NUEVO-V12: logaritmos
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LOGARITMO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "logaritmo", "logaritmo natural", "logaritmo en base",
            "log", "ln", "log base", "log de", "ln de",
            "logaritmo de", "logaritmo común",
        ],
        confianza_grounding=0.9,
        propiedades={
            'inversa_de': 'exponencial',
            'habilidad_asociada': 'MAT_AVANZADA',
        }
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PI",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["pi", "π", "3.14159", "número pi"],
        confianza_grounding=0.9,
        propiedades={'valor': '3.14159265...', 'es': 'razón circunferencia/diámetro'}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_E",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["e", "número de euler", "2.71828", "base natural"],
        confianza_grounding=0.9,
        propiedades={'valor': '2.71828...', 'es': 'base logaritmo natural'}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CONSTANTE",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["constante", "constant", "valor fijo", "constante matemática"],
        confianza_grounding=0.9,
        propiedades={'ejemplos': 'π, e, números'}
    ))

    # NUEVO-V13: número complejo
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NUMERO_COMPLEJO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "número complejo", "complex number", "parte imaginaria",
            "número imaginario", "i imaginario", "√-1",
        ],
        confianza_grounding=0.9,
        propiedades={
            'forma': 'a + bi',
            'unidad_imaginaria': 'i = √-1',
        }
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FUNCION_EXPONENCIAL",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "función exponencial", "exponencial", "e^x", "exp(x)",
            "crecimiento exponencial", "decaimiento exponencial",
        ],
        confianza_grounding=0.9,
        propiedades={'formula': 'f(x) = e^x', 'derivada': 'e^x'}
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FUNCION_LOGARITMICA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "función logarítmica", "función logarítmo", "log(x)", "ln(x)",
            "inversa de la exponencial",
        ],
        confianza_grounding=0.9,
        propiedades={'inversa_de': 'exponencial', 'dominio': 'x > 0'}
    ))

    return conceptos


# ═══════════════════════════════════════════════════════════════════════
# FUNCIÓN AUXILIAR
# ═══════════════════════════════════════════════════════════════════════

def obtener_concepto_por_palabra(palabra: str, conceptos: list = None):
    """Busca un concepto que corresponda a una palabra en español."""
    if conceptos is None:
        conceptos = obtener_conceptos_matematicas_avanzadas()
    palabra_lower = palabra.lower()
    for concepto in conceptos:
        if palabra_lower in [p.lower() for p in concepto.palabras_español]:
            return concepto
    return None


if __name__ == '__main__':
    conceptos = obtener_conceptos_matematicas_avanzadas()
    print(f"✅ Vocabulario Matemáticas Avanzadas v4.0: {len(conceptos)} conceptos")

    operativos = [c for c in conceptos if c.tipo.name == 'OPERACION_SISTEMA']
    abstractos = [c for c in conceptos if c.tipo.name == 'CONCEPTO_ABSTRACTO']
    grounding_1 = [c for c in conceptos if c.confianza_grounding == 1.0]

    print(f"   - Operativos (ejecutables): {len(operativos)}")
    print(f"   - Abstractos (vocabulario): {len(abstractos)}")
    print(f"   - Grounding 1.0: {len(grounding_1)}")
    print(f"   - Grounding promedio: {sum(c.confianza_grounding for c in conceptos) / len(conceptos):.2f}")
    print(f"\n   Conceptos operativos:")
    for c in operativos:
        print(f"     · {c.id}")