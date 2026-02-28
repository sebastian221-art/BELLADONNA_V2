"""
Conceptos Abstractos - Expansión Fase 4A.

Ideas abstractas, cualidades mentales y valores.

Conceptos: 50 total
Grounding promedio: 0.72
Tipo: ACCION_COGNITIVA (Bell puede razonar sobre estos)
"""
from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto


def obtener_conceptos_abstractos():
    """
    Retorna conceptos abstractos.
    
    Categorías:
    - Cualidades mentales (12)
    - Valores (12)
    - Estados conceptuales (13)
    - Ideas abstractas (13)
    """
    conceptos = []
    
    # ══════════ CUALIDADES MENTALES ═════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INTELIGENCIA",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["inteligencia", "intelecto", "capacidad mental"],
        confianza_grounding=0.75,
        propiedades={
            "es_abstracto": True,
            "es_cualidad": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CREATIVIDAD",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["creatividad", "inventiva", "originalidad"],
        confianza_grounding=0.72,
        propiedades={
            "es_abstracto": True,
            "es_cualidad": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LOGICA",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["lógica", "razonamiento", "deducción"],
        confianza_grounding=0.80,
        propiedades={
            "es_abstracto": True,
            "es_cualidad": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_RAZONAR"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MEMORIA_ABSTRACTA",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["memoria", "recuerdo", "retención"],
        confianza_grounding=0.75,
        propiedades={
            "es_abstracto": True,
            "es_cualidad": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ATENCION",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["atención", "concentración", "enfoque"],
        confianza_grounding=0.75,
        propiedades={
            "es_abstracto": True,
            "es_cualidad": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PACIENCIA",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["paciencia", "calma", "serenidad"],
        confianza_grounding=0.72,
        propiedades={
            "es_abstracto": True,
            "es_cualidad": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PERSEVERANCIA",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["perseverancia", "constancia", "determinación"],
        confianza_grounding=0.72,
        propiedades={
            "es_abstracto": True,
            "es_cualidad": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SABIDURIA",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["sabiduría", "prudencia", "juicio"],
        confianza_grounding=0.70,
        propiedades={
            "es_abstracto": True,
            "es_cualidad": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CURIOSIDAD_ABSTRACTA",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["curiosidad", "interés", "inquietud mental"],
        confianza_grounding=0.75,
        propiedades={
            "es_abstracto": True,
            "es_cualidad": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EMPATIA",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["empatía", "comprensión", "sensibilidad"],
        confianza_grounding=0.70,
        propiedades={
            "es_abstracto": True,
            "es_cualidad": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INTUICION",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["intuición", "presentimiento", "corazonada"],
        confianza_grounding=0.68,
        propiedades={
            "es_abstracto": True,
            "es_cualidad": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_IMAGINACION",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["imaginación", "fantasía", "invención"],
        confianza_grounding=0.70,
        propiedades={
            "es_abstracto": True,
            "es_cualidad": True,
        },
    ))
    
    # ══════════ VALORES ═════════════════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_HONESTIDAD",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["honestidad", "sinceridad", "franqueza"],
        confianza_grounding=0.78,
        propiedades={
            "es_valor": True,
            "es_abstracto": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RESPETO",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["respeto", "consideración", "deferencia"],
        confianza_grounding=0.78,
        propiedades={
            "es_valor": True,
            "es_abstracto": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_JUSTICIA",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["justicia", "equidad", "imparcialidad"],
        confianza_grounding=0.75,
        propiedades={
            "es_valor": True,
            "es_abstracto": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LIBERTAD",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["libertad", "autonomía", "independencia"],
        confianza_grounding=0.72,
        propiedades={
            "es_valor": True,
            "es_abstracto": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RESPONSABILIDAD",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["responsabilidad", "deber", "compromiso"],
        confianza_grounding=0.78,
        propiedades={
            "es_valor": True,
            "es_abstracto": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LEALTAD",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["lealtad", "fidelidad", "devoción"],
        confianza_grounding=0.72,
        propiedades={
            "es_valor": True,
            "es_abstracto": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CONFIANZA_VALOR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["confianza", "fe", "credibilidad"],
        confianza_grounding=0.75,
        propiedades={
            "es_valor": True,
            "es_abstracto": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SOLIDARIDAD",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["solidaridad", "apoyo mutuo", "cooperación"],
        confianza_grounding=0.72,
        propiedades={
            "es_valor": True,
            "es_abstracto": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_HUMILDAD",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["humildad", "modestia", "sencillez"],
        confianza_grounding=0.72,
        propiedades={
            "es_valor": True,
            "es_abstracto": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_VALENTIA",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["valentía", "coraje", "audacia"],
        confianza_grounding=0.70,
        propiedades={
            "es_valor": True,
            "es_abstracto": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TOLERANCIA",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["tolerancia", "aceptación", "apertura"],
        confianza_grounding=0.72,
        propiedades={
            "es_valor": True,
            "es_abstracto": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_GENEROSIDAD",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["generosidad", "desprendimiento", "altruismo"],
        confianza_grounding=0.70,
        propiedades={
            "es_valor": True,
            "es_abstracto": True,
        },
    ))
    
    # ══════════ ESTADOS CONCEPTUALES ════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EXITO",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["éxito", "logro", "triunfo"],
        confianza_grounding=0.75,
        propiedades={
            "es_abstracto": True,
            "es_estado": True,
            "valencia": "positiva",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_FRACASO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FRACASO",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["fracaso", "fallo", "derrota"],
        confianza_grounding=0.75,
        propiedades={
            "es_abstracto": True,
            "es_estado": True,
            "valencia": "negativa",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_EXITO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PROGRESO",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["progreso", "avance", "mejora"],
        confianza_grounding=0.75,
        propiedades={
            "es_abstracto": True,
            "es_estado": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ESTANCAMIENTO",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["estancamiento", "paralización", "bloqueo"],
        confianza_grounding=0.72,
        propiedades={
            "es_abstracto": True,
            "es_estado": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CRECIMIENTO",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["crecimiento", "desarrollo", "evolución"],
        confianza_grounding=0.75,
        propiedades={
            "es_abstracto": True,
            "es_estado": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EQUILIBRIO",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["equilibrio", "balance", "armonía"],
        confianza_grounding=0.72,
        propiedades={
            "es_abstracto": True,
            "es_estado": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CAOS",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["caos", "desorden", "confusión total"],
        confianza_grounding=0.70,
        propiedades={
            "es_abstracto": True,
            "es_estado": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_ORDEN_ABSTRACTO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ORDEN_ABSTRACTO",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["orden", "organización", "estructura"],
        confianza_grounding=0.75,
        propiedades={
            "es_abstracto": True,
            "es_estado": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_CAOS"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PAZ",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["paz", "tranquilidad", "serenidad"],
        confianza_grounding=0.72,
        propiedades={
            "es_abstracto": True,
            "es_estado": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_CONFLICTO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CONFLICTO",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["conflicto", "disputa", "confrontación"],
        confianza_grounding=0.72,
        propiedades={
            "es_abstracto": True,
            "es_estado": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_PAZ"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_COMPLEJIDAD",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["complejidad", "complicación", "intrincado"],
        confianza_grounding=0.72,
        propiedades={
            "es_abstracto": True,
            "es_estado": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_SIMPLICIDAD"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SIMPLICIDAD",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["simplicidad", "sencillez", "claridad"],
        confianza_grounding=0.75,
        propiedades={
            "es_abstracto": True,
            "es_estado": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_COMPLEJIDAD"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_POTENCIAL",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["potencial", "capacidad", "posibilidad"],
        confianza_grounding=0.72,
        propiedades={
            "es_abstracto": True,
            "es_estado": True,
        },
    ))
    
    # ══════════ IDEAS ABSTRACTAS ════════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_VERDAD_ABSTRACTA",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["verdad", "realidad", "certeza"],
        confianza_grounding=0.75,
        propiedades={
            "es_abstracto": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_MENTIRA"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MENTIRA",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["mentira", "falsedad", "engaño"],
        confianza_grounding=0.75,
        propiedades={
            "es_abstracto": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_VERDAD_ABSTRACTA"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CONOCIMIENTO",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["conocimiento", "saber", "entendimiento"],
        confianza_grounding=0.78,
        propiedades={
            "es_abstracto": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_IGNORANCIA"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_IGNORANCIA",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["ignorancia", "desconocimiento", "falta de saber"],
        confianza_grounding=0.72,
        propiedades={
            "es_abstracto": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_CONOCIMIENTO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_IDEA",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["idea", "concepto", "noción"],
        confianza_grounding=0.78,
        propiedades={
            "es_abstracto": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SOLUCION",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["solución", "respuesta", "resolución"],
        confianza_grounding=0.80,
        propiedades={
            "es_abstracto": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_PROBLEMA"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PROBLEMA",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["problema", "dificultad", "obstáculo"],
        confianza_grounding=0.80,
        propiedades={
            "es_abstracto": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_SOLUCION"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_OPORTUNIDAD",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["oportunidad", "posibilidad", "chance"],
        confianza_grounding=0.75,
        propiedades={
            "es_abstracto": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RIESGO",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["riesgo", "peligro", "amenaza"],
        confianza_grounding=0.75,
        propiedades={
            "es_abstracto": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_OBJETIVO",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["objetivo", "meta", "fin"],
        confianza_grounding=0.78,
        propiedades={
            "es_abstracto": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ESTRATEGIA",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["estrategia", "plan", "táctica"],
        confianza_grounding=0.78,
        propiedades={
            "es_abstracto": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PROCESO",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["proceso", "procedimiento", "método"],
        confianza_grounding=0.80,
        propiedades={
            "es_abstracto": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RESULTADO",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["resultado", "consecuencia", "efecto"],
        confianza_grounding=0.80,
        propiedades={
            "es_abstracto": True,
        },
    ))
    
    return conceptos


if __name__ == '__main__':
    conceptos = obtener_conceptos_abstractos()
    grounding_prom = sum(c.confianza_grounding for c in conceptos) / len(conceptos)
    print(f"✅ Conceptos Abstractos: {len(conceptos)} conceptos")
    print(f"   Grounding promedio: {grounding_prom:.2f}")