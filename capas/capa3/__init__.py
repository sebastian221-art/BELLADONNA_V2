# capas/capa3/__init__.py
# ================================================
# CAPA 3 — COMPRENSIÓN PROFUNDA
# Recibe la red activa de la Capa 2
# Construye tres comprensiones simultáneas:
# literal, contextual y profunda
# ================================================

from capas.capa3.paquete_capa3 import PaqueteCapa3
from capas.capa3.constructor_comprension import ConstructorComprension
from capas.capa3.detector_ambiguedad import DetectorAmbiguedad
from capas.capa3.detector_gaps import DetectorGaps
from capas.capa3.consejeras.lyra_capa3 import LyraCapa3
from capas.capa3.consejeras.echo_capa3 import EchoCapa3

# Instancias que se reusan
_constructor   = ConstructorComprension()
_ambiguedad    = DetectorAmbiguedad()
_gaps          = DetectorGaps()
_lyra          = LyraCapa3()
_echo          = EchoCapa3()


def procesar(paquete_capa2: dict) -> dict:
    """
    La única función pública de la Capa 3.
    Recibe el paquete de la Capa 2.
    Retorna siempre un diccionario.
    Nunca lanza excepciones.
    """
    try:
        return _procesar_interno(paquete_capa2)
    except Exception as e:
        return {
            'exitoso':       False,
            'error':         f'Error en Capa 3: {str(e)}',
            'comprension':   {},
            'paquete_capa2': paquete_capa2
        }


def _procesar_interno(paquete_capa2: dict) -> dict:
    """El procesamiento interno de la Capa 3."""

    red_activa   = paquete_capa2.get('red_activa', {})
    paquete_c1   = paquete_capa2.get('paquete_capa1', {})
    texto_original = paquete_c1.get('contenido_original', '')
    contexto       = paquete_c1.get('contexto', {})
    tono           = paquete_c1.get('tono_detectado', 'neutral')

    # ---- 1. CONSTRUIR TRES COMPRENSIONES ----
    comprension = _constructor.construir(
        red_activa=red_activa,
        texto_original=texto_original,
        contexto=contexto,
        tono=tono
    )

    # ---- 2. DETECTAR AMBIGÜEDAD ----
    resultado_ambiguedad = _ambiguedad.detectar(
        comprension=comprension,
        contexto=contexto
    )

    # ---- 3. LYRA — LECTURA EMOCIONAL ----
    lectura_lyra = _lyra.leer(
        texto_original=texto_original,
        tono=tono,
        comprension_profunda=comprension.get('profunda', {}),
        contexto=contexto
    )

    # ---- 4. ECHO — VERIFICAR COHERENCIA ----
    verificacion_echo = _echo.verificar(
        comprension=comprension,
        texto_original=texto_original,
        red_activa=red_activa
    )

    # ---- 5. DETECTAR GAPS ----
    gaps = _gaps.detectar(
        comprension=comprension,
        red_activa=red_activa,
        desconocidos=paquete_c1.get('desconocidos', [])
    )

    # ---- 6. CONSTRUIR PAQUETE ----
    paquete = PaqueteCapa3(
        comprension=comprension,
        ambiguedad=resultado_ambiguedad,
        lectura_lyra=lectura_lyra,
        verificacion_echo=verificacion_echo,
        gaps=gaps,
        nivel_certeza=_calcular_certeza_global(
            comprension, verificacion_echo
        ),
        lista_para_capa4=_esta_lista_para_capa4(
            resultado_ambiguedad, gaps
        ),
        paquete_capa2=paquete_capa2
    )

    return paquete.a_dict()


def _calcular_certeza_global(
    comprension: dict,
    verificacion_echo: dict
) -> float:
    """Calcula la certeza global de la comprensión."""
    certeza_literal    = comprension.get('literal', {}).get('certeza', 0)
    certeza_contextual = comprension.get('contextual', {}).get('certeza', 0)
    certeza_profunda   = comprension.get('profunda', {}).get('certeza', 0)
    coherencia_echo    = 1.0 if verificacion_echo.get('coherente', False) else 0.6

    return (
        certeza_literal    * 0.35 +
        certeza_contextual * 0.35 +
        certeza_profunda   * 0.20 +
        coherencia_echo    * 0.10
    )


def _esta_lista_para_capa4(
    ambiguedad: dict,
    gaps: list
) -> bool:
    """Determina si la comprensión es suficiente para continuar."""
    if ambiguedad.get('nivel') == 'critica':
        return False
    gaps_criticos = [g for g in gaps if g.get('critico', False)]
    if gaps_criticos:
        return False
    return True