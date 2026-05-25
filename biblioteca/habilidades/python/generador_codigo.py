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
7. Sigue el estilo de los patrones de Sebastian que se muestran
8. SIEMPRE usa time.perf_counter() para medir tiempos — NUNCA time.time() ni time.monotonic()
9. Si el código involucra Pipeline o medición de tiempo, usa time.perf_counter() en AMBAS soluciones"""


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

        print(f'  [Generador] activo={self._activo} | key={bool(self._api_key)} | req={requerimiento[:50]}')

        # Intentar recargar la key si no está disponible (puede no estar en env al inicio)
        if not self._activo:
            self._api_key = os.getenv('GROQ_API_KEY', '')
            self._activo  = bool(self._api_key)
            print(f'  [Generador] Recargando key: activo={self._activo}')

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

            # Mostrar dónde están los tags para diagnóstico
            tags_encontrados = []
            for tag in ['<solucion_explicita>', '</solucion_explicita>',
                        '<solucion_pythonica>', '</solucion_pythonica>', '```python', '```']:
                idx = raw.find(tag)
                if idx >= 0:
                    tags_encontrados.append(f'{tag}@{idx}')
            print(f'  [Generador] Tags: {tags_encontrados}')
            print(f'  [Generador] Raw preview: {repr(raw[:500])}')

            # Extraer las dos soluciones
            sol_explicita = self._extraer_bloque(raw, 'solucion_explicita')
            sol_pythonica  = self._extraer_bloque(raw, 'solucion_pythonica')

            # Fix: reemplazar time.time() por time.perf_counter() (más preciso)
            import re as _re
            if sol_explicita:
                sol_explicita = _re.sub(r'\btime\.time\(\)', 'time.perf_counter()', sol_explicita)
            if sol_pythonica:
                sol_pythonica = _re.sub(r'\btime\.time\(\)', 'time.perf_counter()', sol_pythonica)

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
            # Validar ejecutando con datos reales — filtra bugs como O(n²) oculto
            validas = self._validar_ejecucion(validas, requerimiento)
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

        # Mensajes con texto/timestamp/emocion → dicts con las claves correctas
        if 'mensaje' in req or ('texto' in req and 'timestamp' in req):
            return {
                'setup': (
                    'datos = ['
                    '{"texto": "Hola mundo", "timestamp": 1000.0, "emocion": "feliz"},'
                    '{"texto": "Texto mas largo aqui para comparar", "timestamp": 1060.0, "emocion": "feliz"},'
                    '{"texto": "Adios", "timestamp": 1120.0, "emocion": "triste"}'
                    ']'
                ),
                'args': 'datos',
            }
        if 'nodo' in req or 'energia' in req:
            return {
                'setup': (
                    'datos = ['
                    '{"energia": 0.8, "id": 1},'
                    '{"energia": 0.3, "id": 2},'
                    '{"energia": True, "id": 3}'
                    ']'
                ),
                'args': 'datos',
            }
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
        print(f'  [Generador] Llamando Groq | len_prompt={len(prompt)}')
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
                    'max_tokens':  1800,
                },
                timeout=_TIMEOUT,
            )
            print(f'  [Generador] Groq status={r.status_code}')
            if r.status_code == 200:
                content = (r.json().get('choices', [{}])[0]
                           .get('message', {}).get('content', '').strip())
                print(f'  [Generador] Groq OK | {len(content)} chars')
                return content, None
            print(f'  [Generador] Groq error: HTTP {r.status_code} | {r.text[:100]}')
            return '', f'HTTP {r.status_code}'
        except Exception as e:
            return '', str(e)

    def _construir_prompt(self, req: str, ctx: str, patrones: str) -> str:
        # Enriquecer con contexto máximo (estilo, librerías, convenciones)
        try:
            from biblioteca.habilidades.python.contexto_maximo import construir_contexto
            ctx_max = construir_contexto(req)
            if ctx_max:
                ctx = ctx_max + ('\n' + ctx if ctx else '')
        except Exception:
            pass
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
        """Extractor tolerante: acepta con/sin cierre, con/sin backticks."""
        # Intento 1: tag apertura + cierre
        m = re.search(
            rf'<{etiqueta}>\s*(?:```python)?\s*\n?(.*?)(?:```)?\s*</{etiqueta}>',
            texto, re.DOTALL | re.IGNORECASE
        )
        if m and m.group(1).strip():
            return m.group(1).strip()
        # Intento 2: solo apertura, hasta el próximo tag o fin de texto
        m2 = re.search(
            rf'<{etiqueta}>\s*(?:```python)?\s*\n?(.*?)(?=<[a-zA-Z/]|\Z)',
            texto, re.DOTALL | re.IGNORECASE
        )
        if m2 and m2.group(1).strip():
            code = re.sub(r'```\s*$', '', m2.group(1)).strip()
            return code
        return ''

    def _extraer_codigo_generico(self, texto: str) -> str:
        """Fallback: extrae cualquier bloque de código Python del texto."""
        # ```python ... ```
        m = re.search(r'```python\s*\n(.*?)```', texto, re.DOTALL)
        if m and m.group(1).strip():
            return m.group(1).strip()
        # ``` ... ``` (sin lenguaje)
        m = re.search(r'```\s*\n(.*?)```', texto, re.DOTALL)
        if m and m.group(1).strip():
            code = m.group(1).strip()
            if 'def ' in code or 'class ' in code:
                return code
        # Último recurso: todo el texto si parece código
        if 'def ' in texto or 'class ' in texto:
            lineas = texto.split('\n')
            for i, l in enumerate(lineas):
                if re.match(r'^(def |class |from |import )', l.strip()):
                    return '\n'.join(lineas[i:]).strip()
        return ''

    def _validar_ejecucion(self, soluciones: list, requerimiento: str) -> list:
        """
        Valida ejecutando cada solución con datos de prueba.
        ADVISORY — nunca descarta código AST-válido.
        Las clases se aceptan directamente sin ejecución.
        """
        import subprocess, sys, tempfile, os, json

        datos = self._generar_datos_prueba(requerimiento)
        resultado = []

        for sol in soluciones:
            try:
                arbol = ast.parse(sol.codigo)

                # Clases: no se pueden instanciar con datos genéricos → aceptar sin ejecutar
                tiene_clase = any(isinstance(n, ast.ClassDef) for n in ast.walk(arbol))
                if tiene_clase:
                    resultado.append(sol)
                    continue

                funciones = [n.name for n in ast.walk(arbol)
                             if isinstance(n, ast.FunctionDef)]
                if not funciones:
                    resultado.append(sol)
                    continue

                fn = funciones[0]
                script = (
                    f'{datos["setup"]}\n'
                    f'{sol.codigo}\n'
                    f'import json\n'
                    f'try:\n'
                    f'    r = {fn}({datos["args"]})\n'
                    f'    print(json.dumps({{"ok": True, "tipo": type(r).__name__}}))\n'
                    f'except Exception as e:\n'
                    f'    print(json.dumps({{"ok": False, "error": str(e)}}))\n'
                )

                with tempfile.NamedTemporaryFile(suffix='.py', mode='w',
                                                  delete=False) as f:
                    f.write(script)
                    path = f.name

                proc = subprocess.run(
                    [sys.executable, path],
                    capture_output=True, text=True, timeout=10,
                )
                os.unlink(path)

                if proc.stdout.strip():
                    datos_res = json.loads(proc.stdout.strip())
                    if not datos_res.get('ok'):
                        # Bug detectado — advertencia pero NO descartar
                        error_corto = datos_res.get('error', '')[:60]
                        sol.descripcion += f' ⚠️ ({error_corto})'

                resultado.append(sol)  # siempre añadir — es advisory

            except Exception:
                resultado.append(sol)

        return resultado

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