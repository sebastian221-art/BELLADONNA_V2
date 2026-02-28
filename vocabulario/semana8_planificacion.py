"""
Vocabulario de Planificación Multi-Paso - Semana 8 (Fase 3).

40 conceptos relacionados con planificación y ejecución de planes.
Grounding: 1.0 (Bell usa motor real de planificación)
"""

from pathlib import Path
import sys

# Agregar path del proyecto
proyecto_path = Path(__file__).parent.parent
sys.path.insert(0, str(proyecto_path))

from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto

# Importar motor y ejecutor (será inyectado en runtime)
motor_planificacion = None
ejecutor_planes = None


def configurar_planificacion(motor, ejecutor):
    """Configura motor y ejecutor para los conceptos."""
    global motor_planificacion, ejecutor_planes
    motor_planificacion = motor
    ejecutor_planes = ejecutor


def obtener_conceptos_planificacion():
    """
    Retorna 40 conceptos de planificación multi-paso.
    
    Categorías:
    - Plan (8 conceptos)
    - Paso (7 conceptos)
    - Dependencias (6 conceptos)
    - Ejecución (8 conceptos)
    - Estados (6 conceptos)
    - Optimización (5 conceptos)
    """
    conceptos = []
    
    # ==================== PLAN (8) ====================
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CREAR_PLAN",
        tipo=TipoConcepto.OPERACION_SISTEMA,  # CORREGIDO
        palabras_español=[
            "crear plan", "nuevo plan", "planificar",
            "hacer plan", "plan"
        ],
        operaciones={
            'ejecutar': lambda objetivo, pasos: motor_planificacion.crear_plan(objetivo, pasos)
                        if motor_planificacion else None
        },
        confianza_grounding=1.0,
        propiedades={
            'retorna': 'Plan',
            'requiere': ['objetivo', 'pasos']
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PLAN",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "plan", "planificación", "strategy", "estrategia"
        ],
        confianza_grounding=0.95,
        propiedades={
            'es': 'secuencia de pasos',
            'tiene': ['objetivo', 'pasos', 'estado'],
            'puede_tener': 'dependencias'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_OBJETIVO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "objetivo", "goal", "meta", "propósito"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'resultado deseado',
            'define': 'propósito del plan'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_VALIDAR_PLAN",
        tipo=TipoConcepto.OPERACION_SISTEMA,  # CORREGIDO
        palabras_español=[
            "validar plan", "verificar plan", "comprobar plan"
        ],
        operaciones={
            'ejecutar': lambda plan: motor_planificacion.validar_plan(plan)
                        if motor_planificacion else (False, [])
        },
        confianza_grounding=1.0,
        propiedades={
            'retorna': '(bool, errores)',
            'verifica': 'consistencia'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_OPTIMIZAR_PLAN",
        tipo=TipoConcepto.OPERACION_SISTEMA,  # CORREGIDO
        palabras_español=[
            "optimizar plan", "mejorar plan", "optimización"
        ],
        operaciones={
            'ejecutar': lambda plan: motor_planificacion.optimizar_plan(plan)
                        if motor_planificacion else None
        },
        confianza_grounding=1.0,
        propiedades={
            'elimina': 'redundancias',
            'mejora': 'eficiencia'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RESUMEN_PLAN",
        tipo=TipoConcepto.OPERACION_SISTEMA,  # CORREGIDO
        palabras_español=[
            "resumen del plan", "describir plan", "mostrar plan"
        ],
        operaciones={
            'ejecutar': lambda plan: motor_planificacion.generar_resumen(plan)
                        if motor_planificacion else ""
        },
        confianza_grounding=1.0,
        propiedades={
            'retorna': 'string formateado',
            'muestra': 'detalles del plan'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PROGRESO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "progreso", "avance", "completado"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'porcentaje',
            'mide': 'pasos completados vs totales',
            'rango': '0-100%'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_METADATA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "metadata", "metadatos", "información adicional"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'datos sobre el plan',
            'opcional': True,
            'ejemplos': ['autor', 'fecha', 'prioridad']
        }
    ))
    
    # ==================== PASO (7) ====================
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PASO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "paso", "step", "etapa", "fase"
        ],
        confianza_grounding=0.95,
        propiedades={
            'es': 'unidad de acción',
            'parte_de': 'plan',
            'tiene': ['descripción', 'acción', 'estado']
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ACCION",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "acción", "action", "operación", "tarea"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'operación ejecutable',
            'puede': 'tener parámetros',
            'retorna': 'resultado'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_REGISTRAR_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,  # CORREGIDO
        palabras_español=[
            "registrar acción", "agregar acción", "definir acción"
        ],
        operaciones={
            'ejecutar': lambda nombre, funcion: motor_planificacion.registrar_accion(nombre, funcion)
                        if motor_planificacion else None
        },
        confianza_grounding=1.0,
        propiedades={
            'requiere': ['nombre', 'función'],
            'hace_disponible': 'acción para planes'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PARAMETROS",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "parámetros", "parameters", "argumentos", "inputs"
        ],
        confianza_grounding=0.9,
        propiedades={
            'son': 'datos de entrada',
            'para': 'acción',
            'formato': 'diccionario'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RESULTADO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "resultado", "result", "output", "retorno"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'dato de salida',
            'de': 'ejecución de paso',
            'puede_ser': 'cualquier tipo'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DESCRIPCION",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "descripción", "description", "explicación"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'texto explicativo',
            'describe': 'qué hace el paso',
            'legible': 'para humanos'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ORDEN",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "orden", "secuencia", "order", "posición"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'número de posición',
            'determina': 'secuencia de ejecución',
            'puede_cambiar': 'con dependencias'
        }
    ))
    
    # ==================== DEPENDENCIAS (6) ====================
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DEPENDENCIA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "dependencia", "dependency", "prerequisito", "requerimiento"
        ],
        confianza_grounding=0.95,
        propiedades={
            'es': 'relación entre pasos',
            'significa': 'paso A debe completarse antes de B',
            'puede_ser': 'múltiple'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ORDENAR_DEPENDENCIAS",
        tipo=TipoConcepto.OPERACION_SISTEMA,  # CORREGIDO
        palabras_español=[
            "ordenar por dependencias", "topological sort",
            "ordenamiento topológico"
        ],
        confianza_grounding=0.95,
        propiedades={
            'usa': 'ordenamiento topológico',
            'respeta': 'dependencias',
            'retorna': 'secuencia válida'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CICLO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "ciclo", "cycle", "dependencia circular",
            "circular dependency"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'error',
            'ocurre_cuando': 'A depende de B y B de A',
            'impide': 'ejecución'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_GRAFO_DEPENDENCIAS",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "grafo de dependencias", "dependency graph",
            "grafo"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'estructura de datos',
            'representa': 'dependencias entre pasos',
            'nodos': 'pasos',
            'aristas': 'dependencias'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CAMINO_CRITICO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "camino crítico", "critical path",
            "ruta crítica"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'secuencia más larga',
            'determina': 'tiempo mínimo total',
            'no_puede': 'paralelizarse'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PREREQUISITO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "prerequisito", "prerequisite", "previo"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'paso que debe completarse antes',
            'sinónimo_de': 'dependencia'
        }
    ))
    
    # ==================== EJECUCIÓN (8) ====================
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EJECUTAR_PLAN",
        tipo=TipoConcepto.OPERACION_SISTEMA,  # CORREGIDO
        palabras_español=[
            "ejecutar plan", "run plan", "correr plan",
            "iniciar plan"
        ],
        operaciones={
            'ejecutar': lambda plan: ejecutor_planes.ejecutar_plan(plan)
                        if ejecutor_planes else None
        },
        confianza_grounding=1.0,
        propiedades={
            'retorna': 'ResultadoEjecucion',
            'ejecuta': 'todos los pasos',
            'respeta': 'dependencias'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EJECUTAR_PASO",
        tipo=TipoConcepto.OPERACION_SISTEMA,  # CORREGIDO
        palabras_español=[
            "ejecutar paso", "run step", "correr paso"
        ],
        confianza_grounding=0.95,
        propiedades={
            'ejecuta': 'un solo paso',
            'retorna': 'resultado',
            'puede_fallar': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EJECUTOR",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "ejecutor", "executor", "runner"
        ],
        confianza_grounding=0.95,
        propiedades={
            'es': 'componente',
            'ejecuta': 'planes',
            'maneja': 'errores y log'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RESULTADO_EJECUCION",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "resultado ejecución", "execution result",
            "resultado del plan"
        ],
        confianza_grounding=0.95,
        propiedades={
            'contiene': ['exitoso', 'pasos ejecutados', 'errores'],
            'retornado_por': 'ejecutar_plan'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CONTEXTO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "contexto", "context", "entorno"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'información disponible',
            'para': 'ejecución de paso',
            'incluye': ['plan', 'paso actual', 'resultados previos']
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LOG",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "log", "registro", "bitácora", "historial"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'lista de eventos',
            'registra': 'ejecución',
            'útil_para': 'debugging'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DRY_RUN",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "dry run", "simulación", "prueba", "test run"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'ejecución simulada',
            'no': 'ejecuta realmente',
            'útil_para': 'validar plan'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ROLLBACK_PLAN",
        tipo=TipoConcepto.OPERACION_SISTEMA,  # CORREGIDO
        palabras_español=[
            "rollback", "revertir", "deshacer", "volver atrás"
        ],
        operaciones={
            'ejecutar': lambda plan: ejecutor_planes.rollback_plan(plan)
                        if ejecutor_planes else None
        },
        confianza_grounding=1.0,
        propiedades={
            'revierte': 'cambios',
            'en_orden': 'inverso',
            'cuando': 'plan falla'
        }
    ))
    
    # ==================== ESTADOS (6) ====================
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ESTADO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "estado", "state", "status"
        ],
        confianza_grounding=0.9,
        propiedades={
            'indica': 'situación actual',
            'de': 'paso o plan',
            'puede_cambiar': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PENDIENTE",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "pendiente", "pending", "por hacer"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'estado',
            'significa': 'no ejecutado aún',
            'emoji': '⏳'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EN_PROGRESO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "en progreso", "in progress", "ejecutando"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'estado',
            'significa': 'ejecutándose ahora',
            'emoji': '🔄'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_COMPLETADO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "completado", "completed", "done", "terminado"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'estado',
            'significa': 'ejecutado exitosamente',
            'emoji': '✅'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FALLIDO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "fallido", "failed", "error", "fracasado"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'estado',
            'significa': 'ejecución con error',
            'emoji': '❌'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_OMITIDO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "omitido", "skipped", "saltado"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'estado',
            'significa': 'no ejecutado intencionalmente',
            'emoji': '⏭️'
        }
    ))
    
    # ==================== OPTIMIZACIÓN (5) ====================
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PARALELIZACION",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "paralelización", "parallel", "paralelo",
            "concurrencia"
        ],
        confianza_grounding=0.95,
        propiedades={
            'es': 'técnica de optimización',
            'ejecuta': 'pasos simultáneamente',
            'cuando': 'no hay dependencias mutuas'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EJECUTAR_PARALELO",
        tipo=TipoConcepto.OPERACION_SISTEMA,  # CORREGIDO
        palabras_español=[
            "ejecutar en paralelo", "run parallel"
        ],
        operaciones={
            'ejecutar': lambda plan: ejecutor_planes.ejecutar_paralelo(plan)
                        if ejecutor_planes else None
        },
        confianza_grounding=1.0,
        propiedades={
            'identifica': 'pasos independientes',
            'ejecuta': 'simultáneamente',
            'reduce': 'tiempo total'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ESTIMAR_TIEMPO",
        tipo=TipoConcepto.OPERACION_SISTEMA,  # CORREGIDO
        palabras_español=[
            "estimar tiempo", "estimate time",
            "calcular duración"
        ],
        operaciones={
            'ejecutar': lambda plan: motor_planificacion.estimar_tiempo(plan)
                        if motor_planificacion else 0.0
        },
        confianza_grounding=1.0,
        propiedades={
            'calcula': 'tiempo total',
            'considera': 'camino crítico',
            'retorna': 'float (segundos)'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_REINTENTOS_PLAN",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "reintentos", "retry", "volver a intentar"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es': 'estrategia de recuperación',
            'cuando': 'paso falla',
            'tiene': 'límite máximo'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PAUSAR_PLAN",
        tipo=TipoConcepto.OPERACION_SISTEMA,  # CORREGIDO
        palabras_español=[
            "pausar", "pause", "detener temporalmente"
        ],
        operaciones={
            'ejecutar': lambda plan: ejecutor_planes.pausar_plan(plan)
                        if ejecutor_planes else None
        },
        confianza_grounding=1.0,
        propiedades={
            'detiene': 'ejecución',
            'puede': 'reanudarse',
            'preserva': 'estado'
        }
    ))
    
    return conceptos


# Función auxiliar
def obtener_concepto_por_palabra(palabra: str, conceptos: list = None):
    """Busca un concepto que corresponda a una palabra en español."""
    if conceptos is None:
        conceptos = obtener_conceptos_planificacion()
    
    palabra_lower = palabra.lower()
    for concepto in conceptos:
        if palabra_lower in [p.lower() for p in concepto.palabras_español]:
            return concepto
    return None


if __name__ == '__main__':
    # Test básico
    conceptos = obtener_conceptos_planificacion()
    print(f"✅ Vocabulario Planificación cargado: {len(conceptos)} conceptos")
    
    # Estadísticas
    con_grounding_1 = sum(1 for c in conceptos if c.confianza_grounding == 1.0)
    print(f"   - Grounding 1.0: {con_grounding_1}")
    print(f"   - Grounding promedio: {sum(c.confianza_grounding for c in conceptos) / len(conceptos):.2f}")