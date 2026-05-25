# biblioteca/habilidades/lenguaje/memoria_sesion.py
# ============================================================
# MEMORIA DE SESIÓN — Continuidad emocional en la conversación
#
# Bell recuerda el estado emocional de Sebastian a lo largo
# de la sesión actual. No resetea entre turnos.
#
# Detecta:
#   - Patrón de ánimo acumulado (mejorando / empeorando / estable)
#   - Turnos consecutivos en estado negativo
#   - Cambios de estado (estaba bien, ahora está frustrado)
#   - Temas recurrentes de la sesión
# ============================================================

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class TurnoEmocional:
    texto:    str
    emocion:  str
    tipo:     str
    intensidad: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class EstadoSesion:
    patron_actual:        str   = 'neutro'
    # 'mejorando' | 'empeorando' | 'estable_positivo' | 'estable_negativo' | 'neutro'
    turnos_negativos_consecutivos: int = 0
    turnos_positivos_consecutivos: int = 0
    emocion_dominante:    str   = 'neutra'
    cambio_reciente:      bool  = False   # cambio de estado en últimos 2 turnos
    temas_sesion:         List[str] = field(default_factory=list)
    nota_bell:            str   = ''      # qué debería considerar Bell


class MemoriaSesion:
    """
    Acumula el historial emocional de la sesión actual.
    Singleton — una sola instancia por conversación.
    """

    _instancia: Optional['MemoriaSesion'] = None

    def __init__(self):
        self._turnos: List[TurnoEmocional] = []
        self._temas:  List[str]            = []

    @classmethod
    def obtener(cls) -> 'MemoriaSesion':
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    @classmethod
    def reiniciar(cls):
        cls._instancia = None

    # ── Registro ──────────────────────────────────────────

    def registrar_turno(self, texto: str, emocion: str,
                         tipo: str, intensidad: float = 0.5):
        """Registra un turno de la conversación."""
        turno = TurnoEmocional(
            texto=texto[:120],
            emocion=emocion or 'neutra',
            tipo=tipo,
            intensidad=intensidad,
        )
        self._turnos.append(turno)
        if len(self._turnos) > 20:
            self._turnos = self._turnos[-20:]

        # Extraer temas del texto
        _TEMAS = {
            'Bell': ['bell', 'belladonna'],
            'Python': ['python', 'código', 'bug', 'error', 'función'],
            'Hospital': ['hospital', 'twilio', 'paciente'],
            'trabajo': ['trabajo', 'jelcon', 'cliente', 'proyecto'],
        }
        for tema, palabras in _TEMAS.items():
            if any(p in texto.lower() for p in palabras):
                if tema not in self._temas:
                    self._temas.append(tema)

    # ── Análisis ──────────────────────────────────────────

    def obtener_estado(self) -> EstadoSesion:
        """Calcula el estado emocional actual de la sesión."""
        estado = EstadoSesion()

        if len(self._turnos) < 2:
            return estado

        ultimos = self._turnos[-6:]

        # Emociones negativas y positivas
        _NEG = {'frustracion', 'cansancio', 'ansiedad', 'tristeza', 'rabia',
                'soledad', 'resignacion', 'desesperacion', 'indefinido', 'tedio',
                'impaciencia', 'culpa', 'verguenza'}
        _POS = {'entusiasmo', 'orgullo', 'gratitud', 'esperanza', 'determinacion',
                'alivio', 'satisfaccion'}

        negativos = [t for t in ultimos if t.emocion in _NEG]
        positivos = [t for t in ultimos if t.emocion in _POS]

        estado.turnos_negativos_consecutivos = self._consecutivos_negativos()
        estado.turnos_positivos_consecutivos = self._consecutivos_positivos()

        # Patrón
        n_neg = len(negativos)
        n_pos = len(positivos)
        total = len(ultimos)

        if n_neg >= total * 0.6:
            estado.patron_actual = 'estable_negativo'
        elif n_pos >= total * 0.6:
            estado.patron_actual = 'estable_positivo'
        elif len(self._turnos) >= 3:
            # Tendencia: comparar primera mitad con segunda
            mitad = len(ultimos) // 2
            neg_reciente = sum(1 for t in ultimos[mitad:] if t.emocion in _NEG)
            neg_anterior = sum(1 for t in ultimos[:mitad] if t.emocion in _NEG)
            if neg_reciente > neg_anterior:
                estado.patron_actual = 'empeorando'
            elif neg_anterior > neg_reciente:
                estado.patron_actual = 'mejorando'
            else:
                estado.patron_actual = 'neutro'

        # Emoción dominante
        todas_emociones = [t.emocion for t in ultimos if t.emocion != 'neutra']
        if todas_emociones:
            from collections import Counter
            estado.emocion_dominante = Counter(todas_emociones).most_common(1)[0][0]

        # Cambio reciente (últimos 2 turnos cambiaron de positivo a negativo o viceversa)
        if len(ultimos) >= 2:
            prev = ultimos[-2].emocion
            curr = ultimos[-1].emocion
            if (prev in _POS and curr in _NEG) or (prev in _NEG and curr in _POS):
                estado.cambio_reciente = True

        estado.temas_sesion = self._temas[-5:]

        # Nota para Bell
        estado.nota_bell = self._generar_nota(estado)

        return estado

    def _consecutivos_negativos(self) -> int:
        count = 0
        _NEG = {'frustracion', 'cansancio', 'ansiedad', 'tristeza', 'rabia',
                'soledad', 'resignacion', 'desesperacion', 'indefinido', 'impaciencia'}
        for t in reversed(self._turnos):
            if t.emocion in _NEG:
                count += 1
            else:
                break
        return count

    def _consecutivos_positivos(self) -> int:
        count = 0
        _POS = {'entusiasmo', 'orgullo', 'gratitud', 'esperanza', 'determinacion'}
        for t in reversed(self._turnos):
            if t.emocion in _POS:
                count += 1
            else:
                break
        return count

    def _generar_nota(self, estado: EstadoSesion) -> str:
        """Genera una nota interna para que Bell ajuste su tono."""
        if estado.turnos_negativos_consecutivos >= 4:
            return ('Sebastian lleva varios turnos consecutivos en estado negativo. '
                    'Considerar ofrecer pausa o simplificar. No agregar más carga.')
        if estado.patron_actual == 'empeorando':
            return ('El ánimo ha ido bajando en la sesión. '
                    'Ser más directo y dar más apoyo antes que información.')
        if estado.patron_actual == 'estable_negativo':
            return 'Sesión difícil sostenida. Presencia y brevedad primero.'
        if estado.patron_actual == 'mejorando':
            return 'El ánimo está mejorando. Mantener el momentum positivo.'
        if estado.cambio_reciente:
            return 'Cambio emocional reciente — notar y adaptar tono.'
        return ''

    # ── Contexto para el prompt ───────────────────────────

    def contexto_para_groq(self) -> str:
        """Genera contexto emocional para inyectar al prompt de Groq."""
        estado = self.obtener_estado()
        if not estado.nota_bell:
            return ''

        lineas = ['[Contexto emocional de sesión]']
        if estado.patron_actual != 'neutro':
            lineas.append(f'Patrón: {estado.patron_actual}')
        if estado.emocion_dominante != 'neutra':
            lineas.append(f'Emoción dominante: {estado.emocion_dominante}')
        if estado.turnos_negativos_consecutivos >= 3:
            lineas.append(f'{estado.turnos_negativos_consecutivos} turnos negativos consecutivos')
        lineas.append(f'Nota: {estado.nota_bell}')

        return '\n'.join(lineas)

    def total_turnos(self) -> int:
        return len(self._turnos)