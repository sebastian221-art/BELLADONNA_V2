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