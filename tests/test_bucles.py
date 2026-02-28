"""
Tests para Bucles Autónomos - Fase 2.
"""
import pytest
import time
from bucles.base_bucle import BaseBucle
from bucles.bucle_corto import BucleCorto
from bucles.bucle_medio import BucleMedio
from bucles.bucle_largo import BucleLargo
from bucles.gestor_bucles import GestorBucles

# ===== TESTS BASE BUCLE =====

class BucleTest(BaseBucle):
    """Implementación de prueba de BaseBucle."""
    def __init__(self):
        super().__init__(nombre="Test", intervalo_segundos=1)
        self.contador = 0
    
    def procesar(self):
        self.contador += 1
        return {'contador': self.contador}

def test_base_bucle_crear():
    """Test: Crear bucle base."""
    bucle = BucleTest()
    assert bucle.nombre == "Test"
    assert bucle.intervalo_segundos == 1
    assert bucle.esta_activo() == False

def test_base_bucle_iniciar_detener():
    """Test: Iniciar y detener bucle."""
    bucle = BucleTest()
    
    # Iniciar
    assert bucle.iniciar() == True
    assert bucle.esta_activo() == True
    
    # Esperar para que ejecute al menos una vez
    time.sleep(1.2)  # Reducido de 1.5 a 1.2
    assert bucle.contador >= 1
    
    # Detener
    assert bucle.detener() == True
    assert bucle.esta_activo() == False

def test_base_bucle_estadisticas():
    """Test: Estadísticas de bucle."""
    bucle = BucleTest()
    bucle.iniciar()
    time.sleep(1.2)  # Reducido de 1.5 a 1.2
    bucle.detener()
    
    stats = bucle.obtener_estadisticas()
    assert stats['ejecuciones'] >= 1
    assert stats['nombre'] == "Test"
    assert 'tiempo_promedio_ms' in stats

def test_base_bucle_historial():
    """Test: Historial de ejecuciones."""
    bucle = BucleTest()
    bucle.iniciar()
    time.sleep(1.2)  # Reducido de 1.5 a 1.2
    bucle.detener()
    
    historial = bucle.obtener_historial()
    assert len(historial) >= 1
    assert historial[0]['exito'] == True

# ===== TESTS BUCLE CORTO =====

def test_bucle_corto_crear():
    """Test: Crear bucle corto."""
    bucle = BucleCorto()
    assert bucle.nombre == "BucleCorto"
    assert bucle.intervalo_segundos == 60

def test_bucle_corto_registrar_conceptos():
    """Test: Registrar conceptos usados."""
    bucle = BucleCorto()
    
    # Registrar algunos conceptos
    bucle.registrar_concepto_usado("CONCEPTO_LEER")
    bucle.registrar_concepto_usado("CONCEPTO_LEER")
    bucle.registrar_concepto_usado("CONCEPTO_ESCRIBIR")
    bucle.registrar_concepto_usado("CONCEPTO_LEER")
    
    assert len(bucle.conceptos_recientes) == 4

def test_bucle_corto_procesar():
    """Test: Procesar conceptos."""
    bucle = BucleCorto()
    
    # Registrar conceptos
    for _ in range(5):
        bucle.registrar_concepto_usado("CONCEPTO_LEER")
    for _ in range(2):
        bucle.registrar_concepto_usado("CONCEPTO_ESCRIBIR")
    
    # Procesar
    resultado = bucle.procesar()
    
    assert resultado['conceptos_analizados'] == 7
    assert resultado['conceptos_unicos'] == 2
    assert len(resultado['conceptos_calientes']) >= 1
    assert resultado['top_3'][0] == "CONCEPTO_LEER"

def test_bucle_corto_conceptos_calientes():
    """Test: Detectar conceptos calientes."""
    bucle = BucleCorto()
    
    # Registrar CONCEPTO_LEER 5 veces (suficiente para ser caliente)
    for _ in range(5):
        bucle.registrar_concepto_usado("CONCEPTO_LEER")
    
    bucle.procesar()
    calientes = bucle.obtener_conceptos_calientes()
    
    assert len(calientes) >= 1
    assert calientes[0]['concepto_id'] == "CONCEPTO_LEER"
    assert calientes[0]['usos'] == 5

def test_bucle_corto_limitar_ventana():
    """Test: Limitar ventana de conceptos."""
    bucle = BucleCorto()
    bucle.max_conceptos_recientes = 5
    
    # Registrar más de 5
    for i in range(10):
        bucle.registrar_concepto_usado(f"CONCEPTO_{i}")
    
    # Debe mantener solo los últimos 5
    assert len(bucle.conceptos_recientes) == 5

# ===== TESTS BUCLE MEDIO =====

def test_bucle_medio_crear():
    """Test: Crear bucle medio."""
    bucle = BucleMedio()
    assert bucle.nombre == "BucleMedio"
    assert bucle.intervalo_segundos == 120

def test_bucle_medio_registrar_decisiones():
    """Test: Registrar decisiones."""
    bucle = BucleMedio()
    
    # Registrar algunas decisiones
    bucle.registrar_decision({
        'tipo': 'AFIRMATIVA',
        'puede_ejecutar': True,
        'certeza': 0.9
    })
    bucle.registrar_decision({
        'tipo': 'SALUDO',
        'puede_ejecutar': False,
        'certeza': 0.8
    })
    
    assert len(bucle.decisiones_recientes) == 2

def test_bucle_medio_procesar():
    """Test: Procesar decisiones."""
    bucle = BucleMedio()
    
    # Registrar varias decisiones
    for _ in range(5):
        bucle.registrar_decision({
            'tipo': 'AFIRMATIVA',
            'puede_ejecutar': True,
            'certeza': 0.9
        })
    for _ in range(2):
        bucle.registrar_decision({
            'tipo': 'NEGATIVA',
            'puede_ejecutar': False,
            'certeza': 0.7
        })
    
    # Procesar
    resultado = bucle.procesar()
    
    assert resultado['decisiones_analizadas'] == 7
    assert resultado['tasa_ejecucion'] > 0
    assert resultado['certeza_promedio'] > 0

def test_bucle_medio_detectar_patrones():
    """Test: Detectar patrones conversacionales."""
    bucle = BucleMedio()
    
    # Registrar secuencia de saludos
    for _ in range(3):
        bucle.registrar_decision({
            'tipo': 'SALUDO',
            'puede_ejecutar': False,
            'certeza': 0.9
        })
    
    bucle.procesar()
    patrones = bucle.obtener_patrones()
    
    # Debe detectar patrón de interacción social
    assert len(patrones) > 0
    assert any(p['tipo'] == 'INTERACCION_SOCIAL' for p in patrones)

def test_bucle_medio_patron_no_entendido():
    """Test: Detectar patrón de comunicación problemática."""
    bucle = BucleMedio()
    
    # Registrar muchas decisiones NO_ENTENDIDO
    for _ in range(5):
        bucle.registrar_decision({
            'tipo': 'NO_ENTENDIDO',
            'puede_ejecutar': False,
            'certeza': 0.3
        })
    
    bucle.procesar()
    patrones = bucle.obtener_patrones()
    
    # Debe detectar comunicación problemática
    assert any(p['tipo'] == 'COMUNICACION_PROBLEMATICA' for p in patrones)

# ===== TESTS BUCLE LARGO =====

def test_bucle_largo_crear():
    """Test: Crear bucle largo."""
    bucle = BucleLargo()
    assert bucle.nombre == "BucleLargo"
    assert bucle.intervalo_segundos == 600

def test_bucle_largo_configurar():
    """Test: Configurar dependencias."""
    bucle_corto = BucleCorto()
    bucle_medio = BucleMedio()
    bucle_largo = BucleLargo()
    
    bucle_largo.configurar_bucles(bucle_corto, bucle_medio)
    
    assert bucle_largo.bucle_corto is bucle_corto
    assert bucle_largo.bucle_medio is bucle_medio

def test_bucle_largo_procesar_sin_datos():
    """Test: Procesar sin datos."""
    bucle_largo = BucleLargo()
    
    resultado = bucle_largo.procesar()
    
    assert resultado['insights_generados'] >= 0
    assert resultado['conceptos_analizados'] == 0

def test_bucle_largo_generar_insights():
    """Test: Generar insights con datos."""
    bucle_corto = BucleCorto()
    bucle_medio = BucleMedio()
    bucle_largo = BucleLargo()
    bucle_largo.configurar_bucles(bucle_corto, bucle_medio)
    
    # Preparar datos en bucle corto
    for _ in range(10):
        bucle_corto.registrar_concepto_usado("CONCEPTO_LEER")
    bucle_corto.procesar()
    
    # Preparar datos en bucle medio
    for _ in range(5):
        bucle_medio.registrar_decision({
            'tipo': 'AFIRMATIVA',
            'puede_ejecutar': True,
            'certeza': 0.9
        })
    bucle_medio.procesar()
    
    # Procesar en bucle largo
    resultado = bucle_largo.procesar()
    
    assert resultado['insights_generados'] > 0
    assert resultado['conceptos_analizados'] > 0

def test_bucle_largo_ajustes_recomendados():
    """Test: Generar ajustes recomendados."""
    bucle_corto = BucleCorto()
    bucle_largo = BucleLargo()
    bucle_largo.configurar_bucles(bucle_corto, None)
    
    # Usar concepto frecuentemente
    for _ in range(10):
        bucle_corto.registrar_concepto_usado("CONCEPTO_LEER")
    bucle_corto.procesar()
    
    # Procesar
    bucle_largo.procesar()
    ajustes = bucle_largo.obtener_ajustes_recomendados()
    
    assert len(ajustes) > 0
    assert ajustes[0]['tipo'] == 'AUMENTAR_GROUNDING'
    assert ajustes[0]['concepto_id'] == "CONCEPTO_LEER"

# ===== TESTS GESTOR BUCLES =====

def test_gestor_crear():
    """Test: Crear gestor de bucles."""
    gestor = GestorBucles()
    
    assert gestor.bucle_corto is not None
    assert gestor.bucle_medio is not None
    assert gestor.bucle_largo is not None

def test_gestor_iniciar_detener():
    """Test: Iniciar y detener todos los bucles."""
    gestor = GestorBucles()
    
    # Iniciar
    resultados_inicio = gestor.iniciar_todos()
    assert all(resultados_inicio.values())
    
    time.sleep(0.2)  # Reducido de 0.5 a 0.2 - solo verificar que iniciaron
    
    # Detener (ahora es rápido con sleep interrumpible)
    resultados_detencion = gestor.detener_todos()
    assert all(resultados_detencion.values())

def test_gestor_registrar_concepto():
    """Test: Registrar concepto usado."""
    gestor = GestorBucles()
    
    gestor.registrar_concepto_usado("CONCEPTO_LEER")
    gestor.registrar_concepto_usado("CONCEPTO_ESCRIBIR")
    
    assert len(gestor.bucle_corto.conceptos_recientes) == 2

def test_gestor_registrar_decision():
    """Test: Registrar decisión."""
    gestor = GestorBucles()
    
    gestor.registrar_decision({
        'tipo': 'AFIRMATIVA',
        'puede_ejecutar': True,
        'certeza': 0.9
    })
    
    assert len(gestor.bucle_medio.decisiones_recientes) == 1

def test_gestor_estado_sistema():
    """Test: Estado del sistema."""
    gestor = GestorBucles()
    
    estado = gestor.estado_sistema()
    
    assert 'bucles' in estado
    assert 'resumen' in estado
    assert 'corto' in estado['bucles']
    assert 'medio' in estado['bucles']
    assert 'largo' in estado['bucles']

def test_gestor_obtener_estadisticas():
    """Test: Obtener estadísticas de bucles."""
    gestor = GestorBucles()
    
    # Todas las estadísticas
    stats_todas = gestor.obtener_estadisticas()
    assert 'corto' in stats_todas
    assert 'medio' in stats_todas
    assert 'largo' in stats_todas
    
    # Estadística específica
    stats_corto = gestor.obtener_estadisticas('corto')
    assert stats_corto['nombre'] == 'BucleCorto'

def test_gestor_obtener_conceptos_calientes():
    """Test: Obtener conceptos calientes."""
    gestor = GestorBucles()
    
    for _ in range(5):
        gestor.registrar_concepto_usado("CONCEPTO_LEER")
    
    gestor.bucle_corto.procesar()
    calientes = gestor.obtener_conceptos_calientes()
    
    assert len(calientes) > 0

def test_gestor_obtener_patrones():
    """Test: Obtener patrones."""
    gestor = GestorBucles()
    
    for _ in range(3):
        gestor.registrar_decision({'tipo': 'SALUDO', 'puede_ejecutar': False, 'certeza': 0.9})
    
    gestor.bucle_medio.procesar()
    patrones = gestor.obtener_patrones()
    
    assert isinstance(patrones, list)

def test_gestor_limpiar_historial():
    """Test: Limpiar historial de todos los bucles."""
    gestor = GestorBucles()
    
    # Agregar datos
    gestor.registrar_concepto_usado("CONCEPTO_LEER")
    gestor.registrar_decision({'tipo': 'AFIRMATIVA', 'puede_ejecutar': True, 'certeza': 0.9})
    
    # Limpiar
    gestor.limpiar_historial_todos()
    
    assert len(gestor.bucle_corto.conceptos_recientes) == 0
    assert len(gestor.bucle_medio.decisiones_recientes) == 0

if __name__ == '__main__':
    pytest.main([__file__, '-v'])