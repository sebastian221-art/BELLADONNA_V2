# capas/capa3/detector_gaps.py
# ================================================
# DETECTOR DE GAPS
# Qué le falta a Bell para comprender al 100%
# ================================================


class DetectorGaps:

    def detectar(
        self,
        comprension: dict,
        red_activa: dict,
        desconocidos: list
    ) -> list:
        """
        Detecta qué partes no pudo comprender Bell.
        """
        gaps = []

        # Gaps de la Capa 1 — palabras desconocidas
        for desc in desconocidos:
            gaps.append({
                'tipo':        'concepto',
                'descripcion': desc.get('fragmento', ''),
                'critico':     False,
                'origen':      'capa1',
                'destino':     'zona_desconocimiento'
            })

        # Gap si no hubo activación primaria
        primarios = red_activa.get('nodos_primarios', [])
        if not primarios:
            gaps.append({
                'tipo':        'conocimiento',
                'descripcion': 'Sin activación primaria en la red',
                'critico':     False,
                'origen':      'capa2',
                'destino':     'zona_desconocimiento'
            })

        # Gap si la intención es desconocida
        intencion = comprension.get(
            'profunda', {}
        ).get('intencion_detectada', 'desconocida')

        if intencion == 'desconocida':
            gaps.append({
                'tipo':        'intencion',
                'descripcion': 'Intención del mensaje no clara',
                'critico':     False,
                'origen':      'capa3',
                'destino':     'preguntar_sebastian'
            })

        return gaps