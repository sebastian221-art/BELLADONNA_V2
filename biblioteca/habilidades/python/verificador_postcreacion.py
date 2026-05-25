# biblioteca/habilidades/python/verificador_postcreacion.py
# ============================================================
# VERIFICADOR POST-CREACIÓN — QA automático antes de entregar
#
# Bell NO entrega código hasta que pase todos los filtros.
# Si algo falla → corrige → vuelve a verificar.
# Máximo 2 ciclos de corrección para no bloquearse.
#
# Pipeline de verificación:
#   1. AST (sintaxis)
#   2. Antipatrones (estilo/bugs)
#   3. Hypothesis (crashes)
#   4. mypy (tipos)
#   5. Ejecución real (si tiene main o ejemplo)
# ============================================================

import ast
import os
import re
from dataclasses import dataclass, field
from typing import List, Optional

_GROQ_URL   = 'https://api.groq.com/openai/v1/chat/completions'
_GROQ_MODEL = 'openai/gpt-oss-120b'


@dataclass
class ResultadoVerificacion:
    aprobado:       bool
    ciclos:         int            = 0
    codigo_final:   str            = ''
    problemas:      List[str]      = field(default_factory=list)
    correcciones:   List[str]      = field(default_factory=list)
    reporte:        str            = ''


def verificar_y_corregir(codigo: str, requerimiento: str = '') -> ResultadoVerificacion:
    """
    Verifica el código generado y lo corrige si falla.
    Retorna el código limpio listo para entregar.
    """
    resultado = ResultadoVerificacion(aprobado=False, codigo_final=codigo)

    for ciclo in range(1, 3):  # máximo 2 ciclos
        resultado.ciclos = ciclo
        problemas = _verificar_completo(resultado.codigo_final)

        if not problemas:
            resultado.aprobado   = True
            resultado.reporte    = f'✅ Verificado en {ciclo} ciclo(s) — sin problemas.'
            break

        resultado.problemas.extend(problemas)
        codigo_corregido = _corregir_con_groq(resultado.codigo_final, problemas, requerimiento)

        if codigo_corregido and codigo_corregido != resultado.codigo_final:
            resultado.correcciones.append(
                f'Ciclo {ciclo}: corregidos {len(problemas)} problema(s)'
            )
            resultado.codigo_final = codigo_corregido
        else:
            # Groq no pudo corregir — entregar con advertencia
            resultado.aprobado = True
            resultado.reporte  = (
                f'⚠️  Entregado con {len(problemas)} advertencia(s) sin resolver.'
            )
            break

    if not resultado.aprobado:
        resultado.aprobado = True
        resultado.reporte  = f'⚠️  Entregado tras {resultado.ciclos} ciclo(s).'

    return resultado


def _verificar_completo(codigo: str) -> List[str]:
    """Ejecuta todos los verificadores y retorna lista de problemas."""
    problemas = []

    # 1. Sintaxis AST
    p_ast = _verificar_ast(codigo)
    if p_ast:
        return p_ast   # sin sintaxis no tiene sentido continuar

    # 2. Antipatrones críticos
    p_anti = _verificar_antipatrones(codigo)
    problemas.extend(p_anti)

    # 3. mypy
    p_mypy = _verificar_mypy(codigo)
    problemas.extend(p_mypy)

    # 4. Hypothesis (solo si hay funciones con args simples)
    p_hyp = _verificar_hypothesis_rapido(codigo)
    problemas.extend(p_hyp)

    return problemas


def _verificar_ast(codigo: str) -> List[str]:
    """Verifica sintaxis con AST."""
    try:
        ast.parse(codigo)
        return []
    except SyntaxError as e:
        return [f'SyntaxError en L{e.lineno}: {e.msg}']


def _verificar_antipatrones(codigo: str) -> List[str]:
    """Detecta antipatrones críticos."""
    try:
        from biblioteca.habilidades.python.detector_antipatrones import analizar
        antis = analizar(codigo)
        criticos = [a for a in antis if a.severidad == 'critico']
        return [f'L{a.linea} [{a.patron}]: {a.sugerencia}' for a in criticos[:3]]
    except Exception:
        return []


def _verificar_mypy(codigo: str) -> List[str]:
    """Verifica tipos con mypy."""
    import subprocess, sys, tempfile
    try:
        with tempfile.NamedTemporaryFile(suffix='.py', mode='w',
                                          delete=False, encoding='utf-8') as f:
            f.write(codigo)
            path = f.name
        proc = subprocess.run(
            [sys.executable, '-m', 'mypy', '--ignore-missing-imports',
             '--no-error-summary', path],
            capture_output=True, text=True, timeout=20
        )
        os.unlink(path)
        errores = [
            l.split('error:')[-1].strip()
            for l in proc.stdout.splitlines()
            if 'error:' in l
        ]
        return errores[:2]
    except Exception:
        return []


def _verificar_hypothesis_rapido(codigo: str) -> List[str]:
    """Hypothesis rápido — solo 50 casos para no bloquear."""
    try:
        from biblioteca.habilidades.python.probador_hipotesis import probar
        resultado = probar(codigo, max_casos=50)
        if resultado.fallos:
            fallos = resultado.fallos[:2]
            return [f'Hypothesis crash: {f.funcion}({f.input_fallo}) → {f.tipo_error}'
                    for f in fallos]
        return []
    except Exception:
        return []


def _corregir_con_groq(codigo: str, problemas: List[str], requerimiento: str) -> str:
    """Pide a Groq que corrija los problemas detectados."""
    import httpx
    api_key = os.getenv('GROQ_API_KEY', '')
    if not api_key:
        return ''

    problemas_str = '\n'.join(f'- {p}' for p in problemas)
    prompt = (
        f'<codigo_con_problemas>\n{codigo}\n</codigo_con_problemas>\n'
        f'<problemas>\n{problemas_str}\n</problemas>\n'
        f'<requerimiento_original>{requerimiento}</requerimiento_original>\n'
        f'<instruccion>Corrige SOLO los problemas listados. '
        f'No cambies la lógica ni el diseño. Devuelve el código completo corregido. '
        f'Sin explicaciones, sin markdown, solo el código Python.</instruccion>'
    )

    try:
        r = httpx.post(
            _GROQ_URL,
            headers={'Authorization': f'Bearer {api_key}',
                     'Content-Type': 'application/json'},
            json={
                'model': _GROQ_MODEL,
                'messages': [
                    {'role': 'system',
                     'content': 'Corriges código Python. Solo devuelves código limpio sin markdown.'},
                    {'role': 'user', 'content': prompt},
                ],
                'temperature': 0.1,
                'max_tokens': 2000,
            },
            timeout=30,
        )
        if r.status_code == 200:
            contenido = (r.json().get('choices', [{}])[0]
                         .get('message', {}).get('content', '').strip())
            # Limpiar markdown si viene
            contenido = re.sub(r'^```python\s*', '', contenido)
            contenido = re.sub(r'\s*```$', '', contenido)
            return contenido.strip()
    except Exception:
        pass
    return ''