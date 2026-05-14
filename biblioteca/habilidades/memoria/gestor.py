# biblioteca/memoria/gestor.py
# ============================================================
# GESTOR DE MEMORIA — El cerebro que crece de Bell
#
# Una sola clase que maneja todas las memorias:
# - Sesión actual (contexto conversación)
# - Conocimiento aprendido (internet + Sebastian)
# - Archivos Bell (auto-análisis cacheado)
# - Código Python (librería acumulada)
# - Desconocidos (gaps de vocabulario)
# - Fallas (registro de errores)
# - Perfil Sebastian (quién es Sebastian)
# - Bell Self (auto-conocimiento)
# - Episodios (conversaciones pasadas)
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
    """Normaliza query: minúsculas + sin acentos para cache robusto."""
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
        self._sesion_cache: list = []   # cache en RAM de sesión actual
        self._limpiar_sesion_al_inicio()

    # ══════════════════════════════════════════════════════
    # SESIÓN ACTUAL
    # ══════════════════════════════════════════════════════

    def _limpiar_sesion_al_inicio(self):
        """Cierra sesión anterior y limpia para la nueva."""        # Cerrar sesión anterior (guardar episodio)
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
        """Guarda un intercambio completo en la sesión actual."""
        print(f"  [Memoria] 📝 Sesión: '{mensaje_user[:40]}' → hab={habilidad or 'ninguna'}")
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
        self._sesion_cache.append({'user': mensaje_user, 'bell': respuesta_bell,
                                    'tipo': tipo, 'habilidad': habilidad})
        if len(self._sesion_cache) > 10:
            self._sesion_cache = self._sesion_cache[-10:]

    def obtener_contexto_sesion(self, n: int = 5) -> list:
        """Retorna los últimos N intercambios de esta sesión."""
        return self._sesion_cache[-n:]

    def contexto_para_groq(self, n: int = 4) -> str:
        """
        Devuelve el contexto de sesión formateado para pasarle a Groq.
        Compacto — máximo 4 intercambios para no saturar el contexto.
        """
        ctx = self._sesion_cache[-n:]
        if not ctx:
            return ''
        lines = []
        for ex in ctx:
            lines.append(f"Sebastian: {ex['user'][:120]}")
            lines.append(f"Bell: {ex['bell'][:120]}")
        return "CONTEXTO PREVIO DE ESTA SESIÓN:\n" + '\n'.join(lines)

    def buscar_en_sesion(self, texto: str) -> Optional[str]:
        """
        Busca en la sesión actual si hay algo relacionado.
        Útil para "me refiero al lenguaje" → encontrar "qué es Rust".
        """
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
        """Guarda algo que Bell aprendió."""
        tema_norm = tema.lower().strip()
        print(f"  [Memoria] 🧠 Conocimiento: '{tema_norm[:35]}' ({tipo}/{fuente})")
        with _lock:
            self.db.execute("""
                INSERT INTO conocimiento
                    (tema, tipo, pregunta, respuesta, fuente, url, confianza)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT DO NOTHING
            """, (tema_norm, tipo, pregunta, respuesta, fuente, url, confianza))

    def consultar_conocimiento(self, tema: str) -> Optional[dict]:
        """
        Bell consulta si ya sabe algo sobre un tema.
        Retorna el conocimiento más confiable y reciente.
        """
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
            # Actualizar contador de consultas
            with _lock:
                self.db.execute(
                    "UPDATE conocimiento SET veces_consultado = veces_consultado + 1, "
                    "fecha_consulta = datetime('now','localtime') WHERE id = ?",
                    (row['id'],)
                )
            return dict(row)
        return None

    def _detectar_tipo_conocimiento(self, pregunta: str) -> str:
        """Detecta el tipo de conocimiento según la pregunta."""
        tl = pregunta.lower()
        if any(p in tl for p in ['programacion', 'codigo', 'lenguaje', 'framework',
                                   'docker', 'python', 'rust', 'javascript', 'api']):
            return 'tecnologia'
        if any(p in tl for p in ['quien es', 'cantante', 'actor', 'futbolista',
                                   'presidente', 'artista', 'nacio']):
            return 'persona'
        if any(p in tl for p in ['donde queda', 'pais', 'ciudad', 'capital',
                                   'continente', 'mapa']):
            return 'lugar'
        if any(p in tl for p in ['musica', 'pelicula', 'serie', 'libro',
                                   'cancion', 'album']):
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
        Evita búsquedas repetidas en internet.
        Usa julianday() para comparación robusta independiente de timezone.
        """
        query_norm = _normalizar_query(query)
        with _lock:
            row = self.db.execute("""
                SELECT respuesta, fecha FROM busquedas_web
                WHERE LOWER(query) = ? OR LOWER(query) = ?
                ORDER BY fecha DESC LIMIT 1
            """, (query_norm,)).fetchone()

        if row:
            from datetime import datetime as _dt
            try:
                fecha_guardada = _dt.fromisoformat(row['fecha'])
                edad = _dt.now() - fecha_guardada
                if edad.total_seconds() > max_horas * 3600:
                    print(f"  [Memoria] ⏰ Cache expirado ({edad.seconds//3600}h): '{query_norm[:40]}'")
                    return None
            except Exception:
                pass

            with _lock:
                self.db.execute(
                    "UPDATE busquedas_web SET veces_usada = veces_usada + 1 "
                    "WHERE LOWER(query) = ?", (query_norm,)
                )
            print(f"  [Memoria] ✓ Cache hit: '{query_norm[:40]}'")
            return row['respuesta']

        print(f"  [Memoria] ○ Sin cache para: '{query_norm[:40]}'")
        return None

    def guardar_busqueda_web(self, query: str, respuesta: str,
                              url: str = '', categoria: str = 'general',
                              calidad: float = 0.7):
        """Guarda una búsqueda web para uso futuro."""
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
        print(f"  [Memoria] 💾 Guardado: '{query_norm[:40]}' (cal={calidad})")
        # También guardar en conocimiento para acceso cruzado
        tema = query_norm.replace('que es ', '').replace('quien es ', '') \
                         .replace('donde queda ', '').strip()
        self.guardar_conocimiento(tema, respuesta, tipo, 'internet',
                                   query, url, calidad)

    # ══════════════════════════════════════════════════════
    # ARCHIVOS BELL (auto-análisis cacheado)
    # ══════════════════════════════════════════════════════

    def hash_archivo(self, ruta: str) -> str:
        """Calcula el hash SHA256 de un archivo."""
        try:
            with open(ruta, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()[:16]
        except Exception:
            return ''

    def necesita_reanalisis(self, ruta: str) -> bool:
        """True si el archivo cambió desde el último análisis."""
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
        """Guarda o actualiza el análisis de un archivo."""
        hash_actual = self.hash_archivo(ruta)
        with _lock:
            self.db.execute("""
                INSERT INTO archivos_bell
                    (ruta, nombre, hash_contenido, lineas, cc_max, mi_score,
                     n_funciones, n_clases, sin_doc, resumen_python, analisis_groq)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(ruta) DO UPDATE SET
                    hash_contenido = excluded.hash_contenido,
                    lineas         = excluded.lineas,
                    cc_max         = excluded.cc_max,
                    mi_score       = excluded.mi_score,
                    n_funciones    = excluded.n_funciones,
                    n_clases       = excluded.n_clases,
                    sin_doc        = excluded.sin_doc,
                    resumen_python = excluded.resumen_python,
                    analisis_groq  = CASE WHEN excluded.analisis_groq != ''
                                     THEN excluded.analisis_groq
                                     ELSE archivos_bell.analisis_groq END,
                    ultima_actualizacion = datetime('now','localtime')
            """, (ruta, nombre, hash_actual,
                  metricas.get('lineas', 0), metricas.get('cc_max', 0),
                  metricas.get('mi', 0.0), metricas.get('funciones', 0),
                  metricas.get('clases', 0), metricas.get('sin_doc', 0),
                  resumen_python, analisis_groq))

    def obtener_analisis_archivo(self, nombre: str) -> Optional[dict]:
        """Obtiene el análisis cacheado de un archivo por nombre."""
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
        """Actualiza solo el análisis Groq de un archivo."""
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
        """Guarda un snippet de código en la librería de Bell."""
        with _lock:
            self.db.execute("""
                INSERT INTO codigo_python (instruccion, codigo, analisis, categoria)
                VALUES (?, ?, ?, ?)
            """, (instruccion.strip(), codigo.strip(), analisis, categoria))

    def buscar_codigo(self, instruccion: str) -> Optional[dict]:
        """Busca código similar ya generado."""
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
    # DESCONOCIDOS (gaps de vocabulario)
    # ══════════════════════════════════════════════════════

    def registrar_desconocido(self, palabra: str, contexto: str = ''):
        """Registra una palabra que Bell no reconoció."""
        print(f"  [Memoria] ❓ Desconocido: '{palabra}'")
        with _lock:
            self.db.execute("""
                INSERT INTO desconocidos (palabra, contexto)
                VALUES (?, ?)
                ON CONFLICT(palabra) DO UPDATE SET
                    veces_vista = veces_vista + 1,
                    contexto    = CASE WHEN ? != '' THEN ? ELSE contexto END
            """, (palabra.lower(), contexto, contexto, contexto))

    def obtener_desconocidos_pendientes(self, limite: int = 10) -> list:
        """Retorna palabras desconocidas pendientes de buscar."""
        with _lock:
            rows = self.db.execute(
                "SELECT palabra, contexto, veces_vista FROM desconocidos "
                "WHERE buscado = 0 ORDER BY veces_vista DESC LIMIT ?",
                (limite,)
            ).fetchall()
        return [dict(r) for r in rows]

    def resolver_desconocido(self, palabra: str, solucion: str):
        """Marca una palabra desconocida como resuelta."""
        with _lock:
            self.db.execute("""
                UPDATE desconocidos
                SET buscado = 1, solucion = ?, resuelto = 1
                WHERE palabra = ?
            """, (solucion, palabra.lower()))

    # ══════════════════════════════════════════════════════
    # FALLAS DE BELL
    # ══════════════════════════════════════════════════════

    def registrar_falla(self, tipo: str, mensaje: str,
                         respuesta_dada: str = '',
                         razon: str = '', necesita: str = '',
                         habilidad: str = ''):
        """
        Bell registra honestamente que falló y por qué.
        Tipos: vocab_faltante | busqueda_mala | comprension |
               groq_corte | deteccion_errada | otro
        """
        with _lock:
            self.db.execute("""
                INSERT INTO fallas_bell
                    (tipo_falla, mensaje_original, respuesta_dada,
                     razon_falla, necesita_para_resolver, habilidad_afectada)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (tipo, mensaje, respuesta_dada, razon, necesita, habilidad))

    def generar_mensaje_falla(self, tipo: str, razon: str,
                               necesita: str) -> str:
        """
        Genera el mensaje que Bell le da a Sebastian cuando falla.
        Honesto, directo, sin excusas.
        """
        msgs = {
            'vocab_faltante': (
                f"Sebastian, fallé porque no tengo '{necesita}' en mi vocabulario. "
                f"Lo registré. Cuando tenga búsqueda activa lo buscaré y aprenderé. "
                f"¿Puedes darme más contexto de qué significa?"
            ),
            'busqueda_mala': (
                f"Busqué en internet pero encontré contenido que no respondía bien. "
                f"Lo guardé como falla para mejorar. Razon: {razon}."
            ),
            'comprension': (
                f"No entendí bien tu mensaje. {razon}. "
                f"¿Puedes reformularlo o darme más contexto?"
            ),
            'groq_corte': (
                f"Mi respuesta se cortó porque el modelo tiene límites de contexto. "
                f"Estoy trabajando en esto. Por ahora te doy lo más importante."
            ),
            'deteccion_errada': (
                f"Activé la habilidad equivocada. {razon}. "
                f"Lo registro para mejorar mi detección."
            ),
        }
        return msgs.get(tipo, f"Fallé: {razon}. Lo registré para mejorar.")

    def obtener_fallas_recientes(self, limite: int = 5) -> list:
        """Retorna las fallas más recientes sin resolver."""
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
        """Actualiza o crea un dato del perfil de Sebastian."""
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
        """Obtiene el perfil completo o un dato específico."""
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

    def extraer_datos_sebastian(self, mensaje: str, respuesta: str):
        """
        Analiza el mensaje de Sebastian para extraer datos de su perfil.
        Detecta gustos, proyectos, información personal.
        """
        tl = mensaje.lower()
        # Patrones de auto-revelación
        _PATRONES = [
            (r'tengo\s+(\d+)\s+a[ñn]os',        'edad',         'dato'),
            (r'vivo\s+en\s+(\w+)',               'ciudad',       'dato'),
            (r'trabajo\s+(en|con)\s+(\w+)',      'trabajo',      'dato'),
            (r'me\s+gusta\s+(?:el|la|los|las)?\s*(\w+)', 'gusto', 'preferencia'),
            (r'mi\s+proyecto\s+(?:es|se\s+llama)\s+(\w+)', 'proyecto', 'proyecto'),
            (r'soy\s+(?:de|del?)\s+(\w+)',       'origen',       'dato'),
        ]
        for patron, clave, tipo in _PATRONES:
            m = re.search(patron, tl)
            if m:
                valor = m.group(m.lastindex or 1)
                if len(valor) > 2:
                    self.actualizar_perfil(clave, valor, tipo, 'Sebastian lo dijo')

    def contexto_sebastian_para_groq(self) -> str:
        """Devuelve el perfil de Sebastian en formato compacto para Groq."""
        perfil = self.obtener_perfil()
        if not perfil:
            return ''
        items = [f"{k}={v}" for k, v in list(perfil.items())[:8]]
        return f"PERFIL SEBASTIAN: {', '.join(items)}"

    # ══════════════════════════════════════════════════════
    # BELL SELF (auto-conocimiento)
    # ══════════════════════════════════════════════════════

    def actualizar_bell_self(self, clave: str, valor: str,
                              categoria: str = 'general'):
        """Bell actualiza su auto-conocimiento."""
        with _lock:
            self.db.execute("""
                INSERT INTO bell_self (clave, valor, categoria)
                VALUES (?, ?, ?)
                ON CONFLICT(clave) DO UPDATE SET
                    valor    = excluded.valor,
                    categoria = excluded.categoria,
                    fecha    = datetime('now','localtime')
            """, (clave, valor, categoria))

    def obtener_bell_self(self) -> dict:
        """Retorna el auto-conocimiento de Bell."""
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
        """Guarda el resumen de la conversación actual como episodio."""
        with _lock:
            self.db.execute("""
                INSERT INTO episodios
                    (fecha, resumen, temas, habilidades, aprendizajes, n_intercambios)
                VALUES (datetime('now','localtime'), ?, ?, ?, ?, ?)
            """, (resumen, json.dumps(temas), json.dumps(habilidades),
                  aprendizajes, len(self._sesion_cache)))

    def obtener_episodios_recientes(self, n: int = 3) -> list:
        """Retorna los N episodios más recientes."""
        with _lock:
            rows = self.db.execute(
                "SELECT fecha, resumen, temas FROM episodios "
                "ORDER BY fecha DESC LIMIT ?", (n,)
            ).fetchall()
        return [dict(r) for r in rows]

    # ══════════════════════════════════════════════════════
    # NIVEL 3 — CLARIFICACIONES USANDO SESIÓN
    # ══════════════════════════════════════════════════════

    def resolver_clarificacion(self, respuesta_usuario: str) -> Optional[str]:
        """
        Si el usuario responde a una clarificación de Bell,
        busca en sesión la pregunta original para retomarla.
        Retorna la pregunta original o None.
        """
        tl = respuesta_usuario.lower()
        indicadores = ['me refiero', 'el lenguaje', 'programacion',
                       'el metal', 'el oxide', 'la ciudad', 'es el', 'es la']
        if not any(p in tl for p in indicadores):
            return None
        # Buscar última pregunta de búsqueda en sesión
        for ex in reversed(self._sesion_cache[-5:]):
            prev = ex.get('user', '').lower()
            if any(p in prev for p in ['qué es', 'que es', 'quién es', 'quien es',
                                        'cómo funciona', 'busca', 'dónde']):
                return ex.get('user', '')
        return None

    # ══════════════════════════════════════════════════════
    # NIVEL 4 — DESCONOCIDOS → BÚSQUEDA AUTOMÁTICA
    # ══════════════════════════════════════════════════════

    def procesar_desconocidos_pendientes(self, max_items: int = 3):
        """
        Lanza búsquedas automáticas en segundo plano
        para palabras desconocidas acumuladas.
        """
        import threading
        pendientes = self.obtener_desconocidos_pendientes(max_items)
        if not pendientes:
            return

        def _buscar_desconocidos():
            try:
                from biblioteca.habilidades.busqueda.buscador import buscar_web
                for item in pendientes:
                    palabra = item['palabra']
                    contexto = item.get('contexto', '')
                    query = f"qué significa {palabra}" + (f" en contexto {contexto[:30]}" if contexto else "")
                    resultados = buscar_web(query, max_resultados=2)
                    if resultados:
                        solucion = resultados[0].get('resumen', '')[:200]
                        if solucion:
                            self.resolver_desconocido(palabra, solucion)
                            self.guardar_conocimiento(palabra, solucion, 'general',
                                                       'busqueda_automatica')
                            print(f"  [Memoria] ✅ Aprendí: '{palabra}' → {solucion[:60]}")
            except Exception as e:
                print(f"  [Memoria] ⚠ Error buscando desconocidos: {e}")

        hilo = threading.Thread(target=_buscar_desconocidos, daemon=True)
        hilo.start()

    # ══════════════════════════════════════════════════════
    # NIVEL 5 — EPISODIOS AL CERRAR SESIÓN
    # ══════════════════════════════════════════════════════

    def cerrar_sesion(self):
        """
        Guarda el episodio de esta sesión antes de cerrar.
        Se llama automáticamente al reiniciar Bell.
        """
        if len(self._sesion_cache) < 2:
            return  # sesión muy corta, no guardar

        # Extraer temas y habilidades usadas
        temas = list(set(
            ex.get('tipo', '') for ex in self._sesion_cache
            if ex.get('tipo') and ex.get('tipo') != 'conversacional'
        ))
        habilidades = list(set(
            ex.get('habilidad', '') for ex in self._sesion_cache
            if ex.get('habilidad')
        ))

        # Resumen automático del episodio
        n = len(self._sesion_cache)
        primero = self._sesion_cache[0].get('user', '')[:60]
        ultimo = self._sesion_cache[-1].get('user', '')[:60]
        resumen = (f"Sesión de {n} intercambios. "
                   f"Comenzó con: '{primero}'. "
                   f"Terminó con: '{ultimo}'.")

        aprendizajes = f"Habilidades: {', '.join(habilidades) or 'ninguna'}."

        self.guardar_episodio(resumen, temas, habilidades, aprendizajes)
        print(f"  [Memoria] 📖 Episodio guardado: {n} intercambios")

    def saludo_inicio_sesion(self) -> str:
        """
        Bell genera un saludo personalizado al inicio de sesión
        basado en episodios anteriores y perfil de Sebastian.
        """
        episodios = self.obtener_episodios_recientes(1)
        perfil = self.obtener_perfil()
        stats = self.estadisticas()

        if not episodios:
            return ''

        ep = episodios[0]
        nombre = perfil.get('nombre', 'Sebastian')
        busquedas = stats.get('busquedas', 0)
        conocimientos = stats.get('conocimientos', 0)

        return (f"Bienvenido de vuelta, {nombre}. "
                f"Recuerdo nuestra última sesión: {ep['resumen'][:80]}. "
                f"Tengo {conocimientos} cosas aprendidas y {busquedas} búsquedas en memoria.")

    # ══════════════════════════════════════════════════════
    # NIVEL 6 — BELL SELF EVOLUCIONA EN TIEMPO REAL
    # ══════════════════════════════════════════════════════

    def actualizar_self_post_sesion(self):
        """Bell actualiza su auto-conocimiento después de cada intercambio."""
        stats = self.estadisticas()
        self.actualizar_bell_self('total_conocimientos',
                                   str(stats['conocimientos']), 'metrica')
        self.actualizar_bell_self('total_busquedas',
                                   str(stats['busquedas']), 'metrica')
        self.actualizar_bell_self('palabras_aprendidas',
                                   str(stats['desconocidos']), 'metrica')
        self.actualizar_bell_self('ultima_actividad',
                                   str(__import__('datetime').datetime.now().isoformat()[:16]),
                                   'metrica')

    # ══════════════════════════════════════════════════════
    # NIVEL 7 — BELL APRENDE DE CONVERSACIONES
    # ══════════════════════════════════════════════════════

    def aprender_de_mensaje(self, mensaje: str):
        """
        Detecta cuando Sebastian está enseñando algo a Bell.
        Guarda el conocimiento automáticamente.
        """
        tl = mensaje.lower()
        # Patrones de enseñanza explícita
        _PATRONES = [
            r'(?:es que|o sea|significa que|quiere decir que|se llama)\s+(.{10,80})',
            r'(?:fyi|dato|tip|nota)[:;]\s*(.{10,80})',
            r'recuerda que\s+(.{10,80})',
            r'te cuento que\s+(.{10,80})',
        ]
        import re
        for patron in _PATRONES:
            m = re.search(patron, tl)
            if m:
                conocimiento = m.group(1).strip()
                if len(conocimiento) > 15:
                    self.guardar_conocimiento(
                        tema=conocimiento[:30],
                        respuesta=conocimiento,
                        tipo='general',
                        fuente='sebastian',
                        confianza=0.9
                    )
                    print(f"  [Memoria] 📚 Aprendí de Sebastian: '{conocimiento[:50]}'")
                    break

    # ══════════════════════════════════════════════════════
    # NIVEL 8 — BÚSQUEDA SEMÁNTICA EN MEMORIA
    # ══════════════════════════════════════════════════════

    def buscar_semantico(self, texto: str) -> Optional[str]:
        """
        Busca en toda la memoria (conocimiento + búsquedas)
        algo relacionado con el texto.
        Más flexible que la búsqueda exacta.
        """
        palabras = [w for w in texto.lower().split() if len(w) > 4]
        if not palabras:
            return None

        condiciones = ' OR '.join('tema LIKE ? OR respuesta LIKE ?' for _ in palabras)
        params = []
        for p in palabras:
            params.extend([f'%{p}%', f'%{p}%'])

        with _lock:
            row = self.db.execute(
                f"SELECT respuesta FROM conocimiento WHERE vigente=1 AND ({condiciones}) "
                "ORDER BY confianza DESC, veces_consultado DESC LIMIT 1",
                params
            ).fetchone()

        if row:
            print(f"  [Memoria] 🔍 Búsqueda semántica encontró resultado")
            return row['respuesta']
        return None

    # ══════════════════════════════════════════════════════
    # NIVEL 9 — CONTEXTO ENRIQUECIDO PARA GROQ
    # ══════════════════════════════════════════════════════

    def contexto_completo_para_groq(self, texto_actual: str = '') -> str:
        """
        Contexto completo que Bell pasa a Groq.
        Incluye perfil, sesión, y conocimiento relevante.
        Compacto para no saturar tokens.
        """
        partes = []

        # 1. Perfil compacto de Sebastian
        perfil = self.obtener_perfil()
        if perfil:
            items = [f"{k}={v}" for k, v in list(perfil.items())[:5]]
            partes.append(f"SEBASTIAN: {', '.join(items)}")

        # 2. Últimos intercambios (máximo 3)
        ctx = self.obtener_contexto_sesion(3)
        if ctx:
            lines = []
            for ex in ctx[-3:]:
                lines.append(f"S: {ex['user'][:80]}")
                lines.append(f"B: {ex['bell'][:80]}")
            partes.append("SESIÓN:\n" + '\n'.join(lines))

        # 3. Conocimiento relevante si hay texto actual
        if texto_actual:
            rel = self.buscar_semantico(texto_actual)
            if rel:
                partes.append(f"RECUERDO: {rel[:120]}")

        return '\n'.join(partes) if partes else ''

    # ══════════════════════════════════════════════════════
    # ESTADÍSTICAS Y ESTADO
    # ══════════════════════════════════════════════════════

    def estadisticas(self) -> dict:
        """Resumen del estado de la memoria de Bell."""
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