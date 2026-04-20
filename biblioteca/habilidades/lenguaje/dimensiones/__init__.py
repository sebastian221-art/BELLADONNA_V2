# biblioteca/habilidades/lenguaje/dimensiones/__init__.py
from .base        import DimensionLenguaje, ResultadoDimension
from .literal     import DimensionLiteral
from .inferencial import DimensionInferencial
from .psicologica import DimensionPsicologica
from .tecnica     import DimensionTecnica
from .contextual  import DimensionContextual, DimensionIntrinseca

__all__ = [
    'DimensionLenguaje', 'ResultadoDimension',
    'DimensionLiteral', 'DimensionInferencial',
    'DimensionPsicologica', 'DimensionTecnica',
    'DimensionContextual', 'DimensionIntrinseca',
]