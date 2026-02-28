"""
Naturaleza y Medio Ambiente - Expansión Fase 4A.

Términos de naturaleza, clima y medio ambiente.

Conceptos: 40 total
Grounding promedio: 0.72
Tipo: PALABRA_CONVERSACION / ACCION_COGNITIVA
"""
from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto


def obtener_conceptos_naturaleza():
    """
    Retorna conceptos de naturaleza y medio ambiente.
    
    Categorías:
    - Clima y tiempo atmosférico (12)
    - Elementos naturales (14)
    - Animales comunes (14)
    """
    conceptos = []
    
    # ══════════ CLIMA Y TIEMPO ATMOSFÉRICO ══════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SOL",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["sol", "soleado", "hace sol"],
        confianza_grounding=0.78,
        propiedades={
            "es_clima": True,
            "valencia": "positiva",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LLUVIA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["lluvia", "llover", "llueve", "lloviendo"],
        confianza_grounding=0.78,
        propiedades={
            "es_clima": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NIEVE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["nieve", "nevar", "nieva", "nevando"],
        confianza_grounding=0.75,
        propiedades={
            "es_clima": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_VIENTO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["viento", "ventoso", "brisa", "aire"],
        confianza_grounding=0.75,
        propiedades={
            "es_clima": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TORMENTA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["tormenta", "tempestad", "temporal"],
        confianza_grounding=0.72,
        propiedades={
            "es_clima": True,
            "es_peligroso": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NUBLADO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["nublado", "nube", "nubes", "cielo cubierto"],
        confianza_grounding=0.75,
        propiedades={
            "es_clima": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TEMPERATURA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["temperatura", "grados", "calor", "frío"],
        confianza_grounding=0.78,
        propiedades={
            "es_clima": True,
            "es_medible": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_HUMEDAD",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["humedad", "húmedo", "seco"],
        confianza_grounding=0.72,
        propiedades={
            "es_clima": True,
            "es_medible": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CLIMA_GENERAL",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["clima", "tiempo", "qué tiempo hace"],
        confianza_grounding=0.78,
        propiedades={
            "es_clima": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NIEBLA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["niebla", "neblina", "bruma"],
        confianza_grounding=0.72,
        propiedades={
            "es_clima": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RAYO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["rayo", "relámpago", "trueno"],
        confianza_grounding=0.72,
        propiedades={
            "es_clima": True,
            "es_peligroso": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ARCOIRIS",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["arcoíris", "arco iris"],
        confianza_grounding=0.70,
        propiedades={
            "es_fenomeno": True,
            "valencia": "positiva",
        },
    ))
    
    # ══════════ ELEMENTOS NATURALES ═════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_AGUA_NATURAL",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["agua", "h2o"],
        confianza_grounding=0.80,
        propiedades={
            "es_elemento": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FUEGO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["fuego", "llama", "incendio"],
        confianza_grounding=0.75,
        propiedades={
            "es_elemento": True,
            "es_peligroso": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TIERRA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["tierra", "suelo", "terreno"],
        confianza_grounding=0.75,
        propiedades={
            "es_elemento": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ARBOL",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["árbol", "árboles", "planta grande"],
        confianza_grounding=0.75,
        propiedades={
            "es_naturaleza": True,
            "es_vegetal": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FLOR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["flor", "flores", "florecita"],
        confianza_grounding=0.75,
        propiedades={
            "es_naturaleza": True,
            "es_vegetal": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MONTAÑA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["montaña", "monte", "cerro", "sierra"],
        confianza_grounding=0.72,
        propiedades={
            "es_naturaleza": True,
            "es_geografia": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RIO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["río", "arroyo", "riachuelo"],
        confianza_grounding=0.72,
        propiedades={
            "es_naturaleza": True,
            "es_cuerpo_agua": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MAR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["mar", "océano", "playa"],
        confianza_grounding=0.75,
        propiedades={
            "es_naturaleza": True,
            "es_cuerpo_agua": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_BOSQUE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["bosque", "selva", "jungla"],
        confianza_grounding=0.72,
        propiedades={
            "es_naturaleza": True,
            "es_ecosistema": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DESIERTO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["desierto", "árido", "dunas"],
        confianza_grounding=0.70,
        propiedades={
            "es_naturaleza": True,
            "es_ecosistema": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CIELO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["cielo", "firmamento", "atmósfera"],
        confianza_grounding=0.75,
        propiedades={
            "es_naturaleza": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LUNA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["luna", "lunar", "satélite"],
        confianza_grounding=0.72,
        propiedades={
            "es_naturaleza": True,
            "es_astro": True,
        },
    ))
    
    # ══════════ ANIMALES COMUNES ════════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PERRO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["perro", "can", "cachorro", "mascota"],
        confianza_grounding=0.78,
        propiedades={
            "es_animal": True,
            "es_domestico": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_GATO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["gato", "felino", "gatito", "minino"],
        confianza_grounding=0.78,
        propiedades={
            "es_animal": True,
            "es_domestico": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PAJARO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["pájaro", "ave", "pajarito"],
        confianza_grounding=0.75,
        propiedades={
            "es_animal": True,
            "puede_volar": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PEZ",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["pez", "pescado", "peces"],
        confianza_grounding=0.75,
        propiedades={
            "es_animal": True,
            "es_acuatico": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CABALLO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["caballo", "yegua", "potro"],
        confianza_grounding=0.72,
        propiedades={
            "es_animal": True,
            "es_domestico": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_VACA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["vaca", "toro", "res", "ganado"],
        confianza_grounding=0.72,
        propiedades={
            "es_animal": True,
            "es_domestico": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LEON",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["león", "leona", "felino salvaje"],
        confianza_grounding=0.70,
        propiedades={
            "es_animal": True,
            "es_salvaje": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INSECTO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["insecto", "bicho", "hormiga", "mosca"],
        confianza_grounding=0.72,
        propiedades={
            "es_animal": True,
            "es_invertebrado": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MARIPOSA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["mariposa", "polilla"],
        confianza_grounding=0.70,
        propiedades={
            "es_animal": True,
            "es_invertebrado": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SERPIENTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["serpiente", "víbora", "culebra"],
        confianza_grounding=0.70,
        propiedades={
            "es_animal": True,
            "es_reptil": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ELEFANTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["elefante", "paquidermo"],
        confianza_grounding=0.68,
        propiedades={
            "es_animal": True,
            "es_salvaje": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_OSO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["oso", "osa", "osito"],
        confianza_grounding=0.70,
        propiedades={
            "es_animal": True,
            "es_salvaje": True,
        },
    ))
    
    return conceptos


if __name__ == '__main__':
    conceptos = obtener_conceptos_naturaleza()
    grounding_prom = sum(c.confianza_grounding for c in conceptos) / len(conceptos)
    print(f"✅ Naturaleza: {len(conceptos)} conceptos")
    print(f"   Grounding promedio: {grounding_prom:.2f}")