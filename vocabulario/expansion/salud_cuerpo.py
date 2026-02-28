"""
Salud y Cuerpo - Expansión Fase 4A.

Términos de salud, cuerpo humano y bienestar.

Conceptos: 40 total
Grounding promedio: 0.74
Tipo: PALABRA_CONVERSACION / ACCION_COGNITIVA
"""
from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto


def obtener_conceptos_salud_cuerpo():
    """
    Retorna conceptos de salud y cuerpo.
    
    Categorías:
    - Partes del cuerpo (12)
    - Estados de salud (14)
    - Acciones de bienestar (14)
    """
    conceptos = []
    
    # ══════════ PARTES DEL CUERPO ═══════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CABEZA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["cabeza", "cabecita"],
        confianza_grounding=0.78,
        propiedades={
            "es_cuerpo": True,
            "zona": "superior",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MANO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["mano", "manos", "manita"],
        confianza_grounding=0.78,
        propiedades={
            "es_cuerpo": True,
            "zona": "extremidad",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PIE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["pie", "pies", "piececito"],
        confianza_grounding=0.78,
        propiedades={
            "es_cuerpo": True,
            "zona": "extremidad",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_OJO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["ojo", "ojos", "ojito"],
        confianza_grounding=0.78,
        propiedades={
            "es_cuerpo": True,
            "es_sentido": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_OREJA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["oreja", "oído", "orejas"],
        confianza_grounding=0.75,
        propiedades={
            "es_cuerpo": True,
            "es_sentido": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CORAZON",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["corazón", "corazoncito"],
        confianza_grounding=0.78,
        propiedades={
            "es_cuerpo": True,
            "es_organo": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_BRAZO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["brazo", "brazos", "bracito"],
        confianza_grounding=0.75,
        propiedades={
            "es_cuerpo": True,
            "zona": "extremidad",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PIERNA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["pierna", "piernas"],
        confianza_grounding=0.75,
        propiedades={
            "es_cuerpo": True,
            "zona": "extremidad",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ESPALDA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["espalda", "espaldita"],
        confianza_grounding=0.75,
        propiedades={
            "es_cuerpo": True,
            "zona": "torso",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ESTOMAGO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["estómago", "panza", "barriga", "vientre"],
        confianza_grounding=0.75,
        propiedades={
            "es_cuerpo": True,
            "es_organo": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_BOCA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["boca", "boquita", "labios"],
        confianza_grounding=0.75,
        propiedades={
            "es_cuerpo": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NARIZ",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["nariz", "naricita"],
        confianza_grounding=0.75,
        propiedades={
            "es_cuerpo": True,
            "es_sentido": True,
        },
    ))
    
    # ══════════ ESTADOS DE SALUD ════════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SANO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["sano", "saludable", "en buena salud"],
        confianza_grounding=0.78,
        propiedades={
            "es_estado_salud": True,
            "valencia": "positiva",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_ENFERMO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ENFERMO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["enfermo", "malo", "indispuesto"],
        confianza_grounding=0.78,
        propiedades={
            "es_estado_salud": True,
            "valencia": "negativa",
            "tono_recomendado": "empatico",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_SANO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DOLOR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["dolor", "me duele", "dolorcito"],
        confianza_grounding=0.80,
        propiedades={
            "es_sintoma": True,
            "valencia": "negativa",
            "tono_recomendado": "empatico",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FIEBRE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["fiebre", "calentura", "temperatura alta"],
        confianza_grounding=0.75,
        propiedades={
            "es_sintoma": True,
            "valencia": "negativa",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_GRIPE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["gripe", "gripa", "resfriado", "catarro"],
        confianza_grounding=0.75,
        propiedades={
            "es_enfermedad": True,
            "valencia": "negativa",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CANSADO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["cansado", "agotado", "fatigado", "exhausto"],
        confianza_grounding=0.78,
        propiedades={
            "es_estado": True,
            "valencia": "negativa",
            "tono_recomendado": "empatico",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ENERGICO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["energético", "con energía", "activo", "vital"],
        confianza_grounding=0.75,
        propiedades={
            "es_estado": True,
            "valencia": "positiva",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MAREADO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["mareado", "con mareo", "vértigo"],
        confianza_grounding=0.72,
        propiedades={
            "es_sintoma": True,
            "valencia": "negativa",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_HERIDO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["herido", "lastimado", "lesionado"],
        confianza_grounding=0.75,
        propiedades={
            "es_estado_salud": True,
            "valencia": "negativa",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RECUPERADO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["recuperado", "mejorado", "aliviado"],
        confianza_grounding=0.75,
        propiedades={
            "es_estado_salud": True,
            "valencia": "positiva",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MEDICAMENTO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["medicamento", "medicina", "pastilla", "remedio"],
        confianza_grounding=0.78,
        propiedades={
            "es_salud": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_HOSPITAL",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["hospital", "clínica", "centro de salud"],
        confianza_grounding=0.78,
        propiedades={
            "es_lugar": True,
            "contexto": "salud",
        },
    ))
    
    # ══════════ ACCIONES DE BIENESTAR ═══════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DORMIR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["dormir", "descansar", "echarse", "acostarse"],
        confianza_grounding=0.78,
        propiedades={
            "es_accion_bienestar": True,
            "requiere_cuerpo_fisico": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DESPERTAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["despertar", "levantarse", "madrugar"],
        confianza_grounding=0.75,
        propiedades={
            "es_accion_bienestar": True,
            "requiere_cuerpo_fisico": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EJERCICIO",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["ejercicio", "hacer ejercicio", "entrenar", "workout"],
        confianza_grounding=0.78,
        propiedades={
            "es_accion_bienestar": True,
            "requiere_cuerpo_fisico": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RESPIRAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["respirar", "inhalar", "exhalar"],
        confianza_grounding=0.75,
        propiedades={
            "es_accion_bienestar": True,
            "requiere_cuerpo_fisico": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RELAJARSE",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["relajarse", "desestresarse", "calmarse"],
        confianza_grounding=0.75,
        propiedades={
            "es_accion_bienestar": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MEDITAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["meditar", "meditación", "mindfulness"],
        confianza_grounding=0.72,
        propiedades={
            "es_accion_bienestar": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_BANARSE",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["bañarse", "ducharse", "asearse"],
        confianza_grounding=0.75,
        propiedades={
            "es_accion_bienestar": True,
            "requiere_cuerpo_fisico": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CUIDARSE",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["cuidarse", "autocuidado", "cuidar la salud"],
        confianza_grounding=0.75,
        propiedades={
            "es_accion_bienestar": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ESTIRARSE",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["estirarse", "hacer estiramientos", "elongar"],
        confianza_grounding=0.72,
        propiedades={
            "es_accion_bienestar": True,
            "requiere_cuerpo_fisico": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_HIDRATARSE",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["hidratarse", "tomar agua", "beber líquidos"],
        confianza_grounding=0.75,
        propiedades={
            "es_accion_bienestar": True,
            "requiere_cuerpo_fisico": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CAMINAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["caminar", "andar", "pasear", "dar un paseo"],
        confianza_grounding=0.78,
        propiedades={
            "es_accion_bienestar": True,
            "requiere_cuerpo_fisico": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CORRER_EJERCICIO",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["correr", "trotar", "jogging", "running"],
        confianza_grounding=0.75,
        propiedades={
            "es_accion_bienestar": True,
            "requiere_cuerpo_fisico": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NADAR_EJERCICIO",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["nadar", "natación", "hacer nado"],
        confianza_grounding=0.72,
        propiedades={
            "es_accion_bienestar": True,
            "requiere_cuerpo_fisico": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_YOGA",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["yoga", "hacer yoga", "posturas de yoga"],
        confianza_grounding=0.72,
        propiedades={
            "es_accion_bienestar": True,
            "requiere_cuerpo_fisico": True,
        },
    ))
    
    return conceptos


if __name__ == '__main__':
    conceptos = obtener_conceptos_salud_cuerpo()
    grounding_prom = sum(c.confianza_grounding for c in conceptos) / len(conceptos)
    print(f"✅ Salud y Cuerpo: {len(conceptos)} conceptos")
    print(f"   Grounding promedio: {grounding_prom:.2f}")