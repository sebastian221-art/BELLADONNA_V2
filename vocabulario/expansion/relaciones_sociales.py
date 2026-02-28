"""
Relaciones Sociales - Expansión Fase 4A.

Vocabulario para entender contexto social en conversaciones.

Conceptos: 50 total
Grounding promedio: 0.70
Tipo: PALABRA_CONVERSACION
"""
from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto


def obtener_conceptos_relaciones_sociales():
    """
    Retorna conceptos de relaciones sociales.
    
    Categorías:
    - Familia (14 conceptos)
    - Trabajo (12 conceptos)
    - Relaciones personales (10 conceptos)
    - Pronombres (8 conceptos)
    - Grupos (6 conceptos)
    """
    conceptos = []
    
    # ══════════ FAMILIA ═════════════════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MADRE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["madre", "mamá", "mom", "mami", "ma"],
        confianza_grounding=0.75,
        propiedades={
            "es_relacion": True,
            "es_familia": True,
            "tono_recomendado": "respetuoso",
        },
        relaciones={
            "tipo_de": {"FAMILIA"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PADRE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["padre", "papá", "dad", "papi", "pa"],
        confianza_grounding=0.75,
        propiedades={
            "es_relacion": True,
            "es_familia": True,
            "tono_recomendado": "respetuoso",
        },
        relaciones={
            "tipo_de": {"FAMILIA"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_HIJO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["hijo", "son", "niño"],
        confianza_grounding=0.72,
        propiedades={
            "es_relacion": True,
            "es_familia": True,
        },
        relaciones={
            "tipo_de": {"FAMILIA"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_HIJA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["hija", "daughter", "niña"],
        confianza_grounding=0.72,
        propiedades={
            "es_relacion": True,
            "es_familia": True,
        },
        relaciones={
            "tipo_de": {"FAMILIA"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_HERMANO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["hermano", "brother"],
        confianza_grounding=0.72,
        propiedades={
            "es_relacion": True,
            "es_familia": True,
        },
        relaciones={
            "tipo_de": {"FAMILIA"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_HERMANA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["hermana", "sister"],
        confianza_grounding=0.72,
        propiedades={
            "es_relacion": True,
            "es_familia": True,
        },
        relaciones={
            "tipo_de": {"FAMILIA"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ABUELO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["abuelo", "grandfather", "abuelito"],
        confianza_grounding=0.70,
        propiedades={
            "es_relacion": True,
            "es_familia": True,
        },
        relaciones={
            "tipo_de": {"FAMILIA"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ABUELA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["abuela", "grandmother", "abuelita"],
        confianza_grounding=0.70,
        propiedades={
            "es_relacion": True,
            "es_familia": True,
        },
        relaciones={
            "tipo_de": {"FAMILIA"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TIO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["tío", "uncle"],
        confianza_grounding=0.68,
        propiedades={
            "es_relacion": True,
            "es_familia": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TIA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["tía", "aunt"],
        confianza_grounding=0.68,
        propiedades={
            "es_relacion": True,
            "es_familia": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PRIMO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["primo", "prima", "cousin"],
        confianza_grounding=0.68,
        propiedades={
            "es_relacion": True,
            "es_familia": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ESPOSO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["esposo", "husband", "marido"],
        confianza_grounding=0.72,
        propiedades={
            "es_relacion": True,
            "es_familia": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ESPOSA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["esposa", "wife", "mujer"],
        confianza_grounding=0.72,
        propiedades={
            "es_relacion": True,
            "es_familia": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FAMILIA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["familia", "family", "familiares", "parientes"],
        confianza_grounding=0.75,
        propiedades={
            "es_relacion": True,
            "es_grupo": True,
        },
    ))
    
    # ══════════ TRABAJO ═════════════════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_JEFE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["jefe", "boss", "manager", "supervisor"],
        confianza_grounding=0.72,
        propiedades={
            "es_relacion": True,
            "es_trabajo": True,
            "tono_recomendado": "profesional",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EMPLEADO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["empleado", "employee", "trabajador"],
        confianza_grounding=0.70,
        propiedades={
            "es_relacion": True,
            "es_trabajo": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_COLEGA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["colega", "colleague", "compañero de trabajo", "coworker"],
        confianza_grounding=0.72,
        propiedades={
            "es_relacion": True,
            "es_trabajo": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CLIENTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["cliente", "client", "customer"],
        confianza_grounding=0.75,
        propiedades={
            "es_relacion": True,
            "es_trabajo": True,
            "tono_recomendado": "profesional",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PROFESOR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["profesor", "teacher", "maestro", "docente"],
        confianza_grounding=0.75,
        propiedades={
            "es_relacion": True,
            "es_trabajo": True,
            "tono_recomendado": "respetuoso",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ESTUDIANTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["estudiante", "student", "alumno", "aprendiz"],
        confianza_grounding=0.75,
        propiedades={
            "es_relacion": True,
            "tono_recomendado": "didáctico",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DOCTOR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["doctor", "médico", "dr"],
        confianza_grounding=0.72,
        propiedades={
            "es_relacion": True,
            "es_trabajo": True,
            "tono_recomendado": "profesional",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INGENIERO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["ingeniero", "engineer", "ing"],
        confianza_grounding=0.72,
        propiedades={
            "es_relacion": True,
            "es_trabajo": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DESARROLLADOR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["desarrollador", "developer", "programador", "dev"],
        confianza_grounding=0.78,
        propiedades={
            "es_relacion": True,
            "es_trabajo": True,
            "tono_recomendado": "técnico",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EQUIPO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["equipo", "team", "grupo de trabajo"],
        confianza_grounding=0.75,
        propiedades={
            "es_relacion": True,
            "es_grupo": True,
            "es_trabajo": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EMPRESA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["empresa", "company", "compañía", "negocio"],
        confianza_grounding=0.75,
        propiedades={
            "es_organizacion": True,
            "es_trabajo": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_USUARIO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["usuario", "user"],
        confianza_grounding=0.80,
        propiedades={
            "es_relacion": True,
            "es_digital": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_CLIENTE"},
        },
    ))
    
    # ══════════ RELACIONES PERSONALES ═══════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_AMIGO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["amigo", "amiga", "friend"],
        confianza_grounding=0.75,
        propiedades={
            "es_relacion": True,
            "es_personal": True,
            "tono_recomendado": "amistoso",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MEJOR_AMIGO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["mejor amigo", "mejor amiga", "best friend", "bff"],
        confianza_grounding=0.72,
        propiedades={
            "es_relacion": True,
            "es_personal": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CONOCIDO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["conocido", "conocida", "acquaintance"],
        confianza_grounding=0.68,
        propiedades={
            "es_relacion": True,
            "es_personal": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_VECINO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["vecino", "vecina", "neighbor"],
        confianza_grounding=0.68,
        propiedades={
            "es_relacion": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NOVIO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["novio", "boyfriend", "pareja"],
        confianza_grounding=0.70,
        propiedades={
            "es_relacion": True,
            "es_personal": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NOVIA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["novia", "girlfriend"],
        confianza_grounding=0.70,
        propiedades={
            "es_relacion": True,
            "es_personal": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_COMPANERO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["compañero", "compañera", "partner", "mate"],
        confianza_grounding=0.72,
        propiedades={
            "es_relacion": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EXTRANO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["extraño", "stranger", "desconocido"],
        confianza_grounding=0.68,
        propiedades={
            "es_relacion": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PERSONA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["persona", "person", "individuo", "gente"],
        confianza_grounding=0.75,
        propiedades={
            "es_entidad": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_GENTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["gente", "people", "personas"],
        confianza_grounding=0.72,
        propiedades={
            "es_grupo": True,
        },
    ))
    
    # ══════════ PRONOMBRES ══════════════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_YO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["yo", "I", "me", "mi"],
        confianza_grounding=0.80,
        propiedades={
            "es_pronombre": True,
            "persona": "primera",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TU",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["tú", "you", "te", "ti", "usted"],
        confianza_grounding=0.80,
        propiedades={
            "es_pronombre": True,
            "persona": "segunda",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EL",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["él", "he", "him"],
        confianza_grounding=0.75,
        propiedades={
            "es_pronombre": True,
            "persona": "tercera",
            "genero": "masculino",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ELLA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["ella", "she", "her"],
        confianza_grounding=0.75,
        propiedades={
            "es_pronombre": True,
            "persona": "tercera",
            "genero": "femenino",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NOSOTROS",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["nosotros", "nosotras", "we", "nos"],
        confianza_grounding=0.75,
        propiedades={
            "es_pronombre": True,
            "persona": "primera",
            "numero": "plural",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ELLOS",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["ellos", "ellas", "they", "them"],
        confianza_grounding=0.75,
        propiedades={
            "es_pronombre": True,
            "persona": "tercera",
            "numero": "plural",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ALGUIEN",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["alguien", "someone", "somebody"],
        confianza_grounding=0.72,
        propiedades={
            "es_pronombre": True,
            "es_indefinido": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NADIE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["nadie", "nobody", "no one"],
        confianza_grounding=0.72,
        propiedades={
            "es_pronombre": True,
            "es_negativo": True,
        },
    ))
    
    # ══════════ GRUPOS ══════════════════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_GRUPO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["grupo", "group", "conjunto"],
        confianza_grounding=0.72,
        propiedades={
            "es_grupo": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_COMUNIDAD",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["comunidad", "community"],
        confianza_grounding=0.70,
        propiedades={
            "es_grupo": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SOCIEDAD",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["sociedad", "society"],
        confianza_grounding=0.68,
        propiedades={
            "es_grupo": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ORGANIZACION",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["organización", "organization"],
        confianza_grounding=0.70,
        propiedades={
            "es_organizacion": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MIEMBRO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["miembro", "member", "integrante"],
        confianza_grounding=0.70,
        propiedades={
            "es_relacion": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PUBLICO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["público", "audience", "espectadores"],
        confianza_grounding=0.68,
        propiedades={
            "es_grupo": True,
        },
    ))
    
    return conceptos


if __name__ == '__main__':
    conceptos = obtener_conceptos_relaciones_sociales()
    grounding_prom = sum(c.confianza_grounding for c in conceptos) / len(conceptos)
    print(f"✅ Relaciones Sociales: {len(conceptos)} conceptos")
    print(f"   Grounding promedio: {grounding_prom:.2f}")