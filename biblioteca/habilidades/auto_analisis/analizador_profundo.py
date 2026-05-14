# biblioteca/habilidades/auto_analisis/analizador_profundo.py
# ============================================================
# ANALIZADOR PROFUNDO — Bell analiza su propio código con radon
#
# Para UN archivo: métricas completas de ese archivo.
# Para TODA Bell: métricas de los archivos más críticos.
# Salida: paquete compacto para Groq (~150 tokens).
# ============================================================

import os
import ast
from pathlib import Path
from typing import Optional

try:
    from radon.complexity import cc_visit
    from radon.metrics import mi_visit
    RADON_OK = True
except ImportError:
    RADON_OK = False


_NIVEL_CC = {
    range(0, 6):   'bajo',
    range(6, 11):  'medio',
    range(11, 21): 'alto',
    range(21, 200): 'MUY ALTO — refactor urgente',
}

def _nivel_cc(cc: int) -> str:
    for rng, nivel in _NIVEL_CC.items():
        if cc in rng:
            return nivel
    return 'extremo'

def _nivel_mi(mi: float) -> str:
    if mi >= 80: return 'alta'
    if mi >= 65: return 'media'
    if mi >= 50: return 'baja'
    return 'MUY BAJA — difícil mantener'


def _analizar_archivo_python(ruta: Path, raiz: Path) -> Optional[dict]:
    """Analiza un archivo .py con radon + ast. Retorna métricas."""
    try:
        with open(ruta, 'r', encoding='utf-8', errors='ignore') as f:
            codigo = f.read()
    except Exception:
        return None

    lineas = codigo.count('\n') + 1
    rel = str(ruta.relative_to(raiz)).replace('\\', '/')

    # ── Complejidad ciclomática (radon) ──────────────────────
    cc_total = 0
    cc_max   = 0
    cc_items = []
    if RADON_OK:
        try:
            items = cc_visit(codigo)
            for item in items:
                cc_total += item.complexity
                if item.complexity > cc_max:
                    cc_max = item.complexity
                if item.complexity >= 10:
                    cc_items.append(f"{item.name}(CC={item.complexity})")
        except Exception:
            pass

    # ── Índice de mantenibilidad (radon) ─────────────────────
    mi_score = 0.0
    if RADON_OK:
        try:
            mi_score = mi_visit(codigo, multi=False)
        except Exception:
            pass

    # ── AST: funciones, clases, docstrings ───────────────────
    n_funciones  = 0
    n_sin_doc    = 0
    n_clases     = 0
    func_largas  = []
    try:
        tree = ast.parse(codigo)
        lineas_codigo = codigo.split('\n')
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                n_clases += 1
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                n_funciones += 1
                if not ast.get_docstring(node):
                    n_sin_doc += 1
                # Funciones muy largas
                try:
                    largo = node.end_lineno - node.lineno
                    if largo > 50:
                        func_largas.append(f"{node.name}({largo}L)")
                except Exception:
                    pass
    except Exception:
        pass

    return {
        'ruta':          rel,
        'nombre':        ruta.name,
        'lineas':        lineas,
        'cc_total':      cc_total,
        'cc_max':        cc_max,
        'cc_complejos':  cc_items[:3],
        'mi':            round(mi_score, 1),
        'clases':        n_clases,
        'funciones':     n_funciones,
        'sin_doc':       n_sin_doc,
        'func_largas':   func_largas[:3],
    }


def analizar_archivo(nombre_archivo: str, raiz_str: str) -> str:
    """
    Analiza UN archivo específico de Bell.
    Retorna paquete compacto para Groq.
    """
    raiz = Path(raiz_str)
    _IGNORAR = {'__pycache__', '.git', 'venv', '.venv'}

    # Buscar el archivo en toda la estructura
    encontrado = None
    for ruta in raiz.rglob('*.py'):
        if any(p in ruta.parts for p in _IGNORAR):
            continue
        if ruta.name.lower() == nombre_archivo.lower():
            encontrado = ruta
            break

    if not encontrado:
        return f"No encuentro '{nombre_archivo}' en mi estructura."

    m = _analizar_archivo_python(encontrado, raiz)
    if not m:
        return f"No pude analizar '{nombre_archivo}'."

    # Compacto: ~60 tokens
    res = f"{m['nombre']}: {m['lineas']}L, {m['clases']}clases, {m['funciones']}funcs"
    if m['cc_max'] > 0:
        res += f", CC_max={m['cc_max']}({_nivel_cc(m['cc_max'])})"
    if m['mi'] > 0:
        res += f", MI={m['mi']}({_nivel_mi(m['mi'])})"
    if m['sin_doc'] > 0:
        res += f", {m['sin_doc']}/{m['funciones']}sindoc"
    if m['cc_complejos']:
        res += f". Complejas: {', '.join(m['cc_complejos'])}"
    if m['func_largas']:
        res += f". Largas: {', '.join(m['func_largas'])}"
    return res


def analizar_todo_bell(raiz_str: str, top_n: int = 10) -> str:
    """
    Analiza TODOS los archivos Python de Bell.
    Retorna paquete compacto con los más críticos para Groq.
    """
    raiz = Path(raiz_str)
    _IGNORAR = {'__pycache__', '.git', 'venv', '.venv', 'node_modules'}

    resultados = []
    total_archivos = 0
    total_lineas   = 0

    for ruta in raiz.rglob('*.py'):
        if any(p in ruta.parts for p in _IGNORAR):
            continue
        m = _analizar_archivo_python(ruta, raiz)
        if m and m['lineas'] > 50:
            resultados.append(m)
            total_archivos += 1
            total_lineas   += m['lineas']

    if not resultados:
        return "No encontré archivos Python para analizar."

    # Ordenar por criticidad: CC alto + MI bajo + líneas
    def score(m):
        return m['cc_total'] * 2 + m['lineas'] / 100 + (100 - m['mi'])

    top = sorted(resultados, key=score, reverse=True)[:top_n]

    # Calcular promedios globales
    avg_mi = sum(m['mi'] for m in resultados if m['mi'] > 0) / max(1, len([m for m in resultados if m['mi'] > 0]))
    archivos_cc_alto = len([m for m in resultados if m['cc_max'] >= 11])
    archivos_sin_doc = len([m for m in resultados if m['sin_doc'] > m['funciones'] * 0.5])

    # Paquete ULTRA COMPRIMIDO — máx 80 tokens para que Groq tenga espacio de respuesta
    # Solo top 3 más críticos con las métricas esenciales
    top3 = top[:3]
    lineas_top = []
    for mx in top3:
        l = f"{mx['nombre']}({mx['lineas']}L"
        if mx['cc_max'] > 0: l += f",CC={mx['cc_max']}"
        if mx['mi'] > 0: l += f",MI={mx['mi']:.0f}"
        if mx['sin_doc'] > 0: l += f",{mx['sin_doc']}/{mx['funciones']}sindoc"
        l += ")"
        lineas_top.append(l)

    return (
        f"Bell: {total_archivos}archivos,{total_lineas}L,MI_avg={avg_mi:.0f}/100,"
        f"CC_alto={archivos_cc_alto},sindoc={archivos_sin_doc}. "
        f"Top críticos: {' | '.join(lineas_top)}"
    )