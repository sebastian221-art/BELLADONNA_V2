# capas/capa4/constructor_contexto.py
# ================================================
# CONSTRUCTOR DE CONTEXTO — v2
#
# Arma el dict exacto que necesita
# GestorConsejeras.consultar_todas(contexto)
#
# v2:
# — Incluye campos v2: motor_sugerido,
#   contiene_codigo, modo_mental, complejidad
# — Contexto de memoria de Sebastian
# — Resumen enriquecido para las consejeras
# ================================================

from capas.capa4.paquete_capa4 import (
    RecursosDisponibles, EvaluacionCapacidad, EvaluacionRiesgo
)


class ConstructorContexto:

    def construir(
        self,
        paquete_capa3:  dict,
        recursos:       RecursosDisponibles,
        capacidad:      EvaluacionCapacidad,
        riesgo:         EvaluacionRiesgo,
        campos_v2:      dict = None,
    ) -> dict:
        try:
            return self._construir_interno(
                paquete_capa3, recursos, capacidad, riesgo, campos_v2 or {}
            )
        except Exception as e:
            return self._contexto_minimo(paquete_capa3, e)

    def _construir_interno(
        self,
        paquete_capa3:  dict,
        recursos:       RecursosDisponibles,
        capacidad:      EvaluacionCapacidad,
        riesgo:         EvaluacionRiesgo,
        campos_v2:      dict,
    ) -> dict:

        paquete_c2   = paquete_capa3.get('paquete_capa2', {})
        paquete_c1   = paquete_c2.get('paquete_capa1', {})
        comprension  = paquete_capa3.get('comprension', {})
        profunda     = comprension.get('profunda', {})
        contextual   = comprension.get('contextual', {})
        lectura_lyra = paquete_capa3.get('lectura_lyra', {})
        red_activa   = paquete_c2.get('red_activa', {})
        contexto_c1  = paquete_c1.get('contexto', {})

        # ── Datos del mensaje ─────────────────────────────
        texto_original = paquete_c1.get('contenido_original', '')
        tipo_mensaje   = contextual.get('tipo_mensaje', 'conversacional')
        intencion      = profunda.get('intencion_detectada', 'conversar')
        necesidad      = profunda.get('necesidad_real', 'conexion_social')
        emocion        = profunda.get('emocion_detectada', 'neutra')
        tono_base      = profunda.get('tono_base', 'neutral')
        nombre_usuario = contextual.get('nombre_usuario', 'Sebastian')
        certeza_global = paquete_capa3.get('nivel_certeza', 0.5)

        # ── Campos v2 propagados ──────────────────────────
        motor_sugerido   = campos_v2.get('motor_sugerido', 'local')
        contiene_codigo  = campos_v2.get('contiene_codigo', False)
        lenguaje_codigo  = campos_v2.get('lenguaje_codigo', 'ninguno')
        complejidad      = campos_v2.get('complejidad', 'simple')
        modo_mental      = campos_v2.get('modo_mental', 'social')
        fuente_clasif    = campos_v2.get('fuente_clasif', 'patrones')
        perfil_activacion = campos_v2.get('perfil_activacion', 'conversacional')

        # ── IDs de nodos activos ──────────────────────────
        ids_activos = []
        for nodo in (red_activa.get('nodos_primarios', []) +
                     red_activa.get('nodos_secundarios', [])):
            nid = nodo.get('nodo_id', '') if isinstance(nodo, dict) else ''
            if nid and nid not in ids_activos:
                ids_activos.append(nid)

        # ── Estado emocional desde Lyra ───────────────────
        estado_emocional    = lectura_lyra.get('estado_emocional_sebastian', emocion)
        prioridad_emocional = lectura_lyra.get('prioridad_emocional', emocion == 'negativa')

        # ── Contexto de Sebastian desde memoria ───────────
        contexto_sebastian = self._obtener_contexto_sebastian(contexto_c1)

        # ── Resumen enriquecido para consejeras ───────────
        resumen = self._construir_resumen(
            texto_original, tipo_mensaje, intencion, necesidad,
            estado_emocional, capacidad, riesgo,
            contiene_codigo, complejidad, motor_sugerido
        )

        return {
            # ── Mensaje y comprensión ─────────────────────
            'texto_original':        texto_original,
            'comprension':           comprension,
            'ids_activos':           ids_activos,

            # ── Clasificación ─────────────────────────────
            'tipo_mensaje':          tipo_mensaje,
            'intencion_detectada':   intencion,
            'necesidad_real':        necesidad,
            'fuente_clasificacion':  fuente_clasif,

            # ── Estado emocional ──────────────────────────
            'emocion_detectada':     emocion,
            'estado_emocional':      estado_emocional,
            'prioridad_emocional':   prioridad_emocional,
            'tono_base':             tono_base,

            # ── Usuario ───────────────────────────────────
            'nombre_usuario':        nombre_usuario,
            'contexto_sebastian':    contexto_sebastian,

            # ── Certeza y confianza ───────────────────────
            'certeza_global':        certeza_global,
            'nivel_confianza_bell':  capacidad.nivel_confianza,

            # ── Capacidad de Bell ─────────────────────────
            'puede_responder':       capacidad.puede_responder,
            'puede_ejecutar':        capacidad.puede_ejecutar,
            'tipo_respuesta':        capacidad.tipo_respuesta,
            'alternativa_bell':      capacidad.alternativa,

            # ── Recursos ─────────────────────────────────
            'nodos_activos':         recursos.nodos_activos,
            'tiene_habilidades':     recursos.tiene_habilidades,
            'grounding_promedio':    recursos.grounding_promedio,

            # ── Riesgo para Vega ─────────────────────────
            'nivel_riesgo':          riesgo.nivel,
            'señales_riesgo':        riesgo.señales,
            'principios_en_riesgo':  riesgo.principios_en_riesgo,
            'requiere_revision_vega': riesgo.requiere_veto,

            # ── Campos v2 — motor y complejidad ──────────
            'motor_sugerido':        motor_sugerido,
            'contiene_codigo':       contiene_codigo,
            'lenguaje_codigo':       lenguaje_codigo,
            'complejidad':           complejidad,
            'modo_mental':           modo_mental,
            'perfil_activacion':     perfil_activacion,

            # ── Red activa completa ───────────────────────
            'red_activa':            red_activa,

            # ── Resumen ejecutivo ─────────────────────────
            'resumen_situacion':     resumen,

            # ── Historial ─────────────────────────────────
            'hay_historial': bool(
                contexto_c1.get('conversacion', {}).get('historial_reciente')
            ),
        }

    def _obtener_contexto_sebastian(self, contexto_c1: dict) -> dict:
        """
        Obtiene el contexto de Sebastian desde memoria.
        Si falla, retorna el contexto básico de C1.
        """
        # Primero intentar desde memoria real
        try:
            from biblioteca.memoria import obtener_memoria
            mem    = obtener_memoria()
            perfil = mem.obtener_perfil_sebastian() or {}
            return {
                'nombre':              perfil.get('nombre', 'Sebastian'),
                'estado_emocional':    perfil.get('estado_emocional', 'desconocido'),
                'proyectos_activos':   perfil.get('proyectos', ['BELLADONNA_V2']),
                'ciudad':              perfil.get('ciudad', 'Bucaramanga'),
                'ultimo_fyi':          perfil.get('ultimo_fyi', ''),
            }
        except Exception:
            pass

        # Fallback al contexto de C1
        ctx_sebastian = contexto_c1.get('sebastian', {})
        return {
            'nombre':            ctx_sebastian.get('nombre', 'Sebastian'),
            'estado_emocional':  ctx_sebastian.get('estado_emocional', 'desconocido'),
            'proyectos_activos': ctx_sebastian.get('proyectos_activos', ['BELLADONNA_V2']),
            'ciudad':            ctx_sebastian.get('ciudad', 'Bucaramanga'),
            'ultimo_fyi':        ctx_sebastian.get('ultimo_fyi', ''),
        }

    def _construir_resumen(
        self,
        texto:         str,
        tipo:          str,
        intencion:     str,
        necesidad:     str,
        emocion:       str,
        capacidad:     EvaluacionCapacidad,
        riesgo:        EvaluacionRiesgo,
        contiene_codigo: bool,
        complejidad:   str,
        motor_sugerido: str,
    ) -> str:
        partes = [
            f'Mensaje: "{texto[:70]}{"..." if len(texto) > 70 else ""}"',
            f'Tipo: {tipo}',
            f'Intención: {intencion}',
            f'Necesidad: {necesidad}',
        ]
        if emocion not in ('neutra', ''):
            partes.append(f'Emoción: {emocion}')
        if contiene_codigo:
            partes.append('Contiene código')
        partes.append(
            f'Bell: {"✅" if capacidad.puede_responder else "❌"} '
            f'{capacidad.tipo_respuesta} '
            f'({capacidad.nivel_confianza:.0%}) '
            f'vía {"Groq" if motor_sugerido == "groq" else "Motor local"}'
        )
        if riesgo.nivel not in ('ninguno', 'bajo'):
            partes.append(f'⚠️ Riesgo: {riesgo.nivel}')
        return ' | '.join(partes)

    def _contexto_minimo(self, paquete_capa3: dict, error: Exception) -> dict:
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
            'motor_sugerido':      'local',
            'contiene_codigo':     False,
            'complejidad':         'simple',
            'modo_mental':         'social',
            'resumen_situacion':   f'Error en constructor: {error}',
            'error_constructor':   str(error),
        }