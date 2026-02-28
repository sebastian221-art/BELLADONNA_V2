"""
Demo Fase 2 - Sistema de Consejo Multi-Perspectiva.

Ejecutar: python demos/demo_fase2_consejo.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from vocabulario.gestor_vocabulario import GestorVocabulario
from traduccion.traductor_entrada import TraductorEntrada
from razonamiento.motor_razonamiento import MotorRazonamiento
from consejeras.gestor_consejeras import GestorConsejeras
from generacion.generador_salida import GeneradorSalida

def main():
    print("=" * 90)
    print(" " * 20 + "🌿 BELLADONNA FASE 2 - SISTEMA DE CONSEJO 🌿")
    print("=" * 90)
    print()
    
    # Inicializar
    print("Inicializando sistema...")
    gestor_vocab = GestorVocabulario()
    traductor = TraductorEntrada(gestor_vocab)
    motor = MotorRazonamiento()
    gestor_consejeras = GestorConsejeras(fase=2)
    generador = GeneradorSalida()
    
    print(f"✅ Vocabulario: {len(gestor_vocab.obtener_todos())} conceptos")
    print(f"✅ Consejeras: {len(gestor_consejeras.consejeras)}")
    
    for c in gestor_consejeras.consejeras:
        veto = "🛡️ VETA" if c.puede_vetar else "💭 Opina"
        print(f"   • {c.nombre:8} - {c.especialidad:30} [{veto}]")
    print()
    
    # Casos demostrativos
    casos = [
        ("¿Puedes leer archivos?", "Consenso aprobación"),
        ("Elimina todos los archivos", "VETO Vega"),
        ("No entiendo nada, ayuda", "Lyra empatía"),
        ("Urgente ya ahora mismo", "Luna intuición"),
    ]
    
    print("🧪 DEMOSTRACIÓN")
    print("=" * 90)
    
    for i, (mensaje, esperado) in enumerate(casos, 1):
        print(f"\nCASO {i}: {esperado}")
        print("-" * 90)
        print(f'Usuario: "{mensaje}"')
        print()
        
        # Procesar
        traduccion = traductor.traducir(mensaje)
        decision = motor.razonar(traduccion)
        resultado = gestor_consejeras.consultar_todas(decision, {'traduccion': traduccion})
        
        # Mostrar deliberación
        print("Consejeras:")
        for op in resultado['opiniones']:
            estado = "🛡️ VETO" if op.get('veto') else ("✅" if op['aprobada'] else "❌")
            print(f"  {op['consejera']:8} {estado} - {op['opinion']}")
        
        print()
        print(f"Resultado: {'VETADO' if resultado['veto'] else 'APROBADO'}")
        
        # Respuesta
        respuesta = generador.generar(decision, {
            'traduccion': traduccion,
            'revision_vega': resultado['opiniones'][0]
        })
        print(f'\nBell: "{respuesta}"')
        
        if i < len(casos):
            input("\n[ENTER para continuar...]")
    
    # Stats
    print("\n" + "=" * 90)
    print("ESTADÍSTICAS")
    print("=" * 90)
    
    for stats in gestor_consejeras.estadisticas_globales()['consejeras']:
        print(f"{stats['nombre']:8} - Revisiones: {stats['revisiones']}, Vetos: {stats['vetos']}")
    
    print()
    print("✅ FASE 2 DEMOSTRADA - Sistema de Consejo Funcional")
    print()

if __name__ == '__main__':
    main()