"""
Conceptos de Acciones Cotidianas - Semana 4.

10 conceptos de acciones físicas y cotidianas.
Grounding medio (0.65-0.75) - Bell entiende el concepto pero no puede ejecutar físicamente.
"""
from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto

def obtener_conceptos_acciones():
    """Retorna conceptos de acciones (10 conceptos)."""
    conceptos = []
    
    # ACCIONES FÍSICAS BÁSICAS (5)
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CAMINAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["caminar", "andar", "walk"],
        confianza_grounding=0.65,
        propiedades={
            'es_accion_fisica': True,
            'requiere_cuerpo': True,
            'velocidad': 'media'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CORRER",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["correr", "run"],
        confianza_grounding=0.65,
        propiedades={
            'es_accion_fisica': True,
            'requiere_cuerpo': True,
            'velocidad': 'alta'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DORMIR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["dormir", "descansar", "sleep"],
        confianza_grounding=0.70,
        propiedades={
            'es_estado': True,
            'requiere_cuerpo': True,
            'duracion': 'horas'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_COMER",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["comer", "eat"],
        confianza_grounding=0.70,
        propiedades={
            'es_accion_fisica': True,
            'requiere_cuerpo': True,
            'es_necesidad': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_BEBER",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["beber", "tomar", "drink"],
        confianza_grounding=0.70,
        propiedades={
            'es_accion_fisica': True,
            'requiere_cuerpo': True,
            'es_necesidad': True
        }
    ))
    
    # ACCIONES DE COMUNICACIÓN (3)
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_HABLAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["hablar", "conversar", "speak"],
        confianza_grounding=0.75,
        propiedades={
            'es_comunicacion': True,
            'medio': 'voz',
            'requiere_lenguaje': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ESCUCHAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["escuchar", "oír", "listen"],
        confianza_grounding=0.75,
        propiedades={
            'es_percepcion': True,
            'sentido': 'auditivo',
            'requiere_atencion': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MIRAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["mirar", "ver", "look", "watch"],
        confianza_grounding=0.75,
        propiedades={
            'es_percepcion': True,
            'sentido': 'visual',
            'requiere_atencion': True
        }
    ))
    
    # ACCIONES MENTALES (2)
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RECORDAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["recordar", "acordarse", "remember"],
        confianza_grounding=0.70,
        propiedades={
            'es_mental': True,
            'requiere_memoria': True,
            'tiempo': 'pasado'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_OLVIDAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["olvidar", "forget"],
        confianza_grounding=0.70,
        propiedades={
            'es_mental': True,
            'afecta_memoria': True,
            'opuesto': 'recordar'
        }
    ))
    
    return conceptos