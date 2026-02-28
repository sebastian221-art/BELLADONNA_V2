#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
BELL DUPLICATE ANALYZER v2.0 — Para Obreros
═══════════════════════════════════════════════════════════════════════════════

Este script analiza el vocabulario de Bell y detecta palabras duplicadas
que podrían causar confusión. Genera un reporte claro para obreros.

USO:
    python bell_duplicate_analyzer_v2.py

SALIDA:
    bell_duplicates_report.md — Reporte completo en Markdown

Autor: Mile (Co-Arquitecta)
Versión: 2.0
═══════════════════════════════════════════════════════════════════════════════
"""
import sys
from pathlib import Path
from collections import defaultdict
from datetime import datetime

ROOT = Path(__file__).parent

# ═══════════════════════════════════════════════════════════════════════════════
# CATEGORÍAS DE GRAVEDAD
# ═══════════════════════════════════════════════════════════════════════════════

GRAVEDAD_INFO = {
    "CRITICO": {
        "emoji": "🔴",
        "descripcion": "Dos conceptos EJECUTABLES comparten palabra — Bell puede ejecutar la ACCIÓN EQUIVOCADA",
        "accion": "RESOLVER INMEDIATAMENTE",
    },
    "ALTO": {
        "emoji": "🟠", 
        "descripcion": "Ejecutable vs no-ejecutable — Bell puede confundir acción con descripción",
        "accion": "Resolver pronto",
    },
    "MEDIO": {
        "emoji": "🟡",
        "descripcion": "Mismo dominio semántico — ambigüedad real pero manejable",
        "accion": "Revisar si causa problemas",
    },
    "BAJO": {
        "emoji": "🟢",
        "descripcion": "Diferentes dominios — el contexto lo resuelve",
        "accion": "Ignorar (el traductor lo maneja)",
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# CARGA DEL VOCABULARIO
# ═══════════════════════════════════════════════════════════════════════════════

def cargar_vocabulario():
    """Carga el vocabulario de Bell."""
    try:
        if str(ROOT) not in sys.path:
            sys.path.insert(0, str(ROOT))
        
        from vocabulario.gestor_vocabulario import GestorVocabulario
        gestor = GestorVocabulario(cargar_expansion=True)
        
        conceptos = []
        for c in gestor.obtener_todos():
            # Obtener palabras
            palabras = []
            if hasattr(c, 'palabras_español'):
                palabras = list(c.palabras_español or [])
            elif hasattr(c, 'palabras_espanol'):
                palabras = list(c.palabras_espanol or [])
            
            # Obtener propiedades
            props = getattr(c, 'propiedades', {}) or {}
            
            # Determinar si es ejecutable
            puede_ejecutar = False
            if hasattr(c, 'operaciones') and c.operaciones:
                puede_ejecutar = True
            elif hasattr(c, 'tipo'):
                tipo_str = str(c.tipo)
                if 'OPERACION_SISTEMA' in tipo_str:
                    puede_ejecutar = True
            
            conceptos.append({
                "id": c.id,
                "palabras": palabras,
                "grounding": float(c.confianza_grounding),
                "tipo": str(c.tipo),
                "puede_ejecutar": puede_ejecutar,
                "propiedades": props,
            })
        
        return conceptos
    
    except Exception as e:
        print(f"❌ Error cargando vocabulario: {e}")
        import traceback
        traceback.print_exc()
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# ANÁLISIS DE DUPLICADOS
# ═══════════════════════════════════════════════════════════════════════════════

def detectar_gravedad(conceptos: list) -> str:
    """Determina la gravedad del conflicto."""
    ejecutables = [c for c in conceptos if c.get("puede_ejecutar")]
    
    if len(ejecutables) >= 2:
        return "CRITICO"
    
    if len(ejecutables) == 1:
        return "ALTO"
    
    # Verificar si son del mismo dominio
    dominios = set()
    for c in conceptos:
        tipo = c.get("tipo", "")
        if "OPERACION" in tipo:
            dominios.add("OPERACION")
        elif "PALABRA_CONVERSACION" in tipo:
            dominios.add("CONVERSACION")
        elif "ACCION_COGNITIVA" in tipo:
            dominios.add("COGNITIVA")
        else:
            dominios.add("OTRO")
    
    if len(dominios) == 1:
        return "MEDIO"
    
    return "BAJO"


def sugerir_solucion(palabra: str, conceptos: list, gravedad: str) -> str:
    """Sugiere cómo resolver el conflicto."""
    ids = [c["id"] for c in conceptos]
    ejecutables = [c["id"] for c in conceptos if c.get("puede_ejecutar")]
    
    if gravedad == "CRITICO":
        # Mantener el de mayor grounding
        ganador = max(conceptos, key=lambda c: c["grounding"])
        perdedores = [c["id"] for c in conceptos if c["id"] != ganador["id"]]
        return f"ELIMINAR '{palabra}' de {', '.join(perdedores)}. Mantener solo en {ganador['id']}"
    
    elif gravedad == "ALTO":
        no_exec = [c["id"] for c in conceptos if not c.get("puede_ejecutar")]
        return f"Renombrar '{palabra}' en {no_exec[0]} a algo más específico"
    
    elif gravedad == "MEDIO":
        return f"Agregar contexto diferenciador en cada concepto"
    
    else:
        return "OK - El traductor contextual lo resuelve automáticamente"


def analizar_duplicados(conceptos: list) -> dict:
    """Analiza todos los duplicados en el vocabulario."""
    
    # Indexar palabra → conceptos
    palabra_a_conceptos = defaultdict(list)
    for c in conceptos:
        for palabra in c.get("palabras", []):
            p = palabra.strip().lower()
            if len(p) > 1:  # Ignorar letras sueltas
                palabra_a_conceptos[p].append(c)
    
    # Filtrar solo duplicados
    duplicados = {p: cs for p, cs in palabra_a_conceptos.items() if len(cs) > 1}
    
    # Analizar cada duplicado
    analisis = []
    for palabra, cs in sorted(duplicados.items()):
        gravedad = detectar_gravedad(cs)
        analisis.append({
            "palabra": palabra,
            "gravedad": gravedad,
            "conceptos": [
                {
                    "id": c["id"],
                    "grounding": c["grounding"],
                    "ejecutable": c.get("puede_ejecutar", False),
                    "tipo": c.get("tipo", "?"),
                }
                for c in cs
            ],
            "solucion": sugerir_solucion(palabra, cs, gravedad),
        })
    
    # Ordenar por gravedad
    orden_gravedad = ["CRITICO", "ALTO", "MEDIO", "BAJO"]
    analisis.sort(key=lambda x: orden_gravedad.index(x["gravedad"]))
    
    # Estadísticas
    stats = defaultdict(int)
    for item in analisis:
        stats[item["gravedad"]] += 1
    
    # Conceptos más conflictivos
    conflictos_por_concepto = defaultdict(int)
    for item in analisis:
        for c in item["conceptos"]:
            conflictos_por_concepto[c["id"]] += 1
    
    top_conflictivos = sorted(conflictos_por_concepto.items(), key=lambda x: -x[1])[:10]
    
    return {
        "total_palabras": len(palabra_a_conceptos),
        "total_duplicados": len(duplicados),
        "porcentaje": round(len(duplicados) / max(len(palabra_a_conceptos), 1) * 100, 1),
        "por_gravedad": dict(stats),
        "top_conflictivos": top_conflictivos,
        "duplicados": analisis,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# GENERADOR DE REPORTE MARKDOWN
# ═══════════════════════════════════════════════════════════════════════════════

def generar_reporte(data: dict, total_conceptos: int) -> str:
    """Genera un reporte Markdown claro para obreros."""
    
    lines = [
        "# 🔍 BELL DUPLICATE ANALYZER v2.0",
        f"\n**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "---",
        "",
        "## 📊 RESUMEN EJECUTIVO",
        "",
        "```",
        f"Total conceptos:       {total_conceptos:5d}",
        f"Palabras únicas:       {data['total_palabras']:5d}",
        f"Palabras duplicadas:   {data['total_duplicados']:5d} ({data['porcentaje']}%)",
        "```",
        "",
        "---",
        "",
        "## 🚨 CONFLICTOS POR GRAVEDAD",
        "",
    ]
    
    for gravedad, info in GRAVEDAD_INFO.items():
        count = data["por_gravedad"].get(gravedad, 0)
        lines.append(f"### {info['emoji']} {gravedad}: {count} conflictos")
        lines.append(f"- **Qué significa:** {info['descripcion']}")
        lines.append(f"- **Acción:** {info['accion']}")
        lines.append("")
    
    # Top conceptos conflictivos
    lines.extend([
        "---",
        "",
        "## 🔥 CONCEPTOS MÁS CONFLICTIVOS",
        "",
        "Estos conceptos tienen más palabras en conflicto con otros:",
        "",
        "| Concepto | Conflictos |",
        "|----------|------------|",
    ])
    
    for cid, count in data["top_conflictivos"]:
        lines.append(f"| `{cid}` | {count} |")
    
    # Duplicados por gravedad
    lines.extend([
        "",
        "---",
        "",
        "## 📋 TODOS LOS DUPLICADOS",
        "",
    ])
    
    current_gravedad = None
    for item in data["duplicados"]:
        if item["gravedad"] != current_gravedad:
            current_gravedad = item["gravedad"]
            info = GRAVEDAD_INFO[current_gravedad]
            lines.extend([
                "",
                f"### {info['emoji']} {current_gravedad}",
                "",
            ])
        
        # Formatear conceptos
        conceptos_str = []
        for c in item["conceptos"]:
            exec_mark = "⚡" if c["ejecutable"] else "  "
            conceptos_str.append(f"{exec_mark}`{c['id']}`({c['grounding']})")
        
        lines.append(f"**`{item['palabra']}`**")
        lines.append(f"  - Conceptos: {' | '.join(conceptos_str)}")
        lines.append(f"  - ✏️ *{item['solucion']}*")
        lines.append("")
    
    # Guía para obreros
    lines.extend([
        "",
        "---",
        "",
        "## 📋 GUÍA PARA RESOLVER DUPLICADOS",
        "",
        "### Pasos para resolver un conflicto CRÍTICO:",
        "",
        "1. **Identificar el ganador:** El concepto con mayor grounding",
        "2. **Abrir el archivo** del concepto perdedor",
        "3. **Eliminar la palabra** de `palabras_español`",
        "4. **Agregar sinónimo** más específico si es necesario",
        "5. **Ejecutar tests** para verificar",
        "",
        "### Ejemplo:",
        "",
        "```python",
        "# ANTES (conflicto)",
        'CONCEPTO_A = ConceptoAnclado(',
        '    palabras_español=["file", "archivo"],  # ← "file" duplicado',
        ')',
        "",
        "# DESPUÉS (resuelto)",
        'CONCEPTO_A = ConceptoAnclado(',
        '    palabras_español=["archivo", "fichero"],  # ← "file" eliminado',
        ')',
        "```",
        "",
        "---",
        "",
        "*Reporte generado automáticamente por bell_duplicate_analyzer_v2.py*",
    ])
    
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("   BELL DUPLICATE ANALYZER v2.0")
    print("=" * 70)
    print()
    
    print("📦 Cargando vocabulario de Bell...")
    conceptos = cargar_vocabulario()
    
    if not conceptos:
        print("❌ No se pudo cargar el vocabulario")
        print("   Asegúrate de ejecutar desde el directorio raíz de BELLADONNA")
        sys.exit(1)
    
    print(f"✅ {len(conceptos)} conceptos cargados")
    
    print("🔬 Analizando duplicados...")
    data = analizar_duplicados(conceptos)
    
    print("📝 Generando reporte...")
    reporte = generar_reporte(data, len(conceptos))
    
    out_path = ROOT / "bell_duplicates_report.md"
    out_path.write_text(reporte, encoding="utf-8")
    
    print(f"\n✅ Reporte guardado: {out_path}")
    
    # Resumen en consola
    print(f"""
╔══════════════════════════════════════════════════════════════════════╗
║  RESUMEN DE DUPLICADOS                                               ║
╠══════════════════════════════════════════════════════════════════════╣""")
    
    for gravedad, info in GRAVEDAD_INFO.items():
        count = data["por_gravedad"].get(gravedad, 0)
        if count > 0:
            print(f"║  {info['emoji']} {gravedad:8} : {count:3d} conflictos                                    ║")
    
    print(f"""╠══════════════════════════════════════════════════════════════════════╣
║  Total palabras duplicadas: {data['total_duplicados']:4d} ({data['porcentaje']}%)                          ║
╚══════════════════════════════════════════════════════════════════════╝
""")
    
    # Advertencia si hay críticos
    criticos = data["por_gravedad"].get("CRITICO", 0)
    if criticos > 0:
        print(f"⚠️  ¡HAY {criticos} CONFLICTOS CRÍTICOS! Revisar el reporte.")