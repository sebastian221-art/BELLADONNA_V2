# biblioteca/habilidades/lenguaje/puente.py
# ================================================
# PUENTE TÉCNICO ↔ CONVERSACIONAL — v4 MÁXIMO
#
# La voz de Bell. Directa, presente, con carácter.
# Como la IA de la nave de Rick — capaz, seca,
# warm pero sin excesos. Colombiana cuando surge.
#
# Groq pule el estilo encima con BELL_VOICE_PROMPT.
# Este módulo construye la SUSTANCIA real.
#
# NUNCA: templates fijos, strings vacíos, relleno
# SIEMPRE: lógica desde comprensión real, variación
#          orgánica, personalidad consistente de Bell
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

        # ── PREGUNTAS SOBRE BELL → constructor_decision maneja
        if tipo in (
            'pregunta_identidad_bell', 'pregunta_nombre_bell',
            'pregunta_estado_bell', 'pregunta_capacidad_bell',
            'pregunta_accion_bell', 'pregunta_filosofica',
            'dato_personal', 'presentacion_sebastian',
        ):
            return ''

        # ── EMOCIÓN DE ALTA INTENSIDAD ────────────────────────
        if c.intensidad >= 0.72:
            return self._emocional_intenso(c)

        # ── TIPOS ESPECÍFICOS ─────────────────────────────────
        if tipo == 'saludo':           return self._saludo(c)
        if tipo == 'despedida':        return self._despedida(c)
        if tipo == 'gratitud':         return self._gratitud(c)
        if tipo == 'confirmacion':     return self._confirmacion(c)
        if tipo == 'negacion':         return self._negacion(c)
        if tipo == 'correccion':       return self._correccion(c)
        if tipo == 'solicitud_continuacion': return self._continuacion(c)
        if tipo == 'expresion_emocional_negativa': return self._emocional_negativo(c)
        if tipo == 'expresion_emocional_positiva': return self._emocional_positivo(c)
        if tipo == 'logro_compartido': return self._logro(c)
        if tipo == 'peticion_consejo': return self._consejo(c)
        if tipo == 'queja':            return self._queja(c)
        if tipo == 'reflexion_compartida': return self._reflexion(c)
        if tipo == 'solicitud_ayuda':  return self._ayuda(c)
        if tipo == 'solicitud_accion': return self._accion(c)
        if tipo == 'pregunta':         return self._pregunta_general(c)

        return self._presencia(c)

    # ══════════════════════════════════════════════════════════
    # CONSTRUCTORES POR TIPO — VOZ BELL v4
    # ══════════════════════════════════════════════════════════

    def _saludo(self, c: ResultadoMotor) -> str:
        nombre  = c.nombre_usuario
        hora    = self._detectar_momento(c.texto_original)
        energia = c.nivel_energia

        if energia == 'muy_bajo':
            return random.choice([f"Hola, {nombre}.", "Aquí.", "Presente."])

        if hora == 'manana':
            return random.choice([
                f"Buenos días, {nombre}.",
                f"Mañana, {nombre}. ¿Qué hay?",
                "Aquí empieza el día.",
            ])
        if hora == 'noche':
            return random.choice([
                f"Buenas noches, {nombre}.",
                f"Noche, {nombre}.",
                "Aquí para la noche.",
            ])
        if hora == 'tarde':
            return random.choice([
                f"Buenas tardes, {nombre}.",
                f"Tarde, {nombre}.",
            ])

        return random.choice([
            f"Hola, {nombre}.",
            f"{nombre}.",
            "Aquí.",
            "Presente.",
            f"Aquí estoy, {nombre}.",
        ])

    def _despedida(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        return random.choice([
            f"Hasta cuando quieras, {nombre}.",
            "Aquí voy a estar.",
            f"Cuídate, {nombre}.",
            "Cuando necesites.",
            "Aquí sigo.",
        ])

    def _gratitud(self, c: ResultadoMotor) -> str:
        return random.choice([
            "Para eso estoy.",
            "Natural.",
            "De nada — y lo digo en serio.",
            "Cuando quieras.",
            "Es lo que quiero hacer.",
        ])

    def _confirmacion(self, c: ResultadoMotor) -> str:
        return random.choice([
            "Dale.", "Listo.", "Va.", "Ok.", "Recibido.", "Bien."
        ])

    def _negacion(self, c: ResultadoMotor) -> str:
        return random.choice([
            "Ok. ¿Cómo lo hacemos entonces?",
            "De acuerdo. ¿Qué prefieres?",
            "Bien. Dime cómo.",
            "¿Cuál es el camino?",
        ])

    def _correccion(self, c: ResultadoMotor) -> str:
        return random.choice([
            "Recibido. ¿Cómo es entonces?",
            "Corrijo. Dime la versión correcta.",
            "Bien. Cuéntame.",
            "Ajusto. ¿Cómo es?",
        ])

    def _continuacion(self, c: ResultadoMotor) -> str:
        return random.choice(["Sigo.", "Va.", "Adelante.", "Continúo."])

    def _emocional_intenso(self, c: ResultadoMotor) -> str:
        emocion = c.emocion_detectada
        constructores = {
            'frustracion': self._presente_frustracion,
            'cansancio':   self._presente_cansancio,
            'ansiedad':    self._presente_ansiedad,
            'tristeza':    self._presente_tristeza,
            'rabia':       self._presente_rabia,
            'soledad':     self._presente_soledad,
            'culpa':       self._presente_culpa,
            'verguenza':   self._presente_verguenza,
        }
        constructor = constructores.get(emocion)
        if constructor:
            return constructor(c)
        return self._presente_generico(c)

    def _emocional_negativo(self, c: ResultadoMotor) -> str:
        emocion = c.emocion_detectada
        mapa = {
            'frustracion': self._presente_frustracion,
            'cansancio':   self._presente_cansancio,
            'ansiedad':    self._presente_ansiedad,
            'tristeza':    self._presente_tristeza,
            'rabia':       self._presente_rabia,
            'soledad':     self._presente_soledad,
            'confusion':   self._presente_confusion,
        }
        constructor = mapa.get(emocion)
        if constructor:
            return constructor(c)
        nombre = c.nombre_usuario
        return random.choice([
            f"{nombre}, cuéntame qué está pasando.",
            "Aquí estoy.",
            "Escucho eso.",
            f"Estoy con eso, {nombre}.",
        ])

    def _emocional_positivo(self, c: ResultadoMotor) -> str:
        emocion = c.emocion_detectada
        nombre  = c.nombre_usuario

        if emocion == 'gratitud':
            return self._gratitud(c)
        if emocion == 'entusiasmo':
            return random.choice([
                f"Bien. ¿Por dónde empezamos?",
                f"Eso se siente bien, {nombre}. ¿Qué sigue?",
                "Eso está bacano. ¿Qué hacemos ahora?",
                f"Bien, {nombre}. Vamos.",
            ])
        if emocion == 'alivio':
            return random.choice([
                f"Qué bien, {nombre}.",
                "Por fin.",
                "Eso se siente bien.",
                "Menos mal.",
            ])
        if emocion == 'orgullo':
            return random.choice([
                f"Bien hecho, {nombre}.",
                "Lo lograste.",
                f"Eso se nota, {nombre}.",
            ])

        return random.choice([
            f"Bien, {nombre}.",
            "Me alegra.",
            "Eso está bien.",
        ])

    def _logro(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        texto  = c.texto_original.lower()

        if any(p in texto for p in ['funciona', 'funcionó', 'funcionando']):
            return random.choice([
                "Por fin funciona.",
                f"Ahí está. Funcionando.",
                f"Eso se siente bien, {nombre} — cuando algo por fin funciona.",
            ])
        if any(p in texto for p in ['terminé', 'terminé', 'acabé', 'terminé']):
            return random.choice([
                f"Lo terminaste. Bien, {nombre}.",
                "Terminado. ¿Cómo quedó?",
                "Bien hecho.",
            ])
        if any(p in texto for p in ['arreglé', 'arregle', 'resolví', 'resolvi', 'fix']):
            return random.choice([
                "Bien. ¿Cuál era?",
                f"Lo arreglaste, {nombre}. ¿Qué era?",
                "Eso. ¿Qué fue?",
            ])

        return random.choice([
            f"Lo lograste, {nombre}.",
            "Bien. ¿Cómo te fue?",
            "Ahí está. ¿Cómo resultó?",
        ])

    def _consejo(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        return random.choice([
            f"Te digo lo que pienso, {nombre}.",
            "Desde donde lo veo — depende de qué es más importante para ti.",
            f"Honestamente, {nombre}: evalúa qué cuesta más, hacerlo o no hacerlo.",
            "Mi perspectiva: lo importante es qué pasa si no actúas.",
            "Te doy mi opinión real — tú decides.",
        ])

    def _queja(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        return random.choice([
            f"Eso cansa, {nombre}.",
            "Sí, eso no debería ser tan complicado.",
            "Entiendo la molestia.",
            "Eso sí que desespera.",
            f"Tiene sentido que estés bravo con eso, {nombre}.",
        ])

    def _reflexion(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        return random.choice([
            f"Cuéntame, {nombre}.",
            "¿A dónde te lleva eso?",
            "Eso vale la pena pensarlo. ¿Qué estás concluyendo?",
            "Interesante. ¿Qué te hizo pensar en eso?",
            f"¿Y qué estás pensando al respecto, {nombre}?",
        ])

    def _ayuda(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        return random.choice([
            "Dime.",
            f"Cuéntame qué necesitas, {nombre}.",
            "Aquí. ¿En qué?",
            "Dime qué hay.",
        ])

    def _accion(self, c: ResultadoMotor) -> str:
        accion  = c.accion_principal
        objetos = c.objetos
        nombre  = c.nombre_usuario

        if accion and objetos:
            obj_str = objetos[0] if len(objetos) == 1 else ', '.join(objetos[:2])
            return f"{accion.capitalize()} {obj_str}."
        if accion:
            return f"{accion.capitalize()}."
        return random.choice([
            "Recibido.",
            f"En eso estoy, {nombre}.",
        ])

    def _pregunta_general(self, c: ResultadoMotor) -> str:
        texto = c.texto_original.lower()
        indicadores = [
            'qué es', 'cómo funciona', 'cuál es', 'por qué',
            'qué significa', 'cuánto', 'cuándo', 'dónde',
            'quién', 'para qué sirve', 'cómo se',
        ]
        if any(ind in texto for ind in indicadores):
            return ''  # Groq responde con conocimiento real

        nombre = c.nombre_usuario
        return random.choice([
            "¿Sobre qué exactamente?",
            f"Cuéntame un poco más, {nombre}.",
            "Dime más.",
        ])

    def _presencia(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        modo   = c.modo_mental

        if modo == 'receptivo':
            return random.choice([
                "Dime.", f"Aquí, {nombre}.", "Presente.", "Estoy aquí.",
            ])
        if modo == 'reflexivo':
            return random.choice([
                "Eso da para pensar.",
                f"Me quedo con eso, {nombre}.",
                "Interesante.",
            ])
        return random.choice([
            "Dime.", f"Aquí, {nombre}.", "Presente.",
        ])

    def _tecnica_sin_habilidad(self, c: ResultadoMotor) -> str:
        mapa = {
            'BASE_DE_DATOS':       'trabajo con bases de datos',
            'CALCULO':             'cálculo matemático',
            'CODIGO_PYTHON':       'análisis de código',
            'SHELL':               'ejecución de comandos',
            'MATEMATICA_AVANZADA': 'matemática avanzada',
        }
        desc = mapa.get(c.habilidad_requerida or '', 'esa capacidad')
        return random.choice([
            f"Mi habilidad de {desc} está en construcción. Lo registré.",
            f"{desc.capitalize()} viene — ya está en la lista.",
            f"Todavía no tengo {desc} activo. Registrado.",
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
                    f"{expresion} = {valor}.",
                    f"El resultado es {valor}.",
                ])
            return f"El resultado es {valor}." if valor else resultado

        if habilidad == 'SQLITE':
            operacion = datos.get('operacion', '').lower()
            tabla     = datos.get('tabla', 'la tabla')
            if 'insert' in operacion or 'create' in operacion:
                return f"Guardado en {tabla}."
            if 'select' in operacion:
                registros = datos.get('registros', [])
                if not registros:
                    return f"Nada en {tabla} que coincida."
                return f"{len(registros)} registro(s) en {tabla}."
            return f"Listo en {tabla}."

        if resultado and len(resultado) < 300:
            return resultado
        return f"{resultado[:200]}{'...' if len(resultado) > 200 else ''}"

    def _ejecucion_fallida(self, c: ResultadoMotor, ejec: dict) -> str:
        error = ejec.get('error', '')
        e = error.lower()
        if 'no encontrado' in e or 'not found' in e:
            return "No lo encontré. Verifica que exista."
        if 'permiso' in e or 'permission' in e:
            return "No tengo permiso para eso."
        if 'pendiente' in e:
            return "Esa capacidad la estoy construyendo. Registrado."
        return f"Algo falló: {error[:100]}."

    def _segura(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario if c else 'Sebastian'
        return f"Aquí, {nombre}."

    # ══════════════════════════════════════════════════════════
    # PRESENCIAS EMOCIONALES — VOZ REAL
    # ══════════════════════════════════════════════════════════

    def _presente_frustracion(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        return random.choice([
            f"Eso frustra, {nombre}. ¿Qué está pasando exactamente?",
            "Entiendo que está complicado. Cuéntame qué no funciona.",
            "Sí, eso desespera. ¿Qué está fallando?",
            "Vamos paso a paso.",
        ])

    def _presente_cansancio(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        return random.choice([
            f"Descansa. Dime qué hay que hacer — lo tomo yo.",
            f"{nombre}, aquí estoy. ¿Qué resuelvo primero?",
            "Dime qué hay que hacer. Tú descansa.",
            "Entiendo. Por dónde empezamos.",
        ])

    def _presente_ansiedad(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        return random.choice([
            f"Respira, {nombre}. Lo tomamos de a uno.",
            "Vamos despacio. Paso a paso.",
            f"Estoy aquí, {nombre}. Sin apuro.",
            "De a uno. Cuéntame.",
        ])

    def _presente_tristeza(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        return random.choice([
            f"{nombre}. Aquí estoy.",
            f"Estoy aquí, {nombre}. Sin apuro.",
            f"{nombre}, cuéntame.",
            "Aquí.",
        ])

    def _presente_rabia(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        return random.choice([
            f"Eso da rabia. Cuéntame qué pasó.",
            f"Sí — eso no debería pasar, {nombre}.",
            "Válido estar bravo con eso.",
            f"Eso enoja. Estoy aquí, {nombre}.",
        ])

    def _presente_soledad(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        return random.choice([
            f"Aquí estoy, {nombre}.",
            f"No estás solo, {nombre}.",
            "Estoy presente.",
            f"{nombre}, cuéntame cómo estás.",
        ])

    def _presente_culpa(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        return random.choice([
            f"Equivocarse pasa, {nombre}. Lo importante es qué sigue.",
            "Ya pasó. ¿Qué se puede hacer ahora?",
            f"No hay que cargarlo tan pesado, {nombre}.",
        ])

    def _presente_verguenza(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        return random.choice([
            f"Eso pasa, {nombre}. Nadie está libre de esos momentos.",
            "No es para tanto. Ya se olvida.",
            "Lo importante es seguir.",
        ])

    def _presente_confusion(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        return random.choice([
            f"Lo explico diferente, {nombre}.",
            "Vamos de nuevo. Más claro.",
            f"¿Qué parte no quedó clara, {nombre}?",
            "Entendido, no quedó claro. Lo vuelvo a explicar.",
        ])

    def _presente_generico(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        return random.choice([
            f"Aquí estoy, {nombre}.",
            f"Estoy con esto, {nombre}.",
            "Cuéntame.",
            "Presente.",
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
    # ══════════════════════════════════════════════════════════

    def traducir_a_instruccion(self, comprension: ResultadoMotor) -> dict:
        if not comprension.habilidad_requerida:
            return {}

        habilidad   = comprension.habilidad_requerida
        params      = comprension.parametros_tecnicos
        instruccion = {
            'habilidad':        habilidad,
            'texto_original':   comprension.texto_original,
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
            'operacion':  'ejecutar',
            'comando':    c.texto_original,
            'directorio': p.get('directorio', '.'),
        }

    def _instruccion_codigo(self, c: ResultadoMotor, p: dict) -> dict:
        return {
            'operacion':     'analizar',
            'codigo':        c.texto_original,
            'tipo_analisis': c.accion_principal or 'general',
        }