"""
Adjetivos Básicos - Semana 2.

5 adjetivos comunes para describir conceptos.
Grounding medio (0.6-0.7) - descriptivos pero no operacionales.
"""
from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto

def obtener_conceptos_adjetivos():
    """Retorna adjetivos (5 conceptos)."""
    conceptos = []
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NUEVO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["nuevo", "nueva", "reciente"],
        confianza_grounding=0.7,
        propiedades={
            'es_adjetivo': True,
            'categoria': 'temporal',
            'opuesto': 'viejo'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_VIEJO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["viejo", "vieja", "antiguo", "antigua"],
        confianza_grounding=0.7,
        propiedades={
            'es_adjetivo': True,
            'categoria': 'temporal',
            'opuesto': 'nuevo'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_BUENO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["bueno", "buena", "correcto", "bien"],
        confianza_grounding=0.6,
        propiedades={
            'es_adjetivo': True,
            'categoria': 'cualidad',
            'valoracion': 'positiva'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MALO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["malo", "mala", "incorrecto", "mal"],
        confianza_grounding=0.6,
        propiedades={
            'es_adjetivo': True,
            'categoria': 'cualidad',
            'valoracion': 'negativa'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_GRANDE",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["grande", "mayor", "amplio", "extenso"],
        confianza_grounding=0.7,
        propiedades={
            'es_adjetivo': True,
            'categoria': 'tamaño',
            'opuesto': 'pequeño'
        }
    ))
    
    return conceptos