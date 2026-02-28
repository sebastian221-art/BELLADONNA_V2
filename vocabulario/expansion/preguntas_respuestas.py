"""
Preguntas y Respuestas - Expansión Fase 4A.

Estructuras interrogativas y expresiones de afirmación/negación.

Conceptos: 60 total
Grounding promedio: 0.76
Tipo: PALABRA_CONVERSACION
"""
from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto


def obtener_conceptos_preguntas_respuestas():
    """
    Retorna conceptos de preguntas y respuestas.
    
    Categorías:
    - Palabras interrogativas (10 conceptos)
    - Afirmaciones (10 conceptos)
    - Negaciones (10 conceptos)
    - Expresiones de certeza (10 conceptos)
    - Conectores lógicos (12 conceptos)
    - Expresiones conversacionales (8 conceptos)
    """
    conceptos = []
    
    # ══════════ PALABRAS INTERROGATIVAS ═════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_QUE_PREGUNTA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["qué", "what", "cuál"],
        confianza_grounding=0.82,
        propiedades={
            "es_interrogativa": True,
            "tipo_respuesta": "identificacion",
            "accion_sugerida": "identificar_objeto",
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_PREGUNTA"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_QUIEN_PREGUNTA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["quién", "who", "quiénes"],
        confianza_grounding=0.80,
        propiedades={
            "es_interrogativa": True,
            "tipo_respuesta": "persona",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DONDE_PREGUNTA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["dónde", "where", "en qué lugar"],
        confianza_grounding=0.80,
        propiedades={
            "es_interrogativa": True,
            "tipo_respuesta": "lugar",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CUANDO_PREGUNTA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["cuándo", "when", "en qué momento"],
        confianza_grounding=0.80,
        propiedades={
            "es_interrogativa": True,
            "tipo_respuesta": "tiempo",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_COMO_PREGUNTA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["cómo", "how", "de qué manera"],
        confianza_grounding=0.82,
        propiedades={
            "es_interrogativa": True,
            "tipo_respuesta": "proceso",
            "accion_sugerida": "explicar_proceso",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_POR_QUE_PREGUNTA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["por qué", "why", "para qué"],
        confianza_grounding=0.80,
        propiedades={
            "es_interrogativa": True,
            "tipo_respuesta": "razon",
            "accion_sugerida": "explicar_causa",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CUANTO_PREGUNTA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["cuánto", "how much", "qué cantidad"],
        confianza_grounding=0.78,
        propiedades={
            "es_interrogativa": True,
            "tipo_respuesta": "cantidad",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CUANTOS_PREGUNTA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["cuántos", "how many", "qué tantos"],
        confianza_grounding=0.78,
        propiedades={
            "es_interrogativa": True,
            "tipo_respuesta": "cantidad_plural",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CUAL_PREGUNTA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["cuál", "which", "cuáles"],
        confianza_grounding=0.78,
        propiedades={
            "es_interrogativa": True,
            "tipo_respuesta": "seleccion",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_VERDAD_PREGUNTA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["¿verdad?", "right?", "¿no?", "¿cierto?"],
        confianza_grounding=0.75,
        propiedades={
            "es_interrogativa": True,
            "tipo_respuesta": "confirmacion",
        },
    ))
    
    # ══════════ AFIRMACIONES ════════════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SI_AFIRMACION",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["sí", "yes", "afirmativo", "claro"],
        confianza_grounding=0.85,
        propiedades={
            "es_afirmacion": True,
            "valor_logico": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_NO_NEGACION"},
            "relacionado_con": {"CONCEPTO_TRUE"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CORRECTO_RESP",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["correcto", "correct", "exacto", "así es"],
        confianza_grounding=0.82,
        propiedades={
            "es_afirmacion": True,
            "es_confirmacion": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_VERDAD_RESP",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["verdad", "true", "cierto", "es verdad"],
        confianza_grounding=0.80,
        propiedades={
            "es_afirmacion": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_TRUE"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DE_ACUERDO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["de acuerdo", "ok", "vale", "está bien", "okay"],
        confianza_grounding=0.80,
        propiedades={
            "es_afirmacion": True,
            "es_aceptacion": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_POR_SUPUESTO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["por supuesto", "of course", "desde luego", "obvio"],
        confianza_grounding=0.78,
        propiedades={
            "es_afirmacion": True,
            "intensidad": "alta",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EXACTAMENTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["exactamente", "exactly", "precisamente"],
        confianza_grounding=0.80,
        propiedades={
            "es_afirmacion": True,
            "es_confirmacion": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DEFINITIVAMENTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["definitivamente", "definitely", "sin duda"],
        confianza_grounding=0.78,
        propiedades={
            "es_afirmacion": True,
            "intensidad": "alta",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ABSOLUTAMENTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["absolutamente", "absolutely", "totalmente"],
        confianza_grounding=0.78,
        propiedades={
            "es_afirmacion": True,
            "intensidad": "maxima",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PERFECTO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["perfecto", "perfect", "genial", "excelente"],
        confianza_grounding=0.78,
        propiedades={
            "es_afirmacion": True,
            "es_aprobacion": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ENTENDIDO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["entendido", "understood", "comprendo", "ya entendí"],
        confianza_grounding=0.80,
        propiedades={
            "es_afirmacion": True,
            "es_comprension": True,
        },
    ))
    
    # ══════════ NEGACIONES ══════════════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NO_NEGACION",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["no", "not", "negativo"],
        confianza_grounding=0.85,
        propiedades={
            "es_negacion": True,
            "valor_logico": False,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_SI_AFIRMACION"},
            "relacionado_con": {"CONCEPTO_FALSE"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NUNCA_RESP",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["nunca", "never", "jamás"],
        confianza_grounding=0.80,
        propiedades={
            "es_negacion": True,
            "intensidad": "maxima",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NADA_RESP",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["nada", "nothing", "ninguna cosa"],
        confianza_grounding=0.78,
        propiedades={
            "es_negacion": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NADIE_RESP",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["nadie", "nobody", "ninguna persona"],
        confianza_grounding=0.78,
        propiedades={
            "es_negacion": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NINGUNO_RESP",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["ninguno", "none", "ninguna"],
        confianza_grounding=0.78,
        propiedades={
            "es_negacion": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INCORRECTO_RESP",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["incorrecto", "incorrect", "equivocado", "mal"],
        confianza_grounding=0.78,
        propiedades={
            "es_negacion": True,
            "es_correccion": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FALSO_RESP",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["falso", "false", "mentira"],
        confianza_grounding=0.78,
        propiedades={
            "es_negacion": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_FALSE"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_IMPOSIBLE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["imposible", "impossible", "no se puede"],
        confianza_grounding=0.75,
        propiedades={
            "es_negacion": True,
            "intensidad": "maxima",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TAMPOCO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["tampoco", "neither", "ni yo"],
        confianza_grounding=0.72,
        propiedades={
            "es_negacion": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TODAVIA_NO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["todavía no", "not yet", "aún no"],
        confianza_grounding=0.75,
        propiedades={
            "es_negacion": True,
            "es_temporal": True,
        },
    ))
    
    # ══════════ EXPRESIONES DE CERTEZA ══════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_QUIZAS",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["quizás", "maybe", "tal vez", "quizá"],
        confianza_grounding=0.75,
        propiedades={
            "es_certeza": True,
            "nivel_certeza": 0.5,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PROBABLEMENTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["probablemente", "probably", "es probable"],
        confianza_grounding=0.75,
        propiedades={
            "es_certeza": True,
            "nivel_certeza": 0.7,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_POSIBLEMENTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["posiblemente", "possibly", "es posible"],
        confianza_grounding=0.72,
        propiedades={
            "es_certeza": True,
            "nivel_certeza": 0.6,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SEGURAMENTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["seguramente", "surely", "seguro que"],
        confianza_grounding=0.75,
        propiedades={
            "es_certeza": True,
            "nivel_certeza": 0.85,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_APARENTEMENTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["aparentemente", "apparently", "al parecer"],
        confianza_grounding=0.70,
        propiedades={
            "es_certeza": True,
            "nivel_certeza": 0.6,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_REALMENTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["realmente", "really", "de verdad", "en serio"],
        confianza_grounding=0.78,
        propiedades={
            "es_certeza": True,
            "nivel_certeza": 0.9,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CREO_QUE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["creo que", "I think", "pienso que"],
        confianza_grounding=0.72,
        propiedades={
            "es_certeza": True,
            "nivel_certeza": 0.6,
            "es_opinion": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ESTOY_SEGURO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["estoy seguro", "I'm sure", "estoy convencido"],
        confianza_grounding=0.78,
        propiedades={
            "es_certeza": True,
            "nivel_certeza": 0.9,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NO_ESTOY_SEGURO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["no estoy seguro", "not sure", "no sé si"],
        confianza_grounding=0.75,
        propiedades={
            "es_certeza": True,
            "nivel_certeza": 0.4,
            "accion_sugerida": "clarificar",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DEPENDE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["depende", "depends", "según", "it depends"],
        confianza_grounding=0.75,
        propiedades={
            "es_certeza": True,
            "nivel_certeza": 0.5,
            "accion_sugerida": "pedir_contexto",
        },
    ))
    
    # ══════════ CONECTORES LÓGICOS ══════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PORQUE_CONECTOR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["porque", "because", "ya que", "debido a"],
        confianza_grounding=0.80,
        propiedades={
            "es_conector": True,
            "tipo_logico": "causalidad",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ENTONCES_CONECTOR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["entonces", "then", "por lo tanto", "así que"],
        confianza_grounding=0.80,
        propiedades={
            "es_conector": True,
            "tipo_logico": "consecuencia",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PERO_CONECTOR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["pero", "but", "sin embargo", "aunque"],
        confianza_grounding=0.80,
        propiedades={
            "es_conector": True,
            "tipo_logico": "contraste",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ADEMAS_CONECTOR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["además", "also", "también", "incluso"],
        confianza_grounding=0.78,
        propiedades={
            "es_conector": True,
            "tipo_logico": "adicion",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SIN_EMBARGO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["sin embargo", "however", "no obstante"],
        confianza_grounding=0.78,
        propiedades={
            "es_conector": True,
            "tipo_logico": "contraste",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_POR_LO_TANTO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["por lo tanto", "therefore", "en consecuencia"],
        confianza_grounding=0.78,
        propiedades={
            "es_conector": True,
            "tipo_logico": "conclusion",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ES_DECIR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["es decir", "that is", "o sea", "en otras palabras"],
        confianza_grounding=0.78,
        propiedades={
            "es_conector": True,
            "tipo_logico": "reformulacion",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_POR_EJEMPLO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["por ejemplo", "for example", "como"],
        confianza_grounding=0.80,
        propiedades={
            "es_conector": True,
            "tipo_logico": "ejemplificacion",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EN_CONCLUSION",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["en conclusión", "in conclusion", "para terminar"],
        confianza_grounding=0.75,
        propiedades={
            "es_conector": True,
            "tipo_logico": "conclusion",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PRIMERO_CONECTOR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["primero", "first", "en primer lugar"],
        confianza_grounding=0.78,
        propiedades={
            "es_conector": True,
            "tipo_logico": "secuencia",
            "orden": 1,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LUEGO_CONECTOR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["luego", "then", "después", "a continuación"],
        confianza_grounding=0.78,
        propiedades={
            "es_conector": True,
            "tipo_logico": "secuencia",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FINALMENTE_CONECTOR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["finalmente", "finally", "por último"],
        confianza_grounding=0.78,
        propiedades={
            "es_conector": True,
            "tipo_logico": "secuencia",
            "orden": -1,
        },
    ))
    
    # ══════════ EXPRESIONES CONVERSACIONALES ════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_GRACIAS_EXPR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["gracias", "thanks", "thank you", "te agradezco"],
        confianza_grounding=0.82,
        propiedades={
            "es_expresion_social": True,
            "es_agradecimiento": True,
            "tono_recomendado": "cordial",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_POR_FAVOR_EXPR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["por favor", "please", "porfa"],
        confianza_grounding=0.82,
        propiedades={
            "es_expresion_social": True,
            "es_cortesia": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DISCULPA_EXPR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["disculpa", "sorry", "perdón", "lo siento"],
        confianza_grounding=0.80,
        propiedades={
            "es_expresion_social": True,
            "es_disculpa": True,
            "tono_recomendado": "comprensivo",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_HOLA_EXPR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["hola", "hello", "hi", "hey", "buenas"],
        confianza_grounding=0.85,
        propiedades={
            "es_expresion_social": True,
            "es_saludo": True,
            "tono_recomendado": "amistoso",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ADIOS_EXPR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["adiós", "bye", "goodbye", "hasta luego", "nos vemos"],
        confianza_grounding=0.82,
        propiedades={
            "es_expresion_social": True,
            "es_despedida": True,
            "tono_recomendado": "cordial",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_BUENOS_DIAS",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["buenos días", "good morning", "buen día"],
        confianza_grounding=0.80,
        propiedades={
            "es_expresion_social": True,
            "es_saludo": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_BUENAS_NOCHES",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["buenas noches", "good night"],
        confianza_grounding=0.80,
        propiedades={
            "es_expresion_social": True,
            "es_saludo": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DE_NADA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["de nada", "you're welcome", "no hay de qué"],
        confianza_grounding=0.80,
        propiedades={
            "es_expresion_social": True,
            "es_respuesta_agradecimiento": True,
        },
    ))
    
    return conceptos


if __name__ == '__main__':
    conceptos = obtener_conceptos_preguntas_respuestas()
    grounding_prom = sum(c.confianza_grounding for c in conceptos) / len(conceptos)
    print(f"✅ Preguntas y Respuestas: {len(conceptos)} conceptos")
    print(f"   Grounding promedio: {grounding_prom:.2f}")