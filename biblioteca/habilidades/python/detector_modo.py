# biblioteca/habilidades/python/detector_modo.py
# ================================================
# DETECTOR DE MODO — Habilidad Python
#
# Refina la detección de modo y extrae el código
# o la descripción del mensaje de Sebastian.
# Capa 7 ya detectó el modo general, aquí
# sacamos el contenido concreto para procesar.
# ================================================

import re
from typing import Optional


class DetectorModo:
    """
    Extrae el código o descripción del mensaje
    y refina el modo si es necesario.
    """

    # Patrones para extraer bloques de código
    _BLOQUE_CODIGO = re.compile(
        r'```(?:python|py)?\s*\n?(.*?)```',
        re.DOTALL | re.IGNORECASE
    )
    _CODIGO_INDENTADO = re.compile(
        r'(?:^|\n)((?:[ \t]+\S.*\n?)+)',
        re.MULTILINE
    )
    # Indicadores de que hay código en el mensaje
    _SENALES_CODIGO = [
        r'\bdef\s+\w+\s*\(',
        r'\bclass\s+\w+\s*[:\(]',
        r'^\s*import\s+\w+',
        r'^\s*from\s+\w+\s+import\b',
        r'\bif\s+__name__\s*==\s*["\']__main__["\']',
        r'\bTraceback\s*\(most recent call last\)',
        r'\b\w+Error:\s*\S+',
    ]

    def extraer(self, texto: str, modo_inicial: str) -> dict:
        """
        Retorna:
        {
          'modo': str,             # modo refinado
          'codigo': str,           # código extraído (si hay)
          'descripcion': str,      # descripción o pregunta
          'tiene_codigo': bool,
          'tiene_traceback': bool,
          'archivo_objetivo': str, # para auto_analisis
        }
        """
        # ── Separar descripción de código inline ──────────────
        # Cuando Sebastian escribe "analiza este código:\ndef func..."
        # hay que separar la pregunta del código
        texto_original_completo = texto
        texto_codigo_parte, descripcion_inicial = self._separar_pregunta_codigo(texto)

        resultado = {
            'modo':             modo_inicial,
            'codigo':           '',
            'descripcion':      descripcion_inicial,
            'tiene_codigo':     False,
            'tiene_traceback':  False,
            'archivo_objetivo': '',
        }

        # ── Detectar traceback ────────────────────────────────
        _EJECUTAR = [
            'corre este', 'ejecuta esto', 'ejecuta el código', 'ejecuta este',
            'corre el código', 'prueba esto', 'prueba el código', 'prueba si funciona',
            'comprueba si funciona', 'verifica si funciona', 'testa el código',
            'corre esta función', 'ejecuta esta función', 'ejecuta el script',
        ]
        if any(t in texto.lower() for t in _EJECUTAR):
            resultado['modo'] = 'ejecutar'

        if re.search(r'Traceback\s*\(most recent call last\)', texto, re.IGNORECASE):
            resultado['tiene_traceback'] = True
            resultado['modo']            = 'debug'

        # ── Extraer bloque de código con backticks ────────────
        match_bloque = self._BLOQUE_CODIGO.search(texto)
        if match_bloque:
            codigo = match_bloque.group(1).strip()
            if codigo:
                resultado['codigo']      = codigo
                resultado['tiene_codigo'] = True
                descripcion = texto[:match_bloque.start()].strip()
                if descripcion:
                    resultado['descripcion'] = descripcion

        # ── Si no hay backticks, buscar señales de código ─────
        if not resultado['tiene_codigo']:
            for patron in self._SENALES_CODIGO:
                if re.search(patron, texto_original_completo, re.MULTILINE | re.IGNORECASE):
                    resultado['tiene_codigo'] = True
                    # Usar el texto sin la línea de pregunta
                    texto_analizar = texto_codigo_parte if texto_codigo_parte != texto_original_completo else texto_original_completo
                    lineas_codigo = [
                        l for l in texto_analizar.split('\n')
                        if re.match(r'^\s*(def |class |import |from |    |\t)', l)
                    ]
                    if len(lineas_codigo) >= 1:
                        # Extraer solo las líneas de código
                        lineas_todas = texto_analizar.split('\n')
                        inicio_codigo = None
                        for i, l in enumerate(lineas_todas):
                            if re.match(r'^\s*(def |class |import |from )', l):
                                inicio_codigo = i
                                break
                        if inicio_codigo is not None:
                            resultado['codigo'] = '\n'.join(lineas_todas[inicio_codigo:]).strip()
                        else:
                            resultado['codigo'] = texto_analizar.strip()
                    break

        # ── Refinar modo según el contenido ───────────────────
        if resultado['tiene_traceback']:
            resultado['modo'] = 'debug'
        elif resultado['tiene_codigo'] and resultado['codigo']:
            if modo_inicial in ('explicacion', 'conversacional', ''):
                # Si hay código pero pidió explicación → probablemente análisis
                resultado['modo'] = 'analisis'
        elif not resultado['tiene_codigo']:
            if modo_inicial == 'analisis':
                # Sin código para analizar → explicación
                resultado['modo'] = 'explicacion'

        # ── Detectar archivo objetivo para auto-análisis ──────
        if resultado['modo'] == 'auto_analisis':
            archivo = self._detectar_archivo_objetivo(texto)
            resultado['archivo_objetivo'] = archivo

        return resultado

    def _separar_pregunta_codigo(self, texto: str) -> tuple:
        """
        Separa la pregunta del código inline.
        "analiza este código:\ndef func():" → ("analiza este código", "def func():")
        Retorna (texto_sin_codigo, descripcion)
        """
        import re
        # Si hay bloques con backticks, el texto ya está bien separado
        if '```' in texto:
            return texto, texto.strip()

        # Buscar si hay código Python después de una línea de pregunta
        lineas = texto.split('\n')
        if len(lineas) < 2:
            return texto, texto.strip()

        # La primera línea es la pregunta, las siguientes pueden ser código
        primera = lineas[0].strip()
        resto   = '\n'.join(lineas[1:]).strip()

        # Si el resto tiene señales de código Python
        _SENALES = ['def ', 'class ', 'import ', 'from ', 'Traceback',
                    'Error:', '    ', '\t', 'return ', '>>> ']
        if resto and any(s in resto for s in _SENALES):
            return texto, primera  # descripcion es la primera línea

        return texto, texto.strip()

    def _detectar_archivo_objetivo(self, texto: str) -> str:
        """Detecta qué archivo/capa de Bell se quiere analizar."""
        tl = texto.lower()
        if re.search(r'capa\s*(\d+)', tl):
            match = re.search(r'capa\s*(\d+)', tl)
            return f'capa{match.group(1)}'
        if 'constructor_decision' in tl:  return 'capas/capa6/constructor_decision.py'
        if 'constructor_comprension' in tl: return 'capas/capa3/constructor_comprension.py'
        if 'motor' in tl and 'lenguaje' in tl: return 'biblioteca/habilidades/lenguaje/motor.py'
        if 'gestor_vocabulario' in tl:  return 'biblioteca/vocabulario/gestor_vocabulario.py'
        if 'red_neuronal' in tl:        return 'biblioteca/red/red_neuronal.py'
        if 'generador_groq' in tl:      return 'capas/capa6/generador_groq.py'
        return ''