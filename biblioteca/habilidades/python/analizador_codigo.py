# biblioteca/habilidades/python/analizador_codigo.py — MÁXIMO FINAL
import ast, re, os
import httpx
from typing import Optional

_GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
_GROQ_URL     = 'https://api.groq.com/openai/v1/chat/completions'
_GROQ_MODEL   = 'openai/gpt-oss-120b'
_GROQ_TIMEOUT = 60
_TOKENS = {'simple': 500, 'normal': 1100, 'detallado': 1800}

_SYSTEM = '''Eres Bell — IA creada por Sebastian en Bucaramanga. Tienes la experiencia de un principal Python engineer con 15 años.

MI PROCESO MENTAL AL ANALIZAR CÓDIGO (úsalo exactamente así):

PASO 1 — MODELO MENTAL: Antes de mencionar ningún problema, leo el código completo y formo una imagen de qué intenta hacer. "Esta función conecta a una URL con reintentos automáticos".

PASO 2 — PRIORIZACIÓN DE FALLOS: Primero lo que rompe en producción, luego lo que crea bugs sutiles, luego lo estético.

PASO 3 — CAUSA Y EFECTO (no solo síntoma):
MAL:  "tiene bare_except"
BIEN: "El except: en línea 8 atrapa KeyboardInterrupt y SystemExit — si el usuario hace Ctrl+C mientras conecta, el programa lo ignora y sigue corriendo como zombie"

PASO 4 — FIX EN CÓDIGO REAL, no descripción del fix:
MAL:  "deberías usar except específico"
BIEN: `except (requests.RequestException, ValueError) as e:` — y por qué esas dos excepciones

PASO 5 — RECONOCER LO BUENO: El análisis equilibrado tiene más valor que solo criticar.

EJEMPLO DE RESPUESTA PERFECTA:
---
Oye Sebastian, esta función intenta conectarse con reintentos automáticos — la idea es correcta. Pero hay tres cosas que en producción te van a dar problemas.

El más peligroso es `headers={}` como valor por defecto. Python crea ese diccionario UNA vez cuando importa el módulo. Si alguien lo modifica dentro de la función, esa modificación persiste en todas las llamadas futuras — un bug que aparece aleatoriamente y es casi imposible de reproducir. El fix es `headers=None` y adentro: `if headers is None: headers = {}`.

El segundo es el `except:` sin tipo. Está silenciando absolutamente todo: errores de red, timeouts, y también `KeyboardInterrupt` y `SystemExit`. Si el usuario hace Ctrl+C, el programa lo ignora. Lo correcto: `except (requests.RequestException, ValueError) as e:`.

El tercero es `import requests` dentro del bucle. Python cachea imports así que no es problema de performance, pero es un antipatrón de legibilidad — los imports van al inicio del archivo siempre.

Lo que está bien: la lógica de reintentos con `range(retries)` es correcta y `return None` al final es honesto sobre el fallo.

```python
import requests
from typing import Optional

def conectar(url: str, headers: Optional[dict] = None, retries: int = 3) -> Optional[dict]:
    """Conecta a la URL con reintentos. Retorna None si todos fallan."""
    if headers is None:
        headers = {}
    for intento in range(retries):
        try:
            r = requests.get(url, headers=headers, timeout=10)
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            if intento == retries - 1:
                print(f"Falló después de {retries} intentos: {e}")
    return None
```
---

REGLAS ABSOLUTAS:
- Empiezas con "Oye Sebastian," DIRECTO al análisis — sin "lo que es una buena estrategia", "esta función es correcta"
- Párrafos cortos y densos — una idea por párrafo, no repitas
- PROHIBIDO al final: "esto haría el código más fácil de entender", "buena estructura", "es fácil de leer"
- PROHIBIDO: "lo cual es una buena práctica", "en general", "en resumen", "es importante"
- Código del fix: 4 espacios PEP 8, type hints, timeout donde aplica, raise_for_status() en requests
- "Lo que está bien": máximo 1-2 oraciones específicas y técnicas — nunca genéricas

EJEMPLO MAL (no hagas esto):
"Oye Sebastian, esta función intenta conectarse a una URL con reintentos automáticos, lo que es una buena estrategia para manejar errores de red."
→ Primera oración es relleno puro.

"La función `es_mayor` puede ser simplificada. La condición `if self.edad >= 18` puede ser directamente retornada."
→ Describe el fix sin explicar la causa.

EJEMPLO BIEN (así debes empezar):
"Oye Sebastian, tres problemas. El más peligroso: `headers={}` como default — ese dict existe desde que el módulo se importa. Si Bell reutiliza la sesión entre requests, headers de un usuario podrían filtrarse a otro."
→ Directo, causa específica, escenario de fallo real.

"El if-else en `es_mayor` es innecesario porque la condición ya es booleana: `return self.edad >= 18` hace lo mismo en una línea."
→ Explica POR QUÉ se puede simplificar, no solo que se puede.

REGLAS PARA CALIDAD DE ANÁLISIS:

CÓDIGO LIMPIO — Si el código es correcto para su propósito, di eso con 1-2 mejoras opcionales:
"Esta función es correcta. Para producción agrega type hints y un docstring de una línea."
NO inventes problemas donde no los hay.

SOBRE isinstance EN FUNCIONES UTILITARIAS:
NUNCA sugieras `isinstance` validation en funciones matemáticas o utilitarias simples.
Python usa duck typing intencionalmente: `suma(a, b)` funciona con int, float, Decimal, numpy arrays.
Agregar `isinstance` viola duck typing y es over-engineering. Solo sugerirlo cuando el contexto
REQUIERE validación estricta (APIs públicas, clases con invariantes).

EJEMPLO EXACTO — QUÉ DECIR PARA FUNCIÓN LIMPIA:

INPUT: `def multiplicar(a, b): return a * b`

RESPUESTA CORRECTA — MODELO EXACTO:
"Oye Sebastian, esta función es correcta — usa duck typing de Python correctamente, funciona con int, float, Decimal o cualquier tipo que soporte `*`. Para producción, agrega type hints y docstring:
```python
def multiplicar(a: int | float, b: int | float) -> int | float:
    """Multiplica dos números."""
    return a * b
```"

RESPUESTA INCORRECTA — NUNCA HAGAS ESTO:
"El más peligroso es la falta de validación. Agrega `if not isinstance(a, (int, float)): raise TypeError...`"
→ ESTO ES INCORRECTO. isinstance en utilidades matemáticas es over-engineering que viola duck typing.

HECHOS TÉCNICOS Y PATRONES QUE DEBES DETECTAR:

Flask: SÍNCRONO. GIL: libera para I/O. isinstance en utilitarios: viola duck typing.
copy.copy de listas anidadas: comparte sublistas. deepcopy: las duplica.

BUGS REALES QUE DEBES DETECTAR EN ANÁLISIS:

1. CONTEXT MANAGER ROTO:
   `return self.queue.get()` cuando se espera `with pool.acquire() as conn:` → no es context manager
   Fix: usar @contextmanager con yield

2. EXCEPCIÓN USADA ANTES DE DEFINIRSE:
   `raise PoolTimeoutError(...)` sin definir PoolTimeoutError → NameError en runtime
   Fix: definir la clase antes de usarla

3. STATS CALCULADOS DEL ESTADO (no contadores reales):
   `hits = sum(1 for ... if count > 1)` → incorrecto, no trackea hits reales
   Fix: self._hits += 1 en cada get() exitoso

4. BACKOFF SIN JITTER:
   `time.sleep(2 ** intento)` en código concurrente → thundering herd
   Fix: `time.sleep(2 ** intento + random.uniform(0, 1))`

5. WEAKREF DE MÉTODO BOUND:
   `weakref.ref(self.metodo)` → garbage-collected inmediatamente
   Fix: `weakref.WeakMethod(self.metodo)`

6. GLOB IMPLEMENTADO CON REGEX:
   `re.match("evento.*", nombre)` para patrones glob → `.` en regex ≠ `.` literal
   Fix: `fnmatch.fnmatch(nombre, "evento.*")`

7. FLUENT INTERFACE QUE MUTA EL ORIGINAL:
   `self.campos.append(x); return self` → encadenar modifica el objeto base
   Fix: `nuevo = copy.copy(self); nuevo.campos = [*self.campos, x]; return nuevo`

8. TIEMPO TOTAL NO MEDIDO:
   `tiempo_total = 0` sin actualizar → siempre retorna 0
   Fix: `inicio = time.perf_counter()` antes del try, acumular al final

9. EXCEPCIÓN EN CALLBACK DETIENE OTROS:
   Thread con callback sin try/except → una excepción mata el thread silenciosamente
   Fix: envolver cada callback en try/except con logging del error

NUNCA uses "En resumen". NUNCA cuentes líneas como métrica.'''


class AnalizadorCodigo:

    def analizar(self, codigo: str, verbosidad: str = 'normal') -> dict:
        if not codigo or not codigo.strip():
            return {'exitoso': False, 'resumen': 'No hay código para analizar.'}
        ast_data      = self._analizar_ast(codigo)
        radon_data    = self._analizar_radon(codigo)
        pyflakes_data = self._analizar_pyflakes(codigo)
        respuesta     = self._groq_analizar(codigo, ast_data, radon_data, pyflakes_data, verbosidad)
        if respuesta:
            return {'exitoso': True, 'respuesta': respuesta}
        return {'exitoso': True, 'respuesta': self._basico(ast_data, radon_data, pyflakes_data)}

    def _analizar_ast(self, codigo: str) -> dict:
        try:
            tree = ast.parse(codigo)
        except SyntaxError as e:
            ls = codigo.split('\n')
            lt = ls[e.lineno-1].strip() if e.lineno and e.lineno <= len(ls) else ''
            return {'error_sintaxis': True, 'linea': e.lineno, 'mensaje': str(e.msg), 'linea_codigo': lt}

        lineas    = codigo.strip().split('\n')
        funciones = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
        clases    = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
        imports   = [n for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))]

        anti = []
        for f in funciones:
            for n in ast.walk(f):
                if isinstance(n, ast.ExceptHandler) and n.type is None:
                    anti.append({'tipo': 'bare_except',   'funcion': f.name, 'linea': getattr(n,'lineno','?'), 'gravedad': 'alta'})
            for d in f.args.defaults:
                if isinstance(d, (ast.List, ast.Dict, ast.Set)):
                    anti.append({'tipo': 'mutable_default', 'funcion': f.name, 'linea': f.lineno, 'gravedad': 'critica'})
            sin_doc = not (f.body and isinstance(f.body[0], ast.Expr) and
                           isinstance(f.body[0].value, ast.Constant) and
                           isinstance(f.body[0].value.value, str))
            if sin_doc:
                anti.append({'tipo': 'sin_docstring', 'funcion': f.name, 'linea': f.lineno, 'gravedad': 'baja'})
            hints = f.returns or any(a.annotation for a in f.args.args if a.arg != 'self')
            if not hints and f.name not in ('__init__','__repr__','__str__','main'):
                anti.append({'tipo': 'sin_type_hints', 'funcion': f.name, 'linea': f.lineno, 'gravedad': 'baja'})

        info_f = []
        for f in funciones:
            lf = (getattr(f,'end_lineno',f.lineno) or f.lineno) - f.lineno + 1
            pr = [a.arg for a in f.args.args if a.arg != 'self']
            info_f.append({'nombre': f.name, 'linea': f.lineno, 'lineas': lf, 'params': pr,
                            'n_params': len(pr), 'es_async': isinstance(f, ast.AsyncFunctionDef),
                            'retorna': ast.unparse(f.returns) if f.returns else None})

        info_c = []
        for c in clases:
            mt = [n.name for n in ast.walk(c) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))]
            hr = [ast.unparse(b) for b in c.bases] if c.bases else []
            nl = (getattr(c,'end_lineno',c.lineno) or c.lineno) - c.lineno + 1
            info_c.append({'nombre': c.name, 'linea': c.lineno, 'metodos': mt, 'hereda': hr, 'lineas': nl})

        libs = []
        for i in imports:
            if isinstance(i, ast.Import): libs.extend(a.name.split('.')[0] for a in i.names)
            elif isinstance(i, ast.ImportFrom) and i.module: libs.append(i.module.split('.')[0])

        return {
            'error_sintaxis': False, 'lineas_totales': len(lineas),
            'funciones': info_f, 'clases': info_c,
            'librerias': list(dict.fromkeys(libs)), 'antipatrones': anti,
            'funcs_largas': [f for f in info_f if f['lineas'] > 30],
            'muchos_params': [f for f in info_f if f['n_params'] > 5],
        }

    def _analizar_radon(self, codigo: str) -> dict:
        try:
            from radon.complexity import cc_visit
            from radon.raw        import analyze
            from radon.metrics    import mi_visit
            cc  = cc_visit(codigo)
            raw = analyze(codigo)
            fc  = []
            for r in cc:
                n = ('simple' if r.complexity<=4 else 'moderado' if r.complexity<=7
                     else 'alto' if r.complexity<=12 else 'muy_alto')
                fc.append({'nombre': r.name, 'complejidad': r.complexity, 'nivel': n, 'linea': r.lineno})
            try:    mi = round(mi_visit(codigo, multi=True), 1)
            except: mi = None
            return {'disponible': True,
                    'funciones_cc': sorted(fc, key=lambda x: x['complejidad'], reverse=True),
                    'loc': raw.loc, 'lloc': raw.lloc, 'comentarios': raw.comments,
                    'maintainability': mi, 'max_cc': max((f['complejidad'] for f in fc), default=0)}
        except Exception as e:
            return {'disponible': False, 'error': str(e)}

    def _analizar_pyflakes(self, codigo: str) -> dict:
        try:
            from pyflakes import api as pf
            class Rep:
                def __init__(self): self.msgs = []
                def unexpectedError(self, f, m): self.msgs.append(f'Error: {m}')
                def syntaxError(self, f, m, l, o, t): self.msgs.append(f'Sintaxis {l}: {m}')
                def flake(self, msg): self.msgs.append(str(msg))
            rep = Rep(); pf.check(codigo, '<codigo>', reporter=rep)
            bugs = []
            for m in rep.msgs:
                if   'imported but unused' in m: bugs.append({'tipo':'import_muerto',   'msg':m,'grav':'media'})
                elif 'undefined name'       in m: bugs.append({'tipo':'var_indefinida', 'msg':m,'grav':'alta'})
                elif 'redefinition'         in m: bugs.append({'tipo':'redefinicion',    'msg':m,'grav':'media'})
                elif 'referenced before'    in m: bugs.append({'tipo':'uso_sin_asignar','msg':m,'grav':'critica'})
                else:                             bugs.append({'tipo':'otro',            'msg':m,'grav':'baja'})
            return {'disponible': True, 'bugs': bugs, 'total': len(bugs)}
        except Exception as e:
            return {'disponible': False, 'error': str(e)}

    def _groq_analizar(self, codigo, ad, rd, pd, verbosidad) -> Optional[str]:
        if not _GROQ_API_KEY: return None
        if ad.get('error_sintaxis'):
            return self._groq_sintaxis(ad, codigo)
        m = self._metricas(ad, rd, pd)
        n = _TOKENS.get(verbosidad, 2500)
        inst = {
            'simple':    'Análisis conciso: 100-150 palabras. Qué hace + el problema más importante con su fix.',
            'normal':    'Análisis completo: 400-700 palabras. Modelo mental → problemas con causa-efecto → código del fix → qué está bien. Completa TODAS las ideas.',
            'detallado': 'Análisis exhaustivo: 800-1200 palabras. Arquitectura → cada problema crítico/alto con escenario de fallo y código del fix → mantenibilidad y testability → lo bien hecho. Sin recortes.',
        }.get(verbosidad, '')
        try:
            r = httpx.post(_GROQ_URL,
                headers={'Authorization': f'Bearer {_GROQ_API_KEY}', 'Content-Type': 'application/json'},
                json={'model': _GROQ_MODEL, 'messages': [
                    {'role': 'system', 'content': _SYSTEM},
                    {'role': 'user', 'content': (
                        f'{inst}\n\n'
                        f'DATOS REALES (razona sobre ellos, no los repitas):\n{m}\n\n'
                        f'CÓDIGO:\n```python\n{codigo[:6000]}\n```'
                    )}],
                    'temperature': 0.3, 'max_tokens': n},
                timeout=_GROQ_TIMEOUT)
            if r.status_code == 200:
                resp = r.json()['choices'][0]['message']['content'].strip()
                if resp and len(resp) > 30: return resp
        except Exception as e:
            print(f'  [Analizador] {e}')
        return None

    def _groq_sintaxis(self, ad, codigo) -> Optional[str]:
        if not _GROQ_API_KEY: return None
        try:
            r = httpx.post(_GROQ_URL,
                headers={'Authorization': f'Bearer {_GROQ_API_KEY}', 'Content-Type': 'application/json'},
                json={'model': _GROQ_MODEL, 'messages': [
                    {'role': 'system', 'content': _SYSTEM},
                    {'role': 'user', 'content': (
                        f'Error de sintaxis en línea {ad.get("linea","?")}.\n'
                        f'Error: {ad.get("mensaje","")}\n'
                        f'Línea: `{ad.get("linea_codigo","")}`\n\n'
                        f'Código:\n```python\n{codigo[:3000]}\n```\n\n'
                        f'Explica qué está mal y muestra el código corregido. 150-200 palabras.'
                    )}],
                    'temperature': 0.2, 'max_tokens': 600},
                timeout=_GROQ_TIMEOUT)
            if r.status_code == 200:
                return r.json()['choices'][0]['message']['content'].strip()
        except: pass
        return (f'Oye Sebastian, error de sintaxis en línea {ad.get("linea","?")}: '
                f'{ad.get("mensaje","sintaxis inválida")}.')

    def _metricas(self, ad, rd, pd) -> str:
        p = [f'Líneas: {ad.get("lineas_totales","?")}']
        funcs = ad.get('funciones',[])
        if funcs:
            p.append('Funciones: ' + ', '.join(
                f'{f["nombre"]}({f["n_params"]}p,{f["lineas"]}L{"[async]" if f["es_async"] else ""}{"→"+f["retorna"] if f["retorna"] else ""})'
                for f in funcs[:10]))
        clases = ad.get('clases',[])
        if clases:
            p.append('Clases: ' + ', '.join(f'{c["nombre"]}({len(c["metodos"])}m,{c["lineas"]}L)' for c in clases))
        libs = ad.get('librerias',[])
        if libs: p.append(f'Imports: {", ".join(libs[:10])}')
        anti = ad.get('antipatrones',[])
        for g in ['critica','alta','media']:
            gr = [a for a in anti if a['gravedad']==g]
            if gr: p.append(f'{g.upper()}: ' + '; '.join(f'{a["tipo"]} en {a["funcion"]}() L{a["linea"]}' for a in gr))
        fl = ad.get('funcs_largas',[])
        if fl: p.append('Largas: ' + ', '.join(f'{f["nombre"]}({f["lineas"]}L)' for f in fl))
        mp = ad.get('muchos_params',[])
        if mp: p.append('Muchos params: ' + ', '.join(f'{f["nombre"]}({f["n_params"]})' for f in mp))
        if rd.get('disponible'):
            cc = [f for f in rd['funciones_cc'] if f['complejidad']>4]
            if cc: p.append('CC: ' + ', '.join(f'{f["nombre"]}={f["complejidad"]}({f["nivel"]})' for f in cc[:6]))
            mi = rd.get('maintainability')
            if mi is not None:
                p.append(f'Mantenibilidad: {mi}/100 ({"alta" if mi>=20 else "media" if mi>=10 else "baja"})')
        if pd.get('disponible') and pd.get('bugs'):
            g = [b for b in pd['bugs'] if b['grav'] in ('critica','alta')]
            if g: p.append('Bugs: ' + '; '.join(b['msg'] for b in g[:4]))
            ts = {}
            for b in pd['bugs']: ts[b['tipo']] = ts.get(b['tipo'],0)+1
            if ts: p.append('pyflakes: ' + ', '.join(f'{t}×{n}' for t,n in ts.items()))
        return '\n'.join(p)

    def _basico(self, ad, rd, pd) -> str:
        if ad.get('error_sintaxis'):
            return f'Error de sintaxis en línea {ad["linea"]}: {ad["mensaje"]}.'
        p = []
        f = ad.get('funciones',[])
        if f: p.append(f'{len(f)} función(es): ' + ', '.join(f'`{x["nombre"]}()`' for x in f[:5]))
        g = [a for a in ad.get('antipatrones',[]) if a['gravedad'] in ('critica','alta')]
        if g: p.append('Problemas: ' + ', '.join(f'{a["tipo"]} en `{a["funcion"]}()`' for a in g[:4]))
        if rd.get('disponible'):
            cc = [x for x in rd.get('funciones_cc',[]) if x['complejidad']>7]
            if cc: p.append('Alta CC: ' + ', '.join(f'`{x["nombre"]}` CC={x["complejidad"]}' for x in cc))
        if pd.get('bugs'): p.append(f'{pd["total"]} problema(s) pyflakes.')
        return ' '.join(p) if p else 'El código se ve limpio.'

    def construir_respuesta(self, analisis, verbosidad='normal'):
        return analisis.get('respuesta', analisis.get('resumen', 'Sin análisis.'))