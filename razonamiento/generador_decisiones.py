"""
Generador de Decisiones - Crea objetos Decision.

Toma evaluaciones y las convierte en decisiones estructuradas.
"""
from typing import List
from core.concepto_anclado import ConceptoAnclado
from razonamiento.tipos_decision import Decision, TipoDecision, RazonRechazo
from razonamiento.evaluador_capacidades import EvaluadorCapacidades

class GeneradorDecisiones:
    """
    Genera objetos Decision basados en evaluación de capacidades.
    
    Conecta: Evaluación → Decision estructurada
    """
    
    def __init__(self):
        """Inicializa generador."""
        self.evaluador = EvaluadorCapacidades()
    
    def generar_decision_capacidad(self,
                                   conceptos: List[ConceptoAnclado],
                                   intencion: str) -> Decision:
        """
        Genera decisión para pregunta de capacidad.
        
        Ejemplo: "¿Puedes leer archivos?" → Decision(AFIRMATIVA, certeza=1.0)
        """
        # Evaluar capacidad
        evaluacion = self.evaluador.evaluar_capacidad_accion(conceptos)
        
        # Construir pasos de razonamiento
        pasos = [
            f"1. Detectados {len(conceptos)} conceptos",
            f"2. Concepto principal: {evaluacion['concepto_clave'].id if evaluacion['concepto_clave'] else 'Ninguno'}",
            f"3. Grounding: {evaluacion['confianza']:.2f}",
            f"4. Operaciones: {evaluacion['operacion'] or 'Ninguna'}"
        ]
        
        if evaluacion['puede_ejecutar']:
            # AFIRMATIVA
            pasos.append(f"5. Decisión: PUEDE ejecutar")
            
            return Decision(
                tipo=TipoDecision.AFIRMATIVA,
                certeza=evaluacion['confianza'],
                conceptos_principales=[evaluacion['concepto_clave'].id],
                puede_ejecutar=True,
                operacion_disponible=evaluacion['operacion'],
                razon=evaluacion['razon'],
                pasos_razonamiento=pasos,
                grounding_promedio=evaluacion['confianza']
            )
        else:
            # NEGATIVA
            pasos.append(f"5. Decisión: NO puede ejecutar - {evaluacion['razon']}")
            
            # Determinar razón de rechazo
            if not evaluacion['operacion']:
                razon_rechazo = RazonRechazo.SIN_OPERACION
            else:
                razon_rechazo = RazonRechazo.SIN_GROUNDING
            
            return Decision(
                tipo=TipoDecision.NEGATIVA,
                certeza=evaluacion['confianza'],
                conceptos_principales=[evaluacion['concepto_clave'].id] if evaluacion['concepto_clave'] else [],
                puede_ejecutar=False,
                razon=evaluacion['razon'],
                razon_rechazo=razon_rechazo,
                pasos_razonamiento=pasos,
                grounding_promedio=evaluacion['confianza']
            )
    
    def generar_decision_saludo(self, conceptos: List[ConceptoAnclado]) -> Decision:
        """Genera decisión para saludo."""
        return Decision(
            tipo=TipoDecision.SALUDO,
            certeza=0.95,
            conceptos_principales=[c.id for c in conceptos if 'HOLA' in c.id],
            razon="Detectado saludo",
            pasos_razonamiento=["1. Intención: SALUDO", "2. Responder apropiadamente"],
            grounding_promedio=0.9
        )
    
    def generar_decision_agradecimiento(self, conceptos: List[ConceptoAnclado]) -> Decision:
        """Genera decisión para agradecimiento."""
        return Decision(
            tipo=TipoDecision.AGRADECIMIENTO,
            certeza=0.95,
            conceptos_principales=[c.id for c in conceptos if 'GRACIAS' in c.id],
            razon="Detectado agradecimiento",
            pasos_razonamiento=["1. Intención: AGRADECIMIENTO", "2. Responder apropiadamente"],
            grounding_promedio=0.9
        )
    
    def generar_decision_no_entendido(self, confianza_traduccion: float) -> Decision:
        """Genera decisión cuando no entendió."""
        return Decision(
            tipo=TipoDecision.NO_ENTENDIDO,
            certeza=1.0 - confianza_traduccion,  # Inverso de confianza
            conceptos_principales=[],
            razon=f"Confianza de traducción muy baja: {confianza_traduccion:.0%}",
            razon_rechazo=RazonRechazo.DESCONOCIDO,
            pasos_razonamiento=[
                "1. Traducción con confianza baja",
                "2. Muchas palabras desconocidas",
                "3. No se puede procesar"
            ],
            grounding_promedio=0.0
        )