"""
Conceptos de Acciones - Semana 1 (VERSIÓN REFINADA v2).

3 conceptos de acciones básicas únicas.

CAMBIOS EN ESTA VERSIÓN v2:
- ✅ CONCEPTO_ELIMINAR: Eliminada "delete" (usada en HTTP)
- ✅ CONCEPTO_MODIFICAR: Mantiene "actualizar" aquí (HTTP usa "update")
- ✅ CONCEPTO_RESPUESTA: Mantiene "respuesta" (HTTP usa "response" o "respuesta http")
"""
from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto

def obtener_conceptos_acciones():
    """Retorna conceptos de acciones (3 conceptos - REFINADOS v2)."""
    conceptos = []
    
    # ACCIONES BÁSICAS (3 conceptos únicos)
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MODIFICAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["modificar", "cambiar", "editar", "actualizar"],
        confianza_grounding=0.8,
        propiedades={
            'es_accion_destructiva': False,
            'requiere_confirmacion': False
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ELIMINAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["eliminar", "borrar", "remover", "quitar"],  # ← Sin "delete"
        confianza_grounding=0.8,
        propiedades={
            'es_accion_destructiva': True,
            'requiere_confirmacion': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RESPUESTA",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["respuesta", "responder", "contestar", "reply"],
        confianza_grounding=0.7,
        propiedades={
            'es_interaccion': True
        },
        relaciones={'responde_a': {'CONCEPTO_PREGUNTAR'}}
    ))
    
    return conceptos


if __name__ == '__main__':
    conceptos = obtener_conceptos_acciones()
    print(f"✅ Vocabulario Acciones REFINADO v2: {len(conceptos)} conceptos")
    print(f"   Grounding promedio: {sum(c.confianza_grounding for c in conceptos) / len(conceptos):.2f}")