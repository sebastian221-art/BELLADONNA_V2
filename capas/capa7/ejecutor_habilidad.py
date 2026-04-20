# capas/capa7/ejecutor_habilidad.py
# ================================================
# EJECUTOR DE HABILIDAD — Capa 7
#
# Simple y directo:
# — Si hay habilidad disponible → la ejecuta
# — Si no está disponible → honestidad + zona
#
# La habilidad de lenguaje NO pasa por aquí.
# Vive en Capa 6.
# ================================================

import random
from capas.capa7.paquete_capa7 import ResultadoEjecucion

_RESPUESTAS_SIN_HABILIDAD = {
    'CALCULO': [
        "Mi habilidad de cálculo todavía está en construcción. Lo guardé — cuando esté lista lo hago.",
        "Cálculo matemático viene. Lo registré como pendiente.",
        "Todavía no puedo calcular eso. Ya está en mi zona de habilidades por construir.",
    ],
    'ANALISIS_PYTHON': [
        "Análisis de código está en construcción. Lo registré como pendiente.",
        "Todavía no tengo esa habilidad lista. Lo guardé.",
    ],
    'SHELL': [
        "Ejecutar comandos del sistema todavía no puedo. Lo guardé como pendiente.",
        "Esa habilidad está en construcción. Lo registré.",
    ],
    'SQLITE': [
        "Base de datos viene. Lo registré como pendiente.",
        "Todavía no tengo la habilidad de base de datos lista. Lo guardé.",
    ],
    'DEFAULT': [
        "Esa habilidad todavía no la tengo. Lo registré — viene.",
        "Registré lo que necesitas. Cuando tenga esa habilidad lo hago.",
    ],
}


class EjecutorHabilidad:

    def ejecutar(self, deteccion: dict) -> ResultadoEjecucion:
        habilidad_id = deteccion.get('habilidad_id', '')
        disponible   = deteccion.get('disponible', False)
        texto        = deteccion.get('texto_original', '')

        if disponible:
            return self._ejecutar_habilidad(habilidad_id, texto)
        else:
            return self._sin_habilidad(habilidad_id, texto)

    def _ejecutar_habilidad(
        self, habilidad_id: str, texto: str
    ) -> ResultadoEjecucion:
        if habilidad_id == 'CALCULO':
            return self._ejecutar_calculo(texto)
        if habilidad_id == 'ANALISIS_PYTHON':
            return self._ejecutar_analisis(texto)
        if habilidad_id == 'SHELL':
            return self._ejecutar_shell(texto)
        if habilidad_id == 'SQLITE':
            return self._ejecutar_sqlite(texto)
        return ResultadoEjecucion(
            ejecuto=False, habilidad_id=habilidad_id,
            error=f'Habilidad {habilidad_id} marcada disponible sin implementación',
        )

    def _ejecutar_calculo(self, texto: str) -> ResultadoEjecucion:
        # Implementar cuando llegue la habilidad de cálculo
        return ResultadoEjecucion(
            ejecuto=False, habilidad_id='CALCULO',
            error='Implementación pendiente',
        )

    def _ejecutar_analisis(self, texto: str) -> ResultadoEjecucion:
        return ResultadoEjecucion(
            ejecuto=False, habilidad_id='ANALISIS_PYTHON',
            error='Implementación pendiente',
        )

    def _ejecutar_shell(self, texto: str) -> ResultadoEjecucion:
        return ResultadoEjecucion(
            ejecuto=False, habilidad_id='SHELL',
            error='Implementación pendiente',
        )

    def _ejecutar_sqlite(self, texto: str) -> ResultadoEjecucion:
        return ResultadoEjecucion(
            ejecuto=False, habilidad_id='SQLITE',
            error='Implementación pendiente',
        )

    def _sin_habilidad(
        self, habilidad_id: str, texto: str
    ) -> ResultadoEjecucion:
        fue_a_zona = False
        try:
            from biblioteca.zona_desconocimiento.zona import ZonaDesconocimiento
            zona = ZonaDesconocimiento.obtener()
            zona.agregar(
                fragmento  = texto[:100],
                tipo       = 'habilidad',
                inferencia = f'necesita_habilidad:{habilidad_id}',
            )
            fue_a_zona = True
        except Exception:
            pass

        opciones  = _RESPUESTAS_SIN_HABILIDAD.get(
            habilidad_id, _RESPUESTAS_SIN_HABILIDAD['DEFAULT']
        )
        respuesta = random.choice(opciones)

        return ResultadoEjecucion(
            ejecuto      = False,
            habilidad_id = habilidad_id,
            resultado    = respuesta,
            fue_a_zona   = fue_a_zona,
        )