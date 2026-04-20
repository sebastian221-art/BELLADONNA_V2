# capas/capa5/__init__.py
# ================================================
# CAPA 5 — DELIBERACIÓN
# Las 8 consejeras entran al flujo real.
# Recibe: PaqueteCapa4
# Produce: PaqueteCapa5 con deliberación completa
#
# Flujo interno:
#   1. PreparadorContexto  → mapeo exacto por consejera
#   2. GestorConsejeras    → deliberación real
#   3. ManejadorVeto       → si Vega veta, respuesta honesta
#   4. Sintetizador        → instrucciones para Capa 6
# ================================================

from capas.capa5.paquete_capa5 import PaqueteCapa5, InstruccionRespuesta
from capas.capa5.preparador_contexto import PreparadorContexto
from capas.capa5.manejador_veto      import ManejadorVeto
from capas.capa5.sintetizador        import Sintetizador

# Instancias — se crean una vez y se reusan
_preparador  = PreparadorContexto()
_veto        = ManejadorVeto()
_sintetizador = Sintetizador()


def procesar(paquete_capa4: dict) -> dict:
    """
    La única función pública de la Capa 5.
    Recibe el paquete de la Capa 4.
    Retorna siempre un diccionario.
    Nunca lanza excepciones.
    """
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
                recomendacion_sage = 'Fallback por error en Capa 5',
            ),
            paquete_capa4 = paquete_capa4,
        ).a_dict()


def _procesar_interno(paquete_capa4: dict) -> dict:

    # Verificar que Capa 4 aprobó
    if not paquete_capa4.get('lista_para_capa5', True):
        razon = paquete_capa4.get('razon_bloqueo', 'Capa 4 bloqueó el flujo')
        return PaqueteCapa5(
            aprobado      = False,
            instruccion   = InstruccionRespuesta(
                tipo_respuesta     = 'honestidad_limitacion',
                tono               = 'honesto_directo',
                recomendacion_sage = razon,
            ),
            respuesta_directa = (
                'No pude procesar tu mensaje completamente. '
                f'Razón: {razon}'
            ),
            paquete_capa4 = paquete_capa4,
        ).a_dict()

    # ── 1. PREPARAR CONTEXTO PARA CONSEJERAS ──────────
    contexto_enriquecido = _preparador.preparar(paquete_capa4)

    # ── 2. DELIBERACIÓN REAL ───────────────────────────
    from biblioteca.consejeras.gestor_consejeras import GestorConsejeras
    gestor = GestorConsejeras.obtener()
    deliberacion = gestor.consultar_todas(contexto_enriquecido)

    # ── 3. MANEJAR VETO ────────────────────────────────
    if deliberacion.veto:
        respuesta, instruccion = _veto.manejar(
            veto_por   = deliberacion.veto_por,
            veto_razon = deliberacion.veto_razon,
            contexto   = contexto_enriquecido,
        )
        return PaqueteCapa5(
            aprobado          = False,
            veto              = True,
            veto_por          = deliberacion.veto_por,
            veto_razon        = deliberacion.veto_razon,
            instruccion       = instruccion,
            respuesta_directa = respuesta,
            deliberacion      = deliberacion.a_dict(),
            paquete_capa4     = paquete_capa4,
        ).a_dict()

    # ── 4. SINTETIZAR INSTRUCCIONES ────────────────────
    instruccion = _sintetizador.sintetizar(deliberacion, paquete_capa4)

    return PaqueteCapa5(
        aprobado      = True,
        veto          = False,
        instruccion   = instruccion,
        deliberacion  = deliberacion.a_dict(),
        paquete_capa4 = paquete_capa4,
    ).a_dict()