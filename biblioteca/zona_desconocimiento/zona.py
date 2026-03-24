# biblioteca/zona_desconocimiento/zona.py
# ================================================
# ZONA DE DESCONOCIMIENTO
# Donde viven los nodos incompletos
# Todo lo que Bell no pudo entender
# o no tiene todavía
# Tiene su propio ciclo de vida completo
# ================================================

import time
from typing import List, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class NodoIncompleto:
    """
    Un concepto, habilidad o contexto
    que Bell no pudo procesar completamente.
    """
    fragmento: str              # Lo que llegó
    tipo: str                   # concepto/habilidad/contexto/riesgo
    inferencia: Optional[str]   # Lo que Bell intentó inferir
    timestamp: float = field(default_factory=time.time)
    intentos_resolucion: int = 0
    resuelto: bool = False
    como_se_resolvio: Optional[str] = None

    # Protocolo que se debe ejecutar
    # buscar/preguntar/evaluar/ignorar
    protocolo: str = 'buscar'

    def a_dict(self) -> dict:
        return {
            'fragmento':           self.fragmento,
            'tipo':                self.tipo,
            'inferencia':          self.inferencia,
            'timestamp':           self.timestamp,
            'intentos_resolucion': self.intentos_resolucion,
            'resuelto':            self.resuelto,
            'protocolo':           self.protocolo
        }


class ZonaDesconocimiento:
    """
    La zona donde Bell guarda lo que no sabe.

    No es un archivo estático — es una zona activa.
    Cada elemento tiene un protocolo de resolución.
    Cuando se resuelve se integra a la red principal.

    Singleton — una sola instancia por sesión.
    """

    _instancia = None

    def __init__(self):
        self._nodos: Dict[str, NodoIncompleto] = {}
        self._resueltos_hoy: List[str] = []
        self._red = None  # Se inyecta después

    @classmethod
    def obtener(cls):
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def configurar_red(self, red_neuronal):
        """Inyecta la red neuronal para integrar
        los nodos resueltos."""
        self._red = red_neuronal

    # ==========================================
    # AGREGAR DESCONOCIDOS
    # ==========================================

    def agregar(
        self,
        fragmento: str,
        tipo: str = 'concepto',
        inferencia: Optional[str] = None
    ) -> str:
        """
        Agrega algo que Bell no pudo entender.
        Retorna el ID del nodo incompleto.
        """
        # Normalizar el fragmento como ID
        nodo_id = f'DESC_{fragmento.upper().replace(" ", "_")}'

        # Si ya existe solo incrementar intentos
        if nodo_id in self._nodos:
            self._nodos[nodo_id].intentos_resolucion += 1
            return nodo_id

        # Determinar el protocolo según el tipo
        protocolo = self._determinar_protocolo(tipo, fragmento)

        nodo = NodoIncompleto(
            fragmento=fragmento,
            tipo=tipo,
            inferencia=inferencia,
            protocolo=protocolo
        )

        self._nodos[nodo_id] = nodo
        return nodo_id

    def agregar_desde_capa1(self, desconocidos: List[dict]):
        """
        Procesa los desconocidos que vienen
        del PaqueteCapa1.
        """
        for desc in desconocidos:
            self.agregar(
                fragmento=desc.get('fragmento', ''),
                tipo=desc.get('tipo', 'concepto'),
                inferencia=desc.get('inferencia')
            )

    # ==========================================
    # RESOLVER DESCONOCIDOS
    # ==========================================

    def resolver(
        self,
        nodo_id: str,
        solucion: dict,
        como: str = 'aprendido'
    ) -> bool:
        """
        Marca un nodo incompleto como resuelto
        e intenta integrarlo a la red principal.
        """
        nodo = self._nodos.get(nodo_id)
        if not nodo:
            return False

        nodo.resuelto = True
        nodo.como_se_resolvio = como

        # Integrar a la red si hay solución
        if self._red and solucion:
            self._integrar_a_red(nodo, solucion)
            self._resueltos_hoy.append(nodo_id)

        return True

    def _integrar_a_red(
        self, nodo: NodoIncompleto, solucion: dict
    ):
        """
        Integra un nodo resuelto a la red neuronal.
        """
        try:
            from biblioteca.conectador.conectador_inteligente import (
                ConectadorInteligente
            )
            conectador = ConectadorInteligente(self._red)

            grounding = solucion.get('grounding', 0.5)
            tipo = solucion.get('tipo', 'concepto')

            conectador.integrar_concepto_del_vocabulario(
                concepto_id=solucion.get(
                    'id',
                    f'APRENDIDO_{nodo.fragmento.upper()}'
                ),
                grounding=grounding,
                tipo=tipo
            )
        except Exception as e:
            print(f'Error integrando a red: {e}')

    # ==========================================
    # CONSULTAR
    # ==========================================

    def obtener_pendientes(self) -> List[dict]:
        """
        Retorna todos los nodos sin resolver.
        """
        return [
            nodo.a_dict()
            for nodo in self._nodos.values()
            if not nodo.resuelto
        ]

    def obtener_por_tipo(self, tipo: str) -> List[dict]:
        """
        Retorna nodos pendientes de un tipo.
        """
        return [
            nodo.a_dict()
            for nodo in self._nodos.values()
            if nodo.tipo == tipo and not nodo.resuelto
        ]

    def tiene_pendientes(self) -> bool:
        return any(
            not nodo.resuelto
            for nodo in self._nodos.values()
        )

    def cantidad_pendientes(self) -> int:
        return sum(
            1 for nodo in self._nodos.values()
            if not nodo.resuelto
        )

    def obtener_estado(self) -> dict:
        return {
            'total':           len(self._nodos),
            'pendientes':      self.cantidad_pendientes(),
            'resueltos_hoy':   len(self._resueltos_hoy),
            'por_tipo':        self._contar_por_tipo()
        }

    def _contar_por_tipo(self) -> dict:
        conteo = {}
        for nodo in self._nodos.values():
            if not nodo.resuelto:
                tipo = nodo.tipo
                conteo[tipo] = conteo.get(tipo, 0) + 1
        return conteo

    def _determinar_protocolo(
        self, tipo: str, fragmento: str
    ) -> str:
        """
        Determina qué hacer con este desconocido.
        """
        if tipo == 'riesgo':
            return 'evaluar'
        if tipo == 'habilidad':
            return 'evaluar'
        if tipo == 'contexto':
            return 'preguntar'
        # Conceptos desconocidos — buscar
        return 'buscar'