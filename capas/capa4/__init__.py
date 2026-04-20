# capas/capa4/__init__.py
# ================================================
# CAPA 4 — EVALUACIÓN
# Recibe: PaqueteCapa3
# Produce: PaqueteCapa4 listo para Capa 5
#
# Orquesta 4 evaluadores:
#   1. EvaluadorRecursos   — ¿qué tiene Bell?
#   2. EvaluadorCapacidad  — ¿puede Bell responder?
#   3. EvaluadorRiesgo     — ¿hay algo que revisar?
#   4. ConstructorContexto — arma contexto consejeras
# ================================================

from capas.capa4.paquete_capa4 import (
    PaqueteCapa4, RecursosDisponibles,
    EvaluacionCapacidad, EvaluacionRiesgo
)
from capas.capa4.evaluador_recursos   import EvaluadorRecursos
from capas.capa4.evaluador_capacidad  import EvaluadorCapacidad
from capas.capa4.evaluador_riesgo     import EvaluadorRiesgo
from capas.capa4.constructor_contexto import ConstructorContexto

# Instancias — se crean una vez y se reusan
_recursos    = EvaluadorRecursos()
_capacidad   = EvaluadorCapacidad()
_riesgo      = EvaluadorRiesgo()
_constructor = ConstructorContexto()


def procesar(paquete_capa3: dict) -> dict:
    """
    La única función pública de la Capa 4.
    Recibe el paquete de la Capa 3.
    Retorna siempre un diccionario.
    Nunca lanza excepciones.
    """
    try:
        return _procesar_interno(paquete_capa3)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return PaqueteCapa4(
            exitoso=False,
            error=f'Error en Capa 4: {str(e)}',
            lista_para_capa5=False,
            paquete_capa3=paquete_capa3,
        ).a_dict()


def _procesar_interno(paquete_capa3: dict) -> dict:

    # ---- 1. EVALUAR RECURSOS ----
    recursos = _recursos.evaluar(paquete_capa3)

    # ---- 2. EVALUAR CAPACIDAD ----
    capacidad = _capacidad.evaluar(paquete_capa3, recursos)

    # ---- 3. EVALUAR RIESGO ----
    riesgo = _riesgo.evaluar(paquete_capa3)

    # ---- 4. CONSTRUIR CONTEXTO PARA CONSEJERAS ----
    contexto_consejeras = _constructor.construir(
        paquete_capa3, recursos, capacidad, riesgo
    )

    # ---- 5. DECIDIR SI PASAR A CAPA 5 ----
    lista, razon = _decidir_continuacion(
        paquete_capa3, recursos, capacidad, riesgo
    )

    # ---- 6. RESUMEN EJECUTIVO ----
    resumen = contexto_consejeras.get('resumen_situacion', '')

    paquete = PaqueteCapa4(
        contexto_consejeras=contexto_consejeras,
        recursos=recursos,
        capacidad=capacidad,
        riesgo=riesgo,
        lista_para_capa5=lista,
        razon_bloqueo=razon,
        resumen_situacion=resumen,
        paquete_capa3=paquete_capa3,
        exitoso=True,
    )

    return paquete.a_dict()


def _decidir_continuacion(
    paquete_capa3: dict,
    recursos:      RecursosDisponibles,
    capacidad:     EvaluacionCapacidad,
    riesgo:        EvaluacionRiesgo,
) -> tuple:
    """
    Decide si el paquete está listo para Capa 5.
    Retorna (lista: bool, razon: str)
    """

    # Si Capa 3 no estaba lista — hereda el bloqueo
    if not paquete_capa3.get('lista_para_capa4', True):
        return False, 'Capa 3 reportó comprensión insuficiente'

    # Si Bell no puede responder de ninguna forma
    if not capacidad.puede_responder:
        return False, f'Bell no puede responder: {capacidad.razon_limitacion}'

    # Riesgo crítico bloquea — Vega debe revisarlo en Capa 5 de todas formas,
    # pero si es crítico la deliberación es obligatoria y urgente
    # (no bloqueamos aquí — dejamos que Vega vete en Capa 5)

    # Siempre lista si Bell puede responder y Capa 3 aprobó
    return True, ''