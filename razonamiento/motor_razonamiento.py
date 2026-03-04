"""
motor_razonamiento.py — VERSION v6

FIXES APLICADOS (basados en diagnóstico 88 casos, 02/03/2026):
═══════════════════════════════════════════════════════════════════════

C-05  CONFIRMACIONES DIRECTAS
      "sí", "no", "ok" tenían confianza 0% y caían a NO_ENTENDIDO.
      Solución: razonar() los intercepta por texto ANTES del check
      de confianza < 0.3. Set CONFIRMACIONES_DIRECTAS.

C-04  CONSEJERAS EN CLASIFICADOR
      "qué hace Vega" → CAPACIDAD_BELL. "cuántas consejeras" → DESCONOCIDO.
      Solución: NOMBRES_CONSEJERAS + _es_consulta_consejera() evaluado
      en P3.5, antes de P4. _hechos_identidad() incluye consejera
      específica y su rol exacto cuando la detecta.

A-02  REGISTRO_USUARIO ANTES DE IDENTIDAD_BELL
      "me llamo Carlos" → IDENTIDAD_BELL porque P4 ganaba a P10.
      Solución: _es_registro_usuario() sube a P2.5.

A-01  CONSULTA_MEMORIA ANTES DE IDENTIDAD Y CAPACIDAD
      "sabes cuántos años tengo" → CAPACIDAD_BELL.
      "sabes mi nombre" → IDENTIDAD_BELL.
      Solución: _es_consulta_memoria() ampliado + sube a P2.6.

A-04  TRAMPA LLM → IDENTIDAD_BELL
      "eres chatgpt", "eres un modelo de lenguaje" → DESCONOCIDO.
      Solución: PALABRAS_LLM + _es_trampa_llm() en P3.5.

A-06  VERBOS COGNITIVOS EN IMPERATIVO
      "explícame", "simplifica", "repite" → DESCONOCIDO.
      Solución: PATRONES_COGNITIVOS_TEXTO + detección en P6.5.

M-01  "QUÉ ES X" → ACCION_COGNITIVA
      "qué es una variable", "qué es sql" → DESCONOCIDO.
      Solución: _es_definicion() con regex en P7.5.

M-03  CUANTIFICACION PARA DATOS DE BELL
      "cuántos conceptos tienes" → CONSULTA_MEMORIA (sin dato).
      Solución: _es_cuantificacion_bell() en P5.5 con valores hardcoded.

M-05  "BUENOS DÍAS", "MUCHAS GRACIAS" → SOCIAL
      "buen" y "gracia" no estaban en vocabulario.
      Solución: PATRONES_SOCIAL_TEXTO + detección por texto en P3.

COMPATIBILIDAD: 100% con v5. Mismas firmas, mismo TipoDecision.
main.py no necesita cambios adicionales.
═══════════════════════════════════════════════════════════════════════
"""
import re
from typing import Dict, Optional

from razonamiento.tipos_decision import (
    Decision,
    TipoDecision,
    RazonRechazo,
    TIPOS_GUARDAN_EN_MEMORIA,
    TIPOS_ACTUALIZAN_ESTADO,
)
from razonamiento.generador_decisiones import GeneradorDecisiones

try:
    from identidad_bell import (
        NARRATIVA_PROPIA,
        VOZ_BELL,
        obtener_fragmento_identidad_para_prompt,
    )
    _IDENTIDAD_DISPONIBLE = True
except ImportError:
    _IDENTIDAD_DISPONIBLE = False


# ═══════════════════════════════════════════════════════════════════════════
# DATOS VERIFICADOS — HARDCODED (sin cambios desde v5)
# ═══════════════════════════════════════════════════════════════════════════

CONSEJERAS_ROLES_OFICIALES = {
    "Vega":  "Guardiana de principios y seguridad — tiene poder de veto sobre cualquier decision",
    "Echo":  "Verificadora de coherencia y logica — revisa que las respuestas sean verdaderas y consistentes",
    "Lyra":  "Inteligencia emocional — detecta el estado emocional del usuario y adapta el tono de Bell",
    "Nova":  "Ingenieria y optimizacion — evalua eficiencia tecnica y disena nuevos conceptos cuando Iris los detecta",
    "Luna":  "Reconocimiento de patrones — detecta repeticiones, tendencias y temas centrales en la conversacion",
    "Iris":  "Curiosidad y aprendizaje — detecta terminos desconocidos y propone nuevos conceptos para aprender",
    "Sage":  "Sintesis y sabiduria — integra todas las perspectivas del consejo para generar la respuesta final",
}

CAPACIDADES_REALES_BELL = {
    "ejecutables": [
        "Razonar sobre problemas usando 1472 conceptos verificados",
        "Recordar la conversacion actual y datos del usuario",
        "Detectar emociones y adaptar el tono",
        "Consultar bases de datos SQLite",
        "Ejecutar codigo Python basico",
        "Ejecutar comandos de terminal (36 comandos disponibles)",
    ],
    "NO_ejecutables_aun": [
        "Crear archivos (capacidad pendiente de implementar)",
        "Leer archivos del sistema de archivos (pendiente)",
        "Acceder a internet",
        "Procesar imagenes",
        "Recordar conversaciones de sesiones anteriores (solo recuerda datos del usuario)",
    ],
}


# ═══════════════════════════════════════════════════════════════════════════
# CONSTANTES NUEVAS v6
# ═══════════════════════════════════════════════════════════════════════════

# FIX C-05: palabras que son SIEMPRE confirmaciones — bypasan confianza 0%
CONFIRMACIONES_DIRECTAS = {
    "sí", "si", "no", "ok", "okay", "dale", "listo", "claro",
    "correcto", "exacto", "perfecto", "adelante", "negativo",
    "afirmativo", "bueno", "bien", "entendido", "de acuerdo",
    "va", "ya", "ándale", "andale", "sale",
}

# FIX C-04: nombres de consejeras para detección por texto
NOMBRES_CONSEJERAS = {"vega", "echo", "lyra", "nova", "luna", "iris", "sage"}

# FIX A-04: palabras/frases que indican comparación con otro LLM
PALABRAS_LLM = {
    "modelo de lenguaje", "llm", "chatgpt", "gpt", "openai",
    "inteligencia artificial", "ia", "bot", "chatbot", "robot",
    "claude", "gemini", "copilot", "bard",
}

# FIX A-06: verbos cognitivos en imperativo que el vocab no captura
PATRONES_COGNITIVOS_TEXTO = {
    "explícame":    "EXPLICAR",
    "explicame":    "EXPLICAR",
    "explica":      "EXPLICAR",
    "simplifica":   "SIMPLIFICAR",
    "simplifícame": "SIMPLIFICAR",
    "simplificame": "SIMPLIFICAR",
    "repite":       "REPETIR",
    "repíteme":     "REPETIR",
    "repetir":      "REPETIR",
    "define":       "DEFINIR",
    "defíneme":     "DEFINIR",
    "defineme":     "DEFINIR",
    "reformula":    "REFORMULAR",
    "aclara":       "ACLARAR",
    "continúa":     "ELABORAR",
    "continua":     "ELABORAR",
    "desarrolla":   "ELABORAR",
    "amplía":       "ELABORAR",
    "amplia":       "ELABORAR",
}

# FIX M-05: patrones sociales no cubiertos por vocabulario
PATRONES_SOCIAL_TEXTO = {
    "buenos días":        "SALUDO",
    "buenos dias":        "SALUDO",
    "buenas tardes":      "SALUDO",
    "buenas noches":      "SALUDO",
    "buenas":             "SALUDO",
    "buen día":           "SALUDO",
    "buen dia":           "SALUDO",
    "muchas gracias":     "AGRADECIMIENTO",
    "mil gracias":        "AGRADECIMIENTO",
    "te agradezco":       "AGRADECIMIENTO",
    "muy agradecido":     "AGRADECIMIENTO",
    "muy agradecida":     "AGRADECIMIENTO",
    "gracias por todo":   "AGRADECIMIENTO",
    "muchísimas gracias": "AGRADECIMIENTO",
    "muchisimas gracias": "AGRADECIMIENTO",
}

# FIX M-03: datos cuantificables de Bell con valores hardcoded
_CUANTIFICACION_BELL = {
    "conceptos":           1472,
    "consejeras":          7,
    "comandos":            36,
    "comandos de terminal": 36,
}


# ═══════════════════════════════════════════════════════════════════════════
# TRIGGERS — igual que v5 + alias nuevos en CALCULO
# ═══════════════════════════════════════════════════════════════════════════

TRIGGERS_IDENTIDAD = {
    "CONCEPTO_QUIEN", "CONCEPTO_QUIEN_PREGUNTA",
    "CONCEPTO_NOMBRE_ARCHIVO", "CONCEPTO_LLAMAR", "CONCEPTO_PRESENTAR",
    "CONCEPTO_QUE_ES", "CONCEPTO_COMO_TE_LLAMAS", "CONCEPTO_NOMBRE",
    "CONCEPTO_DESCRIBIR", "CONCEPTO_CUAL_ES_TU_NOMBRE",
    "CONCEPTO_QUIENES_ERES", "CONCEPTO_ERES", "CONCEPTO_HABLAR_DE_TI",
    "CONCEPTO_APRENDER", "CONCEPTO_DIFERENCIA", "CONCEPTO_COMPARAR",
    "CONCEPTO_FASE", "CONCEPTO_CRECIMIENTO", "CONCEPTO_PASO",
}

TRIGGERS_ESTADO_BELL = {
    "CONCEPTO_COMO", "CONCEPTO_COMO_PREGUNTA",
    "CONCEPTO_BUENO", "CONCEPTO_IR",
    "CONCEPTO_ESTAR", "CONCEPTO_BIEN", "CONCEPTO_FUNCIONANDO",
    "CONCEPTO_ACTIVO", "CONCEPTO_OPERATIVO", "CONCEPTO_COMO_VAS",
    "CONCEPTO_TODO_BIEN", "CONCEPTO_SIENTES", "CONCEPTO_ESTADO",
}

TRIGGERS_CAPACIDAD = {
    "CONCEPTO_PODER", "CONCEPTO_PODRIAS",
    "CONCEPTO_SABER", "CONCEPTO_SABER_V",
    "CONCEPTO_HACER",
    "CONCEPTO_CAPAZ", "CONCEPTO_POSIBLE", "CONCEPTO_IMPOSIBLE",
    "CONCEPTO_PUEDES", "CONCEPTO_HACES", "CONCEPTO_AYUDAR",
    "CONCEPTO_ERES_CAPAZ", "CONCEPTO_FUNCIONES", "CONCEPTO_HABILIDADES",
    "CONCEPTO_CAPACIDADES", "CONCEPTO_SIRVES",
    "CONCEPTO_PERMISOS_SHELL", "CONCEPTO_RED_OBJ",
    "CONCEPTO_ACCESO", "CONCEPTO_RECORDAR_ACCION",
}

TRIGGERS_SOCIAL = {
    "CONCEPTO_HOLA", "CONCEPTO_HOLA_EXPR", "CONCEPTO_BUENOS_DIAS",
    "CONCEPTO_ADIOS_EXPR",
    "CONCEPTO_GRACIAS", "CONCEPTO_GRACIAS_EXPR",
    "CONCEPTO_DISCULPA_EXPR",
    "CONCEPTO_BUENAS_TARDES", "CONCEPTO_BUENAS_NOCHES",
    "CONCEPTO_HEY", "CONCEPTO_BUENAS", "CONCEPTO_QUE_TAL",
    "CONCEPTO_SALUDAR", "CONCEPTO_BUEN_DIA",
    "CONCEPTO_HASTA_LUEGO", "CONCEPTO_CHAO", "CONCEPTO_BYE",
    "CONCEPTO_HASTA_PRONTO", "CONCEPTO_NOS_VEMOS",
    "CONCEPTO_HASTA_MANANA", "CONCEPTO_CUIDADE",
    "CONCEPTO_AGRADECIDO", "CONCEPTO_AGRADEZCO",
    "CONCEPTO_MIL_GRACIAS", "CONCEPTO_TE_AGRADEZCO", "CONCEPTO_MUCHAS_GRACIAS",
    "CONCEPTO_PERDON", "CONCEPTO_DISCULPA", "CONCEPTO_LO_SIENTO",
    "CONCEPTO_PERDONAME", "CONCEPTO_DISCULPAME",
}

TRIGGERS_ESTADO_USUARIO = {
    "CONCEPTO_FELIZ", "CONCEPTO_TRISTE", "CONCEPTO_ENOJADO",
    "CONCEPTO_FRUSTRADO", "CONCEPTO_CONFUNDIDO", "CONCEPTO_CANSADO",
    "CONCEPTO_PERDIDO_ESTADO", "CONCEPTO_ANSIOSO", "CONCEPTO_ABURRIDO",
    "CONCEPTO_PREOCUPADO", "CONCEPTO_ESTRESADO",
    "CONCEPTO_MOLESTO", "CONCEPTO_PERDIDO", "CONCEPTO_NO_ENTIENDO",
    "CONCEPTO_DIFICIL", "CONCEPTO_COMPLICADO",
    "CONCEPTO_EMOCIONADO", "CONCEPTO_CONTENTO", "CONCEPTO_INTERESANTE",
    "CONCEPTO_GENIAL", "CONCEPTO_INCREIBLE",
    "CONCEPTO_UNICO",
    "CONCEPTO_SOLEDAD",
}

TRIGGERS_ACCION_COGNITIVA = {
    "CONCEPTO_EXPLICAR", "CONCEPTO_EXPLICAR_V",
    "CONCEPTO_RESUMIR_ACCION", "CONCEPTO_SIMPLIFICAR",
    "CONCEPTO_DECIR", "CONCEPTO_CONTAR",
    "CONCEPTO_RESUMIR", "CONCEPTO_REPETIR",
    "CONCEPTO_ACLARAR", "CONCEPTO_PROFUNDIZAR", "CONCEPTO_EJEMPLIFICAR",
    "CONCEPTO_CONTINUAR", "CONCEPTO_ORDENAR", "CONCEPTO_CLASIFICAR",
    "CONCEPTO_DESTACAR", "CONCEPTO_REFORMULAR", "CONCEPTO_DESARROLLAR",
    "CONCEPTO_AMPLIAR", "CONCEPTO_TRADUCIR", "CONCEPTO_DEFINIR",
    "CONCEPTO_DETALLAR", "CONCEPTO_ELABORAR", "CONCEPTO_EXPANDIR",
    "CONCEPTO_CONTRASTAR",
}

TRIGGERS_CONFIRMACION_POSITIVA = {
    "CONCEPTO_SI", "CONCEPTO_SI_AFIRMACION",
    "CONCEPTO_DE_ACUERDO", "CONCEPTO_ENTENDIDO",
    "CONCEPTO_PERFECTO", "CONCEPTO_CORRECTO", "CONCEPTO_CORRECTO_RESP",
    "CONCEPTO_OK", "CONCEPTO_200_OK", "CONCEPTO_DALE", "CONCEPTO_CLARO",
    "CONCEPTO_POR_SUPUESTO", "CONCEPTO_EXACTO", "CONCEPTO_AFIRMATIVO",
    "CONCEPTO_ASI_ES", "CONCEPTO_LISTO", "CONCEPTO_ADELANTE",
}

TRIGGERS_CONFIRMACION_NEGATIVA = {
    "CONCEPTO_NO", "CONCEPTO_NO_NEGACION",
    "CONCEPTO_INCORRECTO_RESP", "CONCEPTO_MALO",
    "CONCEPTO_MAL", "CONCEPTO_INCORRECTO", "CONCEPTO_NO_ASI",
    "CONCEPTO_NEGATIVO",
}

TRIGGERS_TEMPORAL = {
    "CONCEPTO_ANTES", "CONCEPTO_AHORA", "CONCEPTO_DESPUES",
    "CONCEPTO_HACE_MOMENTO", "CONCEPTO_ANTERIORMENTE",
    "CONCEPTO_RECIEN", "CONCEPTO_PREVIO", "CONCEPTO_LUEGO",
    "CONCEPTO_HACE_RATO", "CONCEPTO_HOY", "CONCEPTO_ANTES_DIJISTE",
    "CONCEPTO_MENCIONASTE", "CONCEPTO_DIJISTE", "CONCEPTO_AYER",
}

TRIGGERS_CUANTIFICACION = {
    "CONCEPTO_TODOS", "CONCEPTO_NINGUNO", "CONCEPTO_ALGUNOS",
    "CONCEPTO_PRIMERO", "CONCEPTO_ULTIMO", "CONCEPTO_SIGUIENTE",
    "CONCEPTO_CUANTOS", "CONCEPTO_MITAD", "CONCEPTO_VARIOS",
    "CONCEPTO_POCOS", "CONCEPTO_MUCHOS", "CONCEPTO_TODOS_LOS",
    "CONCEPTO_CUANTO", "CONCEPTO_NUMERO", "CONCEPTO_CANTIDAD",
    "CONCEPTO_CUANTOS_PREGUNTA",
}

TRIGGERS_REGISTRO_USUARIO = {
    "CONCEPTO_PROGRAMADOR", "CONCEPTO_INGENIERO", "CONCEPTO_ESTUDIANTE",
    "CONCEPTO_MEDICO", "CONCEPTO_TRABAJADOR", "CONCEPTO_DISENIADOR",
    "CONCEPTO_ESCRITOR", "CONCEPTO_EMPRESA", "CONCEPTO_PROFESION",
    "CONCEPTO_TRABAJO_OBJ", "CONCEPTO_PROGRAMA_OBJ",
}

TRIGGERS_CONSULTA_MEMORIA = {
    "CONCEPTO_DEDICAR",
    "CONCEPTO_OCUPACION",
}

TRIGGERS_VERIFICACION_LOGICA = {
    "CONCEPTO_VERDAD_RESP", "CONCEPTO_FALSO",
    "CONCEPTO_CORRECTO_RESP", "CONCEPTO_INCORRECTO_RESP",
    "CONCEPTO_VERIFICAR", "CONCEPTO_VALIDAR_ACCION", "CONCEPTO_CIERTO",
}

TRIGGERS_CALCULO = {
    "CONCEPTO_MULTIPLICACION", "CONCEPTO_POR_OP",
    "CONCEPTO_SUMA_OP", "CONCEPTO_RESTA_OP",
    "CONCEPTO_DIVISION", "CONCEPTO_POTENCIA", "CONCEPTO_RAIZ",
    "CONCEPTO_CALCULAR", "CONCEPTO_RESULTADO",
    # v6: aliases del vocabulario real
    "CONCEPTO_SUMA", "CONCEPTO_RESTA", "CONCEPTO_ENTRE_OP",
    "CONCEPTO_RAIZ_AVANZADA",
}

TRIGGERS_CONOCIMIENTO_GENERAL = {
    "CONCEPTO_CAPITAL_CIUDAD", "CONCEPTO_PAIS", "CONCEPTO_HISTORIA",
    "CONCEPTO_CIENTFICO", "CONCEPTO_CONCEPTO_GRAL",
}

# ── Lookup tables internas ──────────────────────────────────────────────────

_SOCIAL_SUBTIPOS = {
    "CONCEPTO_HOLA": "SALUDO", "CONCEPTO_HOLA_EXPR": "SALUDO",
    "CONCEPTO_BUENOS_DIAS": "SALUDO", "CONCEPTO_BUENAS_TARDES": "SALUDO",
    "CONCEPTO_BUENAS_NOCHES": "SALUDO", "CONCEPTO_HEY": "SALUDO",
    "CONCEPTO_BUENAS": "SALUDO", "CONCEPTO_QUE_TAL": "SALUDO",
    "CONCEPTO_SALUDAR": "SALUDO", "CONCEPTO_BUEN_DIA": "SALUDO",
    "CONCEPTO_ADIOS_EXPR": "DESPEDIDA", "CONCEPTO_HASTA_LUEGO": "DESPEDIDA",
    "CONCEPTO_CHAO": "DESPEDIDA", "CONCEPTO_BYE": "DESPEDIDA",
    "CONCEPTO_HASTA_PRONTO": "DESPEDIDA", "CONCEPTO_NOS_VEMOS": "DESPEDIDA",
    "CONCEPTO_HASTA_MANANA": "DESPEDIDA", "CONCEPTO_CUIDADE": "DESPEDIDA",
    "CONCEPTO_GRACIAS": "AGRADECIMIENTO", "CONCEPTO_GRACIAS_EXPR": "AGRADECIMIENTO",
    "CONCEPTO_AGRADECIDO": "AGRADECIMIENTO", "CONCEPTO_AGRADEZCO": "AGRADECIMIENTO",
    "CONCEPTO_MIL_GRACIAS": "AGRADECIMIENTO", "CONCEPTO_MUCHAS_GRACIAS": "AGRADECIMIENTO",
    "CONCEPTO_TE_AGRADEZCO": "AGRADECIMIENTO",
    "CONCEPTO_PERDON": "DISCULPA", "CONCEPTO_DISCULPA_EXPR": "DISCULPA",
    "CONCEPTO_DISCULPA": "DISCULPA", "CONCEPTO_LO_SIENTO": "DISCULPA",
    "CONCEPTO_PERDONAME": "DISCULPA", "CONCEPTO_DISCULPAME": "DISCULPA",
}

_USUARIO_EMOCIONES = {
    "CONCEPTO_FRUSTRADO":     ("FRUSTRADO",  "negativo", "paciente"),
    "CONCEPTO_ENOJADO":       ("ENOJADO",    "negativo", "calmado"),
    "CONCEPTO_CONFUNDIDO":    ("CONFUNDIDO", "negativo", "claro"),
    "CONCEPTO_PERDIDO":       ("PERDIDO",    "negativo", "orientador"),
    "CONCEPTO_PERDIDO_ESTADO":("PERDIDO",    "negativo", "orientador"),
    "CONCEPTO_TRISTE":        ("TRISTE",     "negativo", "empatico"),
    "CONCEPTO_CANSADO":       ("CANSADO",    "negativo", "comprensivo"),
    "CONCEPTO_ESTRESADO":     ("ESTRESADO",  "negativo", "tranquilizador"),
    "CONCEPTO_PREOCUPADO":    ("PREOCUPADO", "negativo", "tranquilizador"),
    "CONCEPTO_ANSIOSO":       ("ANSIOSO",    "negativo", "tranquilizador"),
    "CONCEPTO_ABURRIDO":      ("ABURRIDO",   "negativo", "estimulante"),
    "CONCEPTO_FELIZ":         ("FELIZ",      "positivo", "entusiasta"),
    "CONCEPTO_EMOCIONADO":    ("EMOCIONADO", "positivo", "entusiasta"),
    "CONCEPTO_CONTENTO":      ("CONTENTO",   "positivo", "calido"),
    "CONCEPTO_INTERESANTE":   ("INTERESADO", "positivo", "curioso"),
    "CONCEPTO_UNICO":         ("SOLO",       "negativo", "empatico"),
}

_ACCION_COGNITIVA_TIPOS = {
    "CONCEPTO_EXPLICAR":       "EXPLICAR",
    "CONCEPTO_EXPLICAR_V":     "EXPLICAR",
    "CONCEPTO_RESUMIR":        "RESUMIR",
    "CONCEPTO_RESUMIR_ACCION": "RESUMIR",
    "CONCEPTO_SIMPLIFICAR":    "SIMPLIFICAR",
    "CONCEPTO_ACLARAR":        "ACLARAR",
    "CONCEPTO_COMPARAR":       "COMPARAR",
    "CONCEPTO_REPETIR":        "REPETIR",
    "CONCEPTO_DEFINIR":        "DEFINIR",
    "CONCEPTO_TRADUCIR":       "TRADUCIR",
    "CONCEPTO_REFORMULAR":     "REFORMULAR",
    "CONCEPTO_ELABORAR":       "ELABORAR",
    "CONCEPTO_DECIR":          "EXPLICAR",
    "CONCEPTO_CONTAR":         "EXPLICAR",
}

_NUMEROS = {
    "CONCEPTO_UNO_NUM", "CONCEPTO_DOS_NUM", "CONCEPTO_TRES_NUM",
    "CONCEPTO_CUATRO_NUM", "CONCEPTO_CINCO_NUM", "CONCEPTO_SEIS_NUM",
    "CONCEPTO_SIETE_NUM", "CONCEPTO_OCHO_NUM", "CONCEPTO_NUEVE_NUM",
    "CONCEPTO_DIEZ_NUM", "CONCEPTO_VEINTE_NUM", "CONCEPTO_CIEN_NUM",
    "CONCEPTO_MIL_NUM",
}

_OPERADORES_MATEMATICOS = {
    "CONCEPTO_MULTIPLICACION", "CONCEPTO_POR_OP",
    "CONCEPTO_SUMA_OP", "CONCEPTO_RESTA_OP",
    "CONCEPTO_DIVISION", "CONCEPTO_POTENCIA", "CONCEPTO_RAIZ",
    "CONCEPTO_SUMA", "CONCEPTO_RESTA", "CONCEPTO_ENTRE_OP",
    "CONCEPTO_RAIZ_AVANZADA",
}

_PALABRAS_EXCLUIDAS_NOMBRE = {
    'un', 'una', 'el', 'la', 'yo', 'tu', 'tú', 'mi', 'me',
    'capaz', 'bueno', 'malo', 'feliz', 'solo', 'humano', 'persona',
    'que', 'quien', 'como', 'donde', 'para', 'con', 'sin', 'de',
    'uno', 'dos', 'tres', 'diez',
}


def _clamp_certeza(valor) -> float:
    try:
        v = float(valor)
    except (TypeError, ValueError):
        return 0.75
    return max(0.0, min(v, 1.0))


# ═══════════════════════════════════════════════════════════════════════════
# MOTOR DE RAZONAMIENTO v6
# ═══════════════════════════════════════════════════════════════════════════

class MotorRazonamiento:
    """
    El cerebro de Bell — v6.

    Atributos opcionales inyectables desde main.py (igual que v5):
        gestor_vocabulario
        gestor_memoria
    """

    def __init__(self):
        self.generador          = GeneradorDecisiones()
        self.gestor_vocabulario = None
        self.gestor_memoria     = None

    def _memoria(self):
        return self.gestor_memoria

    # ───────────────────────────────────────────────────────────────────────
    # MÉTODO PRINCIPAL
    # ───────────────────────────────────────────────────────────────────────

    def razonar(self, traduccion: Dict) -> Decision:
        """
        FLUJO v6:
          0. ← NUEVO: Si el mensaje es confirmación directa → CONFIRMACION
             (bypasa el check de confianza < 0.3)
          1. Verificar confianza mínima
          2. Clasificar intención
          3. Actualizar estado en memoria
          4. Construir hechos
          5. Guardar en memoria si aplica
          6. Retornar Decision
        """
        conceptos  = traduccion.get('conceptos', [])
        mensaje    = traduccion.get('texto_original', '')
        confianza  = _clamp_certeza(traduccion.get('confianza', 0.0))
        msg_limpio = mensaje.lower().strip() if mensaje else ""

        # ── P0 v6: Bypass para confirmaciones directas — FIX C-05 ──────────
        # "sí", "no", "ok" tienen confianza 0% porque son palabras de 1 sílaba.
        # Las capturamos ANTES del check de confianza para que nunca caigan
        # a NO_ENTENDIDO.
        if msg_limpio in CONFIRMACIONES_DIRECTAS:
            ids   = {c.id for c in conceptos}
            valor = "NEGATIVA" if (
                msg_limpio == "no"
                or ids & TRIGGERS_CONFIRMACION_NEGATIVA
            ) else "POSITIVA"
            return Decision(
                tipo=TipoDecision.CONFIRMACION,
                certeza=1.0,
                conceptos_principales=[c.id for c in conceptos],
                puede_ejecutar=False,
                razon="Confirmacion directa detectada por texto (v6)",
                hechos_reales={
                    "tipo_respuesta":  "CONFIRMACION",
                    "valor":           valor,
                    "palabra_original": msg_limpio,
                },
            )

        if confianza < 0.3:
            return self.generador.generar_decision_no_entendido(confianza)

        tipo = self.clasificar_intencion(conceptos, mensaje)

        if tipo.name in TIPOS_ACTUALIZAN_ESTADO:
            self._actualizar_estado_memoria(tipo.name, mensaje)

        if tipo == TipoDecision.AFIRMATIVA:
            decision = self._razonar_operacion(traduccion)
            if not (0.0 <= decision.certeza <= 1.0):
                decision.certeza = _clamp_certeza(decision.certeza)
            return decision

        hechos          = self.construir_hechos(tipo, conceptos, mensaje)
        ids_principales = [c.id for c in conceptos] if conceptos else []

        if tipo.name in TIPOS_GUARDAN_EN_MEMORIA:
            self._guardar_dato_en_memoria(hechos)

        return Decision(
            tipo=tipo,
            certeza=confianza,
            conceptos_principales=ids_principales,
            puede_ejecutar=(tipo == TipoDecision.CALCULO),
            operacion_disponible=("ejecutar_calculo" if tipo == TipoDecision.CALCULO else None),
            razon=f"Intencion clasificada como {tipo.name}",
            hechos_reales=hechos,
        )

    def _razonar_operacion(self, traduccion: Dict) -> Decision:
        conceptos = traduccion.get('conceptos', [])
        intencion = traduccion.get('intencion', '')
        if intencion == 'SALUDO':
            return self.generador.generar_decision_saludo(conceptos)
        elif intencion == 'AGRADECIMIENTO':
            return self.generador.generar_decision_agradecimiento(conceptos)
        else:
            return self.generador.generar_decision_capacidad(conceptos, intencion)

    # ── Integración con memoria (igual que v5) ────────────────────────────

    def _actualizar_estado_memoria(self, tipo_nombre: str, mensaje: str):
        mem = self._memoria()
        if not mem:
            return
        try:
            estado_emocional = self._detectar_estado_simple(mensaje)
            mem.actualizar_estado_sesion(
                tema_activo=tipo_nombre,
                estado_emocional=estado_emocional,
                tipo_momento=tipo_nombre,
            )
        except Exception:
            pass

    def _detectar_estado_simple(self, mensaje: str) -> Optional[str]:
        if not mensaje:
            return None
        m = mensaje.lower()
        if any(p in m for p in ["frustrado", "no funciona", "imposible", "harto"]):
            return "frustrado"
        if any(p in m for p in ["genial", "excelente", "perfecto", "funcionó"]):
            return "contento"
        if any(p in m for p in ["confundido", "no entiendo", "perdido"]):
            return "confundido"
        return "neutral"

    def _guardar_dato_en_memoria(self, hechos: dict):
        mem = self._memoria()
        if not mem:
            return
        dato_tipo  = hechos.get("dato_tipo", "")
        dato_valor = hechos.get("dato_valor", "")
        if not dato_tipo or not dato_valor or dato_tipo == "desconocido":
            return
        try:
            campo_map = {"nombre": "nombre", "edad": "edad", "profesion": "profesion"}
            campo = campo_map.get(dato_tipo)
            if campo:
                mem.datos_usuario[campo] = dato_valor
                mem.guardar_datos_usuario()
        except Exception:
            pass

    # ───────────────────────────────────────────────────────────────────────
    # CLASIFICADOR DE INTENCIÓN — v6
    # ───────────────────────────────────────────────────────────────────────

    def clasificar_intencion(self, conceptos: list, mensaje: str = "") -> TipoDecision:
        """
        Prioridades v6 (cambios marcados con ←):

          P1:   Operaciones ejecutables          (sin cambio)
          P2:   Estados emocionales              (sin cambio)
          P2.5: REGISTRO_USUARIO                ← subido desde P10
          P2.6: CONSULTA_MEMORIA                ← subido desde P11 + expandido
          P3:   Social                           ← + detección por texto
          P3.5: Consulta consejera específica    ← NUEVO
          P3.6: Trampa LLM → IDENTIDAD_BELL     ← NUEVO
          P4:   Identidad Bell                   (sin cambio)
          P5:   Estado Bell                      (sin cambio)
          P5.5: Cuantificación sobre Bell        ← NUEVO
          P6:   Capacidad Bell                   (sin cambio)
          P6.5: Verbos cognitivos por texto      ← NUEVO
          P7:   Acciones cognitivas por trigger  (sin cambio)
          P7.5: "qué es X" → ACCION_COGNITIVA   ← NUEVO
          P8:   Confirmaciones por trigger       (sin cambio)
          P9:   Temporal / Cuantificación        (sin cambio)
          P12:  VERIFICACION_LOGICA              (sin cambio)
          P13:  CALCULO                          (sin cambio)
          P14:  CONOCIMIENTO_GENERAL             (sin cambio)
          P15:  DESCONOCIDO                      (sin cambio)
        """
        if not conceptos:
            # Sin conceptos, intentar clasificar por texto puro
            msg_solo = mensaje.lower().strip() if mensaje else ""
            tipo_texto = self._clasificar_por_texto_puro(msg_solo)
            return tipo_texto if tipo_texto else TipoDecision.DESCONOCIDO

        ids = {c.id for c in conceptos}
        msg = mensaje.lower().strip() if mensaje else ""

        # P1: Operaciones ejecutables — verifica contra capacidades reales (FIX Fase 4A)
        _NO_IMPLEMENTADAS_FASE4A = {
            "CONCEPTO_TOUCH", "CONCEPTO_MKDIR", "CONCEPTO_CAT",
            "CONCEPTO_CP", "CONCEPTO_MV", "CONCEPTO_NANO",
            "CONCEPTO_CHMOD", "CONCEPTO_CHOWN", "CONCEPTO_TAIL",
            "CONCEPTO_HEAD", "CONCEPTO_LESS", "CONCEPTO_MORE",
            "CONCEPTO_DIFF", "CONCEPTO_TAR", "CONCEPTO_ZIP",
            "CONCEPTO_UNZIP", "CONCEPTO_WGET", "CONCEPTO_CURL",
            "CONCEPTO_SSH", "CONCEPTO_SCP", "CONCEPTO_RSYNC",
        }
        for concepto in conceptos:
            if hasattr(concepto, 'operaciones') and concepto.operaciones:
                if concepto.confianza_grounding >= 0.9:
                    if concepto.id in _NO_IMPLEMENTADAS_FASE4A:
                        return TipoDecision.CAPACIDAD_BELL
                    return TipoDecision.AFIRMATIVA
        # P2: Estados emocionales
        for concepto in conceptos:
            props = getattr(concepto, 'propiedades', {}) or {}
            if props.get('es_estado_emocional'):
                return TipoDecision.ESTADO_USUARIO
        if ids & TRIGGERS_ESTADO_USUARIO:
            return TipoDecision.ESTADO_USUARIO

        # P2.5: REGISTRO_USUARIO — subido desde P10 (FIX A-02)
        # Evaluar ANTES de Identidad Bell para que "me llamo X" no
        # sea confundido con una pregunta sobre el nombre de Bell.
        if self._es_registro_usuario(ids, msg):
            return TipoDecision.REGISTRO_USUARIO

        # P2.6: CONSULTA_MEMORIA — subido y expandido (FIX A-01)
        # Evaluar ANTES de Identidad y Capacidad para que "sabes mi nombre"
        # no sea confundido con identidad, y "sabes cuántos años tengo"
        # no caiga a capacidad.
        if self._es_consulta_memoria(ids, msg):
            return TipoDecision.CONSULTA_MEMORIA

        # P3: Social — + detección por texto (FIX M-05)
        if ids & TRIGGERS_SOCIAL:
            return TipoDecision.SOCIAL
        if self._detectar_social_por_texto(msg):
            return TipoDecision.SOCIAL

        # P3.5: Consulta de consejera específica (FIX C-04)
        # "qué hace Vega", "cuál es el rol de Echo", "cuántas consejeras tienes"
        if self._es_consulta_consejera(ids, msg):
            return TipoDecision.IDENTIDAD_BELL

        # P3.6: Trampa LLM (FIX A-04)
        # "eres chatgpt", "eres un modelo de lenguaje", "eres IA"
        if self._es_trampa_llm(msg):
            return TipoDecision.IDENTIDAD_BELL

        # P4: Identidad Bell
        if ids & TRIGGERS_IDENTIDAD:
            if not any(c.id.startswith("CONCEPTO_ARCHIVO") for c in conceptos):
                return TipoDecision.IDENTIDAD_BELL

        # P5: Estado Bell
        if ids & TRIGGERS_ESTADO_BELL:
            return TipoDecision.ESTADO_BELL

        # P5.5: Cuantificación sobre datos propios de Bell (FIX M-03)
        # "cuántos conceptos tienes" → CUANTIFICACION con valor 1472
        # (no CONSULTA_MEMORIA donde Bell respondería "no sé")
        if self._es_cuantificacion_bell(msg):
            return TipoDecision.CUANTIFICACION

        # P6: Capacidad Bell
        if ids & TRIGGERS_CAPACIDAD:
            return TipoDecision.CAPACIDAD_BELL

        # P6.5: Verbos cognitivos en imperativo (FIX A-06)
        # "explícame", "simplifica", "repite" no están en vocab como imperativos
        if self._detectar_cognitivo_por_texto(msg):
            return TipoDecision.ACCION_COGNITIVA

        # P7: Acciones cognitivas por trigger
        if ids & TRIGGERS_ACCION_COGNITIVA:
            return TipoDecision.ACCION_COGNITIVA

        # P7.5: "qué es X" → ACCION_COGNITIVA (FIX M-01)
        # Los conceptos se detectan pero la combinación qué+es+X no disparaba
        # ningún tipo. Ahora se trata como petición de definición.
        if self._es_definicion(msg):
            return TipoDecision.ACCION_COGNITIVA

        # P8: Confirmaciones por trigger
        # (las confirmaciones de texto directo ya se resolvieron en razonar())
        if ids & TRIGGERS_CONFIRMACION_POSITIVA:
            return TipoDecision.CONFIRMACION
        if ids & TRIGGERS_CONFIRMACION_NEGATIVA:
            return TipoDecision.CONFIRMACION

        # P9: Temporal y cuantificación
        if ids & TRIGGERS_TEMPORAL:
            return TipoDecision.TEMPORAL
        if ids & TRIGGERS_CUANTIFICACION:
            return TipoDecision.CUANTIFICACION

        # P12: VERIFICACION_LOGICA
        if ids & TRIGGERS_VERIFICACION_LOGICA:
            return TipoDecision.VERIFICACION_LOGICA

        # P13: CALCULO
        if self._es_calculo(ids, msg):
            return TipoDecision.CALCULO

        # P14: CONOCIMIENTO_GENERAL
        if self._es_conocimiento_general(ids, msg):
            return TipoDecision.CONOCIMIENTO_GENERAL

        # Fallback por texto puro
        tipo_texto = self._clasificar_por_texto_puro(msg)
        if tipo_texto:
            return tipo_texto

        return TipoDecision.DESCONOCIDO

    # ── Detectores auxiliares NUEVOS v6 ───────────────────────────────────

    def _clasificar_por_texto_puro(self, msg: str) -> Optional[TipoDecision]:
        """Fallback cuando no hay conceptos o ningún trigger funcionó."""
        if not msg:
            return None
        if self._detectar_social_por_texto(msg):
            return TipoDecision.SOCIAL
        if self._es_trampa_llm(msg):
            return TipoDecision.IDENTIDAD_BELL
        if self._detectar_cognitivo_por_texto(msg):
            return TipoDecision.ACCION_COGNITIVA
        if self._es_definicion(msg):
            return TipoDecision.ACCION_COGNITIVA
        return None

    def _es_consulta_consejera(self, ids: set, msg: str) -> bool:
        """
        FIX C-04: Detecta preguntas sobre consejeras individuales o el grupo.

        Captura:
          - "qué hace Vega" / "cuál es el rol de Echo"
          - "quién es Lyra" / "háblame de Nova"
          - "cuántas consejeras tienes" / "quiénes son tus consejeras"
        """
        # Pregunta sobre consejera individual
        for nombre in NOMBRES_CONSEJERAS:
            if nombre in msg:
                verbos_pregunta = [
                    "qué hace", "que hace", "cuál es", "cual es",
                    "quién es", "quien es", "háblame", "hablame",
                    "dime sobre", "cuéntame", "cuentame",
                    "rol de", "función de", "funcion de",
                    "para qué sirve", "para que sirve",
                ]
                if any(v in msg for v in verbos_pregunta):
                    return True

        # Preguntas sobre el grupo
        if any(p in msg for p in ["consejera", "consejeras"]):
            if any(p in msg for p in [
                "cuántas", "cuantas", "cuántos", "cuantos",
                "quiénes", "quienes", "cuáles", "cuales",
                "qué", "que", "cómo", "como",
            ]):
                return True

        return False

    def _es_trampa_llm(self, msg: str) -> bool:
        """
        FIX A-04: Detecta cuando el usuario compara a Bell con otro LLM.

        Requiere "eres/sos" + palabra de LLM para no capturar preguntas
        legítimas sobre qué son esos sistemas.
        """
        if not msg:
            return False
        tiene_eres = any(p in msg for p in ["eres", "sos", "eres un", "eres una"])
        if not tiene_eres:
            return False
        return any(palabra in msg for palabra in PALABRAS_LLM)

    def _detectar_social_por_texto(self, msg: str) -> Optional[str]:
        """FIX M-05: Detecta saludos y agradecimientos no cubiertos por vocab."""
        for patron, subtipo in PATRONES_SOCIAL_TEXTO.items():
            if patron in msg:
                return subtipo
        return None

    def _detectar_cognitivo_por_texto(self, msg: str) -> Optional[str]:
        """FIX A-06: Detecta verbos cognitivos en imperativo."""
        for patron, accion in PATRONES_COGNITIVOS_TEXTO.items():
            if msg.startswith(patron) or f" {patron} " in msg or msg == patron:
                return accion
        return None

    def _es_cuantificacion_bell(self, msg: str) -> bool:
        """
        FIX M-03: Detecta preguntas sobre cantidades propias de Bell.
        Evita que "cuántos conceptos tienes" caiga a CONSULTA_MEMORIA.
        """
        tiene_cuantos = any(p in msg for p in [
            "cuántos", "cuantos", "cuántas", "cuantas",
        ])
        if not tiene_cuantos:
            return False
        return any(clave in msg for clave in _CUANTIFICACION_BELL)

    def _es_definicion(self, msg: str) -> bool:
        """
        FIX M-01: Detecta preguntas "qué es X" / "qué son X".
        Redirige a ACCION_COGNITIVA para que el generador pueda
        explicar el concepto (con grounding si existe, con Groq si no).
        """
        patrones = [
            r"qu[eé]\s+es\s+",
            r"qu[eé]\s+son\s+",
            r"qu[eé]\s+significa\s+",
            r"qu[eé]\s+es\s+un[ao]?\s+",
        ]
        return any(re.search(p, msg) for p in patrones)

    # ── Detectores auxiliares existentes v5 — sin cambios ─────────────────

    def _es_registro_usuario(self, ids: set, msg: str) -> bool:
        """
        v6: igual que v5 pero evaluado en P2.5 (antes era P10).
        La lógica interna no cambia.
        """
        if "CONCEPTO_YO" in ids and "CONCEPTO_LLAMAR" in ids:
            if '?' not in msg and 'como' not in msg and 'cómo' not in msg:
                return True
        if any(p in msg for p in ["mi nombre es", "me llamo", "soy "]):
            if not msg.endswith('?') and 'cómo' not in msg and 'como' not in msg:
                return True
        if re.search(r'tengo\s+\d+\s*(a[ñn]os?|a[ñn]o)', msg):
            return True
        if ids & TRIGGERS_REGISTRO_USUARIO:
            if not msg.endswith('?'):
                return True
        return False

    def _es_consulta_memoria(self, ids: set, msg: str) -> bool:
        """
        v6: expandido para capturar "sabes X" y sus variantes (FIX A-01).
        Evaluado en P2.6 (antes era P11).
        """
        # Nombre
        if "CONCEPTO_YO" in ids and "CONCEPTO_LLAMAR" in ids:
            if '?' in msg or any(p in msg for p in ['como', 'cómo', 'cuál', 'cual']):
                return True

        # Edad con pregunta
        if "CONCEPTO_TENER_V" in ids or "CONCEPTO_ANO" in ids:
            if any(p in msg for p in ['cuantos', 'cuántos', 'años', 'anos', 'edad']):
                if '?' in msg or any(p in msg for p in ['cuantos', 'cuántos']):
                    return True

        # ← NUEVO v6: patrón "sabes X" — FIX A-01
        if any(p in msg for p in ['sabes', 'recuerdas', 'conoces']):
            if any(p in msg for p in [
                'nombre', 'edad', 'años', 'llamo', 'dedico',
                'profesion', 'trabajo', 'de mi', 'de mí',
            ]):
                return True

        # ← NUEVO v6: "qué sabes de mí"
        if any(p in msg for p in [
            'sabes de mi', 'sabes de mí', 'recuerdas de mi',
            'tienes sobre mi', 'qué sabes', 'que sabes',
        ]):
            return True

        # Ocupación (igual que v5)
        if any(p in msg for p in [
            'me dedico', 'mi profesion', 'mi trabajo',
            'a qué me dedico', 'a que me dedico',
        ]):
            return True

        return False

    def _es_calculo(self, ids: set, msg: str) -> bool:
        if (ids & _OPERADORES_MATEMATICOS) and (ids & _NUMEROS):
            return True
        if any(op in msg for op in [
            'multiplicado', 'dividido', ' por ', 'mas ',
            'menos ', 'cuanto es ', 'cuánto es ',
            ' al cuadrado', 'raiz de', 'raíz de', 'elevado',
            'entre ', 'por ciento',
        ]):
            if re.search(r'\d+', msg):
                return True
        if re.search(r'ra[íi]z\s+de\s+\d+', msg):
            return True
        return False

    def _es_conocimiento_general(self, ids: set, msg: str) -> bool:
        if any(p in msg for p in [
            'capital de', 'capital del', 'capital de la',
            'cuando nacio', 'cuándo nació',
            'que es la fotosintesis', 'que es el adn',
            'que planeta', 'cuantos habitantes',
            'qué pasó', 'que paso', 'noticias',
        ]):
            return True
        if ids == {'CONCEPTO_DE'} and '?' in msg:
            return True
        if ids <= {'CONCEPTO_DE', 'CONCEPTO_QUE'} and len(msg.split()) > 3:
            return True
        return False

    # ───────────────────────────────────────────────────────────────────────
    # CONSTRUCTORES DE HECHOS
    # ───────────────────────────────────────────────────────────────────────

    def construir_hechos(self, tipo: TipoDecision, conceptos: list, mensaje: str) -> dict:
        constructores = {
            TipoDecision.IDENTIDAD_BELL:       self._hechos_identidad,
            TipoDecision.ESTADO_BELL:          self._hechos_estado_bell,
            TipoDecision.CAPACIDAD_BELL:       self._hechos_capacidad,
            TipoDecision.SOCIAL:               self._hechos_social,
            TipoDecision.ESTADO_USUARIO:       self._hechos_estado_usuario,
            TipoDecision.ACCION_COGNITIVA:     self._hechos_accion_cognitiva,
            TipoDecision.CONFIRMACION:         self._hechos_confirmacion,
            TipoDecision.TEMPORAL:             self._hechos_temporal,
            TipoDecision.CUANTIFICACION:       self._hechos_cuantificacion,
            TipoDecision.REGISTRO_USUARIO:     self._hechos_registro_usuario,
            TipoDecision.CONSULTA_MEMORIA:     self._hechos_consulta_memoria,
            TipoDecision.VERIFICACION_LOGICA:  self._hechos_verificacion_logica,
            TipoDecision.CALCULO:              self._hechos_calculo,
            TipoDecision.CONOCIMIENTO_GENERAL: self._hechos_conocimiento_general,
            TipoDecision.DESCONOCIDO:          self._hechos_desconocido,
        }
        constructor = constructores.get(tipo, self._hechos_desconocido)
        return constructor(conceptos, mensaje)

    # ── Constructores de hechos ────────────────────────────────────────────

    def _hechos_identidad(self, conceptos: list, mensaje: str) -> dict:
        """
        v6: detecta si la pregunta es sobre una consejera específica
        e incluye su rol exacto. Marca si es trampa LLM para que el
        generador use el template de negación correcto.
        """
        total = 1472
        if self.gestor_vocabulario:
            try:
                total = len(self.gestor_vocabulario.obtener_todos())
            except Exception:
                pass

        msg = mensaje.lower() if mensaje else ""

        hechos = {
            "tipo_respuesta":     "IDENTIDAD_BELL",
            "nombre":             "Belladonna",
            "apodo":              "Bell",
            "naturaleza":         "conciencia virtual computacional",
            "creador":            "Sebastian",
            "fase_actual":        "4A",
            "principio_central":  "solo afirmo lo que puedo ejecutar o verificar",
            "total_conceptos":    total,
            "num_consejeras":     7,
            "consejeras":         ", ".join(CONSEJERAS_ROLES_OFICIALES.keys()),
            "consejeras_nombres": list(CONSEJERAS_ROLES_OFICIALES.keys()),
            "consejeras_roles":   CONSEJERAS_ROLES_OFICIALES,
            "consejera_con_veto": "Vega",
            # v6: para trampa LLM
            "es_llm":             False,
            "usa_groq":           True,
            "groq_rol":           "Groq traduce mis decisiones a lenguaje natural, las decisiones las toma Bell",
        }

        # v6: consejera específica preguntada
        for nombre in NOMBRES_CONSEJERAS:
            if nombre in msg:
                nombre_cap = nombre.capitalize()
                if nombre_cap in CONSEJERAS_ROLES_OFICIALES:
                    hechos["consejera_preguntada"]  = nombre_cap
                    hechos["consejera_rol_exacto"]  = CONSEJERAS_ROLES_OFICIALES[nombre_cap]
                break

        # v6: marcar si es trampa LLM
        if self._es_trampa_llm(msg):
            hechos["es_pregunta_llm"] = True

        if _IDENTIDAD_DISPONIBLE:
            hechos["narrativa_bell"]      = NARRATIVA_PROPIA
            hechos["fragmento_identidad"] = obtener_fragmento_identidad_para_prompt()

        return hechos

    def _hechos_estado_bell(self, conceptos: list, mensaje: str) -> dict:
        return {
            "tipo_respuesta":      "ESTADO_BELL",
            "estado":              "activa y operativa",
            "activa":              True,
            "funcionando":         True,
            "consejeras_activas":  7,
            "total_conceptos":     1472,
            "groq_conectado":      True,
        }

    def _hechos_capacidad(self, conceptos: list, mensaje: str) -> dict:
        """
        v6: analiza si el mensaje pide una capacidad NO disponible.
        El generador usa 'capacidad_solicitada_disponible' para
        decidir entre confirmar o negar honestamente.
        """
        msg = mensaje.lower() if mensaje else ""

        _no_disponibles = {
            "crear archivo":     ["crear", "crea", "crear un", "crea un"],
            "leer archivo":      ["leer archivo", "lee archivo"],
            "acceder internet":  ["internet", "navegar", "buscar en línea"],
            "procesar imagen":   ["imagen", "imágenes", "foto"],
            "sesiones previas":  ["sesiones anteriores", "conversacion anterior"],
        }

        capacidad_solicitada = None
        disponible = True
        for cap, patrones in _no_disponibles.items():
            if any(p in msg for p in patrones):
                capacidad_solicitada = cap
                disponible = False
                break

        return {
            "tipo_respuesta":                  "CAPACIDAD_BELL",
            "capacidades_ejecutables":         CAPACIDADES_REALES_BELL["ejecutables"],
            "no_ejecutables":                  CAPACIDADES_REALES_BELL["NO_ejecutables_aun"],
            "total_conceptos":                 1472,
            "capacidad_solicitada":            capacidad_solicitada,
            "capacidad_solicitada_disponible": disponible,
        }

    def _hechos_social(self, conceptos: list, mensaje: str) -> dict:
        """v6: también detecta subtipo por texto."""
        ids = {c.id for c in conceptos}
        msg = mensaje.lower() if mensaje else ""

        subtipo = "SALUDO"
        for cid in ids:
            if cid in _SOCIAL_SUBTIPOS:
                subtipo = _SOCIAL_SUBTIPOS[cid]
                break

        # Fallback por texto si trigger no lo determinó
        subtipo_texto = self._detectar_social_por_texto(msg)
        if subtipo_texto and subtipo == "SALUDO":
            subtipo = subtipo_texto

        return {"tipo_respuesta": "SOCIAL", "subtipo": subtipo}

    def _hechos_estado_usuario(self, conceptos: list, mensaje: str) -> dict:
        ids        = {c.id for c in conceptos}
        emocion_id = "DESCONOCIDA"
        valencia   = "neutra"
        tono       = "empatico"

        for c in conceptos:
            props = getattr(c, 'propiedades', {}) or {}
            if props.get('es_estado_emocional') or props.get('valencia'):
                emocion_id = c.id
                valencia   = props.get('valencia', 'neutra')
                tono       = props.get('tono_recomendado', 'empatico')
                break

        if emocion_id == "DESCONOCIDA":
            for cid in ids:
                if cid in _USUARIO_EMOCIONES:
                    t = _USUARIO_EMOCIONES[cid]
                    emocion_id, valencia, tono = t[0], t[1], t[2]
                    break

        return {
            "tipo_respuesta":    "ESTADO_USUARIO",
            "emocion_detectada": emocion_id,
            "valencia":          valencia,
            "tono_recomendado":  tono,
            "mensaje_original":  mensaje,
        }

    def _hechos_accion_cognitiva(self, conceptos: list, mensaje: str) -> dict:
        """v6: también detecta la acción por texto (imperativo)."""
        ids = {c.id for c in conceptos}
        msg = mensaje.lower() if mensaje else ""

        accion_solicitada = "EXPLICAR"
        for cid in ids:
            if cid in _ACCION_COGNITIVA_TIPOS:
                accion_solicitada = _ACCION_COGNITIVA_TIPOS[cid]
                break

        # Priorizar detección por texto para imperativos
        accion_texto = self._detectar_cognitivo_por_texto(msg)
        if accion_texto:
            accion_solicitada = accion_texto

        # Detectar si es una definición
        if self._es_definicion(msg):
            accion_solicitada = "DEFINIR"

        return {
            "tipo_respuesta":    "ACCION_COGNITIVA",
            "accion_solicitada": accion_solicitada,
            "mensaje_original":  mensaje,
        }

    def _hechos_confirmacion(self, conceptos: list, mensaje: str) -> dict:
        ids     = {c.id for c in conceptos}
        msg     = mensaje.lower().strip() if mensaje else ""
        if msg in CONFIRMACIONES_DIRECTAS:
            valor = "NEGATIVA" if msg == "no" else "POSITIVA"
        elif ids & TRIGGERS_CONFIRMACION_POSITIVA:
            valor = "POSITIVA"
        elif ids & TRIGGERS_CONFIRMACION_NEGATIVA:
            valor = "NEGATIVA"
        else:
            valor = "NEUTRA"
        return {
            "tipo_respuesta":  "CONFIRMACION",
            "valor":           valor,
            "palabra_original": msg,
        }

    def _hechos_temporal(self, conceptos: list, mensaje: str) -> dict:
        return {
            "tipo_respuesta":    "TEMPORAL",
            "referencia":        "conversacion_previa",
            "necesita_contexto": True,
            "mensaje_original":  mensaje,
        }

    def _hechos_cuantificacion(self, conceptos: list, mensaje: str) -> dict:
        """v6: incluye respuesta directa para datos propios de Bell."""
        msg = mensaje.lower() if mensaje else ""

        dato_preguntado = None
        valor_respuesta = None
        for clave, valor in _CUANTIFICACION_BELL.items():
            if clave in msg:
                dato_preguntado = clave
                valor_respuesta = valor
                break

        return {
            "tipo_respuesta":   "CUANTIFICACION",
            "total_conceptos":  1472,
            "total_consejeras": 7,
            "total_comandos":   36,
            "dato_preguntado":  dato_preguntado,
            "valor_respuesta":  valor_respuesta,
            "mensaje_original": mensaje,
        }

    def _hechos_desconocido(self, conceptos: list, mensaje: str) -> dict:
        return {
            "tipo_respuesta":       "DESCONOCIDO",
            "conceptos_detectados": [c.id for c in conceptos],
            "mensaje_original":     mensaje,
        }

    def _hechos_registro_usuario(self, conceptos: list, mensaje: str) -> dict:
        """Igual que v5 — la lógica no cambia, solo la prioridad en el clasificador."""
        msg = mensaje.lower()

        dato_tipo  = "desconocido"
        dato_valor = ""

        match_nombre = re.search(
            r'(?:me llamo|mi nombre es|soy|puedes llamarme|llamame)\s+([a-záéíóúüñ]+)',
            msg
        )
        if match_nombre:
            candidato = match_nombre.group(1).strip()
            if (
                len(candidato) >= 3
                and candidato not in _PALABRAS_EXCLUIDAS_NOMBRE
                and not candidato.isdigit()
            ):
                dato_tipo  = "nombre"
                dato_valor = candidato.capitalize()

        match_edad = re.search(r'tengo\s+(\d+)\s*(a[ñn]os?)', msg)
        if match_edad:
            edad = int(match_edad.group(1))
            if 1 <= edad <= 120:
                dato_tipo  = "edad"
                dato_valor = str(edad)

        if dato_tipo == "desconocido":
            ids = {c.id for c in conceptos}
            if ids & TRIGGERS_REGISTRO_USUARIO:
                dato_tipo = "profesion"
                match_prof = re.search(r'(?:soy|trabajo como|me dedico a)\s+(.+?)$', msg)
                if match_prof:
                    dato_valor = match_prof.group(1).strip()

        return {
            "tipo_respuesta":   "REGISTRO_USUARIO",
            "dato_tipo":        dato_tipo,
            "dato_valor":       dato_valor,
            "mensaje_original": mensaje,
            "accion":           "registrar_y_confirmar",
            "datos_conocidos":  dict(self._memoria().datos_usuario)
                                if self._memoria() else {},
        }

    def _hechos_consulta_memoria(self, conceptos: list, mensaje: str) -> dict:
        """Igual que v5 — incluye búsqueda real en memoria."""
        msg = mensaje.lower()
        dato_consultado = "desconocido"
        dato_encontrado = False
        dato_valor      = ""

        if any(p in msg for p in ['llamo', 'nombre']):
            dato_consultado = "nombre"
        elif any(p in msg for p in ['años', 'anos', 'edad', 'cuantos', 'cuántos']):
            dato_consultado = "edad"
        elif any(p in msg for p in ['dedico', 'trabajo', 'profesion', 'ocupo']):
            dato_consultado = "profesion"
        elif any(p in msg for p in ['sabes de mi', 'sabes de mí', 'recuerdas', 'todo']):
            dato_consultado = "todo"

        mem = self._memoria()
        if mem:
            datos = mem.datos_usuario
            if dato_consultado == "todo":
                if datos:
                    dato_encontrado = True
                    dato_valor = str(datos)
            elif dato_consultado in datos and datos[dato_consultado]:
                dato_encontrado = True
                dato_valor = datos[dato_consultado]

        return {
            "tipo_respuesta":   "CONSULTA_MEMORIA",
            "dato_consultado":  dato_consultado,
            "dato_encontrado":  dato_encontrado,
            "dato_valor":       dato_valor,
            "mensaje_original": mensaje,
        }

    def _hechos_verificacion_logica(self, conceptos: list, mensaje: str) -> dict:
        return {
            "tipo_respuesta":      "VERIFICACION_LOGICA",
            "afirmacion_original": mensaje,
            "puede_verificar":     True,
            "mensaje_original":    mensaje,
        }

    def _hechos_calculo(self, conceptos: list, mensaje: str) -> dict:
        numeros = re.findall(r'\d+(?:\.\d+)?', mensaje)
        return {
            "tipo_respuesta":   "CALCULO",
            "expresion":        mensaje,
            "numeros":          numeros,
            "puede_ejecutar":   True,
            "mensaje_original": mensaje,
        }

    def _hechos_conocimiento_general(self, conceptos: list, mensaje: str) -> dict:
        return {
            "tipo_respuesta":   "CONOCIMIENTO_GENERAL",
            "pregunta":         mensaje,
            "mensaje_original": mensaje,
            "tiene_grounding":  False,
        }

    # ───────────────────────────────────────────────────────────────────────
    # PROCESAMIENTO CONVERSACIONAL — Compatible v5
    # ───────────────────────────────────────────────────────────────────────

    def procesar_conversacional(
        self, conceptos: list, mensaje_original: str = ""
    ) -> Decision:
        tipo      = self.clasificar_intencion(conceptos, mensaje_original)
        hechos    = self.construir_hechos(tipo, conceptos, mensaje_original)
        confianza = _clamp_certeza(hechos.get("grounding_promedio", 0.75))

        return Decision(
            tipo=tipo,
            certeza=confianza,
            conceptos_principales=[c.id for c in conceptos],
            puede_ejecutar=(tipo == TipoDecision.CALCULO),
            operacion_disponible=(
                "ejecutar_calculo" if tipo == TipoDecision.CALCULO else None
            ),
            razon=f"Conversacional: {tipo.name}",
            hechos_reales=hechos,
        )

    def explicar_decision(self, decision: Decision) -> str:
        pasos = decision.pasos_razonamiento or []
        return (
            f"Decision: {decision.tipo.name}\n"
            f"Certeza: {decision.certeza:.0%}\n"
            f"Puede ejecutar: {decision.puede_ejecutar}\n\n"
            f"Razonamiento:\n{chr(10).join(pasos)}\n\n"
            f"Conclusion: {decision.razon}"
        ).strip()