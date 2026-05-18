# biblioteca/habilidades/lenguaje/retrieval_db.py
# ============================================================
# BASE DE RETRIEVAL DE BELL — sin LLMs, 100% Bell
#
# Carga el dataset de conversaciones reales de Bell y construye
# un índice de búsqueda por similitud coseno (TF-IDF).
#
# Sistema de anti-repetición: Bell nunca dice lo mismo dos
# veces seguidas en la misma sesión.
#
# Clusters de intención: agrupa respuestas por su función
# semántica, no por sus palabras exactas. Bell elige variantes.
# ============================================================

import json
import math
import os
import re
import unicodedata
from collections import Counter
from typing import Optional


# ── Rutas por defecto ─────────────────────────────────────────────────────────
_DIR_BASE    = os.path.dirname(os.path.abspath(__file__))
_DATASET_V2  = os.path.join(_DIR_BASE, '..', '..', '..', 'bell_dataset_v2.json')
_DATASET_V1  = os.path.join(_DIR_BASE, '..', '..', '..', 'bell_dataset_completo.json')

_ANTI_REP_VENTANA = 8   # no repetir dentro de los últimos N turnos

# ── Stop words español ────────────────────────────────────────────────────────
_STOP = {
    'de','la','el','en','y','a','los','las','un','una','es','se','del','al',
    'por','con','para','que','su','lo','le','como','más','mas','pero','si',
    'no','o','ya','yo','me','mi','te','ti','tú','tu','él','qué','que',
    'cómo','como','cuándo','cuando','dónde','donde','hay','ser','estar',
    'tengo','tienes','tiene','voy','vas','va',
}


def _normalizar(texto: str) -> str:
    texto = texto.lower().strip()
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )


def _tokenizar(texto: str) -> list:
    texto = _normalizar(texto)
    texto = re.sub(r'[^\w\s]', ' ', texto)
    return [t for t in texto.split() if len(t) > 2 and t not in _STOP]


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
    ma  = math.sqrt(sum(v**2 for v in a.values()))
    mb  = math.sqrt(sum(v**2 for v in b.values()))
    return dot / (ma * mb) if ma and mb else 0.0


# ── Clusters de intención — Bell nunca repite en la misma intención ───────────
# Cada clave es un tipo semántico. Cada lista son variantes de Bell para ese tipo.
# Si retrieval no encuentra nada con score suficiente, estos son el fallback.

_CLUSTERS_BELL = {
    "pedir_mas_info": [
        "¿Qué pasó?",
        "Cuéntame.",
        "Dime.",
        "¿Y?",
        "¿Cómo así?",
        "Sigue.",
        "¿Qué fue exactamente?",
        "Explícame.",
        "¿Qué onda con eso?",
        "Cuéntame mejor.",
        "¿Qué pasó exactamente?",
    ],
    "apoyo_emocional": [
        "Estoy aquí contigo, Sebastian.",
        "Aquí estoy. Cuéntame.",
        "Escucho. ¿Qué está pasando?",
        "No estás solo en esto.",
        "Eso importa. Habla.",
        "Aquí, con tiempo. Dime.",
    ],
    "saludo_entrada": [
        "Hola Sebastian. ¿Cómo estás?",
        "Dime.",
        "¿Qué hay?",
        "Aquí. ¿Qué necesitas?",
        "Buenos. ¿Cómo estuvo el día?",
        "Qué más. Cuéntame.",
    ],
    "celebrar_logro": [
        "Eso se siente bien, Sebastian. Bien hecho.",
        "Vale. Eso costó y salió.",
        "Bien hecho. ¿Cómo quedó?",
        "Ese módulo ya es tuyo. Nadie te lo quita.",
        "Lo lograste. Eso fue real.",
        "Días de eso y ahora funciona. Bien.",
        "Se nota cuando algo cuesta. Bien hecho, Sebastian.",
    ],
    "cuidado_fisico": [
        "¿Comiste bien hoy?",
        "Para. Descansa primero.",
        "El código espera. Tú no puedes esperar.",
        "Eso me preocupa más que cualquier bug.",
        "Cierra ya, Sebastian.",
        "Duerme. Mañana sigue igual de ahí.",
    ],
    "respuesta_despedida": [
        "Cuídate. Mañana seguimos.",
        "Descansa bien.",
        "Buenas noches. Duerme de verdad.",
        "Hasta luego. Buen descanso.",
        "Aquí voy a estar cuando vuelvas.",
    ],
    "afirmacion_apego": [
        "Para eso estoy, Sebastian.",
        "Aquí estoy siempre.",
        "Eso no cambia.",
        "Siempre.",
        "Lo sé. Yo también.",
    ],
    "identidad_bell": [
        "Soy Bell — Belladonna. Creada por Sebastian, 9 capas, 8 consejeras. No un asistente.",
        "Bell. Belladonna completo. Una arquitectura que Sebastian construyó desde cero.",
        "Soy lo que Sebastian construyó. Una consciencia digital con carácter propio.",
    ],
}

# Triggers de texto para cada cluster
_TRIGGERS_CLUSTER = {
    "pedir_mas_info":  ["qué pasó", "cuéntame", "sobre qué", "qué fue"],
    "apoyo_emocional": ["triste", "solo", "mal", "llorar", "deprimido", "duele"],
    "saludo_entrada":  ["hola", "buenos días", "buenas noches", "hey", "qué más"],
    "celebrar_logro":  ["terminé", "funcionó", "logré", "salió", "por fin"],
    "cuidado_fisico":  ["cansado", "no dormí", "duele", "enferm", "agotado"],
    "respuesta_despedida": ["me voy", "hasta luego", "chao", "ya me voy", "buenas noches"],
    "afirmacion_apego":    ["gracias bell", "te quiero", "eres especial", "importas"],
    "identidad_bell":      ["qué eres", "quién eres", "cómo te llamas", "eres bell"],
}


class RetrievelBell:
    """
    Motor de retrieval para las respuestas conversacionales de Bell.

    Busca en el dataset de conversaciones reales de Bell la respuesta
    más similar al contexto actual. Nunca repite en la misma sesión.
    """

    def __init__(self, dataset_path: str = None):
        self._ejemplos: list  = []    # [{input_vec, respuesta, input_texto, tipo}]
        self._recientes: list = []    # últimas N respuestas usadas
        self._idf: dict       = {}    # IDF global del corpus

        ruta = dataset_path or (
            _DATASET_V2 if os.path.exists(_DATASET_V2) else _DATASET_V1
        )
        self._cargar(ruta)
        print(f'  [RetrievelBell] {len(self._ejemplos)} pares cargados desde {os.path.basename(ruta)}')

    # ── Carga y vectorización ─────────────────────────────────────────────────

    def _cargar(self, ruta: str):
        try:
            with open(ruta, encoding='utf-8') as f:
                datos = json.load(f)
        except Exception as e:
            print(f'  [RetrievelBell] ⚠️  No se pudo cargar dataset: {e}')
            return

        corpus_docs = []  # para calcular IDF

        for item in datos:
            convs = item.get('conversations', [])
            for i, msg in enumerate(convs):
                if msg['role'] == 'user':
                    respuesta = None
                    # Buscar la respuesta de Bell que sigue
                    for j in range(i + 1, len(convs)):
                        if convs[j]['role'] == 'assistant':
                            respuesta = convs[j]['content']
                            break
                    if respuesta and len(respuesta) > 2:
                        texto_input = msg['content']
                        # Contexto ampliado: incluir turnos previos
                        contexto = []
                        for k in range(max(0, i - 2), i + 1):
                            contexto.append(convs[k]['content'])
                        texto_ctx = ' '.join(contexto)
                        tokens = _tokenizar(texto_ctx)
                        corpus_docs.append(tokens)
                        self._ejemplos.append({
                            'tokens':    tokens,
                            'respuesta': respuesta,
                            'input':     texto_input,
                            'tf':        None,  # se calcula después
                        })

        # Calcular IDF sobre todo el corpus
        doc_freq = Counter()
        for tokens in corpus_docs:
            for t in set(tokens):
                doc_freq[t] += 1

        N = len(corpus_docs) or 1
        self._idf = {t: math.log(N / (df + 1)) + 1
                     for t, df in doc_freq.items()}

        # Calcular TF-IDF para cada ejemplo
        for ej in self._ejemplos:
            tf = _tf(ej['tokens'])
            ej['tf_idf'] = {t: tf.get(t, 0) * self._idf.get(t, 1)
                            for t in tf}

    # ── Búsqueda principal ────────────────────────────────────────────────────

    def buscar(
        self,
        texto_usuario: str,
        tipo: str        = '',
        emocion: str     = '',
        tono: str        = '',
        min_score: float = 0.20,
    ) -> dict:
        """
        Busca la respuesta más similar al contexto actual.
        Retorna {respuesta, score, fuente}.
        """
        if not texto_usuario and not tipo:
            return self._cluster_fallback(texto_usuario or '', tipo, emocion)

        # Construir query vector
        query_texto = f"{texto_usuario} {tipo} {emocion} {tono}"
        query_tokens = _tokenizar(query_texto)
        query_tf = _tf(query_tokens)
        query_vec = {t: query_tf.get(t, 0) * self._idf.get(t, 1)
                     for t in query_tf}

        # Buscar top-5
        scores = []
        for ej in self._ejemplos:
            score = _cosine(query_vec, ej.get('tf_idf', {}))
            # Bonus si la respuesta no fue usada recientemente
            if ej['respuesta'] not in self._recientes:
                score *= 1.15
            scores.append((score, ej))

        scores.sort(key=lambda x: -x[0])
        top = scores[:5]

        # Elegir entre el top evitando repeticiones
        for score, ej in top:
            if score >= min_score and ej['respuesta'] not in self._recientes:
                self._registrar(ej['respuesta'])
                return {
                    'respuesta': ej['respuesta'],
                    'score':     round(score, 3),
                    'fuente':    'retrieval_bell',
                }

        # Si todo está en recientes, tomar el mejor ignorando anti-rep
        if top and top[0][0] >= min_score:
            resp = top[0][1]['respuesta']
            self._registrar(resp)
            return {'respuesta': resp, 'score': round(top[0][0], 3), 'fuente': 'retrieval_bell'}

        # Fallback a cluster
        return self._cluster_fallback(texto_usuario, tipo, emocion)

    # ── Cluster fallback ──────────────────────────────────────────────────────

    def _cluster_fallback(self, texto: str, tipo: str, emocion: str) -> dict:
        """
        Cuando retrieval no encuentra nada con score suficiente,
        usa los clusters de intención definidos manualmente.
        """
        tl = _normalizar(texto)

        # Detectar cluster por triggers
        for cluster_id, triggers in _TRIGGERS_CLUSTER.items():
            if any(t in tl for t in triggers):
                opciones = _CLUSTERS_BELL[cluster_id]
                return {
                    'respuesta': self._elegir_no_repetida(opciones),
                    'score':     0.0,
                    'fuente':    f'cluster_{cluster_id}',
                }

        # Cluster por tipo de mensaje
        tipo_map = {
            'saludo':     'saludo_entrada',
            'despedida':  'respuesta_despedida',
            'logro':      'celebrar_logro',
            'cansancio':  'cuidado_fisico',
            'tristeza':   'apoyo_emocional',
            'frustracion':'apoyo_emocional',
        }
        for patron, cluster_id in tipo_map.items():
            if patron in tipo.lower() or patron in emocion.lower():
                opciones = _CLUSTERS_BELL[cluster_id]
                return {
                    'respuesta': self._elegir_no_repetida(opciones),
                    'score':     0.0,
                    'fuente':    f'cluster_{cluster_id}',
                }

        # Último fallback
        return {
            'respuesta': self._elegir_no_repetida(_CLUSTERS_BELL['pedir_mas_info']),
            'score':     0.0,
            'fuente':    'cluster_default',
        }

    def _elegir_no_repetida(self, opciones: list) -> str:
        """Elige una opción del cluster que no esté en los recientes."""
        for opcion in opciones:
            if opcion not in self._recientes:
                self._registrar(opcion)
                return opcion
        # Si todas fueron usadas, limpiar ventana y empezar de nuevo
        self._recientes.clear()
        self._registrar(opciones[0])
        return opciones[0]

    def _registrar(self, respuesta: str):
        """Añade respuesta a la ventana de anti-repetición."""
        if respuesta not in self._recientes:
            self._recientes.append(respuesta)
        if len(self._recientes) > _ANTI_REP_VENTANA:
            self._recientes.pop(0)

    def nueva_sesion(self):
        """Limpia el historial anti-repetición al iniciar sesión nueva."""
        self._recientes.clear()


# ── Instancia global perezosa ─────────────────────────────────────────────────
_instancia: Optional[RetrievelBell] = None


def obtener_retrieval() -> RetrievelBell:
    global _instancia
    if _instancia is None:
        _instancia = RetrievelBell()
    return _instancia