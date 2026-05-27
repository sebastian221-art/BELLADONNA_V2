# biblioteca/habilidades/memoria/destilador_conocimiento.py
# ============================================================
# DESTILADOR DE CONOCIMIENTO — principios, no blobs
#
# Antes de guardar lo aprendido, Groq destila el principio
# fundamental (≤30 palabras). Bell razona desde principios,
# no regurgita texto crudo. Si Groq falla → recorte simple.
#
# Groq solo destila (observa/comprime). No decide nada.
# ============================================================

import os
from typing import Optional

_GROQ_URL   = 'https://api.groq.com/openai/v1/chat/completions'
_GROQ_MODEL = os.getenv('GROQ_MODEL', 'openai/gpt-oss-120b')

_MAX_PALABRAS = 30
_FALLBACK_CHARS = 120


class DestiladorConocimiento:
    """Destila conocimiento crudo a principios. Singleton."""

    _instancia: Optional['DestiladorConocimiento'] = None

    @classmethod
    def obtener(cls) -> 'DestiladorConocimiento':
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def destilar(self, tema: str, texto_crudo: str) -> str:
        """Extrae el principio fundamental en ≤30 palabras."""
        texto_crudo = (texto_crudo or '').strip()
        if not texto_crudo:
            return ''
        principio = self._destilar_groq(tema, texto_crudo)
        if principio:
            return self._recortar(principio)
        # Fallback Python: primeros 120 chars del texto crudo
        return texto_crudo[:_FALLBACK_CHARS].strip()

    def guardar_con_destilacion(self, tema: str, texto_crudo: str,
                                 tipo: str, fuente: str, gestor) -> str:
        principio = self.destilar(tema, texto_crudo)
        try:
            gestor.guardar_conocimiento(tema, principio, tipo, fuente, confianza=0.9)
        except Exception:
            pass
        return principio

    # ── interno ───────────────────────────────────────────

    def _recortar(self, texto: str) -> str:
        palabras = texto.split()
        if len(palabras) <= _MAX_PALABRAS:
            return texto.strip()
        return ' '.join(palabras[:_MAX_PALABRAS]).rstrip('.,;:') + '.'

    def _destilar_groq(self, tema: str, texto_crudo: str) -> Optional[str]:
        api_key = os.getenv('GROQ_API_KEY', '')
        if not api_key:
            return None
        prompt = (
            f"Texto sobre '{tema}': {texto_crudo[:800]}\n"
            f"Extrae el principio fundamental en MÁXIMO {_MAX_PALABRAS} palabras. "
            "Solo el principio, sin introducción ni comillas."
        )
        try:
            import httpx
            r = httpx.post(
                _GROQ_URL,
                headers={'Authorization': f'Bearer {api_key}',
                         'Content-Type': 'application/json'},
                json={'model': _GROQ_MODEL,
                      'messages': [
                          {'role': 'system', 'content': 'Destilas ideas a su principio esencial. Conciso.'},
                          {'role': 'user', 'content': prompt}],
                      'temperature': 0.2, 'max_tokens': 80},
                timeout=10,
            )
            if r.status_code != 200:
                return None
            cont = (r.json().get('choices', [{}])[0]
                    .get('message', {}).get('content', '').strip())
            return cont or None
        except Exception:
            return None


# ── Conveniencia a nivel módulo ───────────────────────────

def destilar(tema: str, texto_crudo: str) -> str:
    return DestiladorConocimiento.obtener().destilar(tema, texto_crudo)


def guardar_con_destilacion(tema: str, texto_crudo: str,
                             tipo: str, fuente: str, gestor) -> str:
    return DestiladorConocimiento.obtener().guardar_con_destilacion(
        tema, texto_crudo, tipo, fuente, gestor
    )
