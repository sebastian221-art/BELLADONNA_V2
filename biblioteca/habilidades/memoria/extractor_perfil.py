# biblioteca/habilidades/memoria/extractor_perfil.py
# ============================================================
# EXTRACTOR DE PERFIL — Aprende sobre Sebastian en cada turno
#
# El gestor actual tiene 6 regex rígidos que capturan muy poco.
# Este módulo usa patrones más ricos y contexto semántico para
# detectar todo lo que Sebastian comparte sobre sí mismo.
#
# Detecta:
#   - Proyectos activos ("estoy trabajando en el Hospital")
#   - Tecnologías que usa ("uso FastAPI para esto")
#   - Estado emocional del día ("hoy estoy agotado")
#   - Logros y avances ("terminé el módulo de memoria")
#   - Preferencias ("prefiero esto a aquello")
#   - Datos personales (ciudad, trabajo, edad, etc.)
# ============================================================

import re
from dataclasses import dataclass, field
from typing import List, Optional, Tuple


@dataclass
class DatoExtraido:
    clave:     str
    valor:     str
    tipo:      str    # dato | preferencia | patron | proyecto | logro | tecnologia
    confianza: float  # 0.0 - 1.0
    fuente:    str    # "Sebastian lo dijo" | "inferido"


# ── Patrones extendidos ───────────────────────────────────

_PATRONES = [
    # Datos personales
    (r'tengo\s+(\d+)\s+a[ñn]os',                    'edad',     'dato',       0.95, 'Sebastian lo dijo'),
    (r'vivo\s+en\s+([\w\s]+?)(?:\.|,|$)',             'ciudad',   'dato',       0.90, 'Sebastian lo dijo'),
    (r'soy\s+de\s+([\w\s]+?)(?:\.|,|$)',              'ciudad',   'dato',       0.85, 'Sebastian lo dijo'),
    (r'trabajo\s+(?:en|con)\s+([\w\s]+?)(?:\.|,|$)', 'trabajo',  'dato',       0.90, 'Sebastian lo dijo'),
    (r'estudi[oó]\s+(?:en\s+)?([\w\s]+?)(?:\.|,|$)', 'estudio',  'dato',       0.85, 'Sebastian lo dijo'),

    # Proyectos activos
    (r'(?:proyecto|app|aplicación|sistema)\s+(?:se llama\s+|llamado\s+|es\s+)?([\w\s]+?)(?:\.|,|$)',
                                                      'proyecto_activo', 'proyecto', 0.80, 'Sebastian lo mencionó'),
    (r'(?:estoy|voy|vamos)\s+(?:a\s+)?(?:trabajar en|construyendo|desarrollando|creando)\s+([\w\s]+?)(?:\.|,|$)',
                                                      'proyecto_activo', 'proyecto', 0.75, 'inferido'),
    (r'(?:el|mi)\s+(?:hospital|cliente|empresa)\s+([\w]+)',
                                                      'cliente_activo', 'proyecto', 0.80, 'Sebastian lo mencionó'),

    # Tecnologías
    (r'(?:uso|usamos|usé|usamos|con)\s+(fastapi|flask|django|react|vue|postgres|mysql|redis|docker|kubernetes)',
                                                      'tecnologia', 'tecnologia', 0.90, 'Sebastian lo dijo'),
    (r'(?:uso|con)\s+(python|javascript|typescript|rust|go|java)',
                                                      'lenguaje_pref', 'tecnologia', 0.90, 'Sebastian lo dijo'),

    # Preferencias
    (r'prefiero\s+([\w\s]+?)(?:\s+a\s+|\s+sobre\s+|\.)',
                                                      'preferencia', 'preferencia', 0.85, 'Sebastian lo dijo'),
    (r'me\s+gusta\s+(?:más\s+)?([\w\s]+?)(?:\.|,|$)',
                                                      'gusto',    'preferencia', 0.80, 'Sebastian lo dijo'),
    (r'no\s+me\s+gusta\s+([\w\s]+?)(?:\.|,|$)',
                                                      'no_gusta', 'preferencia', 0.80, 'Sebastian lo dijo'),
]


# ── Detección de logros ───────────────────────────────────

_PATRONES_LOGRO = [
    r'terminé\s+([\w\s]+?)(?:\.|,|$)',
    r'logré\s+([\w\s]+?)(?:\.|,|$)',
    r'ya\s+funciona\s+([\w\s]+?)(?:\.|,|$)',
    r'completé\s+([\w\s]+?)(?:\.|,|$)',
    r'(?:por fin|al fin)\s+(?:funciona|terminé|logré)\s+([\w\s]+?)(?:\.|,|$)',
]


# ── API pública ───────────────────────────────────────────

def extraer(mensaje: str, respuesta: str = '') -> List[DatoExtraido]:
    """
    Extrae todos los datos posibles del mensaje de Sebastian.
    Retorna lista de DatoExtraido listos para guardar en perfil.
    """
    datos: List[DatoExtraido] = []
    tl = mensaje.lower().strip()

    # Patrones estándar
    for patron, clave, tipo, confianza, fuente in _PATRONES:
        m = re.search(patron, tl)
        if m:
            valor = m.group(1).strip() if m.lastindex else m.group(0).strip()
            valor = _limpiar_valor(valor)
            if valor and len(valor) >= 2:
                datos.append(DatoExtraido(
                    clave=clave, valor=valor, tipo=tipo,
                    confianza=confianza, fuente=fuente
                ))

    # Logros
    for patron in _PATRONES_LOGRO:
        m = re.search(patron, tl)
        if m and m.lastindex:
            valor = _limpiar_valor(m.group(1))
            if valor and len(valor) >= 3:
                datos.append(DatoExtraido(
                    clave='logro_reciente', valor=valor, tipo='logro',
                    confianza=0.85, fuente='Sebastian lo mencionó'
                ))

    # Deduplicar por clave (quedarse con el de mayor confianza)
    vistos: dict = {}
    for d in datos:
        if d.clave not in vistos or d.confianza > vistos[d.clave].confianza:
            vistos[d.clave] = d

    return list(vistos.values())


def _limpiar_valor(valor: str) -> str:
    """Limpia el valor extraído de stopwords y puntuación."""
    valor = re.sub(r'[.,;:!?]', '', valor).strip()
    _STOP = {'el', 'la', 'los', 'las', 'un', 'una', 'de', 'del', 'al',
             'en', 'con', 'por', 'para', 'que', 'se', 'mi', 'tu', 'su'}
    palabras = [p for p in valor.split() if p not in _STOP]
    return ' '.join(palabras[:4])  # máximo 4 palabras


def detectar_estado_del_dia(mensaje: str) -> Optional[str]:
    """Detecta si Sebastian menciona cómo está hoy."""
    tl = mensaje.lower()
    _ESTADOS = [
        (['muy bien', 'excelente', 'genial', 'de maravilla'], 'excelente'),
        (['bien',  'bien hoy', 'estoy bien'],                 'bien'),
        (['más o menos', 'regular', 'así así'],               'regular'),
        (['cansado', 'agotado', 'sin energía'],               'cansado'),
        (['mal', 'muy mal', 'pésimo', 'terrible'],            'mal'),
        (['estresado', 'con estrés', 'bajo presión'],         'estresado'),
    ]
    for palabras, estado in _ESTADOS:
        if any(p in tl for p in palabras):
            return estado
    return None