"""
Entretenimiento y Ocio - Expansión Fase 4A.

Actividades recreativas, deportes y pasatiempos.

Conceptos: 40 total
Grounding promedio: 0.74
Tipo: PALABRA_CONVERSACION / ACCION_COGNITIVA
"""
from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto


def obtener_conceptos_entretenimiento():
    """
    Retorna conceptos de entretenimiento y ocio.
    
    Categorías:
    - Deportes (12)
    - Entretenimiento digital (14)
    - Pasatiempos (14)
    """
    conceptos = []
    
    # ══════════ DEPORTES ════════════════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FUTBOL",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["fútbol", "futbol", "soccer", "balompié"],
        confianza_grounding=0.78,
        propiedades={
            "es_deporte": True,
            "es_equipo": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_BASQUETBOL",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["básquetbol", "basketball", "baloncesto"],
        confianza_grounding=0.75,
        propiedades={
            "es_deporte": True,
            "es_equipo": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TENIS",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["tenis", "tennis"],
        confianza_grounding=0.75,
        propiedades={
            "es_deporte": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_BEISBOL",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["béisbol", "beisbol", "baseball"],
        confianza_grounding=0.72,
        propiedades={
            "es_deporte": True,
            "es_equipo": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_GIMNASIO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["gimnasio", "gym", "ir al gym"],
        confianza_grounding=0.78,
        propiedades={
            "es_lugar": True,
            "es_deporte": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PARTIDO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["partido", "juego", "match"],
        confianza_grounding=0.78,
        propiedades={
            "es_evento": True,
            "contexto": "deporte",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EQUIPO_DEPORTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["equipo", "selección", "club"],
        confianza_grounding=0.75,
        propiedades={
            "es_grupo": True,
            "contexto": "deporte",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_GANAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["ganar", "vencer", "triunfar"],
        confianza_grounding=0.78,
        propiedades={
            "es_accion": True,
            "contexto": "competencia",
            "valencia": "positiva",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_PERDER"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PERDER",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["perder", "ser derrotado"],
        confianza_grounding=0.78,
        propiedades={
            "es_accion": True,
            "contexto": "competencia",
            "valencia": "negativa",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_GANAR"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EMPATAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["empatar", "empate", "igualar"],
        confianza_grounding=0.72,
        propiedades={
            "es_accion": True,
            "contexto": "competencia",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ENTRENAMIENTO",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["entrenamiento", "práctica", "training"],
        confianza_grounding=0.75,
        propiedades={
            "es_actividad": True,
            "contexto": "deporte",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_COMPETENCIA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["competencia", "torneo", "campeonato", "liga"],
        confianza_grounding=0.75,
        propiedades={
            "es_evento": True,
            "contexto": "deporte",
        },
    ))
    
    # ══════════ ENTRETENIMIENTO DIGITAL ═════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PELICULA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["película", "peli", "film", "cine"],
        confianza_grounding=0.80,
        propiedades={
            "es_entretenimiento": True,
            "es_digital": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SERIE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["serie", "show", "programa de tv"],
        confianza_grounding=0.80,
        propiedades={
            "es_entretenimiento": True,
            "es_digital": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_VIDEOJUEGO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["videojuego", "juego", "game", "gaming"],
        confianza_grounding=0.82,
        propiedades={
            "es_entretenimiento": True,
            "es_digital": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MUSICA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["música", "canción", "melodía"],
        confianza_grounding=0.80,
        propiedades={
            "es_entretenimiento": True,
            "es_arte": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CANTAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["cantar", "canturrear"],
        confianza_grounding=0.72,
        propiedades={
            "es_actividad": True,
            "requiere_cuerpo_fisico": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_BAILAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["bailar", "danzar", "moverse al ritmo"],
        confianza_grounding=0.72,
        propiedades={
            "es_actividad": True,
            "requiere_cuerpo_fisico": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PODCAST",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["podcast", "pódcast", "audio show"],
        confianza_grounding=0.78,
        propiedades={
            "es_entretenimiento": True,
            "es_digital": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_YOUTUBE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["youtube", "video", "vídeo", "youtuber"],
        confianza_grounding=0.80,
        propiedades={
            "es_entretenimiento": True,
            "es_digital": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_STREAMING",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["streaming", "ver en línea", "netflix", "disney plus"],
        confianza_grounding=0.78,
        propiedades={
            "es_entretenimiento": True,
            "es_digital": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_VER_TV",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["ver tv", "ver tele", "mirar televisión"],
        confianza_grounding=0.78,
        propiedades={
            "es_actividad": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ESCUCHAR_MUSICA",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["escuchar música", "oír música", "poner música"],
        confianza_grounding=0.78,
        propiedades={
            "es_actividad": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_JUGAR_VIDEOJUEGO",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["jugar videojuegos", "gamear", "echar una partida"],
        confianza_grounding=0.78,
        propiedades={
            "es_actividad": True,
        },
    ))
    
    # ══════════ PASATIEMPOS ═════════════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LEER_HOBBY",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["leer", "lectura", "leer un libro"],
        confianza_grounding=0.78,
        propiedades={
            "es_pasatiempo": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LIBRO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["libro", "novela", "texto"],
        confianza_grounding=0.80,
        propiedades={
            "es_objeto": True,
            "contexto": "lectura",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DIBUJAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["dibujar", "ilustrar", "hacer dibujos"],
        confianza_grounding=0.72,
        propiedades={
            "es_pasatiempo": True,
            "es_arte": True,
            "requiere_cuerpo_fisico": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PINTAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["pintar", "hacer pintura", "pintar cuadros"],
        confianza_grounding=0.72,
        propiedades={
            "es_pasatiempo": True,
            "es_arte": True,
            "requiere_cuerpo_fisico": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FOTOGRAFIA",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["fotografía", "tomar fotos", "hacer fotos"],
        confianza_grounding=0.75,
        propiedades={
            "es_pasatiempo": True,
            "es_arte": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_VIAJAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["viajar", "ir de viaje", "conocer lugares"],
        confianza_grounding=0.75,
        propiedades={
            "es_pasatiempo": True,
            "requiere_cuerpo_fisico": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_VACACION",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["vacación", "vacaciones", "holidays"],
        confianza_grounding=0.78,
        propiedades={
            "es_evento": True,
            "valencia": "positiva",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FIESTA",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["fiesta", "celebración", "party"],
        confianza_grounding=0.78,
        propiedades={
            "es_evento": True,
            "valencia": "positiva",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CONCIERTO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["concierto", "show en vivo", "recital"],
        confianza_grounding=0.75,
        propiedades={
            "es_evento": True,
            "contexto": "musica",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_HOBBY",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["hobby", "pasatiempo", "afición"],
        confianza_grounding=0.78,
        propiedades={
            "es_concepto": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DIVERTIDO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["divertido", "entretenido", "fun"],
        confianza_grounding=0.78,
        propiedades={
            "es_adjetivo": True,
            "valencia": "positiva",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ABURRIDO",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=["aburrido", "tedioso", "monótono"],
        confianza_grounding=0.78,
        propiedades={
            "es_adjetivo": True,
            "valencia": "negativa",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_DIVERTIDO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DESCANSAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["descansar", "relajarse", "tomar un break"],
        confianza_grounding=0.78,
        propiedades={
            "es_pasatiempo": True,
        },
    ))
    
    return conceptos


if __name__ == '__main__':
    conceptos = obtener_conceptos_entretenimiento()
    grounding_prom = sum(c.confianza_grounding for c in conceptos) / len(conceptos)
    print(f"✅ Entretenimiento: {len(conceptos)} conceptos")
    print(f"   Grounding promedio: {grounding_prom:.2f}")