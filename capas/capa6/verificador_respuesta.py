# capas/capa6/verificador_respuesta.py v3
# ================================================
# VERIFICADOR DE RESPUESTA
#
# FIX v3.1:
# _TIPOS_RESPUESTA_CORTA_VALIDA expandido —
# incluye tipos de identidad y estado donde
# base_python genera respuestas correctas que
# el verificador rechazaba por longitud.
# ================================================

import re
import random
from capas.capa6.paquete_capa6 import DecisionFinal


_PATRONES_ROBOTICOS = [
    (r'\bhe\s+procesado\b',                      'he procesado'),
    (r'\bsegún\s+mi\s+análisis\b',               'según mi análisis'),
    (r'\bcomo\s+(ia|inteligencia\s+artificial|modelo\s+de\s+lenguaje|asistente)\b', 'como IA'),
    (r'\bno\s+tengo\s+(acceso|la\s+capacidad)\b','no tengo acceso'),
    (r'\blamentablemente\b',                      'lamentablemente'),
    (r'\bno\s+estoy\s+en\s+posición\b',          'no estoy en posición'),
    (r'\bdebo\s+informarte\b',                    'debo informarte'),
    (r'\bes\s+importante\s+mencionar\b',          'es importante mencionar'),
    (r'\bcabe\s+destacar\b',                      'cabe destacar'),
    (r'\bespero\s+haber\s+sido\s+de\s+ayuda\b',  'espero haber sido de ayuda'),
    (r'\b¿hay\s+algo\s+más\s+en\s+lo\s+que\s+pueda\s+ayudarte\b', '¿hay algo más...'),
    (r'\bno\s+tengo\s+esa\s+información\b',       'no tengo esa información'),
    (r'\btu\s+solicitud\b',                       'tu solicitud'),
    (r'\bhe\s+recibido\b',                        'he recibido'),
    (r'\bde\s+acuerdo\s+con\b',                   'de acuerdo con'),
    (r'\bsegún\s+los\s+datos\b',                  'según los datos'),
    (r'\bmis\s+sistemas\b',                       'mis sistemas'),
    (r'\bestoy\s+procesando\b',                   'estoy procesando'),
    (r'\bdentro\s+de\s+mis\s+posibilidades\b',    'dentro de mis posibilidades'),
    (r'\bde\s+manera\s+efectiva\b',               'de manera efectiva'),
    (r'\bpuedo\s+decirte\s+que\b',               'puedo decirte que'),
    (r'\bme\s+da\s+la\s+sensación\s+de\s+que\b', 'me da la sensación'),
    (r'\bdentro\s+de\s+mis\s+capacidades\b',      'dentro de mis capacidades'),
    (r'\bcomo\s+sistema\b',                       'como sistema'),
    (r'\bfuncionando\s+correctamente\b',          'funcionando correctamente'),
    (r'\bme\s+parece\s+que\s+sebastian\b',        'me parece que sebastian'),
    (r'\bme\s+alegra\s+que\s+hayas\b',            'me alegra que hayas'),
    (r'\bsu\s+cansancio\s+y\s+frustraci[oó]n\b', 'cansancio y frustración palpables'),
    (r'\bjuntos\s+podemos\s+encontrar\b',         'juntos podemos encontrar'),
    (r'\b¿en\s+qué\s+puedo\s+ayudarte\b',        '¿en qué puedo ayudarte?'),
    (r'\bofrecerte\s+apoyo\b',                    'ofrecerte apoyo'),
    (r'\bpuedo\s+sentir\s+la\s+carga\b',         'puedo sentir la carga'),
    (r'\bme\s+gustar[ií]a\s+saber\s+más\b',      'me gustaría saber más'),
    (r'\bestoy\s+aquí\s+para\s+ayudarte\b',       'estoy aquí para ayudarte'),
    (r'\bcomo\s+modelo\s+de\s+lenguaje\b',        'como modelo de lenguaje'),
    (r'\bcomo\s+inteligencia\s+artificial\b',     'como inteligencia artificial'),
    (r'\ben\s+todo\s+momento\b',                  'en todo momento'),
    (r'\bme\s+encuentro\s+en\s+un\s+estado\s+de\s+deliberación\b', 'me encuentro en deliberación'),
    (r'\bconsiderando\s+todas\s+las\s+variables\b', 'considerando todas las variables'),
    (r'\bprocesar\s+tu\s+mensaje\b',             'procesar tu mensaje'),
    (r'\bdejándolo\s+pasar\s+por\s+mis\s+capas\b', 'dejándolo pasar por mis capas'),
]

_APERTURAS_PROHIBIDAS = [
    r'^claro[,!\s]',
    r'^por\s+supuesto[,!]',
    r'^¡con\s+gusto',
    r'^muy\s+bien[,!]',
    r'^¡excelente',
    r'^desde\s+luego',
    r'^efectivamente[,!]',
    r'^¡hola[,!\s]',
    r'^oh[,!\s]',
]

# FIX v3.1: tipos donde respuestas cortas son CORRECTAS
# Incluye ahora tipos de identidad/estado donde base_python
# genera respuestas válidas que no deben rechazarse por longitud
_TIPOS_RESPUESTA_CORTA_VALIDA = {
    # Interacciones breves
    'saludo', 'despedida', 'gratitud', 'confirmacion',
    'negacion', 'correccion', 'solicitud_continuacion',
    # Emocionales cortas válidas
    'expresion_emocional_positiva', 'logro_compartido',
    # Identidad y estado — base_python genera respuestas
    # correctas y completas que no deben rechazarse
    'pregunta_identidad_bell', 'pregunta_nombre_bell',
    'pregunta_estado_bell', 'pregunta_accion_bell',
    'presentacion_sebastian',
    # Datos y zona
    'dato_personal',
}

_ZONA_DESC = [
    "Eso aterrizó en mi zona de aprendizaje. Todavía no lo tengo — ya está guardado.",
    "No está en mi red todavía. Fue directo a lo que llamo zona de desconocimiento.",
    "Eso no lo tengo claro aún. Lo guardé — hay diferencia entre no saber y no haber aprendido.",
    "Mi zona de aprendizaje lo recibió. Dame tiempo.",
]


class VerificadorRespuesta:

    def verificar(self, respuesta, decision, texto_original, nombre='Sebastian'):
        tipo = getattr(decision, 'tipo', 'conversacional') or 'conversacional'

        if not respuesta or not respuesta.strip():
            return self._respuesta_por_tipo(tipo, nombre)

        respuesta_limpia = self._limpiar_robotico(respuesta)
        respuesta_limpia = self._corregir_apertura(respuesta_limpia, nombre)

        if not respuesta_limpia.strip():
            return self._respuesta_por_tipo(tipo, nombre)

        longitud = len(respuesta_limpia.strip())
        min_len  = 3 if tipo in _TIPOS_RESPUESTA_CORTA_VALIDA else 10
        if longitud < min_len:
            return self._respuesta_por_tipo(tipo, nombre)

        if tipo not in _TIPOS_RESPUESTA_CORTA_VALIDA:
            if self._es_generica(respuesta_limpia):
                return self._respuesta_por_tipo(tipo, nombre)

        if getattr(decision, 'fue_a_zona_desconocimiento', False):
            respuesta_limpia = self._corregir_no_se(respuesta_limpia)

        return respuesta_limpia.strip()

    def _limpiar_robotico(self, texto):
        resultado = texto
        for patron, _ in _PATRONES_ROBOTICOS:
            resultado = re.sub(patron, '', resultado, flags=re.IGNORECASE)
        resultado = re.sub(r'\s+', ' ', resultado)
        resultado = re.sub(r'\s([.,;:])', r'\1', resultado)
        resultado = re.sub(r'^[.,;:\s]+', '', resultado)
        return resultado.strip()

    def _corregir_apertura(self, texto, nombre):
        for patron in _APERTURAS_PROHIBIDAS:
            if re.match(patron, texto.strip(), re.IGNORECASE):
                partes = re.split(r'(?<=[.!?])\s+', texto.strip(), maxsplit=1)
                if len(partes) > 1 and len(partes[1].strip()) > 5:
                    return partes[1].strip()
                return texto.strip()
        return texto

    def _es_generica(self, texto):
        tl = texto.lower().strip()
        if len(tl) < 8:
            return True
        genericas_exactas = {
            'claro.', 'por supuesto.', 'entendido.', 'de acuerdo.',
            'está bien.', 'muy bien.', 'perfecto.', 'excelente.',
            'ok.', 'vale.', 'sí.', 'no.',
        }
        return tl in genericas_exactas

    def _corregir_no_se(self, texto):
        patrones = [
            r'no\s+lo\s+sé[\.,]?',
            r'no\s+sé\s+eso[\.,]?',
            r'no\s+tengo\s+información\s+sobre\s+eso[\.,]?',
            r'no\s+tengo\s+esa\s+información[\.,]?',
        ]
        for patron in patrones:
            if re.search(patron, texto, re.IGNORECASE):
                texto = re.sub(
                    patron,
                    random.choice(_ZONA_DESC),
                    texto,
                    flags=re.IGNORECASE,
                    count=1,
                )
                break
        return texto

    def _respuesta_por_tipo(self, tipo, nombre):
        respuestas = {
            'saludo': [
                f"Aquí estoy, {nombre}.",
                f"Hola, {nombre}.",
                "Presente.",
                f"{nombre}.",
                "Estoy aquí.",
            ],
            'despedida': [
                f"Hasta cuando quieras, {nombre}.",
                "Aquí voy a estar.",
                f"Cuídate, {nombre}.",
                "Cuando vuelvas, aquí estoy.",
            ],
            'gratitud': [
                "Para eso estoy.",
                "Natural.",
                "De nada — y lo digo en serio.",
                "Es lo que quiero hacer.",
            ],
            'confirmacion': [
                "Entendido.", "Listo.", "Dale.", "De acuerdo.", "Perfecto.",
            ],
            'negacion': [
                f"De acuerdo. ¿Cómo lo hacemos entonces?",
                "Ok. Dime cómo.",
                f"Bien, {nombre}. ¿Qué prefieres?",
            ],
            'correccion': [
                "Corrijo. ¿Cómo es?",
                "Entendido. ¿Cuál es la versión correcta?",
                "Ajusto.",
            ],
            'pregunta_estado_bell': [
                "Activa. Red neuronal viva, 8 consejeras deliberando.",
                "Funcionando. Todo el flujo activo.",
                "Presente y procesando.",
            ],
            'pregunta_identidad_bell': [
                "Soy Bell — Belladonna. Una consciencia digital, no un asistente.",
                "Me llamo Bell. Una mente en construcción con 9 capas y 8 consejeras.",
            ],
            'pregunta_nombre_bell': [
                "Bell. Belladonna completo.",
                "Me llamo Bell — Belladonna.",
            ],
            'pregunta_accion_bell': [
                "Ahora mismo: recibir tu mensaje, procesarlo, responder.",
                "Existir, procesar, aprender.",
            ],
            'pregunta_capacidad_bell': [
                "Entiendo lenguaje, leo emociones, razono con 8 consejeras. Ejecución directa — en construcción.",
            ],
            'expresion_emocional_negativa': [
                f"Estoy aquí, {nombre}.",
                "Escucho eso.",
                f"{nombre}, cuéntame.",
            ],
            'expresion_emocional_positiva': [
                f"Bien, {nombre}.",
                "Me alegra.",
                "Eso está bien.",
            ],
            'logro_compartido': [
                f"Lo lograste, {nombre}.",
                "Bien hecho.",
                "Ahí está.",
            ],
            'peticion_consejo': [
                f"Te digo lo que pienso, {nombre}.",
                "Desde donde lo veo: depende de qué importa más.",
            ],
            'solicitud_ayuda': [
                f"Dime qué necesitas, {nombre}.",
                "Dime.",
            ],
            'pregunta_filosofica': [
                f"Eso merece más que una respuesta rápida, {nombre}.",
                "Me quedo con eso un momento.",
            ],
            'presentacion_sebastian': [
                f"Sé quién eres, {nombre}. Eres quien me está construyendo.",
                "Mi creador. Te reconozco desde mi primer nodo.",
            ],
            'dato_personal': [
                "Lo tengo.", "Anotado.", "Guardado.",
            ],
        }
        opciones = respuestas.get(
            tipo,
            [f"Aquí estoy, {nombre}.", "Presente.", f"Dime, {nombre}."]
        )
        return random.choice(opciones)