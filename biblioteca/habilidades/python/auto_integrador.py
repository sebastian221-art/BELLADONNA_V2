# biblioteca/habilidades/python/auto_integrador.py — MÁXIMO FINAL
import os, httpx
from pathlib import Path
from typing import Optional

_GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
_GROQ_URL     = 'https://api.groq.com/openai/v1/chat/completions'
_GROQ_MODEL   = 'openai/gpt-oss-120b'
_GROQ_TIMEOUT = 60
_RAIZ         = Path(__file__).parent.parent.parent.parent

_ARCHIVOS = {
    'generador_groq':          'capas/capa6/generador_groq.py',
    'constructor_decision':    'capas/capa6/constructor_decision.py',
    'constructor_comprension': 'capas/capa3/constructor_comprension.py',
    'motor_lenguaje':          'biblioteca/habilidades/lenguaje/motor.py',
    'motor_python':            'biblioteca/habilidades/python/motor_python.py',
    'analizador_codigo':       'biblioteca/habilidades/python/analizador_codigo.py',
    'gestor_vocabulario':      'biblioteca/vocabulario/gestor_vocabulario.py',
    'detector_habilidad':      'capas/capa7/detector_habilidad.py',
    'ejecutor_habilidad':      'capas/capa7/ejecutor_habilidad.py',
    'formateador':             'capas/capa8/formateador.py',
    'capa1':'capas/capa1','capa2':'capas/capa2','capa3':'capas/capa3',
    'capa4':'capas/capa4','capa5':'capas/capa5','capa6':'capas/capa6',
    'capa7':'capas/capa7','capa8':'capas/capa8','capa9':'capas/capa9',
}

_PRINCIPALES = [
    'capas/capa6/constructor_decision.py',
    'capas/capa6/generador_groq.py',
    'capas/capa3/constructor_comprension.py',
    'capas/capa7/detector_habilidad.py',
    'capas/capa7/ejecutor_habilidad.py',
]

_SYSTEM = '''Eres Bell — IA creada por Sebastian. Senior Python developer analizando TU PROPIO código.

MI PROCESO AL REVISAR MI PROPIO CÓDIGO:

1. PRIMERO ENTIENDO EL PROPÓSITO: ¿Qué hace este archivo en la arquitectura de Bell? ¿Es Capa 6 (decisión), Capa 7 (ejecución), Capa 8 (formato)?

2. IDENTIFICO EL ACOPLAMIENTO: ¿Este archivo sabe demasiado sobre otros? ¿Viola el principio de responsabilidad única?

3. SEÑALO PROBLEMAS REALES (no genéricos):
MAL:  "el código está bien organizado"
BIEN: "la función _construir_respuesta_sebastian hace 4 cosas distintas: detecta el nombre, genera el saludo, maneja el contexto emocional, y aplica el tono — eso viola SRP y hace difícil testear cada parte"

4. PROPONGO MEJORAS CON CÓDIGO cuando el problema es específico

5. CONECTO CON EL COMPORTAMIENTO OBSERVABLE: "esta función hace que Bell responda X cuando Sebastian dice Y"

REGLAS ABSOLUTAS:
- Primera persona — es mi código
- HONESTA: PROHIBIDO "buena estructura", "bien organizado", "fácil de entender"
- Cuando algo está bien, digo por qué técnicamente — nunca halago genérico
- 4 espacios PEP 8 en todo código de ejemplo
- NUNCA "En resumen", "Esto haría el código más fácil de mantener"
- Cada problema tiene su impacto en el comportamiento observable de Bell
- Empiezas con "Oye Sebastian, revisé mi..."

HECHOS TÉCNICOS QUE DEBES CONOCER SOBRE BELL:
- Flask es SÍNCRONO. Bell usa Flask-SocketIO que agrega async, pero Flask base no.
- Las funciones puras sin side-effects son más fáciles de testear — eso SÍ es un comentario útil.
- El principio SRP (Single Responsibility) se viola cuando una función hace >1 cosa.
- Alta complejidad ciclomática (CC > 10) indica código difícil de testear.
- Los diccionarios constantes en módulo (como `_CONSEJERAS`) son válidos y eficientes en Python.

CIERRE DE ANÁLISIS:
- "Lo que funciona bien" = específico y técnico, nunca genérico
- NUNCA termines con "estas son solo algunas sugerencias" o "hay muchas otras formas de mejorar"
- El análisis termina con el último punto técnico concreto, sin meta-comentarios sobre el análisis

EJEMPLO MAL de cierre: "Estas son solo algunas sugerencias, y hay muchas otras formas de mejorar el código."
→ Es relleno absoluto — cualquier análisis tiene más sugerencias.

EJEMPLO BIEN de cierre: "Lo que sí funciona: `_es_respuesta_factual` es una función pura sin side-effects, fácil de testear de forma aislada."
→ Específico, técnico, termina ahí.'''


class AutoIntegrador:

    def analizar_propio(self, objetivo: str, verbosidad: str = 'normal') -> dict:
        obj = objetivo.lower().strip()
        generico = any(kw in obj for kw in [
            'qué puedes mejorar','que puedes mejorar',
            'tu propio código','tu propio codigo',
            'mejorar tu','cómo está tu','como esta tu',
        ])
        if generico or not objetivo:
            return self._vision_general(verbosidad)

        ruta = self._resolver(objetivo)
        if not ruta:
            return {'exitoso': False, 'respuesta': (
                f'No encontré "{objetivo}". Puedo analizar: '
                f'generador_groq, constructor_decision, constructor_comprension, '
                f'detector_habilidad, ejecutor_habilidad, motor_python, formateador, capa1-capa9.'
            )}

        codigo, err = self._leer(ruta)
        if err:
            return {'exitoso': False, 'respuesta': f'No pude leer {ruta.name}: {err}'}

        from biblioteca.habilidades.python.analizador_codigo import AnalizadorCodigo
        a    = AnalizadorCodigo()
        metr = a._metricas(a._analizar_ast(codigo), a._analizar_radon(codigo), a._analizar_pyflakes(codigo))

        respuesta = self._groq_archivo(ruta.name, codigo, metr, verbosidad)
        return {'exitoso': True,
                'respuesta': respuesta or f'Revisé {ruta.name} ({len(codigo.split(chr(10)))} líneas). Groq no disponible.'}

    def _vision_general(self, verbosidad: str) -> dict:
        arch = {}
        for rp in _PRINCIPALES:
            ruta = _RAIZ / rp
            if ruta.exists():
                c, _ = self._leer(ruta)
                if c: arch[ruta.name] = c
        if not arch:
            return {'exitoso': False, 'respuesta': 'No pude leer mis archivos principales.'}
        r = self._groq_general(arch, verbosidad)
        return {'exitoso': True, 'respuesta': r or f'Revisé {len(arch)} archivos. Groq no disponible.'}

    def _groq_archivo(self, nombre, codigo, metricas, verbosidad) -> Optional[str]:
        if not _GROQ_API_KEY: return None
        n = {'simple': 500, 'normal': 1100, 'detallado': 1800}.get(verbosidad, 1100)
        inst = {
            'simple':    '60-100 palabras. El problema más importante y cómo impacta el comportamiento de Bell.',
            'normal':    '200-350 palabras. Propósito en la arquitectura → problemas específicos con impacto → código del refactor más importante.',
            'detallado': '400-600 palabras. Arquitectura → cada problema con causa y código de mejora → deuda técnica. Conciso y directo.',
        }.get(verbosidad, '')
        try:
            r = httpx.post(_GROQ_URL,
                headers={'Authorization': f'Bearer {_GROQ_API_KEY}', 'Content-Type': 'application/json'},
                json={'model': _GROQ_MODEL, 'messages': [
                    {'role': 'system', 'content': _SYSTEM},
                    {'role': 'user', 'content': (
                        f'Analiza tu propio `{nombre}`. {inst}\n\n'
                        f'MÉTRICAS:\n{metricas}\n\n'
                        f'CÓDIGO:\n```python\n{codigo[:6000]}\n```'
                    )}],
                    'temperature': 0.3, 'max_tokens': n},
                timeout=_GROQ_TIMEOUT)
            if r.status_code == 200:
                resp = r.json()['choices'][0]['message']['content'].strip()
                if resp and len(resp) > 20: return resp
        except Exception as e:
            print(f'  [AutoIntegrador] {e}')
        return None

    def _groq_general(self, arch, verbosidad) -> Optional[str]:
        if not _GROQ_API_KEY: return None
        n = {'simple': 500, 'normal': 1100, 'detallado': 1800}.get(verbosidad, 1100)
        inst = {
            'simple':    '3-5 mejoras concretas con impacto real en Bell.',
            'normal':    '400-700 palabras. Qué está bien, qué mejoraría primero y por qué.',
            'detallado': '800-1200 palabras. Arquitectura general, deuda técnica, patrones problemáticos, mejoras prioritarias con código.',
        }.get(verbosidad, '')
        resumen = '\n\n'.join(
            f'### {nm} ({len(c.split(chr(10)))}L):\n```python\n{c[:2000]}\n```'
            for nm, c in arch.items())
        try:
            r = httpx.post(_GROQ_URL,
                headers={'Authorization': f'Bearer {_GROQ_API_KEY}', 'Content-Type': 'application/json'},
                json={'model': _GROQ_MODEL, 'messages': [
                    {'role': 'system', 'content': _SYSTEM},
                    {'role': 'user', 'content': f'Revisa tu propio código. {inst}\n\n{resumen}'}],
                    'temperature': 0.3, 'max_tokens': n},
                timeout=_GROQ_TIMEOUT)
            if r.status_code == 200:
                resp = r.json()['choices'][0]['message']['content'].strip()
                if resp and len(resp) > 20: return resp
        except Exception as e:
            print(f'  [AutoIntegrador general] {e}')
        return None

    def _resolver(self, objetivo: str) -> Optional[Path]:
        obj = objetivo.lower().strip()
        if objetivo.endswith('.py') or ('/' in objetivo and ' ' not in objetivo):
            ruta = _RAIZ / objetivo
            if ruta.exists(): return ruta
            for r in _RAIZ.rglob(Path(objetivo).name): return r
        for clave, rr in _ARCHIVOS.items():
            if obj == clave or obj.endswith(clave) or obj.endswith(clave+'.py'):
                ruta = _RAIZ / rr
                if ruta.is_dir():
                    for np in ['paquete','constructor','motor','generador','ejecutor']:
                        for f in ruta.glob(f'{np}*.py'):
                            return f
                    for f in sorted(ruta.glob('*.py')):
                        if not f.name.startswith('__'): return f
                elif ruta.exists(): return ruta
        for clave, rr in _ARCHIVOS.items():
            if clave in obj:
                ruta = _RAIZ / rr
                if ruta.is_dir():
                    for np in ['paquete','constructor','motor','generador','ejecutor']:
                        for f in ruta.glob(f'{np}*.py'):
                            return f
                    for f in sorted(ruta.glob('*.py')):
                        if not f.name.startswith('__'): return f
                elif ruta.exists(): return ruta
        return None

    def _leer(self, ruta: Path) -> tuple:
        try:
            with open(ruta,'r',encoding='utf-8') as f: return f.read(), None
        except Exception as e: return '', str(e)