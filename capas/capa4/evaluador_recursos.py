# capas/capa4/evaluador_recursos.py
# ================================================
# EVALUADOR DE RECURSOS — Capa 4
# Responde: ¿qué tiene Bell para responder?
# Lee la red activa de Capa 2 y los conceptos
# enriquecidos para saber con qué cuenta Bell.
# ================================================

from capas.capa4.paquete_capa4 import RecursosDisponibles


class EvaluadorRecursos:

    def evaluar(self, paquete_capa3: dict) -> RecursosDisponibles:
        """
        Evalúa los recursos disponibles de Bell
        para responder a este mensaje.
        """
        try:
            return self._evaluar_interno(paquete_capa3)
        except Exception as e:
            return RecursosDisponibles(
                nodos_activos=0,
                vocabulario_suficiente=False,
                gaps_criticos=[f'Error evaluando recursos: {e}']
            )

    def _evaluar_interno(self, paquete_capa3: dict) -> RecursosDisponibles:
        paquete_c2 = paquete_capa3.get('paquete_capa2', {})
        paquete_c1 = paquete_c2.get('paquete_capa1', {})

        red_activa          = paquete_c2.get('red_activa', {})
        conceptos_enriq     = paquete_c2.get('conceptos_enriquecidos', [])
        nivel_conocimiento  = paquete_c2.get('nivel_conocimiento', {})
        gaps_capa3          = paquete_capa3.get('gaps', [])

        # Nodos activos
        primarios   = red_activa.get('nodos_primarios',   [])
        secundarios = red_activa.get('nodos_secundarios', [])
        terciarios  = red_activa.get('nodos_terciarios',  [])
        total = (
            len(primarios) + len(secundarios) + len(terciarios)
        )

        # Habilidades disponibles
        habilidades_ids = []
        todos_nodos = primarios + secundarios
        for n in todos_nodos:
            nid = n.get('nodo_id', '') if isinstance(n, dict) else ''
            if 'HABILIDAD' in nid.upper():
                habilidades_ids.append(nid)

        # Grounding promedio
        grounding_prom = nivel_conocimiento.get('grounding_promedio', 0.0)
        if not grounding_prom and conceptos_enriq:
            vals = [
                c.get('grounding_efectivo', c.get('grounding', 0.5))
                for c in conceptos_enriq
            ]
            grounding_prom = round(sum(vals) / len(vals), 3) if vals else 0.0

        # Vocabulario suficiente
        desconocidos = paquete_c1.get('desconocidos', [])
        conceptos    = paquete_c1.get('conceptos', [])
        total_tokens = len(conceptos) + len(desconocidos)
        vocab_ok = (
            len(desconocidos) == 0 or
            (total_tokens > 0 and len(conceptos) / total_tokens >= 0.5)
        )

        # Gaps críticos
        gaps_criticos = [
            g.get('descripcion', str(g))
            for g in gaps_capa3
            if isinstance(g, dict) and g.get('critico', False)
        ]

        return RecursosDisponibles(
            nodos_activos=total,
            nodos_primarios=len(primarios),
            nodos_secundarios=len(secundarios),
            tiene_habilidades=len(habilidades_ids) > 0,
            habilidades_ids=habilidades_ids,
            grounding_promedio=grounding_prom,
            vocabulario_suficiente=vocab_ok,
            gaps_criticos=gaps_criticos,
        )