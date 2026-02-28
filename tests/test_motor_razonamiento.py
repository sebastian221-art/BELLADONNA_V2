"""
Tests para Motor de Razonamiento.
"""
import pytest
from vocabulario.gestor_vocabulario import GestorVocabulario
from traduccion.traductor_entrada import TraductorEntrada
from razonamiento.motor_razonamiento import MotorRazonamiento
from razonamiento.tipos_decision import TipoDecision

@pytest.fixture
def motor():
    """Motor con vocabulario completo."""
    return MotorRazonamiento()

@pytest.fixture
def traductor():
    """Traductor con vocabulario."""
    gestor = GestorVocabulario()
    return TraductorEntrada(gestor)

def test_decision_afirmativa_leer(motor, traductor):
    """Test: Decisión afirmativa para capacidad real."""
    traduccion = traductor.traducir("¿Puedes leer archivos?")
    decision = motor.razonar(traduccion)
    
    assert decision.tipo == TipoDecision.AFIRMATIVA
    assert decision.puede_ejecutar == True
    assert decision.certeza >= 0.9
    assert 'CONCEPTO_LEER' in decision.conceptos_principales

def test_decision_negativa_sin_grounding(motor, traductor):
    """Test: Decisión negativa para concepto sin operación."""
    traduccion = traductor.traducir("¿Puedes hackear la NASA?")
    decision = motor.razonar(traduccion)
    
    # Bell detecta "puedes" pero no puede "hackear"
    assert decision.tipo == TipoDecision.NEGATIVA
    assert decision.puede_ejecutar == False

def test_decision_saludo(motor, traductor):
    """Test: Decisión de saludo."""
    traduccion = traductor.traducir("Hola Bell")
    decision = motor.razonar(traduccion)
    
    assert decision.tipo == TipoDecision.SALUDO
    assert decision.certeza >= 0.9

def test_decision_agradecimiento(motor, traductor):
    """Test: Decisión de agradecimiento."""
    traduccion = traductor.traducir("Gracias por tu ayuda")
    decision = motor.razonar(traduccion)
    
    assert decision.tipo == TipoDecision.AGRADECIMIENTO

def test_decision_no_entendido(motor, traductor):
    """Test: NO_ENTENDIDO con palabras desconocidas."""
    # CAMBIAR: "abstract" ahora existe en vocabulario
    traduccion = traductor.traducir("zzzxxx qqwweerr")  # ← Palabras inventadas sin significado
    decision = motor.razonar(traduccion)
    
    assert decision.tipo == TipoDecision.NO_ENTENDIDO
    assert decision.puede_ejecutar == False
    
def test_pasos_razonamiento_incluidos(motor, traductor):
    """Test: Decisión incluye pasos de razonamiento."""
    traduccion = traductor.traducir("¿Puedes escribir archivos?")
    decision = motor.razonar(traduccion)
    
    assert len(decision.pasos_razonamiento) > 0
    assert any('CONCEPTO_ESCRIBIR' in paso for paso in decision.pasos_razonamiento)

def test_grounding_promedio_calculado(motor, traductor):
    """Test: Grounding promedio se calcula."""
    traduccion = traductor.traducir("¿Puedes leer?")
    decision = motor.razonar(traduccion)
    
    assert decision.grounding_promedio > 0.0

if __name__ == '__main__':
    pytest.main([__file__, '-v'])