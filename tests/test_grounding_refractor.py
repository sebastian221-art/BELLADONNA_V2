"""
Test Completo - Sistema de Grounding Refactorizado.

Valida que todos los componentes del módulo grounding/ funcionan correctamente.

Ejecutar:
    python test_grounding_refactor.py
"""

import sys
from pathlib import Path

# Agregar raíz al path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test 1: Verificar que todos los imports funcionan."""
    print("\n" + "="*70)
    print("TEST 1: IMPORTS")
    print("="*70)
    
    try:
        # Imports principales
        from grounding import GestorGrounding, DimensionGrounding
        print("✅ Imports principales: GestorGrounding, DimensionGrounding")
        
        # Dimensiones
        from grounding.dimensiones import (
            GroundingComputacional,
            GroundingSemantico,
            GroundingContextual,
            GroundingPragmatico,
            GroundingSocial,
            GroundingTemporal,
            GroundingCausal,
            GroundingMetacognitivo,
            GroundingPredictivo
        )
        print("✅ Las 9 dimensiones importadas correctamente")
        
        # Calculadores
        from grounding.calculadores import Calculador9D, ExtensionGrounding
        print("✅ Calculadores: Calculador9D, ExtensionGrounding")
        
        # Integración
        from grounding.integracion import IntegradorGroundingBell
        print("✅ Integración: IntegradorGroundingBell")
        
        # Reportes
        from grounding.reportes import (
            GeneradorReporteGrounding,
            EstadoDimension,
            ReporteConcepto,
            ReporteSistema
        )
        print("✅ Reportes: GeneradorReporteGrounding, estructuras de datos")
        
        print("\n✅ TODOS LOS IMPORTS EXITOSOS")
        return True
        
    except ImportError as e:
        print(f"\n❌ ERROR EN IMPORTS: {e}")
        return False


def test_gestor_grounding():
    """Test 2: Verificar que GestorGrounding funciona."""
    print("\n" + "="*70)
    print("TEST 2: GESTOR GROUNDING")
    print("="*70)
    
    try:
        from grounding import GestorGrounding
        from core.concepto_anclado import ConceptoAnclado
        from core.tipos import TipoConcepto
        
        # Crear gestor
        gestor = GestorGrounding()
        print(f"✅ GestorGrounding creado")
        
        # Verificar dimensiones
        dimensiones = gestor.listar_dimensiones()
        print(f"✅ Dimensiones disponibles: {len(dimensiones)}")
        assert len(dimensiones) == 9, "Deben haber 9 dimensiones"
        
        for dim in dimensiones:
            print(f"   • {dim}")
        
        # Crear concepto de prueba
        concepto = ConceptoAnclado(
            id="CONCEPTO_TEST",
            tipo=TipoConcepto.OPERACION_SISTEMA,
            palabras_español=["test", "prueba"],
            operaciones={'ejecutar': lambda: "OK"},
            confianza_grounding=1.0
        )
        print(f"✅ Concepto de prueba creado: {concepto.id}")
        
        # Evaluar 9D
        grounding_9d = gestor.evaluar_9d(concepto)
        print(f"✅ Grounding 9D calculado:")
        
        for dimension, puntaje in grounding_9d.items():
            print(f"   • {dimension:15s}: {puntaje:.2f}")
        
        assert len(grounding_9d) == 9, "Deben haber 9 dimensiones evaluadas"
        
        # Calcular promedio
        promedio = gestor.calcular_promedio(grounding_9d)
        print(f"✅ Promedio: {promedio:.2f}")
        assert 0.0 <= promedio <= 1.0, "Promedio debe estar entre 0 y 1"
        
        # Generar reporte
        reporte = gestor.generar_reporte(concepto)
        print(f"✅ Reporte generado:")
        print(reporte)
        
        print("\n✅ GESTOR GROUNDING FUNCIONA CORRECTAMENTE")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR EN GESTOR: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_calculador_9d():
    """Test 3: Verificar que Calculador9D funciona."""
    print("\n" + "="*70)
    print("TEST 3: CALCULADOR 9D")
    print("="*70)
    
    try:
        from grounding.calculadores import Calculador9D
        from vocabulario.gestor_vocabulario import GestorVocabulario
        from core.concepto_anclado import ConceptoAnclado
        from core.tipos import TipoConcepto
        
        # Crear vocabulario
        vocab = GestorVocabulario()
        print(f"✅ Vocabulario creado: {vocab.total_conceptos()} conceptos")
        
        # Crear calculador
        calculador = Calculador9D(vocab)
        print(f"✅ Calculador9D creado")
        
        # Crear conceptos de prueba
        conceptos_test = [
            ConceptoAnclado(
                id=f"CONCEPTO_TEST_{i}",
                tipo=TipoConcepto.OPERACION_SISTEMA,
                palabras_español=[f"test{i}"],
                operaciones={'ejecutar': lambda: "OK"},
                confianza_grounding=0.9
            )
            for i in range(3)
        ]
        
        # Calcular grounding para cada uno
        print(f"✅ Calculando grounding para {len(conceptos_test)} conceptos...")
        
        for concepto in conceptos_test:
            grounding = calculador.calcular_concepto(concepto)
            promedio = calculador.calcular_promedio(grounding)
            print(f"   • {concepto.id}: {promedio:.2f}")
            
            assert len(grounding) == 9, "Deben haber 9 dimensiones"
            assert 0.0 <= promedio <= 1.0, "Promedio válido"
        
        # Obtener estadísticas
        stats = calculador.obtener_estadisticas()
        print(f"✅ Estadísticas del calculador:")
        print(f"   • Conceptos en cache: {stats['conceptos_en_cache']}")
        print(f"   • Dimensiones activas: {stats['dimensiones_activas']}")
        
        print("\n✅ CALCULADOR 9D FUNCIONA CORRECTAMENTE")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR EN CALCULADOR: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_extension_grounding():
    """Test 4: Verificar que ExtensionGrounding funciona."""
    print("\n" + "="*70)
    print("TEST 4: EXTENSION GROUNDING")
    print("="*70)
    
    try:
        from grounding.calculadores import ExtensionGrounding
        from core.concepto_anclado import ConceptoAnclado
        from core.tipos import TipoConcepto
        
        # Crear concepto
        concepto = ConceptoAnclado(
            id="CONCEPTO_EXTENSION_TEST",
            tipo=TipoConcepto.OPERACION_SISTEMA,
            palabras_español=["extension", "test"],
            operaciones={'ejecutar': lambda: "OK"},
            confianza_grounding=1.0
        )
        print(f"✅ Concepto creado: {concepto.id}")
        
        # Crear extensión
        extension = ExtensionGrounding(concepto)
        print(f"✅ ExtensionGrounding creada")
        
        # Obtener grounding
        grounding = extension.obtener_grounding()
        print(f"✅ Grounding obtenido: {len(grounding)} dimensiones")
        
        # Obtener promedio
        promedio = extension.obtener_promedio()
        print(f"✅ Promedio: {promedio:.2f}")
        
        # Obtener dimensión específica
        computacional = extension.obtener_dimension('computacional')
        print(f"✅ Computacional: {computacional:.2f}")
        
        # Verificar propiedades de compatibilidad
        assert extension.grounding_computacional == computacional
        print(f"✅ Propiedades de compatibilidad funcionan")
        
        # Obtener resumen
        resumen = extension.obtener_resumen()
        print(f"✅ Resumen completo:")
        print(f"   • Score total: {resumen['score_total']:.2f}")
        print(f"   • Concepto ID: {resumen['concepto_id']}")
        
        # Generar reporte
        reporte = extension.generar_reporte()
        print(f"✅ Reporte generado (primeras 5 líneas):")
        for linea in reporte.split('\n')[:5]:
            print(f"   {linea}")
        
        print("\n✅ EXTENSION GROUNDING FUNCIONA CORRECTAMENTE")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR EN EXTENSION: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_integrador():
    """Test 5: Verificar que IntegradorGroundingBell funciona."""
    print("\n" + "="*70)
    print("TEST 5: INTEGRADOR GROUNDING BELL")
    print("="*70)
    
    try:
        from grounding.integracion import IntegradorGroundingBell
        from vocabulario.gestor_vocabulario import GestorVocabulario
        
        # Crear vocabulario
        vocab = GestorVocabulario()
        print(f"✅ Vocabulario creado")
        
        # Crear integrador
        integrador = IntegradorGroundingBell(vocab)
        print(f"✅ IntegradorGroundingBell creado")
        
        # Obtener grounding de un concepto del vocabulario
        concepto_id = vocab.conceptos[0].id if vocab.conceptos else "CONCEPTO_TEST"
        
        grounding = integrador.obtener_grounding(concepto_id)
        
        if grounding:
            print(f"✅ Grounding obtenido para {concepto_id}")
            promedio = integrador.obtener_promedio(concepto_id)
            print(f"   • Promedio: {promedio:.2f}")
            
            # Obtener dimensión específica
            semantico = integrador.obtener_dimension(concepto_id, 'semantico')
            print(f"   • Semántico: {semantico:.2f}")
            
            # Verificar grounding mínimo
            tiene_grounding = integrador.verificar_grounding_minimo(concepto_id, 0.3)
            print(f"   • Tiene grounding mínimo (0.3): {tiene_grounding}")
        
        print("\n✅ INTEGRADOR FUNCIONA CORRECTAMENTE")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR EN INTEGRADOR: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_generador_reportes():
    """Test 6: Verificar que GeneradorReporteGrounding funciona."""
    print("\n" + "="*70)
    print("TEST 6: GENERADOR DE REPORTES")
    print("="*70)
    
    try:
        from grounding.reportes import GeneradorReporteGrounding
        from grounding.calculadores import Calculador9D
        from core.concepto_anclado import ConceptoAnclado
        from core.tipos import TipoConcepto
        
        # Crear calculador
        calculador = Calculador9D()
        print(f"✅ Calculador creado")
        
        # Crear generador
        generador = GeneradorReporteGrounding(calculador)
        print(f"✅ GeneradorReporteGrounding creado")
        
        # Crear concepto de prueba
        concepto = ConceptoAnclado(
            id="CONCEPTO_REPORTE_TEST",
            tipo=TipoConcepto.OPERACION_SISTEMA,
            palabras_español=["reporte", "test"],
            operaciones={'ejecutar': lambda: "OK"},
            confianza_grounding=0.95
        )
        
        # Generar reporte para concepto
        reporte = generador.generar_para_concepto(concepto)
        print(f"✅ Reporte de concepto generado:")
        print(f"   • Concepto: {reporte.concepto_id}")
        print(f"   • Salud: {reporte.salud}")
        print(f"   • Score total: {reporte.score_total:.2f}")
        print(f"   • Dimensiones activas: {reporte.dimensiones_activas}/9")
        
        # Recomendaciones
        recs = reporte.recomendaciones()
        if recs:
            print(f"   • Recomendaciones: {len(recs)}")
        
        print("\n✅ GENERADOR DE REPORTES FUNCIONA CORRECTAMENTE")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR EN GENERADOR REPORTES: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_sistema_completo():
    """Test 7: Verificar que todo el sistema funciona integrado."""
    print("\n" + "="*70)
    print("TEST 7: SISTEMA COMPLETO INTEGRADO")
    print("="*70)
    
    try:
        from vocabulario.gestor_vocabulario import GestorVocabulario
        from grounding import GestorGrounding
        from grounding.calculadores import Calculador9D, ExtensionGrounding
        from grounding.integracion import IntegradorGroundingBell
        from grounding.reportes import GeneradorReporteGrounding
        
        # Crear vocabulario
        vocab = GestorVocabulario()
        print(f"✅ Vocabulario: {vocab.total_conceptos()} conceptos")
        
        # Crear componentes
        gestor = GestorGrounding()
        calculador = Calculador9D(vocab)
        integrador = IntegradorGroundingBell(vocab)
        generador_reportes = GeneradorReporteGrounding(calculador)
        print(f"✅ Todos los componentes creados")
        
        # Tomar concepto de prueba del vocabulario
        concepto = vocab.conceptos[0] if vocab.conceptos else None
        
        if concepto:
            print(f"\n📊 Procesando: {concepto.id}")
            
            # 1. Evaluar con gestor
            grounding_9d = gestor.evaluar_9d(concepto)
            promedio1 = gestor.calcular_promedio(grounding_9d)
            print(f"   Gestor → Promedio: {promedio1:.2f}")
            
            # 2. Evaluar con calculador
            grounding_calc = calculador.calcular_concepto(concepto)
            promedio2 = calculador.calcular_promedio(grounding_calc)
            print(f"   Calculador → Promedio: {promedio2:.2f}")
            
            # 3. Evaluar con integrador
            promedio3 = integrador.obtener_promedio(concepto.id)
            if promedio3:
                print(f"   Integrador → Promedio: {promedio3:.2f}")
            
            # 4. Crear extensión
            extension = ExtensionGrounding(concepto, vocab)
            promedio4 = extension.obtener_promedio()
            print(f"   Extensión → Promedio: {promedio4:.2f}")
            
            # 5. Generar reporte
            reporte = generador_reportes.generar_para_concepto(concepto)
            print(f"   Reporte → Salud: {reporte.salud}")
            
            print(f"\n✅ Todos los componentes procesaron el concepto exitosamente")
        
        print("\n✅ SISTEMA COMPLETO FUNCIONA CORRECTAMENTE")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR EN SISTEMA COMPLETO: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Ejecuta todos los tests."""
    print("\n" + "="*70)
    print("🧪 TEST SUITE - SISTEMA DE GROUNDING REFACTORIZADO")
    print("="*70)
    
    tests = [
        ("Imports", test_imports),
        ("Gestor Grounding", test_gestor_grounding),
        ("Calculador 9D", test_calculador_9d),
        ("Extension Grounding", test_extension_grounding),
        ("Integrador Bell", test_integrador),
        ("Generador Reportes", test_generador_reportes),
        ("Sistema Completo", test_sistema_completo),
    ]
    
    resultados = []
    
    for nombre, test_func in tests:
        try:
            resultado = test_func()
            resultados.append((nombre, resultado))
        except Exception as e:
            print(f"\n❌ ERROR CRÍTICO EN {nombre}: {e}")
            resultados.append((nombre, False))
    
    # Resumen final
    print("\n" + "="*70)
    print("RESUMEN DE TESTS")
    print("="*70)
    
    exitosos = sum(1 for _, resultado in resultados if resultado)
    total = len(resultados)
    
    for nombre, resultado in resultados:
        icono = "✅" if resultado else "❌"
        print(f"{icono} {nombre}")
    
    print(f"\n{'='*70}")
    print(f"RESULTADO: {exitosos}/{total} tests exitosos")
    
    if exitosos == total:
        print("🎉 ¡TODOS LOS TESTS PASARON!")
    else:
        print(f"⚠️  {total - exitosos} tests fallaron")
    
    print("="*70)
    
    return exitosos == total


if __name__ == '__main__':
    exito = main()
    sys.exit(0 if exito else 1)