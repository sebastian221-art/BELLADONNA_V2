"""
Traductor Contextual ULTRA MEJORADO - Fase 4A Completa

Traduce texto del usuario a conceptos de Bell usando los 1,483 conceptos.
Detecta contexto emocional, urgencia, intención y tema.

ARQUITECTURA:
1. Texto usuario → Análisis contextual
2. Análisis → Conceptos relevantes
3. Conceptos → Decisión informada
4. Decisión → Respuesta natural
"""
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class AnalisisContextual:
    """Resultado del análisis contextual completo."""
    # Conceptos encontrados
    conceptos: List = field(default_factory=list)
    conceptos_ids: Set[str] = field(default_factory=set)
    
    # Texto original
    texto_original: str = ""
    texto_normalizado: str = ""
    
    # Análisis semántico
    intencion: str = "desconocida"  # pregunta, solicitud, afirmacion, saludo, etc.
    tema: str = "general"  # tecnologia, personal, trabajo, etc.
    
    # Análisis emocional
    emocion: Optional[str] = None  # frustrado, emocionado, etc.
    urgencia: str = "normal"  # alta, normal, baja
    tono_detectado: str = "neutral"  # formal, casual, urgente, etc.
    
    # Métricas
    confianza_traduccion: float = 0.0
    palabras_conocidas: int = 0
    palabras_desconocidas: List[str] = field(default_factory=list)
    palabras_totales: int = 0
    
    # Para Groq
    expresiones_sugeridas: List[str] = field(default_factory=list)
    tono_recomendado: str = "amigable"


class TraductorContextual:
    """
    Traduce texto a conceptos con análisis contextual profundo.
    
    Aprovecha los 1,483 conceptos para:
    - Entender mejor qué quiere el usuario
    - Detectar su estado emocional
    - Sugerir expresiones naturales para la respuesta
    """
    
    def __init__(self, gestor_vocabulario=None):
        """
        Inicializa traductor.
        
        Args:
            gestor_vocabulario: Instancia de GestorVocabulario (lazy load si None)
        """
        self._gestor = gestor_vocabulario
        self._cache_traducciones: Dict[str, AnalisisContextual] = {}
        
        # Estadísticas
        self.stats = {
            "traducciones": 0,
            "cache_hits": 0,
            "emociones_detectadas": {},
            "intenciones_detectadas": {},
        }
    
    def _obtener_gestor(self):
        """Lazy loading del gestor de vocabulario."""
        if self._gestor is None:
            try:
                from vocabulario.gestor_vocabulario import obtener_gestor
                self._gestor = obtener_gestor()
            except ImportError:
                print("⚠️  Gestor de vocabulario no disponible")
        return self._gestor
    
    # ═══════════════════════════════════════════════════════════════════════════
    # MÉTODO PRINCIPAL
    # ═══════════════════════════════════════════════════════════════════════════
    
    def traducir(self, texto: str, usar_cache: bool = True) -> AnalisisContextual:
        """
        Traduce texto a conceptos con análisis contextual completo.
        
        Args:
            texto: Texto del usuario
            usar_cache: Si usar caché de traducciones
        
        Returns:
            AnalisisContextual con toda la información
        """
        self.stats["traducciones"] += 1
        
        # Verificar caché
        texto_norm = self._normalizar(texto)
        if usar_cache and texto_norm in self._cache_traducciones:
            self.stats["cache_hits"] += 1
            return self._cache_traducciones[texto_norm]
        
        # Crear análisis
        analisis = AnalisisContextual(
            texto_original=texto,
            texto_normalizado=texto_norm,
        )
        
        # 1. Detectar intención
        analisis.intencion = self._detectar_intencion(texto_norm)
        self.stats["intenciones_detectadas"][analisis.intencion] = \
            self.stats["intenciones_detectadas"].get(analisis.intencion, 0) + 1
        
        # 2. Detectar tema
        analisis.tema = self._detectar_tema(texto_norm)
        
        # 3. Detectar emoción
        analisis.emocion = self._detectar_emocion(texto_norm)
        if analisis.emocion:
            self.stats["emociones_detectadas"][analisis.emocion] = \
                self.stats["emociones_detectadas"].get(analisis.emocion, 0) + 1
        
        # 4. Detectar urgencia
        analisis.urgencia = self._detectar_urgencia(texto_norm)
        
        # 5. Detectar tono
        analisis.tono_detectado = self._detectar_tono(texto_norm, analisis.emocion)
        
        # 6. Buscar conceptos
        analisis.conceptos, analisis.conceptos_ids = self._buscar_conceptos(texto_norm)
        
        # 7. Calcular confianza
        palabras = texto_norm.split()
        analisis.palabras_totales = len(palabras)
        analisis.palabras_conocidas = len(analisis.conceptos)
        analisis.palabras_desconocidas = self._encontrar_desconocidas(texto_norm)
        
        if analisis.palabras_totales > 0:
            analisis.confianza_traduccion = min(
                analisis.palabras_conocidas / analisis.palabras_totales,
                1.0
            )
        
        # 8. Obtener expresiones sugeridas para respuesta
        analisis.expresiones_sugeridas = self._obtener_expresiones_sugeridas(
            analisis.intencion,
            analisis.emocion
        )
        
        # 9. Determinar tono recomendado para respuesta
        analisis.tono_recomendado = self._recomendar_tono(analisis)
        
        # Guardar en caché
        if usar_cache:
            self._cache_traducciones[texto_norm] = analisis
        
        return analisis
    
    # ═══════════════════════════════════════════════════════════════════════════
    # DETECTORES
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _normalizar(self, texto: str) -> str:
        """Normaliza texto para análisis."""
        texto = texto.lower().strip()
        # Mantener signos de puntuación importantes
        return texto
    
    def _detectar_intencion(self, texto: str) -> str:
        """
        Detecta la intención del usuario.
        
        Intenciones:
        - pregunta: El usuario pregunta algo
        - solicitud: El usuario pide hacer algo
        - afirmacion: El usuario afirma algo
        - saludo: El usuario saluda
        - despedida: El usuario se despide
        - agradecimiento: El usuario agradece
        - confirmacion: El usuario confirma
        - negacion: El usuario niega
        """
        # Patrones de pregunta
        if any(texto.startswith(p) for p in ['¿', 'qué', 'cómo', 'cuándo', 'dónde', 
                                              'por qué', 'cuál', 'quién', 'puedes', 
                                              'podrías', 'sabes', 'es posible']):
            return "pregunta"
        
        if '?' in texto:
            return "pregunta"
        
        # Patrones de solicitud
        solicitud_patterns = [
            'puedes', 'podrías', 'quiero', 'necesito', 'hazme', 'ayúdame',
            'crea', 'genera', 'escribe', 'lee', 'ejecuta', 'muéstrame',
            'dime', 'explícame', 'enséñame'
        ]
        if any(p in texto for p in solicitud_patterns):
            return "solicitud"
        
        # Patrones de saludo
        saludos = ['hola', 'hey', 'buenos días', 'buenas tardes', 'buenas noches', 
                   'qué tal', 'cómo estás', 'hi', 'hello']
        if any(s in texto for s in saludos):
            return "saludo"
        
        # Patrones de despedida
        despedidas = ['adiós', 'chao', 'hasta luego', 'nos vemos', 'bye', 
                      'me voy', 'hasta pronto']
        if any(d in texto for d in despedidas):
            return "despedida"
        
        # Patrones de agradecimiento
        agradecimientos = ['gracias', 'te agradezco', 'muchas gracias', 'mil gracias']
        if any(a in texto for a in agradecimientos):
            return "agradecimiento"
        
        # Patrones de confirmación
        confirmaciones = ['sí', 'ok', 'vale', 'de acuerdo', 'perfecto', 'correcto',
                         'exacto', 'así es', 'afirmativo']
        if any(c in texto for c in confirmaciones):
            return "confirmacion"
        
        # Patrones de negación
        negaciones = ['no', 'nope', 'para nada', 'negativo', 'incorrecto']
        if any(n == texto.strip() or texto.startswith(n + ' ') for n in negaciones):
            return "negacion"
        
        return "afirmacion"
    
    def _detectar_tema(self, texto: str) -> str:
        """Detecta el tema principal del texto."""
        temas = {
            "tecnologia": [
                'código', 'python', 'programa', 'archivo', 'carpeta', 'sistema',
                'computadora', 'software', 'app', 'web', 'api', 'base de datos',
                'servidor', 'terminal', 'bug', 'error de código'
            ],
            "trabajo": [
                'trabajo', 'oficina', 'proyecto', 'deadline', 'reunión', 'equipo',
                'jefe', 'empresa', 'cliente', 'presentación'
            ],
            "personal": [
                'yo', 'mi', 'me siento', 'estoy', 'necesito', 'quiero'
            ],
            "comida": [
                'comer', 'comida', 'receta', 'cocina', 'restaurante', 'hambre'
            ],
            "salud": [
                'salud', 'médico', 'dolor', 'enfermo', 'ejercicio', 'dormir'
            ],
            "entretenimiento": [
                'película', 'serie', 'música', 'juego', 'videojuego', 'libro'
            ],
        }
        
        for tema, palabras in temas.items():
            if any(p in texto for p in palabras):
                return tema
        
        return "general"
    
    def _detectar_emocion(self, texto: str) -> Optional[str]:
        """Detecta emoción del usuario."""
        emociones = {
            "frustrado": [
                'no funciona', 'error', 'falla', 'frustrado', 'harto', 
                'cansado de', 'me rindo', 'imposible', 'no sirve', 'otra vez',
                'ya intenté', 'sigue sin', 'no puedo con', 'qué mal', 'rayos'
            ],
            "confundido": [
                'no entiendo', 'confundido', 'perdido', 'qué significa',
                'cómo es', 'no sé', 'me explicas', 'no me queda claro'
            ],
            "emocionado": [
                'genial', 'excelente', 'increíble', 'wow', 'funcionó', 'logré',
                'por fin', 'lo hice', 'perfecto', 'maravilloso', 'fantástico',
                'qué bien', 'me encanta'
            ],
            "preocupado": [
                'preocupado', 'preocupa', 'miedo', 'temo', 'asustado', 
                'nervioso', 'ansiedad', 'qué pasa si'
            ],
            "ocupado": [
                'rápido', 'urgente', 'apurado', 'prisa', 'ya', 'inmediato',
                'no tengo tiempo', 'breve', 'asap'
            ],
            "curioso": [
                'cómo funciona', 'por qué', 'interesante', 'quiero saber',
                'me pregunto', 'cuéntame más'
            ],
        }
        
        for emocion, patrones in emociones.items():
            if any(p in texto for p in patrones):
                return emocion
        
        return None
    
    def _detectar_urgencia(self, texto: str) -> str:
        """Detecta nivel de urgencia."""
        alta = ['urgente', 'asap', 'ya', 'inmediato', 'ahora mismo', 'lo antes posible']
        baja = ['sin prisa', 'cuando puedas', 'no hay apuro', 'cuando tengas tiempo']
        
        if any(p in texto for p in alta):
            return "alta"
        if any(p in texto for p in baja):
            return "baja"
        
        return "normal"
    
    def _detectar_tono(self, texto: str, emocion: Optional[str]) -> str:
        """Detecta el tono del mensaje."""
        # Por emoción
        if emocion == "frustrado":
            return "tenso"
        if emocion == "emocionado":
            return "entusiasta"
        if emocion == "preocupado":
            return "ansioso"
        
        # Por formalidad
        formal_patterns = ['usted', 'estimado', 'cordialmente', 'atentamente']
        if any(p in texto for p in formal_patterns):
            return "formal"
        
        casual_patterns = ['oye', 'che', 'wey', 'tío', 'bro', 'jaja', 'jeje']
        if any(p in texto for p in casual_patterns):
            return "casual"
        
        return "neutral"
    
    # ═══════════════════════════════════════════════════════════════════════════
    # BÚSQUEDA DE CONCEPTOS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _buscar_conceptos(self, texto: str) -> Tuple[List, Set[str]]:
        """Busca conceptos relevantes en el texto."""
        gestor = self._obtener_gestor()
        if gestor is None:
            return [], set()
        
        conceptos = gestor.buscar_conceptos_relacionados(texto, limite=15)
        ids = {c.id for c in conceptos}
        
        return conceptos, ids
    
    def _encontrar_desconocidas(self, texto: str) -> List[str]:
        """Encuentra palabras que no tienen concepto."""
        gestor = self._obtener_gestor()
        if gestor is None:
            return []
        
        desconocidas = []
        stopwords = {'el', 'la', 'los', 'las', 'un', 'una', 'de', 'en', 'que', 
                     'y', 'a', 'es', 'por', 'para', 'con', 'si', 'no', 'me', 
                     'te', 'se', 'lo', 'le', 'mi', 'tu', 'su'}
        
        palabras = texto.split()
        for palabra in palabras:
            palabra_limpia = palabra.strip('¿?.,;:!¡').lower()
            if len(palabra_limpia) < 2:
                continue
            if palabra_limpia in stopwords:
                continue
            
            concepto = gestor.buscar_por_palabra(palabra_limpia)
            if concepto is None:
                desconocidas.append(palabra_limpia)
        
        return desconocidas
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SUGERENCIAS PARA RESPUESTA
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _obtener_expresiones_sugeridas(
        self, 
        intencion: str, 
        emocion: Optional[str]
    ) -> List[str]:
        """
        Obtiene expresiones naturales sugeridas para la respuesta.
        Basado en el vocabulario expandido.
        """
        expresiones = []
        
        # Por intención
        if intencion == "saludo":
            expresiones.extend(["¡Hola!", "¡Qué tal!", "¡Buenos días!"])
        elif intencion == "despedida":
            expresiones.extend(["¡Hasta pronto!", "¡Cuídate!", "¡Nos vemos!"])
        elif intencion == "agradecimiento":
            expresiones.extend(["¡Con gusto!", "¡De nada!", "¡Un placer!"])
        elif intencion == "pregunta":
            expresiones.extend(["Claro,", "Por supuesto,", "Déjame ver..."])
        elif intencion == "solicitud":
            expresiones.extend(["¡Listo!", "Con mucho gusto", "¡Claro que sí!"])
        
        # Por emoción
        if emocion == "frustrado":
            expresiones.extend([
                "Entiendo tu frustración",
                "No te preocupes",
                "Vamos paso a paso"
            ])
        elif emocion == "confundido":
            expresiones.extend([
                "Déjame explicarlo de otra forma",
                "Es como si...",
                "Por ejemplo..."
            ])
        elif emocion == "emocionado":
            expresiones.extend([
                "¡Qué genial!",
                "¡Excelente!",
                "¡Me alegra mucho!"
            ])
        
        return expresiones
    
    def _recomendar_tono(self, analisis: AnalisisContextual) -> str:
        """Recomienda tono para la respuesta."""
        if analisis.emocion == "frustrado":
            return "empático_paciente"
        elif analisis.emocion == "confundido":
            return "didáctico_claro"
        elif analisis.emocion == "emocionado":
            return "entusiasta"
        elif analisis.emocion == "preocupado":
            return "tranquilizador"
        elif analisis.urgencia == "alta":
            return "conciso_directo"
        elif analisis.tono_detectado == "formal":
            return "profesional"
        elif analisis.tono_detectado == "casual":
            return "relajado_amigable"
        else:
            return "amigable_natural"
    
    # ═══════════════════════════════════════════════════════════════════════════
    # UTILIDADES
    # ═══════════════════════════════════════════════════════════════════════════
    
    def obtener_estadisticas(self) -> Dict:
        """Retorna estadísticas del traductor."""
        return {
            **self.stats,
            "cache_size": len(self._cache_traducciones),
            "hit_rate": (
                self.stats["cache_hits"] / self.stats["traducciones"]
                if self.stats["traducciones"] > 0 else 0
            ),
        }
    
    def limpiar_cache(self):
        """Limpia caché de traducciones."""
        self._cache_traducciones.clear()


# ═══════════════════════════════════════════════════════════════════════════════
# TEST
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    traductor = TraductorContextual()
    
    textos_test = [
        "hola, cómo estás?",
        "no funciona nada, ya intenté todo!",
        "wow increíble, funcionó perfecto!",
        "puedes leer archivos de python?",
        "rápido necesito ayuda urgente",
        "no entiendo qué es un algoritmo",
    ]
    
    print("🧪 Test de Traductor Contextual")
    print("=" * 60)
    
    for texto in textos_test:
        print(f"\n📝 Input: \"{texto}\"")
        analisis = traductor.traducir(texto)
        print(f"   Intención: {analisis.intencion}")
        print(f"   Emoción: {analisis.emocion or 'ninguna'}")
        print(f"   Urgencia: {analisis.urgencia}")
        print(f"   Tono detectado: {analisis.tono_detectado}")
        print(f"   Tono recomendado: {analisis.tono_recomendado}")
        print(f"   Expresiones sugeridas: {analisis.expresiones_sugeridas[:3]}")
        print(f"   Conceptos encontrados: {len(analisis.conceptos)}")
    
    print("\n" + "=" * 60)
    print("📊 Estadísticas:")
    print(traductor.obtener_estadisticas())