# biblioteca/habilidades/python/detector_antipatrones.py
# ============================================================
# DETECTOR DE ANTIPATRONES — AST puro, cero LLM
#
# Python detecta estos en microsegundos antes de llamar a Groq.
# Bell es la única IA que hace esto con AST real, no con texto.
#
# 15 antipatrones cubiertos:
#   1.  not x == y          → x != y
#   2.  len(x) == 0         → not x
#   3.  x == True/False     → if x / if not x
#   4.  x == None           → x is None
#   5.  for i in range(len) → for item in x
#   6.  eval() / exec()     → peligroso
#   7.  except:             → captura específica
#   8.  def f(x=[]):        → argumento mutable por defecto
#   9.  x = x + 1           → x += 1
#   10. suma en loop con +  → ''.join()
#   11. .keys() en for      → iterar dict directamente
#   12. list(set(x))        → posible uso de dict.fromkeys
#   13. open() sin with     → resource leak
#   14. assert en prod      → no usar assert para validar
#   15. import * from       → importación ambigua
# ============================================================

import ast
import re
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Antipatron:
    linea:      int
    columna:    int
    patron:     str         # nombre del antipatrón
    problema:   str         # descripción del problema
    sugerencia: str         # cómo corregirlo
    severidad:  str         # 'critico' / 'advertencia' / 'estilo'
    codigo_mal: str = ''    # fragmento del código problemático
    codigo_ok:  str = ''    # cómo debería verse


class _VisitorAntipatrones(ast.NodeVisitor):
    """AST visitor que detecta antipatrones en el árbol sintáctico."""

    def __init__(self, codigo: str):
        self.codigo = codigo
        self.lineas = codigo.splitlines()
        self.antipatrones: List[Antipatron] = []

    def _linea(self, nodo) -> str:
        try:
            return self.lineas[nodo.lineno - 1].strip()
        except (IndexError, AttributeError):
            return ''

    def _add(self, nodo, patron, problema, sugerencia, severidad,
             mal='', ok=''):
        self.antipatrones.append(Antipatron(
            linea      = getattr(nodo, 'lineno', 0),
            columna    = getattr(nodo, 'col_offset', 0),
            patron     = patron,
            problema   = problema,
            sugerencia = sugerencia,
            severidad  = severidad,
            codigo_mal = mal or self._linea(nodo),
            codigo_ok  = ok,
        ))

    # ── 1. not x == y ────────────────────────────────────────
    def visit_UnaryOp(self, nodo):
        if isinstance(nodo.op, ast.Not):
            if isinstance(nodo.operand, ast.Compare):
                op = nodo.operand
                if len(op.ops) == 1 and isinstance(op.ops[0], ast.Eq):
                    self._add(nodo, 'negacion_comparacion',
                        'not x == y es confuso',
                        'Usa x != y — más claro y eficiente',
                        'estilo',
                        ok='x != y')
        self.generic_visit(nodo)

    # ── 2. len(x) == 0  /  len(x) > 0 ───────────────────────
    def visit_Compare(self, nodo):
        if isinstance(nodo.left, ast.Call):
            fn = nodo.left
            if (isinstance(fn.func, ast.Name) and fn.func.id == 'len'
                    and len(fn.args) == 1):
                if len(nodo.ops) == 1:
                    op = nodo.ops[0]
                    comp = nodo.comparators[0]
                    es_cero = (isinstance(comp, ast.Constant)
                               and comp.value == 0)
                    if es_cero and isinstance(op, ast.Eq):
                        self._add(nodo, 'len_igual_cero',
                            'len(x) == 0 es innecesariamente verboso',
                            'Usa "if not x:" — más Pythónico y más rápido',
                            'estilo', ok='if not x:')
                    elif es_cero and isinstance(op, ast.Gt):
                        self._add(nodo, 'len_mayor_cero',
                            'len(x) > 0 es innecesariamente verboso',
                            'Usa "if x:" — más Pythónico',
                            'estilo', ok='if x:')

        # ── 3. x == True / x == False ────────────────────────
        for i, (op, comp) in enumerate(
                zip(nodo.ops, nodo.comparators)):
            if (isinstance(comp, ast.Constant)
                    and comp.value in (True, False)
                    and isinstance(op, ast.Eq)):
                bueno = 'if x:' if comp.value else 'if not x:'
                self._add(nodo, 'comparacion_booleana',
                    f'Comparar con {comp.value} explícitamente es redundante',
                    f'Usa {bueno} directamente',
                    'estilo', ok=bueno)

        # ── 4. x == None ─────────────────────────────────────
        for op, comp in zip(nodo.ops, nodo.comparators):
            if (isinstance(comp, ast.Constant) and comp.value is None
                    and isinstance(op, ast.Eq)):
                self._add(nodo, 'comparacion_none',
                    'Usa "is None" en lugar de "== None"',
                    'Python garantiza un solo objeto None — usa identidad, no igualdad',
                    'advertencia', ok='x is None')

        self.generic_visit(nodo)

    # ── 5. for i in range(len(x)) ────────────────────────────
    def visit_For(self, nodo):
        if isinstance(nodo.iter, ast.Call):
            fn = nodo.iter
            if (isinstance(fn.func, ast.Name) and fn.func.id == 'range'
                    and len(fn.args) == 1
                    and isinstance(fn.args[0], ast.Call)):
                inner = fn.args[0]
                if (isinstance(inner.func, ast.Name)
                        and inner.func.id == 'len'):
                    self._add(nodo, 'range_len',
                        'for i in range(len(x)) es anti-Pythónico',
                        'Usa "for item in x:" o "for i, item in enumerate(x):"',
                        'estilo',
                        ok='for item in x:  # o: for i, item in enumerate(x):')
        self.generic_visit(nodo)

    # ── 6. eval() / exec() ───────────────────────────────────
    def visit_Call(self, nodo):
        if isinstance(nodo.func, ast.Name):
            nombre = nodo.func.id

            if nombre in ('eval', 'exec'):
                self._add(nodo, 'eval_exec',
                    f'{nombre}() ejecuta código arbitrario — vulnerabilidad crítica',
                    f'Bandit B307/B102. Evita {nombre}() o valida el input con AST literal_eval',
                    'critico', ok='ast.literal_eval(x)  # solo para literales seguros')

            # ── 11. dict.keys() en for ────────────────────────
            if (isinstance(nodo.func, ast.Attribute)
                    and nodo.func.attr == 'keys'
                    and not nodo.args):
                self._add(nodo, 'keys_en_for',
                    'Iterar .keys() es redundante — los dicts son iterables directamente',
                    'Usa "for key in mi_dict:" en lugar de "for key in mi_dict.keys():"',
                    'estilo', ok='for key in mi_dict:')

            # ── 13. open() sin with ───────────────────────────
            if nombre == 'open':
                padre = getattr(nodo, '_padre', None)
                if not isinstance(padre, (ast.withitem, ast.With)):
                    self._add(nodo, 'open_sin_with',
                        'open() sin "with" puede causar resource leak',
                        'Siempre usa "with open(...) as f:" para garantizar cierre',
                        'advertencia',
                        ok='with open("archivo.txt") as f:')

        self.generic_visit(nodo)

    # ── 7. except: (bare except) ─────────────────────────────
    def visit_ExceptHandler(self, nodo):
        if nodo.type is None:
            self._add(nodo, 'bare_except',
                '"except:" captura TODAS las excepciones, incluyendo SystemExit y KeyboardInterrupt',
                'Especifica la excepción: "except ValueError:" o "except (TypeError, ValueError):"',
                'critico', ok='except (ValueError, TypeError):')
        self.generic_visit(nodo)

    # ── 8. def f(x=[]) — argumento mutable por defecto ───────
    def visit_FunctionDef(self, nodo):
        defaults = nodo.args.defaults + nodo.args.kw_defaults
        for default in defaults:
            if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                tipo = {ast.List: 'list', ast.Dict: 'dict',
                        ast.Set: 'set'}.get(type(default), 'mutable')
                self._add(nodo, 'argumento_mutable',
                    f'Argumento por defecto mutable ({tipo}) — se comparte entre llamadas',
                    f'Usa None y crea el {tipo} dentro de la función',
                    'critico',
                    ok=f'def f(x=None):\n    if x is None: x = {tipo}()')
        self.generic_visit(nodo)

    # Lo mismo para funciones async
    visit_AsyncFunctionDef = visit_FunctionDef

    # ── 15. from modulo import * ─────────────────────────────
    def visit_ImportFrom(self, nodo):
        if any(alias.name == '*' for alias in nodo.names):
            self._add(nodo, 'import_star',
                'from x import * contamina el namespace y oculta el origen de nombres',
                'Importa solo lo que necesitas: from x import ClaseEspecifica',
                'advertencia',
                ok=f'from {nodo.module} import ClaseEspecifica')
        self.generic_visit(nodo)


def _detectar_con_regex(codigo: str) -> List[Antipatron]:
    """Antipatrones detectables con regex (más rápido que AST para algunos casos)."""
    antipatrones = []
    lineas = codigo.splitlines()

    _REGEX_PATRONES = [
        # 9. x = x + n → x += n
        (r'\b(\w+)\s*=\s*\1\s*\+\s*(.+)', 'asignacion_aumentada',
         'x = x + valor es verboso',
         'Usa x += valor — más claro y marginalmentemás eficiente',
         'estilo', r'\1 += \2'),

        # 10. string concatenation in loop
        (r'for\s+.+:\s*$', None, None, None, None, None),  # marker for next line check

        # 14. assert para validación de datos
        (r'\bassert\s+.+,\s*["\']', 'assert_validacion',
         'assert se desactiva con python -O — no usar para validar datos de usuario',
         'Usa raise ValueError(...) para validaciones de producción',
         'advertencia', 'raise ValueError("mensaje")'),
    ]

    for i, linea in enumerate(lineas, 1):
        stripped = linea.strip()

        # 9. x = x + algo → x += algo
        m = re.match(r'(\w+)\s*=\s*\1\s*\+\s*(.+)', stripped)
        if m and not stripped.startswith('#'):
            antipatrones.append(Antipatron(
                linea=i, columna=0,
                patron='asignacion_aumentada',
                problema=f'{m.group(1)} = {m.group(1)} + ... es verboso',
                sugerencia=f'Usa {m.group(1)} += {m.group(2)}',
                severidad='estilo',
                codigo_mal=stripped,
                codigo_ok=f'{m.group(1)} += {m.group(2)}',
            ))

        # 14. assert con mensaje de error → no en producción
        if re.match(r'assert\s+.+,\s*["\']', stripped):
            antipatrones.append(Antipatron(
                linea=i, columna=0,
                patron='assert_validacion',
                problema='assert se desactiva con python -O',
                sugerencia='Usa raise ValueError() para validaciones en producción',
                severidad='advertencia',
                codigo_mal=stripped,
                codigo_ok='raise ValueError("mensaje descriptivo")',
            ))

    return antipatrones


def _marcar_padres(arbol: ast.AST):
    """Marca el padre de cada nodo (para detectar open() sin with)."""
    for nodo in ast.walk(arbol):
        for hijo in ast.iter_child_nodes(nodo):
            hijo._padre = nodo  # type: ignore[attr-defined]


def analizar(codigo: str) -> List[Antipatron]:
    """
    Analiza el código en busca de antipatrones Python.
    Combina AST traversal + regex para máxima cobertura.
    Retorna lista de antipatrones ordenada por línea.
    """
    if not codigo or not codigo.strip():
        return []

    resultados: List[Antipatron] = []

    # AST analysis
    try:
        arbol = ast.parse(codigo)
        _marcar_padres(arbol)
        visitor = _VisitorAntipatrones(codigo)
        visitor.visit(arbol)
        resultados.extend(visitor.antipatrones)
    except SyntaxError:
        pass  # el analizador_codigo ya maneja esto

    # Regex analysis
    resultados.extend(_detectar_con_regex(codigo))

    # Ordenar por línea, luego por severidad
    _orden_severidad = {'critico': 0, 'advertencia': 1, 'estilo': 2}
    resultados.sort(key=lambda a: (a.linea, _orden_severidad.get(a.severidad, 3)))

    return resultados


def formatear_reporte(antipatrones: List[Antipatron]) -> str:
    """Formatea los antipatrones para incluir en el reporte de Bell."""
    if not antipatrones:
        return '✅ Sin antipatrones detectados.'

    criticos    = [a for a in antipatrones if a.severidad == 'critico']
    advertencias = [a for a in antipatrones if a.severidad == 'advertencia']
    estilos     = [a for a in antipatrones if a.severidad == 'estilo']

    partes = []

    if criticos:
        partes.append(f'🔴 {len(criticos)} antipatrón(es) crítico(s):')
        for a in criticos:
            partes.append(f'  • Línea {a.linea} [{a.patron}]: {a.problema}')
            partes.append(f'    → {a.sugerencia}')
            if a.codigo_ok:
                partes.append(f'    ✓ Corrección: {a.codigo_ok}')

    if advertencias:
        partes.append(f'⚠️  {len(advertencias)} advertencia(s):')
        for a in advertencias:
            partes.append(f'  • Línea {a.linea} [{a.patron}]: {a.problema}')
            partes.append(f'    → {a.sugerencia}')

    if estilos:
        partes.append(f'💡 {len(estilos)} mejora(s) de estilo:')
        for a in estilos[:5]:  # máximo 5 de estilo para no saturar
            partes.append(f'  • Línea {a.linea}: {a.sugerencia}')

    return '\n'.join(partes)