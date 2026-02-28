"""
Generador de Reportes de Grounding.

Genera informes del estado de grounding de Bell en todas sus dimensiones.
Honestidad radical: nunca inventa datos.

Fase 3 → Fase 4 Refactorización
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime


# ==================== ESTRUCTURAS DE DATOS ====================

@dataclass
class EstadoDimension:
    """Estado de una dimensión individual de grounding."""
    nombre: str
    score: float
    activa: bool
    descripcion: str = ""
    
    @property
    def nivel(self) -> str:
        """Nivel de grounding en esta dimensión."""
        if self.score == 0.0:
            return "INACTIVA"
        if self.score < 0.4:
            return "BAJA"
        if self.score < 0.7:
            return "MEDIA"
        if self.score < 0.9:
            return "ALTA"
        return "MAXIMA"
    
    def __repr__(self):
        return (
            f"EstadoDimension({self.nombre}, "
            f"score={self.score:.2f}, nivel={self.nivel})"
        )


@dataclass
class ReporteConcepto:
    """
    Reporte completo de grounding para un concepto.
    
    Contiene scores por dimensión, score total, salud general
    y recomendaciones de mejora.
    """
    concepto_id: str
    dimensiones: List[EstadoDimension]
    score_total: float
    dimensiones_activas: int
    timestamp: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )
    
    @property
    def salud(self) -> str:
        """Estado de salud general del concepto."""
        if self.score_total >= 0.85:
            return "EXCELENTE"
        if self.score_total >= 0.65:
            return "BUENA"
        if self.score_total >= 0.40:
            return "REGULAR"
        if self.score_total > 0.0:
            return "DEFICIENTE"
        return "SIN_GROUNDING"
    
    @property
    def dimensiones_inactivas(self) -> List[str]:
        """Lista de dimensiones inactivas."""
        return [d.nombre for d in self.dimensiones if not d.activa]
    
    @property
    def dimension_mas_debil(self) -> Optional[EstadoDimension]:
        """Dimensión con menor score."""
        activas = [d for d in self.dimensiones if d.activa]
        return min(activas, key=lambda d: d.score) if activas else None
    
    @property
    def dimension_mas_fuerte(self) -> Optional[EstadoDimension]:
        """Dimensión con mayor score."""
        activas = [d for d in self.dimensiones if d.activa]
        return max(activas, key=lambda d: d.score) if activas else None
    
    def recomendaciones(self) -> List[str]:
        """Lista de acciones para mejorar el grounding."""
        recs = []
        
        for d in self.dimensiones:
            if not d.activa:
                recs.append(
                    f"Activar dimensión '{d.nombre}' para aumentar cobertura."
                )
            elif d.score < 0.4:
                recs.append(
                    f"Reforzar dimensión '{d.nombre}' (score={d.score:.2f}). "
                    f"{d.descripcion}"
                )
        
        if self.score_total < 0.5:
            recs.append(
                "Score total bajo. Priorizar dimensiones computacional y semántica."
            )
        
        return recs
    
    def __repr__(self):
        return (
            f"ReporteConcepto({self.concepto_id}, "
            f"score={self.score_total:.2f}, "
            f"salud={self.salud}, "
            f"dims={self.dimensiones_activas}/9)"
        )


@dataclass
class ReporteSistema:
    """
    Reporte agregado de todos los conceptos del sistema.
    """
    reportes: List[ReporteConcepto]
    timestamp: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )
    
    @property
    def total_conceptos(self) -> int:
        return len(self.reportes)
    
    @property
    def score_promedio(self) -> float:
        if not self.reportes:
            return 0.0
        return round(
            sum(r.score_total for r in self.reportes) / len(self.reportes), 3
        )
    
    @property
    def conceptos_excelentes(self) -> List[ReporteConcepto]:
        return [r for r in self.reportes if r.salud == "EXCELENTE"]
    
    @property
    def conceptos_deficientes(self) -> List[ReporteConcepto]:
        return [
            r for r in self.reportes 
            if r.salud in ("DEFICIENTE", "SIN_GROUNDING")
        ]
    
    def distribucion_salud(self) -> Dict[str, int]:
        """Distribución de conceptos por salud."""
        dist = {
            "EXCELENTE": 0,
            "BUENA": 0,
            "REGULAR": 0,
            "DEFICIENTE": 0,
            "SIN_GROUNDING": 0,
        }
        
        for r in self.reportes:
            dist[r.salud] += 1
        
        return dist
    
    def dimension_mas_debil_global(self) -> Optional[str]:
        """Nombre de la dimensión con menor promedio global."""
        if not self.reportes or not self.reportes[0].dimensiones:
            return None
        
        n_dims = len(self.reportes[0].dimensiones)
        sumas = [0.0] * n_dims
        
        for r in self.reportes:
            for i, d in enumerate(r.dimensiones):
                sumas[i] += d.score
        
        idx_min = sumas.index(min(sumas))
        return self.reportes[0].dimensiones[idx_min].nombre
    
    def resumen_texto(self) -> str:
        """Genera un resumen legible del estado del sistema."""
        dist = self.distribucion_salud()
        
        lineas = [
            f"╔══════════════════════════════════════════",
            f"║  REPORTE DE GROUNDING — BELLADONNA",
            f"║  {self.timestamp[:19]}",
            f"╠══════════════════════════════════════════",
            f"║  Conceptos: {self.total_conceptos}",
            f"║  Score promedio: {self.score_promedio:.3f}",
            f"╠──────────────────────────────────────────",
            f"║  Distribución de salud:",
        ]
        
        for estado, cantidad in dist.items():
            pct = (
                (cantidad / self.total_conceptos * 100) 
                if self.total_conceptos else 0
            )
            lineas.append(
                f"║    {estado:<15} {cantidad:>4}  ({pct:5.1f}%)"
            )
        
        debil = self.dimension_mas_debil_global()
        if debil:
            lineas.append(f"╠──────────────────────────────────────────")
            lineas.append(f"║  Dimensión más débil: {debil}")
        
        lineas.append(f"╚══════════════════════════════════════════")
        
        return "\n".join(lineas)
    
    def __repr__(self):
        return (
            f"ReporteSistema({self.total_conceptos} conceptos, "
            f"score_prom={self.score_promedio:.2f})"
        )


# ==================== GENERADOR DE REPORTES ====================

class GeneradorReporteGrounding:
    """
    Genera ReporteConcepto y ReporteSistema.
    
    Uso:
        generador = GeneradorReporteGrounding(calculador_9d)
        
        # Un concepto
        reporte = generador.generar_para_concepto(concepto)
        print(reporte.salud)
        
        # Todo el sistema
        reporte_sistema = generador.generar_para_sistema(conceptos)
        print(reporte_sistema.resumen_texto())
    """
    
    _DIMENSIONES_META = [
        ("computacional",  "Conexión directa con operaciones ejecutables."),
        ("semantico",      "Comprensión del significado y similitudes."),
        ("contextual",     "Aprendizaje de cuándo y cómo usar el concepto."),
        ("pragmatico",     "Pre/postcondiciones y affordances verificados."),
        ("social",         "Adecuación al rol y contexto del usuario."),
        ("temporal",       "Vigencia y caducidad del conocimiento."),
        ("causal",         "Relaciones causa-efecto y riesgos asociados."),
        ("metacognitivo",  "Trazado de decisiones y auto-explicación."),
        ("predictivo",     "Historial de éxitos/fallos y predicciones."),
    ]
    
    def __init__(self, calculador_9d):
        """
        Inicializa generador.
        
        Args:
            calculador_9d: Instancia de Calculador9D
        """
        self.calculador = calculador_9d
    
    def generar_para_concepto(self, concepto: Any) -> ReporteConcepto:
        """
        Genera reporte completo para un concepto.
        
        Args:
            concepto: ConceptoAnclado a evaluar
        
        Returns:
            ReporteConcepto con scores de todas las dimensiones
        """
        # Calcular grounding 9D
        grounding_9d = self.calculador.calcular_concepto(concepto)
        
        # Crear estados de dimensiones
        dimensiones = [
            EstadoDimension(
                nombre=nombre,
                score=grounding_9d.get(nombre, 0.0),
                activa=grounding_9d.get(nombre, 0.0) > 0.0,
                descripcion=desc,
            )
            for nombre, desc in self._DIMENSIONES_META
        ]
        
        # Contar activas
        activas = sum(1 for d in dimensiones if d.activa)
        
        # Score total
        score_total = self.calculador.calcular_promedio(grounding_9d)
        
        return ReporteConcepto(
            concepto_id=concepto.id,
            dimensiones=dimensiones,
            score_total=score_total,
            dimensiones_activas=activas,
        )
    
    def generar_para_sistema(self, conceptos: List[Any]) -> ReporteSistema:
        """
        Genera ReporteSistema para lista de conceptos.
        
        Args:
            conceptos: Lista de ConceptoAnclado
        
        Returns:
            ReporteSistema con todos los reportes agregados
        """
        reportes = [self.generar_para_concepto(c) for c in conceptos]
        return ReporteSistema(reportes=reportes)


if __name__ == '__main__':
    print("""
╔══════════════════════════════════════════════════════════╗
║     GENERADOR DE REPORTES - BELLADONNA                  ║
╚══════════════════════════════════════════════════════════╝

Genera reportes de grounding para conceptos y sistema completo.

Uso:
    from grounding.reportes import GeneradorReporteGrounding
    from grounding.calculadores import Calculador9D
    
    # Inicializar
    calculador = Calculador9D(vocabulario)
    generador = GeneradorReporteGrounding(calculador)
    
    # Generar reporte
    reporte = generador.generar_para_concepto(concepto)
    print(reporte.salud)
    print(reporte.recomendaciones())
    
    # Reporte del sistema
    reporte_sistema = generador.generar_para_sistema(conceptos)
    print(reporte_sistema.resumen_texto())
    """)