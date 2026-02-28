"""
Tests para Sistema de Memoria Persistente - Fase 2.
"""
import pytest
import os
import shutil
from datetime import datetime
from pathlib import Path

from memoria.almacen import AlmacenJSON
from memoria.gestor_memoria import GestorMemoria

# Directorio temporal para tests
TEST_DIR = "test_memoria_temp"

@pytest.fixture
def limpiar_test_dir():
    """Limpia directorio de test antes y después."""
    # Limpiar antes
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)
    
    yield
    
    # Limpiar después
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)

# ===== TESTS ALMACEN JSON =====

def test_almacen_crear(limpiar_test_dir):
    """Test: Crear almacén JSON."""
    almacen = AlmacenJSON(TEST_DIR)
    assert almacen.directorio_base == Path(TEST_DIR)
    assert almacen.directorio_base.exists()

def test_almacen_guardar_cargar(limpiar_test_dir):
    """Test: Guardar y cargar datos."""
    almacen = AlmacenJSON(TEST_DIR)
    
    # Guardar dato
    dato = {'id': 'TEST', 'valor': 42}
    assert almacen.guardar('conceptos', dato) == True
    
    # Cargar dato
    datos = almacen.cargar('conceptos')
    assert len(datos) == 1
    assert datos[0]['id'] == 'TEST'
    assert datos[0]['valor'] == 42

def test_almacen_guardar_multiples(limpiar_test_dir):
    """Test: Guardar múltiples datos."""
    almacen = AlmacenJSON(TEST_DIR)
    
    # Guardar varios datos
    almacen.guardar('conceptos', {'id': 'A', 'valor': 1})
    almacen.guardar('conceptos', {'id': 'B', 'valor': 2})
    almacen.guardar('conceptos', {'id': 'C', 'valor': 3})
    
    # Cargar todos
    datos = almacen.cargar('conceptos')
    assert len(datos) == 3

def test_almacen_buscar(limpiar_test_dir):
    """Test: Buscar datos con filtro."""
    almacen = AlmacenJSON(TEST_DIR)
    
    # Guardar datos
    almacen.guardar('conceptos', {'id': 'A', 'tipo': 'X', 'valor': 1})
    almacen.guardar('conceptos', {'id': 'B', 'tipo': 'Y', 'valor': 2})
    almacen.guardar('conceptos', {'id': 'C', 'tipo': 'X', 'valor': 3})
    
    # Buscar con filtro
    resultados = almacen.buscar('conceptos', {'tipo': 'X'})
    assert len(resultados) == 2
    assert all(d['tipo'] == 'X' for d in resultados)

def test_almacen_buscar_con_limite(limpiar_test_dir):
    """Test: Buscar con límite de resultados."""
    almacen = AlmacenJSON(TEST_DIR)
    
    # Guardar 5 datos
    for i in range(5):
        almacen.guardar('conceptos', {'id': f'C{i}', 'valor': i})
    
    # Buscar con límite
    resultados = almacen.buscar('conceptos', limite=3)
    assert len(resultados) == 3

def test_almacen_contar(limpiar_test_dir):
    """Test: Contar registros."""
    almacen = AlmacenJSON(TEST_DIR)
    
    # Guardar datos
    for i in range(7):
        almacen.guardar('conceptos', {'id': f'C{i}'})
    
    assert almacen.contar('conceptos') == 7

def test_almacen_limpiar(limpiar_test_dir):
    """Test: Limpiar datos de un tipo."""
    almacen = AlmacenJSON(TEST_DIR)
    
    # Guardar datos
    almacen.guardar('conceptos', {'id': 'A'})
    almacen.guardar('decisiones', {'id': 'B'})
    
    # Limpiar conceptos
    almacen.limpiar('conceptos')
    
    assert almacen.contar('conceptos') == 0
    assert almacen.contar('decisiones') == 1

def test_almacen_limpiar_todo(limpiar_test_dir):
    """Test: Limpiar todos los datos."""
    almacen = AlmacenJSON(TEST_DIR)
    
    # Guardar datos en varios tipos
    almacen.guardar('conceptos', {'id': 'A'})
    almacen.guardar('decisiones', {'id': 'B'})
    almacen.guardar('patrones', {'id': 'C'})
    
    # Limpiar todo
    almacen.limpiar_todo()
    
    assert almacen.contar('conceptos') == 0
    assert almacen.contar('decisiones') == 0
    assert almacen.contar('patrones') == 0

def test_almacen_estadisticas(limpiar_test_dir):
    """Test: Obtener estadísticas del almacén."""
    almacen = AlmacenJSON(TEST_DIR)
    
    # Guardar datos
    almacen.guardar('conceptos', {'id': 'A'})
    almacen.guardar('conceptos', {'id': 'B'})
    almacen.guardar('decisiones', {'id': 'C'})
    
    stats = almacen.obtener_estadisticas()
    
    assert stats['conteos']['conceptos'] == 2
    assert stats['conteos']['decisiones'] == 1

# ===== TESTS GESTOR MEMORIA =====

def test_gestor_crear(limpiar_test_dir):
    """Test: Crear gestor de memoria."""
    gestor = GestorMemoria(TEST_DIR)
    assert gestor.almacen is not None
    assert gestor.sesion_actual is None

def test_gestor_sesion(limpiar_test_dir):
    """Test: Iniciar y finalizar sesión."""
    gestor = GestorMemoria(TEST_DIR)
    
    # Iniciar sesión
    id_sesion = gestor.iniciar_sesion()
    assert id_sesion is not None
    assert gestor.sesion_actual == id_sesion
    
    # Finalizar sesión
    gestor.finalizar_sesion()
    assert gestor.sesion_actual is None

def test_gestor_guardar_concepto(limpiar_test_dir):
    """Test: Guardar concepto usado."""
    gestor = GestorMemoria(TEST_DIR)
    gestor.iniciar_sesion()
    
    # Guardar concepto
    gestor.guardar_concepto_usado('CONCEPTO_LEER', certeza=0.9)
    
    # Verificar que se guardó
    conceptos = gestor.almacen.cargar('conceptos')
    assert len(conceptos) == 1
    assert conceptos[0]['concepto_id'] == 'CONCEPTO_LEER'
    assert conceptos[0]['ultima_certeza'] == 0.9

def test_gestor_conceptos_mas_usados(limpiar_test_dir):
    """Test: Obtener conceptos más usados."""
    gestor = GestorMemoria(TEST_DIR)
    gestor.iniciar_sesion()
    
    # Usar varios conceptos
    for _ in range(5):
        gestor.guardar_concepto_usado('CONCEPTO_LEER')
    for _ in range(3):
        gestor.guardar_concepto_usado('CONCEPTO_ESCRIBIR')
    for _ in range(1):
        gestor.guardar_concepto_usado('CONCEPTO_CREAR')
    
    # Obtener ranking
    mas_usados = gestor.obtener_conceptos_mas_usados(3)
    
    assert len(mas_usados) == 3
    assert mas_usados[0]['concepto_id'] == 'CONCEPTO_LEER'
    assert mas_usados[0]['usos'] == 5
    assert mas_usados[1]['concepto_id'] == 'CONCEPTO_ESCRIBIR'
    assert mas_usados[1]['usos'] == 3

def test_gestor_guardar_decision(limpiar_test_dir):
    """Test: Guardar decisión."""
    gestor = GestorMemoria(TEST_DIR)
    gestor.iniciar_sesion()
    
    # Guardar decisión
    decision = {
        'tipo': 'AFIRMATIVA',
        'puede_ejecutar': True,
        'certeza': 0.9,
        'conceptos_principales': ['CONCEPTO_LEER'],
        'grounding_promedio': 0.85
    }
    gestor.guardar_decision(decision)
    
    # Verificar
    decisiones = gestor.almacen.cargar('decisiones')
    assert len(decisiones) == 1
    assert decisiones[0]['tipo'] == 'AFIRMATIVA'
    assert decisiones[0]['puede_ejecutar'] == True

def test_gestor_estadisticas_decisiones(limpiar_test_dir):
    """Test: Estadísticas de decisiones."""
    gestor = GestorMemoria(TEST_DIR)
    gestor.iniciar_sesion()
    
    # Guardar varias decisiones
    for i in range(10):
        gestor.guardar_decision({
            'tipo': 'AFIRMATIVA',
            'puede_ejecutar': i % 2 == 0,  # 50% ejecutables
            'certeza': 0.8,
            'conceptos_principales': [],
            'grounding_promedio': 0.75
        })
    
    stats = gestor.obtener_estadisticas_decisiones()
    
    assert stats['total'] == 10
    assert stats['tasa_ejecucion'] == 50.0
    assert stats['certeza_promedio'] == 0.8

def test_gestor_guardar_patron(limpiar_test_dir):
    """Test: Guardar patrón detectado."""
    gestor = GestorMemoria(TEST_DIR)
    gestor.iniciar_sesion()
    
    # Guardar patrón
    patron = {
        'tipo': 'INTERACCION_SOCIAL',
        'descripcion': 'Usuario está siendo cortés',
        'frecuencia': 5,
        'confianza': 0.9
    }
    gestor.guardar_patron(patron)
    
    # Verificar
    patrones = gestor.almacen.cargar('patrones')
    assert len(patrones) == 1
    assert patrones[0]['tipo_patron'] == 'INTERACCION_SOCIAL'

def test_gestor_guardar_insight(limpiar_test_dir):
    """Test: Guardar insight generado."""
    gestor = GestorMemoria(TEST_DIR)
    
    # Guardar insight
    insight = {
        'tipo': 'CONCEPTO_DOMINANTE',
        'descripcion': 'CONCEPTO_LEER domina el uso',
        'relevancia': 'ALTA',
        'datos': {'concepto_id': 'CONCEPTO_LEER', 'porcentaje': 45}
    }
    gestor.guardar_insight(insight)
    
    # Verificar
    insights = gestor.almacen.cargar('insights')
    assert len(insights) == 1
    assert insights[0]['tipo_insight'] == 'CONCEPTO_DOMINANTE'
    assert insights[0]['relevancia'] == 'ALTA'

def test_gestor_insights_por_relevancia(limpiar_test_dir):
    """Test: Filtrar insights por relevancia."""
    gestor = GestorMemoria(TEST_DIR)
    
    # Guardar insights con diferentes relevancias
    gestor.guardar_insight({'tipo': 'A', 'descripcion': 'Test', 'relevancia': 'ALTA', 'datos': {}})
    gestor.guardar_insight({'tipo': 'B', 'descripcion': 'Test', 'relevancia': 'BAJA', 'datos': {}})
    gestor.guardar_insight({'tipo': 'C', 'descripcion': 'Test', 'relevancia': 'ALTA', 'datos': {}})
    
    # Filtrar por ALTA
    insights_alta = gestor.obtener_insights_recientes(10, relevancia='ALTA')
    
    assert len(insights_alta) == 2
    assert all(i['relevancia'] == 'ALTA' for i in insights_alta)

def test_gestor_guardar_ajuste_grounding(limpiar_test_dir):
    """Test: Guardar ajuste de grounding."""
    gestor = GestorMemoria(TEST_DIR)
    
    # Guardar ajuste
    gestor.guardar_ajuste_grounding(
        concepto_id='CONCEPTO_LEER',
        grounding_anterior=0.8,
        grounding_nuevo=0.85,
        razon='Usado frecuentemente',
        aplicado=True
    )
    
    # Verificar
    ajustes = gestor.almacen.cargar('ajustes')
    assert len(ajustes) == 1
    assert ajustes[0]['concepto_id'] == 'CONCEPTO_LEER'
    assert ajustes[0]['grounding_nuevo'] == 0.85

def test_gestor_historial_ajustes_concepto(limpiar_test_dir):
    """Test: Obtener historial de ajustes de un concepto."""
    gestor = GestorMemoria(TEST_DIR)
    
    # Guardar varios ajustes
    gestor.guardar_ajuste_grounding('CONCEPTO_LEER', 0.8, 0.85, 'Razón 1', True)
    gestor.guardar_ajuste_grounding('CONCEPTO_LEER', 0.85, 0.9, 'Razón 2', True)
    gestor.guardar_ajuste_grounding('CONCEPTO_ESCRIBIR', 0.7, 0.75, 'Razón 3', True)
    
    # Obtener historial de CONCEPTO_LEER
    historial = gestor.obtener_ajustes_concepto('CONCEPTO_LEER')
    
    assert len(historial) == 2
    assert all(a['concepto_id'] == 'CONCEPTO_LEER' for a in historial)

def test_gestor_resumen_sesion(limpiar_test_dir):
    """Test: Obtener resumen de sesión."""
    gestor = GestorMemoria(TEST_DIR)
    
    # Iniciar sesión
    id_sesion = gestor.iniciar_sesion()
    
    # Realizar actividades
    gestor.guardar_concepto_usado('CONCEPTO_LEER')
    gestor.guardar_decision({'tipo': 'AFIRMATIVA', 'puede_ejecutar': True, 'certeza': 0.9, 'conceptos_principales': [], 'grounding_promedio': 0.8})
    
    # Obtener resumen
    resumen = gestor.obtener_resumen_sesion()
    
    assert resumen is not None
    assert resumen['id_sesion'] == id_sesion
    assert resumen['conceptos_usados'] == 1
    assert resumen['decisiones_tomadas'] == 1

def test_gestor_estadisticas_globales(limpiar_test_dir):
    """Test: Obtener estadísticas globales."""
    gestor = GestorMemoria(TEST_DIR)
    gestor.iniciar_sesion()
    
    # Generar actividad
    gestor.guardar_concepto_usado('CONCEPTO_LEER')
    gestor.guardar_decision({'tipo': 'AFIRMATIVA', 'puede_ejecutar': True, 'certeza': 0.9, 'conceptos_principales': [], 'grounding_promedio': 0.8})
    gestor.guardar_patron({'tipo': 'TEST', 'descripcion': 'Test', 'frecuencia': 1, 'confianza': 0.8})
    
    stats = gestor.obtener_estadisticas_globales()
    
    assert stats['total_sesiones'] == 1
    assert stats['total_conceptos_usados'] >= 1
    assert stats['total_decisiones'] >= 1
    assert stats['total_patrones'] >= 1

def test_gestor_exportar_importar(limpiar_test_dir):
    """Test: Exportar e importar memoria."""
    gestor1 = GestorMemoria(TEST_DIR)
    gestor1.iniciar_sesion()
    
    # Guardar datos
    gestor1.guardar_concepto_usado('CONCEPTO_LEER')
    gestor1.guardar_decision({'tipo': 'AFIRMATIVA', 'puede_ejecutar': True, 'certeza': 0.9, 'conceptos_principales': [], 'grounding_promedio': 0.8})
    
    # Exportar
    archivo_export = f"{TEST_DIR}/export.json"
    assert gestor1.exportar_memoria(archivo_export) == True
    
    # Crear nuevo gestor e importar
    gestor2 = GestorMemoria(f"{TEST_DIR}_2")
    assert gestor2.importar_memoria(archivo_export) == True
    
    # Verificar que se importaron los datos
    assert gestor2.almacen.contar('conceptos') >= 1
    assert gestor2.almacen.contar('decisiones') >= 1
    
    # Limpiar directorio 2
    if os.path.exists(f"{TEST_DIR}_2"):
        shutil.rmtree(f"{TEST_DIR}_2")

def test_gestor_limpiar_memoria(limpiar_test_dir):
    """Test: Limpiar memoria."""
    gestor = GestorMemoria(TEST_DIR)
    
    # Guardar datos
    gestor.guardar_concepto_usado('CONCEPTO_LEER')
    gestor.guardar_decision({'tipo': 'AFIRMATIVA', 'puede_ejecutar': True, 'certeza': 0.9, 'conceptos_principales': [], 'grounding_promedio': 0.8})
    
    # Limpiar tipo específico
    gestor.limpiar_memoria('conceptos')
    assert gestor.almacen.contar('conceptos') == 0
    assert gestor.almacen.contar('decisiones') == 1
    
    # Limpiar todo
    gestor.limpiar_memoria()
    assert gestor.almacen.contar('decisiones') == 0

if __name__ == '__main__':
    pytest.main([__file__, '-v'])