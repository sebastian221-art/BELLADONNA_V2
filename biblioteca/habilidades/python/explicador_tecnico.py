# biblioteca/habilidades/python/explicador_tecnico.py
# ============================================================
# EXPLICADOR TÉCNICO — fusión herramientas + Groq
#
# Flujo:
#   1. Herramientas calculan CC, MI, errores, seguridad (exacto)
#   2. Esos datos reales se pasan a Groq en XML
#   3. Groq explica QUÉ hace el código + QUÉ significan los números
#
# Resultado: Groq habla con autoridad matemática que no tiene solo.
# Los números son exactos porque vienen de Radon/Bandit, no de intuición.
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
_TIMEOUT    = 20

_SYSTEM_EXPLICADOR = """Eres Bell — IA de Juan Sebastian Mora, analizando código Python.
Recibes métricas EXACTAS calculadas por herramientas (AST, Radon, Bandit, PyFlakes).
NUNCA inventas ni estimas — solo interpretas los datos reales que recibes.

REGLAS:
- Explica QUÉ hace el código en 1-2 oraciones simples
- Interpreta las métricas con palabras humanas (no las copies en bruto)
- Si hay problemas de seguridad, menciónalos primero
- Termina con UNA sugerencia concreta de mejora si aplica
- Voz directa, en español, sin relleno
- Máximo 4-5 oraciones total"""


@dataclass
class Explicacion:
    texto_completo:  str
    puntos_clave:    list
    sugerencias:     list
    nivel_confianza: str  # 'datos_reales' o 'template'


class ExplicadorTecnico:

    def __init__(self):
        self._api_key = os.getenv('GROQ_API_KEY', '')
        self._groq_ok = bool(self._api_key)

    def explicar_analisis(self, analisis: 'AnalisisCompleto',
                          codigo_original: str = '') -> Explicacion:
        """
        Explicación con fusión herramientas + Groq.
        Si Groq no está disponible → usa templates locales.
        """
        # Construir resumen de métricas (para Groq y para fallback)
        metricas_txt = self._metricas_a_texto(analisis)
        sugerencias  = self._calcular_sugerencias(analisis)

        # Template siempre: métricas exactas de las herramientas
        texto_template = self._armar_texto(analisis, sugerencias)

        # Groq añade narrativa: "qué hace este código" en lenguaje humano
        # Se COMBINA con el template (no lo reemplaza)
        if self._groq_ok and codigo_original:
            narrativa = self._llamar_groq(metricas_txt, codigo_original)
            if narrativa:
                texto_final = narrativa.rstrip('.') + '\n\n' + texto_template
                return Explicacion(
                    texto_completo  = texto_final,
                    puntos_clave    = [metricas_txt],
                    sugerencias     = sugerencias,
                    nivel_confianza = 'datos_reales',
                )

        # Sin Groq: solo template (sigue siendo preciso)
        return Explicacion(
            texto_completo  = texto_template,
            puntos_clave    = [],
            sugerencias     = sugerencias,
            nivel_confianza = 'datos_reales',
        )

    def explicar_error(self, error: str, codigo: str = '') -> str:
        """Explica un error de Python en lenguaje humano."""
        el = error.lower()
        if 'nameerror' in el:
            n = self._extraer_nombre(error)
            return f"NameError: '{n}' no está definida en este contexto. Puede ser un typo o que la declaraste después de usarla."
        if 'typeerror' in el:
            return f"TypeError: tipo de dato incorrecto. {error.split('TypeError:')[-1].strip()}"
        if 'indexerror' in el:
            return "IndexError: el índice no existe en la lista. Verifica los límites."
        if 'keyerror' in el:
            n = self._extraer_nombre(error)
            return f"KeyError: la clave '{n}' no existe en el diccionario. Usa .get() para evitarlo."
        if 'importerror' in el or 'modulenotfounderror' in el:
            return f"ImportError: módulo no encontrado. {error.split(':')[-1].strip()}"
        if 'syntaxerror' in el:
            return f"SyntaxError: Python no puede leer el código. {error.split('SyntaxError:')[-1].strip()}"
        if 'attributeerror' in el:
            return f"AttributeError: atributo o método que no existe. {error.split('AttributeError:')[-1].strip()}"
        if 'valueerror' in el:
            return f"ValueError: valor del tipo correcto pero contenido inválido. {error.split('ValueError:')[-1].strip()}"
        if 'zerodivisionerror' in el:
            return "ZeroDivisionError: división por cero. Agrega un if b != 0 antes de dividir."
        if 'recursionerror' in el:
            return "RecursionError: la función se llama a sí misma sin condición de parada. Revisa el caso base."
        return f"Error: {error.strip()[:300]}"

    # ── Groq ──────────────────────────────────────────────────────────────

    def _llamar_groq(self, metricas_txt: str, codigo: str) -> str:
        """Llama a Groq con métricas reales + código. Devuelve explicación en voz Bell."""
        try:
            import httpx
            prompt = (
                f"<metricas_reales>\n{metricas_txt}\n</metricas_reales>\n\n"
                f"<codigo>\n{codigo[:1200]}\n</codigo>\n\n"
                f"<instruccion>En 2-3 oraciones: "
                f"1) qué hace este código en palabras simples, "
                f"2) si hay problemas ERROR o SEGURIDAD en las métricas, menciónalos explícitamente. "
                f"No repitas los números de métricas — eso ya se mostrará aparte.</instruccion>"
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
                    'temperature': 0.3,
                    'max_tokens':  400,
                },
                timeout=_TIMEOUT,
            )
            if r.status_code == 200:
                contenido = (r.json()
                             .get('choices',[{}])[0]
                             .get('message',{})
                             .get('content','')
                             .strip())
                if contenido and len(contenido) > 30:
                    print(f'  [Explicador] Groq fusión OK | {len(contenido)} chars')
                    return contenido
        except Exception as e:
            print(f'  [Explicador] Groq error: {e}')
        return ''

    # ── Métricas → texto estructurado ─────────────────────────────────────

    def _metricas_a_texto(self, analisis: 'AnalisisCompleto') -> str:
        """Convierte AnalisisCompleto a texto compacto para el prompt XML."""
        m = analisis.metricas
        lineas = [
            f"CC={m.cc} | MI={m.mi}/100 | LOC={m.loc} | Riesgo={m.nivel_riesgo.upper()}",
        ]
        # Funciones
        if analisis.funciones:
            sin_doc   = [f['nombre'] for f in analisis.funciones if not f.get('doc')]
            sin_hints = [f['nombre'] for f in analisis.funciones if not f.get('returns') and f.get('args')]
            if sin_doc:
                lineas.append(f"Sin docstring: {', '.join(sin_doc[:4])}")
            if sin_hints:
                lineas.append(f"Sin type hints retorno: {', '.join(sin_hints[:4])}")
        # Problemas
        errores   = [p for p in analisis.problemas if p.tipo == 'error']
        seguridad = [p for p in analisis.problemas if p.herramienta == 'bandit']
        for e in errores[:2]:
            lineas.append(f"ERROR L{e.linea}: {e.mensaje[:80]}")
        for s in seguridad[:3]:
            lineas.append(f"SEGURIDAD L{s.linea}: {s.mensaje[:80]}")
        if not errores and not seguridad:
            lineas.append("Sin errores ni vulnerabilidades detectadas.")
        return '\n'.join(lineas)

    # ── Fallback template ─────────────────────────────────────────────────

    def _calcular_sugerencias(self, analisis: 'AnalisisCompleto') -> list:
        sugs = []
        if analisis.metricas.cc > 10:
            sugs.append(f"CC={analisis.metricas.cc} — refactoriza funciones complejas.")
        if analisis.metricas.mi < 50:
            sugs.append("MI bajo — agrega docstrings y divide funciones largas.")
        if analisis.funciones:
            sin_doc = [f['nombre'] for f in analisis.funciones if not f.get('doc')]
            if sin_doc:
                sugs.append(f"Funciones sin docstring: {', '.join(sin_doc[:5])}.")
            sin_h = [f['nombre'] for f in analisis.funciones if not f.get('returns') and f.get('args')]
            if sin_h:
                sugs.append(f"Funciones sin type hints de retorno: {', '.join(sin_h[:5])}.")
        seg = [p for p in analisis.problemas if p.herramienta == 'bandit']
        if seg:
            sugs.append("Vulnerabilidades de seguridad detectadas — corrige antes de deploy.")
        return sugs

    def _armar_texto(self, analisis: 'AnalisisCompleto', sugerencias: list) -> str:
        riesgo_emoji = {'bajo':'✅','medio':'⚠️','alto':'🔴','crítico':'🚨'}.get(
            analisis.metricas.nivel_riesgo, ''
        )
        m = analisis.metricas
        partes = [f"{riesgo_emoji} Análisis completo — riesgo {m.nivel_riesgo.upper()}.\n"]

        if m.cc <= 5:
            partes.append(f"• Complejidad CC={m.cc} — muy simple, fácil de testear.")
        elif m.cc <= 10:
            partes.append(f"• Complejidad CC={m.cc} — dentro del rango profesional.")
        else:
            partes.append(f"• Complejidad CC={m.cc} — elevada, riesgo de bugs sin probar.")

        if m.mi >= 65:
            partes.append(f"• Índice de mantenibilidad MI={m.mi}/100 — código saludable. "
                          f"Otro developer (o tú en 6 meses) lo va a entender sin problema.")
        elif m.mi >= 30:
            partes.append(f"• Mantenibilidad MI={m.mi}/100 — aceptable pero mejorable.")
        else:
            partes.append(f"• Mantenibilidad MI={m.mi}/100 — difícil de mantener.")

        if m.loc > 0:
            partes.append(f"• Tamaño: {m.loc} líneas totales, {m.lloc} líneas lógicas.")

        errores   = [p for p in analisis.problemas if p.tipo == 'error']
        seguridad = [p for p in analisis.problemas if p.herramienta == 'bandit']
        for e in errores[:3]:
            partes.append(f"• Error línea {e.linea}: {e.mensaje}")
        for s in seguridad[:2]:
            partes.append(f"• ⚠️  Seguridad línea {s.linea}: {s.mensaje}")

        if sugerencias:
            partes.append("\nSugerencias de mejora:")
            for s in sugerencias:
                partes.append(f"  → {s}")

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