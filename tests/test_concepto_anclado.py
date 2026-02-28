"""
Tests para ConceptoAnclado - La clase fundamental.
"""
import pytest
from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto

def test_creacion_concepto_basico():
    """Test: Crear concepto con datos mínimos."""
    concepto = ConceptoAnclado(
        id="CONCEPTO_TEST",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["test"]
    )
    
    assert concepto.id == "CONCEPTO_TEST"
    assert concepto.tipo == TipoConcepto.OPERACION_SISTEMA
    assert concepto.confianza_grounding == 0.0
    assert 'fecha_creacion' in concepto.metadata
    assert concepto.metadata['veces_usado'] == 0

def test_validacion_id_invalido():
    """Test: ID debe empezar con CONCEPTO_."""
    with pytest.raises(ValueError, match="ID debe empezar con CONCEPTO_"):
        ConceptoAnclado(
            id="TEST_INVALIDO",
            tipo=TipoConcepto.OPERACION_SISTEMA,
            palabras_español=["test"]
        )

def test_validacion_grounding_invalido():
    """Test: Grounding debe estar entre 0.0 y 1.0."""
    with pytest.raises(ValueError, match="Confianza debe estar entre"):
        ConceptoAnclado(
            id="CONCEPTO_TEST",
            tipo=TipoConcepto.OPERACION_SISTEMA,
            palabras_español=["test"],
            confianza_grounding=1.5  # Inválido
        )

def test_ejecucion_operacion():
    """Test: Ejecutar operación disponible."""
    concepto = ConceptoAnclado(
        id="CONCEPTO_SUMAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["sumar"],
        operaciones={'ejecutar': lambda a, b: a + b},
        accesible_directamente=True,
        confianza_grounding=1.0
    )
    
    resultado = concepto.ejecutar('ejecutar', 2, 3)
    assert resultado == 5
    assert concepto.metadata['veces_usado'] == 1

def test_operacion_no_disponible():
    """Test: Error al ejecutar operación inexistente."""
    concepto = ConceptoAnclado(
        id="CONCEPTO_TEST",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["test"]
    )
    
    with pytest.raises(ValueError, match="Operación .* no disponible"):
        concepto.ejecutar('operacion_inexistente')

def test_puede_ejecutar():
    """Test: Verificar si puede ejecutar operación."""
    concepto = ConceptoAnclado(
        id="CONCEPTO_TEST",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["test"],
        operaciones={'hacer': lambda: True}
    )
    
    assert concepto.puede_ejecutar('hacer') == True
    assert concepto.puede_ejecutar('inexistente') == False

def test_relaciones_entre_conceptos():
    """Test: Verificar relaciones."""
    concepto = ConceptoAnclado(
        id="CONCEPTO_LEER",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["leer"],
        relaciones={
            'requiere': {'CONCEPTO_ARCHIVO'},
            'relacionado_con': {'CONCEPTO_ESCRIBIR'}
        }
    )
    
    assert concepto.esta_relacionado_con('CONCEPTO_ARCHIVO', 'requiere')
    assert concepto.esta_relacionado_con('CONCEPTO_ESCRIBIR')
    assert not concepto.esta_relacionado_con('CONCEPTO_INEXISTENTE')

def test_obtener_propiedad():
    """Test: Obtener propiedades del concepto."""
    concepto = ConceptoAnclado(
        id="CONCEPTO_TEST",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["test"],
        propiedades={'retorna': 'texto', 'puede_fallar': True}
    )
    
    assert concepto.obtener_propiedad('retorna') == 'texto'
    assert concepto.obtener_propiedad('puede_fallar') == True
    assert concepto.obtener_propiedad('inexistente', 'default') == 'default'

if __name__ == '__main__':
    pytest.main([__file__, '-v'])