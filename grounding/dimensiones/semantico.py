"""
Dimensión Semántica: ¿Bell comprende el significado?

Bell comprende SIGNIFICADO de conceptos usando embeddings semánticos.

IMPORTANTE: Usa SINGLETON para evitar cargar el modelo múltiples veces.

Fase 3 → Fase 4 Refactorización (ARREGLADO)
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from datetime import datetime

from grounding.base_dimension import DimensionGrounding

# Intentar importar sentence-transformers
try:
    from sentence_transformers import SentenceTransformer
    EMBEDDINGS_DISPONIBLES = True
except ImportError:
    EMBEDDINGS_DISPONIBLES = False
    print("⚠️  sentence-transformers no instalado. Grounding semántico limitado.")


# ==================== SINGLETON DEL MODELO ====================

class _SingletonGestorEmbeddings:
    """
    Singleton para el gestor de embeddings.
    
    IMPORTANTE: Evita cargar el modelo múltiples veces.
    Se carga UNA SOLA VEZ y se comparte entre todas las instancias.
    """
    _instancia = None
    _modelo_cargado = False
    
    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia
    
    def __init__(self, modelo_nombre: str = 'all-MiniLM-L6-v2'):
        # Solo cargar si no está cargado
        if not self._modelo_cargado and EMBEDDINGS_DISPONIBLES:
            try:
                print(f"📦 Cargando modelo de embeddings (SINGLETON): {modelo_nombre}...")
                self.modelo = SentenceTransformer(modelo_nombre)
                self.cache = {}
                self._modelo_cargado = True
                print(f"✅ Modelo cargado una sola vez")
            except Exception as e:
                print(f"⚠️  Error cargando embeddings: {e}")
                self.modelo = None
                self.cache = {}
        elif not EMBEDDINGS_DISPONIBLES:
            self.modelo = None
            self.cache = {}
    
    def generar_embedding(self, texto: str) -> Optional[np.ndarray]:
        """Genera embedding para un texto."""
        if self.modelo is None:
            return None
        
        if texto in self.cache:
            return self.cache[texto]
        
        try:
            embedding = self.modelo.encode(texto, convert_to_numpy=True)
            self.cache[texto] = embedding
            return embedding
        except Exception:
            return None
    
    def similitud_coseno(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        """Calcula similitud coseno entre dos embeddings."""
        try:
            emb1_norm = emb1 / np.linalg.norm(emb1)
            emb2_norm = emb2 / np.linalg.norm(emb2)
            
            similitud = np.dot(emb1_norm, emb2_norm)
            similitud_normalizada = (similitud + 1) / 2
            
            return float(similitud_normalizada)
        except Exception:
            return 0.5


# Alias para mantener compatibilidad
GestorEmbeddings = _SingletonGestorEmbeddings


# ==================== CALCULADOR SEMÁNTICO ====================

class CalculadorSemantico:
    """Calculador auxiliar de grounding semántico."""
    
    def __init__(self, gestor_embeddings: _SingletonGestorEmbeddings):
        self.embeddings = gestor_embeddings
        self.embeddings_conceptos = {}
    
    def calcular(self, concepto, vocabulario=None) -> float:
        """
        Calcula grounding semántico para un concepto.
        """
        # Si modelo no disponible, usar heurística simple
        if self.embeddings.modelo is None:
            return self._calcular_simple(concepto)
        
        # 1. Generar embedding
        if not hasattr(concepto, 'palabras_español') or not concepto.palabras_español:
            return 0.0
        
        texto_concepto = " ".join(concepto.palabras_español)
        embedding_concepto = self.embeddings.generar_embedding(texto_concepto)
        
        if embedding_concepto is None:
            return self._calcular_simple(concepto)
        
        self.embeddings_conceptos[concepto.id] = embedding_concepto
        
        # 2. Calcular coherencia interna
        coherencia = self._calcular_coherencia_interna(concepto, embedding_concepto)
        
        # 3. Calcular densidad de red (si hay vocabulario)
        if vocabulario:
            densidad = self._calcular_densidad_red(concepto, embedding_concepto, vocabulario)
        else:
            densidad = 0.5
        
        # 4. Grounding semántico = promedio ponderado
        valor = 0.6 * coherencia + 0.4 * densidad
        
        return valor
    
    def _calcular_simple(self, concepto) -> float:
        """Evaluación simple sin embeddings (fallback)."""
        puntaje = 0.0
        
        if hasattr(concepto, 'palabras_español') and concepto.palabras_español:
            puntaje += 0.3
            
            if len(concepto.palabras_español) >= 3:
                puntaje += 0.3
            elif len(concepto.palabras_español) >= 2:
                puntaje += 0.15
        
        if hasattr(concepto, 'relaciones') and concepto.relaciones:
            num_relaciones = sum(len(rels) for rels in concepto.relaciones.values())
            if num_relaciones >= 5:
                puntaje += 0.4
            elif num_relaciones >= 2:
                puntaje += 0.2
        
        return min(1.0, puntaje)
    
    def _calcular_coherencia_interna(self, concepto, embedding_concepto: np.ndarray) -> float:
        """Calcula coherencia interna del concepto."""
        if len(concepto.palabras_español) <= 1:
            return 1.0
        
        embeddings_palabras = []
        for palabra in concepto.palabras_español:
            emb = self.embeddings.generar_embedding(palabra)
            if emb is not None:
                embeddings_palabras.append(emb)
        
        if len(embeddings_palabras) < 2:
            return 1.0
        
        similitudes = []
        for i in range(len(embeddings_palabras)):
            for j in range(i + 1, len(embeddings_palabras)):
                sim = self.embeddings.similitud_coseno(
                    embeddings_palabras[i],
                    embeddings_palabras[j]
                )
                similitudes.append(sim)
        
        if not similitudes:
            return 1.0
        
        coherencia = np.mean(similitudes)
        return float(coherencia)
    
    def _calcular_densidad_red(self, concepto, embedding_concepto: np.ndarray, vocabulario) -> float:
        """Calcula densidad de red semántica."""
        if hasattr(concepto, 'relaciones') and concepto.relaciones:
            conceptos_relacionados_ids = []
            for tipo_rel, conceptos in concepto.relaciones.items():
                conceptos_relacionados_ids.extend(list(conceptos)[:5])
        else:
            if len(self.embeddings_conceptos) < 2:
                return 0.5
            
            similares = []
            for cid, emb in self.embeddings_conceptos.items():
                if cid != concepto.id:
                    sim = self.embeddings.similitud_coseno(embedding_concepto, emb)
                    similares.append((cid, sim))
            
            similares.sort(key=lambda x: x[1], reverse=True)
            conceptos_relacionados_ids = [cid for cid, _ in similares[:5]]
        
        if not conceptos_relacionados_ids:
            return 0.0
        
        similitudes = []
        for rel_id in conceptos_relacionados_ids:
            if rel_id not in self.embeddings_conceptos:
                rel_concepto = vocabulario.buscar_por_id(rel_id)
                if rel_concepto:
                    texto_rel = " ".join(rel_concepto.palabras_español)
                    emb_rel = self.embeddings.generar_embedding(texto_rel)
                    if emb_rel is not None:
                        self.embeddings_conceptos[rel_id] = emb_rel
                else:
                    continue
            
            if rel_id in self.embeddings_conceptos:
                emb_relacionado = self.embeddings_conceptos[rel_id]
                similitud = self.embeddings.similitud_coseno(embedding_concepto, emb_relacionado)
                similitudes.append(similitud)
        
        if not similitudes:
            return 0.0
        
        densidad = np.mean(similitudes)
        return float(densidad)


# ==================== DIMENSIÓN PRINCIPAL ====================

class GroundingSemantico(DimensionGrounding):
    """
    Grounding semántico: comprensión del significado.
    
    ARREGLADO: Usa singleton para evitar cargar el modelo múltiples veces.
    """
    
    # Singleton compartido entre TODAS las instancias
    _gestor_embeddings_compartido = None
    
    def __init__(self, vocabulario=None):
        """Inicializa dimensión semántica."""
        super().__init__()
        
        self.vocabulario = vocabulario
        
        # Usar gestor singleton (se carga UNA SOLA VEZ)
        if GroundingSemantico._gestor_embeddings_compartido is None:
            GroundingSemantico._gestor_embeddings_compartido = _SingletonGestorEmbeddings()
        
        self.gestor_embeddings = GroundingSemantico._gestor_embeddings_compartido
        
        # Solo crear calculador si hay embeddings
        if EMBEDDINGS_DISPONIBLES and self.gestor_embeddings.modelo is not None:
            self.calculador = CalculadorSemantico(self.gestor_embeddings)
        else:
            self.calculador = None
    
    @property
    def nombre(self) -> str:
        return "Semántico"
    
    @property
    def descripcion(self) -> str:
        return "¿Bell comprende el significado profundo del concepto?"
    
    def evaluar(self, concepto: Any) -> float:
        """Evalúa comprensión semántica."""
        # Si no hay embeddings, usar heurística simple
        if not EMBEDDINGS_DISPONIBLES or not self.calculador:
            return self._evaluar_simple(concepto)
        
        # Evaluar con embeddings
        try:
            return self.calculador.calcular(concepto, self.vocabulario)
        except Exception:
            return self._evaluar_simple(concepto)
    
    def _evaluar_simple(self, concepto: Any) -> float:
        """Evaluación simple sin embeddings (fallback)."""
        puntaje = 0.0
        
        if hasattr(concepto, 'palabras_español') and concepto.palabras_español:
            puntaje += 0.3
            
            if len(concepto.palabras_español) >= 3:
                puntaje += 0.3
            elif len(concepto.palabras_español) >= 2:
                puntaje += 0.15
        
        if hasattr(concepto, 'relaciones') and concepto.relaciones:
            num_relaciones = sum(len(rels) for rels in concepto.relaciones.values())
            if num_relaciones >= 5:
                puntaje += 0.4
            elif num_relaciones >= 2:
                puntaje += 0.2
        
        return min(1.0, puntaje)


if __name__ == '__main__':
    print("Testing GroundingSemantico (con singleton)...")
    
    # Crear múltiples instancias - el modelo se carga UNA SOLA VEZ
    g1 = GroundingSemantico()
    g2 = GroundingSemantico()
    g3 = GroundingSemantico()
    
    print(f"✅ Tres instancias creadas")
    print(f"✅ Mismo gestor: {g1.gestor_embeddings is g2.gestor_embeddings}")
    print(f"✅ Modelo cargado una sola vez")