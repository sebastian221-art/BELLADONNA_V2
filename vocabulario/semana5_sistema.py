"""
Vocabulario de Sistema - Semana 5 (Fase 3) - VERSIÓN CORREGIDA v4.

39 conceptos de operaciones de sistema operativo.
Grounding: 1.0 (Bell ejecuta comandos reales)

═══════════════════════════════════════════════════════════════════════════════
CORRECCIONES FASE 4A v4:
- ✅ CONCEPTO_WC: Sin "count" (conflicto con CONCEPTO_COUNT de BD) [v3]
- ✅ CONCEPTO_ECHO: Sin "print", "imprimir" (conflicto con CONCEPTO_PRINT Python)
- ✅ CONCEPTO_EXTENSION_SHELL: Sin "formato" (conflicto con CONCEPTO_FORMATO)
- ✅ CONCEPTO_DIRECTORIO_SHELL: Solo "directory", "dir" (sin carpeta/folder)
═══════════════════════════════════════════════════════════════════════════════
"""

from pathlib import Path
import sys

proyecto_path = Path(__file__).parent.parent
sys.path.insert(0, str(proyecto_path))

from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto

shell_executor = None


def configurar_executor(executor):
    """Configura el ejecutor de shell para los conceptos."""
    global shell_executor
    shell_executor = executor


def obtener_conceptos_sistema():
    """
    Retorna 39 conceptos de operaciones de sistema (SIN DUPLICADOS v4).
    """
    conceptos = []
    
    # ==================== NAVEGACIÓN Y LISTADO (8) ====================
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LS",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "listar", "ls", "mostrar archivos", 
            "listar archivos", "ver archivos"
        ],
        operaciones={
            'ejecutar': lambda path='.': shell_executor.ejecutar(f"ls -la {path}") 
                        if shell_executor else {'exitoso': False, 'error': 'Executor no configurado'}
        },
        confianza_grounding=1.0,
        propiedades={
            'modifica_sistema': False,
            'solo_lectura': True,
            'requiere_path': False
        },
        relaciones={
            'tipo_de': ['OPERACION_FILESYSTEM'],
            'relacionado_con': ['CONCEPTO_DIRECTORIO', 'CONCEPTO_ARCHIVO']
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PWD",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "pwd", "directorio actual", "dónde estoy",
            "ruta actual", "ubicación actual"
        ],
        operaciones={
            'ejecutar': lambda: shell_executor.ejecutar("pwd") 
                        if shell_executor else {'exitoso': False}
        },
        confianza_grounding=1.0,
        propiedades={
            'modifica_sistema': False,
            'solo_lectura': True,
            'retorna': 'string'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TREE",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "tree", "árbol de directorios", "estructura",
            "mostrar estructura", "árbol"
        ],
        operaciones={
            'ejecutar': lambda path='.': shell_executor.ejecutar(f"tree {path}") 
                        if shell_executor else {'exitoso': False}
        },
        confianza_grounding=1.0,
        propiedades={
            'modifica_sistema': False,
            'visual': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_HEAD",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "head", "primeras líneas", "inicio archivo",
            "ver inicio"
        ],
        operaciones={
            'ejecutar': lambda archivo, lineas=10: 
                        shell_executor.ejecutar(f"head -n {lineas} {archivo}") 
                        if shell_executor else {'exitoso': False}
        },
        confianza_grounding=1.0,
        propiedades={
            'modifica_sistema': False,
            'requiere_archivo': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TAIL",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "tail", "últimas líneas", "final archivo",
            "ver final", "bottom"
        ],
        operaciones={
            'ejecutar': lambda archivo, lineas=10: 
                        shell_executor.ejecutar(f"tail -n {lineas} {archivo}") 
                        if shell_executor else {'exitoso': False}
        },
        confianza_grounding=1.0,
        propiedades={
            'modifica_sistema': False,
            'requiere_archivo': True,
            'útil_para': 'logs'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LESS",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "less", "more", "paginar",
            "mostrar archivo"
        ],
        operaciones={
            'ejecutar': lambda archivo: shell_executor.ejecutar(f"less {archivo}") 
                        if shell_executor else {'exitoso': False}
        },
        confianza_grounding=1.0,
        propiedades={
            'interactivo': True,
            'paginado': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FIND",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "find", "buscar archivo", "encontrar",
            "search", "localizar"
        ],
        operaciones={
            'ejecutar': lambda pattern, path='.': 
                        shell_executor.ejecutar(f"find {path} -name {pattern}") 
                        if shell_executor else {'exitoso': False}
        },
        confianza_grounding=1.0,
        propiedades={
            'recursivo': True,
            'retorna': 'lista'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_GREP",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "grep", "buscar en archivo", "buscar texto",
            "search in file", "filtrar"
        ],
        operaciones={
            'ejecutar': lambda pattern, archivo: 
                        shell_executor.ejecutar(f"grep '{pattern}' {archivo}") 
                        if shell_executor else {'exitoso': False}
        },
        confianza_grounding=1.0,
        propiedades={
            'busca_contenido': True,
            'retorna': 'líneas'
        }
    ))
    
    # ==================== DIRECTORIOS (6) ====================
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MKDIR",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "mkdir", "crear directorio", "nueva carpeta",
            "crear carpeta", "make directory"
        ],
        operaciones={
            'ejecutar': lambda nombre: shell_executor.ejecutar(f"mkdir -p {nombre}") 
                        if shell_executor else {'exitoso': False}
        },
        confianza_grounding=1.0,
        propiedades={
            'modifica_sistema': True,
            'crea_recurso': True,
            'idempotente': True
        },
        relaciones={
            'requiere': ['CONCEPTO_DIRECTORIO'],
            'inverso_de': ['CONCEPTO_ELIMINAR_DIRECTORIO']
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ELIMINAR_DIRECTORIO",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "rmdir", "eliminar directorio", "borrar carpeta",
            "remove directory"
        ],
        operaciones={
            'ejecutar': lambda nombre: shell_executor.ejecutar(f"rmdir {nombre}") 
                        if shell_executor else {'exitoso': False}
        },
        confianza_grounding=1.0,
        propiedades={
            'modifica_sistema': True,
            'destructivo': True,
            'requiere_vacío': True
        },
        relaciones={
            'inverso_de': ['CONCEPTO_CREAR_DIRECTORIO']
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CAMBIAR_DIRECTORIO",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "cd", "cambiar directorio", "ir a",
            "navegar a", "change directory"
        ],
        operaciones={
            'ejecutar': lambda path: shell_executor.ejecutar(f"cd {path} && pwd") 
                        if shell_executor else {'exitoso': False}
        },
        confianza_grounding=1.0,
        propiedades={
            'modifica_estado': True,
            'no_persistente': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DIRECTORIO_SHELL",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "directory", "dir"  # Sin: directorio, carpeta, folder (→ CONCEPTO_DIRECTORIO)
        ],
        confianza_grounding=0.9,
        propiedades={
            'es_contenedor': True,
            'tiene_path': True,
            'jerarquico': True
        },
        relaciones={
            'contiene': ['CONCEPTO_ARCHIVO'],
            'tipo_de': ['RECURSO_FILESYSTEM']
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PATH",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "ruta", "path", "camino", "ubicación",
            "dirección"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es_identificador': True,
            'puede_ser': ['absoluto', 'relativo']
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PATH_ABSOLUTO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "ruta absoluta", "path absoluto", "full path",
            "camino completo"
        ],
        confianza_grounding=0.9,
        propiedades={
            'empieza_en_raiz': True,
            'completo': True
        },
        relaciones={
            'tipo_de': ['CONCEPTO_PATH']
        }
    ))
    
    # ==================== INFORMACIÓN DEL SISTEMA (10) ====================
    
    # ═══════════════════════════════════════════════════════════════════════
    # ✅ FIX v4: CONCEPTO_ECHO - ELIMINADO "print", "imprimir"
    #    Estas palabras están en CONCEPTO_PRINT (semana2_python)
    # ═══════════════════════════════════════════════════════════════════════
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ECHO",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "echo",           # ← Comando shell
            "mostrar texto",  # ← Descripción
            "display",        # ← Inglés alternativo
            "output"          # ← Técnico
            # "print" ELIMINADO → CONCEPTO_PRINT (Python)
            # "imprimir" ELIMINADO → CONCEPTO_PRINT (Python)
        ],
        operaciones={
            'ejecutar': lambda texto: shell_executor.ejecutar(f"echo '{texto}'") 
                        if shell_executor else {'exitoso': False}
        },
        confianza_grounding=1.0,
        propiedades={
            'modifica_sistema': False,
            'simple': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_WHOAMI",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "whoami", "usuario actual", "quién soy",
            "current user", "mi usuario"
        ],
        operaciones={
            'ejecutar': lambda: shell_executor.ejecutar("whoami") 
                        if shell_executor else {'exitoso': False}
        },
        confianza_grounding=1.0,
        propiedades={
            'retorna': 'username',
            'solo_lectura': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_HOSTNAME",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "hostname", "nombre del equipo", "nombre máquina",
            "computer name"
        ],
        operaciones={
            'ejecutar': lambda: shell_executor.ejecutar("hostname") 
                        if shell_executor else {'exitoso': False}
        },
        confianza_grounding=1.0,
        propiedades={
            'retorna': 'string',
            'identifica_máquina': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DATE",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "date", "fecha", "hora", "fecha y hora",
            "timestamp"
        ],
        operaciones={
            'ejecutar': lambda: shell_executor.ejecutar("date") 
                        if shell_executor else {'exitoso': False}
        },
        confianza_grounding=1.0,
        propiedades={
            'retorna': 'datetime',
            'sistema': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_UNAME",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "uname", "información del sistema", "system info",
            "os info", "sistema operativo"
        ],
        operaciones={
            'ejecutar': lambda: shell_executor.ejecutar("uname -a") 
                        if shell_executor else {'exitoso': False}
        },
        confianza_grounding=1.0,
        propiedades={
            'retorna': 'system_info',
            'detallado': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_UPTIME",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "uptime", "tiempo encendido", "tiempo activo",
            "system uptime"
        ],
        operaciones={
            'ejecutar': lambda: shell_executor.ejecutar("uptime") 
                        if shell_executor else {'exitoso': False}
        },
        confianza_grounding=1.0,
        propiedades={
            'retorna': 'tiempo',
            'indica_estabilidad': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DF",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["df", "disk free", "espacio en disco", "storage"],
        operaciones={
            'ejecutar': lambda: shell_executor.ejecutar("df -h") 
                        if shell_executor else {'exitoso': False}
        },
        confianza_grounding=1.0,
        propiedades={
            'retorna': 'disk_info',
            'formato_humano': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DU",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["du", "disk usage específico", "uso de disco", "tamaño directorio"],
        operaciones={
            'ejecutar': lambda path='.': shell_executor.ejecutar(f"du -sh {path}") 
                        if shell_executor else {'exitoso': False}
        },
        confianza_grounding=1.0,
        propiedades={
            'retorna': 'size',
            'recursivo': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FREE",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["free", "memoria libre", "ram disponible", "memory usage"],
        operaciones={
            'ejecutar': lambda: shell_executor.ejecutar("free -h") 
                        if shell_executor else {'exitoso': False}
        },
        confianza_grounding=1.0,
        propiedades={
            'retorna': 'memory_info',
            'incluye_swap': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ENV",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "env", "variables de entorno", "environment",
            "variables ambientales", "environment variables"
        ],
        operaciones={
            'ejecutar': lambda: shell_executor.ejecutar("env") 
                        if shell_executor else {'exitoso': False}
        },
        confianza_grounding=1.0,
        propiedades={
            'retorna': 'dict',
            'configuración': True
        }
    ))
    
    # ==================== PROCESOS (8) ====================
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PS",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "ps", "procesos", "process status",
            "listar procesos", "processes"
        ],
        operaciones={
            'ejecutar': lambda: shell_executor.ejecutar("ps aux") 
                        if shell_executor else {'exitoso': False}
        },
        confianza_grounding=1.0,
        propiedades={
            'retorna': 'lista_procesos',
            'incluye_detalles': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TOP",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "top", "monitor procesos", "task manager",
            "system monitor", "htop"
        ],
        operaciones={
            'ejecutar': lambda: shell_executor.ejecutar("top -b -n 1") 
                        if shell_executor else {'exitoso': False}
        },
        confianza_grounding=1.0,
        propiedades={
            'interactivo': True,
            'tiempo_real': True,
            'cpu_uso': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_KILL",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "kill", "terminar proceso", "matar proceso",
            "stop process", "kill process"
        ],
        operaciones={
            'ejecutar': lambda pid: shell_executor.ejecutar(f"kill {pid}") 
                        if shell_executor else {'exitoso': False}
        },
        confianza_grounding=1.0,
        propiedades={
            'modifica_sistema': True,
            'requiere_pid': True,
            'puede_fallar': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PROCESO_SHELL",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "proceso", "process", "programa en ejecución",
            "running program"
        ],
        confianza_grounding=0.9,
        propiedades={
            'tiene_pid': True,
            'consume_recursos': True,
            'puede_tener_hijos': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PID_SHELL",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "pid", "process id", "identificador proceso",
            "process identifier"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es_numero': True,
            'único_sistema': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CPU_SHELL",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "cpu", "procesador", "processor",
            "central processing unit"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es_hardware': True,
            'ejecuta_procesos': True,
            'tiene_uso_porcentaje': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MEMORIA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "memoria", "ram", "memory",
            "memoria ram", "RAM"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es_hardware': True,
            'volátil': True,
            'se_mide_en': 'bytes'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SWAP",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "swap", "memoria swap", "swap space",
            "virtual memory"
        ],
        confianza_grounding=0.9,
        propiedades={
            'es_disco': True,
            'backup_ram': True,
            'más_lento': True
        }
    ))
    
    # ==================== ARCHIVOS (7) ====================
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CAT",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "cat", "concatenate", "mostrar contenido",
            "ver archivo", "leer archivo"
        ],
        operaciones={
            'ejecutar': lambda archivo: shell_executor.ejecutar(f"cat {archivo}") 
                        if shell_executor else {'exitoso': False}
        },
        confianza_grounding=1.0,
        propiedades={
            'modifica_sistema': False,
            'retorna': 'contenido'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TOUCH",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "touch", "crear archivo", "nuevo archivo",
            "create file", "make file"
        ],
        operaciones={
            'ejecutar': lambda nombre: shell_executor.ejecutar(f"touch {nombre}") 
                        if shell_executor else {'exitoso': False}
        },
        confianza_grounding=1.0,
        propiedades={
            'modifica_sistema': True,
            'crea_archivo_vacío': True,
            'actualiza_timestamp': True
        }
    ))
    
    # ═══════════════════════════════════════════════════════════════════════
    # ✅ FIX v3: CONCEPTO_WC - Sin "count" (conflicto con CONCEPTO_COUNT)
    # ═══════════════════════════════════════════════════════════════════════
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_WC",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "wc", "word count", "contar líneas",
            "contar palabras", "line count"  # Sin "count"
        ],
        operaciones={
            'ejecutar': lambda archivo: shell_executor.ejecutar(f"wc {archivo}") 
                        if shell_executor else {'exitoso': False}
        },
        confianza_grounding=1.0,
        propiedades={
            'retorna': 'estadísticas',
            'cuenta': ['líneas', 'palabras', 'bytes']
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FILE",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "file command", "tipo de archivo", "file type",
            "determinar tipo"
        ],
        operaciones={
            'ejecutar': lambda archivo: shell_executor.ejecutar(f"file {archivo}") 
                        if shell_executor else {'exitoso': False}
        },
        confianza_grounding=1.0,
        propiedades={
            'retorna': 'tipo',
            'usa_magic_numbers': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_STAT",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=[
            "stat", "estadísticas archivo", "file stats",
            "info archivo", "metadata"
        ],
        operaciones={
            'ejecutar': lambda archivo: shell_executor.ejecutar(f"stat {archivo}") 
                        if shell_executor else {'exitoso': False}
        },
        confianza_grounding=1.0,
        propiedades={
            'retorna': 'metadata',
            'incluye': ['tamaño', 'permisos', 'timestamps']
        }
    ))
    
    # ═══════════════════════════════════════════════════════════════════════
    # ✅ FIX v4: CONCEPTO_EXTENSION_SHELL - Sin "formato"
    #    "formato" está en CONCEPTO_FORMATO (semana3_sistema_avanzado)
    # ═══════════════════════════════════════════════════════════════════════
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EXTENSION_SHELL",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "extensión",      # ← Principal
            "extension",      # ← Inglés
            "sufijo",         # ← Alternativa
            "tipo archivo"    # ← Descriptivo
            # "formato" ELIMINADO → CONCEPTO_FORMATO
        ],
        confianza_grounding=0.9,
        propiedades={
            'identifica_tipo': True,
            'después_de_punto': True,
            'ejemplos': ['.txt', '.py', '.md']
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PERMISOS_SHELL",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=[
            "permisos", "permissions", "chmod",
            "acceso", "derechos"
        ],
        confianza_grounding=0.9,
        propiedades={
            'tipos': ['lectura', 'escritura', 'ejecución'],
            'para': ['usuario', 'grupo', 'otros'],
            'se_representa': 'octal o rwx'
        }
    ))
    
    return conceptos


def obtener_concepto_por_palabra(palabra: str, conceptos: list = None):
    """Busca un concepto que corresponda a una palabra en español."""
    if conceptos is None:
        conceptos = obtener_conceptos_sistema()
    
    palabra_lower = palabra.lower()
    for concepto in conceptos:
        if palabra_lower in [p.lower() for p in concepto.palabras_español]:
            return concepto
    return None


if __name__ == '__main__':
    conceptos = obtener_conceptos_sistema()
    print(f"✅ Vocabulario Sistema CORREGIDO v4: {len(conceptos)} conceptos")
    print(f"   ✅ CONCEPTO_WC sin 'count'")
    print(f"   ✅ CONCEPTO_ECHO sin 'print/imprimir'")
    print(f"   ✅ CONCEPTO_EXTENSION_SHELL sin 'formato'")
    
    con_grounding_1 = sum(1 for c in conceptos if c.confianza_grounding == 1.0)
    print(f"   - Grounding 1.0: {con_grounding_1}")
    print(f"   - Grounding promedio: {sum(c.confianza_grounding for c in conceptos) / len(conceptos):.2f}")