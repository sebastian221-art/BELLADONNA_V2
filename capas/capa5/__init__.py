# capas/capa5/__init__.py
# ================================================
# CAPA 5 — DELIBERACIÓN — v2
#
# Las 8 consejeras entran al flujo real.
# Recibe: PaqueteCapa4
# Produce: PaqueteCapa5 con deliberación completa
#
# v2:
# — Logs diagnósticos propios de C5
# — Propagación de campos C1/C2/C3/C4 hacia C6
# ================================================

from capas.capa5.paquete_capa5      import PaqueteCapa5, InstruccionRespuesta
from capas.capa5.preparador_contexto import PreparadorContexto
from capas.capa5.manejador_veto      import ManejadorVeto
from capas.capa5.sintetizador        import Sintetizador

_preparador   = PreparadorContexto()
_veto         = ManejadorVeto()
_sintetizador = Sintetizador()


def procesar(paquete_capa4: dict) -> dict:
    try:
        return _procesar_interno(paquete_capa4)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return PaqueteCapa5(
            exitoso      = False,
            error        = f'Error en Capa 5: {str(e)}',
            aprobado     = True,
            instruccion  = InstruccionRespuesta(
                tipo_respuesta     = 'conversacional',
                tono               = 'cercano_natural',
                recomendacion_sage = f'Fallback por error en Capa 5: {e}',
            ),
            paquete_capa4   = paquete_capa4,
            motor_sugerido  = paquete_capa4.get('motor_sugerido', 'local'),
            contiene_codigo = paquete_capa4.get('contiene_codigo', False),
            complejidad     = paquete_capa4.get('complejidad', 'simple'),
        ).a_dict()


def _procesar_interno(paquete_capa4: dict) -> dict:

    # ── Campos propagados de C1/C2/C3/C4 ─────────────────
    motor_sugerido    = paquete_capa4.get('motor_sugerido', 'local')
    contiene_codigo   = paquete_capa4.get('contiene_codigo', False)
    lenguaje_codigo   = paquete_capa4.get('lenguaje_codigo', 'ninguno')
    es_pregunta       = paquete_capa4.get('es_pregunta', False)
    complejidad       = paquete_capa4.get('complejidad', 'simple')
    perfil_activacion = paquete_capa4.get('perfil_activacion', 'conversacional')
    fuente_clasif     = paquete_capa4.get('fuente_clasificacion', 'patrones')
    modo_mental       = paquete_capa4.get('modo_mental', 'social')

    # ── Verificar que C4 aprobó ───────────────────────────
    if not paquete_capa4.get('lista_para_capa5', True):
        razon = paquete_capa4.get('razon_bloqueo', 'Capa 4 bloqueó el flujo')
        print(f'  C5 ❌ bloqueado: {razon}')
        return PaqueteCapa5(
            aprobado         = False,
            instruccion      = InstruccionRespuesta(
                tipo_respuesta     = 'honestidad_limitacion',
                tono               = 'honesto_directo',
                recomendacion_sage = razon,
            ),
            respuesta_directa = f'No pude procesar tu mensaje. Razón: {razon}',
            paquete_capa4     = paquete_capa4,
            motor_sugerido    = motor_sugerido,
            contiene_codigo   = contiene_codigo,
            complejidad       = complejidad,
        ).a_dict()

    # ── 1. Preparar contexto para consejeras ──────────────
    contexto_enriquecido = _preparador.preparar(paquete_capa4)

    # ── 2. Deliberación real ──────────────────────────────
    from biblioteca.consejeras.gestor_consejeras import GestorConsejeras
    gestor       = GestorConsejeras.obtener()
    deliberacion = gestor.consultar_todas(contexto_enriquecido)

    # ── 3. Manejar veto ───────────────────────────────────
    if deliberacion.veto:
        respuesta, instruccion = _veto.manejar(
            veto_por   = deliberacion.veto_por,
            veto_razon = deliberacion.veto_razon,
            contexto   = contexto_enriquecido,
        )
        print(f'  C5 🚨 VETO por {deliberacion.veto_por}: {deliberacion.veto_razon[:60]}')
        return PaqueteCapa5(
            aprobado          = False,
            veto              = True,
            veto_por          = deliberacion.veto_por,
            veto_razon        = deliberacion.veto_razon,
            instruccion       = instruccion,
            respuesta_directa = respuesta,
            deliberacion      = deliberacion.a_dict(),
            paquete_capa4     = paquete_capa4,
            motor_sugerido    = motor_sugerido,
            contiene_codigo   = contiene_codigo,
            complejidad       = complejidad,
        ).a_dict()

    # ── 4. Sintetizar instrucciones ───────────────────────
    instruccion = _sintetizador.sintetizar(
        deliberacion    = deliberacion,
        paquete_capa4   = paquete_capa4,
        motor_sugerido  = motor_sugerido,
        contiene_codigo = contiene_codigo,
        modo_mental     = modo_mental,
    )

    # ── 5. Logs diagnósticos ──────────────────────────────
    _log_diagnostico(instruccion, deliberacion, motor_sugerido, contiene_codigo)

    return PaqueteCapa5(
        aprobado          = True,
        veto              = False,
        instruccion       = instruccion,
        deliberacion      = deliberacion.a_dict(),
        paquete_capa4     = paquete_capa4,
        # propagación v2
        motor_sugerido    = motor_sugerido,
        contiene_codigo   = contiene_codigo,
        lenguaje_codigo   = lenguaje_codigo,
        es_pregunta       = es_pregunta,
        complejidad       = complejidad,
        perfil_activacion = perfil_activacion,
        fuente_clasificacion = fuente_clasif,
        modo_mental       = modo_mental,
    ).a_dict()


def _log_diagnostico(instruccion, deliberacion, motor_sugerido, contiene_codigo):
    delib = deliberacion.a_dict() if hasattr(deliberacion, 'a_dict') else (
        deliberacion if isinstance(deliberacion, dict) else {}
    )

    tono          = instruccion.tono
    tipo          = instruccion.tipo_respuesta
    confianza     = instruccion.nivel_confianza if hasattr(instruccion, 'nivel_confianza') else instruccion.confianza
    prio_emo      = instruccion.prioridad_emocional
    nivel_detalle = instruccion.nivel_detalle
    sage_msg      = instruccion.recomendacion_sage[:60] if instruccion.recomendacion_sage else ''

    motor_icon = '🤖' if motor_sugerido == 'groq' else '⚡'

    print(f'  C5 tono:    {tono} | veto: False')
    print(f'  C5 tipo:    {tipo} | detalle: {nivel_detalle} | conf: {confianza:.2f}')
    print(f'  C5 motor:   {motor_icon} {motor_sugerido}'
          + (' | 🖥️  código' if contiene_codigo else ''))
    if prio_emo:
        print(f'  C5 🩷 prioridad emocional activa')
    if sage_msg:
        print(f'  C5 sage:    "{sage_msg}"')