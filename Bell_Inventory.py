"""
BELL INVENTORY - AUDITORÍA ARQUITECTÓNICA COMPLETA
===================================================
Script de diagnóstico para Proyecto Belladonna.

Genera 3 archivos críticos:
1. BELL_ARCHITECTURE.md - Mapa visual para humanos
2. BELL_ARCHITECTURE.json - Datos estructurados para IAs
3. BELL_HEALTH_CHECK.txt - Diagnóstico de salud del código

Autor: Sistema Belladonna
Versión: 2.0 (Optimizado para Fase 4A)
"""

import ast
import os
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict, Counter
from dataclasses import dataclass, asdict


@dataclass
class ClaseInfo:
    """Información estructurada de una clase."""
    nombre: str
    hereda_de: List[str]
    metodos_publicos: List[str]
    metodos_privados: List[str]
    tiene_init: bool
    params_init: List[str]
    docstring: str
    linea_inicio: int
    es_abstracta: bool


@dataclass
class ArchivoInfo:
    """Información estructurada de un archivo."""
    ruta_relativa: str
    modulo: str
    docstring: str
    lineas_codigo: int
    clases: List[ClaseInfo]
    funciones_publicas: List[str]
    imports_internos: List[str]  # Imports de módulos de Bell
    imports_externos: List[str]  # Imports de librerías externas
    usa_abc: bool
    usa_typing: bool
    es_test: bool
    es_demo: bool
    es_legacy: bool
    estado: str  # 'ACTIVO', 'LEGACY', 'TEST', 'DEMO'


@dataclass
class ModuloInfo:
    """Información de un módulo completo."""
    nombre: str
    total_archivos: int
    total_clases: int
    total_funciones: int
    total_lineas: int
    archivos: List[str]
    dependencias: Set[str]
    estado: str


class AnalizadorBelladonna:
    """Analizador arquitectónico de Belladonna."""
    
    def __init__(self, raiz: Path = Path('.')):
        self.raiz = raiz
        self.ignorar = {
            '__pycache__', '.git', 'venv', '.venv', 'env',
            '.pytest_cache', '.coverage', 'htmlcov', 'node_modules',
            '.mypy_cache', 'dist', 'build', '*.egg-info'
        }
        
        # Módulos principales de Bell
        self.modulos_core = {
            'core', 'vocabulario', 'traduccion', 'razonamiento',
            'consejeras', 'generacion', 'grounding', 'memoria',
            'bucles', 'aprendizaje', 'operaciones', 'base_datos',
            'llm', 'planificacion'
        }
        
        # Datos recopilados
        self.archivos: Dict[str, ArchivoInfo] = {}
        self.modulos: Dict[str, ModuloInfo] = {}
        self.grafo_dependencias: Dict[str, Set[str]] = defaultdict(set)
        self.clases_por_herencia: Dict[str, List[str]] = defaultdict(list)
        self.archivos_huerfanos: List[str] = []
        self.codigo_obsoleto: List[Tuple[str, str]] = []
        
    def analizar_todo(self):
        """Ejecuta análisis completo del proyecto."""
        print("=" * 80)
        print("BELL INVENTORY - AUDITORÍA ARQUITECTÓNICA")
        print("=" * 80)
        print()
        
        archivos_py = self._encontrar_archivos_python()
        print(f"📊 Analizando {len(archivos_py)} archivos Python...")
        print()
        
        # Fase 1: Analizar cada archivo
        for idx, archivo in enumerate(archivos_py, 1):
            print(f"  [{idx}/{len(archivos_py)}] {archivo.relative_to(self.raiz)}", end='\r')
            info = self._analizar_archivo(archivo)
            if info:
                self.archivos[str(archivo.relative_to(self.raiz))] = info
        
        print("\n")
        
        # Fase 2: Construir grafo de dependencias
        print("🔗 Construyendo grafo de dependencias...")
        self._construir_grafo_dependencias()
        
        # Fase 3: Analizar módulos
        print("📦 Analizando módulos...")
        self._analizar_modulos()
        
        # Fase 4: Detectar código obsoleto
        print("🔍 Detectando código obsoleto...")
        self._detectar_codigo_obsoleto()
        
        # Fase 5: Construir mapa de herencia
        print("🧬 Mapeando herencia de clases...")
        self._construir_mapa_herencia()
        
        print()
        print("✅ Análisis completado")
        print()
        
    def _encontrar_archivos_python(self) -> List[Path]:
        """Encuentra todos los archivos .py relevantes."""
        archivos = []
        
        for archivo in self.raiz.rglob('*.py'):
            # Ignorar directorios específicos
            if any(parte in self.ignorar for parte in archivo.parts):
                continue
            
            # Ignorar archivos de configuración
            if archivo.name in ['setup.py', 'conftest.py']:
                continue
                
            archivos.append(archivo)
        
        return sorted(archivos)
    
    def _analizar_archivo(self, archivo: Path) -> ArchivoInfo:
        """Analiza un archivo Python en profundidad."""
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            arbol = ast.parse(contenido, filename=str(archivo))
            
            # Determinar módulo
            partes = archivo.relative_to(self.raiz).parts
            if len(partes) > 1:
                modulo = partes[0]
            else:
                modulo = 'root'
            
            # Determinar estado
            es_test = 'test' in str(archivo).lower()
            es_demo = 'demo' in str(archivo).lower()
            es_legacy = '_legacy' in str(archivo) or 'legacy' in str(archivo).lower()
            
            if es_legacy:
                estado = 'LEGACY'
            elif es_test:
                estado = 'TEST'
            elif es_demo:
                estado = 'DEMO'
            else:
                estado = 'ACTIVO'
            
            info = ArchivoInfo(
                ruta_relativa=str(archivo.relative_to(self.raiz)),
                modulo=modulo,
                docstring=ast.get_docstring(arbol) or "",
                lineas_codigo=len([l for l in contenido.splitlines() if l.strip() and not l.strip().startswith('#')]),
                clases=self._extraer_clases(arbol),
                funciones_publicas=self._extraer_funciones_publicas(arbol),
                imports_internos=self._extraer_imports_internos(arbol),
                imports_externos=self._extraer_imports_externos(arbol),
                usa_abc=self._usa_abc(arbol),
                usa_typing=self._usa_typing(arbol),
                es_test=es_test,
                es_demo=es_demo,
                es_legacy=es_legacy,
                estado=estado
            )
            
            return info
            
        except Exception as e:
            print(f"\n⚠️  Error en {archivo}: {e}")
            return None
    
    def _extraer_clases(self, arbol: ast.AST) -> List[ClaseInfo]:
        """Extrae información detallada de clases."""
        clases = []
        
        for nodo in arbol.body:
            if isinstance(nodo, ast.ClassDef):
                metodos_pub = []
                metodos_priv = []
                tiene_init = False
                params_init = []
                
                for item in nodo.body:
                    if isinstance(item, ast.FunctionDef):
                        if item.name == '__init__':
                            tiene_init = True
                            params_init = [arg.arg for arg in item.args.args if arg.arg != 'self']
                        elif item.name.startswith('_') and not item.name.startswith('__'):
                            metodos_priv.append(item.name)
                        elif not item.name.startswith('_'):
                            metodos_pub.append(item.name)
                
                # Detectar si es abstracta
                es_abstracta = any(
                    isinstance(base, ast.Name) and base.id == 'ABC'
                    for base in nodo.bases
                )
                
                clase_info = ClaseInfo(
                    nombre=nodo.name,
                    hereda_de=[self._extraer_nombre_base(base) for base in nodo.bases],
                    metodos_publicos=metodos_pub,
                    metodos_privados=metodos_priv,
                    tiene_init=tiene_init,
                    params_init=params_init,
                    docstring=ast.get_docstring(nodo) or "",
                    linea_inicio=nodo.lineno,
                    es_abstracta=es_abstracta
                )
                clases.append(clase_info)
        
        return clases
    
    def _extraer_nombre_base(self, base: ast.expr) -> str:
        """Extrae el nombre de una clase base."""
        if isinstance(base, ast.Name):
            return base.id
        elif isinstance(base, ast.Attribute):
            return f"{base.value.id}.{base.attr}"
        return "Unknown"
    
    def _extraer_funciones_publicas(self, arbol: ast.AST) -> List[str]:
        """Extrae funciones públicas (no métodos)."""
        funciones = []
        
        for nodo in arbol.body:
            if isinstance(nodo, ast.FunctionDef):
                if not nodo.name.startswith('_'):
                    funciones.append(nodo.name)
        
        return funciones
    
    def _extraer_imports_internos(self, arbol: ast.AST) -> List[str]:
        """Extrae imports de módulos internos de Bell."""
        imports = []
        
        for nodo in ast.walk(arbol):
            if isinstance(nodo, ast.ImportFrom):
                if nodo.module and any(nodo.module.startswith(m) for m in self.modulos_core):
                    imports.append(nodo.module)
        
        return list(set(imports))
    
    def _extraer_imports_externos(self, arbol: ast.AST) -> List[str]:
        """Extrae imports de librerías externas."""
        imports = []
        
        for nodo in ast.walk(arbol):
            if isinstance(nodo, ast.Import):
                for alias in nodo.names:
                    if not any(alias.name.startswith(m) for m in self.modulos_core):
                        imports.append(alias.name.split('.')[0])
            
            elif isinstance(nodo, ast.ImportFrom):
                if nodo.module and not any(nodo.module.startswith(m) for m in self.modulos_core):
                    imports.append(nodo.module.split('.')[0])
        
        return list(set(imports))
    
    def _usa_abc(self, arbol: ast.AST) -> bool:
        """Detecta si el archivo usa ABC."""
        for nodo in ast.walk(arbol):
            if isinstance(nodo, ast.ImportFrom):
                if nodo.module == 'abc':
                    return True
        return False
    
    def _usa_typing(self, arbol: ast.AST) -> bool:
        """Detecta si el archivo usa typing."""
        for nodo in ast.walk(arbol):
            if isinstance(nodo, ast.ImportFrom):
                if nodo.module == 'typing':
                    return True
        return False
    
    def _construir_grafo_dependencias(self):
        """Construye grafo de dependencias entre módulos."""
        for ruta, info in self.archivos.items():
            modulo_origen = info.modulo
            
            for import_interno in info.imports_internos:
                modulo_destino = import_interno.split('.')[0]
                if modulo_destino in self.modulos_core:
                    self.grafo_dependencias[modulo_origen].add(modulo_destino)
    
    def _analizar_modulos(self):
        """Analiza estadísticas por módulo."""
        modulos_stats = defaultdict(lambda: {
            'archivos': [],
            'clases': 0,
            'funciones': 0,
            'lineas': 0,
            'dependencias': set()
        })
        
        for ruta, info in self.archivos.items():
            if info.estado == 'ACTIVO':  # Solo contar activos
                modulo = info.modulo
                modulos_stats[modulo]['archivos'].append(ruta)
                modulos_stats[modulo]['clases'] += len(info.clases)
                modulos_stats[modulo]['funciones'] += len(info.funciones_publicas)
                modulos_stats[modulo]['lineas'] += info.lineas_codigo
                modulos_stats[modulo]['dependencias'].update(info.imports_internos)
        
        for modulo, stats in modulos_stats.items():
            self.modulos[modulo] = ModuloInfo(
                nombre=modulo,
                total_archivos=len(stats['archivos']),
                total_clases=stats['clases'],
                total_funciones=stats['funciones'],
                total_lineas=stats['lineas'],
                archivos=stats['archivos'],
                dependencias=stats['dependencias'],
                estado='ACTIVO' if modulo in self.modulos_core else 'AUXILIAR'
            )
    
    def _detectar_codigo_obsoleto(self):
        """Detecta archivos potencialmente obsoletos."""
        for ruta, info in self.archivos.items():
            # Archivos legacy explícitos
            if info.es_legacy:
                self.codigo_obsoleto.append((ruta, "Carpeta _legacy"))
            
            # Archivos sin clases ni funciones
            elif not info.clases and not info.funciones_publicas and not info.es_test:
                if info.lineas_codigo > 10:  # Ignorar __init__.py vacíos
                    self.codigo_obsoleto.append((ruta, "Sin clases ni funciones públicas"))
            
            # Archivos que nadie importa (huérfanos)
            elif info.estado == 'ACTIVO':
                importado = False
                for otra_ruta, otra_info in self.archivos.items():
                    if ruta != otra_ruta:
                        # Verificar si alguien lo importa
                        modulo_actual = info.ruta_relativa.replace('/', '.').replace('\\', '.').replace('.py', '')
                        if any(modulo_actual in imp for imp in otra_info.imports_internos):
                            importado = True
                            break
                
                if not importado and info.modulo not in ['root', 'main']:
                    self.archivos_huerfanos.append(ruta)
    
    def _construir_mapa_herencia(self):
        """Construye mapa de herencia de clases."""
        for ruta, info in self.archivos.items():
            for clase in info.clases:
                for base in clase.hereda_de:
                    self.clases_por_herencia[base].append(f"{clase.nombre} ({ruta})")
    
    def generar_reporte_markdown(self) -> str:
        """Genera reporte visual en Markdown."""
        lineas = []
        
        lineas.append("# 🏗️ ARQUITECTURA DE BELLADONNA - MAPA COMPLETO")
        lineas.append(f"*Generado automáticamente por Bell_Inventory.py*")
        lineas.append("")
        lineas.append("---")
        lineas.append("")
        
        # Resumen ejecutivo
        lineas.append("## 📊 RESUMEN EJECUTIVO")
        lineas.append("")
        
        total_archivos = len(self.archivos)
        activos = sum(1 for info in self.archivos.values() if info.estado == 'ACTIVO')
        legacy = sum(1 for info in self.archivos.values() if info.estado == 'LEGACY')
        tests = sum(1 for info in self.archivos.values() if info.estado == 'TEST')
        
        lineas.append(f"- **Total de archivos**: {total_archivos}")
        lineas.append(f"- **Código activo**: {activos} archivos")
        lineas.append(f"- **Código legacy**: {legacy} archivos")
        lineas.append(f"- **Tests**: {tests} archivos")
        lineas.append(f"- **Módulos principales**: {len(self.modulos)}")
        lineas.append("")
        
        # Estado de salud
        lineas.append("### 🏥 Estado de Salud")
        lineas.append("")
        if len(self.codigo_obsoleto) > 0:
            lineas.append(f"⚠️  **{len(self.codigo_obsoleto)} archivos obsoletos detectados**")
        else:
            lineas.append("✅ No se detectaron archivos obsoletos")
        
        if len(self.archivos_huerfanos) > 0:
            lineas.append(f"⚠️  **{len(self.archivos_huerfanos)} archivos huérfanos** (nadie los importa)")
        else:
            lineas.append("✅ No hay archivos huérfanos")
        lineas.append("")
        lineas.append("---")
        lineas.append("")
        
        # Módulos principales
        lineas.append("## 📦 MÓDULOS PRINCIPALES")
        lineas.append("")
        
        for nombre, modulo in sorted(self.modulos.items(), key=lambda x: x[1].total_lineas, reverse=True):
            if modulo.estado == 'ACTIVO':
                lineas.append(f"### {nombre.upper()}")
                lineas.append("")
                lineas.append(f"- **Archivos**: {modulo.total_archivos}")
                lineas.append(f"- **Clases**: {modulo.total_clases}")
                lineas.append(f"- **Funciones**: {modulo.total_funciones}")
                lineas.append(f"- **Líneas de código**: {modulo.total_lineas}")
                
                if modulo.dependencias:
                    deps = [d.split('.')[0] for d in modulo.dependencias]
                    deps_unicas = sorted(set(deps))
                    lineas.append(f"- **Depende de**: {', '.join(deps_unicas)}")
                
                lineas.append("")
                
                # Listar archivos principales
                lineas.append("**Archivos clave:**")
                for archivo in sorted(modulo.archivos)[:5]:  # Top 5
                    info = self.archivos.get(archivo)
                    if info and info.docstring:
                        doc_primera_linea = info.docstring.split('\n')[0][:60]
                        lineas.append(f"- `{Path(archivo).name}` - {doc_primera_linea}")
                    else:
                        lineas.append(f"- `{Path(archivo).name}`")
                
                lineas.append("")
        
        lineas.append("---")
        lineas.append("")
        
        # Jerarquía de clases
        lineas.append("## 🧬 JERARQUÍA DE CLASES")
        lineas.append("")
        
        bases_importantes = ['ABC', 'BaseBucle', 'Consejera', 'DimensionGrounding', 'EstrategiaAprendizaje']
        
        for base in bases_importantes:
            if base in self.clases_por_herencia:
                lineas.append(f"### Heredan de `{base}`")
                lineas.append("")
                for clase_completa in sorted(self.clases_por_herencia[base])[:10]:  # Top 10
                    lineas.append(f"- {clase_completa}")
                lineas.append("")
        
        lineas.append("---")
        lineas.append("")
        
        # Código obsoleto
        if self.codigo_obsoleto:
            lineas.append("## ⚠️  CÓDIGO OBSOLETO DETECTADO")
            lineas.append("")
            lineas.append("Los siguientes archivos pueden estar obsoletos:")
            lineas.append("")
            
            for ruta, razon in self.codigo_obsoleto[:20]:  # Top 20
                lineas.append(f"- `{ruta}` - *{razon}*")
            
            lineas.append("")
            lineas.append("---")
            lineas.append("")
        
        # Dependencias externas
        lineas.append("## 📚 DEPENDENCIAS EXTERNAS")
        lineas.append("")
        
        deps_externas = Counter()
        for info in self.archivos.values():
            if info.estado == 'ACTIVO':
                for dep in info.imports_externos:
                    deps_externas[dep] += 1
        
        lineas.append("Librerías más usadas:")
        lineas.append("")
        for dep, count in deps_externas.most_common(15):
            lineas.append(f"- **{dep}** - usado en {count} archivos")
        
        lineas.append("")
        lineas.append("---")
        lineas.append("")
        
        # Recomendaciones
        lineas.append("## 💡 RECOMENDACIONES PARA FASE 4A")
        lineas.append("")
        
        lineas.append("### 1. Limpieza de Código")
        if len(self.codigo_obsoleto) > 5:
            lineas.append(f"- **CRÍTICO**: Mover {len(self.codigo_obsoleto)} archivos obsoletos a carpeta `_archive/`")
        else:
            lineas.append("- ✅ Base de código limpia")
        
        lineas.append("")
        lineas.append("### 2. Módulos Activos")
        lineas.append("Los siguientes módulos están listos para Fase 4A:")
        for nombre, modulo in sorted(self.modulos.items()):
            if modulo.estado == 'ACTIVO' and modulo.total_clases > 0:
                lineas.append(f"- ✅ **{nombre}** - {modulo.total_clases} clases, {modulo.total_funciones} funciones")
        
        lineas.append("")
        lineas.append("### 3. Puntos de Integración LLM")
        lineas.append("Módulos clave para conectar con Groq:")
        lineas.append("- `generacion/` - Generador de respuestas (ya existe)")
        lineas.append("- `razonamiento/` - Motor de decisiones (ya existe)")
        lineas.append("- `consejeras/sage/` - Filtro de coherencia (ya existe)")
        
        lineas.append("")
        lineas.append("---")
        lineas.append("")
        lineas.append("*Fin del reporte*")
        
        return "\n".join(lineas)
    
    def generar_datos_json(self) -> dict:
        """Genera datos estructurados para IAs."""
        return {
            "proyecto": "Belladonna",
            "version_analisis": "2.0",
            "timestamp": "GENERADO_AUTOMATICAMENTE",
            "resumen": {
                "total_archivos": len(self.archivos),
                "archivos_activos": sum(1 for info in self.archivos.values() if info.estado == 'ACTIVO'),
                "archivos_legacy": sum(1 for info in self.archivos.values() if info.estado == 'LEGACY'),
                "archivos_test": sum(1 for info in self.archivos.values() if info.estado == 'TEST'),
                "total_modulos": len(self.modulos),
                "codigo_obsoleto": len(self.codigo_obsoleto),
                "archivos_huerfanos": len(self.archivos_huerfanos)
            },
            "modulos": {
                nombre: {
                    "total_archivos": modulo.total_archivos,
                    "total_clases": modulo.total_clases,
                    "total_funciones": modulo.total_funciones,
                    "total_lineas": modulo.total_lineas,
                    "dependencias": list(modulo.dependencias),
                    "estado": modulo.estado
                }
                for nombre, modulo in self.modulos.items()
            },
            "archivos": {
                ruta: {
                    "modulo": info.modulo,
                    "estado": info.estado,
                    "lineas_codigo": info.lineas_codigo,
                    "total_clases": len(info.clases),
                    "clases": [
                        {
                            "nombre": clase.nombre,
                            "hereda_de": clase.hereda_de,
                            "metodos_publicos": clase.metodos_publicos,
                            "es_abstracta": clase.es_abstracta,
                            "tiene_init": clase.tiene_init
                        }
                        for clase in info.clases
                    ],
                    "funciones_publicas": info.funciones_publicas,
                    "imports_internos": info.imports_internos,
                    "imports_externos": info.imports_externos
                }
                for ruta, info in self.archivos.items()
                if info.estado == 'ACTIVO'  # Solo activos en JSON
            },
            "herencia": {
                base: [clase.split(' (')[0] for clase in clases]
                for base, clases in self.clases_por_herencia.items()
                if base in ['ABC', 'BaseBucle', 'Consejera', 'DimensionGrounding']
            },
            "codigo_obsoleto": [
                {"ruta": ruta, "razon": razon}
                for ruta, razon in self.codigo_obsoleto
            ]
        }
    
    def generar_health_check(self) -> str:
        """Genera diagnóstico de salud técnico."""
        lineas = []
        
        lineas.append("=" * 80)
        lineas.append("BELL HEALTH CHECK - DIAGNÓSTICO TÉCNICO")
        lineas.append("=" * 80)
        lineas.append("")
        
        # Estadísticas globales
        lineas.append("ESTADÍSTICAS GLOBALES")
        lineas.append("-" * 80)
        lineas.append(f"Total de archivos Python: {len(self.archivos)}")
        lineas.append(f"Archivos activos: {sum(1 for i in self.archivos.values() if i.estado == 'ACTIVO')}")
        lineas.append(f"Archivos legacy: {sum(1 for i in self.archivos.values() if i.estado == 'LEGACY')}")
        lineas.append(f"Tests: {sum(1 for i in self.archivos.values() if i.estado == 'TEST')}")
        lineas.append("")
        
        total_clases = sum(len(info.clases) for info in self.archivos.values() if info.estado == 'ACTIVO')
        total_funciones = sum(len(info.funciones_publicas) for info in self.archivos.values() if info.estado == 'ACTIVO')
        total_lineas = sum(info.lineas_codigo for info in self.archivos.values() if info.estado == 'ACTIVO')
        
        lineas.append(f"Total de clases (activas): {total_clases}")
        lineas.append(f"Total de funciones (activas): {total_funciones}")
        lineas.append(f"Total de líneas de código (activas): {total_lineas}")
        lineas.append("")
        
        # Estado de módulos
        lineas.append("ESTADO DE MÓDULOS PRINCIPALES")
        lineas.append("-" * 80)
        
        modulos_criticos = ['core', 'vocabulario', 'traduccion', 'razonamiento', 
                           'consejeras', 'generacion', 'grounding']
        
        for modulo in modulos_criticos:
            if modulo in self.modulos:
                info_modulo = self.modulos[modulo]
                status = "✅" if info_modulo.total_clases > 0 else "⚠️ "
                lineas.append(f"{status} {modulo.ljust(20)} - {info_modulo.total_archivos} archivos, {info_modulo.total_clases} clases")
            else:
                lineas.append(f"❌ {modulo.ljust(20)} - NO ENCONTRADO")
        
        lineas.append("")
        
        # Problemas detectados
        lineas.append("PROBLEMAS DETECTADOS")
        lineas.append("-" * 80)
        
        if not self.codigo_obsoleto and not self.archivos_huerfanos:
            lineas.append("✅ No se detectaron problemas")
        else:
            if self.codigo_obsoleto:
                lineas.append(f"⚠️  {len(self.codigo_obsoleto)} archivos obsoletos")
                for ruta, razon in self.codigo_obsoleto[:5]:
                    lineas.append(f"   - {ruta}")
                if len(self.codigo_obsoleto) > 5:
                    lineas.append(f"   ... y {len(self.codigo_obsoleto) - 5} más")
            
            if self.archivos_huerfanos:
                lineas.append(f"⚠️  {len(self.archivos_huerfanos)} archivos huérfanos (no importados)")
                for ruta in self.archivos_huerfanos[:5]:
                    lineas.append(f"   - {ruta}")
                if len(self.archivos_huerfanos) > 5:
                    lineas.append(f"   ... y {len(self.archivos_huerfanos) - 5} más")
        
        lineas.append("")
        
        # Recomendaciones
        lineas.append("RECOMENDACIONES")
        lineas.append("-" * 80)
        
        if len(self.codigo_obsoleto) > 10:
            lineas.append("🔴 CRÍTICO: Limpiar código obsoleto antes de Fase 4A")
        elif len(self.codigo_obsoleto) > 0:
            lineas.append("🟡 ADVERTENCIA: Considerar limpieza de código legacy")
        else:
            lineas.append("✅ Base de código limpia")
        
        lineas.append("")
        lineas.append("=" * 80)
        
        return "\n".join(lineas)


def main():
    """Función principal."""
    print()
    print("🔍 Iniciando auditoría de Belladonna...")
    print()
    
    analizador = AnalizadorBelladonna()
    analizador.analizar_todo()
    
    # Generar archivos de salida
    print("📝 Generando reportes...")
    print()
    
    # 1. Reporte Markdown (humanos)
    with open('BELL_ARCHITECTURE.md', 'w', encoding='utf-8') as f:
        f.write(analizador.generar_reporte_markdown())
    print("✅ BELL_ARCHITECTURE.md - Mapa visual para humanos")
    
    # 2. Datos JSON (IAs)
    with open('BELL_ARCHITECTURE.json', 'w', encoding='utf-8') as f:
        json.dump(analizador.generar_datos_json(), f, indent=2, ensure_ascii=False)
    print("✅ BELL_ARCHITECTURE.json - Datos estructurados para IAs")
    
    # 3. Health Check (diagnóstico)
    with open('BELL_HEALTH_CHECK.txt', 'w', encoding='utf-8') as f:
        f.write(analizador.generar_health_check())
    print("✅ BELL_HEALTH_CHECK.txt - Diagnóstico técnico")
    
    print()
    print("=" * 80)
    print("🎉 AUDITORÍA COMPLETADA")
    print("=" * 80)
    print()
    print("Archivos generados:")
    print("  1. BELL_ARCHITECTURE.md   - Para lectura humana")
    print("  2. BELL_ARCHITECTURE.json - Para procesamiento por IAs")
    print("  3. BELL_HEALTH_CHECK.txt  - Diagnóstico técnico")
    print()
    print("Estos archivos están listos para compartir con otras IAs (GPT, Gemini, etc.)")
    print()


if __name__ == '__main__':
    main()