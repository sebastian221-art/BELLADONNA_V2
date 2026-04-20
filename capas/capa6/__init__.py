# capas/capa6/__init__.py
# ================================================
# CAPA 6 — DECISIÓN Y EXPRESIÓN
#
# La comprensión ya viene enriquecida de Capa 3
# (con el motor de lenguaje si está disponible).
#
# Bell construye respuesta_base en Python puro.
# Groq pule el lenguaje — no inventa ni decide.
# Si Groq produce algo robótico → base gana.
# ================================================

from capas.capa6.paquete_capa6        import PaqueteCapa6, DecisionFinal
from capas.capa6.constructor_decision  import ConstructorDecision
from capas.capa6.constructor_prompt    import ConstructorPrompt
from capas.capa6.generador_groq        import GeneradorGroq
from capas.capa6.verificador_respuesta import VerificadorRespuesta
from capas.capa6.buffer_sesion         import BufferSesion

_decision    = ConstructorDecision()
_prompt      = ConstructorPrompt()
_groq        = GeneradorGroq()
_verificador = VerificadorRespuesta()

_SEÑALES_ROBOTICO = [
    'mis sistemas', 'estoy procesando', 'de manera efectiva',
    'dentro de mis posibilidades', 'me da la sensación',
    'funcionando correctamente', 'me alegra que hayas iniciado',
    'su cansancio y frustración son palpables',
    'me doy cuenta de que', 'juntos podemos encontrar',
    'puedo ofrecerte apoyo', 'me parece que sebastian',
    'debo informarte', 'como ia', 'como asistente',
    'según mi análisis', 'he procesado',
    'tu saludo me encontró', 'en un estado neutro',
    'la aprobación de todas las consejeras',
    'espero tu próximo paso', 'como modelo de lenguaje',
    'como sistema de inteligencia',
]


def procesar(paquete_capa5: dict) -> dict:
    try:
        return _procesar_interno(paquete_capa5)
    except Exception as e:
        import traceback; traceback.print_exc()
        return PaqueteCapa6(
            decision         = DecisionFinal(),
            respuesta_final  = "Algo falló. Bell sigue aquí — intenta de nuevo.",
            fuente_respuesta = 'error',
            paquete_capa5    = paquete_capa5,
            exitoso          = False,
            error            = str(e),
        ).a_dict()


def _procesar_interno(paquete_capa5: dict) -> dict:

    # Veto
    if paquete_capa5.get('veto'):
        respuesta_veto = paquete_capa5.get('respuesta_directa', '')
        _guardar_en_buffer(paquete_capa5, respuesta_veto)
        return PaqueteCapa6(
            decision         = DecisionFinal(tipo='veto_respuesta'),
            respuesta_final  = respuesta_veto,
            fuente_respuesta = 'veto_capa5',
            paquete_capa5    = paquete_capa5,
        ).a_dict()

    paquete_c4     = paquete_capa5.get('paquete_capa4', {})
    paquete_c3     = paquete_c4.get('paquete_capa3', {})
    paquete_c2     = paquete_c3.get('paquete_capa2', {})
    paquete_c1     = paquete_c2.get('paquete_capa1', {})
    comprension    = paquete_c3.get('comprension', {})
    texto_original = paquete_c1.get('contenido_original', '')
    nombre         = comprension.get('contextual', {}).get('nombre_usuario', 'Sebastian')

    # ── 1. BELL DECIDE EL CONTENIDO ────────────────────────
    # La comprensión ya viene enriquecida del motor en Capa 3
    decision       = _decision.construir(paquete_capa5)
    respuesta_base = decision.respuesta_base

    # ── 2. GROQ PULE LA BASE ────────────────────────────────
    prompt = _prompt.construir(
        texto_original = texto_original,
        decision       = decision,
        comprension    = comprension,
        paquete_capa5  = paquete_capa5,
    )
    respuesta_groq, fuente = _groq.generar(prompt, decision.tono)

    # ── 3. VERIFICAR Y ELEGIR ───────────────────────────────
    respuesta_verificada = _verificador.verificar(
        respuesta      = respuesta_groq,
        decision       = decision,
        texto_original = texto_original,
        nombre         = nombre,
    )

    if fuente in ('fallback', 'error'):
        respuesta_final = respuesta_base
        fuente_final    = 'base_python'
    elif _groq_tiene_robotico(respuesta_groq):
        respuesta_final = respuesta_base
        fuente_final    = 'base_python'
    elif _es_mejor_que_base(respuesta_verificada, respuesta_base):
        respuesta_final = respuesta_verificada
        fuente_final    = fuente
    else:
        respuesta_final = respuesta_base
        fuente_final    = 'base_python'

    # ── 4. GUARDAR EN BUFFER ────────────────────────────────
    if texto_original and respuesta_final:
        BufferSesion.obtener().agregar_turno(texto_original, respuesta_final)

    return PaqueteCapa6(
        decision         = decision,
        respuesta_final  = respuesta_final,
        fuente_respuesta = fuente_final,
        prompt_usado     = prompt,
        paquete_capa5    = paquete_capa5,
    ).a_dict()


def _groq_tiene_robotico(respuesta: str) -> bool:
    if not respuesta:
        return False
    rl = respuesta.lower()
    return any(señal in rl for señal in _SEÑALES_ROBOTICO)


def _es_mejor_que_base(respuesta_groq: str, base: str) -> bool:
    if not respuesta_groq or not respuesta_groq.strip():
        return False
    rg = respuesta_groq.strip().lower()
    rb = base.strip().lower()
    if rg == rb:
        return True
    if len(respuesta_groq) > len(base) * 2.5 and len(base) > 20:
        return False
    frases_prompt = [
        'mente pura', 'respuesta base', 'texto pulido',
        'instrucción', 'reglas absolutas', 'sin comillas',
    ]
    for frase in frases_prompt:
        if frase in rg:
            return False
    return True


def _guardar_en_buffer(paquete_capa5: dict, respuesta: str):
    try:
        pc4   = paquete_capa5.get('paquete_capa4', {})
        pc3   = pc4.get('paquete_capa3', {})
        pc2   = pc3.get('paquete_capa2', {})
        pc1   = pc2.get('paquete_capa1', {})
        texto = pc1.get('contenido_original', '')
        if texto and respuesta:
            BufferSesion.obtener().agregar_turno(texto, respuesta)
    except Exception:
        pass