"""
Tests para Vocabulario Expandido.

Verifica la expansión con Python avanzado, Semana 3, Semana 4 y Fase 3 completa.
Total esperado: 460+ conceptos.
"""
import pytest
from vocabulario.gestor_vocabulario import GestorVocabulario

@pytest.fixture
def gestor():
    """Gestor con vocabulario expandido."""
    return GestorVocabulario()

def test_total_conceptos_expandido(gestor):
    """Test: Total debe ser 460+ (Fase 1+2+3 completa)."""
    conceptos = gestor.obtener_todos()
    # Semana 1-4: 225 + Semanas 5-10: 240+ = 465+ conceptos
    assert len(conceptos) >= 460, f"Esperados 460+, encontrados {len(conceptos)}"
    assert len(conceptos) <= 500, f"Demasiados conceptos: {len(conceptos)}"

def test_conceptos_python_avanzado(gestor):
    """Test: Conceptos de Python avanzado presentes."""
    # Verificar algunos conceptos avanzados
    assert gestor.buscar_por_palabra("async") is not None
    assert gestor.buscar_por_palabra("await") is not None
    assert gestor.buscar_por_palabra("yield") is not None
    assert gestor.buscar_por_palabra("lambda") is not None

def test_grounding_promedio_expandido(gestor):
    """Test: Grounding promedio se mantiene >= 0.70 con expansión."""
    stats = gestor.estadisticas()
    assert stats['grounding_promedio'] >= 0.70, \
        f"Grounding degradado: {stats['grounding_promedio']}"

def test_sin_duplicados_expandido(gestor):
    """Test: No debe haber IDs duplicados en vocabulario expandido."""
    conceptos = gestor.obtener_todos()
    ids = [c.id for c in conceptos]
    
    # Identificar duplicados si existen
    duplicados = [id for id in set(ids) if ids.count(id) > 1]
    assert len(duplicados) == 0, f"IDs duplicados encontrados: {duplicados}"
    
    assert len(ids) == len(set(ids)), "Hay IDs duplicados"

if __name__ == '__main__':
    pytest.main([__file__, '-v'])