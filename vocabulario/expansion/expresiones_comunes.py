"""
Expresiones Comunes - Expansión Fase 4A.

Modismos, frases hechas y expresiones cotidianas.

Conceptos: 50 total
Grounding promedio: 0.75
Tipo: PALABRA_CONVERSACION
"""
from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto


def obtener_conceptos_expresiones_comunes():
    """
    Retorna expresiones comunes del español.
    
    Categorías:
    - Expresiones de acuerdo/desacuerdo (10)
    - Expresiones de sorpresa/emoción (10)
    - Expresiones de cortesía (10)
    - Expresiones de opinión (10)
    - Expresiones de transición (10)
    """
    conceptos = []
    
    # ══════════ ACUERDO/DESACUERDO ══════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CLARO_QUE_SI",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["claro que sí", "por supuesto que sí", "cómo no"],
        confianza_grounding=0.80,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "acuerdo_enfatico",
            "tono_recomendado": "entusiasta",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PARA_NADA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["para nada", "ni hablar", "de ninguna manera"],
        confianza_grounding=0.78,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "desacuerdo_enfatico",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ME_PARECE_BIEN",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["me parece bien", "me parece genial", "suena bien"],
        confianza_grounding=0.78,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "aprobacion",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NO_LO_CREO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["no lo creo", "lo dudo", "no me convence"],
        confianza_grounding=0.75,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "duda",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TIENES_RAZON",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["tienes razón", "es verdad", "así es"],
        confianza_grounding=0.80,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "concesion",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NO_ESTOY_DE_ACUERDO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["no estoy de acuerdo", "discrepo", "no coincido"],
        confianza_grounding=0.78,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "desacuerdo_cortes",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_BUENA_IDEA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["buena idea", "gran idea", "excelente idea"],
        confianza_grounding=0.78,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "aprobacion",
            "tono_recomendado": "entusiasta",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NO_SE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["no sé", "no tengo idea", "ni idea"],
        confianza_grounding=0.80,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "ignorancia",
            "accion_sugerida": "ofrecer_buscar",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_A_LO_MEJOR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["a lo mejor", "puede que", "capaz que"],
        confianza_grounding=0.72,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "posibilidad",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SIN_DUDA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["sin duda", "indudablemente", "sin lugar a dudas"],
        confianza_grounding=0.80,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "certeza_total",
        },
    ))
    
    # ══════════ SORPRESA/EMOCIÓN ════════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_QUE_BIEN",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["qué bien", "genial", "fantástico", "increíble"],
        confianza_grounding=0.78,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "entusiasmo",
            "valencia": "positiva",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_QUE_MAL",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["qué mal", "qué lástima", "qué pena"],
        confianza_grounding=0.78,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "lamento",
            "valencia": "negativa",
            "tono_recomendado": "empático",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NO_PUEDE_SER",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["no puede ser", "imposible", "no me lo creo"],
        confianza_grounding=0.75,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "incredulidad",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EN_SERIO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["en serio", "de verdad", "¿en serio?"],
        confianza_grounding=0.78,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "sorpresa",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_QUE_SUERTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["qué suerte", "qué afortunado", "qué buena suerte"],
        confianza_grounding=0.75,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "felicitacion",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_QUE_RARO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["qué raro", "qué extraño", "qué curioso"],
        confianza_grounding=0.75,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "extrañeza",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ME_ALEGRO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["me alegro", "me da gusto", "qué bueno"],
        confianza_grounding=0.78,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "alegria",
            "valencia": "positiva",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LO_SIENTO_MUCHO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["lo siento mucho", "cuánto lo siento", "mis condolencias"],
        confianza_grounding=0.78,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "condolencia",
            "tono_recomendado": "solemne",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_QUE_SORPRESA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["qué sorpresa", "vaya sorpresa", "no me lo esperaba"],
        confianza_grounding=0.75,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "sorpresa",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_QUE_ALIVIO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["qué alivio", "menos mal", "por suerte"],
        confianza_grounding=0.78,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "alivio",
            "valencia": "positiva",
        },
    ))
    
    # ══════════ CORTESÍA ════════════════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CON_GUSTO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["con gusto", "con mucho gusto", "encantado"],
        confianza_grounding=0.80,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "aceptacion_cortes",
            "tono_recomendado": "amable",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NO_HAY_PROBLEMA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["no hay problema", "ningún problema", "no te preocupes"],
        confianza_grounding=0.80,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "tranquilizador",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PERDON_INTERRUPCION",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["perdona que interrumpa", "disculpa la molestia", "siento molestar"],
        confianza_grounding=0.75,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "disculpa_previa",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SI_ME_PERMITES",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["si me permites", "si puedo opinar", "si me dejas añadir"],
        confianza_grounding=0.72,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "solicitud_permiso",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MUCHAS_GRACIAS",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["muchas gracias", "muchísimas gracias", "mil gracias"],
        confianza_grounding=0.82,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "agradecimiento_enfatico",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SERIA_TAN_AMABLE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["sería tan amable", "podría por favor", "le importaría"],
        confianza_grounding=0.75,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "solicitud_formal",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_BUEN_PROVECHO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["buen provecho", "que aproveche"],
        confianza_grounding=0.72,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "deseo_bienestar",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_QUE_TE_MEJORES",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["que te mejores", "mejórate pronto", "recupérate"],
        confianza_grounding=0.75,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "deseo_salud",
            "tono_recomendado": "cariñoso",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_BUENA_SUERTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["buena suerte", "mucha suerte", "éxitos"],
        confianza_grounding=0.78,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "deseo_exito",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CUÍDATE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["cuídate", "cuídate mucho", "cuida de ti"],
        confianza_grounding=0.78,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "despedida_afectuosa",
        },
    ))
    
    # ══════════ OPINIÓN ═════════════════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EN_MI_OPINION",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["en mi opinión", "a mi parecer", "según yo"],
        confianza_grounding=0.78,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "introduccion_opinion",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DESDE_MI_PUNTO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["desde mi punto de vista", "a mi modo de ver", "según mi perspectiva"],
        confianza_grounding=0.75,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "introduccion_opinion",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SI_NO_ME_EQUIVOCO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["si no me equivoco", "si mal no recuerdo", "si la memoria no me falla"],
        confianza_grounding=0.72,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "afirmacion_tentativa",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_POR_LO_QUE_SE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["por lo que sé", "que yo sepa", "hasta donde sé"],
        confianza_grounding=0.75,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "conocimiento_limitado",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LA_VERDAD_ES",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["la verdad es que", "sinceramente", "honestamente"],
        confianza_grounding=0.78,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "sinceridad",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ME_PREGUNTO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["me pregunto", "me da curiosidad", "quisiera saber"],
        confianza_grounding=0.75,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "curiosidad",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TENGO_ENTENDIDO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["tengo entendido que", "según tengo entendido", "por lo que entiendo"],
        confianza_grounding=0.72,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "conocimiento_indirecto",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ME_DA_LA_IMPRESION",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["me da la impresión", "tengo la sensación", "parece que"],
        confianza_grounding=0.72,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "impresion",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DIRIA_QUE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["diría que", "yo diría que", "se podría decir que"],
        confianza_grounding=0.75,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "opinion_cautelosa",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LO_CIERTO_ES",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["lo cierto es", "el hecho es", "la realidad es"],
        confianza_grounding=0.78,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "afirmacion_factual",
        },
    ))
    
    # ══════════ TRANSICIÓN ══════════════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_POR_CIERTO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["por cierto", "a propósito", "hablando de"],
        confianza_grounding=0.78,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "cambio_tema",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EN_CUANTO_A",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["en cuanto a", "respecto a", "con respecto a"],
        confianza_grounding=0.78,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "enfoque_tema",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_VOLVIENDO_AL_TEMA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["volviendo al tema", "retomando", "como decía"],
        confianza_grounding=0.75,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "retorno_tema",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DICHO_ESTO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["dicho esto", "habiendo dicho esto", "con esto en mente"],
        confianza_grounding=0.75,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "transicion",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EN_RESUMEN",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["en resumen", "resumiendo", "para resumir"],
        confianza_grounding=0.78,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "sintesis",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EN_OTRAS_PALABRAS",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["en otras palabras", "o sea", "es decir"],
        confianza_grounding=0.78,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "reformulacion",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DE_HECHO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["de hecho", "en realidad", "en efecto"],
        confianza_grounding=0.80,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "enfasis",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_POR_OTRA_PARTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["por otra parte", "por otro lado", "en cambio"],
        confianza_grounding=0.78,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "contraste",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_A_PROPOSITO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["a propósito", "apropósito de", "ya que mencionas"],
        confianza_grounding=0.75,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "conexion_tema",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PARA_TERMINAR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["para terminar", "para concluir", "finalmente"],
        confianza_grounding=0.78,
        propiedades={
            "es_expresion": True,
            "tipo_expresion": "cierre",
        },
    ))
    
    return conceptos


if __name__ == '__main__':
    conceptos = obtener_conceptos_expresiones_comunes()
    grounding_prom = sum(c.confianza_grounding for c in conceptos) / len(conceptos)
    print(f"✅ Expresiones Comunes: {len(conceptos)} conceptos")
    print(f"   Grounding promedio: {grounding_prom:.2f}")