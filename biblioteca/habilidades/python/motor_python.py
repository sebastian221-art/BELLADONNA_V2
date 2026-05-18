# biblioteca/habilidades/python/motor_python.py
# ============================================================
# MOTOR PYTHON — orquestador principal v3
#
# Coordina los 5 módulos especializados:
#   AnalizadorCodigo  → AST + Radon + PyFlakes + Pylint + Bandit + Ruff
#   EjecutorCodigo   → subprocess sandbox seguro
#   GeneradorCodigo  → Groq con XML prompt + patrones Sebastian
#   AprendizPatrones → TF-IDF del código real de Bell
#   ExplicadorTecnico → métricas reales + voz Bell
#
# Modos detectados por detector_modo.py:
#   analisis    → analizar código existente
#   debug       → encontrar y explicar el error
#   explicacion → explicar qué hace el código
#   generacion  → crear código nuevo
#   ejecutar    → correr código y mostrar resultado
# ============================================================

import re
from typing import Optional


def ejecutar(texto: str, codigo_adjunto: str = '', modo: str = '',
             contexto: dict = None) -> dict:
    """
    Punto de entrada principal de la habilidad Python.
    Retorna dict con respuesta_texto, codigo_generado, analisis, etc.
    """
    ctx = contexto or {}
    nombre = ctx.get('nombre', 'Sebastian')

    # ── Detectar modo si no viene del C7 ─────────────────────────────────
    if not modo:
        modo = _detectar_modo_local(texto, codigo_adjunto)

    print(f'  [PythonMotor] modo={modo} | codigo_adjunto={bool(codigo_adjunto)}')

    # ── Extraer código del texto si hay bloques ───────────────────────────
    if not codigo_adjunto:
        codigo_adjunto = _extraer_bloque_codigo(texto)

    # ── Enrutar al modo correcto ──────────────────────────────────────────
    if modo == 'analisis':
        return _modo_analisis(codigo_adjunto, nombre)
    elif modo == 'debug':
        return _modo_debug(texto, codigo_adjunto, nombre)
    elif modo == 'explicacion':
        return _modo_explicacion(codigo_adjunto, texto, nombre)
    elif modo == 'ejecutar':
        return _modo_ejecutar(codigo_adjunto, nombre)
    elif modo == 'generacion':
        return _modo_generacion(texto, nombre)
    else:
        # Fallback inteligente
        if codigo_adjunto:
            return _modo_analisis(codigo_adjunto, nombre)
        return _modo_generacion(texto, nombre)


# ── MODO: ANÁLISIS ────────────────────────────────────────────────────────

def _modo_analisis(codigo: str, nombre: str) -> dict:
    if not codigo:
        return _respuesta_pide_codigo(nombre)

    from biblioteca.habilidades.python.analizador_codigo import obtener as get_analizador
    from biblioteca.habilidades.python.explicador_tecnico import obtener as get_explicador

    analisis = get_analizador().analizar(codigo)
    # Pasar codigo_original al explicador — Groq lo usa para explicar QUÉ hace + métricas exactas
    explicacion = get_explicador().explicar_analisis(analisis, codigo_original=codigo)

    return {
        'exitoso':         analisis.es_valido_ast,
        'respuesta_texto': explicacion.texto_completo,
        'analisis':        _serializar_analisis(analisis),
        'sugerencias':     explicacion.sugerencias,
        'habilidad':       'PYTHON_COMPLETO',
        'modo':            'analisis',
    }


# ── MODO: DEBUG ───────────────────────────────────────────────────────────

def _modo_debug(texto: str, codigo: str, nombre: str) -> dict:
    from biblioteca.habilidades.python.analizador_codigo import obtener as get_analizador
    from biblioteca.habilidades.python.ejecutor_codigo   import obtener as get_ejecutor
    from biblioteca.habilidades.python.explicador_tecnico import obtener as get_explicador
    from biblioteca.habilidades.python.generador_codigo  import obtener as get_generador
    from biblioteca.habilidades.python.aprendiz_patrones import obtener as get_aprendiz

    respuesta_partes = []

    # 1. Analizar el código
    if codigo:
        analisis = get_analizador().analizar(codigo)
        errores = [p for p in analisis.problemas if p.tipo == 'error']

        if errores:
            respuesta_partes.append("Encontré estos errores en el análisis estático:")
            for e in errores[:5]:
                respuesta_partes.append(
                    f"  Línea {e.linea} [{e.herramienta}]: {e.mensaje}"
                )

        # 2. Ejecutar para ver el error real
        resultado_ejec = get_ejecutor().ejecutar(codigo)
        if not resultado_ejec.exitoso and resultado_ejec.stderr:
            explicacion_error = get_explicador().explicar_error(resultado_ejec.stderr, codigo)
            respuesta_partes.append('')
            respuesta_partes.append("Al ejecutarlo:")
            respuesta_partes.append(explicacion_error)

            # 3. Pedir a Groq que lo corrija con el error real como contexto
            contexto_debug = (
                f"Código con error:\n{codigo}\n\n"
                f"Error real al ejecutar:\n{resultado_ejec.stderr}"
            )
            patrones = get_aprendiz().obtener_contexto_groq(texto)
            resultado_gen = get_generador().generar(
                requerimiento=f"Corrige este código: {texto}",
                contexto_analisis=contexto_debug,
                patrones_sebastian=patrones,
            )
            if resultado_gen.exitoso and resultado_gen.codigo:
                respuesta_partes.append('')
                respuesta_partes.append("Código corregido:")
                return {
                    'exitoso': True,
                    'respuesta_texto': '\n'.join(respuesta_partes),
                    'codigo_generado': resultado_gen.codigo,
                    'habilidad': 'PYTHON_COMPLETO',
                    'modo': 'debug',
                }
        elif resultado_ejec.exitoso:
            respuesta_partes.append(f"El código corre sin errores. {resultado_ejec.resumen_bell}")

    # Extraer error del texto si no hay código
    elif texto:
        for linea in texto.split('\n'):
            if 'Error' in linea or 'Exception' in linea:
                exp = get_explicador().explicar_error(linea)
                respuesta_partes.append(exp)
                break

    if not respuesta_partes:
        respuesta_partes.append("Muéstrame el código o el traceback completo para hacer el diagnóstico.")

    return {
        'exitoso': True,
        'respuesta_texto': '\n'.join(respuesta_partes),
        'habilidad': 'PYTHON_COMPLETO',
        'modo': 'debug',
    }


# ── MODO: EXPLICACIÓN ─────────────────────────────────────────────────────

def _modo_explicacion(codigo: str, texto: str, nombre: str) -> dict:
    from biblioteca.habilidades.python.analizador_codigo import obtener as get_analizador
    from biblioteca.habilidades.python.explicador_tecnico import obtener as get_explicador
    from biblioteca.habilidades.python.generador_codigo  import obtener as get_generador
    from biblioteca.habilidades.python.aprendiz_patrones import obtener as get_aprendiz

    if not codigo:
        # No hay código adjunto — Groq explica el concepto
        patrones = get_aprendiz().obtener_contexto_groq(texto)
        resultado = get_generador().generar(
            requerimiento=f"Explica con comentarios detallados en español: {texto}",
            patrones_sebastian=patrones,
        )
        texto_resp = resultado.codigo if resultado.exitoso else (
            'Muéstrame el código que quieres que explique.'
        )
        return {
            'exitoso': resultado.exitoso,
            'respuesta_texto': texto_resp,
            'habilidad': 'PYTHON_COMPLETO',
            'modo': 'explicacion',
        }

    analisis = get_analizador().analizar(codigo)
    explicacion = get_explicador().explicar_analisis(analisis, codigo_original=codigo)

    partes = [explicacion.texto_completo]

    if analisis.funciones:
        partes.append('')
        partes.append(f"Tiene {len(analisis.funciones)} función(es):")
        for f in analisis.funciones[:5]:
            args_str = ', '.join(f['args']) if f['args'] else 'sin parámetros'
            partes.append(f"  • {f['nombre']}({args_str})"
                         + (f" → {f['returns']}" if f.get('returns') else ''))

    return {
        'exitoso': True,
        'respuesta_texto': '\n'.join(partes),
        'analisis': _serializar_analisis(analisis),
        'habilidad': 'PYTHON_COMPLETO',
        'modo': 'explicacion',
    }


# ── MODO: EJECUTAR ────────────────────────────────────────────────────────

def _modo_ejecutar(codigo: str, nombre: str) -> dict:
    if not codigo:
        return _respuesta_pide_codigo(nombre)

    from biblioteca.habilidades.python.ejecutor_codigo    import obtener as get_ejecutor
    from biblioteca.habilidades.python.analizador_codigo  import obtener as get_analizador
    from biblioteca.habilidades.python.explicador_tecnico import obtener as get_explicador

    # Analizar primero
    analisis = get_analizador().analizar(codigo)
    errores_estaticos = [p for p in analisis.problemas if p.tipo == 'error']

    if errores_estaticos and not analisis.es_valido_ast:
        return {
            'exitoso': False,
            'respuesta_texto': (
                f"No puedo ejecutar — hay un error de sintaxis:\n"
                f"{errores_estaticos[0].mensaje}"
            ),
            'habilidad': 'PYTHON_COMPLETO',
            'modo': 'ejecutar',
        }

    resultado = get_ejecutor().ejecutar(codigo)

    if resultado.bloqueado:
        return {
            'exitoso': False,
            'respuesta_texto': f"Ejecución bloqueada: {resultado.razon_bloqueo}",
            'habilidad': 'PYTHON_COMPLETO',
            'modo': 'ejecutar',
        }

    partes = [resultado.resumen_bell]
    # No añadir stdout separado — resumen_bell ya lo incluye en ejecución exitosa

    if not resultado.exitoso and resultado.stderr:
        exp = get_explicador().explicar_error(resultado.stderr, codigo)
        partes.append(f"\n{exp}")

    return {
        'exitoso': resultado.exitoso,
        'respuesta_texto': '\n'.join(partes),
        'stdout': resultado.stdout,
        'stderr': resultado.stderr,
        'tiempo_ms': resultado.tiempo_ms,
        'habilidad': 'PYTHON_COMPLETO',
        'modo': 'ejecutar',
    }


# ── MODO: GENERACIÓN ──────────────────────────────────────────────────────

def _modo_generacion(texto: str, nombre: str) -> dict:
    from biblioteca.habilidades.python.generador_codigo  import obtener as get_generador
    from biblioteca.habilidades.python.aprendiz_patrones import obtener as get_aprendiz

    # Obtener patrones similares del código de Sebastian
    patrones = get_aprendiz().obtener_contexto_groq(texto)

    resultado = get_generador().generar(
        requerimiento=texto,
        patrones_sebastian=patrones,
    )

    if resultado.exitoso:
        return {
            'exitoso': True,
            'respuesta_texto': resultado.resumen_bell,
            'codigo_generado': resultado.codigo,
            'habilidad': 'PYTHON_COMPLETO',
            'modo': 'generacion',
        }
    else:
        return {
            'exitoso': False,
            'respuesta_texto': resultado.resumen_bell or 'No pude generar el código.',
            'habilidad': 'PYTHON_COMPLETO',
            'modo': 'generacion',
        }


# ── Utilidades ────────────────────────────────────────────────────────────

def _detectar_modo_local(texto: str, codigo: str) -> str:
    t = texto.lower()
    if any(k in t for k in ['ejecuta', 'corre', 'run', 'prueba esto']):
        return 'ejecutar'
    if any(k in t for k in ['analiza', 'revisa', 'qué problemas', 'qué tan bueno']):
        return 'analisis'
    if any(k in t for k in ['error', 'bug', 'falla', 'traceback', 'no funciona', 'exception']):
        return 'debug'
    if any(k in t for k in ['explica', 'qué hace', 'cómo funciona', 'explícame']):
        return 'explicacion'
    if any(k in t for k in ['genera', 'crea', 'escribe', 'construye', 'hacer una función', 'hacer un']):
        return 'generacion'
    if codigo:
        return 'analisis'
    return 'generacion'


def _limpiar_prefijo_no_python(texto: str) -> str:
    """Elimina texto libre antes del código Python real."""
    lineas = texto.split('\n')
    for i, linea in enumerate(lineas):
        strip = linea.strip()
        if strip.startswith(('def ', 'class ', 'import ', 'from ', '@', '#!')):
            return '\n'.join(lineas[i:])
        if ('=' in strip or strip.startswith(('print', 'if ', 'for ', 'while ', 'try:', 'return', '[', '{'))
                and not strip.endswith(':')):
            return '\n'.join(lineas[i:])
    return texto


def _extraer_bloque_codigo(texto: str) -> str:
    # 1. Bloques markdown
    match = re.search(r'```(?:python)?\s*\n(.*?)```', texto, re.DOTALL)
    if match:
        return _limpiar_prefijo_no_python(match.group(1).strip())

    # 2. Después de palabras trigger
    _TRIGGERS = [
        r'analiza[a-z]*(?:[^\n]*)?[:\s]*\n',
        r'ejecuta[a-z]*(?:[^\n]*)?[:\s]*\n',
        r'explica[a-z]*(?:[^\n]*)?[:\s]*\n',
        r'arr[eé]gla[a-z]*(?:[^\n]*)?[:\s]*\n',
        r'tengo[^\n]*error[^\n]*[:\s]*\n',
        r'revisa[a-z]*(?:[^\n]*)?[:\s]*\n',
        r'corre(?:r)?[^\n]*[:\s]*\n',
    ]
    for patron in _TRIGGERS:
        m = re.search(patron, texto, re.IGNORECASE)
        if m:
            resto = texto[m.end():].strip()
            if len(resto) > 5:
                # Encontrar primera línea Python real (def/class/import/@/código)
                lineas = resto.split('\n')
                inicio = 0
                for i, linea in enumerate(lineas):
                    strip = linea.strip()
                    if strip.startswith(('def ', 'class ', 'import ', 'from ', '@', '#')):
                        inicio = i
                        break
                    if '=' in strip or strip.startswith(('print', 'if ', 'for ', 'while ')):
                        inicio = i
                        break
                return '\n'.join(lineas[inicio:])

    # 3. Líneas con def/class/import
    lineas = texto.split('\n')
    codigo_lineas, en_codigo = [], False
    for linea in lineas:
        if linea.strip().startswith(('def ','class ','import ','from ','@')):
            en_codigo = True
        if en_codigo:
            codigo_lineas.append(linea)
    if len(codigo_lineas) >= 2:
        return '\n'.join(codigo_lineas)

    # 4. Indentación
    bloque = [l for l in lineas if l.startswith('    ') or l.startswith('\t')]
    if len(bloque) >= 3:
        return '\n'.join(bloque)
    return ''

def _respuesta_pide_codigo(nombre: str) -> dict:
    return {
        'exitoso': True,
        'respuesta_texto': f'Muéstrame el código, {nombre}. Puedes pegarlo directamente.',
        'habilidad': 'PYTHON_COMPLETO',
        'modo': 'analisis',
    }


def _serializar_analisis(analisis) -> dict:
    return {
        'cc':            analisis.metricas.cc,
        'mi':            analisis.metricas.mi,
        'loc':           analisis.metricas.loc,
        'nivel_riesgo':  analisis.metricas.nivel_riesgo,
        'es_valido':     analisis.es_valido_ast,
        'n_problemas':   len(analisis.problemas),
        'n_funciones':   len(analisis.funciones),
        'n_clases':      len(analisis.clases),
        'imports':       analisis.imports[:10],
    }


# ── Clase wrapper — interfaz requerida por ejecutor_habilidad.py ──────────────

class MotorPython:
    """
    Wrapper con la interfaz que espera ejecutor_habilidad.py:
        motor = MotorPython.obtener()
        resultado = motor.procesar(texto, modo, verbosidad)
        resultado['exitoso'], resultado['respuesta']
    """
    _inst = None

    @classmethod
    def obtener(cls) -> 'MotorPython':
        if cls._inst is None:
            cls._inst = cls()
            # Pre-indexar patrones de Sebastian al arrancar
            try:
                from biblioteca.habilidades.python.aprendiz_patrones import obtener as get_aprendiz
                get_aprendiz().indexar()
            except Exception as e:
                print(f'  [MotorPython] aprendiz: {e}')
        return cls._inst

    def procesar(self, texto: str, modo: str = '', verbosidad: str = 'normal', **kwargs) -> dict:
        """
        Llama a ejecutar() y normaliza el resultado al formato
        que espera ejecutor_habilidad.py: {exitoso, respuesta, ...}
        """
        # Extraer código adjunto si viene en kwargs
        codigo_adjunto = kwargs.get('codigo_adjunto', '')
        contexto       = kwargs.get('contexto', {})

        resultado = ejecutar(
            texto          = texto,
            codigo_adjunto = codigo_adjunto,
            modo           = modo,
            contexto       = contexto,
        )

        # Normalizar clave respuesta_texto → respuesta
        if 'respuesta_texto' in resultado and 'respuesta' not in resultado:
            resultado['respuesta'] = resultado.pop('respuesta_texto')

        # Si hay código generado, añadirlo a la respuesta
        if resultado.get('codigo_generado') and resultado.get('respuesta'):
            resultado['respuesta'] = (
                resultado['respuesta'] + '\n\n```python\n' +
                resultado['codigo_generado'] + '\n```'
            )

        return resultado