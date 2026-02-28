"""
Conectores y Preposiciones - Semana 2.

10 palabras funcionales que conectan conceptos.
Grounding bajo (0.5-0.7) - son estructurales, no operacionales.
"""
from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto

def obtener_conceptos_conectores():
    """Retorna conectores (10 conceptos)."""
    conceptos = []
    
    # PREPOSICIONES BÁSICAS (6)
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PARA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["para", "hacia"],
        confianza_grounding=0.6,
        propiedades={
            'es_preposicion': True,
            'indica': 'proposito'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CON",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["con"],
        confianza_grounding=0.6,
        propiedades={
            'es_preposicion': True,
            'indica': 'compañia'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SIN",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["sin"],
        confianza_grounding=0.6,
        propiedades={
            'es_preposicion': True,
            'indica': 'ausencia'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SOBRE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["sobre", "acerca"],
        confianza_grounding=0.6,
        propiedades={
            'es_preposicion': True,
            'indica': 'tema'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EN",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["en"],
        confianza_grounding=0.6,
        propiedades={
            'es_preposicion': True,
            'indica': 'ubicacion'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["de"],
        confianza_grounding=0.6,
        propiedades={
            'es_preposicion': True,
            'indica': 'pertenencia'
        }
    ))
    
    # CONJUNCIONES (2)
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_Y",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["y", "e"],
        confianza_grounding=0.7,
        propiedades={
            'es_conjuncion': True,
            'tipo': 'aditiva'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_O",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["o", "u"],
        confianza_grounding=0.7,
        propiedades={
            'es_conjuncion': True,
            'tipo': 'disyuntiva'
        }
    ))
    
    # DETERMINANTES (2)
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ESTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["este", "esta", "esto", "estos", "estas"],
        confianza_grounding=0.6,
        propiedades={
            'es_determinante': True,
            'distancia': 'cercano'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ESE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["ese", "esa", "eso", "esos", "esas", "aquel", "aquella"],
        confianza_grounding=0.6,
        propiedades={
            'es_determinante': True,
            'distancia': 'lejano'
        }
    ))
    
    return conceptos