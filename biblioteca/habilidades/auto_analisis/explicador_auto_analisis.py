# biblioteca/habilidades/auto_analisis/explicador_auto_analisis.py
# ============================================================
# EXPLICADOR AUTO-ANÁLISIS — sin Groq, 100% Bell
#
# Convierte los datos compactos de analizador_profundo.py
# en respuestas en voz Bell con métricas reales.
#
# Reemplaza _groq_analisis_profundo() en motor_auto_analisis.py
# ============================================================

import re
from typing import Optional


def explicar_analisis_total(datos: str, pregunta: str = '') -> str:
    """
    Convierte el string de analizar_todo_bell() + el informe de _generar_informe_mejoras()
    en respuesta Bell conversacional con datos reales.
    """
    if not datos:
        return ''

    archivos   = _extraer_int(datos, r'(\d+)archivos')
    lineas     = _extraer_int(datos, r'(\d+)L,')
    mi_avg     = _extraer_float(datos, r'MI_avg=([\d.]+)')
    cc_alto    = _extraer_int(datos, r'CC_alto=(\d+)')
    sin_doc    = _extraer_int(datos, r'sindoc=(\d+)')

    criticos = []
    for m in re.finditer(r'(\w+\.py)\((\d+)L,CC=(\d+),MI=([\d.]+)', datos):
        criticos.append({
            'nombre': m.group(1),
            'lineas': int(m.group(2)),
            'cc':     int(m.group(3)),
            'mi':     float(m.group(4)),
        })

    partes = []

    if archivos and lineas:
        partes.append(
            f"Tengo {archivos} archivos Python, {lineas:,} líneas. "
            f"Salud general MI={mi_avg}/100 — {_nivel_mi(mi_avg)}"
        )

    if cc_alto and cc_alto > 0:
        partes.append(
            f"Hay {cc_alto} función(es) con CC alto — más de 10 caminos de ejecución, "
            f"difícil de testear sin dejar rutas sin cubrir."
        )

    if sin_doc and sin_doc > 30:
        partes.append(
            f"{sin_doc} funciones sin docstring — documentar las públicas debería ser prioridad."
        )
    elif sin_doc and sin_doc > 0:
        partes.append(f"{sin_doc} funciones sin docstring.")

    if criticos:
        top = ', '.join(
            f"{a['nombre']} (CC={a['cc']}, MI={a['mi']})" for a in criticos[:3]
        )
        accion = 'Los dividiría en módulos más pequeños.' if criticos[0]['cc'] > 20 else ''
        partes.append(f"Los más críticos: {top}. {accion}".strip())

    return ' '.join(partes)


def combinar_con_informe(analisis_total: str, informe_mejoras: str) -> str:
    """
    Combina el análisis de métricas (Radon) con el informe de mejoras
    estructurales (_generar_informe_mejoras). Son datos complementarios.
    """
    partes = []
    if analisis_total:
        partes.append(analisis_total)
    if informe_mejoras and informe_mejoras != 'Arquitectura saludable.':
        partes.append(informe_mejoras)
    return ' '.join(partes) if partes else 'Arquitectura saludable.'


def explicar_archivo(datos: str, nombre_archivo: str, base_info: str = '') -> str:
    """
    Convierte el string de analizar_archivo() + _responder_archivo()
    en respuesta Bell sobre un archivo específico.
    """
    if not datos:
        return base_info or f"No encontré datos de calidad sobre {nombre_archivo}."

    lineas   = _extraer_int(datos, r'(\d+)L,')
    clases   = _extraer_int(datos, r'(\d+)clas')
    funcs    = _extraer_int(datos, r'(\d+)func')
    cc_max   = _extraer_int(datos, r'CC_max=(\d+)')
    mi       = _extraer_float(datos, r'MI=([\d.]+)')
    sin_doc  = _extraer_int(datos, r'(\d+)/\d+sindoc')
    complejas = re.findall(r'Complejas: (.+?)(?:\.|Largas|$)', datos)
    largas    = re.findall(r'Largas: (.+?)(?:\.|$)', datos)

    partes = []

    if base_info:
        partes.append(base_info)

    if mi is not None:
        partes.append(
            f"Calidad: MI={mi}/100 — {_nivel_mi(mi)}"
        )

    if cc_max and cc_max > 10:
        partes.append(
            f"Complejidad máxima CC={cc_max} ({'crítica' if cc_max > 20 else 'alta'}). "
            + (f"Funciones: {complejas[0]}." if complejas else '')
        )
    elif cc_max:
        partes.append(f"CC={cc_max} — saludable.")

    if sin_doc and sin_doc > 0:
        total = _extraer_int(datos, r'\d+/(\d+)sindoc') or funcs or 1
        partes.append(f"{sin_doc}/{total} funciones sin docstring.")

    if largas:
        partes.append(f"Función más larga: {largas[0]}.")

    return ' '.join(partes) if partes else (base_info or datos)


def explicar_introspeccion(datos: str, base_introspeccion: str, escaneo=None) -> str:
    """
    Combina la introspección cualitativa con las métricas reales.
    """
    partes = []

    if base_introspeccion:
        partes.append(base_introspeccion)

    mi_avg  = _extraer_float(datos, r'MI_avg=([\d.]+)') if datos else None
    cc_alto = _extraer_int(datos, r'CC_alto=(\d+)') if datos else None

    if mi_avg is not None and cc_alto is not None:
        estado = 'saludable' if mi_avg >= 65 else ('aceptable' if mi_avg >= 40 else 'necesita trabajo')
        partes.append(
            f"En métricas: MI promedio {mi_avg}/100 ({estado}), "
            f"{cc_alto} funciones con alta complejidad. "
            f"Refactorizar esas funciones me haría más mantenible."
        )

    return ' '.join(partes) if partes else (base_introspeccion or 'Sin datos suficientes.')


# ── Helpers ───────────────────────────────────────────────────────────────────

def _nivel_mi(mi: Optional[float]) -> str:
    if mi is None: return ''
    if mi >= 80: return 'excelente.'
    if mi >= 65: return 'saludable, fácil de mantener.'
    if mi >= 40: return 'funcional, con margen de mejora.'
    if mi >= 20: return 'difícil de mantener, deuda técnica acumulada.'
    return 'crítico — necesita refactorización urgente.'


def _extraer_int(texto: str, patron: str) -> Optional[int]:
    m = re.search(patron, texto)
    return int(m.group(1)) if m else None


def _extraer_float(texto: str, patron: str) -> Optional[float]:
    m = re.search(patron, texto)
    return float(m.group(1)) if m else None