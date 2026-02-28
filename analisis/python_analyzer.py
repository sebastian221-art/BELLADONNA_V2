"""
Analizador de código Python usando AST.
FASE 3 - Semana 3-4
"""

import ast
import sys
from typing import Dict, List, Optional, Set
from pathlib import Path
from dataclasses import dataclass


@dataclass
class AnalysisResult:
    """Resultado del análisis de código."""
    valido: bool
    errores: List[str]
    advertencias: List[str]
    metricas: Dict
    
    def es_exitoso(self) -> bool:
        """Retorna True si no hay errores críticos."""
        return self.valido and len(self.errores) == 0


class PythonAnalyzer:
    """
    Analizador de código Python usando AST (Abstract Syntax Tree).
    
    Capacidades:
    - Parsear código Python
    - Contar funciones, clases, imports
    - Calcular complejidad ciclomática
    - Detectar variables sin usar
    - Detectar imports sin usar
    - Encontrar docstrings faltantes
    - Análisis de líneas de código
    """
    
    def __init__(self):
        """Inicializa el analizador."""
        self.ultimo_arbol = None
        self.ultimo_codigo = None
    
    def analizar(self, codigo: str, ruta: str = '<string>') -> AnalysisResult:
        """
        Analiza código fuente Python.
        
        Args:
            codigo: Código fuente a analizar
            ruta: Ruta del archivo (para mensajes de error)
            
        Returns:
            AnalysisResult con resultados del análisis
        """
        errores = []
        advertencias = []
        metricas = {}
        
        # 1. Parsear código
        try:
            arbol = ast.parse(codigo, filename=ruta)
            self.ultimo_arbol = arbol
            self.ultimo_codigo = codigo
            valido = True
        except SyntaxError as e:
            errores.append(f"Error de sintaxis en línea {e.lineno}: {e.msg}")
            return AnalysisResult(
                valido=False,
                errores=errores,
                advertencias=[],
                metricas={'error': str(e)}
            )
        except Exception as e:
            errores.append(f"Error al parsear código: {str(e)}")
            return AnalysisResult(
                valido=False,
                errores=errores,
                advertencias=[],
                metricas={'error': str(e)}
            )
        
        # 2. Extraer métricas básicas
        metricas['funciones'] = self._contar_funciones(arbol)
        metricas['clases'] = self._contar_clases(arbol)
        metricas['imports'] = self._extraer_imports(arbol)
        metricas['lineas_codigo'] = codigo.count('\n') + 1
        metricas['lineas_no_vacias'] = len([l for l in codigo.split('\n') if l.strip()])
        
        # 3. Calcular complejidad
        metricas['complejidad_ciclomatica'] = self._calcular_complejidad(arbol)
        metricas['complejidad_promedio'] = (
            metricas['complejidad_ciclomatica'] / max(metricas['funciones'], 1)
        )
        
        # 4. Detectar problemas
        variables_sin_usar = self._encontrar_variables_sin_usar(arbol)
        if variables_sin_usar:
            advertencias.append(f"Variables sin usar: {', '.join(variables_sin_usar)}")
            metricas['variables_sin_usar'] = variables_sin_usar
        
        imports_sin_usar = self._encontrar_imports_sin_usar(arbol)
        if imports_sin_usar:
            advertencias.append(f"Imports sin usar: {', '.join(imports_sin_usar)}")
            metricas['imports_sin_usar'] = imports_sin_usar
        
        docstrings_faltantes = self._encontrar_docstrings_faltantes(arbol)
        if docstrings_faltantes:
            advertencias.append(
                f"Funciones sin docstring: {', '.join(docstrings_faltantes)}"
            )
            metricas['sin_docstring'] = docstrings_faltantes
        
        # 5. Análisis adicional
        metricas['usa_type_hints'] = self._usa_type_hints(arbol)
        metricas['tiene_tests'] = self._tiene_tests(arbol)
        metricas['ratio_comentarios'] = self._calcular_ratio_comentarios(codigo)
        
        return AnalysisResult(
            valido=valido,
            errores=errores,
            advertencias=advertencias,
            metricas=metricas
        )
    
    def analizar_archivo(self, ruta: Path) -> AnalysisResult:
        """
        Analiza un archivo Python.
        
        Args:
            ruta: Path al archivo .py
            
        Returns:
            AnalysisResult
        """
        if not ruta.exists():
            return AnalysisResult(
                valido=False,
                errores=[f"Archivo no encontrado: {ruta}"],
                advertencias=[],
                metricas={}
            )
        
        try:
            codigo = ruta.read_text(encoding='utf-8')
            return self.analizar(codigo, str(ruta))
        except Exception as e:
            return AnalysisResult(
                valido=False,
                errores=[f"Error al leer archivo: {str(e)}"],
                advertencias=[],
                metricas={}
            )
    
    def _contar_funciones(self, arbol: ast.AST) -> int:
        """Cuenta funciones en el árbol."""
        return sum(1 for node in ast.walk(arbol) 
                   if isinstance(node, ast.FunctionDef))
    
    def _contar_clases(self, arbol: ast.AST) -> int:
        """Cuenta clases en el árbol."""
        return sum(1 for node in ast.walk(arbol) 
                   if isinstance(node, ast.ClassDef))
    
    def _extraer_imports(self, arbol: ast.AST) -> List[str]:
        """Extrae nombres de imports."""
        imports = []
        for node in ast.walk(arbol):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    imports.append(f"{module}.{alias.name}" if module else alias.name)
        return imports
    
    def _calcular_complejidad(self, arbol: ast.AST) -> int:
        """
        Calcula complejidad ciclomática.
        
        Complejidad = 1 (base) + número de decisiones
        Decisiones: if, while, for, except, with, and, or, comprehensions
        """
        complejidad = 1  # Base
        
        for node in ast.walk(arbol):
            # Estructuras de control
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complejidad += 1
            
            # Excepciones
            elif isinstance(node, ast.ExceptHandler):
                complejidad += 1
            
            # Context managers
            elif isinstance(node, (ast.With, ast.AsyncWith)):
                complejidad += 1
            
            # Operadores booleanos
            elif isinstance(node, ast.BoolOp):
                # and/or agregan complejidad
                complejidad += len(node.values) - 1
            
            # Comprehensions
            elif isinstance(node, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
                complejidad += 1
        
        return complejidad
    
    def _encontrar_variables_sin_usar(self, arbol: ast.AST) -> List[str]:
        """
        Encuentra variables asignadas pero nunca usadas.
        
        Nota: Análisis simplificado, puede tener falsos positivos.
        """
        asignadas = set()
        usadas = set()
        
        for node in ast.walk(arbol):
            # Variables asignadas
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        asignadas.add(target.id)
            
            # Variables usadas
            elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                usadas.add(node.id)
        
        # Filtrar variables privadas y especiales
        sin_usar = asignadas - usadas
        sin_usar = {v for v in sin_usar if not v.startswith('_')}
        
        return sorted(list(sin_usar))
    
    def _encontrar_imports_sin_usar(self, arbol: ast.AST) -> List[str]:
        """
        Encuentra imports que no se usan.
        
        Nota: Análisis simplificado.
        """
        imports_nombres = set()
        nombres_usados = set()
        
        # Recopilar imports
        for node in ast.walk(arbol):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    nombre = alias.asname if alias.asname else alias.name.split('.')[0]
                    imports_nombres.add(nombre)
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    nombre = alias.asname if alias.asname else alias.name
                    imports_nombres.add(nombre)
        
        # Recopilar nombres usados
        for node in ast.walk(arbol):
            if isinstance(node, ast.Name):
                nombres_usados.add(node.id)
            elif isinstance(node, ast.Attribute):
                # Para casos como "os.path"
                if isinstance(node.value, ast.Name):
                    nombres_usados.add(node.value.id)
        
        sin_usar = imports_nombres - nombres_usados
        return sorted(list(sin_usar))
    
    def _encontrar_docstrings_faltantes(self, arbol: ast.AST) -> List[str]:
        """Encuentra funciones sin docstring."""
        sin_docstring = []
        
        for node in ast.walk(arbol):
            if isinstance(node, ast.FunctionDef):
                # Verificar si tiene docstring
                docstring = ast.get_docstring(node)
                if not docstring:
                    sin_docstring.append(node.name)
        
        return sin_docstring
    
    def _usa_type_hints(self, arbol: ast.AST) -> bool:
        """Verifica si el código usa type hints."""
        for node in ast.walk(arbol):
            if isinstance(node, ast.FunctionDef):
                # Verificar argumentos con anotaciones
                if node.args.args:
                    for arg in node.args.args:
                        if arg.annotation:
                            return True
                # Verificar return type
                if node.returns:
                    return True
        return False
    
    def _tiene_tests(self, arbol: ast.AST) -> bool:
        """Verifica si el archivo parece contener tests."""
        for node in ast.walk(arbol):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                nombre = node.name.lower()
                if nombre.startswith('test_') or 'test' in nombre:
                    return True
        return False
    
    def _calcular_ratio_comentarios(self, codigo: str) -> float:
        """Calcula ratio de líneas con comentarios."""
        lineas = codigo.split('\n')
        lineas_con_codigo = [l for l in lineas if l.strip() and not l.strip().startswith('#')]
        lineas_comentario = [l for l in lineas if l.strip().startswith('#')]
        
        if not lineas_con_codigo:
            return 0.0
        
        return len(lineas_comentario) / len(lineas_con_codigo)
    
    def obtener_nombres_funciones(self) -> List[str]:
        """Obtiene lista de nombres de funciones del último análisis."""
        if not self.ultimo_arbol:
            return []
        
        nombres = []
        for node in ast.walk(self.ultimo_arbol):
            if isinstance(node, ast.FunctionDef):
                nombres.append(node.name)
        return nombres
    
    def obtener_nombres_clases(self) -> List[str]:
        """Obtiene lista de nombres de clases del último análisis."""
        if not self.ultimo_arbol:
            return []
        
        nombres = []
        for node in ast.walk(self.ultimo_arbol):
            if isinstance(node, ast.ClassDef):
                nombres.append(node.name)
        return nombres
    
    def generar_reporte(self, resultado: AnalysisResult) -> str:
        """
        Genera reporte legible del análisis.
        
        Args:
            resultado: AnalysisResult del análisis
            
        Returns:
            String con reporte formateado
        """
        lineas = []
        lineas.append("=" * 60)
        lineas.append("REPORTE DE ANÁLISIS DE CÓDIGO")
        lineas.append("=" * 60)
        
        # Estado
        if resultado.valido:
            lineas.append("\n✅ Código válido (sin errores de sintaxis)")
        else:
            lineas.append("\n❌ Código inválido")
        
        # Errores
        if resultado.errores:
            lineas.append("\n🔴 ERRORES:")
            for error in resultado.errores:
                lineas.append(f"  - {error}")
        
        # Advertencias
        if resultado.advertencias:
            lineas.append("\n⚠️  ADVERTENCIAS:")
            for advertencia in resultado.advertencias:
                lineas.append(f"  - {advertencia}")
        
        # Métricas
        if resultado.metricas:
            lineas.append("\n📊 MÉTRICAS:")
            m = resultado.metricas
            
            if 'funciones' in m:
                lineas.append(f"  • Funciones: {m['funciones']}")
            if 'clases' in m:
                lineas.append(f"  • Clases: {m['clases']}")
            if 'lineas_codigo' in m:
                lineas.append(f"  • Líneas de código: {m['lineas_codigo']}")
            if 'lineas_no_vacias' in m:
                lineas.append(f"  • Líneas no vacías: {m['lineas_no_vacias']}")
            if 'complejidad_ciclomatica' in m:
                lineas.append(f"  • Complejidad ciclomática: {m['complejidad_ciclomatica']}")
            if 'complejidad_promedio' in m:
                lineas.append(f"  • Complejidad promedio: {m['complejidad_promedio']:.2f}")
            if 'usa_type_hints' in m:
                lineas.append(f"  • Usa type hints: {'Sí' if m['usa_type_hints'] else 'No'}")
            if 'tiene_tests' in m:
                lineas.append(f"  • Tiene tests: {'Sí' if m['tiene_tests'] else 'No'}")
            if 'ratio_comentarios' in m:
                lineas.append(f"  • Ratio comentarios: {m['ratio_comentarios']:.2%}")
        
        lineas.append("\n" + "=" * 60)
        
        return '\n'.join(lineas)


# Ejemplo de uso
if __name__ == '__main__':
    analyzer = PythonAnalyzer()
    
    # Código de ejemplo
    codigo_ejemplo = '''
def calcular_factorial(n):
    """Calcula el factorial de n."""
    if n <= 1:
        return 1
    return n * calcular_factorial(n - 1)

def funcion_sin_usar():
    x = 5
    y = 10
    return x

class MiClase:
    def metodo(self):
        pass
'''
    
    resultado = analyzer.analizar(codigo_ejemplo)
    print(analyzer.generar_reporte(resultado))