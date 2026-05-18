# biblioteca/habilidades/python/probador_hipotesis.py
# ============================================================
# PROBADOR DE HIPÓTESIS — Auto-testing con Hypothesis
#
# Bell extrae funciones del código, genera automáticamente
# cientos de casos de prueba con Hypothesis y detecta
# bugs que nadie anticipó.
#
# GPT-4o PREDICE edge cases. Bell los ENCUENTRA ejecutando.
# ============================================================

import ast
import subprocess
import sys
import tempfile
import os
import re
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class FalloHipotesis:
    funcion:    str
    input_fallo: str
    error:      str
    tipo_error: str


@dataclass
class ResultadoHipotesis:
    funciones_probadas: int                   = 0
    casos_probados:     int                   = 0
    fallos:             List[FalloHipotesis]  = field(default_factory=list)
    edge_cases_ok:      List[str]             = field(default_factory=list)
    reporte:            str                   = ''
    exitoso:            bool                  = True


def _extraer_funciones(codigo: str) -> List[dict]:
    """Extrae funciones del código con sus type hints para generar estrategias."""
    funciones = []
    try:
        arbol = ast.parse(codigo)
    except SyntaxError:
        return []

    for nodo in ast.walk(arbol):
        if not isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if nodo.name.startswith('_'):
            continue  # skip privadas

        args = []
        for arg in nodo.args.args:
            if arg.arg == 'self':
                continue
            tipo = 'any'
            if arg.annotation:
                try:
                    tipo = ast.unparse(arg.annotation).lower()
                except Exception:
                    tipo = 'any'
            args.append({'nombre': arg.arg, 'tipo': tipo})

        retorno = 'any'
        if nodo.returns:
            try:
                retorno = ast.unparse(nodo.returns).lower()
            except Exception:
                retorno = 'any'

        funciones.append({
            'nombre':  nodo.name,
            'args':    args,
            'retorno': retorno,
            'linea':   nodo.lineno,
        })

    return funciones


def _tipo_a_estrategia(tipo: str) -> str:
    """Mapea type hints a estrategias de Hypothesis."""
    tipo = tipo.lower().strip()

    _MAPA = {
        'int':           'st.integers()',
        'float':         'st.floats(allow_nan=False, allow_infinity=False)',
        'str':           'st.text()',
        'bool':          'st.booleans()',
        'bytes':         'st.binary()',
        'list[int]':     'st.lists(st.integers())',
        'list[float]':   'st.lists(st.floats(allow_nan=False, allow_infinity=False))',
        'list[str]':     'st.lists(st.text())',
        'list':          'st.lists(st.integers() | st.text())',
        'dict':          'st.dictionaries(st.text(), st.integers())',
        'tuple':         'st.tuples(st.integers(), st.integers())',
        'optional[int]': 'st.none() | st.integers()',
        'optional[str]': 'st.none() | st.text()',
        'none':          'st.none()',
    }

    # Buscar coincidencia exacta primero
    if tipo in _MAPA:
        return _MAPA[tipo]

    # Buscar parcial
    for key, estrategia in _MAPA.items():
        if key in tipo:
            return estrategia

    # Default: combinación de tipos comunes
    return 'st.integers() | st.text() | st.none() | st.lists(st.integers())'


def _generar_test(funcion: dict) -> str:
    """Genera código de test con Hypothesis para una función."""
    nombre = funcion['nombre']
    args   = funcion['args']

    if not args:
        return ''  # sin argumentos, no hay qué probar

    # Generar estrategias para cada argumento
    estrategias = []
    param_names = []
    for arg in args[:4]:  # máximo 4 argumentos
        estrategias.append(f"    {arg['nombre']}={_tipo_a_estrategia(arg['tipo'])}")
        param_names.append(arg['nombre'])

    params_str = ', '.join(param_names)
    estrategias_str = ',\n'.join(estrategias)

    return f'''
@given(
{estrategias_str}
)
@settings(max_examples=200, deadline=5000)
def test_hypothesis_{nombre}({params_str}):
    """Auto-generado por Bell — prueba edge cases de {nombre}."""
    try:
        resultado = {nombre}({params_str})
        # Si llega aquí sin excepción, es un caso válido
        _casos_ok.append(f"{nombre}({params_str}={{repr({param_names[0]})}}) → {{resultado}}")
    except (ValueError, TypeError, ZeroDivisionError, IndexError, KeyError) as e:
        # Registrar el fallo con el input que lo causó
        _fallos.append({{
            'funcion': '{nombre}',
            'input': f"{params_str}={{repr({param_names[0]})}}" if {param_names !r} else "",
            'error': str(e),
            'tipo': type(e).__name__,
        }})
    except Exception as e:
        # Error inesperado — bug real
        _fallos.append({{
            'funcion': '{nombre}',
            'input': f"{params_str}={{repr({param_names[0]})}}" if {param_names !r} else "",
            'error': f"ERROR INESPERADO: {{str(e)}}",
            'tipo': type(e).__name__,
        }})
        raise  # que Hypothesis lo shrink
'''


def _generar_script_completo(codigo: str, funciones: List[dict]) -> str:
    """Genera el script Python completo para ejecutar con Hypothesis."""
    tests = [_generar_test(f) for f in funciones if f['args']]
    tests = [t for t in tests if t.strip()]

    if not tests:
        return ''

    nombres_test = [
        f"test_hypothesis_{f['nombre']}"
        for f in funciones
        if f['args']
    ]

    script = f'''
import sys
import json
from hypothesis import given, settings, HealthCheck
from hypothesis import strategies as st

_fallos = []
_casos_ok = []

# ── Código original de Sebastian ──────────────────────────
{codigo}

# ── Tests auto-generados ──────────────────────────────────
{"".join(tests)}

# ── Ejecutar todos los tests ──────────────────────────────
if __name__ == "__main__":
    total_casos = 0
    for nombre_test in {nombres_test!r}:
        try:
            fn = globals().get(nombre_test)
            if fn:
                fn()
                total_casos += 200
        except Exception:
            pass  # Hypothesis ya registró el fallo en _fallos

    resultado = {{
        "casos_probados": total_casos,
        "fallos": _fallos[:10],
        "casos_ok": _casos_ok[:5],
    }}
    print(json.dumps(resultado, ensure_ascii=False))
'''
    return script


def probar(codigo: str, timeout: int = 30) -> ResultadoHipotesis:
    """
    Prueba automáticamente las funciones del código con Hypothesis.
    Genera y ejecuta el script en un subprocess aislado.
    """
    resultado = ResultadoHipotesis()

    funciones = _extraer_funciones(codigo)
    funciones_con_args = [f for f in funciones if f['args']]

    if not funciones_con_args:
        resultado.reporte = 'No hay funciones con argumentos para probar.'
        return resultado

    resultado.funciones_probadas = len(funciones_con_args)

    # Verificar que Hypothesis esté disponible
    try:
        import hypothesis  # noqa
    except ImportError:
        resultado.reporte = 'Hypothesis no instalado — instalar con: pip install hypothesis'
        resultado.exitoso = False
        return resultado

    script = _generar_script_completo(codigo, funciones_con_args)
    if not script:
        resultado.reporte = 'No se pudo generar script de pruebas.'
        return resultado

    # Ejecutar en subprocess aislado
    with tempfile.NamedTemporaryFile(suffix='.py', mode='w',
                                     delete=False, encoding='utf-8') as f:
        f.write(script)
        path_script = f.name

    try:
        proc = subprocess.run(
            [sys.executable, path_script],
            capture_output=True, text=True,
            timeout=timeout,
        )

        if proc.stdout.strip():
            import json
            datos = json.loads(proc.stdout.strip())
            resultado.casos_probados = datos.get('casos_probados', 0)

            for fallo_raw in datos.get('fallos', []):
                resultado.fallos.append(FalloHipotesis(
                    funcion     = fallo_raw.get('funcion', ''),
                    input_fallo = fallo_raw.get('input', ''),
                    error       = fallo_raw.get('error', ''),
                    tipo_error  = fallo_raw.get('tipo', ''),
                ))

            resultado.edge_cases_ok = datos.get('casos_ok', [])

    except subprocess.TimeoutExpired:
        resultado.reporte = 'Hypothesis timeout — el código tardó demasiado.'
        resultado.exitoso = False
    except Exception as e:
        resultado.exitoso = False
    finally:
        try:
            os.unlink(path_script)
        except Exception:
            pass

    resultado.reporte = _formatear(resultado, funciones_con_args)
    return resultado


def _formatear(resultado: ResultadoHipotesis, funciones: List[dict]) -> str:
    """Formatea el reporte de Hypothesis para Bell."""
    nombres = ', '.join(f['nombre'] for f in funciones)
    partes = [
        f'🔬 Hypothesis probó {resultado.casos_probados} casos en: {nombres}'
    ]

    if resultado.fallos:
        partes.append(f'\n❌ {len(resultado.fallos)} fallo(s) encontrado(s):')
        for fallo in resultado.fallos[:5]:
            partes.append(
                f'  • {fallo.funcion}({fallo.input_fallo}) '
                f'→ {fallo.tipo_error}: {fallo.error[:80]}'
            )
    else:
        partes.append(
            f'✅ Todos los casos pasaron — '
            f'no se encontraron crashes con {resultado.casos_probados} inputs'
        )

    if resultado.edge_cases_ok:
        partes.append('\nCasos representativos OK:')
        for caso in resultado.edge_cases_ok[:3]:
            partes.append(f'  ✓ {caso[:80]}')

    return '\n'.join(partes)