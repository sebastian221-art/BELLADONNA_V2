# capas/capa9/actualizador_zona.py
# ================================================
# ACTUALIZADOR DE ZONA — Capa 9
#
# Ordena los fragmentos en la zona de
# desconocimiento por prioridad de resolución.
# Los que más veces se pidieron → primero.
# No los resuelve — los prepara para cuando
# lleguen las habilidades.
# ================================================


class ActualizadorZona:

    def actualizar(self) -> dict:
        """
        Ordena la zona de desconocimiento
        y retorna estadísticas de lo que hay.
        """
        try:
            from biblioteca.zona_desconocimiento.zona import ZonaDesconocimiento
            zona = ZonaDesconocimiento.obtener()

            pendientes = zona.obtener_pendientes()
            if not pendientes:
                return {'actualizado': False, 'pendientes': 0}

            # Separar por tipo y ordenar por intentos
            habilidades = sorted(
                [p for p in pendientes if p.get('tipo') == 'habilidad'],
                key=lambda x: x.get('intentos_resolucion', 0),
                reverse=True
            )
            conceptos = sorted(
                [p for p in pendientes if p.get('tipo') == 'concepto'],
                key=lambda x: x.get('intentos_resolucion', 0),
                reverse=True
            )

            # Habilidades más pedidas — prioridad alta
            habilidades_prioritarias = [
                h.get('inferencia', '').replace('necesita_habilidad:', '')
                for h in habilidades[:3]
                if h.get('inferencia')
            ]

            return {
                'actualizado':              True,
                'total_pendientes':         len(pendientes),
                'habilidades_pendientes':   len(habilidades),
                'conceptos_pendientes':     len(conceptos),
                'habilidades_prioritarias': list(set(habilidades_prioritarias)),
                'conceptos_frecuentes':     [c.get('fragmento','') for c in conceptos[:3]],
            }

        except Exception as e:
            return {'actualizado': False, 'error': str(e)}