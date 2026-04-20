# capas/capa9/actualizador_bell_core.py
# ================================================
# ACTUALIZADOR DE BELL_CORE — Capa 9
# Logs controlados por BELL_DEBUG=1
# ================================================

import os
from capas.capa9.paquete_capa9 import ActualizacionBellCore

_DEBUG = os.getenv('BELL_DEBUG', '0') == '1'

_DELTA = {
    'accion_por_turno':            0.008,
    'accion_extra_ejecucion':      0.020,
    'relaciones_por_emocion':      0.012,
    'relaciones_por_turno':        0.005,
    'crecimiento_por_desconocido': 0.010,
    'crecimiento_por_zona':        0.015,
    'integridad_por_veto':         0.025,
}

_MAX_POR_SESION = {
    'accion':      0.08,
    'relaciones':  0.06,
    'crecimiento': 0.07,
    'integridad':  0.05,
}


class ActualizadorBellCore:

    def actualizar(self, historial_stats: dict, zona_pendientes: int) -> ActualizacionBellCore:
        actualizacion = ActualizacionBellCore()

        total_turnos   = historial_stats.get('total_turnos', 0)
        hubo_veto      = historial_stats.get('vetos', 0) > 0
        hubo_ejecucion = historial_stats.get('ejecuciones', 0) > 0
        tipos          = historial_stats.get('tipos_mensajes', {})

        if total_turnos == 0:
            return actualizacion

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

        if zona_pendientes > 0:
            actualizacion.crecimiento = round(
                min(
                    zona_pendientes * _DELTA['crecimiento_por_desconocido'],
                    _MAX_POR_SESION['crecimiento']
                ), 4
            )

        if hubo_veto:
            actualizacion.integridad = _DELTA['integridad_por_veto']

        partes = []
        if actualizacion.accion > 0:
            partes.append(f'accion +{actualizacion.accion:.3f}')
        if actualizacion.relaciones > 0:
            partes.append(f'relaciones +{actualizacion.relaciones:.3f}')
        if actualizacion.crecimiento > 0:
            partes.append(f'crecimiento +{actualizacion.crecimiento:.3f}')
        if actualizacion.integridad > 0:
            partes.append(f'integridad +{actualizacion.integridad:.3f}')

        actualizacion.descripcion = ' | '.join(partes) if partes else 'sin cambios'

        if actualizacion.hubo_cambio():
            self._aplicar_a_red(actualizacion)

        return actualizacion

    def _aplicar_a_red(self, actualizacion: ActualizacionBellCore):
        try:
            from biblioteca import Biblioteca
            b       = Biblioteca.obtener()
            neurona = b.red.obtener_neurona('BELL_CORE')
            if not neurona:
                return

            datos_ext = getattr(neurona.nucleo, 'datos_extra', {}) or {}
            perfil    = datos_ext.get('perfil_vida', {})
            tipos     = perfil.get('tipos', {})

            for campo, delta in [
                ('accion',     actualizacion.accion),
                ('relaciones', actualizacion.relaciones),
                ('crecimiento',actualizacion.crecimiento),
                ('integridad', actualizacion.integridad),
            ]:
                if delta > 0:
                    actual = float(tipos.get(campo, 0.0))
                    tipos[campo] = round(min(1.0, actual + delta), 4)

            perfil['tipos']         = tipos
            datos_ext['perfil_vida'] = perfil

            vals = [v for v in tipos.values() if isinstance(v, (int, float)) and v > 0]
            if vals:
                nueva_vitalidad = round(sum(vals) / len(tipos), 4)
                datos_ext['vitalidad'] = nueva_vitalidad
                if   nueva_vitalidad >= 0.7:  datos_ext['nivel_vida'] = 'plena'
                elif nueva_vitalidad >= 0.5:  datos_ext['nivel_vida'] = 'rica'
                elif nueva_vitalidad >= 0.35: datos_ext['nivel_vida'] = 'funcional'
                elif nueva_vitalidad >= 0.2:  datos_ext['nivel_vida'] = 'emergente'
                elif nueva_vitalidad >= 0.1:  datos_ext['nivel_vida'] = 'latente'
                else:                         datos_ext['nivel_vida'] = 'dormida'

            neurona.nucleo.datos_extra = datos_ext

            # Solo imprimir si BELL_DEBUG=1
            if _DEBUG:
                print(f'  C9 BELL_CORE: {actualizacion.descripcion}')
                print(f'  C9 vitalidad: {datos_ext.get("vitalidad", 0):.4f} ({datos_ext.get("nivel_vida","?")})')

        except Exception as e:
            if _DEBUG:
                print(f'  C9 BELL_CORE error: {e}')