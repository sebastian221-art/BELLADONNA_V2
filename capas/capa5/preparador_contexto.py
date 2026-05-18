# capas/capa5/preparador_contexto.py
# ================================================
# PREPARADOR DE CONTEXTO — v2
#
# Cada consejera espera campos específicos.
# Este módulo hace el mapeo exacto.
#
# v2:
# — Pasa motor_sugerido, contiene_codigo,
#   complejidad, modo_mental a las consejeras
# — Las consejeras ahora saben qué motor usar
#   y si el mensaje tiene código
# ================================================


class PreparadorContexto:

    def preparar(self, paquete_capa4: dict) -> dict:
        try:
            return self._preparar_interno(paquete_capa4)
        except Exception as e:
            ctx = paquete_capa4.get('contexto_consejeras', {})
            ctx['_error_preparacion'] = str(e)
            return ctx

    def _preparar_interno(self, paquete_capa4: dict) -> dict:
        ctx_base   = paquete_capa4.get('contexto_consejeras', {})
        paquete_c3 = paquete_capa4.get('paquete_capa3', {})
        paquete_c2 = paquete_c3.get('paquete_capa2', {})
        paquete_c1 = paquete_c2.get('paquete_capa1', {})
        red_activa = paquete_c2.get('red_activa', {})

        ctx = dict(ctx_base)

        # ── Campos v2 de C4 ───────────────────────────────
        motor_sugerido   = paquete_capa4.get('motor_sugerido', 'local')
        contiene_codigo  = paquete_capa4.get('contiene_codigo', False)
        lenguaje_codigo  = paquete_capa4.get('lenguaje_codigo', 'ninguno')
        complejidad      = paquete_capa4.get('complejidad', 'simple')
        modo_mental      = paquete_capa4.get('modo_mental', 'social')
        fuente_clasif    = paquete_capa4.get('fuente_clasificacion', 'patrones')

        # Inyectar en contexto para que consejeras los lean
        ctx['motor_sugerido']   = motor_sugerido
        ctx['contiene_codigo']  = contiene_codigo
        ctx['lenguaje_codigo']  = lenguaje_codigo
        ctx['complejidad']      = complejidad
        ctx['modo_mental']      = modo_mental
        ctx['fuente_clasif']    = fuente_clasif

        # ── Para SOMA ─────────────────────────────────────
        ctx['contenido_normalizado'] = {
            'contenido_limpio':   paquete_c1.get('contenido_original', ''),
            'tipo_origen':        paquete_c1.get('tipo_origen', 'texto'),
            'contenido_original': paquete_c1.get('contenido_original', ''),
            'exitoso':            paquete_c1.get('exitoso', True),
            'error':              paquete_c1.get('error', None),
        }
        ctx['conceptos']     = paquete_c1.get('conceptos', [])
        ctx['paquete_capa1'] = paquete_c1

        # ── Para LYRA ─────────────────────────────────────
        # Lyra hace: ids_activos & self.EMOCIONES_CRITICAS → necesita SET
        ids_lista = ctx_base.get('ids_activos', [])
        ctx['ids_activos'] = set(ids_lista) if isinstance(ids_lista, list) else ids_lista

        # ── Para ECHO ─────────────────────────────────────
        if 'comprension' not in ctx:
            ctx['comprension'] = paquete_c3.get('comprension', {})

        # ── Para ECHO y VEGA ──────────────────────────────
        if 'red_activa' not in ctx or not ctx.get('red_activa'):
            ctx['red_activa'] = red_activa

        # ── Para VEGA ─────────────────────────────────────
        if not ctx.get('texto_original'):
            ctx['texto_original'] = paquete_c1.get('contenido_original', '')

        # ── Garantizar comprensión completa ───────────────
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
                # v2
                'motor_sugerido':      motor_sugerido,
                'contiene_codigo':     contiene_codigo,
                'modo_mental':         modo_mental,
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

        ctx['comprension']         = comprension
        ctx['_preparado_por_capa5'] = True

        return ctx