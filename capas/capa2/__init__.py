# capas/capa2/__init__.py
# ================================================
# CAPA 2 — Activación neuronal + grounding 9D — v3
#
# v3:
# — Propagación directa de campos C1-v2
#   (contiene_codigo, motor_sugerido, complejidad,
#    es_pregunta, lenguaje_codigo)
# — Activación semántica dirigida según tipo de input
#   (código → nodos técnicos, emoción → nodos emocionales)
# — Logs diagnósticos completos con emoji por zona
# — Grounding promedio visible en consola
# — Detección de perfil de activación
# ================================================

from biblioteca import Biblioteca
from biblioteca.zona_desconocimiento.zona import ZonaDesconocimiento

_RED_VACIA = {
    'nodos_primarios':    [],
    'nodos_secundarios':  [],
    'nodos_terciarios':   [],
    'energia_total':      0.0,
    'nivel_conocimiento': 0.0,
    'tiene_conocimiento': False,
    'total_activados':    0,
}

# Nodos que reciben boost según el tipo de input
_BOOST_CODIGO = {
    'ENTIDAD_CODIGO', 'BELL_HABILIDAD', 'ACCION_EJECUTAR',
    'BELL_MOTOR', 'BELL_PIPELINE', 'ENTIDAD_ERROR',
    'ENTIDAD_FUNCION', 'ENTIDAD_CLASE', 'ENTIDAD_VARIABLE',
    'BELL_CAPA', 'ENTIDAD_API', 'ENTIDAD_SISTEMA',
}
_BOOST_EMOCIONAL = {
    'ESTADO_MAL', 'ESTADO_BIEN', 'ESTADO_TRISTE', 'ESTADO_FELIZ',
    'ESTADO_FRUSTRADO', 'ESTADO_CANSADO', 'ESTADO_PREOCUPADO',
    'ESTADO_EMOCIONADO', 'ESTADO_TRANQUILO', 'ESTADO_ABURRIDO',
    'NEURONA_SEBASTIAN',
}
_BOOST_BELL = {
    'BELL_NOMBRE_BELL', 'BELL_NOMBRE_BELLADONNA', 'BELL_CAPA',
    'BELL_CONSEJERA', 'BELL_MOTOR', 'BELL_HABILIDAD',
    'BELL_MEMORIA', 'BELL_GROUNDING', 'BELL_PIPELINE',
    'CONSEJERA_SAGE', 'CONSEJERA_VEGA', 'CONSEJERA_LYRA',
}


def procesar(paquete_capa1: dict) -> dict:
    try:
        return _procesar_interno(paquete_capa1)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            'exitoso':       False,
            'error':         f'Error en Capa 2: {str(e)}',
            'red_activa':    dict(_RED_VACIA),
            'paquete_capa1': paquete_capa1,
            # propagación mínima aunque falle
            'motor_sugerido':  paquete_capa1.get('motor_sugerido', 'local'),
            'contiene_codigo': paquete_capa1.get('contiene_codigo', False),
            'complejidad':     paquete_capa1.get('complejidad', 'simple'),
        }


def _procesar_interno(paquete_capa1: dict) -> dict:

    biblioteca = Biblioteca.obtener()

    # ── Extraer campos v2 de C1 para propagación ──────────
    contiene_codigo  = paquete_capa1.get('contiene_codigo', False)
    lenguaje_codigo  = paquete_capa1.get('lenguaje_codigo', 'ninguno')
    es_pregunta      = paquete_capa1.get('es_pregunta', False)
    complejidad      = paquete_capa1.get('complejidad', 'simple')
    motor_sugerido   = paquete_capa1.get('motor_sugerido', 'local')

    if not biblioteca.iniciada:
        print('  C2 ⚠️  Biblioteca no iniciada — paquete vacío')
        return {
            'exitoso':                False,
            'error':                  'Biblioteca neuronal no iniciada',
            'red_activa':             dict(_RED_VACIA),
            'nivel_conocimiento':     _nivel_vacio(),
            'conceptos_enriquecidos': [],
            'desconocidos_enviados':  0,
            'paquete_capa1':          paquete_capa1,
            'motor_sugerido':         motor_sugerido,
            'contiene_codigo':        contiene_codigo,
            'lenguaje_codigo':        lenguaje_codigo,
            'es_pregunta':            es_pregunta,
            'complejidad':            complejidad,
            'perfil_activacion':      'vacio',
        }

    conceptos    = paquete_capa1.get('conceptos', [])
    desconocidos = paquete_capa1.get('desconocidos', [])
    contexto_raw = paquete_capa1.get('contexto', {})
    texto        = paquete_capa1.get('contenido_original', '')

    # ── Normalizar conceptos a dict ────────────────────────
    conceptos_norm = _normalizar_conceptos(conceptos)

    # ── Boost semántico según tipo de input ───────────────
    conceptos_norm = _aplicar_boost_semantico(
        conceptos_norm, contiene_codigo, complejidad, texto
    )

    # ── Enriquecer con grounding 9D ───────────────────────
    conceptos_enriquecidos = _enriquecer_con_grounding(
        conceptos_norm, contexto_raw
    )

    # ── Activar la red neuronal ───────────────────────────
    red_activa = biblioteca.activar(conceptos_enriquecidos, texto)

    # Garantizar estructura completa
    if not isinstance(red_activa, dict):
        red_activa = red_activa.a_dict() if hasattr(red_activa, 'a_dict') else dict(_RED_VACIA)
    for campo, valor in _RED_VACIA.items():
        if campo not in red_activa:
            red_activa[campo] = valor

    # ── Registrar uso en grounding ─────────────────────────
    _registrar_uso_grounding(conceptos_norm, red_activa)

    # ── Enviar desconocidos a zona ─────────────────────────
    if desconocidos:
        _enviar_desconocidos(desconocidos)

    # ── Calcular métricas ─────────────────────────────────
    nivel_conocimiento = {
        'bell_conoce_esto':  red_activa.get('tiene_conocimiento', False),
        'profundidad':        red_activa.get('nivel_conocimiento', 0.0),
        'tiene_habilidades':  _verificar_habilidades(red_activa),
        'gaps_detectados':    _detectar_gaps(red_activa, desconocidos),
        'grounding_promedio': _calcular_grounding_promedio(conceptos_enriquecidos),
    }

    perfil = _calcular_perfil_activacion(
        contiene_codigo, complejidad, es_pregunta, red_activa
    )

    # ── Logs diagnósticos ─────────────────────────────────
    _log_diagnostico(
        conceptos_norm, conceptos_enriquecidos, red_activa,
        desconocidos, nivel_conocimiento, contiene_codigo,
        lenguaje_codigo, motor_sugerido, complejidad, perfil
    )

    return {
        'exitoso':                True,
        'red_activa':             red_activa,
        'nivel_conocimiento':     nivel_conocimiento,
        'conceptos_enriquecidos': conceptos_enriquecidos,
        'desconocidos_enviados':  len(desconocidos),
        'paquete_capa1':          paquete_capa1,
        # ── Campos C1-v2 propagados al nivel raíz ─────────
        'motor_sugerido':         motor_sugerido,
        'contiene_codigo':        contiene_codigo,
        'lenguaje_codigo':        lenguaje_codigo,
        'es_pregunta':            es_pregunta,
        'complejidad':            complejidad,
        'perfil_activacion':      perfil,
    }


# ══════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════

def _normalizar_conceptos(conceptos: list) -> list:
    norm = []
    for c in conceptos:
        if isinstance(c, dict):
            norm.append(c)
        else:
            norm.append({
                'id':        getattr(c, 'id', ''),
                'grounding': getattr(c, 'grounding', 0.5),
                'certeza':   getattr(c, 'certeza', 'directo'),
                'tipo':      getattr(c, 'tipo', 'concepto'),
                'texto_original': getattr(c, 'texto_original', ''),
            })
    return norm


def _aplicar_boost_semantico(
    conceptos: list,
    contiene_codigo: bool,
    complejidad: str,
    texto: str
) -> list:
    """
    Aumenta el grounding de nodos relevantes según el tipo
    de input. No inventa nodos — solo potencia los existentes.
    """
    if not conceptos:
        return conceptos

    # Detectar perfil emocional por texto
    texto_lower = texto.lower()
    hay_emocion = any(e in texto_lower for e in [
        'mal', 'bien', 'triste', 'feliz', 'cansado', 'frustrado',
        'preocupado', 'emocionado', 'tranquilo', 'aburrido',
        'siento', 'me siento', 'estoy', 'me da'
    ])
    habla_de_bell = any(b in texto_lower for b in [
        'bell', 'belladonna', 'capa', 'motor', 'habilidad',
        'consejera', 'grounding', 'pipeline'
    ])

    resultado = []
    for c in conceptos:
        c_nuevo = dict(c)
        cid = c.get('id', '')
        gb  = c.get('grounding', 0.5)

        if contiene_codigo and cid in _BOOST_CODIGO:
            c_nuevo['grounding'] = min(1.0, gb * 1.3)
            c_nuevo['boost_aplicado'] = 'codigo'
        elif hay_emocion and cid in _BOOST_EMOCIONAL:
            c_nuevo['grounding'] = min(1.0, gb * 1.2)
            c_nuevo['boost_aplicado'] = 'emocional'
        elif habla_de_bell and cid in _BOOST_BELL:
            c_nuevo['grounding'] = min(1.0, gb * 1.2)
            c_nuevo['boost_aplicado'] = 'bell_tech'
        elif complejidad == 'compleja':
            c_nuevo['grounding'] = min(1.0, gb * 1.1)
            c_nuevo['boost_aplicado'] = 'complejo'

        resultado.append(c_nuevo)
    return resultado


def _enriquecer_con_grounding(conceptos: list, contexto: dict) -> list:
    try:
        from biblioteca.grounding.calculador import CalculadorGrounding
        calc = CalculadorGrounding.obtener()
        enriquecidos = []
        for c in conceptos:
            cid  = c.get('id', '')
            tipo = c.get('tipo', 'concepto')
            gb   = c.get('grounding', 0.5)
            g9d  = calc.calcular(cid, tipo, contexto, gb)
            enriquecido = dict(c)
            enriquecido['grounding_9d']       = g9d.resumen()
            enriquecido['grounding_efectivo'] = g9d.efectivo()
            enriquecido['puede_ejecutar']     = g9d.puede_ejecutar()
            enriquecido['nivel_comprension']  = g9d.nivel_comprension()
            enriquecido['es_seguro']          = g9d.es_seguro()
            enriquecido['grounding']          = g9d.efectivo()
            enriquecidos.append(enriquecido)
        return enriquecidos
    except Exception as e:
        print(f'  C2 ⚠️  Grounding 9D no disponible ({e}), usando base')
        return conceptos


def _registrar_uso_grounding(conceptos: list, red_activa: dict):
    try:
        from biblioteca.grounding.calculador import CalculadorGrounding
        calc    = CalculadorGrounding.obtener()
        exitoso = red_activa.get('tiene_conocimiento', False)
        for c in conceptos:
            cid = c.get('id', '')
            if cid:
                calc.registrar_uso(cid, exitoso)
    except Exception:
        pass


def _enviar_desconocidos(desconocidos: list):
    try:
        zona = ZonaDesconocimiento.obtener()
        dicts = []
        for d in desconocidos:
            if isinstance(d, dict):
                dicts.append(d)
            else:
                dicts.append({
                    'fragmento':  getattr(d, 'fragmento', ''),
                    'tipo':       getattr(d, 'tipo', 'concepto'),
                    'inferencia': getattr(d, 'inferencia', None),
                })
        zona.agregar_desde_capa1(dicts)
    except Exception:
        pass


def _calcular_grounding_promedio(conceptos: list) -> float:
    if not conceptos:
        return 0.0
    vals = [c.get('grounding_efectivo', c.get('grounding', 0.5)) for c in conceptos]
    return round(sum(vals) / len(vals), 3)


def _verificar_habilidades(red_activa: dict) -> bool:
    todos = (red_activa.get('nodos_primarios', []) +
             red_activa.get('nodos_secundarios', []))
    return any(
        'HABILIDAD' in (n.get('nodo_id', '') if isinstance(n, dict) else str(n)).upper()
        for n in todos
    )


def _detectar_gaps(red_activa: dict, desconocidos: list) -> list:
    gaps = []
    for desc in desconocidos:
        frag = (desc.get('fragmento', '') if isinstance(desc, dict)
                else getattr(desc, 'fragmento', ''))
        if frag:
            gaps.append({'tipo': 'concepto', 'descripcion': frag, 'origen': 'capa1'})
    if not red_activa.get('nodos_primarios'):
        gaps.append({'tipo': 'conocimiento', 'descripcion': 'Sin activación primaria', 'origen': 'capa2'})
    return gaps


def _calcular_perfil_activacion(
    contiene_codigo: bool,
    complejidad: str,
    es_pregunta: bool,
    red_activa: dict
) -> str:
    """
    Clasifica el perfil del mensaje para que C3 y C6
    tomen mejores decisiones.
    """
    if contiene_codigo:
        return 'tecnico_codigo'
    if complejidad == 'compleja':
        return 'complejo'
    if es_pregunta:
        return 'pregunta'
    total = red_activa.get('total_activados', 0)
    if total == 0:
        return 'vacio'
    if total <= 3:
        return 'simple'
    return 'conversacional'


def _nivel_vacio() -> dict:
    return {
        'bell_conoce_esto':  False,
        'profundidad':        0.0,
        'tiene_habilidades':  False,
        'gaps_detectados':    [],
        'grounding_promedio': 0.0,
    }


# ══════════════════════════════════════════════════════════
# LOGS DIAGNÓSTICOS
# ══════════════════════════════════════════════════════════

def _log_diagnostico(
    conceptos_norm, conceptos_enriquecidos, red_activa,
    desconocidos, nivel_conocimiento,
    contiene_codigo, lenguaje_codigo,
    motor_sugerido, complejidad, perfil
):
    # Nodos primarios — IDs solamente
    nodos_p = red_activa.get('nodos_primarios', [])
    ids_p = [
        (n.get('nodo_id', str(n)) if isinstance(n, dict) else str(n))
        for n in nodos_p
    ]

    total    = red_activa.get('total_activados', 0)
    gp       = nivel_conocimiento.get('grounding_promedio', 0.0)
    conoce   = nivel_conocimiento.get('bell_conoce_esto', False)
    n_descon = len(desconocidos)

    # Icono de motor
    motor_icon = '🤖' if motor_sugerido == 'groq' else '⚡'

    print(f'  C2 nodos_primarios: {ids_p}')
    print(f'  C2 total_activados: {total}')
    print(f'  C2 grounding_avg:   {gp:.3f}')
    print(f'  C2 conoce_tema:     {conoce}')
    print(f'  C2 perfil:          {perfil}')
    print(f'  C2 complejidad:     {complejidad}')
    print(f'  C2 motor_hint:      {motor_icon} {motor_sugerido}')

    if contiene_codigo:
        print(f'  C2 🖥️  código detectado: {lenguaje_codigo}')

    # Boosts aplicados
    boosts = [
        c.get('boost_aplicado') for c in conceptos_enriquecidos
        if c.get('boost_aplicado')
    ]
    if boosts:
        from collections import Counter
        cnt = Counter(boosts)
        print(f'  C2 boosts: {dict(cnt)}')

    # Desconocidos
    if n_descon > 0:
        frags = [
            (d.get('fragmento', '') if isinstance(d, dict) else getattr(d, 'fragmento', ''))
            for d in desconocidos[:5]
        ]
        print(f'  C2 desconocidos→zona: {frags}{"..." if n_descon > 5 else ""}')

    # Gaps
    gaps = nivel_conocimiento.get('gaps_detectados', [])
    if gaps:
        print(f'  C2 gaps: {len(gaps)} detectados')