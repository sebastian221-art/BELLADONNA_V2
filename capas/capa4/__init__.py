# capas/capa4/__init__.py
# ================================================
# CAPA 4 — EVALUACIÓN — v2
#
# Orquesta 4 evaluadores:
#   1. EvaluadorRecursos   — ¿qué tiene Bell?
#   2. EvaluadorCapacidad  — ¿puede Bell responder?
#   3. EvaluadorRiesgo     — ¿hay algo que revisar?
#   4. ConstructorContexto — arma contexto consejeras
#
# v2:
# — Logs diagnósticos completos (fin de los "?")
# — Propagación de campos C1/C2/C3
# — Contexto enriquecido para consejeras
# ================================================

from capas.capa4.paquete_capa4 import (
    PaqueteCapa4, RecursosDisponibles,
    EvaluacionCapacidad, EvaluacionRiesgo
)
from capas.capa4.evaluador_recursos   import EvaluadorRecursos
from capas.capa4.evaluador_capacidad  import EvaluadorCapacidad
from capas.capa4.evaluador_riesgo     import EvaluadorRiesgo
from capas.capa4.constructor_contexto import ConstructorContexto

_recursos    = EvaluadorRecursos()
_capacidad   = EvaluadorCapacidad()
_riesgo      = EvaluadorRiesgo()
_constructor = ConstructorContexto()


def procesar(paquete_capa3: dict) -> dict:
    try:
        return _procesar_interno(paquete_capa3)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return PaqueteCapa4(
            exitoso          = False,
            error            = f'Error en Capa 4: {str(e)}',
            lista_para_capa5 = False,
            paquete_capa3    = paquete_capa3,
            # propagación mínima
            motor_sugerido   = paquete_capa3.get('motor_sugerido', 'local'),
            contiene_codigo  = paquete_capa3.get('contiene_codigo', False),
            complejidad      = paquete_capa3.get('complejidad', 'simple'),
        ).a_dict()


def _procesar_interno(paquete_capa3: dict) -> dict:

    # ── Extraer campos propagados de C1/C2/C3 ─────────────
    motor_sugerido    = paquete_capa3.get('motor_sugerido', 'local')
    contiene_codigo   = paquete_capa3.get('contiene_codigo', False)
    lenguaje_codigo   = paquete_capa3.get('lenguaje_codigo', 'ninguno')
    es_pregunta       = paquete_capa3.get('es_pregunta', False)
    complejidad       = paquete_capa3.get('complejidad', 'simple')
    perfil_activacion = paquete_capa3.get('perfil_activacion', 'conversacional')
    fuente_clasif     = paquete_capa3.get('fuente_clasificacion', 'patrones')
    modo_mental       = paquete_capa3.get('modo_mental', 'social')

    # ── 1. Evaluar recursos ────────────────────────────────
    recursos = _recursos.evaluar(paquete_capa3)

    # ── 2. Evaluar capacidad ───────────────────────────────
    capacidad = _capacidad.evaluar(paquete_capa3, recursos)

    # ── 3. Evaluar riesgo ──────────────────────────────────
    riesgo = _riesgo.evaluar(paquete_capa3)

    # ── 4. Construir contexto para consejeras ──────────────
    contexto_consejeras = _constructor.construir(
        paquete_capa3   = paquete_capa3,
        recursos        = recursos,
        capacidad       = capacidad,
        riesgo          = riesgo,
        campos_v2       = {
            'motor_sugerido':    motor_sugerido,
            'contiene_codigo':   contiene_codigo,
            'lenguaje_codigo':   lenguaje_codigo,
            'es_pregunta':       es_pregunta,
            'complejidad':       complejidad,
            'modo_mental':       modo_mental,
            'fuente_clasif':     fuente_clasif,
            'perfil_activacion': perfil_activacion,
        }
    )

    # ── 5. Decidir si continuar a C5 ──────────────────────
    lista, razon = _decidir_continuacion(
        paquete_capa3, recursos, capacidad, riesgo
    )

    resumen = contexto_consejeras.get('resumen_situacion', '')

    # ── 6. Logs diagnósticos ───────────────────────────────
    _log_diagnostico(
        recursos, capacidad, riesgo, lista,
        motor_sugerido, contiene_codigo, modo_mental,
        fuente_clasif, complejidad
    )

    # ── 7. Construir paquete ───────────────────────────────
    paquete = PaqueteCapa4(
        contexto_consejeras = contexto_consejeras,
        recursos            = recursos,
        capacidad           = capacidad,
        riesgo              = riesgo,
        lista_para_capa5    = lista,
        razon_bloqueo       = razon,
        resumen_situacion   = resumen,
        paquete_capa3       = paquete_capa3,
        exitoso             = True,
        # propagación v2
        motor_sugerido      = motor_sugerido,
        contiene_codigo     = contiene_codigo,
        lenguaje_codigo     = lenguaje_codigo,
        es_pregunta         = es_pregunta,
        complejidad         = complejidad,
        perfil_activacion   = perfil_activacion,
        fuente_clasificacion = fuente_clasif,
        modo_mental         = modo_mental,
    )

    return paquete.a_dict()


def _decidir_continuacion(
    paquete_capa3: dict,
    recursos:      RecursosDisponibles,
    capacidad:     EvaluacionCapacidad,
    riesgo:        EvaluacionRiesgo,
) -> tuple:
    if not paquete_capa3.get('lista_para_capa4', True):
        return False, 'Capa 3 reportó comprensión insuficiente'
    if not capacidad.puede_responder:
        return False, f'Bell no puede responder: {capacidad.razon_limitacion}'
    return True, ''


def _log_diagnostico(
    recursos, capacidad, riesgo, lista,
    motor_sugerido, contiene_codigo, modo_mental,
    fuente_clasif, complejidad
):
    # Recursos
    print(f'  C4 recursos:    nodos={recursos.nodos_activos} '
          f'(p={recursos.nodos_primarios} s={recursos.nodos_secundarios}) '
          f'grounding={recursos.grounding_promedio:.3f}')

    if recursos.tiene_habilidades:
        print(f'  C4 habilidades: {recursos.habilidades_ids[:3]}')

    if recursos.gaps_criticos:
        print(f'  C4 gaps_crit:   {recursos.gaps_criticos[:2]}')

    # Capacidad
    conf_pct = f'{capacidad.nivel_confianza:.0%}'
    puede    = '✅' if capacidad.puede_responder else '❌'
    ejecuta  = '⚙️' if capacidad.puede_ejecutar else ''
    print(f'  C4 capacidad:   {puede} {capacidad.tipo_respuesta} '
          f'{ejecuta} confianza={conf_pct}')

    if capacidad.razon_limitacion:
        print(f'  C4 limitacion:  {capacidad.razon_limitacion}')

    # Riesgo
    riesgo_icon = {
        'ninguno': '✅', 'bajo': '🟡', 'medio': '🟠',
        'alto': '🔴', 'critico': '🚨'
    }.get(riesgo.nivel, '?')
    print(f'  C4 riesgo:      {riesgo_icon} {riesgo.nivel}'
          + (f' | veto={riesgo.requiere_veto}' if riesgo.requiere_veto else ''))

    if riesgo.señales:
        print(f'  C4 señales:     {riesgo.señales[:2]}')

    # Campos propagados relevantes
    motor_icon = '🤖' if motor_sugerido == 'groq' else '⚡'
    print(f'  C4 motor_hint:  {motor_icon} {motor_sugerido} | '
          f'modo={modo_mental} | complejidad={complejidad}')

    if contiene_codigo:
        print(f'  C4 🖥️  código detectado')

    fuente_icon = {'groq': '🧠', 'motor': '⚙️', 'patrones': '🔤'}.get(fuente_clasif, '?')
    print(f'  C4 fuente_c3:   {fuente_icon} {fuente_clasif}')

    cont = '✅' if lista else '❌'
    print(f'  C4 → C5:        {cont} {"lista" if lista else "bloqueada"}')