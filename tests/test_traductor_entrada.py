"""
Tests para TraductorEntrada.
"""
import pytest
from traduccion.traductor_entrada import TraductorEntrada
from vocabulario.gestor_vocabulario import GestorVocabulario

@pytest.fixture
def traductor():
    """Crea traductor con vocabulario completo."""
    gestor = GestorVocabulario()
    return TraductorEntrada(gestor)

def test_traduccion_simple(traductor):
    """Test: Traducir frase simple."""
    resultado = traductor.traducir("leer archivo")
    
    assert len(resultado['conceptos']) >= 2
    assert 'CONCEPTO_LEER' in resultado['conceptos_ids']
    assert 'CONCEPTO_ARCHIVO' in resultado['conceptos_ids']
    assert resultado['confianza'] >= 0.8

def test_pregunta_capacidad(traductor):
    """Test: Detectar pregunta sobre capacidades."""
    resultado = traductor.traducir("¿Puedes leer archivos?")
    
    assert resultado['es_pregunta'] == True
    assert resultado['intencion'] == 'PREGUNTA_CAPACIDAD'
    assert 'CONCEPTO_PODER' in resultado['conceptos_ids']
    assert 'CONCEPTO_LEER' in resultado['conceptos_ids']

def test_saludo(traductor):
    """Test: Detectar saludo."""
    resultado = traductor.traducir("Hola Bell")
    
    assert resultado['intencion'] == 'SALUDO'
    assert 'CONCEPTO_HOLA' in resultado['conceptos_ids']

def test_palabras_desconocidas(traductor):
    """Test: Reportar palabras desconocidas."""
    resultado = traductor.traducir("xyzabc qwerty asdfgh")
    
    assert len(resultado['palabras_desconocidas']) > 0
    assert resultado['confianza'] == 0.0

def test_confianza_alta(traductor):
    """Test: Alta confianza con palabras conocidas."""
    resultado = traductor.traducir("¿Puedes leer archivos?")
    
    # Todas las palabras importantes están en vocabulario
    assert resultado['confianza'] >= 0.85

def test_confianza_media(traductor):
    """Test: Confianza media con algunas desconocidas."""
    resultado = traductor.traducir("¿Puedes procesar blockchain?")
    
    # "puedes" conocida, "blockchain" desconocida
    assert 0.3 <= resultado['confianza'] <= 0.7

def test_sin_duplicados(traductor):
    """Test: No duplicar conceptos en traducción."""
    resultado = traductor.traducir("leer leer leer archivo")
    
    # "leer" aparece 3 veces, pero CONCEPTO_LEER solo una vez
    ids = resultado['conceptos_ids']
    assert len(ids) == len(set(ids)), "Hay conceptos duplicados"

if __name__ == '__main__':
    pytest.main([__file__, '-v'])