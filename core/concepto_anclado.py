"""
ConceptoAnclado: La unidad fundamental del conocimiento de Bell.

Un ConceptoAnclado NO es una palabra. Es una estructura computacional
que Bell puede manipular, ejecutar y razonar sobre ella.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, Dict, List, Set, Any, Optional
from core.tipos import TipoConcepto

@dataclass
class ConceptoAnclado:
    """
    Representación de un concepto en el lenguaje interno de Bell.
    
    Bell NO piensa en español. Bell piensa en ConceptosAnclados.
    """
    
    # IDENTIDAD
    id: str  # "CONCEPTO_LEER"
    tipo: TipoConcepto
    palabras_español: List[str]  # ["leer", "read", "cargar"]
    
    # GROUNDING REAL (lo más importante)
    operaciones: Dict[str, Callable] = field(default_factory=dict)
    accesible_directamente: bool = False
    confianza_grounding: float = 0.0
    
    # RELACIONES (estructura del conocimiento)
    relaciones: Dict[str, Set[str]] = field(default_factory=dict)
    
    # PROPIEDADES (conocimiento sobre el concepto)
    propiedades: Dict[str, Any] = field(default_factory=dict)
    
    # DATOS (información variable)
    datos: Dict[str, Any] = field(default_factory=dict)
    
    # METADATA (trazabilidad)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validación después de creación."""
        if not self.id.startswith("CONCEPTO_"):
            raise ValueError(f"ID debe empezar con CONCEPTO_: {self.id}")
        
        if self.confianza_grounding < 0.0 or self.confianza_grounding > 1.0:
            raise ValueError(f"Confianza debe estar entre 0.0 y 1.0: {self.confianza_grounding}")
        
        # Metadata por defecto
        if 'fecha_creacion' not in self.metadata:
            self.metadata['fecha_creacion'] = datetime.now().isoformat()
        if 'veces_usado' not in self.metadata:
            self.metadata['veces_usado'] = 0
    
    def puede_ejecutar(self, operacion: str) -> bool:
        """¿Bell puede ejecutar esta operación?"""
        return operacion in self.operaciones
    
    def ejecutar(self, operacion: str, *args, **kwargs) -> Any:
        """
        Ejecuta una operación del concepto.
        
        Esto es GROUNDING REAL: Bell está haciendo algo tangible.
        """
        if not self.puede_ejecutar(operacion):
            raise ValueError(f"Operación '{operacion}' no disponible en {self.id}")
        
        self.metadata['veces_usado'] += 1
        return self.operaciones[operacion](*args, **kwargs)
    
    def esta_relacionado_con(self, otro_concepto_id: str, tipo_relacion: str = None) -> bool:
        """¿Este concepto está relacionado con otro?"""
        if tipo_relacion:
            return otro_concepto_id in self.relaciones.get(tipo_relacion, set())
        else:
            for relaciones in self.relaciones.values():
                if otro_concepto_id in relaciones:
                    return True
            return False
    
    def obtener_propiedad(self, nombre: str, default=None) -> Any:
        """Obtiene una propiedad del concepto."""
        return self.propiedades.get(nombre, default)
    
    def __repr__(self) -> str:
        return (f"ConceptoAnclado(id={self.id}, tipo={self.tipo.name}, "
                f"grounding={self.confianza_grounding:.2f})")