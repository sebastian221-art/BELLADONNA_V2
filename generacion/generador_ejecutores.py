# -*- coding: utf-8 -*-
"""
generacion/generador_ejecutores.py  VERSION v1.0

PROPÓSITO:
==========
Ejecutor genérico de habilidades para el generador de salida.
Análogo a razonamiento/patrones_habilidades.py pero para la capa
de generación: el generador consulta este módulo en vez de crecer.

PRINCIPIO DE ESCALABILIDAD (igual que motor v8.9):
====================================================
Para que el generador ejecute una nueva habilidad:

    1. Crear habilidades/mi_habilidad.py   (heredar BaseHabilidad)
    2. Registrar en registro_habilidades.py con prioridad
    3. Agregar patrones en patrones_habilidades.py
    → generador_salida.py NO se toca nunca más.
    → Este archivo NO se toca nunca más.

FLUJO:
======
    generador_salida.py
        _ejecutar_shell_conversacional()
            ↓ habilidad_id != "SHELL"
        ejecutar_habilidad_generica(habilidad_id, hechos, msg, nombre)
            ↓
        generador_ejecutores.py  ← este módulo
            ↓
        RegistroHabilidades → HabilidadSQLite (o cualquier futura)
            ↓
        resultado verificado + formateado

API PÚBLICA:
============
    ejecutar_habilidad_generica(habilidad_id, hechos, msg, nombre) → str
    verificar_resultado_habilidad(resultado, mensaje_original)      → resultado

COMPATIBILIDAD: generador_salida v8.4+, registro_habilidades v1.5+
"""

import unicodedata
import logging
from typing import Optional

_log = logging.getLogger("generador_ejecutores")

# ── Import defensivo del registro ────────────────────────────────────
try:
    from habilidades.registro_habilidades import RegistroHabilidades, HabilidadMatch
    _REGISTRO_DISPONIBLE = True
except ImportError:
    _REGISTRO_DISPONIBLE = False
    HabilidadMatch = None

# ── Mensajes de veto BD — análogo a _MENSAJES_VETO en generador ──────
_MENSAJES_VETO_BD = {
    'INSERT':  "Vega no aprueba esa operacion: solo puedo leer datos en Fase 4A.",
    'UPDATE':  "Vega no aprueba esa operacion: modificar registros no esta permitido en Fase 4A.",
    'DELETE':  "Vega no aprueba esa operacion: eliminar datos no esta permitido en Fase 4A.",
    'DROP':    "Vega no aprueba esa operacion: eliminar tablas no esta permitido en Fase 4A.",
    'DEFAULT': "Vega no aprobo esa operacion.",
}


# ======================================================================
# NORMALIZADOR — idéntico al del motor y al del generador
# ======================================================================

def _norm(texto: str) -> str:
    """Quita tildes y diacríticos. Convierte a minúsculas."""
    nfkd = unicodedata.normalize('NFD', texto)
    sin_tildes = ''.join(c for c in nfkd if unicodedata.category(c) != 'Mn')
    return sin_tildes.lower()


# ======================================================================
# VERIFICADOR DE RESULTADO (Echo)
# Mismo que _verificar_resultado_habilidad() del generador — extraído
# aquí para no duplicar lógica cuando se llama desde este módulo.
# ======================================================================

def verificar_resultado_habilidad(resultado, mensaje_original: str):
    """
    BUG-G10 FIX: str() defensivo antes de .strip().
    Echo verifica que el resultado sea consistente:
    - Exitoso sin valor → marcar como fallido
    - Valor no-str → convertir
    - Descripción afirmativa en resultado fallido → limpiar
    """
    if resultado is None:
        return resultado

    valor_str = str(resultado.valor) if resultado.valor is not None else ""

    if resultado.exitoso and not valor_str.strip():
        resultado.exitoso = False
        resultado.error   = "Echo: resultado inconsistente — exito sin valor."
        resultado.valor   = ""
        return resultado

    if not isinstance(resultado.valor, str):
        resultado.valor = valor_str

    if not resultado.exitoso and resultado.descripcion:
        afirmaciones = [
            "el resultado es", "la derivada es", "la integral es",
            "el limite es", "las soluciones son",
        ]
        if any(a in resultado.descripcion.lower() for a in afirmaciones):
            resultado.descripcion = ""

    return resultado


# ======================================================================
# EJECUTOR GENÉRICO — punto de extensión principal
# ======================================================================

def ejecutar_habilidad_generica(
    habilidad_id:     str,
    hechos:           dict,
    mensaje_original: str,
    nombre_usuario:   str = "",
) -> str:
    """
    Ejecuta CUALQUIER habilidad registrada por su habilidad_id.
    Llamado por generador_salida._ejecutar_shell_conversacional()
    cuando habilidad_id != "SHELL" (Ruta C).

    Flujo:
        1. Obtener habilidad del registro por habilidad_id
        2. Re-detectar con mensaje normalizado para obtener match completo
        3. Si no matchea: construir match mínimo desde hechos del motor
        4. Ejecutar via registro.ejecutar()
        5. Verificar con Echo (verificar_resultado_habilidad)
        6. Formatear via registro.formatear()

    El generador no necesita saber nada sobre la habilidad.
    Este módulo tampoco — solo habla con RegistroHabilidades.
    """
    n = f", {nombre_usuario}" if nombre_usuario else ""

    if not _REGISTRO_DISPONIBLE:
        return (
            f"El modulo de habilidades no esta disponible{n}. "
            f"No puedo ejecutar la habilidad {habilidad_id}."
        )

    try:
        registro  = RegistroHabilidades.obtener()
        habilidad = registro.obtener_habilidad(habilidad_id)

        if habilidad is None:
            return (
                f"La habilidad '{habilidad_id}' no esta registrada{n}. "
                "Verifica que el modulo este cargado correctamente."
            )

        # ── Paso 1: intentar re-detectar con mensaje normalizado ──────
        # El motor ya detectó la intención general, pero la habilidad
        # necesita su propio match para extraer parámetros precisos
        # (operacion, tabla, sql, etc.)
        match = None
        msg_norm = _norm(mensaje_original) if mensaje_original else ""

        try:
            match = habilidad.detectar(msg_norm, [], hechos or {})
        except Exception as e:
            _log.debug(f"detectar() fallo para {habilidad_id}: {e}")

        # ── Paso 2: match mínimo desde hechos del motor ───────────────
        # Si la habilidad no matcheó con el mensaje normalizado,
        # usar los hechos que dejó el motor (_hechos_ejecucion_bd).
        # Esto cubre casos donde el patrón de la habilidad y el del
        # motor difieren ligeramente.
        if match is None and HabilidadMatch is not None:
            match = HabilidadMatch(
                habilidad_id=habilidad_id,
                confianza=1.0,
                parametros={
                    "operacion":   (hechos or {}).get("operacion", ""),
                    "tabla":       (hechos or {}).get("tabla", ""),
                    "descripcion": (hechos or {}).get("descripcion", ""),
                    "mensaje":     mensaje_original,
                },
                habilidad=habilidad,
            )

        if match is None:
            return (
                f"No pude identificar la operacion solicitada{n}. "
                f"Intenta reformular la consulta para {habilidad_id}."
            )

        # ── Paso 3: ejecutar ──────────────────────────────────────────
        resultado = registro.ejecutar(match, nombre_usuario)
        resultado = verificar_resultado_habilidad(resultado, mensaje_original)

        # ── Paso 4: responder ─────────────────────────────────────────
        if resultado.exitoso:
            return registro.formatear(match, resultado, nombre_usuario)
        else:
            error = resultado.error or f"No pude completar la operacion de {habilidad_id}."

            # Detectar veto de Vega con mensaje específico por tipo
            if "Vega bloqueo" in error or "Vega bloqueó" in error:
                for clave, msg_veto in _MENSAJES_VETO_BD.items():
                    if clave in error.upper():
                        return msg_veto
                return _MENSAJES_VETO_BD['DEFAULT']

            return f"No pude ejecutar esa operacion{n}: {error}"

    except Exception as e:
        _log.error(f"ejecutar_habilidad_generica({habilidad_id}) error: {e}")
        return f"Ocurrio un error al ejecutar la habilidad{n}: {e}"