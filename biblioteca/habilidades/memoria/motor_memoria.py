# biblioteca/habilidades/memoria/motor_memoria.py
# ============================================================
# MOTOR MEMORIA — Bell recuerda y responde
#
# Mente Pura: SQLite recopila datos exactos.
# Groq genera lenguaje Bell con esos datos.
#
# Preguntas que responde:
#   "qué recuerdas de mí"
#   "hablamos de Python antes?"
#   "qué me dijiste sobre motor_python.py"
#   "cuántas conversaciones tenemos"
#   "qué sabes de ti misma"
# ============================================================

import re
import os
from typing import Optional

_GROQ_URL   = 'https://api.groq.com/openai/v1/chat/completions'
_GROQ_MODEL = 'openai/gpt-oss-120b'

_SYSTEM_MEMORIA = """Eres Bell — IA de Juan Sebastian Mora.
Recibes datos EXACTOS de tu propia memoria SQLite.
Responde en primera persona, voz directa, máximo 3 oraciones.
NUNCA inventas datos que no están en los datos recibidos."""


def procesar(texto: str) -> dict:
    """Punto de entrada principal de la habilidad Memoria."""
    try:
        from biblioteca.habilidades.memoria import obtener_memoria
        mem = obtener_memoria()

        tipo = _detectar_tipo(texto)
        datos = _recopilar_datos(mem, tipo, texto)
        respuesta = _generar_respuesta(datos, texto, tipo)

        return {
            'exitoso':   True,
            'respuesta': respuesta,
            'tipo':      tipo,
        }
    except Exception as e:
        return {
            'exitoso':   False,
            'respuesta': f"No pude acceder a mi memoria: {e}",
            'tipo':      'error',
        }


def _detectar_tipo(texto: str) -> str:
    t = texto.lower()

    if any(k in t for k in ['qué sabes de mí', 'que sabes de mi', 'quién soy',
                              'quien soy', 'qué recuerdas de mí', 'que recuerdas de mi',
                              'mi perfil', 'qué sé de ti', 'que se de ti']):
        return 'perfil_sebastian'

    if any(k in t for k in ['hablamos de', 'dijiste sobre', 'recuerdas cuando',
                              'qué me dijiste', 'que me dijiste', 'busca en',
                              'busca cuando', 'búscame', 'buscame']):
        return 'buscar'

    if any(k in t for k in ['cuántas conversaciones', 'cuantas conversaciones',
                              'cuánto llevamos', 'cuanto llevamos',
                              'cuántos turnos', 'estadísticas', 'estadisticas',
                              'cuánto sabes', 'cuanto sabes']):
        return 'estadisticas'

    if any(k in t for k in ['qué sabes de ti', 'que sabes de ti',
                              'cómo eres', 'como eres', 'qué eres',
                              'tu identidad', 'quién eres', 'quien eres']):
        return 'bell_self'

    if any(k in t for k in ['archivos que has analizado', 'archivos analizados',
                              'qué archivos conoces', 'que archivos conoces']):
        return 'archivos_analizados'

    return 'buscar'  # default: buscar en sesión


def _recopilar_datos(mem, tipo: str, texto: str) -> str:
    """Recopila datos exactos de SQLite según el tipo de pregunta."""

    if tipo == 'perfil_sebastian':
        perfil = mem.obtener_perfil_sebastian()
        sesion = mem.obtener_contexto_sesion()
        if isinstance(sesion, list) and sesion:
            sesion_txt = '\n'.join(
                f"{'S' if m.get('rol','')=='user' else 'B'}: {m.get('mensaje','')[:80]}"
                for m in sesion[-4:]
            )
        elif isinstance(sesion, str):
            sesion_txt = sesion[:300]
        else:
            sesion_txt = 'Sin mensajes aún'
        return f"PERFIL:\n{perfil}\n\nSESIÓN ACTUAL:\n{sesion_txt}"

    if tipo == 'buscar':
        # Extraer término de búsqueda
        termino = _extraer_termino(texto)
        resultado = mem.buscar_semantico(termino) if termino else None
        sesion = mem.obtener_contexto_sesion()
        sesion_txt = ''
        if isinstance(sesion, list) and sesion:
            sesion_txt = '\n'.join(
                f"{'S' if m.get('rol','')=='user' else 'B'}: {m.get('mensaje','')[:80]}"
                for m in sesion[-6:]
            )
        elif isinstance(sesion, str):
            sesion_txt = sesion[:400]
        base = f"BÚSQUEDA '{termino}':\n{resultado or 'Sin resultados'}"
        if sesion_txt:
            base += f"\n\nSESIÓN ACTUAL:\n{sesion_txt}"
        return base

    if tipo == 'estadisticas':
        stats  = mem.estadisticas()
        sesion = mem.obtener_contexto_sesion()
        # obtener_contexto_sesion puede devolver lista o string
        if isinstance(sesion, list):
            n_msgs = len(sesion)
        else:
            n_msgs = len([l for l in (sesion or '').split('\n') if l.strip()])
        return (
            f"ESTADÍSTICAS:\n"
            f"- Mensajes en sesión actual: {n_msgs}\n"
            f"- Conocimientos guardados: {stats.get('conocimientos', 0)}\n"
            f"- Búsquedas web almacenadas: {stats.get('busquedas', 0)}\n"
            f"- Archivos Bell analizados: {stats.get('archivos_bell', 0)}\n"
            f"- Código Python guardado: {stats.get('codigo_guardado', 0)}\n"
            f"- Episodios registrados: {stats.get('episodios', 0)}\n"
            f"- Items del perfil de Sebastian: {stats.get('perfil_items', 0)}"
        )

    if tipo == 'bell_self':
        perfil = mem.obtener_bell_self()
        if isinstance(perfil, dict):
            lineas = []
            for k, v in perfil.items():
                val = v.get('valor', str(v)) if isinstance(v, dict) else str(v)
                if val:
                    lineas.append(f"- {k}: {val}")
            return "LO QUE SÉ DE MÍ:\n" + '\n'.join(lineas)
        return f"LO QUE SÉ DE MÍ:\n{perfil}"

    if tipo == 'archivos_analizados':
        try:
            from biblioteca.habilidades.memoria.db import conexion
            conn = conexion()
            cur  = conn.cursor()
            # Solo archivos de Bell: rutas que contengan capas/ o biblioteca/
            cur.execute(
                "SELECT nombre, ruta, cc_max, mi_score FROM archivos_bell "
                "WHERE mi_score IS NOT NULL "
                "AND (ruta LIKE '%capas%' OR ruta LIKE '%biblioteca%' "
                "     OR ruta LIKE '%interfaz%') "
                "ORDER BY mi_score ASC LIMIT 8"
            )
            rows = cur.fetchall()
            if rows:
                lineas = [f"- {r[0]}: CC={r[2]}, MI={r[3]}" for r in rows]
                return "ARCHIVOS ANALIZADOS (peor MI primero):\n" + '\n'.join(lineas)
        except Exception:
            pass
        return "No tengo archivos Bell analizados registrados aún."

    return mem.obtener_contexto_sesion() or "Sin datos disponibles"


def _generar_respuesta(datos: str, pregunta: str, tipo: str) -> str:
    """Groq recibe datos reales y genera lenguaje Bell."""
    # Intentar Groq
    api_key = os.getenv('GROQ_API_KEY', '')
    if api_key:
        groq_resp = _llamar_groq(datos, pregunta, api_key)
        if groq_resp:
            print(f"  [Memoria] Groq fusion OK | {len(groq_resp)} chars")
            return groq_resp

    # Fallback: template directo con los datos
    return _template_fallback(datos, tipo)


def _llamar_groq(datos: str, pregunta: str, api_key: str) -> str:
    try:
        import httpx
        prompt = (
            f"<datos_memoria>\n{datos[:1500]}\n</datos_memoria>\n\n"
            f"<pregunta>{pregunta}</pregunta>\n\n"
            f"<instruccion>Responde usando SOLO los datos de memoria dados. "
            f"Voz Bell, 2-3 oraciones máximo.</instruccion>"
        )
        r = httpx.post(
            _GROQ_URL,
            headers={'Authorization': f'Bearer {api_key}',
                     'Content-Type': 'application/json'},
            json={
                'model':       _GROQ_MODEL,
                'messages':    [
                    {'role': 'system', 'content': _SYSTEM_MEMORIA},
                    {'role': 'user',   'content': prompt},
                ],
                'temperature': 0.2,
                'max_tokens':  350,
            },
            timeout=12,
        )
        if r.status_code == 200:
            resp = (r.json().get('choices', [{}])[0]
                    .get('message', {}).get('content', '').strip())
            return resp if len(resp) > 15 else ''
    except Exception as e:
        print(f"  [Memoria] Groq error: {e}")
    return ''


def _template_fallback(datos: str, tipo: str) -> str:
    if 'PERFIL' in datos:
        lineas = [l for l in datos.split('\n') if l.startswith('- ') or '=' in l]
        return 'Lo que sé de Sebastian: ' + ' | '.join(lineas[:4]) + '.'
    if 'ESTADÍSTICAS' in datos:
        return datos.replace('ESTADÍSTICAS:\n', '').replace('- ', '').replace('\n', '. ')
    if 'BÚSQUEDA' in datos and 'Sin resultados' in datos:
        termino = re.search(r"BÚSQUEDA '(.+?)'", datos)
        t = termino.group(1) if termino else 'eso'
        return f"No encontré conversaciones previas sobre '{t}' en mi memoria."
    return datos[:300]


def _extraer_termino(texto: str) -> str:
    t = texto.lower()
    for patron in [
        r'hablamos de (.+)', r'dijiste sobre (.+)', r'recuerdas (.+)',
        r'búscame (.+)', r'buscame (.+)', r'busca (.+)',
        r'qué me dijiste (?:sobre|de) (.+)', r'que me dijiste (?:sobre|de) (.+)',
    ]:
        m = re.search(patron, t)
        if m:
            termino = m.group(1).strip()
            termino = re.sub(r'\?$|antes\??$', '', termino).strip()
            return termino[:50]
    # Fallback: palabras clave del texto
    palabras = [w for w in texto.split() if len(w) > 3]
    return ' '.join(palabras[:3]) if palabras else texto[:30]