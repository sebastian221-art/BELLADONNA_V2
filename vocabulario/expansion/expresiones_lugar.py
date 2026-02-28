"""
Expresiones de Lugar - Expansión Fase 4A.

Vocabulario espacial para conversación natural.

Conceptos: 50 total
Grounding promedio: 0.72
Tipo: PALABRA_CONVERSACION
"""
from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto


def obtener_conceptos_expresiones_lugar():
    """
    Retorna expresiones de lugar.
    
    Categorías:
    - Preposiciones espaciales (12 conceptos)
    - Direcciones (8 conceptos)
    - Posiciones (10 conceptos)
    - Lugares comunes (20 conceptos)
    """
    conceptos = []
    
    # ══════════ PREPOSICIONES ESPACIALES ════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EN_LUGAR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["en", "dentro de", "in", "adentro de"],
        confianza_grounding=0.78,
        propiedades={
            "es_preposicion": True,
            "es_espacial": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SOBRE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["sobre", "encima de", "on", "arriba de"],
        confianza_grounding=0.75,
        propiedades={
            "es_preposicion": True,
            "es_espacial": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_BAJO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_BAJO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["bajo", "debajo de", "under", "abajo de"],
        confianza_grounding=0.75,
        propiedades={
            "es_preposicion": True,
            "es_espacial": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_SOBRE"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ENTRE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["entre", "en medio de", "between"],
        confianza_grounding=0.72,
        propiedades={
            "es_preposicion": True,
            "es_espacial": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_JUNTO_A",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["junto a", "al lado de", "beside", "cerca de"],
        confianza_grounding=0.72,
        propiedades={
            "es_preposicion": True,
            "es_espacial": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FRENTE_A",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["frente a", "delante de", "enfrente de", "in front of"],
        confianza_grounding=0.72,
        propiedades={
            "es_preposicion": True,
            "es_espacial": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_DETRAS"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DETRAS",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["detrás de", "atrás de", "behind", "tras"],
        confianza_grounding=0.72,
        propiedades={
            "es_preposicion": True,
            "es_espacial": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_FRENTE_A"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DENTRO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["dentro", "adentro", "inside"],
        confianza_grounding=0.75,
        propiedades={
            "es_preposicion": True,
            "es_espacial": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_FUERA"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FUERA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["fuera", "afuera", "outside", "exterior"],
        confianza_grounding=0.75,
        propiedades={
            "es_preposicion": True,
            "es_espacial": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_DENTRO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ALREDEDOR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["alrededor de", "en torno a", "around"],
        confianza_grounding=0.70,
        propiedades={
            "es_preposicion": True,
            "es_espacial": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_A_TRAVES",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["a través de", "por", "through"],
        confianza_grounding=0.70,
        propiedades={
            "es_preposicion": True,
            "es_espacial": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_HACIA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["hacia", "en dirección a", "toward", "rumbo a"],
        confianza_grounding=0.72,
        propiedades={
            "es_preposicion": True,
            "es_espacial": True,
            "es_direccional": True,
        },
    ))
    
    # ══════════ DIRECCIONES ═════════════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ARRIBA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["arriba", "up", "hacia arriba"],
        confianza_grounding=0.78,
        propiedades={
            "es_direccion": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_ABAJO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ABAJO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["abajo", "down", "hacia abajo"],
        confianza_grounding=0.78,
        propiedades={
            "es_direccion": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_ARRIBA"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_IZQUIERDA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["izquierda", "left", "a la izquierda"],
        confianza_grounding=0.78,
        propiedades={
            "es_direccion": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_DERECHA"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DERECHA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["derecha", "right", "a la derecha"],
        confianza_grounding=0.78,
        propiedades={
            "es_direccion": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_IZQUIERDA"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NORTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["norte", "north"],
        confianza_grounding=0.75,
        propiedades={
            "es_direccion": True,
            "es_cardinal": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_SUR"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SUR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["sur", "south"],
        confianza_grounding=0.75,
        propiedades={
            "es_direccion": True,
            "es_cardinal": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_NORTE"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ESTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["este", "east", "oriente"],
        confianza_grounding=0.75,
        propiedades={
            "es_direccion": True,
            "es_cardinal": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_OESTE"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_OESTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["oeste", "west", "occidente"],
        confianza_grounding=0.75,
        propiedades={
            "es_direccion": True,
            "es_cardinal": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_ESTE"},
        },
    ))
    
    # ══════════ POSICIONES ══════════════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_AQUI",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["aquí", "acá", "here", "en este lugar"],
        confianza_grounding=0.78,
        propiedades={
            "es_posicion": True,
            "es_proximal": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_AHI",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["ahí", "allí", "there"],
        confianza_grounding=0.75,
        propiedades={
            "es_posicion": True,
            "es_medial": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ALLA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["allá", "over there", "lejos"],
        confianza_grounding=0.72,
        propiedades={
            "es_posicion": True,
            "es_distal": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CERCA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["cerca", "cercano", "near", "próximo"],
        confianza_grounding=0.75,
        propiedades={
            "es_distancia": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_LEJOS"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LEJOS",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["lejos", "lejano", "far", "distante"],
        confianza_grounding=0.75,
        propiedades={
            "es_distancia": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_CERCA"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CENTRO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["centro", "medio", "center", "mitad"],
        confianza_grounding=0.75,
        propiedades={
            "es_posicion": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_BORDE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["borde", "orilla", "edge", "margen"],
        confianza_grounding=0.70,
        propiedades={
            "es_posicion": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ESQUINA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["esquina", "corner", "ángulo"],
        confianza_grounding=0.72,
        propiedades={
            "es_posicion": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ENTRADA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["entrada", "acceso", "entrance", "ingreso"],
        confianza_grounding=0.75,
        propiedades={
            "es_posicion": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_SALIDA_LUGAR"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SALIDA_LUGAR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["salida", "exit", "egreso"],
        confianza_grounding=0.75,
        propiedades={
            "es_posicion": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_ENTRADA"},
        },
    ))
    
    # ══════════ LUGARES COMUNES ═════════════════════════════════
    
    lugares = [
        ("CONCEPTO_CASA", ["casa", "hogar", "home", "domicilio"]),
        ("CONCEPTO_OFICINA", ["oficina", "office", "trabajo", "despacho"]),
        ("CONCEPTO_ESCUELA", ["escuela", "school", "colegio", "instituto"]),
        ("CONCEPTO_UNIVERSIDAD", ["universidad", "university", "facultad"]),
        ("CONCEPTO_HOSPITAL", ["hospital", "clínica", "centro médico"]),
        ("CONCEPTO_TIENDA", ["tienda", "store", "shop", "comercio"]),
        ("CONCEPTO_RESTAURANTE", ["restaurante", "restaurant", "comedor"]),
        ("CONCEPTO_BANCO", ["banco", "bank"]),
        ("CONCEPTO_PARQUE", ["parque", "park", "plaza"]),
        ("CONCEPTO_BIBLIOTECA", ["biblioteca", "library"]),
        ("CONCEPTO_GIMNASIO", ["gimnasio", "gym"]),
        ("CONCEPTO_SUPERMERCADO", ["supermercado", "supermarket", "mercado"]),
        ("CONCEPTO_FARMACIA", ["farmacia", "pharmacy", "droguería"]),
        ("CONCEPTO_IGLESIA", ["iglesia", "church", "templo"]),
        ("CONCEPTO_MUSEO", ["museo", "museum", "galería"]),
        ("CONCEPTO_CINE", ["cine", "cinema", "teatro"]),
        ("CONCEPTO_PLAYA", ["playa", "beach", "costa"]),
        ("CONCEPTO_MONTANA", ["montaña", "mountain", "cerro"]),
        ("CONCEPTO_CIUDAD", ["ciudad", "city", "urbe"]),
        ("CONCEPTO_PAIS", ["país", "country", "nación"]),
    ]
    
    for id_c, palabras in lugares:
        conceptos.append(ConceptoAnclado(
            id=id_c,
            tipo=TipoConcepto.PALABRA_CONVERSACION,
            palabras_español=palabras,
            confianza_grounding=0.70,
            propiedades={
                "es_lugar": True,
                "bell_puede_ejecutar": False,
            },
        ))
    
    return conceptos


if __name__ == '__main__':
    conceptos = obtener_conceptos_expresiones_lugar()
    grounding_prom = sum(c.confianza_grounding for c in conceptos) / len(conceptos)
    print(f"✅ Expresiones de Lugar: {len(conceptos)} conceptos")
    print(f"   Grounding promedio: {grounding_prom:.2f}")