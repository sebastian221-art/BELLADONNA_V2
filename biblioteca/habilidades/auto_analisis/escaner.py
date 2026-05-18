# biblioteca/habilidades/auto_analisis/escaner.py
# ================================================
# ESCÁNER TOTAL — Lee Bell en tiempo real
# ================================================

import os
import ast
import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional


_EXTENSIONES = {
    '.py':   'Python',
    '.js':   'JavaScript',
    '.css':  'CSS',
    '.html': 'HTML',
    '.json': 'JSON',
    '.md':   'Markdown',
    '.txt':  'Texto',
}

# Directorios que NUNCA son código de Bell
_IGNORAR = {
    '__pycache__', '.git', '.pytest_cache', 'node_modules',
    '.venv', 'venv', 'env', '.env', 'dist', 'build',
    'site-packages', 'lib', 'lib64', 'include', 'bin', 'Scripts',
    'Frameworks', 'Headers', 'Resources', 'share',
    '.mypy_cache', '.ruff_cache', 'htmlcov', '.idea', '.vscode',
}

# Directorios conocidos de Bell (whitelist para Mac)
_DIRS_BELL = {'capas', 'biblioteca', 'interfaz', 'tests', 'test', 'docs', 'scripts'}

# Tamaño máximo de archivo en bytes (300 KB)
_MAX_BYTES = 300_000


@dataclass
class ArchivoInfo:
    ruta:         str
    nombre:       str
    extension:    str
    tipo:         str
    lineas:       int
    tamano_kb:    float
    categoria:    str
    subcategoria: str
    clases:       List[str] = field(default_factory=list)
    funciones:    List[str] = field(default_factory=list)


@dataclass
class EscaneoResult:
    archivos:        List[ArchivoInfo]
    total_archivos:  int
    por_tipo:        Dict[str, int]
    por_categoria:   Dict[str, int]
    total_lineas:    int
    total_kb:        float
    capas:           Dict[str, List[ArchivoInfo]]
    habilidades:     List[str]
    consejeras:      List[str]
    modulos_vocab:   int
    conceptos_vocab: int
    raiz_bell:       str


class EscanerTotal:

    def __init__(self, raiz: str):
        self.raiz = Path(raiz)

    def escanear(self) -> EscaneoResult:
        archivos = []
        por_tipo: Dict[str, int] = {}
        por_categoria: Dict[str, int] = {}
        total_lineas = 0
        total_kb = 0.0

        for ruta in self._iterar_archivos():
            info = self._analizar_archivo(ruta)
            if info:
                archivos.append(info)
                por_tipo[info.tipo] = por_tipo.get(info.tipo, 0) + 1
                por_categoria[info.categoria] = por_categoria.get(info.categoria, 0) + 1
                total_lineas += info.lineas
                total_kb += info.tamano_kb

        # Capas
        capas: Dict[str, List[ArchivoInfo]] = {}
        for a in archivos:
            ruta_n = a.ruta.replace('\\', '/')
            for parte in ruta_n.split('/'):
                if len(parte) == 5 and parte.startswith('capa') and parte[4].isdigit():
                    capas.setdefault(parte, []).append(a)
                    break

        habilidades = self._detectar_habilidades_desde_archivos(archivos)
        consejeras  = self._detectar_consejeras_desde_archivos(archivos)
        vocab_mod, vocab_conc = self._contar_vocabulario_desde_archivos(archivos)

        return EscaneoResult(
            archivos        = archivos,
            total_archivos  = len(archivos),
            por_tipo        = por_tipo,
            por_categoria   = por_categoria,
            total_lineas    = total_lineas,
            total_kb        = round(total_kb, 1),
            capas           = capas,
            habilidades     = habilidades,
            consejeras      = consejeras,
            modulos_vocab   = vocab_mod,
            conceptos_vocab = vocab_conc,
            raiz_bell       = str(self.raiz),
        )

    def _iterar_archivos(self):
        """
        Estrategia doble:
        1. Whitelist — solo directorios conocidos de Bell.
        2. Si whitelist encuentra < 10 archivos → fallback blacklist con cap 600.
        Así funciona en cualquier Mac/Windows independiente de nombres de venv.
        """
        archivos = list(self._whitelist())
        if len(archivos) >= 10:
            yield from archivos
            return
        # Fallback: blacklist con cap
        print(f'  [Escaner] whitelist encontró {len(archivos)}, usando blacklist...')
        yield from self._blacklist()

    def _whitelist(self):
        """
        Escanea directorios Bell usando rglob — más compatible con Mac.
        Evita os.walk que puede fallar con symlinks o permisos en macOS.
        """
        raiz = self.raiz

        # Archivos en raíz directamente (main.py, etc.)
        try:
            for f in raiz.iterdir():
                if f.is_file() and f.suffix in _EXTENSIONES:
                    try:
                        if f.stat().st_size <= _MAX_BYTES:
                            yield f
                    except Exception:
                        pass
        except Exception:
            pass

        # Directorios conocidos de Bell via rglob
        for dir_name in _DIRS_BELL:
            dir_path = raiz / dir_name
            try:
                if not dir_path.exists():
                    continue
                for ruta in dir_path.rglob('*'):
                    try:
                        if not ruta.is_file():
                            continue
                        if ruta.suffix not in _EXTENSIONES:
                            continue
                        # Ignorar si está dentro de directorio problemático
                        partes = ruta.relative_to(dir_path).parts
                        if any(p in _IGNORAR for p in partes):
                            continue
                        if ruta.stat().st_size > _MAX_BYTES:
                            continue
                        yield ruta
                    except Exception:
                        continue
            except Exception as e:
                print(f'  [Escaner] rglob error {dir_name}: {e}')

    def _blacklist(self):
        """
        Fallback: os.walk desde raíz con dos filtros:
        1. Solo entra en directorios de primer nivel conocidos de Bell
        2. Blacklist de subdirectorios problemáticos
        """
        count = 0
        for root, dirs, files in os.walk(str(self.raiz)):
            root_path = Path(root)
            # Calcular profundidad relativa a la raíz
            try:
                rel = root_path.relative_to(self.raiz)
                parts = rel.parts
            except ValueError:
                dirs.clear()
                continue

            # Primer nivel: solo entrar en directorios conocidos de Bell
            if len(parts) == 1 and parts[0] not in _DIRS_BELL:
                dirs.clear()
                continue

            # Filtrar subdirectorios problemáticos
            dirs[:] = [d for d in dirs if d not in _IGNORAR]

            for nombre in files:
                ruta = root_path / nombre
                if ruta.suffix not in _EXTENSIONES:
                    continue
                try:
                    if ruta.stat().st_size > _MAX_BYTES:
                        continue
                except Exception:
                    continue
                yield ruta
                count += 1
                if count >= 1000:
                    return

    def _analizar_archivo(self, ruta: Path) -> Optional[ArchivoInfo]:
        try:
            tamano_kb = ruta.stat().st_size / 1024
            try:
                with open(ruta, 'r', encoding='utf-8', errors='ignore') as f:
                    contenido = f.read()
                lineas = contenido.count('\n') + 1
            except Exception:
                lineas = 0
                contenido = ''

            relativa = ruta.relative_to(self.raiz)
            ruta_norm = str(relativa).replace('\\', '/')
            partes = ruta_norm.split('/')
            categoria, subcategoria = self._clasificar(partes)
            extension = ruta.suffix
            tipo = _EXTENSIONES.get(extension, 'Otro')

            clases = []
            funciones = []
            if extension == '.py' and contenido:
                clases, funciones = self._extraer_py(contenido)

            return ArchivoInfo(
                ruta         = ruta_norm,
                nombre       = ruta.name,
                extension    = extension,
                tipo         = tipo,
                lineas       = lineas,
                tamano_kb    = round(tamano_kb, 1),
                categoria    = categoria,
                subcategoria = subcategoria,
                clases       = clases,
                funciones    = funciones,
            )
        except Exception:
            return None

    def _clasificar(self, partes: List[str]) -> tuple:
        if not partes:
            return 'raiz', ''
        p0 = partes[0]
        if p0 == 'capas':
            return (partes[1] if len(partes) > 1 else 'capas'), ''
        if p0 == 'biblioteca':
            return 'biblioteca', (partes[2] if len(partes) > 2 else '')
        if p0 == 'interfaz':
            return 'interfaz', (partes[1] if len(partes) > 1 else '')
        if p0 in ('tests', 'test'):
            return 'tests', ''
        if p0 == 'docs':
            return 'docs', ''
        return 'raiz', p0

    def _extraer_py(self, contenido: str):
        clases = []
        funciones = []
        try:
            tree = ast.parse(contenido)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    clases.append(node.name)
                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    funciones.append(node.name)
        except Exception:
            pass
        return clases[:5], funciones[:10]

    def _detectar_habilidades_desde_archivos(self, archivos: List[ArchivoInfo]) -> List[str]:
        habs = set()
        for a in archivos:
            ruta_n = a.ruta.replace('\\', '/')
            if 'biblioteca/habilidades/' in ruta_n:
                partes = ruta_n.split('/')
                try:
                    idx = partes.index('habilidades')
                    if idx + 1 < len(partes) and partes[idx + 1]:
                        habs.add(partes[idx + 1])
                except ValueError:
                    pass
        return sorted(habs)

    def _detectar_consejeras_desde_archivos(self, archivos: List[ArchivoInfo]) -> List[str]:
        _NOMBRES = {'soma', 'vega', 'nova', 'echo', 'lyra', 'luna', 'iris', 'sage'}
        encontradas = set()
        for a in archivos:
            nombre_base = a.nombre.replace('.py', '').lower()
            if nombre_base in _NOMBRES:
                encontradas.add(nombre_base)
        return sorted(encontradas)

    def _contar_vocabulario_desde_archivos(self, archivos: List[ArchivoInfo]):
        modulos = 0
        conceptos = 0
        for a in archivos:
            if 'vocabulario' in a.ruta or 'vocab' in a.ruta:
                if a.extension == '.py':
                    modulos += 1
                    conceptos += max(0, a.lineas // 4)
        return modulos, conceptos