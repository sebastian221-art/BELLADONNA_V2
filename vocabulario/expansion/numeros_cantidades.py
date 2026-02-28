"""
Números y Cantidades - Expansión Fase 4A.

Conceptos numéricos y de cantidad.

Conceptos: 50 total
Grounding promedio: 0.78
Tipo: PROPIEDAD (valores medibles)
"""
from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto


def obtener_conceptos_numeros_cantidades():
    """
    Retorna conceptos de números y cantidades.
    
    Categorías:
    - Números cardinales (15 conceptos)
    - Números ordinales (10 conceptos)
    - Cantidades relativas (10 conceptos)
    - Operadores (8 conceptos)
    - Unidades de medida (7 conceptos)
    """
    conceptos = []
    
    # ══════════ NÚMEROS CARDINALES ══════════════════════════════
    
    cardinales = [
        ("CONCEPTO_CERO_NUM", ["cero", "0", "zero"], 0),
        ("CONCEPTO_UNO_NUM", ["uno", "1", "un", "una", "one"], 1),
        ("CONCEPTO_DOS_NUM", ["dos", "2", "two", "par"], 2),
        ("CONCEPTO_TRES_NUM", ["tres", "3", "three", "trío"], 3),
        ("CONCEPTO_CUATRO_NUM", ["cuatro", "4", "four"], 4),
        ("CONCEPTO_CINCO_NUM", ["cinco", "5", "five"], 5),
        ("CONCEPTO_SEIS_NUM", ["seis", "6", "six"], 6),
        ("CONCEPTO_SIETE_NUM", ["siete", "7", "seven"], 7),
        ("CONCEPTO_OCHO_NUM", ["ocho", "8", "eight"], 8),
        ("CONCEPTO_NUEVE_NUM", ["nueve", "9", "nine"], 9),
        ("CONCEPTO_DIEZ_NUM", ["diez", "10", "ten"], 10),
        ("CONCEPTO_CIEN_NUM", ["cien", "100", "ciento", "hundred"], 100),
        ("CONCEPTO_MIL_NUM", ["mil", "1000", "thousand"], 1000),
        ("CONCEPTO_MILLON_NUM", ["millón", "1000000", "million"], 1000000),
        ("CONCEPTO_BILLÓN_NUM", ["billón", "billion"], 1000000000),
    ]
    
    for id_c, palabras, valor in cardinales:
        conceptos.append(ConceptoAnclado(
            id=id_c,
            tipo=TipoConcepto.PROPIEDAD,
            palabras_español=palabras,
            confianza_grounding=0.85,
            propiedades={
                "es_numero": True,
                "es_cardinal": True,
                "valor_numerico": valor,
            },
            relaciones={
                "tipo_de": {"NUMERO"},
            },
        ))
    
    # ══════════ NÚMEROS ORDINALES ═══════════════════════════════
    
    ordinales = [
        ("CONCEPTO_PRIMERO_ORD", ["primero", "1ro", "1°", "primer", "first"], 1),
        ("CONCEPTO_SEGUNDO_ORD", ["segundo", "2do", "2°", "second"], 2),
        ("CONCEPTO_TERCERO_ORD", ["tercero", "3ro", "3°", "tercer", "third"], 3),
        ("CONCEPTO_CUARTO_ORD", ["cuarto", "4to", "4°", "fourth"], 4),
        ("CONCEPTO_QUINTO_ORD", ["quinto", "5to", "5°", "fifth"], 5),
        ("CONCEPTO_SEXTO_ORD", ["sexto", "6to", "6°", "sixth"], 6),
        ("CONCEPTO_SEPTIMO_ORD", ["séptimo", "7mo", "seventh"], 7),
        ("CONCEPTO_OCTAVO_ORD", ["octavo", "8vo", "eighth"], 8),
        ("CONCEPTO_NOVENO_ORD", ["noveno", "9no", "ninth"], 9),
        ("CONCEPTO_DECIMO_ORD", ["décimo", "10mo", "tenth"], 10),
    ]
    
    for id_c, palabras, posicion in ordinales:
        conceptos.append(ConceptoAnclado(
            id=id_c,
            tipo=TipoConcepto.PROPIEDAD,
            palabras_español=palabras,
            confianza_grounding=0.82,
            propiedades={
                "es_numero": True,
                "es_ordinal": True,
                "posicion": posicion,
            },
            relaciones={
                "tipo_de": {"NUMERO_ORDINAL"},
            },
        ))
    
    # ══════════ CANTIDADES RELATIVAS ════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MITAD",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["mitad", "half", "medio", "50%"],
        confianza_grounding=0.80,
        propiedades={
            "es_cantidad": True,
            "es_fraccion": True,
            "valor": 0.5,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TERCIO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["tercio", "tercera parte", "1/3"],
        confianza_grounding=0.78,
        propiedades={
            "es_cantidad": True,
            "es_fraccion": True,
            "valor": 0.33,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CUARTO_CANT",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["cuarto", "cuarta parte", "25%", "1/4"],
        confianza_grounding=0.78,
        propiedades={
            "es_cantidad": True,
            "es_fraccion": True,
            "valor": 0.25,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DOBLE",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["doble", "double", "dos veces", "2x"],
        confianza_grounding=0.80,
        propiedades={
            "es_cantidad": True,
            "es_multiplicador": True,
            "factor": 2,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TRIPLE",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["triple", "tres veces", "3x"],
        confianza_grounding=0.78,
        propiedades={
            "es_cantidad": True,
            "es_multiplicador": True,
            "factor": 3,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DECENA",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["decena", "diez", "10"],
        confianza_grounding=0.75,
        propiedades={
            "es_cantidad": True,
            "valor": 10,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DOCENA",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["docena", "dozen", "12"],
        confianza_grounding=0.78,
        propiedades={
            "es_cantidad": True,
            "valor": 12,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CENTENA",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["centena", "cien", "100"],
        confianza_grounding=0.75,
        propiedades={
            "es_cantidad": True,
            "valor": 100,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PORCENTAJE",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["porcentaje", "percent", "%", "por ciento"],
        confianza_grounding=0.80,
        propiedades={
            "es_cantidad": True,
            "es_proporcion": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CANTIDAD",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["cantidad", "amount", "número de"],
        confianza_grounding=0.78,
        propiedades={
            "es_cantidad": True,
            "es_abstracto": True,
        },
    ))
    
    # ══════════ OPERADORES ══════════════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MAS_OP",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["más", "plus", "+", "adicional"],
        confianza_grounding=0.82,
        propiedades={
            "es_operador": True,
            "operacion": "suma",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_MENOS_OP"},
            "relacionado_con": {"CONCEPTO_SUMA"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MENOS_OP",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["menos", "minus", "-", "restando"],
        confianza_grounding=0.82,
        propiedades={
            "es_operador": True,
            "operacion": "resta",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_MAS_OP"},
            "relacionado_con": {"CONCEPTO_RESTA"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_POR_OP",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["por", "times", "x", "multiplicado"],
        confianza_grounding=0.80,
        propiedades={
            "es_operador": True,
            "operacion": "multiplicacion",
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_MULTIPLICACION"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ENTRE_OP",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["entre", "dividido", "/", "divided by"],
        confianza_grounding=0.80,
        propiedades={
            "es_operador": True,
            "operacion": "division",
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_DIVISION"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_IGUAL_OP",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["igual", "equals", "=", "es igual a"],
        confianza_grounding=0.82,
        propiedades={
            "es_operador": True,
            "operacion": "igualdad",
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_IGUAL"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MAYOR_OP",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["mayor que", "greater than", ">", "más grande que"],
        confianza_grounding=0.80,
        propiedades={
            "es_operador": True,
            "operacion": "comparacion",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_MENOR_OP"},
            "relacionado_con": {"CONCEPTO_MAYOR"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MENOR_OP",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["menor que", "less than", "<", "más pequeño que"],
        confianza_grounding=0.80,
        propiedades={
            "es_operador": True,
            "operacion": "comparacion",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_MAYOR_OP"},
            "relacionado_con": {"CONCEPTO_MENOR"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PROMEDIO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["promedio", "average", "media", "mean"],
        confianza_grounding=0.78,
        propiedades={
            "es_operador": True,
            "es_estadistico": True,
        },
    ))
    
    # ══════════ UNIDADES DE MEDIDA ══════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_METRO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["metro", "m", "metros"],
        confianza_grounding=0.75,
        propiedades={
            "es_unidad": True,
            "tipo_medida": "longitud",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_KILOMETRO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["kilómetro", "km", "kilómetros"],
        confianza_grounding=0.75,
        propiedades={
            "es_unidad": True,
            "tipo_medida": "longitud",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_KILOGRAMO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["kilogramo", "kg", "kilo", "kilos"],
        confianza_grounding=0.75,
        propiedades={
            "es_unidad": True,
            "tipo_medida": "peso",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LITRO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["litro", "l", "litros"],
        confianza_grounding=0.75,
        propiedades={
            "es_unidad": True,
            "tipo_medida": "volumen",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_GRADO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["grado", "°", "grados"],
        confianza_grounding=0.72,
        propiedades={
            "es_unidad": True,
            "tipo_medida": "temperatura",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MEGABYTE",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["megabyte", "MB", "megas"],
        confianza_grounding=0.82,
        propiedades={
            "es_unidad": True,
            "tipo_medida": "datos",
            "es_digital": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_GIGABYTE",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["gigabyte", "GB", "gigas"],
        confianza_grounding=0.82,
        propiedades={
            "es_unidad": True,
            "tipo_medida": "datos",
            "es_digital": True,
        },
    ))
    
    return conceptos


if __name__ == '__main__':
    conceptos = obtener_conceptos_numeros_cantidades()
    grounding_prom = sum(c.confianza_grounding for c in conceptos) / len(conceptos)
    print(f"✅ Números y Cantidades: {len(conceptos)} conceptos")
    print(f"   Grounding promedio: {grounding_prom:.2f}")