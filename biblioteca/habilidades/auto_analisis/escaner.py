# biblioteca/habilidades/auto_analisis/escaner.py
# ================================================
# ESCÁNER TOTAL — Lee Bell en tiempo real
#
# Recorre TODOS los archivos de Bell:
# Python, JS, CSS, HTML, JSON, Markdown.
# Retorna un mapa completo y actualizado.
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

_IGNORAR = {'__pycache__', '.git', '.pytest_cache', 'node_modules',
            '.venv', 'venv', '.env', 'dist', 'build'}


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

        # Capas — leer directo de a.ruta (robusto en Windows)
        capas: Dict[str, List[ArchivoInfo]] = {}
        for a in archivos:
            ruta_n = a.ruta.replace('\\', '/').replace('\\', '/')
            # Buscar segmento 'capaX' en la ruta
            for parte in ruta_n.split('/'):
                if len(parte) == 5 and parte.startswith('capa') and parte[4].isdigit():
                    capas.setdefault(parte, []).append(a)
                    break

        # Habilidades — extrae de archivos ya escaneados (robusto en cualquier OS)
        habilidades = self._detectar_habilidades_desde_archivos(archivos)

        # Consejeras — igual
        consejeras = self._detectar_consejeras_desde_archivos(archivos)

        # Vocabulario
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
        for root, dirs, files in os.walk(self.raiz):
            dirs[:] = [d for d in dirs if d not in _IGNORAR]
            for nombre in files:
                ruta = Path(root) / nombre
                if ruta.suffix in _EXTENSIONES:
                    yield ruta

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
            # Normalizar separadores a '/' para consistencia en cualquier OS
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

    def _clasificar(self, partes) -> tuple:
        if not partes:
            return 'raiz', ''
        p0 = partes[0]
        if p0 == 'capas' and len(partes) > 1:
            return partes[1], (partes[2] if len(partes) > 2 else '')
        if p0 == 'biblioteca':
            sub = '/'.join(partes[1:3]) if len(partes) > 1 else ''
            return 'biblioteca', sub
        if p0 == 'interfaz':
            return 'interfaz', (partes[1] if len(partes) > 1 else '')
        if p0 == 'docs':
            return 'docs', ''
        if p0 == 'datos':
            return 'datos', ''
        return 'raiz', ''

    def _extraer_py(self, contenido: str):
        clases = []
        funciones = []
        try:
            tree = ast.parse(contenido)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    clases.append(node.name)
                elif isinstance(node, ast.FunctionDef):
                    funciones.append(node.name)
        except Exception:
            clases    = re.findall(r'^class\s+(\w+)', contenido, re.MULTILINE)
            funciones = re.findall(r'^def\s+(\w+)', contenido, re.MULTILINE)
        return clases[:20], funciones[:30]

    # ── Detección robusta usando archivos ya escaneados ──────────────

    def _detectar_habilidades_desde_archivos(self, archivos: List[ArchivoInfo]) -> List[str]:
        """Extrae habilidades desde las rutas ya escaneadas — robusto en cualquier OS."""
        habs = set()
        for a in archivos:
            if 'biblioteca/habilidades/' in a.ruta:
                parts = a.ruta.split('biblioteca/habilidades/')
                if len(parts) > 1:
                    sub = parts[1].split('/')[0]
                    if sub and not sub.startswith('_') and not sub.startswith('.') and '.' not in sub:
                        habs.add(sub)
        return sorted(habs)

    def _detectar_consejeras_desde_archivos(self, archivos: List[ArchivoInfo]) -> List[str]:
        """Extrae consejeras desde las rutas ya escaneadas."""
        cons = set()
        for a in archivos:
            if 'biblioteca/consejeras/' in a.ruta:
                parts = a.ruta.split('biblioteca/consejeras/')
                if len(parts) > 1:
                    sub = parts[1].split('/')[0]
                    if sub and not sub.startswith('_') and not sub.startswith('.') and '.' not in sub:
                        cons.add(sub)
        return sorted(cons)

    def _contar_vocabulario_desde_archivos(self, archivos: List[ArchivoInfo]) -> tuple:
        """Cuenta vocabulario desde rutas y contenido escaneado."""
        modulos = 0
        conceptos = 0
        for a in archivos:
            if ('biblioteca/vocabulario/base/' in a.ruta or
                    'biblioteca/fundacional/vocabulario/' in a.ruta) and a.extension == '.py':
                if a.nombre != '__init__.py':
                    modulos += 1
                    # Leer y contar entradas
                    try:
                        ruta_abs = self.raiz / a.ruta.replace('/', os.sep)
                        with open(ruta_abs, 'r', encoding='utf-8', errors='ignore') as f:
                            contenido = f.read()
                        # Formato dict: '  "palabra": {'
                        n_dict = len(re.findall(
                            r"^\s+'[^'_][^']*'\s*:\s*\{", contenido, re.MULTILINE))
                        # Formato tupla: ('NOMBRE', ...)
                        n_tuple = len(re.findall(
                            r"^\s+\('[A-Z_]+',", contenido, re.MULTILINE))
                        conceptos += max(n_dict, n_tuple)
                    except Exception:
                        pass
        return modulos, conceptos