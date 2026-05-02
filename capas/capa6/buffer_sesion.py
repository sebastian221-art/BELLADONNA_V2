# capas/capa6/buffer_sesion.py v3
# ================================================
# BUFFER DE SESIÓN — Capa 6
#
# v3: conectado a MemoriaPersistente.
#
# El buffer maneja la sesión actual (RAM).
# La MemoriaPersistente maneja todo lo anterior (disco).
# Juntos le dan a Bell memoria real y continua.
#
# PRINCIPIO:
# Bell usa lo que sabe — nunca se lo recuerda
# a Sebastian como si fuera un registro.
# Lo sabe. Punto.
# ================================================

from collections import deque
from typing import List


class BufferSesion:
    _instancia = None

    def __init__(self, max_turnos: int = 12):
        self._turnos:        deque = deque(maxlen=max_turnos)
        self._hechos_sesion: dict  = {}
        self._memoria                = None  # carga lazy

    @classmethod
    def obtener(cls) -> 'BufferSesion':
        if cls._instancia is None:
            cls._instancia = BufferSesion()
            cls._instancia._iniciar_sesion()
        return cls._instancia

    def _iniciar_sesion(self):
        try:
            from biblioteca.memoria.memoria_persistente import MemoriaPersistente
            self._memoria = MemoriaPersistente.obtener()
            self._memoria.iniciar_sesion()
        except Exception:
            self._memoria = None

    # ── Agregar turno ─────────────────────────────────────

    def agregar_turno(
        self,
        texto_usuario: str,
        respuesta_bell: str,
        comprension: dict = None,
    ):
        self._turnos.append({
            'usuario':    texto_usuario,
            'bell':       respuesta_bell,
            'comprension': comprension or {},
        })
        self._extraer_hechos(texto_usuario, comprension)

        # Registrar en memoria persistente
        if self._memoria:
            try:
                self._memoria.registrar_turno(texto_usuario, respuesta_bell, comprension)
            except Exception:
                pass

    # ── Extracción de hechos de sesión actual ─────────────

    def _extraer_hechos(self, texto: str, comprension: dict = None):
        import re
        tl = texto.lower()

        # Edad
        m = re.search(r'tengo\s+(\d+)\s*años?', tl)
        if m:
            self._hechos_sesion['edad'] = m.group(1)

        # Nombre propio
        m = re.search(r'(?:me llamo|mi nombre es)\s+(\w+)', tl)
        if m:
            self._hechos_sesion['nombre_mencionado'] = m.group(1)

        # Estado emocional
        neg = ['cansado','agotado','estresado','frustrado','mal','triste','ansioso','preocupado']
        pos = ['bien','genial','feliz','contento','motivado','emocionado','alegre']
        if any(s in tl for s in neg):
            self._hechos_sesion['estado_emocional'] = 'negativo'
        elif any(s in tl for s in pos):
            self._hechos_sesion['estado_emocional'] = 'positivo'

        # Desde comprensión
        if comprension:
            profunda = comprension.get('profunda', {})
            emocion  = profunda.get('emocion_detectada', '')
            if emocion and emocion not in ('neutra', ''):
                self._hechos_sesion['emocion_actual'] = emocion

        # Temas de sesión
        catalogo = {
            'belladonna': ['belladonna', 'bell', 'el proyecto'],
            'trabajo':    ['trabajo', 'empresa', 'jefe'],
            'estudio':    ['universidad', 'clase', 'examen'],
            'familia':    ['familia', 'papá', 'mamá', 'hermano'],
            'codigo':     ['código', 'codigo', 'python', 'archivo', 'función'],
        }
        for tema, palabras in catalogo.items():
            if any(p in tl for p in palabras):
                lista = self._hechos_sesion.get('temas', [])
                if tema not in lista:
                    lista.append(tema)
                    self._hechos_sesion['temas'] = lista

    # ── Contexto para el prompt ───────────────────────────

    def obtener_contexto_para_prompt(self) -> str:
        """
        Contexto completo: memoria persistente + sesión actual.
        Bell usa esto internamente — nunca se lo dice a Sebastian.
        """
        bloques = []

        # 1. Memoria persistente (lo de antes de esta sesión)
        if self._memoria:
            try:
                ctx_persistente = self._memoria.obtener_contexto_rico()
                if ctx_persistente:
                    bloques.append(ctx_persistente)
            except Exception:
                pass

        # 2. Hechos de esta sesión
        if self._hechos_sesion:
            lineas = ['ESTA SESIÓN:']
            if 'edad' in self._hechos_sesion:
                lineas.append(f'  Mencionó que tiene {self._hechos_sesion["edad"]} años')
            if 'nombre_mencionado' in self._hechos_sesion:
                lineas.append(f'  Se presentó como {self._hechos_sesion["nombre_mencionado"]}')
            if 'estado_emocional' in self._hechos_sesion:
                est = self._hechos_sesion['estado_emocional']
                lineas.append(f'  Ha expresado estado {"difícil" if est == "negativo" else "positivo"} en esta sesión')
            if 'emocion_actual' in self._hechos_sesion:
                lineas.append(f'  Emoción detectada: {self._hechos_sesion["emocion_actual"]}')
            if 'temas' in self._hechos_sesion:
                lineas.append(f'  Temas de esta sesión: {", ".join(self._hechos_sesion["temas"])}')
            if len(lineas) > 1:
                bloques.append('\n'.join(lineas))

        # 3. Últimas respuestas de Bell (anti-repetición)
        turnos_lista = list(self._turnos)
        if turnos_lista:
            lineas = ['ÚLTIMAS RESPUESTAS DE BELL (no repetir):']
            for t in turnos_lista[-4:]:
                b = t['bell'][:70] + ('...' if len(t['bell']) > 70 else '')
                lineas.append(f'  • "{b}"')
            bloques.append('\n'.join(lineas))

        return '\n\n'.join(bloques) if bloques else ''

    def obtener_iniciativa_conversacional(self) -> str:
        """
        Retorna un string con información para que Bell
        pueda tomar iniciativa si el contexto lo permite.
        Solo cuando hay historia real.
        """
        if not self._memoria:
            return ''
        try:
            pendientes = self._memoria.obtener_pendientes_relevantes()
            temas      = self._memoria.obtener_temas_para_iniciativa()

            lineas = []
            if pendientes:
                ultimo = pendientes[-1]
                lineas.append(
                    f'TEMA PENDIENTE (Bell puede retomarlo si viene al caso): '
                    f'"{ultimo.get("texto","")[:80]}"'
                )
            if temas and not pendientes:
                lineas.append(
                    f'TEMAS RECURRENTES DE SEBASTIAN: {", ".join(temas)} — '
                    f'Bell puede preguntar si hay algo nuevo si el momento es natural.'
                )
            return '\n'.join(lineas)
        except Exception:
            return ''

    def obtener_ultimas_respuestas_bell(self, n: int = 4) -> List[str]:
        return [t['bell'] for t in list(self._turnos)[-n:]]

    def tiene_contexto(self) -> bool:
        return len(self._turnos) > 0 or len(self._hechos_sesion) > 0

    def tiene_historia_previa(self) -> bool:
        if self._memoria:
            return self._memoria.tiene_historia()
        return False

    def limpiar(self):
        self._turnos.clear()
        self._hechos_sesion.clear()