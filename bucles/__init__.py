"""
Paquete de Bucles Autónomos - Fase 2.

Permite que Bell "piense" en segundo plano, analizando su propio
comportamiento y generando insights.

Componentes:
- BaseBucle: Clase abstracta base
- BucleCorto (60s): Análisis de conceptos recientes
- BucleMedio (120s): Detección de patrones conversacionales
- BucleLargo (600s): Consolidación de aprendizaje
- GestorBucles: Coordinación de todos los bucles
"""
from bucles.base_bucle import BaseBucle
from bucles.bucle_corto import BucleCorto
from bucles.bucle_medio import BucleMedio
from bucles.bucle_largo import BucleLargo
from bucles.gestor_bucles import GestorBucles

__all__ = [
    'BaseBucle',
    'BucleCorto',
    'BucleMedio',
    'BucleLargo',
    'GestorBucles'
]