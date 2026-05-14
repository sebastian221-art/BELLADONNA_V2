# biblioteca/memoria/db.py
# ============================================================
# ESQUEMA Y CONEXIÓN — Base de datos de Bell
#
# Archivo: datos/memoria.db
# Motor:   SQLite (nativo Python, sin servidor)
# ============================================================

import sqlite3
import threading
from pathlib import Path
import os

_lock = threading.Lock()
_conn: sqlite3.Connection | None = None


def _ruta_db() -> Path:
    raiz = os.environ.get('BELL_ROOT', '')
    if not raiz:
        raiz = str(Path(__file__).resolve().parents[3])
    datos = Path(raiz) / 'datos'
    datos.mkdir(exist_ok=True)
    return datos / 'memoria.db'


def conexion() -> sqlite3.Connection:
    global _conn
    if _conn is None:
        with _lock:
            if _conn is None:
                _conn = sqlite3.connect(str(_ruta_db()),
                                        check_same_thread=False,
                                        isolation_level=None)  # autocommit
                _conn.row_factory = sqlite3.Row
                _conn.execute('PRAGMA journal_mode=WAL')
                _conn.execute('PRAGMA foreign_keys=ON')
                _crear_tablas(_conn)
    return _conn


def _crear_tablas(c: sqlite3.Connection) -> None:
    """Crea todas las tablas si no existen."""

    c.executescript("""

    -- ── SESIÓN ACTUAL ────────────────────────────────────────
    -- Últimos intercambios de la conversación en curso.
    -- Se limpia al iniciar Bell.
    CREATE TABLE IF NOT EXISTS sesion_actual (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp   TEXT    NOT NULL DEFAULT (datetime('now','localtime')),
        rol         TEXT    NOT NULL,  -- 'user' | 'bell'
        mensaje     TEXT    NOT NULL,
        tipo        TEXT,              -- tipo_mensaje de C3
        habilidad   TEXT,              -- habilidad usada en C7
        exitoso     INTEGER DEFAULT 1
    );

    -- ── CONOCIMIENTO ─────────────────────────────────────────
    -- Todo lo que Bell ha aprendido: de internet, de Sebastian, de sí misma.
    CREATE TABLE IF NOT EXISTS conocimiento (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        tema            TEXT    NOT NULL,    -- "Maluma", "Docker", "asyncio"
        tipo            TEXT    NOT NULL,    -- persona|lugar|tecnologia|cultura|ciencia|otro
        pregunta        TEXT,
        respuesta       TEXT    NOT NULL,
        fuente          TEXT    NOT NULL,    -- internet|sebastian|groq|autoanalisis
        url             TEXT,
        confianza       REAL    DEFAULT 0.8, -- 0.0-1.0
        veces_consultado INTEGER DEFAULT 0,
        fecha_creacion  TEXT    NOT NULL DEFAULT (datetime('now','localtime')),
        fecha_consulta  TEXT,
        vigente         INTEGER DEFAULT 1    -- 1=activo, 0=desactualizado
    );
    CREATE INDEX IF NOT EXISTS idx_conocimiento_tema ON conocimiento(tema);

    -- ── BUSQUEDAS WEB ─────────────────────────────────────────
    -- Cache de búsquedas de internet, categorizadas.
    CREATE TABLE IF NOT EXISTS busquedas_web (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        query       TEXT    NOT NULL,
        respuesta   TEXT    NOT NULL,
        url         TEXT,
        categoria   TEXT    NOT NULL DEFAULT 'general',
        -- categorias: programacion|personas|lugares|cultura|ciencia|noticias|general
        calidad     REAL    DEFAULT 0.7,  -- 0.0-1.0, Bell evalúa la calidad
        fecha       TEXT    NOT NULL DEFAULT (datetime('now','localtime')),
        veces_usada INTEGER DEFAULT 1
    );
    CREATE INDEX IF NOT EXISTS idx_busquedas_query ON busquedas_web(query);

    -- ── ARCHIVOS BELL ─────────────────────────────────────────
    -- Análisis cacheado de cada archivo de BELLADONNA.
    -- Solo se re-analiza si el hash cambia.
    CREATE TABLE IF NOT EXISTS archivos_bell (
        id                  INTEGER PRIMARY KEY AUTOINCREMENT,
        ruta                TEXT    NOT NULL UNIQUE,
        nombre              TEXT    NOT NULL,
        hash_contenido      TEXT    NOT NULL,
        lineas              INTEGER DEFAULT 0,
        cc_max              INTEGER DEFAULT 0,   -- complejidad ciclomática
        mi_score            REAL    DEFAULT 0,   -- mantenibilidad 0-100
        n_funciones         INTEGER DEFAULT 0,
        n_clases            INTEGER DEFAULT 0,
        sin_doc             INTEGER DEFAULT 0,   -- funciones sin docstring
        resumen_python      TEXT,                -- análisis estructural Python
        analisis_groq       TEXT,                -- análisis profesional Groq
        ultima_actualizacion TEXT   NOT NULL DEFAULT (datetime('now','localtime')),
        veces_consultado    INTEGER DEFAULT 0
    );
    CREATE INDEX IF NOT EXISTS idx_archivos_ruta ON archivos_bell(ruta);

    -- ── CÓDIGO PYTHON ─────────────────────────────────────────
    -- Librería de código acumulada por Bell.
    CREATE TABLE IF NOT EXISTS codigo_python (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        instruccion     TEXT    NOT NULL,    -- "función para ordenar lista"
        codigo          TEXT    NOT NULL,
        lenguaje        TEXT    DEFAULT 'python',
        categoria       TEXT,               -- algoritmos|web|datos|utilidades
        analisis        TEXT,               -- análisis del código guardado
        fecha           TEXT    NOT NULL DEFAULT (datetime('now','localtime')),
        veces_usado     INTEGER DEFAULT 0,
        calidad         REAL    DEFAULT 0.8
    );

    -- ── DESCONOCIDOS ─────────────────────────────────────────
    -- Palabras y conceptos que C1 no reconoció.
    CREATE TABLE IF NOT EXISTS desconocidos (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        palabra     TEXT    NOT NULL,
        contexto    TEXT,                   -- frase donde apareció
        veces_vista INTEGER DEFAULT 1,
        buscado     INTEGER DEFAULT 0,      -- 0=pendiente, 1=buscado
        solucion    TEXT,                   -- lo que se encontró
        fecha       TEXT    NOT NULL DEFAULT (datetime('now','localtime')),
        resuelto    INTEGER DEFAULT 0
    );
    CREATE UNIQUE INDEX IF NOT EXISTS idx_desconocidos_palabra ON desconocidos(palabra);

    -- ── FALLAS BELL ──────────────────────────────────────────
    -- Registro honesto de errores de Bell para que aprenda de ellos.
    CREATE TABLE IF NOT EXISTS fallas_bell (
        id                  INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo_falla          TEXT    NOT NULL,
        -- tipos: vocab_faltante|busqueda_mala|comprension|groq_corte|deteccion_errada|otro
        mensaje_original    TEXT    NOT NULL,
        respuesta_dada      TEXT,
        razon_falla         TEXT,
        necesita_para_resolver TEXT,
        habilidad_afectada  TEXT,
        resuelta            INTEGER DEFAULT 0,
        fecha               TEXT    NOT NULL DEFAULT (datetime('now','localtime')),
        fecha_resolucion    TEXT
    );

    -- ── PERFIL SEBASTIAN ─────────────────────────────────────
    -- Perfil dinámico de Sebastian, construido en tiempo real.
    CREATE TABLE IF NOT EXISTS perfil_sebastian (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        clave       TEXT    NOT NULL UNIQUE,
        valor       TEXT    NOT NULL,
        tipo        TEXT    DEFAULT 'dato',   -- dato|preferencia|patron|proyecto
        confianza   REAL    DEFAULT 0.8,
        fuente      TEXT,                     -- "Sebastian lo dijo"|"inferido"|"búsqueda"
        fecha       TEXT    NOT NULL DEFAULT (datetime('now','localtime')),
        activo      INTEGER DEFAULT 1
    );

    -- ── BELL SELF ────────────────────────────────────────────
    -- Auto-conocimiento de Bell: quién es, qué puede, cómo está.
    CREATE TABLE IF NOT EXISTS bell_self (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        clave       TEXT    NOT NULL UNIQUE,
        valor       TEXT    NOT NULL,
        categoria   TEXT    DEFAULT 'general',
        -- categorias: habilidad|metrica|identidad|logro|aprendizaje
        fecha       TEXT    NOT NULL DEFAULT (datetime('now','localtime'))
    );

    -- ── EPISODIOS ────────────────────────────────────────────
    -- Resúmenes de conversaciones pasadas.
    CREATE TABLE IF NOT EXISTS episodios (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha           TEXT    NOT NULL,
        resumen         TEXT    NOT NULL,
        temas           TEXT,               -- JSON list de temas
        habilidades     TEXT,               -- habilidades usadas
        aprendizajes    TEXT,               -- qué aprendió Bell ese día
        n_intercambios  INTEGER DEFAULT 0
    );

    """)

    # Insertar perfil base de Sebastian si no existe
    c.execute("""
        INSERT OR IGNORE INTO perfil_sebastian (clave, valor, tipo, fuente)
        VALUES
        ('nombre', 'Sebastian Gómez', 'dato', 'sistema'),
        ('edad', '19', 'dato', 'sistema'),
        ('ciudad', 'Bucaramanga', 'dato', 'sistema'),
        ('pais', 'Colombia', 'dato', 'sistema'),
        ('proyecto_principal', 'BELLADONNA', 'proyecto', 'sistema'),
        ('lenguaje_principal', 'Python', 'preferencia', 'sistema')
    """)

    # Insertar identidad base de Bell si no existe
    c.execute("""
        INSERT OR IGNORE INTO bell_self (clave, valor, categoria)
        VALUES
        ('nombre', 'Bell (BELLADONNA)', 'identidad'),
        ('creadora', 'Sebastian Gómez', 'identidad'),
        ('version', '1.0', 'identidad'),
        ('motor_lenguaje', 'openai/gpt-oss-120b via Groq', 'habilidad'),
        ('arquitectura', '9 capas, 8 consejeras', 'identidad')
    """)