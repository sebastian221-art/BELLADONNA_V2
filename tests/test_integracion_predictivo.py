"""
Tests de Integración Predictiva - Fase 3 Semana 9.
Verifica que ExtensionGroundingMultidimensional integra correctamente
el grounding predictivo (dimensión 9).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from core.concepto_anclado import ConceptoAnclado, TipoConcepto
from extension_grounding import ExtensionGroundingMultidimensional
from grounding_predictivo import NivelConfianzaPrediccion


# ─── Fixtures ──────────────────────────────────────────────────────────────

@pytest.fixture
def concepto():
    return ConceptoAnclado(
        id='CONCEPTO_LEER',
        palabras_español=['leer', 'lectura'],
        tipo=TipoConcepto.OPERACION_SISTEMA,      # ← valor correcto
        confianza_grounding=1.0,
    )


@pytest.fixture
def ext(concepto):
    return ExtensionGroundingMultidimensional(concepto)


@pytest.fixture
def ext_con_historial(ext):
    """Extensión con 10 resultados exitosos registrados."""
    for _ in range(10):
        ext.registrar_resultado_predictivo(True, 0.9)
    return ext


# ─── Tests básicos ─────────────────────────────────────────────────────────

def test_grounding_predictivo_empieza_en_cero(ext):
    assert ext.grounding_predictivo == 0.0


def test_gestor_predictivo_inicial_none(ext):
    assert ext._gpred is None


def test_inicializar_gestor_predictivo(ext):
    ext.inicializar_gestor_predictivo()
    assert ext._gpred is not None


def test_registrar_resultado_inicializa_automaticamente(ext):
    ext.registrar_resultado_predictivo(True, 0.8)
    assert ext._gpred is not None


# ─── Tests de historial y score ────────────────────────────────────────────

def test_registrar_resultado_actualiza_grounding(ext):
    before = ext.grounding_predictivo
    ext.registrar_resultado_predictivo(True, 0.9)
    assert ext.grounding_predictivo > before


def test_mas_resultados_mayor_grounding(ext):
    ext.registrar_resultado_predictivo(True, 0.8)
    g1 = ext.grounding_predictivo
    for _ in range(9):
        ext.registrar_resultado_predictivo(True, 0.8)
    g10 = ext.grounding_predictivo
    assert g10 > g1


def test_fallos_bajan_grounding(concepto):
    ext_a = ExtensionGroundingMultidimensional(concepto)
    ext_b = ExtensionGroundingMultidimensional(concepto)
    for _ in range(8):
        ext_a.registrar_resultado_predictivo(False, 0.2)
    for _ in range(8):
        ext_b.registrar_resultado_predictivo(True, 0.9)
    assert ext_b.grounding_predictivo > ext_a.grounding_predictivo


# ─── Tests de predicción ───────────────────────────────────────────────────

def test_predecir_sin_historial_retorna_sin_datos(ext):
    pred = ext.predecir_exito('leer')
    assert pred.confianza == NivelConfianzaPrediccion.SIN_DATOS


def test_predecir_con_historial_exitoso(ext_con_historial):
    pred = ext_con_historial.predecir_exito('leer')
    assert pred.es_favorable
    assert pred.n_muestras == 10


def test_predecir_accion_en_prediccion(ext_con_historial):
    pred = ext_con_historial.predecir_exito('leer archivo')
    assert pred.accion == 'leer archivo'


def test_predecir_retorna_recomendacion(ext_con_historial):
    pred = ext_con_historial.predecir_exito()
    assert len(pred.recomendacion) > 0


def test_predecir_tendencia_con_historial_estable(ext_con_historial):
    from grounding_predictivo import TendenciaHistorica
    pred = ext_con_historial.predecir_exito()
    assert pred.tendencia in (
        TendenciaHistorica.ESTABLE,
        TendenciaHistorica.MEJORANDO,
    )


# ─── Tests de diagnóstico ──────────────────────────────────────────────────

def test_diagnostico_predictivo_sin_datos(ext):
    d = ext.diagnostico_predictivo()
    assert d['score_total'] == 0.0
    assert d['estado'] == 'SIN_DATOS'
    assert d['n_registros'] == 0


def test_diagnostico_predictivo_con_datos(ext_con_historial):
    d = ext_con_historial.diagnostico_predictivo()
    assert d['score_total'] > 0.0
    assert d['n_registros'] == 10
    assert d['tasa_exito'] == 1.0


def test_diagnostico_predictivo_incluye_todos_campos(ext_con_historial):
    d = ext_con_historial.diagnostico_predictivo()
    for campo in ('score_total', 'estado', 'n_registros', 'tasa_exito', 'score_promedio'):
        assert campo in d


# ─── Tests de integración con 9 dimensiones ────────────────────────────────

def test_dimensiones_activas_cuenta_predictivo(ext):
    n_sin = ext._contar_dimensiones_activas()
    ext.registrar_resultado_predictivo(True, 0.9)
    assert ext._contar_dimensiones_activas() == n_sin + 1


def test_grounding_total_mejora_con_predictivo(ext):
    total_sin = ext.calcular_grounding_total()
    for _ in range(8):
        ext.registrar_resultado_predictivo(True, 0.9)
    total_con = ext.calcular_grounding_total()
    assert total_con > total_sin


def test_resumen_incluye_grounding_predictivo(ext_con_historial):
    r = ext_con_historial.obtener_resumen()
    assert 'grounding_predictivo' in r
    assert r['grounding_predictivo'] > 0.0


def test_resumen_incluye_diagnostico_predictivo(ext_con_historial):
    r = ext_con_historial.obtener_resumen()
    assert 'diagnostico_predictivo' in r
    assert r['diagnostico_predictivo']['n_registros'] == 10


def test_extensiones_predictivas_independientes(concepto):
    """Dos extensiones del mismo concepto tienen historiales separados."""
    ext_a = ExtensionGroundingMultidimensional(concepto)
    ext_b = ExtensionGroundingMultidimensional(concepto)
    for _ in range(5):
        ext_a.registrar_resultado_predictivo(True, 0.9)
    assert ext_a.grounding_predictivo > 0.0
    assert ext_b.grounding_predictivo == 0.0


def test_grounding_total_con_comp_y_predictivo(ext):
    """comp(1.0*0.20) + predictivo(>0*0.16) > 0.20"""
    for _ in range(5):
        ext.registrar_resultado_predictivo(True, 0.9)
    assert ext.calcular_grounding_total() > 0.20