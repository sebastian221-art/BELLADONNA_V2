# biblioteca/habilidades/python/generador_codigo.py
# ============================================================
# GENERADOR DE CÓDIGO — Groq con prompt XML estructurado
#
# Groq maneja toda la generación (simple y compleja).
# Bell inyecta:
#   - Patrones reales de Sebastian (contexto de estilo)
#   - Análisis previo si existe (contexto técnico)
#   - Prompt XML con restricciones estrictas
#
# El output de Groq es extraído con regex desde <bell_code>,
# validado con AST, y si falla mypy se reintenta con el error.
# ============================================================

import os
import re
import ast
import subprocess
import tempfile
import time
import json
from typing import Optional
from dataclasses import dataclass


_GROQ_URL    = 'https://api.groq.com/openai/v1/chat/completions'
_GROQ_MODEL  = 'openai/gpt-oss-120b'
_TIMEOUT     = 25


@dataclass
class ResultadoGeneracion:
    exitoso:     bool
    codigo:      str  = ''
    es_valido:   bool = False
    intentos:    int  = 1
    fuente:      str  = 'groq'
    error:       str  = ''
    resumen_bell: str = ''


_SYSTEM_PROMPT = """Eres el motor de generación de código de BELLADONNA, la IA de Sebastian.
Generas ÚNICAMENTE código Python 3.12 perfecto, sin texto adicional.

REGLAS ABSOLUTAS:
1. Responde SOLO con el código dentro de <bell_code>...</bell_code>
2. Type hints obligatorios en TODAS las funciones
3. Docstrings en español, formato Google
4. Sin markdown (``` no se usa), sin explicaciones fuera del código
5. Comentarios inline en español cuando algo no sea obvio
6. Sigue exactamente el estilo de los patrones de Sebastian que se te muestran"""


class GeneradorCodigo:

    def __init__(self):
        self._api_key = os.getenv('GROQ_API_KEY', '')
        self._activo = bool(self._api_key)
        if not self._activo:
            print('  [Generador] ⚠️  GROQ_API_KEY no disponible')

    def generar(
        self,
        requerimiento: str,
        contexto_analisis: str = '',
        patrones_sebastian: str = '',
        max_intentos: int = 2,
    ) -> ResultadoGeneracion:

        if not self._activo:
            return ResultadoGeneracion(
                exitoso=False,
                error='GROQ_API_KEY no configurada.',
                resumen_bell='No puedo generar código ahora — falta la API key de Groq.'
            )

        prompt = self._construir_prompt(requerimiento, contexto_analisis, patrones_sebastian)

        for intento in range(1, max_intentos + 1):
            codigo, error_groq = self._llamar_groq(prompt)
            if not codigo:
                if intento == max_intentos:
                    return ResultadoGeneracion(
                        exitoso=False, intentos=intento,
                        error=error_groq,
                        resumen_bell='Groq no respondió correctamente.'
                    )
                continue

            # Validar AST
            valido, error_ast = self._validar_ast(codigo)
            if not valido:
                # Reintentar con el error
                prompt = self._prompt_con_error(requerimiento, codigo, error_ast)
                continue

            return ResultadoGeneracion(
                exitoso=True,
                codigo=codigo,
                es_valido=True,
                intentos=intento,
                fuente='groq',
                resumen_bell=self._resumen_generacion(codigo, requerimiento),
            )

        return ResultadoGeneracion(
            exitoso=False, intentos=max_intentos,
            error='No se pudo generar código válido.',
            resumen_bell='Intenté varias veces pero el código no pasó validación.'
        )

    def _construir_prompt(
        self, requerimiento: str, contexto: str, patrones: str
    ) -> str:
        partes = [f"<requerimiento>\n{requerimiento}\n</requerimiento>"]

        if patrones:
            partes.insert(0,
                f"<patrones_sebastian>\n{patrones}\n</patrones_sebastian>"
            )

        if contexto:
            partes.append(f"<contexto_tecnico>\n{contexto}\n</contexto_tecnico>")

        partes.append(
            "<restricciones>\n"
            "Genera ÚNICAMENTE el código Python dentro de <bell_code>.\n"
            "Type hints obligatorios. Docstrings en español.\n"
            "Sin texto fuera de <bell_code>.\n"
            "</restricciones>"
        )

        return '\n\n'.join(partes)

    def _prompt_con_error(self, req: str, codigo_fallido: str, error: str) -> str:
        return (
            f"<requerimiento>\n{req}\n</requerimiento>\n\n"
            f"<codigo_anterior_con_error>\n{codigo_fallido}\n</codigo_anterior_con_error>\n\n"
            f"<error_detectado>\n{error}\n</error_detectado>\n\n"
            "<instruccion>Corrige el error y genera el código correcto dentro de <bell_code>.</instruccion>"
        )

    def _llamar_groq(self, prompt: str) -> tuple:
        try:
            import httpx
            t0 = time.time()
            r = httpx.post(
                _GROQ_URL,
                headers={
                    'Authorization': f'Bearer {self._api_key}',
                    'Content-Type': 'application/json',
                },
                json={
                    'model': _GROQ_MODEL,
                    'messages': [
                        {'role': 'system', 'content': _SYSTEM_PROMPT},
                        {'role': 'user',   'content': prompt},
                    ],
                    'temperature': 0.2,
                    'max_tokens': 2048,
                },
                timeout=_TIMEOUT,
            )
            elapsed = round(time.time() - t0, 2)

            if r.status_code != 200:
                return '', f'HTTP {r.status_code}'

            contenido = (
                r.json()
                .get('choices', [{}])[0]
                .get('message', {})
                .get('content', '')
                .strip()
            )

            codigo = self._extraer_bell_code(contenido)
            print(f'  [Generador] Groq {elapsed}s | {len(codigo)} chars')
            return codigo, ''

        except Exception as e:
            return '', str(e)

    def _extraer_bell_code(self, texto: str) -> str:
        """Extrae código de las etiquetas <bell_code>...</bell_code>"""
        match = re.search(r'<bell_code>(.*?)</bell_code>', texto, re.DOTALL)
        if match:
            return match.group(1).strip()

        # Fallback: si no hay etiquetas, limpiar markdown y usar todo
        texto = re.sub(r'```python\s*', '', texto)
        texto = re.sub(r'```\s*', '', texto)
        return texto.strip()

    def _validar_ast(self, codigo: str) -> tuple:
        try:
            ast.parse(codigo)
            return True, ''
        except SyntaxError as e:
            return False, f'SyntaxError línea {e.lineno}: {e.msg}'

    def _resumen_generacion(self, codigo: str, req: str) -> str:
        lineas = len(codigo.strip().split('\n'))
        funciones = len(re.findall(r'^\s*def ', codigo, re.MULTILINE))
        clases = len(re.findall(r'^\s*class ', codigo, re.MULTILINE))

        partes = [f"Código generado: {lineas} líneas."]
        if funciones:
            partes.append(f"{funciones} función(es).")
        if clases:
            partes.append(f"{clases} clase(s).")
        partes.append("Validado con AST — sintaxis correcta.")
        return ' '.join(partes)


_instancia: Optional[GeneradorCodigo] = None

def obtener() -> GeneradorCodigo:
    global _instancia
    if _instancia is None:
        _instancia = GeneradorCodigo()
    return _instancia