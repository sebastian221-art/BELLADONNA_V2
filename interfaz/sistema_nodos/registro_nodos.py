# interfaz/sistema_nodos/registro_nodos.py
# ================================================
# REGISTRO DE NODOS — Inventario central de Bell
# Todo lo que existe en Bell está registrado aquí
# La visualización lee desde aquí
# ================================================

import os
import json
from pathlib import Path


class RegistroNodos:
    """
    Singleton — existe una sola instancia.
    Mantiene el inventario de todos los nodos
    que existen en el proyecto de Bell.
    """

    _instancia = None

    # Tipos de nodos y sus colores
    TIPOS = {
        'carpeta':   {'color': '#1B3A6B', 'tamanio': 2.0},
        'archivo':   {'color': '#1565C0', 'tamanio': 1.2},
        'capa':      {'color': '#00695C', 'tamanio': 2.5},
        'consejera': {'color': '#7B00FF', 'tamanio': 2.0},
        'neurona':   {'color': '#4A9EFF', 'tamanio': 1.0},
        'core':      {'color': '#FFFFFF', 'tamanio': 3.0},
        'habilidad': {'color': '#00838F', 'tamanio': 1.5}
    }

    # Carpetas del proyecto y su tipo
    CARPETAS_BELL = {
        'capas':       'capa',
        'consejeras':  'consejera',
        'biblioteca':  'neurona',
        'habilidades': 'habilidad',
        'core':        'core',
        'memoria':     'archivo',
        'grounding':   'archivo',
        'interfaz':    'archivo',
        'docs':        'archivo'
    }

    # Carpetas que NUNCA se escanean
    CARPETAS_IGNORADAS = {
        'venv', '.venv', 'env', '.env',
        '__pycache__', '.git', '.idea',
        'node_modules', '.pytest_cache',
        'dist', 'build', '.egg-info',
        '.mypy_cache', '.tox'
    }

    def __init__(self):
        self.nodos = {}
        self.conexiones = {}
        self.capas_existentes = []
        self._raiz = self._encontrar_raiz()

    @classmethod
    def obtener(cls):
        if cls._instancia is None:
            cls._instancia = cls()
            cls._instancia.escanear_proyecto()
        return cls._instancia

    def _encontrar_raiz(self) -> Path:
        """
        Encuentra la raíz del proyecto de manera segura.
        Prioridad:
        1. Variable de entorno BELL_RAIZ (la más confiable)
        2. Buscar main.py subiendo desde aquí
        3. Fallback a la carpeta actual
        """
        # Opción 1 — variable de entorno (la más confiable)
        raiz_env = os.environ.get('BELL_RAIZ')
        if raiz_env:
            raiz = Path(raiz_env)
            if raiz.exists() and (raiz / 'main.py').exists():
                print(f'Raíz encontrada por variable de entorno: {raiz}')
                return raiz

        # Opción 2 — buscar main.py subiendo desde este archivo
        # Este archivo está en interfaz/sistema_nodos/registro_nodos.py
        # Subir 3 niveles debería llegar a la raíz
        ruta_actual = Path(__file__).parent  # sistema_nodos/
        for _ in range(5):
            ruta_actual = ruta_actual.parent
            if (ruta_actual / 'main.py').exists():
                print(f'Raíz encontrada por main.py: {ruta_actual}')
                return ruta_actual

        # Opción 3 — fallback
        fallback = Path(__file__).parent.parent.parent
        print(f'Raíz por fallback: {fallback}')
        return fallback

    def _es_raiz_valida(self, raiz: Path) -> bool:
        """
        Verifica que la raíz sea válida y segura para escanear.
        Evita escanear carpetas del sistema o enormes.
        """
        if not raiz.exists():
            return False

        # Debe tener main.py o al menos una carpeta conocida de Bell
        carpetas_bell = {'capas', 'interfaz', 'docs'}
        contenido = {x.name for x in raiz.iterdir() if x.is_dir()}
        tiene_carpetas_bell = bool(contenido & carpetas_bell)

        if not tiene_carpetas_bell:
            print(f'ADVERTENCIA: La raíz {raiz} no parece ser Bell')
            return False

        # No debe tener demasiadas carpetas (señal de carpeta del sistema)
        carpetas_validas = [
            x for x in raiz.iterdir()
            if x.is_dir() and x.name not in self.CARPETAS_IGNORADAS
            and not x.name.startswith('.')
        ]
        if len(carpetas_validas) > 30:
            print(f'ADVERTENCIA: Demasiadas carpetas en {raiz}: {len(carpetas_validas)}')
            return False

        return True

    def escanear_proyecto(self):
        """
        Escanea el proyecto completo y registra
        todos los archivos y carpetas como nodos.
        """
        self.nodos = {}
        self.conexiones = {}
        self.capas_existentes = []

        # Verificar que la raíz sea válida
        if not self._es_raiz_valida(self._raiz):
            print(f'ERROR: Raíz inválida: {self._raiz}')
            print('Bell no puede escanear el proyecto.')
            self.registrar_nodo(
                id='bell_core',
                nombre='Bell',
                tipo='core',
                ruta=str(self._raiz),
                estado='error'
            )
            return

        print(f'Escaneando proyecto en: {self._raiz}')

        # Registrar nodo raíz de Bell
        self.registrar_nodo(
            id='bell_core',
            nombre='Bell',
            tipo='core',
            ruta=str(self._raiz),
            estado='activo'
        )

        # Escanear solo las carpetas principales — un nivel
        for carpeta in sorted(self._raiz.iterdir()):
            if not carpeta.is_dir():
                continue
            if carpeta.name in self.CARPETAS_IGNORADAS:
                continue
            if carpeta.name.startswith('.'):
                continue

            self._escanear_carpeta(carpeta, padre_id='bell_core')

        # Detectar qué capas existen
        self._detectar_capas()

        # Detectar conexiones entre archivos Python
        self._detectar_conexiones()

        print(f'Escaneo completo: {len(self.nodos)} nodos, '
              f'{len(self.conexiones)} conexiones')

    def _escanear_carpeta(self, ruta_carpeta: Path,
                          padre_id: str, profundidad: int = 0):
        """
        Escanea una carpeta recursivamente.
        Máximo 3 niveles de profundidad.
        Ignora carpetas del sistema.
        """
        # Límite de profundidad
        if profundidad > 3:
            return

        # Ignorar carpetas del sistema
        if ruta_carpeta.name in self.CARPETAS_IGNORADAS:
            return

        nombre = ruta_carpeta.name
        tipo = self.CARPETAS_BELL.get(nombre, 'carpeta')
        nodo_id = self._generar_id(ruta_carpeta)

        self.registrar_nodo(
            id=nodo_id,
            nombre=nombre,
            tipo=tipo,
            ruta=str(ruta_carpeta),
            estado='inactivo',
            padre_id=padre_id
        )

        # Conectar con el padre
        self.registrar_conexion(
            id=f'conn_{padre_id}_{nodo_id}',
            origen_id=padre_id,
            destino_id=nodo_id,
            peso=0.7
        )

        # Escanear contenido
        try:
            items = sorted(ruta_carpeta.iterdir())

            # Límite de items por carpeta para no saturar
            if len(items) > 100:
                print(f'Carpeta grande ignorada parcialmente: {nombre} '
                      f'({len(items)} items)')
                items = items[:100]

            for item in items:
                if item.name.startswith('.'):
                    continue
                if item.name in self.CARPETAS_IGNORADAS:
                    continue

                if item.is_dir():
                    self._escanear_carpeta(
                        item, nodo_id, profundidad + 1
                    )
                elif item.is_file():
                    self._registrar_archivo(item, nodo_id)

        except PermissionError:
            pass
        except Exception as e:
            print(f'Error escaneando {ruta_carpeta}: {e}')

    def _registrar_archivo(self, ruta_archivo: Path, padre_id: str):
        """
        Registra un archivo como nodo.
        """
        nodo_id = self._generar_id(ruta_archivo)

        self.registrar_nodo(
            id=nodo_id,
            nombre=ruta_archivo.name,
            tipo='archivo',
            ruta=str(ruta_archivo),
            estado='inactivo',
            padre_id=padre_id
        )

        self.registrar_conexion(
            id=f'conn_{padre_id}_{nodo_id}',
            origen_id=padre_id,
            destino_id=nodo_id,
            peso=0.5
        )

    def _detectar_capas(self):
        """
        Detecta qué capas del flujo existen.
        """
        carpeta_capas = self._raiz / 'capas'
        if not carpeta_capas.exists():
            return

        for i in range(1, 10):
            carpeta_capa = carpeta_capas / f'capa{i}'
            if carpeta_capa.exists():
                self.capas_existentes.append(f'capa{i}')

        print(f'Capas encontradas: {self.capas_existentes}')

    def _detectar_conexiones(self):
        """
        Detecta conexiones entre archivos Python
        por imports. Solo archivos pequeños.
        """
        for nodo_id, nodo in list(self.nodos.items()):
            ruta_str = nodo.get('ruta', '')
            if not ruta_str.endswith('.py'):
                continue

            ruta = Path(ruta_str)
            if not ruta.exists():
                continue

            try:
                # Solo archivos pequeños
                if ruta.stat().st_size > 30000:
                    continue

                contenido = ruta.read_text(encoding='utf-8')
                self._analizar_imports(contenido, nodo_id)
            except Exception:
                pass

    def _analizar_imports(self, contenido: str, nodo_id_origen: str):
        """
        Analiza imports de un archivo y crea conexiones.
        """
        lineas = contenido.split('\n')
        for linea in lineas[:50]:  # Solo primeras 50 líneas
            linea = linea.strip()
            if not (linea.startswith('from ') or
                    linea.startswith('import ')):
                continue

            for nodo_id_destino, nodo in self.nodos.items():
                if nodo_id_destino == nodo_id_origen:
                    continue

                nombre_modulo = nodo.get('nombre', '').replace('.py', '')
                if (nombre_modulo and
                        len(nombre_modulo) > 3 and
                        nombre_modulo in linea):
                    conn_id = f'import_{nodo_id_origen}_{nodo_id_destino}'
                    if conn_id not in self.conexiones:
                        self.registrar_conexion(
                            id=conn_id,
                            origen_id=nodo_id_origen,
                            destino_id=nodo_id_destino,
                            peso=0.6
                        )

    def registrar_nodo(self, id: str, nombre: str, tipo: str,
                       ruta: str = '', estado: str = 'inactivo',
                       padre_id: str = None):
        """
        Registra o actualiza un nodo.
        """
        self.nodos[id] = {
            'id': id,
            'nombre': nombre,
            'tipo': tipo,
            'ruta': ruta,
            'estado': estado,
            'padre_id': padre_id,
            'config': self.TIPOS.get(tipo, self.TIPOS['archivo'])
        }

    def registrar_conexion(self, id: str, origen_id: str,
                           destino_id: str, peso: float = 0.5):
        """
        Registra una conexión entre dos nodos.
        """
        self.conexiones[id] = {
            'id': id,
            'origen': origen_id,
            'destino': destino_id,
            'peso': peso
        }

    def actualizar_estado_nodo(self, nodo_id: str, nuevo_estado: str):
        """
        Actualiza el estado de un nodo.
        """
        if nodo_id in self.nodos:
            self.nodos[nodo_id]['estado'] = nuevo_estado

    def obtener_nodo(self, nodo_id: str):
        """
        Retorna los datos de un nodo específico.
        """
        return self.nodos.get(nodo_id)

    def obtener_estado_completo(self) -> dict:
        """
        Retorna el estado completo para el frontend.
        """
        return {
            'nodos': list(self.nodos.values()),
            'conexiones': list(self.conexiones.values()),
            'capas_existentes': self.capas_existentes,
            'total_nodos': len(self.nodos),
            'total_conexiones': len(self.conexiones)
        }

    def _generar_id(self, ruta) -> str:
        """
        Genera un ID único basado en la ruta relativa.
        """
        try:
            relativa = Path(ruta).relative_to(self._raiz)
            return str(relativa).replace(os.sep, '_').replace('.', '_')
        except ValueError:
            return str(ruta).replace(os.sep, '_').replace('.', '_')
