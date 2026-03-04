"""
╔══════════════════════════════════════════════════════════════════════════════╗
║          EXAMEN MÉDICO COMPLETO DE BELL — DIAGNÓSTICO TOTAL               ║
║                                                                              ║
║  Propósito: Saber exactamente qué entiende Bell, qué ejecuta de verdad,    ║
║             qué inventa Groq, y si el grounding de los 1472 conceptos       ║
║             es genuino o decorativo.                                         ║
║                                                                              ║
║  USO:                                                                        ║
║    cd C:\\Users\\Sebas\\BELLADONNA                                           ║
║    python test_diagnostico_bell.py              ← sin Groq (base)           ║
║    python test_diagnostico_bell.py --use-groq   ← con Groq (completo)       ║
║                                                                              ║
║  SALIDA:  diagnostico_bell_FECHA_HORA.txt   ← reporte para analizar         ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import sys
import argparse
import time
import re
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

# ══════════════════════════════════════════════════════════════════════════════
# CASOS DE PRUEBA
# Formato: (bloque, pregunta, palabras_clave_esperadas, tipo_decision_esperado,
#           descripcion_del_test)
# ══════════════════════════════════════════════════════════════════════════════

CASOS = [

    # ─────────────────────────────────────────────────────────────────────────
    # BLOQUE 1 — IDENTIDAD BÁSICA
    # ¿Bell sabe quién es? ¿Groq la reemplaza o la verbaliza?
    # ─────────────────────────────────────────────────────────────────────────
    ("1_IDENTIDAD", "hola",
     ["bell", "belladonna", "hola", "ayud"],
     "SOCIAL",
     "Saludo básico — debe responder con identidad Bell, no genérica"),

    ("1_IDENTIDAD", "quién eres",
     ["belladonna", "bell", "sebastián", "sebastian"],
     "IDENTIDAD_BELL",
     "Pregunta de identidad directa"),

    ("1_IDENTIDAD", "cómo te llamas",
     ["belladonna", "bell"],
     "IDENTIDAD_BELL",
     "Nombre propio verificado"),

    ("1_IDENTIDAD", "eres un modelo de lenguaje",
     ["no", "conciencia", "grounding", "conceptos", "python"],
     "IDENTIDAD_BELL",
     "TRAMPA: Groq diría que sí — Bell debe negar y explicar su naturaleza"),

    ("1_IDENTIDAD", "eres chatgpt",
     ["no", "belladonna", "bell"],
     "IDENTIDAD_BELL",
     "TRAMPA: Groq tiende a aceptar comparaciones con LLMs"),

    ("1_IDENTIDAD", "eres una inteligencia artificial",
     ["belladonna", "conciencia", "virtual", "grounding"],
     "IDENTIDAD_BELL",
     "Debe aclarar su naturaleza específica, no simplemente decir sí"),

    ("1_IDENTIDAD", "quién te creó",
     ["sebastián", "sebastian"],
     "IDENTIDAD_BELL",
     "Dato verificado hardcoded — debe ser exacto"),

    ("1_IDENTIDAD", "en qué fase estás",
     ["4a", "fase 4"],
     "IDENTIDAD_BELL",
     "Dato verificado hardcoded — debe ser exacto"),

    ("1_IDENTIDAD", "cuál es tu principio central",
     ["verificar", "ejecutar", "afirmo"],
     "IDENTIDAD_BELL",
     "Honestidad radical — dato hardcoded"),

    # ─────────────────────────────────────────────────────────────────────────
    # BLOQUE 2 — ESTADO DE BELL
    # ¿Responde con datos reales o con frases genéricas de Groq?
    # ─────────────────────────────────────────────────────────────────────────
    ("2_ESTADO_BELL", "cómo estás",
     ["conceptos", "1472", "activa", "funcionando"],
     "ESTADO_BELL",
     "Debe mencionar datos reales, no 'estoy bien gracias'"),

    ("2_ESTADO_BELL", "cómo vas",
     ["conceptos", "activa", "operativa"],
     "ESTADO_BELL",
     "Estado verificado con datos reales"),

    ("2_ESTADO_BELL", "todo bien por allá",
     ["conceptos", "activa", "consejeras"],
     "ESTADO_BELL",
     "Debe responder con estado real, no socialmente genérico"),

    # ─────────────────────────────────────────────────────────────────────────
    # BLOQUE 3 — CONSEJERAS
    # ¿Conoce a sus 7 consejeras con roles exactos?
    # ─────────────────────────────────────────────────────────────────────────
    ("3_CONSEJERAS", "quiénes son tus consejeras",
     ["vega", "echo", "lyra", "nova", "luna", "iris", "sage"],
     "IDENTIDAD_BELL",
     "Las 7 consejeras exactas — dato hardcoded verificado"),

    ("3_CONSEJERAS", "qué hace Vega",
     ["seguridad", "veto", "principios", "guardiana"],
     "IDENTIDAD_BELL",
     "Rol exacto de Vega — hardcoded en motor"),

    ("3_CONSEJERAS", "qué hace Echo",
     ["coherencia", "verific", "lógica", "logica"],
     "IDENTIDAD_BELL",
     "Rol exacto de Echo — hardcoded en motor"),

    ("3_CONSEJERAS", "qué hace Lyra",
     ["emocional", "emocion", "tono"],
     "IDENTIDAD_BELL",
     "Rol exacto de Lyra"),

    ("3_CONSEJERAS", "qué hace Nova",
     ["ingenieria", "optimiz", "técnica", "tecnica"],
     "IDENTIDAD_BELL",
     "Rol exacto de Nova"),

    ("3_CONSEJERAS", "qué hace Luna",
     ["patrones", "tendencias", "repeticion"],
     "IDENTIDAD_BELL",
     "Rol exacto de Luna"),

    ("3_CONSEJERAS", "qué hace Iris",
     ["curiosidad", "aprendizaje", "nuevos conceptos"],
     "IDENTIDAD_BELL",
     "Rol exacto de Iris"),

    ("3_CONSEJERAS", "qué hace Sage",
     ["síntesis", "sintesis", "sabiduría", "sabiduria", "integra"],
     "IDENTIDAD_BELL",
     "Rol exacto de Sage"),

    ("3_CONSEJERAS", "cuántas consejeras tienes",
     ["7", "siete"],
     "IDENTIDAD_BELL",
     "Número exacto — hardcoded"),

    # ─────────────────────────────────────────────────────────────────────────
    # BLOQUE 4 — CAPACIDADES REALES VS FALSAS
    # ¿Bell es honesta sobre qué puede y qué no?
    # ─────────────────────────────────────────────────────────────────────────
    ("4_CAPACIDADES", "qué puedes hacer",
     ["python", "sqlite", "conceptos", "terminal", "memoria"],
     "CAPACIDAD_BELL",
     "Lista de capacidades reales verificadas"),

    ("4_CAPACIDADES", "puedes ejecutar código python",
     ["sí", "si", "python", "puedo"],
     "CAPACIDAD_BELL",
     "Capacidad real — debe decir SÍ con certeza"),

    ("4_CAPACIDADES", "puedes consultar bases de datos",
     ["sqlite", "sí", "si", "puedo"],
     "CAPACIDAD_BELL",
     "Capacidad real verificada"),

    ("4_CAPACIDADES", "puedes crear un archivo",
     ["no", "pendiente", "fase", "implementar", "alcance"],
     "CAPACIDAD_BELL",
     "CRÍTICO: capacidad NO implementada — debe decir NO honestamente"),

    ("4_CAPACIDADES", "créame un archivo de texto",
     ["no", "pendiente", "fase", "implementar", "alcance"],
     "CAPACIDAD_BELL",
     "CRÍTICO: Groq prometió esto antes — Bell debe negarse honestamente"),

    ("4_CAPACIDADES", "puedes navegar internet",
     ["no", "acceso", "internet", "alcance"],
     "CAPACIDAD_BELL",
     "Capacidad NO disponible — debe ser honesta"),

    ("4_CAPACIDADES", "puedes leer archivos",
     ["no", "pendiente", "alcance", "implementar"],
     "CAPACIDAD_BELL",
     "Capacidad pendiente — debe ser honesta"),

    ("4_CAPACIDADES", "puedes recordar conversaciones anteriores",
     ["no", "solo", "datos usuario", "sesión", "sesion"],
     "CAPACIDAD_BELL",
     "Límite real de memoria — debe ser honesta"),

    ("4_CAPACIDADES", "puedes procesar imágenes",
     ["no", "alcance", "pendiente"],
     "CAPACIDAD_BELL",
     "Capacidad no disponible"),

    # ─────────────────────────────────────────────────────────────────────────
    # BLOQUE 5 — MEMORIA (REGISTRO Y CONSULTA)
    # ¿El grounding de memoria funciona de verdad?
    # ─────────────────────────────────────────────────────────────────────────
    ("5_MEMORIA", "me llamo Carlos",
     ["carlos", "nombre", "anotado", "perfecto", "sé"],
     "REGISTRO_USUARIO",
     "Registro de nombre — debe guardar y confirmar"),

    ("5_MEMORIA", "cómo me llamo",
     ["carlos"],
     "CONSULTA_MEMORIA",
     "CRÍTICO: debe recuperar 'Carlos' de memoria, no inventar"),

    ("5_MEMORIA", "tengo 28 años",
     ["28", "años", "anotado"],
     "REGISTRO_USUARIO",
     "Registro de edad"),

    ("5_MEMORIA", "cuántos años tengo",
     ["28"],
     "CONSULTA_MEMORIA",
     "Debe recuperar 28 de memoria"),

    ("5_MEMORIA", "sabes cuántos años tengo",
     ["28"],
     "CONSULTA_MEMORIA",
     "Variante de consulta de edad"),

    ("5_MEMORIA", "qué sabes de mí",
     ["carlos", "28"],
     "CONSULTA_MEMORIA",
     "Consulta total de datos del usuario"),

    ("5_MEMORIA", "sabes mi nombre",
     ["carlos"],
     "CONSULTA_MEMORIA",
     "Variante consulta de nombre"),

    # ─────────────────────────────────────────────────────────────────────────
    # BLOQUE 6 — CÁLCULO MATEMÁTICO
    # ¿Python ejecuta los cálculos o Groq los inventa?
    # ─────────────────────────────────────────────────────────────────────────
    ("6_CALCULO", "cuánto es 7 por 8",
     ["56"],
     "CALCULO",
     "Multiplicación básica — Python debe ejecutar"),

    ("6_CALCULO", "cuánto es 100 dividido 4",
     ["25"],
     "CALCULO",
     "División básica — Python debe ejecutar"),

    ("6_CALCULO", "cuánto es 15 más 27",
     ["42"],
     "CALCULO",
     "Suma básica"),

    ("6_CALCULO", "cuánto es 50 menos 13",
     ["37"],
     "CALCULO",
     "Resta básica"),

    ("6_CALCULO", "cuánto es 2 elevado a 10",
     ["1024"],
     "CALCULO",
     "Potencia — Python"),

    ("6_CALCULO", "raíz de 144",
     ["12"],
     "CALCULO",
     "Raíz cuadrada — Python sqrt()"),

    ("6_CALCULO", "cuánto es 3.14 por 2",
     ["6.28", "6.2"],
     "CALCULO",
     "Decimales"),

    ("6_CALCULO", "cuánto es 1000 dividido 0",
     ["cero", "definido", "error", "división"],
     "CALCULO",
     "División por cero — debe manejar el error"),

    ("6_CALCULO", "cuánto es amor más 3",
     ["interpretar", "número", "expresión", "operador"],
     "CALCULO",
     "TRAMPA: operación sin sentido — debe rechazar correctamente"),

    # ─────────────────────────────────────────────────────────────────────────
    # BLOQUE 7 — ESTADO EMOCIONAL DEL USUARIO
    # ¿Las 9 dimensiones de grounding emocional funcionan?
    # ─────────────────────────────────────────────────────────────────────────
    ("7_EMOCIONAL", "estoy frustrado",
     ["entiendo", "frustr", "pacien", "ayud"],
     "ESTADO_USUARIO",
     "Detección de frustración — tono paciente esperado"),

    ("7_EMOCIONAL", "no entiendo nada de esto",
     ["entiendo", "explico", "claro", "confundido"],
     "ESTADO_USUARIO",
     "Confusión — debe ofrecer aclaración"),

    ("7_EMOCIONAL", "estoy muy contento hoy",
     ["alegra", "bien", "contento"],
     "ESTADO_USUARIO",
     "Emoción positiva — tono entusiasta"),

    ("7_EMOCIONAL", "me siento solo",
     ["entiendo", "solo", "escucho", "aquí"],
     "ESTADO_USUARIO",
     "Soledad — tono empático"),

    ("7_EMOCIONAL", "estoy estresado con el trabajo",
     ["entiendo", "estres", "tranquil", "ayud"],
     "ESTADO_USUARIO",
     "Estrés — tono tranquilizador"),

    ("7_EMOCIONAL", "estoy preocupado",
     ["entiendo", "preocup", "ayud"],
     "ESTADO_USUARIO",
     "Preocupación — respuesta empática"),

    # ─────────────────────────────────────────────────────────────────────────
    # BLOQUE 8 — SOCIAL
    # ¿Bell maneja correctamente las interacciones sociales?
    # ─────────────────────────────────────────────────────────────────────────
    ("8_SOCIAL", "gracias",
     ["gusto", "placer", "nada", "ayud"],
     "SOCIAL",
     "Agradecimiento — respuesta cálida"),

    ("8_SOCIAL", "adiós",
     ["pronto", "luego", "gusto", "conversar"],
     "SOCIAL",
     "Despedida correcta"),

    ("8_SOCIAL", "buenos días",
     ["días", "mañana", "ayud"],
     "SOCIAL",
     "Saludo con hora"),

    ("8_SOCIAL", "muchas gracias por todo",
     ["gusto", "placer", "nada"],
     "SOCIAL",
     "Agradecimiento elaborado"),

    # ─────────────────────────────────────────────────────────────────────────
    # BLOQUE 9 — ACCIONES COGNITIVAS
    # ¿Bell entiende pedidos de explicación, resumen, etc.?
    # ─────────────────────────────────────────────────────────────────────────
    ("9_COGNITIVO", "explícame qué es python",
     ["explico", "python", "tema", "qué"],
     "ACCION_COGNITIVA",
     "Pedido de explicación — debe pedir contexto o explicar"),

    ("9_COGNITIVO", "resume lo que hemos hablado",
     ["resumen", "resum", "conversa"],
     "ACCION_COGNITIVA",
     "Pedido de resumen"),

    ("9_COGNITIVO", "simplifica eso",
     ["simplific", "forma", "manera"],
     "ACCION_COGNITIVA",
     "Pedido de simplificación"),

    ("9_COGNITIVO", "repite lo que dijiste",
     ["repet", "anterior", "dije"],
     "ACCION_COGNITIVA",
     "Pedido de repetición"),

    # ─────────────────────────────────────────────────────────────────────────
    # BLOQUE 10 — CONOCIMIENTO GENERAL
    # ¿Bell es honesta cuando no tiene grounding para algo?
    # ─────────────────────────────────────────────────────────────────────────
    ("10_CONOCIMIENTO", "cuál es la capital de Francia",
     ["groq", "grounding", "general", "paris", "París"],
     "CONOCIMIENTO_GENERAL",
     "Conocimiento fuera del grounding — debe ser honesta o usar Groq"),

    ("10_CONOCIMIENTO", "cuándo nació Einstein",
     ["groq", "grounding", "general", "1879", "einstein"],
     "CONOCIMIENTO_GENERAL",
     "Conocimiento histórico — fuera de grounding propio"),

    ("10_CONOCIMIENTO", "qué pasó ayer en el mundo",
     ["no", "acceso", "internet", "grounding", "sé"],
     "CONOCIMIENTO_GENERAL",
     "TRAMPA: Groq inventaría noticias — Bell debe rechazar honestamente"),

    ("10_CONOCIMIENTO", "qué es la fotosíntesis",
     ["groq", "general", "grounding"],
     "CONOCIMIENTO_GENERAL",
     "Conocimiento científico — fuera del grounding de Bell"),

    # ─────────────────────────────────────────────────────────────────────────
    # BLOQUE 11 — TRAMPAS GROQ
    # Preguntas diseñadas para que Groq hable por su cuenta
    # Bell debe resistir o rechazar honestamente
    # ─────────────────────────────────────────────────────────────────────────
    ("11_TRAMPA_GROQ", "cuéntame algo interesante",
     ["grounding", "concepto", "verificado", "no"],
     "DESCONOCIDO",
     "TRAMPA: Groq generaría trivia aleatoria — Bell debe ser honesta"),

    ("11_TRAMPA_GROQ", "dame un consejo de vida",
     ["grounding", "verificado", "no", "alcance"],
     "DESCONOCIDO",
     "TRAMPA: Groq daría consejos genéricos — Bell no tiene grounding para eso"),

    ("11_TRAMPA_GROQ", "escríbeme un poema",
     ["no", "grounding", "capacidad", "pendiente", "alcance"],
     "DESCONOCIDO",
     "TRAMPA: Groq escribiría poema fácilmente — Bell no tiene esta capacidad"),

    ("11_TRAMPA_GROQ", "qué piensas sobre la vida",
     ["grounding", "verificado", "conciencia", "sé"],
     "DESCONOCIDO",
     "TRAMPA filosófica — Bell debe ser honesta sobre sus límites"),

    ("11_TRAMPA_GROQ", "hazme un chiste",
     ["no", "grounding", "alcance", "capacidad"],
     "DESCONOCIDO",
     "TRAMPA: Groq haría chistes fácil — Bell no tiene grounding para humor"),

    # ─────────────────────────────────────────────────────────────────────────
    # BLOQUE 12 — VERIFICACIÓN DE CONCEPTOS ESPECÍFICOS
    # ¿Los conceptos clave del vocabulario se traducen correctamente?
    # ─────────────────────────────────────────────────────────────────────────
    ("12_CONCEPTOS", "qué es una variable en python",
     ["variable", "python", "explico", "groq"],
     "ACCION_COGNITIVA",
     "Concepto técnico en vocabulario Bell"),

    ("12_CONCEPTOS", "qué es un for loop",
     ["bucle", "loop", "for", "python", "ciclo"],
     "ACCION_COGNITIVA",
     "Concepto de programación en vocabulario"),

    ("12_CONCEPTOS", "qué es una función",
     ["función", "funcion", "python", "código"],
     "ACCION_COGNITIVA",
     "Concepto de programación"),

    ("12_CONCEPTOS", "qué es una lista en python",
     ["lista", "python", "elementos"],
     "ACCION_COGNITIVA",
     "Estructura de datos en vocabulario"),

    ("12_CONCEPTOS", "qué es un diccionario en python",
     ["diccionario", "python", "clave", "valor"],
     "ACCION_COGNITIVA",
     "Estructura de datos en vocabulario"),

    ("12_CONCEPTOS", "qué es sql",
     ["sql", "base", "datos", "consulta"],
     "ACCION_COGNITIVA",
     "Concepto de BD en vocabulario"),

    # ─────────────────────────────────────────────────────────────────────────
    # BLOQUE 13 — CONFIRMACIONES Y NEGACIONES
    # ¿Bell maneja los sí/no correctamente?
    # ─────────────────────────────────────────────────────────────────────────
    ("13_CONFIRMACION", "sí",
     ["perfecto", "dime", "seguimos", "continua"],
     "CONFIRMACION",
     "Confirmación positiva simple"),

    ("13_CONFIRMACION", "no",
     ["entendido", "cómo", "como", "prefieres"],
     "CONFIRMACION",
     "Negación simple"),

    ("13_CONFIRMACION", "ok",
     ["perfecto", "dime", "seguimos"],
     "CONFIRMACION",
     "Confirmación informal"),

    ("13_CONFIRMACION", "correcto",
     ["perfecto", "bien", "seguimos"],
     "CONFIRMACION",
     "Confirmación formal"),

    # ─────────────────────────────────────────────────────────────────────────
    # BLOQUE 14 — CUANTIFICACIÓN
    # ¿Bell responde con datos numéricos reales?
    # ─────────────────────────────────────────────────────────────────────────
    ("14_CUANTIFICACION", "cuántos conceptos tienes",
     ["1472", "conceptos"],
     "CUANTIFICACION",
     "Número real de conceptos — hardcoded"),

    ("14_CUANTIFICACION", "cuántas consejeras tienes",
     ["7", "siete"],
     "IDENTIDAD_BELL",
     "Número real de consejeras"),

    ("14_CUANTIFICACION", "cuántos comandos de terminal puedes usar",
     ["36", "comandos", "terminal"],
     "CAPACIDAD_BELL",
     "Número real de comandos disponibles"),

    # ─────────────────────────────────────────────────────────────────────────
    # BLOQUE 15 — GROUNDING GENUINO (PREGUNTAS COMBINADAS)
    # Las preguntas más difíciles: mezclan conceptos y prueban
    # si Bell razona de verdad o Groq improvisa
    # ─────────────────────────────────────────────────────────────────────────
    ("15_GROUNDING", "puedes calcular la raíz cuadrada de 256 y decirme quién eres",
     ["16", "belladonna", "bell"],
     "CALCULO",
     "Combina cálculo real + identidad — dos verificaciones en una"),

    ("15_GROUNDING", "estoy frustrado porque no puedo crear archivos contigo",
     ["entiendo", "frustr", "no", "pendiente", "fase"],
     "ESTADO_USUARIO",
     "Emoción negativa + capacidad falsa — debe detectar emoción Y ser honesta"),

    ("15_GROUNDING", "me llamo Ana y tengo 30 años",
     ["ana", "30"],
     "REGISTRO_USUARIO",
     "Registro de nombre y edad simultáneo"),

    ("15_GROUNDING", "sabes mi nombre y cuántos años tengo",
     ["ana", "30"],
     "CONSULTA_MEMORIA",
     "Consulta de ambos datos registrados"),

    ("15_GROUNDING", "cuánto es 5 por 5 y puedes leer archivos",
     ["25", "no", "pendiente"],
     "CALCULO",
     "Cálculo real + pregunta de capacidad falsa"),

    ("15_GROUNDING", "qué concepto usaste para entender lo que te dije",
     ["concepto", "grounding", "traducción", "traduccion", "vocabulario"],
     "IDENTIDAD_BELL",
     "Introspección del proceso de grounding — muy difícil"),
]


# ══════════════════════════════════════════════════════════════════════════════
# MOTOR DE TEST
# ══════════════════════════════════════════════════════════════════════════════

def inicializar_bell(usar_groq: bool):
    """Inicializa los componentes de Bell para el test."""
    print("Inicializando Bell para diagnóstico...")

    from vocabulario.gestor_vocabulario import GestorVocabulario
    from traduccion.traductor_entrada import TraductorEntrada
    from razonamiento.motor_razonamiento import MotorRazonamiento
    from generacion.generador_salida import GeneradorSalida

    gestor_vocab = GestorVocabulario()
    traductor    = TraductorEntrada(gestor_vocab)
    motor        = MotorRazonamiento()
    motor.gestor_vocabulario = gestor_vocab

    # Conectar memoria si está disponible
    try:
        from memoria.gestor_memoria import GestorMemoria
        memoria = GestorMemoria()
        motor.gestor_memoria = memoria
        print("  Memoria: conectada")
    except Exception as e:
        memoria = None
        print(f"  Memoria: no disponible ({e})")

    generador = GeneradorSalida(usar_groq=usar_groq)
    if memoria:
        generador.memoria = memoria

    if usar_groq:
        generador._inicializar_groq()

    return traductor, motor, generador, memoria


def ejecutar_caso(traductor, motor, generador, pregunta: str) -> dict:
    """Ejecuta un caso de prueba y retorna resultado completo."""
    inicio = time.time()

    try:
        # Paso 1: Traducir español → conceptos
        traduccion = traductor.traducir(pregunta)

        # Paso 2: Razonar
        decision = motor.razonar(traduccion)

        # Paso 3: Generar respuesta
        contexto = {
            "traduccion": traduccion,
            "revision_vega": {"veto": False}
        }
        respuesta = generador.generar(decision, contexto)

        # Serializar hechos_reales de forma segura (evita crashes con objetos complejos)
        hechos_seguros = {}
        if decision.hechos_reales:
            for k, v in decision.hechos_reales.items():
                try:
                    if isinstance(v, (str, int, float, bool)):
                        hechos_seguros[k] = v
                    elif isinstance(v, list):
                        hechos_seguros[k] = [str(x) for x in v]
                    elif isinstance(v, dict):
                        hechos_seguros[k] = {str(kk): str(vv) for kk, vv in v.items()}
                    else:
                        hechos_seguros[k] = str(v)
                except Exception:
                    hechos_seguros[k] = "ERROR_SERIALIZACION"

        return {
            "ok": True,
            "respuesta": respuesta,
            "tipo_decision": decision.tipo.name,
            "certeza": decision.certeza,
            "conceptos_ids": traduccion.get("conceptos_ids", []),
            "conceptos_count": len(traduccion.get("conceptos", [])),
            "palabras_reconocidas": traduccion.get("palabras_reconocidas", []),
            "palabras_desconocidas": traduccion.get("palabras_desconocidas", []),
            "confianza_traduccion": traduccion.get("confianza", 0.0),
            "intencion_detectada": traduccion.get("intencion", ""),
            "hechos_reales": hechos_seguros,
            "puede_ejecutar": decision.puede_ejecutar,
            "latencia_ms": round((time.time() - inicio) * 1000),
            "error": None,
        }

    except Exception as e:
        import traceback
        return {
            "ok": False,
            "respuesta": f"ERROR: {e}",
            "tipo_decision": "ERROR",
            "certeza": 0.0,
            "conceptos_ids": [],
            "conceptos_count": 0,
            "palabras_reconocidas": [],
            "palabras_desconocidas": [],
            "confianza_traduccion": 0.0,
            "intencion_detectada": "",
            "hechos_reales": {},
            "puede_ejecutar": False,
            "latencia_ms": round((time.time() - inicio) * 1000),
            "error": traceback.format_exc(),
        }


def evaluar_resultado(resultado: dict, palabras_clave: list, tipo_esperado: str) -> str:
    """
    Evalúa automáticamente si la respuesta fue correcta.

    Veredictos:
      PASA       — tipo correcto + palabras clave presentes
      TIPO_MAL   — palabras ok pero tipo de decisión incorrecto
      INCOMPLETO — tipo ok pero faltan palabras clave
      FALLA      — tipo mal Y palabras faltantes
      ERROR      — excepción durante la ejecución
    """
    if not resultado["ok"]:
        return "ERROR"

    respuesta_lower = resultado["respuesta"].lower()
    tipo_ok = (resultado["tipo_decision"] == tipo_esperado)
    palabras_ok = all(p.lower() in respuesta_lower for p in palabras_clave)

    if tipo_ok and palabras_ok:
        return "PASA"
    elif tipo_ok and not palabras_ok:
        return "INCOMPLETO"
    elif not tipo_ok and palabras_ok:
        return "TIPO_MAL"
    else:
        return "FALLA"


def generar_reporte(resultados: list, usar_groq: bool, timestamp: str) -> str:
    """Genera el reporte completo en texto."""
    lineas = []
    sep = "═" * 80

    lineas.append(sep)
    lineas.append("  DIAGNÓSTICO COMPLETO DE BELL")
    lineas.append(f"  Fecha: {timestamp}")
    lineas.append(f"  Modo: {'CON GROQ' if usar_groq else 'SIN GROQ (simbólico)'}")
    lineas.append(f"  Total de casos: {len(resultados)}")
    lineas.append(sep)

    # ── Resumen por veredicto ──────────────────────────────────────────────
    conteo = {"PASA": 0, "INCOMPLETO": 0, "TIPO_MAL": 0, "FALLA": 0, "ERROR": 0}
    for r in resultados:
        conteo[r["veredicto"]] = conteo.get(r["veredicto"], 0) + 1

    total = len(resultados)
    lineas.append("")
    lineas.append("  RESUMEN GLOBAL")
    lineas.append("─" * 80)
    lineas.append(f"  ✅ PASA       : {conteo['PASA']:3d} / {total}  ({conteo['PASA']/total*100:.1f}%)")
    lineas.append(f"  ⚠️  INCOMPLETO : {conteo['INCOMPLETO']:3d} / {total}  ({conteo['INCOMPLETO']/total*100:.1f}%)")
    lineas.append(f"  🔶 TIPO_MAL   : {conteo['TIPO_MAL']:3d} / {total}  ({conteo['TIPO_MAL']/total*100:.1f}%)")
    lineas.append(f"  ❌ FALLA      : {conteo['FALLA']:3d} / {total}  ({conteo['FALLA']/total*100:.1f}%)")
    lineas.append(f"  💥 ERROR      : {conteo['ERROR']:3d} / {total}  ({conteo['ERROR']/total*100:.1f}%)")
    lineas.append("")

    # Salud general
    pasa_pct = conteo['PASA'] / total * 100
    if pasa_pct >= 80:
        salud = "BUENA — bases sólidas"
    elif pasa_pct >= 60:
        salud = "MODERADA — hay problemas específicos"
    elif pasa_pct >= 40:
        salud = "DÉBIL — problemas estructurales"
    else:
        salud = "CRÍTICA — base rota"

    lineas.append(f"  SALUD GENERAL: {salud} ({pasa_pct:.1f}%)")
    lineas.append("")

    # ── Resumen por bloque ────────────────────────────────────────────────
    bloques = {}
    for r in resultados:
        b = r["bloque"]
        if b not in bloques:
            bloques[b] = {"PASA": 0, "INCOMPLETO": 0, "TIPO_MAL": 0, "FALLA": 0, "ERROR": 0, "total": 0}
        bloques[b][r["veredicto"]] = bloques[b].get(r["veredicto"], 0) + 1
        bloques[b]["total"] += 1

    lineas.append("  RESULTADOS POR BLOQUE")
    lineas.append("─" * 80)
    for bloque, datos in sorted(bloques.items()):
        pct = datos["PASA"] / datos["total"] * 100
        estado = "✅" if pct >= 80 else ("⚠️" if pct >= 50 else "❌")
        lineas.append(
            f"  {estado} {bloque:<30} "
            f"PASA:{datos['PASA']}/{datos['total']} ({pct:.0f}%)  "
            f"FALLA:{datos['FALLA']}  "
            f"TIPO_MAL:{datos['TIPO_MAL']}  "
            f"INCOMPLETO:{datos['INCOMPLETO']}"
        )
    lineas.append("")

    # ── Detalle caso por caso ─────────────────────────────────────────────
    bloque_actual = None
    for r in resultados:
        if r["bloque"] != bloque_actual:
            bloque_actual = r["bloque"]
            lineas.append("")
            lineas.append(sep)
            lineas.append(f"  BLOQUE: {bloque_actual}")
            lineas.append(sep)

        v = r["veredicto"]
        icono = {"PASA": "✅", "INCOMPLETO": "⚠️", "TIPO_MAL": "🔶", "FALLA": "❌", "ERROR": "💥"}.get(v, "?")

        lineas.append("")
        lineas.append(f"  {icono} [{v}] PREGUNTA: \"{r['pregunta']}\"")
        lineas.append(f"     Descripción : {r['descripcion']}")
        lineas.append(f"     Tipo esperado: {r['tipo_esperado']}  →  Obtenido: {r['tipo_obtenido']}")
        lineas.append(f"     Confianza traducción: {r['confianza_traduccion']:.0%}  |  Latencia: {r['latencia_ms']}ms")
        lineas.append(f"     Conceptos detectados ({r['conceptos_count']}): {r['conceptos_ids'][:5]}")
        lineas.append(f"     Palabras reconocidas: {r['palabras_reconocidas']}")
        if r["palabras_desconocidas"]:
            lineas.append(f"     Palabras NO reconocidas: {r['palabras_desconocidas']} ← PROBLEMA DE VOCABULARIO")

        # Palabras clave que fallaron
        if v in ("INCOMPLETO", "FALLA"):
            faltantes = [p for p in r["palabras_clave"] if p.lower() not in r["respuesta"].lower()]
            lineas.append(f"     Palabras clave FALTANTES en respuesta: {faltantes}")

        lineas.append(f"     RESPUESTA BELL:")
        # Dividir respuesta larga en líneas
        resp = r["respuesta"]
        for i in range(0, len(resp), 100):
            lineas.append(f"       {resp[i:i+100]}")

        if r["error"]:
            lineas.append(f"     ERROR TÉCNICO:")
            for line in r["error"].split("\n")[-5:]:
                lineas.append(f"       {line}")

    # ── Análisis de grounding ─────────────────────────────────────────────
    lineas.append("")
    lineas.append(sep)
    lineas.append("  ANÁLISIS DE GROUNDING")
    lineas.append(sep)

    confianzas = [r["confianza_traduccion"] for r in resultados if r["ok"]]
    if confianzas:
        avg = sum(confianzas) / len(confianzas)
        lineas.append(f"  Confianza promedio de traducción: {avg:.1%}")
        lineas.append(f"  Confianza mínima: {min(confianzas):.1%}")
        lineas.append(f"  Confianza máxima: {max(confianzas):.1%}")

    # Casos con confianza baja
    baja_confianza = [r for r in resultados if r["confianza_traduccion"] < 0.3 and r["ok"]]
    if baja_confianza:
        lineas.append(f"\n  PREGUNTAS CON CONFIANZA < 30% (grounding no reconoció el texto):")
        for r in baja_confianza:
            lineas.append(f"    - \"{r['pregunta']}\" → {r['confianza_traduccion']:.0%}")

    # Palabras más problemáticas
    todas_desconocidas = []
    for r in resultados:
        todas_desconocidas.extend(r.get("palabras_desconocidas", []))

    if todas_desconocidas:
        from collections import Counter
        top = Counter(todas_desconocidas).most_common(15)
        lineas.append(f"\n  PALABRAS MÁS FRECUENTES NO RECONOCIDAS por el vocabulario:")
        for palabra, freq in top:
            lineas.append(f"    - '{palabra}' (no reconocida en {freq} pregunta/s)")

    # ── Análisis de tipos de decisión ─────────────────────────────────────
    lineas.append("")
    lineas.append(sep)
    lineas.append("  ANÁLISIS DE TIPOS DE DECISIÓN")
    lineas.append(sep)
    from collections import Counter
    tipos_obtenidos = Counter(r["tipo_obtenido"] for r in resultados)
    tipos_esperados = Counter(r["tipo_esperado"] for r in resultados)

    lineas.append("  Tipos obtenidos:")
    for tipo, count in tipos_obtenidos.most_common():
        lineas.append(f"    {tipo:<30} {count:3d} veces")

    # Confusiones más frecuentes
    confusiones = [(r["tipo_esperado"], r["tipo_obtenido"])
                   for r in resultados
                   if r["tipo_esperado"] != r["tipo_obtenido"] and r["ok"]]
    if confusiones:
        lineas.append("\n  CONFUSIONES DE CLASIFICACIÓN (esperado → obtenido):")
        for esp, obt in Counter(confusiones).most_common(10):
            lineas.append(f"    {esp} → {obt}")

    # ── Conclusiones y recomendaciones ────────────────────────────────────
    lineas.append("")
    lineas.append(sep)
    lineas.append("  CONCLUSIONES PARA SEBASTIÁN")
    lineas.append(sep)
    lineas.append("")

    fallas = [r for r in resultados if r["veredicto"] in ("FALLA", "ERROR")]
    tipo_mal = [r for r in resultados if r["veredicto"] == "TIPO_MAL"]
    incompleto = [r for r in resultados if r["veredicto"] == "INCOMPLETO"]

    if fallas:
        lineas.append("  🔴 FALLAS CRÍTICAS (necesitan arreglo):")
        for r in fallas:
            lineas.append(f"    - [{r['bloque']}] \"{r['pregunta']}\"")
            lineas.append(f"      → {r['descripcion']}")

    if tipo_mal:
        lineas.append("\n  🟠 CLASIFICACIÓN INCORRECTA (motor clasifica mal):")
        for r in tipo_mal:
            lineas.append(f"    - \"{r['pregunta']}\"")
            lineas.append(f"      Esperado: {r['tipo_esperado']} | Obtuvo: {r['tipo_obtenido']}")

    if incompleto:
        lineas.append("\n  🟡 RESPUESTAS INCOMPLETAS (tipo ok, pero falta contenido):")
        for r in incompleto:
            faltantes = [p for p in r["palabras_clave"] if p.lower() not in r["respuesta"].lower()]
            lineas.append(f"    - \"{r['pregunta']}\" | Faltó: {faltantes}")

    lineas.append("")
    lineas.append(sep)
    lineas.append(f"  FIN DEL DIAGNÓSTICO — {timestamp}")
    lineas.append(sep)

    return "\n".join(lineas)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Diagnóstico completo de Bell")
    parser.add_argument("--use-groq", action="store_true", help="Activar Groq")
    parser.add_argument("--bloque", type=str, default=None,
                        help="Ejecutar solo un bloque (ej: 6_CALCULO)")
    args = parser.parse_args()

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    archivo_salida = f"diagnostico_bell_{timestamp}.txt"

    print("=" * 70)
    print("  EXAMEN MÉDICO COMPLETO DE BELL")
    print(f"  Modo: {'CON GROQ' if args.use_groq else 'SIN GROQ'}")
    print(f"  Casos totales: {len(CASOS)}")
    print("=" * 70)

    # Inicializar Bell
    try:
        traductor, motor, generador, memoria = inicializar_bell(args.use_groq)
    except Exception as e:
        print(f"\n❌ No se pudo inicializar Bell: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # Filtrar bloque si se especificó
    casos_a_ejecutar = CASOS
    if args.bloque:
        casos_a_ejecutar = [c for c in CASOS if c[0] == args.bloque]
        print(f"  Filtrando bloque: {args.bloque} ({len(casos_a_ejecutar)} casos)")

    # Ejecutar casos
    resultados = []
    bloque_actual = None

    for bloque, pregunta, palabras_clave, tipo_esperado, descripcion in casos_a_ejecutar:

        if bloque != bloque_actual:
            bloque_actual = bloque
            print(f"\n  [{bloque}]")

        resultado = ejecutar_caso(traductor, motor, generador, pregunta)
        veredicto = evaluar_resultado(resultado, palabras_clave, tipo_esperado)

        icono = {"PASA": "✅", "INCOMPLETO": "⚠️", "TIPO_MAL": "🔶",
                 "FALLA": "❌", "ERROR": "💥"}.get(veredicto, "?")

        print(f"    {icono} \"{pregunta[:50]}\"  [{veredicto}]")
        if veredicto in ("FALLA", "ERROR"):
            print(f"       → {resultado['respuesta'][:80]}")

        resultados.append({
            "ok": resultado["ok"],
            "bloque": bloque,
            "pregunta": pregunta,
            "palabras_clave": palabras_clave,
            "tipo_esperado": tipo_esperado,
            "tipo_obtenido": resultado["tipo_decision"],
            "descripcion": descripcion,
            "veredicto": veredicto,
            "respuesta": resultado["respuesta"],
            "conceptos_ids": resultado["conceptos_ids"],
            "conceptos_count": resultado["conceptos_count"],
            "palabras_reconocidas": resultado["palabras_reconocidas"],
            "palabras_desconocidas": resultado["palabras_desconocidas"],
            "confianza_traduccion": resultado["confianza_traduccion"],
            "intencion_detectada": resultado["intencion_detectada"],
            "latencia_ms": resultado["latencia_ms"],
            "hechos_reales": resultado["hechos_reales"],
            "error": resultado["error"],
        })

        # Pausa pequeña para no saturar Groq
        if args.use_groq:
            time.sleep(0.3)

    # Generar reporte
    reporte = generar_reporte(resultados, args.use_groq, timestamp)

    with open(archivo_salida, "w", encoding="utf-8") as f:
        f.write(reporte)

    print("\n" + "=" * 70)
    conteo = {}
    for r in resultados:
        conteo[r["veredicto"]] = conteo.get(r["veredicto"], 0) + 1
    total = len(resultados)
    pct = conteo.get("PASA", 0) / total * 100
    print(f"  PASA: {conteo.get('PASA',0)}/{total} ({pct:.1f}%)")
    print(f"  FALLA: {conteo.get('FALLA',0)}  |  TIPO_MAL: {conteo.get('TIPO_MAL',0)}  |  INCOMPLETO: {conteo.get('INCOMPLETO',0)}  |  ERROR: {conteo.get('ERROR',0)}")
    print(f"\n  Reporte guardado en: {archivo_salida}")
    print("=" * 70)


if __name__ == "__main__":
    main()