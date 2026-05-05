# biblioteca/registrador_automatico.py
# ================================================
# REGISTRADOR AUTOMÁTICO
# Cuando se agrega algo nuevo a Bell
# este registrador lo integra automáticamente
# a la red neuronal con sus conexiones correctas
#
# LOGS LIMPIOS: solo muestra resúmenes,
# no cada nodo individual.
# ================================================

import os
from pathlib import Path
from typing import Optional


class RegistradorAutomatico:
    """
    Analiza qué tipo de cosa es un archivo
    y crea la neurona correcta en la biblioteca.
    """

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

    def registrar_archivo(
        self,
        ruta_archivo: str,
        forzar: bool = False
    ) -> Optional[str]:
        """
        Registra un archivo como neurona en la red.
        Retorna el ID del nodo creado o None si ya existía.
        Sin log por archivo — solo cuenta.
        """
        ruta = Path(ruta_archivo)

        if ruta.suffix not in ['.py', '.js', '.css', '.html', '.md']:
            return None

        if any(parte.startswith('__') for parte in ruta.parts):
            if ruta.name not in ['__init__.py']:
                return None

        nodo_id = self._generar_id(ruta)

        if nodo_id in self._registrados and not forzar:
            return None

        tipo        = self._determinar_tipo(ruta)
        descripcion = self._generar_descripcion(ruta, tipo)
        grounding   = self._calcular_grounding(ruta, tipo)

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

            self._conectar_segun_tipo(nodo_id, tipo, ruta)
            self._registrados.add(nodo_id)
            return nodo_id

        else:
            self._registrados.add(nodo_id)
            return None

    def registrar_directorio(
        self,
        ruta_directorio: str,
        recursivo: bool = True
    ) -> int:
        ruta = Path(ruta_directorio)
        if not ruta.exists():
            return 0

        ignorar = {
            '__pycache__', '.git', 'venv', 'env',
            'node_modules', '.pytest_cache', 'dist', 'build'
        }

        nuevos = 0
        patron = '**/*.py' if recursivo else '*.py'

        for archivo in ruta.glob(patron):
            if any(parte in ignorar for parte in archivo.parts):
                continue
            nodo_id = self.registrar_archivo(str(archivo))
            if nodo_id:
                nuevos += 1

        return nuevos

    def registrar_todo_el_proyecto(self, raiz: str) -> int:
        """
        Escanea TODO el proyecto y registra lo nuevo.
        Solo muestra el resumen final.
        """
        ruta = Path(raiz)
        total_nuevos = 0

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

        # Solo mostrar resumen — sin logs por nodo
        if total_nuevos > 0:
            print(f'  ✓ Auto-registro: {total_nuevos} nuevas neuronas integradas')
        else:
            print('  ✓ Auto-registro: sin cambios')

        return total_nuevos

    def _generar_id(self, ruta: Path) -> str:
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
        partes_relevantes = partes[-3:] if len(partes) > 3 else partes
        return 'AUTO_' + '_'.join(partes_relevantes)

    def _determinar_tipo(self, ruta: Path) -> str:
        partes_lower = [p.lower() for p in ruta.parts]
        for carpeta, tipo in self.TIPOS_POR_CARPETA.items():
            if carpeta in partes_lower:
                return tipo
        return 'desconocido'

    def _generar_descripcion(self, ruta: Path, tipo: str) -> str:
        nombre = ruta.stem.replace('_', ' ')
        descripciones = {
            'capa_flujo':    f'Capa del flujo: {nombre}',
            'interfaz':      f'Interfaz: {nombre}',
            'habilidad':     f'Habilidad: {nombre}',
            'vocabulario':   f'Vocabulario: {nombre}',
            'cerebro':       f'Cerebro: {nombre}',
            'fundacional':   f'Fundacional: {nombre}',
            'consejera':     f'Consejera: {nombre}',
            'documentacion': f'Doc: {nombre}',
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

    def _conectar_segun_tipo(self, nodo_id: str, tipo: str, ruta: Path):
        conexiones_base = {
            'capa_flujo': [
                ('BELL_CORE',           0.75),
                ('BIBLIOTECA_CEREBRAL', 0.80),
            ],
            'interfaz': [
                ('BELL_CORE',           0.70),
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

        partes_lower = [p.lower() for p in ruta.parts]
        if 'capa1' in partes_lower and self.red.existe_nodo('CAPA1_RECEPCION'):
            self.red.conectar(nodo_id, 'CAPA1_RECEPCION', 0.85, 'parte_de')
        elif 'capa2' in partes_lower and self.red.existe_nodo('CAPA2_ACTIVACION'):
            self.red.conectar(nodo_id, 'CAPA2_ACTIVACION', 0.85, 'parte_de')
        elif 'capa3' in partes_lower and self.red.existe_nodo('CAPA3_COMPRENSION'):
            self.red.conectar(nodo_id, 'CAPA3_COMPRENSION', 0.85, 'parte_de')