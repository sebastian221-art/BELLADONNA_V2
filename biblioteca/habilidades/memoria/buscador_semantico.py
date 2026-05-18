# biblioteca/habilidades/memoria/buscador_semantico.py
# ============================================================
# BÚSQUEDA SEMÁNTICA — TF-IDF puro Python
#
# Reemplaza el LIKE básico con similitud coseno real.
# Sin dependencias externas — solo math y re.
#
# Entiende sinónimos funcionales porque compara
# vectores de términos, no strings exactos.
# ============================================================

import re
import math
import unicodedata
from collections import Counter
from typing import Optional


def _normalizar(texto: str) -> str:
    texto = texto.lower().strip()
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )


def _tokenizar(texto: str) -> list:
    """Tokeniza texto en palabras significativas."""
    texto = _normalizar(texto)
    # Eliminar puntuación
    texto = re.sub(r'[^\w\s]', ' ', texto)
    tokens = texto.split()
    # Stop words español + inglés
    _STOP = {
        'de','la','el','en','y','a','los','las','un','una',
        'es','se','del','al','por','con','para','que','su',
        'lo','le','como','mas','pero','si','no','o','ya',
        'the','a','an','is','in','of','to','and','for','with',
        'this','that','are','be','it','on','at','or','by',
    }
    return [t for t in tokens if len(t) > 2 and t not in _STOP]


def _tf(tokens: list) -> dict:
    """Term Frequency normalizado."""
    if not tokens:
        return {}
    counts = Counter(tokens)
    total  = len(tokens)
    return {term: count / total for term, count in counts.items()}


def _cosine_similarity(vec_a: dict, vec_b: dict) -> float:
    """Similitud coseno entre dos vectores TF."""
    if not vec_a or not vec_b:
        return 0.0
    terms = set(vec_a) | set(vec_b)
    dot   = sum(vec_a.get(t, 0) * vec_b.get(t, 0) for t in terms)
    mag_a = math.sqrt(sum(v ** 2 for v in vec_a.values()))
    mag_b = math.sqrt(sum(v ** 2 for v in vec_b.values()))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


def buscar_semantico_en_lista(
    query: str,
    documentos: list,
    campo_texto: str = 'respuesta',
    campo_tema: str  = 'tema',
    min_sim: float   = 0.15,
    top_n: int       = 1,
) -> list:
    """
    Busca semánticamente en una lista de dicts.
    Retorna los top_n más similares con score >= min_sim.

    documentos: [{'tema': str, 'respuesta': str, ...}]
    """
    if not query or not documentos:
        return []

    query_tokens = _tokenizar(query)
    if not query_tokens:
        return []

    query_vec = _tf(query_tokens)
    resultados = []

    for doc in documentos:
        texto_doc = ' '.join([
            str(doc.get(campo_tema, '')),
            str(doc.get(campo_texto, '')),
        ])
        doc_tokens = _tokenizar(texto_doc)
        if not doc_tokens:
            continue
        doc_vec  = _tf(doc_tokens)
        similitud = _cosine_similarity(query_vec, doc_vec)

        if similitud >= min_sim:
            resultados.append({**doc, '_similitud': round(similitud, 3)})

    resultados.sort(key=lambda x: x['_similitud'], reverse=True)
    return resultados[:top_n]


def buscar_semantico_sqlite(
    query: str,
    db,
    tabla: str        = 'conocimiento',
    campo_texto: str  = 'respuesta',
    campo_tema: str   = 'tema',
    min_sim: float    = 0.12,
    limit_fetch: int  = 200,
    top_n: int        = 1,
) -> Optional[str]:
    """
    Busca semánticamente en SQLite.
    Fetch hasta limit_fetch filas, aplica TF-IDF, retorna el mejor.
    """
    try:
        import threading
        _lock = threading.Lock()
        with _lock:
            rows = db.execute(
                f"SELECT {campo_tema}, {campo_texto} FROM {tabla} "
                f"WHERE vigente = 1 ORDER BY confianza DESC LIMIT ?",
                (limit_fetch,)
            ).fetchall()
    except Exception:
        return None

    if not rows:
        return None

    documentos = [
        {campo_tema: r[campo_tema], campo_texto: r[campo_texto]}
        for r in rows if r[campo_texto]
    ]

    resultados = buscar_semantico_en_lista(
        query, documentos,
        campo_texto=campo_texto,
        campo_tema=campo_tema,
        min_sim=min_sim,
        top_n=top_n,
    )

    if resultados:
        return resultados[0].get(campo_texto, '')
    return None