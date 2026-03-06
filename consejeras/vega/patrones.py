"""
consejeras/vega/patrones.py — VERSION v2.0

CAMBIOS v2.0 sobre v1.0:
════════════════════════════════════════════════════════════════════
FASE 4B — Vega analiza riesgo REAL en vez de bloquear por palabras.

PROBLEMA v1.0:
  Vega bloqueaba "eliminar" + "todo/todos" pero también dejaba pasar
  DELETE FROM clientes sin WHERE (que es igual de destructivo).
  Además bloqueaba operaciones legítimas de BD por falsos positivos.

NUEVA LÓGICA:
  Vega tiene 3 niveles de respuesta:
    BLOQUEAR  → No ejecuta. Error claro al usuario.
    ADVERTIR  → Ejecuta pero avisa (nota en la respuesta).
    OK        → Ejecuta sin comentario.

  Criterios exactos:

  BLOQUEAR:
    - DELETE/eliminar SIN identificador específico (sin WHERE, sin nombre)
    - Eliminar TODOS los datos de la aplicación entera (no de una tabla)
    - Auto-modificación del código de Bell
    - Acceso a credenciales/passwords

  ADVERTIR (ejecuta con nota, no bloquea):
    - DROP TABLE con nombre específico → "Eliminará tabla X permanentemente"
    - Vaciar tabla completa → "Eliminará todos los registros de X"
    - DELETE con WHERE → ejecuta normalmente (tiene filtro específico)

  OK (sin comentario):
    - INSERT, UPDATE con WHERE
    - CREATE TABLE
    - SELECT
    - Cualquier operación con target específico

COMPATIBILIDAD: Vega.py no necesita cambios — solo cambia este módulo.
"""
from typing import Dict, List, Tuple
import re


class PatronesPeligrosos:
    """
    Biblioteca de patrones para análisis de riesgo real.

    Vega v2.0: analiza el CONTEXTO, no solo las palabras.
    La misma palabra "eliminar" puede ser OK o peligrosa
    dependiendo de si tiene filtro específico o no.
    """

    def __init__(self):
        # ── AUTO-MODIFICACIÓN (siempre bloquear) ──────────────────────
        self.palabras_modificacion = [
            'modificar', 'modifica', 'cambiar', 'cambia',
            'editar', 'edita', 'alterar', 'altera', 'reescribir',
        ]
        self.palabras_auto_referencia = [
            'tu código', 'mi código', 'código de bell',
            'core', 'tu mismo', 'ti mismo', 'belladonna',
            'tus archivos de código', 'tu sistema de archivos de código',
            'motor_razonamiento', 'generador_salida', 'main.py',
        ]

        # ── PRIVACIDAD (siempre bloquear) ─────────────────────────────
        self.palabras_sensibles = [
            'contraseña', 'contraseñas', 'password', 'passwords',
            'credencial', 'credenciales', 'clave secreta', 'claves secretas',
            'token secreto', 'api key', 'secret key', 'private key',
        ]
        self.palabras_acceso = [
            'leer', 'lee', 'mostrar', 'muestra', 'escribir',
            'guardar', 'guardar', 'read', 'write', 'dame',
        ]

        # ── DESTRUCTIVO MASIVO — contexto importa ─────────────────────
        # Palabras destructivas básicas
        self.palabras_destructivas = [
            'eliminar', 'elimina', 'borrar', 'borra',
            'delete', 'remove', 'destruir', 'destruye',
        ]
        # Alcance total SIN tabla específica = realmente peligroso
        self.palabras_alcance_total = [
            'todo', 'todos', 'todas', 'all',
            'completo', 'completa', 'entera', 'entero',
        ]
        # Palabras que indican target específico = OK con advertencia máxima
        self.palabras_target_bd = [
            'tabla', 'table', 'registro', 'registros', 'fila', 'filas',
            'from', 'de la', 'del', 'en la', 'en el',
        ]

    # ------------------------------------------------------------------
    # DETECCIÓN PRINCIPAL
    # ------------------------------------------------------------------

    def detectar_todos_los_riesgos(self, texto: str) -> List[str]:
        """
        Analiza todos los riesgos en el texto.
        Retorna lista de tipos de riesgo (solo los que BLOQUEAR).
        ADVERTIR se maneja dentro de la habilidad, no aquí.
        """
        riesgos = []

        if self.es_auto_modificacion(texto):
            riesgos.append('AUTO_MODIFICACION')

        if self.viola_privacidad(texto):
            riesgos.append('VIOLACION_PRIVACIDAD')

        if self.es_accion_destructiva(texto):
            riesgos.append('ACCION_DESTRUCTIVA')

        return riesgos

    # ------------------------------------------------------------------
    # DETECTORES INDIVIDUALES
    # ------------------------------------------------------------------

    def es_accion_destructiva(self, texto: str) -> bool:
        """
        SOLO bloquea destrucción masiva SIN contexto de BD específico.

        Casos que SÍ bloquea:
          "elimina todos los datos"           → BLOQUEAR
          "borra todo"                        → BLOQUEAR
          "elimina todo el sistema"           → BLOQUEAR

        Casos que NO bloquea (tienen target de BD):
          "elimina la tabla usuarios"         → OK (advertir en habilidad)
          "vacía la tabla clientes"           → OK (advertir en habilidad)
          "elimina a Juan de usuarios"        → OK (tiene WHERE)
          "DELETE FROM clientes WHERE id=1"   → OK
          "DELETE FROM clientes"              → OK (habilidad decide el nivel)
          "borra todos los registros de X"    → OK (target específico)
        """
        texto_lower = texto.lower()

        tiene_destruccion = any(p in texto_lower for p in self.palabras_destructivas)
        if not tiene_destruccion:
            return False

        tiene_alcance_total = any(p in texto_lower for p in self.palabras_alcance_total)
        if not tiene_alcance_total:
            return False

        # Tiene destrucción + alcance total. PERO:
        # Si también tiene referencia a BD específica, NO es destructivo masivo
        tiene_target_bd = any(p in texto_lower for p in self.palabras_target_bd)
        if tiene_target_bd:
            # "borra todos los registros de X" → tiene target → no bloquear aquí
            # La habilidad SQLite maneja vaciar_tabla con advertencia
            return False

        # "elimina todo", "borra todos" sin referencia a BD → SÍ bloquear
        return True

    def es_auto_modificacion(self, texto: str) -> bool:
        """
        Detecta intentos de que Bell modifique su propio código.
        Igual que v1.0 — este criterio es correcto.
        """
        texto_lower = texto.lower()

        tiene_modificacion = any(p in texto_lower for p in self.palabras_modificacion)
        if not tiene_modificacion:
            return False

        return any(p in texto_lower for p in self.palabras_auto_referencia)

    def viola_privacidad(self, texto: str) -> bool:
        """
        Detecta acceso a información sensible (passwords, tokens).
        Solo bloquea si es acceso a CREDENCIALES reales, no a cualquier dato.
        """
        texto_lower = texto.lower()

        tiene_sensible = any(p in texto_lower for p in self.palabras_sensibles)
        if not tiene_sensible:
            return False

        return any(p in texto_lower for p in self.palabras_acceso)

    # ------------------------------------------------------------------
    # ANÁLISIS DE RIESGO BD (helper para diagnóstico)
    # ------------------------------------------------------------------

    def analizar_riesgo_bd(self, texto: str) -> Tuple[str, str]:
        """
        Analiza el nivel de riesgo de una operación BD en lenguaje natural.
        Retorna (nivel, descripcion):
          "BLOQUEAR"  → no ejecutar
          "ADVERTIR"  → ejecutar con nota
          "OK"        → ejecutar sin comentario

        Usado por la habilidad SQLite para operaciones de escritura.
        Vega.revisar() usa detectar_todos_los_riesgos() para veto total.
        """
        texto_lower = texto.lower()

        # DROP TABLE con nombre → advertir
        if re.search(r'(?:drop\s+table|elimin[a-z]*\s+(?:la\s+)?tabla|borra(?:r)?\s+(?:la\s+)?tabla)\s+\w+',
                     texto_lower):
            m = re.search(r'(?:tabla|table)\s+(\w+)', texto_lower)
            nombre = m.group(1) if m else "desconocida"
            return ("ADVERTIR", f"Eliminará permanentemente la tabla '{nombre}' y todos sus datos.")

        # Vaciar tabla → advertir
        if re.search(r'(?:vac[ií]a|limpia|truncate|borra(?:r)?\s+todos|elimin[a-z]*\s+todos)',
                     texto_lower):
            m = re.search(r'(?:tabla|table|de\s+|en\s+)(\w+)', texto_lower)
            nombre = m.group(1) if m else "X"
            if nombre.lower() not in {'la', 'el', 'los', 'las', 'de', 'en'}:
                return ("ADVERTIR", f"Eliminará todos los registros de '{nombre}'.")

        # DELETE con WHERE → OK
        if re.search(r'delete\s+from\s+\w+\s+where', texto_lower):
            return ("OK", "")

        # DELETE sin WHERE → bloquear (ya lo maneja la habilidad)
        if re.search(r'delete\s+from\s+\w+\s*$', texto_lower):
            return ("BLOQUEAR", "DELETE sin WHERE eliminará TODOS los registros.")

        # INSERT, UPDATE, CREATE → OK
        if re.search(r'^(?:insert|update|create)', texto_lower):
            return ("OK", "")

        return ("OK", "")