# capas/capa5/preparador_contexto.py
# ================================================
# PREPARADOR DE CONTEXTO — Capa 5
#
# Cada consejera espera campos específicos.
# Este módulo hace el mapeo exacto para que
# cada consejera reciba exactamente lo que necesita.
#
# SOMA    → contenido_normalizado + conceptos + paquete_capa1
# VEGA    → texto_original + comprension (ya viene de Capa 4)
# NOVA    → comprension + tipo_mensaje
# ECHO    → comprension (dict mutable) + red_activa
# LYRA    → ids_activos como SET + emocion + tono
# LUNA    → tipo_mensaje + emocion
# IRIS    → tipo_mensaje + necesidad
# SAGE    → resultados_consejeras (lo agrega el gestor)
# ================================================


class PreparadorContexto:

    def preparar(self, paquete_capa4: dict) -> dict:
        """
        Toma el contexto_consejeras de Capa 4
        y lo enriquece con los campos que cada
        consejera espera específicamente.
        """
        try:
            return self._preparar_interno(paquete_capa4)
        except Exception as e:
            # Si algo falla, retornar el contexto base
            ctx = paquete_capa4.get('contexto_consejeras', {})
            ctx['_error_preparacion'] = str(e)
            return ctx

    def _preparar_interno(self, paquete_capa4: dict) -> dict:
        ctx_base   = paquete_capa4.get('contexto_consejeras', {})
        paquete_c3 = paquete_capa4.get('paquete_capa3', {})
        paquete_c2 = paquete_c3.get('paquete_capa2', {})
        paquete_c1 = paquete_c2.get('paquete_capa1', {})
        red_activa = paquete_c2.get('red_activa', {})

        # Comenzar con el contexto que armó Capa 4
        ctx = dict(ctx_base)

        # ── PARA SOMA ──────────────────────────────────
        # Soma.evaluar() busca contenido_normalizado y conceptos
        # directamente en el contexto
        ctx['contenido_normalizado'] = {
            'contenido_limpio':    paquete_c1.get('contenido_original', ''),
            'tipo_origen':         paquete_c1.get('tipo_origen', 'texto'),
            'contenido_original':  paquete_c1.get('contenido_original', ''),
            'exitoso':             paquete_c1.get('exitoso', True),
            'error':               paquete_c1.get('error', None),
        }
        ctx['conceptos']    = paquete_c1.get('conceptos', [])
        ctx['paquete_capa1'] = paquete_c1

        # ── PARA LYRA ──────────────────────────────────
        # Lyra.evaluar() hace: ids_activos & self.EMOCIONES_CRITICAS
        # necesita un SET, no una lista
        ids_lista = ctx_base.get('ids_activos', [])
        ctx['ids_activos'] = set(ids_lista) if isinstance(ids_lista, list) else ids_lista

        # ── PARA ECHO ──────────────────────────────────
        # Echo modifica comprension['profunda']['intencion_detectada']
        # in-place — necesita el dict real, no una copia
        # Ya viene de Capa 4 como dict mutable — verificar
        if 'comprension' not in ctx:
            ctx['comprension'] = paquete_c3.get('comprension', {})

        # ── PARA ECHO Y VEGA ───────────────────────────
        # Ambas necesitan red_activa
        if 'red_activa' not in ctx or not ctx.get('red_activa'):
            ctx['red_activa'] = red_activa

        # ── PARA VEGA ──────────────────────────────────
        # Vega ya recibe texto_original desde Capa 4
        # Verificar que está presente
        if not ctx.get('texto_original'):
            ctx['texto_original'] = paquete_c1.get('contenido_original', '')

        # ── PARA TODAS ─────────────────────────────────
        # Asegurar que comprension tiene todas las subcapas
        comprension = ctx.get('comprension', {})
        if 'contextual' not in comprension:
            comprension['contextual'] = {
                'tipo_mensaje':  ctx.get('tipo_mensaje', 'conversacional'),
                'nombre_usuario': ctx.get('nombre_usuario', 'Sebastian'),
                'hay_historial': ctx.get('hay_historial', False),
                'ids_activos':   list(ctx.get('ids_activos', [])),
                'certeza':       ctx.get('certeza_global', 0.5),
            }
        if 'profunda' not in comprension:
            comprension['profunda'] = {
                'intencion_detectada': ctx.get('intencion_detectada', 'conversar'),
                'necesidad_real':      ctx.get('necesidad_real', 'conexion_social'),
                'emocion_detectada':   ctx.get('emocion_detectada', 'neutra'),
                'tono_base':           ctx.get('tono_base', 'neutral'),
                'certeza':             ctx.get('certeza_global', 0.5),
                'puede_ejecutar':      ctx.get('puede_ejecutar', False),
                'nivel_comprension':   'profunda',
                'grounding_promedio':  ctx.get('grounding_promedio', 0.5),
            }
        if 'literal' not in comprension:
            comprension['literal'] = {
                'tiene_contenido': bool(ctx.get('texto_original', '')),
                'certeza':         ctx.get('certeza_global', 0.5),
                'texto_limpio':    ctx.get('texto_original', ''),
                'nodos_directos':  [
                    {'nodo_id': nid}
                    for nid in list(ctx.get('ids_activos', []))[:3]
                ],
            }
        ctx['comprension'] = comprension

        # ── METADATOS PARA DIAGNÓSTICO ─────────────────
        ctx['_preparado_por_capa5'] = True

        return ctx