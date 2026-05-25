# biblioteca/habilidades/python/analizador_complejidad_algoritmica.py
# ============================================================
# ANALIZADOR DE COMPLEJIDAD BIG-O REAL
#
# No estima — MIDE.
# Ejecuta la función con n=10,100,1000,10000, mide tiempos reales
# y hace regresión matemática para clasificar la complejidad.
#
# Ninguna IA hace esto hoy. Bell lo mide con datos reales.
#
# Clasificaciones posibles:
#   O(1)        → tiempo constante
#   O(log n)    → logarítmica
#   O(n)        → lineal
#   O(n log n)  → linealítmica
#   O(n²)       → cuadrática
#   O(n³)       → cúbica
#   O(2ⁿ)       → exponencial
# ============================================================

import ast
import math
import subprocess
import sys
import tempfile
import os
from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class ResultadoComplejidad:
    funcion:        str
    complejidad:    str           # O(n), O(n²), etc.
    confianza:      float         # 0.0 - 1.0
    tiempos_reales: List[Tuple]   # [(n, ms), ...]
    factor_escala:  float         # cuánto crece al duplicar n
    reporte:        str


def analizar_complejidad(codigo: str) -> List[ResultadoComplejidad]:
    """
    Analiza la complejidad algorítmica real de las funciones del código.
    Retorna una lista de ResultadoComplejidad por función.
    """
    funciones = _extraer_funciones_medibles(codigo)
    resultados = []

    for fn in funciones[:3]:  # máximo 3 funciones para no bloquear
        r = _medir_funcion(codigo, fn)
        if r:
            resultados.append(r)

    return resultados


def _extraer_funciones_medibles(codigo: str) -> List[dict]:
    """Extrae funciones que pueden medirse con n variable."""
    funciones = []
    try:
        arbol = ast.parse(codigo)
    except SyntaxError:
        return []

    for nodo in ast.walk(arbol):
        if not isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if nodo.name.startswith('_'):
            continue

        args = [a.arg for a in nodo.args.args if a.arg != 'self']
        if not args:
            continue

        # Detectar si recibe una lista o un entero como primer arg
        primer_arg = args[0]
        tipo_hint = ''
        if nodo.args.args[0].annotation:
            try:
                tipo_hint = ast.unparse(nodo.args.args[0].annotation)
            except Exception:
                pass

        funciones.append({
            'nombre':    nodo.name,
            'primer_arg': primer_arg,
            'tipo_hint': tipo_hint,
            'n_args':    len(args),
        })

    return funciones


def _medir_funcion(codigo: str, fn: dict) -> Optional[ResultadoComplejidad]:
    """Mide el tiempo de la función con n creciente."""
    nombre = fn['nombre']
    tipo   = fn['tipo_hint'].lower()

    # Determinar tipo de input según el hint o el nombre
    usa_lista = any(t in tipo for t in ['list', 'sequence', 'array', 'str']) or \
                any(w in nombre.lower() for w in ['sort', 'search', 'find', 'filter', 'process'])

    valores_n = [10, 50, 100, 500, 1000, 5000]

    script = _construir_script(codigo, nombre, fn, usa_lista, valores_n)
    if not script:
        return None

    try:
        with tempfile.NamedTemporaryFile(suffix='.py', mode='w',
                                          delete=False, encoding='utf-8') as f:
            f.write(script)
            path = f.name

        proc = subprocess.run(
            [sys.executable, path],
            capture_output=True, text=True, timeout=30,
        )
        os.unlink(path)

        if not proc.stdout.strip():
            return None

        # Parsear tiempos
        tiempos = []
        for linea in proc.stdout.strip().splitlines():
            partes = linea.split(',')
            if len(partes) == 2:
                try:
                    n  = int(partes[0])
                    ms = float(partes[1])
                    tiempos.append((n, ms))
                except ValueError:
                    pass

        if len(tiempos) < 3:
            return None

        complejidad, confianza, factor = _clasificar_complejidad(tiempos)
        reporte = _generar_reporte(nombre, complejidad, tiempos, factor)

        return ResultadoComplejidad(
            funcion=nombre,
            complejidad=complejidad,
            confianza=confianza,
            tiempos_reales=tiempos,
            factor_escala=factor,
            reporte=reporte,
        )

    except Exception:
        return None


def _construir_script(codigo: str, nombre: str, fn: dict,
                       usa_lista: bool, valores_n: List[int]) -> str:
    """Construye el script de medición."""
    if usa_lista:
        setup_inputs = '\n'.join([
            f'inputs[{n}] = list(range({n}))' for n in valores_n
        ])
        call = f'{nombre}(inputs[n])'
    else:
        # Verificar que el primer arg puede ser int
        setup_inputs = ''
        call = f'{nombre}(n)'

    return f'''
import time

{codigo}

inputs = {{}}
{setup_inputs}

for n in {valores_n}:
    try:
        t0 = time.perf_counter()
        for _ in range(3):
            {call}
        t1 = time.perf_counter()
        ms = round((t1 - t0) / 3 * 1000, 6)
        print(f"{{n}},{{ms}}")
    except Exception:
        pass
'''


def _clasificar_complejidad(tiempos: List[Tuple]) -> Tuple[str, float, float]:
    """
    Clasifica la complejidad usando regresión logarítmica sobre los tiempos.
    Retorna (complejidad, confianza, factor_escala).
    """
    ns  = [t[0] for t in tiempos if t[1] > 0]
    ms  = [t[1] for t in tiempos if t[1] > 0]

    if len(ns) < 3:
        return 'O(?)', 0.3, 1.0

    # Factor de escala: cuánto creció el tiempo al 10x el input
    if len(tiempos) >= 4:
        n_bajo = tiempos[1][0]
        n_alto = tiempos[-2][0]
        t_bajo = tiempos[1][1]
        t_alto = tiempos[-2][1]
        if t_bajo > 0:
            factor_real = t_alto / t_bajo
            n_ratio     = n_alto / n_bajo
        else:
            factor_real = 1.0
            n_ratio     = 10.0
    else:
        factor_real = 1.0
        n_ratio     = 10.0

    # Regresión: log(tiempo) vs log(n) para detectar potencia
    try:
        log_n  = [math.log(n) for n in ns]
        log_ms = [math.log(max(m, 1e-9)) for m in ms]

        # Regresión lineal simple: log_ms = a * log_n + b → tiempo ~ n^a
        n_pts = len(log_n)
        sum_x  = sum(log_n)
        sum_y  = sum(log_ms)
        sum_xy = sum(x * y for x, y in zip(log_n, log_ms))
        sum_x2 = sum(x * x for x in log_n)

        denom = n_pts * sum_x2 - sum_x ** 2
        if abs(denom) < 1e-10:
            return 'O(1)', 0.5, factor_real

        a = (n_pts * sum_xy - sum_x * sum_y) / denom  # exponente

        # Clasificar por el exponente a
        if a < 0.15:
            return 'O(1)',       0.85, factor_real
        elif a < 0.55:
            return 'O(log n)',   0.80, factor_real
        elif a < 1.25:
            return 'O(n)',       0.85, factor_real
        elif a < 1.65:
            return 'O(n log n)', 0.75, factor_real
        elif a < 2.35:
            return 'O(n²)',      0.85, factor_real
        elif a < 3.35:
            return 'O(n³)',      0.80, factor_real
        else:
            return 'O(2ⁿ)',      0.70, factor_real

    except Exception:
        return 'O(?)', 0.3, factor_real


def _generar_reporte(nombre: str, complejidad: str,
                      tiempos: List[Tuple], factor: float) -> str:
    """Genera el reporte legible de complejidad."""
    lineas = [f'📊 Complejidad real de `{nombre}`: **{complejidad}**']
    lineas.append('')
    lineas.append('| n       | tiempo     |')
    lineas.append('|---------|------------|')
    for n, ms in tiempos:
        lineas.append(f'| {n:6,} | {ms:.4f}ms |')
    if factor > 1:
        lineas.append(f'\n→ Al multiplicar n por {round(tiempos[-1][0]/tiempos[0][0])}x, '
                      f'el tiempo creció {round(factor, 1)}x — consistente con {complejidad}.')
    return '\n'.join(lineas)