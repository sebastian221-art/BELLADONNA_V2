"""
Contexto Conversacional - Expansión Fase 4A.

Palabras que ayudan a Bell a entender la intención del usuario.

Conceptos: 40 total
Grounding promedio: 0.78
Tipo: PALABRA_CONVERSACION
"""
from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto


def obtener_conceptos_contexto_conversacional():
    """
    Retorna conceptos de contexto conversacional.
    
    Categorías:
    - Urgencia/Prioridad (10)
    - Modalidad (10)
    - Actitud del hablante (10)
    - Referencia/Deixis (10)
    """
    conceptos = []
    
    # ══════════ URGENCIA/PRIORIDAD ══════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_URGENTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["urgente", "urgentemente", "es urgente", "de emergencia"],
        confianza_grounding=0.82,
        propiedades={
            "es_contexto": True,
            "nivel_urgencia": "alto",
            "accion_sugerida": "priorizar",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LO_ANTES_POSIBLE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["lo antes posible", "asap", "cuanto antes", "ya mismo"],
        confianza_grounding=0.80,
        propiedades={
            "es_contexto": True,
            "nivel_urgencia": "alto",
            "accion_sugerida": "responder_rapido",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CUANDO_PUEDAS",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["cuando puedas", "sin prisa", "no hay apuro"],
        confianza_grounding=0.78,
        propiedades={
            "es_contexto": True,
            "nivel_urgencia": "bajo",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_IMPORTANTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["importante", "es importante", "crucial", "crítico"],
        confianza_grounding=0.82,
        propiedades={
            "es_contexto": True,
            "nivel_prioridad": "alto",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NECESITO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["necesito", "requiero", "me hace falta"],
        confianza_grounding=0.85,
        propiedades={
            "es_contexto": True,
            "tipo_solicitud": "necesidad",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_QUISIERA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["quisiera", "me gustaría", "desearía"],
        confianza_grounding=0.80,
        propiedades={
            "es_contexto": True,
            "tipo_solicitud": "deseo",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PODRIAS",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["podrías", "puedes", "serías capaz de"],
        confianza_grounding=0.85,
        propiedades={
            "es_contexto": True,
            "tipo_solicitud": "capacidad",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DEBERIAS",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["deberías", "tendrías que", "habría que"],
        confianza_grounding=0.78,
        propiedades={
            "es_contexto": True,
            "tipo_solicitud": "sugerencia",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RAPIDO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["rápido", "rápidamente", "de prisa", "veloz"],
        confianza_grounding=0.80,
        propiedades={
            "es_contexto": True,
            "nivel_urgencia": "medio",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_POR_FAVOR_CONTEXTO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["por favor", "porfa", "te lo pido"],
        confianza_grounding=0.85,
        propiedades={
            "es_contexto": True,
            "es_cortesia": True,
            "tono_recomendado": "servicial",
        },
    ))
    
    # ══════════ MODALIDAD ═══════════════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PUEDE_SER",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["puede ser", "es posible", "podría ser"],
        confianza_grounding=0.75,
        propiedades={
            "es_contexto": True,
            "modalidad": "posibilidad",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TIENE_QUE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["tiene que", "debe", "hay que", "es necesario"],
        confianza_grounding=0.82,
        propiedades={
            "es_contexto": True,
            "modalidad": "obligacion",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NO_HACE_FALTA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["no hace falta", "no es necesario", "no tienes que"],
        confianza_grounding=0.78,
        propiedades={
            "es_contexto": True,
            "modalidad": "no_obligacion",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PERMITIDO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["permitido", "se puede", "está bien"],
        confianza_grounding=0.78,
        propiedades={
            "es_contexto": True,
            "modalidad": "permiso",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PROHIBIDO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["prohibido", "no se puede", "está mal", "no debes"],
        confianza_grounding=0.80,
        propiedades={
            "es_contexto": True,
            "modalidad": "prohibicion",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_OPCIONAL",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["opcional", "si quieres", "opcionalmente"],
        confianza_grounding=0.78,
        propiedades={
            "es_contexto": True,
            "modalidad": "opcional",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_OBLIGATORIO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["obligatorio", "requerido", "mandatorio"],
        confianza_grounding=0.80,
        propiedades={
            "es_contexto": True,
            "modalidad": "obligacion",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CONVIENE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["conviene", "convendría", "sería bueno"],
        confianza_grounding=0.75,
        propiedades={
            "es_contexto": True,
            "modalidad": "recomendacion",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EVITAR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["evitar", "hay que evitar", "mejor no"],
        confianza_grounding=0.78,
        propiedades={
            "es_contexto": True,
            "modalidad": "advertencia",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PREFERIR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["preferir", "prefiero", "mejor", "es preferible"],
        confianza_grounding=0.78,
        propiedades={
            "es_contexto": True,
            "modalidad": "preferencia",
        },
    ))
    
    # ══════════ ACTITUD DEL HABLANTE ════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_HONESTAMENTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["honestamente", "sinceramente", "francamente"],
        confianza_grounding=0.78,
        propiedades={
            "es_contexto": True,
            "actitud": "sinceridad",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_OBVIAMENTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["obviamente", "claramente", "evidentemente"],
        confianza_grounding=0.78,
        propiedades={
            "es_contexto": True,
            "actitud": "certeza",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DESAFORTUNADAMENTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["desafortunadamente", "lamentablemente", "por desgracia"],
        confianza_grounding=0.78,
        propiedades={
            "es_contexto": True,
            "actitud": "pesar",
            "tono_recomendado": "empático",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_AFORTUNADAMENTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["afortunadamente", "por suerte", "felizmente"],
        confianza_grounding=0.78,
        propiedades={
            "es_contexto": True,
            "actitud": "alivio",
            "valencia": "positiva",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_BASICAMENTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["básicamente", "esencialmente", "fundamentalmente"],
        confianza_grounding=0.78,
        propiedades={
            "es_contexto": True,
            "actitud": "simplificacion",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LITERALMENTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["literalmente", "textualmente"],
        confianza_grounding=0.75,
        propiedades={
            "es_contexto": True,
            "actitud": "precision",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_APROXIMADAMENTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["aproximadamente", "más o menos", "cerca de", "alrededor de"],
        confianza_grounding=0.78,
        propiedades={
            "es_contexto": True,
            "actitud": "aproximacion",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EXACTAMENTE_CONTEXTO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["exactamente", "precisamente", "justo"],
        confianza_grounding=0.80,
        propiedades={
            "es_contexto": True,
            "actitud": "precision",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PERSONALMENTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["personalmente", "en lo personal", "para mí"],
        confianza_grounding=0.75,
        propiedades={
            "es_contexto": True,
            "actitud": "opinion_personal",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TECNICAMENTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["técnicamente", "en términos técnicos"],
        confianza_grounding=0.78,
        propiedades={
            "es_contexto": True,
            "actitud": "precision_tecnica",
        },
    ))
    
    # ══════════ REFERENCIA/DEIXIS ═══════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ESTO_REF",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["esto", "este", "esta"],
        confianza_grounding=0.82,
        propiedades={
            "es_contexto": True,
            "es_deixis": True,
            "referencia": "proximal",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ESO_REF",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["eso", "ese", "esa"],
        confianza_grounding=0.82,
        propiedades={
            "es_contexto": True,
            "es_deixis": True,
            "referencia": "medial",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_AQUELLO_REF",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["aquello", "aquel", "aquella"],
        confianza_grounding=0.78,
        propiedades={
            "es_contexto": True,
            "es_deixis": True,
            "referencia": "distal",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LO_ANTERIOR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["lo anterior", "lo de antes", "lo previo"],
        confianza_grounding=0.78,
        propiedades={
            "es_contexto": True,
            "es_deixis": True,
            "referencia": "anaforica",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LO_SIGUIENTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["lo siguiente", "lo que sigue", "a continuación"],
        confianza_grounding=0.78,
        propiedades={
            "es_contexto": True,
            "es_deixis": True,
            "referencia": "cataforica",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MISMO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["mismo", "el mismo", "lo mismo"],
        confianza_grounding=0.80,
        propiedades={
            "es_contexto": True,
            "es_deixis": True,
            "referencia": "identidad",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_OTRO_REF",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["otro", "otra cosa", "algo más"],
        confianza_grounding=0.78,
        propiedades={
            "es_contexto": True,
            "es_deixis": True,
            "referencia": "alteridad",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TODO_REF",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["todo", "todos", "todas", "todo esto"],
        confianza_grounding=0.80,
        propiedades={
            "es_contexto": True,
            "es_deixis": True,
            "referencia": "totalidad",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ALGO_REF",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["algo", "alguna cosa", "cualquier cosa"],
        confianza_grounding=0.78,
        propiedades={
            "es_contexto": True,
            "es_deixis": True,
            "referencia": "indefinido",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NADA_REF",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["nada", "ninguna cosa", "nada de eso"],
        confianza_grounding=0.80,
        propiedades={
            "es_contexto": True,
            "es_deixis": True,
            "referencia": "negacion",
        },
    ))
    
    return conceptos


if __name__ == '__main__':
    conceptos = obtener_conceptos_contexto_conversacional()
    grounding_prom = sum(c.confianza_grounding for c in conceptos) / len(conceptos)
    print(f"✅ Contexto Conversacional: {len(conceptos)} conceptos")
    print(f"   Grounding promedio: {grounding_prom:.2f}")