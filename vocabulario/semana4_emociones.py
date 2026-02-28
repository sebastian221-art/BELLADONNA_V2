"""
Conceptos de Emociones - Semana 4.

15 conceptos de estados emocionales y sentimientos.
Grounding medio-bajo (0.60-0.75) - son abstractos.

NOTA: CONCEPTO_SEGURO renombrado a CONCEPTO_SEGURO_EMOCION
para evitar duplicado con CONCEPTO_SEGURO de Semana 3.
"""
from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto

def obtener_conceptos_emociones():
    """Retorna conceptos de emociones (15 conceptos)."""
    conceptos = []
    
    # EMOCIONES BÁSICAS (6)
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FELIZ",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["feliz", "contento", "alegre", "happy"],
        confianza_grounding=0.70,
        propiedades={
            'es_emocion': True,
            'valencia': 'positiva',
            'intensidad': 'alta'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TRISTE",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["triste", "deprimido", "melancólico", "sad"],
        confianza_grounding=0.70,
        propiedades={
            'es_emocion': True,
            'valencia': 'negativa',
            'opuesto': 'feliz'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ENOJADO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["enojado", "molesto", "furioso", "angry"],
        confianza_grounding=0.70,
        propiedades={
            'es_emocion': True,
            'valencia': 'negativa',
            'intensidad': 'alta'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MIEDO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["miedo", "temor", "asustado", "fear"],
        confianza_grounding=0.70,
        propiedades={
            'es_emocion': True,
            'valencia': 'negativa',
            'respuesta': 'huida'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SORPRESA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["sorpresa", "asombro", "surprised"],
        confianza_grounding=0.65,
        propiedades={
            'es_emocion': True,
            'valencia': 'neutral',
            'duracion': 'breve'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CONFUNDIDO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["confundido", "desconcertado", "perplejo"],
        confianza_grounding=0.70,
        propiedades={
            'es_estado_mental': True,
            'claridad': 'baja'
        }
    ))
    
    # ESTADOS EMOCIONALES (5)
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FRUSTRADO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["frustrado", "desesperado", "impaciente"],
        confianza_grounding=0.70,
        propiedades={
            'es_estado_emocional': True,
            'valencia': 'negativa',
            'causa': 'obstaculo'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ANSIOSO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["ansioso", "nervioso", "preocupado"],
        confianza_grounding=0.70,
        propiedades={
            'es_estado_emocional': True,
            'valencia': 'negativa',
            'orientacion': 'futuro'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CALMADO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["calmado", "tranquilo", "sereno", "calm"],
        confianza_grounding=0.70,
        propiedades={
            'es_estado_emocional': True,
            'valencia': 'positiva',
            'intensidad': 'baja'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ABURRIDO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["aburrido", "hastiado", "bored"],
        confianza_grounding=0.65,
        propiedades={
            'es_estado_emocional': True,
            'valencia': 'negativa',
            'causa': 'falta_estimulo'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INTERESADO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["interesado", "curioso", "intrigado"],
        confianza_grounding=0.70,
        propiedades={
            'es_estado_mental': True,
            'valencia': 'positiva',
            'motivacion': 'alta'
        }
    ))
    
    # ACTITUDES (4) - CONCEPTO_SEGURO renombrado a CONCEPTO_SEGURO_EMOCION
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SEGURO_EMOCION",  # ← RENOMBRADO para evitar duplicado
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["seguro", "confiado", "confident"],
        confianza_grounding=0.70,
        propiedades={
            'es_actitud': True,
            'certeza': 'alta',
            'valencia': 'positiva'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INSEGURO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["inseguro", "dudoso", "insecure"],
        confianza_grounding=0.70,
        propiedades={
            'es_actitud': True,
            'certeza': 'baja',
            'opuesto': 'seguro'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_OPTIMISTA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["optimista", "esperanzado", "positivo"],
        confianza_grounding=0.65,
        propiedades={
            'es_actitud': True,
            'orientacion': 'futuro',
            'valencia': 'positiva'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SATISFECHO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["satisfecho", "complacido", "satisfied"],
        confianza_grounding=0.70,
        propiedades={
            'es_estado_emocional': True,
            'valencia': 'positiva',
            'necesidades': 'cumplidas'
        }
    ))
    
    return conceptos