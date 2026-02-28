"""
Vocabulario Conversación Expandida - Semana 3 (VERSIÓN REFINADA).

30 conceptos conversacionales adicionales.
Grounding medio (0.6-0.8).

CAMBIOS EN ESTA VERSIÓN:
- ✅ SIN CAMBIOS: No tiene duplicados
- Todos los conceptos son únicos y bien definidos
"""
from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto

def obtener_conceptos_conversacion_expandida():
    """Retorna conceptos conversación (30 conceptos)."""
    conceptos = []
    
    # TIEMPO Y FRECUENCIA (8)
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_AHORA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["ahora", "now", "actualmente"],
        confianza_grounding=0.8,
        propiedades={
            'temporal': True,
            'presente': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DESPUES",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["después", "luego", "later"],
        confianza_grounding=0.8,
        propiedades={
            'temporal': True,
            'futuro': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ANTES",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["antes", "before", "previamente"],
        confianza_grounding=0.8,
        propiedades={
            'temporal': True,
            'pasado': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SIEMPRE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["siempre", "always"],
        confianza_grounding=0.7,
        propiedades={
            'frecuencia': 'constante'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NUNCA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["nunca", "never", "jamás"],
        confianza_grounding=0.7,
        propiedades={
            'frecuencia': 'cero'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_A_VECES",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["a veces", "sometimes"],
        confianza_grounding=0.7,
        propiedades={
            'frecuencia': 'ocasional'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FRECUENTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["frecuente", "often", "seguido"],
        confianza_grounding=0.7,
        propiedades={
            'frecuencia': 'alta'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RARO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["raro", "rare", "poco común"],
        confianza_grounding=0.7,
        propiedades={
            'frecuencia': 'baja'
        }
    ))
    
    # CANTIDAD Y COMPARACIÓN (8)
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MUCHO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["mucho", "muchos", "many"],
        confianza_grounding=0.8,
        propiedades={
            'cantidad': 'alta'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_POCO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["poco", "pocos", "few"],
        confianza_grounding=0.8,
        propiedades={
            'cantidad': 'baja'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NINGUNO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["ninguno", "ninguna", "none"],
        confianza_grounding=0.8,
        propiedades={
            'cantidad': 'cero'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ALGUNOS",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["algunos", "algunas", "some"],
        confianza_grounding=0.8,
        propiedades={
            'cantidad': 'indeterminada'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MAS",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["más", "more"],
        confianza_grounding=0.8,
        propiedades={
            'comparativo': True,
            'incremento': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MENOS",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["menos", "less"],
        confianza_grounding=0.8,
        propiedades={
            'comparativo': True,
            'decremento': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_IGUAL",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["igual", "same", "equivalente"],
        confianza_grounding=0.8,
        propiedades={
            'comparativo': True,
            'igualdad': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DIFERENTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["diferente", "different", "distinto"],
        confianza_grounding=0.8,
        propiedades={
            'comparativo': True,
            'desigualdad': True
        }
    ))
    
    # MODALIDAD Y POSIBILIDAD (8)
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DEBE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["debe", "deber", "should", "must"],
        confianza_grounding=0.7,
        propiedades={
            'modalidad': 'obligacion'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PUEDE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["puede", "podría", "might"],
        confianza_grounding=0.7,
        propiedades={
            'modalidad': 'posibilidad'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_QUIZA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["quizá", "quizás", "maybe", "tal vez"],
        confianza_grounding=0.7,
        propiedades={
            'certeza': 'media'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SEGURO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["seguro", "certainly", "definitivamente"],
        confianza_grounding=0.7,
        propiedades={
            'certeza': 'alta'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PROBABLE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["probable", "likely"],
        confianza_grounding=0.7,
        propiedades={
            'probabilidad': 'alta'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_POSIBLE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["posible", "possible"],
        confianza_grounding=0.7,
        propiedades={
            'probabilidad': 'existente'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_IMPOSIBLE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["imposible", "impossible"],
        confianza_grounding=0.7,
        propiedades={
            'probabilidad': 'cero'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DIFICIL",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["difícil", "difficult", "complicado"],
        confianza_grounding=0.7,
        propiedades={
            'complejidad': 'alta'
        }
    ))
    
    # EVALUACIÓN (6)
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CORRECTO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["correcto", "correct", "right"],
        confianza_grounding=0.8,
        propiedades={
            'evaluacion': 'positiva'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INCORRECTO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["incorrecto", "wrong", "equivocado"],
        confianza_grounding=0.8,
        propiedades={
            'evaluacion': 'negativa'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MEJOR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["mejor", "best", "óptimo"],
        confianza_grounding=0.7,
        propiedades={
            'comparativo_superlativo': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PEOR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["peor", "worst"],
        confianza_grounding=0.7,
        propiedades={
            'comparativo_superlativo': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RAPIDO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["rápido", "fast", "veloz"],
        confianza_grounding=0.8,
        propiedades={
            'velocidad': 'alta'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LENTO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["lento", "slow"],
        confianza_grounding=0.8,
        propiedades={
            'velocidad': 'baja'
        }
    ))
    
    return conceptos


if __name__ == '__main__':
    # Validación
    conceptos = obtener_conceptos_conversacion_expandida()
    print(f"✅ Vocabulario Conversación Expandida REFINADO: {len(conceptos)} conceptos")
    print(f"   Grounding promedio: {sum(c.confianza_grounding for c in conceptos) / len(conceptos):.2f}")