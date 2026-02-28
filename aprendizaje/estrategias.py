"""
Estrategias de Aprendizaje - Define cómo ajustar grounding.

Diferentes estrategias para ajustar el grounding de conceptos
basado en uso, éxito y patrones detectados.
"""
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

class EstrategiaAprendizaje(ABC):
    """
    Clase base abstracta para estrategias de aprendizaje.
    
    Cada estrategia define cómo calcular ajustes de grounding.
    """
    
    @abstractmethod
    def calcular_ajuste(
        self,
        concepto_id: str,
        grounding_actual: float,
        contexto: Dict[str, Any]
    ) -> Optional[float]:
        """
        Calcula nuevo grounding para un concepto.
        
        Args:
            concepto_id: ID del concepto
            grounding_actual: Grounding actual
            contexto: Información para calcular ajuste
        
        Returns:
            Nuevo grounding o None si no hay ajuste
        """
        pass


class EstrategiaUsoFrecuente(EstrategiaAprendizaje):
    """
    Aumenta grounding de conceptos usados frecuentemente.
    
    Rationale: Si un concepto se usa mucho y funciona,
    debemos confiar más en él.
    """
    
    def __init__(self, umbral_usos: int = 10, incremento: float = 0.05):
        """
        Inicializa estrategia.
        
        Args:
            umbral_usos: Mínimo de usos para ajustar
            incremento: Cuánto aumentar el grounding
        """
        self.umbral_usos = umbral_usos
        self.incremento = incremento
    
    def calcular_ajuste(
        self,
        concepto_id: str,
        grounding_actual: float,
        contexto: Dict[str, Any]
    ) -> Optional[float]:
        """
        Aumenta grounding si el concepto se usa frecuentemente.
        
        contexto debe contener:
        - 'usos': número de veces usado
        - 'tasa_exito': % de usos exitosos (opcional)
        """
        usos = contexto.get('usos', 0)
        
        # Solo ajustar si supera umbral
        if usos < self.umbral_usos:
            return None
        
        # Verificar tasa de éxito si está disponible
        tasa_exito = contexto.get('tasa_exito', 1.0)
        if tasa_exito < 0.7:  # Menos del 70% de éxito
            return None
        
        # Calcular nuevo grounding
        nuevo = min(1.0, grounding_actual + self.incremento)
        
        # Solo ajustar si hay cambio significativo
        if abs(nuevo - grounding_actual) < 0.01:
            return None
        
        return nuevo


class EstrategiaExitoFallido(EstrategiaAprendizaje):
    """
    Ajusta grounding basado en tasa de éxito/fallo.
    
    Aumenta con éxito, disminuye con fallo.
    """
    
    def __init__(
        self,
        incremento_exito: float = 0.03,
        decremento_fallo: float = 0.05
    ):
        """
        Inicializa estrategia.
        
        Args:
            incremento_exito: Cuánto aumentar con éxito
            decremento_fallo: Cuánto disminuir con fallo
        """
        self.incremento_exito = incremento_exito
        self.decremento_fallo = decremento_fallo
    
    def calcular_ajuste(
        self,
        concepto_id: str,
        grounding_actual: float,
        contexto: Dict[str, Any]
    ) -> Optional[float]:
        """
        Ajusta basado en tasa de éxito.
        
        contexto debe contener:
        - 'usos_exitosos': número de usos exitosos
        - 'usos_fallidos': número de usos fallidos
        """
        exitos = contexto.get('usos_exitosos', 0)
        fallos = contexto.get('usos_fallidos', 0)
        total = exitos + fallos
        
        if total == 0:
            return None
        
        tasa_exito = exitos / total
        
        # Decidir ajuste
        if tasa_exito >= 0.8:  # 80%+ de éxito
            nuevo = min(1.0, grounding_actual + self.incremento_exito)
        elif tasa_exito <= 0.4:  # 40%- de éxito
            nuevo = max(0.0, grounding_actual - self.decremento_fallo)
        else:
            return None  # No ajustar en zona media
        
        # Solo ajustar si hay cambio significativo
        if abs(nuevo - grounding_actual) < 0.01:
            return None
        
        return nuevo


class EstrategiaInsights(EstrategiaAprendizaje):
    """
    Ajusta basado en insights del BucleLargo.
    
    Aplica recomendaciones específicas generadas por análisis.
    """
    
    def calcular_ajuste(
        self,
        concepto_id: str,
        grounding_actual: float,
        contexto: Dict[str, Any]
    ) -> Optional[float]:
        """
        Aplica ajuste recomendado por insight.
        
        contexto debe contener:
        - 'ajuste_sugerido': ajuste recomendado (+/-)
        - 'razon': razón del ajuste
        - 'prioridad': prioridad del ajuste
        """
        ajuste = contexto.get('ajuste_sugerido', 0.0)
        
        if ajuste == 0.0:
            return None
        
        # Aplicar ajuste
        nuevo = grounding_actual + ajuste
        nuevo = max(0.0, min(1.0, nuevo))  # Clamp [0, 1]
        
        # Solo ajustar si hay cambio significativo
        if abs(nuevo - grounding_actual) < 0.01:
            return None
        
        return nuevo


class EstrategiaConservadora(EstrategiaAprendizaje):
    """
    Estrategia conservadora: ajustes pequeños y graduales.
    
    Útil cuando no queremos cambios drásticos.
    """
    
    def __init__(self, max_cambio: float = 0.02):
        """
        Inicializa estrategia.
        
        Args:
            max_cambio: Máximo cambio permitido por ajuste
        """
        self.max_cambio = max_cambio
    
    def calcular_ajuste(
        self,
        concepto_id: str,
        grounding_actual: float,
        contexto: Dict[str, Any]
    ) -> Optional[float]:
        """
        Aplica ajuste conservador.
        
        contexto debe contener:
        - 'direccion': 'aumentar' o 'disminuir'
        - 'confianza': confianza en el ajuste (0-1)
        """
        direccion = contexto.get('direccion', '')
        confianza = contexto.get('confianza', 0.5)
        
        if direccion not in ['aumentar', 'disminuir']:
            return None
        
        # Calcular ajuste proporcional a confianza
        cambio = self.max_cambio * confianza
        
        if direccion == 'aumentar':
            nuevo = min(1.0, grounding_actual + cambio)
        else:
            nuevo = max(0.0, grounding_actual - cambio)
        
        # Solo ajustar si hay cambio significativo
        if abs(nuevo - grounding_actual) < 0.005:
            return None
        
        return nuevo


class EstrategiaComposite(EstrategiaAprendizaje):
    """
    Combina múltiples estrategias.
    
    Aplica la primera estrategia que genere un ajuste.
    """
    
    def __init__(self, estrategias: list[EstrategiaAprendizaje]):
        """
        Inicializa con lista de estrategias.
        
        Args:
            estrategias: Lista de estrategias a aplicar en orden
        """
        self.estrategias = estrategias
    
    def calcular_ajuste(
        self,
        concepto_id: str,
        grounding_actual: float,
        contexto: Dict[str, Any]
    ) -> Optional[float]:
        """
        Aplica la primera estrategia que genere ajuste.
        """
        for estrategia in self.estrategias:
            ajuste = estrategia.calcular_ajuste(
                concepto_id,
                grounding_actual,
                contexto
            )
            if ajuste is not None:
                return ajuste
        
        return None