"""
conceptos_capa1.py — Vocabulario Capa 1 (Fix de diagnóstico 02/03/2026)

30 conceptos que causaban el 40% de fallas en el diagnóstico de 88 casos.

PROBLEMAS RESUELTOS:
════════════════════════════════════════════════════════════════════════
C-03  "ser"/"estar" — verbos más usados del español, ausentes en vocab
      Causa: "eres X", "estoy Y" → DESCONOCIDO siempre (24 fallas)

C-04  Nombres de consejeras no estaban en vocabulario
      Causa: "qué hace Vega" → motor no detectaba "vega" → fallaba
      NOTA CRÍTICA: CONCEPTO_ECHO_CONSEJERA usa grounding 0.7 SIN
      operaciones para que NO active P1 (que es para shell con 1.0).

A-03  Palabras comunes faltantes: python, consejera, buen, gracia,
      verbos cognitivos en imperativo, IA/LLM externos.

M-03  "cuántas consejeras" no se resolvía porque "consejera" no existía.

M-05  "buenos días" fallaba porque "buen" no estaba en vocabulario.

REGLAS DE GROUNDING USADAS:
  1.0 → operaciones ejecutables (shell, código)
  0.9 → conceptos de sistema bien definidos
  0.7 → conceptos conversacionales estables
  0.5 → conceptos relacionales / gramáticales
════════════════════════════════════════════════════════════════════════
"""

from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto


def obtener_conceptos_capa1() -> list:
    """
    Retorna los ~30 conceptos faltantes críticos detectados en diagnóstico.
    Se carga DESPUÉS de la expansión para que en caso de conflicto,
    este archivo tenga prioridad (el GestorVocabulario prioriza mayor grounding
    cuando hay duplicados en buscar_por_palabra).
    """
    conceptos = []

    # ═══════════════════════════════════════════════════════════════════════
    # BLOQUE 1: VERBOS FUNDAMENTALES DEL ESPAÑOL (FIX C-03)
    # Los más usados en cualquier oración — sin ellos el 30% falla.
    # Grounding 0.5: son relacionales/gramaticales, no ejecutables.
    # ═══════════════════════════════════════════════════════════════════════

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SER",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=[
            "ser",
            "eres", "es", "son", "soy", "somos",
            "fue", "era", "eran", "fui",
            "sería", "serías", "sean",
        ],
        confianza_grounding=0.5,
        propiedades={
            "es_verbo": True,
            "es_copulativo": True,
            "indica_identidad": True,
            "no_ejecutable": True,
        },
        relaciones={
            "relacionado_con": ["CONCEPTO_ERES", "CONCEPTO_IDENTIDAD"],
        }
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ESTAR",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=[
            "estar",
            "estoy", "estás", "está", "estamos", "están",
            "estaba", "estabas", "estaban",
            "estuvo", "estuve",
        ],
        confianza_grounding=0.5,
        propiedades={
            "es_verbo": True,
            "es_copulativo": True,
            "indica_estado": True,
            "no_ejecutable": True,
        }
    ))

    # ═══════════════════════════════════════════════════════════════════════
    # BLOQUE 2: CONSEJERAS DE BELL (FIX C-04)
    # Grounding 0.7: conceptos estables, NO tienen operaciones.
    # CRÍTICO: Sin operaciones → P1 NO dispara → clasificador puede
    # llegar a P3.5 donde _es_consulta_consejera() los detecta.
    #
    # CONCEPTO_ECHO_CONSEJERA: nombre distinto de CONCEPTO_ECHO (shell).
    # semana5_sistema.py tiene CONCEPTO_ECHO con grounding 1.0 + ops.
    # Si "echo" mapeara a ese concepto, P1 dispararía AFIRMATIVA.
    # Solución: semana5_sistema.py quitó "echo" como palabra directa
    # (ver esa corrección). Ahora "echo" solo mapea aquí (sin ops).
    # ═══════════════════════════════════════════════════════════════════════

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_VEGA_CONSEJERA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "vega",
        ],
        confianza_grounding=0.7,
        propiedades={
            "es_consejera": True,
            "es_nombre_propio": True,
            "rol": "guardiana y seguridad",
            "tiene_veto": True,
        }
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ECHO_CONSEJERA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "echo",
            # "echo" se quitó de CONCEPTO_ECHO (shell) en semana5_sistema.py
            # para que aquí sea la referencia principal de la palabra "echo".
        ],
        confianza_grounding=0.7,
        propiedades={
            "es_consejera": True,
            "es_nombre_propio": True,
            "rol": "verificadora de coherencia",
            "tiene_veto": False,
        }
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LYRA_CONSEJERA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "lyra",
        ],
        confianza_grounding=0.7,
        propiedades={
            "es_consejera": True,
            "es_nombre_propio": True,
            "rol": "inteligencia emocional",
        }
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NOVA_CONSEJERA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "nova",
        ],
        confianza_grounding=0.7,
        propiedades={
            "es_consejera": True,
            "es_nombre_propio": True,
            "rol": "ingeniería y optimización",
        }
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LUNA_CONSEJERA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "luna",
        ],
        confianza_grounding=0.7,
        propiedades={
            "es_consejera": True,
            "es_nombre_propio": True,
            "rol": "reconocimiento de patrones",
        }
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_IRIS_CONSEJERA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "iris",
        ],
        confianza_grounding=0.7,
        propiedades={
            "es_consejera": True,
            "es_nombre_propio": True,
            "rol": "curiosidad y aprendizaje",
        }
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SAGE_CONSEJERA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "sage",
        ],
        confianza_grounding=0.7,
        propiedades={
            "es_consejera": True,
            "es_nombre_propio": True,
            "rol": "síntesis y sabiduría",
        }
    ))

    # ═══════════════════════════════════════════════════════════════════════
    # BLOQUE 3: CONCEPTO_CONSEJERA — para "cuántas consejeras tienes"
    # ═══════════════════════════════════════════════════════════════════════

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CONSEJERA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "consejera", "consejeras",
            "consejero", "consejeros",
            "consejos",
        ],
        confianza_grounding=0.7,
        propiedades={
            "es_rol": True,
            "cantidad_bell": 7,
            "relacionado_con_bell": True,
        }
    ))

    # ═══════════════════════════════════════════════════════════════════════
    # BLOQUE 4: PYTHON COMO LENGUAJE (FIX A-03)
    # Diferente de los conceptos de Python ya existentes (funciones, loops).
    # ═══════════════════════════════════════════════════════════════════════

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PYTHON_LENGUAJE",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "python",
            "lenguaje python",
            "python lang",
        ],
        confianza_grounding=0.8,
        propiedades={
            "es_lenguaje_programacion": True,
            "bell_usa": True,
            "interpretado": True,
        }
    ))

    # ═══════════════════════════════════════════════════════════════════════
    # BLOQUE 5: SALUDOS EXTENDIDOS (FIX M-05)
    # "buen" no estaba → "buenos días" → DESCONOCIDO
    # ═══════════════════════════════════════════════════════════════════════

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_BUEN",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=[
            "buen", "buenos", "buenas",
            "buen día", "buenos días",
            "buenas tardes", "buenas noches",
            "buen dia", "buenos dias",
        ],
        confianza_grounding=0.6,
        propiedades={
            "es_saludo": True,
            "es_adjetivo": True,
            "contexto": "social",
        }
    ))

    # ═══════════════════════════════════════════════════════════════════════
    # BLOQUE 6: GRACIAS — VARIANTES Y LEMMA (FIX M-05)
    # "gracia" es el lemma de "gracias" pero no estaba en vocab.
    # ═══════════════════════════════════════════════════════════════════════

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_GRACIAS_VARIANTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=[
            "gracia",              # lemma de "gracias"
            "muchas gracias",
            "mil gracias",
            "muchísimas gracias",
            "muchisimas gracias",
            "muy agradecido",
            "muy agradecida",
            "te lo agradezco",
            "se lo agradezco",
        ],
        confianza_grounding=0.6,
        propiedades={
            "es_agradecimiento": True,
            "es_social": True,
            "subtipo_social": "AGRADECIMIENTO",
        }
    ))

    # ═══════════════════════════════════════════════════════════════════════
    # BLOQUE 7: VERBOS COGNITIVOS EN IMPERATIVO (FIX A-06)
    # Los infinitivos ya estaban; las formas imperativas no.
    # ═══════════════════════════════════════════════════════════════════════

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EXPLICAR_IMP",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=[
            "explícame", "explicame",
            "explica",
            "explícanos", "explicanos",
        ],
        confianza_grounding=0.7,
        propiedades={
            "es_accion_cognitiva": True,
            "subtipo_cognitivo": "EXPLICAR",
            "es_imperativo": True,
        }
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SIMPLIFICAR_IMP",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=[
            "simplifica", "simplificame", "simplifícame",
            "simplificar",
            "hazlo más simple", "hazlo sencillo",
        ],
        confianza_grounding=0.7,
        propiedades={
            "es_accion_cognitiva": True,
            "subtipo_cognitivo": "SIMPLIFICAR",
            "es_imperativo": True,
        }
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_REPETIR_IMP",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=[
            "repite", "repíteme", "repiteme",
            "vuelve a decir", "di de nuevo",
            "otra vez",
        ],
        confianza_grounding=0.7,
        propiedades={
            "es_accion_cognitiva": True,
            "subtipo_cognitivo": "REPETIR",
            "es_imperativo": True,
        }
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DEFINIR_IMP",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=[
            "define", "defíneme", "defineme",
            "definición de", "que significa",
            "qué significa", "qué es exactamente",
        ],
        confianza_grounding=0.7,
        propiedades={
            "es_accion_cognitiva": True,
            "subtipo_cognitivo": "DEFINIR",
            "es_imperativo": True,
        }
    ))

    # ═══════════════════════════════════════════════════════════════════════
    # BLOQUE 8: LLM Y COMPARACIONES (FIX A-04)
    # Para que "eres chatgpt" → IDENTIDAD_BELL (no DESCONOCIDO)
    # ═══════════════════════════════════════════════════════════════════════

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LLM_EXTERNO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "chatgpt", "gpt", "gpt-4",
            "gemini", "copilot", "bard",
            "llm", "modelo de lenguaje",
            "large language model",
        ],
        confianza_grounding=0.7,
        propiedades={
            "es_ia_externa": True,
            "bell_no_es": True,
            "activa_identidad_bell": True,
        }
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INTELIGENCIA_ARTIFICIAL",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "inteligencia artificial",
            "artificial",
            "ia", "ai",
            "sistema de ia",
        ],
        confianza_grounding=0.6,
        propiedades={
            "es_categoria_tecnologica": True,
            "bell_es_diferente": True,
        }
    ))

    # ═══════════════════════════════════════════════════════════════════════
    # BLOQUE 9: CONCEPTOS GENERALES FALTANTES
    # ═══════════════════════════════════════════════════════════════════════

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MUNDO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "mundo", "mundo real",
            "el mundo", "planeta",
            "global", "mundial",
        ],
        confianza_grounding=0.5,
        propiedades={
            "es_lugar": True,
            "bell_no_tiene_acceso_internet": True,
        }
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LENGUAJE_NAT",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "lenguaje",
            "lenguaje natural",
            "idioma",
            "lengua",
        ],
        confianza_grounding=0.6,
        propiedades={
            "es_herramienta_comunicacion": True,
        }
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CREADOR",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "creador", "creadora",
            "quien te creó", "quien te hizo",
            "autor", "desarrollador",
            "te hizo", "te creó", "te diseño", "te diseñó",
        ],
        confianza_grounding=0.7,
        propiedades={
            "relacion_bell": True,
            "valor": "Sebastian",
        }
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PRINCIPIO_BELL",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "principio", "principios",
            "principio central",
            "filosofía", "filosofia",
            "valor central",
        ],
        confianza_grounding=0.6,
        propiedades={
            "relacion_bell": True,
            "activar_identidad": True,
        }
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TIENES_VARIANTE",
        tipo=TipoConcepto.PALABRA_CONVERSACION,
        palabras_español=[
            "tienes", "tiene",
            "tien", "tené",   # variantes coloquiales
            "tenés",
        ],
        confianza_grounding=0.5,
        propiedades={
            "es_verbo": True,
            "forma_de": "tener",
            "segunda_persona": True,
        }
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CHATBOT",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "chatbot", "bot", "robot",
            "asistente virtual",
            "asistente de chat",
        ],
        confianza_grounding=0.6,
        propiedades={
            "es_ia_generica": True,
            "bell_no_es": True,
            "activa_identidad_bell": True,
        }
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_GROUNDING_BELL",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "grounding", "anclaje",
            "concepto anclado",
            "computacional",
            "verificable",
            "verificado",
        ],
        confianza_grounding=0.8,
        propiedades={
            "es_concepto_bell": True,
            "arquitectura_bell": True,
        }
    ))

    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FASE_BELL",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "fase", "fases",
            "etapa", "etapas",
            "fase actual", "en qué fase",
            "fase 4a", "4a",
        ],
        confianza_grounding=0.7,
        propiedades={
            "es_concepto_bell": True,
            "fase_actual": "4A",
            "activa_identidad": True,
        }
    ))

    return conceptos


if __name__ == '__main__':
    conceptos = obtener_conceptos_capa1()
    print(f"✅ Capa 1 — {len(conceptos)} conceptos cargados")
    print()

    por_bloque = {
        "Verbos fundamentales (ser/estar)": 0,
        "Consejeras": 0,
        "Consejera (grupo)": 0,
        "Python lenguaje": 0,
        "Saludos extendidos": 0,
        "Gracias variantes": 0,
        "Verbos cognitivos imperativos": 0,
        "LLM externos": 0,
        "Conceptos generales": 0,
    }

    for c in conceptos:
        print(f"  {c.id} → {c.palabras_español[:3]}... (g={c.confianza_grounding})")