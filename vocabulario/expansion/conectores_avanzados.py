"""
Conectores Avanzados - Expansión Fase 4A.

Marcadores de discurso, conectores lógicos y estructuradores.

Conceptos: 40 total
Grounding promedio: 0.75
Tipo: PALABRA_CONVERSACION
"""
from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto


def obtener_conceptos_conectores_avanzados():
    """
    Retorna conectores avanzados del discurso.
    
    Categorías:
    - Causales (8)
    - Consecutivos (8)
    - Condicionales (8)
    - Concesivos (8)
    - Organizadores (8)
    """
    conceptos = []
    
    # ══════════ CAUSALES ════════════════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DEBIDO_A",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["debido a", "debido a que", "a causa de"],
        confianza_grounding=0.78,
        propiedades={
            "es_conector": True,
            "tipo_logico": "causal",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_GRACIAS_A",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["gracias a", "gracias a que"],
        confianza_grounding=0.78,
        propiedades={
            "es_conector": True,
            "tipo_logico": "causal_positivo",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PUESTO_QUE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["puesto que", "dado que", "ya que"],
        confianza_grounding=0.78,
        propiedades={
            "es_conector": True,
            "tipo_logico": "causal",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_POR_ESO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["por eso", "por esto", "por tal razón"],
        confianza_grounding=0.80,
        propiedades={
            "es_conector": True,
            "tipo_logico": "causal_consecutivo",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_COMO_RESULTADO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["como resultado", "como consecuencia", "en consecuencia"],
        confianza_grounding=0.78,
        propiedades={
            "es_conector": True,
            "tipo_logico": "consecutivo",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_POR_CULPA_DE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["por culpa de", "a causa de"],
        confianza_grounding=0.75,
        propiedades={
            "es_conector": True,
            "tipo_logico": "causal_negativo",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RAZON_ES",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["la razón es", "el motivo es", "esto se debe a"],
        confianza_grounding=0.78,
        propiedades={
            "es_conector": True,
            "tipo_logico": "explicativo",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_POR_TANTO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["por tanto", "por ende", "así pues"],
        confianza_grounding=0.78,
        propiedades={
            "es_conector": True,
            "tipo_logico": "consecutivo",
        },
    ))
    
    # ══════════ CONSECUTIVOS ════════════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DE_AHI_QUE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["de ahí que", "de modo que", "de manera que"],
        confianza_grounding=0.75,
        propiedades={
            "es_conector": True,
            "tipo_logico": "consecutivo",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_POR_CONSIGUIENTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["por consiguiente", "consecuentemente"],
        confianza_grounding=0.75,
        propiedades={
            "es_conector": True,
            "tipo_logico": "consecutivo",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ASI_QUE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["así que", "conque", "total que"],
        confianza_grounding=0.80,
        propiedades={
            "es_conector": True,
            "tipo_logico": "consecutivo_coloquial",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DE_FORMA_QUE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["de forma que", "de tal forma que", "de tal manera que"],
        confianza_grounding=0.75,
        propiedades={
            "es_conector": True,
            "tipo_logico": "consecutivo",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RESULTA_QUE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["resulta que", "sucede que", "pasa que"],
        confianza_grounding=0.78,
        propiedades={
            "es_conector": True,
            "tipo_logico": "explicativo",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TANTO_QUE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["tanto que", "tan... que", "hasta tal punto que"],
        confianza_grounding=0.75,
        propiedades={
            "es_conector": True,
            "tipo_logico": "consecutivo_intensivo",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LO_CUAL",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["lo cual", "lo que", "cosa que"],
        confianza_grounding=0.78,
        propiedades={
            "es_conector": True,
            "tipo_logico": "relativo",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ESTO_SIGNIFICA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["esto significa", "esto implica", "esto quiere decir"],
        confianza_grounding=0.80,
        propiedades={
            "es_conector": True,
            "tipo_logico": "explicativo",
        },
    ))
    
    # ══════════ CONDICIONALES ═══════════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SI_CONDICIONAL",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["si", "en caso de que", "siempre que"],
        confianza_grounding=0.82,
        propiedades={
            "es_conector": True,
            "tipo_logico": "condicional",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_A_MENOS_QUE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["a menos que", "a no ser que", "salvo que"],
        confianza_grounding=0.78,
        propiedades={
            "es_conector": True,
            "tipo_logico": "condicional_negativo",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CON_TAL_DE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["con tal de que", "siempre y cuando", "a condición de que"],
        confianza_grounding=0.75,
        propiedades={
            "es_conector": True,
            "tipo_logico": "condicional",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EN_CASO_DE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["en caso de", "de ser así", "si es el caso"],
        confianza_grounding=0.78,
        propiedades={
            "es_conector": True,
            "tipo_logico": "condicional",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SUPONIENDO_QUE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["suponiendo que", "asumiendo que", "imaginando que"],
        confianza_grounding=0.75,
        propiedades={
            "es_conector": True,
            "tipo_logico": "condicional_hipotetico",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DE_LO_CONTRARIO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["de lo contrario", "si no", "en caso contrario"],
        confianza_grounding=0.78,
        propiedades={
            "es_conector": True,
            "tipo_logico": "condicional_negativo",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MIENTRAS_COND",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["mientras", "mientras que", "en tanto que"],
        confianza_grounding=0.78,
        propiedades={
            "es_conector": True,
            "tipo_logico": "condicional_temporal",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DADO_CASO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["dado el caso", "llegado el caso", "si llegara a"],
        confianza_grounding=0.72,
        propiedades={
            "es_conector": True,
            "tipo_logico": "condicional_hipotetico",
        },
    ))
    
    # ══════════ CONCESIVOS ══════════════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_AUNQUE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["aunque", "a pesar de que", "pese a que"],
        confianza_grounding=0.80,
        propiedades={
            "es_conector": True,
            "tipo_logico": "concesivo",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_AUN_ASI",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["aun así", "aún así", "con todo"],
        confianza_grounding=0.78,
        propiedades={
            "es_conector": True,
            "tipo_logico": "concesivo",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NO_OBSTANTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["no obstante", "sin embargo", "con todo"],
        confianza_grounding=0.78,
        propiedades={
            "es_conector": True,
            "tipo_logico": "concesivo",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_A_PESAR_DE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["a pesar de", "pese a", "a despecho de"],
        confianza_grounding=0.78,
        propiedades={
            "es_conector": True,
            "tipo_logico": "concesivo",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_POR_MAS_QUE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["por más que", "por mucho que", "por muy... que"],
        confianza_grounding=0.75,
        propiedades={
            "es_conector": True,
            "tipo_logico": "concesivo_intensivo",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SI_BIEN",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["si bien", "bien que", "aun cuando"],
        confianza_grounding=0.75,
        propiedades={
            "es_conector": True,
            "tipo_logico": "concesivo",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DE_TODAS_FORMAS",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["de todas formas", "de todos modos", "en cualquier caso"],
        confianza_grounding=0.78,
        propiedades={
            "es_conector": True,
            "tipo_logico": "concesivo",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CON_TODO_Y_ESO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["con todo y eso", "así y todo", "y aun así"],
        confianza_grounding=0.75,
        propiedades={
            "es_conector": True,
            "tipo_logico": "concesivo_coloquial",
        },
    ))
    
    # ══════════ ORGANIZADORES ═══════════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PARA_EMPEZAR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["para empezar", "en primer lugar", "antes que nada"],
        confianza_grounding=0.80,
        propiedades={
            "es_conector": True,
            "tipo_logico": "organizador_inicio",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_A_CONTINUACION",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["a continuación", "seguidamente", "después de esto"],
        confianza_grounding=0.78,
        propiedades={
            "es_conector": True,
            "tipo_logico": "organizador_secuencia",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_POR_ULTIMO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["por último", "finalmente", "para finalizar"],
        confianza_grounding=0.80,
        propiedades={
            "es_conector": True,
            "tipo_logico": "organizador_cierre",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EN_PRIMER_LUGAR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["en primer lugar", "primeramente", "en principio"],
        confianza_grounding=0.78,
        propiedades={
            "es_conector": True,
            "tipo_logico": "organizador_orden",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EN_SEGUNDO_LUGAR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["en segundo lugar", "segundo", "además de esto"],
        confianza_grounding=0.78,
        propiedades={
            "es_conector": True,
            "tipo_logico": "organizador_orden",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_POR_UN_LADO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["por un lado", "de un lado", "por una parte"],
        confianza_grounding=0.78,
        propiedades={
            "es_conector": True,
            "tipo_logico": "organizador_contraste",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_POR_OTRO_LADO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["por otro lado", "por otra parte", "de otro lado"],
        confianza_grounding=0.78,
        propiedades={
            "es_conector": True,
            "tipo_logico": "organizador_contraste",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EN_DEFINITIVA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["en definitiva", "en suma", "al fin y al cabo"],
        confianza_grounding=0.78,
        propiedades={
            "es_conector": True,
            "tipo_logico": "organizador_conclusion",
        },
    ))
    
    return conceptos


if __name__ == '__main__':
    conceptos = obtener_conceptos_conectores_avanzados()
    grounding_prom = sum(c.confianza_grounding for c in conceptos) / len(conceptos)
    print(f"✅ Conectores Avanzados: {len(conceptos)} conceptos")
    print(f"   Grounding promedio: {grounding_prom:.2f}")