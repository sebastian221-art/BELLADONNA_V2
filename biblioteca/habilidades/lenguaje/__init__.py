# biblioteca/habilidades/lenguaje/__init__.py
# ================================================
# HABILIDAD DE LENGUAJE — Punto de entrada
#
# Esta función produce SOLO comprensión.
# La respuesta la construye constructor_decision.
# ================================================

from biblioteca.habilidades.lenguaje.motor  import MotorComprension
from biblioteca.habilidades.lenguaje.paquete import SalidaLenguaje

_motor = MotorComprension.obtener()


def procesar(parametros: dict) -> dict:
    try:
        texto    = parametros.get('texto', '')
        contexto = parametros.get('contexto', {})

        if not texto.strip():
            return SalidaLenguaje(exitoso=False, error='Texto vacío').a_dict()

        comprension = _motor.comprender(texto, contexto)

        return SalidaLenguaje(
            exitoso             = True,
            intencion           = comprension.intencion,
            accion_principal    = comprension.accion_principal,
            tipo_mensaje        = comprension.tipo_mensaje,
            objetos             = comprension.objetos,
            habilidad_requerida = comprension.habilidad_requerida,
            dominio_tecnico     = comprension.dominio_tecnico,
            parametros_tecnicos = comprension.parametros_tecnicos,
            emocion_detectada   = comprension.emocion_detectada,
            intensidad          = comprension.intensidad,
            tono_base           = comprension.tono_base,
            necesidad_real      = comprension.necesidad_real,
            id_lyra             = comprension.id_lyra,
            ids_activos         = comprension.ids_activos,
            respuesta_base      = '',  # constructor_decision la construye
            confianza           = comprension.confianza_global,
            dimensiones_activas = comprension.dimensiones_activas,
        ).a_dict()

    except Exception as e:
        return SalidaLenguaje(exitoso=False, error=str(e)).a_dict()