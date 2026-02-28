"""
Ejecutor de Planes Multi-Paso.
FASE 3 - Semana 6
"""

from typing import Dict, Callable, Optional, Any
from dataclasses import dataclass
import time
from .motor_planificacion import Plan, Paso, EstadoPaso, MotorPlanificacion


@dataclass
class ResultadoEjecucion:
    """Resultado de ejecutar un plan."""
    plan_id: str
    exitoso: bool
    pasos_ejecutados: int
    pasos_fallidos: int
    tiempo_total: float
    resultados: Dict[str, Any]
    errores: Dict[str, str]


class EjecutorPlanes:
    """
    Ejecutor para planes multi-paso.
    
    Capacidades:
    - Ejecutar planes paso a paso
    - Manejar errores en pasos
    - Ejecutar pasos en paralelo (simulado)
    - Rollback en caso de error
    - Logging de ejecución
    """
    
    def __init__(self, motor: MotorPlanificacion):
        """
        Inicializa el ejecutor.
        
        Args:
            motor: Motor de planificación
        """
        self.motor = motor
        self.log_ejecucion: list = []
        self.modo_dry_run = False
    
    def ejecutar_plan(
        self,
        plan: Plan,
        detener_en_error: bool = True
    ) -> ResultadoEjecucion:
        """
        Ejecuta un plan completo.
        
        Args:
            plan: Plan a ejecutar
            detener_en_error: Si detener al primer error
            
        Returns:
            ResultadoEjecucion
        """
        # Validar plan
        valido, errores = self.motor.validar_plan(plan)
        if not valido:
            return ResultadoEjecucion(
                plan_id=plan.id,
                exitoso=False,
                pasos_ejecutados=0,
                pasos_fallidos=0,
                tiempo_total=0.0,
                resultados={},
                errores={"validacion": str(errores)}
            )
        
        tiempo_inicio = time.time()
        plan.estado = "ejecutando"
        
        resultados = {}
        errores_ejecucion = {}
        pasos_ejecutados = 0
        pasos_fallidos = 0
        
        self._log(f"Iniciando ejecución del plan: {plan.objetivo}")
        
        # Ejecutar pasos en orden
        while True:
            siguiente_paso = self.motor.obtener_siguiente_paso(plan)
            
            if not siguiente_paso:
                break  # No hay más pasos ejecutables
            
            # Ejecutar paso
            resultado_paso = self.ejecutar_paso(plan, siguiente_paso)
            
            if resultado_paso['exitoso']:
                siguiente_paso.estado = EstadoPaso.COMPLETADO
                siguiente_paso.resultado = resultado_paso['resultado']
                resultados[siguiente_paso.id] = resultado_paso['resultado']
                pasos_ejecutados += 1
                self._log(f"✅ Paso completado: {siguiente_paso.descripcion}")
            else:
                siguiente_paso.estado = EstadoPaso.FALLIDO
                siguiente_paso.error = resultado_paso['error']
                errores_ejecucion[siguiente_paso.id] = resultado_paso['error']
                pasos_fallidos += 1
                self._log(f"❌ Paso fallido: {siguiente_paso.descripcion}")
                
                if detener_en_error:
                    self._log("Deteniendo ejecución por error")
                    break
            
            plan.actualizar_progreso()
        
        tiempo_total = time.time() - tiempo_inicio
        
        # Determinar si fue exitoso
        exitoso = (pasos_fallidos == 0 and 
                  len(plan.pasos_completados()) == len(plan.pasos))
        
        plan.estado = "completado" if exitoso else "fallido"
        
        self._log(f"Ejecución finalizada en {tiempo_total:.2f}s")
        
        return ResultadoEjecucion(
            plan_id=plan.id,
            exitoso=exitoso,
            pasos_ejecutados=pasos_ejecutados,
            pasos_fallidos=pasos_fallidos,
            tiempo_total=tiempo_total,
            resultados=resultados,
            errores=errores_ejecucion
        )
    
    def ejecutar_paso(
        self,
        plan: Plan,
        paso: Paso
    ) -> Dict[str, Any]:
        """
        Ejecuta un paso individual.
        
        Args:
            plan: Plan al que pertenece
            paso: Paso a ejecutar
            
        Returns:
            Dict con resultado
        """
        self._log(f"Ejecutando paso: {paso.descripcion}")
        
        if self.modo_dry_run:
            self._log("  (Modo dry-run, no se ejecuta realmente)")
            return {
                'exitoso': True,
                'resultado': f"DRY_RUN: {paso.accion}",
                'error': None
            }
        
        paso.estado = EstadoPaso.EN_PROGRESO
        
        try:
            # Obtener función de la acción
            accion_fn = self.motor.acciones_disponibles.get(paso.accion)
            
            if not accion_fn:
                raise Exception(f"Acción '{paso.accion}' no registrada")
            
            # Preparar contexto de ejecución
            contexto = {
                'plan': plan,
                'paso': paso,
                'resultados_previos': {
                    p.id: p.resultado 
                    for p in plan.pasos_completados()
                }
            }
            
            # Ejecutar acción
            if paso.parametros:
                resultado = accion_fn(contexto, **paso.parametros)
            else:
                resultado = accion_fn(contexto)
            
            return {
                'exitoso': True,
                'resultado': resultado,
                'error': None
            }
            
        except Exception as e:
            return {
                'exitoso': False,
                'resultado': None,
                'error': str(e)
            }
    
    def ejecutar_paralelo(self, plan: Plan) -> ResultadoEjecucion:
        """
        Ejecuta pasos que pueden correr en paralelo.
        
        Nota: Simulado, no usa threads reales.
        
        Args:
            plan: Plan a ejecutar
            
        Returns:
            ResultadoEjecucion
        """
        grupos = self.motor.puede_ejecutar_en_paralelo(plan)
        
        self._log(f"Ejecutando en paralelo: {len(grupos)} grupos")
        
        tiempo_inicio = time.time()
        resultados = {}
        errores_ejecucion = {}
        pasos_ejecutados = 0
        pasos_fallidos = 0
        
        for i, grupo in enumerate(grupos, 1):
            self._log(f"Grupo {i}: {len(grupo)} pasos")
            
            # Simular ejecución paralela
            for paso in grupo:
                resultado_paso = self.ejecutar_paso(plan, paso)
                
                if resultado_paso['exitoso']:
                    paso.estado = EstadoPaso.COMPLETADO
                    paso.resultado = resultado_paso['resultado']
                    resultados[paso.id] = resultado_paso['resultado']
                    pasos_ejecutados += 1
                else:
                    paso.estado = EstadoPaso.FALLIDO
                    paso.error = resultado_paso['error']
                    errores_ejecucion[paso.id] = resultado_paso['error']
                    pasos_fallidos += 1
        
        tiempo_total = time.time() - tiempo_inicio
        exitoso = pasos_fallidos == 0
        
        return ResultadoEjecucion(
            plan_id=plan.id,
            exitoso=exitoso,
            pasos_ejecutados=pasos_ejecutados,
            pasos_fallidos=pasos_fallidos,
            tiempo_total=tiempo_total,
            resultados=resultados,
            errores=errores_ejecucion
        )
    
    def rollback_plan(self, plan: Plan) -> bool:
        """
        Revierte los pasos ejecutados de un plan.
        
        Args:
            plan: Plan a revertir
            
        Returns:
            True si el rollback fue exitoso
        """
        self._log(f"Iniciando rollback del plan: {plan.objetivo}")
        
        # Revertir en orden inverso
        pasos_revertir = plan.pasos_completados()
        pasos_revertir.reverse()
        
        for paso in pasos_revertir:
            # Buscar acción de rollback
            accion_rollback = f"{paso.accion}_rollback"
            rollback_fn = self.motor.acciones_disponibles.get(accion_rollback)
            
            if rollback_fn:
                try:
                    self._log(f"Revirtiendo: {paso.descripcion}")
                    rollback_fn(paso.resultado)
                    paso.estado = EstadoPaso.PENDIENTE
                    paso.resultado = None
                except Exception as e:
                    self._log(f"Error en rollback: {e}")
                    return False
            else:
                self._log(f"No hay rollback para: {paso.accion}")
        
        plan.estado = "revertido"
        plan.actualizar_progreso()
        
        return True
    
    def ejecutar_con_reintentos(
        self,
        plan: Plan,
        paso: Paso,
        max_intentos: int = 3
    ) -> Dict[str, Any]:
        """
        Ejecuta un paso con reintentos.
        
        Args:
            plan: Plan
            paso: Paso a ejecutar
            max_intentos: Número máximo de intentos
            
        Returns:
            Resultado de ejecución
        """
        for intento in range(1, max_intentos + 1):
            self._log(f"Intento {intento}/{max_intentos}: {paso.descripcion}")
            
            resultado = self.ejecutar_paso(plan, paso)
            
            if resultado['exitoso']:
                return resultado
            
            if intento < max_intentos:
                self._log(f"Reintentando en 1 segundo...")
                time.sleep(1)
        
        return resultado
    
    def simular_ejecucion(self, plan: Plan) -> Dict[str, Any]:
        """
        Simula la ejecución de un plan sin ejecutar.
        
        Args:
            plan: Plan a simular
            
        Returns:
            Dict con estadísticas de la simulación
        """
        self.modo_dry_run = True
        
        resultado = self.ejecutar_plan(plan, detener_en_error=False)
        
        self.modo_dry_run = False
        
        # Resetear estados
        for paso in plan.pasos:
            paso.estado = EstadoPaso.PENDIENTE
            paso.resultado = None
            paso.error = None
        
        plan.estado = "creado"
        plan.progreso = 0.0
        
        return {
            'tiempo_estimado': resultado.tiempo_total,
            'pasos_totales': len(plan.pasos),
            'validacion_exitosa': True
        }
    
    def _log(self, mensaje: str):
        """Agrega mensaje al log."""
        timestamp = time.strftime("%H:%M:%S")
        entrada = f"[{timestamp}] {mensaje}"
        self.log_ejecucion.append(entrada)
        print(entrada)
    
    def obtener_log(self) -> str:
        """Retorna el log completo."""
        return '\n'.join(self.log_ejecucion)
    
    def limpiar_log(self):
        """Limpia el log de ejecución."""
        self.log_ejecucion = []


# Ejemplo de uso
if __name__ == '__main__':
    from motor_planificacion import MotorPlanificacion
    
    # Crear motor
    motor = MotorPlanificacion()
    
    # Registrar acciones
    def accion_analizar(ctx):
        return {"archivos_analizados": 10, "errores_encontrados": 3}
    
    def accion_corregir(ctx):
        errores = ctx['resultados_previos'].get('paso_1', {}).get('errores_encontrados', 0)
        return {"errores_corregidos": errores}
    
    motor.registrar_accion("analizar", accion_analizar)
    motor.registrar_accion("corregir", accion_corregir)
    
    # Crear plan
    pasos = [
        {"descripcion": "Analizar código", "accion": "analizar"},
        {"descripcion": "Corregir errores", "accion": "corregir", 
         "dependencias": ["paso_1"]}
    ]
    
    plan = motor.crear_plan("Mejorar código", pasos)
    
    # Ejecutar
    ejecutor = EjecutorPlanes(motor)
    resultado = ejecutor.ejecutar_plan(plan)
    
    print(f"\n✅ Ejecución {'exitosa' if resultado.exitoso else 'fallida'}")
    print(f"Pasos ejecutados: {resultado.pasos_ejecutados}")
    print(f"Tiempo total: {resultado.tiempo_total:.2f}s")