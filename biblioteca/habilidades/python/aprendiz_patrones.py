# biblioteca/habilidades/python/aprendiz_patrones.py
# ============================================================
# APRENDIZ DE PATRONES — aprende del código de Sebastian
#
# Lee todos los archivos .py de BELLADONNA, extrae funciones,
# clases e imports, y construye un índice TF-IDF.
#
# Cuando Sebastian pide código, Bell busca el patrón más similar
# del propio proyecto y lo inyecta como referencia a Groq.
# Así Groq genera código que respeta el estilo exacto de Sebastian.
# ============================================================

import ast
import os
import re
import math
import json
import unicodedata
from collections import Counter
from dataclasses import dataclass
from typing import List, Optional


_STOP = {
    'self', 'cls', 'args', 'kwargs', 'return', 'def', 'class',
    'import', 'from', 'if', 'else', 'elif', 'for', 'while',
    'try', 'except', 'finally', 'with', 'as', 'pass', 'none',
    'true', 'false', 'and', 'or', 'not', 'in', 'is',
}


@dataclass
class PatronCodigo:
    archivo:    str
    nombre:     str      # nombre función/clase
    tipo:       str      # 'funcion' / 'clase' / 'metodo'
    codigo:     str      # código completo del patrón
    tokens:     list
    tf_idf:     dict
    linea:      int = 0


def _normalizar(texto: str) -> str:
    t = texto.lower()
    return ''.join(
        c for c in unicodedata.normalize('NFD', t)
        if unicodedata.category(c) != 'Mn'
    )


def _tokenizar_codigo(codigo: str) -> list:
    """
    Tokeniza código Python extrayendo nombres significativos.
    Divide snake_case en palabras individuales para mejor matching.
    """
    tokens = []
    # Extraer identificadores
    palabras = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', codigo)
    for p in palabras:
        # Dividir snake_case
        partes = p.split('_')
        for parte in partes:
            t = _normalizar(parte)
            if len(t) > 2 and t not in _STOP:
                tokens.append(t)
    return tokens


def _tf(tokens: list) -> dict:
    if not tokens:
        return {}
    c = Counter(tokens)
    total = len(tokens)
    return {t: v / total for t, v in c.items()}


def _cosine(a: dict, b: dict) -> float:
    if not a or not b:
        return 0.0
    dot = sum(a.get(t, 0) * b.get(t, 0) for t in set(a) | set(b))
    ma = math.sqrt(sum(v**2 for v in a.values()))
    mb = math.sqrt(sum(v**2 for v in b.values()))
    return dot / (ma * mb) if ma and mb else 0.0


class AprendizPatrones:
    """
    Lee el código de BELLADONNA y aprende los patrones de Sebastian.
    Funciona como memoria de código — no necesita GPU ni LLM.
    """

    def __init__(self, raiz_proyecto: str = None):
        self._patrones: List[PatronCodigo] = []
        self._idf: dict = {}
        self._raiz = raiz_proyecto or self._detectar_raiz()
        self._indexado = False

    def _detectar_raiz(self) -> str:
        candidatos = [
            '/Users/sebastian/BELLADONNA_V2',
            os.path.expanduser('~/BELLADONNA_V2'),
            os.path.join(os.path.dirname(__file__), '..', '..', '..'),
        ]
        for c in candidatos:
            if os.path.isdir(c):
                return os.path.abspath(c)
        return os.getcwd()

    def indexar(self, forzar: bool = False):
        """Lee todos los .py del proyecto y construye el índice."""
        if self._indexado and not forzar:
            return

        archivos = self._listar_py(self._raiz)
        corpus = []

        for archivo in archivos:
            try:
                with open(archivo, encoding='utf-8', errors='ignore') as f:
                    codigo = f.read()
                patrones = self._extraer_patrones(codigo, archivo)
                for p in patrones:
                    tokens = _tokenizar_codigo(p.codigo)
                    p.tokens = tokens
                    corpus.append(tokens)
                    self._patrones.append(p)
            except Exception:
                pass

        # Calcular IDF global
        doc_freq = Counter()
        for tokens in corpus:
            for t in set(tokens):
                doc_freq[t] += 1

        N = len(corpus) or 1
        self._idf = {t: math.log(N / (df + 1)) + 1 for t, df in doc_freq.items()}

        # Calcular TF-IDF por patrón
        for p in self._patrones:
            tf = _tf(p.tokens)
            p.tf_idf = {t: tf.get(t, 0) * self._idf.get(t, 1) for t in tf}

        self._indexado = True
        print(f'  [AprendizPatrones] {len(self._patrones)} patrones indexados de {len(archivos)} archivos')

    def buscar(self, consulta: str, top_k: int = 3) -> List[PatronCodigo]:
        """Busca los patrones más similares a la consulta."""
        if not self._indexado:
            self.indexar()

        if not self._patrones:
            return []

        tokens_q = _tokenizar_codigo(consulta)
        tf_q = _tf(tokens_q)
        vec_q = {t: tf_q.get(t, 0) * self._idf.get(t, 1) for t in tf_q}

        scores = [(_cosine(vec_q, p.tf_idf), p) for p in self._patrones]
        scores.sort(key=lambda x: -x[0])

        return [p for score, p in scores[:top_k] if score > 0.05]

    def obtener_contexto_groq(self, consulta: str) -> str:
        """
        Retorna los patrones más similares formateados para inyectar
        en el prompt XML de Groq como referencia de estilo.
        """
        if not self._indexado:
            self.indexar()

        patrones = self.buscar(consulta, top_k=2)
        if not patrones:
            return ''

        partes = []
        for p in patrones:
            codigo_ref = p.codigo[:600]  # máx 600 chars por patrón
            partes.append(
                f"# Patrón real de Sebastian en {os.path.basename(p.archivo)}:\n"
                f"{codigo_ref}"
            )

        return '\n\n'.join(partes)

    def _listar_py(self, raiz: str) -> List[str]:
        archivos = []
        excluir = {'__pycache__', '.git', 'venv', 'env', '.venv', 'node_modules'}
        for root, dirs, files in os.walk(raiz):
            dirs[:] = [d for d in dirs if d not in excluir]
            for f in files:
                if f.endswith('.py') and not f.startswith('.'):
                    archivos.append(os.path.join(root, f))
        return archivos

    def _extraer_patrones(self, codigo: str, archivo: str) -> List[PatronCodigo]:
        try:
            arbol = ast.parse(codigo)
        except SyntaxError:
            return []

        lineas = codigo.split('\n')
        patrones = []

        for nodo in ast.walk(arbol):
            if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
                fin = nodo.end_lineno if hasattr(nodo, 'end_lineno') else nodo.lineno + 20
                extracto = '\n'.join(lineas[nodo.lineno - 1:fin])
                if len(extracto) < 30:
                    continue
                patrones.append(PatronCodigo(
                    archivo=archivo,
                    nombre=nodo.name,
                    tipo='funcion',
                    codigo=extracto,
                    tokens=[],
                    tf_idf={},
                    linea=nodo.lineno,
                ))
            elif isinstance(nodo, ast.ClassDef):
                fin = nodo.end_lineno if hasattr(nodo, 'end_lineno') else nodo.lineno + 30
                extracto = '\n'.join(lineas[nodo.lineno - 1:min(fin, nodo.lineno + 25)])
                if len(extracto) < 30:
                    continue
                patrones.append(PatronCodigo(
                    archivo=archivo,
                    nombre=nodo.name,
                    tipo='clase',
                    codigo=extracto,
                    tokens=[],
                    tf_idf={},
                    linea=nodo.lineno,
                ))

        return patrones


_instancia: Optional[AprendizPatrones] = None

def obtener(raiz: str = None) -> AprendizPatrones:
    global _instancia
    if _instancia is None:
        _instancia = AprendizPatrones(raiz)
    return _instancia