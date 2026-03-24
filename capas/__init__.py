# capas/__init__.py
# ================================================
# CAPAS — El flujo de procesamiento de Bell
# Cada capa es completamente independiente
# Se comunican solo a través de paquetes definidos
# ================================================

# Versión del sistema de capas
VERSION = '1.0.0'

# Capas disponibles
# Se actualiza automáticamente cuando
# se agregan nuevas capas
CAPAS_DISPONIBLES = []

def _detectar_capas():
    """
    Detecta qué capas están implementadas.
    """
    from pathlib import Path
    carpeta_capas = Path(__file__).parent

    for i in range(1, 10):
        carpeta_capa = carpeta_capas / f'capa{i}'
        if carpeta_capa.exists():
            CAPAS_DISPONIBLES.append(f'capa{i}')

_detectar_capas()