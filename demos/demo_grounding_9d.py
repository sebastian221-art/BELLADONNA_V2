"""
Demo Visual - Sistema de Grounding 9D Refactorizado.

Muestra el sistema en acción con ejemplos visuales.

Ejecutar:
    python demo_grounding_9d.py
"""

import sys
from pathlib import Path
import time

# Agregar raíz al path
sys.path.insert(0, str(Path(__file__).parent))


def imprimir_titulo(titulo):
    """Imprime un título bonito."""
    print("\n" + "="*70)
    print(f" {titulo:^68} ")
    print("="*70 + "\n")


def imprimir_seccion(titulo):
    """Imprime una sección."""
    print(f"\n{'─'*70}")
    print(f"▶ {titulo}")
    print(f"{'─'*70}\n")


def demo_inicio():
    """Muestra la introducción del demo."""
    imprimir_titulo("🌿 BELLADONNA - SISTEMA DE GROUNDING 9D 🌿")
    
    print("Bienvenido al demo del sistema de grounding multidimensional refactorizado.")
    print()
    print("Este demo muestra:")
    print("  • Arquitectura modular del sistema")
    print("  • Evaluación de grounding en 9 dimensiones")
    print("  • Generación de reportes visuales")
    print("  • Integración con Belladonna")
    print()
    input("Presiona ENTER para continuar...")


def demo_imports():
    """Demo 1: Mostrar imports."""
    imprimir_seccion("1. IMPORTANDO MÓDULO GROUNDING")
    
    print("Importando componentes del sistema...")
    print()
    
    from grounding import GestorGrounding
    print("✅ from grounding import GestorGrounding")
    time.sleep(0.3)
    
    from grounding.dimensiones import GroundingComputacional, GroundingSemantico
    print("✅ from grounding.dimensiones import GroundingComputacional, GroundingSemantico")
    time.sleep(0.3)
    
    from grounding.calculadores import Calculador9D, ExtensionGrounding
    print("✅ from grounding.calculadores import Calculador9D, ExtensionGrounding")
    time.sleep(0.3)
    
    from grounding.integracion import IntegradorGroundingBell
    print("✅ from grounding.integracion import IntegradorGroundingBell")
    time.sleep(0.3)
    
    from grounding.reportes import GeneradorReporteGrounding
    print("✅ from grounding.reportes import GeneradorReporteGrounding")
    
    print()
    print("🎉 Todos los módulos importados exitosamente")
    
    input("\nPresiona ENTER para continuar...")
    
    return GestorGrounding, Calculador9D, ExtensionGrounding


def demo_gestor(GestorGrounding):
    """Demo 2: Mostrar GestorGrounding."""
    imprimir_seccion("2. GESTOR GROUNDING - COORDINADOR CENTRAL")
    
    print("Creando GestorGrounding...")
    gestor = GestorGrounding()
    
    print()
    print("📋 Dimensiones disponibles:")
    dimensiones = gestor.listar_dimensiones()
    
    for i, dim in enumerate(dimensiones, 1):
        print(f"  {i}. {dim.capitalize()}")
        time.sleep(0.2)
    
    print()
    print(f"✅ {len(dimensiones)} dimensiones cargadas y listas")
    
    input("\nPresiona ENTER para continuar...")
    
    return gestor


def demo_concepto():
    """Demo 3: Crear concepto de ejemplo."""
    imprimir_seccion("3. CREANDO CONCEPTO DE EJEMPLO")
    
    from core.concepto_anclado import ConceptoAnclado
    from core.tipos import TipoConcepto
    
    print("Creando concepto: CONCEPTO_LEER")
    print()
    
    concepto = ConceptoAnclado(
        id="CONCEPTO_LEER",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["leer", "read", "cargar", "abrir"],
        operaciones={
            'ejecutar': lambda archivo: f"Leyendo {archivo}...",
            'validar': lambda: True
        },
        confianza_grounding=1.0,
        propiedades={
            'precondiciones': ['archivo_existe', 'permiso_lectura'],
            'postcondiciones': ['contenido_disponible'],
            'efectos': ['archivo_leido'],
            'duracion_estimada': '100ms'
        },
        metadata={
            'veces_usado': 42,
            'fecha_creacion': '2026-01-15'
        }
    )
    
    print(f"ID: {concepto.id}")
    print(f"Tipo: {concepto.tipo.name}")
    print(f"Palabras español: {', '.join(concepto.palabras_español)}")
    print(f"Operaciones: {len(concepto.operaciones)}")
    print(f"Confianza base: {concepto.confianza_grounding}")
    
    print()
    print("✅ Concepto creado con datos ricos para evaluación")
    
    input("\nPresiona ENTER para continuar...")
    
    return concepto


def demo_evaluacion(gestor, concepto):
    """Demo 4: Evaluar concepto."""
    imprimir_seccion("4. EVALUANDO GROUNDING 9D")
    
    print(f"Evaluando: {concepto.id}")
    print()
    print("Calculando grounding en 9 dimensiones...")
    print()
    
    grounding_9d = gestor.evaluar_9d(concepto)
    
    # Mostrar cada dimensión con animación
    for dimension, puntaje in grounding_9d.items():
        barra = generar_barra(puntaje)
        print(f"  {dimension:15s} │ {barra} │ {puntaje:.2f}")
        time.sleep(0.3)
    
    promedio = gestor.calcular_promedio(grounding_9d)
    
    print()
    print(f"{'─'*50}")
    print(f"  {'PROMEDIO':15s} │ {generar_barra(promedio)} │ {promedio:.2f}")
    print(f"{'─'*50}")
    
    input("\nPresiona ENTER para continuar...")
    
    return grounding_9d, promedio


def demo_reporte(gestor, concepto):
    """Demo 5: Generar reporte."""
    imprimir_seccion("5. GENERANDO REPORTE VISUAL")
    
    print("Generando reporte completo...")
    print()
    
    reporte = gestor.generar_reporte(concepto)
    print(reporte)
    
    input("\nPresiona ENTER para continuar...")


def demo_extension(ExtensionGrounding, concepto):
    """Demo 6: Usar ExtensionGrounding."""
    imprimir_seccion("6. EXTENSION GROUNDING - API SIMPLIFICADA")
    
    print("La ExtensionGrounding provee una API simple para usar en Bell:")
    print()
    
    extension = ExtensionGrounding(concepto)
    
    print("# Crear extensión")
    print(f"extension = ExtensionGrounding(concepto)")
    print()
    
    time.sleep(0.5)
    
    print("# Obtener grounding completo")
    grounding = extension.obtener_grounding()
    print(f"grounding = extension.obtener_grounding()")
    print(f"  → {len(grounding)} dimensiones evaluadas")
    print()
    
    time.sleep(0.5)
    
    print("# Obtener promedio")
    promedio = extension.obtener_promedio()
    print(f"promedio = extension.obtener_promedio()")
    print(f"  → {promedio:.2f}")
    print()
    
    time.sleep(0.5)
    
    print("# Obtener dimensión específica")
    semantico = extension.obtener_dimension('semantico')
    print(f"semantico = extension.obtener_dimension('semantico')")
    print(f"  → {semantico:.2f}")
    print()
    
    time.sleep(0.5)
    
    print("# Verificar grounding mínimo")
    tiene_grounding = promedio >= 0.7
    print(f"tiene_grounding = promedio >= 0.7")
    print(f"  → {tiene_grounding}")
    
    print()
    print("✅ API simple y fácil de usar")
    
    input("\nPresiona ENTER para continuar...")


def demo_vocabulario():
    """Demo 7: Evaluar conceptos del vocabulario."""
    imprimir_seccion("7. EVALUANDO CONCEPTOS DEL VOCABULARIO")
    
    from vocabulario.gestor_vocabulario import GestorVocabulario
    from grounding.calculadores import Calculador9D
    
    print("Cargando vocabulario de Belladonna...")
    vocab = GestorVocabulario()
    print(f"✅ {vocab.total_conceptos()} conceptos cargados")
    print()
    
    print("Creando calculador 9D...")
    calculador = Calculador9D(vocab)
    print("✅ Calculador listo")
    print()
    
    print("Evaluando primeros 5 conceptos:")
    print()
    
    for i, concepto in enumerate(vocab.conceptos[:5], 1):
        grounding = calculador.calcular_concepto(concepto)
        promedio = calculador.calcular_promedio(grounding)
        
        barra = generar_barra(promedio, longitud=15)
        print(f"  {i}. {concepto.id:30s} │ {barra} │ {promedio:.2f}")
        time.sleep(0.3)
    
    print()
    print("✅ Conceptos evaluados exitosamente")
    
    input("\nPresiona ENTER para continuar...")


def demo_final():
    """Demo final: Resumen."""
    imprimir_titulo("✨ DEMO COMPLETADO ✨")
    
    print("Has visto el sistema de grounding 9D en acción:")
    print()
    print("✅ Arquitectura modular (grounding/)")
    print("✅ 9 dimensiones independientes")
    print("✅ GestorGrounding centralizado")
    print("✅ Calculador9D para lotes")
    print("✅ ExtensionGrounding para API simple")
    print("✅ IntegradorGroundingBell para Bell")
    print("✅ GeneradorReporteGrounding para análisis")
    print()
    print("🎯 Ventajas del sistema refactorizado:")
    print("  • Modular: Agregar dimensión 10 = crear 1 archivo")
    print("  • Mantenible: Bug en temporal → editar temporal.py")
    print("  • Testeable: Cada dimensión se prueba independiente")
    print("  • Escalable: Listo para Fase 4")
    print()
    print("📁 Estructura del módulo:")
    print("  grounding/")
    print("  ├── __init__.py")
    print("  ├── base_dimension.py")
    print("  ├── gestor_grounding.py")
    print("  ├── dimensiones/      (9 archivos)")
    print("  ├── calculadores/     (2 archivos)")
    print("  ├── integracion/      (1 archivo)")
    print("  └── reportes/         (1 archivo)")
    print()
    print("🚀 Próximos pasos:")
    print("  1. Copiar archivos a tu proyecto")
    print("  2. Ejecutar: python test_grounding_refactor.py")
    print("  3. Actualizar main.py")
    print("  4. ¡Listo para Fase 4!")
    print()
    print("="*70)
    print()


def generar_barra(valor, longitud=20):
    """Genera barra de progreso visual."""
    lleno = int(valor * longitud)
    vacio = longitud - lleno
    return '█' * lleno + '░' * vacio


def main():
    """Ejecuta el demo completo."""
    try:
        # 0. Inicio
        demo_inicio()
        
        # 1. Imports
        GestorGrounding, Calculador9D, ExtensionGrounding = demo_imports()
        
        # 2. Gestor
        gestor = demo_gestor(GestorGrounding)
        
        # 3. Concepto
        concepto = demo_concepto()
        
        # 4. Evaluación
        grounding_9d, promedio = demo_evaluacion(gestor, concepto)
        
        # 5. Reporte
        demo_reporte(gestor, concepto)
        
        # 6. Extension
        demo_extension(ExtensionGrounding, concepto)
        
        # 7. Vocabulario
        demo_vocabulario()
        
        # 8. Final
        demo_final()
        
        print("¡Gracias por ver el demo! 🌿")
        
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrumpido")
    except Exception as e:
        print(f"\n❌ Error en demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()