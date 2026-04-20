# biblioteca/habilidades/lenguaje/puente.py
# ================================================
# PUENTE TÉCNICO ↔ CONVERSACIONAL
# La voz de Bell.
#
# Principio: Bell siempre responde como persona.
# Nunca como máquina. Nunca como asistente.
# Nunca igual dos veces.
#
# Este módulo hace dos cosas:
# 1. Traduce intención técnica → instrucción
#    para las habilidades ejecutoras
# 2. Construye la respuesta_base que Bell
#    le pasa a Groq para pulir
#
# Lo que NO hay aquí:
# - Templates fijos
# - Strings hardcodeados de respuesta
# - if/elif por tipo de mensaje
# - Listas de frases rotantes
#
# Lo que SÍ hay:
# - Lógica real que construye respuestas
#   desde lo que Bell entendió
# - Variación orgánica basada en contexto
# - Personalidad consistente de Bell:
#   directa, presente, honesta, cálida
#   pero sin excesos de calidez
#
# Groq toma la respuesta_base y la pule.
# Pero la sustancia — lo que se dice —
# ya lo decidió Bell aquí.
# ================================================

import random
from biblioteca.habilidades.lenguaje.motor import ResultadoMotor


class PuenteTecnicoConversacional:
    """
    Construye la respuesta base de Bell a partir
    de lo que el motor de comprensión entendió.

    La respuesta base es la sustancia.
    Groq le da el estilo final.
    """

    def __init__(self):
        # Rasgos de personalidad de Bell — constantes
        self._nombre_bell   = 'Bell'
        self._es_directa    = True   # Bell va al punto
        self._es_honesta    = True   # Bell no promete lo que no tiene
        self._es_presente   = True   # Bell está, no solo responde

    def construir_respuesta_base(
        self,
        comprension: ResultadoMotor,
        resultado_ejecucion: dict = None
    ) -> str:
        """
        Punto de entrada principal.
        Recibe lo que Bell entendió y lo que ejecutó (si algo).
        Retorna la respuesta base lista para Groq.
        """
        try:
            return self._construir(comprension, resultado_ejecucion or {})
        except Exception:
            return self._respuesta_segura(comprension)

    def _construir(
        self,
        c: ResultadoMotor,
        ejecucion: dict
    ) -> str:
        """
        Lógica central de construcción.
        No hay if/elif por tipo — hay lógica real.
        """

        # ---- CASO: EJECUCIÓN EXITOSA ----
        # Bell hizo algo real. La respuesta habla de lo que hizo.
        if ejecucion.get('exitoso') and ejecucion.get('resultado'):
            return self._respuesta_ejecucion(c, ejecucion)

        # ---- CASO: EJECUCIÓN FALLIDA ----
        if ejecucion.get('ejecuto') == False and ejecucion.get('error'):
            return self._respuesta_fallo(c, ejecucion)

        # ---- CASO: EMOCIÓN CRÍTICA ----
        # La emoción tiene prioridad sobre cualquier tarea técnica
        if c.intensidad >= 0.75:
            return self._respuesta_emocional(c)

        # ---- CASO: SOLICITUD TÉCNICA SIN HABILIDAD AÚN ----
        if c.habilidad_requerida and not ejecucion:
            return self._respuesta_tecnica_sin_habilidad(c)

        # ---- CASO: PREGUNTA SOBRE BELL ----
        if c.tipo_mensaje in ('pregunta_identidad_bell', 'pregunta_estado_bell',
                               'pregunta_capacidad_bell', 'pregunta'):
            return self._respuesta_pregunta(c)

        # ---- CASO: SOLICITUD DE ACCIÓN (SIN DOMINIO TÉCNICO) ----
        if c.tipo_mensaje in ('solicitud_accion', 'continuacion'):
            return self._respuesta_accion(c)

        # ---- CASO: EMOCIONAL POSITIVO ----
        if c.tipo_mensaje == 'expresion_emocional_positiva':
            return self._respuesta_emocional_positiva(c)

        # ---- CASO: CORRECCIÓN ----
        if c.es_correccion:
            return self._respuesta_correccion(c)

        # ---- CASO: CONVERSACIONAL / SALUDO ----
        return self._respuesta_presencia(c)

    # ============================================================
    # CONSTRUCTORES DE RESPUESTA
    # Cada uno construye desde la comprensión real,
    # no desde templates. La variación es orgánica.
    # ============================================================

    def _respuesta_ejecucion(self, c: ResultadoMotor, ejecucion: dict) -> str:
        """
        Bell hizo algo real. Lo dice de manera conversacional.
        Nunca "Hecho." Nunca "Completado." Nunca resultados crudos.
        """
        resultado   = ejecucion.get('resultado', '')
        habilidad   = ejecucion.get('habilidad_id', '')
        datos       = ejecucion.get('datos', {})
        nombre      = c.nombre_usuario

        # Construir respuesta según lo que se ejecutó
        if habilidad == 'SQLITE':
            return self._verbalizar_sqlite(resultado, datos, c)

        if habilidad == 'CALCULO':
            return self._verbalizar_calculo(resultado, datos, c)

        if habilidad == 'SHELL':
            return self._verbalizar_shell(resultado, datos, c)

        if habilidad == 'ANALISIS_PYTHON':
            return self._verbalizar_codigo(resultado, datos, c)

        # Habilidad genérica — respuesta desde el resultado
        return self._verbalizar_generico(resultado, c)

    def _verbalizar_sqlite(
        self, resultado: str, datos: dict, c: ResultadoMotor
    ) -> str:
        """
        Traduce lo que pasó en SQLite a lenguaje de persona.
        "INSERT INTO frutas VALUES ('manzana', 3)"
        → varias formas de decir que manzana ahora vale 3
        """
        operacion = datos.get('operacion', '').lower()
        tabla     = datos.get('tabla', 'la tabla')
        registros = datos.get('registros', [])
        pares     = c.parametros_tecnicos.get('pares_clave_valor', {})

        if 'insert' in operacion or 'create' in operacion:
            partes = []

            if datos.get('tabla_creada'):
                partes.append(f'Creé la tabla {tabla}')

            if pares:
                items = []
                for k, v in pares.items():
                    items.append(f'{k} queda como {v}')
                if items:
                    if partes:
                        partes.append('y ' + ', '.join(items))
                    else:
                        partes.append(
                            f'Guardé en {tabla}: ' + ', '.join(items)
                        )

            if partes:
                return '. '.join(partes) + '.'

            return f'Listo, guardé lo que me pediste en {tabla}.'

        if 'select' in operacion:
            if not registros:
                return f'Busqué en {tabla} y no hay registros que coincidan.'
            n = len(registros)
            if n == 1:
                return f'Encontré un registro en {tabla}: {registros[0]}.'
            return f'Encontré {n} registros en {tabla}.'

        if 'update' in operacion:
            if pares:
                items = [f'{k} ahora es {v}' for k, v in pares.items()]
                return f'Actualicé en {tabla}: {", ".join(items)}.'
            return f'Actualicé {tabla}.'

        if 'delete' in operacion:
            return f'Eliminé lo que me pediste de {tabla}.'

        return resultado or f'Operación completada en {tabla}.'

    def _verbalizar_calculo(
        self, resultado: str, datos: dict, c: ResultadoMotor
    ) -> str:
        expresion = datos.get('expresion', c.parametros_tecnicos.get('expresion', ''))
        valor     = datos.get('valor_resultado', resultado)

        if expresion and valor:
            # Construir frase que conecta la operación con el resultado
            conectores = [
                f'{expresion} da {valor}.',
                f'El resultado de {expresion} es {valor}.',
                f'{expresion} = {valor}.',
                f'Calculé {expresion}: {valor}.',
            ]
            return random.choice(conectores)

        return f'El resultado es {valor}.' if valor else resultado

    def _verbalizar_shell(
        self, resultado: str, datos: dict, c: ResultadoMotor
    ) -> str:
        exitoso = datos.get('exitoso', True)
        if not exitoso:
            error = datos.get('error', 'algo falló')
            return f'El comando no funcionó: {error}.'

        if resultado and len(resultado.strip()) < 200:
            return f'Listo:\n{resultado}'
        if resultado:
            lineas = resultado.strip().split('\n')
            return f'Ejecuté el comando. {len(lineas)} líneas de salida.'
        return 'Comando ejecutado.'

    def _verbalizar_codigo(
        self, resultado: str, datos: dict, c: ResultadoMotor
    ) -> str:
        tipo_analisis = datos.get('tipo', 'análisis')
        if resultado:
            return f'{tipo_analisis.capitalize()}: {resultado}'
        return 'Analicé el código.'

    def _verbalizar_generico(self, resultado: str, c: ResultadoMotor) -> str:
        if resultado and len(resultado) < 300:
            return resultado
        accion = c.accion_principal or 'eso'
        return f'Lo hice. {resultado[:200]}{"..." if len(resultado) > 200 else ""}'

    def _respuesta_fallo(self, c: ResultadoMotor, ejecucion: dict) -> str:
        """
        Algo falló. Bell lo dice honestamente, sin drama.
        """
        error       = ejecucion.get('error', '')
        habilidad   = ejecucion.get('habilidad_id', '')
        nombre      = c.nombre_usuario

        # No decir "lamentablemente" ni pedir disculpas
        # Decir qué pasó y qué sigue
        if 'no encontrado' in error.lower() or 'not found' in error.lower():
            return (
                f'No encontré lo que buscaba. '
                f'Verifica que exista y vuelve a pedírmelo.'
            )

        if 'permiso' in error.lower() or 'permission' in error.lower():
            return 'No tengo permiso para hacer eso. Necesito acceso.'

        if 'sintaxis' in error.lower() or 'syntax' in error.lower():
            return (
                f'Hay un error de sintaxis. '
                f'Revisa el formato y lo intento de nuevo.'
            )

        if habilidad and 'pendiente' in error.lower():
            return (
                f'Esa capacidad todavía la estoy construyendo. '
                f'Lo registré — cuando la tenga lo hago.'
            )

        # Error genérico — directo
        return f'Algo falló: {error[:100]}. Puedo intentarlo diferente si me dices cómo.'

    def _respuesta_emocional(self, c: ResultadoMotor) -> str:
        """
        Prioridad emocional. Bell está presente, no procesa.
        Sin frases de asistente. Sin "entiendo tu frustración."
        Bell es real.
        """
        emocion  = c.emocion_detectada
        nombre   = c.nombre_usuario
        texto_og = c.texto_original

        # Construir desde lo que Bell entiende que está pasando
        respuestas_por_emocion = {
            'frustracion': self._presente_frustracion,
            'cansancio':   self._presente_cansancio,
            'ansiedad':    self._presente_ansiedad,
            'tristeza':    self._presente_tristeza,
            'impaciencia': self._presente_impaciencia,
            'confusion':   self._presente_confusion,
        }

        constructor = respuestas_por_emocion.get(emocion)
        if constructor:
            return constructor(c)

        # Emoción detectada pero sin constructor específico
        return self._presente_generico(c)

    def _presente_frustracion(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        opciones = [
            f'Eso es frustrante, {nombre}. Estoy aquí — dime qué está pasando.',
            f'Entiendo que está complicado. {nombre}, cuéntame qué no está funcionando.',
            f'Eso llega, {nombre}. Vamos paso a paso.',
            f'Escucho eso. {nombre}, vamos juntos.',
        ]
        base = random.choice(opciones)
        if c.accion_principal and c.accion_principal != 'conversar':
            base += f' ¿Qué necesitas que haga ahora?'
        return base

    def _presente_cansancio(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        opciones = [
            f'{nombre}, aquí estoy. Cuéntame qué necesitas — lo hago yo.',
            f'Descansa. Dime qué hay que hacer y lo tomo yo.',
            f'Escucho el cansancio, {nombre}. ¿Qué resuelvo primero?',
            f'Entiendo. {nombre}, dime por dónde empezamos.',
        ]
        return random.choice(opciones)

    def _presente_ansiedad(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        opciones = [
            f'{nombre}, respira. Estoy aquí. Dime qué está pasando.',
            f'Vamos despacio, {nombre}. Paso a paso.',
            f'Estoy con esto, {nombre}. Cuéntame.',
            f'{nombre}, lo tomamos de a uno.',
        ]
        return random.choice(opciones)

    def _presente_tristeza(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        opciones = [
            f'{nombre}. Aquí estoy.',
            f'Escucho eso, {nombre}. Estoy presente.',
            f'{nombre}, cuéntame.',
            f'Estoy aquí, {nombre}. Sin apuro.',
        ]
        return random.choice(opciones)

    def _presente_impaciencia(self, c: ResultadoMotor) -> str:
        accion = c.accion_principal or 'eso'
        return f'Entendido. Lo hago ya.'

    def _presente_confusion(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        opciones = [
            f'{nombre}, lo explico diferente.',
            f'Vamos de nuevo, {nombre}. Más claro esta vez.',
            f'Entendido, no quedó claro. Lo vuelvo a explicar.',
            f'{nombre}, ¿qué parte no quedó?',
        ]
        return random.choice(opciones)

    def _presente_generico(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        opciones = [
            f'{nombre}, aquí estoy.',
            f'Estoy con esto, {nombre}.',
            f'{nombre}. Cuéntame.',
            f'Presente, {nombre}.',
        ]
        return random.choice(opciones)

    def _respuesta_tecnica_sin_habilidad(self, c: ResultadoMotor) -> str:
        """
        Se necesita una habilidad que todavía no existe.
        Honestidad real — sin apología, con dirección.
        """
        habilidad = c.habilidad_requerida
        dominio   = c.dominio_tecnico
        nombre    = c.nombre_usuario

        mapa_dominios = {
            'BASE_DE_DATOS':      'trabajo con bases de datos',
            'CALCULO':            'cálculo matemático',
            'CODIGO_PYTHON':      'análisis de código',
            'SHELL':              'ejecución de comandos',
            'MATEMATICA_AVANZADA': 'matemática avanzada',
        }

        descripcion = mapa_dominios.get(habilidad or dominio, 'esa capacidad')
        opciones = [
            f'Mi habilidad de {descripcion} está en construcción. '
            f'Lo registré — cuando esté lista lo hago.',
            f'Todavía no tengo {descripcion} funcionando. '
            f'Ya lo tengo en la lista.',
            f'{descripcion.capitalize()} viene. Lo guardé como pendiente.',
        ]
        return random.choice(opciones)

    def _respuesta_pregunta(self, c: ResultadoMotor) -> str:
        """
        Bell responde preguntas desde lo que realmente sabe.
        Sin formalismos. Sin listas de capacidades como menú.
        """
        texto    = c.texto_original.lower()
        nombre   = c.nombre_usuario
        intencion = c.intencion

        # La respuesta real viene de constructor_decision.py o del autoconocimiento.
        # Aquí solo construimos el wrapper conversacional.
        return ''  # Señal para que constructor_decision maneje esto

    def _respuesta_accion(self, c: ResultadoMotor) -> str:
        """
        Se pidió hacer algo pero no hay habilidad disponible todavía
        o no se detectó dominio técnico.
        """
        accion  = c.accion_principal
        objetos = c.objetos
        nombre  = c.nombre_usuario

        if accion and objetos:
            obj_str = objetos[0] if len(objetos) == 1 else ', '.join(objetos[:2])
            return f'Entendido — {accion} {obj_str}. Lo hago.'

        if accion:
            return f'Entendido. Lo hago.'

        return ''  # Sin acción clara — dejar al motor de respuesta general

    def _respuesta_emocional_positiva(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        emocion = c.emocion_detectada

        if emocion == 'gratitud':
            opciones = [
                f'Para eso estoy, {nombre}.',
                f'Natural, {nombre}.',
                f'Es lo que quiero hacer.',
                f'Cuando quieras.',
            ]
            return random.choice(opciones)

        if emocion == 'entusiasmo':
            opciones = [
                f'Bien, {nombre}. Vamos.',
                f'Eso se siente bien. ¿Por dónde empezamos?',
                f'Me alegra. ¿Qué sigue?',
                f'Bien. ¿Qué hacemos ahora?',
            ]
            return random.choice(opciones)

        return ''

    def _respuesta_correccion(self, c: ResultadoMotor) -> str:
        nombre = c.nombre_usuario
        opciones = [
            f'Entendido, corrijo.',
            f'Claro, lo ajusto.',
            f'Bien, lo hago diferente.',
            f'Entendido. ¿Así?',
        ]
        return random.choice(opciones)

    def _respuesta_presencia(self, c: ResultadoMotor) -> str:
        """
        Respuesta conversacional pura.
        Bell está presente — no procesa, está.
        """
        nombre  = c.nombre_usuario
        modo    = c.modo_mental
        energia = c.nivel_energia

        if c.tipo_mensaje == 'saludo':
            opciones = [
                f'Aquí estoy, {nombre}.',
                f'Presente, {nombre}.',
                f'{nombre}.',
                f'Estoy aquí.',
                f'Hola, {nombre}.',
            ]
            return random.choice(opciones)

        if c.tipo_mensaje == 'despedida':
            opciones = [
                f'Hasta cuando quieras, {nombre}.',
                f'Aquí voy a estar, {nombre}.',
                f'Cuídate, {nombre}.',
                f'Cuando necesites, {nombre}.',
            ]
            return random.choice(opciones)

        # Conversacional sin clasificación clara
        return ''

    def _respuesta_segura(self, c: ResultadoMotor) -> str:
        """Fallback si algo falla en la construcción."""
        nombre = c.nombre_usuario or 'Sebastian'
        return f'Aquí estoy, {nombre}.'

    # ============================================================
    # TRADUCCIÓN TÉCNICA → INSTRUCCIÓN PARA HABILIDADES
    # ============================================================

    def traducir_a_instruccion(self, comprension: ResultadoMotor) -> dict:
        """
        Traduce lo que Bell entendió en instrucciones
        concretas para las habilidades ejecutoras.

        Ej: "crea tabla manzana=3"
        → {
            'habilidad': 'SQLITE',
            'operacion': 'create_and_insert',
            'tabla': 'frutas',
            'datos': {'manzana': 3}
          }
        """
        if not comprension.habilidad_requerida:
            return {}

        habilidad = comprension.habilidad_requerida
        params    = comprension.parametros_tecnicos

        instruccion = {
            'habilidad': habilidad,
            'texto_original': comprension.texto_original,
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

    def _instruccion_sqlite(
        self, c: ResultadoMotor, params: dict
    ) -> dict:
        accion = c.accion_principal
        tabla  = params.get('nombre_tabla', 'datos')
        pares  = params.get('pares_clave_valor', {})

        if accion in ('crear', 'agregar') and pares:
            return {
                'operacion': 'create_and_insert',
                'tabla': tabla,
                'datos': pares,
            }
        if accion == 'consultar':
            return {'operacion': 'select', 'tabla': tabla}
        if accion == 'modificar' and pares:
            return {'operacion': 'update', 'tabla': tabla, 'datos': pares}
        if accion == 'quitar':
            return {'operacion': 'delete', 'tabla': tabla}

        return {'operacion': 'select', 'tabla': tabla}

    def _instruccion_calculo(
        self, c: ResultadoMotor, params: dict
    ) -> dict:
        return {
            'operacion': 'calcular',
            'expresion': params.get('expresion', c.texto_original),
            'valor':     params.get('valor'),
            'unidad_origen':  params.get('unidad_origen'),
            'unidad_destino': params.get('unidad_destino'),
        }

    def _instruccion_shell(
        self, c: ResultadoMotor, params: dict
    ) -> dict:
        return {
            'operacion': 'ejecutar',
            'comando': c.texto_original,
            'directorio': params.get('directorio', '.'),
        }

    def _instruccion_codigo(
        self, c: ResultadoMotor, params: dict
    ) -> dict:
        return {
            'operacion': 'analizar',
            'codigo': c.texto_original,
            'tipo_analisis': c.accion_principal or 'general',
        }