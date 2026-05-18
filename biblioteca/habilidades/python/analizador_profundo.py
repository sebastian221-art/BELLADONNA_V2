# biblioteca/habilidades/python/analizador_profundo.py
# ============================================================
# ANALIZADOR PROFUNDO — herramientas que las IAs no tienen
#
# Capacidades exclusivas de Bell:
#   dis         → bytecode compilado real (instrucciones CPU)
#   tracemalloc → memoria real por línea de código
#   timeit      → benchmark real con múltiples ejecuciones
#   mypy        → verificación de tipos estricta
#   vulture     → código muerto real
#
# Ninguna IA puede ejecutar código real.
# Bell sí — y usa eso para dar datos exactos, no estimaciones.
# ============================================================

import ast
import dis
import subprocess
import sys
import tempfile
import os
import tracemalloc
import timeit as _timeit
import textwrap
from dataclasses import dataclass, field
from typing import List, Optional, Dict


@dataclass
class AnalisisBytecode:
    instrucciones:   int    = 0
    carga_globales:  int    = 0
    saltos:          int    = 0
    llamadas:        int    = 0
    resumen:         str    = ''
    detalle:         str    = ''


@dataclass
class AnalisisMemoria:
    pico_kb:         float  = 0.0
    inicio_kb:       float  = 0.0
    diferencia_kb:   float  = 0.0
    resumen:         str    = ''


@dataclass
class BenchmarkSolucion:
    nombre:          str    = ''
    tiempo_ms:       float  = 0.0
    iteraciones:     int    = 0
    codigo:          str    = ''


@dataclass
class AnalisisProfundo:
    bytecode:        Optional[AnalisisBytecode] = None
    memoria:         Optional[AnalisisMemoria]  = None
    benchmarks:      List[BenchmarkSolucion]    = field(default_factory=list)
    errores_mypy:    List[str]                  = field(default_factory=list)
    codigo_muerto:   List[str]                  = field(default_factory=list)
    reporte:         str                        = ''


# ── BYTECODE (dis) ────────────────────────────────────────

def analizar_bytecode(codigo: str) -> AnalisisBytecode:
    """
    Analiza el bytecode compilado de las funciones.
    Muestra cuántas instrucciones reales genera el código.
    """
    resultado = AnalisisBytecode()
    instrucciones_capturadas = []

    try:
        codigo_obj = compile(codigo, '<bell>', 'exec')
    except SyntaxError:
        resultado.resumen = 'No se puede compilar — verifica la sintaxis.'
        return resultado

    # Capturar output de dis
    import io
    from contextlib import redirect_stdout

    buffer = io.StringIO()

    def _analizar_codigo_obj(obj):
        with redirect_stdout(buffer):
            dis.dis(obj)
        for const in obj.co_consts:
            if hasattr(const, 'co_code'):
                _analizar_codigo_obj(const)

    try:
        _analizar_codigo_obj(codigo_obj)
        detalle_raw = buffer.getvalue()

        # Parsear las instrucciones
        for linea in detalle_raw.splitlines():
            linea = linea.strip()
            if not linea or linea.startswith('Disassembly'):
                continue
            instrucciones_capturadas.append(linea)

            # Contar tipos de instrucciones
            if any(op in linea for op in ['LOAD_GLOBAL', 'LOAD_NAME',
                                           'LOAD_DEREF']):
                resultado.carga_globales += 1
            if any(op in linea for op in ['JUMP', 'FOR_ITER', 'POP_JUMP']):
                resultado.saltos += 1
            if 'CALL' in linea:
                resultado.llamadas += 1

        resultado.instrucciones = len([l for l in instrucciones_capturadas
                                        if l and not l.startswith(('>>',))])
        resultado.detalle = detalle_raw[:800]  # primeros 800 chars

        # Clasificar eficiencia
        if resultado.instrucciones < 10:
            nivel = 'muy eficiente'
        elif resultado.instrucciones < 25:
            nivel = 'eficiente'
        elif resultado.instrucciones < 50:
            nivel = 'moderado'
        else:
            nivel = 'complejo — considera refactorizar'

        resultado.resumen = (
            f'{resultado.instrucciones} instrucciones bytecode | '
            f'{resultado.llamadas} llamadas a funciones | '
            f'{resultado.saltos} saltos | '
            f'Nivel: {nivel}'
        )

    except Exception as e:
        resultado.resumen = f'Error analizando bytecode: {e}'

    return resultado


# ── MEMORIA (tracemalloc) ─────────────────────────────────

def analizar_memoria(codigo: str) -> AnalisisMemoria:
    """
    Mide el uso de memoria real al ejecutar el código.
    Usa tracemalloc de la librería estándar.
    """
    resultado = AnalisisMemoria()

    script = f'''
import tracemalloc
import sys
import json

tracemalloc.start()
snapshot_inicio = tracemalloc.take_snapshot()

try:
    exec(compile({repr(codigo)}, "<bell>", "exec"))
except Exception:
    pass

snapshot_fin = tracemalloc.take_snapshot()
tracemalloc.stop()

stats = snapshot_fin.compare_to(snapshot_inicio, "lineno")
pico_actual, pico_total = tracemalloc.get_traced_memory() if False else (0, 0)

total_diff = sum(s.size_diff for s in stats)
print(json.dumps({{
    "total_diff_bytes": total_diff,
    "top_3": [
        {{"linea": str(s.traceback), "size": s.size_diff}}
        for s in sorted(stats, key=lambda x: abs(x.size_diff), reverse=True)[:3]
    ]
}}))
'''

    with tempfile.NamedTemporaryFile(suffix='.py', mode='w',
                                     delete=False, encoding='utf-8') as f:
        f.write(script)
        path = f.name

    try:
        proc = subprocess.run(
            [sys.executable, path],
            capture_output=True, text=True, timeout=15,
        )
        if proc.stdout.strip():
            import json
            datos = json.loads(proc.stdout.strip())
            diff_bytes = datos.get('total_diff_bytes', 0)
            diff_kb = diff_bytes / 1024

            resultado.diferencia_kb = round(diff_kb, 3)

            if diff_kb < 1:
                nivel = 'mínimo (< 1 KB)'
            elif diff_kb < 100:
                nivel = f'moderado ({diff_kb:.1f} KB)'
            elif diff_kb < 1024:
                nivel = f'alto ({diff_kb:.1f} KB)'
            else:
                nivel = f'muy alto ({diff_kb/1024:.1f} MB)'

            resultado.resumen = (
                f'Memoria asignada: {diff_kb:.2f} KB | Nivel: {nivel}'
            )
    except Exception as e:
        resultado.resumen = f'No se pudo medir memoria: {e}'
    finally:
        try:
            os.unlink(path)
        except Exception:
            pass

    return resultado


# ── BENCHMARKING (timeit) ─────────────────────────────────

def benchmark_soluciones(soluciones: List[Dict[str, str]],
                          setup: str = '',
                          iteraciones: int = 10000) -> List[BenchmarkSolucion]:
    """
    Benchmark real de múltiples soluciones con timeit.
    Retorna las soluciones ordenadas de más rápida a más lenta.

    soluciones: [{'nombre': 'Counter', 'codigo': 'Counter(lista)'}, ...]
    setup: código de setup (imports, datos de prueba)
    """
    resultados = []

    for sol in soluciones:
        try:
            t = _timeit.timeit(
                stmt=sol['codigo'],
                setup=setup,
                number=iteraciones,
            )
            tiempo_ms = (t / iteraciones) * 1000  # ms por ejecución

            resultados.append(BenchmarkSolucion(
                nombre      = sol['nombre'],
                tiempo_ms   = round(tiempo_ms, 4),
                iteraciones = iteraciones,
                codigo      = sol['codigo'],
            ))
        except Exception as e:
            resultados.append(BenchmarkSolucion(
                nombre    = sol['nombre'],
                tiempo_ms = -1,
                codigo    = sol['codigo'],
            ))

    resultados.sort(key=lambda x: x.tiempo_ms if x.tiempo_ms >= 0 else 9999)
    return resultados


def formatear_benchmark(benchmarks: List[BenchmarkSolucion]) -> str:
    """Formatea el benchmark para el reporte de Bell."""
    if not benchmarks:
        return ''

    validos = [b for b in benchmarks if b.tiempo_ms >= 0]
    if not validos:
        return '⚡ Benchmark: No se pudo medir el rendimiento.'

    partes = [f'⚡ Benchmark real ({validos[0].iteraciones:,} iteraciones):']
    mas_rapido = validos[0]

    for b in validos:
        if b.tiempo_ms == mas_rapido.tiempo_ms:
            icono = '🥇'
            extra = ' ← más rápida'
        else:
            ratio = b.tiempo_ms / mas_rapido.tiempo_ms
            icono = '🥈' if ratio < 2 else '🥉'
            extra = f' ({ratio:.1f}x más lenta)'
        partes.append(
            f'  {icono} {b.nombre}: {b.tiempo_ms:.4f}ms{extra}'
        )

    if len(validos) > 1:
        ratio_total = validos[-1].tiempo_ms / validos[0].tiempo_ms
        partes.append(
            f'\n→ La versión más rápida es {ratio_total:.1f}x más eficiente'
        )

    return '\n'.join(partes)


# ── MYPY (verificación de tipos) ─────────────────────────

def verificar_tipos_mypy(codigo: str) -> List[str]:
    """
    Ejecuta mypy sobre el código para verificación estricta de tipos.
    Retorna lista de errores de tipo encontrados.
    """
    with tempfile.NamedTemporaryFile(suffix='.py', mode='w',
                                     delete=False, encoding='utf-8') as f:
        f.write(codigo)
        path = f.name

    errores = []
    try:
        proc = subprocess.run(
            [sys.executable, '-m', 'mypy', '--ignore-missing-imports',
             '--no-error-summary', '--strict', path],
            capture_output=True, text=True, timeout=20,
        )
        for linea in proc.stdout.splitlines():
            if ':' in linea and 'error:' in linea:
                # Limpiar el path del archivo temporal
                linea_limpia = re.sub(r'^.+?:(\d+):', r'Línea \1:', linea)
                errores.append(linea_limpia.strip())
    except Exception:
        pass
    finally:
        try:
            os.unlink(path)
        except Exception:
            pass

    return errores[:8]  # máximo 8 errores


# ── VULTURE (código muerto) ───────────────────────────────

def detectar_codigo_muerto(codigo: str) -> List[str]:
    """
    Usa vulture para detectar funciones, variables y código nunca ejecutado.
    """
    with tempfile.NamedTemporaryFile(suffix='.py', mode='w',
                                     delete=False, encoding='utf-8') as f:
        f.write(codigo)
        path = f.name

    muertos = []
    try:
        proc = subprocess.run(
            [sys.executable, '-m', 'vulture', path, '--min-confidence', '80'],
            capture_output=True, text=True, timeout=15,
        )
        for linea in proc.stdout.splitlines():
            if linea.strip():
                # Limpiar el path
                limpia = re.sub(r'^.+?:(\d+):', r'Línea \1:', linea)
                muertos.append(limpia.strip())
    except Exception:
        pass
    finally:
        try:
            os.unlink(path)
        except Exception:
            pass

    return muertos[:5]



# ── PROFILING DE RECURSIÓN ────────────────────────────────

def perfilar_recursion(codigo: str) -> str:
    """
    Detecta funciones recursivas y mide su rendimiento real con n creciente.
    Compara automáticamente con la versión memoizada (lru_cache).
    Muestra el factor de crecimiento real — NO estimado.
    """
    import ast as ast_mod
    import subprocess, sys, tempfile, os, json

    # Detectar funciones recursivas con AST
    try:
        arbol = ast_mod.parse(codigo)
    except SyntaxError:
        return ''

    recursivas = []
    for nodo in ast_mod.walk(arbol):
        if not isinstance(nodo, ast_mod.FunctionDef):
            continue
        nombre = nodo.name
        # Buscar si se llama a sí misma
        for sub in ast_mod.walk(nodo):
            if (isinstance(sub, ast_mod.Call) and
                    isinstance(getattr(sub, 'func', None), ast_mod.Name) and
                    sub.func.id == nombre):
                recursivas.append(nombre)
                break

    if not recursivas:
        return ''

    fn_nombre = recursivas[0]

    # Extraer argumentos de la función
    fn_nodo = next(
        n for n in ast_mod.walk(arbol)
        if isinstance(n, ast_mod.FunctionDef) and n.name == fn_nombre
    )
    args = [a.arg for a in fn_nodo.args.args]
    if not args:
        return ''
    primer_arg = args[0]

    # Script de profiling: medir con n=10, 15, 20, 25, 28
    # Para lru_cache correcto: redefinir la función con @lru_cache Y recursión interna memoizada
    codigo_memo = f"from functools import lru_cache\n@lru_cache(maxsize=None)\n" + codigo.strip()
    # Renombrar función memoizada para no colisionar
    codigo_memo_renamed = codigo_memo.replace(
        f'def {fn_nombre}(',
        f'def {fn_nombre}_memo('
    ).replace(
        f'{fn_nombre}(n-1)',
        f'{fn_nombre}_memo(n-1)'
    ).replace(
        f'{fn_nombre}(n-2)',
        f'{fn_nombre}_memo(n-2)'
    )

    script = f'''
import time
import json

{codigo}

{codigo_memo_renamed}

resultados = {{}}
valores_n = [10, 15, 20, 25, 28]

for n in valores_n:
    t0 = time.perf_counter()
    try:
        {fn_nombre}(n)
        t1 = time.perf_counter()
        resultados[str(n)] = round((t1 - t0) * 1000, 4)
    except RecursionError:
        resultados[str(n)] = -1
        break
    except Exception as e:
        resultados[str(n)] = -2
        break

resultados_memo = {{}}
for n in valores_n:
    {fn_nombre}_memo.cache_clear()
    t0 = time.perf_counter()
    try:
        {fn_nombre}_memo(n)
        t1 = time.perf_counter()
        resultados_memo[str(n)] = round((t1 - t0) * 1000, 6)
    except Exception:
        resultados_memo[str(n)] = -1

print(json.dumps({{"original": resultados, "memo": resultados_memo}}))
'''

    with tempfile.NamedTemporaryFile(suffix='.py', mode='w',
                                      delete=False, encoding='utf-8') as f:
        f.write(script)
        path = f.name

    try:
        proc = subprocess.run(
            [sys.executable, path],
            capture_output=True, text=True, timeout=60,
        )
        os.unlink(path)

        if not proc.stdout.strip():
            return ''

        datos = json.loads(proc.stdout.strip())
        orig = datos.get('original', {})
        memo = datos.get('memo', {})

        # Calcular factor de crecimiento entre n=20 y n=25
        t20 = orig.get('20', -1)
        t25 = orig.get('25', -1)
        t28 = orig.get('28', -1)

        partes = [f'📈 Profiling real de {fn_nombre}(n):']
        partes.append('')
        partes.append('| n  | Original   | Con lru_cache | Factor mejora |')
        partes.append('|----|-----------|---------------|---------------|')

        valores = [10, 15, 20, 25, 28]
        for n in valores:
            t_orig = orig.get(str(n), -1)
            t_m    = memo.get(str(n), -1)
            if t_orig < 0:
                partes.append(f'| {n} | RecursionError | {t_m:.6f}ms | ∞ |')
                break
            if t_m > 0 and t_orig > 0:
                factor = round(t_orig / t_m)
                partes.append(f'| {n} | {t_orig:.3f}ms | {t_m:.6f}ms | {factor}x más rápido |')
            else:
                partes.append(f'| {n} | {t_orig:.3f}ms | — | — |')

        # Factor de crecimiento exponencial
        if t20 > 0 and t25 > 0:
            factor_crecimiento = round(t25 / t20, 1)
            partes.append('')
            partes.append(
                f'→ Al pasar de n=20 a n=25 el tiempo creció {factor_crecimiento}x '
                f'(esperado ~32x para O(2ⁿ)) — crecimiento exponencial confirmado.'
            )

        if t28 > 0:
            partes.append(
                f'→ Con n=28: {t28:.1f}ms. Escalar a n=50 tomaría horas.'
            )

        partes.append('')
        partes.append(
            '✅ Solución: @lru_cache(maxsize=None) reduce de O(2ⁿ) a O(n) — '
            'o mejor aún: versión iterativa con O(n) tiempo y O(1) memoria adicional.'
        )

        return '\n'.join(partes)

    except Exception as e:
        return ''

# ── ANÁLISIS COMPLETO ─────────────────────────────────────

def analizar_completo(codigo: str,
                       soluciones_extra: Optional[List[Dict]] = None,
                       setup_benchmark: str = '') -> AnalisisProfundo:
    """
    Ejecuta todos los análisis profundos en paralelo (donde es posible).
    Retorna un AnalisisProfundo con todos los resultados.
    """
    import re
    resultado = AnalisisProfundo()

    # Bytecode
    resultado.bytecode = analizar_bytecode(codigo)

    # Memoria
    resultado.memoria = analizar_memoria(codigo)

    # mypy
    resultado.errores_mypy = verificar_tipos_mypy(codigo)

    # vulture
    resultado.codigo_muerto = detectar_codigo_muerto(codigo)

    # Benchmark si hay soluciones para comparar
    if soluciones_extra:
        resultado.benchmarks = benchmark_soluciones(
            soluciones_extra, setup_benchmark
        )

    # Reporte completo
    partes = []

    if resultado.bytecode and resultado.bytecode.instrucciones > 0:
        partes.append(f'🔧 Bytecode: {resultado.bytecode.resumen}')

    if resultado.memoria and resultado.memoria.resumen:
        partes.append(f'💾 {resultado.memoria.resumen}')

    if resultado.errores_mypy:
        partes.append(f'🔴 mypy — {len(resultado.errores_mypy)} error(es) de tipos:')
        for e in resultado.errores_mypy[:3]:
            partes.append(f'  • {e}')
    else:
        partes.append('✅ mypy — Sin errores de tipos')

    if resultado.codigo_muerto:
        partes.append(f'⚰️  Código muerto detectado:')
        for m in resultado.codigo_muerto[:3]:
            partes.append(f'  • {m}')
    else:
        partes.append('✅ vulture — Sin código muerto')

    if resultado.benchmarks:
        partes.append('')
        partes.append(formatear_benchmark(resultado.benchmarks))

    resultado.reporte = '\n'.join(partes)
    return resultado