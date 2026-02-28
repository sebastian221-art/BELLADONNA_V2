#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
BELL STRUCTURE ANALYZER v2.0 — Para Obreros
═══════════════════════════════════════════════════════════════════════════════

Este script analiza la estructura COMPLETA de Bell y genera un reporte
que cualquier obrero puede entender para saber dónde modificar código.

USO:
    python bell_structure_analyzer_v2.py

SALIDA:
    bell_structure_report.md — Reporte completo en Markdown

Autor: Mile (Co-Arquitecta)
Versión: 2.0
═══════════════════════════════════════════════════════════════════════════════
"""
import ast
import sys
from pathlib import Path
from collections import defaultdict
from datetime import datetime

ROOT = Path(__file__).parent

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════════════════════════

CARPETAS_IGNORAR = {"__pycache__", ".venv", "venv", "node_modules", ".git", "tests"}

MODULOS_BELL = {
    "core": "Núcleo fundamental de Bell",
    "vocabulario": "Conceptos y palabras que Bell entiende",
    "traduccion": "Traduce español → lenguaje interno",
    "razonamiento": "Motor de pensamiento y decisiones",
    "consejeras": "Las 7 consejeras (mente de Bell)",
    "generacion": "Genera respuestas naturales",
    "grounding": "Sistema de anclaje 9D",
    "llm": "Integración con Groq/LLM",
    "memoria": "Memoria persistente",
    "aprendizaje": "Motor de aprendizaje",
    "bucles": "Bucles autónomos",
    "operaciones": "Operaciones de sistema",
    "base_datos": "Conexión SQLite",
    "config": "Configuración",
}


# ═══════════════════════════════════════════════════════════════════════════════
# PARSER DE ARCHIVOS PYTHON
# ═══════════════════════════════════════════════════════════════════════════════

def parsear_archivo(path: Path) -> dict:
    """Extrae información detallada de un archivo Python."""
    try:
        codigo = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(codigo, filename=str(path))
    except Exception as e:
        return {"error": str(e), "path": str(path)}
    
    info = {
        "path": str(path.relative_to(ROOT)),
        "lineas": codigo.count("\n") + 1,
        "imports_internos": [],
        "imports_externos": [],
        "clases": [],
        "funciones": [],
        "docstring": None,
        "error": None,
    }
    
    # Docstring del módulo
    if tree.body and isinstance(tree.body[0], ast.Expr):
        if isinstance(tree.body[0].value, ast.Constant):
            info["docstring"] = tree.body[0].value.value[:200]
    
    for node in ast.walk(tree):
        # Imports
        if isinstance(node, ast.ImportFrom) and node.module:
            modulo = node.module
            nombres = [a.name for a in node.names]
            base = modulo.split(".")[0]
            
            if base in MODULOS_BELL or (ROOT / base).exists():
                info["imports_internos"].append({
                    "from": modulo,
                    "names": nombres,
                })
            else:
                info["imports_externos"].append(modulo)
        
        elif isinstance(node, ast.Import):
            for alias in node.names:
                base = alias.name.split(".")[0]
                if base in MODULOS_BELL:
                    info["imports_internos"].append({"from": alias.name, "names": []})
                else:
                    info["imports_externos"].append(alias.name)
        
        # Clases
        elif isinstance(node, ast.ClassDef):
            metodos = []
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    metodos.append(item.name)
            
            info["clases"].append({
                "nombre": node.name,
                "metodos": metodos,
                "linea": node.lineno,
            })
        
        # Funciones de nivel superior
        elif isinstance(node, ast.FunctionDef) and node.col_offset == 0:
            info["funciones"].append({
                "nombre": node.name,
                "linea": node.lineno,
            })
    
    info["imports_externos"] = list(set(info["imports_externos"]))
    return info


# ═══════════════════════════════════════════════════════════════════════════════
# ANÁLISIS COMPLETO
# ═══════════════════════════════════════════════════════════════════════════════

def analizar_proyecto() -> dict:
    """Analiza todo el proyecto Bell."""
    
    archivos = {}
    modulos = defaultdict(list)
    dependencias = defaultdict(set)
    
    # Encontrar todos los archivos Python
    py_files = [
        p for p in ROOT.rglob("*.py")
        if not any(x in p.parts for x in CARPETAS_IGNORAR)
        and p.name != Path(__file__).name
    ]
    
    print(f"📂 Encontrados {len(py_files)} archivos Python")
    
    for path in sorted(py_files):
        info = parsear_archivo(path)
        rel = info["path"]
        archivos[rel] = info
        
        # Agrupar por módulo
        partes = Path(rel).parts
        if len(partes) > 1:
            modulo = partes[0]
            modulos[modulo].append(rel)
        
        # Construir grafo de dependencias
        for imp in info.get("imports_internos", []):
            mod_importado = imp["from"].split(".")[0]
            mod_actual = partes[0] if len(partes) > 1 else "root"
            if mod_importado != mod_actual:
                dependencias[mod_actual].add(mod_importado)
    
    # Detectar huérfanos
    importados = set()
    for info in archivos.values():
        for imp in info.get("imports_internos", []):
            # Convertir import a path
            imp_path = imp["from"].replace(".", "/") + ".py"
            importados.add(imp_path)
            # También el __init__
            base = imp["from"].split(".")[0]
            importados.add(f"{base}/__init__.py")
    
    huerfanos = []
    for rel in archivos:
        if rel == "main.py" or "__init__" in rel:
            continue
        rel_norm = rel.replace("\\", "/")
        if not any(rel_norm.endswith(i.replace("\\", "/")) for i in importados):
            # Verificar si el módulo es importado directamente
            mod_str = rel_norm.replace("/", ".").replace(".py", "")
            if not any(mod_str in str(imp) for imp in importados):
                huerfanos.append(rel)
    
    # Analizar main.py
    main_info = archivos.get("main.py", {})
    
    # Analizar consejeras
    consejeras = {
        "archivos": [r for r in archivos if "consejeras" in r and "gestor" not in r and "__init__" not in r],
        "gestor": next((r for r in archivos if "consejeras" in r and "gestor" in r), None),
    }
    
    # Analizar LLM/Groq
    llm_archivos = {r: archivos[r] for r in archivos if "llm" in r.lower() or "groq" in r.lower()}
    
    # Analizar generación
    gen_archivos = {r: archivos[r] for r in archivos if "generacion" in r}
    
    # Analizar razonamiento
    razon_archivos = {r: archivos[r] for r in archivos if "razonamiento" in r}
    
    return {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "resumen": {
            "total_archivos": len(archivos),
            "total_clases": sum(len(i.get("clases", [])) for i in archivos.values()),
            "total_funciones": sum(len(i.get("funciones", [])) for i in archivos.values()),
            "total_lineas": sum(i.get("lineas", 0) for i in archivos.values()),
            "total_modulos": len(modulos),
            "huerfanos": len(huerfanos),
        },
        "modulos": dict(modulos),
        "dependencias": {k: list(v) for k, v in dependencias.items()},
        "huerfanos": sorted(huerfanos),
        "main": {
            "imports": [i["from"] for i in main_info.get("imports_internos", [])],
            "clases": [c["nombre"] for c in main_info.get("clases", [])],
        },
        "consejeras": consejeras,
        "llm": llm_archivos,
        "generacion": gen_archivos,
        "razonamiento": razon_archivos,
        "archivos": archivos,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# GENERADOR DE REPORTE MARKDOWN
# ═══════════════════════════════════════════════════════════════════════════════

def generar_reporte(data: dict) -> str:
    """Genera un reporte Markdown completo y fácil de entender."""
    
    r = data["resumen"]
    
    lines = [
        "# 🔬 BELL STRUCTURE ANALYZER v2.0",
        f"\n**Fecha:** {data['fecha']}",
        "",
        "---",
        "",
        "## 📊 RESUMEN EJECUTIVO",
        "",
        "```",
        f"Total archivos:    {r['total_archivos']:4d}",
        f"Total clases:      {r['total_clases']:4d}",
        f"Total funciones:   {r['total_funciones']:4d}",
        f"Total líneas:      {r['total_lineas']:4d}",
        f"Módulos:           {r['total_modulos']:4d}",
        f"Huérfanos:         {r['huerfanos']:4d}",
        "```",
        "",
        "---",
        "",
        "## 🗂️ MÓDULOS DE BELL",
        "",
        "| Módulo | Archivos | Descripción |",
        "|--------|----------|-------------|",
    ]
    
    for modulo, archivos in sorted(data["modulos"].items()):
        desc = MODULOS_BELL.get(modulo, "—")
        lines.append(f"| `{modulo}` | {len(archivos)} | {desc} |")
    
    # main.py
    lines.extend([
        "",
        "---",
        "",
        "## 🚀 PUNTO DE ENTRADA: main.py",
        "",
        "### Imports internos:",
        "",
    ])
    
    for imp in sorted(data["main"].get("imports", [])):
        lines.append(f"- `{imp}`")
    
    if data["main"].get("clases"):
        lines.extend([
            "",
            "### Clases definidas:",
            "",
        ])
        for cls in data["main"]["clases"]:
            lines.append(f"- `{cls}`")
    
    # Dependencias entre módulos
    lines.extend([
        "",
        "---",
        "",
        "## 🔗 DEPENDENCIAS ENTRE MÓDULOS",
        "",
        "```",
    ])
    
    for modulo, deps in sorted(data["dependencias"].items()):
        if deps:
            lines.append(f"{modulo} → {', '.join(sorted(deps))}")
    
    lines.append("```")
    
    # Consejeras
    lines.extend([
        "",
        "---",
        "",
        "## 👥 CONSEJERAS (La mente de Bell)",
        "",
        f"**Gestor:** `{data['consejeras'].get('gestor', 'No encontrado')}`",
        "",
        "**Consejeras encontradas:**",
        "",
    ])
    
    for c in sorted(data["consejeras"].get("archivos", [])):
        lines.append(f"- `{c}`")
    
    # Razonamiento (IMPORTANTE para el clasificador)
    lines.extend([
        "",
        "---",
        "",
        "## 🧠 RAZONAMIENTO (Donde va el clasificador)",
        "",
    ])
    
    for path, info in sorted(data["razonamiento"].items()):
        lines.append(f"### `{path}`")
        lines.append(f"- Líneas: {info.get('lineas', 0)}")
        
        if info.get("clases"):
            lines.append("- Clases:")
            for cls in info["clases"]:
                metodos_str = ", ".join(cls["metodos"][:5])
                if len(cls["metodos"]) > 5:
                    metodos_str += f" (+{len(cls['metodos'])-5} más)"
                lines.append(f"  - `{cls['nombre']}`: {metodos_str}")
        
        if info.get("funciones"):
            lines.append("- Funciones:")
            for fn in info["funciones"][:5]:
                lines.append(f"  - `{fn['nombre']}()`")
        
        lines.append("")
    
    # Generación
    lines.extend([
        "",
        "---",
        "",
        "## 💬 GENERACIÓN (Respuestas naturales)",
        "",
    ])
    
    for path, info in sorted(data["generacion"].items()):
        lines.append(f"### `{path}`")
        lines.append(f"- Líneas: {info.get('lineas', 0)}")
        
        if info.get("clases"):
            for cls in info["clases"]:
                lines.append(f"- Clase: `{cls['nombre']}`")
        
        lines.append("")
    
    # LLM/Groq
    lines.extend([
        "",
        "---",
        "",
        "## 🤖 LLM / GROQ",
        "",
    ])
    
    for path, info in sorted(data["llm"].items()):
        lines.append(f"### `{path}`")
        lines.append(f"- Líneas: {info.get('lineas', 0)}")
        
        if info.get("clases"):
            for cls in info["clases"]:
                lines.append(f"- Clase: `{cls['nombre']}`")
                if cls["metodos"]:
                    lines.append(f"  - Métodos: {', '.join(cls['metodos'][:8])}")
        
        deps_ext = info.get("imports_externos", [])
        if deps_ext:
            lines.append(f"- Dependencias externas: {', '.join(deps_ext[:5])}")
        
        lines.append("")
    
    # Huérfanos
    if data["huerfanos"]:
        lines.extend([
            "",
            "---",
            "",
            "## ⚠️ ARCHIVOS HUÉRFANOS",
            "",
            "Estos archivos NO son importados por nadie:",
            "",
        ])
        
        for h in data["huerfanos"]:
            lines.append(f"- `{h}`")
    else:
        lines.extend([
            "",
            "---",
            "",
            "## ✅ NO HAY ARCHIVOS HUÉRFANOS",
            "",
        ])
    
    # Guía para el obrero
    lines.extend([
        "",
        "---",
        "",
        "## 📋 GUÍA RÁPIDA PARA OBREROS",
        "",
        "### ¿Dónde modifico para...?",
        "",
        "| Tarea | Archivo |",
        "|-------|---------|",
        "| Agregar tipo de decisión | `razonamiento/tipos_decision.py` |",
        "| Modificar el motor de razonamiento | `razonamiento/motor_razonamiento.py` |",
        "| Agregar prompts para Groq | `generacion/prompts_naturales.py` |",
        "| Modificar generación de respuestas | `generacion/generador_salida.py` |",
        "| Agregar conceptos | `vocabulario/expansion/*.py` |",
        "| Configurar Groq | `llm/groq_wrapper.py` |",
        "",
        "### NO TOCAR (a menos que se indique):",
        "",
        "- `core/*` — Estructuras fundamentales",
        "- `consejeras/*` — Sistema de consejeras",
        "- `main.py` — Punto de entrada",
        "",
        "---",
        "",
        "*Reporte generado automáticamente por bell_structure_analyzer_v2.py*",
    ])
    
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("   BELL STRUCTURE ANALYZER v2.0")
    print("=" * 70)
    print()
    
    print("🔍 Analizando estructura de Bell...")
    data = analizar_proyecto()
    
    print("📝 Generando reporte...")
    reporte = generar_reporte(data)
    
    out_path = ROOT / "bell_structure_report.md"
    out_path.write_text(reporte, encoding="utf-8")
    
    print(f"\n✅ Reporte guardado: {out_path}")
    
    r = data["resumen"]
    print(f"""
╔══════════════════════════════════════════════════════════════════════╗
║  RESUMEN RÁPIDO                                                      ║
╠══════════════════════════════════════════════════════════════════════╣
║  Archivos: {r['total_archivos']:4d}  │  Clases: {r['total_clases']:4d}  │  Líneas: {r['total_lineas']:5d}           ║
║  Módulos:  {r['total_modulos']:4d}  │  Huérfanos: {r['huerfanos']:3d}                              ║
╚══════════════════════════════════════════════════════════════════════╝
""")