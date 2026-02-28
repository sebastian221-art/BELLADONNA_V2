"""
Demo del Motor de Razonamiento - Semana 3.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from vocabulario.gestor_vocabulario import GestorVocabulario
from traduccion.traductor_entrada import TraductorEntrada
from razonamiento.motor_razonamiento import MotorRazonamiento

def main():
    print("=" * 90)
    print(" " * 25 + "🧠 DEMO: MOTOR DE RAZONAMIENTO 🧠")
    print("=" * 90)
    print()
    
    # Inicializar
    gestor = GestorVocabulario()
    traductor = TraductorEntrada(gestor)
    motor = MotorRazonamiento()
    
    print(f"✅ Sistema cargado: {len(gestor.obtener_todos())} conceptos")
    print()
    
    # Frases de prueba
    frases = [
        "Hola Bell",
        "¿Puedes leer archivos?",
        "¿Puedes modificar bases de datos?",
        "Gracias por tu ayuda",
        "¿Cómo puedo crear una función?",
        "xyz abc qwerty",
    ]
    
    print("🧠 DEMOSTRACIÓN DE RAZONAMIENTO")
    print("=" * 90)
    
    for i, frase in enumerate(frases, 1):
        print(f"\n{i}. \"{frase}\"")
        print("-" * 90)
        
        # Traducir
        traduccion = traductor.traducir(frase)
        print(f"   Traducción: {len(traduccion['conceptos'])} conceptos, "
              f"confianza {traduccion['confianza']:.0%}")
        
        # Razonar
        decision = motor.razonar(traduccion)
        
        # Mostrar decisión
        print(f"\n   🎯 DECISIÓN: {decision.tipo.name}")
        print(f"   Certeza: {decision.certeza:.0%}")
        print(f"   Puede ejecutar: {'✅ SÍ' if decision.puede_ejecutar else '❌ NO'}")
        
        if decision.operacion_disponible:
            print(f"   Operación: {decision.operacion_disponible}")
        
        print(f"\n   Razonamiento:")
        for paso in decision.pasos_razonamiento:
            print(f"     {paso}")
        
        print(f"\n   Conclusión: {decision.razon}")
    
    print("\n" + "=" * 90)
    print(" " * 30 + "✅ DEMO COMPLETADO")
    print("=" * 90)
    print()
    print("Capacidades demostradas:")
    print("  • Traducción Español → Conceptos")
    print("  • Evaluación de grounding")
    print("  • Generación de decisiones")
    print("  • Explicación de razonamiento")
    print()
    print("Próximo paso: Semana 4 - Vega (Guardiana de Principios)")
    print()

if __name__ == '__main__':
    main()