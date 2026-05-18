# biblioteca/habilidades/auto_analisis/grafo_dependencias.py
# ============================================================
# GRAFO DE DEPENDENCIAS — Bell entiende su propio tejido
#
# Lee todos los imports de cada archivo .py de Bell
# y construye el grafo completo de quién depende de quién.
#
# Pregunta que responde:
#   "Si cambio capa6/generador_groq.py, ¿qué archivos se rompen?"
#   "¿Qué archivos son los más críticos (más importados)?"
# ============================================================

import ast
import os
import re
from pathlib import Path
from collections import defaultdict


_IGNORAR = {'__pycache__', '.git', 'venv', '.venv', 'node_modules'}


def _extraer_imports(ruta: Path, raiz: Path) -> list:
    """Extrae todos los módulos importados en un archivo .py."""
    try:
        with open(ruta, 'r', encoding='utf-8', errors='ignore') as f:
            codigo = f.read()
        tree = ast.parse(codigo)
    except Exception:
        return []

    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)

    # Filtrar solo imports internos de Bell (biblioteca.*, capas.*, etc.)
    internos = []
    for imp in imports:
        partes = imp.split('.')
        # Mapear módulo a ruta relativa
        posible = raiz / Path(*partes).with_suffix('.py')
        if posible.exists():
            internos.append(str(posible.relative_to(raiz)).replace('\\', '/'))
        else:
            # Puede ser un __init__.py
            posible_init = raiz / Path(*partes) / '__init__.py'
            if posible_init.exists():
                internos.append(str((raiz / Path(*partes)).relative_to(raiz)).replace('\\', '/'))

    return internos


def construir_grafo(raiz_str: str) -> dict:
    """
    Construye el grafo completo de dependencias.
    Retorna:
    {
        'depende_de':   {archivo: [archivos que importa]},
        'es_importado_por': {archivo: [archivos que lo importan]},
        'mas_criticos': [(archivo, n_importadores)],
        'huerfanos':    [archivos sin importadores],
        'total_archivos': int,
    }
    """
    raiz = Path(raiz_str)
    depende_de        = defaultdict(list)
    es_importado_por  = defaultdict(list)
    todos_archivos    = []

    for ruta in raiz.rglob('*.py'):
        if any(p in ruta.parts for p in _IGNORAR):
            continue
        rel = str(ruta.relative_to(raiz)).replace('\\', '/')
        todos_archivos.append(rel)
        imports = _extraer_imports(ruta, raiz)
        depende_de[rel] = imports
        for imp in imports:
            es_importado_por[imp].append(rel)

    # Más críticos (más importado por otros)
    mas_criticos = sorted(
        [(archivo, len(importadores))
         for archivo, importadores in es_importado_por.items()
         if len(importadores) > 0],
        key=lambda x: x[1], reverse=True
    )[:15]

    # Huérfanos (nadie los importa, pueden ser entry points o muertos)
    huerfanos = [
        a for a in todos_archivos
        if not es_importado_por.get(a)
        and not a.endswith('__init__.py')
        and 'test' not in a.lower()
    ]

    return {
        'depende_de':       dict(depende_de),
        'es_importado_por': dict(es_importado_por),
        'mas_criticos':     mas_criticos,
        'huerfanos':        huerfanos[:10],
        'total_archivos':   len(todos_archivos),
    }


def impacto_de_cambio(archivo: str, grafo: dict, profundidad: int = 3) -> list:
    """
    Si cambias `archivo`, ¿qué otros archivos podrían romperse?
    Busca recursivamente quién importa este archivo y quién importa a esos.
    """
    archivo = archivo.replace('\\', '/')
    es_importado_por = grafo.get('es_importado_por', {})
    afectados = set()

    def _buscar(nodo: str, nivel: int):
        if nivel <= 0:
            return
        importadores = es_importado_por.get(nodo, [])
        for imp in importadores:
            if imp not in afectados:
                afectados.add(imp)
                _buscar(imp, nivel - 1)

    _buscar(archivo, profundidad)
    return sorted(afectados)


def responder_impacto(texto: str, raiz_str: str) -> str:
    """
    Responde preguntas sobre impacto de cambios.
    Ej: "si cambio capa6/generador_groq.py, qué se rompe"
    """
    # Detectar archivo mencionado
    m = re.search(r'(\w[\w_/]*\.py)', texto, re.IGNORECASE)
    if not m:
        return ''

    nombre = m.group(1).replace('\\', '/')
    grafo  = construir_grafo(raiz_str)

    # Buscar match parcial
    archivo_encontrado = None
    for a in grafo['depende_de']:
        if nombre in a or a.endswith(nombre):
            archivo_encontrado = a
            break

    if not archivo_encontrado:
        criticos_str = ', '.join(f[0].split('/')[-1] for f, _ in grafo['mas_criticos'][:5])
        return (f"No encontré '{nombre}' en el grafo. "
                f"Archivos más importados: {criticos_str}.")

    afectados  = impacto_de_cambio(archivo_encontrado, grafo)
    depende    = grafo['depende_de'].get(archivo_encontrado, [])
    n_importa  = len(es_importado := grafo['es_importado_por'].get(archivo_encontrado, []))

    partes = [f"{archivo_encontrado.split('/')[-1]} es importado por {n_importa} archivo(s)."]

    if afectados:
        nombres = [a.split('/')[-1] for a in afectados[:8]]
        partes.append(f"Si lo cambias, se ven afectados: {', '.join(nombres)}.")
    else:
        partes.append("Nadie lo importa directamente — cambio de bajo impacto.")

    if depende:
        partes.append(f"Depende de: {', '.join(d.split('/')[-1] for d in depende[:5])}.")

    return ' '.join(partes)