"""
Profesiones y Trabajo - Expansión Fase 4A.

Términos laborales, profesiones y contexto de trabajo.

Conceptos: 45 total
Grounding promedio: 0.75
Tipo: PALABRA_CONVERSACION / ACCION_COGNITIVA
"""
from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto


def obtener_conceptos_profesiones_trabajo():
    """
    Retorna conceptos de profesiones y trabajo.
    
    Categorías:
    - Profesiones comunes (15)
    - Acciones laborales (15)
    - Contexto laboral (15)
    """
    conceptos = []
    
    # ══════════ PROFESIONES COMUNES ═════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PROGRAMADOR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["programador", "desarrollador", "developer", "dev"],
        confianza_grounding=0.80,
        propiedades={
            "es_profesion": True,
            "campo": "tecnologia",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INGENIERO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["ingeniero", "ingeniera", "engineer"],
        confianza_grounding=0.78,
        propiedades={
            "es_profesion": True,
            "campo": "tecnico",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DISEÑADOR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["diseñador", "diseñadora", "designer"],
        confianza_grounding=0.78,
        propiedades={
            "es_profesion": True,
            "campo": "creativo",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MEDICO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["médico", "doctor", "doctora"],
        confianza_grounding=0.78,
        propiedades={
            "es_profesion": True,
            "campo": "salud",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ABOGADO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["abogado", "abogada", "licenciado en derecho"],
        confianza_grounding=0.75,
        propiedades={
            "es_profesion": True,
            "campo": "legal",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PROFESOR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["profesor", "profesora", "maestro", "docente"],
        confianza_grounding=0.78,
        propiedades={
            "es_profesion": True,
            "campo": "educacion",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ESTUDIANTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["estudiante", "alumno", "alumna"],
        confianza_grounding=0.80,
        propiedades={
            "es_rol": True,
            "campo": "educacion",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_GERENTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["gerente", "manager", "director", "jefe"],
        confianza_grounding=0.78,
        propiedades={
            "es_profesion": True,
            "es_liderazgo": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CONTADOR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["contador", "contadora", "contable"],
        confianza_grounding=0.75,
        propiedades={
            "es_profesion": True,
            "campo": "finanzas",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_VENDEDOR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["vendedor", "vendedora", "comercial"],
        confianza_grounding=0.75,
        propiedades={
            "es_profesion": True,
            "campo": "ventas",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ESCRITOR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["escritor", "escritora", "autor", "redactor"],
        confianza_grounding=0.75,
        propiedades={
            "es_profesion": True,
            "campo": "creativo",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ARQUITECTO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["arquitecto", "arquitecta"],
        confianza_grounding=0.75,
        propiedades={
            "es_profesion": True,
            "campo": "construccion",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CIENTIFICO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["científico", "científica", "investigador"],
        confianza_grounding=0.75,
        propiedades={
            "es_profesion": True,
            "campo": "ciencia",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EMPRENDEDOR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["emprendedor", "emprendedora", "entrepreneur"],
        confianza_grounding=0.75,
        propiedades={
            "es_profesion": True,
            "campo": "negocios",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FREELANCER",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["freelancer", "freelance", "independiente", "autónomo"],
        confianza_grounding=0.78,
        propiedades={
            "es_modalidad": True,
            "campo": "trabajo",
        },
    ))
    
    # ══════════ ACCIONES LABORALES ══════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TRABAJAR_ACCION",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["trabajar", "laborar", "currar"],
        confianza_grounding=0.80,
        propiedades={
            "es_accion_laboral": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_REUNIRSE",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["reunirse", "juntarse", "tener reunión", "meeting"],
        confianza_grounding=0.78,
        propiedades={
            "es_accion_laboral": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PRESENTAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["presentar", "exponer", "mostrar presentación"],
        confianza_grounding=0.78,
        propiedades={
            "es_accion_laboral": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ENTREGAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["entregar", "enviar", "mandar", "submit"],
        confianza_grounding=0.80,
        propiedades={
            "es_accion_laboral": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_REVISAR_LABORAL",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["revisar", "review", "dar feedback"],
        confianza_grounding=0.80,
        propiedades={
            "es_accion_laboral": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_APROBAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["aprobar", "dar visto bueno", "autorizar"],
        confianza_grounding=0.78,
        propiedades={
            "es_accion_laboral": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RECHAZAR_LABORAL",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["rechazar", "denegar", "no aprobar"],
        confianza_grounding=0.78,
        propiedades={
            "es_accion_laboral": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DELEGAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["delegar", "asignar", "encomendar"],
        confianza_grounding=0.75,
        propiedades={
            "es_accion_laboral": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_COORDINAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["coordinar", "organizar equipo", "sincronizar"],
        confianza_grounding=0.75,
        propiedades={
            "es_accion_laboral": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NEGOCIAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["negociar", "llegar a acuerdo", "pactar"],
        confianza_grounding=0.72,
        propiedades={
            "es_accion_laboral": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CONTRATAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["contratar", "emplear", "reclutar"],
        confianza_grounding=0.75,
        propiedades={
            "es_accion_laboral": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DESPEDIR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["despedir", "echar", "prescindir de"],
        confianza_grounding=0.72,
        propiedades={
            "es_accion_laboral": True,
            "valencia": "negativa",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RENUNCIAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["renunciar", "dimitir", "dejar el trabajo"],
        confianza_grounding=0.75,
        propiedades={
            "es_accion_laboral": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ASCENDER",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["ascender", "promover", "subir de puesto"],
        confianza_grounding=0.75,
        propiedades={
            "es_accion_laboral": True,
            "valencia": "positiva",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CAPACITAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["capacitar", "entrenar", "formar"],
        confianza_grounding=0.75,
        propiedades={
            "es_accion_laboral": True,
        },
    ))
    
    # ══════════ CONTEXTO LABORAL ════════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_OFICINA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["oficina", "despacho", "lugar de trabajo"],
        confianza_grounding=0.80,
        propiedades={
            "es_lugar": True,
            "contexto": "laboral",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PROYECTO_LABORAL",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["proyecto", "project", "iniciativa"],
        confianza_grounding=0.82,
        propiedades={
            "es_concepto_laboral": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DEADLINE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["deadline", "fecha límite", "plazo", "vencimiento"],
        confianza_grounding=0.82,
        propiedades={
            "es_concepto_laboral": True,
            "genera_urgencia": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EQUIPO_TRABAJO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["equipo", "team", "grupo de trabajo"],
        confianza_grounding=0.80,
        propiedades={
            "es_concepto_laboral": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CLIENTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["cliente", "customer", "consumidor"],
        confianza_grounding=0.80,
        propiedades={
            "es_rol": True,
            "contexto": "negocios",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SUELDO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["sueldo", "salario", "paga", "remuneración"],
        confianza_grounding=0.78,
        propiedades={
            "es_concepto_laboral": True,
            "es_economico": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CONTRATO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["contrato", "acuerdo laboral"],
        confianza_grounding=0.78,
        propiedades={
            "es_concepto_laboral": True,
            "es_legal": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_VACACIONES",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["vacaciones", "días libres", "tiempo libre"],
        confianza_grounding=0.80,
        propiedades={
            "es_concepto_laboral": True,
            "valencia": "positiva",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_HORARIO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["horario", "schedule", "jornada"],
        confianza_grounding=0.80,
        propiedades={
            "es_concepto_laboral": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_HOME_OFFICE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["home office", "trabajo remoto", "teletrabajo", "trabajo desde casa"],
        confianza_grounding=0.82,
        propiedades={
            "es_modalidad": True,
            "contexto": "laboral",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_STARTUP",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["startup", "emprendimiento", "empresa emergente"],
        confianza_grounding=0.78,
        propiedades={
            "es_tipo_empresa": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EMPRESA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["empresa", "compañía", "corporación", "negocio"],
        confianza_grounding=0.80,
        propiedades={
            "es_entidad": True,
            "contexto": "laboral",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PRODUCTIVIDAD",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["productividad", "rendimiento", "eficiencia"],
        confianza_grounding=0.75,
        propiedades={
            "es_concepto_laboral": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_META_LABORAL",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["meta", "objetivo laboral", "kpi", "indicador"],
        confianza_grounding=0.78,
        propiedades={
            "es_concepto_laboral": True,
        },
    ))
    
    return conceptos


if __name__ == '__main__':
    conceptos = obtener_conceptos_profesiones_trabajo()
    grounding_prom = sum(c.confianza_grounding for c in conceptos) / len(conceptos)
    print(f"✅ Profesiones y Trabajo: {len(conceptos)} conceptos")
    print(f"   Grounding promedio: {grounding_prom:.2f}")