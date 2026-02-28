"""
Expresiones de Tiempo - Expansión Fase 4A.

Vocabulario temporal para conversación natural.

Conceptos: 60 total
Grounding promedio: 0.75
Tipo: PALABRA_CONVERSACION (expresiones temporales)
"""
from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto


def obtener_conceptos_expresiones_tiempo():
    """
    Retorna expresiones de tiempo.
    
    Tipo: PALABRA_CONVERSACION
    Grounding: 0.70-0.80 (Bell reconoce bien contexto temporal)
    
    Categorías:
    - Momentos del día (8 conceptos)
    - Días de la semana (8 conceptos)
    - Meses (12 conceptos)
    - Estaciones (4 conceptos)
    - Frecuencias (10 conceptos)
    - Referencias temporales (10 conceptos)
    - Duraciones (8 conceptos)
    """
    conceptos = []
    
    # ══════════ MOMENTOS DEL DÍA ════════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_AHORA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["ahora", "now", "en este momento", "ya", "ahorita"],
        confianza_grounding=0.80,
        propiedades={
            "es_expresion_temporal": True,
            "referencia": "presente",
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_DATE"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_HOY",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["hoy", "today", "este día"],
        confianza_grounding=0.80,
        propiedades={
            "es_expresion_temporal": True,
            "referencia": "dia_actual",
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_DATE"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_AYER",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["ayer", "yesterday"],
        confianza_grounding=0.78,
        propiedades={
            "es_expresion_temporal": True,
            "referencia": "dia_anterior",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MANANA_TIEMPO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["mañana", "tomorrow"],
        confianza_grounding=0.78,
        propiedades={
            "es_expresion_temporal": True,
            "referencia": "dia_siguiente",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MANANA_PARTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["por la mañana", "morning", "am", "en la mañana"],
        confianza_grounding=0.75,
        propiedades={
            "es_expresion_temporal": True,
            "parte_dia": "mañana",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TARDE_TIEMPO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["por la tarde", "afternoon", "en la tarde"],
        confianza_grounding=0.75,
        propiedades={
            "es_expresion_temporal": True,
            "parte_dia": "tarde",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NOCHE_TIEMPO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["por la noche", "night", "en la noche", "de noche"],
        confianza_grounding=0.75,
        propiedades={
            "es_expresion_temporal": True,
            "parte_dia": "noche",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MEDIODIA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["mediodía", "noon", "las doce"],
        confianza_grounding=0.75,
        propiedades={
            "es_expresion_temporal": True,
            "parte_dia": "mediodia",
        },
    ))
    
    # ══════════ DÍAS DE LA SEMANA ═══════════════════════════════
    
    dias = [
        ("CONCEPTO_LUNES", ["lunes", "monday"]),
        ("CONCEPTO_MARTES", ["martes", "tuesday"]),
        ("CONCEPTO_MIERCOLES", ["miércoles", "wednesday"]),
        ("CONCEPTO_JUEVES", ["jueves", "thursday"]),
        ("CONCEPTO_VIERNES", ["viernes", "friday"]),
        ("CONCEPTO_SABADO", ["sábado", "saturday"]),
        ("CONCEPTO_DOMINGO", ["domingo", "sunday"]),
    ]
    
    for id_c, palabras in dias:
        conceptos.append(ConceptoAnclado(
            id=id_c,
            tipo=TipoConcepto.PALABRA_CONVERSACION,
            palabras_español=palabras,
            confianza_grounding=0.78,
            propiedades={
                "es_expresion_temporal": True,
                "es_dia_semana": True,
            },
            relaciones={
                "tipo_de": {"DIA_SEMANA"},
            },
        ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FIN_SEMANA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["fin de semana", "weekend", "finde"],
        confianza_grounding=0.75,
        propiedades={
            "es_expresion_temporal": True,
        },
    ))
    
    # ══════════ MESES ═══════════════════════════════════════════
    
    meses = [
        ("CONCEPTO_ENERO", ["enero", "january"]),
        ("CONCEPTO_FEBRERO", ["febrero", "february"]),
        ("CONCEPTO_MARZO", ["marzo", "march"]),
        ("CONCEPTO_ABRIL", ["abril", "april"]),
        ("CONCEPTO_MAYO", ["mayo", "may"]),
        ("CONCEPTO_JUNIO", ["junio", "june"]),
        ("CONCEPTO_JULIO", ["julio", "july"]),
        ("CONCEPTO_AGOSTO", ["agosto", "august"]),
        ("CONCEPTO_SEPTIEMBRE", ["septiembre", "september"]),
        ("CONCEPTO_OCTUBRE", ["octubre", "october"]),
        ("CONCEPTO_NOVIEMBRE", ["noviembre", "november"]),
        ("CONCEPTO_DICIEMBRE", ["diciembre", "december"]),
    ]
    
    for id_c, palabras in meses:
        conceptos.append(ConceptoAnclado(
            id=id_c,
            tipo=TipoConcepto.PALABRA_CONVERSACION,
            palabras_español=palabras,
            confianza_grounding=0.78,
            propiedades={
                "es_expresion_temporal": True,
                "es_mes": True,
            },
            relaciones={
                "tipo_de": {"MES"},
            },
        ))
    
    # ══════════ ESTACIONES ══════════════════════════════════════
    
    estaciones = [
        ("CONCEPTO_PRIMAVERA", ["primavera", "spring"]),
        ("CONCEPTO_VERANO", ["verano", "summer"]),
        ("CONCEPTO_OTONO", ["otoño", "autumn", "fall"]),
        ("CONCEPTO_INVIERNO", ["invierno", "winter"]),
    ]
    
    for id_c, palabras in estaciones:
        conceptos.append(ConceptoAnclado(
            id=id_c,
            tipo=TipoConcepto.PALABRA_CONVERSACION,
            palabras_español=palabras,
            confianza_grounding=0.75,
            propiedades={
                "es_expresion_temporal": True,
                "es_estacion": True,
            },
        ))
    
    # ══════════ FRECUENCIAS ═════════════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SIEMPRE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["siempre", "always", "todo el tiempo", "constantemente"],
        confianza_grounding=0.78,
        propiedades={
            "es_frecuencia": True,
            "frecuencia": "maxima",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_NUNCA"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NUNCA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["nunca", "never", "jamás", "en ningún momento"],
        confianza_grounding=0.78,
        propiedades={
            "es_frecuencia": True,
            "frecuencia": "minima",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_SIEMPRE"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_A_VECES",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["a veces", "sometimes", "ocasionalmente", "de vez en cuando"],
        confianza_grounding=0.75,
        propiedades={
            "es_frecuencia": True,
            "frecuencia": "intermedia",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FRECUENTEMENTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["frecuentemente", "often", "a menudo", "seguido"],
        confianza_grounding=0.75,
        propiedades={
            "es_frecuencia": True,
            "frecuencia": "alta",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RARAMENTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["raramente", "rarely", "rara vez", "casi nunca"],
        confianza_grounding=0.75,
        propiedades={
            "es_frecuencia": True,
            "frecuencia": "baja",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DIARIAMENTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["diariamente", "daily", "cada día", "todos los días"],
        confianza_grounding=0.78,
        propiedades={
            "es_frecuencia": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SEMANALMENTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["semanalmente", "weekly", "cada semana"],
        confianza_grounding=0.75,
        propiedades={
            "es_frecuencia": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MENSUALMENTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["mensualmente", "monthly", "cada mes"],
        confianza_grounding=0.75,
        propiedades={
            "es_frecuencia": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ANUALMENTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["anualmente", "yearly", "cada año"],
        confianza_grounding=0.75,
        propiedades={
            "es_frecuencia": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_REGULARMENTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["regularmente", "regularly", "con regularidad"],
        confianza_grounding=0.72,
        propiedades={
            "es_frecuencia": True,
        },
    ))
    
    # ══════════ REFERENCIAS TEMPORALES ══════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ANTES",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["antes", "previamente", "anteriormente", "prior"],
        confianza_grounding=0.78,
        propiedades={
            "es_expresion_temporal": True,
            "direccion": "pasado",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_DESPUES"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DESPUES",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["después", "luego", "posteriormente", "after"],
        confianza_grounding=0.78,
        propiedades={
            "es_expresion_temporal": True,
            "direccion": "futuro",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_ANTES"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PRONTO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["pronto", "soon", "en breve", "dentro de poco"],
        confianza_grounding=0.72,
        propiedades={
            "es_expresion_temporal": True,
            "direccion": "futuro_cercano",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TARDE_ADV",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["tarde", "late", "con retraso"],
        confianza_grounding=0.72,
        propiedades={
            "es_expresion_temporal": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_TEMPRANO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TEMPRANO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["temprano", "early", "con anticipación"],
        confianza_grounding=0.72,
        propiedades={
            "es_expresion_temporal": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_TARDE_ADV"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TODAVIA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["todavía", "still", "aún", "hasta ahora"],
        confianza_grounding=0.75,
        propiedades={
            "es_expresion_temporal": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_YA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["ya", "already", "ya no"],
        confianza_grounding=0.75,
        propiedades={
            "es_expresion_temporal": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MIENTRAS",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["mientras", "while", "durante", "al mismo tiempo"],
        confianza_grounding=0.75,
        propiedades={
            "es_expresion_temporal": True,
            "es_simultaneidad": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CUANDO_TEMP",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["cuando", "when", "al momento de"],
        confianza_grounding=0.78,
        propiedades={
            "es_expresion_temporal": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_HACE_TIEMPO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["hace tiempo", "hace rato", "hace mucho", "long ago"],
        confianza_grounding=0.72,
        propiedades={
            "es_expresion_temporal": True,
            "direccion": "pasado",
        },
    ))
    
    # ══════════ DURACIONES ══════════════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SEGUNDO_TIEMPO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["segundo", "segundos", "seg"],
        confianza_grounding=0.78,
        propiedades={
            "es_duracion": True,
            "unidad": "segundo",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MINUTO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["minuto", "minutos", "min"],
        confianza_grounding=0.78,
        propiedades={
            "es_duracion": True,
            "unidad": "minuto",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_HORA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["hora", "horas", "hrs"],
        confianza_grounding=0.78,
        propiedades={
            "es_duracion": True,
            "unidad": "hora",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DIA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["día", "días"],
        confianza_grounding=0.78,
        propiedades={
            "es_duracion": True,
            "unidad": "dia",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SEMANA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["semana", "semanas"],
        confianza_grounding=0.78,
        propiedades={
            "es_duracion": True,
            "unidad": "semana",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MES",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["mes", "meses"],
        confianza_grounding=0.78,
        propiedades={
            "es_duracion": True,
            "unidad": "mes",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ANO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["año", "años"],
        confianza_grounding=0.78,
        propiedades={
            "es_duracion": True,
            "unidad": "año",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SIGLO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["siglo", "siglos", "century"],
        confianza_grounding=0.72,
        propiedades={
            "es_duracion": True,
            "unidad": "siglo",
        },
    ))
    
    return conceptos


if __name__ == '__main__':
    conceptos = obtener_conceptos_expresiones_tiempo()
    grounding_prom = sum(c.confianza_grounding for c in conceptos) / len(conceptos)
    print(f"✅ Expresiones de Tiempo: {len(conceptos)} conceptos")
    print(f"   Grounding promedio: {grounding_prom:.2f}")