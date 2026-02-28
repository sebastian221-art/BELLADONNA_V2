"""
Demo del Traductor de Entrada - Semana 2.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from traduccion.traductor_entrada import TraductorEntrada
from vocabulario.gestor_vocabulario import GestorVocabulario

def main():
    print("=" * 80)
    print(" " * 20 + "🌿 DEMO: TRADUCTOR DE ENTRADA 🌿")
    print("=" * 80)
    print()
    
    # Inicializar
    gestor = GestorVocabulario()
    traductor = TraductorEntrada(gestor)
    
    print(f"✅ Vocabulario cargado: {len(gestor.obtener_todos())} conceptos")
    print()
    
    # Frases de prueba
    frases_test = [
        "Hola Bell",
        "¿Puedes leer archivos?",
        "Gracias por tu ayuda",
        "¿Cómo puedo crear una función?",
        "Necesito ayuda para entender variables",
        "xyzabc palabra inventada",
    ]
    
    print("🔄 PRUEBAS DE TRADUCCIÓN")
    print("=" * 80)
    
    for i, frase in enumerate(frases_test, 1):
        print(f"\n{i}. \"{frase}\"")
        print("-" * 80)
        
        resultado = traductor.traducir(frase)
        
        # Mostrar resultados
        print(f"   Intención: {resultado['intencion']}")
        print(f"   Confianza: {resultado['confianza']:.0%}")
        print(f"   Conceptos: {resultado['conceptos_ids']}")
        
        if resultado['palabras_desconocidas']:
            print(f"   ⚠️  Desconocidas: {resultado['palabras_desconocidas']}")
        
        # Evaluación
        if resultado['confianza'] >= 0.9:
            print("   ✅ EXCELENTE traducción")
        elif resultado['confianza'] >= 0.7:
            print("   🟢 BUENA traducción")
        elif resultado['confianza'] >= 0.5:
            print("   🟡 REGULAR traducción")
        else:
            print("   🔴 MALA traducción")
    
    print("\n" + "=" * 80)
    print(" " * 25 + "✅ DEMO COMPLETADO")
    print("=" * 80)
    print()
    print("Logros:")
    print("  • Traductor funcional")
    print("  • Detección de intenciones")
    print("  • Cálculo de confianza")
    print("  • Manejo de palabras desconocidas")
    print()

if __name__ == '__main__':
    main()