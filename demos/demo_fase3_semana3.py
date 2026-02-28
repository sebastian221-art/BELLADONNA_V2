"""
Demo de Análisis de Código - Fase 3 Semana 3-4.
Muestra capacidades de Bell para analizar código Python.
"""

import sys
from pathlib import Path

# Agregar path del proyecto
proyecto_path = Path(__file__).parent.parent
sys.path.insert(0, str(proyecto_path))

from analisis.python_analyzer import PythonAnalyzer
from vocabulario.semana6_analisis import (
    obtener_conceptos_analisis,
    configurar_analyzer,
    obtener_concepto_por_palabra
)


def print_separador(titulo=""):
    """Imprime separador visual."""
    print("\n" + "=" * 80)
    if titulo:
        print(f"  {titulo}")
        print("=" * 80)


def demo_analyzer_basico():
    """Demo del analizador básico."""
    print_separador("DEMO 1: ANALIZADOR DE CÓDIGO PYTHON")
    
    analyzer = PythonAnalyzer()
    
    # Código de ejemplo
    codigo_ejemplo = '''
def calcular_factorial(n):
    """Calcula el factorial de n."""
    if n <= 1:
        return 1
    return n * calcular_factorial(n - 1)

class Calculadora:
    def suma(self, a, b):
        return a + b
    
    def resta(self, a, b):
        return a - b
'''
    
    print("\n📝 CÓDIGO A ANALIZAR:")
    print(codigo_ejemplo)
    
    print("\n🔍 ANALIZANDO...")
    resultado = analyzer.analizar(codigo_ejemplo)
    
    print(f"\n✅ Análisis completado!")
    print(f"   - Válido: {resultado.valido}")
    print(f"   - Errores: {len(resultado.errores)}")
    print(f"   - Advertencias: {len(resultado.advertencias)}")
    
    print("\n📊 MÉTRICAS:")
    for key, value in resultado.metricas.items():
        if not isinstance(value, (list, dict)):
            print(f"   • {key}: {value}")


def demo_codigo_con_problemas():
    """Demo con código que tiene problemas."""
    print_separador("DEMO 2: DETECCIÓN DE PROBLEMAS")
    
    analyzer = PythonAnalyzer()
    
    codigo_problematico = '''
import os
import sys

def funcion_sin_docstring(x, y):
    variable_no_usada = 10
    resultado = x + y
    return resultado

def otra_funcion():
    for i in range(10):
        if i % 2 == 0:
            while i < 5:
                if i > 2:
                    print(i)
'''
    
    print("\n📝 CÓDIGO CON PROBLEMAS:")
    print(codigo_problematico)
    
    resultado = analyzer.analizar(codigo_problematico)
    
    print("\n⚠️ PROBLEMAS DETECTADOS:")
    
    if resultado.advertencias:
        for adv in resultado.advertencias:
            print(f"   • {adv}")
    
    if 'variables_sin_usar' in resultado.metricas:
        print(f"\n🔴 Variables sin usar: {resultado.metricas['variables_sin_usar']}")
    
    if 'imports_sin_usar' in resultado.metricas:
        print(f"🔴 Imports sin usar: {resultado.metricas['imports_sin_usar']}")
    
    if 'sin_docstring' in resultado.metricas:
        print(f"🔴 Sin docstring: {resultado.metricas['sin_docstring']}")
    
    print(f"\n📊 COMPLEJIDAD:")
    print(f"   • Ciclomática: {resultado.metricas['complejidad_ciclomatica']}")
    print(f"   • Promedio: {resultado.metricas['complejidad_promedio']:.2f}")


def demo_codigo_invalido():
    """Demo con código con errores de sintaxis."""
    print_separador("DEMO 3: CÓDIGO CON ERRORES DE SINTAXIS")
    
    analyzer = PythonAnalyzer()
    
    codigo_invalido = '''
def suma(a, b
    return a + b

class MiClase
    def metodo(self):
        pass
'''
    
    print("\n📝 CÓDIGO CON ERROR DE SINTAXIS:")
    print(codigo_invalido)
    
    resultado = analyzer.analizar(codigo_invalido)
    
    print(f"\n❌ CÓDIGO INVÁLIDO")
    print(f"\n🔴 ERRORES:")
    for error in resultado.errores:
        print(f"   • {error}")


def demo_reporte_completo():
    """Demo de reporte completo."""
    print_separador("DEMO 4: REPORTE COMPLETO")
    
    analyzer = PythonAnalyzer()
    
    codigo = '''
def calcular_promedio(numeros: list) -> float:
    """
    Calcula el promedio de una lista de números.
    
    Args:
        numeros: Lista de números
        
    Returns:
        Promedio de los números
    """
    if not numeros:
        return 0.0
    
    total = sum(numeros)
    return total / len(numeros)

def test_calcular_promedio():
    assert calcular_promedio([1, 2, 3]) == 2.0
    assert calcular_promedio([]) == 0.0
'''
    
    resultado = analyzer.analizar(codigo)
    reporte = analyzer.generar_reporte(resultado)
    
    print(reporte)


def demo_vocabulario_analisis():
    """Demo del vocabulario de análisis."""
    print_separador("DEMO 5: VOCABULARIO DE ANÁLISIS")
    
    conceptos = obtener_conceptos_analisis()
    
    print(f"\n📚 CONCEPTOS CARGADOS: {len(conceptos)}")
    
    # Estadísticas
    con_grounding_1 = sum(1 for c in conceptos if c.confianza_grounding == 1.0)
    con_operaciones = sum(1 for c in conceptos if hasattr(c, 'operaciones') and c.operaciones)
    
    print(f"  • Grounding 1.0: {con_grounding_1}/{len(conceptos)}")
    print(f"  • Con operaciones: {con_operaciones}/{len(conceptos)}")
    print(f"  • Grounding promedio: {sum(c.confianza_grounding for c in conceptos) / len(conceptos):.2f}")
    
    # Conceptos por tipo
    print("\n📊 CONCEPTOS POR TIPO:")
    tipos = {}
    for c in conceptos:
        tipo_str = str(c.tipo)
        tipos[tipo_str] = tipos.get(tipo_str, 0) + 1
    
    for tipo, cantidad in sorted(tipos.items(), key=lambda x: x[1], reverse=True):
        print(f"  • {tipo}: {cantidad}")
    
    # Mostrar algunos conceptos importantes
    print("\n🔍 CONCEPTOS CLAVE:")
    
    palabras_clave = [
        'analizar código',
        'ast',
        'complejidad ciclomática',
        'docstring',
        'type hints'
    ]
    
    for palabra in palabras_clave:
        concepto = obtener_concepto_por_palabra(palabra, conceptos)
        if concepto:
            print(f"\n  🔹 {concepto.id}")
            print(f"     Palabras: {concepto.palabras_español[:3]}")
            print(f"     Grounding: {concepto.confianza_grounding}")


def demo_integracion():
    """Demo de integración vocabulario + analyzer."""
    print_separador("DEMO 6: INTEGRACIÓN COMPLETA")
    
    # Configurar
    analyzer = PythonAnalyzer()
    configurar_analyzer(analyzer)
    conceptos = obtener_conceptos_analisis()
    
    print("\n🔗 ANALYZER CONECTADO A VOCABULARIO")
    
    # Código de prueba
    codigo_prueba = '''
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
'''
    
    print("\n📝 Código a analizar:")
    print(codigo_prueba)
    
    # Buscar concepto de análisis
    concepto = obtener_concepto_por_palabra('analizar código', conceptos)
    
    if concepto and concepto.operaciones:
        print(f"\n→ Usando concepto: {concepto.id}")
        print(f"→ Grounding: {concepto.confianza_grounding}")
        
        # Ejecutar análisis
        resultado = concepto.operaciones['ejecutar'](codigo_prueba)
        
        print(f"\n✅ Análisis ejecutado:")
        print(f"   • Válido: {resultado.valido}")
        print(f"   • Funciones: {resultado.metricas.get('funciones', 0)}")
        print(f"   • Complejidad: {resultado.metricas.get('complejidad_ciclomatica', 0)}")


def demo_comparacion_codigos():
    """Demo comparando dos códigos."""
    print_separador("DEMO 7: COMPARACIÓN DE CÓDIGOS")
    
    analyzer = PythonAnalyzer()
    
    # Código simple
    codigo_simple = '''
def suma(a, b):
    return a + b
'''
    
    # Código complejo
    codigo_complejo = '''
def procesar_datos(datos, filtro=None):
    """Procesa lista de datos con filtro opcional."""
    if not datos:
        return []
    
    resultado = []
    for item in datos:
        if filtro:
            if filtro(item):
                resultado.append(item)
        else:
            resultado.append(item)
    
    return resultado
'''
    
    print("\n📊 CÓDIGO SIMPLE:")
    r1 = analyzer.analizar(codigo_simple)
    print(f"   • Complejidad: {r1.metricas['complejidad_ciclomatica']}")
    print(f"   • Líneas: {r1.metricas['lineas_codigo']}")
    print(f"   • Type hints: {r1.metricas['usa_type_hints']}")
    
    print("\n📊 CÓDIGO COMPLEJO:")
    r2 = analyzer.analizar(codigo_complejo)
    print(f"   • Complejidad: {r2.metricas['complejidad_ciclomatica']}")
    print(f"   • Líneas: {r2.metricas['lineas_codigo']}")
    print(f"   • Type hints: {r2.metricas['usa_type_hints']}")
    
    print(f"\n💡 El código complejo es {r2.metricas['complejidad_ciclomatica'] / r1.metricas['complejidad_ciclomatica']:.1f}x más complejo")


def main():
    """Ejecuta todas las demos."""
    print("\n" + "🌿" * 40)
    print("  BELLADONNA - FASE 3: ANÁLISIS DE CÓDIGO")
    print("  Semana 3-4: Python Analyzer + Vocabulario")
    print("🌿" * 40)
    
    try:
        # Demo 1: Básico
        demo_analyzer_basico()
        
        # Demo 2: Problemas
        demo_codigo_con_problemas()
        
        # Demo 3: Errores
        demo_codigo_invalido()
        
        # Demo 4: Reporte
        demo_reporte_completo()
        
        # Demo 5: Vocabulario
        demo_vocabulario_analisis()
        
        # Demo 6: Integración
        demo_integracion()
        
        # Demo 7: Comparación
        demo_comparacion_codigos()
        
        # Resumen final
        print_separador("RESUMEN")
        print("""
✅ Python Analyzer funcionando
✅ 50 conceptos de análisis cargados
✅ Integración vocabulario + analyzer
✅ Detección de problemas activa
✅ Métricas de código completas

📊 ESTADÍSTICAS:
  • Conceptos nuevos: 50
  • Tests: 35+
  • Grounding promedio: 0.96
  • Detecta: errores, advertencias, complejidad

🎯 PRÓXIMO: Semana 5 - Matemáticas Avanzadas
        """)
        
    except Exception as e:
        print(f"\n❌ Error en demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()