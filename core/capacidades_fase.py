"""
capacidades_fase.py — FUENTE ÚNICA DE VERDAD

QUÉ ES ESTE ARCHIVO:
    El único lugar donde vive la respuesta a "¿qué puede hacer Bell ahora?".
    Todos los módulos que necesiten saber si una capacidad está implementada
    importan desde aquí. Nadie más tiene su propia lista.

POR QUÉ EXISTE:
    Antes había TRES listas desincronizadas:
      A) _NO_IMPLEMENTADAS_FASE4A inline en motor_razonamiento.py (21 conceptos)
      B) capacidades_fase4a.no_implementadas en BELL_WHITELIST.json (17 conceptos)
      C) _no_disponibles en _hechos_capacidad() del motor (patrones de texto)

    Las tres tenían contenidos distintos. CONCEPTO_LEER y CONCEPTO_ESCRIBIR
    no estaban en A ni en B, aunque sí en C. Eso causaba que Bell mintiera
    sobre capacidades de archivos en el 90% de los casos.

CÓMO SE USA:
    from core.capacidades_fase import NO_IMPLEMENTADAS, esta_implementada, razon_no_implementada

DEPENDENCIAS: ninguna — solo stdlib de Python.
"""

# ═══════════════════════════════════════════════════════════════════════
# FASE ACTUAL
# ═══════════════════════════════════════════════════════════════════════

FASE_ACTUAL = "4A"

# ═══════════════════════════════════════════════════════════════════════
# CONCEPTOS NO IMPLEMENTADOS EN FASE 4A
#
# Formato: { "CONCEPTO_ID": "razón para el usuario" }
#
# Un concepto aquí significa:
#   - El código Python puede existir (grounding real)
#   - Pero Bell NO puede ejecutarlo para el usuario en esta fase
#   - Cualquier módulo que consulte esto debe responder NEGATIVA honesta
# ═══════════════════════════════════════════════════════════════════════

NO_IMPLEMENTADAS: dict = {
    # ── Operaciones de archivo — LOS DOS QUE CAUSABAN TODAS LAS MENTIRAS ──
    "CONCEPTO_LEER":    "Leer archivos del sistema de archivos está pendiente de implementar en Fase 4A",
    "CONCEPTO_ESCRIBIR": "Escribir/crear archivos está pendiente de implementar en Fase 4A",

    # ── Comandos shell no disponibles ─────────────────────────────────────
    "CONCEPTO_TOUCH":              "Crear archivos vacíos (touch) no implementado en Fase 4A",
    "CONCEPTO_MKDIR":              "Crear directorios (mkdir) no implementado en Fase 4A",
    "CONCEPTO_CAT":                "Mostrar contenido de archivos (cat) no implementado en Fase 4A",
    "CONCEPTO_HEAD":               "Mostrar inicio de archivos (head) no implementado en Fase 4A",
    "CONCEPTO_TAIL":               "Mostrar final de archivos (tail) no implementado en Fase 4A",
    "CONCEPTO_LESS":               "Paginar archivos (less) no implementado en Fase 4A",
    "CONCEPTO_MORE":               "Paginar archivos (more) no implementado en Fase 4A",
    "CONCEPTO_GREP":               "Buscar en archivos (grep) no implementado en Fase 4A",
    "CONCEPTO_FIND":               "Buscar archivos (find) no implementado en Fase 4A",
    "CONCEPTO_WC":                 "Contar palabras/líneas (wc) no implementado en Fase 4A",
    "CONCEPTO_CP":                 "Copiar archivos (cp) no implementado en Fase 4A",
    "CONCEPTO_MV":                 "Mover archivos (mv) no implementado en Fase 4A",
    "CONCEPTO_CHMOD":              "Cambiar permisos (chmod) no implementado en Fase 4A",
    "CONCEPTO_CHOWN":              "Cambiar propietario (chown) no implementado en Fase 4A",
    "CONCEPTO_DIFF":               "Comparar archivos (diff) no implementado en Fase 4A",
    "CONCEPTO_TAR":                "Comprimir/empaquetar (tar) no implementado en Fase 4A",
    "CONCEPTO_ZIP":                "Comprimir (zip) no implementado en Fase 4A",
    "CONCEPTO_UNZIP":              "Descomprimir (unzip) no implementado en Fase 4A",
    "CONCEPTO_WGET":               "Descargar de internet (wget) no implementado en Fase 4A",
    "CONCEPTO_CURL":               "Transferir datos (curl) no implementado en Fase 4A",
    "CONCEPTO_SSH":                "Conexión remota (ssh) no implementado en Fase 4A",
    "CONCEPTO_SCP":                "Copia remota (scp) no implementado en Fase 4A",
    "CONCEPTO_RSYNC":              "Sincronización (rsync) no implementado en Fase 4A",
    "CONCEPTO_ELIMINAR_DIRECTORIO":"Eliminar directorio no implementado en Fase 4A",
    "CONCEPTO_CAMBIAR_DIRECTORIO": "Cambiar directorio (cd) no implementado en Fase 4A",
    "CONCEPTO_STAT":               "Ver metadatos (stat) no implementado en Fase 4A",
    "CONCEPTO_FILE":               "Detectar tipo de archivo (file) no implementado en Fase 4A",
    "CONCEPTO_KILL":               "Terminar procesos (kill) no implementado en Fase 4A",
    "CONCEPTO_NANO":               "Editor de texto (nano) no implementado en Fase 4A",
}

# Set de solo IDs para búsquedas rápidas O(1)
NO_IMPLEMENTADAS_IDS: frozenset = frozenset(NO_IMPLEMENTADAS.keys())


# ═══════════════════════════════════════════════════════════════════════
# PATRONES DE TEXTO — para detección en mensajes del usuario
#
# Complementan la lista de IDs cuando el motor necesita detectar
# si el usuario está pidiendo algo no implementado por texto libre.
# ═══════════════════════════════════════════════════════════════════════

PATRONES_NO_IMPLEMENTADOS: dict = {
    "leer archivo":       "Leer archivos del sistema de archivos está pendiente de implementar",
    "leer el archivo":    "Leer archivos del sistema de archivos está pendiente de implementar",
    "lee el archivo":     "Leer archivos del sistema de archivos está pendiente de implementar",
    "crear archivo":      "Crear archivos está pendiente de implementar en Fase 4A",
    "crea un archivo":    "Crear archivos está pendiente de implementar en Fase 4A",
    "crea el archivo":    "Crear archivos está pendiente de implementar en Fase 4A",
    "crear un archivo":   "Crear archivos está pendiente de implementar en Fase 4A",
    "escribe un archivo": "Crear/escribir archivos está pendiente de implementar en Fase 4A",
    "escribir archivo":   "Crear/escribir archivos está pendiente de implementar en Fase 4A",
    "generar archivo":    "Generar archivos está pendiente de implementar en Fase 4A",
    "genera un archivo":  "Generar archivos está pendiente de implementar en Fase 4A",
    "acceder internet":   "Acceso a internet no está disponible en Fase 4A",
    "internet":           "Acceso a internet no está disponible en Fase 4A",
    "navegar":            "Navegación web no está disponible en Fase 4A",
    "imagen":             "Procesamiento de imágenes no está disponible en Fase 4A",
    "foto":               "Procesamiento de imágenes no está disponible en Fase 4A",
    "sesiones anteriores":"Memoria entre sesiones no está disponible en Fase 4A",
    "conversacion anterior": "Memoria entre sesiones no está disponible en Fase 4A",
}


# ═══════════════════════════════════════════════════════════════════════
# API PÚBLICA
# ═══════════════════════════════════════════════════════════════════════

def esta_implementada(concepto_id: str) -> bool:
    """
    ¿Está este concepto implementado para el usuario en la fase actual?

    Args:
        concepto_id: ID del concepto, ej: "CONCEPTO_LEER"

    Returns:
        True si está implementado y disponible para el usuario.
        False si existe en el código pero no está habilitado en esta fase.

    Uso:
        if not esta_implementada("CONCEPTO_LEER"):
            return decision_negativa_honesta()
    """
    return concepto_id not in NO_IMPLEMENTADAS_IDS


def razon_no_implementada(concepto_id: str) -> str:
    """
    Razón por la que un concepto no está implementado.

    Args:
        concepto_id: ID del concepto

    Returns:
        String con la razón, o "" si está implementado.
    """
    return NO_IMPLEMENTADAS.get(concepto_id, "")


def detectar_patron_no_implementado(mensaje: str) -> tuple:
    """
    Detecta si el mensaje del usuario pide algo no implementado por texto libre.

    Args:
        mensaje: Texto del usuario en minúsculas

    Returns:
        (patron_encontrado: str, razon: str) o ("", "") si no hay match.
    """
    msg = mensaje.lower()
    for patron, razon in PATRONES_NO_IMPLEMENTADOS.items():
        if patron in msg:
            return (patron, razon)
    return ("", "")


def obtener_lista_no_implementadas() -> list:
    """
    Retorna lista de IDs de conceptos no implementados.
    Para compatibilidad con código que espera una lista.
    """
    return list(NO_IMPLEMENTADAS_IDS)