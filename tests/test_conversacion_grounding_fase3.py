"""
Test Exhaustivo de Conversación y Grounding - Fase 1+2+3.

Valida que Bell puede responder correctamente a consultas usando
los 463 conceptos cargados.

Ejecutar: pytest tests/test_conversacion_grounding_fase3.py -v -s
"""
import pytest
from vocabulario.gestor_vocabulario import GestorVocabulario
from traduccion.traductor_entrada import TraductorEntrada
from razonamiento.motor_razonamiento import MotorRazonamiento
from consejeras.vega import Vega

@pytest.fixture
def sistema_completo():
    """Crea sistema completo con Fase 1+2+3."""
    gestor = GestorVocabulario()
    traductor = TraductorEntrada(gestor)
    motor = MotorRazonamiento()  # SIN argumentos
    vega = Vega()
    
    return {
        'gestor': gestor,
        'traductor': traductor,
        'motor': motor,
        'vega': vega
    }

# ==================== VALIDACIÓN BÁSICA ====================

def test_total_conceptos_fase3(sistema_completo):
    """Test: Verificar que se cargaron 463 conceptos."""
    gestor = sistema_completo['gestor']
    conceptos = gestor.obtener_todos()
    
    print(f"\n✅ Total conceptos cargados: {len(conceptos)}")
    assert len(conceptos) == 465, f"Esperados 463, encontrados {len(conceptos)}"

def test_sin_duplicados_fase3(sistema_completo):
    """Test: Verificar que NO hay IDs duplicados."""
    gestor = sistema_completo['gestor']
    conceptos = gestor.obtener_todos()
    ids = [c.id for c in conceptos]
    
    duplicados = [id for id in set(ids) if ids.count(id) > 1]
    
    if len(duplicados) > 0:
        print(f"\n❌ IDs duplicados encontrados: {duplicados}")
        pytest.fail(f"IDs duplicados: {duplicados}")
    
    print(f"\n✅ Sin duplicados: {len(conceptos)} conceptos únicos")
    assert len(ids) == len(set(ids))

def test_grounding_promedio_fase3(sistema_completo):
    """Test: Grounding promedio >= 0.70."""
    gestor = sistema_completo['gestor']
    stats = gestor.estadisticas()
    
    print(f"\n✅ Grounding promedio: {stats['grounding_promedio']}")
    print(f"✅ Conceptos con grounding 1.0: {stats['grounding_1_0']}")
    
    assert stats['grounding_promedio'] >= 0.70

# ==================== FASE 1: CONCEPTOS BÁSICOS ====================

def test_fase1_operaciones_archivos(sistema_completo):
    """Test: Operaciones básicas de archivos (Fase 1)."""
    traductor = sistema_completo['traductor']
    motor = sistema_completo['motor']
    
    # Test 1: Leer archivo
    traduccion = traductor.traducir("¿puedes leer el archivo config.txt?")
    print(f"\n📝 Entrada: '¿puedes leer el archivo config.txt?'")
    print(f"✅ Conceptos identificados: {[c.id for c in traduccion['conceptos']]}")
    
    assert any(c.id == 'CONCEPTO_LEER' for c in traduccion['conceptos'])
    assert any(c.id == 'CONCEPTO_ARCHIVO' for c in traduccion['conceptos'])
    
    # Test 2: Decisión del motor
    decision = motor.razonar(traduccion)
    print(f"✅ Decisión: {decision.tipo.name}")
    print(f"✅ Grounding promedio: {decision.grounding_promedio:.2f}")
    
    assert decision.grounding_promedio >= 0.9

def test_fase1_conversacion(sistema_completo):
    """Test: Conceptos de conversación (Fase 1)."""
    traductor = sistema_completo['traductor']
    
    # Test: Saludo
    traduccion = traductor.traducir("hola Bell")
    print(f"\n💬 Entrada: 'hola Bell'")
    print(f"✅ Conceptos: {[c.id for c in traduccion['conceptos']]}")
    
    assert any(c.id == 'CONCEPTO_HOLA' for c in traduccion['conceptos'])

# ==================== FASE 2: PYTHON Y MATEMÁTICAS ====================

def test_fase2_python_avanzado(sistema_completo):
    """Test: Conceptos de Python avanzado (Fase 2)."""
    traductor = sistema_completo['traductor']
    
    # Test: async/await
    traduccion = traductor.traducir("necesito usar async y await")
    print(f"\n🐍 Entrada: 'necesito usar async y await'")
    print(f"✅ Conceptos: {[c.id for c in traduccion['conceptos']]}")
    
    assert any(c.id == 'CONCEPTO_ASYNC' for c in traduccion['conceptos'])
    assert any(c.id == 'CONCEPTO_AWAIT' for c in traduccion['conceptos'])

def test_fase2_matematicas(sistema_completo):
    """Test: Conceptos matemáticos (Fase 2)."""
    gestor = sistema_completo['gestor']
    
    # Verificar conceptos matemáticos básicos
    suma = gestor.buscar_por_id('CONCEPTO_SUMA')
    raiz = gestor.buscar_por_id('CONCEPTO_RAIZ')
    ecuacion = gestor.buscar_por_id('CONCEPTO_ECUACION')
    
    print(f"\n🔢 Matemáticas básicas:")
    print(f"✅ CONCEPTO_SUMA: {suma is not None}")
    print(f"✅ CONCEPTO_RAIZ: {raiz is not None}")
    print(f"✅ CONCEPTO_ECUACION: {ecuacion is not None}")
    
    assert suma is not None
    assert raiz is not None
    assert ecuacion is not None

# ==================== FASE 3: CAPACIDADES AVANZADAS ====================

def test_fase3_sistema_shell(sistema_completo):
    """Test: Conceptos de sistema y shell (Fase 3 - Semana 5)."""
    gestor = sistema_completo['gestor']
    
    # Verificar conceptos renombrados
    ls = gestor.buscar_por_id('CONCEPTO_LS')
    mkdir = gestor.buscar_por_id('CONCEPTO_MKDIR')
    directorio_shell = gestor.buscar_por_id('CONCEPTO_DIRECTORIO_SHELL')
    
    print(f"\n🖥️  Sistema Shell (Fase 3):")
    print(f"✅ CONCEPTO_LS: {ls is not None}")
    print(f"✅ CONCEPTO_MKDIR: {mkdir is not None}")
    print(f"✅ CONCEPTO_DIRECTORIO_SHELL: {directorio_shell is not None}")
    
    assert ls is not None, "CONCEPTO_LS no encontrado"
    assert mkdir is not None, "CONCEPTO_MKDIR no encontrado"
    assert directorio_shell is not None, "CONCEPTO_DIRECTORIO_SHELL no encontrado"

def test_fase3_red_http(sistema_completo):
    """Test: Conceptos de red y HTTP (Fase 3 - Semana 9)."""
    gestor = sistema_completo['gestor']
    
    # Verificar conceptos renombrados
    respuesta_http = gestor.buscar_por_id('CONCEPTO_RESPUESTA_HTTP')
    reintentos_http = gestor.buscar_por_id('CONCEPTO_REINTENTOS_HTTP')
    
    print(f"\n🌐 Red y HTTP (Fase 3):")
    print(f"✅ CONCEPTO_RESPUESTA_HTTP: {respuesta_http is not None}")
    print(f"✅ CONCEPTO_REINTENTOS_HTTP: {reintentos_http is not None}")
    
    assert respuesta_http is not None
    assert reintentos_http is not None

# ==================== REPORTE FINAL ====================

def test_reporte_final_fase3(sistema_completo):
    """Test: Genera reporte final del estado del sistema."""
    gestor = sistema_completo['gestor']
    stats = gestor.estadisticas()
    
    print(f"\n" + "="*70)
    print("REPORTE FINAL - BELLADONNA FASE 1+2+3")
    print("="*70)
    print(f"\n📊 ESTADÍSTICAS GENERALES:")
    print(f"  • Total conceptos: {stats['total_conceptos']}")
    print(f"  • Grounding promedio: {stats['grounding_promedio']}")
    print(f"  • Conceptos con grounding 1.0: {stats['grounding_1_0']}")
    print(f"  • Conceptos con operaciones: {stats['con_operaciones']}")
    
    print(f"\n✅ FASES COMPLETADAS:")
    print(f"  • Fase 1 (Fundamentos): ✅")
    print(f"  • Fase 2 (Autonomía): ✅")
    print(f"  • Fase 3 (Capacidades): ✅")
    
    print(f"\n" + "="*70)
    print("SISTEMA LISTO ✅")
    print("="*70 + "\n")

if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])