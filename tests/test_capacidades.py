"""
Tests para CapacidadesBell - Operaciones ejecutables.
"""
import pytest
import tempfile
import os
from pathlib import Path
from core.capacidades_bell import CapacidadesBell

@pytest.fixture
def archivo_temporal():
    """Crea archivo temporal para tests."""
    fd, ruta = tempfile.mkstemp(suffix='.txt')
    os.close(fd)
    yield ruta
    # Limpiar después del test
    if Path(ruta).exists():
        Path(ruta).unlink()

def test_leer_archivo(archivo_temporal):
    """Test: Leer archivo existente."""
    contenido = "Hola desde Belladonna"
    Path(archivo_temporal).write_text(contenido, encoding='utf-8')
    
    resultado = CapacidadesBell.leer_archivo(archivo_temporal)
    assert resultado == contenido

def test_escribir_archivo(archivo_temporal):
    """Test: Escribir en archivo."""
    contenido = "Texto de prueba"
    exito = CapacidadesBell.escribir_archivo(archivo_temporal, contenido)
    
    assert exito == True
    assert Path(archivo_temporal).read_text(encoding='utf-8') == contenido

def test_archivo_existe(archivo_temporal):
    """Test: Verificar si archivo existe."""
    assert CapacidadesBell.archivo_existe(archivo_temporal) == True
    assert CapacidadesBell.archivo_existe('/ruta/inexistente.txt') == False

def test_obtener_tamaño_archivo(archivo_temporal):
    """Test: Obtener tamaño de archivo."""
    contenido = "12345"  # 5 bytes
    Path(archivo_temporal).write_text(contenido, encoding='utf-8')
    
    tamaño = CapacidadesBell.obtener_tamaño_archivo(archivo_temporal)
    assert tamaño == 5

def test_listar_directorio():
    """Test: Listar directorio."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Crear algunos archivos
        Path(tmpdir, 'archivo1.txt').touch()
        Path(tmpdir, 'archivo2.txt').touch()
        
        archivos = CapacidadesBell.listar_directorio(tmpdir)
        assert len(archivos) == 2

if __name__ == '__main__':
    pytest.main([__file__, '-v'])