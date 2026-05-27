# biblioteca/habilidades/memoria/sintetizador_episodios.py
# ============================================================
# SINTETIZADOR DE EPISODIOS — Bell recuerda entre sesiones
#
# Al cerrar sesión, Groq genera un resumen del episodio:
#   - Qué hizo Sebastian
#   - Cómo estaba emocionalmente
#   - Qué aprendió Bell
#   - Qué quedó pendiente
#
# Ese resumen se guarda en la tabla episodios del SQLite
# y en la MemoriaPersistente JSON.
# Al inicio de la siguiente sesión Bell lo tiene disponible.
# ============================================================

import json
import os
from datetime import datetime
from typing import Optional


_GROQ_URL   = 'https://api.groq.com/openai/v1/chat/completions'
_GROQ_MODEL = 'openai/gpt-oss-120b'


def sintetizar_y_guardar(intercambios: list, gestor) -> Optional[str]:
    """
    Genera un resumen del episodio y lo guarda en memoria.

    Args:
        intercambios: lista de dicts con 'user', 'bell', 'tipo', 'habilidad'
        gestor: instancia de GestorMemoria

    Returns:
        El resumen generado, o None si no fue posible.
    """
    if not intercambios or len(intercambios) < 2:
        return None

    # Episodio como CONOCIMIENTO estructurado (Groq devuelve JSON)
    estructura = _generar_estructura_groq(intercambios)

    if estructura:
        resumen_guardar = json.dumps(estructura, ensure_ascii=False)
        temas           = estructura.get('habilidades_usadas') or _extraer_temas(intercambios)
        habilidades     = estructura.get('habilidades_usadas') or list(
            {i.get('habilidad', '') for i in intercambios if i.get('habilidad')})
        aprendizajes    = estructura.get('aprendio_bell', '') or _detectar_aprendizajes(intercambios)
        resumen_legible = estructura.get('tema_principal', '') or 'Sesión registrada.'
    else:
        # Fallback narrativo (comportamiento anterior, no rompe)
        narrativa = _generar_resumen_groq(intercambios) or _generar_resumen_local(intercambios)
        if not narrativa:
            return None
        resumen_guardar = narrativa
        temas           = _extraer_temas(intercambios)
        habilidades     = list({i.get('habilidad', '') for i in intercambios if i.get('habilidad')})
        aprendizajes    = _detectar_aprendizajes(intercambios)
        resumen_legible = narrativa

    # Guardar en SQLite via gestor (resumen = JSON estructurado o narrativa)
    try:
        gestor.guardar_episodio(
            resumen=resumen_guardar,
            temas=temas,
            habilidades=habilidades,
            aprendizajes=aprendizajes,
        )
    except Exception as e:
        print(f'  [Sintetizador] ⚠ SQLite: {e}')

    # Guardar en MemoriaPersistente JSON (texto legible, no el JSON crudo)
    try:
        from biblioteca.memoria.memoria_persistente import MemoriaPersistente
        mp = MemoriaPersistente.obtener()
        mp.registrar_momento(
            mensaje_usuario=f'[Episodio {datetime.now().strftime("%d/%m")}]',
            respuesta_bell=resumen_legible,
            es_importante=True,
        )
        if temas:
            for tema in temas[:3]:
                mp.registrar_tema(tema)
        mp.guardar()
        print(f'  [Sintetizador] ✅ Episodio guardado ({"estructurado" if estructura else "narrativo"})')
    except Exception as e:
        print(f'  [Sintetizador] ⚠ JSON: {e}')

    return resumen_guardar


def _generar_estructura_groq(intercambios: list) -> Optional[dict]:
    """Groq devuelve el episodio como conocimiento estructurado (JSON)."""
    api_key = os.getenv('GROQ_API_KEY', '')
    if not api_key:
        return None

    lineas = []
    for ix in intercambios[-10:]:
        u = ix.get('user', '')[:80]
        b = ix.get('bell', '')[:80]
        if u:
            lineas.append(f'Sebastian: {u}')
        if b:
            lineas.append(f'Bell: {b}')
    transcripcion = '\n'.join(lineas)

    prompt = (
        f'<transcripcion_sesion>\n{transcripcion}\n</transcripcion_sesion>\n\n'
        'Devuelve SOLO este JSON, sin texto adicional:\n'
        '{"tema_principal":"string corto",'
        '"proyecto_activo":"nombre o null",'
        '"estado_proyecto":"en_progreso|resuelto|bloqueado|null",'
        '"que_paso":["hecho 1","hecho 2"],'
        '"pendientes":["pendiente 1"],'
        '"decisiones":["decision 1"],'
        '"emocion_sebastian":"enfocado|frustrado|contento|cansado|neutral",'
        '"aprendio_bell":"máximo 20 palabras",'
        '"habilidades_usadas":["Python","Lenguaje"]}'
    )

    try:
        import httpx
        r = httpx.post(
            _GROQ_URL,
            headers={'Authorization': f'Bearer {api_key}',
                     'Content-Type': 'application/json'},
            json={
                'model': _GROQ_MODEL,
                'messages': [
                    {'role': 'system',
                     'content': 'Resumes sesiones como JSON estructurado. Solo JSON válido.'},
                    {'role': 'user', 'content': prompt},
                ],
                'temperature': 0.2,
                'max_tokens': 400,
            },
            timeout=20,
        )
        if r.status_code != 200:
            return None
        cont = (r.json().get('choices', [{}])[0]
                .get('message', {}).get('content', '').strip())
        import re as _re
        m = _re.search(r'\{.*\}', cont, _re.DOTALL)
        if not m:
            return None
        data = json.loads(m.group(0))
        # Validación mínima: debe tener al menos tema_principal
        if isinstance(data, dict) and data.get('tema_principal'):
            return data
        return None
    except Exception:
        return None


def _generar_resumen_groq(intercambios: list) -> Optional[str]:
    """Usa Groq para generar un resumen inteligente del episodio."""
    api_key = os.getenv('GROQ_API_KEY', '')
    if not api_key:
        return None

    # Construir transcripción resumida
    lineas = []
    for ix in intercambios[-10:]:  # últimos 10 turnos
        u = ix.get('user', '')[:80]
        b = ix.get('bell', '')[:80]
        if u:
            lineas.append(f'Sebastian: {u}')
        if b:
            lineas.append(f'Bell: {b}')

    transcripcion = '\n'.join(lineas)

    prompt = (
        f'<transcripcion_sesion>\n{transcripcion}\n</transcripcion_sesion>\n\n'
        f'<instruccion>Genera un resumen de esta sesión en 3-4 oraciones. '
        f'Incluye: (1) qué hizo Sebastian, (2) cómo estaba emocionalmente, '
        f'(3) qué habilidades usó Bell, (4) si quedó algo pendiente. '
        f'Sé específico y concreto. No uses bullet points. '
        f'Escribe como si fuera una nota interna de Bell.</instruccion>'
    )

    try:
        import httpx
        r = httpx.post(
            _GROQ_URL,
            headers={'Authorization': f'Bearer {api_key}',
                     'Content-Type': 'application/json'},
            json={
                'model': _GROQ_MODEL,
                'messages': [
                    {'role': 'system',
                     'content': 'Eres Bell, una IA. Generates notas internas de sesión en español. '
                                'Sé concisa y específica.'},
                    {'role': 'user', 'content': prompt},
                ],
                'temperature': 0.3,
                'max_tokens': 300,
            },
            timeout=20,
        )
        if r.status_code == 200:
            return (r.json()
                    .get('choices', [{}])[0]
                    .get('message', {})
                    .get('content', '').strip())
    except Exception:
        pass
    return None


def _generar_resumen_local(intercambios: list) -> str:
    """Genera un resumen básico sin Groq cuando no hay API key."""
    n  = len(intercambios)
    habilidades = list({i.get('habilidad', '') for i in intercambios if i.get('habilidad')})
    temas = _extraer_temas(intercambios)

    partes = [f'Sesión de {n} intercambios el {datetime.now().strftime("%d/%m/%Y")}.']
    if habilidades:
        partes.append(f'Habilidades usadas: {", ".join(habilidades[:3])}.')
    if temas:
        partes.append(f'Temas: {", ".join(temas[:3])}.')

    return ' '.join(partes)


def _extraer_temas(intercambios: list) -> list:
    """Extrae los temas principales de la sesión."""
    _TEMAS = {
        'Python':    ['python', 'código', 'bug', 'función', 'error', 'clase'],
        'Bell':      ['bell', 'belladonna', 'habilidad', 'arquitectura', 'capa'],
        'Hospital':  ['hospital', 'twilio', 'paciente', 'llamada'],
        'trabajo':   ['trabajo', 'jelcon', 'cliente', 'proyecto', 'reunión'],
        'personal':  ['cansado', 'bien', 'mal', 'gracias', 'siento'],
    }
    temas_count = {}
    for ix in intercambios:
        texto = (ix.get('user', '') + ' ' + ix.get('bell', '')).lower()
        for tema, palabras in _TEMAS.items():
            if any(p in texto for p in palabras):
                temas_count[tema] = temas_count.get(tema, 0) + 1

    return [t for t, _ in sorted(temas_count.items(), key=lambda x: -x[1])][:4]


def _detectar_aprendizajes(intercambios: list) -> str:
    """Detecta qué aprendió Bell en esta sesión."""
    nuevos = []
    for ix in intercambios:
        texto = ix.get('user', '').lower()
        if any(p in texto for p in ['terminé', 'funciona', 'logré', 'por fin']):
            nuevos.append(ix.get('user', '')[:60])
    if nuevos:
        return 'Logros: ' + '; '.join(nuevos[:2])
    return ''