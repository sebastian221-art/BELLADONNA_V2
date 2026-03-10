"""
capacidades_fase.py — FUENTE ÚNICA DE VERDAD — VERSION v1.1

CAMBIOS v1.1 sobre v1.0:
═══════════════════════════════════════════════════════════════════
FIX-BUG7  CONCEPTO_DESCARGAR no estaba bloqueado
          CAUSA: Bell respondía "eso está dentro de mis capacidades"
          cuando el usuario pedía "descarga el archivo X" porque
          CONCEPTO_DESCARGAR no existía en NO_IMPLEMENTADAS ni en
          PATRONES_NO_IMPLEMENTADOS.
          FIX:   Agregar CONCEPTO_DESCARGAR, CONCEPTO_WGET y
          CONCEPTO_CURL a NO_IMPLEMENTADAS.
          Agregar patrones "descarga", "descargar", "bajar archivo",
          "download" a PATRONES_NO_IMPLEMENTADOS.
═══════════════════════════════════════════════════════════════════

QUÉ ES ESTE ARCHIVO:
    El único lugar donde vive la respuesta a "¿qué puede hacer Bell ahora?".
    Todos los módulos que necesiten saber si una capacidad está implementada
    importan desde aquí. Nadie más tiene su propia lista.

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
# ═══════════════════════════════════════════════════════════════════════

NO_IMPLEMENTADAS: dict = {
    # ── Operaciones de archivo ────────────────────────────────────────
    "CONCEPTO_LEER":    "Leer archivos del sistema de archivos está pendiente de implementar en Fase 4A",
    "CONCEPTO_ESCRIBIR": "Escribir/crear archivos está pendiente de implementar en Fase 4A",

    # ── FIX-BUG7 v1.1: Descargar archivos de internet ─────────────────
    "CONCEPTO_DESCARGAR": "Descargar archivos de internet no está implementado en Fase 4A",

    # ── Comandos shell no disponibles ─────────────────────────────────
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
# PATRONES DE TEXTO
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
    # FIX-BUG7 v1.1: patrones de descarga
    "descarga":           "Descargar archivos de internet no está implementado en Fase 4A",
    "descargar":          "Descargar archivos de internet no está implementado en Fase 4A",
    "bajar el archivo":   "Descargar archivos de internet no está implementado en Fase 4A",
    "bajar archivo":      "Descargar archivos de internet no está implementado en Fase 4A",
    "download":           "Descargar archivos de internet no está implementado en Fase 4A",
    # Patrones existentes preservados
    "acceder internet":   "Acceso a internet no está disponible en Fase 4A",
    "internet":           "Acceso a internet no está disponible en Fase 4A",
    "navegar":            "Navegación web no está disponible en Fase 4A",
    "imagen":             "Procesamiento de imágenes no está disponible en Fase 4A",
    "foto":               "Procesamiento de imágenes no está disponible en Fase 4A",
    "sesiones anteriores":"Memoria entre sesiones no está disponible en Fase 4A",
    "conversacion anterior": "Memoria entre sesiones no está disponible en Fase 4A",
}


# ═══════════════════════════════════════════════════════════════════════
# API PÚBLICA (idéntica a v1.0)
# ═══════════════════════════════════════════════════════════════════════

def esta_implementada(concepto_id: str) -> bool:
    return concepto_id not in NO_IMPLEMENTADAS_IDS


def razon_no_implementada(concepto_id: str) -> str:
    return NO_IMPLEMENTADAS.get(concepto_id, "")


def detectar_patron_no_implementado(mensaje: str) -> tuple:
    msg = mensaje.lower()
    for patron, razon in PATRONES_NO_IMPLEMENTADOS.items():
        if patron in msg:
            return (patron, razon)
    return ("", "")


def obtener_lista_no_implementadas() -> list:
    return list(NO_IMPLEMENTADAS_IDS)