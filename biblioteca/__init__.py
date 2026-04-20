# biblioteca/__init__.py v3
# FIX CRÍTICO: obtener_nodos_para_visualizacion() ahora lee
# las neuronas reales (no los dicts serializados) para que
# datos_extra con vitalidad/nivel_vida llegue al frontend.

from biblioteca.red.red_neuronal import RedNeuronal


class Biblioteca:
    _instancia     = None
    _inicializando = False

    def __init__(self):
        self.red               = RedNeuronal()
        self.iniciada          = False
        self.gestor_consejeras = None
        self._inicializar()

    @classmethod
    def obtener(cls) -> 'Biblioteca':
        if cls._instancia is None:
            if cls._inicializando:
                return cls._instancia
            cls._instancia = Biblioteca()
        return cls._instancia

    def _inicializar(self):
        Biblioteca._inicializando = True
        print('\n╔══════════════════════════════════╗')
        print('║   BELLADONNA — iniciando Bell    ║')
        print('╚══════════════════════════════════╝')
        try:
            from biblioteca.fundacional.cargador_fundacional import CargadorFundacional
            cargador = CargadorFundacional(self.red)
            exito    = cargador.cargar_todo()

            if exito:
                self._aplicar_vida_a_red()
                self._iniciar_consejeras()
                stats = self.red.obtener_estadisticas()
                print(
                    f'OK Biblioteca lista: '
                    f'{stats["total_nodos"]} nodos, '
                    f'{stats["total_conexiones"]} conexiones'
                )
                self.iniciada = True
            else:
                print('ERROR: no se pudo inicializar la biblioteca')
                self.iniciada = False

        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f'ERROR critico: {e}')
            self.iniciada = False
        finally:
            Biblioteca._inicializando = False

    def _aplicar_vida_a_red(self):
        try:
            from biblioteca.grounding.aplicador_vida import AplicadorVida
            AplicadorVida.obtener().aplicar_a_red_completa(self.red)
        except Exception as e:
            print(f'  Grounding de vida no aplicado: {e}')

    def _iniciar_consejeras(self):
        try:
            from biblioteca.consejeras.gestor_consejeras import GestorConsejeras
            self.gestor_consejeras = GestorConsejeras.obtener()
        except Exception as e:
            print(f'  Consejeras no disponibles: {e}')
            self.gestor_consejeras = None

    def aplicar_vida_a_nuevos_nodos(self):
        self._aplicar_vida_a_red()

    # ==========================================
    # API PÚBLICA
    # ==========================================

    def activar(self, conceptos: list, texto: str = '') -> dict:
        try:
            from biblioteca.red.activador import Activador
            return Activador(self.red).activar(conceptos, texto)
        except Exception as e:
            return {
                'nodos_primarios': [], 'nodos_secundarios': [],
                'nodos_terciarios': [], 'total_activados': 0,
                'tiene_conocimiento': False, 'nivel_conocimiento': 0.0,
            }

    def existe_nodo(self, nodo_id: str) -> bool:
        return self.red.existe_nodo(nodo_id)

    def agregar_nodo(self, datos: dict) -> bool:
        try:
            resultado = self.red.agregar_nodo(datos)
            if resultado:
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

    def conectar(self, origen: str, destino: str, peso: float,
                 tipo: str = 'relacionado_con') -> bool:
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
        """
        Lee neuronas REALES para que datos_extra llegue al frontend.

        El problema anterior: obtener_todos_los_nodos() retorna dicts
        serializados que NO incluyen datos_extra. La vitalidad vive en
        neurona.nucleo.datos_extra — hay que leer el objeto real.
        """
        todos_serializados = self.red.obtener_todos_los_nodos()
        nodos_visual       = []
        conexiones_visual  = []

        for nodo_id in list(todos_serializados.keys()):
            # Leer objeto REAL — tiene datos_extra con vitalidad
            neurona = self.red.obtener_neurona(nodo_id)
            if not neurona:
                continue

            nucleo    = neurona.nucleo
            datos_ext = {}
            if hasattr(nucleo, 'datos_extra') and isinstance(nucleo.datos_extra, dict):
                datos_ext = nucleo.datos_extra

            vitalidad  = datos_ext.get('vitalidad',  0.0)
            nivel_vida = datos_ext.get('nivel_vida', 'dormida')

            # Estado basado en uso real
            estado = 'inactivo'
            if hasattr(neurona, 'memoria') and isinstance(neurona.memoria, dict):
                if neurona.memoria.get('veces_usado', 0) > 0:
                    estado = 'activo'

            nodos_visual.append({
                'id':        nodo_id,
                'nombre':    self._nombre_legible(nodo_id),
                'tipo':      getattr(nucleo, 'tipo', 'concepto'),
                'estado':    estado,
                'grounding': getattr(nucleo, 'grounding_base', 0.5),
                'vitalidad':  round(float(vitalidad), 4),
                'nivel_vida': nivel_vida,
                'config': {
                    'tipo':           getattr(nucleo, 'tipo', 'concepto'),
                    'grounding_base': getattr(nucleo, 'grounding_base', 0.5),
                },
            })

            # Conexiones desde el objeto real
            conexiones_neurona = {}
            if hasattr(neurona, 'conexiones') and isinstance(neurona.conexiones, dict):
                conexiones_neurona = neurona.conexiones
            elif hasattr(neurona, '_conexiones') and isinstance(neurona._conexiones, dict):
                conexiones_neurona = neurona._conexiones

            for dest_id, conn in conexiones_neurona.items():
                if isinstance(conn, dict):
                    peso     = conn.get('peso', 0.5)
                    tipo_rel = conn.get('tipo_relacion', 'relacionado_con')
                elif hasattr(conn, 'peso'):
                    peso     = conn.peso
                    tipo_rel = getattr(conn, 'tipo_relacion', 'relacionado_con')
                else:
                    peso     = 0.5
                    tipo_rel = 'relacionado_con'

                conexiones_visual.append({
                    'id':      f'{nodo_id}__{dest_id}',
                    'origen':  nodo_id,
                    'destino': dest_id,
                    'peso':    float(peso),
                    'tipo':    tipo_rel,
                })

        return {
            'nodos':            nodos_visual,
            'conexiones':       conexiones_visual,
            'total_nodos':      len(nodos_visual),
            'total_conexiones': len(conexiones_visual),
        }

    def _nombre_legible(self, nodo_id: str) -> str:
        nombre = nodo_id
        if nombre.startswith('AUTO_'):
            nombre = nombre[5:]
        return nombre.replace('_', ' ').title()