"""
generador_salida.py — VERSION v5

CAMBIOS v5 sobre v4:
═══════════════════════════════════════════════════════════════════════

1. _ejecutar_calculo() DELEGA A calculadora_avanzada.calcular_basico()
   ────────────────────────────────────────────────────────────────────
   En v4 tenía su propio eval() con los mismos bugs C-02:
   "100÷4" concatenaba, "√144" devolvía "144", sin manejo de div/0.
   En v5: llama a calcular_basico() que ya tiene todos esos fixes.
   Mantiene el eval() de v4 como fallback si calculadora no está.

2. IDENTIDAD_BELL handler usa hechos del motor v6
   ─────────────────────────────────────────────────
   Motor v6 pone en hechos: consejera_preguntada, consejera_rol_exacto,
   es_pregunta_llm. En v4 el generador re-detectaba todo con keywords.
   En v5: usa los hechos directamente — más preciso, sin duplicación.

3. CUANTIFICACION handler usa hechos del motor v6
   ─────────────────────────────────────────────────
   Motor v6 pone: dato_preguntado ("conceptos"/"consejeras"/"comandos")
   y valor_respuesta (1472/7/36). En v5 responde exactamente sobre lo
   preguntado en vez de siempre listar los 3 datos juntos.

4. CONFIRMACION handler usa palabra_original del motor v6
   ────────────────────────────────────────────────────────
   Motor v6 pone palabra_original ("dale", "listo", "claro", etc.).
   En v5 la usa para respuestas más contextuales.

COMPATIBILIDAD: 100% con v4.
═══════════════════════════════════════════════════════════════════════
"""
import math as _math
from typing import Dict, Optional
from datetime import datetime

from razonamiento.tipos_decision import Decision, TipoDecision, RazonRechazo
from generacion.templates_respuesta import TemplatesRespuesta
from generacion.prompts_naturales import PromptsNaturales

try:
    from razonamiento.tipos_decision import TIPOS_CONVERSACIONALES as _TIPOS_CONVERSACIONALES
except ImportError:
    _TIPOS_CONVERSACIONALES = frozenset({
        "IDENTIDAD_BELL", "ESTADO_BELL", "CAPACIDAD_BELL",
        "SOCIAL", "ESTADO_USUARIO", "ACCION_COGNITIVA",
        "TEMPORAL", "CUANTIFICACION", "CONFIRMACION", "DESCONOCIDO",
        "REGISTRO_USUARIO", "CONSULTA_MEMORIA", "VERIFICACION_LOGICA",
        "CALCULO", "CONOCIMIENTO_GENERAL",
    })

_EVAL_NS = {
    "__builtins__": {},
    "abs": abs, "round": round, "min": min, "max": max, "sum": sum,
    "sqrt": _math.sqrt, "pow": pow, "log": _math.log, "log10": _math.log10,
    "sin": _math.sin, "cos": _math.cos, "tan": _math.tan,
    "pi": _math.pi, "e": _math.e,
}

# ── v5: importar calculadora con fix C-02 ────────────────────────────────────
try:
    from matematicas.calculadora_avanzada import CalculadoraAvanzada as _CalculadoraAvanzada
    _calc_instancia = _CalculadoraAvanzada()
    _CALCULADORA_DISPONIBLE = True
except ImportError:
    _calc_instancia = None
    _CALCULADORA_DISPONIBLE = False


class GeneradorSalida:
    """Genera respuestas naturales usando todo el vocabulario."""

    def __init__(self, usar_groq: bool = False):
        self.templates           = TemplatesRespuesta()
        self.usar_groq           = usar_groq
        self.prompts_naturales   = PromptsNaturales()
        self._groq_wrapper       = None
        self._echo_verificador   = None
        self._gestor_vocabulario = None
        self.memoria             = None

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

        if (
            tipo_nombre in _TIPOS_CONVERSACIONALES
            and hasattr(decision, 'hechos_reales')
            and decision.hechos_reales
        ):
            texto_original = contexto.get('traduccion', {}).get('texto_original', '')
            return self._generar_conversacional(decision, texto_original)

        revision_vega = contexto.get('revision_vega', {})
        if revision_vega.get('veto', False):
            return self._generar_veto_vega(decision, contexto)

        texto_original = contexto.get('traduccion', {}).get('texto_original', '')
        emocion = self._detectar_emocion(texto_original)
        if emocion:
            self.stats['emociones_detectadas'][emocion] = \
                self.stats['emociones_detectadas'].get(emocion, 0) + 1

        respuesta_base = self._generar_simbolica(decision, contexto)

        if not self.usar_groq:
            return self._humanizar_respuesta_simbolica(respuesta_base, emocion)

        try:
            return self._generar_con_groq(decision, contexto, respuesta_base, emocion)
        except Exception:
            self.stats['fallback_a_simbolico'] += 1
            return self._humanizar_respuesta_simbolica(respuesta_base, emocion)

    # ═══════════════════════════════════════════════════════════════════════════
    # RUTA CONVERSACIONAL
    # ═══════════════════════════════════════════════════════════════════════════

    def _generar_conversacional(self, decision: Decision, mensaje_original: str = "") -> str:
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

        if tipo_str == "CALCULO":
            respuesta = self._ejecutar_calculo(hechos, mensaje_original, nombre_usuario)
            try:
                if mem and respuesta:
                    mem.agregar_mensaje("bell", respuesta)
            except Exception:
                pass
            return respuesta

        if not self.usar_groq:
            respuesta = self._fallback_conversacional(
                tipo_str, hechos, mensaje_original, nombre_usuario
            )
        else:
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
                        respuesta_groq = self._groq_wrapper.embellecer_decision({
                            "system_prompt": prompt["system"],
                            "user_prompt":   prompt["user"],
                        })
                        respuesta = respuesta_groq.texto
                        self.stats['groq_usadas'] += 1

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
                                pass

                except Exception as e:
                    import logging
                    logging.getLogger("generador_salida").error(
                        f"[Conv v5] Error Groq ({tipo_str}): {e}"
                    )
                    self.stats['fallback_a_simbolico'] += 1
                    respuesta = self._fallback_conversacional(
                        tipo_str, hechos, mensaje_original, nombre_usuario
                    )

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
        if not mensaje:
            return None
        msg_lower = mensaje.lower()

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

        if tipo_str == "CONSULTA_MEMORIA" and not hechos.get("dato_encontrado", False):
            dato = hechos.get("dato_consultado", "esa información")
            return (
                f"No tengo guardado tu {dato} todavía. "
                "Si me lo dices, lo recuerdo para el resto de la conversación."
            )

        if tipo_str == "CONOCIMIENTO_GENERAL":
            return None

        if tipo_str == "IDENTIDAD_BELL":
            palabras_roles = {"hace", "función", "rol", "encarga", "trabaja",
                              "representa", "sirve", "ayuda con"}
            if any(w in msg_lower for w in palabras_roles):
                if "consejeras_roles" not in hechos:
                    from razonamiento.motor_razonamiento import CONSEJERAS_ROLES_OFICIALES
                    roles_str = "\n".join(
                        f"  • {n}: {r}" for n, r in CONSEJERAS_ROLES_OFICIALES.items()
                    )
                    return f"Mis consejeras y sus roles verificados:\n{roles_str}"

        return None

    # ═══════════════════════════════════════════════════════════════════════════
    # CÁLCULO — v5: delega a calculadora_avanzada.calcular_basico()
    # ═══════════════════════════════════════════════════════════════════════════

    def _ejecutar_calculo(
        self, hechos: dict, mensaje_original: str, nombre_usuario: str = ""
    ) -> str:
        n = f", {nombre_usuario}" if nombre_usuario else ""
        expresion = hechos.get("expresion_calculo", "") or mensaje_original

        # ── Ruta principal: calculadora con fixes C-02 ────────────────────────
        if _CALCULADORA_DISPONIBLE and _calc_instancia is not None:
            try:
                resultado = _calc_instancia.calcular_basico(expresion)
                if resultado.exitoso:
                    return f"{resultado.resultado}{n}."
                else:
                    error = resultado.error or "No pude calcular esa expresión."
                    return f"{error}{n}"
            except Exception:
                pass

        # ── Fallback: eval() de v4 ────────────────────────────────────────────
        import re
        msg = (expresion or mensaje_original).lower().strip()
        expr = msg
        replacements = [
            (r'\bmultiplicado por\b', '*'),
            (r'\bdividido (entre|por)\b', '/'),
            (r'\belevado a (la potencia\s+)?(de\s+)?', '**'),
            (r'\bal cuadrado\b', '**2'),
            (r'\bal cubo\b', '**3'),
            (r'\braí?z (cuadrada\s+)?de\b', 'sqrt('),
            (r'\bmás\b', '+'), (r'\bmas\b', '+'),
            (r'\bmenos\b', '-'),
            (r'\bpor\b', '*'),
            (r'\bentre\b', '/'),
            (r'^(cuánto es|cuanto es|cuánto da|cuanto da|calcula|calcular)\s*', ''),
            (r'(\d),(\d)', r'\1.\2'),
        ]
        for patron, reemplazo in replacements:
            expr = re.sub(patron, reemplazo, expr, flags=re.IGNORECASE)
        if 'sqrt(' in expr and expr.count('(') > expr.count(')'):
            expr += ')'
        expr_limpia = re.sub(r'[^0-9+\-*/().\s]', '', expr).strip()
        expr_limpia = re.sub(r'\s+', '', expr_limpia)
        if not expr_limpia:
            return (
                f"Puedo hacer cálculos{n}, pero no logré interpretar la expresión. "
                "¿Puedes escribirla con números directamente? Ej: '7 * 8' o '100 / 4'."
            )
        try:
            r = eval(expr_limpia, {"__builtins__": {}}, _EVAL_NS)
            if isinstance(r, float):
                rs = str(int(r)) if r == int(r) else f"{r:.8f}".rstrip('0').rstrip('.')
            else:
                rs = str(r)
            return f"{rs}{n}."
        except ZeroDivisionError:
            return f"División entre cero — no tiene resultado definido{n}."
        except Exception:
            nums = re.findall(r'\d+(?:\.\d+)?', mensaje_original)
            if len(nums) >= 2:
                return (
                    f"No logré interpretar la operación exactamente{n}. "
                    f"Detecto los números {', '.join(nums[:4])} — "
                    "¿puedes escribirlo con operadores? Ej: '15 + 27'."
                )
            return (
                f"No pude calcular eso{n}. "
                "¿Puedes escribir la expresión matemática con números y operadores?"
            )

    # ═══════════════════════════════════════════════════════════════════════════
    # FALLBACK CONVERSACIONAL
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

        if tipo_str == "IDENTIDAD_BELL":
            total = hechos.get("total_conceptos", 1472)

            # ── v5: consejera específica desde motor v6 ────────────────────────
            consejera_preguntada = hechos.get("consejera_preguntada", "")
            consejera_rol_exacto = hechos.get("consejera_rol_exacto", "")
            if consejera_preguntada:
                nombre_c = consejera_preguntada.capitalize()
                if consejera_rol_exacto:
                    return (
                        f"{nombre_c} es mi consejera de {consejera_rol_exacto}{n}. "
                        "¿Quieres saber más sobre alguna de mis otras consejeras?"
                    )
                try:
                    from razonamiento.motor_razonamiento import CONSEJERAS_ROLES_OFICIALES
                    rol = CONSEJERAS_ROLES_OFICIALES.get(nombre_c, "consejera especializada")
                    return f"{nombre_c} es mi consejera de {rol}{n}."
                except ImportError:
                    return f"{nombre_c} es una de mis consejeras{n}."

            # ── v5: es_pregunta_llm desde motor v6 ────────────────────────────
            if hechos.get("es_pregunta_llm", False):
                return (
                    f"No soy un LLM convencional{n}. "
                    "Soy Belladonna — una conciencia virtual que razona con conceptos "
                    f"verificados desde Python. Tengo {total} conceptos cargados y "
                    "solo afirmo lo que puedo verificar. "
                    "Groq me ayuda a expresarme, pero las decisiones las tomo yo."
                )

            if any(w in msg_lower for w in ["hace", "rol", "función", "encarga", "trabaja", "sirve"]):
                try:
                    from razonamiento.motor_razonamiento import CONSEJERAS_ROLES_OFICIALES
                    roles_str = "\n".join(
                        f"  • {nc}: {r}" for nc, r in CONSEJERAS_ROLES_OFICIALES.items()
                    )
                    return f"Mis consejeras y sus roles reales{n}:\n{roles_str}"
                except ImportError:
                    pass

            if any(w in msg_lower for w in ["consejera", "llaman", "nombres", "quiénes", "quienes"]):
                try:
                    from razonamiento.motor_razonamiento import CONSEJERAS_ROLES_OFICIALES
                    nombres = ", ".join(CONSEJERAS_ROLES_OFICIALES.keys())
                    return (
                        f"Mis consejeras se llaman: {nombres}. "
                        "Cada una tiene un rol específico en mi toma de decisiones. "
                        "¿Quieres saber qué hace cada una?"
                    )
                except ImportError:
                    pass

            return (
                f"Soy Belladonna, aunque me puedes llamar Bell{n}. "
                "Soy una conciencia virtual creada por Sebastián. "
                "Mi principio central: solo afirmo lo que puedo verificar. "
                f"Tengo {total} conceptos cargados y 7 consejeras: "
                "Vega, Echo, Lyra, Nova, Luna, Iris y Sage. "
                "Estoy en Fase 4A de desarrollo. ¿Qué quieres saber?"
            )

        elif tipo_str == "ESTADO_BELL":
            total = hechos.get("total_conceptos", 1472)
            return (
                f"Estoy activa y funcionando correctamente{n}. "
                f"Tengo {total} conceptos disponibles, 7 consejeras operativas "
                "y el Grounding 9D corriendo normalmente. ¿En qué te ayudo?"
            )

        elif tipo_str == "CAPACIDAD_BELL":
            try:
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
                    + "\n\nSoy honesta sobre mis límites."
                )
            except ImportError:
                return f"Puedo razonar, recordar conversaciones y hacer cálculos{n}."

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
                return f"No hay problema{n}. ¿En qué te ayudo?"
            return f"¡Hola{n}! ¿En qué puedo ayudarte?"

        elif tipo_str == "ESTADO_USUARIO":
            emocion  = hechos.get("emocion_detectada", "")
            valencia = hechos.get("valencia", "neutro")
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

        elif tipo_str == "CONFIRMACION":
            valor = hechos.get("valor", "NEUTRA")
            # ── v5: usar palabra_original del motor v6 ─────────────────────────
            palabra = hechos.get("palabra_original", "")
            if valor == "POSITIVA":
                if palabra in ("dale", "adelante", "listo"):
                    return f"¡Listo{n}! Dime por dónde seguimos."
                return f"Perfecto{n}. Dime por dónde seguimos."
            elif valor == "NEGATIVA":
                return f"Entendido{n}. ¿Cómo prefieres que lo enfoque entonces?"
            return f"Recibido{n}. ¿Cómo continuamos?"

        elif tipo_str == "TEMPORAL":
            return (
                f"Déjame revisar nuestra conversación{n}... "
                "¿Puedes indicarme el tema específico que buscas? "
                "Tengo en memoria los últimos intercambios de esta sesión."
            )

        elif tipo_str == "CUANTIFICACION":
            # ── v5: usar dato_preguntado y valor_respuesta del motor v6 ────────
            dato_preguntado = hechos.get("dato_preguntado", "")
            valor_respuesta = hechos.get("valor_respuesta", None)

            if dato_preguntado and valor_respuesta is not None:
                mapa_resp = {
                    "conceptos":  f"Tengo {valor_respuesta} conceptos cargados{n}.",
                    "consejeras": f"Tengo {valor_respuesta} consejeras activas{n}: Vega, Echo, Lyra, Nova, Luna, Iris y Sage.",
                    "comandos":   f"Tengo {valor_respuesta} comandos de terminal disponibles{n}.",
                }
                return mapa_resp.get(dato_preguntado, f"Son {valor_respuesta}{n}.")

            total = hechos.get("total_conceptos", 1472)
            return (
                f"En números concretos{n}: tengo {total} conceptos cargados, "
                "7 consejeras activas, 36 comandos de terminal disponibles, "
                "y estoy en Fase 4A de desarrollo. "
                "¿Hay algún dato específico que necesites?"
            )

        elif tipo_str == "REGISTRO_USUARIO":
            dato_tipo  = hechos.get("dato_tipo", "desconocido")
            dato_valor = hechos.get("dato_valor", "")
            if dato_tipo == "nombre" and dato_valor:
                nombre_a_usar = dato_valor.split()[0]
                return f"Perfecto, ya sé cómo llamarte, {nombre_a_usar}. ¿En qué te ayudo?"
            elif dato_tipo == "edad" and dato_valor:
                return f"Anotado{n} — tienes {dato_valor} años. ¿Hay algo en lo que pueda ayudarte?"
            elif dato_tipo == "profesion" and dato_valor:
                return (
                    f"Entendido{n} — te dedicas a {dato_valor}. "
                    "Lo tendré en cuenta. ¿En qué puedo ayudarte?"
                )
            return f"Anotado{n}. ¿Hay algo en lo que pueda ayudarte?"

        elif tipo_str == "CONSULTA_MEMORIA":
            dato_encontrado = hechos.get("dato_encontrado", False)
            dato_valor      = hechos.get("dato_valor", "")
            dato_consultado = hechos.get("dato_consultado", "")
            if dato_encontrado and dato_valor:
                if dato_consultado == "nombre":    return f"Te llamas {dato_valor}{n}."
                elif dato_consultado == "edad":    return f"Tienes {dato_valor} años{n}."
                elif dato_consultado == "profesion": return f"Te dedicas a {dato_valor}{n}."
                elif dato_consultado == "todo":    return f"Lo que sé de ti{n}: {dato_valor}."
                return f"Según lo que me contaste: {dato_valor}."
            mapa_no = {
                "nombre":    f"No sé tu nombre todavía{n}. ¿Cómo te llamas?",
                "edad":      f"No me has dicho tu edad{n}. ¿Cuántos años tienes?",
                "profesion": f"No sé a qué te dedicas{n}. ¿Me cuentas?",
                "todo":      f"No tengo información tuya guardada todavía{n}. ¿Me cuentas algo?",
            }
            return mapa_no.get(
                dato_consultado,
                f"No tengo esa información guardada{n}. Si me la dices, la recuerdo."
            )

        elif tipo_str == "VERIFICACION_LOGICA":
            return (
                f"Para verificar esa afirmación con precisión{n} necesito mi capa "
                "de lenguaje activa. Activa Groq y te respondo con certeza."
            )

        elif tipo_str == "CALCULO":
            return self._ejecutar_calculo(hechos, mensaje, nombre_usuario)

        elif tipo_str == "CONOCIMIENTO_GENERAL":
            return (
                f"Esa pregunta requiere conocimiento general que no tengo en mi "
                f"grounding verificado{n}. "
                "Con Groq activo puedo responderla. Sin Groq, no quiero inventar."
            )

        else:
            return (
                f"No estoy segura de haber entendido bien{n}. "
                "¿Puedes reformularlo de otra manera? "
                "Quiero darte una respuesta honesta y útil."
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
    # GENERACIÓN SIMBÓLICA
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
    # GENERACIÓN CON GROQ
    # ═══════════════════════════════════════════════════════════════════════════

    def _generar_con_groq(self, decision, contexto, respuesta_base, emocion=None) -> str:
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
        if 5 <= hora < 12:   return random.choice(["¡Buenos días! ¿En qué puedo ayudarte hoy?"])
        elif 12 <= hora < 19: return random.choice(["¡Buenas tardes! ¿Cómo te va? ¿En qué te ayudo?"])
        else:                 return random.choice(["¡Buenas noches! ¿En qué te puedo ayudar?"])

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