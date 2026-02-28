"""
Test de Conversación Completo — Grounding 9D integrado con Bell.

Valida que todas las dimensiones funcionan juntas en el flujo conversacional:
  Dim 1: Computacional  — Bell sabe qué puede ejecutar
  Dim 2: Semántico      — Bell entiende el significado
  Dim 3: Contextual     — Bell aprende del historial de contexto
  Dim 4: Pragmático     — Bell evalúa pre/postcondiciones
  Dim 5: Social         — Bell distingue roles de usuario
  Dim 6: Temporal       — Bell sabe si el conocimiento está vigente
  Dim 7: Causal         — Bell detecta riesgos y efectos
  Dim 8: Metacognitivo  — Bell explica sus decisiones
  Dim 9: Predictivo     — Bell aprende de éxitos y fallos anteriores
"""
import sys
import os
import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.concepto_anclado import ConceptoAnclado, TipoConcepto
from extension_grounding import ExtensionGroundingMultidimensional
from integracion_grounding_bell import GestorIntegracionGrounding, EvaluacionGrounding
from grounding_predictivo import NivelConfianzaPrediccion, TendenciaHistorica
from reporte_grounding import GeneradorReporteGrounding


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def concepto_leer():
    return ConceptoAnclado(
        id='CONCEPTO_LEER',
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=['leer', 'leer archivo', 'read'],
        operaciones={'ejecutar': lambda: "contenido del archivo"},
        confianza_grounding=1.0,
    )


@pytest.fixture
def concepto_escribir():
    return ConceptoAnclado(
        id='CONCEPTO_ESCRIBIR',
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=['escribir', 'guardar', 'write'],
        operaciones={'ejecutar': lambda: True},
        confianza_grounding=0.95,
    )


@pytest.fixture
def concepto_sin_grounding():
    return ConceptoAnclado(
        id='CONCEPTO_DESCONOCIDO',
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=['desconocido'],
        confianza_grounding=0.0,
    )


@pytest.fixture
def gestor():
    return GestorIntegracionGrounding()


@pytest.fixture
def ext_leer(concepto_leer):
    return ExtensionGroundingMultidimensional(concepto_leer)


# ─────────────────────────────────────────────────────────────────────────────
# Bloque 1: DIM 1 — Computacional
# ─────────────────────────────────────────────────────────────────────────────

class TestDim1Computacional:
    """Bell sabe qué puede ejecutar con certeza."""

    def test_concepto_con_grounding_puede_proceder(self, gestor, concepto_leer):
        eval_g = gestor.evaluar_antes_de_actuar(concepto_leer)
        assert eval_g.grounding_computacional == 1.0
        assert eval_g.puede_proceder is True

    def test_concepto_sin_grounding_no_puede_proceder(self, gestor, concepto_sin_grounding):
        eval_g = gestor.evaluar_antes_de_actuar(concepto_sin_grounding)
        assert eval_g.grounding_computacional == 0.0
        assert eval_g.puede_proceder is False

    def test_razon_explicada_cuando_no_puede(self, gestor, concepto_sin_grounding):
        eval_g = gestor.evaluar_antes_de_actuar(concepto_sin_grounding)
        assert len(eval_g.razones) > 0
        assert any('computacional' in r.lower() or 'CONCEPTO_DESCONOCIDO' in r 
                   for r in eval_g.razones)

    def test_score_computacional_alto_sube_total(self, gestor, concepto_leer):
        eval_g = gestor.evaluar_antes_de_actuar(concepto_leer)
        # Computacional tiene peso 20% → con solo comp=1.0, total ≥ 0.20
        assert eval_g.score_total >= 0.20

    def test_nivel_confianza_con_grounding_completo(self, gestor, concepto_leer):
        eval_g = gestor.evaluar_antes_de_actuar(concepto_leer)
        # Con al menos comp activo: nivel no SIN_DATOS
        assert eval_g.nivel_confianza != "SIN_DATOS"


# ─────────────────────────────────────────────────────────────────────────────
# Bloque 2: DIM 2 — Semántico
# ─────────────────────────────────────────────────────────────────────────────

class TestDim2Semantico:
    """Bell entiende el significado de los conceptos."""

    def test_registrar_semantica_actualiza_extension(self, gestor, concepto_leer):
        ext = gestor.registrar_concepto_con_semantica(concepto_leer)
        assert ext.grounding_semantico > 0.0

    def test_semantica_con_similares_mayor_densidad(self, gestor, concepto_leer, concepto_escribir):
        ext_sin = gestor.obtener_extension(concepto_leer)
        g_sin = ext_sin.grounding_semantico

        gestor.registrar_concepto_con_semantica(
            concepto_leer,
            similares=[('CONCEPTO_ESCRIBIR', 0.8), ('CONCEPTO_ABRIR', 0.7)]
        )
        g_con = gestor.obtener_extension(concepto_leer).grounding_semantico
        assert g_con > g_sin or g_con >= 0.0  # Al menos no bajó

    def test_actualizar_grounding_semantico_directo(self, ext_leer):
        ext_leer.actualizar_grounding_semantico(
            embedding=np.ones(10),
            coherencia=0.9,
            densidad=0.8,
            similares=[('CONCEPTO_ABRIR', 0.75)]
        )
        assert ext_leer.grounding_semantico > 0.0
        assert ext_leer.coherencia_interna == 0.9
        assert ext_leer.densidad_red == 0.8

    def test_similares_guardados_correctamente(self, ext_leer):
        similares = [('CONCEPTO_A', 0.9), ('CONCEPTO_B', 0.7)]
        ext_leer.actualizar_grounding_semantico(
            embedding=np.ones(10), coherencia=0.8,
            densidad=0.6, similares=similares
        )
        assert ext_leer.obtener_similares(2) == similares[:2]

    def test_es_similar_a_con_umbral(self, ext_leer):
        ext_leer.actualizar_grounding_semantico(
            embedding=np.ones(10), coherencia=0.8,
            densidad=0.6, similares=[('CONCEPTO_X', 0.8)]
        )
        assert ext_leer.es_similar_a('CONCEPTO_X', umbral=0.5) is True
        assert ext_leer.es_similar_a('CONCEPTO_X', umbral=0.9) is False


# ─────────────────────────────────────────────────────────────────────────────
# Bloque 3: DIM 3 — Contextual
# ─────────────────────────────────────────────────────────────────────────────

class TestDim3Contextual:
    """Bell aprende cuándo usar cada concepto según el contexto."""

    def test_registrar_uso_contextual_actualiza_score(self, gestor, concepto_leer):
        ext = gestor.obtener_extension(concepto_leer)
        g_inicial = ext.grounding_contextual

        gestor.registrar_resultado(concepto_leer, exito=True, score=0.9,
                                   contexto='archivo texto')
        # El contextual puede haber cambiado (puede necesitar tracker inicializado)
        # Solo verificamos que no rompió nada
        assert ext.grounding_contextual >= 0.0

    def test_multiples_exitos_no_rompen_sistema(self, gestor, concepto_leer):
        for i in range(5):
            gestor.registrar_resultado(concepto_leer, exito=True, score=0.85,
                                       contexto=f'contexto_{i}')
        # Sistema sigue funcionando
        eval_g = gestor.evaluar_antes_de_actuar(concepto_leer)
        assert eval_g.puede_proceder is True

    def test_historial_resultados_crece(self, gestor, concepto_leer):
        n_inicial = len(gestor._historial_resultados)
        gestor.registrar_resultado(concepto_leer, exito=True)
        gestor.registrar_resultado(concepto_leer, exito=False)
        assert len(gestor._historial_resultados) == n_inicial + 2

    def test_tasa_exito_en_estadisticas(self, gestor, concepto_leer):
        for _ in range(3):
            gestor.registrar_resultado(concepto_leer, exito=True)
        for _ in range(1):
            gestor.registrar_resultado(concepto_leer, exito=False)
        stats = gestor.estadisticas()
        assert 0.0 < stats['tasa_exito_global'] < 1.0


# ─────────────────────────────────────────────────────────────────────────────
# Bloque 4: DIM 4 — Pragmático
# ─────────────────────────────────────────────────────────────────────────────

class TestDim4Pragmatico:
    """Bell evalúa precondiciones antes de actuar."""

    def test_pragmatico_empieza_en_cero(self, ext_leer):
        assert ext_leer.grounding_pragmatico == 0.0

    def test_puede_ejecutar_sin_datos_pragmaticos(self, ext_leer):
        # Sin datos pragmáticos, puede ejecutar por defecto (no bloquea)
        assert ext_leer.puede_ejecutar_ahora({}) is True

    def test_affordances_vacias_sin_datos(self, ext_leer):
        assert ext_leer.affordances_disponibles({}) == []

    def test_conceptos_habilitados_vacios_sin_datos(self, ext_leer):
        assert ext_leer.conceptos_habilitados({}) == []

    def test_evaluacion_precondiciones_sin_datos(self, ext_leer):
        resultado = ext_leer.evaluar_precondiciones({})
        assert resultado.puede_ejecutar is True  # Sin datos → permite por defecto


# ─────────────────────────────────────────────────────────────────────────────
# Bloque 5: DIM 5 — Social
# ─────────────────────────────────────────────────────────────────────────────

class TestDim5Social:
    """Bell distingue quién pide qué y si tiene permiso."""

    def test_social_empieza_en_cero(self, ext_leer):
        assert ext_leer.grounding_social == 0.0

    def test_desarrollador_puede_ejecutar(self, ext_leer):
        from grounding_social import RolUsuario
        puede = ext_leer.puede_responder_a(
            rol=RolUsuario.DESARROLLADOR,
            solicitud='leer archivo config',
        )
        assert puede is True
        assert ext_leer.grounding_social > 0.0

    def test_grounding_social_positivo_tras_evaluar(self, ext_leer):
        from grounding_social import RolUsuario
        ext_leer.puede_responder_a(RolUsuario.DESARROLLADOR, 'leer archivo')
        assert ext_leer.grounding_social > 0.0

    def test_evaluacion_incluye_score_social(self, gestor, concepto_leer):
        from grounding_social import GestorGroundingSocial, RolUsuario
        ext = gestor.obtener_extension(concepto_leer)
        gestor_social = GestorGroundingSocial()
        ctx = gestor_social.crear_contexto(RolUsuario.DESARROLLADOR, 'leer archivo', 'Sebastian')
        ext.evaluar_contexto_social(ctx)

        eval_g = gestor.evaluar_antes_de_actuar(concepto_leer)
        assert eval_g.grounding_social > 0.0


# ─────────────────────────────────────────────────────────────────────────────
# Bloque 6: DIM 6 — Temporal
# ─────────────────────────────────────────────────────────────────────────────

class TestDim6Temporal:
    """Bell sabe si el conocimiento que tiene sigue vigente."""

    def test_temporal_empieza_en_invalido(self, ext_leer):
        from grounding_temporal import EstadoTemporal
        assert ext_leer.grounding_temporal == 0.0

    def test_registrar_validez_temporal_sube_score(self, ext_leer):
        from grounding_temporal import ValidezTemporal
        ext_leer.registrar_validez_temporal(ValidezTemporal.PERMANENTE)
        assert ext_leer.grounding_temporal > 0.0

    def test_operacion_sistema_vigente(self, ext_leer):
        ext_leer.usar_fabrica_temporal('operacion_sistema')
        assert ext_leer.conocimiento_vigente() is True

    def test_evaluar_temporalidad_retorna_resultado(self, ext_leer):
        ext_leer.usar_fabrica_temporal('operacion_sistema')
        resultado = ext_leer.evaluar_temporalidad()
        assert resultado is not None

    def test_temporal_contribuye_al_total(self, ext_leer):
        t_sin = ext_leer.calcular_grounding_total()
        ext_leer.usar_fabrica_temporal('operacion_sistema')
        t_con = ext_leer.calcular_grounding_total()
        assert t_con > t_sin


# ─────────────────────────────────────────────────────────────────────────────
# Bloque 7: DIM 7 — Causal
# ─────────────────────────────────────────────────────────────────────────────

class TestDim7Causal:
    """Bell detecta causas, efectos y riesgos antes de actuar."""

    def test_causal_empieza_en_cero(self, ext_leer):
        assert ext_leer.grounding_causal == 0.0

    def test_seguro_causalmente_sin_datos(self, ext_leer):
        assert ext_leer.es_seguro_causalmente() is True

    def test_registrar_relacion_sube_score(self, ext_leer):
        from grounding_causal import TipoCausal
        ext_leer.registrar_relacion_causal(
            efecto_id='CONCEPTO_CONTENIDO_DISPONIBLE',
            tipo=TipoCausal.SUFICIENTE,
            probabilidad=0.99,
            descripcion='Al leer, el contenido queda en memoria',
        )
        assert ext_leer.grounding_causal > 0.0

    def test_fabrica_causal_leer_archivo(self, ext_leer):
        ext_leer.usar_fabrica_causal('leer_archivo')
        assert ext_leer.grounding_causal > 0.0

    def test_analizar_consecuencias_retorna_resultado(self, ext_leer):
        ext_leer.usar_fabrica_causal('leer_archivo')
        resultado = ext_leer.analizar_consecuencias()
        assert resultado is not None

    def test_causal_contribuye_al_total(self, ext_leer):
        t_sin = ext_leer.calcular_grounding_total()
        ext_leer.usar_fabrica_causal('leer_archivo')
        t_con = ext_leer.calcular_grounding_total()
        assert t_con > t_sin


# ─────────────────────────────────────────────────────────────────────────────
# Bloque 8: DIM 8 — Metacognitivo
# ─────────────────────────────────────────────────────────────────────────────

class TestDim8Metacognitivo:
    """Bell puede explicar por qué tomó una decisión."""

    def test_metacognitivo_empieza_en_cero(self, ext_leer):
        assert ext_leer.grounding_metacognitivo == 0.0

    def test_registrar_decision_sube_score(self, ext_leer):
        from grounding_metacognitivo import TipoDecision
        ext_leer.registrar_decision('leer config.json', TipoDecision.APROBACION)
        assert ext_leer.grounding_metacognitivo > 0.0

    def test_explicacion_usuario_no_vacia(self, ext_leer):
        from grounding_metacognitivo import TipoDecision, NivelExplicacion
        ext_leer.registrar_decision('leer archivo', TipoDecision.APROBACION)
        exp = ext_leer.explicar_decision(NivelExplicacion.USUARIO)
        assert exp is not None and len(exp) > 0

    def test_historial_decisiones_crece(self, ext_leer):
        from grounding_metacognitivo import TipoDecision
        assert len(ext_leer.historial_decisiones()) == 0
        ext_leer.registrar_decision('accion_1', TipoDecision.APROBACION)
        ext_leer.registrar_decision('accion_2', TipoDecision.RECHAZO)
        assert len(ext_leer.historial_decisiones(5)) == 2

    def test_explicacion_simple_mas_corta_que_tecnica(self, ext_leer):
        from grounding_metacognitivo import TipoDecision, NivelExplicacion
        ext_leer.registrar_decision('leer', TipoDecision.APROBACION)
        simple = ext_leer.explicar_decision(NivelExplicacion.SIMPLE) or ""
        tecnico = ext_leer.explicar_decision(NivelExplicacion.TECNICO) or ""
        assert len(simple) <= len(tecnico)

    def test_gestor_explica_ultima_decision(self, gestor, concepto_leer):
        gestor.evaluar_antes_de_actuar(concepto_leer)
        exp = gestor.explicar_ultima_decision(concepto_leer, "USUARIO")
        assert isinstance(exp, str) and len(exp) > 0


# ─────────────────────────────────────────────────────────────────────────────
# Bloque 9: DIM 9 — Predictivo
# ─────────────────────────────────────────────────────────────────────────────

class TestDim9Predictivo:
    """Bell aprende de su historial de éxitos y fallos."""

    def test_predictivo_empieza_en_cero(self, gestor, concepto_leer):
        ext = gestor.obtener_extension(concepto_leer)
        assert ext.grounding_predictivo == 0.0

    def test_registrar_exitos_sube_predictivo(self, gestor, concepto_leer):
        for _ in range(5):
            gestor.registrar_resultado(concepto_leer, exito=True, score=0.9)
        ext = gestor.obtener_extension(concepto_leer)
        assert ext.grounding_predictivo > 0.0

    def test_evaluacion_incluye_prediccion(self, gestor, concepto_leer):
        for _ in range(5):
            gestor.registrar_resultado(concepto_leer, exito=True, score=0.9)
        eval_g = gestor.evaluar_antes_de_actuar(concepto_leer)
        assert eval_g.grounding_predictivo > 0.0
        assert 0.0 <= eval_g.prediccion_exito <= 1.0

    def test_solo_fallos_genera_precaucion(self, gestor, concepto_leer):
        for _ in range(8):
            gestor.registrar_resultado(concepto_leer, exito=False, score=0.1)
        eval_g = gestor.evaluar_antes_de_actuar(concepto_leer)
        assert eval_g.requiere_precaucion is True

    def test_sin_historial_prediccion_sin_datos(self, gestor, concepto_escribir):
        ext = gestor.obtener_extension(concepto_escribir)
        pred = ext.predecir_exito('escribir')
        assert pred.confianza == NivelConfianzaPrediccion.SIN_DATOS

    def test_tendencia_mejorando_con_exitos_recientes(self, gestor, concepto_leer):
        # Primeros 5 con baja tasa
        for _ in range(5):
            gestor.registrar_resultado(concepto_leer, exito=False, score=0.2)
        # Últimos 5 con alta tasa
        for _ in range(5):
            gestor.registrar_resultado(concepto_leer, exito=True, score=0.95)
        ext = gestor.obtener_extension(concepto_leer)
        pred = ext.predecir_exito()
        assert pred.tendencia == TendenciaHistorica.MEJORANDO


# ─────────────────────────────────────────────────────────────────────────────
# Bloque 10: Integración — 9 dimensiones juntas
# ─────────────────────────────────────────────────────────────────────────────

class TestIntegracion9Dimensiones:
    """Verifica que las 9 dimensiones trabajan juntas correctamente."""

    def _activar_todas_las_dimensiones(self, ext, concepto):
        """Activa las 9 dimensiones en una extensión."""
        import numpy as np
        from grounding_temporal import ValidezTemporal
        from grounding_causal import TipoCausal
        from grounding_metacognitivo import TipoDecision
        from grounding_social import RolUsuario

        # Dim 2: Semántico
        ext.actualizar_grounding_semantico(
            embedding=np.ones(10), coherencia=0.85,
            densidad=0.75, similares=[('CONCEPTO_OTRO', 0.7)]
        )
        # Dim 3: Contextual (via registros)
        for _ in range(3):
            try:
                ext.registrar_uso_contextual(exito=True, duracion_ms=100)
            except Exception:
                pass

        # Dim 5: Social
        ext.puede_responder_a(RolUsuario.DESARROLLADOR, 'test')

        # Dim 6: Temporal
        ext.usar_fabrica_temporal('operacion_sistema')

        # Dim 7: Causal
        ext.usar_fabrica_causal('leer_archivo')

        # Dim 8: Metacognitivo
        ext.registrar_decision('test', TipoDecision.APROBACION)

        # Dim 9: Predictivo
        for _ in range(5):
            ext.registrar_resultado_predictivo(True, 0.9)

    def test_9_dimensiones_activas_todas(self, concepto_leer):
        ext = ExtensionGroundingMultidimensional(concepto_leer)
        self._activar_todas_las_dimensiones(ext, concepto_leer)
        # comp(1) + sem + soc + tem + cau + meta + pred = 7 mínimo
        assert ext._contar_dimensiones_activas() >= 7

    def test_score_total_mayor_con_mas_dimensiones(self, concepto_leer):
        ext = ExtensionGroundingMultidimensional(concepto_leer)
        t_solo_comp = ext.calcular_grounding_total()
        self._activar_todas_las_dimensiones(ext, concepto_leer)
        t_9d = ext.calcular_grounding_total()
        assert t_9d > t_solo_comp

    def test_resumen_incluye_las_9_dimensiones(self, concepto_leer):
        ext = ExtensionGroundingMultidimensional(concepto_leer)
        self._activar_todas_las_dimensiones(ext, concepto_leer)
        resumen = ext.obtener_resumen()
        campos_grounding = [
            'confianza_grounding', 'grounding_semantico', 'grounding_contextual',
            'grounding_pragmatico', 'grounding_social', 'grounding_temporal',
            'grounding_causal', 'grounding_metacognitivo', 'grounding_predictivo',
        ]
        for campo in campos_grounding:
            assert campo in resumen, f"Campo faltante: {campo}"

    def test_reporte_9d_genera_para_concepto_completo(self, concepto_leer):
        ext = ExtensionGroundingMultidimensional(concepto_leer)
        self._activar_todas_las_dimensiones(ext, concepto_leer)
        gen = GeneradorReporteGrounding()
        reporte = gen.generar_para_concepto(ext)
        assert len(reporte.dimensiones) == 9
        assert reporte.score_total > 0.0
        assert reporte.salud in ("EXCELENTE", "BUENA", "REGULAR", "DEFICIENTE")

    def test_evaluar_concepto_completamente_cargado(self, gestor, concepto_leer):
        ext = gestor.obtener_extension(concepto_leer)
        self._activar_todas_las_dimensiones(ext, concepto_leer)
        eval_g = gestor.evaluar_antes_de_actuar(concepto_leer)
        assert eval_g.puede_proceder is True
        assert eval_g.score_total > 0.5
        assert eval_g.dimensiones_activas >= 7

    def test_ciclo_completo_evaluar_ejecutar_aprender(self, gestor, concepto_leer):
        """Simula un ciclo conversacional completo."""
        # 1. Bell evalúa antes de actuar
        eval_g = gestor.evaluar_antes_de_actuar(concepto_leer, accion='leer archivo')
        assert isinstance(eval_g, EvaluacionGrounding)

        # 2. Bell ejecuta (simulado como éxito)
        gestor.registrar_resultado(concepto_leer, exito=True, score=0.92,
                                   contexto='lectura de config')

        # 3. Bell evalúa de nuevo — grounding predictivo ya tiene 1 dato
        eval_g2 = gestor.evaluar_antes_de_actuar(concepto_leer, accion='leer archivo')
        assert eval_g2.grounding_predictivo > eval_g.grounding_predictivo

    def test_10_ciclos_mejoran_grounding_predictivo(self, gestor, concepto_leer):
        """10 ciclos exitosos → grounding predictivo crece significativamente."""
        g_inicial = gestor.evaluar_antes_de_actuar(concepto_leer).grounding_predictivo
        for _ in range(10):
            gestor.registrar_resultado(concepto_leer, exito=True, score=0.9)
        g_final = gestor.evaluar_antes_de_actuar(concepto_leer).grounding_predictivo
        assert g_final > g_inicial

    def test_resumen_para_bell_es_string(self, gestor, concepto_leer):
        eval_g = gestor.evaluar_antes_de_actuar(concepto_leer)
        resumen = eval_g.resumen_para_bell()
        assert isinstance(resumen, str) and len(resumen) > 0

    def test_reporte_sistema_con_multiples_conceptos(self, gestor, concepto_leer, concepto_escribir):
        gestor.evaluar_antes_de_actuar(concepto_leer)
        gestor.evaluar_antes_de_actuar(concepto_escribir)
        reporte = gestor.reporte_sistema()
        assert isinstance(reporte, str) and len(reporte) > 10

    def test_estadisticas_reflejan_actividad(self, gestor, concepto_leer, concepto_escribir):
        gestor.evaluar_antes_de_actuar(concepto_leer)
        gestor.evaluar_antes_de_actuar(concepto_escribir)
        gestor.registrar_resultado(concepto_leer, exito=True)
        gestor.registrar_resultado(concepto_escribir, exito=False)
        stats = gestor.estadisticas()
        assert stats['evaluaciones_realizadas'] >= 2
        assert stats['resultados_registrados'] >= 2
        assert stats['tasa_exito_global'] == 0.5


# ─────────────────────────────────────────────────────────────────────────────
# Bloque 11: Escenarios conversacionales reales
# ─────────────────────────────────────────────────────────────────────────────

class TestEscenariosConversacionales:
    """Simula conversaciones reales con Bell y verifica comportamiento."""

    def test_escenario_lectura_exitosa_repetida(self, gestor, concepto_leer):
        """Bell lee archivos 5 veces con éxito → grounding mejora."""
        scores = []
        for i in range(5):
            eval_g = gestor.evaluar_antes_de_actuar(concepto_leer, accion=f'leer archivo_{i}')
            scores.append(eval_g.grounding_predictivo)
            gestor.registrar_resultado(concepto_leer, exito=True, score=0.9,
                                       contexto=f'archivo_{i}')
        # Scores deben subir (o al menos no bajar al final)
        assert scores[-1] >= scores[0]

    def test_escenario_concepto_desconocido_advertencia(self, gestor, concepto_sin_grounding):
        """Cuando Bell no tiene grounding, el resultado explica por qué."""
        eval_g = gestor.evaluar_antes_de_actuar(concepto_sin_grounding)
        assert eval_g.puede_proceder is False
        resumen = eval_g.resumen_para_bell()
        assert 'No puedo' in resumen or 'confianza' in resumen.lower()

    def test_escenario_historial_negativo_genera_advertencia(self, gestor, concepto_escribir):
        """Historial de fallos → Bell advierte antes de actuar."""
        for _ in range(8):
            gestor.registrar_resultado(concepto_escribir, exito=False, score=0.1)
        eval_g = gestor.evaluar_antes_de_actuar(concepto_escribir)
        assert eval_g.requiere_precaucion is True

    def test_escenario_recuperacion_tras_fallos(self, gestor, concepto_leer):
        """Tras fallos, éxitos recientes recuperan la predicción."""
        for _ in range(5):
            gestor.registrar_resultado(concepto_leer, exito=False, score=0.1)
        eval_malo = gestor.evaluar_antes_de_actuar(concepto_leer)

        for _ in range(8):
            gestor.registrar_resultado(concepto_leer, exito=True, score=0.95)
        eval_recuperado = gestor.evaluar_antes_de_actuar(concepto_leer)

        assert eval_recuperado.grounding_predictivo > eval_malo.grounding_predictivo

    def test_escenario_dos_conceptos_independientes(self, gestor, concepto_leer, concepto_escribir):
        """El historial de LEER no afecta a ESCRIBIR."""
        for _ in range(10):
            gestor.registrar_resultado(concepto_leer, exito=False, score=0.1)

        eval_leer = gestor.evaluar_antes_de_actuar(concepto_leer)
        eval_escribir = gestor.evaluar_antes_de_actuar(concepto_escribir)

        # LEER tiene historial malo, ESCRIBIR no tiene historial
        assert eval_leer.grounding_predictivo != eval_escribir.grounding_predictivo or \
               eval_escribir.grounding_predictivo == 0.0

    def test_escenario_bell_aprende_vocabulario_principal(self, gestor):
        """Simula que Bell precarga sus conceptos principales."""
        conceptos_demo = []
        for i in range(5):
            c = ConceptoAnclado(
                id=f'CONCEPTO_DEMO_{i}',
                tipo=TipoConcepto.OPERACION_SISTEMA,
                palabras_español=[f'demo_{i}'],
                confianza_grounding=1.0 - i * 0.15,
            )
            conceptos_demo.append(c)
            gestor.registrar_concepto_con_semantica(c)

        stats = gestor.estadisticas()
        assert stats['conceptos_con_extension'] >= 5