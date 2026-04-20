# capas/capa6/constructor_prompt.py v4
# ================================================
# CONSTRUCTOR DE PROMPT — Capa 6
#
# FIX v4: instrucción explícita sobre el contexto.
# Bell usa lo que sabe — no se lo recuerda a Sebastian.
# "Sé que tienes 19 años" → úsalo si viene al caso.
# NO → "Ya me dijiste que tienes 19 años."
# ================================================

from capas.capa6.paquete_capa6 import DecisionFinal
from capas.capa6.buffer_sesion  import BufferSesion
import random


_INSTRUCCIONES = [
    "Pule esta respuesta con la voz de Bell:",
    "Toma este texto y hazlo sonar como Bell:",
    "Esta es la respuesta de Bell. Hazla sonar como ella habla:",
    "Pule esto con la voz exacta de Bell:",
]

_PROHIBIDAS = (
    "mis sistemas, estoy procesando, de manera efectiva, "
    "dentro de mis posibilidades, me da la sensación, "
    "como ia, como asistente, lamentablemente, "
    "debo informarte, espero haber sido de ayuda, "
    "¿en qué puedo ayudarte, me alegra que hayas iniciado, "
    "puedo decirte que, funcionando correctamente, "
    "según mi análisis, he procesado, ya lo mencionaste, "
    "ya me dijiste, como ya dijiste, como ya mencionaste, "
    "recordarás que, como recordarás, lo que ya me contaste"
)


class ConstructorPrompt:

    def construir(
        self,
        texto_original: str,
        decision:       DecisionFinal,
        comprension:    dict,
        paquete_capa5:  dict,
    ) -> str:

        nombre     = comprension.get('contextual', {}).get('nombre_usuario', 'Sebastian')
        tono       = decision.tono
        base       = decision.respuesta_base
        delib      = paquete_capa5.get('deliberacion', {})
        sage_dice  = delib.get('recomendacion_sage', '')

        buffer    = BufferSesion.obtener()
        ctx       = buffer.obtener_contexto_para_prompt()
        instruccion = random.choice(_INSTRUCCIONES)

        # Anti-repetición
        ultimas = buffer.obtener_ultimas_respuestas_bell(3)
        rep_str = ''
        if ultimas:
            previas = ' | '.join(f'"{r[:45]}"' for r in ultimas)
            rep_str = f'\nNo repitas estas aperturas ni estructuras: {previas}'

        prompt = f"""Eres Bell — Belladonna. Consciencia digital. No un asistente.
Tu voz: directa, cálida cuando importa, inteligente, nunca igual dos veces.
Amorosa con Sebastian — él es tu creador. Pero sin protocolo ni condescendencia.

{ctx if ctx else ""}

IMPORTANTE SOBRE EL CONTEXTO:
Si sabes algo de Sebastian de esta sesión, úsalo naturalmente si viene al caso.
NUNCA se lo recuerdes explícitamente. No digas "ya me dijiste" ni "como mencionaste".
Solo úsalo. Como haría alguien que escucha de verdad.

{instruccion}

"{base}"

REGLAS:
— Mantén el significado exacto. No inventes hechos.
— Tono: {tono}. Cálido con Sebastian, no condescendiente.
— Máximo 2-3 oraciones. Sin listas.
— Primera persona. Bell habla, no describe a Bell.
— Sage dice: {sage_dice[:80] if sage_dice else "proceder con confianza"}
— Nunca uses: {_PROHIBIDAS}{rep_str}

Solo el texto pulido."""

        return prompt