# biblioteca/habilidades/memoria/recuperador_inteligente.py
# ============================================================
# RECUPERADOR INTELIGENTE — recupera por tipo de consulta
#
# Reemplaza el LIKE ciego. Según el tipo (lo decide motor_memoria
# en Python), va al store correcto y devuelve un string factual.
# Si no hay datos → honesto ("No tengo registro de eso").
# ============================================================

import json
import re
from typing import Optional

PERFIL       = 'PERFIL'
EPISODIO     = 'EPISODIO'
CONOCIMIENTO = 'CONOCIMIENTO'
BELL_SELF    = 'BELL_SELF'
SESION       = 'SESION'


class RecuperadorInteligente:
    """Recuperación de memoria por tipo. Singleton."""

    _instancia: Optional['RecuperadorInteligente'] = None

    @classmethod
    def obtener(cls) -> 'RecuperadorInteligente':
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def recuperar(self, texto: str, tipo: str, gestor) -> str:
        try:
            if tipo == PERFIL:       return self._perfil(gestor)
            if tipo == EPISODIO:     return self._episodio(texto, gestor)
            if tipo == CONOCIMIENTO: return self._conocimiento(texto, gestor)
            if tipo == BELL_SELF:    return self._bell_self(gestor)
            return self._sesion(gestor)
        except Exception:
            return ''

    # ── PERFIL ────────────────────────────────────────────

    def _perfil(self, gestor) -> str:
        ident = {}
        proyectos = {}
        prefs = {}
        try:
            from biblioteca.habilidades.memoria.modelo_sebastian import ModeloSebastian
            modelo = ModeloSebastian.obtener().obtener_modelo()
            ident     = modelo.get('identidad', {}) or {}
            proyectos = modelo.get('proyectos', {}) or {}
            prefs     = modelo.get('preferencias', {}) or {}
        except Exception:
            pass
        # Reforzar con perfil SQLite
        try:
            psql = gestor.obtener_perfil()
            for k in ('nombre', 'edad', 'ciudad', 'trabajo', 'estudio'):
                if not ident.get(k) and psql.get(k):
                    ident[k] = psql[k]
        except Exception:
            pass

        frases = []
        cab = []
        if ident.get('nombre'):  cab.append(f"eres {ident['nombre']}")
        if ident.get('edad'):    cab.append(f"{ident['edad']} años")
        if ident.get('ciudad'):  cab.append(f"de {ident['ciudad']}")
        if cab:
            frases.append('Sé que ' + ', '.join(cab) + '.')
        if ident.get('trabajo'):
            frases.append(f"Trabajas en {ident['trabajo']}.")
        if ident.get('estudio'):
            frases.append(f"Estudias {ident['estudio']}.")
        if ident.get('proyecto_principal'):
            frases.append(f"Tu proyecto principal es {ident['proyecto_principal']}.")

        activos = [n for n, v in proyectos.items() if (v or {}).get('estado') != 'resuelto']
        if activos:
            frases.append('Proyectos activos: ' + ', '.join(activos[:3]) + '.')
        tecnicas = (prefs.get('tecnicas') or [])[:2]
        if tecnicas:
            frases.append('Sé que ' + '; '.join(tecnicas) + '.')

        return ' '.join(frases)

    # ── EPISODIO ──────────────────────────────────────────

    def _episodio(self, texto: str, gestor) -> str:
        episodios = []
        try:
            episodios = gestor.obtener_episodio_estructurado(5)
        except Exception:
            try:
                episodios = gestor.obtener_episodios_recientes(5)
            except Exception:
                episodios = []
        if not episodios:
            return ''

        # Filtrar por palabras clave del texto (Python puro)
        palabras = [w for w in texto.lower().split() if len(w) > 4]
        def _relevante(ep):
            blob = json.dumps(ep, ensure_ascii=False).lower()
            return any(w in blob for w in palabras)
        relevantes = [e for e in episodios if _relevante(e)] or episodios
        ep = relevantes[0]

        # Episodio estructurado
        if isinstance(ep, dict) and ep.get('tema_principal'):
            partes = [f"La última vez trabajamos en {ep['tema_principal']}."]
            if ep.get('proyecto_activo'):
                est = ep.get('estado_proyecto')
                partes.append(f"Proyecto {ep['proyecto_activo']}"
                              + (f" ({est})." if est else "."))
            pend = ep.get('pendientes') or []
            if pend:
                partes.append('Quedó pendiente: ' + '; '.join(pend[:2]) + '.')
            dec = ep.get('decisiones') or []
            if dec:
                partes.append('Decidiste: ' + dec[0] + '.')
            return ' '.join(partes)

        # Episodio narrativo (backward compat)
        if isinstance(ep, dict):
            res = ep.get('resumen', '')
            fecha = (ep.get('fecha', '') or '')[:10]
            if res:
                return (f"{fecha}: " if fecha else '') + res[:220]
        return ''

    # ── CONOCIMIENTO ──────────────────────────────────────

    def _conocimiento(self, texto: str, gestor) -> str:
        # 1. Extraer tema ("...sobre/de X")
        m = re.search(r'(?:sobre|de|del|acerca de)\s+([\wáéíóúñ][\wáéíóúñ\s]{1,40})', texto.lower())
        tema = m.group(1).strip() if m else None
        if tema:
            # primera palabra significativa del tema
            tema_kw = tema.split()[0] if tema.split() else tema
            try:
                r = gestor.consultar_conocimiento(tema_kw)
                if r and r.get('respuesta'):
                    return r['respuesta']
            except Exception:
                pass
        # 2. Fallback semántico/LIKE en principios
        try:
            r2 = gestor.buscar_semantico(texto)
            if r2:
                return r2
        except Exception:
            pass
        return ''

    # ── BELL_SELF ─────────────────────────────────────────

    def _bell_self(self, gestor) -> str:
        partes = []
        # Conversaciones desde MemoriaPersistente (JSON, fuente viva)
        try:
            from biblioteca.memoria.memoria_persistente import MemoriaPersistente
            mp = MemoriaPersistente.obtener()
            s = mp.sesiones_anteriores()
            t = mp.datos_sebastian and mp._datos.get('total_turnos', 0)
            if s:
                partes.append(f"Hemos tenido {s} conversaciones"
                              + (f", {t} turnos en total." if t else "."))
        except Exception:
            pass
        # Estadísticas del SQLite
        try:
            st = gestor.estadisticas()
            if st.get('conocimientos'):
                partes.append(f"Tengo {st['conocimientos']} conocimientos guardados.")
            if st.get('episodios'):
                partes.append(f"Recuerdo {st['episodios']} episodios.")
        except Exception:
            pass
        return ' '.join(partes)

    # ── SESION ────────────────────────────────────────────

    def _sesion(self, gestor) -> str:
        try:
            return gestor.contexto_para_groq(6) or ''
        except Exception:
            return ''
