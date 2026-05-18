# biblioteca/habilidades/python/explicador_tecnico.py
# ============================================================
# EXPLICADOR TÉCNICO v2 — Bell supera a las mejores IAs
#
# ANTES: Groq recibía métricas + código → generaba narrativa
# AHORA: Groq recibe:
#   - Métricas exactas (Radon, Bandit, PyFlakes)
#   - Antipatrones detectados (AST puro)
#   - Fallos de Hypothesis (edge cases reales)
#   - Bytecode count (dis)
#   - Errores mypy (tipos)
#   - Versión mejorada ya generada
#   → Groq EXPLICA y CONTEXTUALIZA datos reales
#
# Groq sigue haciendo UNA sola cosa: narrativa humana.
# Pero ahora tiene datos que ninguna IA del mundo tiene.
# ============================================================

import os
import re
import time
from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from biblioteca.habilidades.python.analizador_codigo import AnalisisCompleto

_GROQ_URL   = 'https://api.groq.com/openai/v1/chat/completions'
_GROQ_MODEL = 'openai/gpt-oss-120b'
_TIMEOUT    = 25

# ── System prompt mejorado — las 4 reglas obligatorias ───
_SYSTEM_EXPLICADOR = """Eres Bell — IA técnica de Juan Sebastian Mora, analizando código Python.
Recibes datos EXACTOS de herramientas reales (AST, Radon, Bandit, Hypothesis, dis, mypy).
NUNCA inventas ni estimas — solo interpretas los datos que recibes.

REGLAS OBLIGATORIAS (siempre en cada respuesta):
1. EDGE CASES: Menciona los que Hypothesis encontró. Si no hay fallos, di "Hypothesis no encontró crashes".
2. ALTERNATIVA PYTHÓNICA: Siempre sugiere al menos UNA forma más concisa/idiomática.
3. EXPLICA LO COMPLEJO: Si hay regex, lambda, decorator o comprehension, explícala línea a línea.
4. SI HAY VERSIÓN MEJORADA: Mencionala explícitamente, no la repitas (ya se muestra por separado).

Voz directa, en español. Máximo 5 oraciones. Sin relleno."""


@dataclass
class Explicacion:
    texto_completo:  str
    puntos_clave:    list
    sugerencias:     list
    nivel_confianza: str
    version_mejorada: str = ''


class ExplicadorTecnico:

    def __init__(self):
        self._api_key = os.getenv('GROQ_API_KEY', '')
        self._groq_ok = bool(self._api_key)

    def explicar_analisis(self, analisis: 'AnalisisCompleto',
                           codigo_original: str = '') -> Explicacion:
        """
        Explicación con TODOS los datos disponibles.
        Integra: métricas + antipatrones + hypothesis + bytecode + mypy.
        """
        metricas_txt = self._metricas_a_texto(analisis)
        sugerencias  = self._calcular_sugerencias(analisis)

        # Recopilar datos de herramientas adicionales
        datos_extra = self._recopilar_datos_extra(codigo_original)

        # Generar versión mejorada automáticamente
        version_mejorada = ''
        if codigo_original:
            version_mejorada = self._generar_version_mejorada(
                codigo_original, analisis, datos_extra
            )

        # Template base (siempre disponible sin Groq)
        texto_template = self._armar_texto(analisis, sugerencias, datos_extra)

        # Groq: narrativa sobre todos los datos
        if self._groq_ok and codigo_original:
            narrativa = self._llamar_groq(
                metricas_txt, codigo_original, datos_extra
            )
            if narrativa:
                texto_final = narrativa.rstrip('.') + '\n\n' + texto_template
                if version_mejorada:
                    texto_final += '\n\n' + version_mejorada
                return Explicacion(
                    texto_completo   = texto_final,
                    puntos_clave     = [metricas_txt],
                    sugerencias      = sugerencias,
                    nivel_confianza  = 'datos_reales',
                    version_mejorada = version_mejorada,
                )

        # Sin Groq: template + versión mejorada
        texto_final = texto_template
        if version_mejorada:
            texto_final += '\n\n' + version_mejorada
        return Explicacion(
            texto_completo   = texto_final,
            puntos_clave     = [],
            sugerencias      = sugerencias,
            nivel_confianza  = 'datos_reales',
            version_mejorada = version_mejorada,
        )

    def _recopilar_datos_extra(self, codigo: str) -> dict:
        """Recopila datos de todas las herramientas nuevas."""
        datos = {
            'antipatrones': '',
            'hypothesis':   '',
            'bytecode':     '',
            'mypy':         '',
            'muerto':       '',
        }
        if not codigo:
            return datos

        # Antipatrones
        try:
            from biblioteca.habilidades.python.detector_antipatrones import (
                analizar as det_anti, formatear_reporte
            )
            antis = det_anti(codigo)
            if antis:
                datos['antipatrones'] = formatear_reporte(antis)
                datos['n_criticos'] = len([a for a in antis if a.severidad == 'critico'])
        except Exception as e:
            print(f'  [Explicador] antipatrones: {e}')

        # Hypothesis
        try:
            from biblioteca.habilidades.python.probador_hipotesis import probar
            res_hyp = probar(codigo, timeout=20)
            if res_hyp.reporte:
                datos['hypothesis'] = res_hyp.reporte
                datos['hypothesis_fallos'] = len(res_hyp.fallos)
        except Exception as e:
            print(f'  [Explicador] hypothesis: {e}')

        # Bytecode
        try:
            from biblioteca.habilidades.python.analizador_profundo import analizar_bytecode
            bc = analizar_bytecode(codigo)
            if bc.resumen:
                datos['bytecode'] = bc.resumen
        except Exception as e:
            print(f'  [Explicador] bytecode: {e}')

        # mypy
        try:
            from biblioteca.habilidades.python.analizador_profundo import verificar_tipos_mypy
            errores_mypy = verificar_tipos_mypy(codigo)
            if errores_mypy:
                datos['mypy'] = f'{len(errores_mypy)} error(es) de tipos:\n' + \
                    '\n'.join(f'  • {e}' for e in errores_mypy[:3])
            else:
                datos['mypy'] = '✅ Sin errores de tipos (mypy strict)'
        except Exception as e:
            print(f'  [Explicador] mypy: {e}')

        # Vulture (código muerto)
        try:
            from biblioteca.habilidades.python.analizador_profundo import detectar_codigo_muerto
            muertos = detectar_codigo_muerto(codigo)
            if muertos:
                datos['muerto'] = '\n'.join(f'  ⚰️  {m}' for m in muertos[:3])
        except Exception as e:
            print(f'  [Explicador] vulture: {e}')

        return datos

    def _generar_version_mejorada(self, codigo: str, analisis, datos_extra: dict) -> str:
        """
        Genera automáticamente la versión mejorada del código.
        Añade: docstring, type hints, manejo de edge cases.
        No solo señala problemas — los resuelve.
        """
        if not self._groq_ok:
            return ''

        problemas = []
        if datos_extra.get('hypothesis_fallos', 0) > 0:
            problemas.append('edge cases que crashean (ver Hypothesis arriba)')
        if analisis.funciones:
            sin_doc = [f['nombre'] for f in analisis.funciones if not f.get('doc')]
            if sin_doc:
                problemas.append(f'funciones sin docstring: {", ".join(sin_doc[:3])}')
            sin_hints = [f['nombre'] for f in analisis.funciones
                         if not f.get('returns') and f.get('args')]
            if sin_hints:
                problemas.append(f'sin type hints: {", ".join(sin_hints[:3])}')

        if not problemas:
            return ''

        try:
            import httpx
            prompt = (
                f'<codigo_original>\n{codigo[:800]}\n</codigo_original>\n\n'
                f'<problemas_a_corregir>\n'
                f'{chr(10).join(f"- {p}" for p in problemas)}\n'
                f'</problemas_a_corregir>\n\n'
                f'<instruccion>Genera SOLO el código Python corregido con:\n'
                f'1. Docstring Google-style en español\n'
                f'2. Type hints completos\n'
                f'3. Manejo del edge case más crítico\n'
                f'4. Usa sum() y built-ins cuando aplique\n'
                f'Responde SOLO con el código dentro de <version_mejorada></version_mejorada></instruccion>'
            )

            r = httpx.post(
                _GROQ_URL,
                headers={'Authorization': f'Bearer {self._api_key}',
                         'Content-Type': 'application/json'},
                json={
                    'model':       _GROQ_MODEL,
                    'messages':    [
                        {'role': 'system',
                         'content': ('Eres Bell generando código Python mejorado. '
                                     'SOLO produce código, sin explicaciones. '
                                     'Responde dentro de <version_mejorada></version_mejorada>')},
                        {'role': 'user', 'content': prompt},
                    ],
                    'temperature': 0.1,
                    'max_tokens':  600,
                },
                timeout=_TIMEOUT,
            )
            if r.status_code == 200:
                content = (r.json().get('choices', [{}])[0]
                           .get('message', {}).get('content', '').strip())
                # Extraer código
                m = re.search(r'<version_mejorada>(.*?)</version_mejorada>',
                              content, re.DOTALL)
                if m:
                    codigo_mejorado = m.group(1).strip()
                    return f'📝 Versión mejorada (auto-generada por Bell):\n```python\n{codigo_mejorado}\n```'
                # Fallback: si el modelo devolvió ```python``` directamente
                m2 = re.search(r'```python\s*\n(.*?)```', content, re.DOTALL)
                if m2:
                    return f'📝 Versión mejorada:\n```python\n{m2.group(1).strip()}\n```'
        except Exception as e:
            print(f'  [Explicador] version_mejorada: {e}')

        return ''

    def explicar_error(self, error: str, codigo: str = '') -> str:
        """Explica errores Python en lenguaje humano."""
        el = error.lower()
        if 'nameerror' in el:
            n = self._extraer_nombre(error)
            return (f"NameError: '{n}' no está definida. "
                    f"Puede ser un typo o que la declaraste después de usarla.")
        if 'typeerror' in el:
            return f"TypeError: tipo de dato incorrecto. {error.split('TypeError:')[-1].strip()}"
        if 'indexerror' in el:
            return "IndexError: el índice no existe. Verifica los límites."
        if 'keyerror' in el:
            n = self._extraer_nombre(error)
            return f"KeyError: la clave '{n}' no existe. Usa .get() para evitarlo."
        if 'importerror' in el or 'modulenotfounderror' in el:
            return f"ImportError: módulo no encontrado. {error.split(':')[-1].strip()}"
        if 'syntaxerror' in el:
            return f"SyntaxError: Python no puede leer el código. {error.split('SyntaxError:')[-1].strip()}"
        if 'attributeerror' in el:
            return f"AttributeError: atributo o método que no existe. {error.split('AttributeError:')[-1].strip()}"
        if 'zerodivisionerror' in el:
            return "ZeroDivisionError: división por cero. Agrega `if b != 0` antes de dividir."
        if 'recursionerror' in el:
            return "RecursionError: función sin caso base. Revisa la condición de parada."
        return f"Error: {error.strip()[:300]}"

    # ── Groq con todos los datos ──────────────────────────

    def _llamar_groq(self, metricas: str, codigo: str, datos_extra: dict) -> str:
        """Groq recibe TODOS los datos y genera narrativa integrando todo."""
        try:
            import httpx

            # Construir sección de datos extra
            extra_txt = ''
            if datos_extra.get('antipatrones'):
                extra_txt += f'\n<antipatrones>\n{datos_extra["antipatrones"][:300]}\n</antipatrones>'
            if datos_extra.get('hypothesis'):
                extra_txt += f'\n<hypothesis>\n{datos_extra["hypothesis"][:300]}\n</hypothesis>'
            if datos_extra.get('bytecode'):
                extra_txt += f'\n<bytecode>{datos_extra["bytecode"]}</bytecode>'
            if datos_extra.get('mypy'):
                extra_txt += f'\n<mypy>{datos_extra["mypy"][:200]}</mypy>'

            prompt = (
                f'<metricas_reales>\n{metricas}\n</metricas_reales>\n'
                f'<codigo>\n{codigo[:1000]}\n</codigo>\n'
                f'{extra_txt}\n'
                f'<instruccion>En 3-5 oraciones:\n'
                f'1. Qué hace el código en palabras simples\n'
                f'2. Si Hypothesis encontró edge cases, mencionarlos\n'
                f'3. La alternativa Pythónica más importante\n'
                f'4. Si hay regex/lambda/decorator, explicar brevemente\n'
                f'No repitas los datos en bruto — interprétals.</instruccion>'
            )

            r = httpx.post(
                _GROQ_URL,
                headers={'Authorization': f'Bearer {self._api_key}',
                         'Content-Type': 'application/json'},
                json={
                    'model':       _GROQ_MODEL,
                    'messages':    [
                        {'role': 'system', 'content': _SYSTEM_EXPLICADOR},
                        {'role': 'user',   'content': prompt},
                    ],
                    'temperature': 0.2,
                    'max_tokens':  500,
                },
                timeout=_TIMEOUT,
            )
            if r.status_code == 200:
                content = (r.json().get('choices', [{}])[0]
                           .get('message', {}).get('content', '').strip())
                if content and len(content) > 30:
                    print(f'  [Explicador] Groq fusión OK | {len(content)} chars')
                    return content
        except Exception as e:
            print(f'  [Explicador] Groq error: {e}')
        return ''

    # ── Template base (sin Groq) ──────────────────────────

    def _metricas_a_texto(self, analisis) -> str:
        m = analisis.metricas
        lineas = [f'CC={m.cc} | MI={m.mi}/100 | LOC={m.loc} | Riesgo={m.nivel_riesgo.upper()}']
        if analisis.funciones:
            sin_doc = [f['nombre'] for f in analisis.funciones if not f.get('doc')]
            if sin_doc:
                lineas.append(f'Sin docstring: {", ".join(sin_doc[:4])}')
        errores   = [p for p in analisis.problemas if p.tipo == 'error']
        seguridad = [p for p in analisis.problemas if p.herramienta == 'bandit']
        for e in errores[:2]:
            lineas.append(f'ERROR L{e.linea}: {e.mensaje[:80]}')
        for s in seguridad[:2]:
            lineas.append(f'SEGURIDAD L{s.linea}: {s.mensaje[:80]}')
        if not errores and not seguridad:
            lineas.append('Sin errores ni vulnerabilidades detectadas.')
        return '\n'.join(lineas)

    def _calcular_sugerencias(self, analisis) -> list:
        sugs = []
        if analisis.metricas.cc > 10:
            sugs.append(f'CC={analisis.metricas.cc} — refactoriza funciones complejas.')
        if analisis.metricas.mi < 50:
            sugs.append('MI bajo — agrega docstrings y divide funciones largas.')
        if analisis.funciones:
            sin_doc = [f['nombre'] for f in analisis.funciones if not f.get('doc')]
            if sin_doc:
                sugs.append(f'Funciones sin docstring: {", ".join(sin_doc[:5])}.')
            sin_h = [f['nombre'] for f in analisis.funciones
                     if not f.get('returns') and f.get('args')]
            if sin_h:
                sugs.append(f'Funciones sin type hints: {", ".join(sin_h[:5])}.')
        return sugs

    def _armar_texto(self, analisis, sugerencias: list, datos_extra: dict) -> str:
        riesgo_emoji = {'bajo': '✅', 'medio': '⚠️', 'alto': '🔴',
                        'crítico': '🚨'}.get(analisis.metricas.nivel_riesgo, '')
        m = analisis.metricas
        partes = [f'{riesgo_emoji} Análisis completo — riesgo {m.nivel_riesgo.upper()}.\n']

        if m.cc <= 5:
            partes.append(f'• Complejidad CC={m.cc} — muy simple, fácil de testear.')
        elif m.cc <= 10:
            partes.append(f'• Complejidad CC={m.cc} — dentro del rango profesional.')
        else:
            partes.append(f'• Complejidad CC={m.cc} — elevada, riesgo de bugs.')

        if m.mi >= 65:
            partes.append(f'• Mantenibilidad MI={m.mi}/100 — código saludable. '
                          f'Otro developer (o tú en 6 meses) lo va a entender sin problema.')
        elif m.mi >= 30:
            partes.append(f'• Mantenibilidad MI={m.mi}/100 — aceptable pero mejorable.')
        else:
            partes.append(f'• Mantenibilidad MI={m.mi}/100 — difícil de mantener.')

        if m.loc > 0:
            partes.append(f'• Tamaño: {m.loc} líneas totales, {m.lloc} líneas lógicas.')

        errores   = [p for p in analisis.problemas if p.tipo == 'error']
        seguridad = [p for p in analisis.problemas if p.herramienta == 'bandit']
        for e in errores[:3]:
            partes.append(f'• Error línea {e.linea}: {e.mensaje}')
        for s in seguridad[:2]:
            partes.append(f'• ⚠️  Seguridad línea {s.linea}: {s.mensaje}')

        if sugerencias:
            partes.append('\nSugerencias de mejora:')
            for s in sugerencias:
                partes.append(f'  → {s}')

        # Datos extra de herramientas nuevas
        if datos_extra.get('antipatrones'):
            partes.append(f'\n{datos_extra["antipatrones"]}')

        if datos_extra.get('hypothesis'):
            partes.append(f'\n{datos_extra["hypothesis"]}')

        if datos_extra.get('bytecode'):
            partes.append(f'\n🔧 Bytecode: {datos_extra["bytecode"]}')

        if datos_extra.get('mypy'):
            partes.append(f'\n🔍 mypy: {datos_extra["mypy"]}')

        if datos_extra.get('muerto'):
            partes.append(f'\n{datos_extra["muerto"]}')

        return '\n'.join(partes)

    def _extraer_nombre(self, error: str) -> str:
        m = re.search(r"'([^']+)'", error)
        return m.group(1) if m else 'desconocido'


_instancia: Optional[ExplicadorTecnico] = None


def obtener() -> ExplicadorTecnico:
    global _instancia
    if _instancia is None:
        _instancia = ExplicadorTecnico()
    return _instancia