# capas/capa8/__init__.py
# ================================================
# CAPA 8 — EXPRESIÓN FINAL
#
# Recibe: PaqueteCapa7
# Produce: PaqueteCapa8 — lo que ve Sebastian
#
# Flujo:
# 1. VerificadorTono  → tono correcto según Sage
# 2. Formateador      → limpia y da formato final
# 3. RegistradorTurno → guarda para Capa 9
# ================================================

from capas.capa8.paquete_capa8      import PaqueteCapa8, RegistroTurno
from capas.capa8.verificador_tono   import VerificadorTono
from capas.capa8.formateador        import Formateador
from capas.capa8.registrador_turno  import RegistradorTurno

_verificador_tono = VerificadorTono()
_formateador      = Formateador()
_registrador      = RegistradorTurno()


def procesar(paquete_capa7: dict) -> dict:
    try:
        return _procesar_interno(paquete_capa7)
    except Exception as e:
        import traceback; traceback.print_exc()
        respuesta = paquete_capa7.get('respuesta_final', '')
        return PaqueteCapa8(
            respuesta_final = respuesta,
            paquete_capa7   = paquete_capa7,
            exitoso         = False,
            error           = str(e),
        ).a_dict()


def _procesar_interno(paquete_capa7: dict) -> dict:

    respuesta_c7   = paquete_capa7.get('respuesta_final', '')

    # Extraer datos de capas anteriores
    paquete_c6   = paquete_capa7.get('paquete_capa6', {})
    paquete_c5   = paquete_c6.get('paquete_capa5', {})
    paquete_c4   = paquete_c5.get('paquete_capa4', {})
    paquete_c3   = paquete_c4.get('paquete_capa3', {})
    paquete_c2   = paquete_c3.get('paquete_capa2', {})
    paquete_c1   = paquete_c2.get('paquete_capa1', {})

    instruccion         = paquete_c5.get('instruccion', {})
    tono_esperado       = instruccion.get('tono', 'cercano_natural')
    tipo_respuesta      = instruccion.get('tipo_respuesta', 'conversacional')
    prioridad_emocional = instruccion.get('prioridad_emocional', False)
    texto_usuario       = paquete_c1.get('contenido_original', '')

    # ── 1. VERIFICAR TONO ────────────────────────────
    respuesta_con_tono = _verificador_tono.verificar_y_ajustar(
        respuesta           = respuesta_c7,
        tono_esperado       = tono_esperado,
        prioridad_emocional = prioridad_emocional,
    )

    # ── 2. FORMATEAR ─────────────────────────────────
    respuesta_final = _formateador.formatear(
        respuesta      = respuesta_con_tono,
        tipo_respuesta = tipo_respuesta,
    )

    # ── 3. REGISTRAR TURNO ───────────────────────────
    registro = _registrador.registrar(
        texto_usuario  = texto_usuario,
        respuesta_bell = respuesta_final,
        paquete_capa7  = paquete_capa7,
        paquete_capa5  = paquete_c5,
    )

    return PaqueteCapa8(
        respuesta_final = respuesta_final,
        tono_final      = tono_esperado,
        tipo_respuesta  = tipo_respuesta,
        longitud_chars  = len(respuesta_final),
        registro_turno  = registro,
        paquete_capa7   = paquete_capa7,
    ).a_dict()