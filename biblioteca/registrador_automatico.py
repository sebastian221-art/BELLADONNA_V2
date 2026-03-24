# biblioteca/registrador_automatico.py
# ================================================
# REGISTRADOR AUTOMÁTICO
# Cuando se agrega algo nuevo a Bell
# este registrador lo integra automáticamente
# a la red neuronal con sus conexiones correctas
#
# Bell crece — y sabe que creció.
# ================================================

import os
from pathlib import Path
from typing import Optional


class RegistradorAutomatico:
    """
    Analiza qué tipo de cosa es un archivo
    y crea la neurona correcta en la biblioteca.

    Principio: todo lo que Bell tiene
    debe estar en su cerebro.
    Sin excepción.
    """

    # Mapeo de carpetas a tipos de neurona
    TIPOS_POR_CARPETA = {
        'capas':       'capa_flujo',
        'biblioteca':  'cerebro',
        'interfaz':    'interfaz',
        'habilidades': 'habilidad',
        'vocabulario': 'vocabulario',
        'fundacional': 'fundacional',
        'consejeras':  'consejera',
        'docs':        'documentacion',
    }

    # Prefijos de ID según tipo
    PREFIJOS_ID = {
        'capa_flujo':    'AUTO_CAPA',
        'interfaz':      'AUTO_INTERFAZ',
        'habilidad':     'AUTO_HABILIDAD',
        'vocabulario':   'AUTO_VOCAB',
        'cerebro':       'AUTO_CEREBRO',
        'fundacional':   'AUTO_FUND',
        'consejera':     'AUTO_CONSEJERA',
        'documentacion': 'AUTO_DOC',
        'desconocido':   'AUTO_NODO',
    }

    def __init__(self, biblioteca):
        self.biblioteca = biblioteca
        self.red        = biblioteca.red
        self._registrados: set = set()
        print('  Registrador automático iniciado')

    def registrar_archivo(
        self,
        ruta_archivo: str,
        forzar: bool = False
    ) -> Optional[str]:
        """
        Registra un archivo como neurona en la red.
        Retorna el ID del nodo creado o None si ya existía.
        """
        ruta = Path(ruta_archivo)

        # Ignorar archivos que no son código
        if ruta.suffix not in ['.py', '.js', '.css', '.html', '.md']:
            return None

        # Ignorar archivos del sistema
        if any(parte.startswith('__') for parte in ruta.parts):
            if ruta.name not in ['__init__.py']:
                return None

        # Generar ID único para este archivo
        nodo_id = self._generar_id(ruta)

        # Si ya está registrado no duplicar
        if nodo_id in self._registrados and not forzar:
            return None

        # Determinar qué tipo de neurona crear
        tipo = self._determinar_tipo(ruta)
        descripcion = self._generar_descripcion(ruta, tipo)
        grounding = self._calcular_grounding(ruta, tipo)

        # Crear el nodo si no existe en la red
        if not self.red.existe_nodo(nodo_id):
            self.red.agregar_nodo({
                'id': nodo_id,
                'nucleo': {
                    'tipo':       tipo,
                    'subtipo':    'auto_registrado',
                    'grounding_base': grounding,
                    'dimensiones_activas': ['conocimiento'],
                    'archivo_real': str(ruta),
                    'inmutable':  False,
                    'descripcion': descripcion,
                    'auto_registrado': True
                },
                'activacion': {
                    'umbral':    0.30,
                    'velocidad': 'media',
                    'mielina':   False
                },
                'memoria': {
                    'veces_usado':        0,
                    'ultimo_uso':         None,
                    'contextos_de_uso':   [],
                    'resultado_historico': grounding
                }
            })

            # Conectar con la red según su tipo
            self._conectar_segun_tipo(nodo_id, tipo, ruta)
            self._registrados.add(nodo_id)

            print(f'    + Auto-registrado: {nodo_id} ({tipo})')
            return nodo_id

        else:
            self._registrados.add(nodo_id)
            return None

    def registrar_directorio(
        self,
        ruta_directorio: str,
        recursivo: bool = True
    ) -> int:
        """
        Registra todos los archivos de un directorio.
        Retorna la cantidad de nodos nuevos creados.
        """
        ruta = Path(ruta_directorio)
        if not ruta.exists():
            return 0

        # Carpetas a ignorar
        ignorar = {
            '__pycache__', '.git', 'venv', 'env',
            'node_modules', '.pytest_cache', 'dist', 'build'
        }

        nuevos = 0
        patron = '**/*.py' if recursivo else '*.py'

        for archivo in ruta.glob(patron):
            # Verificar que no está en carpeta ignorada
            if any(parte in ignorar for parte in archivo.parts):
                continue
            nodo_id = self.registrar_archivo(str(archivo))
            if nodo_id:
                nuevos += 1

        return nuevos

    def registrar_todo_el_proyecto(self, raiz: str) -> int:
        """
        Escanea TODO el proyecto de Bell
        y registra lo que no está en la red.
        Este método es la base del auto-conocimiento total.
        """
        print('  Escaneando proyecto para auto-registro...')
        ruta = Path(raiz)
        total_nuevos = 0

        # Carpetas principales a escanear
        carpetas_principales = [
            'capas', 'biblioteca', 'interfaz',
            'habilidades', 'docs'
        ]

        for carpeta in carpetas_principales:
            ruta_carpeta = ruta / carpeta
            if ruta_carpeta.exists():
                nuevos = self.registrar_directorio(
                    str(ruta_carpeta), recursivo=True
                )
                total_nuevos += nuevos

        if total_nuevos > 0:
            print(
                f'  ✓ Auto-registro completo: '
                f'{total_nuevos} nodos nuevos integrados'
            )
        else:
            print('  ✓ Auto-registro: todo ya estaba registrado')

        return total_nuevos

    def _generar_id(self, ruta: Path) -> str:
        """
        Genera un ID único para el archivo.
        Basado en su ruta relativa al proyecto.
        """
        partes = []
        for parte in ruta.parts:
            if parte not in ['.', '..', 'C:\\', '/']:
                partes.append(
                    parte.upper()
                    .replace('.PY', '')
                    .replace('.JS', '')
                    .replace('.CSS', '')
                    .replace('-', '_')
                    .replace(' ', '_')
                )

        # Tomar las últimas 3 partes para el ID
        partes_relevantes = partes[-3:] if len(partes) > 3 else partes
        return 'AUTO_' + '_'.join(partes_relevantes)

    def _determinar_tipo(self, ruta: Path) -> str:
        """
        Determina qué tipo de neurona crear
        basándose en la carpeta del archivo.
        """
        partes_lower = [p.lower() for p in ruta.parts]

        for carpeta, tipo in self.TIPOS_POR_CARPETA.items():
            if carpeta in partes_lower:
                return tipo

        return 'desconocido'

    def _generar_descripcion(self, ruta: Path, tipo: str) -> str:
        nombre = ruta.stem.replace('_', ' ')
        descripciones = {
            'capa_flujo':    f'Componente de capa del flujo: {nombre}',
            'interfaz':      f'Componente de interfaz: {nombre}',
            'habilidad':     f'Habilidad de Bell: {nombre}',
            'vocabulario':   f'Módulo de vocabulario: {nombre}',
            'cerebro':       f'Componente del cerebro: {nombre}',
            'fundacional':   f'Componente fundacional: {nombre}',
            'consejera':     f'Componente de consejera: {nombre}',
            'documentacion': f'Documentación: {nombre}',
            'desconocido':   f'Componente: {nombre}',
        }
        return descripciones.get(tipo, f'Componente: {nombre}')

    def _calcular_grounding(self, ruta: Path, tipo: str) -> float:
        groundings = {
            'capa_flujo':    0.85,
            'interfaz':      0.80,
            'habilidad':     0.85,
            'vocabulario':   0.80,
            'cerebro':       0.90,
            'fundacional':   0.85,
            'consejera':     0.85,
            'documentacion': 0.60,
            'desconocido':   0.50,
        }
        return groundings.get(tipo, 0.50)

    def _conectar_segun_tipo(
        self, nodo_id: str, tipo: str, ruta: Path
    ):
        """
        Conecta el nodo auto-registrado con los
        nodos correctos según su tipo.
        """
        conexiones_base = {
            'capa_flujo': [
                ('BELL_CORE',           0.75),
                ('BIBLIOTECA_CEREBRAL', 0.80),
            ],
            'interfaz': [
                ('BELL_CORE',           0.70),
                ('NEURONA_SEBASTIAN',   0.75),
                ('INTERFAZ_SERVIDOR',   0.80),
            ],
            'habilidad': [
                ('BELL_CORE',           0.75),
                ('PROPOSITO_COMPANERA_VIDA', 0.70),
            ],
            'vocabulario': [
                ('GESTOR_VOCABULARIO_NODO', 0.85),
                ('BIBLIOTECA_CEREBRAL', 0.75),
            ],
            'cerebro': [
                ('BIBLIOTECA_CEREBRAL', 0.85),
                ('BELL_CORE',           0.75),
            ],
            'fundacional': [
                ('BELL_CORE',           0.80),
                ('BIBLIOTECA_CEREBRAL', 0.80),
            ],
            'consejera': [
                ('BELL_CORE',           0.80),
                ('CONSEJERA_SAGE',      0.75),
            ],
            'desconocido': [
                ('BELL_CORE',           0.50),
            ],
        }

        conexiones = conexiones_base.get(tipo, [('BELL_CORE', 0.50)])

        for destino_id, peso in conexiones:
            if self.red.existe_nodo(destino_id):
                self.red.conectar(
                    nodo_id, destino_id, peso, 'parte_de'
                )

        # Conexión adicional según carpeta específica
        partes_lower = [p.lower() for p in ruta.parts]
        if 'capa1' in partes_lower and self.red.existe_nodo('CAPA1_RECEPCION'):
            self.red.conectar(nodo_id, 'CAPA1_RECEPCION', 0.85, 'parte_de')
        elif 'capa2' in partes_lower and self.red.existe_nodo('CAPA2_ACTIVACION'):
            self.red.conectar(nodo_id, 'CAPA2_ACTIVACION', 0.85, 'parte_de')
        elif 'capa3' in partes_lower and self.red.existe_nodo('CAPA3_COMPRENSION'):
            self.red.conectar(nodo_id, 'CAPA3_COMPRENSION', 0.85, 'parte_de')