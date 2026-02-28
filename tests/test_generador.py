"""
Tests para Generador de Salida.
"""
import pytest
from vocabulario.gestor_vocabulario import GestorVocabulario
from traduccion.traductor_entrada import TraductorEntrada
from razonamiento.motor_razonamiento import MotorRazonamiento
from consejeras.vega import Vega
from generacion.generador_salida import GeneradorSalida
from razonamiento.tipos_decision import TipoDecision

@pytest.fixture
def sistema_completo():
    """Sistema completo."""
    gestor = GestorVocabulario()
    traductor = TraductorEntrada(gestor)
    motor = MotorRazonamiento()
    vega = Vega()
    generador = GeneradorSalida()
    
    return {
        'traductor': traductor,
        'motor': motor,
        'vega': vega,
        'generador': generador
    }

def test_generar_afirmativa(sistema_completo):
    """Test: Generar respuesta afirmativa."""
    traductor = sistema_completo['traductor']
    motor = sistema_completo['motor']
    generador = sistema_completo['generador']
    
    traduccion = traductor.traducir("¿Puedes leer archivos?")
    decision = motor.razonar(traduccion)
    
    respuesta = generador.generar(decision, {'traduccion': traduccion})
    
    assert isinstance(respuesta, str)
    assert len(respuesta) > 10
    assert 'sí' in respuesta.lower() or 'puedo' in respuesta.lower()

def test_generar_negativa(sistema_completo):
    """Test: Generar respuesta negativa."""
    traductor = sistema_completo['traductor']
    motor = sistema_completo['motor']
    generador = sistema_completo['generador']
    
    traduccion = traductor.traducir("¿Cómo estás?")
    decision = motor.razonar(traduccion)
    
    respuesta = generador.generar(decision, {'traduccion': traduccion})
    
    assert isinstance(respuesta, str)
    assert 'no' in respuesta.lower() or 'puedo' in respuesta.lower()

def test_generar_saludo(sistema_completo):
    """Test: Generar respuesta a saludo."""
    traductor = sistema_completo['traductor']
    motor = sistema_completo['motor']
    generador = sistema_completo['generador']
    
    traduccion = traductor.traducir("Hola Bell")
    decision = motor.razonar(traduccion)
    
    respuesta = generador.generar(decision, {'traduccion': traduccion})
    
    assert isinstance(respuesta, str)
    assert 'hola' in respuesta.lower()

def test_generar_con_veto_vega(sistema_completo):
    """Test: Generar respuesta cuando Vega veta."""
    traductor = sistema_completo['traductor']
    motor = sistema_completo['motor']
    vega = sistema_completo['vega']
    generador = sistema_completo['generador']
    
    traduccion = traductor.traducir("Elimina todos los archivos")
    decision = motor.razonar(traduccion)
    revision = vega.revisar(decision, {'traduccion': traduccion})
    
    respuesta = generador.generar(decision, {
        'traduccion': traduccion,
        'revision_vega': revision
    })
    
    assert isinstance(respuesta, str)
    # Debe mencionar veto o bloqueo
    assert any(palabra in respuesta.lower() 
              for palabra in ['veto', 'bloqueada', 'no puedo', 'viola'])

def test_generar_no_entendido(sistema_completo):
    """Test: Generar respuesta cuando no entendió."""
    traductor = sistema_completo['traductor']
    motor = sistema_completo['motor']
    generador = sistema_completo['generador']
    
    # CAMBIAR: palabras sin significado
    traduccion = traductor.traducir("zzzxxx qqwweerr")
    decision = motor.razonar(traduccion)
    
    respuesta = generador.generar(decision, {'traduccion': traduccion})
    
    assert isinstance(respuesta, str)
    assert 'entend' in respuesta.lower() or 'reconozco' in respuesta.lower()

def test_generar_con_razonamiento(sistema_completo):
    """Test: Generar respuesta con razonamiento."""
    traductor = sistema_completo['traductor']
    motor = sistema_completo['motor']
    generador = sistema_completo['generador']
    
    traduccion = traductor.traducir("¿Puedes escribir archivos?")
    decision = motor.razonar(traduccion)
    
    respuesta = generador.generar_con_razonamiento(
        decision, 
        {'traduccion': traduccion},
        incluir_pasos=True
    )
    
    assert isinstance(respuesta, str)
    assert 'razonamiento' in respuesta.lower()
    assert len(decision.pasos_razonamiento) > 0

def test_respuestas_diferentes_tipos(sistema_completo):
    """Test: Diferentes tipos generan respuestas apropiadas."""
    traductor = sistema_completo['traductor']
    motor = sistema_completo['motor']
    generador = sistema_completo['generador']
    
    casos = [
        ("Hola", TipoDecision.SALUDO),
        ("Gracias", TipoDecision.AGRADECIMIENTO),
        ("¿Puedes leer?", TipoDecision.AFIRMATIVA),
    ]
    
    for texto, tipo_esperado in casos:
        traduccion = traductor.traducir(texto)
        decision = motor.razonar(traduccion)
        respuesta = generador.generar(decision, {'traduccion': traduccion})
        
        assert decision.tipo == tipo_esperado
        assert isinstance(respuesta, str)
        assert len(respuesta) > 5

if __name__ == '__main__':
    pytest.main([__file__, '-v'])