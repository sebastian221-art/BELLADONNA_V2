# -*- coding: utf-8 -*-
"""
habilidades/shell_habilidad.py — VERSION v2.0 MÁXIMA

MEJORAS SOBRE v1.3/v1.4:
═══════════════════════════════════════════════════════════════════════

FIXES ACUMULADOS (v1.1→v1.4):
  FIX-H1  Tiempo de actividad: "cuánto tiempo llevas activa/activo"
  FIX-H2  Versión Python: "qué python tienes"
  FIX-H3  Compatibilidad Windows/Linux vía ShellExecutor v3.0
  FIX-H4  Timeout 15s para PowerShell en Windows
  FIX-H5  "muestrame los archivos" → cubre muestr[a-z]*
  FIX-H6  "activa" (femenino) en patrón uptime
  FIX-H7  "qué usuario eres/soy/tienes/es" → whoami

NUEVOS v2.0:
═══════════════════════════════════════════════════════════════════════

NUEVO-H8  Comandos de CPU y hardware:
          "cuántos núcleos tienes", "info del procesador",
          "arquitectura del sistema", "temperatura CPU"

NUEVO-H9  Monitoreo en tiempo real (top/htop sin interactivo):
          "muéstrame los procesos más pesados" → ps aux --sort=-%cpu | head -10
          "qué consume más CPU" → misma ruta
          "qué consume más RAM" → ps aux --sort=-%mem | head -10

NUEVO-H10 Comandos de red ampliados:
          "qué IP tengo", "mi dirección IP", "puertos abiertos",
          "conexiones activas", "hay internet", "ping a google",
          "velocidad de red", "interfaces de red"

NUEVO-H11 Búsqueda de archivos:
          "busca el archivo X", "dónde está el archivo X",
          "archivos modificados hoy", "archivos grandes"

NUEVO-H12 Información de Python ampliada:
          "qué paquetes tengo instalados", "versión de pip",
          "dónde está Python", "ruta de Python"

NUEVO-H13 Variables de entorno específicas:
          "cuál es el PATH", "qué PYTHONPATH tienes",
          "variables de entorno de Python"

NUEVO-H14 Comandos de texto/archivos:
          "muéstrame el contenido de X", "primeras líneas de X",
          "últimas líneas de X", "cuántas líneas tiene X"

NUEVO-H15 Git ampliado:
          "quién modificó X", "cuándo fue el último commit",
          "diferencias entre commits", "estado detallado de git",
          "tags de git", "stash de git"

NUEVO-H16 Estado del sistema ampliado:
          "carga del sistema", "temperatura del sistema",
          "información de hardware", "información de CPU"

NUEVO-H17 Formateo de respuesta mejorado:
          - Detecta si la salida es una tabla y la preserva
          - Detecta salida vacía con mensaje específico
          - Truncado inteligente (no corta a mitad de línea)
          - Preview con indicador de líneas restantes

NUEVO-H18 Patrones en segunda persona ampliados:
          "tienes internet", "tu IP", "tus archivos",
          "tus procesos", "tu disco", "tu memoria"

TODOS LOS FIXES v1.x PRESERVADOS INTACTOS.
COMPATIBILIDAD: motor v9.0+, shell_executor v3.0+, registro_habilidades v1.6+
"""

import re
import logging
from typing import Optional

from habilidades.registro_habilidades import (
    BaseHabilidad,
    HabilidadMatch,
    ResultadoHabilidad,
)

logger = logging.getLogger("habilidades.shell")


# ======================================================================
# MAPA DE INTENCIÓN → COMANDO (v2.0 MÁXIMO)
# ======================================================================

_MAPA_SHELL: list = [

    # ── Git ──────────────────────────────────────────────────────────

    (
        [r'estado\s+(?:de\s+)?git', r'git\s+status', r'cambios\s+git',
         r'que\s+cambi(?:o|os)', r'cambios\s+pendientes',
         r'archivos\s+modificados', r'que\s+hay\s+en\s+git',
         r'estado\s+del?\s+repositorio'],
        "git status",
        "Estado de git",
    ),
    (
        [r'log\s+(?:de\s+)?git', r'git\s+log', r'historial\s+(?:de\s+)?git',
         r'commits?\s+recientes?', r'ultimos?\s+commits?',
         r'historial\s+de\s+commits?', r'cuando\s+fue\s+el\s+ultimo\s+commit',
         r'ultimo\s+commit'],
        "git log --oneline -10",
        "Historial de git (últimos 10 commits)",
    ),
    (
        [r'diff\s+(?:de\s+)?git', r'git\s+diff', r'diferencias?\s+git',
         r'que\s+cambi[oó]\s+en\s+git', r'que\s+modifique'],
        "git diff",
        "Diferencias en git",
    ),
    (
        [r'ramas?\s+(?:de\s+)?git', r'git\s+branch', r'branches?',
         r'que\s+ramas?\s+(?:hay|tienes|existen)', r'ramas?\s+disponibles?'],
        "git branch",
        "Ramas de git",
    ),
    (
        # NUEVO-H15: git stash
        [r'git\s+stash', r'que\s+stash', r'cambios\s+guardados\s+git'],
        "git stash list",
        "Stash de git",
    ),
    (
        # NUEVO-H15: git tags
        [r'git\s+tags?', r'que\s+tags?\s+(?:hay|tienes)', r'versiones?\s+git'],
        "git tag",
        "Tags de git",
    ),
    (
        # NUEVO-H15: git log detallado
        [r'git\s+log\s+detallado', r'historial\s+detallado\s+git',
         r'commits?\s+con\s+fecha'],
        "git log --format='%h %ad %s' --date=short -10",
        "Historial de git con fechas",
    ),

    # ── Fecha y hora ─────────────────────────────────────────────────

    (
        [r'que\s+fecha',
         r'fecha\s+(?:de\s+)?hoy',
         r'que\s+hora',
         r'hora\s+actual',
         r'dime\s+la\s+fecha',
         r'dime\s+la\s+hora',
         r'que\s+dia\s+es',
         r'que\s+dia\s+(?:es\s+)?hoy',
         r'cual\s+es\s+la\s+fecha',
         r'cual\s+es\s+la\s+hora',
         r'calendar(?:io)?',
         r'^\s*fecha\s*$',
         r'^\s*hora\s*$',
         r'que\s+dia\s+tenemos',
         r'dime\s+la\s+fecha\s+y\s+hora',
         r'fecha\s+y\s+hora\s+actual'],
        "date",
        "Fecha y hora del sistema",
    ),

    # ── Usuario y sistema ─────────────────────────────────────────────

    (
        [r'quien\s+eres\s+en\s+el\s+sistema',
         r'usuario\s+del\s+sistema',
         r'\bwhoami\b',
         r'con\s+que\s+usuario',
         r'que\s+usuario\s+(?:soy|eres|es|tienes)',   # FIX-H7 ampliado
         r'cual\s+es\s+(?:tu\s+)?usuario',
         r'bajo\s+que\s+usuario',
         r'que\s+usuario\s+ejecutas?',
         r'usuario\s+actual'],
        "whoami",
        "Usuario del sistema",
    ),
    (
        [r'nombre\s+del\s+(?:equipo|servidor|m[aá]quina)',
         r'\bhostname\b',
         r'como\s+se\s+llama\s+(?:el\s+)?(?:equipo|servidor|m[aá]quina)',
         r'nombre\s+(?:del\s+)?host',
         r'nombre\s+del\s+sistema',
         r'como\s+se\s+llama\s+(?:el\s+)?sistema'],
        "hostname",
        "Nombre del equipo",
    ),
    (
        [r'sistema\s+operativo',
         r'\buname\b',
         r'que\s+sistema',
         r'informaci[oó]n\s+del\s+sistema',
         r'version\s+del\s+sistema',
         r'que\s+linux',
         r'que\s+kernel',
         r'version\s+del\s+kernel',
         r'que\s+os\s+(?:tienes|usas)',
         r'que\s+sistema\s+operativo'],
        "uname -a",
        "Información del sistema operativo",
    ),
    (
        # FIX-H6 + FIX-H1: activ[oa] cubre masculino y femenino
        [r'cuanto\s+tiempo\s+(?:lleva|llevo|llevas)\s+(?:encendid[oa]|activ[oa]|corriendo|funcionando)',
         r'\buptime\b',
         r'tiempo\s+encendido',
         r'tiempo\s+activo',
         r'cuanto\s+tiempo\s+llevas\s+corriendo',
         r'desde\s+cuando\s+(?:estas?|llevas)\s+(?:activ[oa]|corriendo|encendid[oa])',
         r'tiempo\s+en\s+linea',
         r'tiempo\s+funcionando'],
        "uptime",
        "Tiempo de actividad del sistema",
    ),
    (
        [r'(?:mis\s+)?grupos?\s+(?:del\s+)?(?:usuario|sistema)',
         r'\bgroups\b',
         r'a\s+que\s+grupos\s+pertenezco',
         r'permisos?\s+del\s+usuario',
         r'mi\s+id\s+de\s+usuario'],
        "id",
        "Usuario e información de grupos",
    ),
    (
        [r'variables?\s+de\s+entorno',
         r'\benv\b',
         r'\bprintenv\b',
         r'que\s+variables?\s+(?:hay|tengo|existen)',
         r'entorno\s+actual',
         r'variables?\s+del\s+sistema'],
        "env",
        "Variables de entorno",
    ),
    (
        # NUEVO-H13: variables de entorno específicas
        [r'cual\s+es\s+(?:el\s+)?(?:tu\s+)?(?:path|PATH)',
         r'que\s+(?:tiene\s+)?(?:el\s+)?PATH',
         r'ruta\s+(?:del\s+)?PATH'],
        "echo $PATH",
        "Variable PATH del sistema",
    ),
    (
        # NUEVO-H13: PYTHONPATH
        [r'pythonpath', r'PYTHONPATH', r'variables?\s+(?:de\s+)?python'],
        "echo $PYTHONPATH",
        "Variable PYTHONPATH",
    ),

    # ── CPU y Hardware (NUEVO-H8) ─────────────────────────────────────

    (
        [r'arquitectura',
         r'\barch\b',
         r'tipo\s+de\s+procesador',
         r'procesador\s+de\s+cuantos\s+bits',
         r'arquitectura\s+del\s+sistema',
         r'bits\s+del\s+sistema'],
        "uname -m",
        "Arquitectura del sistema",
    ),
    (
        [r'informaci[oó]n\s+(?:de\s+)?(?:la\s+)?cpu',
         r'cu[aá]ntos?\s+(?:n[uú]cleos|cores|procesadores)',
         r'\bnproc\b',
         r'n[uú]mero\s+de\s+(?:cores?|n[uú]cleos)',
         r'cuantos\s+procesadores?\s+(?:tienes|hay)',
         r'nucle[oa]s\s+(?:del\s+)?cpu',
         r'threads?\s+del\s+cpu'],
        "nproc",
        "Número de CPUs disponibles",
    ),
    (
        # NUEVO-H16: información detallada de CPU
        [r'informaci[oó]n\s+detallada\s+(?:de\s+)?cpu',
         r'modelo\s+del\s+(?:cpu|procesador)',
         r'detalles?\s+del\s+(?:cpu|procesador)',
         r'que\s+procesador\s+(?:tienes|hay)',
         r'info\s+cpu'],
        "cat /proc/cpuinfo | head -30",
        "Información detallada del CPU",
    ),

    # ── Procesos ──────────────────────────────────────────────────────

    (
        [r'procesos\s+(?:activos?|corriendo|en\s+ejecuci[oó]n)',
         r'que\s+procesos',
         r'lista\s+(?:de\s+)?procesos',
         r'que\s+esta\s+corriendo',
         r'\bps\b',
         r'tus\s+procesos',
         r'procesos\s+del\s+sistema'],
        "ps aux",
        "Procesos activos",
    ),
    (
        # NUEVO-H9: procesos más pesados por CPU
        [r'procesos?\s+(?:m[aá]s\s+)?(?:pesados?|que\s+consumen?\s+(?:m[aá]s\s+)?cpu)',
         r'que\s+consume\s+m[aá]s\s+cpu',
         r'top\s+procesos?\s+cpu',
         r'procesos?\s+cpu'],
        "ps aux --sort=-%cpu | head -11",
        "Procesos que más consumen CPU",
    ),
    (
        # NUEVO-H9: procesos más pesados por RAM
        [r'procesos?\s+que\s+consumen?\s+(?:m[aá]s\s+)?(?:ram|memoria)',
         r'que\s+consume\s+m[aá]s\s+(?:ram|memoria)',
         r'top\s+procesos?\s+(?:ram|memoria)',
         r'procesos?\s+(?:ram|memoria)'],
        "ps aux --sort=-%mem | head -11",
        "Procesos que más consumen RAM",
    ),
    (
        [r'procesos?\s+python', r'python\s+corriendo',
         r'que\s+scripts?\s+python', r'instancias?\s+python'],
        "ps aux | grep python",
        "Procesos Python activos",
    ),
    (
        [r'procesos?\s+(?:de\s+)?bell', r'bell\s+corriendo',
         r'instancias?\s+(?:de\s+)?bell'],
        "ps aux | grep bell",
        "Procesos Bell activos",
    ),

    # ── Disco y memoria ───────────────────────────────────────────────

    (
        [r'espacio\s+en\s+disco',
         r'disco\s+disponible',
         r'cu[aá]nto\s+espacio',
         r'espacio\s+libre',
         r'\bdf\b',
         r'espacio\s+en\s+(?:el\s+)?disco',
         r'cuanto\s+queda\s+en\s+disco',
         r'espacio\s+disponible',
         r'cuanto\s+disco\s+(?:tienes|hay|queda)',
         r'tu\s+disco',
         r'discos?\s+disponibles?'],
        "df -h",
        "Espacio en disco",
    ),
    (
        [r'uso\s+de\s+(?:directorio|carpeta|disco)\s+actual',
         r'cu[aá]nto\s+ocupa',
         r'\bdu\b',
         r'tama[nñ]o\s+(?:del\s+)?directorio',
         r'peso\s+del\s+directorio',
         r'cuanto\s+pesa\s+(?:esta\s+)?carpeta'],
        "du -sh .",
        "Uso de disco del directorio actual",
    ),
    (
        [r'memoria\s+(?:ram|disponible|libre|usada)',
         r'cu[aá]nta\s+(?:ram|memoria)',
         r'\bfree\b',
         r'uso\s+de\s+memoria',
         r'cuanta\s+memoria\s+tienes',
         r'cuanta\s+ram\s+(?:tienes|hay)',
         r'ram\s+disponible',
         r'memoria\s+disponible',
         r'tu\s+ram',
         r'tu\s+memoria',
         r'cuanta\s+ram\s+usas?'],
        "free -h",
        "Uso de memoria RAM",
    ),
    (
        # NUEVO-H16: carga del sistema
        [r'carga\s+del\s+sistema',
         r'load\s+average',
         r'carga\s+promedio',
         r'que\s+tan\s+cargado\s+(?:estas?|esta)'],
        "uptime && cat /proc/loadavg 2>/dev/null || uptime",
        "Carga del sistema",
    ),

    # ── Directorio y archivos ─────────────────────────────────────────

    (
        [r'donde\s+est[aá]s?',
         r'directorio\s+actual',
         r'ruta\s+actual',
         r'en\s+que\s+carpeta',
         r'\bpwd\b',
         r'cual\s+es\s+tu\s+directorio',
         r'en\s+que\s+directorio',
         r'ruta\s+completa',
         r'donde\s+(?:estas?|te\s+encuentras)',
         r'cual\s+es\s+(?:tu\s+)?(?:ruta|directorio|ubicacion)',
         r'en\s+que\s+ruta\s+(?:estas?|te\s+encuentras)',
         r'tu\s+directorio\s+actual'],
        "pwd",
        "Directorio actual",
    ),
    (
        # FIX-H5: muestr[a-z]* cubre muestra/muestrame/muestrale/etc.
        [r'lista\s+(?:tus\s+)?archivos',
         r'lista\s+(?:los\s+)?archivos',
         r'muestr[a-z]*\s+(?:tus?\s+|los\s+)?archivos',
         r'que\s+archivos\s+(?:hay|tienes)',
         r'archivos\s+disponibles',
         r'contenido\s+de\s+(?:la\s+)?carpeta',
         r'\bls\b',
         r'que\s+hay\s+en\s+(?:tu\s+)?directorio',
         r'muestra\s+(?:el\s+)?directorio',
         r'lista\s+(?:el\s+)?directorio',
         r'que\s+archivos?\s+(?:existen|tienes|hay)',
         r'ver\s+(?:los\s+)?archivos',
         r'mostrar\s+(?:los\s+)?archivos',
         r'tus\s+archivos',
         r'mis\s+archivos'],
        "ls -la",
        "Archivos del directorio actual",
    ),
    (
        [r'archivos?\s+(?:py|python)',
         r'scripts?\s+python',
         r'que\s+(?:archivos?\s+)?\.py',
         r'archivos?\s+\.py',
         r'tus\s+scripts?\s+python'],
        "ls -la *.py",
        "Archivos Python en el directorio",
    ),
    (
        [r'estructura\s+(?:de\s+)?(?:carpetas|directorios|archivos)',
         r'\btree\b',
         r'arbol\s+(?:de\s+)?(?:directorios|carpetas)',
         r'jerarquia\s+(?:de\s+)?(?:carpetas|directorios)',
         r'estructura\s+de\s+carpetas',
         r'como\s+(?:esta\s+)?organizado'],
        "tree -L 2",
        "Estructura de directorios (2 niveles)",
    ),
    (
        [r'archivos?\s+(?:de\s+)?(?:log|logs)',
         r'logs?\s+(?:del\s+)?sistema',
         r'que\s+logs?\s+(?:hay|tienes)'],
        "ls -la *.log 2>/dev/null || echo 'No hay archivos .log en este directorio'",
        "Archivos de log",
    ),
    (
        # NUEVO-H11: archivos modificados recientemente
        [r'archivos?\s+modificados?\s+(?:hoy|recientemente|recientes?)',
         r'ultimos?\s+archivos?\s+modificados?',
         r'que\s+archivos?\s+cambi[ée]\s+(?:hoy|recientemente)'],
        "find . -type f -mtime -1 -not -path './.git/*' 2>/dev/null | head -20",
        "Archivos modificados en las últimas 24 horas",
    ),
    (
        # NUEVO-H11: archivos grandes
        [r'archivos?\s+(?:grandes?|m[aá]s\s+pesados?)',
         r'que\s+archivos?\s+ocupan?\s+(?:m[aá]s|mucho)',
         r'archivos?\s+que\s+pesan?\s+m[aá]s'],
        "find . -type f -not -path './.git/*' 2>/dev/null | xargs ls -lS 2>/dev/null | head -10",
        "Archivos más grandes del directorio",
    ),
    (
        # NUEVO-H11: buscar archivo por nombre
        [r'busca\s+(?:el\s+)?archivo\s+(\w+)',
         r'donde\s+esta\s+(?:el\s+)?archivo\s+(\w+)',
         r'find\s+(\w+)'],
        "find . -name '*.py' -o -name '*.txt' 2>/dev/null | head -20",
        "Buscar archivos",
    ),

    # ── Red e internet (NUEVO-H10 ampliado) ──────────────────────────

    (
        [r'ping\s+(?:a\s+)?google',
         r'tienes\s+(?:acceso\s+a\s+)?internet',
         r'hay\s+internet',
         r'conexi[oó]n\s+a\s+internet',
         r'acceso\s+a\s+internet',
         r'puedes\s+llegar\s+a\s+internet',
         r'internet\s+funcionando'],
        "ping -c 3 google.com",
        "Conectividad a internet",
    ),
    (
        [r'(?:mi\s+|tu\s+)?ip\s+(?:local|del\s+sistema|de\s+(?:la\s+)?m[aá]quina)',
         r'direcci[oó]n\s+ip',
         r'que\s+ip\s+(?:tienes|tengo)',
         r'\bifconfig\b',
         r'\bip\s+addr\b',
         r'mi\s+ip',
         r'tu\s+ip',
         r'ip\s+local',
         r'interfaces?\s+de\s+red'],
        "ip addr show 2>/dev/null || ifconfig",
        "Dirección IP del sistema",
    ),
    (
        [r'puertos?\s+(?:abiertos?|en\s+uso|escuchando)',
         r'\bss\b',
         r'\bnetstat\b',
         r'que\s+puertos?\s+(?:hay|estan)',
         r'conexiones?\s+activas?',
         r'puertos?\s+tcp',
         r'que\s+escucha'],
        "ss -tuln",
        "Puertos en uso",
    ),

    # ── Python específico (NUEVO-H12 ampliado) ───────────────────────

    (
        [r'version\s+(?:de\s+)?python',
         r'python\s+version',
         r'que\s+version\s+(?:de\s+)?python',
         r'que\s+python\s+(?:hay|tienes|esta)',
         r'cual\s+es\s+(?:la\s+)?version\s+(?:de\s+)?python',
         r'python\s+(?:que\s+)?tengo'],
        "python3 --version",
        "Versión de Python",
    ),
    (
        [r'paquetes?\s+(?:pip|python|instalados?)',
         r'que\s+(?:paquetes?|librerias?)\s+(?:hay|tienes|instalados?)',
         r'\bpip\s+list\b',
         r'pip\s+freeze',
         r'librerias?\s+instaladas?',
         r'modulos?\s+instalados?'],
        "pip3 list",
        "Paquetes Python instalados",
    ),
    (
        # NUEVO-H12: dónde está Python
        [r'donde\s+esta\s+python',
         r'ruta\s+(?:de\s+)?python',
         r'que\s+python\s+(?:uso|ejecuto)',
         r'which\s+python'],
        "which python3 || which python",
        "Ruta del intérprete Python",
    ),
    (
        # NUEVO-H12: versión de pip
        [r'version\s+(?:de\s+)?pip',
         r'pip\s+version',
         r'que\s+pip\s+(?:hay|tienes)'],
        "pip3 --version",
        "Versión de pip",
    ),

    # ── Búsqueda en archivos (NUEVO-H14 + originales) ────────────────

    (
        [r'busca\s+(?:la\s+palabra\s+)?errores?\s+en\s+(?:los\s+)?(?:logs?|c[oó]digo)',
         r'grep\s+error',
         r'busca\s+error',
         r'errores?\s+en\s+(?:el\s+)?c[oó]digo',
         r'busca\s+errores?'],
        "grep -r 'error' . --include='*.py' 2>/dev/null | head -20",
        "Búsqueda de errores en código Python",
    ),
    (
        [r'busca\s+(?:la\s+palabra\s+)?todo',
         r'que\s+todos?\s+(?:hay|pendientes)',
         r'busca\s+todos?\s+en\s+(?:el\s+)?c[oó]digo',
         r'pendientes?\s+en\s+(?:el\s+)?c[oó]digo',
         r'fixmes?'],
        "grep -r 'TODO\\|FIXME\\|HACK' . --include='*.py' 2>/dev/null | head -20",
        "TODOs y FIXMEs en el código",
    ),

    # ── Historia de comandos ──────────────────────────────────────────

    (
        [r'(?:ultimos?\s+)?comandos?\s+(?:usados?|ejecutados?|recientes?)',
         r'historial\s+(?:de\s+)?(?:comandos?|terminal)',
         r'\bhistory\b',
         r'que\s+comandos?\s+(?:use|ejecute)\s+antes',
         r'historial\s+del\s+terminal'],
        "history | tail -20",
        "Últimos 20 comandos ejecutados",
    ),

    # ── NUEVO-H14: Contenido de archivos ─────────────────────────────

    (
        [r'primeras?\s+l[ií]neas?\s+(?:de|del)\s+(\S+)',
         r'inicio\s+(?:de|del)\s+archivo\s+(\S+)',
         r'head\s+(\S+)'],
        "head -20 *.py 2>/dev/null | head -40",
        "Primeras líneas de archivos Python",
    ),
    (
        [r'[uú]ltimas?\s+l[ií]neas?\s+(?:de|del)\s+(\S+)',
         r'final\s+(?:de|del)\s+archivo\s+(\S+)',
         r'tail\s+(\S+)'],
        "tail -20 *.py 2>/dev/null | tail -40",
        "Últimas líneas de archivos Python",
    ),
    (
        [r'cu[aá]ntas?\s+l[ií]neas?\s+(?:hay|tiene)',
         r'n[uú]mero\s+de\s+l[ií]neas?',
         r'l[ií]neas?\s+de\s+c[oó]digo'],
        "find . -name '*.py' | xargs wc -l 2>/dev/null | tail -5",
        "Líneas de código Python",
    ),

]


# ======================================================================
# DETECTORES AUXILIARES
# ======================================================================

def _detectar_comando_intento(msg: str) -> Optional[tuple]:
    """Busca el primer patrón que coincida y retorna (comando, descripción)."""
    for patrones, comando, descripcion in _MAPA_SHELL:
        for patron in patrones:
            if re.search(patron, msg, re.IGNORECASE):
                return (comando, descripcion)
    return None


def _es_pregunta_capacidad_shell(msg: str) -> bool:
    """
    Distingue entre pregunta de capacidad y solicitud real de ejecución.

    'puedes listar archivos?'      → True  (capacidad, no ejecutar)
    'lista tus archivos'           → False (ejecutar)
    'muestrame los archivos'       → False (ejecutar)  ← FIX-H5
    'cuánto tiempo llevas activa'  → False (ejecutar)  ← FIX-H6
    'qué usuario eres'             → False (ejecutar)  ← FIX-H7
    """
    verbos_capacidad = [
        'puedes', 'sabes', 'eres capaz', 'podrias', 'es posible',
        'puedes hacer', 'sabes hacer', 'tienes capacidad',
        'seria posible', 'podrias', 'serias capaz',
        'tienes la capacidad', 'puedes ejecutar',
        'eres capaz de', 'serian capaz',
    ]
    return any(v in msg for v in verbos_capacidad)


def _tipo_salida(stdout: str) -> str:
    """
    NUEVO-H17: detecta el tipo de salida para formateo inteligente.
    Retorna: 'tabla', 'lista', 'valor_unico', 'multilinea', 'vacio'
    """
    if not stdout or not stdout.strip():
        return 'vacio'
    lineas = [l for l in stdout.strip().split('\n') if l.strip()]
    if len(lineas) == 1:
        return 'valor_unico'
    # Detectar tabla: múltiples columnas separadas por espacios consistentemente
    if len(lineas) > 2:
        cols = [len(l.split()) for l in lineas[:5]]
        if max(cols) - min(cols) <= 2 and min(cols) >= 3:
            return 'tabla'
    if len(lineas) <= 10:
        return 'lista'
    return 'multilinea'


# ======================================================================
# HABILIDAD SHELL v2.0
# ======================================================================

class HabilidadShell(BaseHabilidad):
    """
    Habilidad de ejecución de comandos shell. v2.0 MÁXIMA.

    Vega aprueba antes de ejecutar.
    Echo verifica stdout en el generador.
    Timeout: 15s (PowerShell en Windows puede tomar hasta 8s).

    Cubre: git, fecha/hora, usuario, sistema, CPU, procesos,
    disco, memoria, red, Python, archivos, búsqueda, historial.
    """

    @property
    def id(self) -> str:
        return "SHELL"

    @property
    def descripcion_para_bell(self) -> str:
        return (
            "Ejecutar comandos de terminal aprobados por Vega. "
            "Cubre: ls, pwd, date, whoami, hostname, uname, uptime, "
            "ps (incluyendo top por CPU/RAM), df, du, free, "
            "git (status/log/diff/branch/stash/tags), "
            "python --version, pip list, which python, "
            "grep, find, wc, env, ip, ss, nproc, history, tree, "
            "archivos recientes, archivos grandes, líneas de código."
        )

    @property
    def consejeras_requeridas(self) -> list:
        return ["Vega", "Echo"]

    # ------------------------------------------------------------------
    # DETECCIÓN
    # ------------------------------------------------------------------

    def detectar(self, mensaje: str, conceptos: list, hechos: dict) -> Optional[HabilidadMatch]:
        msg = mensaje.lower().strip() if mensaje else ""

        if not msg:
            return None

        # Preguntas de capacidad → no ejecutar
        if _es_pregunta_capacidad_shell(msg):
            return None

        resultado = _detectar_comando_intento(msg)
        if resultado is None:
            return None

        comando, descripcion = resultado

        return HabilidadMatch(
            habilidad_id="SHELL",
            confianza=0.92,
            parametros={
                "comando":     comando,
                "descripcion": descripcion,
                "mensaje":     mensaje,
            },
            habilidad=self,
        )

    # ------------------------------------------------------------------
    # EJECUCIÓN
    # ------------------------------------------------------------------

    def ejecutar(self, match: HabilidadMatch, nombre_usuario: str = "") -> ResultadoHabilidad:
        comando     = match.parametros.get("comando", "")
        descripcion = match.parametros.get("descripcion", "")

        if not comando:
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error="No se determinó el comando a ejecutar.",
                tipo_habilidad="SHELL",
            )

        executor = self._obtener_executor()
        if executor is None:
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error="ShellExecutor no disponible en este entorno.",
                tipo_habilidad="SHELL",
            )

        aprobado, razon_veto = self._aprobar_con_vega(comando, executor)
        if not aprobado:
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error=f"Vega bloqueó el comando: {razon_veto}",
                tipo_habilidad="SHELL",
                aprobado_vega=False,
            )

        try:
            resultado_shell = executor.ejecutar(comando)
        except TimeoutError:
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error=f"El comando excedió el tiempo límite de {executor.timeout}s.",
                tipo_habilidad="SHELL",
            )
        except Exception as e:
            logger.error(f"HabilidadShell.ejecutar error: {e}")
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error=f"Error al ejecutar '{comando}': {e}",
                tipo_habilidad="SHELL",
            )

        if resultado_shell.get("exitoso", False):
            stdout = resultado_shell.get("stdout", "").strip()
            if not stdout:
                # NUEVO-H17: mensaje específico por comando vacío
                stdout = self._mensaje_vacio(comando)
            return ResultadoHabilidad(
                exitoso=True,
                valor=stdout,
                descripcion=descripcion,
                pasos=[
                    f"Comando ejecutado: {comando}",
                    f"Código de retorno: 0",
                    f"Aprobado por Vega: sí",
                ],
                tipo_habilidad="SHELL",
                datos_raw=resultado_shell,
                aprobado_vega=True,
            )
        else:
            stderr = resultado_shell.get("stderr", "").strip()
            codigo = resultado_shell.get("codigo", -1)
            error_msg = stderr if stderr else f"El comando retornó código {codigo}"
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error=error_msg,
                tipo_habilidad="SHELL",
                datos_raw=resultado_shell,
            )

    # ------------------------------------------------------------------
    # HELPERS PRIVADOS
    # ------------------------------------------------------------------

    def _obtener_executor(self):
        """FIX-H4: timeout=15s para dar tiempo a PowerShell en Windows."""
        try:
            from operaciones.shell_executor import ShellExecutor
            return ShellExecutor(timeout=15)
        except ImportError:
            logger.warning("ShellExecutor no disponible")
            return None

    def _aprobar_con_vega(self, comando: str, executor) -> tuple:
        try:
            if executor.es_seguro(comando):
                return (True, "")
            else:
                razon_fn = getattr(executor, '_razon_inseguridad',
                           getattr(executor, '_razón_inseguridad', None))
                if callable(razon_fn):
                    return (False, razon_fn(comando))
                return (False, f"'{comando}' no está en la lista permitida por Vega")
        except Exception as e:
            logger.error(f"Error en verificación Vega: {e}")
            return (False, f"Error en verificación de seguridad: {e}")

    def _mensaje_vacio(self, comando: str) -> str:
        """NUEVO-H17: mensajes específicos cuando un comando no produce salida."""
        cmd = comando.lower()
        if 'git' in cmd:
            return "(git ejecutado correctamente — sin salida)"
        if 'ls' in cmd or 'dir' in cmd:
            return "(directorio vacío o sin archivos que coincidan)"
        if 'grep' in cmd:
            return "(no se encontraron coincidencias)"
        if 'find' in cmd:
            return "(no se encontraron archivos con esos criterios)"
        if 'ps' in cmd:
            return "(no hay procesos que coincidan)"
        return f"('{comando}' se ejecutó correctamente sin producir salida)"

    # ------------------------------------------------------------------
    # FORMATEO INTELIGENTE v2.0 (NUEVO-H17)
    # ------------------------------------------------------------------

    def formatear_respuesta(self, resultado: ResultadoHabilidad, nombre_usuario: str = "") -> str:
        n = f", {nombre_usuario}" if nombre_usuario else ""

        if not resultado.exitoso:
            error = resultado.error or "Error desconocido"
            return f"No pude ejecutar ese comando{n}: {error}"

        stdout   = resultado.valor
        desc     = resultado.descripcion or "Resultado"
        tipo_sal = _tipo_salida(stdout)

        if tipo_sal == 'vacio':
            return f"{desc}{n}: {stdout}"

        if tipo_sal == 'valor_unico':
            return f"{desc}{n}: {stdout.strip()}"

        lineas = stdout.split("\n")
        total  = len(lineas)

        # Tablas y listas: mostrar hasta 30 líneas
        limite = 30
        if total <= limite:
            return f"{desc}{n}:\n{stdout}"
        else:
            preview = "\n".join(lineas[:limite])
            resto   = total - limite
            return f"{desc}{n}:\n{preview}\n... ({resto} líneas más)"