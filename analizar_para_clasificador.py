#!/usr/bin/env python3
"""
ANALIZADOR v3 - Simplificado
"""
import sys
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent))

def main():
    print("\n" + "=" * 70)
    print("   ANALIZADOR DE VOCABULARIO v3")
    print("=" * 70)
    
    # Cargar
    print("\n📦 Cargando vocabulario...")
    from vocabulario.gestor_vocabulario import GestorVocabulario
    gestor = GestorVocabulario(cargar_expansion=True)
    
    # Obtener conceptos (puede ser lista o dict)
    conceptos_raw = gestor._conceptos if hasattr(gestor, '_conceptos') else gestor.conceptos
    
    # Convertir a dict si es lista
    if isinstance(conceptos_raw, list):
        conceptos = {c.id: c for c in conceptos_raw}
    else:
        conceptos = conceptos_raw
    
    print(f"✅ Total conceptos: {len(conceptos)}")
    
    # Crear índice palabra -> concepto
    palabra_a_id = defaultdict(list)
    for id_c, c in conceptos.items():
        palabras = getattr(c, 'palabras_español', []) or getattr(c, 'palabras_espanol', []) or []
        for p in palabras:
            palabra_a_id[p.lower()].append(id_c)
    
    print(f"✅ Índice de palabras: {len(palabra_a_id)} palabras únicas")
    
    # ═══════════════════════════════════════════════════════════════════
    # ANÁLISIS DE TRIGGERS
    # ═══════════════════════════════════════════════════════════════════
    
    TRIGGERS = {
        "IDENTIDAD_BELL": ["quién", "quien", "qué eres", "nombre", "llamas", "presentar", "eres"],
        "ESTADO_BELL": ["cómo", "como", "estás", "estas", "estar", "sentir", "bien", "tal", "vas"],
        "CAPACIDAD_BELL": ["puedes", "poder", "saber", "sabes", "hacer", "haces", "capaz", "sirves"],
        "SOCIAL": ["hola", "hey", "buenos", "buenas", "adiós", "adios", "chao", "bye", "gracias", "perdón", "disculpa"],
        "ESTADO_USUARIO": ["estoy", "me siento", "feliz", "frustrado", "confundido", "triste", "enojado", "cansado", "perdido"],
        "ACCION_COGNITIVA": ["explicar", "explica", "explícame", "resumir", "simplificar", "aclarar", "repetir"],
        "CONFIRMACION": ["sí", "si", "ok", "okay", "entendido", "perfecto", "correcto", "dale", "vale", "claro", "no", "mal"],
    }
    
    print("\n" + "=" * 70)
    print("ANÁLISIS DE TRIGGERS POR CATEGORÍA")
    print("=" * 70)
    
    for categoria, palabras in TRIGGERS.items():
        print(f"\n📂 {categoria}:")
        encontrados = 0
        for palabra in palabras:
            if palabra in palabra_a_id:
                ids = palabra_a_id[palabra][:2]
                print(f"   ✅ '{palabra}' → {ids}")
                encontrados += 1
            else:
                # Buscar parcial
                parciales = [p for p in palabra_a_id.keys() if palabra in p][:1]
                if parciales:
                    print(f"   🔄 '{palabra}' → parcial '{parciales[0]}' → {palabra_a_id[parciales[0]][:1]}")
                    encontrados += 1
                else:
                    print(f"   ❌ '{palabra}' → NO ENCONTRADO")
        
        pct = encontrados / len(palabras) * 100
        print(f"   Cobertura: {encontrados}/{len(palabras)} ({pct:.0f}%)")
    
    # ═══════════════════════════════════════════════════════════════════
    # ANÁLISIS DE PROPIEDADES
    # ═══════════════════════════════════════════════════════════════════
    
    print("\n" + "=" * 70)
    print("ANÁLISIS DE PROPIEDADES")
    print("=" * 70)
    
    props_count = defaultdict(int)
    props_ejemplos = defaultdict(list)
    
    for id_c, c in conceptos.items():
        props = getattr(c, 'propiedades', {}) or {}
        for prop, val in props.items():
            props_count[prop] += 1
            if len(props_ejemplos[prop]) < 2:
                props_ejemplos[prop].append((id_c, val))
    
    # Propiedades críticas
    props_criticas = [
        "es_estado_emocional", "valencia", "tono_recomendado", "accion_sugerida",
        "es_comunicacion", "bell_puede_ejecutar", "es_interrogativa"
    ]
    
    print("\n🎯 Propiedades CRÍTICAS para el clasificador:\n")
    for prop in props_criticas:
        count = props_count.get(prop, 0)
        estado = "✅" if count >= 5 else "⚠️" if count > 0 else "❌"
        print(f"   {estado} {prop}: {count} conceptos")
        for ej in props_ejemplos.get(prop, []):
            print(f"      └─ {ej[0]}: {ej[1]}")
    
    print(f"\n📋 Top 15 propiedades más usadas:\n")
    for prop, count in sorted(props_count.items(), key=lambda x: -x[1])[:15]:
        print(f"   • {prop}: {count}")
    
    # ═══════════════════════════════════════════════════════════════════
    # ANÁLISIS DE TIPOS
    # ═══════════════════════════════════════════════════════════════════
    
    print("\n" + "=" * 70)
    print("ANÁLISIS DE TIPOS DE CONCEPTOS")
    print("=" * 70)
    
    tipos_count = defaultdict(int)
    for id_c, c in conceptos.items():
        tipo = str(getattr(c, 'tipo', 'DESCONOCIDO'))
        tipos_count[tipo] += 1
    
    print()
    for tipo, count in sorted(tipos_count.items(), key=lambda x: -x[1]):
        pct = count / len(conceptos) * 100
        print(f"   • {tipo}: {count} ({pct:.1f}%)")
    
    # ═══════════════════════════════════════════════════════════════════
    # BÚSQUEDA ESPECÍFICA
    # ═══════════════════════════════════════════════════════════════════
    
    print("\n" + "=" * 70)
    print("CONCEPTOS CON PROPIEDADES DE EMOCIÓN")
    print("=" * 70)
    
    emocionales = []
    for id_c, c in conceptos.items():
        props = getattr(c, 'propiedades', {}) or {}
        if props.get('es_estado_emocional') or props.get('valencia'):
            emocionales.append((id_c, props.get('valencia', '?'), props.get('tono_recomendado', '?')))
    
    print(f"\n📊 Total conceptos emocionales: {len(emocionales)}\n")
    for id_c, valencia, tono in emocionales[:15]:
        print(f"   • {id_c}: valencia={valencia}, tono={tono}")
    if len(emocionales) > 15:
        print(f"   ... y {len(emocionales) - 15} más")
    
    # ═══════════════════════════════════════════════════════════════════
    # RESUMEN FINAL
    # ═══════════════════════════════════════════════════════════════════
    
    print("\n" + "=" * 70)
    print("📋 RESUMEN FINAL")
    print("=" * 70)
    
    # Calcular cobertura total
    total_palabras = sum(len(p) for p in TRIGGERS.values())
    total_encontradas = 0
    for palabras in TRIGGERS.values():
        for palabra in palabras:
            if palabra in palabra_a_id or any(palabra in p for p in palabra_a_id.keys()):
                total_encontradas += 1
    
    cobertura = total_encontradas / total_palabras * 100
    
    print(f"""
┌─────────────────────────────────────────────────────────────────────┐
│  Total conceptos:          {len(conceptos):5d}                              │
│  Palabras únicas:          {len(palabra_a_id):5d}                              │
│  Conceptos emocionales:    {len(emocionales):5d}                              │
│  Cobertura triggers:       {cobertura:5.1f}%                             │
└─────────────────────────────────────────────────────────────────────┘
""")
    
    if cobertura >= 70:
        print("   ✅ COBERTURA SUFICIENTE - Podemos crear el paquete de obrero")
    elif cobertura >= 50:
        print("   ⚠️  COBERTURA PARCIAL - Funciona pero con limitaciones")
    else:
        print("   ❌ COBERTURA BAJA - Necesitamos crear más conceptos")
    
    print("\n" + "=" * 70)
    print("   FIN DEL ANÁLISIS")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()