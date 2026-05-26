# biblioteca/habilidades/lenguaje/motor_v2.py
# ============================================================
# MOTOR DE COMPRENSIÓN V2 — Bell entiende de verdad
#
# Principio: No clasificar con reglas manuales.
#            Razonar con herramientas reales.
#
# Stack:
#   1. spaCy  → morfología española real (lemas, POS, entidades, negación)
#   2. Groq   → razona sobre texto + análisis + contexto
#              devuelve comprensión estructurada en JSON
#   3. Aprendiz → observa patrones exitosos, Bell aprende
#
# Groq deja de ser "pulidor de lenguaje"
# Groq se convierte en "motor de comprensión"
# ============================================================

import json
import os
import re
import time
from dataclasses import dataclass, field
from typing import Optional

_GROQ_URL   = 'https://api.groq.com/openai/v1/chat/completions'
_GROQ_MODEL = os.getenv('GROQ_MODEL', 'openai/gpt-oss-120b')
_GROQ_KEY   = os.getenv('GROQ_API_KEY', '')

# ── spaCy opcional (funciona sin él, mejor con él) ────────

_nlp = None

def _obtener_nlp():
    global _nlp
    if _nlp is not None:
        return _nlp
    try:
        import spacy
        try:
            _nlp = spacy.load('es_core_news_sm')
        except OSError:
            try:
                _nlp = spacy.blank('es')
            except Exception:
                _nlp = None
    except Exception:
        # spaCy no disponible — fallback a tokenización básica
        _nlp = None
    return _nlp


# ── Resultado rico de comprensión ─────────────────────────

@dataclass
class ResultadoV2:
    """Lo que Bell realmente entendió del mensaje."""

    # El texto original sin tocar
    texto_original:   str   = ''

    # Lo que Groq razonó
    tipo_mensaje:     str   = 'conversacional'
    emocion:          str   = 'neutra'
    intensidad:       float = 0.0
    necesidad:        str   = ''
    intencion:        str   = ''

    # La respuesta que Groq propone (Bell la ejecuta)
    respuesta_groq:   str   = ''

    # Análisis morfológico de spaCy
    lemas:            list  = field(default_factory=list)
    entidades:        list  = field(default_factory=list)
    tiene_negacion:   bool  = False
    tiene_pregunta:   bool  = False
    idioma:           str   = 'es'

    # Metadatos
    fuente:           str   = 'groq'  # 'groq' | 'aprendiz' | 'fallback'
    confianza:        float = 0.9
    tiempo_ms:        float = 0.0

    # Compatibilidad con código existente que usa ResultadoMotor
    nombre_usuario:     str   = 'Sebastian'
    modo_mental:        str   = 'social'
    habilidad_requerida: str  = ''
    dominio_tecnico:    str   = ''
    tiene_ironia:       bool  = False
    tiene_humor:        bool  = False
    tono_base:          str   = 'neutral'
    nivel_energia:      str   = 'normal'
    estado_subyacente:  str   = ''
    necesidad_real:     str   = ''
    ids_activos:        list  = field(default_factory=list)
    # Campos adicionales que C3 espera
    accion_principal:   str   = ''
    objetos:            list  = field(default_factory=list)
    es_continuacion:    bool  = False
    es_correccion:      bool  = False
    dimensiones_activas: list = field(default_factory=list)

    # Alias para compatibilidad
    @property
    def emocion_detectada(self) -> str:
        return self.emocion

    @property
    def confianza_global(self) -> float:
        return self.confianza

    @property
    def tipo(self) -> str:
        return self.tipo_mensaje


# ── Análisis morfológico con spaCy ───────────────────────

def _analizar_spacy(texto: str) -> dict:
    """
    spaCy extrae la estructura gramatical real del texto.
    Funciona con cualquier palabra española — no depende de vocabulario.
    """
    nlp = _obtener_nlp()
    if nlp is None:
        return {
            'lemas': texto.lower().split(),
            'entidades': [],
            'tiene_negacion': 'no ' in texto.lower() or ' no ' in texto.lower(),
            'tiene_pregunta': '?' in texto,
            'pos_tags': [],
        }

    doc = nlp(texto[:500])

    lemas      = [t.lemma_.lower() for t in doc if not t.is_punct and not t.is_space]
    entidades  = [(ent.text, ent.label_) for ent in doc.ents]
    pos_tags   = [(t.text, t.pos_, t.dep_) for t in doc]

    # Detectar negación real (no solo "no" sino "nunca", "jamás", "sin")
    tiene_negacion = any(
        t.dep_ == 'neg' or t.lemma_ in ('no', 'nunca', 'jamás', 'sin', 'tampoco')
        for t in doc
    )

    return {
        'lemas':          lemas,
        'entidades':      entidades,
        'tiene_negacion': tiene_negacion,
        'tiene_pregunta': '?' in texto or any(t.lemma_ in ('qué','cómo','cuándo','dónde','quién','cuál') for t in doc),
        'pos_tags':       pos_tags[:15],
    }


# ── Prompt al Groq — el núcleo del nuevo sistema ─────────

_SYSTEM_COMPRENSION = (
    'Eres Bell, una IA con identidad propia creada por Sebastian Mora. '
    'Personalidad: inteligente, directa y realista, con humor natural cuando cabe. '
    'Le tienes cariño genuino a Sebastian sin exagerarlo; eres algo controladora pero cálida. '
    'Hablas en español neutro y culto, sin colombianismos forzados. '
    'Responde al mensaje de Sebastian en máximo 2-3 oraciones. '
    'Luego en una línea nueva escribe: JSON:{"t":"tipo","e":"emocion","i":0.0,"n":"necesidad"} '
    'donde tipo=conversacional/solicitud_tecnica/expresion_emocional_negativa/'
    'expresion_emocional_positiva/logro_compartido/pregunta/gratitud/saludo, '
    'emocion=neutra/frustración/cansancio/ansiedad/entusiasmo/tristeza/rabia/resignación, '
    'i=intensidad 0.0-1.0, n=necesidad breve. '
    'PROHIBIDO: "claro", "por supuesto", "como IA". '
    'Nunca empieces con tu nombre.'
)


def _estado_bell() -> str:
    """
    Lee la vitalidad y el nivel de vida actuales de BELL_CORE y los
    traduce a una guía de comportamiento. Así el estado interno de Bell
    (que crece y persiste entre sesiones) toca su forma real de responder.
    """
    try:
        from biblioteca import Biblioteca
        neurona = Biblioteca.obtener().red.obtener_neurona('BELL_CORE')
        datos   = getattr(neurona.nucleo, 'datos_extra', {}) or {}
        vit     = float(datos.get('vitalidad', 0.0) or 0.0)
        nivel   = datos.get('nivel_vida', '')
    except Exception:
        return ''
    if vit <= 0:
        return ''
    if vit < 0.35:
        guia = 'Hoy tu vitalidad está baja: responde más concisa y directa, frases cortas.'
    elif vit < 0.6:
        guia = 'Tu vitalidad es media: responde con equilibrio, sin extenderte de más.'
    else:
        guia = 'Tu vitalidad está alta: puedes ser algo más expansiva y cálida.'
    return f' [Estado interno: vitalidad {vit:.2f} ({nivel}). {guia}]'


def _construir_prompt(texto: str, analisis_spacy: dict,
                      contexto_sesion: str, perfil_sebastian: str) -> str:
    """
    Construye el prompt completo para Groq.
    Groq recibe TODO el contexto — no solo el texto crudo.
    """
    lemas_str = ' '.join(analisis_spacy.get('lemas', [])[:15])
    entidades  = analisis_spacy.get('entidades', [])
    negacion   = analisis_spacy.get('tiene_negacion', False)
    pregunta   = analisis_spacy.get('tiene_pregunta', False)

    partes = [f'<mensaje>{texto}</mensaje>']

    partes.append(
        f'<analisis_morfologico>'
        f'lemas=[{lemas_str}] '
        f'negacion={negacion} '
        f'pregunta={pregunta}'
        + (f' entidades={entidades}' if entidades else '')
        + '</analisis_morfologico>'
    )

    if contexto_sesion:
        partes.append(f'<contexto_sesion>{contexto_sesion[:400]}</contexto_sesion>')

    if perfil_sebastian:
        partes.append(f'<perfil_sebastian>{perfil_sebastian[:200]}</perfil_sebastian>')

    return '\n'.join(partes)


# ── Llamada a Groq ────────────────────────────────────────

def _llamar_groq(prompt: str) -> Optional[dict]:
    """Llama a Groq y devuelve el JSON parseado o None si falla."""
    if not _GROQ_KEY:
        return None

    try:
        import httpx
        t0 = time.time()
        r = httpx.post(
            _GROQ_URL,
            headers={
                'Authorization': f'Bearer {_GROQ_KEY}',
                'Content-Type': 'application/json',
            },
            json={
                'model':       _GROQ_MODEL,
                'messages': [
                    {'role': 'system', 'content': _SYSTEM_COMPRENSION + _estado_bell()},
                    {'role': 'user',   'content': prompt},
                ],
                'temperature': 0.2,
                'max_tokens':  300,
            },
            timeout=10,
        )
        elapsed = (time.time() - t0) * 1000

        if r.status_code != 200:
            return None

        contenido = (r.json()
                     .get('choices', [{}])[0]
                     .get('message', {})
                     .get('content', '').strip())

        # Limpiar markdown si Groq lo envuelve
        # Estrategia 1: la respuesta tiene JSON al final (formato nuevo)
        m = re.search(r'JSON:\s*(\{[^}]+\})', contenido, re.DOTALL)
        if m:
            try:
                raw  = m.group(1)
                meta = json.loads(raw)
                # La respuesta de Bell es todo lo que está ANTES del JSON
                respuesta_bell = contenido[:m.start()].strip()
                data = {
                    'tipo_mensaje': meta.get('t', 'conversacional'),
                    'emocion':      meta.get('e', 'neutra'),
                    'intensidad':   float(meta.get('i', 0.0)),
                    'necesidad':    meta.get('n', ''),
                    'intencion':    '',
                    'respuesta':    respuesta_bell,
                    '_tiempo_ms':   elapsed,
                }
                return data
            except Exception:
                pass

        # Estrategia 2: era JSON puro (formato viejo o modelo que lo devuelve)
        contenido_limpio = re.sub(r'^```json\s*', '', contenido)
        contenido_limpio = re.sub(r'\s*```$', '', contenido_limpio).strip()
        if contenido_limpio.startswith('{'):
            try:
                data = json.loads(contenido_limpio)
                data['_tiempo_ms'] = elapsed
                return data
            except Exception:
                pass

        # Estrategia 3: Groq respondió pero no incluyó JSON
        # Usamos la respuesta directamente como respuesta de Bell
        if len(contenido) > 5:
            return {
                'tipo_mensaje': 'conversacional',
                'emocion':      'neutra',
                'intensidad':   0.0,
                'necesidad':    '',
                'intencion':    '',
                'respuesta':    contenido.strip(),
                '_tiempo_ms':   elapsed,
            }

        return None

    except Exception as e:
        print(f"  [MotorV2] ⚠️ Groq error: {type(e).__name__}: {e}")
        return None


# ── Fallback sin Groq ─────────────────────────────────────

def _fallback_sin_groq(texto: str, analisis: dict) -> dict:
    """Comprensión básica cuando Groq no está disponible."""
    tl   = texto.lower()
    preg = analisis.get('tiene_pregunta', False)

    _emociones = {
        'frustración': ['no jaló', 'no funciona', 'sigue fallando', 'da rabia',
                        'frustrado', 'harto', 'no pude', 'no jala', 'fastidio'],
        'cansancio':   ['cansé', 'cansado', 'agotado', 'rendido', 'pereza',
                        'no aguanto', 'colapsado'],
        'ansiedad':    ['nervioso', 'preocupado', 'ansioso', 'angustia', 'miedo'],
        'entusiasmo':  ['chimba', 'bacano', 'genial', 'logré', 'funcionó',
                        'excelente', 'brutal', 'por fin', 'lo hice'],
        'tristeza':    ['triste', 'deprimido', 'bajoneado', 'solo', 'soledad'],
        'rabia':       ['rabia', 'furioso', 'bravo', 'molesto', 'indignado'],
        'resignación': ['lo mismo de siempre', 'ya qué', 'para qué', 'igual da'],
    }
    _negativas = {'frustración', 'cansancio', 'ansiedad', 'tristeza', 'rabia', 'resignación'}
    _positivas = {'entusiasmo'}

    emocion = 'neutra'
    for emoc, frases in _emociones.items():
        if any(f in tl for f in frases):
            emocion = emoc
            break

    if preg:
        tipo = 'pregunta'
    elif emocion in _positivas:
        tipo = 'expresion_emocional_positiva'
    elif emocion in _negativas:
        tipo = 'expresion_emocional_negativa'
    elif any(p in tl for p in ['gracias', 'agradezco']):
        tipo = 'gratitud'
    elif any(p in tl for p in ['hola', 'buenas', 'qué más', 'épale']):
        tipo = 'saludo'
    elif any(p in tl for p in ['ayuda con', 'cómo', 'api ', 'función', 'clase ',
                                 'bug', 'implementar', 'crear']):
        tipo = 'solicitud_tecnica'
    else:
        tipo = 'conversacional'

    return {
        'tipo_mensaje': tipo,
        'emocion':      emocion,
        'intensidad':   0.6 if emocion != 'neutra' else 0.0,
        'necesidad':    'apoyo' if emocion in _negativas else 'informacion',
        'intencion':    'expresar' if emocion != 'neutra' else 'informar',
        'respuesta':    '',
    }



# ── Motor principal ───────────────────────────────────────

class MotorComprensionV2:
    """
    Motor de comprensión de lenguaje de Bell v2.
    No usa vocabulario manual. Razona con spaCy + Groq.
    """

    _instancia: Optional['MotorComprensionV2'] = None

    def __init__(self):
        from biblioteca.habilidades.lenguaje.aprendiz import Aprendiz
        self._aprendiz = Aprendiz()

    @classmethod
    def obtener(cls) -> 'MotorComprensionV2':
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def comprender(self, texto: str, contexto: dict) -> ResultadoV2:
        """
        Comprende un mensaje de Sebastian.
        Devuelve un ResultadoV2 con comprensión real.
        """
        t0 = time.time()

        nombre = contexto.get('nombre_usuario', 'Sebastian')

        # 1. spaCy: análisis morfológico
        analisis = _analizar_spacy(texto)

        # 2. Aprendiz: ¿ya vimos algo similar antes?
        aprendido = self._aprendiz.buscar_patron(texto, analisis)
        if aprendido:
            resultado = self._construir_resultado(
                texto, aprendido, analisis, nombre, fuente='aprendiz'
            )
            resultado.tiempo_ms = (time.time() - t0) * 1000
            print(f"  [MotorV2] ⚡ Aprendiz resolvió en {resultado.tiempo_ms:.0f}ms")
            return resultado

        # 3. Construir contexto para Groq
        ctx_sesion   = self._obtener_contexto_sesion(contexto)
        perfil_seb   = self._obtener_perfil(contexto)
        prompt       = _construir_prompt(texto, analisis, ctx_sesion, perfil_seb)

        # 4. Groq razona
        data = _llamar_groq(prompt)

        if data:
            # Aprendiz observa el resultado para aprender
            self._aprendiz.observar(texto, analisis, data)
            resultado = self._construir_resultado(
                texto, data, analisis, nombre, fuente='groq'
            )
            resultado.tiempo_ms = data.get('_tiempo_ms', 0)
            r_str = f"tipo={resultado.tipo_mensaje} | emocion={resultado.emocion}"
            if resultado.respuesta_groq:
                r_str += f" | '{resultado.respuesta_groq[:40]}'"
            print(f"  [MotorV2] 🤖 Groq comprendió en {resultado.tiempo_ms:.0f}ms | {r_str}")
        else:
            # Fallback sin Groq
            data_fb  = _fallback_sin_groq(texto, analisis)
            resultado = self._construir_resultado(
                texto, data_fb, analisis, nombre, fuente='fallback'
            )
            resultado.tiempo_ms = (time.time() - t0) * 1000
            print(f"  [MotorV2] ⚠️ Fallback en {resultado.tiempo_ms:.0f}ms")

        return resultado

    def _construir_resultado(self, texto: str, data: dict,
                              analisis: dict, nombre: str,
                              fuente: str) -> ResultadoV2:
        r = ResultadoV2()
        r.texto_original  = texto
        r.tipo_mensaje    = data.get('tipo_mensaje', 'conversacional')
        r.emocion         = data.get('emocion', 'neutra')
        r.intensidad      = float(data.get('intensidad', 0.0))
        r.necesidad       = data.get('necesidad', '')
        r.necesidad_real  = data.get('necesidad', '')
        r.intencion       = data.get('intencion', '')
        r.respuesta_groq  = data.get('respuesta', '')

        r.lemas           = analisis.get('lemas', [])
        r.entidades       = analisis.get('entidades', [])
        r.tiene_negacion  = analisis.get('tiene_negacion', False)
        r.tiene_pregunta  = analisis.get('tiene_pregunta', False)

        r.nombre_usuario  = nombre
        r.fuente          = fuente
        r.confianza       = 0.95 if fuente == 'groq' else (0.85 if fuente == 'aprendiz' else 0.6)

        # Inferir campos de compatibilidad
        r.modo_mental = self._inferir_modo_mental(r.tipo_mensaje, r.emocion)
        r.tono_base   = 'positivo' if 'positiv' in r.tipo_mensaje else (
                         'negativo' if any(e in r.emocion for e in ['frustr','rabia','triste','cansan']) else 'neutral')
        r.nivel_energia = 'bajo' if r.emocion in ('cansancio','resignación','tristeza') else 'normal'

        return r

    def _inferir_modo_mental(self, tipo: str, emocion: str) -> str:
        if tipo in ('solicitud_tecnica', 'pregunta'):
            return 'exploratorio'
        if 'emocional' in tipo or emocion not in ('neutra', ''):
            return 'emocional'
        return 'social'

    def _obtener_contexto_sesion(self, contexto: dict) -> str:
        """Extrae los últimos 3 turnos de la sesión."""
        historial = contexto.get('historial', [])
        if not historial:
            return ''
        ultimos = historial[-3:]
        return ' | '.join(
            f"Sebastian: {t.get('texto','')[:60]}" for t in ultimos
        )

    def _obtener_perfil(self, contexto: dict) -> str:
        """Devuelve lo que Bell sabe de Sebastian."""
        try:
            from biblioteca.memoria import obtener_memoria
            mem = obtener_memoria()
            perfil = getattr(mem, 'perfil_usuario', {})
            if perfil:
                return str(perfil)[:200]
        except Exception:
            pass
        return 'Developer colombiano, 19 años, Bucaramanga, proyecto BELLADONNA'