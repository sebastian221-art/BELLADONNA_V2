# biblioteca/habilidades/navegador/memoria_planes.py
# ============================================================
# MEMORIA DE PLANES EXITOSOS
#
# Cuando un plan funciona, Bell guarda qué selectores usó.
# La próxima vez parte de esos selectores en lugar de redescubrir.
# Si un selector falla 3 veces → se elimina.
# Persiste en datos/planes_exitosos.json.
# ============================================================

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

_UMBRAL_FALLOS = 3


def _raiz() -> Path:
    raiz = (os.environ.get('BELL_ROOT')
            or os.environ.get('BELLADONNA_ROOT')
            or os.environ.get('BELL_RAIZ'))
    if raiz:
        return Path(raiz)
    return Path(__file__).resolve().parents[3]


def _ruta() -> Path:
    datos = _raiz() / 'datos'
    datos.mkdir(parents=True, exist_ok=True)
    return datos / 'planes_exitosos.json'


class MemoriaPlanes:
    """Selectores que funcionaron, por tipo de plan. Singleton."""

    _instancia: Optional['MemoriaPlanes'] = None

    def __init__(self):
        self._ruta  = _ruta()
        self._datos = self._cargar()

    @classmethod
    def obtener(cls) -> 'MemoriaPlanes':
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def _cargar(self) -> dict:
        try:
            if self._ruta.exists():
                with open(self._ruta, encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return {}

    def _guardar(self):
        try:
            self._ruta.parent.mkdir(parents=True, exist_ok=True)
            tmp = self._ruta.with_name(self._ruta.name + '.tmp')
            with open(tmp, 'w', encoding='utf-8') as f:
                json.dump(self._datos, f, ensure_ascii=False, indent=2)
            os.replace(tmp, self._ruta)
        except Exception:
            pass

    def _plan(self, nombre: str) -> dict:
        return self._datos.setdefault(nombre, {
            'ultimo_exito': None,
            'selectores': {},
            'fallos_selector': {},
            'tiempo_promedio_ms': 0,
            'veces_exitoso': 0,
            'veces_fallido': 0,
        })

    # ── API pública ───────────────────────────────────────
    def guardar_exito(self, nombre_plan: str, selectores_usados: dict, tiempo_ms: int = 0):
        p = self._plan(nombre_plan)
        for nombre, sel in (selectores_usados or {}).items():
            if sel:
                p['selectores'][nombre] = sel
                p['fallos_selector'].pop(nombre, None)  # reset fallos al funcionar
        p['veces_exitoso'] += 1
        if tiempo_ms:
            n = p['veces_exitoso']
            p['tiempo_promedio_ms'] = int((p['tiempo_promedio_ms'] * (n - 1) + tiempo_ms) / n)
        p['ultimo_exito'] = datetime.now().isoformat()[:10]
        self._guardar()

    def guardar_fallo(self, nombre_plan: str, selector_que_fallo: str):
        p = self._plan(nombre_plan)
        p['veces_fallido'] += 1
        if selector_que_fallo:
            fallos = p['fallos_selector']
            fallos[selector_que_fallo] = fallos.get(selector_que_fallo, 0) + 1
            if fallos[selector_que_fallo] >= _UMBRAL_FALLOS:
                # Eliminar el selector roto de los validados
                for nombre, sel in list(p['selectores'].items()):
                    if sel == selector_que_fallo:
                        p['selectores'].pop(nombre, None)
                fallos.pop(selector_que_fallo, None)
        self._guardar()

    def obtener_selectores(self, nombre_plan: str) -> dict:
        return dict(self._datos.get(nombre_plan, {}).get('selectores', {}))
