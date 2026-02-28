"""
Vocabulario de Análisis de Código - Semana 6 (Fase 3).

50 conceptos relacionados con análisis de código Python.
Grounding: 1.0 (Bell usa herramientas reales: ast, pylint)


VERSIÓN REFINADA v3:
- 3 duplicados corregidos automáticamente
- Listo para Groq whitelist
"""

from pathlib import Path
import sys

# Agregar path del proyecto
proyecto_path = Path(__file__).parent.parent
sys.path.insert(0, str(proyecto_path))

from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto

# Importar analizador (será inyectado en runtime)
python_analyzer = None


def configurar_analyzer(analyzer):
    """Configura el analizador para los conceptos."""
    global python_analyzer
    python_analyzer = analyzer


def obtener_conceptos_analisis():
    """
    Retorna 50 conceptos de análisis de código.
    
    Categorías:
    - AST y Parsing (10 conceptos)
    - Métricas de Código (10 conceptos)
    - Complejidad (8 conceptos)
    - Calidad de Código (10 conceptos)
    - Detección de Problemas (12 conceptos)
    """
    conceptos = []
    
    # ==================== AST Y PARSING (10) ====================
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ANALIZAR_CODIGO",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "analizar código", "parsear código", "analizar python",
            "revisar código", "inspeccionar código"
        ],
        operaciones={
            'ejecutar': lambda codigo: python_analyzer.analizar(codigo) 
                        if python_analyzer else None
        },
        confianza_grounding=1.0,
        propiedades={
            'usa_ast': True,
            'retorna': 'AnalysisResult',
            'puede_fallar': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_AST",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "ast", "abstract syntax tree", "árbol sintáctico",
            "árbol de sintaxis abstracta"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es_representacion': True,
            'de': 'código fuente',
            'permite': 'análisis estructural'
        },
        relaciones={
            'usado_por': ['CONCEPTO_ANALIZAR_CODIGO'],
            'tipo_de': ['ESTRUCTURA_DATOS']
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PARSEAR",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "parsear", "parse", "analizar sintaxis",
            "convertir a ast"
        ],
        confianza_grounding=1.0,
        propiedades={
            'entrada': 'código fuente',
            'salida': 'AST',
            'puede_lanzar': 'SyntaxError'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SYNTAX_ERROR",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "syntax error", "error de sintaxis", "error sintáctico",
            "sintaxis incorrecta"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es_error': True,
            'detectable_en': 'parsing',
            'impide': 'ejecución'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FUNCION_DEF",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["def", "definición función", "declarar función"],
        confianza_grounding=0.9,
        propiedades={
            'palabra_clave': 'def',
            'contiene': ['nombre', 'argumentos', 'cuerpo'],
            'puede_tener': 'docstring'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CLASS_DEF",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["class def", "definición de clase", "declarar clase"],
        confianza_grounding=0.9,
        propiedades={
            'palabra_clave': 'class',
            'contiene': ['nombre', 'métodos', 'atributos']
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_IMPORT_CODE",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["import statement", "importación", "from import"],
        confianza_grounding=0.9,
        propiedades={
            'trae': 'módulos externos',
            'tipos': ['import', 'from import'],
            'puede_tener': 'alias'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DOCSTRING",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "docstring", "documentation string", "cadena de documentación",
            "doc string"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'string literal',
            'ubicacion': 'primera línea función/clase',
            'proposito': 'documentación'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TYPE_HINTS",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "type hints", "type annotations", "anotaciones de tipo",
            "hints de tipo"
        ],
        confianza_grounding=0.9,
        propiedades={
            'introducido_en': 'Python 3.5',
            'proposito': 'indicar tipos',
            'opcional': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NODO_AST",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "nodo ast", "ast node", "nodo del árbol",
            "elemento ast"
        ],
        confianza_grounding=0.9,
        propiedades={
            'parte_de': 'AST',
            'representa': 'elemento sintáctico',
            'tipos': ['FunctionDef', 'ClassDef', 'If', 'For', 'etc']
        }
    ))
    
    # ==================== MÉTRICAS DE CÓDIGO (10) ====================
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CONTAR_FUNCIONES",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "contar funciones", "número de funciones", "cuántas funciones",
            "cantidad funciones"
        ],
        operaciones={
            'ejecutar': lambda arbol: python_analyzer._contar_funciones(arbol)
                        if python_analyzer else 0
        },
        confianza_grounding=1.0,
        propiedades={
            'metrica': True,
            'nivel': 'archivo'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CONTAR_CLASES",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "contar clases", "número de clases", "cuántas clases",
            "cantidad clases"
        ],
        operaciones={
            'ejecutar': lambda arbol: python_analyzer._contar_clases(arbol)
                        if python_analyzer else 0
        },
        confianza_grounding=1.0,
        propiedades={
            'metrica': True,
            'nivel': 'archivo'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LINEAS_CODIGO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "líneas de código", "loc", "lines of code",
            "cantidad de líneas"
        ],
        confianza_grounding=0.9,
        propiedades={
            'metrica': True,
            'tipo': 'tamaño',
            'unidad': 'líneas'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LINEAS_NO_VACIAS",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "líneas no vacías", "sloc", "líneas con código",
            "líneas efectivas"
        ],
        confianza_grounding=0.9,
        propiedades={
            'metrica': True,
            'excluye': 'líneas en blanco',
            'mas_preciso_que': 'LOC'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RATIO_COMENTARIOS",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "ratio de comentarios", "proporción comentarios",
            "comentarios vs código"
        ],
        confianza_grounding=0.9,
        propiedades={
            'metrica': True,
            'tipo': 'calidad',
            'formula': 'comentarios / código'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NOMBRE_FUNCION",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "nombre de función", "función llamada", "identificador función"
        ],
        confianza_grounding=0.9,
        propiedades={
            'tipo': 'identificador',
            'debe_ser': 'descriptivo',
            'convención': 'snake_case'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NOMBRE_CLASE",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "nombre de clase", "clase llamada", "identificador clase"
        ],
        confianza_grounding=0.9,
        propiedades={
            'tipo': 'identificador',
            'convención': 'PascalCase',
            'debe_ser': 'sustantivo'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ARGUMENTOS",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "argumentos", "parámetros", "args", "parameters"
        ],
        confianza_grounding=0.9,
        propiedades={
            'parte_de': 'función',
            'tipos': ['posicionales', '*args', '**kwargs'],
            'pueden_tener': 'valores por defecto'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RETURN_TYPE",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "tipo de retorno", "return type", "valor retornado"
        ],
        confianza_grounding=0.9,
        propiedades={
            'parte_de': 'función',
            'opcional_en': 'Python',
            'especificado_con': 'type hint'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_METODO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "método", "method", "función de clase"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'función dentro de clase',
            'primer_param': 'self',
            'tipos': ['instancia', 'clase', 'estático']
        }
    ))
    
    # ==================== COMPLEJIDAD (8) ====================
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_COMPLEJIDAD_CICLOMATICA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "complejidad ciclomática", "cyclomatic complexity",
            "complejidad de mccabe"
        ],
        confianza_grounding=1.0,
        propiedades={
            'metrica': True,
            'tipo': 'complejidad',
            'mide': 'número de caminos',
            'formula': '1 + decisiones'
        },
        relaciones={
            'medida_por': ['CONCEPTO_CALCULAR_COMPLEJIDAD']
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CALCULAR_COMPLEJIDAD",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "calcular complejidad", "medir complejidad",
            "obtener complejidad"
        ],
        operaciones={
            'ejecutar': lambda arbol: python_analyzer._calcular_complejidad(arbol)
                        if python_analyzer else 1
        },
        confianza_grounding=1.0,
        propiedades={
            'retorna': 'número',
            'cuenta': 'decisiones'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DECISION",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "decisión", "punto de decisión", "bifurcación",
            "branch point"
        ],
        confianza_grounding=0.9,
        propiedades={
            'incrementa': 'complejidad',
            'ejemplos': ['if', 'while', 'for', 'and', 'or']
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_IF_STATEMENT",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "if", "condicional", "if statement", "sentencia if"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'estructura de control',
            'tiene': 'condición',
            'puede_tener': 'elif, else',
            'incrementa_complejidad': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LOOP",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "loop", "bucle", "ciclo", "iteración"
        ],
        confianza_grounding=0.9,
        propiedades={
            'tipos': ['for', 'while'],
            'repite': 'código',
            'incrementa_complejidad': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_COMPREHENSION_CODE",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "comprehension", "comprensión de lista", "list comp",
            "comprensión"
        ],
        confianza_grounding=0.9,
        propiedades={
            'tipos': ['list', 'dict', 'set', 'generator'],
            'sintaxis_compacta': True,
            'incrementa_complejidad': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_BOOL_OP",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "operador booleano", "and", "or", "bool op"
        ],
        confianza_grounding=0.9,
        propiedades={
            'tipos': ['and', 'or'],
            'incrementa_complejidad': True,
            'en': 'condiciones'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_COMPLEJIDAD_ALTA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "complejidad alta", "código complejo", "alta complejidad"
        ],
        confianza_grounding=0.9,
        propiedades={
            'umbral': '> 10',
            'indica': 'refactorización necesaria',
            'dificil_de': 'mantener y testear'
        }
    ))
    
    # ==================== CALIDAD DE CÓDIGO (10) ====================
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_VARIABLE_SIN_USAR",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "variable sin usar", "unused variable", "variable no usada"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'code smell',
            'indica': 'código muerto',
            'debe': 'eliminarse'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_IMPORT_SIN_USAR",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "import sin usar", "unused import", "import no usado"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'code smell',
            'causa': 'imports innecesarios',
            'debe': 'eliminarse'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DOCSTRING_FALTANTE",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "sin docstring", "falta docstring", "docstring missing"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'mala práctica',
            'afecta': 'mantenibilidad',
            'recomendado': 'siempre agregar'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CODE_SMELL",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "code smell", "mal olor", "indicador de problema"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'síntoma',
            'indica': 'posible problema',
            'ejemplos': ['código duplicado', 'funciones largas']
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_REFACTORIZACION",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "refactorización", "refactoring", "refactorizar",
            "mejorar código"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'proceso',
            'mejora': 'estructura',
            'sin_cambiar': 'funcionalidad'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LINT",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "lint", "linting", "análisis estático", "linter"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'análisis automático',
            'detecta': 'errores y problemas',
            'herramientas': ['pylint', 'flake8']
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PEP8",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "pep8", "pep 8", "style guide", "guía de estilo"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'estándar',
            'para': 'Python',
            'define': 'convenciones de estilo'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MANTENIBILIDAD",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "mantenibilidad", "maintainability", "fácil de mantener"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'calidad',
            'afectada_por': ['complejidad', 'documentación'],
            'deseable': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LEGIBILIDAD",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "legibilidad", "readability", "fácil de leer"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'calidad',
            'mejorada_por': ['comentarios', 'nombres claros'],
            'muy_importante': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_BUENAS_PRACTICAS",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "buenas prácticas", "best practices", "prácticas recomendadas"
        ],
        confianza_grounding=0.9,
        propiedades={
            'son': 'convenciones',
            'mejoran': 'calidad',
            'incluyen': ['PEP8', 'docstrings', 'type hints']
        }
    ))
    
    # ==================== DETECCIÓN DE PROBLEMAS (12) ====================
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ENCONTRAR_VARIABLES_SIN_USAR",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "encontrar variables sin usar", "detectar variables no usadas"
        ],
        operaciones={
            'ejecutar': lambda arbol: python_analyzer._encontrar_variables_sin_usar(arbol)
                        if python_analyzer else []
        },
        confianza_grounding=1.0,
        propiedades={
            'retorna': 'lista',
            'detecta': 'código muerto'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ENCONTRAR_IMPORTS_SIN_USAR",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "encontrar imports sin usar", "detectar imports no usados"
        ],
        operaciones={
            'ejecutar': lambda arbol: python_analyzer._encontrar_imports_sin_usar(arbol)
                        if python_analyzer else []
        },
        confianza_grounding=1.0,
        propiedades={
            'retorna': 'lista',
            'limpia': 'imports innecesarios'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ENCONTRAR_DOCSTRINGS_FALTANTES",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "encontrar sin docstring", "funciones sin documentar"
        ],
        operaciones={
            'ejecutar': lambda arbol: python_analyzer._encontrar_docstrings_faltantes(arbol)
                        if python_analyzer else []
        },
        confianza_grounding=1.0,
        propiedades={
            'retorna': 'lista',
            'mejora': 'documentación'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ERROR",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "error", "fallo", "bug", "problema crítico"
        ],
        confianza_grounding=0.9,
        propiedades={
            'gravedad': 'alta',
            'impide': 'ejecución',
            'debe_corregirse': 'inmediatamente'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ADVERTENCIA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "advertencia", "warning", "aviso"
        ],
        confianza_grounding=0.9,
        propiedades={
            'gravedad': 'media',
            'no_impide': 'ejecución',
            'deberia_corregirse': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_VALIDACION",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "validación", "validation", "verificación"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'proceso',
            'verifica': 'corrección',
            'retorna': 'válido/inválido'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_REPORTE",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "reporte", "report", "informe", "resumen"
        ],
        confianza_grounding=0.9,
        propiedades={
            'contiene': 'resultados',
            'formato': 'legible',
            'incluye': ['métricas', 'errores', 'advertencias']
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_METRICAS",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "métricas", "metrics", "medidas", "estadísticas"
        ],
        confianza_grounding=0.9,
        propiedades={
            'son': 'mediciones',
            'cuantifican': 'características',
            'ejemplos': ['LOC', 'complejidad', 'cobertura']
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ANALISIS_ESTATICO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "análisis estático", "static analysis",
            "análisis sin ejecutar"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'análisis',
            'sin': 'ejecutar código',
            'detecta': 'problemas potenciales'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CODIGO_VALIDO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "código válido", "sintaxis correcta", "sin errores"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'estado',
            'sin': 'errores sintácticos',
            'puede_ejecutarse': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CODIGO_INVALIDO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "código inválido", "sintaxis incorrecta", "con errores"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'estado',
            'tiene': 'errores sintácticos',
            'no_puede_ejecutarse': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_GENERAR_REPORTE",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "generar reporte", "crear informe", "producir resumen"
        ],
        operaciones={
            'ejecutar': lambda resultado: python_analyzer.generar_reporte(resultado)
                        if python_analyzer else ""
        },
        confianza_grounding=1.0,
        propiedades={
            'retorna': 'string formateado',
            'incluye': 'todas las métricas'
        }
    ))
    
    return conceptos


# Función auxiliar
def obtener_concepto_por_palabra(palabra: str, conceptos: list = None):
    """Busca un concepto que corresponda a una palabra en español."""
    if conceptos is None:
        conceptos = obtener_conceptos_analisis()
    
    palabra_lower = palabra.lower()
    for concepto in conceptos:
        if palabra_lower in [p.lower() for p in concepto.palabras_español]:
            return concepto
    return None


if __name__ == '__main__':
    # Test básico
    conceptos = obtener_conceptos_analisis()
    print(f"✅ Vocabulario Análisis cargado: {len(conceptos)} conceptos")
    
    # Estadísticas
    con_grounding_1 = sum(1 for c in conceptos if c.confianza_grounding == 1.0)
    print(f"   - Grounding 1.0: {con_grounding_1}")
    print(f"   - Grounding promedio: {sum(c.confianza_grounding for c in conceptos) / len(conceptos):.2f}")