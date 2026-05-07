# biblioteca/habilidades/python/motor_python.py
# ================================================
# MOTOR PYTHON — Habilidad Python
# Entrada principal de la habilidad.
#
# Recibe (texto, modo, verbosidad) y enruta
# a los 5 sub-módulos según el modo detectado.
#
# Mente Pura: toda la lógica es Python puro.
# Groq solo pule el lenguaje en Capa 8.
# ================================================

from typing import Optional


class MotorPython:
    """
    Motor principal de la habilidad Python de Bell.
    Singleton — una instancia por proceso.
    """

    _instancia: Optional['MotorPython'] = None

    def __init__(self):
        self._analizador   = None
        self._generador    = None
        self._explicador   = None
        self._auto         = None
        self._detector     = None

    @classmethod
    def obtener(cls) -> 'MotorPython':
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    # ── Carga lazy de sub-módulos ─────────────────────────────
    def _get_analizador(self):
        if self._analizador is None:
            from biblioteca.habilidades.python.analizador_codigo import AnalizadorCodigo
            self._analizador = AnalizadorCodigo()
        return self._analizador

    def _get_generador(self):
        if self._generador is None:
            from biblioteca.habilidades.python.generador_codigo import GeneradorCodigo
            self._generador = GeneradorCodigo()
        return self._generador

    def _get_explicador(self):
        if self._explicador is None:
            from biblioteca.habilidades.python.explicador_tecnico import ExplicadorTecnico
            self._explicador = ExplicadorTecnico()
        return self._explicador

    def _get_auto(self):
        if self._auto is None:
            from biblioteca.habilidades.python.auto_integrador import AutoIntegrador
            self._auto = AutoIntegrador()
        return self._auto

    def _get_detector(self):
        if self._detector is None:
            from biblioteca.habilidades.python.detector_modo import DetectorModo
            self._detector = DetectorModo()
        return self._detector

    # ── Parser del formato de panel ──────────────────────
    def _extraer_panel(self, texto: str) -> tuple:
        """Extrae instrucción y código del formato [INSTRUCCION][CODIGO]."""
        import re
        instruccion_match = re.search(r'\[INSTRUCCION\](.*?)\[/INSTRUCCION\]', texto, re.DOTALL)
        codigo_match      = re.search(r'\[CODIGO\](.*?)\[/CODIGO\]',           texto, re.DOTALL)
        if instruccion_match and codigo_match:
            return instruccion_match.group(1).strip(), codigo_match.group(1).strip()
        return texto, ''

    # ── Punto de entrada principal ────────────────────────────
    def procesar(
        self,
        texto:      str,
        modo:       str       = 'explicacion',
        verbosidad: str       = 'normal',
    ) -> dict:
        # ── Formato del panel de código ───────────────────────
        # Cuando Sebastian usa el panel, el mensaje llega como:
        # [INSTRUCCION]texto[/INSTRUCCION][CODIGO]código[/CODIGO]
        texto, codigo_panel = self._extraer_panel(texto)
        """
        Procesa el mensaje de Sebastian y retorna la respuesta.

        Args:
            texto:      Mensaje original
            modo:       'analisis' | 'generacion' | 'explicacion' |
                        'debug' | 'auto_analisis'
            verbosidad: 'simple' | 'normal' | 'detallado'

        Returns:
            {
                'exitoso':           bool,
                'respuesta':         str,   # Texto listo para Bell
                'respuesta_fallback': str,  # Si falló, respuesta honesta
                'modo_usado':        str,
                'tiene_codigo':      bool,
                'codigo_generado':   str,
            }
        """
        if not texto or not texto.strip():
            return self._resultado_fallback(modo, 'No recibí texto para procesar.')

        # ── Refinar modo y extraer contenido ─────────────────
        detector  = self._get_detector()
        extraccion = detector.extraer(texto, modo)

        modo_final  = extraccion.get('modo', modo)
        codigo      = extraccion.get('codigo', '')
        descripcion = extraccion.get('descripcion', texto)

        # ── Enrutar al modo correcto ──────────────────────────
        try:
            if modo_final == 'debug' or extraccion.get('tiene_traceback'):
                return self._modo_debug(texto, codigo, descripcion, verbosidad)

            if modo_final == 'auto_analisis':
                return self._modo_auto(
                    texto,
                    extraccion.get('archivo_objetivo', ''),
                    verbosidad
                )

            if modo_final == 'analisis':
                return self._modo_analisis(codigo_panel or codigo or texto, verbosidad)

            if modo_final == 'generacion':
                return self._modo_generacion(descripcion, verbosidad)

            # default: explicacion
            return self._modo_explicacion(descripcion, verbosidad)

        except Exception as e:
            return self._resultado_fallback(
                modo_final,
                f'Encontré un problema procesando eso: {str(e)[:80]}'
            )

    def _fix_indentacion(self, respuesta: str) -> str:
        """Convierte 2-space a 4-space en bloques de codigo. PEP 8."""
        import re as _r

        def _arreglar(codigo: str) -> str:
            lineas = codigo.split('\n')
            # Detectar si alguna linea usa exactamente 2-space de base
            usa_2 = any(
                l.startswith('  ') and not l.startswith('    ')
                for l in lineas if l.strip()
            )
            if not usa_2:
                return codigo
            salida = []
            for l in lineas:
                n = len(l) - len(l.lstrip(' '))
                if n > 0 and n % 2 == 0:
                    salida.append(' ' * (n * 2) + l[n:])
                else:
                    salida.append(l)
            return '\n'.join(salida)

        def _sub(m):
            return m.group(1) + '\n' + _arreglar(m.group(2)) + '```'

        return _r.sub(r'(```[^\n]*)\n(.*?)```', _sub, respuesta, flags=_r.DOTALL)

    def _limpiar_respuesta(self, respuesta: str) -> str:
        """
        Elimina respuestas duplicadas o auto-correcciones de Groq.
        Groq a veces genera la respuesta, luego escribe 'No, mejor así:'
        y la repite. Nos quedamos con la primera versión completa.
        """
        import re
        # Patrones de auto-corrección que Groq genera
        patrones_corte = [
            r'\nNo,\s*mejor\s+así:',
            r'\nMejor\s+así:',
            r'\nCorrecci[oó]n:',
            r'\nActualización:',
            r'\nEn\s+realidad,\s+mejor:',
        ]
        for patron in patrones_corte:
            m = re.search(patron, respuesta, re.IGNORECASE)
            if m:
                # Tomar solo lo que vino antes de la auto-corrección
                parte = respuesta[:m.start()].strip()
                if len(parte) > 50:  # Solo si hay contenido real
                    return parte

        # Detectar segunda aparición de "Oye Sebastian," o "Mira Sebastian,"
        for saludo in ['Oye Sebastian,', 'Mira Sebastian,', 'Oye Sebas,']:
            idx1 = respuesta.find(saludo)
            if idx1 != -1:
                idx2 = respuesta.find(saludo, idx1 + len(saludo))
                if idx2 != -1 and idx2 > 200:  # Segunda aparición real
                    parte = respuesta[:idx2].strip()
                    if len(parte) > 50:
                        return parte

        return respuesta

    # ── MODO ANÁLISIS ─────────────────────────────────────────
    def _modo_analisis(self, codigo: str, verbosidad: str) -> dict:
        analizador = self._get_analizador()
        analisis   = analizador.analizar(codigo, verbosidad)
        respuesta  = analizador.construir_respuesta(analisis, verbosidad)

        respuesta = self._fix_indentacion(respuesta)
        respuesta = self._fix_indentacion(respuesta)
        respuesta = self._limpiar_respuesta(respuesta)
        return {
            'exitoso':          bool(respuesta),
            'respuesta':        respuesta,
            'respuesta_fallback': 'No pude analizar ese código. ¿Puedes pegarlo entre ``` para que lo vea completo?',
            'modo_usado':       'analisis',
            'tiene_codigo':     True,
            'codigo_generado':  '',
        }

    # ── MODO GENERACIÓN ───────────────────────────────────────
    def _modo_generacion(self, descripcion: str, verbosidad: str) -> dict:
        generador = self._get_generador()
        resultado = generador.generar(descripcion, verbosidad)

        if resultado.get('exitoso') and resultado.get('codigo'):
            codigo      = resultado['codigo']
            explicacion = resultado.get('explicacion', '')
            aviso       = resultado.get('aviso_sintaxis', '')
            # Construir respuesta con código intacto
            partes = []
            if explicacion: partes.append(explicacion)
            partes.append(f'```python\n{codigo}\n```')
            if aviso: partes.append(aviso)
            respuesta = '\n\n'.join(partes)
        elif resultado.get('explicacion'):
            respuesta = resultado['explicacion']
        else:
            respuesta = 'No pude generar ese código con los detalles dados.'

        respuesta = self._fix_indentacion(respuesta)
        respuesta = self._limpiar_respuesta(respuesta)
        return {
            'exitoso':            resultado.get('exitoso', False),
            'respuesta':          respuesta,
            'respuesta_fallback': 'Describe con más detalle qué debe hacer el código.',
            'modo_usado':         'generacion',
            'tiene_codigo':       bool(resultado.get('codigo')),
            'codigo_generado':    resultado.get('codigo', ''),
            'explicacion':        resultado.get('explicacion', ''),
            'aviso_sintaxis':     resultado.get('aviso_sintaxis', ''),
        }

    # ── MODO EXPLICACIÓN ──────────────────────────────────────
    def _modo_explicacion(self, consulta: str, verbosidad: str) -> dict:
        explicador = self._get_explicador()
        resultado  = explicador.explicar(consulta, verbosidad)

        return {
            'exitoso':           resultado.get('exitoso', False),
            'respuesta':         resultado.get('respuesta', ''),
            'respuesta_fallback': 'No encontré ese concepto. Prueba con más contexto o pégame el código.',
            'modo_usado':        'explicacion',
            'tiene_codigo':      False,
            'codigo_generado':   '',
        }

    # ── MODO DEBUG ────────────────────────────────────────────
    def _modo_debug(
        self,
        texto:       str,
        codigo:      str,
        descripcion: str,
        verbosidad:  str,
    ) -> dict:
        """
        Bell diagnostica un error. Lee el traceback o error
        y da el diagnóstico en lenguaje natural.
        """
        import re

        respuesta_partes = []

        # ── Detectar tipo de error ────────────────────────────
        error_match = re.search(
            r'(\w+Error|cannot import|ImportError):\s*(.+?)(?:\n|$)',
            texto, re.IGNORECASE
        )
        # Fix: "cannot import name X from Y" pattern
        if not error_match:
            cannot_match = re.search(r'cannot import name (\S+)', texto, re.IGNORECASE)
            if cannot_match:
                # Treat as ImportError
                class _FakeMatch:
                    def group(self, n):
                        return 'ImportError' if n==1 else f'cannot import name {cannot_match.group(1)}'
                error_match = _FakeMatch()
        traceback_match = re.search(
            r'File "(.+?)", line (\d+)',
            texto, re.IGNORECASE
        )
        lineno_match = re.search(
            r'line (\d+)',
            texto, re.IGNORECASE
        )

        if error_match:
            tipo_error  = error_match.group(1)
            mensaje_err = error_match.group(2).strip()

            # Diagnóstico específico por tipo de error
            diagnostico = self._diagnosticar_error(tipo_error, mensaje_err, texto)
            respuesta_partes.append(diagnostico['explicacion'])

            if verbosidad != 'simple':
                if diagnostico.get('causa'):
                    respuesta_partes.append(f'\nCausa probable: {diagnostico["causa"]}')
                if diagnostico.get('solucion'):
                    respuesta_partes.append(f'\nSolución: {diagnostico["solucion"]}')
                if diagnostico.get('ejemplo') and verbosidad == 'detallado':
                    respuesta_partes.append(f'\nEjemplo:\n{diagnostico["ejemplo"]}')
        else:
            # No hay un error explícito — analizar el código si hay
            if codigo:
                return self._modo_analisis(codigo, verbosidad)
            else:
                respuesta_partes.append(
                    'No veo el traceback completo. Pégame el error exacto '
                    '(el texto que aparece en rojo en la terminal) y lo diagnostico.'
                )

        # Información de ubicación
        if traceback_match and verbosidad != 'simple':
            archivo = traceback_match.group(1).split('/')[-1].split('\\')[-1]
            linea   = traceback_match.group(2)
            respuesta_partes.append(f'\nOcurrió en `{archivo}`, línea {linea}.')

        respuesta_base = '\n'.join(respuesta_partes).strip()

        # Si hay Groq disponible y el error es complejo, enriquecer
        groq_key = __import__('os').getenv('GROQ_API_KEY', '')
        if groq_key and respuesta_base and codigo and verbosidad != 'simple':
            try:
                import httpx
                r = httpx.post('https://api.groq.com/openai/v1/chat/completions',
                    headers={'Authorization': f'Bearer {groq_key}', 'Content-Type': 'application/json'},
                    json={'model': 'openai/gpt-oss-120b', 'messages': [
                        {'role': 'system', 'content': (
                            'Eres Bell — senior Python developer. '
                            'Ya tienes el diagnóstico inicial. Amplíalo con: '
                            '(1) La causa exacta en ESTE código específico, '
                            '(2) El fix completo con código ejecutable. '
                            'Máximo 3 párrafos. Sin repetir lo que ya dice el diagnóstico.'
                        )},
                        {'role': 'user', 'content': (
                            f'Diagnóstico inicial:\n{respuesta_base}\n\n'
                            f'Código con el error:\n```python\n{codigo[:2000]}\n```\n\n'
                            f'Error reportado: {texto[:300]}'
                        )}],
                        'temperature': 0.2, 'max_tokens': 600},
                    timeout=40)
                if r.status_code == 200:
                    enriquecido = r.json()['choices'][0]['message']['content'].strip()
                    if enriquecido and len(enriquecido) > 50:
                        respuesta_base = enriquecido
            except Exception:
                pass  # Usar respuesta base sin Groq

        respuesta_base = self._fix_indentacion(respuesta_base)

        return {
            'exitoso':           True,
            'respuesta':         respuesta_base,
            'respuesta_fallback': 'Pégame el error completo y lo diagnostico.',
            'modo_usado':        'debug',
            'tiene_codigo':      bool(codigo),
            'codigo_generado':   '',
        }

    def _diagnosticar_error(self, tipo: str, mensaje: str, contexto: str) -> dict:
        """Diagnóstico específico por tipo de error Python."""
        tl = tipo.lower()
        ml = mensaje.lower()

        if 'modulenotfounderror' in tl or 'importerror' in tl:
            modulo = mensaje.replace("No module named ", "").strip().strip("'\"")
            return {
                'explicacion': f'Python no encuentra el módulo `{modulo}`.',
                'causa': 'No está instalado, o el venv no está activo, o hay un typo.',
                'solucion': f'Prueba: `pip install {modulo}` con el venv activo.',
                'ejemplo': f'# Primero activa el venv:\n# .\\venv\\Scripts\\activate\npip install {modulo}',
            }

        if 'recursionerror' in tl or 'recursion' in tl:
            return {
                'explicacion': '`RecursionError`: la función se llama a sí misma sin parar hasta agotar la pila.',
                'causa': 'Falta el caso base — la condición que detiene la recursión. Sin ella, `factorial(n)` llama a `factorial(n-1)` que llama a `factorial(n-2)`... hasta que Python explota.',
                'solucion': 'Agrega el caso base al inicio:\n```python\ndef factorial(n: int) -> int:\n    if n <= 1:  # CASO BASE — aquí para la recursión\n        return 1\n    return n * factorial(n - 1)\n```',
            }

        if 'typeerror' in tl:
            if 'takes' in ml and 'argument' in ml:
                return {
                    'explicacion': f'Función llamada con el número incorrecto de argumentos.',
                    'causa': 'Pasaste más o menos parámetros de los que la función espera.',
                    'solucion': 'Revisa la firma de la función y cuántos argumentos le pasas.',
                }
            if 'not subscriptable' in ml or 'not iterable' in ml:
                return {
                    'explicacion': f'Intentaste acceder con índice a algo que no es lista/dict/string.',
                    'causa': 'La variable es `None` o un tipo que no soporta indexación.',
                    'solucion': 'Verifica que la variable tenga el valor correcto antes de acceder. Agrega `print(type(variable))` antes de la línea del error.',
                }
            return {
                'explicacion': f'`TypeError`: {mensaje}.',
                'causa': 'Tipo de dato incorrecto para la operación.',
                'solucion': 'Verifica los tipos con `print(type(variable))` antes del error.',
            }

        if 'nameerror' in tl:
            nombre = re.search(r"name '(\w+)' is not defined", mensaje)
            var    = nombre.group(1) if nombre else 'variable'
            return {
                'explicacion': f'`{var}` no está definida en ese punto del código.',
                'causa': 'O no se definió, o se definió después de usarse, o hay un typo.',
                'solucion': f'Busca dónde defines `{var}` y asegúrate que sea antes de usarla.',
            }

        if 'keyerror' in tl:
            clave = mensaje.strip().strip("'\"")
            return {
                'explicacion': f'La clave `{clave}` no existe en el diccionario.',
                'causa': 'El diccionario no tiene esa clave en ese momento.',
                'solucion': f'Usa `.get("{clave}", valor_por_defecto)` para evitar el error, o verifica con `if "{clave}" in mi_dict:` primero.',
            }

        if 'attributeerror' in tl:
            return {
                'explicacion': f'`AttributeError`: {mensaje}.',
                'causa': 'El objeto no tiene ese atributo o método — puede ser `None` cuando no debería.',
                'solucion': 'Verifica con `print(type(objeto))` y `print(objeto)` antes de la línea del error.',
            }

        if 'indexerror' in tl:
            return {
                'explicacion': 'Accediste a un índice que no existe en la lista.',
                'causa': 'La lista está vacía o tiene menos elementos de los esperados.',
                'solucion': 'Verifica `len(lista)` antes de acceder por índice, o usa `if lista:` primero.',
            }

        if 'valueerror' in tl:
            return {
                'explicacion': f'`ValueError`: {mensaje}.',
                'causa': 'Un valor tiene el tipo correcto pero un valor no válido para la operación.',
                'solucion': 'Valida el input antes de procesarlo.',
            }

        if 'indentationerror' in tl or 'syntaxerror' in tl:
            return {
                'explicacion': f'Error de {"indentación" if "indentation" in tl else "sintaxis"}: {mensaje}.',
                'causa': 'Python es estricto con la indentación — mezclar tabs y espacios causa esto.',
                'solucion': 'En VS Code: selecciona todo (Ctrl+A) → Editar → Convertir indentación a espacios.',
            }

        # Error genérico
        return {
            'explicacion': f'`{tipo}`: {mensaje}.',
            'causa': 'Revisa el traceback completo para ver en qué línea ocurrió.',
            'solucion': 'Lee el error de abajo hacia arriba — la línea más útil suele ser la del medio.',
        }

    # ── MODO AUTO-ANÁLISIS ────────────────────────────────────
    def _modo_auto(
        self,
        texto:            str,
        archivo_objetivo: str,
        verbosidad:       str,
    ) -> dict:
        auto      = self._get_auto()
        resultado = auto.analizar_propio(archivo_objetivo or texto, verbosidad)

        return {
            'exitoso':           resultado.get('exitoso', False),
            'respuesta':         resultado.get('respuesta', ''),
            'respuesta_fallback': 'No encontré ese archivo en mi estructura.',
            'modo_usado':        'auto_analisis',
            'tiene_codigo':      False,
            'codigo_generado':   '',
        }

    # ── Helpers ───────────────────────────────────────────────
    def _formatear_generacion(
        self, codigo: str, explicacion: str, verbosidad: str
    ) -> str:
        """Formatea el código generado con su explicación."""
        if verbosidad == 'simple':
            return f'```python\n{codigo}\n```'

        partes = []
        if explicacion:
            partes.append(explicacion)
        partes.append(f'```python\n{codigo}\n```')
        return '\n\n'.join(partes)

    def _resultado_fallback(self, modo: str, razon: str) -> dict:
        mensajes = {
            'analisis':     'Pégame el código entre ``` para analizarlo.',
            'generacion':   'Descríbeme con más detalle qué debe hacer el código.',
            'explicacion':  'Pregúntame sobre un concepto Python específico.',
            'debug':        'Pégame el error completo (el traceback) para diagnosticarlo.',
            'auto_analisis':'Dime qué parte de mi código quieres que revise.',
        }
        return {
            'exitoso':           False,
            'respuesta':         '',
            'respuesta_fallback': mensajes.get(modo, razon),
            'modo_usado':        modo,
            'tiene_codigo':      False,
            'codigo_generado':   '',
        }