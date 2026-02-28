"""
Tests para AnalizadorEspañol.
"""
import pytest
from traduccion.analizador_español import AnalizadorEspañol

@pytest.fixture
def analizador():
    """Crea analizador para tests."""
    return AnalizadorEspañol()

def test_analisis_basico(analizador):
    """Test: Análisis de frase simple."""
    resultado = analizador.analizar("Hola, ¿cómo estás?")
    
    assert resultado['texto_original'] == "Hola, ¿cómo estás?"
    assert 'Hola' in resultado['tokens']
    assert 'cómo' in resultado['tokens']
    assert resultado['es_pregunta'] == True

def test_extraccion_lemas(analizador):
    """Test: Lematización correcta."""
    resultado = analizador.analizar("Los archivos están guardados")
    
    # "archivos" → "archivo" (singular)
    # "están" → "estar" (infinitivo)
    # "guardados" → "guardar" (infinitivo)
    assert 'archivo' in resultado['lemas']
    assert 'estar' in resultado['lemas']

def test_deteccion_verbos(analizador):
    """Test: Detectar verbos."""
    resultado = analizador.analizar("Puedes leer archivos")
    
    assert 'poder' in resultado['verbos']  # "puedes" → "poder"
    assert 'leer' in resultado['verbos']

def test_deteccion_sustantivos(analizador):
    """Test: Detectar sustantivos."""
    resultado = analizador.analizar("El archivo está en la carpeta")
    
    assert 'archivo' in resultado['sustantivos']
    assert 'carpeta' in resultado['sustantivos']

def test_frase_simple(analizador):
    """Test: Detectar frases simples."""
    simple = analizador.analizar("Hola Bell")
    compleja = analizador.analizar("¿Puedes ayudarme a leer el archivo que está en la carpeta principal?")
    
    assert analizador.es_frase_simple(simple) == True
    assert analizador.es_frase_simple(compleja) == False

def test_palabras_clave(analizador):
    """Test: Extraer palabras clave."""
    resultado = analizador.analizar("¿Puedes leer el archivo?")
    palabras = analizador.palabras_clave(resultado)
    
    assert 'poder' in palabras  # verbo
    assert 'leer' in palabras   # verbo
    assert 'archivo' in palabras  # sustantivo

if __name__ == '__main__':
    pytest.main([__file__, '-v'])