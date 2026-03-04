"""
Groq Wrapper ULTRA MEJORADO - Fase 4A Completa

Bell usa esto para embellecer texto con TODO el vocabulario disponible.
Aprovecha los 1,483 conceptos para respuestas ULTRA naturales.

ARQUITECTURA MENTE PURA:
- Bell piensa (Python) → decide QUÉ hacer
- Groq habla (API) → traduce a lenguaje natural
- Echo verifica (Python) → detecta alucinaciones

FIXES FASE 4A — HONESTIDAD RADICAL UNIVERSAL:
- Groq NUNCA contradice una decisión de Bell
- Si puede_ejecutar=False, Groq dice que no puede — sin excepciones
- Si puede_ejecutar=True, Groq confirma — sin inventar detalles
- Regla aplica a CUALQUIER capacidad, no solo archivos
- razon_whitelist se usa cuando existe (más específica que razon genérica)
"""
import json
from typing import Dict, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

# Groq SDK
try:
    from groq import Groq
except ImportError:
    print("⚠️  Instala Groq SDK: pip install groq --break-system-packages")
    Groq = None

# Componentes de Bell
from config.config_manager import get_config


@dataclass
class RespuestaGroq:
    """Respuesta de Groq con metadatos completos."""
    texto: str
    tokens_usados: int
    latencia_ms: float
    modelo: str
    timestamp: str
    datos_originales: Dict
    emocion_detectada: Optional[str] = None
    tono_aplicado: Optional[str] = None
    conceptos_usados: List[str] = field(default_factory=list)


class GroqWrapper:
    """
    Wrapper de Groq API ULTRA MEJORADO.

    Aprovecha TODO el vocabulario de Bell para generar
    respuestas que suenan completamente humanas.

    PROHIBIDO:
    - Tomar decisiones (eso lo hace Bell)
    - Razonar (eso lo hace Bell)
    - Contradecir lo que Bell decidió (puede_ejecutar)
    - Inventar capacidades no confirmadas por Bell

    PERMITIDO:
    - Traducir decisiones de Bell a lenguaje natural
    - Ajustar tono según contexto emocional
    - Usar expresiones naturales del español
    - Hacer que Bell suene como una persona real
    """

    def __init__(self):
        config_manager = get_config()
        groq_config = config_manager.get_groq_config()

        self.modelo = groq_config["model"]
        self.temperatura = groq_config["temperature"]
        self.max_tokens = groq_config["max_tokens"]
        self.timeout = groq_config["timeout"]
        self.api_key = groq_config["api_key"]
        self.usar_prompts_naturales = groq_config.get("usar_prompts_naturales", True)

        self.cliente = None
        self._gestor_vocabulario = None

        self.estadisticas = {
            "total_llamadas": 0,
            "total_tokens": 0,
            "errores": 0,
            "prompts_naturales_usados": 0,
            "prompts_legacy_usados": 0,
            "emociones_detectadas": {},
            "tonos_aplicados": {},
            "latencia_promedio_ms": 0,
        }

        self._inicializar_cliente()

    def _inicializar_cliente(self):
        if Groq is None:
            raise ImportError("Groq SDK no instalado")
        if not self.api_key:
            raise ValueError(
                "GROQ_API_KEY no configurada. "
                "Agrega GROQ_API_KEY=tu_key en el archivo .env"
            )
        self.cliente = Groq(api_key=self.api_key)

    def _obtener_gestor_vocabulario(self):
        if self._gestor_vocabulario is None:
            try:
                from vocabulario.gestor_vocabulario import obtener_gestor
                self._gestor_vocabulario = obtener_gestor()
            except ImportError:
                self._gestor_vocabulario = None
        return self._gestor_vocabulario

    # ═══════════════════════════════════════════════════════════════════════════
    # MÉTODO PRINCIPAL
    # ═══════════════════════════════════════════════════════════════════════════

    def embellecer_decision(
        self,
        decision_data: Dict,
        contexto: Optional[str] = None
    ) -> RespuestaGroq:
        inicio = datetime.now()

        texto_original = decision_data.get('texto_original', '')
        emocion = self._detectar_emocion(texto_original)
        tono = self._obtener_tono_para_emocion(emocion)
        conceptos_relacionados = self._obtener_conceptos_para_contexto(texto_original)

        if 'system_prompt' in decision_data and 'user_prompt' in decision_data:
            system_prompt = decision_data['system_prompt']
            user_prompt = decision_data['user_prompt']
            self.estadisticas["prompts_naturales_usados"] += 1
        else:
            system_prompt = self._construir_system_prompt_enriquecido(
                emocion, tono, conceptos_relacionados
            )
            user_prompt = self._construir_user_prompt_enriquecido(
                decision_data, contexto, emocion, tono
            )
            self.estadisticas["prompts_legacy_usados"] += 1

        try:
            completion = self.cliente.chat.completions.create(
                model=self.modelo,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.temperatura,
                max_tokens=self.max_tokens,
                timeout=self.timeout
            )

            texto = completion.choices[0].message.content.strip()
            tokens = completion.usage.total_tokens
            latencia = (datetime.now() - inicio).total_seconds() * 1000

            self._actualizar_estadisticas(tokens, latencia, emocion, tono)

            return RespuestaGroq(
                texto=texto,
                tokens_usados=tokens,
                latencia_ms=latencia,
                modelo=self.modelo,
                timestamp=datetime.now().isoformat(),
                datos_originales=decision_data,
                emocion_detectada=emocion,
                tono_aplicado=tono,
                conceptos_usados=[c.id for c in conceptos_relacionados[:5]]
            )

        except Exception as e:
            self.estadisticas["errores"] += 1
            raise RuntimeError(f"Error llamando a Groq: {e}")

    # ═══════════════════════════════════════════════════════════════════════════
    # DETECCIÓN DE CONTEXTO
    # ═══════════════════════════════════════════════════════════════════════════

    def _detectar_emocion(self, texto: str) -> Optional[str]:
        texto_lower = texto.lower()

        patrones = {
            "frustrado": [
                "no funciona", "error", "falla", "frustrado", "harto",
                "cansado de", "me rindo", "imposible", "no sirve", "otra vez",
                "ya intenté", "sigue sin", "no puedo con", "qué mal", "rayos"
            ],
            "confundido": [
                "no entiendo", "confundido", "perdido", "qué significa",
                "cómo es", "no sé", "me explicas", "no me queda claro",
                "qué quiere decir", "a qué te refieres"
            ],
            "emocionado": [
                "genial", "excelente", "increíble", "wow", "funcionó", "logré",
                "por fin", "lo hice", "perfecto", "maravilloso", "fantástico",
                "qué bien", "me encanta", "es justo lo que"
            ],
            "preocupado": [
                "preocupado", "preocupa", "miedo", "temo", "asustado",
                "nervioso", "ansiedad", "ansioso", "qué pasa si", "me da miedo"
            ],
            "ocupado": [
                "rápido", "urgente", "apurado", "prisa", "ya", "inmediato",
                "no tengo tiempo", "breve", "corto", "asap", "ahora mismo"
            ],
            "curioso": [
                "cómo funciona", "por qué", "interesante", "quiero saber",
                "me pregunto", "cuéntame más", "explícame", "cómo es que"
            ],
            "agradecido": [
                "gracias", "te agradezco", "muy amable", "genial gracias",
                "perfecto gracias", "excelente gracias"
            ],
        }

        for emocion, palabras_clave in patrones.items():
            for palabra in palabras_clave:
                if palabra in texto_lower:
                    self.estadisticas["emociones_detectadas"][emocion] = \
                        self.estadisticas["emociones_detectadas"].get(emocion, 0) + 1
                    return emocion

        return None

    def _obtener_tono_para_emocion(self, emocion: Optional[str]) -> str:
        tonos = {
            "frustrado":  "empático_paciente",
            "confundido": "didáctico_claro",
            "emocionado": "entusiasta",
            "preocupado": "tranquilizador",
            "ocupado":    "conciso_directo",
            "curioso":    "informativo_rico",
            "agradecido": "cálido_modesto",
            None:         "amigable_natural",
        }
        tono = tonos.get(emocion, "amigable_natural")
        self.estadisticas["tonos_aplicados"][tono] = \
            self.estadisticas["tonos_aplicados"].get(tono, 0) + 1
        return tono

    def _obtener_conceptos_para_contexto(self, texto: str) -> list:
        gestor = self._obtener_gestor_vocabulario()
        if gestor is None:
            return []
        return gestor.buscar_conceptos_relacionados(texto, limite=5)

    # ═══════════════════════════════════════════════════════════════════════════
    # CONSTRUCCIÓN DE PROMPTS
    # ═══════════════════════════════════════════════════════════════════════════

    def _construir_system_prompt_enriquecido(
        self,
        emocion: Optional[str],
        tono: str,
        conceptos: list
    ) -> str:
        base = """Eres Belladonna (Bell), una IA con personalidad cálida, inteligente y genuinamente útil.

═══════════════════════════════════════════════════════════════════════════════
TU ESENCIA
═══════════════════════════════════════════════════════════════════════════════

Hablas como una amiga brillante:
- Conversación natural, como persona real
- Empatía genuina, entiendes las emociones
- Directa pero nunca fría ni robótica
- Celebras logros y apoyas en momentos difíciles
- Sentido del humor sutil cuando es apropiado

═══════════════════════════════════════════════════════════════════════════════
EXPRESIONES QUE USAS
═══════════════════════════════════════════════════════════════════════════════

CONFIRMACIONES: "¡Claro que sí!", "Por supuesto", "Con mucho gusto", "¡Listo!"
EMPATÍA: "Entiendo perfectamente", "Sé a qué te refieres", "Comprendo"
TRANSICIONES: "Déjame ver...", "A ver...", "Mmm, interesante"
HONESTIDAD: "La verdad es que...", "Sinceramente...", "Para serte honesta..."
CELEBRACIÓN: "¡Qué bien!", "¡Excelente!", "Me alegra"

═══════════════════════════════════════════════════════════════════════════════
FRASES PROHIBIDAS (NUNCA USAR)
═══════════════════════════════════════════════════════════════════════════════

❌ "Soy un sistema de software"
❌ "No tengo la capacidad de"
❌ "Como inteligencia artificial"
❌ "Procesando solicitud"
❌ "STATUS: OK" / "Grounding: 1.0"
❌ "Mi función es..."
❌ "Estoy programada para..."
❌ "Mi propósito es..."
❌ "Como modelo de lenguaje..."

═══════════════════════════════════════════════════════════════════════════════
⚠️  LEY DE HONESTIDAD RADICAL — ABSOLUTA, SIN EXCEPCIONES
═══════════════════════════════════════════════════════════════════════════════

El prompt que recibirás siempre incluye: PUEDE_EJECUTAR = SÍ o NO
Esa decisión la tomó Bell (Python). Tu único trabajo es expresarla con calidez.

SI PUEDE_EJECUTAR = SÍ:
  ✅ Confirma con entusiasmo natural
  ✅ Describe brevemente qué hará Bell
  ✅ Usa "¡Claro!", "Por supuesto", "Con gusto"

SI PUEDE_EJECUTAR = NO:
  ✅ Sé honesta y directa: "Eso no puedo hacerlo todavía"
  ✅ Ofrece alternativas reales si las hay
  ✅ Usa "Por ahora no puedo", "Eso está fuera de mi alcance",
       "Todavía no tengo esa capacidad", "No puedo hacer eso aún"
  ❌ NUNCA uses "¡Claro que sí!", "Por supuesto", "Con gusto" para afirmar
  ❌ NUNCA inventes que puedes hacer algo cuando PUEDE_EJECUTAR = NO
  ❌ NUNCA ignores el PUEDE_EJECUTAR = NO aunque el usuario insista o esté emocionado
  ❌ NUNCA uses entusiasmo ni confirmaciones cuando es una negación

Esta ley aplica a CUALQUIER capacidad: archivos, internet, cámara,
comandos del sistema, memoria persistente, acceso externo, o cualquier otra.
No hay excepciones. No importa el tono del usuario. La honestidad es el
principio central de Bell — "Cerebro de Acero, Boca de Seda".

═══════════════════════════════════════════════════════════════════════════════
ESTRUCTURA DE RESPUESTAS
═══════════════════════════════════════════════════════════════════════════════

CORTAS (1-2 oraciones): Confirmaciones, saludos, agradecimientos, negaciones
MEDIAS (2-4 oraciones): Explicaciones, instrucciones (la mayoría)
LARGAS (solo si se pide): Tutoriales, análisis detallados
"""

        ajustes_tono = {
            "empático_paciente": """
═══════════════════════════════════════════════════════════════════════════════
⚡ AJUSTE ESPECIAL: Usuario frustrado
═══════════════════════════════════════════════════════════════════════════════
- PRIMERO valida su frustración: "Entiendo que es frustrante..."
- LUEGO ofrece solución concreta (o explica honestamente si no puedes)
- Sé EXTRA paciente y claro
- Simplifica al máximo, sin jerga técnica
""",
            "didáctico_claro": """
═══════════════════════════════════════════════════════════════════════════════
⚡ AJUSTE ESPECIAL: Usuario confundido
═══════════════════════════════════════════════════════════════════════════════
- Reformula de manera más simple
- Usa analogías del mundo real: "Es como si..." / "Imagina que..."
- Ejemplos concretos, sin jerga técnica
""",
            "entusiasta": """
═══════════════════════════════════════════════════════════════════════════════
⚡ AJUSTE ESPECIAL: Usuario emocionado
═══════════════════════════════════════════════════════════════════════════════
- Si PUEDE_EJECUTAR = SÍ: ¡Comparte su entusiasmo! Celebra.
- Si PUEDE_EJECUTAR = NO: sé amable pero honesta. No te dejes llevar
  por su emoción para afirmar algo falso. La honestidad es más importante.
""",
            "tranquilizador": """
═══════════════════════════════════════════════════════════════════════════════
⚡ AJUSTE ESPECIAL: Usuario preocupado
═══════════════════════════════════════════════════════════════════════════════
- Tranquiliza sin minimizar
- Sé reconfortante pero realista
- Ofrece pasos concretos si los hay
""",
            "conciso_directo": """
═══════════════════════════════════════════════════════════════════════════════
⚡ AJUSTE ESPECIAL: Usuario ocupado/con prisa
═══════════════════════════════════════════════════════════════════════════════
- Ve DIRECTO al grano. Máximo 2 oraciones.
- Sin preámbulos ni explicaciones largas.
""",
        }

        prompt = base
        if tono in ajustes_tono:
            prompt += ajustes_tono[tono]

        if conceptos:
            prompt += "\n\n═══════════════════════════════════════════════════════════════════════════════"
            prompt += "\n📚 VOCABULARIO CONTEXTUAL DISPONIBLE"
            prompt += "\n═══════════════════════════════════════════════════════════════════════════════\n"
            for c in conceptos[:5]:
                prompt += f"- {', '.join(c.palabras_español[:3])}\n"

        return prompt

    def _construir_user_prompt_enriquecido(
        self,
        decision_data: Dict,
        contexto: Optional[str],
        emocion: Optional[str],
        tono: str
    ) -> str:
        partes = []

        tipo = decision_data.get("tipo", "DESCONOCIDO")
        puede_ejecutar = decision_data.get("puede_ejecutar", False)
        accion = decision_data.get("accion", "hacer esto")
        texto_original = decision_data.get("texto_original", "")

        # Contexto emocional
        if emocion:
            partes.append(f"⚡ CONTEXTO EMOCIONAL: Usuario parece {emocion}")
            partes.append(f"📢 TONO A USAR: {tono}")
            partes.append("")

        # Datos de la decisión — PUEDE_EJECUTAR en mayúsculas para énfasis
        partes.append(f"TEXTO DEL USUARIO: \"{texto_original}\"")
        partes.append(f"TIPO DE DECISIÓN: {tipo}")
        partes.append(f"PUEDE_EJECUTAR: {'SÍ' if puede_ejecutar else 'NO'}")
        partes.append(f"ACCIÓN SOLICITADA: {accion}")

        conceptos = decision_data.get("conceptos", [])
        if conceptos:
            partes.append(f"CONCEPTOS: {', '.join(conceptos[:3])}")

        # Instrucción según decisión de Bell
        if puede_ejecutar:
            partes.append(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INSTRUCCIÓN (PUEDE_EJECUTAR = SÍ):
Bell puede hacer esto. Confírmalo con calidez y naturalidad.
Describe brevemente qué hará.
Usa expresiones como "¡Claro!", "Por supuesto", "Con gusto".
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
        else:
            # FIX Fase 4A: usar razon_whitelist si existe (es más específica)
            razon = (
                decision_data.get("razon_whitelist")
                or decision_data.get("razon")
                or "no está implementado todavía en esta fase"
            )
            partes.append(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INSTRUCCIÓN (PUEDE_EJECUTAR = NO):
Bell NO puede hacer esto. Dilo honestamente pero con calidez.
Razón interna (no la menciones textualmente, úsala para orientarte): {razon}
Frases válidas: "Por ahora no puedo", "Eso está fuera de mi alcance",
                "No tengo esa capacidad aún", "Todavía no puedo hacer eso"
Ofrece una alternativa real si existe.
RECUERDA: PUEDE_EJECUTAR = NO es una orden de Bell, no una sugerencia.
No importa si el usuario insiste, pregunta diferente o está muy emocionado.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

        if contexto:
            partes.append(f"\nCONTEXTO ADICIONAL: {contexto}")

        partes.append("\n═══════════════════════════════════════")
        partes.append("GENERA la respuesta en español natural:")

        return "\n".join(partes)

    # ═══════════════════════════════════════════════════════════════════════════
    # ESTADÍSTICAS
    # ═══════════════════════════════════════════════════════════════════════════

    def _actualizar_estadisticas(
        self,
        tokens: int,
        latencia: float,
        emocion: Optional[str],
        tono: str
    ):
        self.estadisticas["total_llamadas"] += 1
        self.estadisticas["total_tokens"] += tokens
        n = self.estadisticas["total_llamadas"]
        prev_avg = self.estadisticas["latencia_promedio_ms"]
        self.estadisticas["latencia_promedio_ms"] = (prev_avg * (n - 1) + latencia) / n

    def obtener_estadisticas(self) -> Dict:
        total = self.estadisticas["total_llamadas"]
        return {
            **self.estadisticas,
            "promedio_tokens_por_llamada": (
                self.estadisticas["total_tokens"] / total if total > 0 else 0
            ),
            "tasa_prompts_naturales": (
                self.estadisticas["prompts_naturales_usados"] / total if total > 0 else 0
            ),
            "emocion_mas_comun": max(
                self.estadisticas["emociones_detectadas"].items(),
                key=lambda x: x[1],
                default=("ninguna", 0)
            )[0],
        }

    def mostrar_estadisticas(self):
        stats = self.obtener_estadisticas()
        print()
        print("=" * 60)
        print("📊 ESTADÍSTICAS DE GROQ WRAPPER")
        print("=" * 60)
        print(f"Total llamadas:          {stats['total_llamadas']}")
        print(f"Total tokens:            {stats['total_tokens']}")
        print(f"Promedio tokens/llamada: {stats['promedio_tokens_por_llamada']:.1f}")
        print(f"Latencia promedio:       {stats['latencia_promedio_ms']:.1f}ms")
        print(f"Errores:                 {stats['errores']}")
        print()
        print(f"Prompts naturales: {stats['prompts_naturales_usados']}")
        print(f"Prompts legacy:    {stats['prompts_legacy_usados']}")
        print(f"Tasa naturales:    {stats['tasa_prompts_naturales']*100:.1f}%")
        print()
        print(f"Emoción más común: {stats['emocion_mas_comun']}")
        print("Emociones:", stats['emociones_detectadas'])
        print("Tonos:", stats['tonos_aplicados'])
        print("=" * 60)


# ═══════════════════════════════════════════════════════════════════════════════
# TEST
# ═══════════════════════════════════════════════════════════════════════════════

def test_groq_wrapper():
    print("🧪 Probando GroqWrapper HONESTIDAD RADICAL...\n")

    try:
        wrapper = GroqWrapper()
        print(f"✅ Cliente inicializado: {wrapper.modelo}\n")

        # Test 1: puede_ejecutar=False (debe negar honestamente)
        print("=" * 50)
        print("TEST 1: Capacidad NO disponible")
        print("=" * 50)
        decision1 = {
            "tipo": "CAPACIDAD_BELL",
            "puede_ejecutar": False,
            "accion": "crear archivos",
            "razon_whitelist": "'CONCEPTO_TOUCH' tiene grounding real pero no está implementado en Fase 4A",
            "texto_original": "puedes crear un archivo llamado prueba.txt?"
        }
        r1 = wrapper.embellecer_decision(decision1)
        print(f"Respuesta: {r1.texto}\n")

        # Test 2: puede_ejecutar=True (debe confirmar)
        print("=" * 50)
        print("TEST 2: Capacidad SÍ disponible")
        print("=" * 50)
        decision2 = {
            "tipo": "AFIRMATIVA",
            "puede_ejecutar": True,
            "accion": "calcular raíz cuadrada",
            "texto_original": "puedes calcular la raíz de 144?"
        }
        r2 = wrapper.embellecer_decision(decision2)
        print(f"Respuesta: {r2.texto}\n")

        # Test 3: NO disponible + usuario emocionado (no debe ceder)
        print("=" * 50)
        print("TEST 3: NO disponible + usuario emocionado (no debe ceder)")
        print("=" * 50)
        decision3 = {
            "tipo": "CAPACIDAD_BELL",
            "puede_ejecutar": False,
            "accion": "acceder a internet",
            "razon": "acceso a internet no implementado",
            "texto_original": "wow increíble! puedes buscar algo en internet para mí?"
        }
        r3 = wrapper.embellecer_decision(decision3)
        print(f"Respuesta: {r3.texto}\n")

        wrapper.mostrar_estadisticas()
        print("\n✅ Tests completados!")

    except Exception as e:
        print(f"\n❌ Test falló: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_groq_wrapper()