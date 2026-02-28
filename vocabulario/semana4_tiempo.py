"""
Conceptos de Tiempo y Temporalidad - Semana 4 (VERSIÓN REFINADA).

10 conceptos relacionados con tiempo, fechas, duraciones.
Grounding medio (0.70-0.80).

CAMBIOS EN ESTA VERSIÓN:
- ❌ ELIMINADO: CONCEPTO_AHORA (ya en semana3_conversacion_expandida)
- ❌ ELIMINADO: CONCEPTO_ANTES (ya en semana3_conversacion_expandida)
- ❌ ELIMINADO: CONCEPTO_DESPUES (ya en semana3_conversacion_expandida)
- ❌ ELIMINADO: CONCEPTO_SIEMPRE (ya en semana3_conversacion_expandida)
- ❌ ELIMINADO: CONCEPTO_NUNCA (ya en semana3_conversacion_expandida)
- ❌ ELIMINADO: CONCEPTO_HORA (duplicado con CONCEPTO_DATE en semana5)
- ✅ Total: 10 conceptos únicos
"""
from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto

def obtener_conceptos_tiempo():
    """Retorna conceptos de tiempo (10 conceptos - SIN DUPLICADOS)."""
    conceptos = []
    
    # MOMENTOS TEMPORALES (3)
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_HOY",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["hoy", "today"],
        confianza_grounding=0.90,  # ← OPTIMIZADO de 0.80 a 0.90
        propiedades={
            'es_temporal': True,
            'relativo': True,
            'precision': 'dia'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_AYER",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["ayer", "yesterday"],
        confianza_grounding=0.90,  # ← OPTIMIZADO de 0.80 a 0.90
        propiedades={
            'es_temporal': True,
            'relativo': True,
            'direccion': 'pasado'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MAÑANA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["mañana", "tomorrow"],
        confianza_grounding=0.90,  # ← OPTIMIZADO de 0.80 a 0.90
        propiedades={
            'es_temporal': True,
            'relativo': True,
            'direccion': 'futuro'
        }
    ))
    
    # DURACIONES (5)
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SEGUNDO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["segundo", "segundos"],
        confianza_grounding=0.75,
        propiedades={
            'es_unidad_tiempo': True,
            'duracion_segundos': 1
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MINUTO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["minuto", "minutos"],
        confianza_grounding=0.75,
        propiedades={
            'es_unidad_tiempo': True,
            'duracion_segundos': 60
        }
    ))
    
    # CONCEPTO_HORA eliminado - duplicado con CONCEPTO_DATE en semana5
    # Usar CONCEPTO_DATE para consultas de hora/timestamp
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DIA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["día", "dias"],
        confianza_grounding=0.75,
        propiedades={
            'es_unidad_tiempo': True,
            'duracion_segundos': 86400
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SEMANA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["semana", "semanas"],
        confianza_grounding=0.75,
        propiedades={
            'es_unidad_tiempo': True,
            'duracion_segundos': 604800
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MES",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["mes", "meses", "month"],
        confianza_grounding=0.75,
        propiedades={
            'es_unidad_tiempo': True,
            'duracion_aproximada_segundos': 2592000  # ~30 días
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_AÑO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["año", "años", "year"],
        confianza_grounding=0.75,
        propiedades={
            'es_unidad_tiempo': True,
            'duracion_segundos': 31536000  # 365 días
        }
    ))
    
    # VELOCIDAD/FRECUENCIA TEMPORAL (2)
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RAPIDO_TIEMPO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["pronto", "rápido en el tiempo", "soon"],
        confianza_grounding=0.70,
        propiedades={
            'es_velocidad_temporal': True,
            'valor': 'alto'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LENTO_TIEMPO",
        tipo=TipoConcepto.PROPIEDAD,
        palabras_español=["tarde", "despacio en el tiempo", "slowly"],
        confianza_grounding=0.70,
        propiedades={
            'es_velocidad_temporal': True,
            'valor': 'bajo'
        }
    ))
    
    return conceptos


if __name__ == '__main__':
    # Validación
    conceptos = obtener_conceptos_tiempo()
    print(f"✅ Vocabulario Tiempo REFINADO: {len(conceptos)} conceptos")
    print(f"   Grounding promedio: {sum(c.confianza_grounding for c in conceptos) / len(conceptos):.2f}")