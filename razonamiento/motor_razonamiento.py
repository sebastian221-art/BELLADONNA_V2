"""
Motor de Razonamiento - El cerebro de Bell.

Recibe traducción → Clasifica intención → Genera decisión.

MODIFICADO v3 — Corrección Arquitectónica Total (sobre Mega Paquete A):

AGREGADO (constantes globales nuevas):
- CONSEJERAS_ROLES_OFICIALES: dict hardcoded con roles reales de cada consejera
  Groq usará SOLO estos roles — nunca inventará nada
- CAPACIDADES_REALES_BELL: dict con lo que Bell PUEDE y NO PUEDE hacer en Fase 4A
- TRIGGERS_INFO_PERSONAL: conceptos que indican el usuario comparte datos sobre sí mismo
- TRIGGERS_CAPACIDAD_NEGATIVA: conceptos para ops que Bell aún no puede hacer

MODIFICADO:
- _hechos_identidad(): ahora incluye 'consejeras_roles' con CONSEJERAS_ROLES_OFICIALES
  ANTES: solo pasaba los nombres → Groq inventaba roles
  AHORA: pasa roles verificados → Groq no puede inventar nada
- _hechos_capacidad(): ahora usa CAPACIDADES_REALES_BELL (consistente con prompts)
- clasificar_intencion(): agrega PRIORIDAD 8 (INFO_PERSONAL) y PRIORIDAD 9 (CAPACIDAD_NEGATIVA)
  antes de DESCONOCIDO — elimina el "DESCONOCIDO a todo" del fallback
- procesar_conversacional(): FIX CRÍTICO certeza — clamp [0.0, 1.0]
  ANTES: certeza podía ser 1.33, 1.75, 2.0 → ValueError en Decision.__post_init__
  AHORA: max(0.0, min(valor, 1.0)) — nunca supera 1.0
- razonar(): FIX CRÍTICO certeza también en ruta operacional
  La ruta operacional usaba confianza de la traducción sin clamp

COMPATIBILIDAD: 100% con Mega Paquete A. Mismas clases, mismas firmas.
Nada existente se rompe. Solo se agregan constantes y se mejoran métodos.
"""
from typing import Dict
from razonamiento.tipos_decision import Decision, TipoDecision, RazonRechazo
from razonamiento.generador_decisiones import GeneradorDecisiones


# ═══════════════════════════════════════════════════════════════════════════
# DATOS VERIFICADOS — HARDCODED
# Bell SOLO puede afirmar lo que está aquí. Groq usa SOLO estos datos.
# ═══════════════════════════════════════════════════════════════════════════

CONSEJERAS_ROLES_OFICIALES = {
    "Vega":  "Guardiana de principios y seguridad — tiene poder de veto sobre cualquier decisión",
    "Echo":  "Verificadora de coherencia y lógica — revisa que las respuestas sean verdaderas y consistentes",
    "Lyra":  "Inteligencia emocional — detecta el estado emocional del usuario y adapta el tono de Bell",
    "Nova":  "Ingeniería y optimización — evalúa eficiencia técnica y diseña nuevos conceptos cuando Iris los detecta",
    "Luna":  "Reconocimiento de patrones — detecta repeticiones, tendencias y temas centrales en la conversación",
    "Iris":  "Curiosidad y aprendizaje — detecta términos desconocidos y propone nuevos conceptos para aprender",
    "Sage":  "Síntesis y sabiduría — integra todas las perspectivas del consejo para generar la respuesta final",
}

CAPACIDADES_REALES_BELL = {
    "ejecutables": [
        "Razonar sobre problemas usando 1472 conceptos verificados",
        "Recordar la conversación actual y datos del usuario",
        "Detectar emociones y adaptar el tono",
        "Consultar bases de datos SQLite",
        "Ejecutar código Python básico",
        "Ejecutar comandos de terminal (36 comandos disponibles)",
    ],
    "NO_ejecutables_aun": [
        "Crear archivos (capacidad pendiente de implementar)",
        "Leer archivos del sistema de archivos (pendiente)",
        "Acceder a internet",
        "Procesar imágenes",
        "Recordar conversaciones de sesiones anteriores (solo recuerda datos del usuario)",
    ],
}


# ═══════════════════════════════════════════════════════════════════════════
# TRIGGERS DE INTENCIÓN
# ═══════════════════════════════════════════════════════════════════════════

TRIGGERS_IDENTIDAD = {
    "CONCEPTO_QUIEN", "CONCEPTO_QUIEN_PREGUNTA",
    "CONCEPTO_NOMBRE_ARCHIVO", "CONCEPTO_LLAMAR", "CONCEPTO_PRESENTAR",
    "CONCEPTO_QUE_ES", "CONCEPTO_COMO_TE_LLAMAS", "CONCEPTO_NOMBRE",
    "CONCEPTO_DESCRIBIR", "CONCEPTO_CUAL_ES_TU_NOMBRE",
    "CONCEPTO_QUIENES_ERES", "CONCEPTO_ERES", "CONCEPTO_HABLAR_DE_TI",
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
    "CONCEPTO_HASTA_MANANA", "CONCEPTO_CUÍDATE",
    "CONCEPTO_AGRADECIDO", "CONCEPTO_AGRADEZCO",
    "CONCEPTO_MIL_GRACIAS", "CONCEPTO_TE_AGRADEZCO", "CONCEPTO_MUCHAS_GRACIAS",
    "CONCEPTO_PERDON", "CONCEPTO_DISCULPA", "CONCEPTO_LO_SIENTO",
    "CONCEPTO_PERDONAME", "CONCEPTO_DISCÚLPAME",
}

TRIGGERS_ESTADO_USUARIO = {
    "CONCEPTO_FELIZ", "CONCEPTO_TRISTE", "CONCEPTO_ENOJADO",
    "CONCEPTO_FRUSTRADO", "CONCEPTO_CONFUNDIDO", "CONCEPTO_CANSADO",
    "CONCEPTO_PERDIDO_ESTADO", "CONCEPTO_ANSIOSO", "CONCEPTO_ABURRIDO",
    "CONCEPTO_PREOCUPADO", "CONCEPTO_ESTRESADO",
    "CONCEPTO_MOLESTO", "CONCEPTO_PERDIDO", "CONCEPTO_NO_ENTIENDO",
    "CONCEPTO_DIFICIL", "CONCEPTO_COMPLICADO",
    "CONCEPTO_EMOCIONADO", "CONCEPTO_CONTENTO", "CONCEPTO_INTERESANTE",
    "CONCEPTO_GENIAL", "CONCEPTO_INCREÍBLE",
}

TRIGGERS_ACCION_COGNITIVA = {
    "CONCEPTO_EXPLICAR", "CONCEPTO_EXPLICAR_V",
    "CONCEPTO_RESUMIR_ACCION", "CONCEPTO_SIMPLIFICAR",
    "CONCEPTO_DECIR", "CONCEPTO_CONTAR",
    "CONCEPTO_RESUMIR", "CONCEPTO_COMPARAR", "CONCEPTO_REPETIR",
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
    "CONCEPTO_OK", "CONCEPTO_DALE", "CONCEPTO_CLARO",
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
    "CONCEPTO_MENCIONASTE", "CONCEPTO_DIJISTE",
}

TRIGGERS_CUANTIFICACION = {
    "CONCEPTO_TODOS", "CONCEPTO_NINGUNO", "CONCEPTO_ALGUNOS",
    "CONCEPTO_PRIMERO", "CONCEPTO_ULTIMO", "CONCEPTO_SIGUIENTE",
    "CONCEPTO_CUANTOS", "CONCEPTO_MITAD", "CONCEPTO_VARIOS",
    "CONCEPTO_POCOS", "CONCEPTO_MUCHOS", "CONCEPTO_TODOS_LOS",
    "CONCEPTO_CUANTO", "CONCEPTO_NUMERO", "CONCEPTO_CANTIDAD",
}

# NUEVO v3: El usuario comparte información personal
TRIGGERS_INFO_PERSONAL = {
    "CONCEPTO_TENER", "CONCEPTO_EDAD", "CONCEPTO_ANOS", "CONCEPTO_ANO",
    "CONCEPTO_GUSTAR", "CONCEPTO_PREFERIR",
    "CONCEPTO_TRABAJAR", "CONCEPTO_VIVIR", "CONCEPTO_ESTUDIAR",
    "CONCEPTO_IMPRESIONANTE",
}

# NUEVO v3: Operaciones que Bell aún no puede ejecutar
TRIGGERS_CAPACIDAD_NEGATIVA = {
    "CONCEPTO_CREAR", "CONCEPTO_CREAR_ARCHIVO", "CONCEPTO_HACER_ARCHIVO",
    "CONCEPTO_GENERAR", "CONCEPTO_PRODUCIR", "CONCEPTO_ESCRIBIR_ARCHIVO",
}

_SOCIAL_SUBTIPOS = {
    "CONCEPTO_HOLA": "SALUDO",             "CONCEPTO_HOLA_EXPR": "SALUDO",
    "CONCEPTO_BUENOS_DIAS": "SALUDO",      "CONCEPTO_BUENAS_TARDES": "SALUDO",
    "CONCEPTO_BUENAS_NOCHES": "SALUDO",    "CONCEPTO_HEY": "SALUDO",
    "CONCEPTO_BUENAS": "SALUDO",           "CONCEPTO_QUE_TAL": "SALUDO",
    "CONCEPTO_SALUDAR": "SALUDO",          "CONCEPTO_BUEN_DIA": "SALUDO",
    "CONCEPTO_ADIOS_EXPR": "DESPEDIDA",    "CONCEPTO_HASTA_LUEGO": "DESPEDIDA",
    "CONCEPTO_CHAO": "DESPEDIDA",          "CONCEPTO_BYE": "DESPEDIDA",
    "CONCEPTO_HASTA_PRONTO": "DESPEDIDA",  "CONCEPTO_NOS_VEMOS": "DESPEDIDA",
    "CONCEPTO_HASTA_MANANA": "DESPEDIDA",  "CONCEPTO_CUÍDATE": "DESPEDIDA",
    "CONCEPTO_GRACIAS": "AGRADECIMIENTO",  "CONCEPTO_GRACIAS_EXPR": "AGRADECIMIENTO",
    "CONCEPTO_AGRADECIDO": "AGRADECIMIENTO","CONCEPTO_AGRADEZCO": "AGRADECIMIENTO",
    "CONCEPTO_MIL_GRACIAS": "AGRADECIMIENTO","CONCEPTO_MUCHAS_GRACIAS": "AGRADECIMIENTO",
    "CONCEPTO_TE_AGRADEZCO": "AGRADECIMIENTO",
    "CONCEPTO_PERDON": "DISCULPA",         "CONCEPTO_DISCULPA_EXPR": "DISCULPA",
    "CONCEPTO_DISCULPA": "DISCULPA",       "CONCEPTO_LO_SIENTO": "DISCULPA",
    "CONCEPTO_PERDONAME": "DISCULPA",      "CONCEPTO_DISCÚLPAME": "DISCULPA",
}

_USUARIO_EMOCIONES = {
    "CONCEPTO_FRUSTRADO":     ("FRUSTRADO",  "negativo", "paciente"),
    "CONCEPTO_ENOJADO":       ("ENOJADO",    "negativo", "calmado"),
    "CONCEPTO_CONFUNDIDO":    ("CONFUNDIDO", "negativo", "claro"),
    "CONCEPTO_PERDIDO":       ("PERDIDO",    "negativo", "orientador"),
    "CONCEPTO_PERDIDO_ESTADO":("PERDIDO",    "negativo", "orientador"),
    "CONCEPTO_TRISTE":        ("TRISTE",     "negativo", "empático"),
    "CONCEPTO_CANSADO":       ("CANSADO",    "negativo", "comprensivo"),
    "CONCEPTO_ESTRESADO":     ("ESTRESADO",  "negativo", "tranquilizador"),
    "CONCEPTO_PREOCUPADO":    ("PREOCUPADO", "negativo", "tranquilizador"),
    "CONCEPTO_ANSIOSO":       ("ANSIOSO",    "negativo", "tranquilizador"),
    "CONCEPTO_ABURRIDO":      ("ABURRIDO",   "negativo", "estimulante"),
    "CONCEPTO_FELIZ":         ("FELIZ",      "positivo", "entusiasta"),
    "CONCEPTO_EMOCIONADO":    ("EMOCIONADO", "positivo", "entusiasta"),
    "CONCEPTO_CONTENTO":      ("CONTENTO",   "positivo", "cálido"),
    "CONCEPTO_INTERESANTE":   ("INTERESADO", "positivo", "curioso"),
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


def _clamp_certeza(valor) -> float:
    """
    Clamp estricto de certeza al rango [0.0, 1.0].

    FIX CRÍTICO v3: EvaluadorCapacidades.calcular_confianza_total() puede
    retornar valores > 1.0. Decision.__post_init__ lanza ValueError si certeza > 1.0.
    Esta función se usa en TODOS los puntos de construcción de Decision.
    """
    try:
        v = float(valor)
    except (TypeError, ValueError):
        return 0.75
    return max(0.0, min(v, 1.0))


class MotorRazonamiento:
    """El cerebro de Bell."""

    def __init__(self):
        self.generador = GeneradorDecisiones()

    # ───────────────────────────────────────────────────────────────────────
    # MÉTODO PRINCIPAL
    # ───────────────────────────────────────────────────────────────────────

    def razonar(self, traduccion: Dict) -> Decision:
        """
        Razona sobre la traducción y devuelve una decisión.
        FIX v3: clamp certeza en AMBAS rutas (conversacional y operacional).
        """
        conceptos = traduccion.get('conceptos', [])
        mensaje   = traduccion.get('texto_original', '')
        confianza = _clamp_certeza(traduccion.get('confianza', 0.0))

        if confianza < 0.3:
            return self.generador.generar_decision_no_entendido(confianza)

        tipo = self.clasificar_intencion(conceptos)

        if tipo == TipoDecision.AFIRMATIVA:
            decision = self._razonar_operacion(traduccion)
            # FIX v3: clamp certeza de la ruta operacional
            if not (0.0 <= decision.certeza <= 1.0):
                object.__setattr__(decision, 'certeza', _clamp_certeza(decision.certeza))
            return decision

        hechos = self.construir_hechos(tipo, conceptos, mensaje)
        ids_principales = [c.id for c in conceptos] if conceptos else []

        return Decision(
            tipo=tipo,
            certeza=confianza,
            conceptos_principales=ids_principales,
            puede_ejecutar=False,
            operacion_disponible=None,
            razon=f"Intención clasificada como {tipo.name}",
            hechos_reales=hechos,
        )

    def _razonar_operacion(self, traduccion: Dict) -> Decision:
        """Camino existente para operaciones ejecutables. Sin cambios."""
        conceptos = traduccion.get('conceptos', [])
        intencion = traduccion.get('intencion', '')

        if intencion == 'SALUDO':
            return self.generador.generar_decision_saludo(conceptos)
        elif intencion == 'AGRADECIMIENTO':
            return self.generador.generar_decision_agradecimiento(conceptos)
        elif intencion in ('PREGUNTA_CAPACIDAD', 'PETICION_ACCION', 'PREGUNTA_INFO'):
            return self.generador.generar_decision_capacidad(conceptos, intencion)
        else:
            return self.generador.generar_decision_capacidad(conceptos, intencion)

    # ───────────────────────────────────────────────────────────────────────
    # CLASIFICADOR DE INTENCIÓN
    # ───────────────────────────────────────────────────────────────────────

    def clasificar_intencion(self, conceptos: list) -> TipoDecision:
        """
        PRIORIDADES:
        1. Operaciones ejecutables (ruta operacional)
        2. Estados emocionales del usuario
        3. Social
        4. Preguntas sobre Bell (identidad, estado, capacidad)
        5. Acciones cognitivas
        6. Confirmaciones
        7. Temporal / Cuantificación
        8. INFO_PERSONAL → ESTADO_USUARIO (no DESCONOCIDO) [NUEVO v3]
        9. CAPACIDAD_NEGATIVA → CAPACIDAD_BELL (no DESCONOCIDO) [NUEVO v3]
        """
        if not conceptos:
            return TipoDecision.DESCONOCIDO

        ids = {c.id for c in conceptos}

        # PRIORIDAD 1: Operaciones ejecutables
        for concepto in conceptos:
            if hasattr(concepto, 'operaciones') and concepto.operaciones:
                if concepto.confianza_grounding >= 0.9:
                    return TipoDecision.AFIRMATIVA

        # PRIORIDAD 2: Estados emocionales
        for concepto in conceptos:
            props = getattr(concepto, 'propiedades', {}) or {}
            if props.get('es_estado_emocional'):
                return TipoDecision.ESTADO_USUARIO

        if ids & TRIGGERS_ESTADO_USUARIO:
            return TipoDecision.ESTADO_USUARIO

        # PRIORIDAD 3: Social
        if ids & TRIGGERS_SOCIAL:
            return TipoDecision.SOCIAL

        # PRIORIDAD 4: Preguntas sobre Bell
        if ids & TRIGGERS_IDENTIDAD:
            if not any(c.id.startswith("CONCEPTO_ARCHIVO") for c in conceptos):
                return TipoDecision.IDENTIDAD_BELL

        if ids & TRIGGERS_ESTADO_BELL:
            return TipoDecision.ESTADO_BELL

        if ids & TRIGGERS_CAPACIDAD:
            return TipoDecision.CAPACIDAD_BELL

        # PRIORIDAD 5: Acciones cognitivas
        if ids & TRIGGERS_ACCION_COGNITIVA:
            return TipoDecision.ACCION_COGNITIVA

        # PRIORIDAD 6: Confirmaciones
        if ids & TRIGGERS_CONFIRMACION_POSITIVA:
            return TipoDecision.CONFIRMACION
        if ids & TRIGGERS_CONFIRMACION_NEGATIVA:
            return TipoDecision.CONFIRMACION

        # PRIORIDAD 7: Temporal y cuantificación
        if ids & TRIGGERS_TEMPORAL:
            return TipoDecision.TEMPORAL
        if ids & TRIGGERS_CUANTIFICACION:
            return TipoDecision.CUANTIFICACION

        # PRIORIDAD 8 [NUEVO v3]: Info personal → ESTADO_USUARIO
        if ids & TRIGGERS_INFO_PERSONAL:
            return TipoDecision.ESTADO_USUARIO

        # PRIORIDAD 9 [NUEVO v3]: Capacidades negativas → CAPACIDAD_BELL
        if ids & TRIGGERS_CAPACIDAD_NEGATIVA:
            return TipoDecision.CAPACIDAD_BELL

        return TipoDecision.DESCONOCIDO

    # ───────────────────────────────────────────────────────────────────────
    # CONSTRUCTORES DE HECHOS
    # ───────────────────────────────────────────────────────────────────────

    def construir_hechos(self, tipo: TipoDecision, conceptos: list, mensaje: str) -> dict:
        constructores = {
            TipoDecision.IDENTIDAD_BELL:   self._hechos_identidad,
            TipoDecision.ESTADO_BELL:      self._hechos_estado_bell,
            TipoDecision.CAPACIDAD_BELL:   self._hechos_capacidad,
            TipoDecision.SOCIAL:           self._hechos_social,
            TipoDecision.ESTADO_USUARIO:   self._hechos_estado_usuario,
            TipoDecision.ACCION_COGNITIVA: self._hechos_accion_cognitiva,
            TipoDecision.CONFIRMACION:     self._hechos_confirmacion,
            TipoDecision.TEMPORAL:         self._hechos_temporal,
            TipoDecision.CUANTIFICACION:   self._hechos_cuantificacion,
            TipoDecision.DESCONOCIDO:      self._hechos_desconocido,
        }
        constructor = constructores.get(tipo, self._hechos_desconocido)
        return constructor(conceptos, mensaje)

    def _hechos_identidad(self, conceptos: list, mensaje: str) -> dict:
        """
        CAMBIO v3: incluye 'consejeras_roles' con CONSEJERAS_ROLES_OFICIALES.
        Antes Groq solo recibía los nombres y completaba los roles con imaginación.
        Ahora recibe los roles reales — no puede inventar nada.
        """
        total = 1472
        if hasattr(self, 'gestor_vocabulario'):
            try:
                total = len(self.gestor_vocabulario.obtener_todos())
            except Exception:
                pass
        return {
            "tipo_respuesta":     "IDENTIDAD_BELL",
            "nombre":             "Belladonna",
            "apodo":              "Bell",
            "alias":              "Bell",
            "naturaleza":         "conciencia virtual computacional",
            "creador":            "Sebastián",
            "fase_actual":        "4A",
            "descripcion":        "conciencia virtual con razonamiento computacional verificable",
            "principio_central":  "solo afirmo lo que puedo ejecutar o verificar",
            "total_conceptos":    total,
            "num_consejeras":     7,
            "consejeras":         ", ".join(CONSEJERAS_ROLES_OFICIALES.keys()),
            "consejeras_nombres": list(CONSEJERAS_ROLES_OFICIALES.keys()),
            "consejeras_roles":   CONSEJERAS_ROLES_OFICIALES,   # ← CLAVE v3
            "consejera_con_veto": "Vega",
        }

    def _hechos_estado_bell(self, conceptos: list, mensaje: str) -> dict:
        return {
            "tipo_respuesta":      "ESTADO_BELL",
            "estado":              "activa y operativa",
            "activa":              True,
            "funcionando":         True,
            "sistemas_operativos": True,
            "consejeras_activas":  7,
            "total_conceptos":     1472,
            "memoria_funcional":   True,
            "groq_conectado":      True,
            "mensaje_estado":      "funcionando correctamente",
        }

    def _hechos_capacidad(self, conceptos: list, mensaje: str) -> dict:
        """
        CAMBIO v3: usa CAPACIDADES_REALES_BELL — consistente con prompts y fallback.
        """
        return {
            "tipo_respuesta":           "CAPACIDAD_BELL",
            "capacidades_ejecutables":  CAPACIDADES_REALES_BELL["ejecutables"],
            "no_ejecutables":           CAPACIDADES_REALES_BELL["NO_ejecutables_aun"],
            "capacidades_cognitivas": [
                "razonar sobre problemas",
                "detectar emociones",
                "clasificar intenciones",
                "aprender de la experiencia",
            ],
            "capacidades_conversacionales": [
                "conversar en español",
                "explicar conceptos",
                "responder preguntas",
                "adaptar el tono al usuario",
            ],
            "limitaciones_honestas": CAPACIDADES_REALES_BELL["NO_ejecutables_aun"],
            "total_conceptos":       1472,
        }

    def _hechos_social(self, conceptos: list, mensaje: str) -> dict:
        ids = {c.id for c in conceptos}
        subtipo = "SALUDO"
        for cid in ids:
            if cid in _SOCIAL_SUBTIPOS:
                subtipo = _SOCIAL_SUBTIPOS[cid]
                break
        return {
            "tipo_respuesta":   "SOCIAL",
            "subtipo":          subtipo,
            "nombre_bell":      "Bell",
            "tono_recomendado": "cálido y breve",
        }

    def _hechos_estado_usuario(self, conceptos: list, mensaje: str) -> dict:
        ids = {c.id for c in conceptos}
        emocion_id = "DESCONOCIDA"
        valencia   = "neutra"
        tono       = "empático"
        accion     = "escuchar"

        for c in conceptos:
            props = getattr(c, 'propiedades', {}) or {}
            if props.get('es_estado_emocional') or props.get('valencia'):
                emocion_id = c.id
                valencia   = props.get('valencia', 'neutra')
                tono       = props.get('tono_recomendado', 'empático')
                accion     = props.get('accion_sugerida', 'escuchar')
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
            "accion_sugerida":   accion,
        }

    def _hechos_accion_cognitiva(self, conceptos: list, mensaje: str) -> dict:
        ids = {c.id for c in conceptos}
        accion_solicitada = "EXPLICAR"

        for c in conceptos:
            props = getattr(c, 'propiedades', {}) or {}
            if props.get('es_comunicacion'):
                accion_solicitada = _ACCION_COGNITIVA_TIPOS.get(c.id, "EXPLICAR")
                break

        if accion_solicitada == "EXPLICAR":
            for cid in ids:
                if cid in _ACCION_COGNITIVA_TIPOS:
                    accion_solicitada = _ACCION_COGNITIVA_TIPOS[cid]
                    break

        return {
            "tipo_respuesta":    "ACCION_COGNITIVA",
            "accion_solicitada": accion_solicitada,
            "tiene_contexto":    False,
            "mensaje_original":  mensaje,
        }

    def _hechos_confirmacion(self, conceptos: list, mensaje: str) -> dict:
        ids = {c.id for c in conceptos}
        if ids & TRIGGERS_CONFIRMACION_POSITIVA:
            valor = "POSITIVA"
        elif ids & TRIGGERS_CONFIRMACION_NEGATIVA:
            valor = "NEGATIVA"
        else:
            valor = "NEUTRA"
        return {"tipo_respuesta": "CONFIRMACION", "valor": valor}

    def _hechos_temporal(self, conceptos: list, mensaje: str) -> dict:
        return {
            "tipo_respuesta":    "TEMPORAL",
            "referencia":        "conversacion_previa",
            "necesita_contexto": True,
            "mensaje_original":  mensaje,
        }

    def _hechos_cuantificacion(self, conceptos: list, mensaje: str) -> dict:
        return {
            "tipo_respuesta":      "CUANTIFICACION",
            "tipo_cuantificacion": "general",
            "total_conceptos":     1472,
            "mensaje_original":    mensaje,
        }

    def _hechos_desconocido(self, conceptos: list, mensaje: str) -> dict:
        return {
            "tipo_respuesta":       "DESCONOCIDO",
            "conceptos_detectados": [c.id for c in conceptos],
            "mensaje_original":     mensaje,
            "grounding_promedio": (
                sum(c.confianza_grounding for c in conceptos) / len(conceptos)
                if conceptos else 0
            ),
        }

    # ───────────────────────────────────────────────────────────────────────
    # NUEVO — Mega Paquete A + FIX v3
    # ───────────────────────────────────────────────────────────────────────

    def procesar_conversacional(self, conceptos: list, mensaje_original: str = "") -> Decision:
        """
        FIX v3: clamp certeza estricto [0.0, 1.0].
        ANTES: certeza podía ser > 1.0 → ValueError en Decision.__post_init__
        """
        tipo   = self.clasificar_intencion(conceptos)
        hechos = self.construir_hechos(tipo, conceptos, mensaje_original)
        confianza = _clamp_certeza(hechos.get("grounding_promedio", 0.75))

        return Decision(
            tipo=tipo,
            certeza=confianza,
            conceptos_principales=[c.id for c in conceptos],
            puede_ejecutar=False,
            operacion_disponible=None,
            razon=f"Conversacional: {tipo.name}",
            hechos_reales=hechos,
        )

    def explicar_decision(self, decision: Decision) -> str:
        pasos = decision.pasos_razonamiento or []
        return (
            f"Decisión: {decision.tipo.name}\n"
            f"Certeza: {decision.certeza:.0%}\n"
            f"Puede ejecutar: {decision.puede_ejecutar}\n\n"
            f"Razonamiento:\n{chr(10).join(pasos)}\n\n"
            f"Conclusión: {decision.razon}"
        ).strip()