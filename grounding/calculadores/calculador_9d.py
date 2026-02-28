"""
Calculador de Grounding 9D.

Calcula grounding completo (9 dimensiones) para conceptos individuales
o lotes completos de conceptos.

Fase 3 → Fase 4 Refactorización
"""

from typing import Dict, List, Optional, Any
from grounding.gestor_grounding import GestorGrounding
from datetime import datetime
import json
from pathlib import Path


class Calculador9D:
    """
    Calcula grounding en las 9 dimensiones para conceptos.
    
    Uso:
        calculador = Calculador9D(vocabulario)
        
        # Un concepto
        grounding = calculador.calcular_concepto(concepto)
        
        # Todos los conceptos
        resultados = calculador.calcular_todos()
    """
    
    def __init__(self, gestor_vocabulario=None):
        """
        Inicializa calculador.
        
        Args:
            gestor_vocabulario: GestorVocabulario (opcional, mejora cálculos)
        """
        self.vocabulario = gestor_vocabulario
        
        # Crear gestor de grounding
        self.gestor = GestorGrounding()
        
        # Configurar dimensión semántica con vocabulario si está disponible
        if self.vocabulario:
            from grounding.dimensiones.semantico import GroundingSemantico
            self.gestor.dimensiones['semantico'] = GroundingSemantico(self.vocabulario)
        
        # Cache de resultados
        self.cache_resultados = {}
    
    def calcular_concepto(self, concepto: Any) -> Dict[str, float]:
        """
        Calcula grounding 9D para un concepto.
        
        Args:
            concepto: ConceptoAnclado a evaluar
        
        Returns:
            Dict con puntajes de las 9 dimensiones:
            {
                'computacional': 1.0,
                'semantico': 0.9,
                'contextual': 0.85,
                ...
            }
        """
        # Verificar cache
        concepto_id = getattr(concepto, 'id', str(concepto))
        
        if concepto_id in self.cache_resultados:
            return self.cache_resultados[concepto_id]
        
        # Calcular usando gestor
        grounding_9d = self.gestor.evaluar_9d(concepto)
        
        # Guardar en cache
        self.cache_resultados[concepto_id] = grounding_9d
        
        return grounding_9d
    
    def calcular_todos(self) -> Dict[str, Dict[str, float]]:
        """
        Calcula grounding 9D para TODOS los conceptos del vocabulario.
        
        Returns:
            Dict de {concepto_id: grounding_9d}
        
        Raises:
            RuntimeError: Si no hay vocabulario configurado
        """
        if not self.vocabulario:
            raise RuntimeError(
                "No hay vocabulario configurado. "
                "Inicializar con: Calculador9D(gestor_vocabulario)"
            )
        
        resultados = {}
        conceptos = self.vocabulario.obtener_todos()
        total = len(conceptos)
        
        print(f"\n🧠 Calculando grounding 9D para {total} conceptos...")
        
        for i, concepto in enumerate(conceptos, 1):
            if i % 50 == 0:
                print(f"   Progreso: {i}/{total} ({i*100//total}%)")
            
            grounding_9d = self.calcular_concepto(concepto)
            resultados[concepto.id] = grounding_9d
        
        print(f"✅ Grounding 9D calculado para {len(resultados)} conceptos")
        
        return resultados
    
    def calcular_promedio(self, grounding_9d: Dict[str, float]) -> float:
        """
        Calcula grounding promedio de las 9 dimensiones.
        
        Args:
            grounding_9d: Dict con puntajes de cada dimensión
        
        Returns:
            float: Promedio [0.0-1.0]
        """
        return self.gestor.calcular_promedio(grounding_9d)
    
    def guardar_resultados(
        self, 
        resultados: Dict[str, Dict[str, float]], 
        ruta: str = "grounding_9d.json"
    ):
        """
        Guarda resultados en archivo JSON.
        
        Args:
            resultados: Dict de {concepto_id: grounding_9d}
            ruta: Ruta del archivo de salida
        """
        # Preparar datos serializables
        datos = {
            'timestamp': datetime.now().isoformat(),
            'total_conceptos': len(resultados),
            'dimensiones': self.gestor.listar_dimensiones(),
            'resultados': resultados
        }
        
        # Guardar
        ruta_path = Path(ruta)
        ruta_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(ruta_path, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Resultados guardados en: {ruta}")
    
    def cargar_resultados(self, ruta: str = "grounding_9d.json") -> Dict[str, Dict[str, float]]:
        """
        Carga resultados desde archivo JSON.
        
        Args:
            ruta: Ruta del archivo
        
        Returns:
            Dict de {concepto_id: grounding_9d}
        """
        with open(ruta, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        
        resultados = datos.get('resultados', {})
        
        # Actualizar cache
        self.cache_resultados.update(resultados)
        
        print(f"✅ Cargados {len(resultados)} resultados desde {ruta}")
        
        return resultados
    
    def limpiar_cache(self):
        """Limpia cache de resultados."""
        self.cache_resultados.clear()
        self.gestor.limpiar_caches()
        print("✅ Cache limpiado")
    
    def obtener_estadisticas(self) -> Dict:
        """
        Obtiene estadísticas de uso del calculador.
        
        Returns:
            Dict con estadísticas
        """
        return {
            'conceptos_en_cache': len(self.cache_resultados),
            'dimensiones_activas': len(self.gestor.dimensiones),
            'estadisticas_dimensiones': self.gestor.obtener_estadisticas()
        }


if __name__ == '__main__':
    print("""
╔══════════════════════════════════════════════════════════╗
║         CALCULADOR DE GROUNDING 9D - BELLADONNA         ║
╚══════════════════════════════════════════════════════════╝

Calcula grounding en las 9 dimensiones para conceptos.

Uso:
    from grounding.calculadores.calculador_9d import Calculador9D
    from vocabulario.gestor_vocabulario import GestorVocabulario
    
    # Inicializar
    vocabulario = GestorVocabulario()
    calculador = Calculador9D(vocabulario)
    
    # Calcular todos
    resultados = calculador.calcular_todos()
    
    # Guardar
    calculador.guardar_resultados(resultados, 'grounding_9d.json')
    """)