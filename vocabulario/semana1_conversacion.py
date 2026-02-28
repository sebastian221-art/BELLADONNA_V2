"""
Conceptos de Conversación - Semana 1 (VERSIÓN REFINADA).

10 conceptos de palabras básicas de conversación.
Incluye saludos, interrogativos, afirmación/negación.

CAMBIOS EN ESTA VERSIÓN:
- ✅ OPTIMIZADO: Grounding de palabras ultra-frecuentes subido a 0.95
- ✅ OPTIMIZADO: Interrogativos comunes subidos a 0.90
- Sin eliminaciones (todos son únicos y necesarios)
"""
from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto

def obtener_conceptos_conversacion():
    """Retorna conceptos de conversación (10 conceptos - OPTIMIZADOS)."""
    conceptos = []
    
    # SALUDOS Y CORTESÍA (2) - GROUNDING OPTIMIZADO
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_HOLA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["hola", "hi", "hello", "hey"],
        confianza_grounding=0.95,  # ← OPTIMIZADO de 0.9 a 0.95
        propiedades={
            'es_saludo': True,
            'requiere_respuesta': True,
            'ultra_frecuente': True
        },
        datos={
            'respuestas_apropiadas': [
                "Hola, ¿en qué puedo ayudarte?",
                "¡Hola! ¿Qué necesitas?"
            ]
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_GRACIAS",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["gracias", "thanks", "thank you"],
        confianza_grounding=0.95,  # ← OPTIMIZADO de 0.9 a 0.95
        propiedades={
            'es_agradecimiento': True,
            'ultra_frecuente': True
        }
    ))
    
    # AFIRMACIÓN/NEGACIÓN (2) - GROUNDING OPTIMIZADO
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SI",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["sí", "si", "yes", "afirmativo"],
        confianza_grounding=0.95,  # ← OPTIMIZADO de 0.9 a 0.95
        propiedades={
            'es_afirmacion': True,
            'ultra_frecuente': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["no", "nope", "negativo"],
        confianza_grounding=0.95,  # ← OPTIMIZADO de 0.9 a 0.95
        propiedades={
            'es_negacion': True,
            'ultra_frecuente': True
        }
    ))
    
    # INTERROGATIVOS (6) - GROUNDING OPTIMIZADO
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_QUE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["qué", "que", "what"],
        confianza_grounding=0.90,  # ← OPTIMIZADO de 0.8 a 0.90
        propiedades={
            'es_interrogativo': True,
            'muy_frecuente': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_COMO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["cómo", "como", "how"],
        confianza_grounding=0.90,  # ← OPTIMIZADO de 0.8 a 0.90
        propiedades={
            'es_interrogativo': True,
            'muy_frecuente': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_QUIEN",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["quién", "quien", "who"],
        confianza_grounding=0.85,  # ← OPTIMIZADO de 0.8 a 0.85
        propiedades={
            'es_interrogativo': True,
            'frecuente': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DONDE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["dónde", "donde", "where"],
        confianza_grounding=0.85,  # ← OPTIMIZADO de 0.8 a 0.85
        propiedades={
            'es_interrogativo': True,
            'frecuente': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CUANDO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["cuándo", "cuando", "when"],
        confianza_grounding=0.85,  # ← OPTIMIZADO de 0.8 a 0.85
        propiedades={
            'es_interrogativo': True,
            'frecuente': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_POR_QUE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["por qué", "porque", "why"],
        confianza_grounding=0.85,  # ← OPTIMIZADO de 0.8 a 0.85
        propiedades={
            'es_interrogativo': True,
            'pide_razon': True,
            'frecuente': True
        }
    ))
    
    return conceptos


if __name__ == '__main__':
    # Validación
    conceptos = obtener_conceptos_conversacion()
    print(f"✅ Vocabulario Conversación REFINADO: {len(conceptos)} conceptos")
    print(f"   Grounding promedio: {sum(c.confianza_grounding for c in conceptos) / len(conceptos):.2f}")
    print(f"   Conceptos ultra-frecuentes (≥0.95): {sum(1 for c in conceptos if c.confianza_grounding >= 0.95)}")