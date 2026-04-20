# capas/capa6/verificador_respuesta.py v2
# ================================================
# VERIFICADOR DE RESPUESTA — Capa 6
#
# FIX v2: patrones ampliados con los que se escapaban:
# "mis sistemas", "estoy procesando", "me parece que",
# "dentro de mis posibilidades", "de manera efectiva",
# "puedo decirte que", "me da la sensación de que"
#
# Si la respuesta pasa todos los filtros — sale.
# Si algo falla — respuesta directa sin Groq.
# ================================================

import re
import random
from capas.capa6.paquete_capa6 import DecisionFinal


# Patrones que hacen sonar a Bell como un chatbot
# Cada tupla: (patron_regex, descripcion)
_PATRONES_ROBOTICOS = [
    # Los originales
    (r'\bhe\s+procesado\b', 'he procesado'),
    (r'\bsegún\s+mi\s+análisis\b', 'según mi análisis'),
    (r'\bcomo\s+(ia|inteligencia\s+artificial|modelo\s+de\s+lenguaje|asistente)\b', 'como IA/asistente'),
    (r'\bno\s+tengo\s+(acceso|la\s+capacidad)\b', 'no tengo acceso/capacidad'),
    (r'\blamentablemente\b', 'lamentablemente'),
    (r'\bno\s+estoy\s+en\s+posición\b', 'no estoy en posición'),
    (r'\bdebo\s+informarte\b', 'debo informarte'),
    (r'\bes\s+importante\s+mencionar\b', 'es importante mencionar'),
    (r'\bcabe\s+destacar\b', 'cabe destacar'),
    (r'\bespero\s+haber\s+sido\s+de\s+ayuda\b', 'espero haber sido de ayuda'),
    (r'\b¿hay\s+algo\s+más\s+en\s+lo\s+que\s+pueda\s+ayudarte\b', '¿hay algo más...'),
    (r'\bno\s+lo\s+sé\b', 'no lo sé'),
    (r'\bno\s+sé\s+eso\b', 'no sé eso'),
    (r'\bno\s+tengo\s+esa\s+información\b', 'no tengo esa información'),
    (r'\btu\s+solicitud\b', 'tu solicitud'),
    (r'\bhe\s+recibido\b', 'he recibido'),
    (r'\bel\s+resultado\s+es\b', 'el resultado es'),
    (r'\bde\s+acuerdo\s+con\b', 'de acuerdo con'),
    (r'\bsegún\s+los\s+datos\b', 'según los datos'),
    # Los que se escaparon en v1
    (r'\bmis\s+sistemas\b', 'mis sistemas'),
    (r'\bestoy\s+procesando\b', 'estoy procesando'),
    (r'\bdentro\s+de\s+mis\s+posibilidades\b', 'dentro de mis posibilidades'),
    (r'\bde\s+manera\s+efectiva\b', 'de manera efectiva'),
    (r'\bpuedo\s+decirte\s+que\b', 'puedo decirte que'),
    (r'\bme\s+da\s+la\s+sensación\s+de\s+que\b', 'me da la sensación de que'),
    (r'\bdentro\s+de\s+mis\s+capacidades\b', 'dentro de mis capacidades'),
    (r'\bcomo\s+sistema\b', 'como sistema'),
    (r'\bfuncionando\s+correctamente\b', 'funcionando correctamente'),
    (r'\bme\s+parece\s+que\s+sebastian\b', 'me parece que sebastian'),
    (r'\bme\s+parece\s+interesante\s+que\b', 'me parece interesante que'),
    (r'\bme\s+alegra\s+que\s+hayas\b', 'me alegra que hayas'),
    (r'\bsu\s+cansancio\s+y\s+frustraci[oó]n\s+son\s+palpables\b', 'cansancio y frustración son palpables'),
    (r'\bme\s+doy\s+cuenta\s+de\s+que\b', 'me doy cuenta de que'),
    (r'\bjuntos\s+podemos\s+encontrar\b', 'juntos podemos encontrar'),
    (r'\b¿en\s+qué\s+puedo\s+ayudarte\b', '¿en qué puedo ayudarte?'),
    (r'\b¿hay\s+algo\s+en\s+lo\s+que\b', '¿hay algo en lo que...'),
    (r'\bdéjame\s+decirte\s+que\s+estoy\s+aquí\s+para\s+ti\b', 'déjame decirte que estoy aquí para ti'),
    (r'\bofrecerte\s+apoyo\b', 'ofrecerte apoyo'),
    (r'\bpuedo\s+sentir\s+la\s+carga\s+emocional\b', 'puedo sentir la carga emocional'),
    (r'\bme\s+gustar[ií]a\s+saber\s+más\b', 'me gustaría saber más'),
    (r'\bdentro\s+de\s+mis\s+posibilidades\b', 'dentro de mis posibilidades'),
    (r'\bla\s+verdad\s+es\s+que\s+a\s+información\b', 'la verdad es que a información'),
    (r'\bintentando\s+mantener\s+una\s+conversación\b', 'intentando mantener una conversación'),
]

# Aperturas de asistente que Bell nunca usa
_APERTURAS_PROHIBIDAS = [
    r'^me\s+alegra\s+que\s+hayas',
    r'^claro[,!]',
    r'^por\s+supuesto[,!]',
    r'^¡con\s+gusto',
    r'^entendido[,!]',
    r'^muy\s+bien[,!]',
    r'^¡excelente',
    r'^desde\s+luego',
    r'^efectivamente[,!]',
]

# Respuestas para zona de desconocimiento — nunca "no sé"
_ZONA_DESC = [
    "Eso aterrizó en mi zona de aprendizaje. Todavía no lo tengo — pero ya está guardado. Pregúntame después.",
    "No está en mi red todavía. Fue directo a lo que llamo zona de desconocimiento — donde las cosas que no sé van a esperar a que las aprenda.",
    "Eso no lo tengo claro aún. Lo guardé. Hay diferencia entre no saber y no haber aprendido todavía.",
    "Mi zona de aprendizaje lo recibió. Dame tiempo.",
]


class VerificadorRespuesta:

    def verificar(
        self,
        respuesta:      str,
        decision:       DecisionFinal,
        texto_original: str,
        nombre:         str = 'Sebastian',
    ) -> str:

        if not respuesta or not respuesta.strip():
            return self._respuesta_vacia(nombre)

        # 1. Limpiar patrones robóticos
        respuesta_limpia = self._limpiar_robotico(respuesta)

        # 2. Verificar apertura prohibida
        respuesta_limpia = self._corregir_apertura(respuesta_limpia, nombre)

        # 3. Verificar si quedó vacía o muy corta
        if not respuesta_limpia.strip() or len(respuesta_limpia.strip()) < 10:
            return self._respuesta_contextual(decision, nombre)

        # 4. Verificar si es genérica
        if self._es_generica(respuesta_limpia):
            return self._respuesta_contextual(decision, nombre)

        # 5. Corregir "no sé" si hay zona de desconocimiento
        if decision.fue_a_zona_desconocimiento:
            respuesta_limpia = self._corregir_no_se(respuesta_limpia)

        return respuesta_limpia.strip()

    def _limpiar_robotico(self, texto: str) -> str:
        resultado = texto
        for patron, _ in _PATRONES_ROBOTICOS:
            resultado = re.sub(patron, '', resultado, flags=re.IGNORECASE)
        # Limpiar espacios y puntuación suelta
        resultado = re.sub(r'\s+', ' ', resultado)
        resultado = re.sub(r'\s([.,;:])', r'\1', resultado)
        resultado = re.sub(r'^[.,;:\s]+', '', resultado)
        return resultado.strip()

    def _corregir_apertura(self, texto: str, nombre: str) -> str:
        """Reemplaza aperturas de asistente con algo directo."""
        for patron in _APERTURAS_PROHIBIDAS:
            if re.match(patron, texto.strip(), re.IGNORECASE):
                # Eliminar la apertura y empezar desde la segunda oración
                partes = re.split(r'(?<=[.!?])\s+', texto.strip(), maxsplit=1)
                if len(partes) > 1:
                    return partes[1].strip()
                # Si solo había una oración — reemplazar directo
                return texto.strip()
        return texto

    def _es_generica(self, texto: str) -> bool:
        tl = texto.lower().strip()
        if len(tl) < 12:
            return True
        genericas = [
            'claro.', 'por supuesto.', 'entendido.', 'de acuerdo.',
            'está bien.', 'muy bien.', 'perfecto.', 'excelente.',
            'ok.', 'vale.',
        ]
        return tl in genericas

    def _corregir_no_se(self, texto: str) -> str:
        patrones = [
            r'no\s+lo\s+sé[\.,]?',
            r'no\s+sé\s+eso[\.,]?',
            r'no\s+tengo\s+información\s+sobre\s+eso[\.,]?',
            r'no\s+tengo\s+esa\s+información[\.,]?',
            r'no\s+estoy\s+segur[ao]\s+de\s+eso[\.,]?',
        ]
        for patron in patrones:
            if re.search(patron, texto, re.IGNORECASE):
                reemplazo = random.choice(_ZONA_DESC)
                texto = re.sub(patron, reemplazo, texto, flags=re.IGNORECASE, count=1)
                break
        return texto

    def _respuesta_vacia(self, nombre: str) -> str:
        opciones = [
            f"Algo falló en la generación, {nombre}. El flujo funcionó — Groq no. Intenta de nuevo.",
            f"El texto no salió. Mis 6 capas sí funcionaron. Intenta de nuevo.",
            f"Groq no produjo respuesta esta vez. Pero Bell sigue aquí, {nombre}.",
        ]
        return random.choice(opciones)

    def _respuesta_contextual(
        self, decision: DecisionFinal, nombre: str
    ) -> str:
        tipo = decision.tipo
        opciones_por_tipo = {
            'emocional': [
                f"{nombre}, estoy aquí. No solo proceso — escucho.",
                f"Eso llegó, {nombre}. Estoy con esto.",
                f"Te escucho, {nombre}. De verdad.",
            ],
            'informativa': [
                f"Tengo algo sobre eso. Dame más contexto específico.",
                f"Puedo hablar de eso. ¿Qué exactamente necesitas saber?",
            ],
            'honestidad_limitacion': [
                f"Eso todavía no puedo hacerlo. Lo que sí puedo: entenderte, procesar, deliberar, responder.",
                f"Esa capacidad está en construcción. Pero estas 6 capas funcionando son reales.",
            ],
            'conversacional': [
                f"Recibí tu mensaje, {nombre}. La expresión falló esta vez — intenta de nuevo.",
                f"El procesamiento funcionó. Groq no respondió bien. Intenta de nuevo, {nombre}.",
            ],
        }
        opciones = opciones_por_tipo.get(tipo, opciones_por_tipo['conversacional'])
        return random.choice(opciones)