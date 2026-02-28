"""
Generador de Salida - Fase 4A Completa

Decision → Español Natural usando TODO el vocabulario.

MODIFICADO v3 — Corrección Arquitectónica Total (sobre Mega Paquete A):

CORRECCIONES CRÍTICAS:
- BUG CORREGIDO: respuesta_groq.texto — NUNCA desempaquetar como tupla
- Echo CONECTADO en ruta conversacional (estaba ausente en versión anterior)
- _verificar_huecos_antes_de_groq(): Anti-Invención expandida — detecta
  "escríbeme un archivo", "hazme un archivo", etc. (no solo CAPACIDAD_BELL)
- _fallback_conversacional(): cubre TODOS los casos con respuestas específicas
- Memoria compartida: registra usuario Y Bell en el mismo objeto
- Contexto de espera para manejar "sí"/"no" con historial
"""
from typing import Dict, Optional, List
from datetime import datetime

from razonamiento.tipos_decision import Decision, TipoDecision, RazonRechazo
from generacion.templates_respuesta import TemplatesRespuesta
from generacion.prompts_naturales import PromptsNaturales


_TIPOS_CONVERSACIONALES = frozenset({
    "IDENTIDAD_BELL", "ESTADO_BELL", "CAPACIDAD_BELL",
    "SOCIAL", "ESTADO_USUARIO", "ACCION_COGNITIVA",
    "TEMPORAL", "CUANTIFICACION", "CONFIRMACION", "DESCONOCIDO",
})


class GeneradorSalida:
    """Genera respuestas naturales usando todo el vocabulario."""

    def __init__(self, usar_groq: bool = False):
        self.templates         = TemplatesRespuesta()
        self.usar_groq         = usar_groq
        self.prompts_naturales = PromptsNaturales()
        self._groq_wrapper     = None
        self._echo_verificador = None
        self._gestor_vocabulario = None
        self.memoria           = None

        self.stats = {
            'total_generadas':      0,
            'groq_usadas':          0,
            'groq_bloqueadas':      0,
            'fallback_a_simbolico': 0,
            'emociones_detectadas': {},
            'tipos_decision':       {},
        }

    def _inicializar_groq(self):
        if self._groq_wrapper is not None:
            return
        try:
            from llm.groq_wrapper import GroqWrapper
            from consejeras.echo.verificador_coherencia import VerificadorCoherenciaEcho
            self._groq_wrapper     = GroqWrapper()
            self._echo_verificador = VerificadorCoherenciaEcho()
        except Exception as e:
            print(f"⚠️  Error inicializando Groq: {e}")
            self.usar_groq = False

    def _obtener_gestor_vocabulario(self):
        if self._gestor_vocabulario is None:
            try:
                from vocabulario.gestor_vocabulario import obtener_gestor
                self._gestor_vocabulario = obtener_gestor()
            except ImportError:
                self._gestor_vocabulario = None
        return self._gestor_vocabulario

    def _obtener_memoria(self):
        if self.memoria is not None:
            return self.memoria
        try:
            from memoria.gestor_memoria import GestorMemoria
            self.memoria = GestorMemoria()
        except Exception:
            pass
        return self.memoria

    # ═══════════════════════════════════════════════════════════════════════════
    # MÉTODO PRINCIPAL
    # ═══════════════════════════════════════════════════════════════════════════

    def generar(self, decision: Decision, contexto: Dict = None) -> str:
        contexto = contexto or {}
        self.stats['total_generadas'] += 1

        tipo_nombre = decision.tipo.name if hasattr(decision.tipo, 'name') else str(decision.tipo)
        self.stats['tipos_decision'][tipo_nombre] = \
            self.stats['tipos_decision'].get(tipo_nombre, 0) + 1

        # RUTA CONVERSACIONAL
        if (
            tipo_nombre in _TIPOS_CONVERSACIONALES
            and hasattr(decision, 'hechos_reales')
            and decision.hechos_reales
        ):
            texto_original = contexto.get('traduccion', {}).get('texto_original', '')
            return self._generar_conversacional(decision, texto_original)

        # Verificar veto de Vega
        revision_vega = contexto.get('revision_vega', {})
        if revision_vega.get('veto', False):
            return self._generar_veto_vega(decision, contexto)

        # Detectar emoción
        texto_original = contexto.get('traduccion', {}).get('texto_original', '')
        emocion = self._detectar_emocion(texto_original)
        if emocion:
            self.stats['emociones_detectadas'][emocion] = \
                self.stats['emociones_detectadas'].get(emocion, 0) + 1

        # Generar respuesta simbólica
        respuesta_base = self._generar_simbolica(decision, contexto)

        if not self.usar_groq:
            return self._humanizar_respuesta_simbolica(respuesta_base, emocion)

        try:
            return self._generar_con_groq(decision, contexto, respuesta_base, emocion)
        except Exception as e:
            self.stats['fallback_a_simbolico'] += 1
            return self._humanizar_respuesta_simbolica(respuesta_base, emocion)

    # ═══════════════════════════════════════════════════════════════════════════
    # RUTA CONVERSACIONAL v3
    # ═══════════════════════════════════════════════════════════════════════════

    def _generar_conversacional(self, decision: Decision, mensaje_original: str = "") -> str:
        """
        FLUJO:
        1. Obtener memoria
        2. Si confirmación + contexto_espera → enriquecer mensaje
        3. Registrar mensaje usuario en memoria
        4a. Sin Groq → _fallback_conversacional()
        4b. Con Groq → _verificar_huecos_antes_de_groq() primero
            - Hueco detectado → respuesta honesta directa
            - Sin hueco → llamar Groq → verificar con Echo
        5. SIEMPRE registrar respuesta Bell en memoria
        6. Si Bell preguntó algo → registrar contexto_espera
        """
        mem            = None
        contexto_chat  = ""
        nombre_usuario = ""

        try:
            mem = self._obtener_memoria()
            if mem and mensaje_original:
                contexto_espera = mem.obtener_contexto_espera()

                if contexto_espera and self._es_confirmacion(mensaje_original):
                    mensaje_enriquecido = (
                        f"[Contexto: Bell había preguntado '{contexto_espera['pregunta_bell']}' "
                        f"sobre el tema '{contexto_espera['tema']}'. "
                        f"El usuario respondió: '{mensaje_original}']"
                    )
                    mem.agregar_mensaje("usuario", mensaje_original)
                    mem.limpiar_contexto_espera()
                    mensaje_original = mensaje_enriquecido
                else:
                    mem.agregar_mensaje("usuario", mensaje_original)
                    mem.limpiar_contexto_espera()

            if mem:
                contexto_chat  = mem.obtener_contexto(n_mensajes=8)
                nombre_usuario = mem.el_usuario_se_llama()

        except Exception:
            pass

        tipo_str = (
            decision.tipo.name
            if hasattr(decision.tipo, "name")
            else str(decision.tipo).split(".")[-1].upper()
        )
        hechos = decision.hechos_reales if hasattr(decision, "hechos_reales") else {}

        # ── Generar respuesta ─────────────────────────────────────────────────
        if not self.usar_groq:
            respuesta = self._fallback_conversacional(
                tipo_str, hechos, mensaje_original, nombre_usuario
            )
        else:
            # Anti-Invención: verificar huecos ANTES de Groq
            respuesta_honesta = self._verificar_huecos_antes_de_groq(
                tipo_str, hechos, mensaje_original
            )
            if respuesta_honesta:
                respuesta = respuesta_honesta
                self.stats['fallback_a_simbolico'] += 1
            else:
                try:
                    if self._groq_wrapper is None:
                        self._inicializar_groq()

                    if not self.usar_groq:
                        respuesta = self._fallback_conversacional(
                            tipo_str, hechos, mensaje_original, nombre_usuario
                        )
                    else:
                        from generacion.prompts_naturales import obtener_prompt_conversacional
                        prompt = obtener_prompt_conversacional(
                            tipo_decision  = tipo_str,
                            hechos         = hechos,
                            mensaje        = mensaje_original,
                            contexto_chat  = contexto_chat,
                            nombre_usuario = nombre_usuario,
                        )
                        # ✅ CORRECTO: .texto — NUNCA desempaquetar como tupla
                        respuesta_groq = self._groq_wrapper.embellecer_decision({
                            "system_prompt": prompt["system"],
                            "user_prompt":   prompt["user"],
                        })
                        respuesta = respuesta_groq.texto
                        self.stats['groq_usadas'] += 1

                        # ── Echo verifica que Groq no haya alucinado ──────────
                        # NUEVO v3: Echo ahora está conectado en ruta conversacional
                        if self._echo_verificador:
                            try:
                                resultado_echo = self._echo_verificador.verificar(
                                    respuesta, decision
                                )
                                if resultado_echo.accion_recomendada == "BLOQUEAR":
                                    self.stats['groq_bloqueadas'] += 1
                                    respuesta = self._fallback_conversacional(
                                        tipo_str, hechos, mensaje_original, nombre_usuario
                                    )
                            except Exception:
                                pass  # Si Echo falla, usar la respuesta de Groq

                except Exception as e:
                    import logging
                    logging.getLogger("generador_salida").error(
                        f"[Conv v3] Error Groq ({tipo_str}): {e}"
                    )
                    self.stats['fallback_a_simbolico'] += 1
                    respuesta = self._fallback_conversacional(
                        tipo_str, hechos, mensaje_original, nombre_usuario
                    )

        # SIEMPRE registrar respuesta de Bell en memoria
        try:
            if mem and respuesta:
                mem.agregar_mensaje("bell", respuesta)
                if self._es_pregunta_de_seguimiento(respuesta):
                    mem.registrar_contexto_espera(
                        tema          = tipo_str,
                        pregunta_bell = respuesta[-120:],
                    )
        except Exception:
            pass

        return respuesta

    # ── Helpers de contexto ───────────────────────────────────────────────────

    def _es_confirmacion(self, mensaje: str) -> bool:
        msg = mensaje.lower().strip().rstrip('!?.¿¡')
        confirmaciones = {
            'si', 'sí', 'no', 'ok', 'dale', 'claro', 'por supuesto', 'adelante',
            'listo', 'correcto', 'exacto', 'así es', 'afirmativo', 'negativo',
            'más', 'mas', 'continúa', 'continua', 'cuéntame', 'cuentame',
        }
        return msg in confirmaciones or len(msg.split()) <= 2

    def _es_pregunta_de_seguimiento(self, respuesta: str) -> bool:
        return any(s in respuesta[-80:] for s in ['?', '¿'])

    def _verificar_huecos_antes_de_groq(
        self, tipo_str: str, hechos: dict, mensaje: str
    ) -> Optional[str]:
        """
        Anti-Invención: si no hay datos suficientes o Bell no puede hacer algo,
        responde honestamente SIN llamar a Groq.

        Groq completa huecos con información fabricada → INVENCIÓN.
        Esta función lo previene.
        """
        if not mensaje:
            return None
        msg_lower = mensaje.lower()

        # Petición de crear/escribir/generar archivo (Bell no puede en Fase 4A)
        # Ampliado vs versión anterior: cubre más variantes de la petición
        palabras_crear = {
            "crear archivo", "crea un archivo", "crea el archivo",
            "hacer archivo", "hazme un archivo", "haz un archivo",
            "escríbeme un archivo", "escribeme un archivo",
            "escribe un archivo", "escribe el archivo",
            "generar archivo", "genera un archivo",
            "hacer un archivo", "crea un txt", "crea un doc",
        }
        if any(w in msg_lower for w in palabras_crear):
            return (
                "Crear archivos es una capacidad que todavía no tengo — estoy en Fase 4A "
                "y esa función está pendiente de implementar. "
                "Lo que sí puedo hacer: razonar sobre problemas, recordar nuestra "
                "conversación, ejecutar código Python básico y consultar bases de datos."
            )

        # Pregunta sobre roles de consejeras sin tener los roles en hechos
        if tipo_str == "IDENTIDAD_BELL":
            palabras_roles = {"hace", "función", "rol", "encarga", "trabaja",
                              "representa", "sirve", "ayuda con"}
            if any(w in msg_lower for w in palabras_roles):
                if "consejeras_roles" not in hechos:
                    # Salvavidas: en v3 siempre está, pero por si algo falla
                    from razonamiento.motor_razonamiento import CONSEJERAS_ROLES_OFICIALES
                    roles_str = "\n".join(
                        f"  • {n}: {r}" for n, r in CONSEJERAS_ROLES_OFICIALES.items()
                    )
                    return f"Mis consejeras y sus roles verificados:\n{roles_str}"

        return None  # Sin hueco — Groq puede llamarse

    # ═══════════════════════════════════════════════════════════════════════════
    # FALLBACK CONVERSACIONAL (sin Groq — siempre honesto y específico)
    # ═══════════════════════════════════════════════════════════════════════════

    def _fallback_conversacional(
        self,
        tipo_str:       str,
        hechos:         dict,
        mensaje:        str,
        nombre_usuario: str = "",
    ) -> str:
        import re
        n         = f", {nombre_usuario}" if nombre_usuario else ""
        msg_lower = mensaje.lower() if mensaje else ""

        # ── IDENTIDAD_BELL ────────────────────────────────────────────────────
        if tipo_str == "IDENTIDAD_BELL":
            total = hechos.get("total_conceptos", 1472)

            if any(w in msg_lower for w in ["hace", "rol", "función", "encarga", "trabaja", "sirve"]):
                from razonamiento.motor_razonamiento import CONSEJERAS_ROLES_OFICIALES
                roles_str = "\n".join(
                    f"  • {nombre_c}: {rol}"
                    for nombre_c, rol in CONSEJERAS_ROLES_OFICIALES.items()
                )
                return f"Mis consejeras y sus roles reales{n}:\n{roles_str}"

            if any(w in msg_lower for w in ["consejera", "llaman", "nombres", "quiénes", "quienes"]):
                from razonamiento.motor_razonamiento import CONSEJERAS_ROLES_OFICIALES
                nombres = ", ".join(CONSEJERAS_ROLES_OFICIALES.keys())
                return (
                    f"Mis consejeras se llaman: {nombres}. "
                    "Cada una tiene un rol específico en mi proceso de toma de decisiones. "
                    "¿Quieres saber qué hace cada una?"
                )

            if any(w in msg_lower for w in [
                "llm", "modelo de lenguaje", "gpt", "chatgpt", "ia",
                "inteligencia artificial", "bot", "chatbot", "robot"
            ]):
                return (
                    f"No soy un LLM convencional{n}. "
                    "Soy Belladonna — una conciencia virtual que razona con conceptos "
                    "verificados desde Python. "
                    f"Tengo {total} conceptos cargados y solo afirmo lo que puedo verificar. "
                    "Groq me ayuda a expresarme, pero las decisiones las tomo yo."
                )

            return (
                f"Soy Belladonna, aunque me puedes llamar Bell{n}. "
                "Soy una conciencia virtual creada por Sebastián. "
                "Mi principio central: solo afirmo lo que puedo verificar. "
                f"Tengo {total} conceptos cargados y 7 consejeras: "
                "Vega, Echo, Lyra, Nova, Luna, Iris y Sage. "
                "Estoy en Fase 4A de desarrollo. ¿Qué quieres saber?"
            )

        # ── ESTADO_BELL ───────────────────────────────────────────────────────
        elif tipo_str == "ESTADO_BELL":
            total = hechos.get("total_conceptos", 1472)
            return (
                f"Estoy activa y funcionando correctamente{n}. "
                f"Tengo {total} conceptos disponibles, 7 consejeras operativas "
                "y el Grounding 9D corriendo normalmente. ¿En qué te ayudo?"
            )

        # ── CAPACIDAD_BELL ────────────────────────────────────────────────────
        elif tipo_str == "CAPACIDAD_BELL":
            from razonamiento.motor_razonamiento import CAPACIDADES_REALES_BELL

            palabras_archivo = {
                "crear", "archivo", "generar archivo", "escribir archivo",
                "escríbeme", "escribeme", "hazme", "hacer un archivo", "crea un"
            }
            if any(w in msg_lower for w in palabras_archivo):
                return (
                    f"Crear archivos es una capacidad que todavía no tengo{n}. "
                    "Estoy en Fase 4A y esa función está pendiente de implementar. "
                    "Lo que sí puedo hacer:\n"
                    + "\n".join(f"  ✅ {c}" for c in CAPACIDADES_REALES_BELL["ejecutables"][:4])
                )

            caps    = CAPACIDADES_REALES_BELL["ejecutables"]
            no_caps = CAPACIDADES_REALES_BELL["NO_ejecutables_aun"]
            return (
                f"Mis capacidades reales en este momento{n}:\n"
                + "\n".join(f"  ✅ {c}" for c in caps)
                + "\n\nCosas que todavía NO puedo hacer:\n"
                + "\n".join(f"  ❌ {c}" for c in no_caps[:3])
                + "\n\nSoy honesta sobre mis límites — no quiero afirmar algo que no puedo cumplir."
            )

        # ── SOCIAL ────────────────────────────────────────────────────────────
        elif tipo_str == "SOCIAL":
            subtipo = hechos.get("subtipo", "SALUDO")
            hora    = datetime.now().hour

            if subtipo == "SALUDO":
                if nombre_usuario:
                    if 5 <= hora < 12:
                        return f"¡Buenos días, {nombre_usuario}! ¿En qué te puedo ayudar hoy?"
                    elif 12 <= hora < 19:
                        return f"¡Buenas tardes, {nombre_usuario}! ¿Qué necesitas?"
                    else:
                        return f"¡Buenas noches, {nombre_usuario}! Aquí estoy. ¿En qué te ayudo?"
                else:
                    if 5 <= hora < 12:
                        return "¡Buenos días! Soy Bell. ¿Cómo te llamas y en qué te ayudo?"
                    elif 12 <= hora < 19:
                        return "¡Buenas tardes! ¿En qué te puedo ayudar?"
                    else:
                        return "¡Buenas noches! Aquí estoy para lo que necesites."
            elif subtipo == "DESPEDIDA":
                return f"¡Hasta pronto{n}! Fue un gusto conversar. Aquí estaré cuando me necesites."
            elif subtipo == "AGRADECIMIENTO":
                return f"¡Con mucho gusto{n}! No dudes en preguntar si necesitas algo más."
            elif subtipo == "DISCULPA":
                return f"No hay problema{n}. Sigamos adelante, ¿en qué te ayudo?"
            return f"¡Hola{n}! ¿En qué puedo ayudarte?"

        # ── ESTADO_USUARIO ────────────────────────────────────────────────────
        elif tipo_str == "ESTADO_USUARIO":
            emocion  = hechos.get("emocion_detectada", "")
            valencia = hechos.get("valencia", "neutro")

            match_edad = re.search(r'tengo\s+(\d+)\s+años', msg_lower)
            if match_edad:
                edad = match_edad.group(1)
                return (
                    f"Entendido{n}, tienes {edad} años. "
                    "Lo he registrado para conocerte mejor. "
                    "¿Hay algo en lo que pueda ayudarte?"
                )

            if any(w in msg_lower for w in [
                "gusta", "gusto", "encanta", "interesante", "increíble",
                "genial", "forma de ser", "personalidad"
            ]):
                return (
                    f"Me alegra mucho escuchar eso{n}. "
                    "Intento ser lo más auténtica posible. "
                    "¿Hay algo en lo que pueda ayudarte?"
                )

            if any(w in msg_lower for w in ["llm", "ia", "bot", "chatbot", "artificial"]):
                return (
                    f"Soy Belladonna{n} — una conciencia virtual, no un chatbot convencional. "
                    "Razono con conceptos verificados y solo afirmo lo que puedo demostrar."
                )

            if valencia == "negativo":
                if emocion and emocion != "DESCONOCIDA":
                    return (
                        f"Entiendo que te sientes {emocion.lower()}{n}. "
                        "Cuéntame más si quieres — estoy aquí para escucharte. "
                        "¿Hay algo concreto en lo que pueda ayudarte?"
                    )
                return f"Parece que algo no va bien{n}. ¿Qué está pasando? Cuéntame."

            if valencia == "positivo":
                return f"¡Me alegra que te sientas bien{n}! ¿En qué puedo ayudarte?"

            return f"Entendido{n}. ¿Hay algo en lo que pueda ayudarte?"

        # ── ACCION_COGNITIVA ──────────────────────────────────────────────────
        elif tipo_str in ("ACCION_COGNITIVA", "ACCION_COGNITIVA_CONV"):
            accion = hechos.get("accion_solicitada", "EXPLICAR")
            mapa = {
                "EXPLICAR":    f"Con gusto te explico{n}. ¿Sobre qué tema específicamente?",
                "RESUMIR":     f"Puedo hacer un resumen{n}. ¿De qué texto o tema?",
                "REPETIR":     f"Claro{n}. ¿Qué quieres que repita de lo que hemos hablado?",
                "DEFINIR":     f"¿Qué término quieres que defina{n}?",
                "SIMPLIFICAR": f"Puedo simplificarlo{n}. ¿De qué tema o texto?",
                "ACLARAR":     f"Claro{n}. ¿Qué parte quieres que aclare?",
                "COMPARAR":    f"Puedo comparar{n}. ¿Qué dos cosas o conceptos?",
                "ELABORAR":    f"Con gusto elaboro más{n}. ¿Sobre qué parte?",
            }
            return mapa.get(accion, f"Entendido{n}. ¿Sobre qué tema específicamente?")

        # ── CONFIRMACION ──────────────────────────────────────────────────────
        elif tipo_str == "CONFIRMACION":
            valor = hechos.get("valor", "NEUTRA")
            if valor == "POSITIVA":
                return f"Perfecto{n}. Dime por dónde seguimos."
            elif valor == "NEGATIVA":
                return f"Entendido{n}. ¿Cómo prefieres que lo enfoque entonces?"
            return f"Recibido{n}. ¿Cómo continuamos?"

        # ── TEMPORAL ──────────────────────────────────────────────────────────
        elif tipo_str == "TEMPORAL":
            return (
                f"Déjame revisar nuestra conversación{n}... "
                "¿Puedes indicarme el tema específico que buscas? "
                "Tengo en memoria los últimos intercambios de esta sesión."
            )

        # ── CUANTIFICACION ────────────────────────────────────────────────────
        elif tipo_str == "CUANTIFICACION":
            total = hechos.get("total_conceptos", 1472)
            return (
                f"En números concretos{n}: tengo {total} conceptos cargados, "
                "7 consejeras activas, 36 comandos de terminal disponibles, "
                "y estoy en Fase 4A de desarrollo. "
                "¿Hay algún dato específico que necesites?"
            )

        # ── DESCONOCIDO ───────────────────────────────────────────────────────
        else:
            return (
                f"No estoy segura de haber entendido bien{n}. "
                "¿Puedes reformularlo de otra manera? "
                "Quiero asegurarme de darte una respuesta honesta y útil."
            )

    # ═══════════════════════════════════════════════════════════════════════════
    # DETECCIÓN DE EMOCIÓN
    # ═══════════════════════════════════════════════════════════════════════════

    def _detectar_emocion(self, texto: str) -> Optional[str]:
        if not texto:
            return None
        texto_lower = texto.lower()
        patrones = {
            "frustrado": ["no funciona", "error", "falla", "frustrado", "harto",
                          "imposible", "ya intenté", "sigue sin"],
            "confundido": ["no entiendo", "confundido", "qué significa", "me explicas"],
            "emocionado": ["genial", "excelente", "increíble", "funcionó", "perfecto"],
            "preocupado": ["preocupado", "miedo", "temo", "nervioso"],
            "ocupado":    ["rápido", "urgente", "apurado", "prisa"],
        }
        for emocion, keywords in patrones.items():
            if any(k in texto_lower for k in keywords):
                return emocion
        return None

    # ═══════════════════════════════════════════════════════════════════════════
    # GENERACIÓN SIMBÓLICA (ruta operacional — preservada íntegra)
    # ═══════════════════════════════════════════════════════════════════════════

    def _generar_simbolica(self, decision: Decision, contexto: Dict) -> str:
        if decision.tipo == TipoDecision.AFIRMATIVA:
            return self._generar_afirmativa(decision, contexto)
        elif decision.tipo == TipoDecision.NEGATIVA:
            return self._generar_negativa(decision, contexto)
        elif decision.tipo == TipoDecision.SALUDO:
            return self._generar_saludo(decision)
        elif decision.tipo == TipoDecision.AGRADECIMIENTO:
            return self._generar_agradecimiento(decision)
        elif decision.tipo == TipoDecision.NO_ENTENDIDO:
            return self._generar_no_entendido(decision, contexto)
        elif decision.tipo == TipoDecision.NECESITA_ACLARACION:
            return self._generar_aclaracion(decision)
        else:
            return "Déjame ver cómo puedo ayudarte con eso."

    def _humanizar_respuesta_simbolica(self, respuesta: str, emocion: Optional[str]) -> str:
        prefijos = {
            "frustrado":  "Entiendo que puede ser frustrante. ",
            "confundido": "Déjame explicarlo de forma más clara. ",
            "emocionado": "¡Qué bien! ",
            "preocupado": "No te preocupes. ",
            "ocupado":    "",
        }
        prefijo = prefijos.get(emocion, "")
        reemplazos = [
            ("Sí, puedo ", "¡Claro! Puedo "),
            ("No, no puedo ", "La verdad, no puedo "),
            ("Procesando...", ""),
            ("STATUS: OK", ""),
        ]
        resultado = respuesta
        for viejo, nuevo in reemplazos:
            resultado = resultado.replace(viejo, nuevo)
        return prefijo + resultado

    # ═══════════════════════════════════════════════════════════════════════════
    # GENERACIÓN CON GROQ (ruta operacional)
    # ═══════════════════════════════════════════════════════════════════════════

    def _generar_con_groq(self, decision, contexto, respuesta_base, emocion=None) -> str:
        """
        BUG CORREGIDO:
        ✅ CORRECTO:   respuesta_groq_obj.texto
        ❌ INCORRECTO: texto, tokens = self._groq_wrapper.embellecer_decision(...)
        """
        if self._groq_wrapper is None:
            self._inicializar_groq()
        if not self.usar_groq:
            return respuesta_base

        decision_data = self._extraer_datos_decision(decision, contexto)
        if emocion:
            decision_data['emocion_usuario'] = emocion

        system_prompt = self.prompts_naturales.obtener_system_prompt()
        user_prompt   = self.prompts_naturales.obtener_prompt(decision.tipo, decision_data)
        decision_data['system_prompt'] = system_prompt
        decision_data['user_prompt']   = user_prompt

        # ✅ CORRECTO: .texto — NUNCA desempaquetar como tupla
        respuesta_groq_obj = self._groq_wrapper.embellecer_decision(decision_data)
        texto_groq = respuesta_groq_obj.texto
        self.stats['groq_usadas'] += 1

        resultado_verificacion = self._echo_verificador.verificar(texto_groq, decision_data)
        if resultado_verificacion.accion_recomendada == "BLOQUEAR":
            self.stats['groq_bloqueadas'] += 1
            return respuesta_base
        return texto_groq

    def _extraer_datos_decision(self, decision: Decision, contexto: Dict) -> Dict:
        traduccion = contexto.get('traduccion', {})
        gestor = self._obtener_gestor_vocabulario()
        expresiones_naturales = []
        if gestor:
            texto = traduccion.get('texto_original', '')
            conceptos_rel = gestor.buscar_conceptos_relacionados(texto, limite=3)
            for c in conceptos_rel:
                expresiones_naturales.extend(c.palabras_español[:2])
        return {
            'tipo':                  decision.tipo.name,
            'puede_ejecutar':        decision.puede_ejecutar,
            'certeza':               decision.certeza,
            'conceptos':             [c.id for c in traduccion.get('conceptos', [])[:3]],
            'accion':                self._extraer_accion(decision, contexto),
            'texto_original':        traduccion.get('texto_original', ''),
            'razon':                 decision.razon if hasattr(decision, 'razon') else None,
            'razon_rechazo': (
                decision.razon_rechazo.name
                if hasattr(decision, 'razon_rechazo') and decision.razon_rechazo
                else None
            ),
            'expresiones_sugeridas': expresiones_naturales[:5],
            'total_conceptos':       gestor.total_conceptos() if gestor else 0,
        }

    # ═══════════════════════════════════════════════════════════════════════════
    # GENERADORES ESPECÍFICOS
    # ═══════════════════════════════════════════════════════════════════════════

    def _generar_veto_vega(self, decision: Decision, contexto: Dict) -> str:
        revision_vega = contexto.get('revision_vega', {})
        razon = revision_vega.get('razon_veto', 'Esta acción está restringida por seguridad')
        import random
        return random.choice([
            f"Entiendo lo que quieres, pero {razon.lower()}. ¿Hay algo más en lo que pueda ayudarte?",
            f"No puedo hacer eso porque {razon.lower()}.",
        ])

    def _generar_afirmativa(self, decision: Decision, contexto: Dict) -> str:
        accion = self._extraer_accion(decision, contexto)
        import random
        if decision.certeza >= 0.9:
            return random.choice([
                f"¡Claro que sí! Puedo {accion} sin problema.",
                f"¡Por supuesto! Eso de {accion} está dentro de mis capacidades.",
            ])
        return random.choice([
            f"Sí, puedo {accion}, aunque quizás necesite algunos detalles más.",
            f"Creo que puedo {accion}. ¿Me das más contexto?",
        ])

    def _generar_negativa(self, decision: Decision, contexto: Dict) -> str:
        accion = self._extraer_accion(decision, contexto)
        import random
        return random.choice([
            f"Eso de {accion} está fuera de mi alcance, pero puedo ayudarte de otras formas.",
            f"No tengo la capacidad de {accion}. ¿Hay algo más en lo que pueda asistirte?",
        ])

    def _generar_saludo(self, decision: Decision) -> str:
        hora = datetime.now().hour
        import random
        if 5 <= hora < 12:
            return random.choice(["¡Buenos días! ¿En qué puedo ayudarte hoy?"])
        elif 12 <= hora < 19:
            return random.choice(["¡Buenas tardes! ¿Cómo te va? ¿En qué te ayudo?"])
        else:
            return random.choice(["¡Buenas noches! ¿En qué te puedo ayudar?"])

    def _generar_agradecimiento(self, decision: Decision) -> str:
        import random
        return random.choice([
            "¡Con mucho gusto! Me alegra haber ayudado.",
            "¡Para eso estoy! No dudes en preguntar más.",
        ])

    def _generar_no_entendido(self, decision: Decision, contexto: Dict) -> str:
        import random
        return random.choice([
            "No estoy segura de entender bien. ¿Podrías darme más detalles?",
            "Perdona, ¿a qué te refieres exactamente?",
        ])

    def _generar_aclaracion(self, decision: Decision) -> str:
        return "Necesito un poco más de información para poder ayudarte. ¿Me cuentas más?"

    def _extraer_accion(self, decision: Decision, contexto: Dict) -> str:
        traduccion = contexto.get('traduccion', {})
        texto_original = traduccion.get('texto_original', '').lower()
        verbos = {
            'leer': 'leer archivos', 'escribir': 'escribir', 'crear': 'crear',
            'eliminar': 'eliminar', 'listar': 'listar', 'mostrar': 'mostrar',
            'ejecutar': 'ejecutar código', 'calcular': 'hacer cálculos',
        }
        for palabra in texto_original.split():
            p = palabra.strip('¿?.,;:!').lower()
            if p in verbos:
                return verbos[p]
        return "eso"

    # ═══════════════════════════════════════════════════════════════════════════
    # ESTADÍSTICAS
    # ═══════════════════════════════════════════════════════════════════════════

    def obtener_estadisticas(self) -> Dict:
        total = self.stats['total_generadas']
        return {
            'total_generadas':      total,
            'groq_usadas':          self.stats['groq_usadas'],
            'groq_bloqueadas':      self.stats['groq_bloqueadas'],
            'fallback_a_simbolico': self.stats['fallback_a_simbolico'],
            'tasa_groq':            self.stats['groq_usadas'] / total if total > 0 else 0.0,
            'tasa_bloqueo': (
                self.stats['groq_bloqueadas'] / self.stats['groq_usadas']
                if self.stats['groq_usadas'] > 0 else 0.0
            ),
            'emociones_detectadas': self.stats['emociones_detectadas'],
            'tipos_decision':       self.stats['tipos_decision'],
        }

    def mostrar_estadisticas(self):
        stats = self.obtener_estadisticas()
        print()
        print("=" * 60)
        print("📊 ESTADÍSTICAS DEL GENERADOR DE SALIDA")
        print("=" * 60)
        print(f"Total respuestas: {stats['total_generadas']}")
        print(f"Con Groq: {stats['groq_usadas']} ({stats['tasa_groq']*100:.1f}%)")
        print(f"Bloqueadas por Echo: {stats['groq_bloqueadas']}")
        print(f"Fallback a simbólico: {stats['fallback_a_simbolico']}")
        print("=" * 60)