# biblioteca/persistencia_core.py
# ================================================
# PERSISTENCIA DE BELL_CORE
#
# Serializa/rehidrata la "vida" acumulada de BELL_CORE
# (perfil_vida.tipos, vitalidad, nivel_vida) a disco para
# que sobreviva reinicios del proceso.
#
# Sin dependencias pesadas: solo json + path. La dirección
# de import es capas → biblioteca, así que vive aquí.
# ================================================

import json
import os
from pathlib import Path


def _raiz() -> Path:
    raiz = os.environ.get('BELLADONNA_ROOT') or os.environ.get('BELL_RAIZ')
    if raiz:
        return Path(raiz)
    # Fallback: este archivo está en biblioteca/, raíz = su padre
    return Path(__file__).resolve().parent.parent


def ruta_estado_core() -> Path:
    return _raiz() / 'datos' / 'bell_core_state.json'


def guardar_estado_core(datos_extra: dict) -> bool:
    """Escribe el estado de vida de BELL_CORE a disco (atómico)."""
    try:
        perfil = (datos_extra or {}).get('perfil_vida', {}) or {}
        estado = {
            'tipos':      perfil.get('tipos', {}) or {},
            'vitalidad':  datos_extra.get('vitalidad', 0.0),
            'nivel_vida': datos_extra.get('nivel_vida', 'dormida'),
        }
        ruta = ruta_estado_core()
        ruta.parent.mkdir(parents=True, exist_ok=True)
        tmp = ruta.with_name(ruta.name + '.tmp')
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(estado, f, ensure_ascii=False, indent=2)
        os.replace(tmp, ruta)  # reemplazo atómico
        return True
    except Exception as e:
        print(f'  persistencia BELL_CORE: no se pudo guardar ({e})')
        return False


def cargar_estado_core():
    """Lee el estado de vida persistido, o None si no existe."""
    try:
        ruta = ruta_estado_core()
        if not ruta.exists():
            return None
        with open(ruta, encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f'  persistencia BELL_CORE: no se pudo leer ({e})')
        return None
