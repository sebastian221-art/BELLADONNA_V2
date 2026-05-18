# capas/capa7/clasificador_habilidad_groq.py
# ================================================
# CLASIFICADOR DE HABILIDAD — Bell nativo (sin Groq)
#
# Reemplaza la versión Groq. Misma interfaz,
# cero llamadas a API externa.
#
# La clasificación real ahora viene de C3
# (clasificador_bell.py → habilidad_req).
# Este archivo es solo fallback de compatibilidad.
# ================================================


class ClasificadorHabilidadGroq:

    def __init__(self):
        pass  # sin API key, sin dependencias externas

    def clasificar(self, texto: str, contexto_extra: str = '') -> dict | None:
        """
        Ya no usa Groq. Retorna None para que C7
        use el habilidad_req que viene de C3.
        """
        return None


_instancia = None

def obtener() -> ClasificadorHabilidadGroq:
    global _instancia
    if _instancia is None:
        _instancia = ClasificadorHabilidadGroq()
    return _instancia