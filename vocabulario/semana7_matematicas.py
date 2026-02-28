"""
Vocabulario de Matemáticas Avanzadas - Semana 7 (Fase 3).

45 conceptos relacionados con matemáticas avanzadas usando SymPy.
Grounding: 1.0 (Bell usa SymPy real)


VERSIÓN REFINADA v3:
- 6 duplicados corregidos automáticamente
- Listo para Groq whitelist
"""

from pathlib import Path
import sys

# Agregar path del proyecto
proyecto_path = Path(__file__).parent.parent
sys.path.insert(0, str(proyecto_path))

from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto

# Importar calculadora (será inyectado en runtime)
calculadora = None


def configurar_calculadora(calc):
    """Configura la calculadora para los conceptos."""
    global calculadora
    calculadora = calc


def obtener_conceptos_matematicas_avanzadas():
    """
    Retorna 45 conceptos de matemáticas avanzadas.
    
    Categorías:
    - Derivadas (8 conceptos)
    - Integrales (8 conceptos)
    - Ecuaciones (7 conceptos)
    - Simplificación (6 conceptos)
    - Límites y Series (8 conceptos)
    - Evaluación (8 conceptos)
    """
    conceptos = []
    
    # ==================== DERIVADAS (8) ====================
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DERIVAR",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["derivar", "calcular derivada", "diferencial"],
        operaciones={
            'ejecutar': lambda expr, var='x': calculadora.derivar(expr, var)
                        if calculadora else None
        },
        confianza_grounding=1.0,
        propiedades={
            'usa_sympy': True,
            'retorna': 'ResultadoMatematico',
            'soporta_orden': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DERIVADA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["derivada", "derivative", "tasa de cambio"],
        confianza_grounding=0.9,
        propiedades={
            'es': 'operador',
            'mide': 'tasa de cambio',
            'notacion': "f'(x), dy/dx, d/dx"
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DERIVADA_PRIMERA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "primera derivada", "derivada de primer orden",
            "velocidad", "tasa de cambio"
        ],
        confianza_grounding=0.9,
        propiedades={
            'orden': 1,
            'notacion': "f'(x)",
            'representa': 'velocidad de cambio'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DERIVADA_SEGUNDA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "segunda derivada", "derivada de segundo orden",
            "aceleración", "concavidad"
        ],
        confianza_grounding=0.9,
        propiedades={
            'orden': 2,
            'notacion': "f''(x)",
            'representa': 'aceleración'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_REGLA_CADENA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "regla de la cadena", "chain rule",
            "derivada de composición"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'regla de derivación',
            'para': 'funciones compuestas',
            'formula': '(f∘g)\'(x) = f\'(g(x))·g\'(x)'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_REGLA_PRODUCTO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "regla del producto", "product rule",
            "derivada de producto"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'regla de derivación',
            'para': 'producto de funciones',
            'formula': '(f·g)\' = f\'·g + f·g\''
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_REGLA_COCIENTE",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "regla del cociente", "quotient rule",
            "derivada de cociente"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'regla de derivación',
            'para': 'cociente de funciones',
            'formula': '(f/g)\' = (f\'g - fg\')/g²'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DERIVADA_SIMBOLICA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "derivada simbólica", "symbolic derivative",
            "derivación simbólica"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'cálculo simbólico',
            'vs': 'derivada numérica',
            'resultado': 'expresión algebraica'
        }
    ))
    
    # ==================== INTEGRALES (8) ====================
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INTEGRAR",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["integrar", "calcular integral", "integración"],
        operaciones={
            'ejecutar': lambda expr, var='x', a=None, b=None: 
                        calculadora.integrar(expr, var, a, b)
                        if calculadora else None
        },
        confianza_grounding=1.0,
        propiedades={
            'usa_sympy': True,
            'retorna': 'ResultadoMatematico',
            'tipos': ['definida', 'indefinida']
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INTEGRAL",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["integral", "antiderivada", "primitiva"],
        confianza_grounding=0.9,
        propiedades={
            'es': 'operador',
            'inversa_de': 'derivada',
            'notacion': '∫f(x)dx'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INTEGRAL_DEFINIDA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "integral definida", "definite integral",
            "área bajo la curva"
        ],
        confianza_grounding=0.9,
        propiedades={
            'tiene': 'límites de integración',
            'resultado': 'número',
            'notacion': '∫[a,b] f(x)dx',
            'representa': 'área'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INTEGRAL_INDEFINIDA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "integral indefinida", "indefinite integral",
            "antiderivada", "primitiva"
        ],
        confianza_grounding=0.9,
        propiedades={
            'sin': 'límites',
            'resultado': 'función + C',
            'notacion': '∫f(x)dx',
            'constante': 'C'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CONSTANTE_INTEGRACION",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "constante de integración", "c", "constante arbitraria"
        ],
        confianza_grounding=0.9,
        propiedades={
            'simbolo': 'C',
            'aparece_en': 'integrales indefinidas',
            'razon': 'derivada de constante es 0'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TEOREMA_FUNDAMENTAL_CALCULO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "teorema fundamental del cálculo",
            "fundamental theorem of calculus"
        ],
        confianza_grounding=0.9,
        propiedades={
            'conecta': 'derivadas e integrales',
            'dice': '∫[a,b] f\'(x)dx = f(b) - f(a)'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SUSTITUCION",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "sustitución", "u-substitution",
            "cambio de variable"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'técnica de integración',
            'usa': 'regla de la cadena al revés'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INTEGRACION_POR_PARTES",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "integración por partes", "integration by parts"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'técnica de integración',
            'formula': '∫u dv = uv - ∫v du',
            'usa': 'regla del producto al revés'
        }
    ))
    
    # ==================== ECUACIONES (7) ====================
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RESOLVER_ECUACION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "resolver ecuación", "solve", "encontrar solución",
            "hallar raíces"
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
            'tipos': ['algebraicas', 'trascendentales']
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ECUACION_AVANZADA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "ecuación", "equation", "igualdad matemática"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'igualdad',
            'tiene': 'variables',
            'objetivo': 'encontrar valores que la satisfacen'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RAIZ_AVANZADA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "raíz", "root", "solución", "cero"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'valor que hace f(x) = 0',
            'tambien_llamado': 'cero de la función'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ECUACION_CUADRATICA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "ecuación cuadrática", "quadratic equation",
            "ecuación de segundo grado"
        ],
        confianza_grounding=0.9,
        propiedades={
            'forma': 'ax² + bx + c = 0',
            'formula': 'x = (-b ± √(b²-4ac))/2a',
            'max_soluciones': 2
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DISCRIMINANTE",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "discriminante", "discriminant"
        ],
        confianza_grounding=0.9,
        propiedades={
            'formula': 'b² - 4ac',
            'determina': 'número de raíces reales',
            'si_positivo': '2 raíces reales',
            'si_cero': '1 raíz doble',
            'si_negativo': '2 raíces complejas'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SISTEMA_ECUACIONES",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "sistema de ecuaciones", "system of equations",
            "ecuaciones simultáneas"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'conjunto de ecuaciones',
            'objetivo': 'encontrar valores que satisfacen todas',
            'metodos': ['sustitución', 'eliminación', 'matrices']
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ECUACION_DIFERENCIAL",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "ecuación diferencial", "differential equation",
            "ode"
        ],
        confianza_grounding=0.9,
        propiedades={
            'contiene': 'derivadas',
            'solucion': 'función',
            'tipos': ['ordinarias', 'parciales']
        }
    ))
    
    # ==================== SIMPLIFICACIÓN (6) ====================
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SIMPLIFICAR",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "simplificar", "simplify", "reducir expresión"
        ],
        operaciones={
            'ejecutar': lambda expr: calculadora.simplificar(expr)
                        if calculadora else None
        },
        confianza_grounding=1.0,
        propiedades={
            'usa_sympy': True,
            'retorna': 'expresión simplificada'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EXPANDIR",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "expandir", "expand", "desarrollar expresión"
        ],
        operaciones={
            'ejecutar': lambda expr: calculadora.expandir(expr)
                        if calculadora else None
        },
        confianza_grounding=1.0,
        propiedades={
            'usa_sympy': True,
            'ejemplo': '(x+1)² → x² + 2x + 1'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FACTORIZAR",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "factorizar", "factor", "factorear"
        ],
        operaciones={
            'ejecutar': lambda expr: calculadora.factorizar(expr)
                        if calculadora else None
        },
        confianza_grounding=1.0,
        propiedades={
            'usa_sympy': True,
            'ejemplo': 'x² - 4 → (x-2)(x+2)',
            'inversa_de': 'expandir'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FACTOR",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "factor", "divisor"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'término multiplicativo',
            'divide': 'expresión sin residuo'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TERMINO_COMUN",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "término común", "factor común",
            "common factor"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'factor presente en todos los términos',
            'se_extrae_en': 'factorización'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EXPRESION_ALGEBRAICA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "expresión algebraica", "algebraic expression"
        ],
        confianza_grounding=0.9,
        propiedades={
            'contiene': 'variables y operadores',
            'tipos': ['monomio', 'binomio', 'polinomio']
        }
    ))
    
    # ==================== LÍMITES Y SERIES (8) ====================
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LIMITE",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["límite matemático", "limit cálculo", "límite función"],
        operaciones={
            'ejecutar': lambda expr, var='x', punto=0: 
                        calculadora.limite(expr, var, punto)
                        if calculadora else None
        },
        confianza_grounding=1.0,
        propiedades={
            'usa_sympy': True,
            'notacion': 'lim[x→a] f(x)',
            'soporta': 'infinito'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INFINITO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "infinito", "infinity", "∞"
        ],
        confianza_grounding=0.9,
        propiedades={
            'simbolo': '∞',
            'no_es': 'número',
            'representa': 'sin límite'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CONTINUIDAD",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "continuidad", "continuous", "función continua"
        ],
        confianza_grounding=0.9,
        propiedades={
            'significa': 'sin saltos ni huecos',
            'condicion': 'lim[x→a] f(x) = f(a)'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SERIE_TAYLOR",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "serie de taylor", "taylor series",
            "expansión de taylor"
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
            'alrededor_de': 'punto'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SERIE",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "serie", "series", "suma infinita"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'suma de términos',
            'puede_ser': 'infinita',
            'tipos': ['geométrica', 'armónica', 'potencias']
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CONVERGENCIA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "convergencia", "convergent", "converge"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'propiedad de serie/secuencia',
            'significa': 'tiende a un valor finito'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DIVERGENCIA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "divergencia", "divergent", "diverge"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'propiedad de serie/secuencia',
            'significa': 'no converge a valor finito'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_APROXIMACION",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "aproximación", "approximation", "valor aproximado"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'valor cercano',
            'metodos': ['Taylor', 'numérico', 'lineal']
        }
    ))
    
    # ==================== EVALUACIÓN (8) ====================
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EVALUAR",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "evaluar", "evaluate", "calcular valor",
            "sustituir"
        ],
        operaciones={
            'ejecutar': lambda expr, valores: 
                        calculadora.evaluar(expr, valores)
                        if calculadora else None
        },
        confianza_grounding=1.0,
        propiedades={
            'usa_sympy': True,
            'requiere': 'valores para variables',
            'retorna': 'número'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SUSTITUCION_AVANZADA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "sustitución", "substitution", "reemplazo"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'reemplazar variable por valor',
            'notacion': 'f(x)|[x=a]'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_VARIABLE_MATEMATICA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["variable matemática", "incógnita", "x variable"],
        confianza_grounding=0.9,
        propiedades={
            'es': 'símbolo que representa valor',
            'comunes': 'x, y, z, t, n'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CONSTANTE",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "constante", "constant", "valor fijo"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'valor que no cambia',
            'ejemplos': 'π, e, números'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PI",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "pi", "π", "3.14159"
        ],
        confianza_grounding=0.9,
        propiedades={
            'simbolo': 'π',
            'valor': '3.14159265...',
            'es': 'razón circunferencia/diámetro'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_E",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "e", "número de euler", "2.71828"
        ],
        confianza_grounding=0.9,
        propiedades={
            'simbolo': 'e',
            'valor': '2.71828...',
            'es': 'base logaritmo natural'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EXPRESION",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "expresión matemática", "expression",
            "fórmula"
        ],
        confianza_grounding=0.9,
        propiedades={
            'contiene': 'números, variables, operadores',
            'tipos': ['numérica', 'algebraica', 'lógica']
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SIMBOLICO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "simbólico", "symbolic", "algebraico"
        ],
        confianza_grounding=0.9,
        propiedades={
            'usa': 'símbolos en lugar de números',
            'vs': 'numérico',
            'permite': 'manipulación algebraica exacta'
        }
    ))
    
    return conceptos


# Función auxiliar
def obtener_concepto_por_palabra(palabra: str, conceptos: list = None):
    """Busca un concepto que corresponda a una palabra en español."""
    if conceptos is None:
        conceptos = obtener_conceptos_matematicas()
    
    palabra_lower = palabra.lower()
    for concepto in conceptos:
        if palabra_lower in [p.lower() for p in concepto.palabras_español]:
            return concepto
    return None


if __name__ == '__main__':
    # Test básico
    conceptos = obtener_conceptos_matematicas_avanzadas()
    print(f"✅ Vocabulario Matemáticas cargado: {len(conceptos)} conceptos")
    
    # Estadísticas
    con_grounding_1 = sum(1 for c in conceptos if c.confianza_grounding == 1.0)
    print(f"   - Grounding 1.0: {con_grounding_1}")
    print(f"   - Grounding promedio: {sum(c.confianza_grounding for c in conceptos) / len(conceptos):.2f}")