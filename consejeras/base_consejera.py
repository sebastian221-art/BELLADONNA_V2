"""
Clase Base para Consejeras - Definición abstracta.

TODAS las consejeras heredan de aquí.
Define interfaz común y comportamiento compartido.
"""
from abc import ABC, abstractmethod
from typing import Dict, Optional
from razonamiento.tipos_decision import Decision

class Consejera(ABC):
    """
    Clase abstracta para consejeras.
    
    Cada consejera especializa en analizar decisiones desde una perspectiva.
    """
    
    def __init__(self, nombre: str, especialidad: str):
        """
        Args:
            nombre: Nombre de la consejera
            especialidad: Área de especialización
        """
        self.nombre = nombre
        self.especialidad = especialidad
        self.activa = True
        
        # Estadísticas
        self.revisiones_realizadas = 0
        self.vetos_aplicados = 0
        self.opiniones_dadas = 0
    
    @abstractmethod
    def revisar(self, decision: Decision, contexto: Dict) -> Dict:
        """
        Revisa una decisión y retorna opinión.
        
        TODAS las consejeras DEBEN implementar este método.
        
        Args:
            decision: Decision del motor de razonamiento
            contexto: Contexto adicional (traducción, etc.)
            
        Returns:
            {
                'consejera': str,           # Nombre de la consejera
                'aprobada': bool,           # ¿Aprueba la decisión?
                'veto': bool,               # ¿Aplica veto? (solo algunas pueden)
                'opinion': str,             # Opinión textual
                'confianza': float,         # Confianza en su análisis (0.0-1.0)
                'razonamiento': List[str],  # Pasos de razonamiento
                'sugerencias': List[str]    # Sugerencias opcionales
            }
        """
        pass
    
    def activar(self):
        """Activa la consejera."""
        self.activa = True
    
    def desactivar(self):
        """Desactiva la consejera."""
        self.activa = False
    
    def registrar_revision(self, aprobada: bool, veto: bool = False):
        """Registra estadística de revisión."""
        self.revisiones_realizadas += 1
        self.opiniones_dadas += 1
        
        if veto:
            self.vetos_aplicados += 1
    
    def estadisticas(self) -> Dict:
        """Retorna estadísticas de la consejera."""
        # Calcular tasa de veto
        if self.revisiones_realizadas > 0:
            tasa_veto = self.vetos_aplicados / self.revisiones_realizadas
        else:
            tasa_veto = 0.0
        
        return {
            'nombre': self.nombre,
            'especialidad': self.especialidad,
            'activa': self.activa,
            'revisiones': self.revisiones_realizadas,
            'vetos': self.vetos_aplicados,
            'opiniones': self.opiniones_dadas,
            'tasa_veto': round(tasa_veto, 2)  # ← AGREGADO
        }
    
    def __repr__(self) -> str:
        return f"<{self.nombre} ({self.especialidad})>"