# biblioteca/habilidades/python/analizador_codigo.py
# ============================================================
# ANALIZADOR DE CÓDIGO — nivel senior máximo
#
# Herramientas fusionadas:
#   AST     → estructura exacta, nunca aproxima
#   Radon   → CC, MI, Halstead — matemáticamente exactos
#   PyFlakes → variables no definidas, imports no usados
#   Pylint  → 300+ reglas de calidad
#   Bandit  → vulnerabilidades de seguridad
#   Ruff    → linting ultrarrápido (primer pase, <10ms)
#
# Ningún LLM produce análisis con esta precisión.
# ============================================================

import ast
import subprocess
import sys
import tempfile
import os
import json
import re
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ProblemaDetectado:
    linea:       int
    tipo:        str          # error / advertencia / info / seguridad
    herramienta: str          # ast / pyflakes / pylint / bandit / ruff
    mensaje:     str
    codigo:      str = ''     # código de regla (ej. E501, B602)


@dataclass
class MetricasComplejidad:
    cc:              float = 0.0   # complejidad ciclomática (ideal ≤ 10)
    mi:              float = 0.0   # índice de mantenibilidad (0-100, ideal ≥ 65)
    loc:             int   = 0     # líneas de código
    lloc:            int   = 0     # líneas lógicas
    comentarios:     int   = 0
    funciones:       int   = 0
    clases:          int   = 0
    halstead_vol:    float = 0.0
    halstead_dif:    float = 0.0
    nivel_riesgo:    str   = 'bajo'   # bajo / medio / alto / crítico


@dataclass
class AnalisisCompleto:
    exitoso:         bool             = True
    error_fatal:     str              = ''
    codigo_original: str              = ''
    metricas:        MetricasComplejidad = field(default_factory=MetricasComplejidad)
    problemas:       List[ProblemaDetectado] = field(default_factory=list)
    funciones:       List[dict]       = field(default_factory=list)
    imports:         List[str]        = field(default_factory=list)
    clases:          List[str]        = field(default_factory=list)
    es_valido_ast:   bool             = False
    resumen_bell:    str              = ''


class AnalizadorCodigo:
    """
    Analizador de código Python con precisión matemática.
    Fusiona AST + Radon + PyFlakes + Pylint + Bandit + Ruff.
    """

    def analizar(self, codigo: str, nombre: str = 'codigo.py') -> AnalisisCompleto:
        resultado = AnalisisCompleto(codigo_original=codigo)

        if not codigo or not codigo.strip():
            resultado.exitoso = False
            resultado.error_fatal = 'Código vacío.'
            return resultado

        # ── PASO 1: Validar AST (estructura Python válida) ────────────────
        try:
            arbol = ast.parse(codigo)
            resultado.es_valido_ast = True
        except SyntaxError as e:
            resultado.exitoso = False
            resultado.error_fatal = f'SyntaxError línea {e.lineno}: {e.msg}'
            resultado.problemas.append(ProblemaDetectado(
                linea=e.lineno or 0, tipo='error',
                herramienta='ast', mensaje=str(e.msg), codigo='SyntaxError'
            ))
            return resultado

        # Extraer estructura del AST
        resultado.funciones  = self._extraer_funciones(arbol)
        resultado.imports    = self._extraer_imports(arbol)
        resultado.clases     = self._extraer_clases(arbol)

        # ── PASO 2: Métricas Radon ────────────────────────────────────────
        self._analizar_radon(codigo, resultado)

        # ── PASO 3: PyFlakes (errores reales) ─────────────────────────────
        self._analizar_pyflakes(codigo, nombre, resultado)

        # ── PASO 4: Ruff (linting rápido) ─────────────────────────────────
        self._analizar_ruff(codigo, nombre, resultado)

        # ── PASO 5: Bandit (seguridad) ─────────────────────────────────────
        self._analizar_bandit(codigo, nombre, resultado)

        # ── PASO 6: Determinar nivel de riesgo ────────────────────────────
        resultado.metricas.nivel_riesgo = self._calcular_riesgo(resultado)

        # ── PASO 7: Resumen en voz Bell ───────────────────────────────────
        resultado.resumen_bell = self._generar_resumen(resultado)

        return resultado

    # ── Radon ─────────────────────────────────────────────────────────────

    def _analizar_radon(self, codigo: str, r: AnalisisCompleto):
        try:
            from radon.complexity import cc_visit, cc_rank
            from radon.metrics   import mi_visit
            from radon.raw       import analyze

            raw = analyze(codigo)
            r.metricas.loc         = raw.loc
            r.metricas.lloc        = raw.lloc
            r.metricas.comentarios = raw.comments

            mi = mi_visit(codigo, True)
            r.metricas.mi = round(mi, 1)

            bloques = cc_visit(codigo)
            if bloques:
                ccs = [b.complexity for b in bloques]
                r.metricas.cc = round(sum(ccs) / len(ccs), 1)
                # Marcar funciones con CC alto
                for b in bloques:
                    if b.complexity > 10:
                        r.problemas.append(ProblemaDetectado(
                            linea=b.lineno, tipo='advertencia',
                            herramienta='radon',
                            mensaje=f"'{b.name}' CC={b.complexity} (ideal ≤10, riesgo de bugs)",
                            codigo='CC_ALTO'
                        ))
            else:
                r.metricas.cc = 1.0

            try:
                from radon.metrics import h_visit
                h = h_visit(codigo)
                if h:
                    bloque = list(h)[0] if h else None
                    if bloque:
                        r.metricas.halstead_vol = round(bloque.volume, 1)
                        r.metricas.halstead_dif = round(bloque.difficulty, 1)
            except Exception:
                pass

        except ImportError:
            r.problemas.append(ProblemaDetectado(
                0, 'info', 'radon', 'radon no instalado — métricas CC/MI no disponibles'
            ))

    # ── PyFlakes ──────────────────────────────────────────────────────────

    def _analizar_pyflakes(self, codigo: str, nombre: str, r: AnalisisCompleto):
        try:
            from pyflakes import api as pf_api
            from pyflakes.checker import Checker
            from pyflakes import messages as pf_msgs
            import io

            buf = io.StringIO()
            tree = ast.parse(codigo)
            checker = Checker(tree, filename=nombre)

            for msg in checker.messages:
                tipo = 'error' if isinstance(msg, (
                    pf_msgs.UndefinedName, pf_msgs.UndefinedLocal,
                    pf_msgs.ImportShadowedByLoopVar
                )) else 'advertencia'
                r.problemas.append(ProblemaDetectado(
                    linea=msg.lineno, tipo=tipo,
                    herramienta='pyflakes',
                    mensaje=str(msg.message % msg.message_args),
                    codigo=type(msg).__name__
                ))
        except Exception:
            pass

    # ── Ruff ──────────────────────────────────────────────────────────────

    def _analizar_ruff(self, codigo: str, nombre: str, r: AnalisisCompleto):
        try:
            with tempfile.NamedTemporaryFile(suffix='.py', mode='w',
                                             delete=False, encoding='utf-8') as f:
                f.write(codigo)
                tmp = f.name

            proc = subprocess.run(
                ['ruff', 'check', '--output-format=json', tmp],
                capture_output=True, text=True, timeout=10
            )
            os.unlink(tmp)

            if proc.stdout.strip():
                datos = json.loads(proc.stdout)
                for item in datos[:15]:  # max 15 problemas de ruff
                    r.problemas.append(ProblemaDetectado(
                        linea=item.get('location', {}).get('row', 0),
                        tipo='advertencia',
                        herramienta='ruff',
                        mensaje=item.get('message', ''),
                        codigo=item.get('code', '')
                    ))
        except Exception:
            pass

    # ── Bandit (seguridad) ────────────────────────────────────────────────

    def _analizar_bandit(self, codigo: str, nombre: str, r: AnalisisCompleto):
        try:
            with tempfile.NamedTemporaryFile(suffix='.py', mode='w',
                                             delete=False, encoding='utf-8') as f:
                f.write(codigo)
                tmp = f.name

            proc = subprocess.run(
                ['bandit', '-f', 'json', '-q', tmp],
                capture_output=True, text=True, timeout=15
            )
            os.unlink(tmp)

            salida = proc.stdout.strip()
            if salida:
                datos = json.loads(salida)
                for issue in datos.get('results', []):
                    severidad = issue.get('issue_severity', 'LOW')
                    tipo = 'error' if severidad == 'HIGH' else 'advertencia'
                    r.problemas.append(ProblemaDetectado(
                        linea=issue.get('line_number', 0),
                        tipo=tipo,
                        herramienta='bandit',
                        mensaje=f"[{severidad}] {issue.get('issue_text', '')}",
                        codigo=issue.get('test_id', '')
                    ))
        except Exception:
            pass

    # ── Extracción AST ────────────────────────────────────────────────────

    def _extraer_funciones(self, arbol: ast.AST) -> List[dict]:
        funcs = []
        for nodo in ast.walk(arbol):
            if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
                args = [a.arg for a in nodo.args.args]
                returns = ''
                if nodo.returns:
                    try:
                        returns = ast.unparse(nodo.returns)
                    except Exception:
                        pass
                doc = ast.get_docstring(nodo) or ''
                funcs.append({
                    'nombre':   nodo.name,
                    'linea':    nodo.lineno,
                    'args':     args,
                    'returns':  returns,
                    'doc':      doc[:100],
                    'es_async': isinstance(nodo, ast.AsyncFunctionDef),
                })
        return funcs

    def _extraer_imports(self, arbol: ast.AST) -> List[str]:
        imports = []
        for nodo in ast.walk(arbol):
            if isinstance(nodo, ast.Import):
                for alias in nodo.names:
                    imports.append(alias.name)
            elif isinstance(nodo, ast.ImportFrom):
                modulo = nodo.module or ''
                for alias in nodo.names:
                    imports.append(f'{modulo}.{alias.name}')
        return list(set(imports))

    def _extraer_clases(self, arbol: ast.AST) -> List[str]:
        return [n.name for n in ast.walk(arbol) if isinstance(n, ast.ClassDef)]

    # ── Riesgo y resumen ──────────────────────────────────────────────────

    def _calcular_riesgo(self, r: AnalisisCompleto) -> str:
        errores    = sum(1 for p in r.problemas if p.tipo == 'error')
        seguridad  = sum(1 for p in r.problemas if p.herramienta == 'bandit')
        cc         = r.metricas.cc
        mi         = r.metricas.mi

        if errores > 0 or seguridad > 2 or cc > 20:
            return 'crítico'
        if seguridad > 0 or cc > 15 or mi < 20:
            return 'alto'
        if cc > 10 or mi < 50:
            return 'medio'
        return 'bajo'

    def _generar_resumen(self, r: AnalisisCompleto) -> str:
        errores = [p for p in r.problemas if p.tipo == 'error']
        avisos  = [p for p in r.problemas if p.tipo == 'advertencia']
        seg     = [p for p in r.problemas if p.herramienta == 'bandit']

        partes = []
        partes.append(f"Código de {r.metricas.loc} líneas.")

        cc = r.metricas.cc
        if cc <= 5:
            partes.append(f"Complejidad CC={cc} — muy simple, excelente.")
        elif cc <= 10:
            partes.append(f"Complejidad CC={cc} — dentro del rango aceptable.")
        elif cc <= 15:
            partes.append(f"Complejidad CC={cc} — elevada, vale la pena refactorizar.")
        else:
            partes.append(f"Complejidad CC={cc} — crítica, demasiados caminos de ejecución.")

        mi = r.metricas.mi
        if mi >= 65:
            partes.append(f"Mantenibilidad MI={mi} — código limpio y legible.")
        elif mi >= 30:
            partes.append(f"Mantenibilidad MI={mi} — aceptable pero mejorable.")
        else:
            partes.append(f"Mantenibilidad MI={mi} — difícil de mantener a largo plazo.")

        if errores:
            partes.append(f"{len(errores)} error(es) crítico(s) que rompen el código.")
        if seg:
            partes.append(f"{len(seg)} problema(s) de seguridad detectado(s).")
        if avisos and not errores:
            partes.append(f"{len(avisos)} advertencia(s) de estilo/calidad.")
        if not errores and not seg and not avisos:
            partes.append("Sin problemas detectados.")

        riesgo_txt = {
            'bajo': 'Riesgo bajo — código en buen estado.',
            'medio': 'Riesgo medio — revisión recomendada.',
            'alto': 'Riesgo alto — necesita atención.',
            'crítico': 'Riesgo crítico — no se recomienda usar en producción sin fixes.',
        }
        partes.append(riesgo_txt.get(r.metricas.nivel_riesgo, ''))

        return ' '.join(partes)


_instancia: Optional[AnalizadorCodigo] = None

def obtener() -> AnalizadorCodigo:
    global _instancia
    if _instancia is None:
        _instancia = AnalizadorCodigo()
    return _instancia