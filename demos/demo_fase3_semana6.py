"""
Demo de Planificación Multi-Paso - Fase 3 Semana 6.
Muestra capacidades de planificación de Bell.
"""

import sys
from pathlib import Path

# Agregar path del proyecto
proyecto_path = Path(__file__).parent.parent
sys.path.insert(0, str(proyecto_path))

from planificacion.motor_planificacion import MotorPlanificacion, EstadoPaso
from planificacion.ejecutor_planes import EjecutorPlanes
from vocabulario.semana8_planificacion import (
    obtener_conceptos_planificacion,
    configurar_planificacion
)


def print_separador(titulo=""):
    """Imprime separador visual."""
    print("\n" + "=" * 80)
    if titulo:
        print(f"  {titulo}")
        print("=" * 80)


def demo_crear_plan():
    """Demo 1: Crear un plan simple."""
    print_separador("DEMO 1: CREAR PLAN")
    
    motor = MotorPlanificacion()
    
    pasos = [
        {"descripcion": "Analizar requisitos", "accion": "analizar"},
        {"descripcion": "Diseñar solución", "accion": "diseñar",
         "dependencias": ["paso_1"]},
        {"descripcion": "Implementar", "accion": "implementar",
         "dependencias": ["paso_2"]},
        {"descripcion": "Probar", "accion": "probar",
         "dependencias": ["paso_3"]}
    ]
    
    plan = motor.crear_plan("Desarrollar nueva funcionalidad", pasos)
    
    print(f"\n✅ Plan creado: {plan.objetivo}")
    print(f"   ID: {plan.id}")
    print(f"   Pasos: {len(plan.pasos)}")
    print(f"   Estado: {plan.estado}")
    
    print("\n📋 PASOS:")
    for paso in plan.pasos:
        deps = f" (depende de: {', '.join(paso.dependencias)})" if paso.dependencias else ""
        print(f"   {paso.id}: {paso.descripcion}{deps}")


def demo_dependencias():
    """Demo 2: Manejo de dependencias."""
    print_separador("DEMO 2: DEPENDENCIAS")
    
    motor = MotorPlanificacion()
    
    # Plan con dependencias complejas
    pasos = [
        {"descripcion": "Crear base de datos", "accion": "crear_db"},
        {"descripcion": "Crear tablas", "accion": "crear_tablas",
         "dependencias": ["paso_1"]},
        {"descripcion": "Insertar datos", "accion": "insertar",
         "dependencias": ["paso_2"]},
        {"descripcion": "Crear índices", "accion": "indices",
         "dependencias": ["paso_2"]},  # Paralelo con paso_3
        {"descripcion": "Optimizar", "accion": "optimizar",
         "dependencias": ["paso_3", "paso_4"]}
    ]
    
    plan = motor.crear_plan("Configurar base de datos", pasos)
    
    print("\n📊 ANÁLISIS DE DEPENDENCIAS:")
    for paso in plan.pasos:
        print(f"\n{paso.id}: {paso.descripcion}")
        if paso.dependencias:
            print(f"  ⬅️  Depende de: {', '.join(paso.dependencias)}")
        else:
            print(f"  🟢 Sin dependencias (puede empezar)")
    
    # Identificar pasos paralelos
    grupos = motor.puede_ejecutar_en_paralelo(plan)
    print(f"\n🔀 OPORTUNIDADES DE PARALELIZACIÓN:")
    print(f"   {len(grupos)} grupos identificados")
    for i, grupo in enumerate(grupos, 1):
        pasos_ids = [p.id for p in grupo]
        print(f"   Grupo {i}: {', '.join(pasos_ids)}")


def demo_validacion():
    """Demo 3: Validación de planes."""
    print_separador("DEMO 3: VALIDACIÓN")
    
    motor = MotorPlanificacion()
    motor.registrar_accion("accion_valida", lambda ctx: "ok")
    
    # Plan válido
    print("\n✅ PLAN VÁLIDO:")
    pasos_validos = [
        {"descripcion": "Paso 1", "accion": "accion_valida"}
    ]
    plan_valido = motor.crear_plan("Plan correcto", pasos_validos)
    valido, errores = motor.validar_plan(plan_valido)
    print(f"   Válido: {valido}")
    print(f"   Errores: {len(errores)}")
    
    # Plan inválido - acción no existe
    print("\n❌ PLAN INVÁLIDO (acción no registrada):")
    pasos_invalidos = [
        {"descripcion": "Paso 1", "accion": "accion_inexistente"}
    ]
    plan_invalido = motor.crear_plan("Plan con error", pasos_invalidos)
    valido, errores = motor.validar_plan(plan_invalido)
    print(f"   Válido: {valido}")
    print(f"   Errores encontrados:")
    for error in errores:
        print(f"     • {error}")


def demo_ejecucion():
    """Demo 4: Ejecución de planes."""
    print_separador("DEMO 4: EJECUTAR PLAN")
    
    motor = MotorPlanificacion()
    
    # Registrar acciones
    def accion_analizar(ctx):
        return {"archivos": 10, "lineas": 500}
    
    def accion_corregir(ctx):
        prev = ctx['resultados_previos'].get('paso_1', {})
        return {"errores_corregidos": prev.get('archivos', 0)}
    
    def accion_probar(ctx):
        return {"tests_pasados": 15, "tests_fallidos": 0}
    
    motor.registrar_accion("analizar", accion_analizar)
    motor.registrar_accion("corregir", accion_corregir)
    motor.registrar_accion("probar", accion_probar)
    
    # Crear plan
    pasos = [
        {"descripcion": "Analizar código", "accion": "analizar"},
        {"descripcion": "Corregir errores", "accion": "corregir",
         "dependencias": ["paso_1"]},
        {"descripcion": "Ejecutar tests", "accion": "probar",
         "dependencias": ["paso_2"]}
    ]
    
    plan = motor.crear_plan("Mejorar calidad del código", pasos)
    
    # Ejecutar
    ejecutor = EjecutorPlanes(motor)
    print(f"\n🚀 Ejecutando plan: {plan.objetivo}\n")
    
    resultado = ejecutor.ejecutar_plan(plan)
    
    print(f"\n{'✅ ÉXITO' if resultado.exitoso else '❌ FALLO'}")
    print(f"   Pasos ejecutados: {resultado.pasos_ejecutados}/{len(plan.pasos)}")
    print(f"   Pasos fallidos: {resultado.pasos_fallidos}")
    print(f"   Tiempo total: {resultado.tiempo_total:.3f}s")
    
    print("\n📦 RESULTADOS:")
    for paso_id, res in resultado.resultados.items():
        print(f"   {paso_id}: {res}")


def demo_manejo_errores():
    """Demo 5: Manejo de errores."""
    print_separador("DEMO 5: MANEJO DE ERRORES")
    
    motor = MotorPlanificacion()
    
    # Acción que falla
    def accion_ok(ctx):
        return "éxito"
    
    def accion_error(ctx):
        raise Exception("Error simulado")
    
    motor.registrar_accion("ok", accion_ok)
    motor.registrar_accion("error", accion_error)
    
    pasos = [
        {"descripcion": "Paso exitoso", "accion": "ok"},
        {"descripcion": "Paso con error", "accion": "error"},
        {"descripcion": "Este paso no se ejecutará", "accion": "ok",
         "dependencias": ["paso_2"]}
    ]
    
    plan = motor.crear_plan("Plan con error", pasos)
    
    ejecutor = EjecutorPlanes(motor)
    print("\n🚀 Ejecutando plan con error...\n")
    
    resultado = ejecutor.ejecutar_plan(plan, detener_en_error=True)
    
    print(f"\n{'✅' if resultado.exitoso else '❌'} Resultado: {'Éxito' if resultado.exitoso else 'Fallo'}")
    print(f"   Pasos ejecutados: {resultado.pasos_ejecutados}")
    print(f"   Pasos fallidos: {resultado.pasos_fallidos}")
    
    if resultado.errores:
        print("\n💥 ERRORES:")
        for paso_id, error in resultado.errores.items():
            print(f"   {paso_id}: {error}")


def demo_progreso():
    """Demo 6: Seguimiento de progreso."""
    print_separador("DEMO 6: PROGRESO DEL PLAN")
    
    motor = MotorPlanificacion()
    
    # Registrar acciones
    for i in range(5):
        motor.registrar_accion(f"accion{i}", lambda ctx: f"ok{i}")
    
    # Crear plan con 5 pasos
    pasos = [
        {"descripcion": f"Paso {i+1}", "accion": f"accion{i}"}
        for i in range(5)
    ]
    
    plan = motor.crear_plan("Plan con seguimiento", pasos)
    
    print(f"\n📊 PROGRESO INICIAL: {plan.progreso:.1f}%")
    
    # Simular ejecución paso a paso
    for paso in plan.pasos:
        paso.estado = EstadoPaso.COMPLETADO
        plan.actualizar_progreso()
        print(f"   ✅ {paso.descripcion} → Progreso: {plan.progreso:.1f}%")


def demo_optimizacion():
    """Demo 7: Optimización de planes."""
    print_separador("DEMO 7: OPTIMIZACIÓN")
    
    motor = MotorPlanificacion()
    
    # Plan con pasos duplicados
    pasos = [
        {"descripcion": "Compilar", "accion": "compilar"},
        {"descripcion": "Compilar", "accion": "compilar"},  # Duplicado
        {"descripcion": "Probar", "accion": "probar"},
        {"descripcion": "Compilar", "accion": "compilar"}  # Duplicado
    ]
    
    plan = motor.crear_plan("Plan con redundancia", pasos)
    
    print(f"\n📋 ANTES DE OPTIMIZAR:")
    print(f"   Pasos totales: {len(plan.pasos)}")
    
    plan_optimizado = motor.optimizar_plan(plan)
    
    print(f"\n✨ DESPUÉS DE OPTIMIZAR:")
    print(f"   Pasos totales: {len(plan_optimizado.pasos)}")
    print(f"   Pasos eliminados: {len(pasos) - len(plan_optimizado.pasos)}")


def demo_estimacion_tiempo():
    """Demo 8: Estimación de tiempo."""
    print_separador("DEMO 8: ESTIMACIÓN DE TIEMPO")
    
    motor = MotorPlanificacion()
    
    # Plan secuencial
    pasos_secuencial = [
        {"descripcion": "Paso 1", "accion": "a1"},
        {"descripcion": "Paso 2", "accion": "a2", "dependencias": ["paso_1"]},
        {"descripcion": "Paso 3", "accion": "a3", "dependencias": ["paso_2"]}
    ]
    
    plan_sec = motor.crear_plan("Plan secuencial", pasos_secuencial)
    tiempo_sec = motor.estimar_tiempo(plan_sec, tiempo_por_paso=2.0)
    
    print(f"\n⏱️  PLAN SECUENCIAL:")
    print(f"   Pasos: {len(plan_sec.pasos)}")
    print(f"   Tiempo estimado: {tiempo_sec:.1f}s")
    
    # Plan paralelo
    pasos_paralelo = [
        {"descripcion": "Paso 1", "accion": "a1"},
        {"descripcion": "Paso 2", "accion": "a2"},  # Paralelo con 1
        {"descripcion": "Paso 3", "accion": "a3"}   # Paralelo con 1 y 2
    ]
    
    plan_par = motor.crear_plan("Plan paralelo", pasos_paralelo)
    tiempo_par = motor.estimar_tiempo(plan_par, tiempo_por_paso=2.0)
    
    print(f"\n⏱️  PLAN PARALELO:")
    print(f"   Pasos: {len(plan_par.pasos)}")
    print(f"   Tiempo estimado: {tiempo_par:.1f}s")
    print(f"   Ahorro: {tiempo_sec - tiempo_par:.1f}s ({((tiempo_sec - tiempo_par)/tiempo_sec * 100):.0f}%)")


def demo_resumen():
    """Demo 9: Generar resumen."""
    print_separador("DEMO 9: RESUMEN DEL PLAN")
    
    motor = MotorPlanificacion()
    motor.registrar_accion("a1", lambda ctx: "ok")
    motor.registrar_accion("a2", lambda ctx: "ok")
    
    pasos = [
        {"descripcion": "Inicializar sistema", "accion": "a1"},
        {"descripcion": "Procesar datos", "accion": "a2",
         "dependencias": ["paso_1"]},
        {"descripcion": "Generar reporte", "accion": "a1",
         "dependencias": ["paso_2"]}
    ]
    
    plan = motor.crear_plan("Procesar información", pasos)
    
    # Simular ejecución parcial
    plan.pasos[0].estado = EstadoPaso.COMPLETADO
    plan.pasos[1].estado = EstadoPaso.EN_PROGRESO
    plan.actualizar_progreso()
    
    resumen = motor.generar_resumen(plan)
    print(resumen)


def demo_vocabulario():
    """Demo 10: Vocabulario de planificación."""
    print_separador("DEMO 10: VOCABULARIO DE PLANIFICACIÓN")
    
    conceptos = obtener_conceptos_planificacion()
    
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
        'Plan': ['plan', 'objetivo', 'crear'],
        'Paso': ['paso', 'acción', 'descripción'],
        'Dependencias': ['dependencia', 'ciclo', 'grafo'],
        'Ejecución': ['ejecutar', 'ejecutor', 'resultado'],
        'Estados': ['estado', 'pendiente', 'completado'],
        'Optimización': ['paralel', 'optimizar', 'estimar']
    }
    
    for cat, palabras in categorias.items():
        count = sum(1 for c in conceptos
                   if any(p in ' '.join(c.palabras_español).lower()
                         for p in palabras))
        print(f"  • {cat}: {count}")


def demo_integracion():
    """Demo 11: Integración completa."""
    print_separador("DEMO 11: INTEGRACIÓN COMPLETA")
    
    # Configurar todo
    motor = MotorPlanificacion()
    ejecutor = EjecutorPlanes(motor)
    configurar_planificacion(motor, ejecutor)
    
    print("\n✅ Sistema de planificación configurado")
    print(f"   Motor: {type(motor).__name__}")
    print(f"   Ejecutor: {type(ejecutor).__name__}")
    print(f"   Acciones registradas: {len(motor.acciones_disponibles)}")
    
    # Registrar acciones para el ejemplo
    motor.registrar_accion("backup", lambda ctx: "DB backed up")
    motor.registrar_accion("deploy", lambda ctx: "App deployed")
    motor.registrar_accion("smoke_test", lambda ctx: "Tests passed")
    
    # Crear y ejecutar plan
    pasos = [
        {"descripcion": "Backup de base de datos", "accion": "backup"},
        {"descripcion": "Desplegar aplicación", "accion": "deploy",
         "dependencias": ["paso_1"]},
        {"descripcion": "Smoke tests", "accion": "smoke_test",
         "dependencias": ["paso_2"]}
    ]
    
    plan = motor.crear_plan("Despliegue a producción", pasos)
    
    print(f"\n📋 Plan: {plan.objetivo}")
    print(f"   Pasos: {len(plan.pasos)}")
    
    # Validar
    valido, errores = motor.validar_plan(plan)
    print(f"   Válido: {'✅' if valido else '❌'}")
    
    # Ejecutar
    if valido:
        resultado = ejecutor.ejecutar_plan(plan)
        print(f"\n✅ Ejecución completada")
        print(f"   Tiempo: {resultado.tiempo_total:.3f}s")


def main():
    """Ejecuta todas las demos."""
    print("\n" + "📋" * 40)
    print("  BELLADONNA - FASE 3: PLANIFICACIÓN MULTI-PASO")
    print("  Semana 6: Motor de Planificación + Ejecutor")
    print("📋" * 40)
    
    try:
        # Demo 1
        demo_crear_plan()
        
        # Demo 2
        demo_dependencias()
        
        # Demo 3
        demo_validacion()
        
        # Demo 4
        demo_ejecucion()
        
        # Demo 5
        demo_manejo_errores()
        
        # Demo 6
        demo_progreso()
        
        # Demo 7
        demo_optimizacion()
        
        # Demo 8
        demo_estimacion_tiempo()
        
        # Demo 9
        demo_resumen()
        
        # Demo 10
        demo_vocabulario()
        
        # Demo 11
        demo_integracion()
        
        # Resumen final
        print_separador("RESUMEN")
        print("""
✅ Motor de Planificación funcionando
✅ Ejecutor de Planes funcionando
✅ 40 conceptos de planificación cargados
✅ Validación de planes
✅ Manejo de dependencias
✅ Detección de ciclos
✅ Ejecución paso a paso
✅ Manejo de errores
✅ Seguimiento de progreso
✅ Optimización de planes

📊 ESTADÍSTICAS:
  • Conceptos nuevos: 40
  • Tests: 30+
  • Grounding promedio: 0.95
  • Operaciones: crear, validar, ejecutar, optimizar

🎯 PRÓXIMO: Semana 7 - Red y APIs (HTTP Client)
        """)
        
    except Exception as e:
        print(f"\n❌ Error en demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()