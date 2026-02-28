"""
Conceptos de Operaciones del Sistema - Semana 1 - VERSIÓN CORREGIDA v3.

5 conceptos fundamentales con grounding 1.0.
Estos son operaciones que Bell PUEDE ejecutar directamente.

═══════════════════════════════════════════════════════════════════════════════
CORRECCIONES FASE 4A:
- ✅ CONCEPTO_ARCHIVO: ELIMINADO "file" (conflicto con CONCEPTO_FILE de shell)
     Ahora usa: "archivo", "documento", "fichero"
═══════════════════════════════════════════════════════════════════════════════
"""
from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto
from core.capacidades_bell import CapacidadesBell


def obtener_conceptos_operaciones():
    """
    Retorna conceptos de operaciones (5 conceptos).
    
    Todos tienen grounding 1.0 porque Bell puede ejecutarlos.
    """
    conceptos = []
    
    # 1. CONCEPTO_LEER
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LEER",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["leer", "read", "cargar"],
        operaciones={
            'ejecutar': CapacidadesBell.leer_archivo,
            'verificar': CapacidadesBell.archivo_existe
        },
        accesible_directamente=True,
        confianza_grounding=1.0,
        relaciones={'requiere': {'CONCEPTO_ARCHIVO'}},
        propiedades={
            'retorna': 'texto',
            'puede_fallar': True,
            'requiere_permisos': True
        }
    ))
    
    # 2. CONCEPTO_ESCRIBIR
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ESCRIBIR",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["escribir", "write", "guardar"],
        operaciones={'ejecutar': CapacidadesBell.escribir_archivo},
        accesible_directamente=True,
        confianza_grounding=1.0,
        relaciones={'requiere': {'CONCEPTO_ARCHIVO'}},
        propiedades={
            'retorna': 'booleano',
            'puede_fallar': True,
            'modifica_sistema': True
        }
    ))
    
    # ═══════════════════════════════════════════════════════════════════════
    # ✅ FIX: CONCEPTO_ARCHIVO - ELIMINADO "file"
    #    "file" ahora está SOLO en CONCEPTO_FILE (comando shell para detectar tipo)
    # ═══════════════════════════════════════════════════════════════════════
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ARCHIVO",
        tipo=TipoConcepto.ENTIDAD_DIGITAL,
        palabras_español=[
            "archivo",     # ← Principal en español
            "documento",   # ← Alternativa común
            "fichero"      # ← Alternativa (España)
            # "file" ELIMINADO - conflicto con CONCEPTO_FILE (comando shell)
        ],
        operaciones={
            'existe': CapacidadesBell.archivo_existe,
            'tamaño': CapacidadesBell.obtener_tamaño_archivo
        },
        accesible_directamente=True,
        confianza_grounding=1.0,
        propiedades={
            'es_fisico': False,
            'es_digital': True
        }
    ))
    
    # 4. CONCEPTO_DIRECTORIO
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DIRECTORIO",
        tipo=TipoConcepto.ENTIDAD_DIGITAL,
        palabras_español=["directorio", "carpeta", "folder"],
        operaciones={'listar': CapacidadesBell.listar_directorio},
        accesible_directamente=True,
        confianza_grounding=1.0,
        relaciones={'contiene': {'CONCEPTO_ARCHIVO'}},
        propiedades={
            'es_contenedor': True
        }
    ))
    
    # 5. CONCEPTO_EXISTE
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EXISTE",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["existe", "hay", "está"],
        operaciones={'verificar': CapacidadesBell.archivo_existe},
        accesible_directamente=True,
        confianza_grounding=1.0,
        propiedades={
            'retorna': 'booleano',
            'es_verificacion': True
        }
    ))
    
    return conceptos


if __name__ == '__main__':
    conceptos = obtener_conceptos_operaciones()
    print(f"✅ Vocabulario Operaciones CORREGIDO v3: {len(conceptos)} conceptos")
    print(f"   ✅ CONCEPTO_ARCHIVO sin 'file' (ya no hay conflicto)")
    print(f"   ✅ 'file' → CONCEPTO_FILE (comando shell)")
    print(f"   Todos con grounding 1.0 (ejecutables)")