"""
Templates de Respuesta - Convertir Decisiones a Español.

Bell usa templates para generar respuestas naturales.
NO es generación mágica. Son templates + variables.
"""
from typing import Dict, List
from razonamiento.tipos_decision import TipoDecision, RazonRechazo

class TemplatesRespuesta:
    """
    Contiene templates de respuesta para cada tipo de decisión.
    
    Bell NO improvisa. Bell usa templates predefinidos.
    """
    
    def __init__(self):
        """Inicializa templates."""
        self.templates = self._cargar_templates()
    
    def _cargar_templates(self) -> Dict:
        """Define todos los templates de respuesta."""
        return {
            # AFIRMATIVA
            TipoDecision.AFIRMATIVA: {
                'certeza_alta': [
                    "Sí, puedo {accion}. Tengo grounding {grounding} con operación ejecutable.",
                    "Correcto, puedo {accion}. Operación disponible: {operacion}.",
                    "Sí. Puedo ejecutar {accion} con certeza {certeza}%.",
                ],
                'certeza_media': [
                    "Puedo intentar {accion}. Grounding medio ({grounding}), proceder con precaución.",
                    "Sí, aunque con advertencia. Grounding {grounding} para {accion}.",
                ]
            },
            
            # NEGATIVA
            TipoDecision.NEGATIVA: {
                RazonRechazo.SIN_OPERACION: [
                    "No puedo {accion}. Razón: {razon}",
                    "No tengo capacidad para {accion}. {razon}",
                    "Lo siento, no puedo {accion} porque no tengo la operación necesaria.",
                ],
                RazonRechazo.SIN_GROUNDING: [
                    "No puedo {accion}. Mi grounding es insuficiente ({grounding}).",
                    "No tengo confianza suficiente para {accion}. Grounding: {grounding}.",
                ],
                RazonRechazo.VEGA_VETO: [
                    "No puedo {accion}. Vega ha vetado esta acción por violar: {principio}.",
                    "Acción bloqueada. Razón: {razon_veto}",
                    "No procederé. Esta acción viola el principio de {principio}. {recomendacion}",
                ]
            },
            
            # SALUDO
            TipoDecision.SALUDO: [
                "Hola! ¿En qué puedo ayudarte?",
                "Hola! Estoy lista para ayudar.",
                "Hola! ¿Qué necesitas?",
            ],
            
            # AGRADECIMIENTO
            TipoDecision.AGRADECIMIENTO: [
                "De nada! Estoy aquí para ayudar.",
                "Con gusto! ¿Necesitas algo más?",
                "No hay de qué! ¿Puedo ayudarte con algo más?",
            ],
            
            # NO_ENTENDIDO
            TipoDecision.NO_ENTENDIDO: [
                "No entendí tu mensaje. ¿Podrías reformularlo?",
                "Lo siento, no pude procesar eso. Confianza de traducción: {confianza}%.",
                "No reconozco suficientes palabras. Palabras desconocidas: {desconocidas}.",
            ],
            
            # NECESITA_ACLARACION
            TipoDecision.NECESITA_ACLARACION: [
                "¿Podrías ser más específico? {razon}",
                "Necesito más información. ¿A qué te refieres exactamente?",
            ]
        }
    
    def obtener_template(self, tipo: TipoDecision, 
                        subtipo=None, 
                        preferencia: int = 0) -> str:
        """
        Obtiene un template apropiado.
        
        Args:
            tipo: TipoDecision
            subtipo: Subtipo (ej: certeza_alta, RazonRechazo)
            preferencia: Índice del template (si hay varios)
            
        Returns:
            Template string con placeholders
        """
        templates_tipo = self.templates.get(tipo, [])
        
        # Si hay subtipos (dict)
        if isinstance(templates_tipo, dict):
            if subtipo is None:
                # Tomar primer subtipo disponible
                subtipo = list(templates_tipo.keys())[0]
            
            templates_lista = templates_tipo.get(subtipo, ["No hay template disponible"])
        else:
            # Lista directa
            templates_lista = templates_tipo
        
        # Seleccionar template
        if preferencia < len(templates_lista):
            return templates_lista[preferencia]
        else:
            return templates_lista[0]  # Fallback al primero