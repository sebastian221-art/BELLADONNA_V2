# capas/capa7/ejecutor_habilidad.py — v5 DIRECTO
# La habilidad Python ya habla en lenguaje natural porque sus módulos
# llaman a Groq directamente con prompts expertos.
# El humanizador anterior recortaba las respuestas a 900 tokens.
# AHORA: la respuesta del skill llega DIRECTA al usuario — sin re-procesar.
import random
from capas.capa7.paquete_capa7 import ResultadoEjecucion

_RESPUESTAS_SIN_HABILIDAD = {
    'CALCULO': ['Mi habilidad de cálculo está en construcción.'],
    'SHELL':   ['Ejecutar comandos del sistema todavía no puedo. Lo guardé como pendiente.'],
    'SQLITE':  ['Base de datos viene. Lo registré como pendiente.'],
    'DEFAULT': ['Esa habilidad todavía no la tengo. Lo registré — viene.'],
}


class EjecutorHabilidad:

    def ejecutar(self, deteccion: dict) -> ResultadoEjecucion:
        habilidad_id = deteccion.get('habilidad_id', '')
        disponible   = deteccion.get('disponible', False)
        texto        = deteccion.get('texto_original', '')
        modo         = deteccion.get('modo', None)
        verbosidad   = deteccion.get('verbosidad', 'normal')
        if disponible:
            return self._ejecutar_habilidad(habilidad_id, texto, modo, verbosidad)
        return self._sin_habilidad(habilidad_id, texto)

    def _ejecutar_habilidad(self, habilidad_id, texto, modo, verbosidad):
        # Fix clarificación: usar memoria de sesión para retomar búsqueda pendiente
        try:
            from biblioteca.habilidades.busqueda.motor_busqueda import _PENDIENTE, _es_respuesta_clarificacion
            # Check _PENDIENTE state first
            if _PENDIENTE.get('activo'):
                if _es_respuesta_clarificacion(texto):
                    print(f"  [DEBUG C7] Retomando búsqueda pendiente: {_PENDIENTE.get('pregunta')}")
                    return self._ejecutar_busqueda(texto)
            # Check session memory for context (resuelve "me refiero al lenguaje")
            elif not habilidad_id:
                from biblioteca.memoria import obtener_memoria
                mem = obtener_memoria()
                pregunta_previa = mem.resolver_clarificacion(texto)
                if pregunta_previa:
                    # Retomar la búsqueda original con la clarificación
                    from biblioteca.habilidades.busqueda.motor_busqueda import ejecutar_busqueda
                    resultado = ejecutar_busqueda(pregunta_previa, clarificacion_previa=texto)
                    if resultado.get('exitoso'):
                        from capas.capa7.ejecutor_habilidad import ResultadoEjecucion
                        return ResultadoEjecucion(
                            ejecuto=True,
                            habilidad_id='BUSQUEDA_INTERNET',
                            resultado=resultado['respuesta'],
                        )
        except Exception as _e:
            pass
        if habilidad_id == 'PYTHON_COMPLETO':
            return self._ejecutar_python(texto, modo, verbosidad)
        if habilidad_id == 'BUSQUEDA_INTERNET':
            return self._ejecutar_busqueda(texto)

        if habilidad_id == 'AUTO_ANALISIS_TOTAL':
            return self._ejecutar_auto_analisis(texto)
        if habilidad_id in ('CALCULO', 'SHELL', 'SQLITE'):
            return ResultadoEjecucion(ejecuto=False, habilidad_id=habilidad_id, error='Pendiente')
        return ResultadoEjecucion(ejecuto=False, habilidad_id=habilidad_id, error='Sin implementación')

    def _ejecutar_busqueda(self, texto: str) -> 'ResultadoEjecucion':
        """Bell busca en internet y responde con información real."""
        try:
            from biblioteca.habilidades.busqueda.motor_busqueda import ejecutar_busqueda
            resultado = ejecutar_busqueda(texto)
            if resultado.get('exitoso'):
                return ResultadoEjecucion(
                    ejecuto=True,
                    habilidad_id='BUSQUEDA_INTERNET',
                    resultado=resultado['respuesta'],
                )
            return ResultadoEjecucion(
                ejecuto=True,
                habilidad_id='BUSQUEDA_INTERNET',
                resultado=resultado.get('respuesta', 'No encontré resultados.'),
            )
        except Exception as e:
            import traceback
            print(f"[Busqueda ERROR] {type(e).__name__}: {e}")
            print(traceback.format_exc())
            return ResultadoEjecucion(
                ejecuto=True,
                habilidad_id='BUSQUEDA_INTERNET',
                resultado=f'Error al buscar: {type(e).__name__}: {str(e)[:120]}',
            )

    def _ejecutar_auto_analisis(self, texto: str) -> 'ResultadoEjecucion':
        try:
            from biblioteca.habilidades.auto_analisis import ejecutar_auto_analisis
            resultado = ejecutar_auto_analisis(texto)
            if resultado.get('exitoso') and resultado.get('respuesta'):
                return ResultadoEjecucion(
                    ejecuto      = True,
                    habilidad_id = 'AUTO_ANALISIS_TOTAL',
                    resultado    = resultado['respuesta'],
                )
            return ResultadoEjecucion(
                ejecuto=False, habilidad_id='AUTO_ANALISIS_TOTAL',
                error=resultado.get('respuesta', 'Error en auto-análisis'),
            )
        except Exception as e:
            return ResultadoEjecucion(
                ejecuto=False, habilidad_id='AUTO_ANALISIS_TOTAL',
                error=str(e)[:100],
                resultado='No pude leerme a mí misma en este momento.',
            )

    def _ejecutar_python(self, texto: str, modo: str, verbosidad: str) -> ResultadoEjecucion:
        try:
            from biblioteca.habilidades.python.motor_python import MotorPython
            motor     = MotorPython.obtener()
            resultado = motor.procesar(texto=texto, modo=modo or 'explicacion', verbosidad=verbosidad)

            if not (resultado.get('exitoso') and resultado.get('respuesta')):
                fallback = resultado.get('respuesta_fallback', '')
                return ResultadoEjecucion(
                    ejecuto=False, habilidad_id='PYTHON_COMPLETO',
                    error=resultado.get('error', 'sin resultado'),
                    resultado=fallback,
                )

            # ── RESPUESTA DIRECTA — sin humanizador ───────────────
            # Los módulos del skill (analizador, explicador, generador,
            # auto_integrador) ya llaman a Groq con prompts expertos
            # que producen lenguaje natural perfecto.
            # Pasar por otro Groq solo trunca y degrada la calidad.
            return ResultadoEjecucion(
                ejecuto      = True,
                habilidad_id = 'PYTHON_COMPLETO',
                resultado    = resultado['respuesta'],
            )

        except ImportError:
            return ResultadoEjecucion(ejecuto=False, habilidad_id='PYTHON_COMPLETO',
                                       error='MotorPython no disponible',
                                       resultado='La habilidad Python está en construcción.')
        except Exception as e:
            return ResultadoEjecucion(ejecuto=False, habilidad_id='PYTHON_COMPLETO',
                                       error=str(e),
                                       resultado='Encontré un problema procesando eso. Dímelo de otra forma.')

    def _sin_habilidad(self, habilidad_id: str, texto: str) -> ResultadoEjecucion:
        try:
            from biblioteca.zona_desconocimiento.zona import ZonaDesconocimiento
            ZonaDesconocimiento.obtener().agregar(
                fragmento=texto[:100], tipo='habilidad',
                inferencia=f'necesita_habilidad:{habilidad_id}',
            )
        except Exception:
            pass
        opciones = _RESPUESTAS_SIN_HABILIDAD.get(habilidad_id, _RESPUESTAS_SIN_HABILIDAD['DEFAULT'])
        return ResultadoEjecucion(ejecuto=False, habilidad_id=habilidad_id,
                                   resultado=random.choice(opciones), fue_a_zona=True)