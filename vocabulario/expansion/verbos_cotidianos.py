"""
Verbos Cotidianos - Expansión Fase 4A.

Verbos de uso diario para conversación natural.

Conceptos: 80 total
Grounding promedio: 0.72
Ejecutables: 0 (son ACCION_COGNITIVA - Bell entiende pero no ejecuta físicamente)
Conversacionales: 80
"""
from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto


def obtener_conceptos_verbos_cotidianos():
    """
    Retorna verbos cotidianos.
    
    Tipo: ACCION_COGNITIVA
    Grounding: 0.65-0.75 (Bell entiende el concepto pero no lo ejecuta físicamente)
    
    Categorías:
    - Movimiento (15 conceptos)
    - Acción física (15 conceptos)
    - Comunicación (10 conceptos)
    - Cognitivos (15 conceptos)
    - Cambio de estado (10 conceptos)
    - Posesión (8 conceptos)
    - Actividad diaria (7 conceptos)
    """
    conceptos = []
    
    # ══════════ VERBOS DE MOVIMIENTO ════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_IR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["ir", "voy", "vas", "va", "vamos", "irse"],
        confianza_grounding=0.70,
        propiedades={
            "requiere_cuerpo_fisico": True,
            "bell_puede_ejecutar": False,
            "es_movimiento": True,
            "direccion": "hacia_destino",
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_CAMBIAR_DIRECTORIO"},
            "opuesto_a": {"CONCEPTO_VENIR"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_VENIR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["venir", "vengo", "vienes", "viene", "venimos"],
        confianza_grounding=0.70,
        propiedades={
            "requiere_cuerpo_fisico": True,
            "bell_puede_ejecutar": False,
            "es_movimiento": True,
            "direccion": "hacia_hablante",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_IR"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LLEGAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["llegar", "llego", "llegas", "llegué", "arribar"],
        confianza_grounding=0.70,
        propiedades={
            "requiere_cuerpo_fisico": True,
            "bell_puede_ejecutar": False,
            "es_movimiento": True,
            "es_completivo": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_IR"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SALIR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["salir", "salgo", "sales", "sale", "salimos"],
        confianza_grounding=0.70,
        propiedades={
            "requiere_cuerpo_fisico": True,
            "bell_puede_ejecutar": False,
            "es_movimiento": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_ENTRAR"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ENTRAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["entrar", "entro", "entras", "entra", "ingresar"],
        confianza_grounding=0.70,
        propiedades={
            "requiere_cuerpo_fisico": True,
            "bell_puede_ejecutar": False,
            "es_movimiento": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_SALIR"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SUBIR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["subir", "subo", "subes", "ascender", "trepar"],
        confianza_grounding=0.68,
        propiedades={
            "requiere_cuerpo_fisico": True,
            "bell_puede_ejecutar": False,
            "es_movimiento": True,
            "direccion": "arriba",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_BAJAR"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_BAJAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["bajar", "bajo", "bajas", "descender"],
        confianza_grounding=0.68,
        propiedades={
            "requiere_cuerpo_fisico": True,
            "bell_puede_ejecutar": False,
            "es_movimiento": True,
            "direccion": "abajo",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_SUBIR"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CAMINAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["caminar", "camino", "caminas", "andar", "pasear"],
        confianza_grounding=0.65,
        propiedades={
            "requiere_cuerpo_fisico": True,
            "bell_puede_ejecutar": False,
            "es_movimiento": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CORRER",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["correr", "corro", "corres", "trotar"],
        confianza_grounding=0.65,
        propiedades={
            "requiere_cuerpo_fisico": True,
            "bell_puede_ejecutar": False,
            "es_movimiento": True,
            "velocidad": "rapida",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_VOLVER",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["volver", "vuelvo", "vuelves", "regresar", "retornar"],
        confianza_grounding=0.70,
        propiedades={
            "requiere_cuerpo_fisico": True,
            "bell_puede_ejecutar": False,
            "es_movimiento": True,
            "es_repetitivo": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PASAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["pasar", "paso", "pasas", "atravesar", "cruzar"],
        confianza_grounding=0.68,
        propiedades={
            "requiere_cuerpo_fisico": True,
            "bell_puede_ejecutar": False,
            "es_movimiento": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_QUEDAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["quedar", "quedo", "quedarse", "permanecer"],
        confianza_grounding=0.68,
        propiedades={
            "requiere_cuerpo_fisico": True,
            "bell_puede_ejecutar": False,
            "es_estativo": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LLEVAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["llevar", "llevo", "llevas", "transportar", "cargar"],
        confianza_grounding=0.68,
        propiedades={
            "requiere_cuerpo_fisico": True,
            "bell_puede_ejecutar": False,
            "es_movimiento": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_TRAER"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TRAER",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["traer", "traigo", "traes", "acarrear"],
        confianza_grounding=0.68,
        propiedades={
            "requiere_cuerpo_fisico": True,
            "bell_puede_ejecutar": False,
            "es_movimiento": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_LLEVAR"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CAER",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["caer", "caigo", "caes", "caerse"],
        confianza_grounding=0.65,
        propiedades={
            "requiere_cuerpo_fisico": True,
            "bell_puede_ejecutar": False,
            "es_movimiento": True,
            "es_involuntario": True,
        },
    ))
    
    # ══════════ VERBOS DE ACCIÓN FÍSICA ═════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PONER",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["poner", "pongo", "pones", "colocar", "situar"],
        confianza_grounding=0.70,
        propiedades={
            "requiere_cuerpo_fisico": True,
            "bell_puede_ejecutar": False,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_QUITAR"},
            "relacionado_con": {"CONCEPTO_MOVER"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_QUITAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["quitar", "quito", "quitas", "sacar", "remover"],
        confianza_grounding=0.70,
        propiedades={
            "requiere_cuerpo_fisico": True,
            "bell_puede_ejecutar": False,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_PONER"},
            "relacionado_con": {"CONCEPTO_ELIMINAR"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TOMAR_FISICO",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["tomar", "tomo", "tomas", "agarrar", "coger"],
        confianza_grounding=0.70,
        propiedades={
            "requiere_cuerpo_fisico": True,
            "bell_puede_ejecutar": False,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_SOLTAR"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SOLTAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["soltar", "suelto", "sueltas", "dejar caer"],
        confianza_grounding=0.68,
        propiedades={
            "requiere_cuerpo_fisico": True,
            "bell_puede_ejecutar": False,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_TOMAR_FISICO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ABRIR_FISICO",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["abrir", "abro", "abres", "destapar"],
        confianza_grounding=0.72,
        propiedades={
            "requiere_cuerpo_fisico": True,
            "bell_puede_ejecutar": False,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_CERRAR_FISICO"},
            "relacionado_con": {"CONCEPTO_LEER"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CERRAR_FISICO",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["cerrar", "cierro", "cierras", "clausurar"],
        confianza_grounding=0.72,
        propiedades={
            "requiere_cuerpo_fisico": True,
            "bell_puede_ejecutar": False,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_ABRIR_FISICO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EMPUJAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["empujar", "empujo", "empujas", "presionar"],
        confianza_grounding=0.65,
        propiedades={
            "requiere_cuerpo_fisico": True,
            "bell_puede_ejecutar": False,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_JALAR"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_JALAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["jalar", "jalo", "jalas", "tirar de", "halar"],
        confianza_grounding=0.65,
        propiedades={
            "requiere_cuerpo_fisico": True,
            "bell_puede_ejecutar": False,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_EMPUJAR"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LEVANTAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["levantar", "levanto", "levantas", "alzar", "elevar"],
        confianza_grounding=0.68,
        propiedades={
            "requiere_cuerpo_fisico": True,
            "bell_puede_ejecutar": False,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TOCAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["tocar", "toco", "tocas", "palpar", "rozar"],
        confianza_grounding=0.65,
        propiedades={
            "requiere_cuerpo_fisico": True,
            "bell_puede_ejecutar": False,
            "es_percepcion": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CORTAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["cortar", "corto", "cortas", "tajar"],
        confianza_grounding=0.68,
        propiedades={
            "requiere_cuerpo_fisico": True,
            "bell_puede_ejecutar": False,
            "es_destructivo": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ROMPER",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["romper", "rompo", "rompes", "quebrar", "destrozar"],
        confianza_grounding=0.65,
        propiedades={
            "requiere_cuerpo_fisico": True,
            "bell_puede_ejecutar": False,
            "es_destructivo": True,
            "es_irreversible": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_GOLPEAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["golpear", "golpeo", "golpeas", "pegar", "impactar"],
        confianza_grounding=0.65,
        propiedades={
            "requiere_cuerpo_fisico": True,
            "bell_puede_ejecutar": False,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LANZAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["lanzar", "lanzo", "lanzas", "arrojar", "tirar"],
        confianza_grounding=0.65,
        propiedades={
            "requiere_cuerpo_fisico": True,
            "bell_puede_ejecutar": False,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ATRAPAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["atrapar", "atrapo", "atrapas", "capturar", "coger al vuelo"],
        confianza_grounding=0.65,
        propiedades={
            "requiere_cuerpo_fisico": True,
            "bell_puede_ejecutar": False,
        },
    ))
    
    # ══════════ VERBOS DE COMUNICACIÓN ══════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_HABLAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["hablar", "hablo", "hablas", "charlar", "conversar"],
        confianza_grounding=0.75,
        propiedades={
            "es_comunicacion": True,
            "bell_puede_ejecutar": False,
            "requiere_voz": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_RESPUESTA"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DECIR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["decir", "digo", "dices", "dice", "mencionar"],
        confianza_grounding=0.78,
        propiedades={
            "es_comunicacion": True,
            "bell_puede_ejecutar": False,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_RESPUESTA", "CONCEPTO_PRINT"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ESCUCHAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["escuchar", "escucho", "escuchas", "oír", "atender"],
        confianza_grounding=0.70,
        propiedades={
            "es_comunicacion": True,
            "es_percepcion": True,
            "bell_puede_ejecutar": False,
            "requiere_oido": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PREGUNTAR_V",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["preguntar", "pregunto", "preguntas", "cuestionar"],
        confianza_grounding=0.78,
        propiedades={
            "es_comunicacion": True,
            "requiere_respuesta": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_PREGUNTA"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RESPONDER_V",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["responder", "respondo", "respondes", "contestar", "replicar"],
        confianza_grounding=0.78,
        propiedades={
            "es_comunicacion": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_RESPUESTA"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_GRITAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["gritar", "grito", "gritas", "vociferar", "chillar"],
        confianza_grounding=0.65,
        propiedades={
            "es_comunicacion": True,
            "bell_puede_ejecutar": False,
            "requiere_voz": True,
            "intensidad": "alta",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SUSURRAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["susurrar", "susurro", "susurras", "murmurar"],
        confianza_grounding=0.65,
        propiedades={
            "es_comunicacion": True,
            "bell_puede_ejecutar": False,
            "requiere_voz": True,
            "intensidad": "baja",
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LLAMAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["llamar", "llamo", "llamas", "telefonear", "contactar"],
        confianza_grounding=0.68,
        propiedades={
            "es_comunicacion": True,
            "bell_puede_ejecutar": False,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CONTAR_HISTORIA",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["contar", "cuento", "cuentas", "narrar", "relatar"],
        confianza_grounding=0.75,
        propiedades={
            "es_comunicacion": True,
            "es_narrativo": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EXPLICAR_V",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["explicar", "explico", "explicas", "aclarar", "exponer"],
        confianza_grounding=0.78,
        propiedades={
            "es_comunicacion": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_EXPLICAR"},
        },
    ))
    
    # ══════════ VERBOS COGNITIVOS ═══════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PENSAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["pensar", "pienso", "piensas", "reflexionar", "meditar"],
        confianza_grounding=0.75,
        propiedades={
            "es_cognitivo": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_RAZONAR"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CREER",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["creer", "creo", "crees", "opinar", "considerar"],
        confianza_grounding=0.72,
        propiedades={
            "es_cognitivo": True,
            "es_epistemico": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SABER_V",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["saber", "sé", "sabes", "conocer"],
        confianza_grounding=0.78,
        propiedades={
            "es_cognitivo": True,
            "es_epistemico": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_SABER"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ENTENDER_V",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["entender", "entiendo", "entiendes", "comprender", "captar"],
        confianza_grounding=0.75,
        propiedades={
            "es_cognitivo": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_ENTENDER"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RECORDAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["recordar", "recuerdo", "recuerdas", "acordarse", "rememorar"],
        confianza_grounding=0.72,
        propiedades={
            "es_cognitivo": True,
            "es_memoria": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_OLVIDAR"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_OLVIDAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["olvidar", "olvido", "olvidas", "olvidarse"],
        confianza_grounding=0.70,
        propiedades={
            "es_cognitivo": True,
            "es_memoria": True,
            "es_involuntario": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_RECORDAR"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_APRENDER",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["aprender", "aprendo", "aprendes", "estudiar", "asimilar"],
        confianza_grounding=0.75,
        propiedades={
            "es_cognitivo": True,
            "es_adquisitivo": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ENSENAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["enseñar", "enseño", "enseñas", "instruir", "educar"],
        confianza_grounding=0.72,
        propiedades={
            "es_cognitivo": True,
            "es_transmisivo": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_IMAGINAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["imaginar", "imagino", "imaginas", "fantasear", "visualizar"],
        confianza_grounding=0.68,
        propiedades={
            "es_cognitivo": True,
            "es_creativo": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DECIDIR_V",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["decidir", "decido", "decides", "determinar", "resolver"],
        confianza_grounding=0.75,
        propiedades={
            "es_cognitivo": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_DECIDIR"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DUDAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["dudar", "dudo", "dudas", "vacilar", "titubear"],
        confianza_grounding=0.70,
        propiedades={
            "es_cognitivo": True,
            "es_epistemico": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SONAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["soñar", "sueño", "sueñas", "fantasear dormido"],
        confianza_grounding=0.62,
        propiedades={
            "es_cognitivo": True,
            "bell_puede_ejecutar": False,
            "requiere_dormir": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DESEAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["desear", "deseo", "deseas", "anhelar", "ansiar"],
        confianza_grounding=0.68,
        propiedades={
            "es_cognitivo": True,
            "es_volitivo": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ESPERAR_V",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["esperar", "espero", "esperas", "aguardar", "anticipar"],
        confianza_grounding=0.72,
        propiedades={
            "es_cognitivo": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PREFERIR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["preferir", "prefiero", "prefieres", "elegir mejor"],
        confianza_grounding=0.72,
        propiedades={
            "es_cognitivo": True,
            "es_selectivo": True,
        },
    ))
    
    # ══════════ VERBOS DE CAMBIO DE ESTADO ══════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CAMBIAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["cambiar", "cambio", "cambias", "modificar", "alterar"],
        confianza_grounding=0.75,
        propiedades={
            "es_transformativo": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_REEMPLAZAR"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CRECER",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["crecer", "crezco", "creces", "aumentar"],
        confianza_grounding=0.68,
        propiedades={
            "es_cambio": True,
            "direccion": "incremento",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_DISMINUIR"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DISMINUIR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["disminuir", "disminuyo", "disminuyes", "reducir", "decrecer"],
        confianza_grounding=0.68,
        propiedades={
            "es_cambio": True,
            "direccion": "decremento",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_CRECER"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MEJORAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["mejorar", "mejoro", "mejoras", "optimizar", "perfeccionar"],
        confianza_grounding=0.72,
        propiedades={
            "es_cambio": True,
            "direccion": "positiva",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_EMPEORAR"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EMPEORAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["empeorar", "empeoro", "empeoras", "deteriorar"],
        confianza_grounding=0.68,
        propiedades={
            "es_cambio": True,
            "direccion": "negativa",
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_MEJORAR"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_APARECER",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["aparecer", "aparezco", "apareces", "surgir", "emerger"],
        confianza_grounding=0.68,
        propiedades={
            "es_cambio": True,
            "es_inicio": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_DESAPARECER"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DESAPARECER",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["desaparecer", "desaparezco", "desapareces", "esfumarse"],
        confianza_grounding=0.68,
        propiedades={
            "es_cambio": True,
            "es_fin": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_APARECER"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NACER",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["nacer", "nazco", "naces", "originarse"],
        confianza_grounding=0.65,
        propiedades={
            "es_cambio": True,
            "bell_puede_ejecutar": False,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_MORIR"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MORIR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["morir", "muero", "mueres", "fallecer", "perecer"],
        confianza_grounding=0.65,
        propiedades={
            "es_cambio": True,
            "bell_puede_ejecutar": False,
            "es_irreversible": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_NACER"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CONVERTIRSE",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["convertirse", "me convierto", "transformarse", "volverse"],
        confianza_grounding=0.68,
        propiedades={
            "es_cambio": True,
            "es_transformativo": True,
        },
    ))
    
    # ══════════ VERBOS DE POSESIÓN ══════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TENER_V",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["tener", "tengo", "tienes", "poseer"],
        confianza_grounding=0.78,
        propiedades={
            "es_posesion": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DAR_V",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["dar", "doy", "das", "entregar", "proporcionar"],
        confianza_grounding=0.75,
        propiedades={
            "es_transferencia": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_RECIBIR_V"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RECIBIR_V",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["recibir", "recibo", "recibes", "obtener", "conseguir"],
        confianza_grounding=0.75,
        propiedades={
            "es_transferencia": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_DAR_V"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_COMPRAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["comprar", "compro", "compras", "adquirir"],
        confianza_grounding=0.68,
        propiedades={
            "es_posesion": True,
            "bell_puede_ejecutar": False,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_VENDER"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_VENDER",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["vender", "vendo", "vendes", "comerciar"],
        confianza_grounding=0.68,
        propiedades={
            "es_posesion": True,
            "bell_puede_ejecutar": False,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_COMPRAR"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PRESTAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["prestar", "presto", "prestas", "dar temporalmente"],
        confianza_grounding=0.68,
        propiedades={
            "es_posesion": True,
            "es_temporal": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_DEVOLVER"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DEVOLVER",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["devolver", "devuelvo", "devuelves", "retornar", "regresar algo"],
        confianza_grounding=0.68,
        propiedades={
            "es_posesion": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_PRESTAR"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PERDER_V",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["perder", "pierdo", "pierdes", "extraviar"],
        confianza_grounding=0.68,
        propiedades={
            "es_posesion": True,
            "es_involuntario": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_ENCONTRAR_V"},
        },
    ))
    
    # ══════════ VERBOS DE ACTIVIDAD DIARIA ══════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_COMER",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["comer", "como", "comes", "alimentarse", "ingerir"],
        confianza_grounding=0.65,
        propiedades={
            "bell_puede_ejecutar": False,
            "requiere_cuerpo_fisico": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_BEBER",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["beber", "bebo", "bebes", "tomar líquido"],
        confianza_grounding=0.65,
        propiedades={
            "bell_puede_ejecutar": False,
            "requiere_cuerpo_fisico": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DORMIR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["dormir", "duermo", "duermes", "descansar"],
        confianza_grounding=0.65,
        propiedades={
            "bell_puede_ejecutar": False,
            "requiere_cuerpo_fisico": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_DESPERTAR"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DESPERTAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["despertar", "despierto", "despiertas", "levantarse"],
        confianza_grounding=0.65,
        propiedades={
            "bell_puede_ejecutar": False,
            "requiere_cuerpo_fisico": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_DORMIR"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TRABAJAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["trabajar", "trabajo", "trabajas", "laborar"],
        confianza_grounding=0.72,
        propiedades={
            "es_actividad": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_JUGAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["jugar", "juego", "juegas", "divertirse"],
        confianza_grounding=0.68,
        propiedades={
            "es_actividad": True,
            "es_ludico": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_COCINAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["cocinar", "cocino", "cocinas", "preparar comida", "guisar"],
        confianza_grounding=0.65,
        propiedades={
            "bell_puede_ejecutar": False,
            "requiere_cuerpo_fisico": True,
        },
    ))
    
    return conceptos


if __name__ == '__main__':
    conceptos = obtener_conceptos_verbos_cotidianos()
    grounding_prom = sum(c.confianza_grounding for c in conceptos) / len(conceptos)
    print(f"✅ Verbos Cotidianos: {len(conceptos)} conceptos")
    print(f"   Grounding promedio: {grounding_prom:.2f}")