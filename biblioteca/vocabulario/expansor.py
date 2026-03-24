# biblioteca/vocabulario/expansor.py
# ================================================
# EXPANSOR DE VOCABULARIO
# Integra palabras nuevas a la red neuronal
# Todo lo que Bell aprende pasa por aquí
# ================================================

class ExpansorVocabulario:
    """
    Cuando Bell encuentra una palabra nueva
    este expansor la integra al vocabulario
    y la conecta a la red neuronal.

    Principio: aprender = agregar al vocabulario
    + crear nodo en la biblioteca + conectar.
    """

    def __init__(self, gestor_vocabulario, biblioteca):
        self.vocab     = gestor_vocabulario
        self.biblioteca = biblioteca

    def integrar_palabra_nueva(
        self,
        palabra: str,
        concepto_id: str,
        grounding: float,
        tipo: str = 'concepto'
    ) -> dict:
        """
        Integra una palabra nueva completamente:
        1. La agrega al vocabulario
        2. Crea su nodo en la biblioteca
        3. Lo conecta inteligentemente
        """
        # 1. Agregar al vocabulario
        self.vocab.agregar_en_tiempo_real(
            palabra, concepto_id, grounding, tipo
        )

        # 2. Integrar a la biblioteca neuronal
        reporte = self.biblioteca.integrar_concepto(
            concepto_id, grounding, tipo
        )

        return {
            'palabra':     palabra,
            'concepto_id': concepto_id,
            'grounding':   grounding,
            'integrado':   True,
            'reporte':     reporte
        }

    def integrar_desde_desconocido(
        self,
        fragmento: str,
        solucion: dict
    ) -> dict:
        """
        Cuando Bell resuelve algo desconocido
        lo integra al vocabulario y a la red.
        """
        concepto_id = solucion.get('id', f'APRENDIDO_{fragmento.upper()}')
        grounding   = solucion.get('grounding', 0.5)
        tipo        = solucion.get('tipo', 'concepto')

        return self.integrar_palabra_nueva(
            fragmento, concepto_id, grounding, tipo
        )