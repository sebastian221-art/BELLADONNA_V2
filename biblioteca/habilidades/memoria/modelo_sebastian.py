# biblioteca/habilidades/memoria/modelo_sebastian.py
# ============================================================
# MODELO DE SEBASTIAN — un modelo cognitivo, no una tabla de regex
#
# Filosofía Bell:
#   Groq OBSERVA hechos del mensaje (extractor semántico).
#   Python DECIDE si y dónde guardarlos. Groq nunca decide.
#   Si Groq falla → fallback regex determinístico (extractor_perfil).
#
# Estructura (datos/modelo_sebastian.json):
#   identidad   → nombre, edad, ciudad, trabajo, proyecto_principal
#   proyectos   → {nombre: {estado, ultima_actividad, tecnologias, pendientes}}
#   preferencias→ {tecnicas, comunicacion, filosofia}
#   patrones    → horario_activo, estado_emocional_frecuente, estilo_trabajo
# ============================================================

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

_GROQ_URL   = 'https://api.groq.com/openai/v1/chat/completions'
_GROQ_MODEL = os.getenv('GROQ_MODEL', 'openai/gpt-oss-120b')

_CAMPOS_IDENTIDAD = {'nombre', 'edad', 'ciudad', 'trabajo', 'estudio', 'proyecto_principal'}


def _raiz() -> Path:
    raiz = (os.environ.get('BELL_ROOT')
            or os.environ.get('BELLADONNA_ROOT')
            or os.environ.get('BELL_RAIZ'))
    if raiz:
        return Path(raiz)
    return Path(__file__).resolve().parents[3]


def _ruta_modelo() -> Path:
    datos = _raiz() / 'datos'
    datos.mkdir(parents=True, exist_ok=True)
    return datos / 'modelo_sebastian.json'


class ModeloSebastian:
    """Modelo cognitivo de Sebastian. Singleton."""

    _instancia: Optional['ModeloSebastian'] = None

    def __init__(self):
        self._ruta  = _ruta_modelo()
        self._datos = self._cargar_o_bootstrap()

    @classmethod
    def obtener(cls) -> 'ModeloSebastian':
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    # ── Carga / bootstrap ─────────────────────────────────

    def _estructura_vacia(self) -> dict:
        return {
            'identidad':    {},
            'proyectos':    {},
            'preferencias': {'tecnicas': [], 'comunicacion': [], 'filosofia': []},
            'patrones':     {},
            'actualizado':  None,
        }

    def _cargar_o_bootstrap(self) -> dict:
        base = self._estructura_vacia()
        # 1. Cargar archivo si existe
        try:
            if self._ruta.exists():
                with open(self._ruta, encoding='utf-8') as f:
                    datos = json.load(f)
                for k, v in base.items():
                    datos.setdefault(k, v)
                return datos
        except Exception:
            pass
        # 2. Bootstrap desde la memoria existente (SQLite + JSON)
        try:
            from biblioteca.habilidades.memoria.gestor import obtener_memoria
            perfil = obtener_memoria().obtener_perfil()
            for clave in ('nombre', 'edad', 'ciudad', 'trabajo', 'estudio'):
                if perfil.get(clave):
                    base['identidad'][clave] = perfil[clave]
            if perfil.get('proyecto') or perfil.get('proyecto_principal'):
                base['identidad']['proyecto_principal'] = (
                    perfil.get('proyecto_principal') or perfil.get('proyecto')
                )
        except Exception:
            pass
        try:
            from biblioteca.memoria.memoria_persistente import MemoriaPersistente
            sd = MemoriaPersistente.obtener().datos_sebastian()
            if sd.get('nombre_real'):
                base['identidad'].setdefault('nombre', sd['nombre_real'])
            if sd.get('edad'):
                base['identidad'].setdefault('edad', str(sd['edad']))
            if sd.get('lugar'):
                base['identidad'].setdefault('ciudad', sd['lugar'])
        except Exception:
            pass
        return base

    def _guardar(self):
        try:
            self._datos['actualizado'] = datetime.now().isoformat()[:19]
            self._ruta.parent.mkdir(parents=True, exist_ok=True)
            tmp = self._ruta.with_name(self._ruta.name + '.tmp')
            with open(tmp, 'w', encoding='utf-8') as f:
                json.dump(self._datos, f, ensure_ascii=False, indent=2)
            os.replace(tmp, self._ruta)
        except Exception:
            pass

    # ── API pública ───────────────────────────────────────

    def actualizar(self, mensaje: str, contexto: dict = None) -> bool:
        """
        Observa el mensaje y actualiza el modelo. Devuelve True si cambió.
        Groq extrae (si está); el regex determinístico siempre refuerza.
        Python decide qué entra. Nunca bloquea el pipeline.
        """
        if not mensaje or len(mensaje.strip()) < 3:
            return False
        cambios = False
        try:
            # 1. Groq como extractor semántico (si disponible)
            dato_groq = self._extraer_groq(mensaje)
            if dato_groq and float(dato_groq.get('confianza', 0)) > 0.7:
                cambios = self._aplicar_dato(dato_groq) or cambios
            # 2. Fallback/refuerzo regex — determinístico, siempre corre
            for d in self._extraer_regex(mensaje):
                cambios = self._aplicar_dato(d) or cambios
            if cambios:
                self._guardar()
        except Exception:
            pass
        return cambios

    def obtener_modelo(self) -> dict:
        return json.loads(json.dumps(self._datos))  # copia defensiva

    def obtener_compacto(self) -> str:
        """Modelo en ≤100 palabras para inyectar a prompts."""
        ident = self._datos.get('identidad', {})
        partes = []
        if ident.get('nombre'):  partes.append(f"{ident['nombre']}")
        if ident.get('edad'):    partes.append(f"{ident['edad']} años")
        if ident.get('ciudad'):  partes.append(f"de {ident['ciudad']}")
        if ident.get('trabajo'): partes.append(f"trabaja en {ident['trabajo']}")
        if ident.get('proyecto_principal'):
            partes.append(f"proyecto {ident['proyecto_principal']}")
        cab = ', '.join(partes)
        proyectos = self._datos.get('proyectos', {})
        activos = [n for n, v in proyectos.items()
                   if (v or {}).get('estado') != 'resuelto']
        prefs = self._datos.get('preferencias', {}).get('tecnicas', [])
        extra = []
        if activos:
            extra.append('Proyectos activos: ' + ', '.join(activos[:3]))
        if prefs:
            extra.append('Prefiere: ' + ', '.join(prefs[:2]))
        texto = '. '.join([p for p in [cab] + extra if p])
        return ' '.join(texto.split()[:100])

    # ── Extracción ────────────────────────────────────────

    def _extraer_groq(self, mensaje: str) -> Optional[dict]:
        api_key = os.getenv('GROQ_API_KEY', '')
        if not api_key:
            return None
        prompt = (
            f"Mensaje de Sebastian: '{mensaje[:400]}'\n"
            "Extrae SOLO hechos observables sobre Sebastian en JSON: "
            '{"nuevo_dato_detectado":"valor","tipo":"identidad|proyecto|preferencia|patron","confianza":0.0}. '
            "Si no hay dato nuevo sobre Sebastian, responde exactamente: null. "
            "No inventes. No expliques."
        )
        try:
            import httpx
            r = httpx.post(
                _GROQ_URL,
                headers={'Authorization': f'Bearer {api_key}',
                         'Content-Type': 'application/json'},
                json={'model': _GROQ_MODEL,
                      'messages': [
                          {'role': 'system', 'content': 'Eres un extractor de hechos. Solo JSON o null.'},
                          {'role': 'user', 'content': prompt}],
                      'temperature': 0.0, 'max_tokens': 120},
                timeout=10,
            )
            if r.status_code != 200:
                return None
            cont = (r.json().get('choices', [{}])[0]
                    .get('message', {}).get('content', '').strip())
            if cont.lower().startswith('null') or not cont:
                return None
            import re as _re
            m = _re.search(r'\{.*\}', cont, _re.DOTALL)
            if not m:
                return None
            data = json.loads(m.group(0))
            valor = str(data.get('nuevo_dato_detectado', '')).strip()
            if not valor:
                return None
            return {'campo': str(data.get('tipo', 'patron')),
                    'valor': valor,
                    'categoria': self._categoria_desde_tipo(str(data.get('tipo', ''))),
                    'confianza': float(data.get('confianza', 0.0))}
        except Exception:
            return None

    def _categoria_desde_tipo(self, tipo: str) -> str:
        t = tipo.lower()
        if 'proyecto' in t:      return 'proyecto'
        if 'prefer'  in t:       return 'preferencia'
        if 'patron'  in t:       return 'patron'
        return 'identidad'

    def _extraer_regex(self, mensaje: str) -> list:
        """Fallback determinístico — reutiliza extractor_perfil."""
        out = []
        try:
            from biblioteca.habilidades.memoria.extractor_perfil import extraer
            for d in extraer(mensaje):
                if d.tipo == 'dato' and d.clave in _CAMPOS_IDENTIDAD:
                    out.append({'campo': d.clave, 'valor': d.valor,
                                'categoria': 'identidad', 'confianza': d.confianza})
                elif d.tipo == 'proyecto':
                    out.append({'campo': 'nombre', 'valor': d.valor,
                                'categoria': 'proyecto', 'confianza': d.confianza})
                elif d.tipo == 'tecnologia':
                    out.append({'campo': 'tecnica', 'valor': f'usa {d.valor}',
                                'categoria': 'preferencia', 'confianza': d.confianza})
                elif d.tipo == 'preferencia':
                    out.append({'campo': 'tecnica', 'valor': d.valor,
                                'categoria': 'preferencia', 'confianza': d.confianza})
        except Exception:
            pass
        return out

    # ── Decisión: dónde guardar (Python, no Groq) ─────────

    def _aplicar_dato(self, dato: dict) -> bool:
        cat   = dato.get('categoria', 'identidad')
        valor = str(dato.get('valor', '')).strip()
        if not valor or len(valor) < 2:
            return False
        hoy = datetime.now().isoformat()[:10]

        if cat == 'identidad':
            campo = dato.get('campo', '')
            if campo not in _CAMPOS_IDENTIDAD:
                return False
            if self._datos['identidad'].get(campo) == valor:
                return False
            self._datos['identidad'][campo] = valor
            return True

        if cat == 'proyecto':
            proy = self._datos['proyectos']
            if valor not in proy:
                proy[valor] = {'estado': 'en_progreso', 'ultima_actividad': hoy,
                               'tecnologias': [], 'pendientes': []}
                return True
            proy[valor]['ultima_actividad'] = hoy
            return True

        if cat == 'preferencia':
            lista = self._datos['preferencias'].setdefault('tecnicas', [])
            if valor not in lista:
                lista.append(valor)
                return True
            return False

        if cat == 'patron':
            campo = dato.get('campo', 'nota')
            if self._datos['patrones'].get(campo) == valor:
                return False
            self._datos['patrones'][campo] = valor
            return True

        return False
