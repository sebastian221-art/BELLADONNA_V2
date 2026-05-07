"""
test_python.py — Evaluación completa Habilidad Python de Bell
Corre con: python test_python.py
Prueba los 5 modos + verbosidad + casos edge
"""
import os
os.environ['BELL_DEBUG'] = '0'
import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()

from interfaz.api.chat import _procesar_mensaje

OK   = '\033[92m✓\033[0m'
WARN = '\033[93m?\033[0m'
FAIL = '\033[91m✗\033[0m'
BOLD = '\033[1m'
CYAN = '\033[96m'

resultados = {'ok': 0, 'warn': 0, 'fail': 0}
issues = []

def preguntar(msg):
    r = _procesar_mensaje(msg)
    return r.get('respuesta', '').strip()

def evaluar(categoria, preguntas):
    print(f'\n{CYAN}{"="*64}\033[0m')
    print(f'{BOLD}  {categoria}\033[0m')
    print(f'{CYAN}{"="*64}\033[0m')

    for item in preguntas:
        p    = item['p']
        debe = item.get('debe', [])
        no   = item.get('no_debe', [])
        cualq = item.get('debe_cualquiera', [])
        nota  = item.get('nota', '')

        resp  = preguntar(p)
        rl    = resp.lower()

        fallo = False
        razon = ''
        for nd in no:
            if nd.lower() in rl:
                idx = rl.find(nd.lower())
                ctx = rl[max(0, idx-10):idx]
                if not any(neg in ctx for neg in ['no ', 'nunca ', 'sin ']):
                    fallo = True
                    razon = nd
                    break

        falta_debe   = [d for d in debe if d.lower() not in rl]
        falta_cualq  = bool(cualq) and not any(d.lower() in rl for d in cualq)
        largo_minimo = item.get('largo_minimo', 0)
        muy_corta    = len(resp) < largo_minimo

        if fallo:
            icono = FAIL
            resultados['fail'] += 1
            estado = f'CONTIENE: "{razon}"'
            issues.append(f'FAIL [{p[:50]}] → {estado}')
        elif falta_debe or falta_cualq or muy_corta:
            icono = WARN
            resultados['warn'] += 1
            if falta_debe:
                estado = f'FALTA: {falta_debe}'
            elif falta_cualq:
                estado = f'FALTA alguno de: {cualq}'
            else:
                estado = f'RESPUESTA MUY CORTA ({len(resp)} chars, mínimo {largo_minimo})'
            issues.append(f'WARN [{p[:50]}] → {estado}')
        else:
            icono = OK
            resultados['ok'] += 1
            estado = ''

        print(f'\n{icono} [{p[:70]}]')
        print(f'   Bell: "{resp[:160]}"')
        if estado:
            print(f'   /!\\ {estado}')
        if nota:
            print(f'   [?] {nota}')

# ══════════════════════════════════════════════════════════════
# MODO 1: EXPLICACIÓN TÉCNICA
# ══════════════════════════════════════════════════════════════
evaluar('1. EXPLICACIÓN TÉCNICA — Bell habla como persona', [
    {
        'p': 'cómo funciona async await en python',
        'debe_cualquiera': ['async', 'await', 'asyncio'],
        'largo_minimo': 80,
        'no_debe': ['todavía no tengo', 'está en construcción'],
        'nota': 'Debe explicar async/await en lenguaje humano con ejemplo'
    },
    {
        'p': 'qué es un decorador en python',
        'debe_cualquiera': ['decorador', 'función', 'envuelve', 'wraps'],
        'largo_minimo': 80,
        'no_debe': ['todavía no tengo', 'está en construcción'],
        'nota': 'Debe explicar decoradores con ejemplo concreto'
    },
    {
        'p': 'cómo hago un bucle for en python',
        'debe_cualquiera': ['for', 'range', 'lista', 'iterar', 'in '],
        'largo_minimo': 60,
        'no_debe': ['todavía no tengo', 'está en construcción'],
        'nota': 'Debe dar ejemplo de bucle for'
    },
    {
        'p': 'qué es venv y cómo lo creo',
        'debe_cualquiera': ['venv', 'virtualenv', 'entorno', 'python -m'],
        'largo_minimo': 60,
        'no_debe': ['todavía no tengo', 'está en construcción'],
        'nota': 'Debe explicar entorno virtual con comando'
    },
    {
        'p': 'qué son los generadores y el yield',
        'debe_cualquiera': ['yield', 'generador', 'produce', 'memoria'],
        'largo_minimo': 60,
        'no_debe': ['todavía no tengo', 'está en construcción'],
        'nota': 'Debe explicar yield/generadores'
    },
    {
        'p': 'qué es flask y cómo funciona',
        'debe_cualquiera': ['flask', 'web', 'route', 'app.route', 'framework'],
        'largo_minimo': 60,
        'no_debe': ['todavía no tengo', 'está en construcción'],
        'nota': 'Debe explicar Flask con ejemplo básico'
    },
    {
        'p': 'cómo hago commit en git',
        'debe_cualquiera': ['git commit', 'git add', 'commit', 'push'],
        'largo_minimo': 50,
        'no_debe': ['todavía no tengo', 'está en construcción'],
        'nota': 'Debe dar los comandos de git'
    },
])

# ══════════════════════════════════════════════════════════════
# MODO 2: ANÁLISIS DE CÓDIGO
# ══════════════════════════════════════════════════════════════
evaluar('2. ANÁLISIS DE CÓDIGO — Bell lee y diagnostica', [
    {
        'p': 'analiza este código:\ndef dividir(a, b):\n    try:\n        return a / b\n    except:\n        return None',
        'debe_cualquiera': ['except', 'bare', 'tipo', 'Exception', 'docstring'],
        'largo_minimo': 80,
        'no_debe': ['todavía no tengo', 'no pude analizar', 'dímelo de otra forma'],
        'nota': 'Debe detectar bare except y falta de docstring'
    },
    {
        'p': 'qué hace este código:\n```python\ndef saludar(nombre: str) -> str:\n    """Saluda a la persona."""\n    return f"Hola, {nombre}!"\n```',
        'debe_cualquiera': ['saluda', 'nombre', 'retorna', 'función', 'devuelve'],
        'largo_minimo': 40,
        'no_debe': ['todavía no tengo', 'no pude analizar'],
        'nota': 'Debe describir qué hace la función en lenguaje natural'
    },
    {
        'p': 'revisa este código y dime qué tiene mal:\ndef procesar(lista=[]):\n    lista.append(1)\n    return lista',
        'debe_cualquiera': ['mutable', 'default', 'lista', 'problema', 'bug', 'argumento'],
        'largo_minimo': 60,
        'no_debe': ['todavía no tengo', 'no pude analizar'],
        'nota': 'Debe detectar el bug de argumento mutable por defecto'
    },
    {
        'p': 'analiza este código:\n```python\nimport os\nimport json\n\ndef leer_config(ruta):\n    with open(ruta) as f:\n        return json.load(f)\n```',
        'debe_cualquiera': ['json', 'archivo', 'config', 'abre', 'lee', 'retorna'],
        'largo_minimo': 40,
        'no_debe': ['todavía no tengo', 'no pude analizar'],
        'nota': 'Debe describir qué hace el código'
    },
])

# ══════════════════════════════════════════════════════════════
# MODO 3: GENERACIÓN DE CÓDIGO
# ══════════════════════════════════════════════════════════════
evaluar('3. GENERACIÓN DE CÓDIGO — Bell crea desde descripción', [
    {
        'p': 'crea una función en python que reciba una lista de números y retorne el promedio',
        'debe_cualquiera': ['def ', 'return', 'sum(', 'len(', 'promedio'],
        'largo_minimo': 60,
        'no_debe': ['todavía no tengo', 'está en construcción'],
        'nota': 'Debe generar código real de función promedio'
    },
    {
        'p': 'hazme un endpoint de Flask que reciba datos por POST y retorne JSON',
        'debe_cualquiera': ['@app.route', 'POST', 'jsonify', 'request', 'flask'],
        'largo_minimo': 80,
        'no_debe': ['todavía no tengo', 'está en construcción'],
        'nota': 'Debe generar endpoint Flask con POST'
    },
    {
        'p': 'escribe el código para leer un archivo JSON en python',
        'debe_cualquiera': ['json', 'open', 'load', 'def '],
        'largo_minimo': 50,
        'no_debe': ['todavía no tengo', 'está en construcción'],
        'nota': 'Debe generar función para leer JSON'
    },
    {
        'p': 'crea una clase Python que represente un usuario con nombre y edad',
        'debe_cualquiera': ['class', '__init__', 'self', 'nombre', 'edad'],
        'largo_minimo': 60,
        'no_debe': ['todavía no tengo', 'está en construcción'],
        'nota': 'Debe generar clase con constructor'
    },
])

# ══════════════════════════════════════════════════════════════
# MODO 4: DEBUG DE ERRORES
# ══════════════════════════════════════════════════════════════
evaluar('4. DEBUG — Bell diagnostica errores', [
    {
        'p': 'tengo este error: ModuleNotFoundError: No module named flask',
        'debe_cualquiera': ['pip install', 'venv', 'instala', 'módulo', 'flask'],
        'largo_minimo': 60,
        'no_debe': ['todavía no tengo', 'está en construcción'],
        'nota': 'Debe diagnosticar el error de importación y dar solución'
    },
    {
        'p': 'me sale este error: TypeError: unsupported operand type(s) for +: int and str',
        'debe_cualquiera': ['tipo', 'int', 'str', 'cadena', 'número', 'convertir', 'type'],
        'largo_minimo': 60,
        'no_debe': ['todavía no tengo', 'está en construcción'],
        'nota': 'Debe diagnosticar el TypeError int + str'
    },
    {
        'p': 'me aparece: KeyError: username al acceder al diccionario',
        'debe_cualquiera': ['clave', 'diccionario', '.get(', 'username', 'existe', 'key'],
        'largo_minimo': 50,
        'no_debe': ['todavía no tengo', 'está en construcción'],
        'nota': 'Debe explicar KeyError y sugerir .get()'
    },
    {
        'p': 'tengo un error de importación: cannot import name MotorPython from biblioteca.habilidades.python',
        'debe_cualquiera': ['importación', 'import', 'módulo', 'ruta', 'archivo', 'existe'],
        'largo_minimo': 50,
        'no_debe': ['todavía no tengo', 'está en construcción'],
        'nota': 'Debe diagnosticar error de import con ruta'
    },
    {
        'p': 'me sale IndentationError: unexpected indent en la línea 5',
        'debe_cualquiera': ['indentación', 'tab', 'espacio', 'línea', 'sangría'],
        'largo_minimo': 40,
        'no_debe': ['todavía no tengo', 'está en construcción'],
        'nota': 'Debe explicar el IndentationError'
    },
])

# ══════════════════════════════════════════════════════════════
# MODO 5: AUTO-ANÁLISIS
# ══════════════════════════════════════════════════════════════
evaluar('5. AUTO-ANÁLISIS — Bell se analiza a sí misma', [
    {
        'p': 'analiza tu generador_groq',
        'debe_cualquiera': ['generador', 'groq', 'línea', 'clase', 'función', 'archivo'],
        'largo_minimo': 60,
        'no_debe': ['no encontré', 'todavía no tengo', 'cuéntame un poco más'],
        'nota': 'Debe leer y analizar su propio generador_groq.py'
    },
    {
        'p': 'analiza tu constructor_decision',
        'debe_cualquiera': ['constructor', 'decisión', 'línea', 'función', 'archivo', 'decision'],
        'largo_minimo': 60,
        'no_debe': ['no encontré', 'todavía no tengo', 'cuéntame un poco más'],
        'nota': 'Debe analizar su constructor_decision.py'
    },
    {
        'p': 'analiza tu capa6',
        'debe_cualquiera': ['capa', 'archivo', 'función', 'línea', 'código'],
        'largo_minimo': 50,
        'no_debe': ['no encontré', 'todavía no tengo'],
        'nota': 'Debe analizar archivos de capa6'
    },
    {
        'p': 'qué puedes mejorar de tu propio código',
        'debe_cualquiera': ['código', 'mejorar', 'archivo', 'propio', 'mejora'],
        'largo_minimo': 50,
        'no_debe': ['todavía no tengo', 'está en construcción'],
        'nota': 'Debe hacer auto-reflexión sobre su código'
    },
])

# ══════════════════════════════════════════════════════════════
# MODO 6: VERBOSIDAD — Bell ajusta el nivel de detalle
# ══════════════════════════════════════════════════════════════
evaluar('6. VERBOSIDAD — Bell ajusta según lo pedido', [
    {
        'p': 'qué es async await, explícamelo más simple',
        'debe_cualquiera': ['async', 'await', 'pausa', 'espera'],
        'largo_minimo': 20,
        'no_debe': ['todavía no tengo', 'está en construcción'],
        'nota': 'Modo simple: respuesta corta sin código'
    },
    {
        'p': 'qué es un decorador, explícamelo en detalle con todo',
        'debe_cualquiera': ['decorador', 'wraps', 'función', 'functools'],
        'largo_minimo': 150,
        'no_debe': ['todavía no tengo', 'está en construcción'],
        'nota': 'Modo detallado: respuesta larga con ejemplos completos'
    },
    {
        'p': 'analiza este código brevemente:\ndef hola():\n    print("hola")',
        'debe_cualquiera': ['hola', 'función', 'imprime', 'print'],
        'largo_minimo': 20,
        'no_debe': ['todavía no tengo', 'no pude analizar'],
        'nota': 'Análisis breve solicitado explícitamente'
    },
    {
        'p': 'explícame venv de forma simple y corta',
        'debe_cualquiera': ['venv', 'virtual', 'entorno', 'paquete'],
        'largo_minimo': 20,
        'no_debe': ['todavía no tengo', 'está en construcción'],
        'nota': 'Modo simple: debe ser conciso'
    },
])

# ══════════════════════════════════════════════════════════════
# MODO 7: LENGUAJE HUMANO — No suena como máquina
# ══════════════════════════════════════════════════════════════
evaluar('7. HUMANIDAD — Bell habla como persona, no como manual', [
    {
        'p': 'cómo funciona async',
        'no_debe': ['todavía no tengo esa capacidad', 'está en construcción', 'lista sebastian'],
        'largo_minimo': 50,
        'nota': 'No debe responder como si no tuviera la habilidad'
    },
    {
        'p': 'explícame los type hints de python',
        'debe_cualquiera': ['type', 'tipo', 'hint', 'int', 'str', 'anotación', 'anotacion'],
        'largo_minimo': 50,
        'no_debe': ['todavía no tengo', 'está en construcción'],
        'nota': 'Debe explicar type hints naturalmente'
    },
    {
        'p': 'qué es un context manager',
        'debe_cualquiera': ['with', 'context', 'cierra', 'recurso', 'finally', 'gestor'],
        'largo_minimo': 50,
        'no_debe': ['todavía no tengo', 'está en construcción'],
        'nota': 'Debe explicar context manager'
    },
    {
        'p': 'explícame cómo funciona git',
        'debe_cualquiera': ['commit', 'git', 'repositorio', 'cambios', 'push'],
        'largo_minimo': 50,
        'no_debe': ['todavía no tengo', 'está en construcción'],
        'nota': 'Debe explicar git naturalmente'
    },
])

# ══════════════════════════════════════════════════════════════
# RESUMEN
# ══════════════════════════════════════════════════════════════
total = resultados['ok'] + resultados['warn'] + resultados['fail']
score = (resultados['ok'] / total * 100) if total else 0

print(f'\n{CYAN}{"="*64}\033[0m')
print(f'{BOLD}  RESUMEN — HABILIDAD PYTHON\033[0m')
print(f'{CYAN}{"="*64}\033[0m')
print(f'  {OK}  Correctas:    {resultados["ok"]:3d}')
print(f'  {WARN}  Advertencias: {resultados["warn"]:3d}')
print(f'  {FAIL}  Fallos:       {resultados["fail"]:3d}')
print(f'     Total:        {total:3d}')
print()

bar_ok   = int((resultados['ok']   / total) * 40) if total else 0
bar_warn = int((resultados['warn'] / total) * 40) if total else 0
bar_fail = int((resultados['fail'] / total) * 40) if total else 0
barra = (
    '\033[92m' + chr(9608) * bar_ok   + '\033[0m' +
    '\033[93m' + chr(9618) * bar_warn + '\033[0m' +
    '\033[91m' + chr(9617) * bar_fail + '\033[0m'
)
print(f'  [{barra}]  {BOLD}{score:.1f}%\033[0m')
print()

if score >= 90:
    nivel = 'EXCELENTE — Habilidad Python completa'
elif score >= 75:
    nivel = 'BUENO — Funciona bien, detalles menores'
elif score >= 60:
    nivel = 'ACEPTABLE — Áreas a mejorar'
else:
    nivel = 'NECESITA TRABAJO'

print(f'  NIVEL: {nivel}')

if issues:
    print(f'\n{BOLD}  ISSUES:{RESET if False else chr(27)+"[0m"}')
    for i in issues:
        icono = FAIL if i.startswith('FAIL') else WARN
        print(f'  {icono} {i[5:]}')

print(f'{CYAN}{"="*64}\033[0m\n')