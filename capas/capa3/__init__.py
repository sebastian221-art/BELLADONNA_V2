# capas/capa3/__init__.py
# ================================================
# CAPA 3 — COMPRENSIÓN PROFUNDA — v2
#
# v2: Groq gpt-oss-120b como primer clasificador
# semántico. Si falla → MotorComprension → patrones.
#
# Pipeline de clasificación:
#   1. Groq (0.5s, semántico, preciso)
#   2. MotorComprension / spaCy (fallback)
#   3. Keyword patterns (siempre funciona)
#
# Logs diagnósticos completos.
# Propagación de campos C1/C2.
# ================================================

from capas.capa3.paquete_capa3        import PaqueteCapa3
from capas.capa3.constructor_comprension import ConstructorComprension
from capas.capa3.detector_ambiguedad  import DetectorAmbiguedad
from capas.capa3.detector_gaps        import DetectorGaps
from capas.capa3.consejeras.lyra_capa3 import LyraCapa3
from capas.capa3.consejeras.echo_capa3 import EchoCapa3
from capas.capa3.clasificador_bell    import obtener as obtener_clasificador

_constructor  = ConstructorComprension()
_ambiguedad   = DetectorAmbiguedad()
_gaps         = DetectorGaps()
_lyra         = LyraCapa3()
_echo         = EchoCapa3()
_clasificador = None  # lazy init — evita error si GROQ_API_KEY no está al arrancar


def _get_clasificador():
    global _clasificador
    if _clasificador is None:
        _clasificador = obtener_clasificador()
    return _clasificador


def procesar(paquete_capa2: dict) -> dict:
    try:
        return _procesar_interno(paquete_capa2)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            'exitoso':       False,
            'error':         f'Error en Capa 3: {str(e)}',
            'comprension':   {},
            'paquete_capa2': paquete_capa2,
            # propagación mínima
            'motor_sugerido':  paquete_capa2.get('motor_sugerido', 'local'),
            'contiene_codigo': paquete_capa2.get('contiene_codigo', False),
            'complejidad':     paquete_capa2.get('complejidad', 'simple'),
        }


def _procesar_interno(paquete_capa2: dict) -> dict:

    # ── Extraer datos necesarios ──────────────────────────
    red_activa     = paquete_capa2.get('red_activa', {})
    paquete_c1     = paquete_capa2.get('paquete_capa1', {})
    texto_original = paquete_c1.get('contenido_original', '')
    contexto       = paquete_c1.get('contexto', {})
    tono           = paquete_c1.get('tono_detectado', 'neutral')

    # ── Campos propagados de C1/C2 ────────────────────────
    motor_sugerido    = paquete_capa2.get('motor_sugerido', 'local')
    contiene_codigo   = paquete_capa2.get('contiene_codigo', False)
    lenguaje_codigo   = paquete_capa2.get('lenguaje_codigo', 'ninguno')
    es_pregunta       = paquete_capa2.get('es_pregunta', False)
    complejidad       = paquete_capa2.get('complejidad', 'simple')
    perfil_activacion = paquete_capa2.get('perfil_activacion', 'conversacional')

    # ── PASO 1: Clasificación Groq (semántica, rápida) ────
    clasificacion_groq = None
    fuente_clasificacion = 'patrones'

    try:
        # Extraer ids de C1/C2 para el clasificador propio
        ids_activados = set(red_activa.get('nodos_activos', {}).keys())
        ids_primarios = set(paquete_capa2.get('nodos_primarios', []))
        es_pregunta   = paquete_capa2.get('es_pregunta', False)

        clasificacion_groq = _get_clasificador().clasificar(
            texto           = texto_original,
            contexto        = contexto,
            ids_activados   = ids_activados,
            ids_primarios   = ids_primarios,
            contiene_codigo = contiene_codigo,
            perfil          = perfil_activacion,
            es_pregunta     = es_pregunta,
        )
        if clasificacion_groq:
            fuente_clasificacion = clasificacion_groq.get('fuente', 'clasificador_bell')
    except Exception as e:
        print(f'  C3 ⚠️  Clasificador Bell error: {e}')
        import traceback; traceback.print_exc()

    # Si el mensaje contiene código → forzar tipo técnico
    if contiene_codigo and clasificacion_groq:
        if clasificacion_groq.get('tipo_mensaje') not in ('solicitud_tecnica', 'pregunta'):
            clasificacion_groq['tipo_mensaje'] = 'solicitud_tecnica'

    # ── PASO 2: Construir comprensión completa ────────────
    comprension = _constructor.construir(
        red_activa          = red_activa,
        texto_original      = texto_original,
        contexto            = contexto,
        tono                = tono,
        clasificacion_groq  = clasificacion_groq,
    )

    # Si Groq clasificó, marcar la fuente en comprensión contextual
    if clasificacion_groq:
        if 'contextual' not in comprension:
            comprension['contextual'] = {}
        comprension['contextual']['fuente_clasificacion'] = fuente_clasificacion
        comprension['contextual']['certeza_groq'] = clasificacion_groq.get('certeza', 0.0)
    else:
        fuente_clasificacion = comprension.get('contextual', {}).get(
            'fuente_clasificacion', 'patrones'
        )

    # ── PASO 3: Detectar ambigüedad ───────────────────────
    resultado_ambiguedad = _ambiguedad.detectar(
        comprension=comprension,
        contexto=contexto
    )

    # ── PASO 4: Lyra — lectura emocional ─────────────────
    profunda = comprension.get('profunda', {})
    lectura_lyra = _lyra.leer(
        texto_original       = texto_original,
        tono                 = tono,
        comprension_profunda = dict(profunda),
        contexto             = contexto
    )

    # Enriquecer comprensión con lo que detectó Lyra
    if lectura_lyra:
        if lectura_lyra.get('emocion_detectada') and not profunda.get('emocion_detectada'):
            comprension.setdefault('profunda', {})['emocion_detectada'] = \
                lectura_lyra['emocion_detectada']
        if lectura_lyra.get('estado_subyacente') and not profunda.get('estado_subyacente'):
            comprension.setdefault('profunda', {})['estado_subyacente'] = \
                lectura_lyra['estado_subyacente']

    # ── PASO 5: Echo — verificar coherencia ───────────────
    verificacion_echo = _echo.verificar(
        comprension    = comprension,
        texto_original = texto_original,
        red_activa     = red_activa
    )

    # ── PASO 6: Detectar gaps ─────────────────────────────
    gaps = _gaps.detectar(
        comprension  = comprension,
        red_activa   = red_activa,
        desconocidos = paquete_c1.get('desconocidos', [])
    )

    # ── PASO 7: Métricas globales ─────────────────────────
    nivel_certeza    = _calcular_certeza_global(comprension, verificacion_echo)
    lista_para_capa4 = _esta_lista_para_capa4(resultado_ambiguedad, gaps)
    modo_mental      = _detectar_modo_mental(comprension, clasificacion_groq)

    # ── PASO 8: Logs diagnósticos ─────────────────────────
    _log_diagnostico(
        comprension, lectura_lyra, verificacion_echo,
        resultado_ambiguedad, gaps, nivel_certeza,
        fuente_clasificacion, contiene_codigo, lenguaje_codigo,
        motor_sugerido, modo_mental
    )

    # ── PASO 9: Construir paquete ─────────────────────────
    paquete = PaqueteCapa3(
        comprension          = comprension,
        ambiguedad           = resultado_ambiguedad,
        lectura_lyra         = lectura_lyra,
        verificacion_echo    = verificacion_echo,
        gaps                 = gaps,
        nivel_certeza        = nivel_certeza,
        lista_para_capa4     = lista_para_capa4,
        paquete_capa2        = paquete_capa2,
        # v2
        motor_sugerido       = motor_sugerido,
        contiene_codigo      = contiene_codigo,
        lenguaje_codigo      = lenguaje_codigo,
        es_pregunta          = es_pregunta,
        complejidad          = complejidad,
        perfil_activacion    = perfil_activacion,
        fuente_clasificacion = fuente_clasificacion,
        modo_mental          = modo_mental,
    )

    return paquete.a_dict()


# ══════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════

def _calcular_certeza_global(comprension: dict, verificacion_echo: dict) -> float:
    certeza_literal    = comprension.get('literal',    {}).get('certeza', 0)
    certeza_contextual = comprension.get('contextual', {}).get('certeza', 0)
    certeza_profunda   = comprension.get('profunda',   {}).get('certeza', 0)
    coherencia_echo    = 1.0 if verificacion_echo.get('coherente', False) else 0.6

    return round(
        certeza_literal    * 0.35 +
        certeza_contextual * 0.35 +
        certeza_profunda   * 0.20 +
        coherencia_echo    * 0.10,
        3
    )


def _esta_lista_para_capa4(ambiguedad: dict, gaps: list) -> bool:
    if ambiguedad.get('nivel') == 'critica':
        return False
    gaps_criticos = [g for g in gaps if g.get('critico', False)]
    return len(gaps_criticos) == 0


def _detectar_modo_mental(comprension: dict, clasificacion_groq: dict | None) -> str:
    """Detecta el modo mental del mensaje para orientar a C5 y C6."""
    if clasificacion_groq and clasificacion_groq.get('modo_mental'):
        return clasificacion_groq['modo_mental']

    tipo = comprension.get('contextual', {}).get('tipo_mensaje', 'conversacional')
    if tipo in ('solicitud_tecnica', 'operacion_matematica', 'pregunta_arquitectura_bell'):
        return 'tecnico'
    if tipo in ('expresion_emocional_positiva', 'expresion_emocional_negativa',
                'logro_compartido', 'queja', 'preocupacion'):
        return 'emocional'
    if tipo in ('pregunta', 'pregunta_identidad_bell', 'pregunta_capacidad_bell'):
        return 'exploratorio'
    if tipo in ('solicitud_ayuda',):
        return 'resolutivo'
    return 'social'


# ══════════════════════════════════════════════════════════
# LOGS
# ══════════════════════════════════════════════════════════

def _log_diagnostico(
    comprension, lectura_lyra, verificacion_echo,
    ambiguedad, gaps, nivel_certeza,
    fuente, contiene_codigo, lenguaje_codigo,
    motor_sugerido, modo_mental
):
    contextual = comprension.get('contextual', {})
    profunda   = comprension.get('profunda', {})
    lyra       = lectura_lyra or {}

    tipo_msg   = contextual.get('tipo_mensaje', '?')
    intencion  = profunda.get('intencion_detectada', '?')
    necesidad  = profunda.get('necesidad_real', '?')
    emocion    = profunda.get('emocion_detectada', '?')
    estado_sub = profunda.get('estado_subyacente', '?')
    tono_lyra  = lyra.get('tono_recomendado', '?')

    # Icono de fuente
    fuente_icon = {'groq': '🧠', 'motor': '⚙️', 'patrones': '🔤'}.get(fuente, '?')
    motor_icon  = '🤖' if motor_sugerido == 'groq' else '⚡'

    print(f'  C3 fuente:       {fuente_icon} {fuente}')
    print(f'  C3 tipo_mensaje: {tipo_msg}')
    print(f'  C3 emocion:      {emocion}')
    print(f'  C3 intencion:    {intencion}')
    print(f'  C3 necesidad:    {necesidad}')
    print(f'  C3 estado_sub:   {estado_sub}')
    print(f'  C3 modo_mental:  {modo_mental}')
    print(f'  C3 certeza:      {nivel_certeza:.3f}')
    print(f'  C3 tono_lyra:    {tono_lyra}')
    print(f'  C3 motor_hint:   {motor_icon} {motor_sugerido}')

    if contiene_codigo:
        print(f'  C3 🖥️  código: {lenguaje_codigo}')

    if not verificacion_echo.get('coherente', True):
        correcciones = verificacion_echo.get('correcciones_aplicadas', [])
        print(f'  C3 Echo ⚠️  correcciones: {correcciones}')

    niv_amb = ambiguedad.get('nivel', '?')
    if niv_amb != 'baja':
        print(f'  C3 ambigüedad:  {niv_amb}')

    if gaps:
        tipos_gap = [g.get('tipo', '?') for g in gaps[:3]]
        print(f'  C3 gaps:        {tipos_gap}')