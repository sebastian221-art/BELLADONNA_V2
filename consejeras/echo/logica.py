"""
echo/logica.py — VERSIÓN v2

FIXES APLICADOS:
═══════════════════════════════════════════════════════════════════════

FIX-E1  BUG DE CAMPOS CORREGIDO
        verificar_respuesta_llm() leía resultado.problemas_detectados
        y resultado.patrones_sospechosos — campos que no existen en
        ResultadoVerificacion. Ahora lee los campos reales:
        violaciones, confianza, accion_recomendada.

FIX-E2  VERIFICADOR SIEMPRE ACTIVO
        _inicializar_verificador() se llama en __init__ con lazy load.
        Ya no depende de que Groq esté activo para existir.
        El generador_salida puede instanciar Echo e inmediatamente
        usar verificar_respuesta_llm() y verificar_decision().

FIX-E3  MÉTODO verificar_decision() NUEVO
        Verifica coherencia interna de una Decision ANTES de generar texto.
        Si tipo=AFIRMATIVA pero puede_ejecutar=False → incoherencia crítica.
        Si tipo=CAPACIDAD_BELL y disponible=False → coherente, permite continuar.

═══════════════════════════════════════════════════════════════════════
"""
from typing import Dict, List
from consejeras.base_consejera import Consejera
from razonamiento.tipos_decision import Decision, TipoDecision


class Echo(Consejera):
    """
    Echo - La Lógica.

    v2: verificador siempre activo, bugs de campos corregidos,
    método verificar_decision() para coherencia interna.
    """

    def __init__(self):
        super().__init__("Echo", "Lógica y Razonamiento")
        self.puede_vetar = False

        self.conectores_logicos = [
            'si', 'entonces', 'por lo tanto', 'porque',
            'implica', 'significa', 'consecuencia', 'causa'
        ]
        self.palabras_contradiccion = [
            'pero', 'sin embargo', 'aunque', 'a pesar',
            'contradice', 'opuesto', 'contrario'
        ]

        # FIX-E2: inicializar verificador en __init__, no solo en Groq
        self._verificador = None
        self._inicializar_verificador()

    def _inicializar_verificador(self):
        """Inicializa verificador de coherencia. Siempre, no solo en modo Groq."""
        if self._verificador is not None:
            return
        try:
            from consejeras.echo.verificador_coherencia import VerificadorCoherenciaEcho
            self._verificador = VerificadorCoherenciaEcho()
        except ImportError:
            pass

    def revisar(self, decision: Decision, contexto: Dict) -> Dict:
        """
        Revisa desde perspectiva lógica.
        Busca conectores lógicos y contradicciones en el texto del usuario.
        """
        self.revisiones_realizadas += 1
        self.opiniones_dadas += 1

        traduccion    = contexto.get('traduccion', {})
        texto_usuario = traduccion.get('texto_original', '').lower()

        tiene_logica       = any(c in texto_usuario for c in self.conectores_logicos)
        tiene_contradiccion = any(p in texto_usuario for p in self.palabras_contradiccion)

        if tiene_logica or tiene_contradiccion:
            return self._generar_opinion_logica(texto_usuario, tiene_contradiccion)
        return self._generar_opinion_neutral()

    # ──────────────────────────────────────────────────────────────────────
    # FIX-E3: verificar_decision — coherencia interna ANTES de generar texto
    # ──────────────────────────────────────────────────────────────────────

    def verificar_decision(self, decision: Decision) -> Dict:
        """
        Verifica coherencia interna de la Decision antes de que el generador
        produzca texto.

        Detecta inconsistencias como:
        - tipo=AFIRMATIVA pero puede_ejecutar=False
        - tipo=CAPACIDAD_BELL con disponible=False → coherente, no bloquea

        Returns:
            Dict con 'coherente', 'problemas', 'accion_recomendada'
        """
        problemas = []

        # Incoherencia crítica: tipo dice "sí puedo" pero evaluador dice "no"
        if decision.tipo == TipoDecision.AFIRMATIVA and not decision.puede_ejecutar:
            problemas.append(
                "tipo=AFIRMATIVA pero puede_ejecutar=False — "
                "motor clasificó como ejecutable pero evaluador lo bloqueó"
            )

        # CAPACIDAD_BELL con puede_ejecutar=False es coherente — es la respuesta honesta
        # No agregar problema aquí.

        # NEGATIVA con puede_ejecutar=True sería raro
        if decision.tipo == TipoDecision.NEGATIVA and decision.puede_ejecutar:
            problemas.append(
                "tipo=NEGATIVA pero puede_ejecutar=True — inconsistencia de tipo"
            )

        # Hechos dicen disponible=False pero tipo es AFIRMATIVA
        if decision.hechos_reales:
            disponible = decision.hechos_reales.get('capacidad_solicitada_disponible', True)
            if not disponible and decision.tipo == TipoDecision.AFIRMATIVA:
                problemas.append(
                    "hechos dicen capacidad_solicitada_disponible=False pero tipo=AFIRMATIVA"
                )

        coherente = len(problemas) == 0
        return {
            'coherente':           coherente,
            'problemas':           problemas,
            'accion_recomendada':  'PERMITIR' if coherente else 'BLOQUEAR',
        }

    # ──────────────────────────────────────────────────────────────────────
    # FIX-E1: verificar_respuesta_llm — campos correctos de ResultadoVerificacion
    # ──────────────────────────────────────────────────────────────────────

    def verificar_respuesta_llm(self, texto_llm: str, decision: Decision) -> Dict:
        """
        Verifica que una respuesta del LLM sea coherente con la decisión.

        v2: lee campos reales de ResultadoVerificacion:
            violaciones, confianza, accion_recomendada
        (antes leía problemas_detectados y patrones_sospechosos — no existen)
        """
        if self._verificador is None:
            self._inicializar_verificador()

        if self._verificador is None:
            return {
                'aprobada':            True,
                'confianza':           0.5,
                'problemas':           ['Verificador no disponible'],
                'accion_recomendada':  'PERMITIR',
            }

        resultado = self._verificador.verificar(texto_llm, decision)

        # FIX-E1: usar campos que SÍ existen en ResultadoVerificacion
        return {
            'aprobada':           resultado.accion_recomendada != "BLOQUEAR",
            'confianza':          resultado.confianza,
            'problemas':          resultado.violaciones,           # era problemas_detectados
            'accion_recomendada': resultado.accion_recomendada,
            'fue_corregida':      resultado.fue_corregida,
            'respuesta_corregida': resultado.respuesta_corregida,  # era patrones_sospechosos
        }

    # ──────────────────────────────────────────────────────────────────────
    # Opiniones para gestor de consejeras (sin cambios)
    # ──────────────────────────────────────────────────────────────────────

    def _generar_opinion_logica(self, texto: str, tiene_contradiccion: bool) -> Dict:
        if tiene_contradiccion:
            opinion = "Detectada posible contradicción o estructura lógica compleja."
            sugerencias = [
                "Verificar consistencia del razonamiento",
                "Identificar si hay contradicción real",
                "Clarificar relaciones lógicas",
            ]
            confianza = 0.7
        else:
            opinion = "Detectada estructura lógica (si/entonces). Validar coherencia."
            sugerencias = [
                "Verificar premisas",
                "Validar implicaciones",
                "Asegurar conclusión lógica",
            ]
            confianza = 0.8

        return {
            'consejera': self.nombre,
            'aprobada':  True,
            'veto':      False,
            'opinion':   opinion,
            'confianza': confianza,
            'razonamiento': [
                "1. Análisis: estructura lógica detectada",
                f"2. Contradicción potencial: {tiene_contradiccion}",
                "3. Recomendación: verificar consistencia",
            ],
            'sugerencias': sugerencias,
        }

    def _generar_opinion_neutral(self) -> Dict:
        return {
            'consejera':    self.nombre,
            'aprobada':     True,
            'veto':         False,
            'opinion':      'Sin estructura lógica compleja detectada.',
            'confianza':    0.5,
            'razonamiento': ["No hay conectores lógicos o contradicciones evidentes"],
            'sugerencias':  [],
        }