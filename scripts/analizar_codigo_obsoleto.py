"""
Analizador de Código Obsoleto - Belladonna

Analiza TODOS los archivos Python y detecta:
- Clases definidas
- Métodos/funciones
- Imports
- Código potencialmente obsoleto
- Archivos no usados

Uso:
    python analizar_codigo_obsoleto.py
    python analizar_codigo_obsoleto.py --detallado
"""

import ast
import os
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict
import argparse


class AnalizadorCodigo:
    """Analiza código Python para detectar obsoletos."""
    
    def __init__(self, directorio_raiz: str = '.'):
        self.raiz = Path(directorio_raiz)
        
        # Datos recopilados
        self.archivos_python = []
        self.clases_definidas = defaultdict(list)  # archivo -> [clases]
        self.funciones_definidas = defaultdict(list)  # archivo -> [funciones]
        self.imports = defaultdict(set)  # archivo -> {imports}
        
        # Uso de clases/funciones
        self.clases_usadas = set()
        self.funciones_usadas = set()
        
        # Directorios a ignorar
        self.ignorar = {
            '.git', '__pycache__', 'venv', '.venv', 
            'env', '_legacy', '.pytest_cache', 'node_modules'
        }
    
    def analizar_proyecto(self):
        """Analiza todo el proyecto."""
        print("=" * 70)
        print("ANALIZADOR DE CÓDIGO OBSOLETO")
        print("=" * 70)
        print()
        
        # 1. Encontrar todos los archivos Python
        print("🔍 Buscando archivos Python...")
        self._encontrar_archivos_python()
        print(f"   Encontrados: {len(self.archivos_python)} archivos")
        print()
        
        # 2. Analizar cada archivo
        print("📊 Analizando archivos...")
        for archivo in self.archivos_python:
            self._analizar_archivo(archivo)
        print(f"   ✅ {len(self.archivos_python)} archivos analizados")
        print()
        
        # 3. Detectar uso
        print("🔗 Detectando uso de clases/funciones...")
        self._detectar_uso()
        print(f"   ✅ Análisis de uso completado")
        print()
    
    def _encontrar_archivos_python(self):
        """Encuentra todos los archivos .py."""
        for ruta in self.raiz.rglob('*.py'):
            # Ignorar directorios específicos
            if any(parte in self.ignorar for parte in ruta.parts):
                continue
            
            # Ignorar archivos de test (los analizaremos aparte)
            if 'test' in ruta.stem.lower():
                continue
            
            self.archivos_python.append(ruta)
    
    def _analizar_archivo(self, archivo: Path):
        """Analiza un archivo Python."""
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Parsear con AST
            arbol = ast.parse(contenido, filename=str(archivo))
            
            # Extraer información
            ruta_relativa = str(archivo.relative_to(self.raiz))
            
            for nodo in ast.walk(arbol):
                # Clases
                if isinstance(nodo, ast.ClassDef):
                    self.clases_definidas[ruta_relativa].append(nodo.name)
                
                # Funciones
                elif isinstance(nodo, ast.FunctionDef):
                    self.funciones_definidas[ruta_relativa].append(nodo.name)
                
                # Imports
                elif isinstance(nodo, ast.Import):
                    for alias in nodo.names:
                        self.imports[ruta_relativa].add(alias.name)
                
                elif isinstance(nodo, ast.ImportFrom):
                    if nodo.module:
                        for alias in nodo.names:
                            self.imports[ruta_relativa].add(f"{nodo.module}.{alias.name}")
        
        except Exception as e:
            print(f"  ⚠️  Error en {archivo}: {e}")
    
    def _detectar_uso(self):
        """Detecta qué clases/funciones se usan."""
        # Buscar referencias en todos los archivos
        for archivo in self.archivos_python:
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                
                # Buscar referencias a clases
                for archivo_def, clases in self.clases_definidas.items():
                    for clase in clases:
                        if clase in contenido:
                            self.clases_usadas.add(f"{archivo_def}:{clase}")
                
                # Buscar referencias a funciones
                for archivo_def, funciones in self.funciones_definidas.items():
                    for funcion in funciones:
                        if funcion in contenido:
                            self.funciones_usadas.add(f"{archivo_def}:{funcion}")
            
            except Exception:
                pass
    
    def generar_reporte(self, detallado: bool = False) -> str:
        """Genera reporte de análisis."""
        reporte = []
        reporte.append("=" * 70)
        reporte.append("REPORTE DE ANÁLISIS")
        reporte.append("=" * 70)
        reporte.append("")
        
        # 1. Resumen general
        total_clases = sum(len(clases) for clases in self.clases_definidas.values())
        total_funciones = sum(len(funcs) for funcs in self.funciones_definidas.values())
        
        reporte.append("📊 RESUMEN GENERAL:")
        reporte.append(f"  Archivos analizados: {len(self.archivos_python)}")
        reporte.append(f"  Clases definidas: {total_clases}")
        reporte.append(f"  Funciones definidas: {total_funciones}")
        reporte.append("")
        
        # 2. Clases por archivo
        if detallado:
            reporte.append("📦 CLASES POR ARCHIVO:")
            reporte.append("")
            for archivo, clases in sorted(self.clases_definidas.items()):
                if clases:
                    reporte.append(f"  {archivo}:")
                    for clase in clases:
                        usado = "✅" if f"{archivo}:{clase}" in self.clases_usadas else "❌"
                        reporte.append(f"    {usado} {clase}")
            reporte.append("")
        
        # 3. Clases potencialmente obsoletas
        clases_no_usadas = []
        for archivo, clases in self.clases_definidas.items():
            for clase in clases:
                if f"{archivo}:{clase}" not in self.clases_usadas:
                    clases_no_usadas.append(f"{archivo}:{clase}")
        
        if clases_no_usadas:
            reporte.append("⚠️  CLASES POTENCIALMENTE NO USADAS:")
            reporte.append("")
            for clase in clases_no_usadas[:20]:  # Primeras 20
                archivo, nombre = clase.split(':')
                reporte.append(f"  • {nombre} (en {archivo})")
            
            if len(clases_no_usadas) > 20:
                reporte.append(f"  ... y {len(clases_no_usadas) - 20} más")
            reporte.append("")
        
        # 4. Archivos con muchas clases (posible refactorización)
        reporte.append("📊 ARCHIVOS CON MUCHAS CLASES:")
        reporte.append("")
        archivos_grandes = [(archivo, len(clases)) 
                           for archivo, clases in self.clases_definidas.items()
                           if len(clases) > 3]
        
        for archivo, cantidad in sorted(archivos_grandes, key=lambda x: -x[1])[:10]:
            reporte.append(f"  • {archivo}: {cantidad} clases")
        reporte.append("")
        
        # 5. Módulos más importados
        reporte.append("🔗 MÓDULOS MÁS IMPORTADOS:")
        reporte.append("")
        
        todos_imports = defaultdict(int)
        for imports in self.imports.values():
            for imp in imports:
                modulo = imp.split('.')[0]
                todos_imports[modulo] += 1
        
        for modulo, cantidad in sorted(todos_imports.items(), key=lambda x: -x[1])[:10]:
            reporte.append(f"  • {modulo}: {cantidad} veces")
        reporte.append("")
        
        # 6. Archivos potencialmente obsoletos
        reporte.append("🗑️  ARCHIVOS POTENCIALMENTE OBSOLETOS:")
        reporte.append("(Archivos sin clases usadas o con muy poco código)")
        reporte.append("")
        
        archivos_sospechosos = []
        for archivo in self.archivos_python:
            ruta_rel = str(archivo.relative_to(self.raiz))
            
            # Archivos sin clases
            if ruta_rel not in self.clases_definidas:
                archivos_sospechosos.append((ruta_rel, "Sin clases definidas"))
            
            # Archivos con todas las clases no usadas
            elif ruta_rel in self.clases_definidas:
                clases = self.clases_definidas[ruta_rel]
                if clases:
                    todas_no_usadas = all(
                        f"{ruta_rel}:{clase}" not in self.clases_usadas 
                        for clase in clases
                    )
                    if todas_no_usadas:
                        archivos_sospechosos.append((ruta_rel, "Clases no usadas"))
        
        for archivo, razon in archivos_sospechosos[:15]:
            reporte.append(f"  • {archivo} ({razon})")
        
        if len(archivos_sospechosos) > 15:
            reporte.append(f"  ... y {len(archivos_sospechosos) - 15} más")
        reporte.append("")
        
        reporte.append("=" * 70)
        
        return "\n".join(reporte)
    
    def generar_recomendaciones(self) -> str:
        """Genera recomendaciones de limpieza."""
        rec = []
        rec.append("")
        rec.append("💡 RECOMENDACIONES:")
        rec.append("")
        
        # Detectar archivos en raíz que deberían estar en módulos
        archivos_raiz = [a for a in self.archivos_python 
                        if len(a.relative_to(self.raiz).parts) == 1]
        
        if len(archivos_raiz) > 5:
            rec.append("1. ORGANIZACIÓN:")
            rec.append(f"   Hay {len(archivos_raiz)} archivos en la raíz.")
            rec.append("   Considera moverlos a módulos apropiados.")
            rec.append("")
        
        # Detectar duplicación
        clases_nombres = defaultdict(list)
        for archivo, clases in self.clases_definidas.items():
            for clase in clases:
                clases_nombres[clase].append(archivo)
        
        duplicadas = {nombre: archivos for nombre, archivos in clases_nombres.items()
                     if len(archivos) > 1}
        
        if duplicadas:
            rec.append("2. CLASES DUPLICADAS:")
            for nombre, archivos in list(duplicadas.items())[:5]:
                rec.append(f"   • {nombre} definida en:")
                for archivo in archivos:
                    rec.append(f"     - {archivo}")
            rec.append("")
        
        # Detectar archivos legacy
        archivos_legacy = [str(a.relative_to(self.raiz)) 
                          for a in self.archivos_python 
                          if 'legacy' in str(a).lower() or '_old' in str(a).lower()]
        
        if archivos_legacy:
            rec.append("3. ARCHIVOS LEGACY:")
            rec.append(f"   Encontrados {len(archivos_legacy)} archivos legacy.")
            rec.append("   Considera eliminarlos si ya no se usan.")
            rec.append("")
        
        rec.append("=" * 70)
        
        return "\n".join(rec)


def main():
    """Main."""
    parser = argparse.ArgumentParser(
        description='Analiza código Python para detectar obsoletos'
    )
    parser.add_argument(
        '--detallado',
        action='store_true',
        help='Reporte detallado con todas las clases'
    )
    parser.add_argument(
        '--directorio',
        default='.',
        help='Directorio raíz del proyecto'
    )
    
    args = parser.parse_args()
    
    # Analizar
    analizador = AnalizadorCodigo(args.directorio)
    analizador.analizar_proyecto()
    
    # Generar reportes
    print(analizador.generar_reporte(detallado=args.detallado))
    print(analizador.generar_recomendaciones())


if __name__ == '__main__':
    main()