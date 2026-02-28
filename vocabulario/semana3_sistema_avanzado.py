"""
Vocabulario Sistema Avanzado - Semana 3 (VERSIÓN CORREGIDA v4 - Fase 4A).

19 conceptos de operaciones sistema avanzadas.
Grounding medio-alto (0.7-0.9).

═══════════════════════════════════════════════════════════════════════════════
CORRECCIONES FASE 4A v4:
- ❌ ELIMINADO: CONCEPTO_CREAR_DIRECTORIO (duplicado con CONCEPTO_MKDIR)
- ❌ ELIMINADO: CONCEPTO_RUTA (duplicado con CONCEPTO_PATH de semana5)
- ✅ CONCEPTO_PAUSAR: Palabras específicas código (sin "pausar", "pause")
- ✅ CONCEPTO_TERMINAR: Sin "kill" (conflicto con CONCEPTO_KILL)
- ✅ CONCEPTO_FECHA_MODIFICACION: Sin "timestamp" (conflicto con DATE)

Total anterior: 22 → Total actual: 19 conceptos
═══════════════════════════════════════════════════════════════════════════════
"""
from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto

def obtener_conceptos_sistema_avanzado():
    """Retorna conceptos sistema avanzado (19 conceptos - SIN DUPLICADOS v4)."""
    conceptos = []
    
    # ==================== OPERACIONES FILESYSTEM (7) ====================
    # NOTA: CONCEPTO_CREAR_DIRECTORIO eliminado → usar CONCEPTO_MKDIR de semana5
    # NOTA: CONCEPTO_RUTA eliminado → usar CONCEPTO_PATH de semana5
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_COPIAR",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["copiar", "copy", "duplicar"],
        confianza_grounding=0.9,
        propiedades={
            'modifica_sistema': True,
            'crea_archivo': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MOVER",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["mover", "move", "renombrar"],
        confianza_grounding=0.9,
        propiedades={
            'modifica_sistema': True,
            'cambia_ubicacion': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ABSOLUTA",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["absoluta", "absolute", "ruta completa"],
        confianza_grounding=0.8,
        propiedades={
            'desde_raiz': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RELATIVA",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["relativa", "relative"],
        confianza_grounding=0.8,
        propiedades={
            'desde_actual': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NOMBRE_ARCHIVO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["nombre", "filename", "nombre archivo"],
        confianza_grounding=0.9,
        propiedades={
            'identifica_archivo': True
        }
    ))
    
    # ═══════════════════════════════════════════════════════════════════════
    # ✅ FIX: CONCEPTO_FECHA_MODIFICACION - ELIMINADO "timestamp"
    #    "timestamp" ahora está SOLO en CONCEPTO_DATE (semana5_sistema)
    # ═══════════════════════════════════════════════════════════════════════
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FECHA_MODIFICACION",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=[
            "fecha modificación",  # ← Principal
            "mtime",               # ← Técnico Unix
            "última modificación"  # ← Alternativa
            # "timestamp" ELIMINADO → CONCEPTO_DATE
        ],
        confianza_grounding=0.8,
        propiedades={
            'es_metadata': True,
            'es_datetime': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DISCO",
        tipo=TipoConcepto.ENTIDAD_DIGITAL,
        palabras_español=["disco", "disk", "almacenamiento"],
        confianza_grounding=0.9,
        propiedades={
            'es_hardware': True,
            'persistente': True
        }
    ))
    
    # ==================== OPERACIONES PROCESO (4) ====================
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_THREAD",
        tipo=TipoConcepto.ENTIDAD_DIGITAL,
        palabras_español=["thread", "hilo"],
        confianza_grounding=0.7,
        propiedades={
            'concurrente': True,
            'comparte_memoria': True
        }
    ))
    
    # ═══════════════════════════════════════════════════════════════════════
    # ✅ FIX: CONCEPTO_TERMINAR - ELIMINADO "kill"
    #    "kill" ahora está SOLO en CONCEPTO_KILL (semana5_sistema)
    # ═══════════════════════════════════════════════════════════════════════
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TERMINAR",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "terminar",      # ← Principal
            "detener",       # ← Alternativa
            "finalizar"      # ← Alternativa formal
            # "kill" ELIMINADO → CONCEPTO_KILL
        ],
        confianza_grounding=0.8,
        propiedades={
            'finaliza_proceso': True,
            'puede_fallar': True
        }
    ))
    
    # ═══════════════════════════════════════════════════════════════════════
    # ✅ FIX: CONCEPTO_PAUSAR - Palabras específicas para código/programación
    #    "pausar"/"pause" genéricos → CONCEPTO_PAUSAR_PLAN (semana8)
    # ═══════════════════════════════════════════════════════════════════════
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PAUSAR",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "sleep",              # ← Específico código
            "esperar",            # ← Alternativa
            "pausar ejecución",   # ← Específico código
            "delay"               # ← Técnico
            # "pausar"/"pause" genéricos → CONCEPTO_PAUSAR_PLAN
        ],
        confianza_grounding=0.9,
        propiedades={
            'detiene_ejecucion': True,
            'temporal': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_REANUDAR",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["reanudar", "resume", "continuar"],
        confianza_grounding=0.8,
        propiedades={
            'continua_ejecucion': True
        }
    ))
    
    # ==================== OPERACIONES TEXTO (8) ====================
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_REEMPLAZAR",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["reemplazar", "replace", "sustituir"],
        confianza_grounding=0.9,
        propiedades={
            'modifica_texto': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DIVIDIR",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["dividir", "split", "separar"],
        confianza_grounding=0.9,
        propiedades={
            'retorna_lista': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_UNIR",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["unir", "join", "concatenar"],
        confianza_grounding=0.9,
        propiedades={
            'combina_elementos': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MAYUSCULAS",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["mayúsculas", "upper", "uppercase"],
        confianza_grounding=0.9,
        propiedades={
            'modifica_texto': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MINUSCULAS",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["minúsculas", "lower", "lowercase"],
        confianza_grounding=0.9,
        propiedades={
            'modifica_texto': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_STRIP",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["strip", "limpiar", "trim"],
        confianza_grounding=0.9,
        propiedades={
            'elimina_espacios': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FORMATO",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["formato", "format", "formatear"],
        confianza_grounding=0.9,
        propiedades={
            'inserta_valores': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ENCODING",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["encoding", "codificación", "utf-8"],
        confianza_grounding=0.8,
        propiedades={
            'representa_caracteres': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_REGEX",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["regex", "expresión regular", "pattern"],
        confianza_grounding=0.7,
        propiedades={
            'patron_busqueda': True,
            'complejo': True
        }
    ))
    
    return conceptos


if __name__ == '__main__':
    conceptos = obtener_conceptos_sistema_avanzado()
    print(f"✅ Vocabulario Sistema Avanzado CORREGIDO v4: {len(conceptos)} conceptos")
    print(f"   ❌ ELIMINADO: CONCEPTO_CREAR_DIRECTORIO → usar CONCEPTO_MKDIR")
    print(f"   ❌ ELIMINADO: CONCEPTO_RUTA → usar CONCEPTO_PATH")
    print(f"   ✅ CONCEPTO_PAUSAR sin 'pausar/pause'")
    print(f"   ✅ CONCEPTO_TERMINAR sin 'kill'")
    print(f"   ✅ CONCEPTO_FECHA_MODIFICACION sin 'timestamp'")
    print(f"   Grounding promedio: {sum(c.confianza_grounding for c in conceptos) / len(conceptos):.2f}")