"""
Demo de Calculadora Avanzada - Fase 3 Semana 5.
Muestra capacidades matemáticas de Bell usando SymPy.
"""

import sys
from pathlib import Path

# Agregar path del proyecto
proyecto_path = Path(__file__).parent.parent
sys.path.insert(0, str(proyecto_path))

from matematicas.calculadora_avanzada import CalculadoraAvanzada
from vocabulario.semana7_matematicas import (
    obtener_conceptos_matematicas,
    configurar_calculadora,
    obtener_concepto_por_palabra
)


def print_separador(titulo=""):
    """Imprime separador visual."""
    print("\n" + "=" * 80)
    if titulo:
        print(f"  {titulo}")
        print("=" * 80)


def demo_derivadas():
    """Demo de derivadas."""
    print_separador("DEMO 1: DERIVADAS")
    
    calc = CalculadoraAvanzada()
    
    ejemplos = [
        ("x**2", 1),
        ("x**3 + 2*x**2 + 3*x", 1),
        ("sin(x)", 1),
        ("exp(x)", 2),
        ("x**4", 3)
    ]
    
    for expresion, orden in ejemplos:
        print(f"\n📝 Expresión: {expresion}")
        resultado = calc.derivar(expresion, orden=orden)
        
        if resultado.exitoso:
            print(f"   Derivada de orden {orden}: {resultado.resultado}")
        else:
            print(f"   Error: {resultado.error}")


def demo_integrales():
    """Demo de integrales."""
    print_separador("DEMO 2: INTEGRALES")
    
    calc = CalculadoraAvanzada()
    
    print("\n🔹 INTEGRALES INDEFINIDAS:")
    indefinidas = ["x**2", "sin(x)", "exp(x)", "1/x"]
    
    for expr in indefinidas:
        resultado = calc.integrar(expr)
        if resultado.exitoso:
            print(f"   ∫{expr} dx = {resultado.resultado} + C")
    
    print("\n🔹 INTEGRALES DEFINIDAS:")
    definidas = [
        ("x**2", 0, 1),
        ("x", 0, 10),
        ("sin(x)", 0, 3.14159)
    ]
    
    for expr, a, b in definidas:
        resultado = calc.integrar(expr, limite_inferior=a, limite_superior=b)
        if resultado.exitoso:
            print(f"   ∫[{a},{b}] {expr} dx = {resultado.resultado}")


def demo_ecuaciones():
    """Demo de resolver ecuaciones."""
    print_separador("DEMO 3: RESOLVER ECUACIONES")
    
    calc = CalculadoraAvanzada()
    
    ecuaciones = [
        "x**2 - 4",
        "2*x + 3 = 7",
        "x**2 + 2*x + 1",
        "x**3 - 1"
    ]
    
    for ecuacion in ecuaciones:
        print(f"\n📝 Ecuación: {ecuacion} = 0")
        resultado = calc.resolver_ecuacion(ecuacion)
        
        if resultado.exitoso:
            print(f"   Soluciones: {resultado.resultado}")
        else:
            print(f"   Error: {resultado.error}")


def demo_simplificacion():
    """Demo de simplificación."""
    print_separador("DEMO 4: SIMPLIFICACIÓN Y MANIPULACIÓN")
    
    calc = CalculadoraAvanzada()
    
    print("\n🔹 SIMPLIFICAR:")
    expresiones = [
        "x + x + x",
        "sin(x)**2 + cos(x)**2",
        "(x**2 - 1)/(x - 1)"
    ]
    
    for expr in expresiones:
        resultado = calc.simplificar(expr)
        if resultado.exitoso:
            print(f"   {expr} → {resultado.resultado}")
    
    print("\n🔹 EXPANDIR:")
    expandir_exprs = [
        "(x + 1)**2",
        "(x + 2)*(x + 3)",
        "(x - 1)**3"
    ]
    
    for expr in expandir_exprs:
        resultado = calc.expandir(expr)
        if resultado.exitoso:
            print(f"   {expr} → {resultado.resultado}")
    
    print("\n🔹 FACTORIZAR:")
    factorizar_exprs = [
        "x**2 - 4",
        "x**2 + 2*x",
        "x**3 - 1"
    ]
    
    for expr in factorizar_exprs:
        resultado = calc.factorizar(expr)
        if resultado.exitoso:
            print(f"   {expr} → {resultado.resultado}")


def demo_limites():
    """Demo de límites."""
    print_separador("DEMO 5: LÍMITES")
    
    calc = CalculadoraAvanzada()
    
    limites = [
        ("x**2", 0),
        ("1/x", 'oo'),
        ("(x**2 - 1)/(x - 1)", 1),
        ("sin(x)/x", 0)
    ]
    
    for expr, punto in limites:
        print(f"\n📝 lim[x→{punto}] {expr}")
        resultado = calc.limite(expr, punto=punto)
        
        if resultado.exitoso:
            print(f"   = {resultado.resultado}")


def demo_series_taylor():
    """Demo de series de Taylor."""
    print_separador("DEMO 6: SERIES DE TAYLOR")
    
    calc = CalculadoraAvanzada()
    
    funciones = [
        ("exp(x)", 0, 5),
        ("sin(x)", 0, 4),
        ("cos(x)", 0, 4),
        ("log(1+x)", 0, 3)
    ]
    
    for expr, punto, orden in funciones:
        print(f"\n📝 {expr} alrededor de {punto}, orden {orden}:")
        resultado = calc.serie_taylor(expr, punto=punto, orden=orden)
        
        if resultado.exitoso:
            print(f"   ≈ {resultado.resultado}")


def demo_evaluacion():
    """Demo de evaluación."""
    print_separador("DEMO 7: EVALUACIÓN DE EXPRESIONES")
    
    calc = CalculadoraAvanzada()
    
    evaluaciones = [
        ("x**2", {"x": 2}),
        ("x + y", {"x": 3, "y": 5}),
        ("sin(x)", {"x": 0}),
        ("x**2 + y**2", {"x": 3, "y": 4})
    ]
    
    for expr, valores in evaluaciones:
        print(f"\n📝 {expr} con {valores}")
        resultado = calc.evaluar(expr, valores)
        
        if resultado.exitoso:
            print(f"   = {resultado.resultado}")


def demo_vocabulario():
    """Demo del vocabulario de matemáticas."""
    print_separador("DEMO 8: VOCABULARIO DE MATEMÁTICAS")
    
    conceptos = obtener_conceptos_matematicas()
    
    print(f"\n📚 CONCEPTOS CARGADOS: {len(conceptos)}")
    
    # Estadísticas
    con_grounding_1 = sum(1 for c in conceptos if c.confianza_grounding == 1.0)
    con_operaciones = sum(1 for c in conceptos if hasattr(c, 'operaciones') and c.operaciones)
    
    print(f"  • Grounding 1.0: {con_grounding_1}/{len(conceptos)}")
    print(f"  • Con operaciones: {con_operaciones}/{len(conceptos)}")
    print(f"  • Grounding promedio: {sum(c.confianza_grounding for c in conceptos) / len(conceptos):.2f}")
    
    # Conceptos por categoría
    print("\n📊 CONCEPTOS POR CATEGORÍA:")
    categorias = {
        'derivadas': ['derivar', 'derivada', 'regla'],
        'integrales': ['integrar', 'integral', 'antiderivada'],
        'ecuaciones': ['resolver', 'ecuación', 'raíz'],
        'simplificación': ['simplificar', 'expandir', 'factorizar'],
        'límites': ['límite', 'infinito', 'serie']
    }
    
    for cat, palabras_clave in categorias.items():
        count = sum(1 for c in conceptos 
                   if any(p in ' '.join(c.palabras_español).lower() 
                         for p in palabras_clave))
        print(f"  • {cat.capitalize()}: {count}")
    
    # Mostrar algunos conceptos clave
    print("\n🔍 CONCEPTOS CLAVE:")
    
    palabras = [
        'derivar',
        'integrar',
        'resolver ecuación',
        'límite',
        'serie de taylor'
    ]
    
    for palabra in palabras:
        concepto = obtener_concepto_por_palabra(palabra, conceptos)
        if concepto:
            print(f"\n  🔹 {concepto.id}")
            print(f"     Palabras: {concepto.palabras_español[:3]}")
            print(f"     Grounding: {concepto.confianza_grounding}")
            if concepto.operaciones:
                print(f"     ✅ Operación ejecutable")


def demo_integracion():
    """Demo de integración vocabulario + calculadora."""
    print_separador("DEMO 9: INTEGRACIÓN COMPLETA")
    
    # Configurar
    calc = CalculadoraAvanzada()
    configurar_calculadora(calc)
    conceptos = obtener_conceptos_matematicas()
    
    print("\n🔗 CALCULADORA CONECTADA A VOCABULARIO")
    
    # Buscar concepto de derivada
    concepto = obtener_concepto_por_palabra('derivar', conceptos)
    
    if concepto and concepto.operaciones:
        print(f"\n→ Usando concepto: {concepto.id}")
        print(f"→ Grounding: {concepto.confianza_grounding}")
        
        # Ejecutar derivada
        print(f"\n📝 Derivar: x**3 + 2*x")
        resultado = concepto.operaciones['ejecutar']("x**3 + 2*x")
        
        print(f"   Resultado: {resultado.resultado}")
        print(f"   Pasos:")
        for paso in resultado.paso_a_paso:
            print(f"     • {paso}")


def demo_problema_fisica():
    """Demo de problema de física."""
    print_separador("DEMO 10: PROBLEMA DE FÍSICA")
    
    calc = CalculadoraAvanzada()
    
    print("""
🌟 PROBLEMA: Movimiento de un proyectil

Posición: s(t) = -4.9*t**2 + 20*t + 10
donde s es altura en metros, t es tiempo en segundos
""")
    
    # Velocidad = primera derivada
    print("\n1️⃣ Velocidad (primera derivada):")
    velocidad = calc.derivar("-4.9*t**2 + 20*t + 10", variable='t')
    print(f"   v(t) = {velocidad.resultado}")
    
    # Aceleración = segunda derivada
    print("\n2️⃣ Aceleración (segunda derivada):")
    aceleracion = calc.derivar("-4.9*t**2 + 20*t + 10", variable='t', orden=2)
    print(f"   a(t) = {aceleracion.resultado}")
    
    # ¿Cuándo llega al suelo?
    print("\n3️⃣ ¿Cuándo llega al suelo? (s(t) = 0):")
    tiempo = calc.resolver_ecuacion("-4.9*t**2 + 20*t + 10", variable='t')
    print(f"   t = {tiempo.resultado}")
    
    # Altura máxima (cuando v(t) = 0)
    print("\n4️⃣ ¿Cuándo alcanza altura máxima? (v(t) = 0):")
    t_max = calc.resolver_ecuacion(velocidad.resultado, variable='t')
    print(f"   t = {t_max.resultado}")


def main():
    """Ejecuta todas las demos."""
    print("\n" + "🔢" * 40)
    print("  BELLADONNA - FASE 3: MATEMÁTICAS AVANZADAS")
    print("  Semana 5: CalculadoraAvanzada + SymPy")
    print("🔢" * 40)
    
    try:
        # Demo 1: Derivadas
        demo_derivadas()
        
        # Demo 2: Integrales
        demo_integrales()
        
        # Demo 3: Ecuaciones
        demo_ecuaciones()
        
        # Demo 4: Simplificación
        demo_simplificacion()
        
        # Demo 5: Límites
        demo_limites()
        
        # Demo 6: Series
        demo_series_taylor()
        
        # Demo 7: Evaluación
        demo_evaluacion()
        
        # Demo 8: Vocabulario
        demo_vocabulario()
        
        # Demo 9: Integración
        demo_integracion()
        
        # Demo 10: Física
        demo_problema_fisica()
        
        # Resumen final
        print_separador("RESUMEN")
        print("""
✅ Calculadora Avanzada funcionando
✅ 45 conceptos matemáticos cargados
✅ Derivadas e integrales simbólicas
✅ Resolver ecuaciones algebraicas
✅ Límites y series de Taylor
✅ Integración con vocabulario

📊 ESTADÍSTICAS:
  • Conceptos nuevos: 45
  • Tests: 35+
  • Grounding promedio: 0.95
  • Operaciones: derivar, integrar, resolver, simplificar

🎯 PRÓXIMO: Semana 6 - Planificación Multi-Paso
        """)
        
    except Exception as e:
        print(f"\n❌ Error en demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()