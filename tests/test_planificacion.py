"""
Tests para Motor de Planificación y Ejecutor.
FASE 3 - Tests de planificación multi-paso.
"""

import pytest
from pathlib import Path
import sys

# Importar módulos
proyecto_path = Path(__file__).parent.parent
sys.path.insert(0, str(proyecto_path))

from planificacion.motor_planificacion import (
    MotorPlanificacion,
    Plan,
    Paso,
    EstadoPaso
)
from planificacion.ejecutor_planes import (
    EjecutorPlanes,
    ResultadoEjecucion
)


class TestMotorPlanificacion:
    """Tests del motor de planificación."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.motor = MotorPlanificacion()
    
    def test_crear_plan_simple(self):
        """Test: crear plan con pasos simples."""
        pasos = [
            {"descripcion": "Paso 1", "accion": "accion1"},
            {"descripcion": "Paso 2", "accion": "accion2"}
        ]
        
        plan = self.motor.crear_plan("Objetivo test", pasos)
        
        assert plan is not None
        assert plan.objetivo == "Objetivo test"
        assert len(plan.pasos) == 2
        assert plan.estado == "creado"
    
    def test_crear_plan_con_dependencias(self):
        """Test: crear plan con dependencias."""
        pasos = [
            {"descripcion": "Paso 1", "accion": "accion1"},
            {"descripcion": "Paso 2", "accion": "accion2",
             "dependencias": ["paso_1"]}
        ]
        
        plan = self.motor.crear_plan("Test", pasos)
        
        assert len(plan.pasos) == 2
        assert plan.pasos[1].dependencias == ["paso_1"]
    
    def test_registrar_accion(self):
        """Test: registrar acción."""
        def mi_accion(ctx):
            return "resultado"
        
        self.motor.registrar_accion("mi_accion", mi_accion)
        
        assert "mi_accion" in self.motor.acciones_disponibles
    
    def test_obtener_siguiente_paso(self):
        """Test: obtener siguiente paso ejecutable."""
        pasos = [
            {"descripcion": "Paso 1", "accion": "accion1"},
            {"descripcion": "Paso 2", "accion": "accion2"}
        ]
        
        plan = self.motor.crear_plan("Test", pasos)
        siguiente = self.motor.obtener_siguiente_paso(plan)
        
        assert siguiente is not None
        assert siguiente.id == "paso_1"


class TestValidacionPlanes:
    """Tests de validación de planes."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.motor = MotorPlanificacion()
        self.motor.registrar_accion("accion1", lambda ctx: "ok")
    
    def test_validar_plan_correcto(self):
        """Test: validar plan correcto."""
        pasos = [
            {"descripcion": "Paso 1", "accion": "accion1"}
        ]
        
        plan = self.motor.crear_plan("Test", pasos)
        valido, errores = self.motor.validar_plan(plan)
        
        assert valido is True
        assert len(errores) == 0
    
    def test_validar_plan_sin_pasos(self):
        """Test: validar plan sin pasos."""
        plan = self.motor.crear_plan("Test", [])
        valido, errores = self.motor.validar_plan(plan)
        
        assert valido is False
        assert "no tiene pasos" in errores[0]
    
    def test_validar_accion_inexistente(self):
        """Test: validar con acción no registrada."""
        pasos = [
            {"descripcion": "Paso 1", "accion": "accion_inexistente"}
        ]
        
        plan = self.motor.crear_plan("Test", pasos)
        valido, errores = self.motor.validar_plan(plan)
        
        assert valido is False
        assert any("no disponible" in e for e in errores)
    
    def test_validar_dependencia_inexistente(self):
        """Test: validar con dependencia inexistente."""
        pasos = [
            {"descripcion": "Paso 1", "accion": "accion1",
             "dependencias": ["paso_inexistente"]}
        ]
        
        plan = self.motor.crear_plan("Test", pasos)
        valido, errores = self.motor.validar_plan(plan)
        
        assert valido is False


class TestDependencias:
    """Tests de manejo de dependencias."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.motor = MotorPlanificacion()
    
    def test_ordenar_por_dependencias(self):
        """Test: ordenar pasos respetando dependencias."""
        pasos = [
            {"descripcion": "Paso 2", "accion": "accion2",
             "dependencias": ["paso_1"]},
            {"descripcion": "Paso 1", "accion": "accion1"}
        ]
        
        plan = self.motor.crear_plan("Test", pasos)
        
        # El paso 1 debe estar antes que el paso 2
        paso_ids = [p.id for p in plan.pasos]
        assert paso_ids.index("paso_1") < paso_ids.index("paso_2")
    
    def test_detectar_ciclos(self):
        """Test: detectar dependencias cíclicas."""
        paso1 = Paso(id="paso_1", descripcion="Paso 1", 
                     accion="a1", dependencias=["paso_2"])
        paso2 = Paso(id="paso_2", descripcion="Paso 2",
                     accion="a2", dependencias=["paso_1"])
        
        tiene_ciclos = self.motor._tiene_ciclos([paso1, paso2])
        
        assert tiene_ciclos is True


class TestEjecutorPlanes:
    """Tests del ejecutor de planes."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.motor = MotorPlanificacion()
        self.ejecutor = EjecutorPlanes(self.motor)
        
        # Registrar acciones de prueba
        self.motor.registrar_accion("sumar", lambda ctx: 5)
        self.motor.registrar_accion("multiplicar", lambda ctx: 10)
    
    def test_ejecutar_plan_simple(self):
        """Test: ejecutar plan simple."""
        pasos = [
            {"descripcion": "Sumar", "accion": "sumar"}
        ]
        
        plan = self.motor.crear_plan("Test", pasos)
        resultado = self.ejecutor.ejecutar_plan(plan)
        
        assert resultado.exitoso is True
        assert resultado.pasos_ejecutados == 1
        assert resultado.pasos_fallidos == 0
    
    def test_ejecutar_plan_con_dependencias(self):
        """Test: ejecutar plan con dependencias."""
        pasos = [
            {"descripcion": "Sumar", "accion": "sumar"},
            {"descripcion": "Multiplicar", "accion": "multiplicar",
             "dependencias": ["paso_1"]}
        ]
        
        plan = self.motor.crear_plan("Test", pasos)
        resultado = self.ejecutor.ejecutar_plan(plan)
        
        assert resultado.exitoso is True
        assert resultado.pasos_ejecutados == 2
    
    def test_ejecutar_paso_individual(self):
        """Test: ejecutar un paso individual."""
        pasos = [
            {"descripcion": "Sumar", "accion": "sumar"}
        ]
        
        plan = self.motor.crear_plan("Test", pasos)
        paso = plan.pasos[0]
        
        resultado = self.ejecutor.ejecutar_paso(plan, paso)
        
        assert resultado['exitoso'] is True
        assert resultado['resultado'] == 5
    
    def test_manejar_error_en_paso(self):
        """Test: manejar error en un paso."""
        def accion_error(ctx):
            raise Exception("Error de prueba")
        
        self.motor.registrar_accion("error", accion_error)
        
        pasos = [
            {"descripcion": "Error", "accion": "error"}
        ]
        
        plan = self.motor.crear_plan("Test", pasos)
        resultado = self.ejecutor.ejecutar_plan(plan)
        
        assert resultado.exitoso is False
        assert resultado.pasos_fallidos == 1


class TestEstados:
    """Tests de estados de pasos."""
    
    def test_estado_inicial(self):
        """Test: estado inicial de un paso."""
        paso = Paso(id="paso_1", descripcion="Test", accion="test")
        
        assert paso.estado == EstadoPaso.PENDIENTE
    
    def test_cambio_estado_completado(self):
        """Test: cambiar estado a completado."""
        paso = Paso(id="paso_1", descripcion="Test", accion="test")
        paso.estado = EstadoPaso.COMPLETADO
        
        assert paso.estado == EstadoPaso.COMPLETADO
    
    def test_pasos_completados(self):
        """Test: obtener pasos completados."""
        motor = MotorPlanificacion()
        pasos = [
            {"descripcion": "Paso 1", "accion": "a1"},
            {"descripcion": "Paso 2", "accion": "a2"}
        ]
        
        plan = motor.crear_plan("Test", pasos)
        plan.pasos[0].estado = EstadoPaso.COMPLETADO
        
        completados = plan.pasos_completados()
        
        assert len(completados) == 1
        assert completados[0].id == "paso_1"


class TestProgreso:
    """Tests de progreso del plan."""
    
    def test_progreso_inicial(self):
        """Test: progreso inicial es 0."""
        motor = MotorPlanificacion()
        plan = motor.crear_plan("Test", [
            {"descripcion": "Paso 1", "accion": "a1"}
        ])
        
        assert plan.progreso == 0.0
    
    def test_actualizar_progreso(self):
        """Test: actualizar progreso del plan."""
        motor = MotorPlanificacion()
        plan = motor.crear_plan("Test", [
            {"descripcion": "Paso 1", "accion": "a1"},
            {"descripcion": "Paso 2", "accion": "a2"}
        ])
        
        plan.pasos[0].estado = EstadoPaso.COMPLETADO
        plan.actualizar_progreso()
        
        assert plan.progreso == 50.0


class TestOptimizacion:
    """Tests de optimización de planes."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.motor = MotorPlanificacion()
    
    def test_optimizar_plan(self):
        """Test: optimizar plan eliminando duplicados."""
        pasos = [
            {"descripcion": "Paso 1", "accion": "accion1"},
            {"descripcion": "Paso 1", "accion": "accion1"}  # Duplicado
        ]
        
        plan = self.motor.crear_plan("Test", pasos)
        plan_optimizado = self.motor.optimizar_plan(plan)
        
        assert len(plan_optimizado.pasos) == 1
    
    def test_estimar_tiempo(self):
        """
        Test: estimar tiempo de ejecución.
        
        CORREGIDO: Con el camino crítico, 2 pasos sin dependencias 
        pueden ejecutarse en paralelo, entonces el tiempo es el máximo
        de un solo paso, no la suma.
        """
        pasos = [
            {"descripcion": "Paso 1", "accion": "a1"},
            {"descripcion": "Paso 2", "accion": "a2"}  # Sin dependencias
        ]
        
        plan = self.motor.crear_plan("Test", pasos)
        tiempo = self.motor.estimar_tiempo(plan, tiempo_por_paso=2.0)
        
        # Sin dependencias, pueden correr en paralelo = 2.0 (no 4.0)
        assert tiempo == 2.0
    
    def test_identificar_pasos_paralelos(self):
        """Test: identificar pasos que pueden ejecutarse en paralelo."""
        pasos = [
            {"descripcion": "Paso 1", "accion": "a1"},
            {"descripcion": "Paso 2", "accion": "a2"}  # Sin dependencias
        ]
        
        plan = self.motor.crear_plan("Test", pasos)
        grupos = self.motor.puede_ejecutar_en_paralelo(plan)
        
        assert len(grupos) > 0


class TestResumen:
    """Tests de generación de resumen."""
    
    def test_generar_resumen(self):
        """Test: generar resumen del plan."""
        motor = MotorPlanificacion()
        motor.registrar_accion("a1", lambda ctx: "ok")
        
        pasos = [
            {"descripcion": "Paso 1", "accion": "a1"}
        ]
        
        plan = motor.crear_plan("Test objetivo", pasos)
        resumen = motor.generar_resumen(plan)
        
        assert "Test objetivo" in resumen
        assert "Paso 1" in resumen
    
    def test_resumen_con_estados(self):
        """Test: resumen muestra estados de pasos."""
        motor = MotorPlanificacion()
        plan = motor.crear_plan("Test", [
            {"descripcion": "Paso 1", "accion": "a1"}
        ])
        
        plan.pasos[0].estado = EstadoPaso.COMPLETADO
        resumen = motor.generar_resumen(plan)
        
        assert "✅" in resumen


class TestDryRun:
    """Tests de ejecución en modo dry-run."""
    
    def test_modo_dry_run(self):
        """Test: ejecutar en modo dry-run."""
        motor = MotorPlanificacion()
        ejecutor = EjecutorPlanes(motor)
        
        motor.registrar_accion("a1", lambda ctx: "resultado")
        
        pasos = [
            {"descripcion": "Paso 1", "accion": "a1"}
        ]
        
        plan = motor.crear_plan("Test", pasos)
        
        ejecutor.modo_dry_run = True
        resultado = ejecutor.ejecutar_plan(plan)
        
        assert resultado.exitoso is True
        # El paso no se ejecutó realmente
        assert "DRY_RUN" in str(resultado.resultados.get("paso_1", ""))


if __name__ == '__main__':
    # Ejecutar tests
    pytest.main([__file__, '-v', '--tb=short'])