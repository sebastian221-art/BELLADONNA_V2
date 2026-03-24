# biblioteca/red/activador.py
# ================================================
# ACTIVADOR corregido — retorna dict siempre
# Actualiza PerfilVida al activar
# ================================================

from typing import List
from biblioteca.red.red_neuronal import RedNeuronal


class NodoActivado:
    def __init__(self, nodo_id, energia, nivel, camino):
        self.nodo_id = nodo_id
        self.energia = energia
        self.nivel   = nivel
        self.camino  = camino

    def a_dict(self):
        return {
            'nodo_id': self.nodo_id,
            'energia': self.energia,
            'nivel':   self.nivel,
            'camino':  self.camino
        }


class ResultadoActivacion:
    def __init__(self):
        self.nodos_primarios:   List[NodoActivado] = []
        self.nodos_secundarios: List[NodoActivado] = []
        self.nodos_terciarios:  List[NodoActivado] = []
        self.energia_total:     float = 0.0

    def agregar(self, nodo):
        if nodo.nivel == 'primario':
            self.nodos_primarios.append(nodo)
        elif nodo.nivel == 'secundario':
            self.nodos_secundarios.append(nodo)
        else:
            self.nodos_terciarios.append(nodo)
        self.energia_total += nodo.energia

    def todos(self):
        return (self.nodos_primarios +
                self.nodos_secundarios +
                self.nodos_terciarios)

    def tiene_conocimiento(self):
        return len(self.nodos_primarios) > 0

    def nivel_conocimiento(self):
        if not self.nodos_primarios:
            return 0.0
        return min(1.0, sum(
            n.energia for n in self.nodos_primarios
        ) / len(self.nodos_primarios))

    def a_dict(self):
        """Siempre retorna dict — contrato con Capa 2."""
        return {
            'nodos_primarios':   [n.a_dict() for n in self.nodos_primarios],
            'nodos_secundarios': [n.a_dict() for n in self.nodos_secundarios],
            'nodos_terciarios':  [n.a_dict() for n in self.nodos_terciarios],
            'energia_total':     self.energia_total,
            'nivel_conocimiento': self.nivel_conocimiento(),
            'tiene_conocimiento': self.tiene_conocimiento(),
            'total_activados':   len(self.todos()),
        }


class Activador:

    ENERGIA_INICIAL       = 1.0
    FACTOR_DECAY_SEC      = 0.75
    FACTOR_DECAY_TER      = 0.55
    UMBRAL_ACTIVACION     = 0.15
    MAX_NODOS_SECUNDARIOS = 15
    MAX_NODOS_TERCIARIOS  = 10

    def __init__(self, red: RedNeuronal):
        self.red = red

    def activar(
        self,
        conceptos_entrada: List[dict],
        contexto: str = ''
    ) -> dict:
        """
        SIEMPRE retorna dict.
        Nunca retorna ResultadoActivacion directamente.
        """
        resultado          = ResultadoActivacion()
        nodos_ya_activados = set()

        # ---- PRIMARIOS ----
        for concepto in conceptos_entrada:
            cid       = concepto.get('id', '')
            grounding = concepto.get('grounding', 0.5)
            if not cid:
                continue

            neurona = self.red.obtener_neurona(cid)
            energia = self.ENERGIA_INICIAL * grounding

            nodo = NodoActivado(cid, energia, 'primario', [cid])
            resultado.agregar(nodo)
            nodos_ya_activados.add(cid)

            if neurona:
                self.red.activar_nodo(cid, contexto, True)
                self._actualizar_vida(neurona, energia, 'primario')

        # ---- SECUNDARIOS ----
        candidatos_sec = []
        for np in resultado.nodos_primarios:
            for vid, peso in self.red.obtener_vecinos(
                np.nodo_id, peso_minimo=self.UMBRAL_ACTIVACION
            ):
                if vid in nodos_ya_activados:
                    continue
                e = np.energia * self.FACTOR_DECAY_SEC * peso
                if e >= self.UMBRAL_ACTIVACION:
                    candidatos_sec.append((vid, e, np.nodo_id))

        candidatos_sec.sort(key=lambda x: x[1], reverse=True)
        for vid, e, origen in candidatos_sec[:self.MAX_NODOS_SECUNDARIOS]:
            if vid in nodos_ya_activados:
                continue
            nodo = NodoActivado(vid, e, 'secundario', [origen, vid])
            resultado.agregar(nodo)
            nodos_ya_activados.add(vid)
            neurona = self.red.obtener_neurona(vid)
            if neurona:
                self.red.activar_nodo(vid, contexto, True)
                self._actualizar_vida(neurona, e, 'secundario')

        # ---- TERCIARIOS ----
        candidatos_ter = []
        for ns in resultado.nodos_secundarios:
            for vid, peso in self.red.obtener_vecinos(
                ns.nodo_id, peso_minimo=0.5
            ):
                if vid in nodos_ya_activados:
                    continue
                e = ns.energia * self.FACTOR_DECAY_TER * peso
                if e >= self.UMBRAL_ACTIVACION:
                    candidatos_ter.append((vid, e, ns.nodo_id))

        candidatos_ter.sort(key=lambda x: x[1], reverse=True)
        for vid, e, origen in candidatos_ter[:self.MAX_NODOS_TERCIARIOS]:
            if vid in nodos_ya_activados:
                continue
            camino = self._camino(resultado, origen, vid)
            nodo   = NodoActivado(vid, e, 'terciario', camino)
            resultado.agregar(nodo)
            nodos_ya_activados.add(vid)
            neurona = self.red.obtener_neurona(vid)
            if neurona:
                self._actualizar_vida(neurona, e, 'terciario')

        # SIEMPRE retornar dict
        return resultado.a_dict()

    def _actualizar_vida(self, neurona, energia: float, nivel: str):
        """Actualiza el PerfilVida al activar. La vida crece con el uso."""
        try:
            perfil = neurona.nucleo.datos_extra.get('_perfil_obj')
            if not perfil:
                return
            intensidad = energia * 0.05
            if nivel == 'primario':
                perfil.evento('proposito_cumplido', intensidad)
                perfil.emocional.presencia_emocional = min(1.0,
                    perfil.emocional.presencia_emocional + intensidad)
                perfil.autoconocimiento.conocimiento_capacidades = min(1.0,
                    perfil.autoconocimiento.conocimiento_capacidades + intensidad * 0.5)
            elif nivel == 'secundario':
                perfil.evento('vinculo_fortalecido', intensidad * 0.5)
                perfil.relaciones.interdependencia = min(1.0,
                    perfil.relaciones.interdependencia + intensidad * 0.3)
            elif nivel == 'terciario':
                perfil.crecimiento.integracion_experiencia = min(1.0,
                    perfil.crecimiento.integracion_experiencia + intensidad * 0.2)

            neurona.nucleo.datos_extra['vitalidad']  = perfil.vitalidad()
            neurona.nucleo.datos_extra['nivel_vida'] = perfil.nivel_vida()
        except Exception:
            pass

    def _camino(self, resultado, origen_sec, destino):
        for ns in resultado.nodos_secundarios:
            if ns.nodo_id == origen_sec:
                return ns.camino + [destino]
        return [origen_sec, destino]

    def activar_por_ids(self, nodo_ids, contexto=''):
        conceptos = [
            {'id': nid, 'grounding': self._grounding(nid)}
            for nid in nodo_ids
        ]
        return self.activar(conceptos, contexto)

    def _grounding(self, nodo_id):
        n = self.red.obtener_neurona(nodo_id)
        return n.grounding_efectivo() if n else 0.5