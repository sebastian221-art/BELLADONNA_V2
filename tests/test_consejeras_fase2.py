"""
Tests para Consejeras de Fase 2: Lyra, Luna, Iris, Sage.
"""
import pytest
from vocabulario.gestor_vocabulario import GestorVocabulario
from traduccion.traductor_entrada import TraductorEntrada
from razonamiento.motor_razonamiento import MotorRazonamiento
from consejeras.lyra import Lyra
from consejeras.luna import Luna
from consejeras.iris import Iris
from consejeras.sage import Sage

@pytest.fixture
def sistema():
    """Sistema completo para tests."""
    gestor = GestorVocabulario()
    traductor = TraductorEntrada(gestor)
    motor = MotorRazonamiento()
    
    return {
        'traductor': traductor,
        'motor': motor
    }

# ===== TESTS LYRA (Empatía) =====

def test_lyra_detecta_frustracion(sistema):
    """Test: Lyra detecta frustración."""
    lyra = Lyra()
    traductor = sistema['traductor']
    motor = sistema['motor']
    
    traduccion = traductor.traducir("No entiendo nada, esto es muy confuso")
    decision = motor.razonar(traduccion)
    
    opinion = lyra.revisar(decision, {'traduccion': traduccion})
    
    assert opinion['consejera'] == 'Lyra'
    assert opinion['veto'] == False  # Lyra nunca veta
    assert len(opinion['sugerencias']) > 0

def test_lyra_detecta_necesidad_ayuda(sistema):
    """Test: Lyra detecta necesidad de ayuda."""
    lyra = Lyra()
    traductor = sistema['traductor']
    motor = sistema['motor']
    
    traduccion = traductor.traducir("Necesito ayuda con esto por favor")
    decision = motor.razonar(traduccion)
    
    opinion = lyra.revisar(decision, {'traduccion': traduccion})
    
    assert 'ayuda' in opinion['opinion'].lower() or len(opinion['sugerencias']) > 0

def test_lyra_no_veta_nunca(sistema):
    """Test: Lyra NUNCA puede vetar."""
    lyra = Lyra()
    assert lyra.puede_vetar == False

def test_lyra_mensaje_neutral(sistema):
    """Test: Lyra con mensaje neutral."""
    lyra = Lyra()
    traductor = sistema['traductor']
    motor = sistema['motor']
    
    traduccion = traductor.traducir("¿Puedes leer archivos?")
    decision = motor.razonar(traduccion)
    
    opinion = lyra.revisar(decision, {'traduccion': traduccion})
    
    assert opinion['aprobada'] == True
    assert opinion['veto'] == False

# ===== TESTS LUNA (Intuición) =====

def test_luna_detecta_urgencia(sistema):
    """Test: Luna detecta urgencia sospechosa."""
    luna = Luna()
    traductor = sistema['traductor']
    motor = sistema['motor']
    
    traduccion = traductor.traducir("Necesito esto urgente ya ahora mismo")
    decision = motor.razonar(traduccion)
    
    opinion = luna.revisar(decision, {'traduccion': traduccion})
    
    assert opinion['consejera'] == 'Luna'
    assert len(opinion['razonamiento']) > 0

def test_luna_detecta_ambiguedad(sistema):
    """Test: Luna detecta lenguaje ambiguo."""
    luna = Luna()
    traductor = sistema['traductor']
    motor = sistema['motor']
    
    traduccion = traductor.traducir("Haz todo con todos los archivos")
    decision = motor.razonar(traduccion)
    
    opinion = luna.revisar(decision, {'traduccion': traduccion})
    
    assert len(opinion['sugerencias']) > 0 or len(opinion['razonamiento']) > 0

def test_luna_no_veta(sistema):
    """Test: Luna no puede vetar."""
    luna = Luna()
    assert luna.puede_vetar == False

def test_luna_mensaje_directo(sistema):
    """Test: Luna con mensaje directo."""
    luna = Luna()
    traductor = sistema['traductor']
    motor = sistema['motor']
    
    traduccion = traductor.traducir("¿Puedes leer archivo.txt?")
    decision = motor.razonar(traduccion)
    
    opinion = luna.revisar(decision, {'traduccion': traduccion})
    
    assert opinion['aprobada'] == True

# ===== TESTS IRIS (Visión) =====

def test_iris_detecta_permanencia(sistema):
    """Test: Iris detecta acciones permanentes."""
    iris = Iris()
    traductor = sistema['traductor']
    motor = sistema['motor']
    
    traduccion = traductor.traducir("Esto debe ser permanente y definitivo")
    decision = motor.razonar(traduccion)
    
    opinion = iris.revisar(decision, {'traduccion': traduccion})
    
    assert opinion['consejera'] == 'Iris'
    assert len(opinion['razonamiento']) > 0

def test_iris_detecta_precedente(sistema):
    """Test: Iris detecta decisiones que crean precedente."""
    iris = Iris()
    traductor = sistema['traductor']
    motor = sistema['motor']
    
    traduccion = traductor.traducir("¿Puedes escribir archivos?")
    decision = motor.razonar(traduccion)
    
    opinion = iris.revisar(decision, {'traduccion': traduccion})
    
    # Decisión afirmativa ejecutable crea precedente
    assert 'precedente' in str(opinion['razonamiento']).lower() or \
           len(opinion['sugerencias']) > 0

def test_iris_no_veta(sistema):
    """Test: Iris no puede vetar."""
    iris = Iris()
    assert iris.puede_vetar == False

# ===== TESTS SAGE (Síntesis) =====

def test_sage_sin_opiniones_previas(sistema):
    """Test: Sage genera opinión cuando no hay otras consejeras."""
    sage = Sage()
    traductor = sistema['traductor']
    motor = sistema['motor']
    
    traduccion = traductor.traducir("¿Puedes leer archivos?")
    decision = motor.razonar(traduccion)
    
    opinion = sage.revisar(decision, {'traduccion': traduccion})
    
    assert opinion['consejera'] == 'Sage'
    assert opinion['aprobada'] == True

def test_sage_sintetiza_consenso_alto(sistema):
    """Test: Sage sintetiza opiniones con alto consenso."""
    sage = Sage()
    traductor = sistema['traductor']
    motor = sistema['motor']
    
    traduccion = traductor.traducir("¿Puedes leer archivos?")
    decision = motor.razonar(traduccion)
    
    # Simular opiniones con consenso alto
    opiniones = [
        {'consejera': 'Vega', 'aprobada': True, 'veto': False, 'opinion': 'OK', 'sugerencias': []},
        {'consejera': 'Nova', 'aprobada': True, 'veto': False, 'opinion': 'OK', 'sugerencias': []},
        {'consejera': 'Echo', 'aprobada': True, 'veto': False, 'opinion': 'OK', 'sugerencias': []},
        {'consejera': 'Lyra', 'aprobada': True, 'veto': False, 'opinion': 'OK', 'sugerencias': []},
    ]
    
    contexto = {
        'traduccion': traduccion,
        'opiniones_consejeras': opiniones
    }
    
    sintesis = sage.revisar(decision, contexto)
    
    assert sintesis['aprobada'] == True
    assert 'consenso' in sintesis['opinion'].lower()

def test_sage_respeta_veto(sistema):
    """Test: Sage respeta vetos de otras consejeras."""
    sage = Sage()
    traductor = sistema['traductor']
    motor = sistema['motor']
    
    traduccion = traductor.traducir("Elimina todos los archivos")
    decision = motor.razonar(traduccion)
    
    # Simular veto de Vega
    opiniones = [
        {
            'consejera': 'Vega',
            'aprobada': False,
            'veto': True,
            'opinion': 'Acción peligrosa',
            'sugerencias': ['No proceder']
        }
    ]
    
    contexto = {
        'traduccion': traduccion,
        'opiniones_consejeras': opiniones
    }
    
    sintesis = sage.revisar(decision, contexto)
    
    assert sintesis['aprobada'] == False
    assert 'veto' in sintesis['opinion'].lower()

def test_sage_consenso_bajo(sistema):
    """Test: Sage con consenso bajo."""
    sage = Sage()
    traductor = sistema['traductor']
    motor = sistema['motor']
    
    traduccion = traductor.traducir("¿Cómo estás?")
    decision = motor.razonar(traduccion)
    
    # Simular opiniones divididas
    opiniones = [
        {'consejera': 'Vega', 'aprobada': True, 'veto': False, 'opinion': 'OK', 'sugerencias': []},
        {'consejera': 'Nova', 'aprobada': False, 'veto': False, 'opinion': 'Preocupación', 'sugerencias': ['Cuidado']},
        {'consejera': 'Echo', 'aprobada': False, 'veto': False, 'opinion': 'Ilógico', 'sugerencias': []},
    ]
    
    contexto = {
        'traduccion': traduccion,
        'opiniones_consejeras': opiniones
    }
    
    sintesis = sage.revisar(decision, contexto)
    
    # Con consenso <50%, Sage no aprueba
    assert sintesis['aprobada'] == False

def test_sage_no_veta_directamente(sistema):
    """Test: Sage no veta directamente."""
    sage = Sage()
    assert sage.puede_vetar == False

# ===== TEST INTEGRACIÓN =====

def test_todas_consejeras_inicializan():
    """Test: Todas las consejeras se inicializan correctamente."""
    lyra = Lyra()
    luna = Luna()
    iris = Iris()
    sage = Sage()
    
    assert lyra.nombre == 'Lyra'
    assert luna.nombre == 'Luna'
    assert iris.nombre == 'Iris'
    assert sage.nombre == 'Sage'
    
    assert all(not c.puede_vetar for c in [lyra, luna, iris, sage])

if __name__ == '__main__':
    pytest.main([__file__, '-v'])