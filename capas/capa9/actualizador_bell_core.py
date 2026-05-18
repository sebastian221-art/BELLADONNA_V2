# capas/capa9/actualizador_bell_core.py
# ================================================
# ACTUALIZADOR DE BELL_CORE — v2
# v2: Log siempre visible cuando BELL_CORE sube
# ================================================

from capas.capa9.paquete_capa9 import ActualizacionBellCore

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

    def actualizar(
        self, historial_stats: dict, zona_pendientes: int
    ) -> ActualizacionBellCore:

        act = ActualizacionBellCore()
        total          = historial_stats.get('total_turnos', 0)
        hubo_veto      = historial_stats.get('vetos', 0) > 0
        hubo_ejecucion = historial_stats.get('ejecuciones', 0) > 0
        tipos          = historial_stats.get('tipos_mensajes', {})

        if total == 0:
            return act

        # Acción
        delta_accion = min(
            total * _DELTA['accion_por_turno'], _MAX_POR_SESION['accion']
        )
        if hubo_ejecucion:
            delta_accion = min(
                delta_accion + _DELTA['accion_extra_ejecucion'],
                _MAX_POR_SESION['accion']
            )
        act.accion = round(delta_accion, 4)

        # Relaciones
        emo = (tipos.get('emocional', 0) +
               tipos.get('expresion_emocional_negativa', 0) +
               tipos.get('expresion_emocional_positiva', 0))
        act.relaciones = round(min(
            emo * _DELTA['relaciones_por_emocion'] +
            total * _DELTA['relaciones_por_turno'],
            _MAX_POR_SESION['relaciones']
        ), 4)

        # Crecimiento
        if zona_pendientes > 0:
            act.crecimiento = round(min(
                zona_pendientes * _DELTA['crecimiento_por_desconocido'],
                _MAX_POR_SESION['crecimiento']
            ), 4)

        # Integridad
        if hubo_veto:
            act.integridad = _DELTA['integridad_por_veto']

        # Descripción
        partes = []
        if act.accion     > 0: partes.append(f'accion+{act.accion:.3f}')
        if act.relaciones > 0: partes.append(f'relaciones+{act.relaciones:.3f}')
        if act.crecimiento> 0: partes.append(f'crecimiento+{act.crecimiento:.3f}')
        if act.integridad > 0: partes.append(f'integridad+{act.integridad:.3f}')
        act.descripcion = ' | '.join(partes) if partes else 'sin cambios'

        if act.hubo_cambio():
            self._aplicar_a_red(act)

        return act

    def _aplicar_a_red(self, act: ActualizacionBellCore):
        try:
            from biblioteca import Biblioteca
            neurona = Biblioteca.obtener().red.obtener_neurona('BELL_CORE')
            if not neurona:
                return

            datos_ext = getattr(neurona.nucleo, 'datos_extra', {}) or {}
            perfil    = datos_ext.get('perfil_vida', {})
            tipos     = perfil.get('tipos', {})

            for campo, delta in [
                ('accion',      act.accion),
                ('relaciones',  act.relaciones),
                ('crecimiento', act.crecimiento),
                ('integridad',  act.integridad),
            ]:
                if delta > 0:
                    tipos[campo] = round(min(1.0, float(tipos.get(campo, 0.0)) + delta), 4)

            perfil['tipos']          = tipos
            datos_ext['perfil_vida'] = perfil

            vals = [v for v in tipos.values() if isinstance(v, (int, float)) and v > 0]
            if vals:
                vitalidad = round(sum(vals) / len(tipos), 4)
                datos_ext['vitalidad'] = vitalidad
                nivel = ('plena'     if vitalidad >= 0.7  else
                         'rica'      if vitalidad >= 0.5  else
                         'funcional' if vitalidad >= 0.35 else
                         'emergente' if vitalidad >= 0.2  else
                         'latente'   if vitalidad >= 0.1  else 'dormida')
                datos_ext['nivel_vida'] = nivel
                # Siempre visible — es el latido de Bell
                print(f'  C9 vitalidad: {vitalidad:.4f} ({nivel})')

            neurona.nucleo.datos_extra = datos_ext

        except Exception as e:
            print(f'  C9 BELL_CORE error: {e}')