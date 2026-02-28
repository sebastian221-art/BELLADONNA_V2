"""
Adjetivos Descriptivos - Expansión Fase 4A.

Adjetivos para describir propiedades de cosas.

Conceptos: 70 total
Grounding promedio: 0.72
Tipo: PROPIEDAD (atributos medibles/clasificables)
"""
from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto


def obtener_conceptos_adjetivos_descriptivos():
    """
    Retorna adjetivos descriptivos.
    
    Tipo: PROPIEDAD
    Grounding: 0.7-0.8 (Bell puede clasificar y entender estas propiedades)
    
    Categorías:
    - Tamaño (10 conceptos)
    - Colores (12 conceptos)
    - Cualidades físicas (12 conceptos)
    - Estados (12 conceptos)
    - Valoraciones (14 conceptos)
    - Cantidad (10 conceptos)
    """
    conceptos = []
    
    # ══════════ TAMAÑO ══════════════════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_GRANDE",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["grande", "enorme", "gigante", "inmenso"],
        confianza_grounding=0.75,
        propiedades={
            "es_medible": True,
            "dimension": "tamaño",
            "valor_relativo": "alto",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_PEQUEÑO"},
            "tipo_de": {"PROPIEDAD_TAMAÑO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PEQUEÑO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["pequeño", "chico", "diminuto", "minúsculo"],
        confianza_grounding=0.75,
        propiedades={
            "es_medible": True,
            "dimension": "tamaño",
            "valor_relativo": "bajo",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_GRANDE"},
            "tipo_de": {"PROPIEDAD_TAMAÑO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LARGO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["largo", "extenso", "prolongado", "alargado"],
        confianza_grounding=0.75,
        propiedades={
            "es_medible": True,
            "dimension": "longitud",
            "valor_relativo": "alto",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_CORTO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CORTO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["corto", "breve", "reducido"],
        confianza_grounding=0.75,
        propiedades={
            "es_medible": True,
            "dimension": "longitud",
            "valor_relativo": "bajo",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_LARGO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ALTO_ADJ",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["alto", "elevado", "erguido"],
        confianza_grounding=0.75,
        propiedades={
            "es_medible": True,
            "dimension": "altura",
            "valor_relativo": "alto",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_BAJO_ADJ"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_BAJO_ADJ",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["bajo", "bajito", "pequeño de estatura"],
        confianza_grounding=0.75,
        propiedades={
            "es_medible": True,
            "dimension": "altura",
            "valor_relativo": "bajo",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_ALTO_ADJ"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ANCHO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["ancho", "amplio", "espacioso", "holgado"],
        confianza_grounding=0.72,
        propiedades={
            "es_medible": True,
            "dimension": "anchura",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_ESTRECHO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ESTRECHO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["estrecho", "angosto", "ajustado"],
        confianza_grounding=0.72,
        propiedades={
            "es_medible": True,
            "dimension": "anchura",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_ANCHO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_GRUESO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["grueso", "gordo", "voluminoso"],
        confianza_grounding=0.70,
        propiedades={
            "es_medible": True,
            "dimension": "grosor",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_DELGADO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DELGADO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["delgado", "fino", "esbelto", "flaco"],
        confianza_grounding=0.70,
        propiedades={
            "es_medible": True,
            "dimension": "grosor",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_GRUESO"},
        },
    ))
    
    # ══════════ COLORES ═════════════════════════════════════════
    
    colores = [
        ("CONCEPTO_ROJO", ["rojo", "colorado", "carmesí", "escarlata"]),
        ("CONCEPTO_AZUL", ["azul", "celeste", "índigo", "añil"]),
        ("CONCEPTO_VERDE", ["verde", "verdoso", "esmeralda"]),
        ("CONCEPTO_AMARILLO", ["amarillo", "dorado", "áureo"]),
        ("CONCEPTO_NARANJA", ["naranja", "anaranjado"]),
        ("CONCEPTO_MORADO", ["morado", "violeta", "púrpura", "lila"]),
        ("CONCEPTO_ROSA", ["rosa", "rosado"]),
        ("CONCEPTO_MARRON", ["marrón", "café", "castaño", "pardo"]),
        ("CONCEPTO_NEGRO", ["negro", "oscuro", "azabache"]),
        ("CONCEPTO_BLANCO", ["blanco", "claro", "níveo"]),
        ("CONCEPTO_GRIS", ["gris", "grisáceo", "plomizo"]),
        ("CONCEPTO_TRANSPARENTE", ["transparente", "cristalino", "traslúcido"]),
    ]
    
    for id_c, palabras in colores:
        conceptos.append(ConceptoAnclado(
            id=id_c,
            tipo=TipoConcepto.PROPIEDAD,
            palabras_español=palabras,
            confianza_grounding=0.78,
            propiedades={
                "es_color": True,
                "es_visual": True,
            },
            relaciones={
                "tipo_de": {"PROPIEDAD_COLOR"},
            },
        ))
    
    # ══════════ CUALIDADES FÍSICAS ══════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DURO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["duro", "sólido", "firme", "rígido"],
        confianza_grounding=0.72,
        propiedades={
            "es_tactil": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_BLANDO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_BLANDO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["blando", "suave", "mullido", "esponjoso"],
        confianza_grounding=0.72,
        propiedades={
            "es_tactil": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_DURO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CALIENTE",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["caliente", "cálido", "ardiente", "tibio"],
        confianza_grounding=0.75,
        propiedades={
            "es_temperatura": True,
            "es_medible": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_FRIO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FRIO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["frío", "helado", "gélido", "congelado"],
        confianza_grounding=0.75,
        propiedades={
            "es_temperatura": True,
            "es_medible": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_CALIENTE"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SECO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["seco", "árido", "deshidratado"],
        confianza_grounding=0.72,
        propiedades={
            "es_humedad": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_MOJADO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MOJADO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["mojado", "húmedo", "empapado"],
        confianza_grounding=0.72,
        propiedades={
            "es_humedad": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_SECO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PESADO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["pesado", "macizo", "denso"],
        confianza_grounding=0.75,
        propiedades={
            "es_medible": True,
            "dimension": "peso",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_LIGERO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LIGERO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["ligero", "liviano", "leve"],
        confianza_grounding=0.75,
        propiedades={
            "es_medible": True,
            "dimension": "peso",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_PESADO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LISO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["liso", "suave", "terso", "pulido"],
        confianza_grounding=0.70,
        propiedades={
            "es_tactil": True,
            "es_textura": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_RUGOSO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RUGOSO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["rugoso", "áspero", "irregular", "rasposo"],
        confianza_grounding=0.70,
        propiedades={
            "es_tactil": True,
            "es_textura": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_LISO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_BRILLANTE",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["brillante", "reluciente", "luminoso", "resplandeciente"],
        confianza_grounding=0.72,
        propiedades={
            "es_visual": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_OPACO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_OPACO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["opaco", "mate", "sin brillo"],
        confianza_grounding=0.70,
        propiedades={
            "es_visual": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_BRILLANTE"},
        },
    ))
    
    # ══════════ ESTADOS ═════════════════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LLENO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["lleno", "repleto", "colmado", "completo"],
        confianza_grounding=0.78,
        propiedades={
            "es_estado": True,
            "es_medible": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_VACIO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_VACIO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["vacío", "hueco", "desocupado"],
        confianza_grounding=0.78,
        propiedades={
            "es_estado": True,
            "es_medible": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_LLENO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ABIERTO_ADJ",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["abierto", "destapado", "descubierto"],
        confianza_grounding=0.78,
        propiedades={
            "es_estado": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_CERRADO_ADJ"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CERRADO_ADJ",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["cerrado", "clausurado", "tapado"],
        confianza_grounding=0.78,
        propiedades={
            "es_estado": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_ABIERTO_ADJ"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ENCENDIDO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["encendido", "prendido", "activo", "on"],
        confianza_grounding=0.80,
        propiedades={
            "es_estado": True,
            "es_digital": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_APAGADO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_APAGADO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["apagado", "inactivo", "off"],
        confianza_grounding=0.80,
        propiedades={
            "es_estado": True,
            "es_digital": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_ENCENDIDO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LIMPIO_ADJ",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["limpio", "aseado", "pulcro", "impecable"],
        confianza_grounding=0.72,
        propiedades={
            "es_estado": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_SUCIO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SUCIO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["sucio", "manchado", "mugriento"],
        confianza_grounding=0.72,
        propiedades={
            "es_estado": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_LIMPIO_ADJ"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ROTO_ADJ",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["roto", "quebrado", "averiado", "dañado"],
        confianza_grounding=0.75,
        propiedades={
            "es_estado": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_ENTERO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ENTERO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["entero", "completo", "íntegro", "intacto"],
        confianza_grounding=0.75,
        propiedades={
            "es_estado": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_ROTO_ADJ"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NUEVO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["nuevo", "recién", "flamante", "reciente"],
        confianza_grounding=0.75,
        propiedades={
            "es_estado": True,
            "es_temporal": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_VIEJO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_VIEJO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["viejo", "antiguo", "usado", "gastado"],
        confianza_grounding=0.75,
        propiedades={
            "es_estado": True,
            "es_temporal": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_NUEVO"},
        },
    ))
    
    # ══════════ VALORACIONES ════════════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_BUENO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["bueno", "bien", "excelente", "estupendo"],
        confianza_grounding=0.72,
        propiedades={
            "es_valoracion": True,
            "valor": "positivo",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_MALO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MALO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["malo", "mal", "pésimo", "terrible"],
        confianza_grounding=0.72,
        propiedades={
            "es_valoracion": True,
            "valor": "negativo",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_BUENO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FACIL",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["fácil", "sencillo", "simple", "elemental"],
        confianza_grounding=0.75,
        propiedades={
            "es_valoracion": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_DIFICIL"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DIFICIL",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["difícil", "complicado", "complejo", "arduo"],
        confianza_grounding=0.75,
        propiedades={
            "es_valoracion": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_FACIL"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RAPIDO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["rápido", "veloz", "ágil", "pronto"],
        confianza_grounding=0.78,
        propiedades={
            "es_medible": True,
            "dimension": "velocidad",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_LENTO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LENTO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["lento", "pausado", "calmoso", "despacio"],
        confianza_grounding=0.78,
        propiedades={
            "es_medible": True,
            "dimension": "velocidad",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_RAPIDO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_IMPORTANTE",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["importante", "relevante", "significativo", "crucial"],
        confianza_grounding=0.72,
        propiedades={
            "es_valoracion": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_UTIL",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["útil", "práctico", "funcional", "provechoso"],
        confianza_grounding=0.72,
        propiedades={
            "es_valoracion": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_INUTIL"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INUTIL",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["inútil", "innecesario", "impractico"],
        confianza_grounding=0.70,
        propiedades={
            "es_valoracion": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_UTIL"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CORRECTO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["correcto", "exacto", "preciso", "acertado"],
        confianza_grounding=0.80,
        propiedades={
            "es_valoracion": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_INCORRECTO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INCORRECTO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["incorrecto", "equivocado", "erróneo", "falso"],
        confianza_grounding=0.80,
        propiedades={
            "es_valoracion": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_CORRECTO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SEGURO_VALORACION",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["seguro", "confiable", "fiable"],
        confianza_grounding=0.75,
        propiedades={
            "es_valoracion": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_PELIGROSO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PELIGROSO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["peligroso", "riesgoso", "inseguro", "arriesgado"],
        confianza_grounding=0.75,
        propiedades={
            "es_valoracion": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_SEGURO_VALORACION"},
        },
    ))
    
    # ══════════ CANTIDAD ════════════════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MUCHO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["mucho", "abundante", "numeroso", "bastante"],
        confianza_grounding=0.72,
        propiedades={
            "es_cantidad": True,
            "valor_relativo": "alto",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_POCO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_POCO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["poco", "escaso", "reducido"],
        confianza_grounding=0.72,
        propiedades={
            "es_cantidad": True,
            "valor_relativo": "bajo",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_MUCHO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TODO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["todo", "todos", "completo", "total"],
        confianza_grounding=0.78,
        propiedades={
            "es_cantidad": True,
            "valor": "maximo",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_NADA"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NADA",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["nada", "ninguno", "cero"],
        confianza_grounding=0.78,
        propiedades={
            "es_cantidad": True,
            "valor": "minimo",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_TODO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SUFICIENTE",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["suficiente", "bastante", "adecuado"],
        confianza_grounding=0.70,
        propiedades={
            "es_cantidad": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EXCESIVO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["excesivo", "demasiado", "exagerado"],
        confianza_grounding=0.70,
        propiedades={
            "es_cantidad": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PRIMERO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["primero", "inicial", "principal", "primer"],
        confianza_grounding=0.78,
        propiedades={
            "es_ordinal": True,
            "posicion": 1,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_ULTIMO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ULTIMO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["último", "final", "postrero"],
        confianza_grounding=0.78,
        propiedades={
            "es_ordinal": True,
            "posicion": -1,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_PRIMERO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_UNICO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["único", "solo", "singular", "exclusivo"],
        confianza_grounding=0.75,
        propiedades={
            "es_cantidad": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_VARIOS",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["varios", "múltiples", "diversos", "algunos"],
        confianza_grounding=0.72,
        propiedades={
            "es_cantidad": True,
        },
    ))
    
    return conceptos


if __name__ == '__main__':
    conceptos = obtener_conceptos_adjetivos_descriptivos()
    grounding_prom = sum(c.confianza_grounding for c in conceptos) / len(conceptos)
    print(f"✅ Adjetivos Descriptivos: {len(conceptos)} conceptos")
    print(f"   Grounding promedio: {grounding_prom:.2f}")