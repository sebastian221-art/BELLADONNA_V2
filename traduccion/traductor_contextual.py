"""
Traductor Contextual ULTRA MEJORADO - Fase 4A Completa

Traduce texto del usuario a conceptos de Bell usando los 1,483 conceptos.
Detecta contexto emocional, urgencia, intención y tema.
"""
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, field


@dataclass
class AnalisisContextual:
    """Resultado del análisis contextual completo."""
    conceptos: List = field(default_factory=list)
    conceptos_ids: Set[str] = field(default_factory=set)
    texto_original: str = ""
    texto_normalizado: str = ""
    intencion: str = "desconocida"
    tema: str = "general"
    emocion: Optional[str] = None
    urgencia: str = "normal"
    tono_detectado: str = "neutral"
    confianza_traduccion: float = 0.0
    palabras_conocidas: int = 0
    palabras_desconocidas: List[str] = field(default_factory=list)
    palabras_totales: int = 0
    expresiones_sugeridas: List[str] = field(default_factory=list)
    tono_recomendado: str = "amigable"


class TraductorContextual:
    """
    Traduce texto a conceptos con análisis contextual profundo.
    """

    def __init__(self, gestor_vocabulario=None):
        self._gestor = gestor_vocabulario
        self._cache_traducciones: Dict[str, AnalisisContextual] = {}
        self.stats = {
            "traducciones": 0,
            "cache_hits": 0,
            "emociones_detectadas": {},
            "intenciones_detectadas": {},
        }

    def _obtener_gestor(self):
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
        """Traduce texto a conceptos con análisis contextual completo."""
        self.stats["traducciones"] += 1

        texto_norm = self._normalizar(texto)
        if usar_cache and texto_norm in self._cache_traducciones:
            self.stats["cache_hits"] += 1
            return self._cache_traducciones[texto_norm]

        analisis = AnalisisContextual(
            texto_original=texto,
            texto_normalizado=texto_norm,
        )

        analisis.intencion = self._detectar_intencion(texto_norm)
        self.stats["intenciones_detectadas"][analisis.intencion] = \
            self.stats["intenciones_detectadas"].get(analisis.intencion, 0) + 1

        analisis.tema     = self._detectar_tema(texto_norm)
        analisis.emocion  = self._detectar_emocion(texto_norm)
        if analisis.emocion:
            self.stats["emociones_detectadas"][analisis.emocion] = \
                self.stats["emociones_detectadas"].get(analisis.emocion, 0) + 1

        analisis.urgencia       = self._detectar_urgencia(texto_norm)
        analisis.tono_detectado = self._detectar_tono(texto_norm, analisis.emocion)
        analisis.conceptos, analisis.conceptos_ids = self._buscar_conceptos(texto_norm)

        palabras = texto_norm.split()
        analisis.palabras_totales      = len(palabras)
        analisis.palabras_conocidas    = len(analisis.conceptos)
        analisis.palabras_desconocidas = self._encontrar_desconocidas(texto_norm)

        if analisis.palabras_totales > 0:
            analisis.confianza_traduccion = min(
                analisis.palabras_conocidas / analisis.palabras_totales, 1.0
            )

        analisis.expresiones_sugeridas = self._obtener_expresiones_sugeridas(
            analisis.intencion, analisis.emocion
        )
        analisis.tono_recomendado = self._recomendar_tono(analisis)

        if usar_cache:
            self._cache_traducciones[texto_norm] = analisis

        return analisis

    # ═══════════════════════════════════════════════════════════════════════════
    # FIX: método requerido por TraductorEntrada — DEBE estar dentro de la clase
    # ═══════════════════════════════════════════════════════════════════════════

    def seleccionar_concepto_por_contexto(
        self, lema: str, candidatos: list, texto: str
    ):
        """
        Selecciona el concepto más relevante para un lema dado el contexto.

        Llamado por TraductorEntrada cuando hay varios candidatos para una
        misma palabra y se necesita desambiguar usando el contexto completo.
        """
        if not candidatos:
            return None
        if len(candidatos) == 1:
            return candidatos[0]

        # Analizar contexto completo sin caché
        analisis = self.traducir(texto, usar_cache=False)
        ids_contexto = analisis.conceptos_ids

        # Preferir candidato cuyo ID aparece en el análisis contextual
        for candidato in candidatos:
            concepto_id = getattr(candidato, "id", None)
            if concepto_id and concepto_id in ids_contexto:
                return candidato

        # Fallback: mayor confianza_grounding
        try:
            return max(candidatos, key=lambda c: getattr(c, "confianza_grounding", 0.0))
        except (TypeError, ValueError):
            return candidatos[0]

    # ═══════════════════════════════════════════════════════════════════════════
    # DETECTORES
    # ═══════════════════════════════════════════════════════════════════════════

    def _normalizar(self, texto: str) -> str:
        return texto.lower().strip()

    def _detectar_intencion(self, texto: str) -> str:
        if any(texto.startswith(p) for p in [
            '¿', 'qué', 'cómo', 'cuándo', 'dónde', 'por qué',
            'cuál', 'quién', 'puedes', 'podrías', 'sabes', 'es posible'
        ]):
            return "pregunta"
        if '?' in texto:
            return "pregunta"
        if any(p in texto for p in [
            'puedes', 'podrías', 'quiero', 'necesito', 'hazme', 'ayúdame',
            'crea', 'genera', 'escribe', 'lee', 'ejecuta', 'muéstrame',
            'dime', 'explícame', 'enséñame'
        ]):
            return "solicitud"
        if any(s in texto for s in [
            'hola', 'hey', 'buenos días', 'buenas tardes', 'buenas noches',
            'qué tal', 'cómo estás', 'hi', 'hello'
        ]):
            return "saludo"
        if any(d in texto for d in [
            'adiós', 'chao', 'hasta luego', 'nos vemos', 'bye', 'me voy', 'hasta pronto'
        ]):
            return "despedida"
        if any(a in texto for a in ['gracias', 'te agradezco', 'muchas gracias', 'mil gracias']):
            return "agradecimiento"
        if any(c in texto for c in [
            'sí', 'ok', 'vale', 'de acuerdo', 'perfecto', 'correcto', 'exacto', 'así es'
        ]):
            return "confirmacion"
        negaciones = ['no', 'nope', 'para nada', 'negativo', 'incorrecto']
        if any(n == texto.strip() or texto.startswith(n + ' ') for n in negaciones):
            return "negacion"
        return "afirmacion"

    def _detectar_tema(self, texto: str) -> str:
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
            "personal":        ['yo', 'mi', 'me siento', 'estoy', 'necesito', 'quiero'],
            "comida":          ['comer', 'comida', 'receta', 'cocina', 'restaurante', 'hambre'],
            "salud":           ['salud', 'médico', 'dolor', 'enfermo', 'ejercicio', 'dormir'],
            "entretenimiento": ['película', 'serie', 'música', 'juego', 'videojuego', 'libro'],
        }
        for tema, palabras in temas.items():
            if any(p in texto for p in palabras):
                return tema
        return "general"

    def _detectar_emocion(self, texto: str) -> Optional[str]:
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
        if any(p in texto for p in ['urgente', 'asap', 'ya', 'inmediato', 'ahora mismo', 'lo antes posible']):
            return "alta"
        if any(p in texto for p in ['sin prisa', 'cuando puedas', 'no hay apuro', 'cuando tengas tiempo']):
            return "baja"
        return "normal"

    def _detectar_tono(self, texto: str, emocion: Optional[str]) -> str:
        if emocion == "frustrado":  return "tenso"
        if emocion == "emocionado": return "entusiasta"
        if emocion == "preocupado": return "ansioso"
        if any(p in texto for p in ['usted', 'estimado', 'cordialmente', 'atentamente']):
            return "formal"
        if any(p in texto for p in ['oye', 'che', 'wey', 'tío', 'bro', 'jaja', 'jeje']):
            return "casual"
        return "neutral"

    # ═══════════════════════════════════════════════════════════════════════════
    # BÚSQUEDA DE CONCEPTOS
    # ═══════════════════════════════════════════════════════════════════════════

    def _buscar_conceptos(self, texto: str) -> Tuple[List, Set[str]]:
        gestor = self._obtener_gestor()
        if gestor is None:
            return [], set()
        conceptos = gestor.buscar_conceptos_relacionados(texto, limite=15)
        return conceptos, {c.id for c in conceptos}

    def _encontrar_desconocidas(self, texto: str) -> List[str]:
        gestor = self._obtener_gestor()
        if gestor is None:
            return []
        stopwords = {
            'el', 'la', 'los', 'las', 'un', 'una', 'de', 'en', 'que',
            'y', 'a', 'es', 'por', 'para', 'con', 'si', 'no', 'me',
            'te', 'se', 'lo', 'le', 'mi', 'tu', 'su'
        }
        desconocidas = []
        for palabra in texto.split():
            pl = palabra.strip('¿?.,;:!¡').lower()
            if len(pl) < 2 or pl in stopwords:
                continue
            if gestor.buscar_por_palabra(pl) is None:
                desconocidas.append(pl)
        return desconocidas

    # ═══════════════════════════════════════════════════════════════════════════
    # SUGERENCIAS PARA RESPUESTA
    # ═══════════════════════════════════════════════════════════════════════════

    def _obtener_expresiones_sugeridas(
        self, intencion: str, emocion: Optional[str]
    ) -> List[str]:
        expresiones = []
        mapa = {
            "saludo":         ["¡Hola!", "¡Qué tal!", "¡Buenos días!"],
            "despedida":      ["¡Hasta pronto!", "¡Cuídate!", "¡Nos vemos!"],
            "agradecimiento": ["¡Con gusto!", "¡De nada!", "¡Un placer!"],
            "pregunta":       ["Claro,", "Por supuesto,", "Déjame ver..."],
            "solicitud":      ["¡Listo!", "Con mucho gusto", "¡Claro que sí!"],
        }
        expresiones.extend(mapa.get(intencion, []))
        mapa_emocion = {
            "frustrado":  ["Entiendo tu frustración", "No te preocupes", "Vamos paso a paso"],
            "confundido": ["Déjame explicarlo de otra forma", "Es como si...", "Por ejemplo..."],
            "emocionado": ["¡Qué genial!", "¡Excelente!", "¡Me alegra mucho!"],
        }
        expresiones.extend(mapa_emocion.get(emocion or "", []))
        return expresiones

    def _recomendar_tono(self, analisis: AnalisisContextual) -> str:
        if analisis.emocion == "frustrado":        return "empático_paciente"
        if analisis.emocion == "confundido":       return "didáctico_claro"
        if analisis.emocion == "emocionado":       return "entusiasta"
        if analisis.emocion == "preocupado":       return "tranquilizador"
        if analisis.urgencia == "alta":            return "conciso_directo"
        if analisis.tono_detectado == "formal":    return "profesional"
        if analisis.tono_detectado == "casual":    return "relajado_amigable"
        return "amigable_natural"

    # ═══════════════════════════════════════════════════════════════════════════
    # UTILIDADES
    # ═══════════════════════════════════════════════════════════════════════════

    def obtener_estadisticas(self) -> Dict:
        return {
            **self.stats,
            "cache_size": len(self._cache_traducciones),
            "hit_rate": (
                self.stats["cache_hits"] / self.stats["traducciones"]
                if self.stats["traducciones"] > 0 else 0
            ),
        }

    def limpiar_cache(self):
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
        print(f"   Intención:  {analisis.intencion}")
        print(f"   Emoción:    {analisis.emocion or 'ninguna'}")
        print(f"   Urgencia:   {analisis.urgencia}")
        print(f"   Tono:       {analisis.tono_detectado} → {analisis.tono_recomendado}")
        print(f"   Conceptos:  {len(analisis.conceptos)}")
    print("\n" + "=" * 60)
    print(traductor.obtener_estadisticas())
