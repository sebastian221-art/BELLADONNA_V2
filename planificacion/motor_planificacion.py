"""
Motor de Planificación Multi-Paso.
FASE 3 - Semana 6 (VERSIÓN CORREGIDA - RETORNA Plan DIRECTAMENTE)

CAMBIOS:
- crear_plan() retorna Plan directamente (NO Dict)
- Eliminado método to_dict() innecesario  
- Esto arregla los 22 tests de planificación
"""

from typing import List, Dict, Optional, Callable, Any
from dataclasses import dataclass, field
from enum import Enum
import uuid


class EstadoPaso(Enum):
    """Estado de un paso del plan."""
    PENDIENTE = "pendiente"
    EN_PROGRESO = "en_progreso"
    COMPLETADO = "completado"
    FALLIDO = "fallido"
    OMITIDO = "omitido"


@dataclass
class Paso:
    """Un paso individual en un plan."""
    id: str
    descripcion: str
    accion: str
    parametros: Dict = field(default_factory=dict)
    dependencias: List[str] = field(default_factory=list)
    estado: EstadoPaso = EstadoPaso.PENDIENTE
    resultado: Optional[any] = None
    error: Optional[str] = None
    orden: int = 0


@dataclass
class Plan:
    """Un plan completo con múltiples pasos."""
    id: str
    objetivo: str
    pasos: List[Paso]
    estado: str = "creado"
    progreso: float = 0.0
    metadata: Dict = field(default_factory=dict)
    
    def obtener_paso(self, paso_id: str) -> Optional[Paso]:
        """Obtiene un paso por su ID."""
        for paso in self.pasos:
            if paso.id == paso_id:
                return paso
        return None
    
    def pasos_completados(self) -> List[Paso]:
        """Retorna lista de pasos completados."""
        return [p for p in self.pasos if p.estado == EstadoPaso.COMPLETADO]
    
    def pasos_pendientes(self) -> List[Paso]:
        """Retorna lista de pasos pendientes."""
        return [p for p in self.pasos if p.estado == EstadoPaso.PENDIENTE]
    
    def actualizar_progreso(self):
        """Actualiza el progreso del plan."""
        if not self.pasos:
            self.progreso = 0.0
            return
        
        completados = len(self.pasos_completados())
        self.progreso = (completados / len(self.pasos)) * 100.0


class MotorPlanificacion:
    """
    Motor para crear y gestionar planes multi-paso.
    
    Capacidades:
    - Crear planes con múltiples pasos
    - Gestionar dependencias entre pasos
    - Ordenar pasos automáticamente
    - Validar planes
    - Optimizar planes
    """
    
    def __init__(self):
        """Inicializa el motor de planificación."""
        self.planes: Dict[str, Plan] = {}
        self.acciones_disponibles: Dict[str, Callable] = {}
    
    def registrar_accion(self, nombre: str, funcion: Callable):
        """
        Registra una acción ejecutable.
        
        Args:
            nombre: Nombre de la acción
            funcion: Función a ejecutar
        """
        self.acciones_disponibles[nombre] = funcion
    
    def crear_plan(
        self,
        objetivo: str,
        pasos: List[Dict],
        metadata: Optional[Dict] = None
    ) -> Plan:  # ✅ CAMBIADO: Dict[str, Any] -> Plan
        """
        Crea un nuevo plan.
        
        Args:
            objetivo: Objetivo del plan
            pasos: Lista de diccionarios con info de pasos
            metadata: Metadata adicional
            
        Returns:
            Plan creado (objeto Plan directamente)
        """
        plan_id = str(uuid.uuid4())
        
        # Crear pasos
        pasos_obj = []
        for i, paso_dict in enumerate(pasos):
            paso = Paso(
                id=f"paso_{i+1}",
                descripcion=paso_dict.get("descripcion", ""),
                accion=paso_dict.get("accion", ""),
                parametros=paso_dict.get("parametros", {}),
                dependencias=paso_dict.get("dependencias", []),
                orden=i
            )
            pasos_obj.append(paso)
        
        # Ordenar por dependencias
        pasos_ordenados = self._ordenar_por_dependencias(pasos_obj)
        
        # Crear plan
        plan = Plan(
            id=plan_id,
            objetivo=objetivo,
            pasos=pasos_ordenados,
            metadata=metadata or {}
        )
        
        self.planes[plan_id] = plan
        
        # ✅ RETORNAR Plan directamente
        return plan
    
    def _ordenar_por_dependencias(self, pasos: List[Paso]) -> List[Paso]:
        """
        Ordena pasos respetando dependencias usando ordenamiento topológico.
        
        CORREGIDO: Evita recursión infinita
        """
        # Mapa de paso_id -> paso
        paso_map = {p.id: p for p in pasos}
        
        # Si no hay dependencias, mantener orden original
        tiene_deps = any(p.dependencias for p in pasos)
        if not tiene_deps:
            return pasos
        
        # Ordenamiento topológico con protección contra ciclos
        ordenados = []
        visitados = set()
        en_proceso = set()  # Para detectar ciclos
        
        def visitar(paso_id: str) -> bool:
            """Retorna True si se detecta ciclo."""
            if paso_id in visitados:
                return False
            
            if paso_id in en_proceso:
                # Ciclo detectado
                return True
            
            paso = paso_map.get(paso_id)
            if not paso:
                return False
            
            en_proceso.add(paso_id)
            
            # Visitar dependencias primero
            for dep_id in paso.dependencias:
                if visitar(dep_id):
                    return True  # Propagar detección de ciclo
            
            en_proceso.remove(paso_id)
            visitados.add(paso_id)
            ordenados.append(paso)
            return False
        
        # Visitar todos los pasos
        for paso in pasos:
            if paso.id not in visitados:
                if visitar(paso.id):
                    # Hay ciclo, retornar orden original
                    return pasos
        
        return ordenados
    
    def validar_plan(self, plan: Plan) -> tuple[bool, List[str]]:
        """
        Valida un plan.
        
        Args:
            plan: Plan a validar
            
        Returns:
            (es_valido, lista_errores)
        """
        errores = []
        
        # Validar que hay pasos
        if not plan.pasos:
            errores.append("El plan no tiene pasos")
        
        # Validar acciones
        for paso in plan.pasos:
            if not paso.accion:
                errores.append(f"Paso {paso.id} no tiene acción")
            elif paso.accion not in self.acciones_disponibles:
                errores.append(f"Acción '{paso.accion}' no disponible")
        
        # Validar dependencias
        paso_ids = {p.id for p in plan.pasos}
        for paso in plan.pasos:
            for dep_id in paso.dependencias:
                if dep_id not in paso_ids:
                    errores.append(
                        f"Paso {paso.id} depende de {dep_id} que no existe"
                    )
        
        # Detectar ciclos en dependencias
        if self._tiene_ciclos(plan.pasos):
            errores.append("El plan tiene dependencias cíclicas")
        
        return (len(errores) == 0, errores)
    
    def _tiene_ciclos(self, pasos: List[Paso]) -> bool:
        """Detecta si hay ciclos en las dependencias."""
        paso_map = {p.id: p for p in pasos}
        visitando = set()
        visitados = set()
        
        def visitar(paso_id: str) -> bool:
            if paso_id in visitando:
                return True  # Ciclo detectado
            
            if paso_id in visitados:
                return False
            
            visitando.add(paso_id)
            
            paso = paso_map.get(paso_id)
            if paso:
                for dep_id in paso.dependencias:
                    if visitar(dep_id):
                        return True
            
            visitando.remove(paso_id)
            visitados.add(paso_id)
            return False
        
        for paso in pasos:
            if visitar(paso.id):
                return True
        
        return False
    
    def optimizar_plan(self, plan: Plan) -> Plan:
        """
        Optimiza un plan eliminando pasos redundantes.
        
        Args:
            plan: Plan a optimizar
            
        Returns:
            Plan optimizado
        """
        # Eliminar pasos duplicados
        pasos_unicos = []
        vistos = set()
        
        for paso in plan.pasos:
            clave = (paso.descripcion, paso.accion)
            if clave not in vistos:
                vistos.add(clave)
                pasos_unicos.append(paso)
        
        plan.pasos = pasos_unicos
        
        # Reordenar para minimizar esperas
        plan.pasos = self._ordenar_por_dependencias(plan.pasos)
        
        return plan
    
    def obtener_siguiente_paso(self, plan: Plan) -> Optional[Paso]:
        """
        Obtiene el siguiente paso ejecutable.
        
        Args:
            plan: Plan
            
        Returns:
            Siguiente paso o None
        """
        for paso in plan.pasos:
            if paso.estado != EstadoPaso.PENDIENTE:
                continue
            
            # Verificar que dependencias estén completas
            deps_completas = True
            for dep_id in paso.dependencias:
                dep = plan.obtener_paso(dep_id)
                if dep and dep.estado != EstadoPaso.COMPLETADO:
                    deps_completas = False
                    break
            
            if deps_completas:
                return paso
        
        return None
    
    def puede_ejecutar_en_paralelo(self, plan: Plan) -> List[List[Paso]]:
        """
        Identifica pasos que pueden ejecutarse en paralelo.
        
        Args:
            plan: Plan
            
        Returns:
            Lista de grupos de pasos paralelos
        """
        grupos = []
        procesados = set()
        
        for paso in plan.pasos:
            if paso.id in procesados:
                continue
            
            # Encontrar pasos sin dependencias mutuas
            grupo = [paso]
            procesados.add(paso.id)
            
            for otro in plan.pasos:
                if otro.id in procesados:
                    continue
                
                # Ver si puede ir en este grupo
                puede_ir = True
                for paso_grupo in grupo:
                    if (paso_grupo.id in otro.dependencias or
                        otro.id in paso_grupo.dependencias):
                        puede_ir = False
                        break
                
                if puede_ir:
                    grupo.append(otro)
                    procesados.add(otro.id)
            
            grupos.append(grupo)
        
        return grupos
    
    def estimar_tiempo(self, plan: Plan, tiempo_por_paso: float = 1.0) -> float:
        """
        Estima tiempo de ejecución del plan considerando dependencias.
        
        CORREGIDO: Ahora calcula correctamente el camino crítico
        
        Args:
            plan: Plan
            tiempo_por_paso: Tiempo estimado por paso
            
        Returns:
            Tiempo total estimado
        """
        if not plan.pasos:
            return 0.0
        
        # Calcular camino crítico considerando dependencias
        paso_map = {p.id: p for p in plan.pasos}
        tiempos = {}
        
        def calcular_tiempo(paso_id: str) -> float:
            if paso_id in tiempos:
                return tiempos[paso_id]
            
            paso = paso_map.get(paso_id)
            if not paso:
                return 0.0
            
            # Si tiene dependencias, el tiempo es el máximo de sus dependencias + tiempo propio
            if paso.dependencias:
                max_dep = 0.0
                for dep_id in paso.dependencias:
                    max_dep = max(max_dep, calcular_tiempo(dep_id))
                tiempo_total = max_dep + tiempo_por_paso
            else:
                # Sin dependencias, es solo el tiempo del paso
                tiempo_total = tiempo_por_paso
            
            tiempos[paso_id] = tiempo_total
            return tiempo_total
        
        # Calcular para todos los pasos y retornar el máximo
        tiempo_max = 0.0
        for paso in plan.pasos:
            tiempo_max = max(tiempo_max, calcular_tiempo(paso.id))
        
        return tiempo_max
    
    def generar_resumen(self, plan: Plan) -> str:
        """
        Genera resumen legible del plan.
        
        Args:
            plan: Plan
            
        Returns:
            String con resumen
        """
        lineas = []
        lineas.append("=" * 60)
        lineas.append(f"PLAN: {plan.objetivo}")
        lineas.append("=" * 60)
        lineas.append(f"ID: {plan.id}")
        lineas.append(f"Estado: {plan.estado}")
        lineas.append(f"Progreso: {plan.progreso:.1f}%")
        lineas.append(f"Pasos totales: {len(plan.pasos)}")
        lineas.append(f"Pasos completados: {len(plan.pasos_completados())}")
        lineas.append(f"Pasos pendientes: {len(plan.pasos_pendientes())}")
        
        lineas.append("\nPASOS:")
        for i, paso in enumerate(plan.pasos, 1):
            estado_emoji = {
                EstadoPaso.PENDIENTE: "⏳",
                EstadoPaso.EN_PROGRESO: "🔄",
                EstadoPaso.COMPLETADO: "✅",
                EstadoPaso.FALLIDO: "❌",
                EstadoPaso.OMITIDO: "⏭️"
            }
            emoji = estado_emoji.get(paso.estado, "❓")
            
            lineas.append(f"\n{i}. {emoji} {paso.descripcion}")
            lineas.append(f"   ID: {paso.id}")
            lineas.append(f"   Acción: {paso.accion}")
            if paso.dependencias:
                lineas.append(f"   Dependencias: {', '.join(paso.dependencias)}")
            if paso.estado == EstadoPaso.FALLIDO and paso.error:
                lineas.append(f"   Error: {paso.error}")
        
        lineas.append("\n" + "=" * 60)
        
        return '\n'.join(lineas)


# Ejemplo de uso
if __name__ == '__main__':
    motor = MotorPlanificacion()
    
    # Registrar acciones
    motor.registrar_accion("analizar", lambda ctx: "análisis completo")
    motor.registrar_accion("corregir", lambda ctx: "errores corregidos")
    
    # Crear plan - AHORA RETORNA Plan directamente
    pasos = [
        {"descripcion": "Analizar código", "accion": "analizar"},
        {"descripcion": "Corregir errores", "accion": "corregir"}
    ]
    
    plan = motor.crear_plan("Mejorar código", pasos)
    
    print(f"✅ Plan creado")
    print(f"   ID: {plan.id}")
    print(f"   Objetivo: {plan.objetivo}")
    print(f"   Pasos: {len(plan.pasos)}")