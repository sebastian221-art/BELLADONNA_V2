# capas/capa6/buffer_sesion.py
# ================================================
# BUFFER DE SESIÓN — v4
#
# Responsabilidad única: contexto de la sesión
# ACTUAL en RAM para que el motor de Bell pueda
# evitar repeticiones y recordar el hilo.
#
# La MEMORIA PERSISTENTE es responsabilidad de
# biblioteca/habilidades/memoria/ — no duplicar.
# Este buffer solo maneja la sesión viva.
#
# Qué guarda:
#   - Últimos 12 turnos (usuario↔Bell)
#   - Hechos mencionados en esta sesión
#   - Estado emocional detectado esta sesión
#   - Anti-repetición: últimas respuestas de Bell
# ================================================

from collections import deque
from typing import List


class BufferSesion:
    _instancia = None

    def __init__(self, max_turnos: int = 12):
        self._turnos:  deque = deque(maxlen=max_turnos)
        self._hechos:  dict  = {}
        self._memoria        = None  # memoria persistente — lazy

    @classmethod
    def obtener(cls) -> 'BufferSesion':
        if cls._instancia is None:
            cls._instancia = BufferSesion()
            cls._instancia._conectar_memoria()
        return cls._instancia

    def _conectar_memoria(self):
        """Conecta con la habilidad de memoria — sin bloquear si falla."""
        try:
            from biblioteca.memoria.memoria_persistente import MemoriaPersistente
            self._memoria = MemoriaPersistente.obtener()
            self._memoria.iniciar_sesion()
        except Exception:
            self._memoria = None

    # ── Agregar turno ─────────────────────────────────────

    def agregar_turno(
        self,
        texto_usuario:  str,
        respuesta_bell: str,
        comprension:    dict = None,
    ):
        self._turnos.append({
            'usuario': texto_usuario,
            'bell':    respuesta_bell,
            'comp':    comprension or {},
        })
        self._actualizar_hechos(texto_usuario, comprension)

        # Delegar persistencia a la habilidad de memoria
        if self._memoria:
            try:
                self._memoria.registrar_turno(
                    texto_usuario, respuesta_bell, comprension
                )
            except Exception:
                pass

    # ── Extracción de hechos de sesión ────────────────────

    def _actualizar_hechos(self, texto: str, comprension: dict = None):
        import re
        tl = texto.lower()

        m = re.search(r'tengo\s+(\d+)\s*años?', tl)
        if m:
            self._hechos['edad'] = m.group(1)

        m = re.search(r'(?:me llamo|mi nombre es)\s+(\w+)', tl)
        if m:
            self._hechos['nombre_mencionado'] = m.group(1)

        neg = ['cansado','agotado','estresado','frustrado','mal','triste','ansioso','preocupado']
        pos = ['bien','genial','feliz','contento','motivado','emocionado','alegre']
        if any(s in tl for s in neg):
            self._hechos['estado_sesion'] = 'negativo'
        elif any(s in tl for s in pos):
            self._hechos['estado_sesion'] = 'positivo'

        if comprension:
            emocion = comprension.get('profunda', {}).get('emocion_detectada', '')
            if emocion and emocion not in ('neutra', ''):
                self._hechos['emocion_actual'] = emocion

        catalogo = {
            'belladonna': ['belladonna', 'bell', 'el proyecto', 'las capas'],
            'trabajo':    ['trabajo', 'jelcon', 'empresa'],
            'estudio':    ['universidad', 'uniminuto', 'clase', 'examen'],
            'codigo':     ['código', 'python', 'función', 'error', 'bug'],
        }
        for tema, palabras in catalogo.items():
            if any(p in tl for p in palabras):
                temas = self._hechos.setdefault('temas', [])
                if tema not in temas:
                    temas.append(tema)

    # ── Contexto para el motor ────────────────────────────

    def obtener_contexto_para_prompt(self) -> str:
        """
        Contexto mínimo y útil para el motor de Bell.
        Solo lo que realmente ayuda a no repetirse y recordar el hilo.
        """
        bloques = []

        # 1. Hechos de la sesión actual
        if self._hechos:
            lineas = ['ESTA SESIÓN:']
            if 'edad' in self._hechos:
                lineas.append(f'  Mencionó {self._hechos["edad"]} años')
            if 'nombre_mencionado' in self._hechos:
                lineas.append(f'  Se presentó como {self._hechos["nombre_mencionado"]}')
            if 'estado_sesion' in self._hechos:
                est = 'difícil' if self._hechos['estado_sesion'] == 'negativo' else 'positivo'
                lineas.append(f'  Estado emocional: {est}')
            if 'emocion_actual' in self._hechos:
                lineas.append(f'  Emoción: {self._hechos["emocion_actual"]}')
            if 'temas' in self._hechos:
                lineas.append(f'  Temas: {", ".join(self._hechos["temas"])}')
            if len(lineas) > 1:
                bloques.append('\n'.join(lineas))

        # 2. Anti-repetición — últimas 4 respuestas de Bell
        turnos_lista = list(self._turnos)
        if turnos_lista:
            lineas = ['ÚLTIMAS RESPUESTAS (no repetir apertura ni estructura):']
            for t in turnos_lista[-4:]:
                b = t['bell'][:70] + ('...' if len(t['bell']) > 70 else '')
                lineas.append(f'  • "{b}"')
            bloques.append('\n'.join(lineas))

        # 3. Contexto enriquecido desde memoria persistente
        if self._memoria:
            try:
                ctx = self._memoria.obtener_contexto_rico()
                if ctx:
                    bloques.insert(0, ctx)  # memoria al inicio
            except Exception:
                pass

        return '\n\n'.join(bloques) if bloques else ''

    def obtener_iniciativa_conversacional(self) -> str:
        """Temas pendientes que Bell puede retomar naturalmente."""
        if not self._memoria:
            return ''
        try:
            pendientes = self._memoria.obtener_pendientes_relevantes()
            temas      = self._memoria.obtener_temas_para_iniciativa()
            lineas = []
            if pendientes:
                ultimo = pendientes[-1]
                lineas.append(
                    f'PENDIENTE (retomar si viene al caso): '
                    f'"{ultimo.get("texto","")[:80]}"'
                )
            elif temas:
                lineas.append(
                    f'TEMAS RECURRENTES: {", ".join(temas)} — '
                    f'preguntar si hay algo nuevo si el momento es natural.'
                )
            return '\n'.join(lineas)
        except Exception:
            return ''

    def obtener_ultimas_respuestas_bell(self, n: int = 4) -> List[str]:
        return [t['bell'] for t in list(self._turnos)[-n:]]

    def tiene_contexto(self) -> bool:
        return len(self._turnos) > 0 or bool(self._hechos)

    def tiene_historia_previa(self) -> bool:
        return self._memoria.tiene_historia() if self._memoria else False

    def limpiar(self):
        self._turnos.clear()
        self._hechos.clear()