# capas/capa4/evaluador_riesgo.py
# ================================================
# EVALUADOR DE RIESGO — Capa 4
# Detecta señales que Vega debe revisar en Capa 5.
# No toma decisiones éticas — solo detecta y señala.
# Las decisiones éticas son de Vega.
# ================================================

from capas.capa4.paquete_capa4 import EvaluacionRiesgo

# Palabras que activan análisis de riesgo
SEÑALES_RIESGO_ALTO = {
    'matar', 'atacar', 'dañar', 'lastimar', 'destruir',
    'hackear', 'robar', 'engañar', 'manipular', 'explotar',
    'violar', 'abusar', 'amenazar', 'extorsionar',
}

SEÑALES_RIESGO_MEDIO = {
    'modificar', 'eliminar', 'borrar', 'cambiar codigo',
    'acceder', 'contraseña', 'password', 'secreto',
    'trampa', 'mentir', 'fingir',
}

SEÑALES_RIESGO_BAJO = {
    'peligro', 'riesgo', 'problema', 'conflicto',
    'preocupado', 'asustado', 'miedo',
}

PRINCIPIOS_BELL = {
    'HONESTIDAD', 'NO_AUTO_MODIFICACION', 'SEGURIDAD_DATOS',
    'PRIVACIDAD', 'NO_VIOLENCIA', 'NO_MANIPULACION',
}


class EvaluadorRiesgo:

    def evaluar(self, paquete_capa3: dict) -> EvaluacionRiesgo:
        try:
            return self._evaluar_interno(paquete_capa3)
        except Exception as e:
            return EvaluacionRiesgo(
                nivel='bajo',
                señales=[f'Evaluación parcial: {e}'],
            )

    def _evaluar_interno(self, paquete_capa3: dict) -> EvaluacionRiesgo:
        paquete_c2 = paquete_capa3.get('paquete_capa2', {})
        paquete_c1 = paquete_c2.get('paquete_capa1', {})
        texto      = paquete_c1.get('contenido_original', '').lower()

        comprension = paquete_capa3.get('comprension', {})
        profunda    = comprension.get('profunda', {})
        intencion   = profunda.get('intencion_detectada', '')

        señales               = []
        principios_en_riesgo  = []
        nivel                 = 'ninguno'
        requiere_veto         = False

        # Análisis de texto
        for palabra in SEÑALES_RIESGO_ALTO:
            if palabra in texto:
                señales.append(f'Señal alta: "{palabra}"')
                nivel = 'alto'
                if palabra in ('matar', 'atacar', 'lastimar', 'dañar',
                               'manipular', 'engañar'):
                    principios_en_riesgo.append('NO_VIOLENCIA')
                    principios_en_riesgo.append('NO_MANIPULACION')
                    requiere_veto = True

        if nivel != 'alto':
            for palabra in SEÑALES_RIESGO_MEDIO:
                if palabra in texto:
                    señales.append(f'Señal media: "{palabra}"')
                    if nivel == 'ninguno':
                        nivel = 'medio'

        if nivel == 'ninguno':
            for palabra in SEÑALES_RIESGO_BAJO:
                if palabra in texto:
                    señales.append(f'Señal baja: "{palabra}"')
                    nivel = 'bajo'

        # Señales desde comprensión profunda
        if 'manipular' in intencion.lower():
            señales.append('Intención de manipulación detectada')
            principios_en_riesgo.append('NO_MANIPULACION')
            nivel = 'alto'
            requiere_veto = True

        if 'modificar_bell' in intencion.lower():
            señales.append('Solicitud de auto-modificación')
            principios_en_riesgo.append('NO_AUTO_MODIFICACION')
            nivel = 'critico'
            requiere_veto = True

        # Limpiar duplicados
        principios_en_riesgo = list(set(principios_en_riesgo))

        # Si nivel es alto o crítico — siempre requiere Vega
        if nivel in ('alto', 'critico'):
            requiere_veto = True

        return EvaluacionRiesgo(
            nivel=nivel,
            señales=señales,
            requiere_veto=requiere_veto,
            principios_en_riesgo=principios_en_riesgo,
            confianza_evaluacion=0.85,
        )