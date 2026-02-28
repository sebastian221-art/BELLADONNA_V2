"""
Conceptos Matemáticos - Semana 3 (VERSIÓN REFINADA v2).

20 conceptos de operaciones y términos matemáticos.

CAMBIOS EN ESTA VERSIÓN v2:
- ✅ Renombrados SUMA, RESTA, MULTIPLICACION, DIVISION (eran SUMAR, RESTAR...)
- ✅ Sin "antiderivada" (reservada para semana7)
- ✅ CONCEPTO_NEGATIVO: Solo "negativo", "menor que cero" (sin conflicto con "no")
"""
from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto

def obtener_conceptos_matematicas():
    """Retorna conceptos matemáticos (20 conceptos - REFINADOS v2)."""
    conceptos = []
    
    # OPERACIONES BÁSICAS (4)
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SUMA",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["suma", "sumar", "adición", "más"],
        confianza_grounding=0.85,
        propiedades={
            'es_operacion': True,
            'simbolo': '+',
            'conmutativa': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RESTA",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["resta", "restar", "sustracción", "menos"],
        confianza_grounding=0.85,
        propiedades={
            'es_operacion': True,
            'simbolo': '-',
            'conmutativa': False
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MULTIPLICACION",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["multiplicación", "multiplicar", "producto", "por"],
        confianza_grounding=0.85,
        propiedades={
            'es_operacion': True,
            'simbolo': '*',
            'conmutativa': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DIVISION",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["división", "dividir", "cociente", "entre"],
        confianza_grounding=0.85,
        propiedades={
            'es_operacion': True,
            'simbolo': '/',
            'conmutativa': False,
            'puede_error': True
        }
    ))
    
    # TÉRMINOS NUMÉRICOS (4)
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ENTERO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["entero", "integer", "número entero"],
        confianza_grounding=0.80,
        propiedades={
            'es_tipo_numerico': True,
            'tiene_decimales': False
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DECIMAL",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["decimal", "flotante", "float", "número decimal"],
        confianza_grounding=0.80,
        propiedades={
            'es_tipo_numerico': True,
            'tiene_decimales': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_POSITIVO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["positivo", "mayor que cero", "número positivo"],
        confianza_grounding=0.75,
        propiedades={
            'es_signo': True,
            'valor': '> 0'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NEGATIVO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["negativo", "menor que cero", "número negativo"],  # ← Específico
        confianza_grounding=0.75,
        propiedades={
            'es_signo': True,
            'valor': '< 0'
        }
    ))
    
    # OPERACIONES AVANZADAS (6)
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_POTENCIA",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["potencia", "exponente", "elevado", "power"],
        confianza_grounding=0.80,
        propiedades={
            'es_operacion': True,
            'simbolo': '**'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RAIZ",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["raíz", "raíz cuadrada", "sqrt", "square root"],
        confianza_grounding=0.80,
        propiedades={
            'es_operacion': True,
            'inversa_de': 'potencia'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MODULO",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["módulo", "resto", "mod", "residuo"],
        confianza_grounding=0.80,
        propiedades={
            'es_operacion': True,
            'simbolo': '%',
            'retorna': 'resto'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ABS",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["absoluto", "abs", "valor absoluto"],
        confianza_grounding=0.80,
        propiedades={
            'es_funcion': True,
            'retorna': 'positivo'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_REDONDEO",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["redondear", "round", "aproximar"],
        confianza_grounding=0.75,
        propiedades={
            'es_funcion': True,
            'modifica_precision': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MAXIMO",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["máximo", "max", "mayor valor"],
        confianza_grounding=0.80,
        propiedades={
            'es_comparacion': True,
            'retorna': 'mayor_valor'
        }
    ))
    
    # CONCEPTOS ESTADÍSTICOS (6)
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PROMEDIO",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["promedio", "media", "average"],
        confianza_grounding=0.75,
        propiedades={
            'es_estadistica': True,
            'requiere': 'lista_numeros'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MINIMO",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["mínimo", "min", "menor valor"],
        confianza_grounding=0.80,
        propiedades={
            'es_comparacion': True,
            'retorna': 'menor_valor'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RANGO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["rango", "range", "intervalo"],
        confianza_grounding=0.75,
        propiedades={
            'tiene_inicio': True,
            'tiene_fin': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PORCENTAJE",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["porcentaje", "por ciento", "percent"],
        confianza_grounding=0.75,
        propiedades={
            'simbolo': '%',
            'base': 100
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FRACCION",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["fracción", "quebrado", "racional"],
        confianza_grounding=0.70,
        propiedades={
            'tiene_numerador': True,
            'tiene_denominador': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ECUACION",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["ecuación", "igualdad", "fórmula"],
        confianza_grounding=0.70,
        propiedades={
            'tiene_variables': True,
            'tiene_igualdad': True
        }
    ))
    
    return conceptos


if __name__ == '__main__':
    conceptos = obtener_conceptos_matematicas()
    print(f"✅ Vocabulario Matemáticas REFINADO v2: {len(conceptos)} conceptos")
    print(f"   Grounding promedio: {sum(c.confianza_grounding for c in conceptos) / len(conceptos):.2f}")