"""
Verbos Comunes - Semana 2 (VERSIÓN CORREGIDA v3 - Fase 4A).

10 verbos de acción frecuentes en conversación.
Grounding medio (0.7-0.8) - conceptos de acción sin operaciones directas.

═══════════════════════════════════════════════════════════════════════════════
CORRECCIONES FASE 4A:
- ✅ CONCEPTO_PREGUNTAR: ELIMINADO "consultar" (conflicto con HTTP_GET)
- ✅ CONCEPTO_TENER: ELIMINADO "contar" (conflicto con COUNT de BD)
- ✅ CONCEPTO_BUSCAR: ELIMINADO "encontrar", "localizar" (conflicto con FIND)
═══════════════════════════════════════════════════════════════════════════════
"""
from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto

def obtener_conceptos_verbos():
    """Retorna verbos comunes (10 conceptos - CORREGIDOS v3)."""
    conceptos = []
    
    # VERBOS DE NECESIDAD/DESEO (3)
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NECESITAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["necesitar", "necesito", "requiero", "preciso"],
        confianza_grounding=0.7,
        propiedades={
            'expresa_necesidad': True,
            'prioridad': 'alta'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_QUERER",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["querer", "quiero", "desear", "deseo"],
        confianza_grounding=0.7,
        propiedades={
            'expresa_deseo': True,
            'prioridad': 'media'
        }
    ))
    
    # ═══════════════════════════════════════════════════════════════════════
    # ✅ FIX: CONCEPTO_BUSCAR - ELIMINADO "encontrar", "localizar"
    #    Estas palabras ahora están SOLO en CONCEPTO_FIND (semana5_sistema)
    # ═══════════════════════════════════════════════════════════════════════
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_BUSCAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=[
            "buscar",        # ← Principal
            "búsqueda",      # ← Sustantivo
            "indagar"        # ← Alternativa cognitiva
            # "encontrar" ELIMINADO → CONCEPTO_FIND
            # "localizar" ELIMINADO → CONCEPTO_FIND
        ],
        confianza_grounding=0.8,
        propiedades={
            'es_busqueda': True,
            'retorna_resultado': True
        }
    ))
    
    # VERBOS DE COMUNICACIÓN (3)
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DECIR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["decir", "mencionar", "comentar", "expresar"],
        confianza_grounding=0.7,
        propiedades={
            'es_comunicacion': True,
            'direccion': 'salida'
        }
    ))
    
    # ═══════════════════════════════════════════════════════════════════════
    # ✅ FIX: CONCEPTO_PREGUNTAR - ELIMINADO "consultar"
    #    "consultar" ahora está SOLO en CONCEPTO_HTTP_GET (semana9_red)
    # ═══════════════════════════════════════════════════════════════════════
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PREGUNTAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=[
            "preguntar",     # ← Principal
            "cuestionar",    # ← Alternativa formal
            "interrogar"     # ← Alternativa
            # "consultar" ELIMINADO → CONCEPTO_HTTP_GET
        ],
        confianza_grounding=0.7,
        propiedades={
            'es_comunicacion': True,
            'requiere_respuesta': True
        },
        relaciones={'relacionado_con': {'CONCEPTO_PREGUNTA'}}
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["dar", "proporcionar", "proveer", "entregar"],
        confianza_grounding=0.7,
        propiedades={
            'es_transferencia': True,
            'direccion': 'hacia_otro'
        }
    ))
    
    # VERBOS DE PROCESO (4)
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_USAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["usar", "utilizar", "emplear"],
        confianza_grounding=0.8,
        propiedades={
            'es_uso': True,
            'requiere_objeto': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_VER",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["ver", "mirar", "observar", "revisar"],
        confianza_grounding=0.7,
        propiedades={
            'es_percepcion': True,
            'sentido': 'visual'
        }
    ))
    
    # ═══════════════════════════════════════════════════════════════════════
    # ✅ FIX: CONCEPTO_TENER - ELIMINADO "contar"
    #    "contar" ahora está SOLO en CONCEPTO_COUNT (semana10_bd)
    # ═══════════════════════════════════════════════════════════════════════
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TENER",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=[
            "tener",        # ← Principal
            "poseer",       # ← Alternativa
            "disponer"      # ← Alternativa formal
            # "contar" ELIMINADO → CONCEPTO_COUNT
        ],
        confianza_grounding=0.7,
        propiedades={
            'es_posesion': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_OBTENER",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["obtener", "conseguir", "adquirir", "lograr"],
        confianza_grounding=0.7,
        propiedades={
            'es_adquisicion': True,
            'cambia_estado': True
        }
    ))
    
    return conceptos


if __name__ == '__main__':
    conceptos = obtener_conceptos_verbos()
    print(f"✅ Vocabulario Verbos CORREGIDO v3: {len(conceptos)} conceptos")
    print(f"   ✅ CONCEPTO_PREGUNTAR sin 'consultar'")
    print(f"   ✅ CONCEPTO_TENER sin 'contar'")
    print(f"   ✅ CONCEPTO_BUSCAR sin 'encontrar/localizar'")
    print(f"   Grounding promedio: {sum(c.confianza_grounding for c in conceptos) / len(conceptos):.2f}")