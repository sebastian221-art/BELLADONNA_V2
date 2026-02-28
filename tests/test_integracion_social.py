"""
Tests de Integración Social - Fase 3 Semana 5.

Verifica que ExtensionGroundingMultidimensional integra correctamente
el grounding social (Semana 5) junto con las dimensiones previas.
"""
import sys
import os
import tempfile
import shutil

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pytest

from core.concepto_anclado import ConceptoAnclado, TipoConcepto
from extension_grounding import ExtensionGroundingMultidimensional
from grounding_social import (
    GestorGroundingSocial,
    ContextoSocial,
    ResultadoEvaluacionSocial,
    RolUsuario,
    NivelConfianza,
    TipoIntencion,
    IntencionInferida,
    RiesgoSocial
)
from grounding_pragmatico import FabricaDatosPragmaticos


# ─────────────────────────────────────────────
# FIXTURES
# ─────────────────────────────────────────────

@pytest.fixture
def directorio_temporal():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def concepto_leer():
    return ConceptoAnclado(
        id='CONCEPTO_LEER',
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=['leer', 'archivo'],
        confianza_grounding=1.0,
        propiedades={}
    )


@pytest.fixture
def extension_base(concepto_leer):
    """Extensión con semántico y pragmático ya activos."""
    ext = ExtensionGroundingMultidimensional(concepto_leer)
    ext.actualizar_grounding_semantico(
        embedding=np.random.rand(384),
        coherencia=0.80,
        densidad=0.70,
        similares=[('CONCEPTO_ESCRIBIR', 0.72)]
    )
    ext.registrar_datos_pragmaticos(FabricaDatosPragmaticos.para_leer_archivo())
    return ext


@pytest.fixture
def gestor_social():
    return GestorGroundingSocial()


@pytest.fixture
def ctx_desarrollador(gestor_social):
    return gestor_social.crear_contexto(
        rol=RolUsuario.DESARROLLADOR,
        solicitud="ejecuta el análisis del archivo",
        nombre="Sebastian"
    )


@pytest.fixture
def ctx_anonimo(gestor_social):
    return gestor_social.crear_contexto(
        rol=RolUsuario.ANONIMO,
        solicitud="ejecuta el sistema completo"
    )


@pytest.fixture
def ctx_consejera(gestor_social):
    return gestor_social.crear_contexto(
        rol=RolUsuario.CONSEJERA,
        solicitud="veto esta acción",
        nombre="Vega"
    )


# ─────────────────────────────────────────────
# TESTS
# ─────────────────────────────────────────────

def test_inicializar_gestor_social(extension_base):
    """Test: Gestor social empieza como None."""
    assert extension_base.gestor_social is None
    extension_base.inicializar_gestor_social()
    assert extension_base.gestor_social is not None


def test_grounding_social_empieza_en_cero(extension_base):
    """Test: Grounding social empieza en 0.0."""
    assert extension_base.grounding_social == 0.0


def test_evaluar_contexto_social_actualiza_grounding(extension_base, ctx_desarrollador):
    """Test: evaluar_contexto_social actualiza grounding_social."""
    extension_base.evaluar_contexto_social(ctx_desarrollador)
    assert extension_base.grounding_social > 0.0


def test_evaluar_contexto_social_retorna_resultado(extension_base, ctx_desarrollador):
    """Test: evaluar_contexto_social retorna ResultadoEvaluacionSocial."""
    resultado = extension_base.evaluar_contexto_social(ctx_desarrollador)
    assert isinstance(resultado, ResultadoEvaluacionSocial)


def test_puede_responder_a_desarrollador(extension_base):
    """Test: Bell puede responder a un desarrollador."""
    puede = extension_base.puede_responder_a(
        rol=RolUsuario.DESARROLLADOR,
        solicitud="ejecuta el análisis",
        nombre="Sebastian"
    )
    assert puede is True


def test_no_puede_responder_a_anonimo_ejecutar(extension_base):
    """Test: Bell no puede ejecutar para usuario anónimo."""
    puede = extension_base.puede_responder_a(
        rol=RolUsuario.ANONIMO,
        solicitud="ejecuta todos los procesos del sistema"
    )
    assert puede is False


def test_puede_responder_a_anonimo_informar(extension_base):
    """Test: Bell puede informar a un anónimo."""
    puede = extension_base.puede_responder_a(
        rol=RolUsuario.ANONIMO,
        solicitud="qué hace este concepto"
    )
    assert puede is True


def test_veto_consejera_bloquea(extension_base, ctx_consejera):
    """Test: Veto de consejera bloquea la acción."""
    resultado = extension_base.evaluar_contexto_social(ctx_consejera)
    assert resultado.puede_proceder is False
    assert resultado.veto_activo is True


def test_grounding_social_alto_desarrollador(extension_base, ctx_desarrollador):
    """Test: Grounding social alto con desarrollador e intención clara."""
    extension_base.evaluar_contexto_social(ctx_desarrollador)
    assert extension_base.grounding_social > 0.6


def test_grounding_social_bajo_anonimo(extension_base, ctx_anonimo):
    """Test: Grounding social bajo con anónimo."""
    extension_base.evaluar_contexto_social(ctx_anonimo)
    assert extension_base.grounding_social < 0.5


def test_grounding_total_con_5_dimensiones(extension_base, directorio_temporal, ctx_desarrollador):
    """Test: grounding_total con 5 dimensiones activas."""
    # Activar contextual
    extension_base.inicializar_tracker_contextual(directorio_datos=directorio_temporal)
    extension_base.registrar_uso_contextual(exito=True, duracion_ms=100)

    # Activar social
    extension_base.evaluar_contexto_social(ctx_desarrollador)

    total = extension_base.calcular_grounding_total()
    dimensiones = extension_base._contar_dimensiones_activas()

    assert dimensiones == 5
    assert total > 0.80


def test_grounding_total_mejora_con_social(extension_base, ctx_desarrollador):
    """Test: Agregar social activa la dimension social y suma al total."""
    assert extension_base.grounding_social == 0.0
    dims_antes = extension_base._contar_dimensiones_activas()

    extension_base.evaluar_contexto_social(ctx_desarrollador)

    # La dimension social debe activarse
    assert extension_base.grounding_social > 0.0
    # Debe haber una dimension mas activa
    assert extension_base._contar_dimensiones_activas() == dims_antes + 1


def test_resumen_incluye_grounding_social(extension_base, ctx_desarrollador):
    """Test: obtener_resumen incluye grounding_social."""
    extension_base.evaluar_contexto_social(ctx_desarrollador)
    resumen = extension_base.obtener_resumen()
    assert 'grounding_social' in resumen
    assert resumen['grounding_social'] > 0.0


def test_resumen_incluye_diagnostico_social(extension_base, ctx_desarrollador):
    """Test: obtener_resumen incluye diagnostico_social."""
    extension_base.evaluar_contexto_social(ctx_desarrollador)
    resumen = extension_base.obtener_resumen()
    assert 'diagnostico_social' in resumen
    assert 'score_total' in resumen['diagnostico_social']


def test_dimensiones_activas_cuenta_social(extension_base, ctx_desarrollador):
    """Test: _contar_dimensiones_activas incluye social."""
    extension_base.evaluar_contexto_social(ctx_desarrollador)
    dimensiones = extension_base._contar_dimensiones_activas()
    assert dimensiones >= 4  # comp + semántico + pragmático + social


def test_ultimo_contexto_social_guardado(extension_base, ctx_desarrollador):
    """Test: Guarda el último contexto evaluado."""
    assert extension_base.ultimo_contexto_social is None
    extension_base.evaluar_contexto_social(ctx_desarrollador)
    assert extension_base.ultimo_contexto_social is not None
    assert extension_base.ultimo_contexto_social.perfil.rol == RolUsuario.DESARROLLADOR


def test_flujo_5_dimensiones_completo(extension_base, directorio_temporal, gestor_social):
    """Test: Flujo completo con las 5 dimensiones."""
    # Dim 3: Contextual
    extension_base.inicializar_tracker_contextual(directorio_datos=directorio_temporal)
    extension_base.registrar_uso_contextual(exito=True, duracion_ms=50)

    # Dim 5: Social - Evaluación pragmática + social combinada
    ctx = gestor_social.crear_contexto(
        rol=RolUsuario.DESARROLLADOR,
        solicitud="ejecuta la lectura del archivo de datos",
        nombre="Sebastian"
    )
    resultado_social = extension_base.evaluar_contexto_social(ctx)
    assert resultado_social.puede_proceder is True

    # Evaluación pragmática en el mismo contexto
    contexto_pragmatico = {'archivo_existe': True, 'tiene_permiso_lectura': True}
    assert extension_base.puede_ejecutar_ahora(contexto_pragmatico) is True

    # Grounding total con 5 dimensiones
    total = extension_base.calcular_grounding_total()
    dims = extension_base._contar_dimensiones_activas()
    assert dims == 5
    assert total > 0.80


def test_extension_sin_social_no_bloquea(extension_base):
    """Test: Sin grounding social inicializado, Bell funciona normalmente."""
    assert extension_base.gestor_social is None
    # Debe funcionar sin error
    total = extension_base.calcular_grounding_total()
    assert isinstance(total, float)
    dims = extension_base._contar_dimensiones_activas()
    assert isinstance(dims, int)


def test_riesgo_critico_bloqueado_independiente_rol(extension_base, gestor_social):
    """Test: Riesgo crítico bloquea aunque sea desarrollador."""
    intencion_critica = IntencionInferida(
        tipo=TipoIntencion.MODIFICAR,
        confianza=0.9,
        descripcion="Modificar valores core del sistema",
        requiere_ejecucion=True,
        riesgo_estimado=RiesgoSocial.CRITICO
    )
    perfil_dev = gestor_social.gestor_confianza.crear_perfil(
        RolUsuario.DESARROLLADOR, "Sebastian"
    )
    ctx_critico = ContextoSocial(perfil=perfil_dev, intencion=intencion_critica)
    resultado = extension_base.evaluar_contexto_social(ctx_critico)
    assert resultado.puede_proceder is False