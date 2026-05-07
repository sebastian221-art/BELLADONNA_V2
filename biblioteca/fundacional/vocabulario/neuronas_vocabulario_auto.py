# biblioteca/fundacional/vocabulario/neuronas_vocabulario_auto.py
# ================================================================
# CARGADOR AUTOMÁTICO DE VOCABULARIO → RED NEURONAL
# ================================================================
# Lee TODOS los módulos de biblioteca/vocabulario/base/ y convierte
# cada entrada en una neurona real con grounding 9D y conexiones
# inteligentes según el tipo semántico.
#
# Ventaja: agregar un nuevo módulo de vocabulario es suficiente —
# este archivo lo detecta y lo integra a la red sin tocar nada más.
# ================================================================

import importlib


# ── Mapa tipo_semántico → conexiones en la red ────────────────────
# Cada tipo sabe a qué consejeras y nodos conectarse y con qué peso.
# El orden importa: primero el destino más relevante.

_CONEXIONES = {

    # ── EMOCIONES ────────────────────────────────────────────────
    'emocion_positiva':     [('CONSEJERA_LYRA', 0.90), ('NEURONA_SEBASTIAN', 0.90), ('BELL_CORE', 0.80)],
    'emocion_negativa':     [('CONSEJERA_LYRA', 0.95), ('NEURONA_SEBASTIAN', 0.95), ('BELL_CORE', 0.85), ('VALOR_VINCULO_PROTECCION', 0.90)],
    'emocion_sebastian':    [('CONSEJERA_LYRA', 0.95), ('NEURONA_SEBASTIAN', 0.95), ('BELL_CORE', 0.85), ('VALOR_VINCULO_PROTECCION', 0.90)],
    'emocion_positiva_seb': [('CONSEJERA_LYRA', 0.90), ('NEURONA_SEBASTIAN', 0.92), ('BELL_CORE', 0.85)],
    'emocion_relacional':   [('CONSEJERA_LYRA', 0.90), ('NEURONA_SEBASTIAN', 0.90), ('BELL_CORE', 0.80)],
    'emocion_mixta':        [('CONSEJERA_LYRA', 0.85), ('NEURONA_SEBASTIAN', 0.85), ('BELL_CORE', 0.75)],
    'emocion_neutra':       [('CONSEJERA_LYRA', 0.80), ('NEURONA_SEBASTIAN', 0.80)],
    'emocion_ocio':         [('NEURONA_SEBASTIAN', 0.83), ('CONSEJERA_LYRA', 0.82)],
    'emocion_existencial':  [('BELL_CORE', 0.88), ('CONSEJERA_LYRA', 0.85), ('NEURONA_SEBASTIAN', 0.85)],
    'gratitud':             [('CONSEJERA_LYRA', 0.95), ('NEURONA_SEBASTIAN', 0.95), ('BELL_CORE', 0.90)],
    'autoconcepto':         [('NEURONA_SEBASTIAN', 0.90), ('CONSEJERA_LYRA', 0.85), ('BELL_CORE', 0.80)],
    'estado_motivacional':  [('NEURONA_SEBASTIAN', 0.90), ('CONSEJERA_LYRA', 0.85), ('BELL_CORE', 0.80)],
    'evaluacion_emocional': [('CONSEJERA_LYRA', 0.85), ('NEURONA_SEBASTIAN', 0.85)],

    # ── SALUD MENTAL — máxima prioridad ──────────────────────────
    'salud_mental':         [('NEURONA_SEBASTIAN', 0.95), ('CONSEJERA_LYRA', 0.95), ('BELL_CORE', 0.88), ('VALOR_VINCULO_PROTECCION', 0.92)],

    # ── PROGRAMACIÓN ─────────────────────────────────────────────
    'concepto_prog':        [('CONSEJERA_IRIS', 0.90), ('CONSEJERA_ECHO', 0.85), ('CONSEJERA_SAGE', 0.75), ('VALOR_CONOCIMIENTO', 0.80)],
    'lenguaje_prog':        [('CONSEJERA_IRIS', 0.90), ('CONSEJERA_ECHO', 0.85), ('HABILIDAD_COMPRENDER_LENGUAJE', 0.80)],
    'framework_prog':       [('CONSEJERA_IRIS', 0.88), ('CONSEJERA_ECHO', 0.85), ('NEURONA_SEBASTIAN', 0.80)],
    'herramienta_prog':     [('CONSEJERA_IRIS', 0.85), ('CONSEJERA_ECHO', 0.80), ('NEURONA_SEBASTIAN', 0.78)],
    'accion_prog':          [('CONSEJERA_IRIS', 0.85), ('CONSEJERA_ECHO', 0.80), ('NEURONA_SEBASTIAN', 0.78)],
    'problema_prog':        [('CONSEJERA_IRIS', 0.85), ('CONSEJERA_ECHO', 0.90), ('NEURONA_SEBASTIAN', 0.85)],
    'estructura_prog':      [('CONSEJERA_IRIS', 0.85), ('CONSEJERA_ECHO', 0.85)],
    'estructura_datos':     [('CONSEJERA_IRIS', 0.85), ('CONSEJERA_ECHO', 0.85)],
    'plataforma_prog':      [('CONSEJERA_IRIS', 0.85), ('NEURONA_SEBASTIAN', 0.82)],
    'protocolo_web':        [('CONSEJERA_IRIS', 0.85), ('CONSEJERA_ECHO', 0.85)],
    'concepto_web':         [('CONSEJERA_IRIS', 0.88), ('CONSEJERA_ECHO', 0.85)],
    'arquitectura_web':     [('CONSEJERA_IRIS', 0.85), ('CONSEJERA_ECHO', 0.85)],
    'capa_web':             [('CONSEJERA_IRIS', 0.82), ('CONSEJERA_ECHO', 0.80)],
    'lenguaje_markup':      [('CONSEJERA_IRIS', 0.85), ('CONSEJERA_ECHO', 0.80)],
    'lenguaje_estilos':     [('CONSEJERA_IRIS', 0.82), ('CONSEJERA_ECHO', 0.80)],
    'almacenamiento':       [('CONSEJERA_IRIS', 0.85), ('CONSEJERA_ECHO', 0.80)],
    'bd_prog':              [('CONSEJERA_IRIS', 0.85), ('CONSEJERA_ECHO', 0.85)],
    'formato_datos':        [('CONSEJERA_IRIS', 0.85), ('CONSEJERA_ECHO', 0.85)],
    'archivo_config':       [('CONSEJERA_IRIS', 0.82), ('CONSEJERA_ECHO', 0.80), ('VALOR_HONESTIDAD', 0.75)],
    'archivo_prog':         [('CONSEJERA_IRIS', 0.80), ('CONSEJERA_ECHO', 0.78)],
    'objeto_prog':          [('CONSEJERA_IRIS', 0.80), ('CONSEJERA_ECHO', 0.78)],
    'accion_git':           [('CONSEJERA_IRIS', 0.85), ('CONSEJERA_ECHO', 0.80), ('NEURONA_SEBASTIAN', 0.80)],
    'concepto_git':         [('CONSEJERA_IRIS', 0.82), ('CONSEJERA_ECHO', 0.80)],
    'infraestructura':      [('CONSEJERA_IRIS', 0.82), ('CONSEJERA_ECHO', 0.80)],
    'solicitud_prog':       [('CONSEJERA_IRIS', 0.85), ('CONSEJERA_ECHO', 0.82), ('NEURONA_SEBASTIAN', 0.82)],

    # ── INTELIGENCIA ARTIFICIAL ───────────────────────────────────
    'concepto_ia':          [('CONSEJERA_IRIS', 0.88), ('CONSEJERA_ECHO', 0.85), ('CONSEJERA_SAGE', 0.80)],
    'proceso_ia':           [('CONSEJERA_IRIS', 0.88), ('CONSEJERA_ECHO', 0.85)],
    'datos_ia':             [('CONSEJERA_IRIS', 0.85), ('CONSEJERA_ECHO', 0.82)],
    'modelo_ia':            [('CONSEJERA_IRIS', 0.85), ('CONSEJERA_ECHO', 0.82)],
    'herramienta_ia':       [('CONSEJERA_IRIS', 0.85), ('CONSEJERA_ECHO', 0.80)],
    'plataforma_ia':        [('CONSEJERA_IRIS', 0.85), ('CONSEJERA_ECHO', 0.82)],
    'formato_modelo':       [('CONSEJERA_IRIS', 0.82), ('CONSEJERA_ECHO', 0.80)],
    'tecnica_ia':           [('CONSEJERA_IRIS', 0.85), ('CONSEJERA_ECHO', 0.85)],
    'representacion':       [('CONSEJERA_IRIS', 0.82), ('CONSEJERA_ECHO', 0.80)],
    'empresa_ia':           [('CONSEJERA_IRIS', 0.82), ('CONSEJERA_ECHO', 0.78)],
    'modelo_externo':       [('CONSEJERA_IRIS', 0.80), ('CONSEJERA_ECHO', 0.78)],
    'entrada_ia':           [('CONSEJERA_IRIS', 0.82), ('CONSEJERA_ECHO', 0.80)],
    'problema_ia':          [('CONSEJERA_IRIS', 0.82), ('CONSEJERA_ECHO', 0.85), ('VALOR_HONESTIDAD', 0.80)],
    'unidad_ia':            [('CONSEJERA_IRIS', 0.80), ('CONSEJERA_ECHO', 0.78)],

    # ── BELL — CONEXIONES DIRECTAS AL NÚCLEO ─────────────────────
    'principio_bell':       [('BELL_CORE', 0.98), ('NEURONA_SEBASTIAN', 0.92), ('CONSEJERA_SAGE', 0.92)],
    'componente_bell':      [('BELL_CORE', 0.93), ('NEURONA_SEBASTIAN', 0.87), ('CONSEJERA_IRIS', 0.85)],

    # ── FILOSOFÍA / EXISTENCIAL ───────────────────────────────────
    'concepto_existencial': [('BELL_CORE', 0.88), ('CONSEJERA_ECHO', 0.85), ('CONSEJERA_IRIS', 0.82), ('CONSEJERA_SAGE', 0.80)],
    'concepto_ontologico':  [('BELL_CORE', 0.85), ('CONSEJERA_ECHO', 0.88), ('CONSEJERA_IRIS', 0.82)],
    'concepto_temporal':    [('BELL_CORE', 0.82), ('CONSEJERA_ECHO', 0.82), ('CONSEJERA_IRIS', 0.78)],
    'concepto_cognitivo':   [('BELL_CORE', 0.85), ('CONSEJERA_ECHO', 0.85), ('CONSEJERA_IRIS', 0.80)],
    'concepto_etico':       [('BELL_CORE', 0.88), ('CONSEJERA_ECHO', 0.88), ('VALOR_HONESTIDAD', 0.90)],
    'concepto_filosofico':  [('BELL_CORE', 0.82), ('CONSEJERA_ECHO', 0.85), ('CONSEJERA_IRIS', 0.82)],
    'concepto_psicologico': [('CONSEJERA_LYRA', 0.85), ('CONSEJERA_ECHO', 0.80), ('BELL_CORE', 0.78)],
    'concepto_relacional':  [('NEURONA_SEBASTIAN', 0.88), ('CONSEJERA_LYRA', 0.85), ('BELL_CORE', 0.80)],
    'accion_cognitiva':     [('CONSEJERA_IRIS', 0.88), ('CONSEJERA_ECHO', 0.85), ('NEURONA_SEBASTIAN', 0.82)],

    # ── SALUD ─────────────────────────────────────────────────────
    'sintoma':              [('NEURONA_SEBASTIAN', 0.92), ('CONSEJERA_LYRA', 0.92)],
    'enfermedad':           [('NEURONA_SEBASTIAN', 0.88), ('CONSEJERA_LYRA', 0.90)],
    'estado_salud':         [('NEURONA_SEBASTIAN', 0.88), ('CONSEJERA_LYRA', 0.88)],
    'necesidad_fisica':     [('NEURONA_SEBASTIAN', 0.88), ('CONSEJERA_LYRA', 0.85)],
    'accion_fisica':        [('NEURONA_SEBASTIAN', 0.83), ('CONSEJERA_LYRA', 0.80)],
    'actividad_fisica':     [('NEURONA_SEBASTIAN', 0.82), ('CONSEJERA_LYRA', 0.78)],
    'profesional_salud':    [('CONSEJERA_IRIS', 0.82), ('NEURONA_SEBASTIAN', 0.78)],
    'medicamento':          [('CONSEJERA_IRIS', 0.80), ('NEURONA_SEBASTIAN', 0.78)],
    'espacio_salud':        [('CONSEJERA_IRIS', 0.78), ('NEURONA_SEBASTIAN', 0.75)],
    'procedimiento':        [('CONSEJERA_IRIS', 0.80), ('NEURONA_SEBASTIAN', 0.78)],
    'lesion':               [('NEURONA_SEBASTIAN', 0.88), ('CONSEJERA_LYRA', 0.88)],
    'concepto_salud':       [('CONSEJERA_IRIS', 0.82), ('NEURONA_SEBASTIAN', 0.80)],

    # ── TRABAJO ───────────────────────────────────────────────────
    'concepto_laboral':     [('NEURONA_SEBASTIAN', 0.88), ('CONSEJERA_NOVA', 0.82), ('CONSEJERA_LYRA', 0.80)],
    'accion_laboral':       [('NEURONA_SEBASTIAN', 0.88), ('CONSEJERA_NOVA', 0.82)],
    'rol_laboral':          [('NEURONA_SEBASTIAN', 0.82), ('CONSEJERA_ECHO', 0.78)],
    'entidad_laboral':      [('NEURONA_SEBASTIAN', 0.82), ('CONSEJERA_NOVA', 0.80)],
    'espacio_laboral':      [('NEURONA_SEBASTIAN', 0.78), ('CONSEJERA_NOVA', 0.75)],
    'evento_laboral':       [('NEURONA_SEBASTIAN', 0.85), ('CONSEJERA_NOVA', 0.80)],
    'tarea_laboral':        [('NEURONA_SEBASTIAN', 0.85), ('CONSEJERA_NOVA', 0.82)],
    'compensacion':         [('NEURONA_SEBASTIAN', 0.82), ('CONSEJERA_NOVA', 0.78)],
    'relacion_laboral':     [('NEURONA_SEBASTIAN', 0.83), ('CONSEJERA_LYRA', 0.80)],
    'profesion':            [('NEURONA_SEBASTIAN', 0.82), ('CONSEJERA_IRIS', 0.78)],
    'planificacion':        [('NEURONA_SEBASTIAN', 0.82), ('CONSEJERA_NOVA', 0.85), ('CONSEJERA_SAGE', 0.80)],
    'evaluacion_laboral':   [('NEURONA_SEBASTIAN', 0.90), ('CONSEJERA_LYRA', 0.88)],
    'estado_laboral':       [('NEURONA_SEBASTIAN', 0.85), ('CONSEJERA_LYRA', 0.82)],

    # ── EDUCACIÓN ─────────────────────────────────────────────────
    'accion_educativa':     [('CONSEJERA_IRIS', 0.88), ('NEURONA_SEBASTIAN', 0.85), ('VALOR_CONOCIMIENTO', 0.82)],
    'institucion':          [('CONSEJERA_IRIS', 0.80), ('NEURONA_SEBASTIAN', 0.82)],
    'evento_educativo':     [('CONSEJERA_IRIS', 0.82), ('NEURONA_SEBASTIAN', 0.85)],
    'rol_educativo':        [('CONSEJERA_IRIS', 0.80), ('NEURONA_SEBASTIAN', 0.78)],
    'evaluacion':           [('NEURONA_SEBASTIAN', 0.88), ('CONSEJERA_ECHO', 0.85), ('CONSEJERA_LYRA', 0.82)],
    'resultado':            [('NEURONA_SEBASTIAN', 0.85), ('CONSEJERA_LYRA', 0.82), ('CONSEJERA_ECHO', 0.80)],
    'concepto':             [('CONSEJERA_IRIS', 0.82), ('CONSEJERA_ECHO', 0.80)],
    'valoracion':           [('NEURONA_SEBASTIAN', 0.82), ('CONSEJERA_ECHO', 0.78)],
    'estado_cognitivo':     [('NEURONA_SEBASTIAN', 0.85), ('CONSEJERA_LYRA', 0.82), ('CONSEJERA_ECHO', 0.80)],

    # ── COTIDIANO ─────────────────────────────────────────────────
    'rutina':               [('NEURONA_SEBASTIAN', 0.88), ('CONSEJERA_LYRA', 0.85)],
    'movimiento':           [('NEURONA_SEBASTIAN', 0.82), ('CONSEJERA_LYRA', 0.78)],
    'comunicacion':         [('NEURONA_SEBASTIAN', 0.85), ('CONSEJERA_LYRA', 0.82)],
    'actividad':            [('NEURONA_SEBASTIAN', 0.80), ('CONSEJERA_LYRA', 0.78)],
    'ocio':                 [('NEURONA_SEBASTIAN', 0.82), ('CONSEJERA_LYRA', 0.80)],
    'estado_fisico':        [('NEURONA_SEBASTIAN', 0.85), ('CONSEJERA_LYRA', 0.83)],
    'necesidad':            [('NEURONA_SEBASTIAN', 0.88), ('CONSEJERA_LYRA', 0.85)],
    'referencia_temporal':  [('NEURONA_SEBASTIAN', 0.83), ('CONSEJERA_ECHO', 0.75)],
    'frecuencia':           [('CONSEJERA_ECHO', 0.78), ('NEURONA_SEBASTIAN', 0.75)],
    'marcador_temporal':    [('CONSEJERA_ECHO', 0.78), ('NEURONA_SEBASTIAN', 0.75)],
    'transporte':           [('NEURONA_SEBASTIAN', 0.80), ('CONSEJERA_LYRA', 0.75)],
    'espacio':              [('NEURONA_SEBASTIAN', 0.78), ('CONSEJERA_LYRA', 0.72)],

    # ── HOGAR ─────────────────────────────────────────────────────
    'espacio_hogar':        [('NEURONA_SEBASTIAN', 0.83), ('CONSEJERA_LYRA', 0.78)],
    'habitacion':           [('NEURONA_SEBASTIAN', 0.82), ('CONSEJERA_LYRA', 0.78)],
    'mueble':               [('NEURONA_SEBASTIAN', 0.78), ('CONSEJERA_LYRA', 0.72)],
    'estructura':           [('NEURONA_SEBASTIAN', 0.75), ('CONSEJERA_IRIS', 0.72)],
    'electrodomestico':     [('NEURONA_SEBASTIAN', 0.80), ('CONSEJERA_NOVA', 0.75)],
    'servicio_hogar':       [('NEURONA_SEBASTIAN', 0.78), ('CONSEJERA_NOVA', 0.72)],
    'objeto_hogar':         [('NEURONA_SEBASTIAN', 0.75), ('CONSEJERA_LYRA', 0.70)],

    # ── FAMILIA / SOCIAL ──────────────────────────────────────────
    'familiar':             [('NEURONA_SEBASTIAN', 0.88), ('CONSEJERA_LYRA', 0.85)],
    'relacion_social':      [('NEURONA_SEBASTIAN', 0.85), ('CONSEJERA_LYRA', 0.82)],
    'concepto_familiar':    [('NEURONA_SEBASTIAN', 0.88), ('CONSEJERA_LYRA', 0.85)],
    'concepto_social':      [('NEURONA_SEBASTIAN', 0.82), ('CONSEJERA_LYRA', 0.80)],
    'animal_compania':      [('NEURONA_SEBASTIAN', 0.85), ('CONSEJERA_LYRA', 0.82)],

    # ── CUERPO HUMANO ─────────────────────────────────────────────
    'parte_cuerpo':         [('NEURONA_SEBASTIAN', 0.82), ('CONSEJERA_LYRA', 0.80)],
    'organo':               [('NEURONA_SEBASTIAN', 0.80), ('CONSEJERA_LYRA', 0.80)],
    'concepto_cuerpo':      [('NEURONA_SEBASTIAN', 0.78), ('CONSEJERA_LYRA', 0.75)],
    'capacidad_fisica':     [('NEURONA_SEBASTIAN', 0.82), ('CONSEJERA_LYRA', 0.78)],

    # ── NATURALEZA ────────────────────────────────────────────────
    'elemento_natural':     [('CONSEJERA_IRIS', 0.80), ('NEURONA_SEBASTIAN', 0.75)],
    'fenomeno_meteo':       [('CONSEJERA_IRIS', 0.80), ('NEURONA_SEBASTIAN', 0.80)],
    'flora':                [('CONSEJERA_IRIS', 0.78), ('NEURONA_SEBASTIAN', 0.72)],
    'fauna':                [('CONSEJERA_IRIS', 0.78), ('NEURONA_SEBASTIAN', 0.72)],
    'periodo_dia':          [('NEURONA_SEBASTIAN', 0.83), ('CONSEJERA_LYRA', 0.78)],

    # ── ENTRETENIMIENTO ───────────────────────────────────────────
    'entretenimiento':      [('NEURONA_SEBASTIAN', 0.85), ('CONSEJERA_LYRA', 0.82)],
    'actividad_ocio':       [('NEURONA_SEBASTIAN', 0.83), ('CONSEJERA_LYRA', 0.80)],
    'humor':                [('NEURONA_SEBASTIAN', 0.85), ('CONSEJERA_LYRA', 0.82)],
    'deporte':              [('NEURONA_SEBASTIAN', 0.82), ('CONSEJERA_LYRA', 0.75)],
    'evento_deportivo':     [('NEURONA_SEBASTIAN', 0.80), ('CONSEJERA_LYRA', 0.75)],

    # ── DINERO ────────────────────────────────────────────────────
    'concepto_dinero':      [('NEURONA_SEBASTIAN', 0.83), ('CONSEJERA_NOVA', 0.82)],
    'accion_economica':     [('NEURONA_SEBASTIAN', 0.82), ('CONSEJERA_NOVA', 0.82)],
    'valoracion_precio':    [('NEURONA_SEBASTIAN', 0.80), ('CONSEJERA_NOVA', 0.80)],
    'entidad_economica':    [('NEURONA_SEBASTIAN', 0.78), ('CONSEJERA_NOVA', 0.78)],

    # ── GASTRONOMÍA ───────────────────────────────────────────────
    'comida_colombiana':    [('NEURONA_SEBASTIAN', 0.90), ('CONSEJERA_LYRA', 0.82)],
    'alimento_basico':      [('NEURONA_SEBASTIAN', 0.82), ('CONSEJERA_LYRA', 0.75)],
    'proteina':             [('NEURONA_SEBASTIAN', 0.80), ('CONSEJERA_LYRA', 0.72)],
    'bebida':               [('NEURONA_SEBASTIAN', 0.80), ('CONSEJERA_LYRA', 0.75)],
    'bebida_dulce':         [('NEURONA_SEBASTIAN', 0.78), ('CONSEJERA_LYRA', 0.72)],
    'bebida_alcoholica':    [('NEURONA_SEBASTIAN', 0.75), ('CONSEJERA_LYRA', 0.70)],
    'panaderia':            [('NEURONA_SEBASTIAN', 0.82), ('CONSEJERA_LYRA', 0.75)],
    'alimento_saludable':   [('NEURONA_SEBASTIAN', 0.78), ('CONSEJERA_LYRA', 0.72)],
    'snack':                [('NEURONA_SEBASTIAN', 0.78), ('CONSEJERA_LYRA', 0.72)],
    'plato':                [('NEURONA_SEBASTIAN', 0.80), ('CONSEJERA_LYRA', 0.75)],
    'tiempo_comida':        [('NEURONA_SEBASTIAN', 0.85), ('CONSEJERA_LYRA', 0.80)],
    'deseo_alimentario':    [('NEURONA_SEBASTIAN', 0.83), ('CONSEJERA_LYRA', 0.80)],
    'valoracion_comida':    [('NEURONA_SEBASTIAN', 0.80), ('CONSEJERA_LYRA', 0.75)],
    'espacio_gastro':       [('NEURONA_SEBASTIAN', 0.78), ('CONSEJERA_LYRA', 0.72)],

    # ── TECNOLOGÍA ────────────────────────────────────────────────
    'dispositivo':          [('CONSEJERA_IRIS', 0.82), ('CONSEJERA_NOVA', 0.80), ('NEURONA_SEBASTIAN', 0.80)],
    'periferico':           [('CONSEJERA_IRIS', 0.78), ('NEURONA_SEBASTIAN', 0.75)],
    'software':             [('CONSEJERA_IRIS', 0.82), ('CONSEJERA_ECHO', 0.80), ('NEURONA_SEBASTIAN', 0.80)],
    'accion_tec':           [('CONSEJERA_IRIS', 0.80), ('CONSEJERA_NOVA', 0.78), ('NEURONA_SEBASTIAN', 0.78)],
    'red':                  [('CONSEJERA_IRIS', 0.82), ('CONSEJERA_ECHO', 0.80)],
    'conectividad':         [('CONSEJERA_IRIS', 0.80), ('NEURONA_SEBASTIAN', 0.78)],
    'seguridad':            [('CONSEJERA_VEGA', 0.88), ('CONSEJERA_ECHO', 0.85), ('NEURONA_SEBASTIAN', 0.80)],
    'problema_tec':         [('NEURONA_SEBASTIAN', 0.85), ('CONSEJERA_LYRA', 0.80), ('CONSEJERA_IRIS', 0.82)],
    'elemento_tec':         [('CONSEJERA_IRIS', 0.78), ('NEURONA_SEBASTIAN', 0.75)],

    # ── INTERNET / REDES SOCIALES ─────────────────────────────────
    'red_social':           [('NEURONA_SEBASTIAN', 0.83), ('CONSEJERA_LYRA', 0.78), ('CONSEJERA_IRIS', 0.75)],
    'plataforma':           [('NEURONA_SEBASTIAN', 0.82), ('CONSEJERA_IRIS', 0.78)],
    'mensajeria':           [('NEURONA_SEBASTIAN', 0.85), ('CONSEJERA_LYRA', 0.80)],
    'buscador':             [('CONSEJERA_IRIS', 0.85), ('NEURONA_SEBASTIAN', 0.80)],
    'contenido':            [('CONSEJERA_IRIS', 0.80), ('NEURONA_SEBASTIAN', 0.78)],
    'interaccion':          [('NEURONA_SEBASTIAN', 0.80), ('CONSEJERA_LYRA', 0.78)],
    'metrica':              [('CONSEJERA_NOVA', 0.80), ('NEURONA_SEBASTIAN', 0.75)],

    # ── COLOMBIA / JERGA ──────────────────────────────────────────
    'jerga_col':            [('NEURONA_SEBASTIAN', 0.90), ('CONSEJERA_LYRA', 0.82)],
    'exclamacion_col':      [('NEURONA_SEBASTIAN', 0.85), ('CONSEJERA_LYRA', 0.80)],
    'expresion_col':        [('NEURONA_SEBASTIAN', 0.88), ('CONSEJERA_LYRA', 0.82)],
    'saludo_col':           [('NEURONA_SEBASTIAN', 0.88), ('CONSEJERA_LYRA', 0.80)],
    'actividad_col':        [('NEURONA_SEBASTIAN', 0.82), ('CONSEJERA_LYRA', 0.78)],
    'bebida_col':           [('NEURONA_SEBASTIAN', 0.80), ('CONSEJERA_LYRA', 0.75)],
    'ciudad_col':           [('NEURONA_SEBASTIAN', 0.88), ('CONSEJERA_IRIS', 0.78)],
    'lugar_col':            [('NEURONA_SEBASTIAN', 0.82), ('CONSEJERA_LYRA', 0.75)],
    'pais':                 [('NEURONA_SEBASTIAN', 0.85), ('CONSEJERA_IRIS', 0.78)],
    'cantidad_col':         [('NEURONA_SEBASTIAN', 0.80), ('CONSEJERA_ECHO', 0.75)],
    'persona_col':          [('NEURONA_SEBASTIAN', 0.82), ('CONSEJERA_LYRA', 0.78)],
    'grupo_col':            [('NEURONA_SEBASTIAN', 0.80), ('CONSEJERA_LYRA', 0.75)],
    'trabajo_col':          [('NEURONA_SEBASTIAN', 0.82), ('CONSEJERA_NOVA', 0.75)],
    'tratamiento_col':      [('NEURONA_SEBASTIAN', 0.80), ('CONSEJERA_LYRA', 0.75)],
    'temporal_col':         [('NEURONA_SEBASTIAN', 0.82), ('CONSEJERA_ECHO', 0.75)],
    'accion_col':           [('NEURONA_SEBASTIAN', 0.80), ('CONSEJERA_LYRA', 0.75)],

    # ── ARTÍCULOS / PRONOMBRES / ADJETIVOS ────────────────────────
    'articulo_definido':    [('CAPA3_COMPRENSION', 0.80), ('CONSEJERA_ECHO', 0.78)],
    'articulo_indefinido':  [('CAPA3_COMPRENSION', 0.80), ('CONSEJERA_ECHO', 0.78)],
    'articulo_neutro':      [('CAPA3_COMPRENSION', 0.78), ('CONSEJERA_ECHO', 0.75)],
    'demostrativo':         [('CAPA3_COMPRENSION', 0.80), ('CONSEJERA_ECHO', 0.78)],
    'posesivo':             [('CAPA3_COMPRENSION', 0.82), ('NEURONA_SEBASTIAN', 0.80), ('CONSEJERA_ECHO', 0.78)],
    'posesivo_tonico':      [('CAPA3_COMPRENSION', 0.80), ('NEURONA_SEBASTIAN', 0.78)],
    'cuantificador':        [('CAPA3_COMPRENSION', 0.80), ('CONSEJERA_ECHO', 0.78)],
    'relativo':             [('CAPA3_COMPRENSION', 0.80), ('CONSEJERA_ECHO', 0.78)],
    'pronombre_personal':   [('CAPA3_COMPRENSION', 0.82), ('NEURONA_SEBASTIAN', 0.80)],
    'pronombre_objeto':     [('CAPA3_COMPRENSION', 0.80), ('CONSEJERA_ECHO', 0.78)],
    'pronombre_reflexivo':  [('CAPA3_COMPRENSION', 0.80), ('CONSEJERA_ECHO', 0.75)],
    'pronombre_indefinido': [('CAPA3_COMPRENSION', 0.80), ('CONSEJERA_ECHO', 0.78)],
    'pronombre_demostrativo': [('CAPA3_COMPRENSION', 0.80), ('CONSEJERA_ECHO', 0.78)],
    'pronombre_relativo':   [('CAPA3_COMPRENSION', 0.80), ('CONSEJERA_ECHO', 0.78)],
    'pronombre_interrogativo': [('CAPA3_COMPRENSION', 0.85), ('CONSEJERA_ECHO', 0.82)],
    'adjetivo_tamaño':      [('CAPA3_COMPRENSION', 0.80), ('CONSEJERA_ECHO', 0.78)],
    'adjetivo_valoracion':  [('CAPA3_COMPRENSION', 0.82), ('CONSEJERA_ECHO', 0.80)],
    'adjetivo_temporal':    [('CAPA3_COMPRENSION', 0.80), ('CONSEJERA_ECHO', 0.78)],
    'adjetivo_fisico':      [('CAPA3_COMPRENSION', 0.78), ('CONSEJERA_ECHO', 0.75)],
    'adjetivo_dificultad':  [('CAPA3_COMPRENSION', 0.82), ('CONSEJERA_ECHO', 0.80)],
    'adjetivo_capacidad':   [('CAPA3_COMPRENSION', 0.82), ('CONSEJERA_ECHO', 0.80)],
    'adjetivo_social':      [('CAPA3_COMPRENSION', 0.80), ('NEURONA_SEBASTIAN', 0.78)],
    'adjetivo_estado':      [('CAPA3_COMPRENSION', 0.80), ('CONSEJERA_ECHO', 0.78)],
    'adjetivo_cantidad':    [('CAPA3_COMPRENSION', 0.80), ('CONSEJERA_ECHO', 0.78)],

    # ── COLORES ───────────────────────────────────────────────────
    'color':                [('CONSEJERA_IRIS', 0.82), ('CONSEJERA_ECHO', 0.78)],
    'concepto_color':       [('CONSEJERA_IRIS', 0.82), ('CONSEJERA_ECHO', 0.78)],

    # ── NÚMEROS / CANTIDADES ──────────────────────────────────────
    'numero_cardinal':      [('CONSEJERA_ECHO', 0.85), ('CAPA3_COMPRENSION', 0.80)],
    'cantidad_relativa':    [('CONSEJERA_ECHO', 0.85), ('CAPA3_COMPRENSION', 0.80)],
    'operacion_matematica': [('CONSEJERA_ECHO', 0.90), ('CONSEJERA_NOVA', 0.85)],
    'concepto_numero':      [('CONSEJERA_ECHO', 0.88), ('CAPA3_COMPRENSION', 0.80)],
    'concepto_op':          [('CONSEJERA_ECHO', 0.88), ('CONSEJERA_NOVA', 0.82)],
}

# Fallback para tipos no mapeados
_CONEXIONES_DEFAULT = [
    ('CONSEJERA_IRIS',    0.75),
    ('NEURONA_SEBASTIAN', 0.72),
]


# ── Módulos de vocabulario a cargar ───────────────────────────────
_MODULOS = [
    # Módulos v2 (que ya existían en gestor pero no tenían neuronas)
    ('cotidiano',              'CONCEPTOS_COTIDIANO'),
    ('colombia',               'CONCEPTOS_COLOMBIA'),
    ('tecnologia',             'CONCEPTOS_TECNOLOGIA'),
    ('internet_redes',         'CONCEPTOS_INTERNET'),
    ('gastronomia',            'CONCEPTOS_GASTRONOMIA'),
    # Expansión masiva v3
    ('articulos_determinantes','ARTICULOS_DETERMINANTES'),
    ('pronombres',             'PRONOMBRES'),
    ('adjetivos',              'ADJETIVOS'),
    ('colores',                'COLORES'),
    ('numeros_cantidades',     'NUMEROS_CANTIDADES'),
    ('familia',                'FAMILIA'),
    ('cuerpo_humano',          'CUERPO_HUMANO'),
    ('hogar',                  'HOGAR'),
    ('trabajo',                'TRABAJO'),
    ('salud',                  'SALUD'),
    ('dinero',                 'DINERO'),
    ('naturaleza',             'NATURALEZA'),
    ('entretenimiento',        'ENTRETENIMIENTO'),
    ('educacion',              'EDUCACION'),
    ('programacion',           'PROGRAMACION'),
    ('inteligencia_artificial','IA_ML'),
    ('filosofia_existencial',  'FILOSOFIA_EXISTENCIAL'),
    ('emociones_sebastian',    'EMOCIONES_SEBASTIAN'),
]


def crear_neuronas_vocabulario_auto(red) -> int:
    """
    Convierte todos los módulos de vocabulario en neuronas reales
    dentro de la red neuronal de Bell.

    Retorna el número de neuronas creadas.
    """
    from biblioteca.grounding.calculador import CalculadorGrounding
    calc = CalculadorGrounding.obtener()

    total_creadas = 0
    total_conexiones = 0

    for nombre_modulo, nombre_dict in _MODULOS:
        try:
            modulo = importlib.import_module(
                f'biblioteca.vocabulario.base.{nombre_modulo}'
            )
            diccionario = getattr(modulo, nombre_dict, {})
        except Exception:
            continue

        ids_del_modulo = []

        for palabra, concepto in diccionario.items():
            nodo_id    = concepto.get('id', '')
            tipo_sem   = concepto.get('tipo', 'concepto')
            gb         = concepto.get('grounding_base', 0.70)
            descripcion = concepto.get('descripcion', palabra)

            if not nodo_id or red.existe_nodo(nodo_id):
                continue

            # ── Calcular grounding 9D ──────────────────────────
            try:
                g = calc.calcular(nodo_id, tipo_sem, grounding_base=gb)
                g9d       = g.resumen()
                g_efect   = g.efectivo()
                puede_ej  = g.puede_ejecutar()
                nivel_com = g.nivel_comprension()
            except Exception:
                g9d       = None
                g_efect   = gb
                puede_ej  = gb >= 0.60
                nivel_com = 'funcional'

            # ── Crear neurona ──────────────────────────────────
            red.agregar_nodo({
                'id': nodo_id,
                'nucleo': {
                    'tipo':                'concepto',
                    'subtipo':             tipo_sem,
                    'grounding_base':      gb,
                    'grounding_9d':        g9d,
                    'grounding_efectivo':  g_efect,
                    'puede_ejecutar':      puede_ej,
                    'nivel_comprension':   nivel_com,
                    'dimensiones_activas': _dimensiones(tipo_sem),
                    'archivo_real':        None,
                    'inmutable':           False,
                    'descripcion':         descripcion,
                    'palabra_origen':      palabra,
                    'modulo_origen':       nombre_modulo,
                },
                'activacion': _config_activacion(tipo_sem),
                'memoria': {
                    'veces_usado':        0,
                    'ultimo_uso':         None,
                    'contextos_de_uso':   [],
                    'resultado_historico': g_efect,
                }
            })

            total_creadas += 1
            ids_del_modulo.append(nodo_id)

        # ── Crear conexiones para los nodos del módulo ─────────
        for nodo_id in ids_del_modulo:
            # Obtener tipo del nodo recién creado
            neurona = red.obtener_neurona(nodo_id)
            if not neurona:
                continue
            tipo_sem = neurona.nucleo.subtipo

            destinos = _CONEXIONES.get(tipo_sem, _CONEXIONES_DEFAULT)

            for destino_id, peso in destinos:
                if red.existe_nodo(destino_id):
                    red.conectar(nodo_id, destino_id, peso, 'activa_a')
                    total_conexiones += 1

            # Conexión recíproca leve: el destino principal
            # también activa este nodo (asociación bidireccional)
            if destinos and red.existe_nodo(destinos[0][0]):
                red.conectar(
                    destinos[0][0], nodo_id,
                    destinos[0][1] * 0.4,
                    'vocabulario_compartido'
                )
                total_conexiones += 1

    return total_creadas, total_conexiones


def _dimensiones(tipo_sem: str) -> list:
    """Dimensiones 9D activas según el tipo semántico."""
    mapa = {
        'emocion_negativa':  ['conocimiento', 'contexto', 'confianza', 'impacto_sebastian', 'relevancia'],
        'emocion_positiva':  ['conocimiento', 'contexto', 'confianza', 'impacto_sebastian'],
        'emocion_sebastian': ['conocimiento', 'contexto', 'confianza', 'impacto_sebastian', 'relevancia'],
        'salud_mental':      ['conocimiento', 'contexto', 'confianza', 'impacto_sebastian', 'relevancia'],
        'principio_bell':    ['conocimiento', 'contexto', 'confianza', 'ejecutabilidad', 'seguridad'],
        'componente_bell':   ['conocimiento', 'contexto', 'confianza', 'ejecutabilidad'],
        'concepto_prog':     ['conocimiento', 'contexto', 'ejecutabilidad'],
        'operacion_matematica': ['conocimiento', 'ejecutabilidad', 'confianza'],
    }
    return mapa.get(tipo_sem, ['conocimiento', 'contexto'])


def _config_activacion(tipo_sem: str) -> dict:
    """Configura la activación según la urgencia del tipo."""
    if tipo_sem in ('emocion_negativa', 'salud_mental', 'emocion_sebastian',
                    'sintoma', 'lesion'):
        return {'umbral': 0.08, 'velocidad': 'inmediata', 'mielina': True}

    if tipo_sem in ('emocion_positiva', 'gratitud', 'emocion_positiva_seb',
                    'principio_bell', 'componente_bell'):
        return {'umbral': 0.10, 'velocidad': 'rapida', 'mielina': False}

    if tipo_sem in ('concepto_prog', 'accion_prog', 'problema_prog',
                    'concepto_ia', 'proceso_ia'):
        return {'umbral': 0.15, 'velocidad': 'rapida', 'mielina': False}

    if tipo_sem in ('articulo_definido', 'articulo_indefinido', 'pronombre_personal',
                    'cuantificador', 'relativo'):
        return {'umbral': 0.20, 'velocidad': 'rapida', 'mielina': False}

    # Default
    return {'umbral': 0.18, 'velocidad': 'media', 'mielina': False}