# capas/capa6/buffer_sesion.py v2
# ================================================
# BUFFER DE SESIÓN — Capa 6
#
# FIX v2: el contexto llega a Groq como información
# que Bell usa para responder mejor — no como algo
# que Bell le recuerda a Sebastian que ya dijo.
#
# ANTES: "Ya mencionaste que tienes 19 años"
# AHORA: Bell simplemente sabe que tiene 19 años
#        y lo usa si viene al caso — sin anunciarlo.
# ================================================

from collections import deque
from typing import List


class BufferSesion:
    _instancia = None

    def __init__(self, max_turnos: int = 8):
        self._turnos:        deque = deque(maxlen=max_turnos)
        self._hechos_sesion: dict  = {}

    @classmethod
    def obtener(cls) -> 'BufferSesion':
        if cls._instancia is None:
            cls._instancia = BufferSesion()
        return cls._instancia

    def agregar_turno(self, texto_usuario: str, respuesta_bell: str):
        self._turnos.append({
            'usuario': texto_usuario,
            'bell':    respuesta_bell,
        })
        self._extraer_hechos(texto_usuario)

    def _extraer_hechos(self, texto: str):
        import re
        tl = texto.lower()

        match = re.search(r'tengo\s+(\d+)\s+años', tl)
        if match:
            self._hechos_sesion['edad'] = match.group(1)

        match = re.search(r'me\s+llamo\s+(\w+)', tl)
        if match:
            self._hechos_sesion['nombre_mencionado'] = match.group(1)

        if any(s in tl for s in ['cansado','agotado','estresado','frustrado','mal']):
            self._hechos_sesion['estado_emocional_sesion'] = 'negativo'
        if any(s in tl for s in ['bien','genial','feliz','contento','motivado']):
            self._hechos_sesion['estado_emocional_sesion'] = 'positivo'

        temas = {
            'trabajo':   ['trabajo','empleo','jefe','oficina'],
            'estudio':   ['estudios','universidad','carrera','clases'],
            'familia':   ['familia','papá','mamá','hermano','hermana'],
            'proyecto':  ['proyecto','belladonna','bell','desarrollando'],
        }
        for tema, palabras in temas.items():
            if any(p in tl for p in palabras):
                lista = self._hechos_sesion.get('temas_sesion', [])
                if tema not in lista:
                    lista.append(tema)
                    self._hechos_sesion['temas_sesion'] = lista

    def obtener_contexto_para_prompt(self) -> str:
        """
        Contexto silencioso para Groq.
        Bell usa esta información para responder mejor.
        NO para recordarle a Sebastian lo que ya dijo.
        El prompt explica esto explícitamente.
        """
        if not self._turnos and not self._hechos_sesion:
            return ''

        lineas = []

        # Hechos — información que Bell sabe y puede usar
        if self._hechos_sesion:
            lineas.append('CONTEXTO QUE BELL SABE (usar si viene al caso):')
            if 'edad' in self._hechos_sesion:
                lineas.append(f'  Sebastian tiene {self._hechos_sesion["edad"]} años')
            if 'nombre_mencionado' in self._hechos_sesion:
                lineas.append(f'  Se presentó como {self._hechos_sesion["nombre_mencionado"]}')
            if 'estado_emocional_sesion' in self._hechos_sesion:
                est = self._hechos_sesion['estado_emocional_sesion']
                if est == 'negativo':
                    lineas.append('  Ha expresado algo negativo en esta sesión')
                else:
                    lineas.append('  Ha expresado algo positivo en esta sesión')
            if 'temas_sesion' in self._hechos_sesion:
                temas = ', '.join(self._hechos_sesion['temas_sesion'])
                lineas.append(f'  Temas mencionados: {temas}')

        # Últimos 3 turnos — para no repetir estructuras
        turnos_lista = list(self._turnos)
        if turnos_lista:
            lineas.append('\nÚLTIMAS RESPUESTAS DE BELL (no repetir estas estructuras):')
            for t in turnos_lista[-3:]:
                b = t['bell'][:60] + ('...' if len(t['bell']) > 60 else '')
                lineas.append(f'  • "{b}"')

        return '\n'.join(lineas)

    def obtener_ultimas_respuestas_bell(self, n: int = 3) -> List[str]:
        return [t['bell'] for t in list(self._turnos)[-n:]]

    def tiene_contexto(self) -> bool:
        return len(self._turnos) > 0 or len(self._hechos_sesion) > 0

    def limpiar(self):
        self._turnos.clear()
        self._hechos_sesion.clear()