# biblioteca/__init__.py
# ================================================
# LA BIBLIOTECA — El cerebro de Bell
# Ahora aplica grounding de vida a todo
# ================================================

from biblioteca.red.red_neuronal import RedNeuronal


class Biblioteca:
    """
    El cerebro de Bell. Singleton.
    Contiene la red neuronal + todos los subsistemas.
    Al iniciarse aplica grounding de vida a toda la red.
    """

    _instancia = None

    def __init__(self):
        self.red               = RedNeuronal()
        self.iniciada          = False
        self.gestor_consejeras = None
        self._inicializar()

    @classmethod
    def obtener(cls) -> 'Biblioteca':
        if cls._instancia is None:
            cls._instancia = Biblioteca()
        return cls._instancia

    def _inicializar(self):
        print('\nInicializando biblioteca neuronal...')
        try:
            from biblioteca.fundacional.cargador_fundacional import (
                CargadorFundacional
            )
            cargador = CargadorFundacional(self.red)
            exito    = cargador.cargar_todo()

            if exito:
                # Aplicar grounding de vida a toda la red
                self._aplicar_vida_a_red()
                # Iniciar consejeras
                self._iniciar_consejeras()

                stats = self.red.obtener_estadisticas()
                print(
                    f'Biblioteca lista: '
                    f'{stats["total_nodos"]} nodos, '
                    f'{stats["total_conexiones"]} conexiones'
                )
                self.iniciada = True
            else:
                print('ERROR: No se pudo inicializar la biblioteca')
                self.iniciada = False

        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f'ERROR crítico en biblioteca: {e}')
            self.iniciada = False

    def _aplicar_vida_a_red(self):
        """
        Aplica los 23 tipos de grounding a todo lo que existe.
        Nada en Bell estará vacío o incomprendido.
        """
        try:
            from biblioteca.grounding.aplicador_vida import AplicadorVida
            aplicador = AplicadorVida.obtener()
            resultado = aplicador.aplicar_a_red_completa(self.red)
        except Exception as e:
            print(f'  ⚠ Grounding de vida no aplicado: {e}')

    def _iniciar_consejeras(self):
        """Las consejeras toman conciencia de sí mismas."""
        try:
            from biblioteca.consejeras.gestor_consejeras import GestorConsejeras
            self.gestor_consejeras = GestorConsejeras.obtener()
        except Exception as e:
            print(f'  ⚠ Consejeras no disponibles: {e}')
            self.gestor_consejeras = None

    # ==========================================
    # API PÚBLICA
    # ==========================================

    def activar(self, conceptos: list, texto: str = '') -> dict:
        try:
            from biblioteca.red.activador import Activador
            return Activador(self.red).activar(conceptos, texto)
        except Exception as e:
            print(f'Error activando red: {e}')
            return {
                'nodos_primarios':    [],
                'nodos_secundarios':  [],
                'nodos_terciarios':   [],
                'total_activados':    0,
                'tiene_conocimiento': False,
                'nivel_conocimiento': 0.0,
            }

    def existe_nodo(self, nodo_id: str) -> bool:
        return self.red.existe_nodo(nodo_id)

    def agregar_nodo(self, datos: dict) -> bool:
        try:
            resultado = self.red.agregar_nodo(datos)
            if resultado:
                # Aplicar grounding de vida al nodo nuevo
                try:
                    from biblioteca.grounding.aplicador_vida import AplicadorVida
                    neurona = self.red.obtener_neurona(datos['id'])
                    if neurona:
                        AplicadorVida.obtener().aplicar_a_neurona(neurona)
                except Exception:
                    pass
            return resultado
        except Exception:
            return False

    def conectar(
        self,
        origen: str,
        destino: str,
        peso: float,
        tipo: str = 'relacionado_con'
    ) -> bool:
        try:
            return self.red.conectar(origen, destino, peso, tipo)
        except Exception:
            return False

    def estado(self) -> dict:
        stats = self.red.obtener_estadisticas()
        return {
            'iniciada':      self.iniciada,
            'estadisticas':  stats,
            'consejeras_ok': self.gestor_consejeras is not None,
        }

    def obtener_nodos_para_visualizacion(self) -> dict:
        todos = self.red.obtener_todos_los_nodos()
        nodos_visual       = []
        conexiones_visual  = []

        for nodo_id, nodo in todos.items():
            nucleo    = nodo.get('nucleo', {})
            datos_ext = nucleo.get('datos_extra', {}) if isinstance(nucleo, dict) else {}
            nodos_visual.append({
                'id':        nodo_id,
                'nombre':    self._nombre_legible(nodo_id),
                'tipo':      nucleo.get('tipo', 'concepto') if isinstance(nucleo, dict) else 'concepto',
                'estado':    'activo' if nodo.get('memoria', {}).get('veces_usado', 0) > 0 else 'inactivo',
                'grounding': nodo.get('grounding_efectivo', 0.5),
                'vitalidad': datos_ext.get('vitalidad', 0.0),
                'nivel_vida': datos_ext.get('nivel_vida', 'dormida'),
                'config':    nucleo
            })
            for dest_id, conn in nodo.get('conexiones', {}).items():
                conexiones_visual.append({
                    'id':      f'{nodo_id}__{dest_id}',
                    'origen':  nodo_id,
                    'destino': dest_id,
                    'peso':    conn.get('peso', 0.5) if isinstance(conn, dict) else 0.5,
                    'tipo':    conn.get('tipo_relacion', 'relacionado_con') if isinstance(conn, dict) else 'relacionado_con'
                })

        return {
            'nodos':             nodos_visual,
            'conexiones':        conexiones_visual,
            'total_nodos':       len(nodos_visual),
            'total_conexiones':  len(conexiones_visual)
        }

    def _nombre_legible(self, nodo_id: str) -> str:
        return nodo_id.replace('_', ' ').title()