# biblioteca/habilidades/memoria/gestor.py
# ============================================================
# GESTOR DE MEMORIA — v2
#
# Motor central de memoria de Bell.
# Una sola clase, un solo SQLite, todo lo que Bell recuerda.
#
# v2:
# — Fix bug SQL buscar_cache_web (dos ? → dos valores)
# — obtener_perfil_sebastian() devuelve string para Groq
# — contexto_completo_para_groq fusiona SQLite + JSON
# — __init__.py exporta correctamente
# ============================================================

import hashlib
import json
import re
import threading
from datetime import datetime
from pathlib import Path
from typing import Optional

from .db import conexion

_lock = threading.Lock()


def _normalizar_query(texto: str) -> str:
    import unicodedata
    texto = texto.lower().strip()
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )


class GestorMemoria:
    """
    Motor central de memoria de Bell.
    Singleton — una sola instancia por proceso.
    """

    def __init__(self):
        self.db = conexion()
        self._sesion_cache: list = []
        self._mem_persistente = None  # lazy — JSON complementario
        self._limpiar_sesion_al_inicio()

    def _obtener_mem_persistente(self):
        """Lazy init de MemoriaPersistente (JSON)."""
        if self._mem_persistente is None:
            try:
                from biblioteca.memoria.memoria_persistente import MemoriaPersistente
                self._mem_persistente = MemoriaPersistente.obtener()
            except Exception:
                self._mem_persistente = None
        return self._mem_persistente

    # ══════════════════════════════════════════════════════
    # SESIÓN ACTUAL
    # ══════════════════════════════════════════════════════

    def _limpiar_sesion_al_inicio(self):
        try:
            sesion_anterior = self.db.execute(
                "SELECT COUNT(*) FROM sesion_actual"
            ).fetchone()[0]
            if sesion_anterior > 4:
                self.cerrar_sesion()
        except Exception:
            pass
        with _lock:
            self.db.execute("DELETE FROM sesion_actual")
        self._sesion_cache = []
        print("  [Memoria] 🧹 Sesión iniciada")

    def guardar_intercambio(self, mensaje_user: str, respuesta_bell: str,
                             tipo: str = '', habilidad: str = '', exitoso: bool = True):
        print(f"  [Memoria] 📝 '{mensaje_user[:40]}' → hab={habilidad or 'ninguna'}")
        with _lock:
            self.db.execute(
                "INSERT INTO sesion_actual (rol, mensaje, tipo, habilidad, exitoso) "
                "VALUES ('user', ?, ?, ?, ?)",
                (mensaje_user, tipo, habilidad, int(exitoso))
            )
            self.db.execute(
                "INSERT INTO sesion_actual (rol, mensaje, tipo, habilidad, exitoso) "
                "VALUES ('bell', ?, ?, ?, ?)",
                (respuesta_bell, tipo, habilidad, int(exitoso))
            )
        self._sesion_cache.append({
            'user': mensaje_user, 'bell': respuesta_bell,
            'tipo': tipo, 'habilidad': habilidad
        })
        if len(self._sesion_cache) > 10:
            self._sesion_cache = self._sesion_cache[-10:]

    def obtener_contexto_sesion(self, n: int = 5) -> list:
        return self._sesion_cache[-n:]

    def contexto_para_groq(self, n: int = 4) -> str:
        ctx = self._sesion_cache[-n:]
        if not ctx:
            return ''
        lines = []
        for ex in ctx:
            lines.append(f"Sebastian: {ex['user'][:120]}")
            lines.append(f"Bell: {ex['bell'][:120]}")
        return "CONTEXTO PREVIO DE ESTA SESIÓN:\n" + '\n'.join(lines)

    def buscar_en_sesion(self, texto: str) -> Optional[str]:
        tl = texto.lower()
        for ex in reversed(self._sesion_cache):
            msg = ex.get('user', '').lower()
            if any(w in msg for w in tl.split() if len(w) > 3):
                return ex.get('user', '')
        return None

    # ══════════════════════════════════════════════════════
    # CONOCIMIENTO APRENDIDO
    # ══════════════════════════════════════════════════════

    def guardar_conocimiento(self, tema: str, respuesta: str,
                              tipo: str = 'general', fuente: str = 'internet',
                              pregunta: str = '', url: str = '',
                              confianza: float = 0.8):
        tema_norm = tema.lower().strip()
        with _lock:
            self.db.execute("""
                INSERT INTO conocimiento
                    (tema, tipo, pregunta, respuesta, fuente, url, confianza)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT DO NOTHING
            """, (tema_norm, tipo, pregunta, respuesta, fuente, url, confianza))

    def consultar_conocimiento(self, tema: str) -> Optional[dict]:
        tema_norm = tema.lower().strip()
        with _lock:
            row = self.db.execute("""
                SELECT * FROM conocimiento
                WHERE vigente = 1
                  AND (tema = ? OR tema LIKE ?)
                ORDER BY confianza DESC, fecha_creacion DESC
                LIMIT 1
            """, (tema_norm, f'%{tema_norm}%')).fetchone()
        if row:
            with _lock:
                self.db.execute(
                    "UPDATE conocimiento SET veces_consultado = veces_consultado + 1, "
                    "fecha_consulta = datetime('now','localtime') WHERE id = ?",
                    (row['id'],)
                )
            return dict(row)
        return None

    def _detectar_tipo_conocimiento(self, pregunta: str) -> str:
        tl = pregunta.lower()
        if any(p in tl for p in ['programacion', 'codigo', 'lenguaje', 'framework',
                                   'docker', 'python', 'rust', 'javascript', 'api']):
            return 'tecnologia'
        if any(p in tl for p in ['quien es', 'cantante', 'actor', 'futbolista',
                                   'presidente', 'artista', 'nacio']):
            return 'persona'
        if any(p in tl for p in ['donde queda', 'pais', 'ciudad', 'capital']):
            return 'lugar'
        if any(p in tl for p in ['musica', 'pelicula', 'serie', 'libro']):
            return 'cultura'
        if any(p in tl for p in ['ciencia', 'biologia', 'quimica', 'fisica',
                                   'matematica', 'formula']):
            return 'ciencia'
        return 'general'

    # ══════════════════════════════════════════════════════
    # BÚSQUEDAS WEB CACHEADAS
    # ══════════════════════════════════════════════════════

    def buscar_cache_web(self, query: str, max_horas: int = 48) -> Optional[str]:
        """
        Revisa si ya se buscó esto recientemente.
        v2 FIX: dos ? → dos valores (query_norm, query_norm).
        """
        query_norm = _normalizar_query(query)
        with _lock:
            # FIX: antes era (query_norm,) con dos ? → crasheaba silenciosamente
            row = self.db.execute("""
                SELECT respuesta, fecha FROM busquedas_web
                WHERE LOWER(query) = ? OR LOWER(query) = ?
                ORDER BY fecha DESC LIMIT 1
            """, (query_norm, query_norm)).fetchone()  # ← FIX: dos valores

        if row:
            try:
                from datetime import datetime as _dt
                fecha_guardada = _dt.fromisoformat(row['fecha'])
                edad = _dt.now() - fecha_guardada
                if edad.total_seconds() > max_horas * 3600:
                    print(f"  [Memoria] ⏰ Cache expirado: '{query_norm[:40]}'")
                    return None
            except Exception:
                pass
            with _lock:
                self.db.execute(
                    "UPDATE busquedas_web SET veces_usada = veces_usada + 1 "
                    "WHERE LOWER(query) = ?", (query_norm,)
                )
            print(f"  [Memoria] ✓ Cache: '{query_norm[:40]}'")
            return row['respuesta']

        return None

    def guardar_busqueda_web(self, query: str, respuesta: str,
                              url: str = '', categoria: str = 'general',
                              calidad: float = 0.7):
        query_norm = _normalizar_query(query)
        tipo = self._detectar_tipo_conocimiento(query)
        if categoria == 'general':
            categoria = tipo
        with _lock:
            self.db.execute("""
                INSERT INTO busquedas_web
                    (query, respuesta, url, categoria, calidad)
                VALUES (?, ?, ?, ?, ?)
            """, (query_norm, respuesta, url, categoria, calidad))
        tema = re.sub(r'\b(wikipedia|definicion|definición|explicacion|que es|quien es)\b',
                      '', query_norm).strip()
        if tema:
            self.guardar_conocimiento(tema, respuesta, tipo, 'internet', query, url, calidad)

    # ══════════════════════════════════════════════════════
    # ARCHIVOS BELL
    # ══════════════════════════════════════════════════════

    def hash_archivo(self, ruta: str) -> str:
        try:
            with open(ruta, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()[:16]
        except Exception:
            return ''

    def necesita_reanalisis(self, ruta: str) -> bool:
        hash_actual = self.hash_archivo(ruta)
        if not hash_actual:
            return False
        with _lock:
            row = self.db.execute(
                "SELECT hash_contenido FROM archivos_bell WHERE ruta = ?",
                (ruta,)
            ).fetchone()
        return row is None or row['hash_contenido'] != hash_actual

    def guardar_analisis_archivo(self, ruta: str, nombre: str,
                                  metricas: dict, resumen_python: str,
                                  analisis_groq: str = ''):
        hash_actual = self.hash_archivo(ruta)
        with _lock:
            self.db.execute("""
                INSERT INTO archivos_bell
                    (ruta, nombre, hash_contenido, lineas, cc_max, mi_score,
                     n_funciones, n_clases, sin_doc, resumen_python, analisis_groq)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(ruta) DO UPDATE SET
                    hash_contenido       = excluded.hash_contenido,
                    lineas               = excluded.lineas,
                    cc_max               = excluded.cc_max,
                    mi_score             = excluded.mi_score,
                    n_funciones          = excluded.n_funciones,
                    n_clases             = excluded.n_clases,
                    sin_doc              = excluded.sin_doc,
                    resumen_python       = excluded.resumen_python,
                    analisis_groq        = CASE WHEN excluded.analisis_groq != ''
                                           THEN excluded.analisis_groq
                                           ELSE archivos_bell.analisis_groq END,
                    ultima_actualizacion = datetime('now','localtime')
            """, (ruta, nombre, hash_actual,
                  metricas.get('lineas', 0), metricas.get('cc_max', 0),
                  metricas.get('mi', 0.0), metricas.get('funciones', 0),
                  metricas.get('clases', 0), metricas.get('sin_doc', 0),
                  resumen_python, analisis_groq))

    def obtener_analisis_archivo(self, nombre: str) -> Optional[dict]:
        with _lock:
            row = self.db.execute(
                "SELECT * FROM archivos_bell WHERE nombre LIKE ? "
                "ORDER BY veces_consultado DESC LIMIT 1",
                (f'%{nombre}%',)
            ).fetchone()
        if row:
            with _lock:
                self.db.execute(
                    "UPDATE archivos_bell SET veces_consultado = veces_consultado + 1 "
                    "WHERE id = ?", (row['id'],)
                )
            return dict(row)
        return None

    def guardar_analisis_groq_archivo(self, ruta: str, analisis_groq: str):
        with _lock:
            self.db.execute(
                "UPDATE archivos_bell SET analisis_groq = ? WHERE ruta = ?",
                (analisis_groq, ruta)
            )

    # ══════════════════════════════════════════════════════
    # CÓDIGO PYTHON
    # ══════════════════════════════════════════════════════

    def guardar_codigo(self, instruccion: str, codigo: str,
                        analisis: str = '', categoria: str = 'general'):
        with _lock:
            self.db.execute("""
                INSERT INTO codigo_python (instruccion, codigo, analisis, categoria)
                VALUES (?, ?, ?, ?)
            """, (instruccion.strip(), codigo.strip(), analisis, categoria))

    def buscar_codigo(self, instruccion: str) -> Optional[dict]:
        tl = instruccion.lower()
        palabras = [w for w in tl.split() if len(w) > 4]
        if not palabras:
            return None
        condiciones = ' OR '.join("instruccion LIKE ?" for _ in palabras)
        params = [f'%{p}%' for p in palabras]
        with _lock:
            row = self.db.execute(
                f"SELECT * FROM codigo_python WHERE {condiciones} "
                "ORDER BY calidad DESC, veces_usado DESC LIMIT 1",
                params
            ).fetchone()
        return dict(row) if row else None

    # ══════════════════════════════════════════════════════
    # DESCONOCIDOS
    # ══════════════════════════════════════════════════════

    def registrar_desconocido(self, palabra: str, contexto: str = ''):
        with _lock:
            self.db.execute("""
                INSERT INTO desconocidos (palabra, contexto)
                VALUES (?, ?)
                ON CONFLICT(palabra) DO UPDATE SET
                    veces_vista = veces_vista + 1,
                    contexto    = CASE WHEN ? != '' THEN ? ELSE contexto END
            """, (palabra.lower(), contexto, contexto, contexto))

    def obtener_desconocidos_pendientes(self, limite: int = 10) -> list:
        with _lock:
            rows = self.db.execute(
                "SELECT palabra, contexto, veces_vista FROM desconocidos "
                "WHERE buscado = 0 ORDER BY veces_vista DESC LIMIT ?",
                (limite,)
            ).fetchall()
        return [dict(r) for r in rows]

    def resolver_desconocido(self, palabra: str, solucion: str):
        with _lock:
            self.db.execute("""
                UPDATE desconocidos
                SET buscado = 1, solucion = ?, resuelto = 1
                WHERE palabra = ?
            """, (solucion, palabra.lower()))

    # ══════════════════════════════════════════════════════
    # FALLAS
    # ══════════════════════════════════════════════════════

    def registrar_falla(self, tipo: str, mensaje: str, respuesta_dada: str = '',
                         razon: str = '', necesita: str = '', habilidad: str = ''):
        with _lock:
            self.db.execute("""
                INSERT INTO fallas_bell
                    (tipo_falla, mensaje_original, respuesta_dada,
                     razon_falla, necesita_para_resolver, habilidad_afectada)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (tipo, mensaje, respuesta_dada, razon, necesita, habilidad))

    def obtener_fallas_recientes(self, limite: int = 5) -> list:
        with _lock:
            rows = self.db.execute(
                "SELECT * FROM fallas_bell WHERE resuelta = 0 "
                "ORDER BY fecha DESC LIMIT ?", (limite,)
            ).fetchall()
        return [dict(r) for r in rows]

    # ══════════════════════════════════════════════════════
    # PERFIL SEBASTIAN
    # ══════════════════════════════════════════════════════

    def actualizar_perfil(self, clave: str, valor: str,
                           tipo: str = 'dato', fuente: str = 'conversacion',
                           confianza: float = 0.8):
        with _lock:
            self.db.execute("""
                INSERT INTO perfil_sebastian (clave, valor, tipo, fuente, confianza)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(clave) DO UPDATE SET
                    valor     = excluded.valor,
                    fuente    = excluded.fuente,
                    confianza = excluded.confianza,
                    fecha     = datetime('now','localtime')
            """, (clave, valor, tipo, fuente, confianza))

    def obtener_perfil(self, clave: str = None) -> dict:
        with _lock:
            if clave:
                row = self.db.execute(
                    "SELECT valor FROM perfil_sebastian WHERE clave = ? AND activo = 1",
                    (clave,)
                ).fetchone()
                return {'valor': row['valor']} if row else {}
            else:
                rows = self.db.execute(
                    "SELECT clave, valor, tipo FROM perfil_sebastian WHERE activo = 1"
                ).fetchall()
                return {r['clave']: r['valor'] for r in rows}

    def obtener_perfil_sebastian(self) -> str:
        """
        v2 NEW: Retorna perfil compacto como string para Groq y búsqueda.
        Fusiona SQLite + JSON (MemoriaPersistente) para máximo contexto.
        """
        perfil = self.obtener_perfil()
        items = []

        # Datos base del SQLite
        if perfil.get('nombre'):    items.append(f"nombre={perfil['nombre']}")
        if perfil.get('ciudad'):    items.append(f"ciudad={perfil['ciudad']}")
        if perfil.get('trabajo'):   items.append(f"trabajo={perfil['trabajo']}")
        if perfil.get('estudio'):   items.append(f"estudio={perfil['estudio']}")
        if perfil.get('proyecto'):  items.append(f"proyecto={perfil['proyecto']}")

        # Enriquecer con JSON si está disponible
        mem_p = self._obtener_mem_persistente()
        if mem_p:
            datos_sd = mem_p.datos_sebastian()
            if datos_sd.get('empresa') and 'trabajo' not in perfil:
                items.append(f"empresa={datos_sd['empresa']}")
            if datos_sd.get('carrera'):
                items.append(f"carrera={datos_sd['carrera']}")

        return ', '.join(items) if items else (
            'nombre=Sebastian, ciudad=Bucaramanga, trabajo=Jelcon, proyecto=BELLADONNA'
        )

    def extraer_datos_sebastian(self, mensaje: str, respuesta: str):
        tl = mensaje.lower()
        _PATRONES = [
            (r'tengo\s+(\d+)\s+a[ñn]os',              'edad',     'dato'),
            (r'vivo\s+en\s+(\w+)',                     'ciudad',   'dato'),
            (r'trabajo\s+(?:en|con)\s+(\w+)',          'trabajo',  'dato'),
            (r'me\s+gusta\s+(?:el|la|los|las)?\s*(\w+)', 'gusto', 'preferencia'),
            (r'mi\s+proyecto\s+(?:es|se\s+llama)\s+(\w+)', 'proyecto', 'proyecto'),
            (r'soy\s+(?:de|del?)\s+(\w+)',             'origen',   'dato'),
        ]
        for patron, clave, tipo in _PATRONES:
            m = re.search(patron, tl)
            if m:
                valor = m.group(m.lastindex or 1)
                if len(valor) > 2:
                    self.actualizar_perfil(clave, valor, tipo, 'Sebastian lo dijo')

    # ══════════════════════════════════════════════════════
    # BELL SELF
    # ══════════════════════════════════════════════════════

    def actualizar_bell_self(self, clave: str, valor: str, categoria: str = 'general'):
        with _lock:
            self.db.execute("""
                INSERT INTO bell_self (clave, valor, categoria)
                VALUES (?, ?, ?)
                ON CONFLICT(clave) DO UPDATE SET
                    valor     = excluded.valor,
                    categoria = excluded.categoria,
                    fecha     = datetime('now','localtime')
            """, (clave, valor, categoria))

    def obtener_bell_self(self) -> dict:
        with _lock:
            rows = self.db.execute(
                "SELECT clave, valor, categoria FROM bell_self"
            ).fetchall()
        return {r['clave']: {'valor': r['valor'], 'cat': r['categoria']}
                for r in rows}

    # ══════════════════════════════════════════════════════
    # EPISODIOS
    # ══════════════════════════════════════════════════════

    def guardar_episodio(self, resumen: str, temas: list,
                          habilidades: list, aprendizajes: str):
        with _lock:
            self.db.execute("""
                INSERT INTO episodios
                    (fecha, resumen, temas, habilidades, aprendizajes, n_intercambios)
                VALUES (datetime('now','localtime'), ?, ?, ?, ?, ?)
            """, (resumen, json.dumps(temas), json.dumps(habilidades),
                  aprendizajes, len(self._sesion_cache)))

    def obtener_episodios_recientes(self, n: int = 3) -> list:
        with _lock:
            rows = self.db.execute(
                "SELECT fecha, resumen, temas FROM episodios "
                "ORDER BY fecha DESC LIMIT ?", (n,)
            ).fetchall()
        return [dict(r) for r in rows]

    # ══════════════════════════════════════════════════════
    # CLARIFICACIONES
    # ══════════════════════════════════════════════════════

    def resolver_clarificacion(self, respuesta_usuario: str) -> Optional[str]:
        tl = respuesta_usuario.lower()
        indicadores = ['me refiero', 'el lenguaje', 'programacion', 'el metal',
                       'la ciudad', 'es el', 'es la', 'framework']
        if not any(p in tl for p in indicadores):
            return None
        for ex in reversed(self._sesion_cache[-5:]):
            prev = ex.get('user', '').lower()
            if any(p in prev for p in ['qué es', 'que es', 'quién es', 'quien es',
                                        'cómo funciona', 'busca', 'dónde']):
                return ex.get('user', '')
        return None

    # ══════════════════════════════════════════════════════
    # DESCONOCIDOS EN SEGUNDO PLANO (L5 búsqueda proactiva)
    # ══════════════════════════════════════════════════════

    def procesar_desconocidos_pendientes(self, max_items: int = 3):
        import threading
        pendientes = self.obtener_desconocidos_pendientes(max_items)
        if not pendientes:
            return

        def _buscar():
            try:
                from biblioteca.habilidades.busqueda.buscador import buscar_web
                for item in pendientes:
                    palabra = item['palabra']
                    contexto = item.get('contexto', '')
                    query = f"qué significa {palabra}" + (
                        f" en contexto {contexto[:30]}" if contexto else ""
                    )
                    resultados = buscar_web(query, max_resultados=2)
                    if resultados:
                        solucion = resultados[0].get('resumen', '')[:200]
                        if solucion:
                            self.resolver_desconocido(palabra, solucion)
                            self.guardar_conocimiento(
                                palabra, solucion, 'general', 'busqueda_automatica'
                            )
                            print(f"  [Memoria] ✅ Aprendí '{palabra}': {solucion[:60]}")
            except Exception as e:
                print(f"  [Memoria] ⚠ Desconocidos: {e}")

        threading.Thread(target=_buscar, daemon=True).start()

    # ══════════════════════════════════════════════════════
    # CERRAR SESIÓN
    # ══════════════════════════════════════════════════════

    def cerrar_sesion(self):
        if len(self._sesion_cache) < 2:
            return
        temas = list(set(
            ex.get('tipo', '') for ex in self._sesion_cache
            if ex.get('tipo') and ex.get('tipo') != 'conversacional'
        ))
        habilidades = list(set(
            ex.get('habilidad', '') for ex in self._sesion_cache
            if ex.get('habilidad')
        ))
        n = len(self._sesion_cache)
        primero = self._sesion_cache[0].get('user', '')[:60]
        ultimo  = self._sesion_cache[-1].get('user', '')[:60]
        resumen = (f"Sesión de {n} intercambios. "
                   f"Comenzó: '{primero}'. Terminó: '{ultimo}'.")
        self.guardar_episodio(resumen, temas, habilidades,
                              f"Habilidades: {', '.join(habilidades) or 'ninguna'}.")
        print(f"  [Memoria] 📖 Episodio guardado: {n} intercambios")

    # ══════════════════════════════════════════════════════
    # APRENDER DE MENSAJES
    # ══════════════════════════════════════════════════════

    def aprender_de_mensaje(self, mensaje: str):
        tl = mensaje.lower()
        _PATRONES = [
            # Sin FYI aquí — FYI va a verificación en C9._procesar_fyi
            (r'(?:o sea|significa que|quiere decir que|se llama)\s+(.{10,80})', 0.75),
            (r'recuerda que\s+(.{10,80})', 0.70),
            (r'te cuento que\s+(.{10,80})', 0.65),
            # FYI sin verificar → confianza baja (0.30), C9 maneja el flujo verificado
            (r'(?:fyi|dato|tip|nota)[:;]\s*(.{10,80})', 0.30),
        ]
        for patron, confianza in _PATRONES:
            m = re.search(patron, tl)
            if m:
                conocimiento = m.group(1).strip()
                if len(conocimiento) > 15:
                    self.guardar_conocimiento(
                        conocimiento[:30], conocimiento,
                        'general', 'sebastian', confianza=confianza
                    )
                    if confianza >= 0.65:
                        print(f"  [Memoria] 📚 Aprendí: '{conocimiento[:50]}'")
                    break

    # ══════════════════════════════════════════════════════
    # BÚSQUEDA SEMÁNTICA
    # ══════════════════════════════════════════════════════

    def buscar_semantico(self, texto: str) -> Optional[str]:
        """
        Búsqueda semántica real usando TF-IDF + cosine similarity.
        Entiende sinónimos y reformulaciones — no solo palabras exactas.
        Fallback a LIKE si TF-IDF no encuentra nada.
        """
        if not texto or len(texto.strip()) < 3:
            return None
        # TF-IDF semántico (primario)
        try:
            from biblioteca.habilidades.memoria.buscador_semantico import buscar_semantico_sqlite
            resultado = buscar_semantico_sqlite(
                texto, self.db,
                tabla='conocimiento',
                campo_texto='respuesta',
                campo_tema='tema',
                min_sim=0.12,
                limit_fetch=300,
            )
            if resultado and len(resultado) > 15:
                print(f'  [Memoria] 🔍 TF-IDF encontró resultado (sim≥0.12)')
                return resultado
        except Exception as e:
            print(f'  [Memoria] TF-IDF error: {e}')

        # Fallback: LIKE básico
        palabras = [w for w in texto.lower().split() if len(w) > 4]
        if not palabras:
            return None
        condiciones = ' OR '.join('tema LIKE ? OR respuesta LIKE ?' for _ in palabras[:4])
        params = []
        for p in palabras[:4]:
            params.extend([f'%{p}%', f'%{p}%'])
        with _lock:
            row = self.db.execute(
                f"SELECT respuesta FROM conocimiento WHERE vigente=1 AND ({condiciones}) "
                "ORDER BY confianza DESC, veces_consultado DESC LIMIT 1",
                params
            ).fetchone()
        if row:
            return row['respuesta']
        return None

    # ══════════════════════════════════════════════════════
    # CONTEXTO PARA GROQ — FUSIÓN SQLite + JSON
    # ══════════════════════════════════════════════════════

    def contexto_completo_para_groq(self, texto_actual: str = '') -> str:
        """
        v2: Fusiona SQLite + MemoriaPersistente (JSON).
        Produce el contexto más rico posible para Bell.
        """
        partes = []

        # 1. Perfil Sebastian compacto
        perfil_str = self.obtener_perfil_sebastian()
        if perfil_str:
            partes.append(f"SEBASTIAN: {perfil_str}")

        # 2. Historia rica del JSON (sesiones anteriores)
        mem_p = self._obtener_mem_persistente()
        if mem_p:
            ctx_rico = mem_p.obtener_contexto_rico()
            if ctx_rico:
                partes.append(ctx_rico)

        # 3. Sesión actual (últimos 3 intercambios)
        ctx_sesion = self._sesion_cache[-3:]
        if ctx_sesion:
            lines = []
            for ex in ctx_sesion:
                lines.append(f"S: {ex['user'][:80]}")
                lines.append(f"B: {ex['bell'][:80]}")
            partes.append("SESIÓN:\n" + '\n'.join(lines))

        # 4. Conocimiento relevante al texto actual
        if texto_actual:
            rel = self.buscar_semantico(texto_actual)
            if rel:
                partes.append(f"RECUERDO: {rel[:120]}")

        return '\n\n'.join(partes) if partes else ''

    def obtener_contexto_rico(self) -> str:
        """Alias para contexto_completo_para_groq — compatibilidad."""
        return self.contexto_completo_para_groq()

    # ══════════════════════════════════════════════════════
    # BELL SELF EVOLUCIONA
    # ══════════════════════════════════════════════════════

    def actualizar_self_post_sesion(self):
        stats = self.estadisticas()
        self.actualizar_bell_self('total_conocimientos', str(stats['conocimientos']), 'metrica')
        self.actualizar_bell_self('total_busquedas',     str(stats['busquedas']),     'metrica')
        self.actualizar_bell_self('palabras_aprendidas', str(stats['desconocidos']),  'metrica')
        self.actualizar_bell_self(
            'ultima_actividad',
            str(__import__('datetime').datetime.now().isoformat()[:16]),
            'metrica'
        )

    # ══════════════════════════════════════════════════════
    # PENDIENTES (compatibilidad con buffer_sesion)
    # ══════════════════════════════════════════════════════

    def obtener_pendientes_relevantes(self) -> list:
        mem_p = self._obtener_mem_persistente()
        if mem_p:
            return mem_p.obtener_pendientes_relevantes()
        return []

    def obtener_temas_para_iniciativa(self) -> list:
        mem_p = self._obtener_mem_persistente()
        if mem_p:
            return mem_p.obtener_temas_para_iniciativa()
        return []

    def tiene_historia(self) -> bool:
        mem_p = self._obtener_mem_persistente()
        if mem_p:
            return mem_p.tiene_historia()
        return self.estadisticas().get('episodios', 0) > 0

    # ══════════════════════════════════════════════════════
    # ESTADÍSTICAS
    # ══════════════════════════════════════════════════════

    def estadisticas(self) -> dict:
        c = self.db
        with _lock:
            return {
                'conocimientos':   c.execute("SELECT COUNT(*) FROM conocimiento WHERE vigente=1").fetchone()[0],
                'busquedas':       c.execute("SELECT COUNT(*) FROM busquedas_web").fetchone()[0],
                'archivos_bell':   c.execute("SELECT COUNT(*) FROM archivos_bell").fetchone()[0],
                'codigo_guardado': c.execute("SELECT COUNT(*) FROM codigo_python").fetchone()[0],
                'desconocidos':    c.execute("SELECT COUNT(*) FROM desconocidos WHERE resuelto=0").fetchone()[0],
                'fallas':          c.execute("SELECT COUNT(*) FROM fallas_bell WHERE resuelta=0").fetchone()[0],
                'episodios':       c.execute("SELECT COUNT(*) FROM episodios").fetchone()[0],
                'perfil_items':    c.execute("SELECT COUNT(*) FROM perfil_sebastian WHERE activo=1").fetchone()[0],
            }


# ── Singleton global ─────────────────────────────────────────
_instancia: Optional[GestorMemoria] = None


def obtener_memoria() -> GestorMemoria:
    global _instancia
    if _instancia is None:
        _instancia = GestorMemoria()
    return _instancia