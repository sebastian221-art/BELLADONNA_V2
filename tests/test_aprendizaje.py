"""
Tests para Sistema de Aprendizaje Básico - Fase 2.
"""
import pytest
from datetime import datetime

from aprendizaje.estrategias import (
    EstrategiaUsoFrecuente,
    EstrategiaExitoFallido,
    EstrategiaInsights,
    EstrategiaConservadora,
    EstrategiaComposite
)
from aprendizaje.ajustador_grounding import AjustadorGrounding
from aprendizaje.aplicador_insights import AplicadorInsights
from aprendizaje.motor_aprendizaje import MotorAprendizaje
from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto

# ===== TESTS ESTRATEGIAS =====

def test_estrategia_uso_frecuente():
    """Test: Estrategia de uso frecuente."""
    estrategia = EstrategiaUsoFrecuente(umbral_usos=5, incremento=0.05)
    
    # Contexto con muchos usos
    contexto = {'usos': 10, 'tasa_exito': 0.9}
    nuevo = estrategia.calcular_ajuste('TEST', 0.8, contexto)
    
    assert nuevo is not None
    assert nuevo == pytest.approx(0.85)  # 0.8 + 0.05

def test_estrategia_uso_frecuente_no_alcanza_umbral():
    """Test: No ajustar si no alcanza umbral."""
    estrategia = EstrategiaUsoFrecuente(umbral_usos=10, incremento=0.05)
    
    # Pocos usos
    contexto = {'usos': 5}
    nuevo = estrategia.calcular_ajuste('TEST', 0.8, contexto)
    
    assert nuevo is None

def test_estrategia_exito_fallido_aumentar():
    """Test: Aumentar con alta tasa de éxito."""
    estrategia = EstrategiaExitoFallido(incremento_exito=0.03, decremento_fallo=0.05)
    
    # Alta tasa de éxito
    contexto = {'usos_exitosos': 8, 'usos_fallidos': 2}  # 80% éxito
    nuevo = estrategia.calcular_ajuste('TEST', 0.7, contexto)
    
    assert nuevo is not None
    assert nuevo == 0.73  # 0.7 + 0.03

def test_estrategia_exito_fallido_disminuir():
    """Test: Disminuir con baja tasa de éxito."""
    estrategia = EstrategiaExitoFallido(incremento_exito=0.03, decremento_fallo=0.05)
    
    # Baja tasa de éxito
    contexto = {'usos_exitosos': 2, 'usos_fallidos': 8}  # 20% éxito
    nuevo = estrategia.calcular_ajuste('TEST', 0.7, contexto)
    
    assert nuevo is not None
    assert nuevo == pytest.approx(0.65)  # 0.7 - 0.05

def test_estrategia_insights():
    """Test: Aplicar insight."""
    estrategia = EstrategiaInsights()
    
    contexto = {
        'ajuste_sugerido': 0.05,
        'razon': 'Test',
        'prioridad': 'ALTA'
    }
    nuevo = estrategia.calcular_ajuste('TEST', 0.75, contexto)
    
    assert nuevo is not None
    assert nuevo == 0.80  # 0.75 + 0.05

def test_estrategia_conservadora():
    """Test: Estrategia conservadora."""
    estrategia = EstrategiaConservadora(max_cambio=0.02)
    
    contexto = {'direccion': 'aumentar', 'confianza': 1.0}
    nuevo = estrategia.calcular_ajuste('TEST', 0.8, contexto)
    
    assert nuevo is not None
    assert nuevo == pytest.approx(0.82)  # 0.8 + (0.02 * 1.0)

def test_estrategia_composite():
    """Test: Estrategia composite."""
    estrategia = EstrategiaComposite([
        EstrategiaUsoFrecuente(umbral_usos=100, incremento=0.05),  # No se aplicará
        EstrategiaExitoFallido()  # Esta sí
    ])
    
    # Contexto que active segunda estrategia
    contexto = {'usos_exitosos': 8, 'usos_fallidos': 2}
    nuevo = estrategia.calcular_ajuste('TEST', 0.7, contexto)
    
    assert nuevo is not None

# ===== TESTS AJUSTADOR GROUNDING =====

def test_ajustador_crear():
    """Test: Crear ajustador."""
    ajustador = AjustadorGrounding()
    assert ajustador.estrategia is not None
    assert len(ajustador.historial_ajustes) == 0

def test_ajustador_proponer_ajuste():
    """Test: Proponer ajuste válido."""
    ajustador = AjustadorGrounding(EstrategiaUsoFrecuente(umbral_usos=5))
    
    contexto = {'usos': 10, 'tasa_exito': 0.9}
    propuesta = ajustador.proponer_ajuste('CONCEPTO_TEST', 0.8, contexto)
    
    assert propuesta is not None
    assert propuesta['concepto_id'] == 'CONCEPTO_TEST'
    assert propuesta['grounding_propuesto'] == pytest.approx(0.85)

def test_ajustador_rechazar_ajuste_excesivo():
    """Test: Rechazar ajuste excesivo."""
    ajustador = AjustadorGrounding()
    ajustador.max_ajuste_por_vez = 0.05
    
    # Intentar ajuste de 0.2 (excesivo)
    contexto = {'ajuste_sugerido': 0.2}
    propuesta = ajustador.proponer_ajuste('TEST', 0.7, contexto)
    
    # No debería generar propuesta
    assert propuesta is None

def test_ajustador_aplicar_ajuste():
    """Test: Aplicar ajuste a concepto."""
    ajustador = AjustadorGrounding(EstrategiaUsoFrecuente(umbral_usos=5))
    
    # Crear concepto con keyword arguments
    concepto = ConceptoAnclado(
        id='CONCEPTO_TEST',
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=['test'],
        confianza_grounding=0.8
    )
    
    # Proponer y aplicar
    contexto = {'usos': 10}
    propuesta = ajustador.proponer_ajuste(concepto.id, concepto.confianza_grounding, contexto)
    
    if propuesta:
        exito = ajustador.aplicar_ajuste(concepto, propuesta)
        assert exito == True
        assert concepto.confianza_grounding == pytest.approx(0.85)

def test_ajustador_historial():
    """Test: Registrar ajustes en historial."""
    ajustador = AjustadorGrounding(EstrategiaUsoFrecuente(umbral_usos=5))
    
    concepto = ConceptoAnclado(
        id='CONCEPTO_TEST',
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=['test'],
        confianza_grounding=0.8
    )
    
    contexto = {'usos': 10}
    propuesta = ajustador.proponer_ajuste(concepto.id, concepto.confianza_grounding, contexto)
    
    if propuesta:
        ajustador.aplicar_ajuste(concepto, propuesta)
    
    historial = ajustador.obtener_historial()
    assert len(historial) >= 1

def test_ajustador_estadisticas():
    """Test: Estadísticas del ajustador."""
    ajustador = AjustadorGrounding(EstrategiaUsoFrecuente(umbral_usos=5))
    
    concepto = ConceptoAnclado(
        id='CONCEPTO_TEST',
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=['test'],
        confianza_grounding=0.8
    )
    contexto = {'usos': 10}
    propuesta = ajustador.proponer_ajuste(concepto.id, concepto.confianza_grounding, contexto)
    
    if propuesta:
        ajustador.aplicar_ajuste(concepto, propuesta)
    
    stats = ajustador.obtener_estadisticas()
    assert 'total_ajustes' in stats
    assert 'ajustes_aplicados' in stats

# ===== TESTS APLICADOR INSIGHTS =====

def test_aplicador_crear():
    """Test: Crear aplicador."""
    aplicador = AplicadorInsights()
    assert len(aplicador.insights_procesados) == 0

def test_aplicador_procesar_concepto_dominante():
    """Test: Procesar insight de concepto dominante."""
    aplicador = AplicadorInsights()
    
    insight = {
        'tipo': 'CONCEPTO_DOMINANTE',
        'descripcion': 'Test',
        'relevancia': 'ALTA',
        'datos': {'concepto_id': 'CONCEPTO_LEER', 'porcentaje': 45}
    }
    
    acciones = aplicador.procesar_insight(insight)
    
    assert len(acciones) == 1
    assert acciones[0]['tipo'] == 'AJUSTAR_GROUNDING'
    assert acciones[0]['concepto_id'] == 'CONCEPTO_LEER'

def test_aplicador_procesar_patron_conductual():
    """Test: Procesar patrón conductual."""
    aplicador = AplicadorInsights()
    
    insight = {
        'tipo': 'PATRON_CONDUCTUAL',
        'descripcion': 'Test',
        'relevancia': 'MEDIA',
        'datos': {'patron': 'COMUNICACION_PROBLEMATICA'}
    }
    
    acciones = aplicador.procesar_insight(insight)
    
    assert len(acciones) >= 1

def test_aplicador_multiples_insights():
    """Test: Procesar múltiples insights."""
    aplicador = AplicadorInsights()
    
    insights = [
        {
            'tipo': 'CONCEPTO_DOMINANTE',
            'descripcion': 'Test 1',
            'relevancia': 'ALTA',
            'datos': {'concepto_id': 'CONCEPTO_A', 'porcentaje': 40}
        },
        {
            'tipo': 'CONCEPTO_DOMINANTE',
            'descripcion': 'Test 2',
            'relevancia': 'ALTA',
            'datos': {'concepto_id': 'CONCEPTO_B', 'porcentaje': 35}
        }
    ]
    
    acciones = aplicador.procesar_multiples_insights(insights)
    
    assert len(acciones) >= 2

def test_aplicador_priorizar_acciones():
    """Test: Priorizar acciones."""
    aplicador = AplicadorInsights()
    
    insights = [
        {'tipo': 'CONCEPTO_DOMINANTE', 'descripcion': 'Test', 'relevancia': 'BAJA', 'datos': {'concepto_id': 'A', 'porcentaje': 31}},
        {'tipo': 'CONCEPTO_DOMINANTE', 'descripcion': 'Test', 'relevancia': 'ALTA', 'datos': {'concepto_id': 'B', 'porcentaje': 45}}
    ]
    
    acciones = aplicador.procesar_multiples_insights(insights)
    
    # Primera acción debe ser de alta prioridad
    assert acciones[0]['prioridad'] == 'ALTA'

def test_aplicador_estadisticas():
    """Test: Estadísticas del aplicador."""
    aplicador = AplicadorInsights()
    
    insight = {
        'tipo': 'CONCEPTO_DOMINANTE',
        'descripcion': 'Test',
        'relevancia': 'ALTA',
        'datos': {'concepto_id': 'TEST', 'porcentaje': 40}
    }
    aplicador.procesar_insight(insight)
    
    stats = aplicador.obtener_estadisticas()
    
    assert stats['insights_procesados'] == 1
    assert stats['acciones_generadas'] >= 1

# ===== TESTS MOTOR APRENDIZAJE =====

def test_motor_crear():
    """Test: Crear motor de aprendizaje."""
    motor = MotorAprendizaje()
    assert motor.ajustador is not None
    assert motor.aplicador is not None

def test_motor_configurar_integraciones():
    """Test: Configurar integraciones."""
    motor = MotorAprendizaje()
    
    motor.configurar_integraciones(
        vocabulario='vocab',
        memoria='mem',
        bucles='bucles'
    )
    
    assert motor.gestor_vocabulario == 'vocab'
    assert motor.gestor_memoria == 'mem'
    assert motor.gestor_bucles == 'bucles'

def test_motor_estadisticas():
    """Test: Estadísticas del motor."""
    motor = MotorAprendizaje()
    
    stats = motor.obtener_estadisticas()
    
    assert 'ciclos_ejecutados' in stats
    assert 'ajustador' in stats
    assert 'aplicador' in stats

def test_motor_procesar_uso_concepto():
    """Test: Procesar uso de concepto."""
    from vocabulario.gestor_vocabulario import GestorVocabulario
    
    motor = MotorAprendizaje()
    gestor_vocab = GestorVocabulario()
    motor.configurar_integraciones(vocabulario=gestor_vocab)
    
    # Procesar uso exitoso
    motor.procesar_uso_concepto('CONCEPTO_LEER', exitoso=True, certeza=0.9)
    
    # Verificar que no causó error
    assert motor.ciclos_ejecutados >= 0

def test_motor_obtener_historial_ajustes():
    """Test: Obtener historial de ajustes."""
    motor = MotorAprendizaje()
    
    historial = motor.obtener_historial_ajustes()
    assert isinstance(historial, list)

def test_motor_obtener_acciones_pendientes():
    """Test: Obtener acciones pendientes."""
    motor = MotorAprendizaje()
    
    acciones = motor.obtener_acciones_pendientes()
    assert isinstance(acciones, list)

def test_motor_reiniciar_estadisticas():
    """Test: Reiniciar estadísticas."""
    motor = MotorAprendizaje()
    motor.ciclos_ejecutados = 5
    
    motor.reiniciar_estadisticas()
    
    assert motor.ciclos_ejecutados == 0

if __name__ == '__main__':
    pytest.main([__file__, '-v'])