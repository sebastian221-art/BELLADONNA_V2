# biblioteca/habilidades/python/contexto_maximo.py
# ============================================================
# CONTEXTO MÁXIMO — Todo lo que Bell sabe antes de generar
#
# Antes de generar código, Bell recopila:
#   1. Estilo de Sebastian (TF-IDF sobre su código real)
#   2. Errores frecuentes (historial de Hypothesis)
#   3. Librerías ya usadas (requirements.txt + imports del proyecto)
#   4. Patrones de naming (snake_case, prefijos, convenciones)
#   5. Ejemplos de código similar ya aprobado
#
# El prompt de generación sale con todo esto →
# el código generado sale como si Sebastian mismo lo hubiera escrito.
# ============================================================

import ast
import os
import re
from pathlib import Path
from typing import List, Optional


_RAIZ = Path(os.environ.get('BELL_ROOT', str(Path(__file__).resolve().parents[4])))


def construir_contexto(requerimiento: str, codigo_existente: str = '') -> str:
    """
    Construye el contexto máximo para generación de código.
    Retorna un string XML listo para inyectar al prompt de Groq.
    """
    partes = []

    # 1. Patrón más similar del proyecto
    patron = _buscar_patron_similar(requerimiento)
    if patron:
        partes.append(f'<patron_estilo_sebastian>\n{patron[:600]}\n</patron_estilo_sebastian>')

    # 2. Librerías ya usadas en el proyecto
    libs = _obtener_librerias_usadas()
    if libs:
        partes.append(f'<librerias_del_proyecto>{", ".join(libs[:15])}</librerias_del_proyecto>')

    # 3. Convenciones de naming
    convenciones = _detectar_convenciones()
    if convenciones:
        partes.append(f'<convenciones>\n{convenciones}\n</convenciones>')

    # 4. Errores frecuentes del proyecto
    errores = _obtener_errores_frecuentes()
    if errores:
        partes.append(f'<errores_frecuentes_evitar>\n{errores}\n</errores_frecuentes_evitar>')

    # 5. Código existente como referencia
    if codigo_existente and len(codigo_existente) < 500:
        partes.append(f'<contexto_actual>\n{codigo_existente[:500]}\n</contexto_actual>')

    if not partes:
        return ''

    return '\n'.join(partes)


def _buscar_patron_similar(requerimiento: str) -> str:
    """Busca en el proyecto el código más similar al requerimiento."""
    try:
        from biblioteca.habilidades.python.aprendiz_patrones import AprendizPatrones
        aprendiz = AprendizPatrones.obtener()
        patron = aprendiz.buscar(requerimiento, top_k=1)
        if patron:
            return patron[0].codigo
    except Exception:
        pass
    return ''


def _obtener_librerias_usadas() -> List[str]:
    """Extrae las librerías realmente usadas en el proyecto."""
    libs = set()

    # Leer requirements.txt si existe
    req = _RAIZ / 'requirements.txt'
    if req.exists():
        try:
            for linea in req.read_text().splitlines():
                nombre = re.split(r'[>=<!\[]', linea.strip())[0].strip()
                if nombre and not nombre.startswith('#'):
                    libs.add(nombre.lower())
        except Exception:
            pass

    # Escanear imports del proyecto (muestra parcial)
    archivos_py = list((_RAIZ / 'biblioteca').rglob('*.py'))[:30]
    for archivo in archivos_py:
        try:
            contenido = archivo.read_text(encoding='utf-8', errors='ignore')
            for linea in contenido.splitlines()[:30]:
                m = re.match(r'^(?:import|from)\s+(\w+)', linea)
                if m:
                    lib = m.group(1)
                    if lib not in {'os', 'sys', 're', 'json', 'typing', 'dataclasses',
                                   'pathlib', 'abc', 'copy', 'math', 'time', 'datetime',
                                   'threading', 'collections', 'functools', 'itertools'}:
                        libs.add(lib)
        except Exception:
            pass

    # Priorizar las más relevantes para Python dev
    prioritarias = {'httpx', 'flask', 'fastapi', 'sqlalchemy', 'pydantic', 'numpy',
                    'pandas', 'pytest', 'hypothesis', 'radon', 'mypy', 'black', 'spacy'}
    libs_ordenadas = sorted(libs & prioritarias) + sorted(libs - prioritarias)
    return libs_ordenadas[:20]


def _detectar_convenciones() -> str:
    """Detecta las convenciones de naming del proyecto."""
    convenciones = []
    snake_count = 0
    camel_count  = 0
    prefijos     = {}

    archivos_py = list((_RAIZ / 'biblioteca').rglob('*.py'))[:20]
    for archivo in archivos_py:
        try:
            arbol = ast.parse(archivo.read_text(encoding='utf-8', errors='ignore'))
            for nodo in ast.walk(arbol):
                if isinstance(nodo, ast.FunctionDef):
                    n = nodo.name
                    if '_' in n:
                        snake_count += 1
                    elif n != n.lower():
                        camel_count += 1
                    # Detectar prefijos privados
                    if n.startswith('_'):
                        prefijos['_privado'] = prefijos.get('_privado', 0) + 1
        except Exception:
            pass

    if snake_count > camel_count:
        convenciones.append('- Funciones: snake_case (ej: calcular_total, obtener_nodo)')
    if prefijos.get('_privado', 0) > 3:
        convenciones.append('- Métodos privados con prefijo _ (ej: _procesar, _validar)')
    convenciones.append('- Type hints en todos los parámetros y retornos')
    convenciones.append('- Docstrings en español estilo Google')
    convenciones.append('- Dataclasses para estructuras de datos')

    return '\n'.join(convenciones)


def _obtener_errores_frecuentes() -> str:
    """Obtiene los errores más frecuentes detectados por Hypothesis."""
    try:
        from biblioteca.habilidades.memoria.gestor import obtener_memoria
        mem = obtener_memoria()
        fallas = mem.obtener_fallas_recientes(5)
        if fallas:
            tipos = [f['tipo_falla'] for f in fallas if f.get('tipo_falla')]
            if tipos:
                return 'Evitar: ' + ', '.join(set(tipos[:3]))
    except Exception:
        pass
    return ''