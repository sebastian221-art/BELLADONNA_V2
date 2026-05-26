# biblioteca/habilidades/lenguaje/aprendiz.py
# ============================================================
# APRENDIZ — Bell aprende de cada interacción con Groq
#
# Cada vez que Groq comprende bien un mensaje, Bell extrae
# el patrón subyacente y lo guarda. La próxima vez que
# llegue algo similar, Bell lo maneja sola.
#
# Con el tiempo: Bell llama a Groq menos, pero mejor.
# ============================================================

import json
import os
import sqlite3
import time
from pathlib import Path
from typing import Optional

_RAIZ = Path(os.environ.get('BELL_ROOT',
             str(Path(__file__).resolve().parents[4])))
_DB   = _RAIZ / 'datos' / 'aprendizaje_lenguaje.db'
_DB.parent.mkdir(parents=True, exist_ok=True)

# Umbral de similitud para usar patrón aprendido vs llamar a Groq
_UMBRAL_CONFIANZA = 0.82


def _init_db(conn: sqlite3.Connection):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS patrones (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            lemas_clave TEXT NOT NULL,
            tipo        TEXT NOT NULL,
            emocion     TEXT NOT NULL,
            intensidad  REAL,
            necesidad   TEXT,
            respuesta   TEXT,
            usos        INTEGER DEFAULT 1,
            calidad     REAL DEFAULT 0.9,
            creado      REAL
        )
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_lemas ON patrones(lemas_clave)
    """)
    conn.commit()


# ── Similitud entre mensajes ──────────────────────────────

def _lemas_clave(lemas: list) -> str:
    """Extrae los lemas más informativos (excluye stopwords básicas)."""
    _stop = {
        'el','la','los','las','un','una','que','de','en','a','y','o',
        'es','se','su','por','con','para','lo','le','me','te','yo',
        'no','ser','estar','haber','tener','hacer','ir','más','muy',
        'pero','como','si','este','ese','ya','aquí','todo','bien',
    }
    informativos = [l for l in lemas if l not in _stop and len(l) > 2]
    return ' '.join(sorted(informativos)[:8])


def _similitud(lemas_a: str, lemas_b: str) -> float:
    """Similitud de Jaccard entre conjuntos de lemas."""
    set_a = set(lemas_a.split())
    set_b = set(lemas_b.split())
    if not set_a or not set_b:
        return 0.0
    interseccion = set_a & set_b
    union        = set_a | set_b
    return len(interseccion) / len(union)


# ── Clase Aprendiz ────────────────────────────────────────

class Aprendiz:
    """
    Aprende de las comprensiones exitosas de Groq.
    Resuelve casos similares sin llamar a Groq.
    """

    def __init__(self):
        self._conn: Optional[sqlite3.Connection] = None
        self._cache: dict = {}  # lemas_clave → patrón (cache en memoria)
        self._inicializar()

    def _inicializar(self):
        try:
            self._conn = sqlite3.connect(str(_DB), check_same_thread=False)
            _init_db(self._conn)
            self._cargar_cache()
            total = self._conn.execute("SELECT COUNT(*) FROM patrones").fetchone()[0]
            print(f"  [Aprendiz] 📚 {total} patrones cargados")
        except Exception as e:
            print(f"  [Aprendiz] ⚠️ Error inicializando: {e}")
            self._conn = None

    def _cargar_cache(self):
        """Carga los patrones más usados en memoria."""
        if not self._conn:
            return
        try:
            rows = self._conn.execute(
                "SELECT lemas_clave, tipo, emocion, intensidad, "
                "necesidad, respuesta, calidad "
                "FROM patrones WHERE usos >= 2 ORDER BY usos DESC LIMIT 500"
            ).fetchall()
            for row in rows:
                self._cache[row[0]] = {
                    'tipo_mensaje': row[1],
                    'emocion':      row[2],
                    'intensidad':   row[3],
                    'necesidad':    row[4],
                    'respuesta':    row[5],
                    '_calidad':     row[6],
                }
        except Exception:
            pass

    def observar(self, texto: str, analisis: dict, data_groq: dict):
        """
        Bell observa una comprensión exitosa de Groq.
        Extrae el patrón y lo guarda para uso futuro.
        """
        lemas    = analisis.get('lemas', texto.lower().split())
        clave    = _lemas_clave(lemas)

        if not clave or len(clave) < 4:
            return

        tipo      = data_groq.get('tipo_mensaje', '')
        emocion   = data_groq.get('emocion', 'neutra')
        intensidad = float(data_groq.get('intensidad', 0.0))
        necesidad  = data_groq.get('necesidad', '')
        respuesta  = data_groq.get('respuesta', '')

        # Actualizar cache en memoria
        self._cache[clave] = {
            'tipo_mensaje': tipo,
            'emocion':      emocion,
            'intensidad':   intensidad,
            'necesidad':    necesidad,
            'respuesta':    respuesta,
            '_calidad':     0.9,
        }

        # Guardar en SQLite
        if self._conn:
            try:
                existente = self._conn.execute(
                    "SELECT id, usos FROM patrones WHERE lemas_clave = ?",
                    (clave,)
                ).fetchone()

                if existente:
                    self._conn.execute(
                        "UPDATE patrones SET usos = usos + 1, tipo = ?, "
                        "emocion = ?, intensidad = ?, necesidad = ?, respuesta = ? "
                        "WHERE id = ?",
                        (tipo, emocion, intensidad, necesidad, respuesta, existente[0])
                    )
                else:
                    self._conn.execute(
                        "INSERT INTO patrones "
                        "(lemas_clave, tipo, emocion, intensidad, necesidad, respuesta, creado) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (clave, tipo, emocion, intensidad, necesidad, respuesta, time.time())
                    )
                self._conn.commit()
            except Exception as e:
                print(f"  [Aprendiz] ⚠️ Error guardando patrón: {e}")

    def buscar_patron(self, texto: str, analisis: dict) -> Optional[dict]:
        """
        Busca si hay un patrón aprendido similar al mensaje actual.
        Si encuentra uno con alta confianza, Bell lo usa sin llamar a Groq.
        """
        lemas = analisis.get('lemas', texto.lower().split())
        clave = _lemas_clave(lemas)

        if not clave:
            return None

        # Buscar en cache primero (rápido)
        mejor_sim  = 0.0
        mejor_data = None

        for clave_guardada, data in self._cache.items():
            sim = _similitud(clave, clave_guardada)
            if sim > mejor_sim:
                mejor_sim  = sim
                mejor_data = data

        if mejor_sim >= _UMBRAL_CONFIANZA and mejor_data:
            print(f"  [Aprendiz] ⚡ Patrón encontrado (sim={mejor_sim:.2f})")
            return mejor_data

        return None

    def estadisticas(self) -> dict:
        """Devuelve estadísticas del aprendizaje."""
        if not self._conn:
            return {'total': 0, 'en_cache': 0}
        try:
            total = self._conn.execute("SELECT COUNT(*) FROM patrones").fetchone()[0]
            return {
                'total':    total,
                'en_cache': len(self._cache),
            }
        except Exception:
            return {'total': 0, 'en_cache': 0}