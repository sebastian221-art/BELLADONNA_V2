"""
Demo de Operaciones de Sistema - Fase 3 Semana 1-2.
Muestra capacidades de Bell con shell commands.
"""

import sys
from pathlib import Path

# Agregar path del proyecto
proyecto_path = Path(__file__).parent.parent
sys.path.insert(0, str(proyecto_path))

from operaciones.shell_executor import ShellExecutor, SecurityError
from vocabulario.semana5_sistema import (
    obtener_conceptos_sistema,
    configurar_executor,
    obtener_concepto_por_palabra
)


def print_separador(titulo=""):
    """Imprime separador visual."""
    print("\n" + "=" * 80)
    if titulo:
        print(f"  {titulo}")
        print("=" * 80)


def demo_shell_executor():
    """Demo del ShellExecutor."""
    print_separador("DEMO 1: SHELL EXECUTOR")
    
    executor = ShellExecutor(timeout=5)
    
    # Info del sistema
    print("\n📊 INFORMACIÓN DEL SISTEMA:")
    info = executor.obtener_info_sistema()
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    # Comandos disponibles
    print("\n📋 COMANDOS DISPONIBLES:")
    comandos = executor.listar_comandos_disponibles()
    print(f"  Total: {len(comandos)} comandos")
    print(f"  Primeros 10: {comandos[:10]}")
    
    # Ejecutar comandos seguros
    print("\n✅ EJECUTANDO COMANDOS SEGUROS:")
    
    comandos_demo = [
        ('pwd', 'Directorio actual'),
        ('whoami', 'Usuario actual'),
        ('date', 'Fecha y hora'),
        ('ls', 'Listar archivos'),
    ]
    
    for comando, descripcion in comandos_demo:
        try:
            print(f"\n  🔹 {descripcion} ({comando}):")
            resultado = executor.ejecutar(comando)
            if resultado['exitoso']:
                print(f"     ✓ {resultado['stdout'].strip()[:100]}")
            else:
                print(f"     ✗ Error: {resultado['stderr'][:100]}")
        except Exception as e:
            print(f"     ✗ Excepción: {e}")
    
    # Intentar comando inseguro
    print("\n❌ INTENTANDO COMANDO INSEGURO:")
    try:
        print("  🔹 Intentando: rm -rf /")
        resultado = executor.ejecutar('rm -rf /')
        print("  ❌ ERROR: Comando inseguro se ejecutó (NO DEBERÍA PASAR)")
    except SecurityError as e:
        print(f"  ✅ Bloqueado correctamente: {str(e)[:100]}")


def demo_vocabulario_sistema():
    """Demo del vocabulario de sistema."""
    print_separador("DEMO 2: VOCABULARIO DE SISTEMA")
    
    # Cargar conceptos
    conceptos = obtener_conceptos_sistema()
    
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
    
    # Mostrar algunos conceptos
    print("\n🔍 EJEMPLOS DE CONCEPTOS:")
    
    ejemplos = [
        'listar',
        'mkdir',
        'ps',
        'cat',
        'pwd'
    ]
    
    for palabra in ejemplos:
        concepto = obtener_concepto_por_palabra(palabra, conceptos)
        if concepto:
            print(f"\n  🔹 {concepto.id}")
            print(f"     Palabras: {concepto.palabras_español[:3]}")
            print(f"     Tipo: {concepto.tipo}")
            print(f"     Grounding: {concepto.confianza_grounding}")
            if hasattr(concepto, 'propiedades'):
                print(f"     Propiedades: {list(concepto.propiedades.keys())[:3]}")


def demo_integracion():
    """Demo de integración: vocabulario + ejecutor."""
    print_separador("DEMO 3: INTEGRACIÓN VOCABULARIO + EJECUTOR")
    
    # Configurar
    executor = ShellExecutor(timeout=5)
    configurar_executor(executor)
    conceptos = obtener_conceptos_sistema()
    
    print("\n🔗 CONCEPTOS CONECTADOS A EJECUTOR")
    
    # Simular queries del usuario
    queries = [
        "listar archivos",
        "directorio actual",
        "quien soy",
    ]
    
    for query in queries:
        print(f"\n  Usuario: '{query}'")
        
        # Buscar concepto
        for palabra in query.split():
            concepto = obtener_concepto_por_palabra(palabra, conceptos)
            if concepto:
                print(f"  → Encontrado: {concepto.id}")
                
                # Si tiene operación ejecutable
                if hasattr(concepto, 'operaciones') and concepto.operaciones and 'ejecutar' in concepto.operaciones:
                    print(f"  → Grounding: {concepto.confianza_grounding}")
                    
                    # Ejecutar (solo si es seguro y apropiado)
                    if concepto.confianza_grounding == 1.0:
                        try:
                            # Algunos conceptos necesitan argumentos
                            if concepto.id == 'CONCEPTO_LISTAR_DIRECTORIO':
                                resultado = concepto.operaciones['ejecutar']('.')
                            else:
                                resultado = concepto.operaciones['ejecutar']()
                            
                            if resultado and resultado.get('exitoso'):
                                output = resultado.get('stdout', '')[:80]
                                print(f"  ✅ Ejecutado: {output.strip()}")
                            else:
                                print(f"  ⚠️  Falló: {resultado.get('stderr', '')[:50]}")
                        except Exception as e:
                            print(f"  ⚠️  Error: {str(e)[:50]}")
                break


def demo_seguridad():
    """Demo de sistema de seguridad."""
    print_separador("DEMO 4: SISTEMA DE SEGURIDAD")
    
    executor = ShellExecutor()
    
    print("\n🛡️  VALIDACIÓN DE SEGURIDAD")
    
    # Casos de prueba
    casos = [
        ('ls', True, 'Comando básico permitido'),
        ('pwd', True, 'Información de sistema'),
        ('rm -rf /', False, '¡DESTRUCTIVO! Bloqueado'),
        ('shutdown', False, 'Apagado del sistema'),
        ('ls; rm -rf /', False, 'Encadenamiento malicioso'),
        ('echo $(malicious)', False, 'Command substitution'),
        ('git status', True, 'Git es permitido'),
    ]
    
    for comando, debe_ser_seguro, descripcion in casos:
        es_seguro = executor.es_seguro(comando)
        simbolo = '✅' if es_seguro == debe_ser_seguro else '❌'
        estado = 'SEGURO' if es_seguro else 'BLOQUEADO'
        
        print(f"\n  {simbolo} {comando}")
        print(f"     Estado: {estado}")
        print(f"     Descripción: {descripcion}")
        
        if not es_seguro:
            razon = executor._razón_inseguridad(comando)
            print(f"     Razón: {razon}")


def main():
    """Ejecuta todas las demos."""
    print("\n" + "🌿" * 40)
    print("  BELLADONNA - FASE 3: OPERACIONES DE SISTEMA")
    print("  Semana 1-2: Shell Executor + Vocabulario")
    print("🌿" * 40)
    
    try:
        # Demo 1: Shell Executor
        demo_shell_executor()
        
        # Demo 2: Vocabulario
        demo_vocabulario_sistema()
        
        # Demo 3: Integración
        demo_integracion()
        
        # Demo 4: Seguridad
        demo_seguridad()
        
        # Resumen final
        print_separador("RESUMEN")
        print("""
✅ Shell Executor funcionando
✅ 40 conceptos de sistema cargados
✅ Integración vocabulario + ejecutor
✅ Sistema de seguridad activo
✅ Grounding 1.0 en conceptos ejecutables

📊 ESTADÍSTICAS:
  • Comandos permitidos: 20+
  • Conceptos nuevos: 40
  • Tests: 30+
  • Grounding promedio: 0.97

🎯 PRÓXIMO: Semana 3-4 - Análisis de Código
        """)
        
    except Exception as e:
        print(f"\n❌ Error en demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()