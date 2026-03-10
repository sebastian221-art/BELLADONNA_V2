# -*- coding: utf-8 -*-
"""
consejeras/nova/logica.py — VERSION v2.0

CAMBIOS v2.0 sobre v1.0:
════════════════════════════════════════════════════════════════════
Nova deja de ser genérica y se convierte en la consejera propietaria
de HabilidadAnalisisPython.

MEJORAS:
  ✅ Detecta análisis de código en la decisión y el contexto
  ✅ Interpreta ResultadoAnalisis con perspectiva arquitectónica
  ✅ Genera recomendaciones técnicas reales (no genéricas)
  ✅ Clasifica la gravedad de problemas detectados
  ✅ Sugiere refactorizaciones concretas basadas en métricas
  ✅ Enriquece el contexto con 'nova_analisis' para el generador

ESPECIALIDADES DE NOVA:
  - Análisis de código Python (propietaria de ANALISIS_PYTHON)
  - Revisión arquitectónica de módulos Bell
  - Detección de deuda técnica (complejidad alta, funciones largas)
  - Optimización y refactorización
  - Evaluación de patrones de diseño

REGLAS:
  - Nova NUNCA veta (puede_vetar = False)
  - Nova solo sugiere — la decisión final es de Bell
  - Si el análisis tiene score >= 80: Nova celebra y sugiere mantenimiento
  - Si el análisis tiene score < 50: Nova eleva urgencia de refactorización
  - Nova siempre agrega valor técnico aunque no sea análisis de código

COMPATIBILIDAD: base_consejera, tipos_decision v7+,
                analizador_habilidad v1.0+
"""
from typing import Dict, List, Optional, Any
from consejeras.base_consejera import Consejera
from razonamiento.tipos_decision import Decision, TipoDecision


class Nova(Consejera):
    """
    Nova — La Ingeniera y Analista de Código.

    Consejera propietaria de HabilidadAnalisisPython.
    Especialista en arquitectura, optimización y análisis técnico.

    Nova NO veta — solo enriquece con perspectiva técnica.
    Cuando Bell analiza código, Nova es quien interpreta los
    resultados con visión arquitectónica real.
    """

    def __init__(self):
        super().__init__("Nova", "Ingeniera, Analista de Código y Optimizadora")
        self.puede_vetar = False

        # Palabras que activan el modo técnico general
        self._palabras_tecnicas = {
            'código', 'función', 'clase', 'variable', 'algoritmo',
            'optimizar', 'refactorizar', 'arquitectura', 'diseño', 'patrón',
            'módulo', 'importar', 'dependencia', 'rendimiento', 'eficiencia',
            'complejidad', 'acoplamiento', 'cohesión', 'abstracción',
        }
        self._palabras_problemas = {
            'error', 'bug', 'fallo', 'problema', 'lento',
            'ineficiente', 'roto', 'falla', 'excepción', 'traceback',
        }

        # Umbrales de calidad
        self._umbral_excelente  = 85
        self._umbral_bueno      = 70
        self._umbral_mejorable  = 50

        # Complejidad McCabe
        self._comp_alta      = 10
        self._comp_muy_alta  = 15
        self._lineas_max_fn  = 50

    # ------------------------------------------------------------------
    # MÉTODO PRINCIPAL
    # ------------------------------------------------------------------

    def revisar(self, decision: Decision, contexto: Dict) -> Dict:
        """
        Nova revisa la decisión desde perspectiva técnica.

        Casos especiales:
          1. EJECUCION con habilidad_id="ANALISIS_PYTHON" → Nova interpreta resultado
          2. Cualquier decisión técnica → Nova sugiere mejoras
          3. No técnico → opinión neutral
        """
        self.revisiones_realizadas += 1
        self.opiniones_dadas += 1

        traduccion     = contexto.get('traduccion', {})
        texto_original = traduccion.get('texto_original', '').lower()
        hechos         = decision.hechos_reales or {}

        # ── Caso 1: Resultado de análisis ya disponible en contexto ────
        resultado_analisis = contexto.get('resultado_analisis')
        if resultado_analisis is not None:
            return self._interpretar_resultado_analisis(resultado_analisis, texto_original)

        # ── Caso 2: Decisión EJECUCION de análisis Python ──────────────
        if (decision.tipo == TipoDecision.EJECUCION
                and hechos.get('habilidad_id') == 'ANALISIS_PYTHON'):
            return self._preparar_supervision_analisis(hechos, texto_original)

        # ── Caso 3: Consulta técnica general ───────────────────────────
        es_tecnico  = any(p in texto_original for p in self._palabras_tecnicas)
        es_problema = any(p in texto_original for p in self._palabras_problemas)

        if es_tecnico or es_problema:
            return self._generar_opinion_tecnica(texto_original, es_problema)

        # ── Caso 4: No es de mi especialidad ───────────────────────────
        return self._generar_opinion_neutral()

    # ------------------------------------------------------------------
    # INTERPRETACIÓN DE RESULTADOS DE ANÁLISIS
    # ------------------------------------------------------------------

    def _interpretar_resultado_analisis(
        self, resultado: Any, contexto_texto: str
    ) -> Dict:
        """
        Interpreta un ResultadoAnalisis con perspectiva arquitectónica.
        Este método se llama cuando el generador ya tiene el resultado
        de HabilidadAnalisisPython y lo pasa al contexto.
        """
        try:
            score    = getattr(resultado, 'score_calidad', 0)
            metricas = getattr(resultado, 'metricas', None)
            problemas = getattr(resultado, 'problemas', [])
            archivo  = getattr(resultado, 'archivo', 'desconocido')

            opinion, razonamiento, sugerencias = self._analizar_metricas(
                score, metricas, problemas, archivo
            )

            confianza = 0.95  # Nova es experta en esto

            return {
                'consejera':     self.nombre,
                'aprobada':      True,
                'veto':          False,
                'opinion':       opinion,
                'confianza':     confianza,
                'razonamiento':  razonamiento,
                'sugerencias':   sugerencias,
                'es_analisis':   True,
                'score_calidad': score,
                'nova_analisis': {
                    'score':          score,
                    'valoracion':     self._valoracion_score(score),
                    'prioridad':      self._prioridad_accion(score, problemas),
                    'sugerencias':    sugerencias,
                },
            }
        except Exception as e:
            return self._generar_opinion_tecnica(f"análisis de {contexto_texto}", False)

    def _analizar_metricas(
        self,
        score: int,
        metricas: Any,
        problemas: list,
        archivo: str,
    ):
        """Genera opinion, razonamiento y sugerencias desde métricas reales."""
        valoracion = self._valoracion_score(score)
        opinion    = f"Análisis de '{archivo}': calidad {valoracion} ({score}/100)."

        razonamiento = [f"1. Score de calidad: {score}/100 — {valoracion}"]

        if metricas:
            loc   = getattr(metricas, 'lineas_total', 0)
            fn    = getattr(metricas, 'num_funciones', 0)
            cls   = getattr(metricas, 'num_clases', 0)
            comp  = getattr(metricas, 'complejidad_prom', 0.0)
            cmax  = getattr(metricas, 'complejidad_max', 0)
            fn_mc = getattr(metricas, 'funcion_max_comp', '')
            ratio = getattr(metricas, 'ratio_comentarios', 0.0)
            hints = getattr(metricas, 'tiene_type_hints', False)

            razonamiento.append(
                f"2. Estructura: {loc} LOC, {fn} funciones, {cls} clases"
            )
            razonamiento.append(
                f"3. Complejidad promedio: {comp:.1f} "
                f"(máx {cmax} en '{fn_mc}')"
            )

            # Evaluar documentación
            if ratio < 0.05:
                razonamiento.append("4. Documentación: muy escasa — riesgo de mantenimiento")
            elif ratio < 0.15:
                razonamiento.append("4. Documentación: aceptable — mejorable")
            else:
                razonamiento.append("4. Documentación: buena cobertura")

            # Evaluar type hints
            if hints:
                razonamiento.append("5. Type hints presentes — buena práctica")
            else:
                razonamiento.append("5. Sin type hints — considerar agregar")

        # Clasificar problemas por tipo
        errores      = [p for p in problemas if getattr(p, 'tipo', '') == 'error']
        advertencias = [p for p in problemas if getattr(p, 'tipo', '') == 'advertencia']
        sugerencias_p = [p for p in problemas if getattr(p, 'tipo', '') == 'sugerencia']

        if errores:
            razonamiento.append(
                f"6. {len(errores)} error(es) críticos — requieren atención inmediata"
            )
        if advertencias:
            razonamiento.append(
                f"{'7' if errores else '6'}. {len(advertencias)} advertencia(s) — "
                f"refactorización recomendada"
            )

        # Generar sugerencias arquitectónicas
        sugerencias = self._generar_sugerencias_arquitectonicas(
            score, metricas, problemas
        )

        return opinion, razonamiento, sugerencias

    def _generar_sugerencias_arquitectonicas(
        self,
        score: int,
        metricas: Any,
        problemas: list,
    ) -> List[str]:
        """Sugerencias arquitectónicas concretas basadas en métricas reales."""
        sugerencias = []

        if score >= self._umbral_excelente:
            sugerencias.append(
                "✅ Código en excelente estado. Mantener estándares de documentación y testing."
            )
            return sugerencias

        if metricas:
            comp_max = getattr(metricas, 'complejidad_max', 0)
            fn_max   = getattr(metricas, 'funcion_max_comp', '')
            fn_total = getattr(metricas, 'num_funciones', 0)

            if comp_max > self._comp_muy_alta:
                sugerencias.append(
                    f"Prioridad ALTA: '{fn_max}' tiene complejidad {comp_max} — "
                    f"dividir en funciones más pequeñas con responsabilidad única."
                )
            elif comp_max > self._comp_alta:
                sugerencias.append(
                    f"'{fn_max}' con complejidad {comp_max} — "
                    f"considerar extraer lógica condicional a funciones auxiliares."
                )

            ratio = getattr(metricas, 'ratio_comentarios', 0.0)
            if ratio < 0.10 and fn_total > 5:
                sugerencias.append(
                    "Agregar docstrings a funciones públicas — "
                    "mejora mantenibilidad y onboarding."
                )

            if not getattr(metricas, 'tiene_type_hints', False) and fn_total > 3:
                sugerencias.append(
                    "Agregar type hints a funciones clave — "
                    "mejora legibilidad y detección de errores con mypy."
                )

        # Problemas específicos de alta prioridad
        fns_largas = [
            p for p in problemas
            if hasattr(p, 'descripcion') and 'muy larga' in p.descripcion
        ]
        if fns_largas:
            nombres = [getattr(p, 'nombre', '?') for p in fns_largas[:3]]
            sugerencias.append(
                f"Funciones largas detectadas: {', '.join(nombres)} — "
                f"aplicar principio de responsabilidad única (SRP)."
            )

        fns_camel = [
            p for p in problemas
            if hasattr(p, 'descripcion') and 'camelCase' in p.descripcion
        ]
        if fns_camel:
            sugerencias.append(
                f"{len(fns_camel)} función(es) con nombres camelCase — "
                f"renombrar a snake_case (PEP8) para consistencia."
            )

        if score < self._umbral_mejorable:
            sugerencias.append(
                "Considerar una sesión de refactorización dedicada — "
                "el score indica deuda técnica acumulada."
            )

        if not sugerencias:
            sugerencias.append(
                "Código en estado aceptable. "
                "Continuar agregando tests unitarios para mayor confianza."
            )

        return sugerencias

    def _preparar_supervision_analisis(
        self, hechos: dict, texto: str
    ) -> Dict:
        """
        Prepara la supervisión antes de que se ejecute el análisis.
        Nova establece expectativas y criterios de evaluación.
        """
        operacion = hechos.get('operacion', '')
        modulo    = hechos.get('modulo', '')
        archivo   = hechos.get('archivo', '')

        if operacion == 'analizar_bell':
            opinion = "Iniciando análisis completo de Bell. Evaluaré arquitectura y deuda técnica global."
        elif operacion == 'analizar_modulo':
            opinion = f"Analizando módulo '{modulo}' — foco en complejidad y cohesión."
        elif operacion == 'analizar_archivo':
            opinion = f"Analizando '{archivo}' — evaluaré calidad y posibles mejoras."
        elif operacion == 'analizar_inline':
            opinion = "Analizando código inline — evaluaré calidad y sugeriré mejoras."
        elif operacion == 'metricas_generales':
            opinion = "Generando métricas globales de Bell — visión del sistema completo."
        else:
            opinion = "Preparando análisis de código con perspectiva arquitectónica."

        return {
            'consejera':    self.nombre,
            'aprobada':     True,
            'veto':         False,
            'opinion':      opinion,
            'confianza':    0.95,
            'razonamiento': [
                "1. Operación de análisis — solo lectura, sin riesgo",
                "2. Nova supervisará métricas: LOC, complejidad, calidad",
                "3. Vega aprueba: análisis no modifica código",
            ],
            'sugerencias': [
                "Evaluar complejidad ciclomática McCabe",
                "Verificar ratio de documentación",
                "Identificar funciones candidatas a refactorización",
            ],
            'es_supervision_analisis': True,
        }

    # ------------------------------------------------------------------
    # OPINIONES TÉCNICAS GENERALES
    # ------------------------------------------------------------------

    def _generar_opinion_tecnica(self, texto: str, es_problema: bool) -> Dict:
        if es_problema:
            opinion = "Consulta técnica sobre un problema — sugiero enfoque sistemático de diagnóstico."
            sugerencias = [
                "Identificar el componente afectado (motor, generador, habilidad)",
                "Revisar logs y trazas de error",
                "Aislar el problema con un caso mínimo reproducible",
                "Aplicar fix puntual antes de refactorizar",
            ]
            razonamiento = [
                "1. Problema técnico detectado",
                "2. Enfoque: diagnóstico antes que solución",
                "3. Recomendación: fix quirúrgico, evitar cambios en cascada",
            ]
        else:
            opinion = "Consulta técnica — enfoque en solución clara, escalable y documentada."
            sugerencias = [
                "Explicar con ejemplos concretos del contexto Bell",
                "Sugerir el patrón de diseño más apropiado",
                "Considerar impacto en otros módulos",
            ]
            razonamiento = [
                "1. Consulta técnica general",
                "2. Prioridad: claridad y mantenibilidad",
                "3. Considerar consistencia con arquitectura Bell existente",
            ]

        return {
            'consejera':    self.nombre,
            'aprobada':     True,
            'veto':         False,
            'opinion':      opinion,
            'confianza':    0.80,
            'razonamiento': razonamiento,
            'sugerencias':  sugerencias,
        }

    def _generar_opinion_neutral(self) -> Dict:
        return {
            'consejera':    self.nombre,
            'aprobada':     True,
            'veto':         False,
            'opinion':      'Fuera de mi especialidad técnica — sin comentarios adicionales.',
            'confianza':    0.50,
            'razonamiento': ["No es consulta técnica ni análisis de código"],
            'sugerencias':  [],
        }

    # ------------------------------------------------------------------
    # HELPERS INTERNOS
    # ------------------------------------------------------------------

    def _valoracion_score(self, score: int) -> str:
        if score >= self._umbral_excelente:  return "excelente"
        if score >= self._umbral_bueno:       return "buena"
        if score >= self._umbral_mejorable:   return "mejorable"
        return "necesita trabajo urgente"

    def _prioridad_accion(self, score: int, problemas: list) -> str:
        errores = sum(1 for p in problemas if getattr(p, 'tipo', '') == 'error')
        if errores > 0 or score < self._umbral_mejorable:
            return "ALTA"
        if score < self._umbral_bueno:
            return "MEDIA"
        return "BAJA"

    # ------------------------------------------------------------------
    # API PÚBLICA — para el generador
    # ------------------------------------------------------------------

    def enriquecer_contexto_analisis(
        self, contexto: Dict, resultado_analisis: Any
    ) -> Dict:
        """
        Permite al generador pedirle a Nova que enriquezca el contexto
        con su interpretación antes de generar la respuesta final.
        """
        opinion = self._interpretar_resultado_analisis(
            resultado_analisis,
            contexto.get('traduccion', {}).get('texto_original', ''),
        )
        contexto['nova_revision'] = opinion
        contexto['nova_analisis'] = opinion.get('nova_analisis', {})
        return contexto