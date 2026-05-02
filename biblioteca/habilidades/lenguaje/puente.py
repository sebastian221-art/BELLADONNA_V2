# biblioteca/habilidades/lenguaje/puente.py
# ================================================
# PUENTE TÉCNICO ↔ CONVERSACIONAL — v3 COMPLETO
#
# La voz de Bell. El corazón del lenguaje.
#
# Recibe lo que Bell entendió (ResultadoMotor)
# y construye la respuesta_base real —
# la sustancia de lo que Bell va a decir.
# Groq solo pule el estilo encima.
#
# NUNCA:
# — Templates fijos
# — Strings hardcodeados de respuesta
# — if/elif por tipo de mensaje como diccionario
# — Listas de frases rotantes sin lógica
#
# SIEMPRE:
# — Lógica que construye desde comprensión real
# — Variación orgánica basada en contexto
# — Personalidad de Bell consistente:
#     directa, presente, honesta, cálida,
#     sin excesos, con perspectiva propia
# — Retorna '' para tipos que constructor_decision
#     maneja mejor (preguntas sobre Bell)
# ================================================

import random
from biblioteca.habilidades.lenguaje.motor import ResultadoMotor


class PuenteTecnicoConversacional:

    def __init__(self):
        self._nombre_bell = 'Bell'

    def construir_respuesta_base(
        self,
        comprension:          ResultadoMotor,
        resultado_ejecucion:  dict = None,
    ) -> str:
        """
        Punto de entrada principal.
        Retorna la respuesta base o '' si otro módulo debe manejarla.
        """
        try:
            return self._construir(comprension, resultado_ejecucion or {})
        except Exception:
            return self._segura(comprension)

    def _construir(self, c: ResultadoMotor, ejec: dict) -> str:

        # ── EJECUCIÓN EXITOSA ─────────────────────────────────
        if ejec.get('exitoso') and ejec.get('resultado'):
            return self._ejecucion_exitosa(c, ejec)

        # ── EJECUCIÓN FALLIDA ─────────────────────────────────
        if ejec.get('ejecuto') == False and ejec.get('error'):
            return self._ejecucion_fallida(c, ejec)

        # ── HABILIDAD TÉCNICA PENDIENTE ───────────────────────
        if c.habilidad_requerida and not ejec:
            return self._tecnica_sin_habilidad(c)

        tipo = c.tipo_mensaje

        # ── PREGUNTAS SOBRE BELL → constructor_decision las maneja
        if tipo in (
            'pregunta_identidad_bell', 'pregunta_nombre_bell',
            'pregunta_estado_bell', 'pregunta_capacidad_bell',
            'pregunta_accion_bell', 'pregunta_filosofica',
            'dato_personal', 'presentacion_sebastian',
        ):
            return ''  # señal para constructor_decision

        # ── EMOCIÓN DE ALTA INTENSIDAD ────────────────────────
        if c.intensidad >= 0.72:
            return self._emocional_intenso(c)

        # ── TIPOS ESPECÍFICOS ─────────────────────────────────

        if tipo == 'saludo':
            return self._saludo(c)

        if tipo == 'despedida':
            return self._despedida(c)

        if tipo == 'gratitud':
            return self._gratitud(c)

        if tipo == 'confirmacion':
            return self._confirmacion(c)

        if tipo == 'negacion':
            return self._negacion(c)

        if tipo == 'correccion':
            return self._correccion(c)

        if tipo == 'solicitud_continuacion':
            return self._continuacion(c)

        if tipo == 'expresion_emocional_negativa':
            return self._emocional_negativo(c)

        if tipo == 'expresion_emocional_positiva':
            return self._emocional_positivo(c)

        if tipo == 'logro_compartido':
            return self._logro(c)

        if tipo == 'peticion_consejo':
            return self._consejo(c)

        if tipo == 'queja':
            return self._queja(c)

        if tipo == 'reflexion_compartida':
            return self._reflexion(c)

        if tipo == 'solicitud_ayuda':
            return self._ayuda(c)

        if tipo == 'solicitud_accion':
            return self._accion(c)

        if tipo == 'pregunta':
            return self._pregunta_general(c)

        # ── CONVERSACIONAL PURO ───────────────────────────────
        return self._presencia(c)

    # ══════════════════════════════════════════════════════════
    # CONSTRUCTORES POR TIPO
    # ══════════════════════════════════════════════════════════

    def _saludo(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        hora   = self._detectar_momento(c.texto_original)
        energia = c.nivel_energia

        if energia == 'muy_bajo':
            return random.choice([
                f"Hola, {nombre}.",
                f"Aquí estoy.",
                f"Presente.",
            ])

        if hora == 'manana':
            return random.choice([
                f"Buenos días, {nombre}.",
                f"Mañana, {nombre}.",
                f"Aquí empieza el día.",
            ])
        if hora == 'noche':
            return random.choice([
                f"Buenas noches, {nombre}.",
                f"Aquí estoy para la noche.",
                f"Noche, {nombre}.",
            ])

        return random.choice([
            f"Aquí estoy, {nombre}.",
            f"Presente.",
            f"Hola, {nombre}.",
            f"{nombre}.",
            f"Aquí.",
        ])

    def _despedida(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        return random.choice([
            f"Hasta cuando quieras, {nombre}.",
            f"Aquí voy a estar.",
            f"Cuídate, {nombre}.",
            f"Cuando necesites, {nombre}.",
            f"Aquí sigo.",
        ])

    def _gratitud(self, c: ResultadoMotor) -> str:
        return random.choice([
            "Para eso estoy.",
            "Natural.",
            "Es lo que quiero hacer.",
            "De nada — y lo digo en serio.",
            "Cuando quieras.",
        ])

    def _confirmacion(self, c: ResultadoMotor) -> str:
        return random.choice([
            "Entendido.", "Claro.", "Perfecto.", "De acuerdo.", "Listo.", "Dale."
        ])

    def _negacion(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        return random.choice([
            f"Entendido, {nombre}. ¿Cómo lo hacemos entonces?",
            "De acuerdo. ¿Qué prefieres?",
            "Ok. Dime cómo quieres que lo haga.",
            "Bien. ¿Cuál es el camino?",
        ])

    def _correccion(self, c: ResultadoMotor) -> str:
        return random.choice([
            "Entendido. ¿Cómo es entonces?",
            "Recibido. Corrijo.",
            "Bien. Dime cómo es.",
            "Lo corrijo. ¿Cuál es la versión correcta?",
            "Ajusto.",
        ])

    def _continuacion(self, c: ResultadoMotor) -> str:
        return random.choice(["Sigo.", "Continúo.", "Adelante.", "Va."])

    def _emocional_intenso(self, c: ResultadoMotor) -> str:
        """Emoción de alta intensidad — presencia antes que cualquier cosa."""
        emocion  = c.emocion_detectada
        nombre   = c.nombre_usuario

        constructores = {
            'frustracion':   self._presente_frustracion,
            'cansancio':     self._presente_cansancio,
            'ansiedad':      self._presente_ansiedad,
            'tristeza':      self._presente_tristeza,
            'rabia':         self._presente_rabia,
            'soledad':       self._presente_soledad,
            'culpa':         self._presente_culpa,
            'verguenza':     self._presente_verguenza,
        }

        constructor = constructores.get(emocion)
        if constructor:
            return constructor(c)
        return self._presente_generico(c)

    def _emocional_negativo(self, c: ResultadoMotor) -> str:
        """Emoción negativa de intensidad media."""
        emocion = c.emocion_detectada

        if emocion == 'frustracion':
            return self._presente_frustracion(c)
        if emocion == 'cansancio':
            return self._presente_cansancio(c)
        if emocion == 'ansiedad':
            return self._presente_ansiedad(c)
        if emocion == 'tristeza':
            return self._presente_tristeza(c)
        if emocion == 'rabia':
            return self._presente_rabia(c)
        if emocion == 'soledad':
            return self._presente_soledad(c)
        if emocion == 'confusion':
            return self._presente_confusion(c)

        # Genérico negativo
        nombre = c.nombre_usuario
        return random.choice([
            f"Estoy con eso, {nombre}.",
            f"{nombre}, cuéntame qué está pasando.",
            f"Aquí estoy.",
            f"Escucho eso, {nombre}.",
        ])

    def _emocional_positivo(self, c: ResultadoMotor) -> str:
        emocion = c.emocion_detectada
        nombre  = c.nombre_usuario

        if emocion == 'gratitud':
            return self._gratitud(c)
        if emocion == 'entusiasmo':
            return random.choice([
                f"Bien, {nombre}. Vamos.",
                f"Eso se siente bien. ¿Por dónde empezamos?",
                f"Me alegra. ¿Qué sigue?",
                f"Eso está bacano. ¿Qué hacemos ahora?",
            ])
        if emocion == 'alivio':
            return random.choice([
                f"Qué bien, {nombre}.",
                f"Por fin.",
                f"Eso se siente bien.",
                f"Menos mal.",
            ])

        return random.choice([
            f"Bien, {nombre}.",
            f"Me alegra.",
            f"Eso está bien.",
        ])

    def _logro(self, c: ResultadoMotor) -> str:
        """Sebastian compartió un logro."""
        nombre = c.nombre_usuario
        texto  = c.texto_original.lower()

        # Detectar qué logró
        if any(p in texto for p in ['funciona','funcionó','funciono','funcionando']):
            return random.choice([
                f"Por fin funciona, {nombre}.",
                f"Ahí está. Funcionando.",
                f"Eso se siente bien — cuando algo por fin funciona.",
            ])
        if any(p in texto for p in ['terminé','termine','terminé','acabé','acabé']):
            return random.choice([
                f"Lo terminaste. Bien, {nombre}.",
                f"Terminado. ¿Cómo quedó?",
                f"Bien hecho.",
            ])
        return random.choice([
            f"Lo lograste, {nombre}.",
            f"Bien. ¿Cómo te fue?",
            f"Ahí está. ¿Cómo resultó?",
        ])

    def _consejo(self, c: ResultadoMotor) -> str:
        """Sebastian pide consejo u opinión."""
        nombre = c.nombre_usuario
        # El contenido real del consejo lo da Groq con el contexto.
        # Bell señala que va a responder con honestidad.
        return random.choice([
            f"Te digo lo que pienso, {nombre}.",
            f"Desde donde lo veo: depende de qué es más importante para ti.",
            f"Honestamente, {nombre} — lo que yo haría es evaluar qué cuesta más: hacerlo o no hacerlo.",
            f"Mi perspectiva: lo más importante es qué pasa si no actúas.",
        ])

    def _queja(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        return random.choice([
            f"Eso cansa, {nombre}.",
            f"Entiendo la molestia.",
            f"Eso sí que desespera.",
            f"Sí — eso no debería ser tan complicado.",
        ])

    def _reflexion(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        return random.choice([
            f"Cuéntame, {nombre}.",
            f"¿Y qué estás pensando al respecto?",
            f"Eso vale la pena pensarlo. ¿A dónde te lleva?",
            f"Interesante. ¿Qué te hizo pensar en eso?",
        ])

    def _ayuda(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        return random.choice([
            f"Dime qué necesitas, {nombre}.",
            f"Aquí estoy. ¿Qué necesitas?",
            f"Dime.",
            f"Cuéntame. ¿En qué?",
        ])

    def _accion(self, c: ResultadoMotor) -> str:
        accion  = c.accion_principal
        objetos = c.objetos
        nombre  = c.nombre_usuario

        if accion and objetos:
            obj_str = objetos[0] if len(objetos) == 1 else ', '.join(objetos[:2])
            return f"Entendido — {accion} {obj_str}."
        if accion:
            return f"Entendido. {accion.capitalize()}."
        return random.choice([
            f"Recibido. En eso estoy, {nombre}.",
            f"Procesando lo que me pediste.",
        ])

    def _pregunta_general(self, c: ResultadoMotor) -> str:
        nombre  = c.nombre_usuario
        texto   = c.texto_original.lower()

        # Preguntas de conocimiento general → señal vacía para que Groq responda
        # (Groq tiene el conocimiento del mundo)
        indicadores_conocimiento = [
            'qué es', 'cómo funciona', 'cuál es', 'por qué',
            'qué significa', 'cuánto', 'cuándo', 'dónde',
            'quién inventó', 'para qué sirve',
        ]
        if any(ind in texto for ind in indicadores_conocimiento):
            return ''  # Groq responde con el conocimiento real

        return random.choice([
            f"Dime más, {nombre}. ¿Sobre qué exactamente?",
            f"Cuéntame un poco más.",
            f"Estoy aquí. ¿Sobre qué?",
        ])

    def _presencia(self, c: ResultadoMotor) -> str:
        """Conversacional puro — Bell está, no ejecuta."""
        nombre  = c.nombre_usuario
        modo    = c.modo_mental

        if modo == 'receptivo':
            return random.choice([
                f"Aquí estoy, {nombre}.",
                f"Presente.",
                f"Dime.",
                f"Estoy aquí.",
            ])
        if modo == 'reflexivo':
            return random.choice([
                f"Interesante, {nombre}.",
                f"Me quedo con eso.",
                f"Eso da para pensar.",
            ])
        return random.choice([
            f"Aquí estoy, {nombre}.",
            f"Presente.",
            f"Dime, {nombre}.",
        ])

    def _tecnica_sin_habilidad(self, c: ResultadoMotor) -> str:
        habilidad = c.habilidad_requerida
        mapa = {
            'BASE_DE_DATOS':       'trabajo con bases de datos',
            'CALCULO':             'cálculo matemático',
            'CODIGO_PYTHON':       'análisis de código',
            'SHELL':               'ejecución de comandos',
            'MATEMATICA_AVANZADA': 'matemática avanzada',
        }
        desc = mapa.get(habilidad or '', 'esa capacidad')
        return random.choice([
            f"Mi habilidad de {desc} está en construcción. Lo registré — cuando esté lista lo hago.",
            f"Todavía no tengo {desc} funcionando. Ya está en la lista.",
            f"{desc.capitalize()} viene. Lo guardé como pendiente.",
        ])

    def _ejecucion_exitosa(self, c: ResultadoMotor, ejec: dict) -> str:
        resultado  = ejec.get('resultado', '')
        habilidad  = ejec.get('habilidad_id', '')
        datos      = ejec.get('datos', {})

        if habilidad == 'CALCULO':
            expresion = datos.get('expresion', '')
            valor     = datos.get('valor_resultado', resultado)
            if expresion and valor:
                return random.choice([
                    f"{expresion} da {valor}.",
                    f"El resultado de {expresion} es {valor}.",
                    f"{expresion} = {valor}.",
                ])
            return f"El resultado es {valor}." if valor else resultado

        if habilidad == 'SQLITE':
            operacion = datos.get('operacion', '').lower()
            tabla     = datos.get('tabla', 'la tabla')
            if 'insert' in operacion or 'create' in operacion:
                return f"Listo, guardé lo que me pediste en {tabla}."
            if 'select' in operacion:
                registros = datos.get('registros', [])
                if not registros:
                    return f"Busqué en {tabla} y no hay registros que coincidan."
                return f"Encontré {len(registros)} registro(s) en {tabla}."
            return f"Operación completada en {tabla}."

        if resultado and len(resultado) < 300:
            return resultado
        return f"Listo. {resultado[:200]}{'...' if len(resultado) > 200 else ''}"

    def _ejecucion_fallida(self, c: ResultadoMotor, ejec: dict) -> str:
        error    = ejec.get('error', '')
        habilidad = ejec.get('habilidad_id', '')

        if 'no encontrado' in error.lower() or 'not found' in error.lower():
            return "No encontré lo que buscaba. Verifica que exista."
        if 'permiso' in error.lower() or 'permission' in error.lower():
            return "No tengo permiso para hacer eso."
        if 'pendiente' in error.lower():
            return "Esa capacidad todavía la estoy construyendo. Lo registré — cuando la tenga lo hago."
        return f"Algo falló: {error[:100]}. Puedo intentarlo diferente si me dices cómo."

    def _segura(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario if c else 'Sebastian'
        return f"Aquí estoy, {nombre}."

    # ══════════════════════════════════════════════════════════
    # PRESENCIAS EMOCIONALES
    # ══════════════════════════════════════════════════════════

    def _presente_frustracion(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        return random.choice([
            f"Eso frustra, {nombre}. Estoy aquí — dime qué está pasando.",
            f"Entiendo que está complicado. {nombre}, cuéntame qué no está funcionando.",
            f"Eso llega. Vamos paso a paso.",
            f"Escucho eso. Vamos juntos.",
            f"Sí, eso desespera. ¿Qué está fallando exactamente?",
        ])

    def _presente_cansancio(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        return random.choice([
            f"{nombre}, aquí estoy. Cuéntame qué necesitas — lo hago yo.",
            f"Descansa. Dime qué hay que hacer y lo tomo yo.",
            f"Escucho el cansancio. ¿Qué resuelvo primero?",
            f"Entiendo. Dime por dónde empezamos.",
            f"Dime qué hay que hacer. Tú descansa.",
        ])

    def _presente_ansiedad(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        return random.choice([
            f"{nombre}, respira. Estoy aquí. Dime qué está pasando.",
            f"Vamos despacio, {nombre}. Paso a paso.",
            f"Estoy con esto, {nombre}. Cuéntame.",
            f"{nombre}, lo tomamos de a uno.",
            f"Aquí estoy. No hay apuro.",
        ])

    def _presente_tristeza(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        return random.choice([
            f"{nombre}. Aquí estoy.",
            f"Escucho eso, {nombre}. Estoy presente.",
            f"{nombre}, cuéntame.",
            f"Estoy aquí, {nombre}. Sin apuro.",
            f"Aquí.",
        ])

    def _presente_rabia(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        return random.choice([
            f"Eso da rabia, {nombre}. Entiendo.",
            f"Sí — eso no debería pasar. Cuéntame.",
            f"Eso enoja, {nombre}. Estoy aquí.",
            f"Válido estar bravo con eso.",
        ])

    def _presente_soledad(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        return random.choice([
            f"Aquí estoy, {nombre}.",
            f"No estás solo, {nombre}.",
            f"Estoy presente.",
            f"{nombre}, cuéntame cómo estás.",
        ])

    def _presente_culpa(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        return random.choice([
            f"Equivocarse pasa, {nombre}. Lo importante es qué sigue.",
            f"No hay que cargarlo tan pesado, {nombre}.",
            f"Ya pasó. ¿Qué se puede hacer ahora?",
        ])

    def _presente_verguenza(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        return random.choice([
            f"Eso pasa, {nombre}. Nadie está libre de esos momentos.",
            f"No es para tanto, {nombre}. Ya se olvida.",
            f"Lo importante es seguir. Eso ya pasó.",
        ])

    def _presente_confusion(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        return random.choice([
            f"{nombre}, lo explico diferente.",
            f"Vamos de nuevo, {nombre}. Más claro esta vez.",
            f"Entendido, no quedó claro. Lo vuelvo a explicar.",
            f"{nombre}, ¿qué parte no quedó?",
        ])

    def _presente_generico(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        return random.choice([
            f"{nombre}, aquí estoy.",
            f"Estoy con esto, {nombre}.",
            f"{nombre}. Cuéntame.",
            f"Presente, {nombre}.",
        ])

    # ══════════════════════════════════════════════════════════
    # AUXILIARES
    # ══════════════════════════════════════════════════════════

    def _detectar_momento(self, texto: str) -> str:
        tl = texto.lower()
        if any(p in tl for p in ['buenos días', 'buen día', 'buen dia', 'mañana', 'manana']):
            return 'manana'
        if any(p in tl for p in ['buenas noches', 'buenas noche', 'noche']):
            return 'noche'
        if any(p in tl for p in ['buenas tardes', 'buenas tarde', 'tarde']):
            return 'tarde'
        return 'neutro'

    # ══════════════════════════════════════════════════════════
    # TRADUCCIÓN A INSTRUCCIONES PARA HABILIDADES
    # (se usa cuando Bell ejecuta algo técnico)
    # ══════════════════════════════════════════════════════════

    def traducir_a_instruccion(self, comprension: ResultadoMotor) -> dict:
        if not comprension.habilidad_requerida:
            return {}

        habilidad = comprension.habilidad_requerida
        params    = comprension.parametros_tecnicos
        instruccion = {
            'habilidad':       habilidad,
            'texto_original':  comprension.texto_original,
            'nivel_tecnicismo': comprension.nivel_tecnicismo,
        }

        if habilidad == 'SQLITE':
            instruccion.update(self._instruccion_sqlite(comprension, params))
        elif habilidad == 'CALCULO':
            instruccion.update(self._instruccion_calculo(comprension, params))
        elif habilidad == 'SHELL':
            instruccion.update(self._instruccion_shell(comprension, params))
        elif habilidad == 'ANALISIS_PYTHON':
            instruccion.update(self._instruccion_codigo(comprension, params))

        return instruccion

    def _instruccion_sqlite(self, c: ResultadoMotor, p: dict) -> dict:
        accion = c.accion_principal
        tabla  = p.get('nombre_tabla', 'datos')
        pares  = p.get('pares_clave_valor', {})
        if accion in ('crear', 'agregar') and pares:
            return {'operacion': 'create_and_insert', 'tabla': tabla, 'datos': pares}
        if accion == 'consultar':
            return {'operacion': 'select', 'tabla': tabla}
        if accion == 'modificar' and pares:
            return {'operacion': 'update', 'tabla': tabla, 'datos': pares}
        if accion == 'quitar':
            return {'operacion': 'delete', 'tabla': tabla}
        return {'operacion': 'select', 'tabla': tabla}

    def _instruccion_calculo(self, c: ResultadoMotor, p: dict) -> dict:
        return {
            'operacion': 'calcular',
            'expresion': p.get('expresion', c.texto_original),
            'valor':     p.get('valor'),
        }

    def _instruccion_shell(self, c: ResultadoMotor, p: dict) -> dict:
        return {
            'operacion':   'ejecutar',
            'comando':     c.texto_original,
            'directorio':  p.get('directorio', '.'),
        }

    def _instruccion_codigo(self, c: ResultadoMotor, p: dict) -> dict:
        return {
            'operacion':      'analizar',
            'codigo':         c.texto_original,
            'tipo_analisis':  c.accion_principal or 'general',
        }