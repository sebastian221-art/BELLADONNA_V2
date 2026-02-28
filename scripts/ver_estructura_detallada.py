"""
Script MEJORADO para visualizar estructura detallada del proyecto Belladonna.

Muestra:
- Estructura de directorios
- Clases definidas en cada archivo
- Funciones/métodos principales
- Herencia de clases
- Imports importantes
- Parámetros de __init__

Sin mostrar TODO el código (sería infinito).
"""
import ast
import os
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict


class AnalizadorDetallado:
    """Analiza proyecto Python en detalle."""
    
    def __init__(self):
        self.ignorar = {
            '__pycache__', '.git', 'venv', '.venv', 'env',
            '.pytest_cache', '.coverage', 'htmlcov', 'node_modules'
        }
        
        # Información recopilada
        self.archivos_info = {}  # path -> info del archivo
        
    def analizar_proyecto(self, raiz: Path = Path('.')):
        """Analiza todo el proyecto."""
        print("=" * 80)
        print("ANÁLISIS DETALLADO DEL PROYECTO BELLADONNA")
        print("=" * 80)
        print()
        
        archivos_py = self._encontrar_archivos_python(raiz)
        
        print(f"🔍 Encontrados {len(archivos_py)} archivos Python")
        print()
        
        for archivo in archivos_py:
            info = self._analizar_archivo(archivo)
            if info:
                self.archivos_info[str(archivo.relative_to(raiz))] = info
        
        return self.archivos_info
    
    def _encontrar_archivos_python(self, raiz: Path) -> List[Path]:
        """Encuentra todos los archivos .py."""
        archivos = []
        
        for archivo in raiz.rglob('*.py'):
            # Ignorar directorios específicos
            if any(parte in self.ignorar for parte in archivo.parts):
                continue
            archivos.append(archivo)
        
        return sorted(archivos)
    
    def _analizar_archivo(self, archivo: Path) -> Dict:
        """Analiza un archivo Python con AST."""
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            arbol = ast.parse(contenido, filename=str(archivo))
            
            info = {
                'ruta': str(archivo),
                'docstring': ast.get_docstring(arbol),
                'imports': self._extraer_imports(arbol),
                'clases': self._extraer_clases(arbol),
                'funciones': self._extraer_funciones_globales(arbol),
                'lineas': len(contenido.splitlines())
            }
            
            return info
            
        except Exception as e:
            return {
                'ruta': str(archivo),
                'error': str(e),
                'clases': [],
                'funciones': [],
                'imports': []
            }
    
    def _extraer_imports(self, arbol: ast.AST) -> List[str]:
        """Extrae imports importantes."""
        imports = []
        
        for nodo in ast.walk(arbol):
            if isinstance(nodo, ast.Import):
                for alias in nodo.names:
                    imports.append(alias.name)
            
            elif isinstance(nodo, ast.ImportFrom):
                if nodo.module:
                    # Solo imports de nuestros módulos
                    if any(nodo.module.startswith(m) for m in [
                        'core', 'vocabulario', 'traduccion', 'razonamiento',
                        'consejeras', 'generacion', 'grounding', 'llm',
                        'memoria', 'bucles', 'aprendizaje'
                    ]):
                        for alias in nodo.names:
                            imports.append(f"{nodo.module}.{alias.name}")
        
        return imports[:10]  # Solo primeros 10 imports importantes
    
    def _extraer_clases(self, arbol: ast.AST) -> List[Dict]:
        """Extrae información de clases."""
        clases = []
        
        for nodo in arbol.body:
            if isinstance(nodo, ast.ClassDef):
                clase_info = {
                    'nombre': nodo.name,
                    'hereda_de': self._extraer_herencia(nodo),
                    'docstring': ast.get_docstring(nodo),
                    'metodos': self._extraer_metodos(nodo),
                    'init_params': self._extraer_init_params(nodo)
                }
                clases.append(clase_info)
        
        return clases
    
    def _extraer_herencia(self, nodo_clase: ast.ClassDef) -> List[str]:
        """Extrae de qué clases hereda."""
        bases = []
        for base in nodo_clase.bases:
            if isinstance(base, ast.Name):
                bases.append(base.id)
            elif isinstance(base, ast.Attribute):
                bases.append(f"{base.value.id}.{base.attr}")
        return bases
    
    def _extraer_metodos(self, nodo_clase: ast.ClassDef) -> List[str]:
        """Extrae métodos públicos de una clase."""
        metodos = []
        
        for item in nodo_clase.body:
            if isinstance(item, ast.FunctionDef):
                # Solo métodos públicos (no privados)
                if not item.name.startswith('_') or item.name == '__init__':
                    metodos.append(item.name)
        
        return metodos
    
    def _extraer_init_params(self, nodo_clase: ast.ClassDef) -> List[str]:
        """Extrae parámetros de __init__."""
        for item in nodo_clase.body:
            if isinstance(item, ast.FunctionDef) and item.name == '__init__':
                params = []
                for arg in item.args.args:
                    if arg.arg != 'self':
                        params.append(arg.arg)
                return params
        return []
    
    def _extraer_funciones_globales(self, arbol: ast.AST) -> List[str]:
        """Extrae funciones globales (no métodos)."""
        funciones = []
        
        for nodo in arbol.body:
            if isinstance(nodo, ast.FunctionDef):
                # Solo funciones públicas
                if not nodo.name.startswith('_'):
                    funciones.append(nodo.name)
        
        return funciones
    
    def generar_reporte_modulo(self, modulo: str) -> str:
        """Genera reporte de un módulo específico."""
        reporte = []
        reporte.append("=" * 80)
        reporte.append(f"MÓDULO: {modulo}")
        reporte.append("=" * 80)
        reporte.append("")
        
        archivos_modulo = {
            path: info for path, info in self.archivos_info.items()
            if modulo in path
        }
        
        if not archivos_modulo:
            reporte.append(f"⚠️  No se encontraron archivos en {modulo}")
            return "\n".join(reporte)
        
        for path, info in sorted(archivos_modulo.items()):
            reporte.append(f"\n📄 {path}")
            reporte.append("─" * 80)
            
            # Docstring del archivo
            if info.get('docstring'):
                doc_lines = info['docstring'].split('\n')
                reporte.append(f"📝 {doc_lines[0]}")
            
            # Clases
            if info.get('clases'):
                reporte.append(f"\n  CLASES ({len(info['clases'])}):")
                for clase in info['clases']:
                    herencia = f" → hereda de: {', '.join(clase['hereda_de'])}" if clase['hereda_de'] else ""
                    reporte.append(f"  • {clase['nombre']}{herencia}")
                    
                    if clase['init_params']:
                        reporte.append(f"    __init__({', '.join(clase['init_params'])})")
                    
                    if clase['metodos']:
                        metodos_str = ', '.join(clase['metodos'][:8])
                        if len(clase['metodos']) > 8:
                            metodos_str += f"... +{len(clase['metodos'])-8} más"
                        reporte.append(f"    Métodos: {metodos_str}")
            
            # Funciones globales
            if info.get('funciones'):
                reporte.append(f"\n  FUNCIONES ({len(info['funciones'])}):")
                for func in info['funciones'][:10]:
                    reporte.append(f"  • {func}()")
            
            # Imports importantes
            if info.get('imports'):
                reporte.append(f"\n  IMPORTS CLAVE:")
                for imp in info['imports'][:5]:
                    reporte.append(f"  • {imp}")
            
            reporte.append("")
        
        return "\n".join(reporte)
    
    def generar_reporte_completo(self) -> str:
        """Genera reporte completo del proyecto."""
        reporte = []
        
        # Módulos principales
        modulos = [
            'core',
            'vocabulario',
            'traduccion',
            'razonamiento',
            'consejeras',
            'generacion',
            'grounding',
            'llm',
            'memoria',
            'bucles',
            'aprendizaje',
            'operaciones',
            'base_datos',
            'main.py'
        ]
        
        for modulo in modulos:
            reporte.append(self.generar_reporte_modulo(modulo))
            reporte.append("\n")
        
        return "\n".join(reporte)
    
    def generar_mapa_clases(self) -> str:
        """Genera mapa de todas las clases y su herencia."""
        reporte = []
        reporte.append("=" * 80)
        reporte.append("MAPA DE CLASES - HERENCIA")
        reporte.append("=" * 80)
        reporte.append("")
        
        todas_clases = []
        for path, info in self.archivos_info.items():
            for clase in info.get('clases', []):
                todas_clases.append({
                    'nombre': clase['nombre'],
                    'hereda': clase['hereda_de'],
                    'archivo': path,
                    'metodos': clase['metodos']
                })
        
        # Agrupar por herencia
        por_base = defaultdict(list)
        sin_herencia = []
        
        for clase in todas_clases:
            if clase['hereda']:
                for base in clase['hereda']:
                    por_base[base].append(clase)
            else:
                sin_herencia.append(clase)
        
        # Mostrar jerarquía
        for base, clases in sorted(por_base.items()):
            reporte.append(f"\n📦 Heredan de {base}:")
            for clase in clases:
                metodos_key = ', '.join(clase['metodos'][:5])
                reporte.append(f"  • {clase['nombre']} ({clase['archivo']})")
                reporte.append(f"    Métodos: {metodos_key}")
        
        if sin_herencia:
            reporte.append(f"\n📦 Clases base (sin herencia):")
            for clase in sin_herencia[:20]:
                reporte.append(f"  • {clase['nombre']} ({clase['archivo']})")
        
        return "\n".join(reporte)


def main():
    """Función principal."""
    analizador = AnalizadorDetallado()
    analizador.analizar_proyecto()
    
    # Guardar reporte completo
    with open('ESTRUCTURA_DETALLADA.txt', 'w', encoding='utf-8') as f:
        f.write(analizador.generar_reporte_completo())
    
    # Guardar mapa de clases
    with open('MAPA_CLASES.txt', 'w', encoding='utf-8') as f:
        f.write(analizador.generar_mapa_clases())
    
    print("✅ Análisis completado")
    print()
    print("Archivos generados:")
    print("  • ESTRUCTURA_DETALLADA.txt - Análisis completo de cada módulo")
    print("  • MAPA_CLASES.txt - Mapa de herencia de clases")
    print()
    print("=" * 80)


if __name__ == '__main__':
    main()