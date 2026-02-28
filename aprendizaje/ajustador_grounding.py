"""
Ajustador de Grounding - Modifica grounding de conceptos.

Utiliza estrategias de aprendizaje para ajustar el grounding
de conceptos basado en su uso y efectividad.
"""
from typing import Dict, Any, List, Optional
from datetime import datetime

from aprendizaje.estrategias import (
    EstrategiaAprendizaje,
    EstrategiaUsoFrecuente,
    EstrategiaExitoFallido,
    EstrategiaInsights,
    EstrategiaComposite
)

class AjustadorGrounding:
    """
    Ajustador de grounding de conceptos.
    
    Responsabilidades:
    - Calcular nuevos valores de grounding
    - Aplicar estrategias de aprendizaje
    - Registrar historial de ajustes
    - Validar cambios propuestos
    """
    
    def __init__(self, estrategia: Optional[EstrategiaAprendizaje] = None):
        """
        Inicializa ajustador.
        
        Args:
            estrategia: Estrategia de aprendizaje (None = usar por defecto)
        """
        # Usar estrategia por defecto si no se especifica
        if estrategia is None:
            self.estrategia = EstrategiaComposite([
                EstrategiaInsights(),
                EstrategiaUsoFrecuente(umbral_usos=5, incremento=0.05),
                EstrategiaExitoFallido()
            ])
        else:
            self.estrategia = estrategia
        
        # Historial de ajustes
        self.historial_ajustes: List[Dict[str, Any]] = []
        
        # Límites de seguridad
        self.grounding_minimo = 0.1  # Nunca bajar de 0.1
        self.grounding_maximo = 1.0
        self.max_ajuste_por_vez = 0.1  # Máximo cambio de 0.1 por ajuste
    
    def proponer_ajuste(
        self,
        concepto_id: str,
        grounding_actual: float,
        contexto: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Propone un ajuste de grounding.
        
        Args:
            concepto_id: ID del concepto
            grounding_actual: Grounding actual
            contexto: Información para calcular ajuste
        
        Returns:
            Dict con propuesta de ajuste o None
        """
        # Calcular nuevo grounding usando estrategia
        nuevo_grounding = self.estrategia.calcular_ajuste(
            concepto_id,
            grounding_actual,
            contexto
        )
        
        if nuevo_grounding is None:
            return None
        
        # Validar el ajuste propuesto
        if not self._validar_ajuste(grounding_actual, nuevo_grounding):
            return None
        
        # Crear propuesta
        propuesta = {
            'concepto_id': concepto_id,
            'grounding_actual': grounding_actual,
            'grounding_propuesto': nuevo_grounding,
            'cambio': nuevo_grounding - grounding_actual,
            'razon': contexto.get('razon', 'Ajuste automático'),
            'contexto': contexto,
            'timestamp': datetime.now().isoformat()
        }
        
        return propuesta
    
    def aplicar_ajuste(
        self,
        concepto: Any,  # ConceptoAnclado
        propuesta: Dict[str, Any]
    ) -> bool:
        """
        Aplica un ajuste de grounding a un concepto.
        
        Args:
            concepto: Instancia de ConceptoAnclado
            propuesta: Propuesta de ajuste
        
        Returns:
            True si se aplicó correctamente
        """
        try:
            # Verificar que el concepto coincide
            if concepto.id != propuesta['concepto_id']:
                return False
            
            # Aplicar nuevo grounding
            grounding_anterior = concepto.confianza_grounding
            concepto.confianza_grounding = propuesta['grounding_propuesto']
            
            # Registrar en historial
            self._registrar_ajuste(
                concepto_id=concepto.id,
                grounding_anterior=grounding_anterior,
                grounding_nuevo=concepto.confianza_grounding,
                razon=propuesta['razon'],
                aplicado=True
            )
            
            return True
        
        except Exception as e:
            # Registrar fallo
            self._registrar_ajuste(
                concepto_id=propuesta['concepto_id'],
                grounding_anterior=propuesta['grounding_actual'],
                grounding_nuevo=propuesta['grounding_propuesto'],
                razon=f"ERROR: {str(e)}",
                aplicado=False
            )
            return False
    
    def _validar_ajuste(
        self,
        grounding_actual: float,
        grounding_nuevo: float
    ) -> bool:
        """
        Valida que un ajuste sea seguro.
        
        Args:
            grounding_actual: Valor actual
            grounding_nuevo: Valor propuesto
        
        Returns:
            True si el ajuste es válido
        """
        # Verificar límites
        if grounding_nuevo < self.grounding_minimo:
            return False
        if grounding_nuevo > self.grounding_maximo:
            return False
        
        # Verificar que el cambio no sea excesivo
        cambio = abs(grounding_nuevo - grounding_actual)
        if cambio > self.max_ajuste_por_vez:
            return False
        
        # Verificar que haya un cambio real
        if cambio < 0.01:
            return False
        
        return True
    
    def _registrar_ajuste(
        self,
        concepto_id: str,
        grounding_anterior: float,
        grounding_nuevo: float,
        razon: str,
        aplicado: bool
    ):
        """Registra un ajuste en el historial."""
        registro = {
            'concepto_id': concepto_id,
            'grounding_anterior': grounding_anterior,
            'grounding_nuevo': grounding_nuevo,
            'cambio': grounding_nuevo - grounding_anterior,
            'razon': razon,
            'aplicado': aplicado,
            'timestamp': datetime.now().isoformat()
        }
        
        self.historial_ajustes.append(registro)
    
    def obtener_historial(
        self,
        concepto_id: Optional[str] = None,
        solo_aplicados: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Obtiene historial de ajustes.
        
        Args:
            concepto_id: Filtrar por concepto (None = todos)
            solo_aplicados: Solo ajustes aplicados
        
        Returns:
            Lista de ajustes
        """
        ajustes = self.historial_ajustes.copy()
        
        # Filtrar por concepto
        if concepto_id:
            ajustes = [a for a in ajustes if a['concepto_id'] == concepto_id]
        
        # Filtrar por aplicados
        if solo_aplicados:
            ajustes = [a for a in ajustes if a['aplicado']]
        
        return ajustes
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de ajustes.
        
        Returns:
            Dict con estadísticas
        """
        total = len(self.historial_ajustes)
        aplicados = sum(1 for a in self.historial_ajustes if a['aplicado'])
        
        if total == 0:
            return {
                'total_ajustes': 0,
                'ajustes_aplicados': 0,
                'tasa_aplicacion': 0.0,
                'cambio_promedio': 0.0,
                'conceptos_ajustados': 0
            }
        
        cambios = [abs(a['cambio']) for a in self.historial_ajustes if a['aplicado']]
        cambio_promedio = sum(cambios) / len(cambios) if cambios else 0.0
        
        conceptos_unicos = len(set(a['concepto_id'] for a in self.historial_ajustes))
        
        return {
            'total_ajustes': total,
            'ajustes_aplicados': aplicados,
            'tasa_aplicacion': (aplicados / total) * 100,
            'cambio_promedio': cambio_promedio,
            'conceptos_ajustados': conceptos_unicos
        }
    
    def configurar_limites(
        self,
        minimo: Optional[float] = None,
        maximo: Optional[float] = None,
        max_cambio: Optional[float] = None
    ):
        """
        Configura límites de seguridad.
        
        Args:
            minimo: Grounding mínimo permitido
            maximo: Grounding máximo permitido
            max_cambio: Máximo cambio por ajuste
        """
        if minimo is not None:
            self.grounding_minimo = max(0.0, min(1.0, minimo))
        if maximo is not None:
            self.grounding_maximo = max(0.0, min(1.0, maximo))
        if max_cambio is not None:
            self.max_ajuste_por_vez = max(0.0, min(1.0, max_cambio))