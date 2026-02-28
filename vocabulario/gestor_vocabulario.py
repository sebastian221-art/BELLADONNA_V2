"""
Gestor de Vocabulario de Belladonna - FASE 4A COMPLETA.

Coordina la carga de TODOS los conceptos.
VERSIÓN COMPLETA: Base (453) + Expansión (1,030) = ~1,483 conceptos

ARQUITECTURA:
- Base: Conceptos con operaciones ejecutables (Fases 1-3)
- Expansión: Conceptos conversacionales ricos (Fase 4A)
"""
from typing import List, Optional, Dict, Set
from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto


class GestorVocabulario:
    """
    Administra TODO el vocabulario de Bell de forma modular.
    
    Ahora con 1,483 conceptos para conversación ultra natural.
    """
    
    def __init__(self, cargar_expansion: bool = True):
        """
        Inicializa el gestor.
        
        Args:
            cargar_expansion: Si True, carga los 1,030 conceptos adicionales
        """
        self.conceptos: List[ConceptoAnclado] = []
        self._palabras_a_conceptos: Dict[str, List[ConceptoAnclado]] = {}
        self._id_a_concepto: Dict[str, ConceptoAnclado] = {}
        self._conceptos_por_tipo: Dict[str, List[ConceptoAnclado]] = {}
        self._conceptos_por_categoria: Dict[str, List[ConceptoAnclado]] = {}
        
        self._cargar_conceptos_base()
        
        if cargar_expansion:
            self._cargar_expansion()
        
        self._construir_indices()
        self._construir_indices_avanzados()
    
    def _cargar_conceptos_base(self):
        """Carga los 453 conceptos base (Fase 1+2+3)."""
        
        # ========== FASE 1: FUNDAMENTOS ==========
        
        # SEMANA 1: Fundamentos (30 conceptos)
        from vocabulario.semana1_operaciones import obtener_conceptos_operaciones
        from vocabulario.semana1_conversacion import obtener_conceptos_conversacion
        from vocabulario.semana1_cognitivos import obtener_conceptos_cognitivos
        from vocabulario.semana1_acciones import obtener_conceptos_acciones
        
        self.conceptos.extend(obtener_conceptos_operaciones())
        self.conceptos.extend(obtener_conceptos_conversacion())
        self.conceptos.extend(obtener_conceptos_cognitivos())
        self.conceptos.extend(obtener_conceptos_acciones())
        
        # SEMANA 2: Traducción (40 conceptos)
        from vocabulario.semana2_python import obtener_conceptos_python
        from vocabulario.semana2_verbos import obtener_conceptos_verbos
        from vocabulario.semana2_conectores import obtener_conceptos_conectores
        from vocabulario.semana2_adjetivos import obtener_conceptos_adjetivos
        
        self.conceptos.extend(obtener_conceptos_python())
        self.conceptos.extend(obtener_conceptos_verbos())
        self.conceptos.extend(obtener_conceptos_conectores())
        self.conceptos.extend(obtener_conceptos_adjetivos())
        
        # SEMANA 2.5: Python Avanzado (40 conceptos)
        from vocabulario.semana3_python_avanzado import obtener_conceptos_python_avanzado
        self.conceptos.extend(obtener_conceptos_python_avanzado())
        
        # SEMANA 3: Vocabulario Expandido (77 conceptos)
        from vocabulario.semana3_sistema_avanzado import obtener_conceptos_sistema_avanzado
        from vocabulario.semana3_matematicas import obtener_conceptos_matematicas
        from vocabulario.semana3_conversacion_expandida import obtener_conceptos_conversacion_expandida
        
        self.conceptos.extend(obtener_conceptos_sistema_avanzado())
        self.conceptos.extend(obtener_conceptos_matematicas())
        self.conceptos.extend(obtener_conceptos_conversacion_expandida())

        # SEMANA 4: Acciones, Emociones, Tiempo (35 conceptos)
        from vocabulario.semana4_acciones import obtener_conceptos_acciones as obtener_acciones_s4
        from vocabulario.semana4_emociones import obtener_conceptos_emociones
        from vocabulario.semana4_tiempo import obtener_conceptos_tiempo

        self.conceptos.extend(obtener_acciones_s4())
        self.conceptos.extend(obtener_conceptos_emociones())
        self.conceptos.extend(obtener_conceptos_tiempo())
        
        # ========== FASE 3: CAPACIDADES FUNCIONALES ==========
        
        # SEMANA 5: Sistema y Shell (39 conceptos)
        from vocabulario.semana5_sistema import obtener_conceptos_sistema
        self.conceptos.extend(obtener_conceptos_sistema())
        
        # SEMANA 6: Análisis de Código (50 conceptos)
        from vocabulario.semana6_analisis import obtener_conceptos_analisis
        self.conceptos.extend(obtener_conceptos_analisis())
        
        # SEMANA 7: Matemáticas Avanzadas (45 conceptos)
        from vocabulario.semana7_matematicas import obtener_conceptos_matematicas_avanzadas
        self.conceptos.extend(obtener_conceptos_matematicas_avanzadas())
        
        # SEMANA 8: Planificación Multi-Paso (40 conceptos)
        from vocabulario.semana8_planificacion import obtener_conceptos_planificacion
        self.conceptos.extend(obtener_conceptos_planificacion())
        
        # SEMANA 9: Red y APIs HTTP (35 conceptos)
        from vocabulario.semana9_red import obtener_conceptos_red
        self.conceptos.extend(obtener_conceptos_red())
        
        # SEMANA 10: Bases de Datos SQLite (30 conceptos)
        from vocabulario.semana10_bd import obtener_conceptos_bd
        self.conceptos.extend(obtener_conceptos_bd())
        
        print(f"✅ Base cargada: {len(self.conceptos)} conceptos")
    
    def _cargar_expansion(self):
        """Carga los 1,030 conceptos de expansión conversacional."""
        try:
            from vocabulario.expansion import obtener_todos_conceptos_expansion
            
            conceptos_expansion = obtener_todos_conceptos_expansion()
            self.conceptos.extend(conceptos_expansion)
            
            print(f"✅ Expansión cargada: +{len(conceptos_expansion)} conceptos")
            print(f"📊 TOTAL: {len(self.conceptos)} conceptos disponibles")
            
        except ImportError as e:
            print(f"⚠️  Expansión no disponible: {e}")
    
    def _construir_indices(self):
        """Construye índices para búsqueda rápida."""
        self._palabras_a_conceptos.clear()
        self._id_a_concepto.clear()
        
        for concepto in self.conceptos:
            # Índice por ID
            self._id_a_concepto[concepto.id] = concepto
            
            # Índice por palabra
            for palabra in concepto.palabras_español:
                palabra_lower = palabra.lower()
                if palabra_lower not in self._palabras_a_conceptos:
                    self._palabras_a_conceptos[palabra_lower] = []
                self._palabras_a_conceptos[palabra_lower].append(concepto)
    
    def _construir_indices_avanzados(self):
        """Construye índices avanzados por tipo y categoría."""
        self._conceptos_por_tipo.clear()
        self._conceptos_por_categoria.clear()
        
        for concepto in self.conceptos:
            # Por tipo
            tipo_nombre = concepto.tipo.name
            if tipo_nombre not in self._conceptos_por_tipo:
                self._conceptos_por_tipo[tipo_nombre] = []
            self._conceptos_por_tipo[tipo_nombre].append(concepto)
            
            # Por categorías en propiedades
            for key, value in concepto.propiedades.items():
                if key.startswith("es_") and value:
                    categoria = key[3:]  # Quitar "es_"
                    if categoria not in self._conceptos_por_categoria:
                        self._conceptos_por_categoria[categoria] = []
                    self._conceptos_por_categoria[categoria].append(concepto)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # BÚSQUEDAS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def obtener_todos(self) -> List[ConceptoAnclado]:
        """Retorna todos los conceptos cargados."""
        return self.conceptos
    
    def total_conceptos(self) -> int:
        """Retorna el número total de conceptos."""
        return len(self.conceptos)
    
    def buscar_por_palabra(self, palabra: str) -> Optional[ConceptoAnclado]:
        """Busca concepto por palabra. Prioriza mayor grounding."""
        palabra_lower = palabra.lower()
        conceptos = self._palabras_a_conceptos.get(palabra_lower, [])
        
        if not conceptos:
            return None
        
        return max(conceptos, key=lambda c: c.confianza_grounding)
    
    def buscar_todos_por_palabra(self, palabra: str) -> List[ConceptoAnclado]:
        """Busca TODOS los conceptos que contienen una palabra."""
        palabra_lower = palabra.lower()
        return self._palabras_a_conceptos.get(palabra_lower, [])
    
    def buscar_por_id(self, concepto_id: str) -> Optional[ConceptoAnclado]:
        """Busca concepto por ID."""
        return self._id_a_concepto.get(concepto_id)
    
    def filtrar_por_tipo(self, tipo_concepto) -> List[ConceptoAnclado]:
        """Filtra conceptos por tipo."""
        tipo_nombre = tipo_concepto.name if hasattr(tipo_concepto, 'name') else str(tipo_concepto)
        return self._conceptos_por_tipo.get(tipo_nombre, [])
    
    def filtrar_por_categoria(self, categoria: str) -> List[ConceptoAnclado]:
        """Filtra conceptos por categoría (ej: 'emocion', 'accion', 'tecnologia')."""
        return self._conceptos_por_categoria.get(categoria, [])
    
    # ═══════════════════════════════════════════════════════════════════════════
    # BÚSQUEDAS SEMÁNTICAS (para Groq)
    # ═══════════════════════════════════════════════════════════════════════════
    
    def buscar_conceptos_relacionados(self, texto: str, limite: int = 10) -> List[ConceptoAnclado]:
        """
        Busca conceptos relacionados con un texto.
        Útil para enriquecer respuestas de Groq.
        """
        texto_lower = texto.lower()
        encontrados = []
        scores = {}
        
        for palabra in texto_lower.split():
            palabra = palabra.strip('¿?.,;:!¡')
            if len(palabra) < 2:
                continue
            
            conceptos = self._palabras_a_conceptos.get(palabra, [])
            for c in conceptos:
                if c.id not in scores:
                    scores[c.id] = 0
                    encontrados.append(c)
                scores[c.id] += c.confianza_grounding
        
        # Ordenar por score y retornar top N
        encontrados.sort(key=lambda c: scores.get(c.id, 0), reverse=True)
        return encontrados[:limite]
    
    def obtener_vocabulario_por_contexto(self, contexto: str) -> Dict[str, List[str]]:
        """
        Obtiene vocabulario organizado por contexto.
        
        Args:
            contexto: 'emocional', 'tecnico', 'profesional', 'casual', etc.
        
        Returns:
            Dict con categorías y palabras disponibles
        """
        vocab = {}
        
        if contexto == 'emocional':
            categorias = ['emocion', 'estado', 'sentimiento']
        elif contexto == 'tecnico':
            categorias = ['tecnologia', 'digital', 'accion_digital']
        elif contexto == 'profesional':
            categorias = ['profesion', 'accion_laboral', 'concepto_laboral']
        elif contexto == 'casual':
            categorias = ['conversacion', 'cortesia', 'modismo']
        else:
            categorias = list(self._conceptos_por_categoria.keys())[:5]
        
        for cat in categorias:
            conceptos = self._conceptos_por_categoria.get(cat, [])
            palabras = []
            for c in conceptos[:20]:  # Máximo 20 por categoría
                palabras.extend(c.palabras_español[:2])  # 2 palabras por concepto
            vocab[cat] = palabras
        
        return vocab
    
    def obtener_expresiones_naturales(self, tipo: str = 'todas') -> List[str]:
        """
        Obtiene expresiones naturales para usar en respuestas.
        
        Args:
            tipo: 'afirmacion', 'negacion', 'transicion', 'emocion', 'todas'
        """
        expresiones = []
        
        # Buscar en conceptos de expresiones comunes
        conceptos_expresion = self.filtrar_por_tipo(TipoConcepto.PALABRA_CONVERSACION)
        
        for c in conceptos_expresion:
            props = c.propiedades
            
            if tipo == 'todas':
                expresiones.extend(c.palabras_español)
            elif tipo == 'afirmacion' and props.get('es_acuerdo'):
                expresiones.extend(c.palabras_español)
            elif tipo == 'negacion' and props.get('es_desacuerdo'):
                expresiones.extend(c.palabras_español)
            elif tipo == 'transicion' and props.get('es_conector'):
                expresiones.extend(c.palabras_español)
            elif tipo == 'emocion' and props.get('es_emocion'):
                expresiones.extend(c.palabras_español)
        
        return list(set(expresiones))[:50]  # Máximo 50
    
    # ═══════════════════════════════════════════════════════════════════════════
    # UTILIDADES
    # ═══════════════════════════════════════════════════════════════════════════
    
    def detectar_duplicados(self) -> Dict[str, List[str]]:
        """Detecta palabras que aparecen en múltiples conceptos."""
        duplicados = {}
        for palabra, conceptos in self._palabras_a_conceptos.items():
            if len(conceptos) > 1:
                duplicados[palabra] = [c.id for c in conceptos]
        return duplicados
    
    def estadisticas(self) -> dict:
        """Retorna estadísticas completas del vocabulario."""
        total = len(self.conceptos)
        if total == 0:
            return {'total_conceptos': 0}
        
        grounding_promedio = sum(c.confianza_grounding for c in self.conceptos) / total
        
        # Contar por tipo
        por_tipo = {}
        for tipo, conceptos in self._conceptos_por_tipo.items():
            por_tipo[tipo] = len(conceptos)
        
        # Contar por categoría
        por_categoria = {}
        for cat, conceptos in self._conceptos_por_categoria.items():
            por_categoria[cat] = len(conceptos)
        
        return {
            'total_conceptos': total,
            'grounding_promedio': round(grounding_promedio, 3),
            'por_tipo': por_tipo,
            'por_categoria': por_categoria,
            'con_operaciones': sum(1 for c in self.conceptos if len(c.operaciones) > 0),
            'grounding_1_0': sum(1 for c in self.conceptos if c.confianza_grounding == 1.0),
            'palabras_totales': len(self._palabras_a_conceptos),
            'palabras_duplicadas': len(self.detectar_duplicados()),
            'categorias_disponibles': list(self._conceptos_por_categoria.keys()),
        }
    
    def resumen(self):
        """Imprime resumen del vocabulario."""
        stats = self.estadisticas()
        
        print()
        print("=" * 70)
        print("VOCABULARIO DE BELLADONNA - FASE 4A COMPLETA")
        print("=" * 70)
        print()
        print(f"📊 Total conceptos: {stats['total_conceptos']}")
        print(f"📈 Grounding promedio: {stats['grounding_promedio']}")
        print(f"⚡ Con grounding 1.0 (ejecutables): {stats['grounding_1_0']}")
        print(f"🔧 Con operaciones definidas: {stats['con_operaciones']}")
        print()
        print(f"📝 Palabras totales en índice: {stats['palabras_totales']}")
        print()
        print("Por tipo:")
        for tipo, count in sorted(stats['por_tipo'].items()):
            print(f"  {tipo}: {count}")
        print()
        print(f"Categorías disponibles: {len(stats['categorias_disponibles'])}")
        print("=" * 70)


# Instancia global (singleton)
_gestor_global = None


def obtener_gestor() -> GestorVocabulario:
    """Obtiene instancia global del gestor."""
    global _gestor_global
    if _gestor_global is None:
        _gestor_global = GestorVocabulario(cargar_expansion=True)
    return _gestor_global


if __name__ == '__main__':
    gestor = GestorVocabulario(cargar_expansion=True)
    gestor.resumen()
    
    # Test de búsquedas
    print("\n🧪 Test de búsquedas:")
    
    relacionados = gestor.buscar_conceptos_relacionados("estoy frustrado no funciona")
    print(f"\nConceptos relacionados con 'estoy frustrado no funciona':")
    for c in relacionados[:5]:
        print(f"  - {c.id}: {c.palabras_español[:2]} (g={c.confianza_grounding})")
    
    expresiones = gestor.obtener_expresiones_naturales('afirmacion')
    print(f"\nExpresiones de afirmación: {expresiones[:10]}")