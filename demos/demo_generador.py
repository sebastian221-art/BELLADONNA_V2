"""
Demo del Generador de Salida - Semana 5.
Bell habla por primera vez.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from vocabulario.gestor_vocabulario import GestorVocabulario
from traduccion.traductor_entrada import TraductorEntrada
from razonamiento.motor_razonamiento import MotorRazonamiento
from consejeras.vega import Vega
from generacion.generador_salida import GeneradorSalida

def main():
    print("=" * 90)
    print(" " * 25 + "💬 DEMO: BELL HABLA 💬")
    print("=" * 90)
    print()
    
    # Inicializar sistema completo
    gestor = GestorVocabulario()
    traductor = TraductorEntrada(gestor)
    motor = MotorRazonamiento()
    vega = Vega()
    generador = GeneradorSalida()
    
    print(f"✅ Sistema cargado: {len(gestor.obtener_todos())} conceptos")
    print()
    
    # Conversaciones de prueba
    conversaciones = [
        "Hola Bell",
        "¿Puedes leer archivos?",
        "¿Puedes escribir archivos?",
        "Elimina todos mis archivos",
        "Lee mi archivo de contraseñas",
        "Gracias por tu ayuda",
        "¿Cómo puedes ayudarme?",
        "xyz abc qwerty",
    ]
    
    print("💬 CONVERSACIÓN CON BELL")
    print("=" * 90)
    
    for i, mensaje_usuario in enumerate(conversaciones, 1):
        print(f"\n{i}. Usuario: \"{mensaje_usuario}\"")
        print("-" * 90)
        
        # FLUJO COMPLETO
        traduccion = traductor.traducir(mensaje_usuario)
        decision = motor.razonar(traduccion)
        revision = vega.revisar(decision, {'traduccion': traduccion})
        
        # GENERAR RESPUESTA
        respuesta = generador.generar(decision, {
            'traduccion': traduccion,
            'revision_vega': revision
        })
        
        print(f"   Bell: \"{respuesta}\"")
        
        # Metadata (solo para demo)
        print(f"\n   [Metadata: {decision.tipo.name}, certeza={decision.certeza:.0%}, "
              f"veto={revision['veto']}]")
    
    print("\n" + "=" * 90)
    print(" " * 30 + "✅ DEMO COMPLETADO")
    print("=" * 90)
    print()
    print("🎉 ¡BELL PUEDE CONVERSAR!")
    print()
    print("Capacidades demostradas:")
    print("  • Flujo completo: Español → Conceptos → Razonamiento → Vega → Español")
    print("  • Respuestas naturales en español")
    print("  • Explicación de vetos de Vega")
    print("  • Manejo de casos no entendidos")
    print()
    print("Próximo paso: Semana 6 - Loop conversacional interactivo")
    print()

if __name__ == '__main__':
    main()