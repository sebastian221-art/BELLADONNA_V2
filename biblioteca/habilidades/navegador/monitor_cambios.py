# biblioteca/habilidades/navegador/monitor_cambios.py
# ============================================================
# MONITOR DE CAMBIOS — Bell vigila URLs en segundo plano
#
# Corre en thread daemon, no bloquea. Detecta cambios por hash
# del contenido. Persiste en datos/monitores.json.
# Fallback-safe: si httpx/red falla, no rompe nada.
# ============================================================

import hashlib
import json
import os
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Optional


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
    return datos / 'monitores.json'


def _hash_contenido(texto: str) -> str:
    return hashlib.sha256((texto or '').encode('utf-8', 'ignore')).hexdigest()[:16]


class MonitorCambios:
    """Vigila URLs y reporta cambios. Singleton."""

    _instancia: Optional['MonitorCambios'] = None

    def __init__(self):
        self._ruta   = _ruta()
        self._datos  = self._cargar()
        self._activo = False
        self._hilo   = None
        self._cambios_pendientes = []

    @classmethod
    def obtener(cls) -> 'MonitorCambios':
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
        return {'activos': []}

    def _guardar(self):
        try:
            self._ruta.parent.mkdir(parents=True, exist_ok=True)
            tmp = self._ruta.with_name(self._ruta.name + '.tmp')
            with open(tmp, 'w', encoding='utf-8') as f:
                json.dump(self._datos, f, ensure_ascii=False, indent=2)
            os.replace(tmp, self._ruta)
        except Exception:
            pass

    # ── API pública ───────────────────────────────────────
    def agregar(self, url: str, objetivo: str, intervalo_minutos: int = 30) -> str:
        mid = f'mon_{len(self._datos["activos"]) + 1:03d}'
        self._datos['activos'].append({
            'id': mid, 'url': url, 'objetivo': objetivo,
            'hash_ultimo': '', 'ultimo_check': None,
            'intervalo_minutos': intervalo_minutos,
        })
        self._guardar()
        return mid

    def eliminar(self, id_monitor: str):
        self._datos['activos'] = [m for m in self._datos['activos'] if m.get('id') != id_monitor]
        self._guardar()

    def verificar_todos(self) -> list:
        cambios = []
        for m in self._datos['activos']:
            try:
                import httpx
                r = httpx.get(m['url'], timeout=10, follow_redirects=True,
                              headers={'User-Agent': 'Bell/1.0'})
                if r.status_code != 200:
                    continue
                h = _hash_contenido(r.text)
                if m['hash_ultimo'] and h != m['hash_ultimo']:
                    cambios.append({'id': m['id'], 'url': m['url'], 'objetivo': m['objetivo']})
                m['hash_ultimo'] = h
                m['ultimo_check'] = datetime.now().isoformat()[:19]
            except Exception:
                continue
        if cambios:
            self._cambios_pendientes.extend(cambios)
        self._guardar()
        return cambios

    def obtener_cambios_pendientes(self) -> list:
        c = list(self._cambios_pendientes)
        self._cambios_pendientes = []
        return c

    def iniciar_loop(self):
        if self._activo:
            return
        self._activo = True

        def _loop():
            while self._activo:
                try:
                    self.verificar_todos()
                except Exception:
                    pass
                time.sleep(max(60, 30 * 60))  # mínimo cada 30 min

        self._hilo = threading.Thread(target=_loop, daemon=True)
        self._hilo.start()

    def detener(self):
        self._activo = False
