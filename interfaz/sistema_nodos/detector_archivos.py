# interfaz/sistema_nodos/detector_archivos.py
import threading
import time
from pathlib import Path


class DetectorArchivos:

    INTERVALO_SEGUNDOS = 30
    EXTENSIONES        = {'.py', '.js', '.css', '.html', '.md'}
    IGNORAR_CARPETAS   = {
        '__pycache__', '.git', 'venv', 'env',
        'node_modules', '.pytest_cache'
    }

    def __init__(self, registro_nodos, raiz_proyecto: str):
        self.registro       = registro_nodos
        self.raiz           = Path(raiz_proyecto)
        self._activo        = False
        self._hilo          = None
        self._estado_previo = {}
        self._registrador   = None
        self._inicializar_registrador()

    def _inicializar_registrador(self):
        try:
            from biblioteca import Biblioteca
            from biblioteca.registrador_automatico import RegistradorAutomatico
            biblioteca = Biblioteca.obtener()
            if biblioteca.iniciada:
                self._registrador = RegistradorAutomatico(biblioteca)
                print('  Detector: conectado con registrador automático')
            else:
                print('  Detector: biblioteca no iniciada, sin auto-registro')
        except Exception as e:
            print(f'  Detector: sin auto-registro ({e})')
            self._registrador = None

    def iniciar(self):
        self._activo = True
        self._hilo   = threading.Thread(
            target=self._bucle_deteccion,
            daemon=True
        )
        self._hilo.start()
        print('Detector de archivos activo')

    def detener(self):
        self._activo = False

    def _bucle_deteccion(self):
        while self._activo:
            try:
                self._escanear()
            except Exception as e:
                print(f'Error en detector: {e}')
            time.sleep(self.INTERVALO_SEGUNDOS)

    def _escanear(self):
        estado_actual = self._obtener_estado_actual()
        cambios = self._detectar_cambios(estado_actual)

        if cambios['nuevos'] or cambios['modificados'] or cambios['eliminados']:
            print(
                f'Cambios detectados: '
                f'{len(cambios["nuevos"])} nuevos, '
                f'{len(cambios["modificados"])} modificados, '
                f'{len(cambios["eliminados"])} eliminados'
            )

            if self._registrador and cambios['nuevos']:
                self._registrar_nuevos_en_biblioteca(cambios['nuevos'])

            self._actualizar_registro(cambios)
            self._estado_previo = estado_actual
            self._re_escanear()

    def _registrar_nuevos_en_biblioteca(self, archivos_nuevos: list):
        registrados = 0
        for ruta_str in archivos_nuevos:
            nodo_id = self._registrador.registrar_archivo(ruta_str)
            if nodo_id:
                registrados += 1
                print(f'  Nueva neurona auto-creada: {nodo_id}')
        if registrados > 0:
            print(f'  ✓ {registrados} nuevas neuronas integradas')

    def _obtener_estado_actual(self) -> dict:
        estado = {}
        for archivo in self.raiz.rglob('*'):
            if not archivo.is_file():
                continue
            if archivo.suffix not in self.EXTENSIONES:
                continue
            if any(p in self.IGNORAR_CARPETAS for p in archivo.parts):
                continue
            try:
                estado[str(archivo)] = archivo.stat().st_mtime
            except Exception:
                pass
        return estado

    def _detectar_cambios(self, estado_actual: dict) -> dict:
        nuevos      = []
        modificados = []
        eliminados  = []

        for ruta, mtime in estado_actual.items():
            if ruta not in self._estado_previo:
                nuevos.append(ruta)
            elif self._estado_previo[ruta] != mtime:
                modificados.append(ruta)

        for ruta in self._estado_previo:
            if ruta not in estado_actual:
                eliminados.append(ruta)

        return {
            'nuevos':      nuevos,
            'modificados': modificados,
            'eliminados':  eliminados
        }

    def _actualizar_registro(self, cambios: dict):
        """
        Actualiza el RegistroNodos usando los métodos
        que realmente existen en esa clase.
        """
        for ruta_str in cambios['nuevos']:
            ruta = Path(ruta_str)
            try:
                relativa = ruta.relative_to(self.raiz)
                nodo_id  = (str(relativa)
                            .replace('\\', '_')
                            .replace('/', '_')
                            .replace('.', '_'))
                self.registro.registrar_nodo(
                    id=nodo_id,
                    nombre=ruta.name,
                    tipo='archivo',
                    ruta=ruta_str,
                    estado='inactivo'
                )
            except Exception:
                pass

        for ruta_str in cambios['eliminados']:
            ruta = Path(ruta_str)
            try:
                relativa = ruta.relative_to(self.raiz)
                nodo_id  = (str(relativa)
                            .replace('\\', '_')
                            .replace('/', '_')
                            .replace('.', '_'))
                self.registro.actualizar_estado_nodo(nodo_id, 'eliminado')
            except Exception:
                pass

    def _re_escanear(self):
        try:
            from interfaz.sistema_nodos.estado_nodos import EstadoNodos
            EstadoNodos.obtener().actualizar()
        except Exception:
            pass
