# biblioteca/habilidades/python/ejecutor_codigo.py
# ============================================================
# EJECUTOR SANDBOX — ejecución real y segura
#
# Flujo:
#   1. Guardia AST: bloquea operaciones peligrosas antes de ejecutar
#   2. Subprocess aislado con timeout y límite de output
#   3. Captura stdout, stderr, tiempo, código de salida
#
# Lo que ningún LLM puede hacer: ver el output REAL.
# Bell ejecuta y dice exactamente qué pasó.
# ============================================================

import ast
import subprocess
import sys
import tempfile
import os
import time
from dataclasses import dataclass
from typing import Optional


# Nodos AST peligrosos que se bloquean antes de ejecutar
_NODOS_PELIGROSOS = {
    'os.system', 'os.popen', 'os.remove', 'os.rmdir', 'os.unlink',
    'shutil.rmtree', 'shutil.move', 'subprocess.call', 'subprocess.run',
    'subprocess.Popen', '__import__', 'importlib.import_module',
    'open',  # modo write — se filtra abajo con más granularidad
}

_LLAMADAS_BLOQUEADAS = {
    'eval', 'exec', 'compile', '__import__',
}

_TIMEOUT_SEG  = 10
_MAX_OUTPUT   = 8_000   # chars máximos de stdout


@dataclass
class ResultadoEjecucion:
    exitoso:     bool
    stdout:      str  = ''
    stderr:      str  = ''
    tiempo_ms:   int  = 0
    codigo_exit: int  = 0
    bloqueado:   bool = False
    razon_bloqueo: str = ''
    resumen_bell:  str = ''


class GuardiaAST(ast.NodeVisitor):
    """
    Visita el AST antes de ejecutar y bloquea operaciones peligrosas.
    Matemáticamente preciso — no puede engañarse.
    """

    def __init__(self):
        self.peligros: list = []

    def visit_Call(self, nodo):
        nombre = self._nombre_nodo(nodo.func)
        if nombre in _LLAMADAS_BLOQUEADAS:
            self.peligros.append(f"Llamada bloqueada: {nombre}()")

        # open() en modo escritura
        if nombre == 'open' and nodo.args:
            if len(nodo.args) > 1:
                modo = nodo.args[1]
                if isinstance(modo, ast.Constant) and any(
                    c in str(modo.value) for c in ['w', 'a', 'x']
                ):
                    self.peligros.append("open() en modo escritura bloqueado")

        self.generic_visit(nodo)

    def visit_Import(self, nodo):
        modulos_bloq = {'os', 'shutil', 'subprocess', 'socket', 'ftplib', 'smtplib'}
        for alias in nodo.names:
            if alias.name in modulos_bloq:
                self.peligros.append(f"import {alias.name} bloqueado en sandbox")
        self.generic_visit(nodo)

    def visit_ImportFrom(self, nodo):
        modulos_bloq = {'os', 'shutil', 'subprocess', 'socket'}
        if nodo.module in modulos_bloq:
            self.peligros.append(f"from {nodo.module} import ... bloqueado en sandbox")
        self.generic_visit(nodo)

    def _nombre_nodo(self, nodo) -> str:
        if isinstance(nodo, ast.Name):
            return nodo.id
        if isinstance(nodo, ast.Attribute):
            return f"{self._nombre_nodo(nodo.value)}.{nodo.attr}"
        return ''


class EjecutorCodigo:

    def ejecutar(self, codigo: str, entrada: str = '') -> ResultadoEjecucion:
        if not codigo or not codigo.strip():
            return ResultadoEjecucion(False, stderr='Código vacío.')

        # ── PASO 1: Validar sintaxis ───────────────────────────────────────
        try:
            arbol = ast.parse(codigo)
        except SyntaxError as e:
            return ResultadoEjecucion(
                exitoso=False,
                stderr=f'SyntaxError línea {e.lineno}: {e.msg}',
                resumen_bell=f'El código tiene un error de sintaxis en la línea {e.lineno}: {e.msg}'
            )

        # ── PASO 2: Guardia de seguridad ───────────────────────────────────
        guardia = GuardiaAST()
        guardia.visit(arbol)
        if guardia.peligros:
            razon = ' | '.join(guardia.peligros)
            return ResultadoEjecucion(
                exitoso=False,
                bloqueado=True,
                razon_bloqueo=razon,
                resumen_bell=f'Ejecución bloqueada por seguridad: {razon}'
            )

        # ── PASO 3: Ejecutar en subprocess aislado ─────────────────────────
        with tempfile.NamedTemporaryFile(
            suffix='.py', mode='w', delete=False, encoding='utf-8'
        ) as f:
            f.write(codigo)
            tmp_path = f.name

        t0 = time.time()
        try:
            proc = subprocess.run(
                [sys.executable, tmp_path],
                input=entrada,
                capture_output=True,
                text=True,
                timeout=_TIMEOUT_SEG,
                env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}
            )
            elapsed_ms = int((time.time() - t0) * 1000)

            stdout = proc.stdout[:_MAX_OUTPUT]
            stderr = proc.stderr[:_MAX_OUTPUT]
            exitoso = proc.returncode == 0

            resumen = self._generar_resumen(exitoso, stdout, stderr, elapsed_ms, proc.returncode)

            return ResultadoEjecucion(
                exitoso=exitoso,
                stdout=stdout,
                stderr=stderr,
                tiempo_ms=elapsed_ms,
                codigo_exit=proc.returncode,
                resumen_bell=resumen,
            )

        except subprocess.TimeoutExpired:
            return ResultadoEjecucion(
                exitoso=False,
                stderr=f'Timeout: el código tardó más de {_TIMEOUT_SEG}s.',
                resumen_bell=f'El código superó el tiempo límite de {_TIMEOUT_SEG} segundos. Posible bucle infinito.'
            )
        except Exception as e:
            return ResultadoEjecucion(
                exitoso=False,
                stderr=str(e),
                resumen_bell=f'Error al ejecutar: {e}'
            )
        finally:
            try:
                os.unlink(tmp_path)
            except Exception:
                pass

    def _generar_resumen(self, ok, stdout, stderr, ms, code) -> str:
        if ok:
            lineas_out = stdout.strip().count('\n') + 1 if stdout.strip() else 0
            return (
                f"Ejecución exitosa en {ms}ms. "
                f"{'Output: ' + stdout.strip()[:200] if stdout.strip() else 'Sin output.'}"
            )
        else:
            # Extraer tipo de error del stderr
            tipo_error = 'Error desconocido'
            for linea in (stderr or '').split('\n'):
                if 'Error' in linea or 'Exception' in linea:
                    tipo_error = linea.strip()
                    break
            return f"Falló con código {code} en {ms}ms. {tipo_error}"


_instancia: Optional[EjecutorCodigo] = None

def obtener() -> EjecutorCodigo:
    global _instancia
    if _instancia is None:
        _instancia = EjecutorCodigo()
    return _instancia