# biblioteca/habilidades/python/generador_codigo.py
# ============================================================
# GENERADOR DE CÓDIGO v2 — 2 soluciones + benchmark real
#
# ANTES: generaba UNA solución
# AHORA:
#   1. Genera solución EXPLÍCITA (clara, paso a paso)
#   2. Genera solución PYTHÓNICA (concisa, built-ins, idiomática)
#   3. Hace benchmark real con timeit de ambas
#   4. Valida ambas con AST
#   5. Muestra pros/cons de cada una
#
# El benchmark es REAL — Bell ejecuta ambas y mide.
# GPT-4o solo puede estimarlo. Bell lo prueba.
# ============================================================

import os
import re
import ast
import timeit
from typing import Optional
from dataclasses import dataclass


_GROQ_URL    = 'https://api.groq.com/openai/v1/chat/completions'
_GROQ_MODEL  = 'openai/gpt-oss-120b'
_TIMEOUT     = 30


@dataclass
class SolucionGenerada:
    nombre:       str           # 'explícita' o 'pythónica'
    codigo:       str
    es_valida:    bool
    descripcion:  str           # por qué elegir esta
    tiempo_ms:    float = -1.0  # benchmark real
    n_lineas:     int = 0


@dataclass
class ResultadoGeneracion:
    exitoso:      bool
    soluciones:   list          # List[SolucionGenerada]
    codigo:       str           # solución recomendada (la pythónica si OK)
    fuente:       str = 'groq'
    error:        str = ''
    resumen_bell: str = ''
    benchmark:    str = ''


_SYSTEM_PROMPT = """Eres el generador de código de BELLADONNA, la IA de Sebastian Mora.
Generas código Python 3.12 perfecto en español.

REGLAS ABSOLUTAS:
1. Responde con DOS implementaciones separadas en <solucion_explicita> y <solucion_pythonica>
2. La explícita: clara, paso a paso, para entender fácilmente
3. La pythónica: concisa, usa built-ins (sum, map, filter, Counter, etc.), idiomática
4. Type hints obligatorios en ambas
5. Docstring Google-style en español en ambas
6. Sin markdown dentro del código
7. Sigue el estilo de los patrones de Sebastian que se muestran"""


class GeneradorCodigo:

    def __init__(self):
        self._api_key = os.getenv('GROQ_API_KEY', '')
        self._activo = bool(self._api_key)

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
                soluciones=[],
                codigo='',
                error='GROQ_API_KEY no configurada.',
                resumen_bell='No puedo generar código ahora — falta la API key de Groq.'
            )

        prompt = self._construir_prompt(requerimiento, contexto_analisis,
                                        patrones_sebastian)

        for intento in range(1, max_intentos + 1):
            raw, error_groq = self._llamar_groq(prompt)
            if error_groq:
                continue

            # Extraer las dos soluciones
            sol_explicita = self._extraer_bloque(raw, 'solucion_explicita')
            sol_pythonica  = self._extraer_bloque(raw, 'solucion_pythonica')

            # Fallback: si no separó, intentar extraer un solo bloque
            if not sol_explicita and not sol_pythonica:
                sol_unica = self._extraer_codigo_generico(raw)
                if sol_unica:
                    sol_explicita = sol_unica
                    sol_pythonica = sol_unica

            if not sol_explicita and not sol_pythonica:
                continue

            # Validar con AST
            soluciones = []

            if sol_explicita:
                valida = self._validar_ast(sol_explicita)
                s = SolucionGenerada(
                    nombre='explícita',
                    codigo=sol_explicita,
                    es_valida=valida,
                    descripcion='Clara y paso a paso — ideal para entender la lógica',
                    n_lineas=sol_explicita.count('\n') + 1,
                )
                soluciones.append(s)

            if sol_pythonica and sol_pythonica != sol_explicita:
                valida = self._validar_ast(sol_pythonica)
                s = SolucionGenerada(
                    nombre='pythónica',
                    codigo=sol_pythonica,
                    es_valida=valida,
                    descripcion='Concisa y idiomática — usa built-ins de Python',
                    n_lineas=sol_pythonica.count('\n') + 1,
                )
                soluciones.append(s)

            validas = [s for s in soluciones if s.es_valida]
            if not validas:
                continue

            # Benchmark real con timeit
            benchmark_txt = self._benchmark_soluciones(validas, requerimiento)

            # La recomendada: pythónica si válida, sino explícita
            pythonica_v = next((s for s in validas if s.nombre == 'pythónica'), None)
            explicita_v = next((s for s in validas if s.nombre == 'explícita'), None)
            recomendada = pythonica_v or explicita_v

            # Resumen
            n = recomendada.n_lineas
            n_soluciones = len(validas)
            resumen = (
                f'Código generado: {n} líneas. '
                f'{n_soluciones} solución(es). '
                f'Validado con AST — sintaxis correcta.'
            )
            if n_soluciones > 1:
                resumen += f'\n{benchmark_txt}'

            return ResultadoGeneracion(
                exitoso    = True,
                soluciones = validas,
                codigo     = recomendada.codigo,
                resumen_bell = resumen,
                benchmark  = benchmark_txt,
            )

        return ResultadoGeneracion(
            exitoso      = False,
            soluciones   = [],
            codigo       = '',
            error        = 'No se pudo generar código válido.',
            resumen_bell = 'No pude generar el código. Intenta reformular el requerimiento.',
        )

    def _benchmark_soluciones(self, soluciones: list,
                               requerimiento: str) -> str:
        """
        Benchmark REAL con timeit.
        Extrae la función principal y la ejecuta con datos de prueba.
        """
        if len(soluciones) < 2:
            return ''

        resultados = []
        datos_prueba = self._generar_datos_prueba(requerimiento)

        for sol in soluciones:
            try:
                # Extraer nombre de la función principal
                arbol = ast.parse(sol.codigo)
                funciones = [n.name for n in ast.walk(arbol)
                             if isinstance(n, ast.FunctionDef)]
                if not funciones:
                    continue

                fn_nombre = funciones[0]
                setup = f'{sol.codigo}\n{datos_prueba["setup"]}'
                stmt  = f'{fn_nombre}({datos_prueba["args"]})'

                t = timeit.timeit(stmt=stmt, setup=setup, number=5000)
                tiempo_ms = (t / 5000) * 1000
                sol.tiempo_ms = round(tiempo_ms, 4)
                resultados.append(sol)

            except Exception:
                pass

        if not resultados:
            return ''

        resultados.sort(key=lambda s: s.tiempo_ms)
        partes = ['⚡ Benchmark real (5,000 iteraciones):']

        mas_rapida = resultados[0]
        for sol in resultados:
            if sol.tiempo_ms == mas_rapida.tiempo_ms:
                icono = '🥇'
                extra = ' ← más rápida'
            else:
                ratio = sol.tiempo_ms / mas_rapida.tiempo_ms
                icono = '🥈'
                extra = f' ({ratio:.1f}x más lenta)'
            partes.append(
                f'  {icono} Versión {sol.nombre}: {sol.tiempo_ms:.4f}ms{extra}'
            )

        return '\n'.join(partes)

    def _generar_datos_prueba(self, requerimiento: str) -> dict:
        """Genera datos de prueba apropiados según el requerimiento."""
        req = requerimiento.lower()

        if 'lista' in req and 'número' in req or 'numeros' in req:
            return {
                'setup': 'import random; datos = [random.randint(1, 100) for _ in range(1000)]',
                'args': 'datos',
            }
        if 'texto' in req or 'string' in req or 'str' in req:
            return {
                'setup': 'texto = "Hola mundo este es un texto de prueba " * 50',
                'args': 'texto',
            }
        if 'dict' in req or 'diccionario' in req:
            return {
                'setup': 'datos = {str(i): i for i in range(100)}',
                'args': 'datos',
            }
        # Default: lista de enteros
        return {
            'setup': 'datos = list(range(100))',
            'args': 'datos',
        }

    def _llamar_groq(self, prompt: str):
        try:
            import httpx
            r = httpx.post(
                _GROQ_URL,
                headers={'Authorization': f'Bearer {self._api_key}',
                         'Content-Type': 'application/json'},
                json={
                    'model':       _GROQ_MODEL,
                    'messages':    [
                        {'role': 'system', 'content': _SYSTEM_PROMPT},
                        {'role': 'user',   'content': prompt},
                    ],
                    'temperature': 0.2,
                    'max_tokens':  900,
                },
                timeout=_TIMEOUT,
            )
            if r.status_code == 200:
                content = (r.json().get('choices', [{}])[0]
                           .get('message', {}).get('content', '').strip())
                return content, None
            return '', f'HTTP {r.status_code}'
        except Exception as e:
            return '', str(e)

    def _construir_prompt(self, req: str, ctx: str, patrones: str) -> str:
        partes = [f'<requerimiento>{req}</requerimiento>']
        if ctx:
            partes.append(f'<contexto_analisis>{ctx[:400]}</contexto_analisis>')
        if patrones:
            partes.append(f'<patrones_sebastian>{patrones[:600]}</patrones_sebastian>')
        partes.append(
            '<instruccion>\n'
            'Genera DOS implementaciones:\n'
            '1. <solucion_explicita> ... código ... </solucion_explicita>\n'
            '2. <solucion_pythonica> ... código ... </solucion_pythonica>\n'
            'Ambas deben tener type hints y docstring en español.\n'
            'La pythónica debe usar built-ins: sum(), Counter(), map(), etc.\n'
            '</instruccion>'
        )
        return '\n\n'.join(partes)

    def _extraer_bloque(self, texto: str, etiqueta: str) -> str:
        m = re.search(
            rf'<{etiqueta}>\s*(?:```python)?\s*\n?(.*?)(?:```)?\s*</{etiqueta}>',
            texto, re.DOTALL | re.IGNORECASE
        )
        if m:
            return m.group(1).strip()
        return ''

    def _extraer_codigo_generico(self, texto: str) -> str:
        m = re.search(r'```python\s*\n(.*?)```', texto, re.DOTALL)
        if m:
            return m.group(1).strip()
        m = re.search(r'<bell_code>\s*(.*?)\s*</bell_code>', texto, re.DOTALL)
        if m:
            return m.group(1).strip()
        return ''

    def _validar_ast(self, codigo: str) -> bool:
        try:
            ast.parse(codigo)
            return True
        except SyntaxError:
            return False


_instancia: Optional[GeneradorCodigo] = None


def obtener() -> GeneradorCodigo:
    global _instancia
    if _instancia is None:
        _instancia = GeneradorCodigo()
    return _instancia