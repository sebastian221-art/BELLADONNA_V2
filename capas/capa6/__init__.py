# capas/capa6/__init__.py
# ================================================
# CAPA 6 — DECISIÓN Y EXPRESIÓN — v3
#
# ARQUITECTURA TRI-HÍBRIDA:
#   matematica_python → base_python directo (0s)
#   tecnica_groq      → Groq gpt-oss-120b  (0.5s)
#   conversacional    → Motor Bell local    (5-9s)
#   emocional         → Motor Bell local    (5-9s)
#   informativa       → Motor Bell local    (5-9s)
#
# MENTE PURA:
#   Python decide (constructor_decision.py)
#   Motor pule el lenguaje (nunca inventa)
#   Verificador filtra respuestas malas
# ================================================

import os
from capas.capa6.paquete_capa6        import PaqueteCapa6, DecisionFinal
from capas.capa6.constructor_decision  import ConstructorDecision
from capas.capa6.constructor_prompt    import ConstructorPrompt
from capas.capa6.generador_groq        import GeneradorMotorLocal, GeneradorGroqCloud
from capas.capa6.verificador_respuesta import VerificadorRespuesta
from capas.capa6.buffer_sesion         import BufferSesion

_DEBUG = os.getenv('BELL_DEBUG', '0') == '1'

_decision      = ConstructorDecision()
_prompt        = ConstructorPrompt()
_motor_local   = GeneradorMotorLocal()
_groq_cloud    = GeneradorGroqCloud()
_verificador   = VerificadorRespuesta()

_SEÑALES_ROBOTICO = [
    'mis sistemas', 'estoy procesando', 'de manera efectiva',
    'dentro de mis posibilidades', 'funcionando correctamente',
    'debo informarte', 'como ia', 'como asistente',
    'según mi análisis', 'he procesado', 'como modelo de lenguaje',
    'como sistema de inteligencia', 'me encuentro en un estado',
    'considerando todas las variables', 'espero tu próximo paso',
    'me alegra que hayas iniciado', 'tu saludo me encontró',
    'la aprobación de todas las consejeras',
    'me parece que sebastian', 'puedo ofrecerte apoyo',
    'juntos podemos encontrar', 'su cansancio y frustración son palpables',
    'recibí tu mensaje, sebastian. la expresión',
    'procesando todo lo que me rodea', 'me da la sensación',
    'groq no respondió bien', 'el procesamiento funcionó',
]


def procesar(paquete_capa5: dict) -> dict:
    try:
        return _procesar_interno(paquete_capa5)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return PaqueteCapa6(
            decision         = DecisionFinal(),
            respuesta_final  = 'Aquí estoy. Algo falló — intenta de nuevo.',
            fuente_respuesta = 'error',
            paquete_capa5    = paquete_capa5,
            exitoso          = False,
            error            = str(e),
        ).a_dict()


def _procesar_interno(paquete_capa5: dict) -> dict:

    # ── Veto de C5 → respuesta directa ────────────────────
    if paquete_capa5.get('veto'):
        respuesta_veto = paquete_capa5.get('respuesta_directa', '')
        _guardar_en_buffer(paquete_capa5, respuesta_veto)
        return PaqueteCapa6(
            decision         = DecisionFinal(tipo='veto_respuesta'),
            respuesta_final  = respuesta_veto,
            fuente_respuesta = 'veto_capa5',
            paquete_capa5    = paquete_capa5,
        ).a_dict()

    # ── Extraer datos del pipeline ─────────────────────────
    paquete_c4     = paquete_capa5.get('paquete_capa4', {})
    paquete_c3     = paquete_c4.get('paquete_capa3', {})
    paquete_c2     = paquete_c3.get('paquete_capa2', {})
    paquete_c1     = paquete_c2.get('paquete_capa1', {})
    comprension    = paquete_c3.get('comprension', {})
    instruccion    = paquete_capa5.get('instruccion', {})
    texto_original = paquete_c1.get('contenido_original', '')
    nombre         = comprension.get('contextual', {}).get('nombre_usuario', 'Sebastian')

    # ── Campos v2 propagados ──────────────────────────────
    tipo_respuesta  = instruccion.get('tipo_respuesta', 'conversacional')
    motor_sugerido  = paquete_capa5.get('motor_sugerido', 'local')
    contiene_codigo = paquete_capa5.get('contiene_codigo', False)
    modo_mental     = paquete_capa5.get('modo_mental', 'social')

    # ── 1. Python construye respuesta_base ────────────────
    decision       = _decision.construir(paquete_capa5)
    respuesta_base = decision.respuesta_base or 'Aquí estoy.'

    # ── 2. ROUTING TRI-HÍBRIDO ────────────────────────────
    respuesta_final, fuente_final = _routing_trihibrido(
        tipo_respuesta  = tipo_respuesta,
        respuesta_base  = respuesta_base,
        texto_original  = texto_original,
        decision        = decision,
        comprension     = comprension,
        paquete_capa5   = paquete_capa5,
        motor_sugerido  = motor_sugerido,
        contiene_codigo = contiene_codigo,
        nombre          = nombre,
    )

    # ── 3. Logs diagnósticos ──────────────────────────────
    if _DEBUG:
        print(f'  C6 groq_raw:    "{respuesta_final[:100]}" | fuente: {fuente_final}')

    print(f'  C6 respuesta_base:  "{respuesta_base[:80]}"')
    print(f'  C6 fuente:          {fuente_final}')
    print(f'  C6 respuesta_final: "{respuesta_final[:100]}"')

    # ── 4. Guardar en buffer/memoria ──────────────────────
    if texto_original and respuesta_final:
        BufferSesion.obtener().agregar_turno(
            texto_original, respuesta_final, comprension
        )

    return PaqueteCapa6(
        decision         = decision,
        respuesta_final  = respuesta_final,
        fuente_respuesta = fuente_final,
        prompt_usado     = texto_original,
        paquete_capa5    = paquete_capa5,
        # propagación v2
        motor_sugerido   = motor_sugerido,
        contiene_codigo  = contiene_codigo,
        tipo_respuesta   = tipo_respuesta,
        modo_mental      = modo_mental,
    ).a_dict()


# ══════════════════════════════════════════════════════════
# ROUTING TRI-HÍBRIDO
# ══════════════════════════════════════════════════════════

def _routing_trihibrido(
    tipo_respuesta:  str,
    respuesta_base:  str,
    texto_original:  str,
    decision:        DecisionFinal,
    comprension:     dict,
    paquete_capa5:   dict,
    motor_sugerido:  str,
    contiene_codigo: bool,
    nombre:          str,
) -> tuple:
    """
    Decide qué motor usar según el tipo de respuesta.
    Retorna (respuesta_final, fuente).
    """

    # ── TRACK 1: Python directo — matemáticas o base factual ─
    if tipo_respuesta == 'matematica_python':
        return respuesta_base, 'base_python'

    if _es_factual(respuesta_base, tipo_respuesta):
        return respuesta_base, 'base_python'

    # ── TRACK 2: Groq cloud — tareas técnicas ────────────
    if tipo_respuesta in ('tecnica_groq', 'ejecutiva') or contiene_codigo:
        prompt_tecnico = _prompt.construir(
            texto_original = texto_original,
            decision       = decision,
            comprension    = comprension,
            paquete_capa5  = paquete_capa5,
        )
        respuesta, fuente = _groq_cloud.generar_tecnico(
            texto_original = texto_original,
            prompt_completo = prompt_tecnico,
            tono            = decision.tono,
        )
        if respuesta and not _tiene_robotico(respuesta):
            return respuesta, fuente
        # Fallback a base_python si Groq cloud falla
        return respuesta_base, 'base_python'

    # ── TRACK 3: Bell Voice Engine — conversación pura ──
    tipo_msg = comprension.get('profunda', {}).get('tipo_mensaje', tipo_respuesta)
    emocion  = comprension.get('profunda', {}).get('emocion', '')
    respuesta_motor, fuente_motor = _motor_local.generar(
        texto_original,
        tono    = decision.tono,
        tipo    = tipo_msg,
        emocion = emocion,
        contexto= {'nombre': nombre},
    )

    # Si motor_v2 ya razonó la respuesta, usarla aunque el motor local falle
    respuesta_v2 = comprension.get('contextual', {}).get('respuesta_groq_v2', '')
    if respuesta_v2:
        return respuesta_v2, 'motor_v2'

    if fuente_motor in ('fallback', 'error'):
        # En lugar de base_python genérico, forzar llamada a Groq con la voz de Bell
        if _motor_local._activo:
            resp_groq, _ = _motor_local._groq_conversacional(texto_original, decision.tono)
            if resp_groq:
                return resp_groq, 'groq_fallback'
        return respuesta_base, 'base_python'

    if _tiene_robotico(respuesta_motor):
        if _motor_local._activo:
            resp_groq, _ = _motor_local._groq_conversacional(texto_original, decision.tono)
            if resp_groq:
                return resp_groq, 'groq_fallback'
        return respuesta_base, 'base_python'

    if _es_mejor_que_base(respuesta_motor, respuesta_base):
        verificada = _verificador.verificar(
            respuesta      = respuesta_motor,
            decision       = decision,
            texto_original = texto_original,
            nombre         = nombre,
        )
        if verificada and not _tiene_robotico(verificada):
            return verificada, fuente_motor

    # Último recurso: llamar a Groq directamente antes que base_python
    if _motor_local._activo:
        resp_groq, _ = _motor_local._groq_conversacional(texto_original, decision.tono)
        if resp_groq:
            return resp_groq, 'groq_fallback'

    return respuesta_base, 'base_python'


def _es_factual(respuesta_base: str, tipo: str) -> bool:
    """Respuestas que Python ya construyó bien y no necesitan motor."""
    TIPOS_PYTHON_DIRECTO = {
        'pregunta_sebastian', 'pregunta_identidad_bell',
        'pregunta_arquitectura_bell', 'presentacion_sebastian',
    }
    if tipo in TIPOS_PYTHON_DIRECTO:
        return True
    rb = respuesta_base.strip()
    if not rb or rb == 'Aquí estoy.':
        return False
    # Respuestas cortas factuales (datos concretos)
    if len(rb) < 50 and any(c.isdigit() for c in rb):
        return True
    frases_directas = [
        'no soy de ninguna empresa', 'me creó sebastian',
        'eres sebastian', 'tienes 19', 'bucaramanga',
        'trabajas en jelcon', 'estudias en uniminuto',
    ]
    rb_lower = rb.lower()
    return any(f in rb_lower for f in frases_directas)


def _tiene_robotico(respuesta: str) -> bool:
    if not respuesta:
        return False
    rl = respuesta.lower()
    return any(s in rl for s in _SEÑALES_ROBOTICO)


def _es_mejor_que_base(groq: str, base: str) -> bool:
    if not groq or not groq.strip():
        return False
    rg, rb = groq.strip(), base.strip()
    if rg.lower() == rb.lower():
        return True
    if len(rg) < len(rb) * 0.7 and len(rb) > 12:
        return False
    if len(rg) > len(rb) * 3 and len(rb) > 10:
        return False
    if len(rg) > len(rb) * 2 and len(rb) > 40:
        return False
    for frase in ['mente pura', 'respuesta base', 'sage:', 'tono:', 'escribe solo']:
        if frase in rg.lower():
            return False
    return True


def _guardar_en_buffer(paquete_capa5: dict, respuesta: str):
    try:
        pc1   = (paquete_capa5.get('paquete_capa4', {})
                              .get('paquete_capa3', {})
                              .get('paquete_capa2', {})
                              .get('paquete_capa1', {}))
        texto = pc1.get('contenido_original', '')
        comp  = (paquete_capa5.get('paquete_capa4', {})
                              .get('paquete_capa3', {})
                              .get('comprension', {}))
        if texto and respuesta:
            BufferSesion.obtener().agregar_turno(texto, respuesta, comp)
    except Exception:
        pass