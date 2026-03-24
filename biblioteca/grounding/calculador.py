# biblioteca/grounding/calculador.py
# ================================================
# CALCULADOR DE GROUNDING
# Calcula el grounding 9D de cualquier nodo
# Combina el perfil base con el contexto real
# Se mejora con cada uso
# ================================================

from biblioteca.grounding.dimensiones import Grounding9D
from biblioteca.grounding.perfiles import PerfilesGrounding
from typing import Optional


class CalculadorGrounding:
    """
    Calcula el grounding completo de un concepto.

    No es estático — aprende con cada uso.
    Cuanto más usa Bell un concepto con éxito,
    más sube su grounding.
    Cuanto más falla, más baja.
    """

    _instancia = None

    def __init__(self):
        self._cache: dict = {}
        self._historial_uso: dict = {}

    @classmethod
    def obtener(cls) -> 'CalculadorGrounding':
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def calcular(
        self,
        concepto_id: str,
        tipo: str,
        contexto: dict = None,
        grounding_base: float = None
    ) -> Grounding9D:
        """
        Calcula el grounding completo de un concepto.

        1. Usa el perfil base del tipo
        2. Ajusta con el grounding_base si existe
        3. Ajusta con el contexto si está disponible
        4. Aplica el historial de uso
        """
        # Obtener perfil base
        grounding = PerfilesGrounding.por_tipo(tipo)

        # Ajustar con grounding_base del vocabulario
        if grounding_base is not None:
            grounding = self._ajustar_con_base(
                grounding, grounding_base
            )

        # Ajustar con contexto
        if contexto:
            grounding = self._ajustar_con_contexto(
                grounding, contexto
            )

        # Aplicar historial de uso
        if concepto_id in self._historial_uso:
            grounding = self._ajustar_con_historial(
                grounding, self._historial_uso[concepto_id]
            )

        return grounding

    def registrar_uso(
        self,
        concepto_id: str,
        exitoso: bool,
        contexto: str = ''
    ):
        """
        Registra que Bell usó este concepto.
        El grounding mejora con usos exitosos.
        Bell aprende genuinamente.
        """
        if concepto_id not in self._historial_uso:
            self._historial_uso[concepto_id] = {
                'usos_exitosos':   0,
                'usos_fallidos':   0,
                'contextos':       [],
                'tasa_exito':      0.5
            }

        hist = self._historial_uso[concepto_id]

        if exitoso:
            hist['usos_exitosos'] += 1
        else:
            hist['usos_fallidos'] += 1

        total = hist['usos_exitosos'] + hist['usos_fallidos']
        hist['tasa_exito'] = hist['usos_exitosos'] / total

        if contexto and contexto not in hist['contextos']:
            hist['contextos'].append(contexto)
            # Más contextos → más relacional
            if len(hist['contextos']) > 5:
                hist['contextos'] = hist['contextos'][-10:]

    def _ajustar_con_base(
        self,
        grounding: Grounding9D,
        base: float
    ) -> Grounding9D:
        """
        Ajusta el grounding según el valor base
        del vocabulario. El grounding_base refleja
        cuán directamente ejecutable es el concepto.
        """
        factor = base  # 0.0 a 1.0

        # El grounding_base afecta principalmente
        # ejecutabilidad y conocimiento
        grounding.ejecutabilidad = min(1.0,
            grounding.ejecutabilidad * (0.7 + factor * 0.3)
        )
        grounding.conocimiento = min(1.0,
            grounding.conocimiento * (0.8 + factor * 0.2)
        )
        grounding.confianza = min(1.0,
            grounding.confianza * (0.8 + factor * 0.2)
        )

        return grounding

    def _ajustar_con_contexto(
        self,
        grounding: Grounding9D,
        contexto: dict
    ) -> Grounding9D:
        """
        Ajusta el grounding según el contexto actual.
        """
        # Si hay historial de conversación
        hay_historial = bool(
            contexto.get('conversacion', {}).get('historial_reciente')
        )
        if hay_historial:
            grounding.contexto    = min(1.0, grounding.contexto + 0.10)
            grounding.relevancia  = min(1.0, grounding.relevancia + 0.05)

        # Si Sebastian está presente y activo
        sebastian = contexto.get('sebastian', {})
        if sebastian:
            grounding.impacto_sebastian = min(1.0,
                grounding.impacto_sebastian + 0.05
            )

        return grounding

    def _ajustar_con_historial(
        self,
        grounding: Grounding9D,
        historial: dict
    ) -> Grounding9D:
        """
        Ajusta el grounding con el historial de uso.
        Bell aprende genuinamente.
        """
        tasa = historial.get('tasa_exito', 0.5)
        contextos = len(historial.get('contextos', []))

        # Más éxito → más confianza y ejecutabilidad
        delta_confianza = (tasa - 0.5) * 0.20
        grounding.confianza = max(0.1, min(1.0,
            grounding.confianza + delta_confianza
        ))
        grounding.ejecutabilidad = max(0.1, min(1.0,
            grounding.ejecutabilidad + delta_confianza * 0.5
        ))

        # Más contextos → más relacional y transferible
        if contextos > 3:
            grounding.relacional    = min(1.0, grounding.relacional + 0.05)
            grounding.transferible  = min(1.0, grounding.transferible + 0.05)

        # Marcar que viene del aprendizaje
        if tasa > 0.7:
            grounding.fuente = 'aprendido'
            grounding.version += 1

        return grounding

    def obtener_estadisticas(self) -> dict:
        """Estadísticas del aprendizaje de grounding."""
        if not self._historial_uso:
            return {'conceptos_aprendidos': 0}

        tasas = [
            h['tasa_exito']
            for h in self._historial_uso.values()
        ]
        return {
            'conceptos_aprendidos': len(self._historial_uso),
            'tasa_exito_promedio':  sum(tasas) / len(tasas),
            'conceptos_dominados':  sum(1 for t in tasas if t > 0.8),
        }