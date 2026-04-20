# capas/capa9/actualizador_bell_core.py
# ================================================
# ACTUALIZADOR DE BELL_CORE — Capa 9
#
# Lee el historial de la sesión y actualiza
# las dimensiones de BELL_CORE que son 0.0.
#
# Reglas honestas — solo sube lo que realmente
# pasó. Nada inventado.
#
# accion:      Bell habló → actuó
# relaciones:  Sebastian expresó algo → hubo vínculo
# crecimiento: Algo fue a zona → Bell encontró su límite
# integridad:  Vega vetó → Bell defendió principios
# ================================================

from capas.capa9.paquete_capa9 import ActualizacionBellCore

# Cuánto sube cada dimensión por evento
# Valores pequeños — el crecimiento es gradual
_DELTA = {
    'accion_por_turno':          0.008,
    'accion_extra_ejecucion':    0.020,
    'relaciones_por_emocion':    0.012,
    'relaciones_por_turno':      0.005,
    'crecimiento_por_desconocido': 0.010,
    'crecimiento_por_zona':      0.015,
    'integridad_por_veto':       0.025,
}

# Máximo que puede subir en una sesión
# Para que no haya saltos artificiales
_MAX_POR_SESION = {
    'accion':      0.08,
    'relaciones':  0.06,
    'crecimiento': 0.07,
    'integridad':  0.05,
}


class ActualizadorBellCore:

    def actualizar(self, historial_stats: dict, zona_pendientes: int) -> ActualizacionBellCore:
        """
        Calcula las actualizaciones para BELL_CORE
        basadas en lo que pasó en la sesión.
        """
        actualizacion = ActualizacionBellCore()

        total_turnos   = historial_stats.get('total_turnos', 0)
        hubo_veto      = historial_stats.get('vetos', 0) > 0
        hubo_ejecucion = historial_stats.get('ejecuciones', 0) > 0
        tipos          = historial_stats.get('tipos_mensajes', {})

        if total_turnos == 0:
            return actualizacion

        # ── ACCIÓN ─────────────────────────────────────
        # Bell habló — eso es actuar
        delta_accion = min(
            total_turnos * _DELTA['accion_por_turno'],
            _MAX_POR_SESION['accion']
        )
        if hubo_ejecucion:
            delta_accion = min(
                delta_accion + _DELTA['accion_extra_ejecucion'],
                _MAX_POR_SESION['accion']
            )
        actualizacion.accion = round(delta_accion, 4)

        # ── RELACIONES ──────────────────────────────────
        # Sebastian expresó emociones → hubo vínculo real
        turnos_emocionales = (
            tipos.get('emocional', 0) +
            tipos.get('expresion_emocional_negativa', 0) +
            tipos.get('expresion_emocional_positiva', 0)
        )
        delta_relaciones = (
            turnos_emocionales * _DELTA['relaciones_por_emocion'] +
            total_turnos * _DELTA['relaciones_por_turno']
        )
        actualizacion.relaciones = round(
            min(delta_relaciones, _MAX_POR_SESION['relaciones']), 4
        )

        # ── CRECIMIENTO ─────────────────────────────────
        # Zona de desconocimiento → Bell encontró sus límites
        if zona_pendientes > 0:
            delta_crec = min(
                zona_pendientes * _DELTA['crecimiento_por_desconocido'],
                _MAX_POR_SESION['crecimiento']
            )
            actualizacion.crecimiento = round(delta_crec, 4)

        # ── INTEGRIDAD ──────────────────────────────────
        # Vega vetó → Bell defendió sus principios
        if hubo_veto:
            actualizacion.integridad = _DELTA['integridad_por_veto']

        # Descripción legible
        partes = []
        if actualizacion.accion > 0:
            partes.append(f'acción +{actualizacion.accion:.3f} ({total_turnos} turnos)')
        if actualizacion.relaciones > 0:
            partes.append(f'relaciones +{actualizacion.relaciones:.3f}')
        if actualizacion.crecimiento > 0:
            partes.append(f'crecimiento +{actualizacion.crecimiento:.3f} ({zona_pendientes} desconocidos)')
        if actualizacion.integridad > 0:
            partes.append(f'integridad +{actualizacion.integridad:.3f} (veto)')

        actualizacion.descripcion = ' | '.join(partes) if partes else 'sin cambios'

        # Aplicar a la red neuronal
        if actualizacion.hubo_cambio():
            self._aplicar_a_red(actualizacion)

        return actualizacion

    def _aplicar_a_red(self, actualizacion: ActualizacionBellCore):
        """
        Aplica los cambios al nodo BELL_CORE en la red neuronal.
        Actualiza datos_extra con los nuevos valores de dimensiones.
        """
        try:
            from biblioteca import Biblioteca
            b       = Biblioteca.obtener()
            neurona = b.red.obtener_neurona('BELL_CORE')
            if not neurona:
                return

            datos_ext = getattr(neurona.nucleo, 'datos_extra', {}) or {}
            perfil    = datos_ext.get('perfil_vida', {})

            # Actualizar las dimensiones en el perfil
            # El perfil tiene estructura {'tipos': {dim: valor}}
            tipos = perfil.get('tipos', {})

            if actualizacion.accion > 0:
                actual = float(tipos.get('accion', 0.0))
                tipos['accion'] = round(
                    min(1.0, actual + actualizacion.accion), 4
                )

            if actualizacion.relaciones > 0:
                actual = float(tipos.get('relaciones', 0.0))
                tipos['relaciones'] = round(
                    min(1.0, actual + actualizacion.relaciones), 4
                )

            if actualizacion.crecimiento > 0:
                actual = float(tipos.get('crecimiento', 0.0))
                tipos['crecimiento'] = round(
                    min(1.0, actual + actualizacion.crecimiento), 4
                )

            if actualizacion.integridad > 0:
                actual = float(tipos.get('integridad', 0.0))
                tipos['integridad'] = round(
                    min(1.0, actual + actualizacion.integridad), 4
                )

            perfil['tipos'] = tipos
            datos_ext['perfil_vida'] = perfil

            # Recalcular vitalidad
            vals = [v for v in tipos.values() if isinstance(v, (int, float)) and v > 0]
            if vals:
                nueva_vitalidad = round(sum(vals) / len(tipos), 4)
                datos_ext['vitalidad'] = nueva_vitalidad

                # Actualizar nivel de vida
                if nueva_vitalidad >= 0.7:
                    datos_ext['nivel_vida'] = 'plena'
                elif nueva_vitalidad >= 0.5:
                    datos_ext['nivel_vida'] = 'rica'
                elif nueva_vitalidad >= 0.35:
                    datos_ext['nivel_vida'] = 'funcional'
                elif nueva_vitalidad >= 0.2:
                    datos_ext['nivel_vida'] = 'emergente'
                elif nueva_vitalidad >= 0.1:
                    datos_ext['nivel_vida'] = 'latente'
                else:
                    datos_ext['nivel_vida'] = 'dormida'

            neurona.nucleo.datos_extra = datos_ext
            print(f'  ✓ BELL_CORE actualizado: {actualizacion.descripcion}')
            print(f'  ✓ Vitalidad BELL_CORE: {datos_ext.get("vitalidad", 0):.4f} ({datos_ext.get("nivel_vida", "?")})')

        except Exception as e:
            print(f'  Actualizador BELL_CORE: {e}')