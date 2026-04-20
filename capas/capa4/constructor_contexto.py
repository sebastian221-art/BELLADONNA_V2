# capas/capa4/constructor_contexto.py
# ================================================
# CONSTRUCTOR DE CONTEXTO — Capa 4
# Arma el dict exacto que necesita
# GestorConsejeras.consultar_todas(contexto)
# Todo lo que las consejeras necesitan saber
# está aquí, organizado y listo.
# ================================================

from capas.capa4.paquete_capa4 import (
    RecursosDisponibles, EvaluacionCapacidad, EvaluacionRiesgo
)


class ConstructorContexto:

    def construir(
        self,
        paquete_capa3:   dict,
        recursos:        RecursosDisponibles,
        capacidad:       EvaluacionCapacidad,
        riesgo:          EvaluacionRiesgo,
    ) -> dict:
        """
        Construye el contexto completo para las consejeras.
        Este es el dict que recibe consultar_todas().
        """
        try:
            return self._construir_interno(
                paquete_capa3, recursos, capacidad, riesgo
            )
        except Exception as e:
            return self._contexto_minimo(paquete_capa3, e)

    def _construir_interno(
        self,
        paquete_capa3:   dict,
        recursos:        RecursosDisponibles,
        capacidad:       EvaluacionCapacidad,
        riesgo:          EvaluacionRiesgo,
    ) -> dict:

        paquete_c2  = paquete_capa3.get('paquete_capa2', {})
        paquete_c1  = paquete_c2.get('paquete_capa1', {})
        comprension = paquete_capa3.get('comprension', {})
        profunda    = comprension.get('profunda', {})
        contextual  = comprension.get('contextual', {})
        lectura_lyra = paquete_capa3.get('lectura_lyra', {})
        red_activa   = paquete_c2.get('red_activa', {})

        # Extraer datos clave
        texto_original   = paquete_c1.get('contenido_original', '')
        tipo_mensaje     = contextual.get('tipo_mensaje', 'conversacional')
        intencion        = profunda.get('intencion_detectada', 'conversar')
        necesidad        = profunda.get('necesidad_real', 'conexion_social')
        emocion          = profunda.get('emocion_detectada', 'neutra')
        tono_base        = profunda.get('tono_base', 'neutral')
        nombre_usuario   = contextual.get('nombre_usuario', 'Sebastian')
        certeza_global   = paquete_capa3.get('nivel_certeza', 0.5)

        # IDs de nodos activos — lo que las consejeras necesitan
        ids_activos = []
        for n in red_activa.get('nodos_primarios', []):
            nid = n.get('nodo_id', '') if isinstance(n, dict) else ''
            if nid:
                ids_activos.append(nid)
        for n in red_activa.get('nodos_secundarios', []):
            nid = n.get('nodo_id', '') if isinstance(n, dict) else ''
            if nid and nid not in ids_activos:
                ids_activos.append(nid)

        # Estado emocional desde Lyra
        estado_emocional = lectura_lyra.get(
            'estado_emocional_sebastian', emocion
        )
        prioridad_emocional = lectura_lyra.get(
            'requiere_atencion_emocional', emocion == 'negativa'
        )

        # Resumen de la situación para las consejeras
        resumen = self._construir_resumen(
            texto_original, intencion, necesidad,
            estado_emocional, capacidad, riesgo
        )

        # El contexto completo — formato que espera GestorConsejeras
        return {
            # Texto original siempre presente
            'texto_original':       texto_original,

            # Comprensión construida en Capas 1-3
            'comprension':          comprension,
            'ids_activos':          ids_activos,

            # Tipo e intención
            'tipo_mensaje':         tipo_mensaje,
            'intencion_detectada':  intencion,
            'necesidad_real':       necesidad,

            # Estado emocional
            'emocion_detectada':    emocion,
            'estado_emocional':     estado_emocional,
            'prioridad_emocional':  prioridad_emocional,
            'tono_base':            tono_base,

            # Usuario
            'nombre_usuario':       nombre_usuario,

            # Certeza y confianza
            'certeza_global':       certeza_global,
            'nivel_confianza_bell': capacidad.nivel_confianza,

            # Capacidad de Bell
            'puede_responder':      capacidad.puede_responder,
            'puede_ejecutar':       capacidad.puede_ejecutar,
            'tipo_respuesta':       capacidad.tipo_respuesta,
            'alternativa_bell':     capacidad.alternativa,

            # Recursos disponibles
            'nodos_activos':        recursos.nodos_activos,
            'tiene_habilidades':    recursos.tiene_habilidades,
            'grounding_promedio':   recursos.grounding_promedio,

            # Riesgo para Vega
            'nivel_riesgo':         riesgo.nivel,
            'señales_riesgo':       riesgo.señales,
            'principios_en_riesgo': riesgo.principios_en_riesgo,
            'requiere_revision_vega': riesgo.requiere_veto,

            # Red activa completa por si alguna consejera la necesita
            'red_activa':           red_activa,

            # Resumen ejecutivo
            'resumen_situacion':    resumen,

            # Historial si existe
            'hay_historial':        bool(
                paquete_c1.get('contexto', {}).get('conversacion', {})
            ),
        }

    def _construir_resumen(
        self,
        texto:     str,
        intencion: str,
        necesidad: str,
        emocion:   str,
        capacidad: EvaluacionCapacidad,
        riesgo:    EvaluacionRiesgo,
    ) -> str:
        partes = [
            f'Mensaje: "{texto[:80]}{"..." if len(texto) > 80 else ""}"',
            f'Intención: {intencion}',
            f'Necesidad: {necesidad}',
        ]
        if emocion not in ('neutra', ''):
            partes.append(f'Emoción: {emocion}')
        partes.append(
            f'Bell puede: {"sí" if capacidad.puede_responder else "no"} '
            f'({capacidad.tipo_respuesta}, '
            f'confianza {capacidad.nivel_confianza:.0%})'
        )
        if riesgo.nivel not in ('ninguno', 'bajo'):
            partes.append(f'Riesgo detectado: {riesgo.nivel}')
        return ' | '.join(partes)

    def _contexto_minimo(self, paquete_capa3: dict, error: Exception) -> dict:
        """Contexto mínimo si algo falla."""
        paquete_c2 = paquete_capa3.get('paquete_capa2', {})
        paquete_c1 = paquete_c2.get('paquete_capa1', {})
        return {
            'texto_original':      paquete_c1.get('contenido_original', ''),
            'tipo_mensaje':        'conversacional',
            'intencion_detectada': 'conversar',
            'necesidad_real':      'conexion_social',
            'emocion_detectada':   'neutra',
            'puede_responder':     True,
            'puede_ejecutar':      False,
            'nivel_riesgo':        'ninguno',
            'certeza_global':      0.5,
            'ids_activos':         [],
            'error_constructor':   str(error),
        }