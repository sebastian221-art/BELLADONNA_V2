# biblioteca/habilidades/navegador/conocimiento_web.py
# ============================================================
# CONOCIMIENTO WEB — la memoria del navegador de Bell
#
# Guarda en datos/conocimiento_web.json lo que Bell aprende de
# cada sitio: selectores validados, análisis de páginas, APIs.
# Principio: Bell nunca redescubre lo que ya sabe. No repite el
# mismo análisis de screenshot (< 7 días).
# ============================================================

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

_DIAS_FRESCO = 7


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
    return datos / 'conocimiento_web.json'


def extraer_dominio(url: str) -> str:
    try:
        net = urlparse(url).netloc.lower()
        return net[4:] if net.startswith('www.') else net
    except Exception:
        return (url or '').lower()


class ConocimientoWeb:
    """Memoria persistente del navegador. Singleton."""

    _instancia: Optional['ConocimientoWeb'] = None

    def __init__(self):
        self._ruta  = _ruta()
        self._datos = self._cargar()

    @classmethod
    def obtener(cls) -> 'ConocimientoWeb':
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    # ── persistencia ──────────────────────────────────────
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

    def _sitio(self, dominio: str) -> dict:
        return self._datos.setdefault(dominio, {
            'ultima_visita': None,
            'selectores_validados': {},
            'estructura_detectada': '',
            'apis_disponibles': [],
            'requiere_login': False,
            'analisis_urls': {},   # url -> {fecha, descripcion, elementos}
            'notas': '',
        })

    # ── API pública ───────────────────────────────────────
    def obtener_sitio(self, dominio: str) -> dict:
        return dict(self._datos.get(dominio, {}))

    def guardar_selector(self, dominio: str, nombre: str, selector: str, funciono: bool):
        s = self._sitio(dominio)
        if funciono:
            s['selectores_validados'][nombre] = selector
        else:
            s['selectores_validados'].pop(nombre, None)
        s['ultima_visita'] = datetime.now().isoformat()[:10]
        self._guardar()

    def selector_conocido(self, dominio: str, nombre: str) -> Optional[str]:
        return self._datos.get(dominio, {}).get('selectores_validados', {}).get(nombre)

    def marcar_selector_roto(self, dominio: str, nombre: str):
        s = self._datos.get(dominio, {})
        if s:
            s.get('selectores_validados', {}).pop(nombre, None)
            self._guardar()

    def tiene_api(self, dominio: str):
        apis = self._datos.get(dominio, {}).get('apis_disponibles', [])
        return (bool(apis), apis[0] if apis else '')

    def necesita_screenshot(self, url: str) -> bool:
        """True si nunca se analizó esta URL o el análisis es viejo (>7 días)."""
        dominio = extraer_dominio(url)
        analisis = self._datos.get(dominio, {}).get('analisis_urls', {}).get(url)
        if not analisis:
            return True
        try:
            fecha = datetime.fromisoformat(analisis.get('fecha', ''))
            return (datetime.now() - fecha) > timedelta(days=_DIAS_FRESCO)
        except Exception:
            return True

    def guardar_analisis_screenshot(self, dominio: str, url: str,
                                     descripcion_groq: str,
                                     elementos_detectados) -> None:
        s = self._sitio(dominio)
        s['analisis_urls'][url] = {
            'fecha':       datetime.now().isoformat(),
            'descripcion': descripcion_groq,
            'elementos':   elementos_detectados or [],
        }
        if descripcion_groq and not s.get('estructura_detectada'):
            s['estructura_detectada'] = descripcion_groq[:200]
        s['ultima_visita'] = datetime.now().isoformat()[:10]
        self._guardar()

    def analisis_previo(self, url: str) -> dict:
        dominio = extraer_dominio(url)
        return self._datos.get(dominio, {}).get('analisis_urls', {}).get(url, {})
