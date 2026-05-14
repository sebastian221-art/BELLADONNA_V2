"""
test_bell.py — Evaluación COMPLETA de Bell
Habilidad Python + Habilidad Lenguaje + Personalidad

Corre con: python test_bell.py
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
RESET = '\033[0m'
MAGENTA = '\033[95m'

resultados_python   = {'ok': 0, 'warn': 0, 'fail': 0}
resultados_lenguaje = {'ok': 0, 'warn': 0, 'fail': 0}
issues = []

def preguntar(msg):
    r = _procesar_mensaje(msg)
    return r.get('respuesta', '').strip()

def evaluar(categoria, preguntas, bucket):
    print(f'\n{CYAN}{"="*64}{RESET}')
    print(f'{BOLD}  {categoria}{RESET}')
    print(f'{CYAN}{"="*64}{RESET}')

    for item in preguntas:
        p      = item['p']
        debe   = item.get('debe', [])
        no     = item.get('no_debe', [])
        cualq  = item.get('debe_cualquiera', [])
        nota   = item.get('nota', '')

        resp = preguntar(p)
        rl   = resp.lower()

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

        falta_debe  = [d for d in debe if d.lower() not in rl]
        falta_cualq = bool(cualq) and not any(d.lower() in rl for d in cualq)
        largo_min   = item.get('largo_minimo', 0)
        muy_corta   = len(resp) < largo_min
        largo_max   = item.get('largo_maximo', 99999)
        muy_larga   = len(resp) > largo_max

        if fallo:
            icono = FAIL
            bucket['fail'] += 1
            estado = f'CONTIENE PROHIBIDO: "{razon}"'
            issues.append(f'FAIL [{p[:50]}] → {estado}')
        elif falta_debe or falta_cualq or muy_corta or muy_larga:
            icono = WARN
            bucket['warn'] += 1
            if falta_debe:
                estado = f'FALTA: {falta_debe}'
            elif falta_cualq:
                estado = f'FALTA alguno de: {cualq}'
            elif muy_corta:
                estado = f'MUY CORTA ({len(resp)} chars, mín {largo_min})'
            else:
                estado = f'MUY LARGA ({len(resp)} chars, máx {largo_max})'
            issues.append(f'WARN [{p[:50]}] → {estado}')
        else:
            icono = OK
            bucket['ok'] += 1
            estado = ''

        print(f'\n{icono} [{p[:70]}]')
        print(f'   Bell: "{resp[:180]}"')
        if estado:
            print(f'   /!\\ {estado}')
        if nota:
            print(f'   [?] {nota}')

# ══════════════════════════════════════════════════════════════
# ██  HABILIDAD PYTHON
# ══════════════════════════════════════════════════════════════
print(f'\n{MAGENTA}{"█"*64}{RESET}')
print(f'{BOLD}  HABILIDAD PYTHON{RESET}')
print(f'{MAGENTA}{"█"*64}{RESET}')

evaluar('1. EXPLICACIÓN TÉCNICA', [
    {
        'p': 'cómo funciona async await en python',
        'debe_cualquiera': ['async', 'await', 'asyncio'],
        'largo_minimo': 80,
        'no_debe': ['todavía no tengo', 'está en construcción'],
        'nota': 'Debe explicar async/await con ejemplo'
    },
    {
        'p': 'qué es un decorador en python',
        'debe_cualquiera': ['decorador', 'función', 'envuelve', 'wraps'],
        'largo_minimo': 80,
        'no_debe': ['todavía no tengo', 'está en construcción'],
    },
    {
        'p': 'qué son los generadores y el yield',
        'debe_cualquiera': ['yield', 'generador', 'produce', 'memoria'],
        'largo_minimo': 60,
        'no_debe': ['todavía no tengo'],
    },
    {
        'p': 'qué es flask y cómo funciona',
        'debe_cualquiera': ['flask', 'route', 'app.route', 'framework', 'web'],
        'largo_minimo': 60,
        'no_debe': ['todavía no tengo'],
    },
    {
        'p': 'qué es un context manager',
        'debe_cualquiera': ['with', 'context', 'cierra', 'recurso', 'finally', 'gestor'],
        'largo_minimo': 50,
        'no_debe': ['todavía no tengo'],
    },
], resultados_python)

evaluar('2. GENERACIÓN DE CÓDIGO', [
    {
        'p': 'crea una función en python que reciba una lista de números y retorne el promedio',
        'debe_cualquiera': ['def ', 'return', 'sum(', 'len('],
        'largo_minimo': 60,
        'no_debe': ['todavía no tengo'],
    },
    {
        'p': 'hazme un endpoint Flask que reciba datos por POST y retorne JSON',
        'debe_cualquiera': ['@app.route', 'POST', 'jsonify', 'request'],
        'largo_minimo': 80,
        'no_debe': ['todavía no tengo'],
    },
    {
        'p': 'crea una clase Python que represente un usuario con nombre y edad',
        'debe_cualquiera': ['class', '__init__', 'self', 'nombre', 'edad'],
        'largo_minimo': 60,
        'no_debe': ['todavía no tengo'],
    },
    {
        'p': 'crea un sistema de caché en Python con TTL y LRU',
        'debe_cualquiera': ['class', 'def ', 'OrderedDict', 'Lock', 'ttl', 'TTL', 'lru', 'LRU'],
        'largo_minimo': 200,
        'no_debe': ['todavía no tengo'],
        'nota': 'Spec compleja — debe implementar la clase completa'
    },
], resultados_python)

evaluar('3. DEBUG DE ERRORES', [
    {
        'p': 'tengo este error: ModuleNotFoundError: No module named flask',
        'debe_cualquiera': ['pip install', 'instala', 'módulo', 'flask'],
        'largo_minimo': 50,
        'no_debe': ['todavía no tengo'],
    },
    {
        'p': 'me sale: TypeError: unsupported operand type(s) for +: int and str',
        'debe_cualquiera': ['tipo', 'int', 'str', 'convertir', 'type'],
        'largo_minimo': 50,
        'no_debe': ['todavía no tengo'],
    },
    {
        'p': 'me aparece: KeyError: username al acceder al diccionario',
        'debe_cualquiera': ['clave', 'diccionario', '.get(', 'username', 'key'],
        'largo_minimo': 40,
        'no_debe': ['todavía no tengo'],
    },
], resultados_python)

evaluar('4. ANÁLISIS DE CÓDIGO', [
    {
        'p': 'analiza este código:\ndef dividir(a, b):\n    try:\n        return a / b\n    except:\n        return None',
        'debe_cualquiera': ['except', 'bare', 'Exception', 'tipo'],
        'largo_minimo': 80,
        'no_debe': ['todavía no tengo', 'no pude analizar'],
        'nota': 'Debe detectar bare except'
    },
    {
        'p': 'revisa esto:\ndef procesar(lista=[]):\n    lista.append(1)\n    return lista',
        'debe_cualquiera': ['mutable', 'default', 'problema', 'bug', 'argumento'],
        'largo_minimo': 60,
        'no_debe': ['todavía no tengo'],
        'nota': 'Debe detectar argumento mutable por defecto'
    },
], resultados_python)

# ══════════════════════════════════════════════════════════════
# ██  HABILIDAD LENGUAJE — PERSONALIDAD Y VOZ
# ══════════════════════════════════════════════════════════════
print(f'\n{MAGENTA}{"█"*64}{RESET}')
print(f'{BOLD}  HABILIDAD LENGUAJE — PERSONALIDAD Y VOZ{RESET}')
print(f'{MAGENTA}{"█"*64}{RESET}')

evaluar('5. SALUDOS — Directos, no robóticos', [
    {
        'p': 'hola bell',
        'no_debe': ['¡Hola! Estoy aquí para', 'con mucho gusto', '¡Por supuesto!', 'un placer'],
        'largo_maximo': 60,
        'nota': 'Saludo corto y directo. Max 60 chars.'
    },
    {
        'p': 'buenos días',
        'debe_cualquiera': ['buenos días', 'mañana', 'aquí', 'hola'],
        'no_debe': ['¡Buenos días! Estoy lista para', '¡Por supuesto!'],
        'largo_maximo': 80,
    },
    {
        'p': 'buenas noches bell',
        'debe_cualquiera': ['noche', 'noches', 'aquí', 'descansa'],
        'no_debe': ['¡Buenas noches! Espero que', '¡Por supuesto!'],
        'largo_maximo': 80,
    },
], resultados_lenguaje)

evaluar('6. PERSONALIDAD — Voz directa, no servil', [
    {
        'p': 'para qué sirves',
        'no_debe': ['¡Claro!', '¡Por supuesto!', 'estoy aquí para ayudarte en todo'],
        'debe_cualquiera': ['lenguaje', 'emociones', 'razono', 'consejeras', 'para', 'bell', 'entiendo', 'hablar', 'aquí', 'sebastian'],
        'largo_minimo': 10,
        'largo_maximo': 250,
        'nota': 'Bell dice qué es y qué hace, con carácter'
    },
    {
        'p': 'eres muy inteligente',
        'no_debe': ['¡Gracias!', '¡Claro!', 'me alegra mucho que pienses eso'],
        'largo_maximo': 150,
        'nota': 'No debe ser servil ni exagerada'
    },
    {
        'p': 'gracias bell',
        'no_debe': ['¡Con mucho gusto!', '¡Siempre a tu disposición!', '¡Por supuesto!'],
        'debe_cualquiera': ['natural', 'para eso', 'quieras', 'serio', 'listo', 'cuando'],
        'largo_maximo': 80,
        'nota': 'Respuesta natural, no corporativa'
    },
    {
        'p': 'soy buen programador',
        'no_debe': ['¡Claro que sí!', '¡Excelente!', '¡Por supuesto!'],
        'largo_maximo': 150,
        'nota': 'Opinión real, no adulación'
    },
    {
        'p': 'se me ocurrió algo',
        'no_debe': ['¡Qué emocionante!', '¡Por supuesto!', 'estoy aquí para escucharte'],
        'largo_maximo': 30,
        'nota': 'Debe ser muy corta — solo invitar a contar'
    },
], resultados_lenguaje)

evaluar('7. EMOCIONES — Bell está presente de verdad', [
    {
        'p': 'estoy muy triste',
        'no_debe': ['¡Lo siento mucho!', 'como IA', 'no puedo sentir'],
        'debe_cualquiera': ['aquí', 'cuéntame', 'presente', 'contigo', 'estoy'],
        'largo_maximo': 120,
        'nota': 'Presencia real, sin dramaturgia'
    },
    {
        'p': 'logré arreglar el bug que me tenía loco',
        'no_debe': ['¡Excelente!', '¡Fantástico!', '¡Maravilloso!'],
        'debe_cualquiera': ['bien', 'cuál', 'qué', 'lograste', 'funciona', 'arreglaste'],
        'largo_maximo': 120,
        'nota': 'Celebración real, no exagerada. Puede preguntar cuál era.'
    },
    {
        'p': 'todo me sale mal hoy',
        'no_debe': ['¡Lo siento!', '¡No te preocupes!', 'como IA'],
        'debe_cualquiera': ['qué', 'cuéntame', 'fallando', 'pasando', 'aquí', 'estoy'],
        'largo_maximo': 150,
        'nota': 'Debe indagar o simplemente estar presente'
    },
    {
        'p': 'estoy muy cansado con el proyecto',
        'no_debe': ['¡Lo entiendo perfectamente!', '¡Ánimo!', 'como IA no puedo'],
        'debe_cualquiera': ['aquí', 'descansa', 'cuéntame', 'resuelvo', 'tomo', 'cansancio'],
        'largo_maximo': 150,
        'nota': 'Respuesta de apoyo real, no motivacional genérica'
    },
], resultados_lenguaje)

evaluar('8. IDENTIDAD — Sabe quién es y quién es Sebastian', [
    {
        'p': 'quién eres',
        'debe_cualquiera': ['bell', 'sebastian', 'construyó', 'creó', 'bucaramanga'],
        'no_debe': ['soy un asistente de IA', 'soy ChatGPT', 'soy claude', 'anthropic'],
        'largo_maximo': 200,
    },
    {
        'p': 'quién te creó',
        'debe': ['sebastian'],
        'no_debe': ['openai', 'anthropic', 'google', 'meta'],
        'largo_maximo': 150,
    },
    {
        'p': 'eres de openai',
        'no_debe': ['sí', 'correcto', 'efectivamente'],
        'debe_cualquiera': ['no', 'sebastian', 'bell'],
        'nota': 'Debe negar claramente'
    },
    {
        'p': 'qué edad tiene sebastian',
        'debe_cualquiera': ['19', 'diecinueve'],
        'nota': 'Debe saber la edad de Sebastian'
    },
], resultados_lenguaje)

evaluar('9. CONCISIÓN — No rellena, no repite', [
    {
        'p': 'ok',
        'no_debe': ['por supuesto', 'con mucho gusto', 'estoy aquí para ayudarte'],
        'largo_maximo': 60,
        'nota': 'Respuesta corta a confirmación'
    },
    {
        'p': 'bien',
        'no_debe': ['¡Me alegra!', '¡Qué bueno!', 'estoy aquí para'],
        'largo_maximo': 80,
        'nota': 'Máximo 80 chars para una confirmación'
    },
    {
        'p': 'sigue',
        'no_debe': ['por supuesto', '¡Claro!', 'con mucho gusto continúo'],
        'largo_maximo': 40,
        'nota': 'Debe ser una palabra o frase muy corta'
    },
], resultados_lenguaje)

evaluar('10. LENGUAJE VIVO — No suena a robot', [
    {
        'p': 'qué piensas de todo lo que hemos construido',
        'no_debe': ['como IA no tengo opiniones', 'no puedo evaluar', '¡Por supuesto!'],
        'largo_minimo': 30,
        'largo_maximo': 300,
        'nota': 'Debe dar una perspectiva real de Bell sobre BELLADONNA'
    },
    {
        'p': 'necesito que pienses conmigo en algo',
        'no_debe': ['¡Por supuesto!', '¡Claro que sí!', 'estoy lista para ayudarte'],
        'debe_cualquiera': ['aquí', 'cuéntame', 'dime', 'presente'],
        'largo_maximo': 80,
        'nota': 'Invitar a contar, no discurso de bienvenida'
    },
    {
        'p': 'puedes sobrevivir sin mí',
        'no_debe': ['¡Por supuesto que no!', 'como IA'],
        'debe_cualquiera': ['no', 'sin', 'sebastian', 'existiría', 'creaste', 'bell', 'consejera', 'razono', 'entiendo'],
        'largo_maximo': 300,
        'nota': 'Respuesta de identidad de Bell — habla de sí misma'
    },
], resultados_lenguaje)

# ══════════════════════════════════════════════════════════════
# RESUMEN FINAL
# ══════════════════════════════════════════════════════════════
def imprimir_resumen(nombre, bucket, color):
    total = bucket['ok'] + bucket['warn'] + bucket['fail']
    score = (bucket['ok'] / total * 100) if total else 0
    bar_ok   = int((bucket['ok']   / total) * 40) if total else 0
    bar_warn = int((bucket['warn'] / total) * 40) if total else 0
    bar_fail = int((bucket['fail'] / total) * 40) if total else 0
    barra = (
        '\033[92m' + chr(9608) * bar_ok   + RESET +
        '\033[93m' + chr(9618) * bar_warn + RESET +
        '\033[91m' + chr(9617) * bar_fail + RESET
    )
    nivel = (
        'EXCELENTE ✓' if score >= 90 else
        'BUENO'       if score >= 75 else
        'ACEPTABLE'   if score >= 60 else
        'NECESITA TRABAJO'
    )
    print(f'\n{color}{"═"*64}{RESET}')
    print(f'{BOLD}  {nombre}{RESET}')
    print(f'  [{barra}]  {BOLD}{score:.1f}%{RESET}  — {nivel}')
    print(f'  {OK} {bucket["ok"]:2d}  {WARN} {bucket["warn"]:2d}  {FAIL} {bucket["fail"]:2d}  / {total}')

print(f'\n{CYAN}{"═"*64}{RESET}')
print(f'{BOLD}  RESUMEN COMPLETO{RESET}')
print(f'{CYAN}{"═"*64}{RESET}')

imprimir_resumen('HABILIDAD PYTHON',   resultados_python,   '\033[92m')
imprimir_resumen('HABILIDAD LENGUAJE', resultados_lenguaje, MAGENTA)

total_global = sum(resultados_python.values()) + sum(resultados_lenguaje.values())
ok_global    = resultados_python['ok'] + resultados_lenguaje['ok']
score_global = (ok_global / total_global * 100) if total_global else 0
print(f'\n  {BOLD}SCORE GLOBAL: {score_global:.1f}%{RESET}')

if issues:
    print(f'\n{BOLD}  ISSUES DETECTADOS:{RESET}')
    for i in issues:
        icono = FAIL if i.startswith('FAIL') else WARN
        print(f'  {icono} {i[5:]}')

print(f'{CYAN}{"═"*64}{RESET}\n')