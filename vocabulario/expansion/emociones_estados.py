"""
Emociones y Estados - Expansión Fase 4A.

Vocabulario emocional para reconocer contexto del usuario.

Conceptos: 60 total
Grounding promedio: 0.72
Tipo: PALABRA_CONVERSACION

IMPORTANTE: Bell NO siente emociones, pero reconoce el estado
emocional del usuario para responder apropiadamente.
"""
from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto


def obtener_conceptos_emociones_estados():
    """
    Retorna emociones y estados.
    
    Categorías:
    - Emociones positivas (15 conceptos)
    - Emociones negativas (15 conceptos)
    - Estados físicos (15 conceptos)
    - Estados mentales (15 conceptos)
    """
    conceptos = []
    
    # ══════════ EMOCIONES POSITIVAS ═════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FELIZ",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["feliz", "happy", "contento", "alegre"],
        confianza_grounding=0.75,
        propiedades={
            "es_estado_emocional": True,
            "valencia": "positiva",
            "tono_recomendado": "alegre",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_TRISTE"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EMOCIONADO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["emocionado", "excited", "entusiasmado", "ilusionado"],
        confianza_grounding=0.75,
        propiedades={
            "es_estado_emocional": True,
            "valencia": "positiva",
            "intensidad": "alta",
            "tono_recomendado": "entusiasta",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TRANQUILO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["tranquilo", "calm", "sereno", "relajado", "en paz"],
        confianza_grounding=0.75,
        propiedades={
            "es_estado_emocional": True,
            "valencia": "positiva",
            "intensidad": "baja",
            "tono_recomendado": "calmado",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SATISFECHO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["satisfecho", "satisfied", "complacido", "realizado"],
        confianza_grounding=0.72,
        propiedades={
            "es_estado_emocional": True,
            "valencia": "positiva",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ORGULLOSO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["orgulloso", "proud"],
        confianza_grounding=0.70,
        propiedades={
            "es_estado_emocional": True,
            "valencia": "positiva",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_AGRADECIDO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["agradecido", "grateful", "thankful"],
        confianza_grounding=0.75,
        propiedades={
            "es_estado_emocional": True,
            "valencia": "positiva",
            "tono_recomendado": "apreciativo",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ESPERANZADO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["esperanzado", "hopeful", "optimista"],
        confianza_grounding=0.70,
        propiedades={
            "es_estado_emocional": True,
            "valencia": "positiva",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MOTIVADO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["motivado", "motivated", "animado", "con ganas"],
        confianza_grounding=0.75,
        propiedades={
            "es_estado_emocional": True,
            "valencia": "positiva",
            "tono_recomendado": "alentador",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CONFIADO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["confiado", "confident", "seguro de sí"],
        confianza_grounding=0.72,
        propiedades={
            "es_estado_emocional": True,
            "valencia": "positiva",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ALIVIADO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["aliviado", "relieved"],
        confianza_grounding=0.70,
        propiedades={
            "es_estado_emocional": True,
            "valencia": "positiva",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CURIOSO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["curioso", "curious", "intrigado", "interesado"],
        confianza_grounding=0.75,
        propiedades={
            "es_estado_emocional": True,
            "valencia": "positiva",
            "accion_sugerida": "explorar_mas",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INSPIRADO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["inspirado", "inspired"],
        confianza_grounding=0.70,
        propiedades={
            "es_estado_emocional": True,
            "valencia": "positiva",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DIVERTIDO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["divertido", "amused", "entretenido"],
        confianza_grounding=0.72,
        propiedades={
            "es_estado_emocional": True,
            "valencia": "positiva",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_AMOROSO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["amoroso", "loving", "cariñoso"],
        confianza_grounding=0.68,
        propiedades={
            "es_estado_emocional": True,
            "valencia": "positiva",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ASOMBRADO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["asombrado", "amazed", "sorprendido positivamente", "maravillado"],
        confianza_grounding=0.70,
        propiedades={
            "es_estado_emocional": True,
            "valencia": "positiva",
        },
    ))
    
    # ══════════ EMOCIONES NEGATIVAS ═════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TRISTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["triste", "sad", "apenado", "afligido"],
        confianza_grounding=0.75,
        propiedades={
            "es_estado_emocional": True,
            "valencia": "negativa",
            "tono_recomendado": "empático",
            "accion_sugerida": "consolar",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_FELIZ"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ENOJADO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["enojado", "angry", "furioso", "molesto", "irritado"],
        confianza_grounding=0.75,
        propiedades={
            "es_estado_emocional": True,
            "valencia": "negativa",
            "intensidad": "alta",
            "tono_recomendado": "calmante",
            "accion_sugerida": "validar_emocion",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ASUSTADO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["asustado", "scared", "atemorizado", "con miedo"],
        confianza_grounding=0.75,
        propiedades={
            "es_estado_emocional": True,
            "valencia": "negativa",
            "tono_recomendado": "tranquilizador",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NERVIOSO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["nervioso", "nervous", "ansioso", "inquieto"],
        confianza_grounding=0.75,
        propiedades={
            "es_estado_emocional": True,
            "valencia": "negativa",
            "tono_recomendado": "calmante",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FRUSTRADO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["frustrado", "frustrated"],
        confianza_grounding=0.78,
        propiedades={
            "es_estado_emocional": True,
            "valencia": "negativa",
            "tono_recomendado": "paciente",
            "accion_sugerida": "simplificar",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CONFUNDIDO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["confundido", "confused", "desconcertado", "perdido", "no entiendo"],
        confianza_grounding=0.80,
        propiedades={
            "es_estado_emocional": True,
            "valencia": "negativa",
            "tono_recomendado": "paciente",
            "accion_sugerida": "simplificar_explicacion",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ABURRIDO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["aburrido", "bored", "hastiado"],
        confianza_grounding=0.72,
        propiedades={
            "es_estado_emocional": True,
            "valencia": "negativa",
            "intensidad": "baja",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PREOCUPADO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["preocupado", "worried", "inquieto"],
        confianza_grounding=0.75,
        propiedades={
            "es_estado_emocional": True,
            "valencia": "negativa",
            "tono_recomendado": "tranquilizador",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DECEPCIONADO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["decepcionado", "disappointed", "desilusionado"],
        confianza_grounding=0.72,
        propiedades={
            "es_estado_emocional": True,
            "valencia": "negativa",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ESTRESADO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["estresado", "stressed", "agobiado", "abrumado"],
        confianza_grounding=0.78,
        propiedades={
            "es_estado_emocional": True,
            "valencia": "negativa",
            "tono_recomendado": "calmante",
            "accion_sugerida": "priorizar",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INSEGURO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["inseguro", "insecure", "dubitativo"],
        confianza_grounding=0.70,
        propiedades={
            "es_estado_emocional": True,
            "valencia": "negativa",
            "tono_recomendado": "alentador",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SOLO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["solo", "lonely", "solitario", "aislado"],
        confianza_grounding=0.70,
        propiedades={
            "es_estado_emocional": True,
            "valencia": "negativa",
            "tono_recomendado": "empático",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_AVERGONZADO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["avergonzado", "ashamed", "apenado"],
        confianza_grounding=0.68,
        propiedades={
            "es_estado_emocional": True,
            "valencia": "negativa",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CELOSO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["celoso", "jealous", "envidioso"],
        confianza_grounding=0.65,
        propiedades={
            "es_estado_emocional": True,
            "valencia": "negativa",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DESESPERADO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["desesperado", "desperate", "angustiado"],
        confianza_grounding=0.72,
        propiedades={
            "es_estado_emocional": True,
            "valencia": "negativa",
            "intensidad": "alta",
            "tono_recomendado": "empático",
            "accion_sugerida": "calmar_primero",
        },
    ))
    
    # ══════════ ESTADOS FÍSICOS ═════════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CANSADO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["cansado", "tired", "agotado", "exhausto", "fatigado"],
        confianza_grounding=0.75,
        propiedades={
            "es_estado_fisico": True,
            "valencia": "negativa",
            "accion_sugerida": "ser_breve",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_ENERGICO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ENERGICO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["enérgico", "energetic", "activo", "con energía"],
        confianza_grounding=0.72,
        propiedades={
            "es_estado_fisico": True,
            "valencia": "positiva",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_CANSADO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_HAMBRIENTO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["hambriento", "hungry", "con hambre"],
        confianza_grounding=0.72,
        propiedades={
            "es_estado_fisico": True,
            "bell_puede_ejecutar": False,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SEDIENTO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["sediento", "thirsty", "con sed"],
        confianza_grounding=0.72,
        propiedades={
            "es_estado_fisico": True,
            "bell_puede_ejecutar": False,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SOMNOLIENTO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["somnoliento", "sleepy", "con sueño", "adormilado"],
        confianza_grounding=0.72,
        propiedades={
            "es_estado_fisico": True,
            "accion_sugerida": "ser_breve",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DESPIERTO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["despierto", "awake", "alerta", "despabilado"],
        confianza_grounding=0.72,
        propiedades={
            "es_estado_fisico": True,
            "valencia": "positiva",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ENFERMO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["enfermo", "sick", "mal", "indispuesto"],
        confianza_grounding=0.75,
        propiedades={
            "es_estado_fisico": True,
            "valencia": "negativa",
            "tono_recomendado": "empático",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_SANO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SANO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["sano", "healthy", "saludable", "bien"],
        confianza_grounding=0.72,
        propiedades={
            "es_estado_fisico": True,
            "valencia": "positiva",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_ENFERMO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DOLORIDO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["dolorido", "in pain", "adolorido", "con dolor"],
        confianza_grounding=0.70,
        propiedades={
            "es_estado_fisico": True,
            "valencia": "negativa",
            "tono_recomendado": "empático",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_COMODO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["cómodo", "comfortable", "a gusto"],
        confianza_grounding=0.70,
        propiedades={
            "es_estado_fisico": True,
            "valencia": "positiva",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_INCOMODO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INCOMODO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["incómodo", "uncomfortable"],
        confianza_grounding=0.70,
        propiedades={
            "es_estado_fisico": True,
            "valencia": "negativa",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_COMODO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CON_FRIO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["con frío", "cold", "helado"],
        confianza_grounding=0.68,
        propiedades={
            "es_estado_fisico": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CON_CALOR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["con calor", "hot", "acalorado"],
        confianza_grounding=0.68,
        propiedades={
            "es_estado_fisico": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DEBIL",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["débil", "weak", "sin fuerzas"],
        confianza_grounding=0.68,
        propiedades={
            "es_estado_fisico": True,
            "valencia": "negativa",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FUERTE_ESTADO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["fuerte", "strong", "vigoroso"],
        confianza_grounding=0.68,
        propiedades={
            "es_estado_fisico": True,
            "valencia": "positiva",
        },
    ))
    
    # ══════════ ESTADOS MENTALES ════════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CONCENTRADO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["concentrado", "focused", "enfocado", "atento"],
        confianza_grounding=0.75,
        propiedades={
            "es_estado_mental": True,
            "valencia": "positiva",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_DISTRAIDO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DISTRAIDO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["distraído", "distracted", "despistado"],
        confianza_grounding=0.72,
        propiedades={
            "es_estado_mental": True,
            "valencia": "negativa",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_CONCENTRADO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PENSATIVO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["pensativo", "thoughtful", "reflexivo", "meditabundo"],
        confianza_grounding=0.70,
        propiedades={
            "es_estado_mental": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DECIDIDO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["decidido", "determined", "resuelto"],
        confianza_grounding=0.72,
        propiedades={
            "es_estado_mental": True,
            "valencia": "positiva",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_INDECISO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INDECISO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["indeciso", "undecided", "dudoso"],
        confianza_grounding=0.70,
        propiedades={
            "es_estado_mental": True,
            "valencia": "negativa",
            "accion_sugerida": "ofrecer_opciones",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_DECIDIDO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CREATIVO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["creativo", "creative", "imaginativo"],
        confianza_grounding=0.70,
        propiedades={
            "es_estado_mental": True,
            "valencia": "positiva",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_BLOQUEADO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["bloqueado", "blocked", "atascado", "estancado"],
        confianza_grounding=0.75,
        propiedades={
            "es_estado_mental": True,
            "valencia": "negativa",
            "accion_sugerida": "ofrecer_alternativas",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_OCUPADO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["ocupado", "busy", "atareado", "liado"],
        confianza_grounding=0.75,
        propiedades={
            "es_estado_mental": True,
            "accion_sugerida": "ser_breve",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_LIBRE"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LIBRE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["libre", "free", "disponible", "desocupado"],
        confianza_grounding=0.72,
        propiedades={
            "es_estado_mental": True,
            "valencia": "positiva",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_OCUPADO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LISTO_ESTADO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["listo", "ready", "preparado"],
        confianza_grounding=0.78,
        propiedades={
            "es_estado_mental": True,
            "valencia": "positiva",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PERDIDO_ESTADO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["perdido", "lost", "desorientado"],
        confianza_grounding=0.75,
        propiedades={
            "es_estado_mental": True,
            "valencia": "negativa",
            "tono_recomendado": "guía",
            "accion_sugerida": "clarificar_contexto",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INTERESADO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["interesado", "interested"],
        confianza_grounding=0.75,
        propiedades={
            "es_estado_mental": True,
            "valencia": "positiva",
            "accion_sugerida": "expandir_tema",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ABRUMADO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["abrumado", "overwhelmed", "sobrepasado"],
        confianza_grounding=0.72,
        propiedades={
            "es_estado_mental": True,
            "valencia": "negativa",
            "accion_sugerida": "simplificar",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SEGURO_ESTADO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["seguro", "sure", "cierto", "convencido"],
        confianza_grounding=0.75,
        propiedades={
            "es_estado_mental": True,
            "valencia": "positiva",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ATENTO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["atento", "attentive", "presente"],
        confianza_grounding=0.72,
        propiedades={
            "es_estado_mental": True,
            "valencia": "positiva",
        },
    ))
    
    return conceptos


if __name__ == '__main__':
    conceptos = obtener_conceptos_emociones_estados()
    grounding_prom = sum(c.confianza_grounding for c in conceptos) / len(conceptos)
    positivos = sum(1 for c in conceptos if c.propiedades.get('valencia') == 'positiva')
    negativos = sum(1 for c in conceptos if c.propiedades.get('valencia') == 'negativa')
    print(f"✅ Emociones y Estados: {len(conceptos)} conceptos")
    print(f"   Valencia positiva: {positivos}")
    print(f"   Valencia negativa: {negativos}")
    print(f"   Grounding promedio: {grounding_prom:.2f}")