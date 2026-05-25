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

    resumen = _generar_resumen_groq(intercambios)
    if not resumen:
        resumen = _generar_resumen_local(intercambios)

    if not resumen:
        return None

    # Extraer temas del intercambio
    temas = _extraer_temas(intercambios)

    # Habilidades usadas
    habilidades = list({i.get('habilidad', '') for i in intercambios
                        if i.get('habilidad')})

    # Aprendizajes — qué cosas nuevas aparecieron
    aprendizajes = _detectar_aprendizajes(intercambios)

    # Guardar en SQLite via gestor
    try:
        gestor.guardar_episodio(
            resumen=resumen,
            temas=temas,
            habilidades=habilidades,
            aprendizajes=aprendizajes,
        )
    except Exception as e:
        print(f'  [Sintetizador] ⚠ SQLite: {e}')

    # Guardar en MemoriaPersistente JSON
    try:
        from biblioteca.memoria.memoria_persistente import MemoriaPersistente
        mp = MemoriaPersistente.obtener()
        mp.registrar_momento(
            mensaje_usuario=f'[Episodio {datetime.now().strftime("%d/%m")}]',
            respuesta_bell=resumen,
            es_importante=True,
        )
        if temas:
            for tema in temas[:3]:
                mp.registrar_tema(tema)
        mp.guardar()
        print(f'  [Sintetizador] ✅ Episodio guardado — {len(resumen)} chars')
    except Exception as e:
        print(f'  [Sintetizador] ⚠ JSON: {e}')

    return resumen


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