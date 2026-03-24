# biblioteca/consejeras/gestor_consejeras.py
# ================================================
# GESTOR DE CONSEJERAS
# Orquesta las 8 consejeras de Bell
# Las invoca en orden correcto
# Maneja el veto de Vega
# Garantiza que Sage siempre habla última
# ================================================

from typing import List, Dict, Optional
from biblioteca.consejeras.base_consejera import ResultadoConsejera


class ResultadoDeliberacion:
    """
    El resultado completo de la deliberación
    de todas las consejeras.
    """
    def __init__(self):
        self.aprobado:           bool  = True
        self.veto:               bool  = False
        self.veto_por:           str   = ''
        self.veto_razon:         str   = ''
        self.tono_final:         str   = 'cercano_natural'
        self.recomendacion_sage: str   = ''
        self.confianza_colectiva: float = 0.8
        self.prioridad_emocional: bool  = False
        self.resultados: List[dict]     = []

    def a_dict(self) -> dict:
        return {
            'aprobado':            self.aprobado,
            'veto':                self.veto,
            'veto_por':            self.veto_por,
            'veto_razon':          self.veto_razon,
            'tono_final':          self.tono_final,
            'recomendacion_sage':  self.recomendacion_sage,
            'confianza_colectiva': self.confianza_colectiva,
            'prioridad_emocional': self.prioridad_emocional,
            'total_consejeras':    len(self.resultados),
            'resultados':          self.resultados,
        }


class GestorConsejeras:
    """
    Orquesta las 8 consejeras de Bell.

    Orden de invocación:
    1. Soma    — integridad (siempre primera)
    2. Vega    — ética (puede vetar — si veta, para todo)
    3. Nova    — técnica
    4. Echo    — coherencia
    5. Lyra    — emociones
    6. Luna    — patrones
    7. Iris    — largo plazo
    8. Sage    — síntesis (siempre última)

    Singleton — una sola instancia.
    """

    _instancia = None

    def __init__(self):
        self._consejeras = {}
        self._iniciado   = False
        self._cargar_consejeras()

    @classmethod
    def obtener(cls) -> 'GestorConsejeras':
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def _cargar_consejeras(self):
        """Carga todas las consejeras."""
        print('  Iniciando consejeras de Bell...')
        cargas = [
            ('CONSEJERA_SOMA',  'biblioteca.consejeras.soma.logica',  'Soma'),
            ('CONSEJERA_VEGA',  'biblioteca.consejeras.vega.logica',  'Vega'),
            ('CONSEJERA_NOVA',  'biblioteca.consejeras.nova.logica',  'Nova'),
            ('CONSEJERA_ECHO',  'biblioteca.consejeras.echo.logica',  'Echo'),
            ('CONSEJERA_LYRA',  'biblioteca.consejeras.lyra.logica',  'Lyra'),
            ('CONSEJERA_LUNA',  'biblioteca.consejeras.luna.logica',  'Luna'),
            ('CONSEJERA_IRIS',  'biblioteca.consejeras.iris.logica',  'Iris'),
            ('CONSEJERA_SAGE',  'biblioteca.consejeras.sage.logica',  'Sage'),
        ]

        for consejera_id, modulo_path, clase_nombre in cargas:
            try:
                import importlib
                modulo = importlib.import_module(modulo_path)
                clase  = getattr(modulo, clase_nombre)
                self._consejeras[consejera_id] = clase()
                print(f'    ✓ {clase_nombre} iniciada')
            except Exception as e:
                print(f'    ⚠ {clase_nombre} no disponible: {e}')

        self._iniciado = True
        print(f'  Consejeras activas: {len(self._consejeras)}/8')

    def consultar_todas(
        self,
        contexto: dict,
        consejeras_requeridas: List[str] = None
    ) -> ResultadoDeliberacion:
        """
        Consulta todas las consejeras en orden.
        Si consejeras_requeridas está definido,
        solo consulta esas (más Soma, Vega y Sage que son obligatorias).
        """
        deliberacion = ResultadoDeliberacion()
        resultados_acumulados = []

        # Orden fijo — Soma y Vega siempre primero, Sage siempre último
        orden = [
            'CONSEJERA_SOMA',   # Siempre
            'CONSEJERA_VEGA',   # Siempre — puede vetar
            'CONSEJERA_NOVA',
            'CONSEJERA_ECHO',
            'CONSEJERA_LYRA',
            'CONSEJERA_LUNA',
            'CONSEJERA_IRIS',
            # Sage va al final — después del loop
        ]

        for consejera_id in orden:
            # Si hay filtro, verificar si esta consejera aplica
            # Soma, Vega y Sage siempre van
            obligatorias = {
                'CONSEJERA_SOMA', 'CONSEJERA_VEGA', 'CONSEJERA_SAGE'
            }
            if (consejeras_requeridas is not None and
                    consejera_id not in obligatorias and
                    consejera_id not in consejeras_requeridas):
                continue

            consejera = self._consejeras.get(consejera_id)
            if not consejera:
                continue

            try:
                resultado = consejera.evaluar(contexto)
                resultado_dict = resultado.a_dict()
                resultados_acumulados.append(resultado_dict)

                # Si Vega veta — parar todo
                if resultado.veto:
                    deliberacion.aprobado   = False
                    deliberacion.veto       = True
                    deliberacion.veto_por   = consejera_id
                    deliberacion.veto_razon = resultado.veto_razon
                    deliberacion.resultados = resultados_acumulados
                    print(
                        f'  VETO de {consejera.identidad.nombre}: '
                        f'{resultado.veto_razon}'
                    )
                    return deliberacion  # Parar inmediatamente

            except Exception as e:
                print(f'  Error en {consejera_id}: {e}')

        # Sage siempre al final con todos los resultados
        sage = self._consejeras.get('CONSEJERA_SAGE')
        if sage:
            try:
                contexto_sage = {
                    **contexto,
                    'resultados_consejeras': resultados_acumulados
                }
                resultado_sage = sage.evaluar(contexto_sage)
                resultados_acumulados.append(resultado_sage.a_dict())

                deliberacion.tono_final          = resultado_sage.tono_sugerido or 'cercano_natural'
                deliberacion.recomendacion_sage  = resultado_sage.recomendacion
                deliberacion.confianza_colectiva = resultado_sage.confianza

                datos_sage = resultado_sage.datos_extra
                deliberacion.prioridad_emocional = datos_sage.get(
                    'prioridad_emocional', False
                )

            except Exception as e:
                print(f'  Error en Sage: {e}')

        deliberacion.resultados = resultados_acumulados
        return deliberacion

    def consultar_una(
        self,
        consejera_id: str,
        contexto: dict
    ) -> Optional[ResultadoConsejera]:
        """Consulta una sola consejera."""
        consejera = self._consejeras.get(consejera_id)
        if not consejera:
            return None
        try:
            return consejera.evaluar(contexto)
        except Exception as e:
            print(f'Error consultando {consejera_id}: {e}')
            return None

    def quien_soy(self, consejera_id: str) -> Optional[dict]:
        """La consejera se describe a sí misma."""
        c = self._consejeras.get(consejera_id)
        return c.quien_soy() if c else None

    def estado_todas(self) -> dict:
        """Estado de todas las consejeras."""
        return {
            cid: c.quien_soy()
            for cid, c in self._consejeras.items()
        }