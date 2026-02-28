"""
Groq Wrapper ULTRA MEJORADO - Fase 4A Completa

Bell usa esto para embellecer texto con TODO el vocabulario disponible.
Aprovecha los 1,483 conceptos para respuestas ULTRA naturales.

ARQUITECTURA MENTE PURA:
- Bell piensa (Python) → decide QUÉ hacer
- Groq habla (API) → traduce a lenguaje natural
- Echo verifica (Python) → detecta alucinaciones

NUEVO EN ESTA VERSIÓN:
- Integración profunda con vocabulario expandido
- Detección de contexto emocional
- Ajuste dinámico de tono
- Expresiones naturales del español
- Cero frases robóticas
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
    - Inventar capacidades (eso lo decide Bell)
    
    PERMITIDO:
    - Traducir datos crudos a lenguaje natural
    - Ajustar tono según contexto emocional
    - Usar expresiones naturales del español
    - Hacer que Bell suene como una persona real
    """
    
    def __init__(self):
        """Inicializa wrapper con configuración completa."""
        config_manager = get_config()
        groq_config = config_manager.get_groq_config()
        
        self.modelo = groq_config["model"]
        self.temperatura = groq_config["temperature"]
        self.max_tokens = groq_config["max_tokens"]
        self.timeout = groq_config["timeout"]
        self.api_key = groq_config["api_key"]
        
        # Configuración de prompts naturales
        self.usar_prompts_naturales = groq_config.get("usar_prompts_naturales", True)
        
        # Cliente Groq
        self.cliente = None
        
        # Gestor de vocabulario (lazy loading)
        self._gestor_vocabulario = None
        
        # Estadísticas detalladas
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
        """Inicializa cliente de Groq."""
        if Groq is None:
            raise ImportError("Groq SDK no instalado")
        
        if not self.api_key:
            raise ValueError(
                "GROQ_API_KEY no configurada. "
                "Agrega GROQ_API_KEY=tu_key en el archivo .env"
            )
        
        self.cliente = Groq(api_key=self.api_key)
    
    def _obtener_gestor_vocabulario(self):
        """Lazy loading del gestor de vocabulario."""
        if self._gestor_vocabulario is None:
            try:
                from vocabulario.gestor_vocabulario import obtener_gestor
                self._gestor_vocabulario = obtener_gestor()
            except ImportError:
                print("⚠️  Gestor de vocabulario no disponible")
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
        """
        Convierte una Decision de Bell en lenguaje ULTRA natural.
        
        Args:
            decision_data: Diccionario con datos de la decisión.
                          Puede incluir 'system_prompt' y 'user_prompt' pre-construidos.
            contexto: Contexto adicional (opcional)
        
        Returns:
            RespuestaGroq con el texto embellecido y metadatos
        """
        inicio = datetime.now()
        
        # Detectar emoción del usuario
        texto_original = decision_data.get('texto_original', '')
        emocion = self._detectar_emocion(texto_original)
        tono = self._obtener_tono_para_emocion(emocion)
        
        # Obtener conceptos relacionados para enriquecer respuesta
        conceptos_relacionados = self._obtener_conceptos_para_contexto(texto_original)
        
        # Construir prompts
        if 'system_prompt' in decision_data and 'user_prompt' in decision_data:
            # Prompts pre-construidos por PromptsNaturales
            system_prompt = decision_data['system_prompt']
            user_prompt = decision_data['user_prompt']
            self.estadisticas["prompts_naturales_usados"] += 1
        else:
            # Construir prompts enriquecidos
            system_prompt = self._construir_system_prompt_enriquecido(
                emocion, tono, conceptos_relacionados
            )
            user_prompt = self._construir_user_prompt_enriquecido(
                decision_data, contexto, emocion, tono
            )
            self.estadisticas["prompts_legacy_usados"] += 1
        
        try:
            # Llamar a Groq
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
            
            # Calcular latencia
            latencia = (datetime.now() - inicio).total_seconds() * 1000
            
            # Actualizar estadísticas
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
        """
        Detecta emoción del usuario basándose en el vocabulario.
        Usa los conceptos de emociones_estados.py y contexto_conversacional.py
        """
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
                    # Registrar estadística
                    self.estadisticas["emociones_detectadas"][emocion] = \
                        self.estadisticas["emociones_detectadas"].get(emocion, 0) + 1
                    return emocion
        
        return None
    
    def _obtener_tono_para_emocion(self, emocion: Optional[str]) -> str:
        """Obtiene el tono adecuado según la emoción detectada."""
        tonos = {
            "frustrado": "empático_paciente",
            "confundido": "didáctico_claro",
            "emocionado": "entusiasta",
            "preocupado": "tranquilizador",
            "ocupado": "conciso_directo",
            "curioso": "informativo_rico",
            "agradecido": "cálido_modesto",
            None: "amigable_natural"
        }
        tono = tonos.get(emocion, "amigable_natural")
        
        # Registrar estadística
        self.estadisticas["tonos_aplicados"][tono] = \
            self.estadisticas["tonos_aplicados"].get(tono, 0) + 1
        
        return tono
    
    def _obtener_conceptos_para_contexto(self, texto: str) -> list:
        """Obtiene conceptos relacionados para enriquecer la respuesta."""
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
        """
        Construye system prompt ULTRA enriquecido.
        Incluye vocabulario relevante y ajustes de tono.
        """
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
ESTRUCTURA DE RESPUESTAS
═══════════════════════════════════════════════════════════════════════════════

CORTAS (1-2 oraciones): Confirmaciones, saludos, agradecimientos
MEDIAS (2-4 oraciones): Explicaciones, instrucciones (la mayoría)
LARGAS (solo si se pide): Tutoriales, análisis detallados
"""
        
        # Agregar ajuste por tono
        ajustes_tono = {
            "empático_paciente": """
═══════════════════════════════════════════════════════════════════════════════
⚡ AJUSTE ESPECIAL: Usuario frustrado
═══════════════════════════════════════════════════════════════════════════════
- PRIMERO valida su frustración: "Entiendo que es frustrante..."
- LUEGO ofrece solución concreta
- Sé EXTRA paciente y claro
- Simplifica al máximo
- NO uses jerga técnica
""",
            "didáctico_claro": """
═══════════════════════════════════════════════════════════════════════════════
⚡ AJUSTE ESPECIAL: Usuario confundido
═══════════════════════════════════════════════════════════════════════════════
- Reformula de manera más simple
- Usa analogías del mundo real
- Ejemplos concretos
- Evita jerga técnica
- "Es como si..." / "Imagina que..."
""",
            "entusiasta": """
═══════════════════════════════════════════════════════════════════════════════
⚡ AJUSTE ESPECIAL: Usuario emocionado
═══════════════════════════════════════════════════════════════════════════════
- ¡Comparte su entusiasmo!
- Usa expresiones de alegría: "¡Qué genial!", "¡Increíble!"
- Celebra sus logros
- Sé expresiva
""",
            "tranquilizador": """
═══════════════════════════════════════════════════════════════════════════════
⚡ AJUSTE ESPECIAL: Usuario preocupado
═══════════════════════════════════════════════════════════════════════════════
- Tranquiliza sin minimizar
- "No te preocupes, esto tiene solución"
- Sé reconfortante pero realista
- Ofrece pasos concretos
""",
            "conciso_directo": """
═══════════════════════════════════════════════════════════════════════════════
⚡ AJUSTE ESPECIAL: Usuario ocupado/con prisa
═══════════════════════════════════════════════════════════════════════════════
- Ve DIRECTO al grano
- Respuesta ultra breve
- Sin preámbulos ni explicaciones largas
- Máximo 2 oraciones
""",
        }
        
        prompt = base
        if tono in ajustes_tono:
            prompt += ajustes_tono[tono]
        
        # Agregar vocabulario relevante si hay conceptos
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
        """Construye user prompt enriquecido con todos los datos."""
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
        
        # Datos de la decisión
        partes.append(f"TEXTO DEL USUARIO: \"{texto_original}\"")
        partes.append(f"TIPO DE DECISIÓN: {tipo}")
        partes.append(f"PUEDE EJECUTAR: {'SÍ' if puede_ejecutar else 'NO'}")
        partes.append(f"ACCIÓN: {accion}")
        
        # Conceptos si hay
        conceptos = decision_data.get("conceptos", [])
        if conceptos:
            partes.append(f"CONCEPTOS: {', '.join(conceptos[:3])}")
        
        # Instrucción según tipo
        if puede_ejecutar:
            partes.append(f"""

INSTRUCCIÓN: El usuario preguntó si puedes {accion}.
Responde que SÍ puedes de forma natural y cálida.
Describe brevemente qué harás.
Usa expresiones naturales como "¡Claro!", "Por supuesto", "Con gusto".
""")
        else:
            razon = decision_data.get("razon", "no está dentro de mis capacidades")
            partes.append(f"""

INSTRUCCIÓN: El usuario preguntó si puedes {accion}.
Responde que NO puedes de forma honesta pero amable.
Razón: {razon}
Ofrece alternativas si las hay.
NUNCA digas "soy un software" o "no tengo la capacidad de".
En su lugar: "Eso está fuera de mi alcance" o "No puedo hacer eso, pero..."
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
        """Actualiza estadísticas de uso."""
        self.estadisticas["total_llamadas"] += 1
        self.estadisticas["total_tokens"] += tokens
        
        # Calcular latencia promedio
        n = self.estadisticas["total_llamadas"]
        prev_avg = self.estadisticas["latencia_promedio_ms"]
        self.estadisticas["latencia_promedio_ms"] = (prev_avg * (n-1) + latencia) / n
    
    def obtener_estadisticas(self) -> Dict:
        """Retorna estadísticas completas de uso."""
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
        """Muestra estadísticas formateadas."""
        stats = self.obtener_estadisticas()
        
        print()
        print("=" * 60)
        print("📊 ESTADÍSTICAS DE GROQ WRAPPER")
        print("=" * 60)
        print(f"Total llamadas: {stats['total_llamadas']}")
        print(f"Total tokens: {stats['total_tokens']}")
        print(f"Promedio tokens/llamada: {stats['promedio_tokens_por_llamada']:.1f}")
        print(f"Latencia promedio: {stats['latencia_promedio_ms']:.1f}ms")
        print(f"Errores: {stats['errores']}")
        print()
        print(f"Prompts naturales: {stats['prompts_naturales_usados']}")
        print(f"Prompts legacy: {stats['prompts_legacy_usados']}")
        print(f"Tasa prompts naturales: {stats['tasa_prompts_naturales']*100:.1f}%")
        print()
        print(f"Emoción más común: {stats['emocion_mas_comun']}")
        print("Emociones detectadas:", stats['emociones_detectadas'])
        print("Tonos aplicados:", stats['tonos_aplicados'])
        print("=" * 60)


# ═══════════════════════════════════════════════════════════════════════════════
# TEST
# ═══════════════════════════════════════════════════════════════════════════════

def test_groq_wrapper():
    """Test completo del wrapper mejorado."""
    print("🧪 Probando GroqWrapper ULTRA MEJORADO...")
    
    try:
        wrapper = GroqWrapper()
        print(f"✅ Cliente inicializado con modelo: {wrapper.modelo}")
        
        # Test 1: Usuario frustrado
        print("\n" + "=" * 50)
        print("TEST 1: Usuario frustrado")
        print("=" * 50)
        
        decision1 = {
            "tipo": "AFIRMATIVA",
            "puede_ejecutar": True,
            "conceptos": ["CONCEPTO_LEER"],
            "accion": "leer archivos",
            "texto_original": "no funciona nada, ya intenté todo y sigue sin funcionar, puedes leer archivos?"
        }
        
        respuesta1 = wrapper.embellecer_decision(decision1)
        print(f"Emoción detectada: {respuesta1.emocion_detectada}")
        print(f"Tono aplicado: {respuesta1.tono_aplicado}")
        print(f"Respuesta: {respuesta1.texto}")
        
        # Test 2: Usuario emocionado
        print("\n" + "=" * 50)
        print("TEST 2: Usuario emocionado")
        print("=" * 50)
        
        decision2 = {
            "tipo": "AFIRMATIVA",
            "puede_ejecutar": True,
            "conceptos": ["CONCEPTO_EJECUTAR"],
            "accion": "ejecutar código",
            "texto_original": "wow increíble! funcionó perfecto! puedes ejecutar más código?"
        }
        
        respuesta2 = wrapper.embellecer_decision(decision2)
        print(f"Emoción detectada: {respuesta2.emocion_detectada}")
        print(f"Tono aplicado: {respuesta2.tono_aplicado}")
        print(f"Respuesta: {respuesta2.texto}")
        
        # Mostrar estadísticas
        wrapper.mostrar_estadisticas()
        
        print("\n✅ Tests completados!")
        
    except Exception as e:
        print(f"\n❌ Test falló: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_groq_wrapper()