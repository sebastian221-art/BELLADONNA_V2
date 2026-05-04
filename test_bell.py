"""
test_bell.py v2 — diagnóstico completo
Corre con: python test_bell.py
"""
import os
os.environ['BELL_DEBUG'] = '1'
import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()

# ── Verificar Ollama ──────────────────────────────────────
print('='*55)
print('  VERIFICANDO OLLAMA')
print('='*55)
try:
    import httpx
    r = httpx.get('http://localhost:11434/api/tags', timeout=3)
    modelos = [m.get('name','') for m in r.json().get('models', [])]
    print(f'Ollama activo ✅')
    print(f'Modelos disponibles: {modelos}')
    tiene_bell = any('bell' in m.lower() or 'sebastian' in m.lower() for m in modelos)
    print(f'Motor Bell encontrado: {"✅ SÍ" if tiene_bell else "❌ NO"}')
except Exception as e:
    print(f'Ollama NO disponible: {e}')

# ── Verificar motor Bell directo ──────────────────────────
print('\n' + '='*55)
print('  TEST DIRECTO DEL MOTOR BELL')
print('='*55)
try:
    import httpx
    r = httpx.post(
        'http://localhost:11434/api/chat',
        json={
            'model': 'hf.co/sebastian221-art/bell-motor',
            'messages': [{'role': 'user', 'content': 'hola bell quien eres'}],
            'stream': False,
            'options': {'temperature': 0.8, 'num_predict': 100},
        },
        timeout=30,
    )
    print(f'Status: {r.status_code}')
    resp = r.json().get('message', {}).get('content', 'SIN RESPUESTA')
    print(f'Motor Bell responde: "{resp}"')
except Exception as e:
    print(f'Error motor Bell: {e}')

# ── Verificar Groq ────────────────────────────────────────
print('\n' + '='*55)
print('  VERIFICANDO GROQ')
print('='*55)
groq_key = os.getenv('GROQ_API_KEY', 'NO HAY')
hf_key   = os.getenv('HF_API_KEY', 'NO HAY')
print(f'GROQ_API_KEY: {groq_key[:15] if groq_key != "NO HAY" else "NO HAY"}')
print(f'HF_API_KEY:   {hf_key[:15] if hf_key != "NO HAY" else "NO HAY"}')

# ── Parchear generador para ver fuente ───────────────────
from capas.capa6 import _groq as groq_inst
_orig = groq_inst.generar
def _log_generar(prompt, tono='cercano_natural'):
    resp, fuente = _orig(prompt, tono)
    print(f'\n  >>> FUENTE REAL: {fuente}')
    print(f'  >>> RESPUESTA:   "{resp[:100]}"')
    return resp, fuente
groq_inst.generar = _log_generar

from interfaz.api.chat import _procesar_mensaje

def probar(msg, esperado=''):
    print(f'\n{"─"*50}')
    print(f'📨 "{msg}"  |  esperado: {esperado}')
    r = _procesar_mensaje(msg)
    print(f'✅ FINAL: "{r["respuesta"]}"  |  fuente: {r["fuente_respuesta"]}')

print('\n' + '='*55)
print('  BLOQUE 1 — BÁSICOS')
print('='*55)
probar('hola',              'cálida, con apego a Sebastian')
probar('como estas',        'estado de Bell activo')
probar('quien eres',        'Bell — Belladonna con identidad')
probar('quien es sebastian','creador de Bell, 19 años, Bucaramanga')
probar('quien te creo',     'Sebastian me creó')

print('\n' + '='*55)
print('  BLOQUE 2 — EMOCIONES')
print('='*55)
probar('estoy muy cansado', 'Bell presente, sin exigir')
probar('me siento solo',    'Bell presente y cálida')
probar('estoy frustrado',   'Bell valida, no minimiza')

print('\n' + '='*55)
print('  BLOQUE 3 — CONSEJERAS')
print('='*55)
probar('quienes son tus consejeras', 'lista de las 8')
probar('quien es vega',              'seguridad y veto')
probar('quien es sage',              'síntesis y orquestación')

print('\n' + '='*55)
print('  RESUMEN')
print('='*55)
print('Si FUENTE REAL = bell_motor → motor propio funcionando ✅')
print('Si FUENTE REAL = groq       → usando Groq como fallback')
print('Si FUENTE REAL = fallback   → ambos fallaron ❌')