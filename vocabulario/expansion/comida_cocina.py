"""
Comida y Cocina - Expansión Fase 4A.

Alimentos, bebidas y términos culinarios.

Conceptos: 45 total
Grounding promedio: 0.74
Tipo: PALABRA_CONVERSACION / ACCION_COGNITIVA
"""
from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto


def obtener_conceptos_comida_cocina():
    """
    Retorna conceptos de comida y cocina.
    
    Categorías:
    - Alimentos básicos (15)
    - Bebidas (10)
    - Acciones de cocina (10)
    - Comidas del día (10)
    """
    conceptos = []
    
    # ══════════ ALIMENTOS BÁSICOS ═══════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PAN",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["pan", "panecillo", "baguette"],
        confianza_grounding=0.78,
        propiedades={
            "es_alimento": True,
            "tipo": "carbohidrato",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CARNE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["carne", "res", "pollo", "cerdo"],
        confianza_grounding=0.78,
        propiedades={
            "es_alimento": True,
            "tipo": "proteina",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PESCADO_COMIDA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["pescado", "mariscos", "salmón", "atún"],
        confianza_grounding=0.75,
        propiedades={
            "es_alimento": True,
            "tipo": "proteina",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_VERDURA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["verdura", "verduras", "vegetales", "hortaliza"],
        confianza_grounding=0.78,
        propiedades={
            "es_alimento": True,
            "es_saludable": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FRUTA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["fruta", "frutas", "manzana", "naranja"],
        confianza_grounding=0.78,
        propiedades={
            "es_alimento": True,
            "es_saludable": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ARROZ",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["arroz", "arrocito"],
        confianza_grounding=0.78,
        propiedades={
            "es_alimento": True,
            "tipo": "carbohidrato",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PASTA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["pasta", "fideos", "espagueti", "macarrones"],
        confianza_grounding=0.78,
        propiedades={
            "es_alimento": True,
            "tipo": "carbohidrato",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_HUEVO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["huevo", "huevos", "blanquillo"],
        confianza_grounding=0.78,
        propiedades={
            "es_alimento": True,
            "tipo": "proteina",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_QUESO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["queso", "quesito", "lácteo"],
        confianza_grounding=0.75,
        propiedades={
            "es_alimento": True,
            "tipo": "lacteo",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LECHE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["leche", "lechita"],
        confianza_grounding=0.78,
        propiedades={
            "es_alimento": True,
            "es_bebida": True,
            "tipo": "lacteo",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ENSALADA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["ensalada", "ensaladita"],
        confianza_grounding=0.75,
        propiedades={
            "es_alimento": True,
            "es_saludable": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SOPA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["sopa", "caldo", "consomé"],
        confianza_grounding=0.75,
        propiedades={
            "es_alimento": True,
            "es_caliente": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_POSTRE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["postre", "dulce", "pastel", "helado"],
        confianza_grounding=0.75,
        propiedades={
            "es_alimento": True,
            "es_dulce": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PIZZA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["pizza", "pizzas"],
        confianza_grounding=0.78,
        propiedades={
            "es_alimento": True,
            "es_comida_rapida": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_HAMBURGUESA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["hamburguesa", "burger", "hamburguesita"],
        confianza_grounding=0.78,
        propiedades={
            "es_alimento": True,
            "es_comida_rapida": True,
        },
    ))
    
    # ══════════ BEBIDAS ═════════════════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_AGUA_BEBIDA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["agua", "agüita", "agua natural"],
        confianza_grounding=0.80,
        propiedades={
            "es_bebida": True,
            "es_saludable": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CAFE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["café", "cafecito", "espresso", "cappuccino"],
        confianza_grounding=0.80,
        propiedades={
            "es_bebida": True,
            "tiene_cafeina": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["té", "tecito", "infusión"],
        confianza_grounding=0.78,
        propiedades={
            "es_bebida": True,
            "es_caliente": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_JUGO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["jugo", "zumo", "jugito"],
        confianza_grounding=0.78,
        propiedades={
            "es_bebida": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_REFRESCO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["refresco", "soda", "gaseosa", "coca"],
        confianza_grounding=0.78,
        propiedades={
            "es_bebida": True,
            "es_dulce": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CERVEZA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["cerveza", "chela", "birra"],
        confianza_grounding=0.75,
        propiedades={
            "es_bebida": True,
            "es_alcoholica": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_VINO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["vino", "vino tinto", "vino blanco"],
        confianza_grounding=0.75,
        propiedades={
            "es_bebida": True,
            "es_alcoholica": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LICUADO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["licuado", "smoothie", "batido"],
        confianza_grounding=0.75,
        propiedades={
            "es_bebida": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_BEBIDA_GENERAL",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["bebida", "trago", "algo de tomar"],
        confianza_grounding=0.78,
        propiedades={
            "es_bebida": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CHOCOLATE_BEBIDA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["chocolate", "chocolatito", "chocolate caliente"],
        confianza_grounding=0.75,
        propiedades={
            "es_bebida": True,
            "es_dulce": True,
        },
    ))
    
    # ══════════ ACCIONES DE COCINA ══════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_COCINAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["cocinar", "preparar comida", "guisar"],
        confianza_grounding=0.75,
        propiedades={
            "es_accion_cocina": True,
            "requiere_cuerpo_fisico": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_HORNEAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["hornear", "meter al horno", "asar"],
        confianza_grounding=0.72,
        propiedades={
            "es_accion_cocina": True,
            "requiere_cuerpo_fisico": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FREIR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["freír", "fritir", "sofreír"],
        confianza_grounding=0.72,
        propiedades={
            "es_accion_cocina": True,
            "requiere_cuerpo_fisico": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_HERVIR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["hervir", "cocer", "sancochar"],
        confianza_grounding=0.72,
        propiedades={
            "es_accion_cocina": True,
            "requiere_cuerpo_fisico": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CORTAR_COCINA",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["cortar", "picar", "rebanar"],
        confianza_grounding=0.75,
        propiedades={
            "es_accion_cocina": True,
            "requiere_cuerpo_fisico": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MEZCLAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["mezclar", "revolver", "batir"],
        confianza_grounding=0.75,
        propiedades={
            "es_accion_cocina": True,
            "requiere_cuerpo_fisico": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SAZONAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["sazonar", "condimentar", "salpimentar"],
        confianza_grounding=0.72,
        propiedades={
            "es_accion_cocina": True,
            "requiere_cuerpo_fisico": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SERVIR_COMIDA",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["servir", "emplatar", "poner la mesa"],
        confianza_grounding=0.75,
        propiedades={
            "es_accion_cocina": True,
            "requiere_cuerpo_fisico": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RECETA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["receta", "recetario", "instrucciones de cocina"],
        confianza_grounding=0.78,
        propiedades={
            "es_concepto_cocina": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INGREDIENTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["ingrediente", "ingredientes", "componentes"],
        confianza_grounding=0.78,
        propiedades={
            "es_concepto_cocina": True,
        },
    ))
    
    # ══════════ COMIDAS DEL DÍA ═════════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DESAYUNO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["desayuno", "desayunar", "primera comida"],
        confianza_grounding=0.80,
        propiedades={
            "es_comida": True,
            "momento": "mañana",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ALMUERZO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["almuerzo", "almorzar", "comida del medio día"],
        confianza_grounding=0.80,
        propiedades={
            "es_comida": True,
            "momento": "mediodia",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CENA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["cena", "cenar", "comida de la noche"],
        confianza_grounding=0.80,
        propiedades={
            "es_comida": True,
            "momento": "noche",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MERIENDA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["merienda", "snack", "bocadillo", "tentempié"],
        confianza_grounding=0.75,
        propiedades={
            "es_comida": True,
            "momento": "entre_comidas",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_HAMBRE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["hambre", "tengo hambre", "apetito"],
        confianza_grounding=0.80,
        propiedades={
            "es_estado": True,
            "es_sensacion": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SED",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["sed", "tengo sed", "sediento"],
        confianza_grounding=0.80,
        propiedades={
            "es_estado": True,
            "es_sensacion": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LLENO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["lleno", "satisfecho", "no tengo hambre"],
        confianza_grounding=0.78,
        propiedades={
            "es_estado": True,
            "es_sensacion": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DELICIOSO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["delicioso", "rico", "sabroso", "exquisito"],
        confianza_grounding=0.78,
        propiedades={
            "es_adjetivo": True,
            "contexto": "comida",
            "valencia": "positiva",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RESTAURANTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["restaurante", "restorán", "lugar para comer"],
        confianza_grounding=0.78,
        propiedades={
            "es_lugar": True,
            "contexto": "comida",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_COCINA_LUGAR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["cocina", "cocinita"],
        confianza_grounding=0.78,
        propiedades={
            "es_lugar": True,
            "contexto": "comida",
        },
    ))
    
    return conceptos


if __name__ == '__main__':
    conceptos = obtener_conceptos_comida_cocina()
    grounding_prom = sum(c.confianza_grounding for c in conceptos) / len(conceptos)
    print(f"✅ Comida y Cocina: {len(conceptos)} conceptos")
    print(f"   Grounding promedio: {grounding_prom:.2f}")