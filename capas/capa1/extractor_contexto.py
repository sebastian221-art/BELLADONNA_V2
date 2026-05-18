# capas/capa1/extractor_contexto.py
# ================================================
# EXTRACTOR DE CONTEXTO — v2
#
# Agrega contexto de conversación,
# Sebastian y temporal al paquete.
#
# v2:
# — Conecta con memoria real de Bell
# — Estado emocional de Sebastian desde SQLite
# — Proyectos activos desde memoria
# — Momento del día más preciso
# — Contexto conversacional enriquecido
# ================================================

import time
from datetime import datetime
from capas.capa1.paquete_capa1 import ContextoPaquete


class ExtractorContexto:

    def __init__(self):
        self._historial_sesion   = []
        self._contexto_sebastian = {}
        self._turno_actual       = 0
        self._cache_memoria      = {}
        self._ultimo_refresh     = 0
        self._CACHE_TTL          = 30  # segundos — refresca la memoria cada 30s

    def extraer(self, contenido_normalizado: dict) -> ContextoPaquete:
        """
        Extrae todo el contexto disponible
        y retorna un ContextoPaquete.
        """
        return ContextoPaquete(
            conversacion=self._contexto_conversacion(contenido_normalizado),
            sebastian=self._contexto_sebastian_actual(),
            temporal=self._contexto_temporal()
        )

    # ── Contexto de conversación ──────────────────────────

    def _contexto_conversacion(self, contenido: dict) -> dict:
        self._turno_actual += 1
        return {
            'turno':              self._turno_actual,
            'historial_reciente': self._historial_sesion[-5:]
                                  if self._historial_sesion else [],
            'hay_contexto_previo': len(self._historial_sesion) > 0,
            'tipo_origen':         contenido.get('tipo_origen', 'texto'),
            'total_turnos_sesion': self._turno_actual,
        }

    # ── Contexto de Sebastian ─────────────────────────────

    def _contexto_sebastian_actual(self) -> dict:
        """
        Intenta obtener el contexto real de Sebastian
        desde la memoria persistente. Si falla, usa defaults.
        """
        ahora = time.time()
        # Usar cache si es reciente
        if self._cache_memoria and (ahora - self._ultimo_refresh) < self._CACHE_TTL:
            return self._cache_memoria

        # Intentar obtener de memoria
        contexto = self._obtener_de_memoria()
        if contexto:
            self._cache_memoria  = contexto
            self._ultimo_refresh = ahora
            return contexto

        # Fallback — datos base siempre disponibles
        return self._contexto_sebastian_base()

    def _obtener_de_memoria(self) -> dict:
        """
        Consulta la memoria de Bell para contexto de Sebastian.
        Retorna None si falla — nunca bloquea.
        """
        try:
            from biblioteca.memoria import obtener_memoria
            mem = obtener_memoria()

            # Perfil base de Sebastian
            perfil = mem.obtener_perfil_sebastian() or {}

            # Últimos FYIs relevantes
            conocimiento = mem.buscar_conocimiento('sebastian', limite=5) or []

            # Estado emocional reciente (si existe)
            estado_emocional = 'desconocido'
            try:
                estado_emocional = mem.obtener_estado_emocional_reciente() or 'desconocido'
            except Exception:
                pass  # tabla puede no existir todavía

            return {
                'nombre':              perfil.get('nombre', 'Sebastian'),
                'conocido':            True,
                'estado_emocional':    estado_emocional,
                'ciudad':              perfil.get('ciudad', 'Bucaramanga'),
                'proyectos_activos':   perfil.get('proyectos', ['BELLADONNA_V2']),
                'ultimo_fyi':          conocimiento[0].get('contenido', '') if conocimiento else '',
                'preferencias':        perfil.get('preferencias', {}),
            }
        except Exception:
            return None

    def _contexto_sebastian_base(self) -> dict:
        """Contexto base garantizado — sin dependencias externas."""
        return {
            'nombre':           'Sebastian',
            'conocido':         True,
            'estado_emocional': 'desconocido',
            'ciudad':           'Bucaramanga',
            'proyectos_activos': ['BELLADONNA_V2'],
            'ultimo_fyi':       '',
            'preferencias':     {},
        }

    # ── Contexto temporal ─────────────────────────────────

    def _contexto_temporal(self) -> dict:
        ahora = datetime.now()
        return {
            'timestamp':   time.time(),
            'hora':        ahora.hour,
            'minuto':      ahora.minute,
            'dia_semana':  ahora.weekday(),       # 0=lunes, 6=domingo
            'dia_nombre':  self._nombre_dia(ahora.weekday()),
            'momento_dia': self._momento_del_dia(ahora.hour),
            'es_fin_semana': ahora.weekday() >= 5,
        }

    def _momento_del_dia(self, hora: int) -> str:
        if 5 <= hora < 9:
            return 'madrugada_temprano'
        elif 9 <= hora < 12:
            return 'mañana'
        elif 12 <= hora < 14:
            return 'mediodia'
        elif 14 <= hora < 18:
            return 'tarde'
        elif 18 <= hora < 21:
            return 'noche_temprana'
        elif 21 <= hora < 24:
            return 'noche'
        else:
            return 'madrugada'

    def _nombre_dia(self, weekday: int) -> str:
        dias = ['lunes', 'martes', 'miércoles', 'jueves',
                'viernes', 'sábado', 'domingo']
        return dias[weekday] if 0 <= weekday <= 6 else 'desconocido'

    # ── Historial ─────────────────────────────────────────

    def agregar_al_historial(self, turno: dict):
        self._historial_sesion.append(turno)
        if len(self._historial_sesion) > 20:
            self._historial_sesion = self._historial_sesion[-20:]

    def actualizar_sebastian(self, datos: dict):
        """Actualiza el contexto de Sebastian con datos nuevos."""
        self._contexto_sebastian.update(datos)
        self._cache_memoria  = {}  # invalidar cache
        self._ultimo_refresh = 0