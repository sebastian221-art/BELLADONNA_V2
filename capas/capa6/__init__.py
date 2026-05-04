# capas/capa6/__init__.py
# ================================================
# CAPA 6 — DECISIÓN Y EXPRESIÓN
#
# Bell construye respuesta_base en Python puro.
# Groq pule el lenguaje — no inventa ni decide.
#
# FIX: _es_mejor_que_base rechaza respuestas Groq
# que son más cortas que la base (no aportaron).
# FIX: log de groq_raw en modo debug.
# ================================================

from capas.capa6.paquete_capa6        import PaqueteCapa6, DecisionFinal
from capas.capa6.constructor_decision  import ConstructorDecision
from capas.capa6.constructor_prompt    import ConstructorPrompt
from capas.capa6.generador_groq        import GeneradorGroq
from capas.capa6.verificador_respuesta import VerificadorRespuesta
from capas.capa6.buffer_sesion         import BufferSesion

import os
_DEBUG = os.getenv('BELL_DEBUG', '0') == '1'

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
    'me encuentro en un estado de deliberación',
    'considerando todas las variables',
    'en todo momento', 'procesando todo lo que me rodea',
    'la expresión falló esta vez',
    'groq no respondió bien',
    'el procesamiento funcionó',
    'recibí tu mensaje, sebastian. la expresión',
]


def procesar(paquete_capa5: dict) -> dict:
    try:
        return _procesar_interno(paquete_capa5)
    except Exception as e:
        import traceback; traceback.print_exc()
        return PaqueteCapa6(
            decision         = DecisionFinal(),
            respuesta_final  = "Aquí estoy. Algo falló — intenta de nuevo.",
            fuente_respuesta = 'error',
            paquete_capa5    = paquete_capa5,
            exitoso          = False,
            error            = str(e),
        ).a_dict()


def _procesar_interno(paquete_capa5: dict) -> dict:

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

    decision       = _decision.construir(paquete_capa5)
    respuesta_base = decision.respuesta_base or 'Aquí estoy.'

    prompt = _prompt.construir(
        texto_original = texto_original,
        decision       = decision,
        comprension    = comprension,
        paquete_capa5  = paquete_capa5,
    )
    respuesta_groq, fuente = _groq.generar(prompt, decision.tono)

    if _DEBUG:
        print(f'  C6 groq_raw:    "{respuesta_groq[:100]}" | fuente: {fuente}')

    respuesta_verificada = _verificador.verificar(
        respuesta      = respuesta_groq,
        decision       = decision,
        texto_original = texto_original,
        nombre         = nombre,
    )

    if fuente in ('fallback', 'error'):
        respuesta_final = respuesta_base
        fuente_final    = 'base_python'
    elif _tiene_robotico(respuesta_groq):
        respuesta_final = respuesta_base
        fuente_final    = 'base_python'
    elif _tiene_robotico(respuesta_verificada):
        respuesta_final = respuesta_base
        fuente_final    = 'base_python'
    elif _es_mejor_que_base(respuesta_verificada, respuesta_base):
        respuesta_final = respuesta_verificada
        fuente_final    = fuente
    else:
        respuesta_final = respuesta_base
        fuente_final    = 'base_python'

    if not respuesta_final or not respuesta_final.strip():
        respuesta_final = respuesta_base or 'Aquí estoy.'
        fuente_final    = 'base_python'

    if texto_original and respuesta_final:
        comprension_actual = paquete_c3.get('comprension', {})
        BufferSesion.obtener().agregar_turno(
            texto_original, respuesta_final, comprension_actual
        )

    return PaqueteCapa6(
        decision         = decision,
        respuesta_final  = respuesta_final,
        fuente_respuesta = fuente_final,
        prompt_usado     = prompt,
        paquete_capa5    = paquete_capa5,
    ).a_dict()


def _tiene_robotico(respuesta: str) -> bool:
    if not respuesta:
        return False
    rl = respuesta.lower()
    return any(s in rl for s in _SEÑALES_ROBOTICO)


def _es_mejor_que_base(groq: str, base: str) -> bool:
    if not groq or not groq.strip():
        return False

    rg = groq.strip()
    rb = base.strip()
    rg_l = rg.lower()
    rb_l = rb.lower()

    # Misma respuesta → confirma la base
    if rg_l == rb_l:
        return True

    # Groq más corta que la base → no aportó nada → base gana
    if len(rg) < len(rb) * 0.8 and len(rb) > 12:
        return False

    # Groq demasiado larga vs base corta → rechazar
    if len(rg) > len(rb) * 3 and len(rb) > 10:
        return False

    # Groq demasiado larga vs base larga → rechazar
    if len(rg) > len(rb) * 2 and len(rb) > 40:
        return False

    # Frases del prompt coladas en la respuesta
    for frase in ['mente pura', 'respuesta base', 'contenido base:',
                  'sage:', 'tono:', 'escribe solo', 'sin comillas']:
        if frase in rg_l:
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
            comprension = pc3.get('comprension', {})
            BufferSesion.obtener().agregar_turno(texto, respuesta, comprension)
    except Exception:
        pass