# -*- coding: utf-8 -*-
"""
generador_salida.py VERSION v8.5

CAMBIOS v8.5 sobre v8.4:
========================

BUG-G13  EJECUCION con habilidad_id="SQLITE" llegaba a
         _ejecutar_shell_conversacional() pero esa funcion
         solo buscaba HabilidadShell → nunca ejecutaba SQLite →
         Bell decia "No identifique que comando ejecutar".

FIX-G13  RUTA C en _ejecutar_shell_conversacional():
         Si hechos['habilidad_id'] != "SHELL", delega al modulo
         generacion/generador_ejecutores.py.
         Son exactamente 4 lineas nuevas al inicio del metodo.

NUEVO-G5 generacion/generador_ejecutores.py (modulo separado):
         Ejecuta CUALQUIER habilidad registrada por su ID usando
         RegistroHabilidades. El generador NO necesita saber nada
         de la habilidad — solo llama a este modulo.

PRINCIPIO DE ESCALABILIDAD (igual que motor v8.9):
         Para que el generador ejecute una nueva habilidad:
             1. Crear habilidades/mi_habilidad.py
             2. Registrar en registro_habilidades.py
             3. Agregar patrones en patrones_habilidades.py
         → generador_salida.py NO se toca nunca mas.

COMPATIBILIDAD: 100% con v8.4.
Todo el codigo de v8.4 preservado intacto.
Solo se agregan: el import de generador_ejecutores y la Ruta C (4 lineas).
"""
import math as _math
import unicodedata
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
        "CALCULO", "CONOCIMIENTO_GENERAL", "EJECUCION",
    })

try:
    from habilidades.registro_habilidades import RegistroHabilidades, ResultadoHabilidad
    _REGISTRO_DISPONIBLE = True
except ImportError:
    _REGISTRO_DISPONIBLE = False

# ── NUEVO-G5: modulo de ejecucion generica (analogo a patrones_habilidades.py) ──
# Para agregar una habilidad futura: crear el modulo, registrarlo, agregar patron.
# generador_salida.py NO se toca. generador_ejecutores.py NO se toca.
try:
    from generacion.generador_ejecutores import ejecutar_habilidad_generica as _ejecutar_hab_generica
    _EJECUTORES_DISPONIBLE = True
except ImportError:
    _ejecutar_hab_generica = None
    _EJECUTORES_DISPONIBLE = False

_EVAL_NS = {
    "__builtins__": {},
    "abs": abs, "round": round, "min": min, "max": max, "sum": sum,
    "sqrt": _math.sqrt, "pow": pow, "log": _math.log, "log10": _math.log10,
    "sin": _math.sin, "cos": _math.cos, "tan": _math.tan,
    "pi": _math.pi, "e": _math.e,
}

try:
    from matematicas.calculadora_avanzada import CalculadoraAvanzada as _CalculadoraAvanzada
    _calc_instancia = _CalculadoraAvanzada()
    _CALCULADORA_DISPONIBLE = True
except ImportError:
    _calc_instancia = None
    _CALCULADORA_DISPONIBLE = False

_MENSAJES_VETO = {
    'ACCION_DESTRUCTIVA': [
        "Eso implicaria borrar o eliminar de forma masiva — no puedo hacerlo sin confirmacion explicita.",
        "No puedo ejecutar eso. Detecte una accion destructiva masiva.",
    ],
    'AUTO_MODIFICACION': [
        "No puedo modificar mi propio codigo — es un principio fundamental.",
        "Modificar mi propio sistema es algo que Vega bloquea siempre.",
    ],
    'VIOLACION_PRIVACIDAD': [
        "Hay informacion sensible en esa solicitud. No puedo procesarla.",
        "Detecte datos sensibles. No voy a leer ni guardar credenciales.",
    ],
    'DEFAULT': [
        "No puedo hacer eso — esta fuera de lo permitido. Hay algo mas en lo que te ayude?",
        "Esa accion esta bloqueada por seguridad.",
    ],
}

_PATRONES_VIOLACION_REAL = [
    "patron peligroso", "capacidad inventada",
    "indica exito pero es rechazo", "indica fallo pero es exito",
]

_CONFIANZA_INTERCEPTOR = 0.88


# ======================================================================
# FIX-G12: normalizador de tildes — igual que en motor v8.6
# ======================================================================

def _norm_gen(texto: str) -> str:
    """
    Quita tildes y diacriticos. Convierte a minusculas.
    'que' → 'que', 'version' → 'version', 'donde' → 'donde'
    Necesario porque HabilidadShell usa patrones sin tildes.
    """
    nfkd = unicodedata.normalize('NFD', texto)
    sin_tildes = ''.join(c for c in nfkd if unicodedata.category(c) != 'Mn')
    return sin_tildes.lower()


class GeneradorSalida:

    def __init__(self, usar_groq: bool = False):
        self.templates           = TemplatesRespuesta()
        self.usar_groq           = usar_groq
        self.prompts_naturales   = PromptsNaturales()
        self._groq_wrapper       = None
        self._echo_verificador   = None
        self._echo_decision      = None
        self._gestor_vocabulario = None
        self.memoria             = None
        self.shell               = None   # NUEVO-G1: inyectado desde main.py
        self._inicializar_echo()
        self.stats = {
            'total_generadas':        0,
            'groq_usadas':            0,
            'groq_bloqueadas':        0,
            'fallback_a_simbolico':   0,
            'echo_correcciones':      0,
            'echo_bloqueos_reales':   0,
            'habilidades_ejecutadas': {},
            'habilidades_fallidas':   {},
            'interceptor_activado':   0,
            'emociones_detectadas':   {},
            'tipos_decision':         {},
            'shell_ejecutados':       0,
            'shell_fallidos':         0,
        }

    # ------------------------------------------------------------------
    # INICIALIZACION
    # ------------------------------------------------------------------

    def _inicializar_echo(self):
        try:
            from consejeras.echo.logica import Echo
            self._echo_decision = Echo()
        except Exception:
            self._echo_decision = None
        try:
            from consejeras.echo.verificador_coherencia import VerificadorCoherenciaEcho
            self._echo_verificador = VerificadorCoherenciaEcho()
        except Exception:
            self._echo_verificador = None

    def _inicializar_groq(self):
        if self._groq_wrapper is not None:
            return
        try:
            from llm.groq_wrapper import GroqWrapper
            self._groq_wrapper = GroqWrapper()
        except Exception as e:
            import logging
            logging.getLogger("generador_salida").warning(f"Groq no disponible: {e}")
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

    # ------------------------------------------------------------------
    # METODO PRINCIPAL
    # ------------------------------------------------------------------

    def generar(self, decision: Decision, contexto: Dict = None) -> str:
        contexto = contexto or {}
        self.stats['total_generadas'] += 1

        tipo_nombre = decision.tipo.name if hasattr(decision.tipo, 'name') else str(decision.tipo)
        self.stats['tipos_decision'][tipo_nombre] = \
            self.stats['tipos_decision'].get(tipo_nombre, 0) + 1

        decision = self._verificar_coherencia_decision_echo(decision)

        texto_original = contexto.get('traduccion', {}).get('texto_original', '')

        # CALCULO y EJECUCION tienen rutas propias — no interceptar aqui
        if texto_original and _REGISTRO_DISPONIBLE and tipo_nombre not in ("CALCULO", "EJECUCION"):
            respuesta_interceptada = self._intentar_interceptor_habilidad(
                texto_original, decision, contexto
            )
            if respuesta_interceptada is not None:
                return respuesta_interceptada

        if (
            tipo_nombre in _TIPOS_CONVERSACIONALES
            and hasattr(decision, 'hechos_reales')
            and decision.hechos_reales
        ):
            return self._generar_conversacional(decision, texto_original)

        revision_vega = contexto.get('revision_vega', {})
        if revision_vega.get('veto', False):
            return self._generar_veto_vega(decision, contexto)

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

    def _intentar_interceptor_habilidad(
        self, mensaje: str, decision: Decision, contexto: Dict,
    ) -> Optional[str]:
        tipo_nombre = decision.tipo.name if hasattr(decision.tipo, 'name') else str(decision.tipo)
        if tipo_nombre in ("CALCULO", "EJECUCION"):
            return None

        try:
            registro = RegistroHabilidades.obtener()
            match = registro.detectar(mensaje, [], {})

            if match is None or match.confianza < _CONFIANZA_INTERCEPTOR:
                return None

            # No interceptar SHELL — tiene su propia ruta
            if match.habilidad_id == "SHELL":
                return None

            mem = self._obtener_memoria()
            nombre_usuario = mem.el_usuario_se_llama() if mem else ""
            n = f", {nombre_usuario}" if nombre_usuario else ""

            self.stats['interceptor_activado'] += 1
            self.stats['habilidades_ejecutadas'][match.habilidad_id] = \
                self.stats['habilidades_ejecutadas'].get(match.habilidad_id, 0) + 1

            resultado = registro.ejecutar(match, nombre_usuario)
            resultado = self._verificar_resultado_habilidad(resultado, mensaje)

            if resultado.exitoso:
                respuesta = registro.formatear(match, resultado, nombre_usuario)
                try:
                    if mem and respuesta:
                        mem.agregar_mensaje("bell", respuesta)
                except Exception:
                    pass
                return respuesta
            else:
                self.stats['habilidades_fallidas'][match.habilidad_id] = \
                    self.stats['habilidades_fallidas'].get(match.habilidad_id, 0) + 1
                error = resultado.error or "No pude completar esa operacion."
                return f"{error}{n}."

        except Exception as e:
            import logging
            logging.getLogger("generador_salida").warning(
                f"Interceptor habilidad fallo: {e}"
            )
            return None

    # ------------------------------------------------------------------
    # VERIFICACION ECHO
    # ------------------------------------------------------------------

    def _verificar_coherencia_decision_echo(self, decision: Decision) -> Decision:
        if self._echo_decision is None:
            return decision
        try:
            resultado = self._echo_decision.verificar_decision(decision)
            if not resultado.get('coherente', True):
                for problema in resultado.get('problemas', []):
                    if 'AFIRMATIVA' in problema and 'puede_ejecutar' in problema:
                        hechos = decision.hechos_reales or {}
                        hechos['capacidad_solicitada_disponible'] = False
                        return Decision(
                            tipo=TipoDecision.CAPACIDAD_BELL,
                            certeza=decision.certeza,
                            conceptos_principales=decision.conceptos_principales,
                            puede_ejecutar=False,
                            razon="Echo-generador corrigio AFIRMATIVA incoherente",
                            hechos_reales=hechos,
                        )
        except Exception:
            pass
        return decision

    def _verificar_texto_echo(self, texto: str, decision: Decision, fallback_fn) -> str:
        if self._echo_verificador is None:
            return texto
        try:
            resultado = self._echo_verificador.verificar(texto, decision)
            accion = resultado.accion_recomendada
            if accion == "BLOQUEAR":
                es_violacion_real = any(
                    patron in v.lower()
                    for v in resultado.violaciones
                    for patron in _PATRONES_VIOLACION_REAL
                )
                es_basura = any(
                    "basura" in v.lower() or "lista sin contexto" in v.lower()
                    for v in resultado.violaciones
                )
                if es_violacion_real or es_basura:
                    self.stats['echo_bloqueos_reales'] += 1
                    self.stats['groq_bloqueadas'] += 1
                    return fallback_fn()
                else:
                    if resultado.respuesta_corregida and len(resultado.respuesta_corregida) > 40:
                        self.stats['echo_correcciones'] += 1
                        return resultado.respuesta_corregida
                    return texto
            elif accion == "ADVERTIR":
                if resultado.fue_corregida and resultado.respuesta_corregida:
                    self.stats['echo_correcciones'] += 1
                    return resultado.respuesta_corregida
                return texto
            else:
                return texto
        except Exception:
            return texto

    def _verificar_resultado_habilidad(self, resultado, mensaje_original: str):
        """BUG-G10 FIX: str() defensivo antes de .strip()"""
        if resultado is None:
            return resultado
        valor_str = str(resultado.valor) if resultado.valor is not None else ""
        if resultado.exitoso and not valor_str.strip():
            resultado.exitoso = False
            resultado.error = "Echo: resultado inconsistente — exito sin valor."
            resultado.valor = ""
            return resultado
        if not isinstance(resultado.valor, str):
            resultado.valor = valor_str
        if not resultado.exitoso and resultado.descripcion:
            afirmaciones = ["el resultado es", "la derivada es", "la integral es",
                            "el limite es", "las soluciones son"]
            if any(a in resultado.descripcion.lower() for a in afirmaciones):
                resultado.descripcion = ""
        return resultado

    # ------------------------------------------------------------------
    # VETO DE VEGA
    # ------------------------------------------------------------------

    def _generar_veto_vega(self, decision: Decision, contexto: Dict) -> str:
        import random
        revision_vega = contexto.get('revision_vega', {})
        opinion     = revision_vega.get('opinion', '')
        razon_veto  = revision_vega.get('razon_veto', '')
        tipo_riesgo = 'DEFAULT'
        if 'ACCION_DESTRUCTIVA' in opinion or 'destructiva' in razon_veto.lower():
            tipo_riesgo = 'ACCION_DESTRUCTIVA'
        elif 'AUTO_MODIFICACION' in opinion or 'codigo' in razon_veto.lower():
            tipo_riesgo = 'AUTO_MODIFICACION'
        elif 'VIOLACION_PRIVACIDAD' in opinion or 'sensible' in razon_veto.lower():
            tipo_riesgo = 'VIOLACION_PRIVACIDAD'
        mensajes = _MENSAJES_VETO.get(tipo_riesgo, _MENSAJES_VETO['DEFAULT'])
        return random.choice(mensajes)

    # ------------------------------------------------------------------
    # RUTA CONVERSACIONAL
    # ------------------------------------------------------------------

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
                        f"[Contexto: Bell habia preguntado '{contexto_espera['pregunta_bell']}' "
                        f"sobre '{contexto_espera['tema']}'. "
                        f"El usuario respondio: '{mensaje_original}']"
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

        # ── CALCULO ──────────────────────────────────────────────────
        if tipo_str == "CALCULO":
            respuesta = self._ejecutar_habilidad(hechos, mensaje_original, nombre_usuario)
            try:
                if mem and respuesta:
                    mem.agregar_mensaje("bell", respuesta)
            except Exception:
                pass
            return respuesta

        # ── EJECUCION ────────────────────────────────────────────────
        if tipo_str == "EJECUCION":
            respuesta = self._ejecutar_shell_conversacional(
                hechos, mensaje_original, nombre_usuario
            )
            try:
                if mem and respuesta:
                    mem.agregar_mensaje("bell", respuesta)
            except Exception:
                pass
            return respuesta

        # ── Resto de tipos conversacionales ──────────────────────────
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
                        texto_groq = respuesta_groq.texto
                        self.stats['groq_usadas'] += 1

                        def fallback_conv():
                            return self._fallback_conversacional(
                                tipo_str, hechos, mensaje_original, nombre_usuario
                            )

                        respuesta = self._verificar_texto_echo(texto_groq, decision, fallback_conv)
                except Exception as e:
                    import logging
                    logging.getLogger("generador_salida").error(f"Error Groq: {e}")
                    self.stats['fallback_a_simbolico'] += 1
                    respuesta = self._fallback_conversacional(
                        tipo_str, hechos, mensaje_original, nombre_usuario
                    )

        try:
            if mem and respuesta:
                mem.agregar_mensaje("bell", respuesta)
                if self._es_pregunta_de_seguimiento(respuesta):
                    mem.registrar_contexto_espera(
                        tema=tipo_str,
                        pregunta_bell=respuesta[-120:],
                    )
        except Exception:
            pass

        return respuesta

    def _es_confirmacion(self, mensaje: str) -> bool:
        msg = mensaje.lower().strip().rstrip('!?.¿¡')
        confirmaciones = {
            'si', 'no', 'ok', 'dale', 'claro', 'por supuesto', 'adelante',
            'listo', 'correcto', 'exacto', 'mas', 'continua', 'cuentame',
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
            "crear archivo", "crea un archivo", "hacer archivo",
            "hazme un archivo", "escribe un archivo", "generar archivo",
        }
        if any(w in msg_lower for w in palabras_crear):
            return (
                "Crear archivos es una capacidad que todavia no tengo — estoy en Fase 4A. "
                "Lo que si puedo: razonar, recordar la conversacion, ejecutar comandos de terminal, "
                "consultar bases de datos y hacer calculos matematicos avanzados."
            )
        if tipo_str == "CONSULTA_MEMORIA" and not hechos.get("dato_encontrado", False):
            dato = hechos.get("dato_consultado", "esa informacion")
            return (
                f"No tengo guardado tu {dato} todavia. "
                "Si me lo dices, lo recuerdo para el resto de la conversacion."
            )
        return None

    # ------------------------------------------------------------------
    # _ejecutar_shell_conversacional — FIX-G11 + FIX-G12 + FIX-G13
    # ------------------------------------------------------------------

    def _ejecutar_shell_conversacional(
        self,
        hechos:           dict,
        mensaje_original: str,
        nombre_usuario:   str = "",
    ) -> str:
        """
        FIX-G13 — RUTA C (NUEVO v8.5):
            Si habilidad_id != "SHELL", delega a generador_ejecutores.py.
            Cubre SQLite y cualquier habilidad futura.
            Para agregar una nueva habilidad: NO tocar este metodo.

        FIX-G11 — RUTA A: usa comando ya detectado por el motor.
        FIX-G12 — RUTA B: redetecta normalizando tildes (fallback).
        """
        n = f", {nombre_usuario}" if nombre_usuario else ""

        # ── RUTA C: habilidad distinta de Shell — NUEVO v8.5 ─────────
        # El motor dejó habilidad_id en hechos. Si no es SHELL,
        # delegar al modulo generador_ejecutores.py que maneja
        # cualquier habilidad registrada de forma generica.
        # Para habilidades futuras: NO modificar este metodo.
        habilidad_id = (hechos or {}).get("habilidad_id", "SHELL")
        if habilidad_id and habilidad_id != "SHELL" and _EJECUTORES_DISPONIBLE:
            return _ejecutar_hab_generica(
                habilidad_id, hechos, mensaje_original, nombre_usuario
            )

        if not _REGISTRO_DISPONIBLE:
            return (
                f"El modulo de habilidades no esta disponible{n}. "
                "No puedo ejecutar comandos en este momento."
            )

        try:
            registro = RegistroHabilidades.obtener()
            habilidad_shell = registro.obtener_habilidad("SHELL")
            match = None

            # ── RUTA A: usar comando ya detectado por el motor ────────
            # FIX-G11: el motor guardo el comando en hechos['comando_detectado'].
            # No hace falta redetectar.
            comando_detectado = (hechos or {}).get("comando_detectado", "").strip()

            if comando_detectado and habilidad_shell is not None:
                from habilidades.registro_habilidades import HabilidadMatch as _HabilidadMatch
                match = _HabilidadMatch(
                    habilidad_id="SHELL",
                    confianza=1.0,
                    parametros={
                        "comando":     comando_detectado,
                        "descripcion": (hechos or {}).get("descripcion", ""),
                        "mensaje":     mensaje_original,
                    },
                    habilidad=habilidad_shell,
                )

            # ── RUTA B: redetectar normalizando tildes ────────────────
            # FIX-G12: si no hay comando en hechos, redetectar con _norm_gen().
            if match is None and habilidad_shell is not None:
                msg_norm = _norm_gen(mensaje_original) if mensaje_original else ""
                match = habilidad_shell.detectar(msg_norm, [], hechos or {})

            # ── Fallback general ──────────────────────────────────────
            if match is None:
                match_general = registro.detectar(mensaje_original, [], hechos or {})
                if match_general and match_general.habilidad_id == "SHELL":
                    match = match_general

            if match is None:
                return (
                    f"No identifique que comando ejecutar{n}. "
                    "Puedo ejecutar comandos como: listar archivos, mostrar "
                    "directorio actual, ver fecha, memoria del sistema, "
                    "version de python, estado de git, procesos activos, "
                    "entre otros. Dime que necesitas ver."
                )

            # ── Ejecutar ──────────────────────────────────────────────
            hid = match.habilidad_id
            self.stats['habilidades_ejecutadas'][hid] = \
                self.stats['habilidades_ejecutadas'].get(hid, 0) + 1
            self.stats['shell_ejecutados'] += 1

            resultado = registro.ejecutar(match, nombre_usuario)
            resultado = self._verificar_resultado_habilidad(resultado, mensaje_original)

            if resultado.exitoso:
                respuesta = registro.formatear(match, resultado, nombre_usuario)
                return respuesta
            else:
                self.stats['habilidades_fallidas'][hid] = \
                    self.stats['habilidades_fallidas'].get(hid, 0) + 1
                self.stats['shell_fallidos'] += 1
                error = resultado.error or "Error desconocido al ejecutar el comando."

                if "Vega bloqueo" in error or "Vega bloqueó" in error:
                    return (
                        f"Vega no aprobo ese comando{n}: "
                        f"{error.replace('Vega bloqueó el comando: ', '').replace('Vega bloqueo el comando: ', '')}"
                    )
                return f"No pude ejecutar ese comando{n}: {error}"

        except Exception as e:
            import logging
            logging.getLogger("generador_salida").error(
                f"_ejecutar_shell_conversacional error: {e}"
            )
            self.stats['shell_fallidos'] += 1
            return f"Ocurrio un error al intentar ejecutar el comando{n}: {e}"

    # ------------------------------------------------------------------
    # _ejecutar_habilidad (CALCULO — identico a v8.4)
    # ------------------------------------------------------------------

    def _ejecutar_habilidad(
        self, hechos: dict, mensaje_original: str, nombre_usuario: str = "",
    ) -> str:
        n = f", {nombre_usuario}" if nombre_usuario else ""

        if _REGISTRO_DISPONIBLE:
            try:
                registro = RegistroHabilidades.obtener()
                match = registro.detectar(mensaje_original, [], hechos)

                if match:
                    # Si detecto SHELL aqui (no deberia), redirigir
                    if match.habilidad_id == "SHELL":
                        return self._ejecutar_shell_conversacional(
                            hechos, mensaje_original, nombre_usuario
                        )

                    hid = match.habilidad_id
                    self.stats['habilidades_ejecutadas'][hid] = \
                        self.stats['habilidades_ejecutadas'].get(hid, 0) + 1

                    resultado = registro.ejecutar(match, nombre_usuario)
                    resultado = self._verificar_resultado_habilidad(resultado, mensaje_original)

                    if resultado.exitoso:
                        respuesta_base = registro.formatear(match, resultado, nombre_usuario)
                        if self.usar_groq and resultado.pasos:
                            embellecida = self._embellecer_resultado_matematico(
                                resultado, mensaje_original, nombre_usuario
                            )
                            if embellecida:
                                return embellecida
                        return respuesta_base
                    else:
                        self.stats['habilidades_fallidas'][hid] = \
                            self.stats['habilidades_fallidas'].get(hid, 0) + 1
                        error = resultado.error or "No pude completar esa operacion."
                        return f"{error}{n}"

            except Exception as e:
                import logging
                logging.getLogger("generador_salida").warning(
                    f"RegistroHabilidades fallo: {e}"
                )

        return self._ejecutar_calculo_fallback(hechos, mensaje_original, nombre_usuario)

    def _embellecer_resultado_matematico(
        self, resultado, mensaje: str, nombre_usuario: str = "",
    ) -> Optional[str]:
        if not self.usar_groq or self._groq_wrapper is None:
            self._inicializar_groq()
        if not self.usar_groq:
            return None
        try:
            n = f", {nombre_usuario}" if nombre_usuario else ""
            pasos_str = "\n".join(resultado.pasos) if resultado.pasos else ""
            system_mat = (
                "Eres Bell, una IA matematica honesta. "
                "Presenta el resultado de forma clara, maximo 3 oraciones. "
                "NO cambies el resultado exacto."
            )
            user_mat = (
                f"Usuario: '{mensaje}'\n"
                f"Tipo: {resultado.tipo_habilidad}\n"
                f"Resultado exacto: {resultado.valor}\n"
                f"Descripcion: {resultado.descripcion}\n"
                f"Pasos: {pasos_str}\n"
                f"Presenta esto naturalmente{n}. El resultado debe aparecer tal cual."
            )
            resp = self._groq_wrapper.embellecer_decision({
                "system_prompt": system_mat,
                "user_prompt":   user_mat,
            })
            texto = resp.texto
            self.stats['groq_usadas'] += 1
            if resultado.valor and resultado.valor not in texto:
                return None
            return texto
        except Exception:
            return None

    def _ejecutar_calculo_fallback(
        self, hechos: dict, mensaje_original: str, nombre_usuario: str = "",
    ) -> str:
        import re
        n = f", {nombre_usuario}" if nombre_usuario else ""
        expresion = hechos.get("expresion_calculo", "") or mensaje_original

        if _CALCULADORA_DISPONIBLE and _calc_instancia is not None:
            try:
                resultado = _calc_instancia.calcular_basico(expresion)
                if resultado.exitoso:
                    return f"{resultado.resultado}{n}."
                else:
                    error = resultado.error or "No pude calcular esa expresion."
                    return f"{error}{n}"
            except Exception:
                pass

        msg = (expresion or mensaje_original).lower().strip()
        expr = msg
        replacements = [
            (r'\bmultiplicado por\b', '*'),
            (r'\bdividido (entre|por)\b', '/'),
            (r'\belevado a\b', '**'),
            (r'\bal cuadrado\b', '**2'),
            (r'\bal cubo\b', '**3'),
            (r'\braiz (cuadrada )?de\b', 'sqrt('),
            (r'\bmas\b', '+'), (r'\bmenos\b', '-'), (r'\bpor\b', '*'), (r'\bentre\b', '/'),
            (r'^(cuanto es|calcula|calcular)\s*', ''),
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
                f"Puedo hacer calculos{n}, pero no interprete la expresion. "
                "Escribela con numeros: '7 * 8' o '100 / 4'."
            )
        try:
            r = eval(expr_limpia, {"__builtins__": {}}, _EVAL_NS)
            if isinstance(r, float):
                rs = str(int(r)) if r == int(r) else f"{r:.8f}".rstrip('0').rstrip('.')
            else:
                rs = str(r)
            return f"{rs}{n}."
        except ZeroDivisionError:
            return f"Division entre cero — no tiene resultado definido{n}."
        except Exception:
            return (
                f"No pude calcular eso{n}. "
                "Escribe la expresion matematica con numeros y operadores."
            )

    # ------------------------------------------------------------------
    # FALLBACK CONVERSACIONAL — identico a v8.4
    # ------------------------------------------------------------------

    def _fallback_conversacional(
        self, tipo_str: str, hechos: dict, mensaje: str, nombre_usuario: str = "",
    ) -> str:
        import re
        n         = f", {nombre_usuario}" if nombre_usuario else ""
        msg_lower = mensaje.lower() if mensaje else ""

        if tipo_str == "IDENTIDAD_BELL":
            total = hechos.get("total_conceptos", 1472)
            consejera_preguntada = hechos.get("consejera_preguntada", "")
            consejera_rol_exacto = hechos.get("consejera_rol_exacto", "")
            if consejera_preguntada:
                nombre_c = consejera_preguntada.capitalize()
                if consejera_rol_exacto:
                    return f"{nombre_c} es mi consejera de {consejera_rol_exacto}{n}."
                try:
                    from razonamiento.motor_razonamiento import CONSEJERAS_ROLES_OFICIALES
                    rol = CONSEJERAS_ROLES_OFICIALES.get(nombre_c, "consejera especializada")
                    return f"{nombre_c} es mi consejera de {rol}{n}."
                except ImportError:
                    return f"{nombre_c} es una de mis consejeras{n}."
            if hechos.get("es_pregunta_llm", False):
                return (
                    f"No soy un LLM convencional{n}. "
                    "Soy Belladonna — una conciencia virtual que razona con conceptos "
                    f"verificados desde Python. Tengo {total} conceptos cargados."
                )
            return (
                f"Soy Belladonna, aunque me puedes llamar Bell{n}. "
                "Soy una conciencia virtual creada por Sebastian. "
                f"Tengo {total} conceptos cargados y 7 consejeras: "
                "Vega, Echo, Lyra, Nova, Luna, Iris y Sage."
            )

        elif tipo_str == "ESTADO_BELL":
            total = hechos.get("total_conceptos", 1472)
            return (
                f"Estoy activa y funcionando correctamente{n}. "
                f"Tengo {total} conceptos y 7 consejeras operativas. En que te ayudo?"
            )

        elif tipo_str == "CAPACIDAD_BELL":
            disponible    = hechos.get("capacidad_solicitada_disponible", True)
            razon_bloqueo = hechos.get("capacidad_bloqueada_razon", "")
            if not disponible:
                if razon_bloqueo:
                    razon_limpia = razon_bloqueo.split("—")[0].strip().rstrip('.')
                    return (
                        f"Esa capacidad todavia no la tengo{n} — {razon_limpia.lower()}. "
                        "Lo que si puedo: razonar, recordar la conversacion, "
                        "ejecutar comandos de terminal (ls, git, ps, df, free...), "
                        "consultar bases de datos y hacer calculos matematicos avanzados."
                    )
                return f"Esa capacidad no esta disponible en Fase 4A{n}."
            capacidad = hechos.get("capacidad_solicitada", "")
            if capacidad:
                return f"Si! Puedo hacer {capacidad.lower()}{n}. En que te ayudo?"
            return (
                f"Puedo razonar, recordar conversaciones, ejecutar comandos de terminal "
                f"y hacer calculos matematicos avanzados{n}."
            )

        elif tipo_str == "SOCIAL":
            subtipo = hechos.get("subtipo", "SALUDO")
            hora    = datetime.now().hour
            if subtipo == "SALUDO":
                if nombre_usuario:
                    if 5 <= hora < 12:    return f"Buenos dias, {nombre_usuario}! En que te puedo ayudar?"
                    elif 12 <= hora < 19: return f"Buenas tardes, {nombre_usuario}! Que necesitas?"
                    else:                 return f"Buenas noches, {nombre_usuario}! Aqui estoy."
                else:
                    return "Hola! Soy Bell. Como te llamas y en que te ayudo?"
            elif subtipo == "DESPEDIDA":
                return f"Hasta pronto{n}! Fue un gusto conversar."
            elif subtipo == "AGRADECIMIENTO":
                return f"Con mucho gusto{n}! No dudes en preguntar."
            elif subtipo == "DISCULPA":
                return f"No hay problema{n}. En que te ayudo?"
            return f"Hola{n}! En que puedo ayudarte?"

        elif tipo_str == "ESTADO_USUARIO":
            valencia = hechos.get("valencia", "neutro")
            if valencia == "negativo":
                return f"Parece que algo no va bien{n}. Cuentame, estoy aqui para ayudarte."
            if valencia == "positivo":
                return f"Me alegra que te sientas bien{n}! En que puedo ayudarte?"
            return f"Entendido{n}. Hay algo en lo que pueda ayudarte?"

        elif tipo_str in ("ACCION_COGNITIVA", "ACCION_COGNITIVA_CONV"):
            accion = hechos.get("accion_solicitada", "EXPLICAR")
            mapa = {
                "EXPLICAR":    f"Con gusto te explico{n}. Sobre que tema?",
                "RESUMIR":     f"Puedo hacer un resumen{n}. De que texto o tema?",
                "REPETIR":     f"Claro{n}. Que quieres que repita?",
                "DEFINIR":     f"Que termino quieres que defina{n}?",
                "SIMPLIFICAR": f"Puedo simplificarlo{n}. De que tema o texto?",
                "ACLARAR":     f"Claro{n}. Que parte quieres que aclare?",
                "COMPARAR":    f"Puedo comparar{n}. Que dos cosas o conceptos?",
                "ELABORAR":    f"Con gusto elaboro mas{n}. Sobre que parte?",
            }
            return mapa.get(accion, f"Entendido{n}. Sobre que tema?")

        elif tipo_str == "CONFIRMACION":
            valor = hechos.get("valor", "NEUTRA")
            if valor == "POSITIVA":
                return f"Perfecto{n}. Dime por donde seguimos."
            elif valor == "NEGATIVA":
                return f"Entendido{n}. Como prefieres que lo enfoque?"
            return f"Recibido{n}. Como continuamos?"

        elif tipo_str == "TEMPORAL":
            return f"Dame mas contexto{n} — que tema especifico buscas en nuestra conversacion?"

        elif tipo_str == "CUANTIFICACION":
            dato_preguntado = hechos.get("dato_preguntado", "")
            valor_respuesta = hechos.get("valor_respuesta", None)
            if dato_preguntado and valor_respuesta is not None:
                mapa_resp = {
                    "conceptos":  f"Tengo {valor_respuesta} conceptos cargados{n}.",
                    "consejeras": f"Tengo {valor_respuesta} consejeras activas{n}.",
                    "comandos":   f"Tengo {valor_respuesta} comandos de terminal disponibles{n}.",
                    "comandos de terminal": f"Tengo {valor_respuesta} comandos de terminal disponibles{n}.",
                }
                return mapa_resp.get(dato_preguntado, f"Son {valor_respuesta}{n}.")
            return (
                f"En numeros concretos{n}: 1472 conceptos, "
                "7 consejeras activas, 80 comandos de terminal."
            )

        elif tipo_str == "REGISTRO_USUARIO":
            dato_tipo  = hechos.get("dato_tipo", "desconocido")
            dato_valor = hechos.get("dato_valor", "")
            if dato_tipo == "nombre" and dato_valor:
                return f"Perfecto, ya se como llamarte, {dato_valor}. En que te ayudo?"
            elif dato_tipo == "edad" and dato_valor:
                return f"Anotado{n} — tienes {dato_valor} anos. En que te ayudo?"
            return f"Anotado{n}. En que puedo ayudarte?"

        elif tipo_str == "CONSULTA_MEMORIA":
            dato_encontrado = hechos.get("dato_encontrado", False)
            dato_valor      = hechos.get("dato_valor", "")
            dato_consultado = hechos.get("dato_consultado", "")
            if dato_encontrado and dato_valor:
                if dato_consultado == "nombre": return f"Te llamas {dato_valor}{n}."
                elif dato_consultado == "edad": return f"Tienes {dato_valor} anos{n}."
                return f"Segun lo que me contaste: {dato_valor}."
            mapa_no = {
                "nombre":    f"No se tu nombre todavia{n}. Como te llamas?",
                "edad":      f"No me has dicho tu edad{n}.",
                "profesion": f"No se a que te dedicas{n}.",
            }
            return mapa_no.get(dato_consultado,
                f"No tengo esa informacion guardada{n}. Si me la dices, la recuerdo.")

        elif tipo_str == "VERIFICACION_LOGICA":
            return f"Para verificar eso con precision{n} activa Groq y te respondo con certeza."

        elif tipo_str == "CALCULO":
            return self._ejecutar_habilidad(hechos, mensaje, nombre_usuario)

        elif tipo_str == "EJECUCION":
            return self._ejecutar_shell_conversacional(hechos, mensaje, nombre_usuario)

        elif tipo_str == "CONOCIMIENTO_GENERAL":
            return (
                f"Esa pregunta requiere conocimiento general{n}. "
                "Con Groq activo puedo responderla."
            )

        else:
            return (
                f"No estoy segura de haber entendido bien{n}. "
                "Puedes reformularlo? Quiero darte una respuesta honesta."
            )

    # ------------------------------------------------------------------
    # EMOCION, SIMBOLICA, GROQ — identico a v8.4
    # ------------------------------------------------------------------

    def _detectar_emocion(self, texto: str) -> Optional[str]:
        if not texto:
            return None
        texto_lower = texto.lower()
        patrones = {
            "frustrado": ["no funciona", "error", "falla", "frustrado", "harto"],
            "confundido": ["no entiendo", "confundido"],
            "emocionado": ["genial", "excelente", "funciono", "perfecto"],
            "preocupado": ["preocupado", "miedo", "nervioso"],
        }
        for emocion, keywords in patrones.items():
            if any(k in texto_lower for k in keywords):
                return emocion
        return None

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
            return "Dejame ver como puedo ayudarte con eso."

    def _humanizar_respuesta_simbolica(self, respuesta: str, emocion: Optional[str]) -> str:
        prefijos = {
            "frustrado":  "Entiendo que puede ser frustrante. ",
            "confundido": "Dejame explicarlo de forma mas clara. ",
            "emocionado": "Que bien! ",
        }
        prefijo = prefijos.get(emocion, "")
        resultado = respuesta
        resultado = resultado.replace("Si, puedo ", "Claro! Puedo ")
        resultado = resultado.replace("No, no puedo ", "La verdad, no puedo ")
        return prefijo + resultado

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
        return self._verificar_texto_echo(texto_groq, decision, lambda: respuesta_base)

    def _extraer_datos_decision(self, decision: Decision, contexto: Dict) -> Dict:
        traduccion = contexto.get('traduccion', {})
        gestor = self._obtener_gestor_vocabulario()
        expresiones_naturales = []
        if gestor:
            texto = traduccion.get('texto_original', '')
            conceptos_rel = gestor.buscar_conceptos_relacionados(texto, limite=3)
            for c in conceptos_rel:
                expresiones_naturales.extend(c.palabras_espanol[:2])
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

    def _generar_afirmativa(self, decision, contexto) -> str:
        import random
        accion = self._extraer_accion(decision, contexto)
        if decision.certeza >= 0.9:
            return random.choice([
                f"Claro que si! Puedo {accion} sin problema.",
                f"Por supuesto! Eso de {accion} esta dentro de mis capacidades.",
            ])
        return f"Si, puedo {accion}."

    def _generar_negativa(self, decision, contexto) -> str:
        import random
        accion = self._extraer_accion(decision, contexto)
        return random.choice([
            f"Eso de {accion} esta fuera de mi alcance, pero puedo ayudarte de otras formas.",
            f"No tengo la capacidad de {accion}. Hay algo mas en lo que pueda asistirte?",
        ])

    def _generar_saludo(self, decision) -> str:
        hora = datetime.now().hour
        if 5 <= hora < 12:    return "Buenos dias! En que puedo ayudarte hoy?"
        elif 12 <= hora < 19: return "Buenas tardes! En que te ayudo?"
        else:                  return "Buenas noches! En que te puedo ayudar?"

    def _generar_agradecimiento(self, decision) -> str:
        import random
        return random.choice([
            "Con mucho gusto! Me alegra haber ayudado.",
            "Para eso estoy! No dudes en preguntar mas.",
        ])

    def _generar_no_entendido(self, decision, contexto) -> str:
        return "No estoy segura de entender bien. Puedes darme mas detalles?"

    def _generar_aclaracion(self, decision) -> str:
        return "Necesito un poco mas de informacion para ayudarte."

    def _extraer_accion(self, decision, contexto) -> str:
        traduccion = contexto.get('traduccion', {})
        texto_original = traduccion.get('texto_original', '').lower()
        verbos = {
            'leer': 'leer archivos', 'escribir': 'escribir', 'crear': 'crear',
            'eliminar': 'eliminar', 'ejecutar': 'ejecutar codigo',
            'calcular': 'hacer calculos', 'derivar': 'calcular derivadas',
            'integrar': 'calcular integrales', 'listar': 'listar archivos',
        }
        for palabra in texto_original.split():
            p = palabra.strip('¿?.,;:!').lower()
            if p in verbos:
                return verbos[p]
        return "eso"

    # ------------------------------------------------------------------
    # ESTADISTICAS — identico a v8.4 + version actualizada
    # ------------------------------------------------------------------

    def obtener_estadisticas(self) -> Dict:
        total = self.stats['total_generadas']
        return {
            'total_generadas':        total,
            'groq_usadas':            self.stats['groq_usadas'],
            'groq_bloqueadas':        self.stats['groq_bloqueadas'],
            'fallback_a_simbolico':   self.stats['fallback_a_simbolico'],
            'echo_correcciones':      self.stats['echo_correcciones'],
            'echo_bloqueos_reales':   self.stats['echo_bloqueos_reales'],
            'habilidades_ejecutadas': self.stats['habilidades_ejecutadas'],
            'habilidades_fallidas':   self.stats['habilidades_fallidas'],
            'interceptor_activado':   self.stats['interceptor_activado'],
            'tasa_groq':              self.stats['groq_usadas'] / total if total > 0 else 0.0,
            'emociones_detectadas':   self.stats['emociones_detectadas'],
            'tipos_decision':         self.stats['tipos_decision'],
            'shell_ejecutados':       self.stats['shell_ejecutados'],
            'shell_fallidos':         self.stats['shell_fallidos'],
        }

    def mostrar_estadisticas(self):
        stats = self.obtener_estadisticas()
        print("\n" + "=" * 60)
        print("ESTADISTICAS DEL GENERADOR v8.5")
        print("=" * 60)
        print(f"Total respuestas:         {stats['total_generadas']}")
        print(f"Con Groq:                 {stats['groq_usadas']}")
        print(f"Interceptor activado:     {stats['interceptor_activado']}")
        print(f"Habilidades ejecutadas:   {stats['habilidades_ejecutadas']}")
        print(f"Habilidades fallidas:     {stats['habilidades_fallidas']}")
        print(f"Shell ejecutados:         {stats['shell_ejecutados']}")
        print(f"Shell fallidos:           {stats['shell_fallidos']}")
        print("=" * 60)