# biblioteca/red/red_neuronal.py
# ================================================
# RED NEURONAL — El tejido vivo de Belladonna
# Almacena todos los nodos y conexiones
# Permite agregar, buscar, conectar
# Es la infraestructura pura — no sabe
# nada específico de Bell
# ================================================

import time
from typing import Dict, List, Optional, Tuple
from biblioteca.red.neurona import Neurona
from biblioteca.red.conexion import validar_tipo_relacion


class RedNeuronal:
    """
    La red neuronal de Belladonna.
    Infraestructura genérica — no tiene
    conocimiento específico de Bell.
    Solo sabe crear nodos, conectarlos,
    buscarlos y activarlos.
    """

    def __init__(self):
        self._nodos: Dict[str, Neurona] = {}
        self._indice_tipo: Dict[str, List[str]] = {}
        self._timestamp_creacion = time.time()
        self._total_activaciones = 0

    # ==========================================
    # GESTIÓN DE NODOS
    # ==========================================

    def agregar_nodo(self, datos: dict) -> bool:
        """
        Agrega un nodo nuevo a la red.
        Si ya existe no lo reemplaza.
        Retorna True si se agregó, False si ya existía.
        """
        nodo_id = datos.get('id')
        if not nodo_id:
            return False

        if nodo_id in self._nodos:
            return False  # Ya existe

        neurona = Neurona(nodo_id, datos)
        self._nodos[nodo_id] = neurona

        # Actualizar índice por tipo
        tipo = neurona.nucleo.tipo
        if tipo not in self._indice_tipo:
            self._indice_tipo[tipo] = []
        self._indice_tipo[tipo].append(nodo_id)

        return True

    def obtener_nodo(self, nodo_id: str) -> Optional[dict]:
        """
        Retorna los datos de un nodo.
        """
        neurona = self._nodos.get(nodo_id)
        return neurona.a_dict() if neurona else None

    def obtener_neurona(self, nodo_id: str) -> Optional[Neurona]:
        """
        Retorna la neurona directamente.
        Para uso interno.
        """
        return self._nodos.get(nodo_id)

    def existe_nodo(self, nodo_id: str) -> bool:
        return nodo_id in self._nodos

    def eliminar_nodo(self, nodo_id: str) -> bool:
        """
        Elimina un nodo y todas sus conexiones.
        No puede eliminar nodos inmutables.
        """
        neurona = self._nodos.get(nodo_id)
        if not neurona:
            return False

        if neurona.nucleo.inmutable:
            return False  # No se puede eliminar

        # Eliminar de otros nodos que apuntan a este
        for otra_neurona in self._nodos.values():
            if nodo_id in otra_neurona.conexiones:
                del otra_neurona.conexiones[nodo_id]

        # Eliminar del índice
        tipo = neurona.nucleo.tipo
        if tipo in self._indice_tipo:
            self._indice_tipo[tipo] = [
                n for n in self._indice_tipo[tipo]
                if n != nodo_id
            ]

        del self._nodos[nodo_id]
        return True

    def obtener_todos_los_nodos(self) -> Dict[str, dict]:
        """
        Retorna todos los nodos como diccionarios.
        """
        return {
            nodo_id: neurona.a_dict()
            for nodo_id, neurona in self._nodos.items()
        }

    def obtener_nodos_por_tipo(self, tipo: str) -> List[dict]:
        """
        Retorna todos los nodos de un tipo específico.
        """
        ids = self._indice_tipo.get(tipo, [])
        return [
            self._nodos[nodo_id].a_dict()
            for nodo_id in ids
            if nodo_id in self._nodos
        ]

    # ==========================================
    # GESTIÓN DE CONEXIONES
    # ==========================================

    def conectar(
        self,
        origen_id: str,
        destino_id: str,
        peso: float,
        tipo_relacion: str
    ) -> bool:
        """
        Crea una conexión entre dos nodos.
        Si la conexión ya existe actualiza el peso
        solo si el nuevo es mayor.
        """
        origen = self._nodos.get(origen_id)
        destino = self._nodos.get(destino_id)

        if not origen or not destino:
            return False

        tipo_valido = validar_tipo_relacion(tipo_relacion)
        origen.agregar_conexion(destino_id, peso, tipo_valido)
        return True

    def existe_conexion(
        self, origen_id: str, destino_id: str
    ) -> bool:
        origen = self._nodos.get(origen_id)
        if not origen:
            return False
        return destino_id in origen.conexiones

    def obtener_conexion(
        self, origen_id: str, destino_id: str
    ) -> Optional[dict]:
        origen = self._nodos.get(origen_id)
        if not origen:
            return None
        conexion = origen.conexiones.get(destino_id)
        return conexion.a_dict() if conexion else None

    def actualizar_peso_conexion(
        self,
        origen_id: str,
        destino_id: str,
        nuevo_peso: float
    ) -> bool:
        origen = self._nodos.get(origen_id)
        if not origen:
            return False
        conexion = origen.conexiones.get(destino_id)
        if not conexion:
            return False
        conexion.peso = max(0.1, min(1.0, nuevo_peso))
        return True

    # ==========================================
    # ACTIVACIÓN NEURONAL
    # ==========================================

    def activar_nodo(
        self,
        nodo_id: str,
        contexto: str = '',
        exito: bool = True
    ) -> bool:
        """
        Registra que un nodo fue activado.
        Actualiza su memoria.
        """
        neurona = self._nodos.get(nodo_id)
        if not neurona:
            return False

        neurona.memoria.registrar_uso(contexto, exito)
        self._total_activaciones += 1
        return True

    def obtener_vecinos(
        self,
        nodo_id: str,
        peso_minimo: float = 0.0
    ) -> List[Tuple[str, float]]:
        """
        Retorna los nodos conectados a este nodo
        con su peso de conexión.
        Ordenados por peso descendente.
        """
        neurona = self._nodos.get(nodo_id)
        if not neurona:
            return []

        vecinos = [
            (conn.nodo_destino, conn.peso)
            for conn in neurona.conexiones.values()
            if conn.peso >= peso_minimo
            and conn.nodo_destino in self._nodos
        ]

        return sorted(vecinos, key=lambda x: x[1], reverse=True)

    # ==========================================
    # BÚSQUEDA
    # ==========================================

    def buscar_por_grounding(
        self, grounding_minimo: float = 0.7
    ) -> List[dict]:
        """
        Retorna nodos con grounding mayor al mínimo.
        """
        resultado = []
        for neurona in self._nodos.values():
            if neurona.grounding_efectivo() >= grounding_minimo:
                resultado.append(neurona.a_dict())

        return sorted(
            resultado,
            key=lambda n: n['grounding_efectivo'],
            reverse=True
        )

    def buscar_por_id_parcial(self, fragmento: str) -> List[dict]:
        """
        Busca nodos cuyo ID contiene el fragmento.
        """
        fragmento_upper = fragmento.upper()
        return [
            neurona.a_dict()
            for nodo_id, neurona in self._nodos.items()
            if fragmento_upper in nodo_id.upper()
        ]

    # ==========================================
    # ESTADO Y DIAGNÓSTICO
    # ==========================================

    def obtener_estadisticas(self) -> dict:
        """
        Estadísticas de la red para diagnóstico.
        """
        total_nodos = len(self._nodos)
        total_conexiones = sum(
            len(n.conexiones) for n in self._nodos.values()
        )

        nodos_por_tipo = {
            tipo: len(ids)
            for tipo, ids in self._indice_tipo.items()
        }

        nodos_inmutables = sum(
            1 for n in self._nodos.values()
            if n.nucleo.inmutable
        )

        return {
            'total_nodos':       total_nodos,
            'total_conexiones':  total_conexiones,
            'nodos_por_tipo':    nodos_por_tipo,
            'nodos_inmutables':  nodos_inmutables,
            'total_activaciones': self._total_activaciones,
            'timestamp_creacion': self._timestamp_creacion
        }

    def esta_sana(self) -> dict:
        """
        Verifica la salud básica de la red.
        Retorna un reporte de estado.
        """
        problemas = []

        # Verificar nodos críticos
        nodos_criticos = [
            'BELL_CORE',
            'NEURONA_SEBASTIAN',
            'CONSEJERA_SAGE',
            'CONSEJERA_VEGA'
        ]

        for nodo_id in nodos_criticos:
            if not self.existe_nodo(nodo_id):
                problemas.append(
                    f'Nodo crítico ausente: {nodo_id}'
                )

        # Verificar conexiones huérfanas
        nodos_sin_conexiones = [
            nodo_id
            for nodo_id, neurona in self._nodos.items()
            if len(neurona.conexiones) == 0
            and not neurona.nucleo.inmutable
        ]

        if nodos_sin_conexiones:
            problemas.append(
                f'{len(nodos_sin_conexiones)} nodos sin conexiones'
            )

        return {
            'sana': len(problemas) == 0,
            'problemas': problemas,
            'total_nodos': len(self._nodos),
            'total_conexiones': sum(
                len(n.conexiones)
                for n in self._nodos.values()
            )
        }