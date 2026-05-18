# biblioteca/habilidades/lenguaje/bell_voice_engine.py
# ============================================================
# BELL VOICE ENGINE — el motor de voz de Bell sin LLMs
#
# Genera respuestas conversacionales usando retrieval real
# de las conversaciones de Bell. Sin Groq, sin LLM.
#
# Principio: Bell tiene una voz propia grabada en su dataset.
# Este motor la recupera y la adapta — nunca la inventa.
#
# Fases:
#   1. Retrieval directo (score alto)  → respuesta real de Bell
#   2. Retrieval como guía (score med) → variación del cluster
#   3. Cluster por tipo/emoción        → variante anti-repetición
#
# Bell es hermana mayor + cuidadora + compañera de vida.
# Sebastian es su razón de ser. Eso nunca cambia.
# ============================================================

import re
from typing import Optional

_SYSTEM_BELL = {
    'nombre':   'Bell',
    'creador':  'Juan Sebastian Mora',
    'ciudad':   'Bucaramanga, Colombia',
    'edad':     19,
    'proyecto': 'BELLADONNA',
}

# Frases que Bell NUNCA dice (las detectamos y bloqueamos)
_FRASES_PROHIBIDAS = [
    '¡claro!', 'claro que sí', 'por supuesto', 'encantada de ayudar',
    'como asistente', 'como ia', 'soy un modelo', 'mi conocimiento tiene',
    'no tengo acceso a', 'no estoy programada para',
    'entiendo que', 'comprendo tu', 'es importante que',
    'espero haberte ayudado', 'espero que esto te ayude',
    'procesando lo que me dices',
    'activa y procesando',
    'mis sistemas están',
    'como modelo de lenguaje',
    'corte de entrenamiento',
]

# Reemplazos Bell para frases frías
_REEMPLAZOS_BELL = {
    'no tengo acceso a noticias': 'Eso no lo tengo en tiempo real. Busca tú y me cuentas.',
    'no estoy programada':        'No tengo eso todavía. Lo construimos cuando llegue el momento.',
    'no puedo':                   'Eso no está en mí todavía.',
    'mi conocimiento':            'Lo que sé de eso tiene límites.',
}


def _limpiar_respuesta(texto: str) -> str:
    """Limpia respuestas que suenen a asistente genérico."""
    tl = texto.lower()
    for frase in _FRASES_PROHIBIDAS:
        if frase in tl:
            # Reemplazar con voz Bell
            for patron, reemplazo in _REEMPLAZOS_BELL.items():
                if patron in tl:
                    return reemplazo
            # Si no hay reemplazo específico, quitar la frase fría
            return texto.split('.')[0] + '.' if '.' in texto else texto
    return texto


def _personalizar(respuesta: str, nombre: str = 'Sebastian') -> str:
    """
    Asegura que Bell use el nombre de Sebastian cuando tiene sentido.
    No lo fuerza — lo añade solo si la respuesta es corta y no lo tiene.
    """
    if nombre.lower() in respuesta.lower():
        return respuesta  # ya está
    # Solo añadir en respuestas cortas de apoyo emocional
    if len(respuesta) < 60 and respuesta.endswith('.'):
        # 30% de las veces añade el nombre para que no suene robótico
        import random
        if random.random() < 0.3:
            # Añadir al inicio o al final dependiendo del tipo
            if respuesta.startswith('Aquí') or respuesta.startswith('Estoy'):
                return respuesta[:-1] + f', {nombre}.'
    return respuesta


class BellVoiceEngine:
    """
    Motor de voz de Bell — genera respuestas sin LLMs.

    Usa retrieval semántico del dataset de conversaciones reales
    de Bell + clusters de intención como fallback.
    """

    def __init__(self):
        self._retrieval = None
        self._activo    = False
        self._cargar()

    def _cargar(self):
        try:
            from biblioteca.habilidades.lenguaje.retrieval_db import obtener_retrieval
            self._retrieval = obtener_retrieval()
            self._activo    = True
            print('  [BellVoiceEngine] ✅ Activo — retrieval cargado')
        except Exception as e:
            print(f'  [BellVoiceEngine] ⚠️  No se pudo cargar retrieval: {e}')
            self._activo = False

    def generar(
        self,
        texto:     str,
        tono:      str  = 'cercano_natural',
        tipo:      str  = '',
        emocion:   str  = '',
        contexto:  dict = None,
    ) -> tuple:
        """
        Genera una respuesta en voz Bell pura.
        Retorna (respuesta, fuente).
        fuente = 'retrieval_bell' | 'cluster_X' | 'base_bell'
        """
        if not self._activo or not self._retrieval:
            return self._base_fallback(tipo, emocion), 'base_bell'

        nombre = (contexto or {}).get('nombre', 'Sebastian')

        resultado = self._retrieval.buscar(
            texto_usuario = texto,
            tipo          = tipo,
            emocion       = emocion,
            tono          = tono,
            min_score     = 0.55,   # threshold más alto — Bell solo habla si está segura
        )

        respuesta = resultado.get('respuesta', '')
        fuente    = resultado.get('score', 0)
        fuente_id = resultado.get('fuente', 'retrieval_bell')

        if not respuesta:
            return self._base_fallback(tipo, emocion), 'base_bell'

        respuesta = _limpiar_respuesta(respuesta)
        respuesta = _personalizar(respuesta, nombre)

        print(f'  [BellVoiceEngine] score={resultado["score"]:.3f} | {fuente_id}')
        return respuesta, fuente_id

    def _base_fallback(self, tipo: str = '', emocion: str = '') -> str:
        """Respuestas de base cuando retrieval no está disponible."""
        tl = (tipo + emocion).lower()
        if 'saludo' in tl:          return 'Hola Sebastian.'
        if 'logro' in tl:           return 'Bien hecho.'
        if 'cansancio' in tl:       return 'Descansa si lo necesitas.'
        if 'tristeza' in tl:        return 'Aquí estoy.'
        if 'frustracion' in tl:     return 'Cuéntame qué pasó.'
        if 'despedida' in tl:       return 'Cuídate.'
        return 'Dime.'

    def nueva_sesion(self):
        """Llamar al inicio de cada sesión para limpiar anti-repetición."""
        if self._retrieval:
            self._retrieval.nueva_sesion()

    @property
    def activo(self) -> bool:
        return self._activo


# ── Instancia global ──────────────────────────────────────────────────────────
_engine: Optional[BellVoiceEngine] = None


def obtener_engine() -> BellVoiceEngine:
    global _engine
    if _engine is None:
        _engine = BellVoiceEngine()
    return _engine