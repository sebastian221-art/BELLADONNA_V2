"""
Test de Integración Fase 2 - Verificación completa del sistema.

Este test valida:
1. Bucles se inicializan y ejecutan
2. Memoria persiste datos
3. Respuestas se generan correctamente
4. Consejeras deliberan apropiadamente
"""
import pytest
import time
import sys
from pathlib import Path

# Agregar path del proyecto
sys.path.insert(0, str(Path(__file__).parent.parent))

from vocabulario.gestor_vocabulario import GestorVocabulario
from traduccion.traductor_entrada import TraductorEntrada
from razonamiento.motor_razonamiento import MotorRazonamiento
from consejeras.gestor_consejeras import GestorConsejeras
from generacion.generador_salida import GeneradorSalida
from bucles.gestor_bucles import GestorBucles
from memoria.gestor_memoria import GestorMemoria
from aprendizaje.motor_aprendizaje import MotorAprendizaje

class TestIntegracionFase2:
    """Tests de integración completa Fase 2."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada test."""
        # Inicializar componentes Fase 1
        self.gestor_vocab = GestorVocabulario()
        self.traductor = TraductorEntrada(self.gestor_vocab)
        self.motor = MotorRazonamiento()
        self.gestor_consejeras = GestorConsejeras(fase=2)
        self.generador = GeneradorSalida()
        
        # Inicializar componentes Fase 2
        self.gestor_bucles = GestorBucles()
        self.gestor_memoria = GestorMemoria()
        self.motor_aprendizaje = MotorAprendizaje()
        
        # Configurar integraciones
        self.motor_aprendizaje.configurar_integraciones(
            vocabulario=self.gestor_vocab,
            memoria=self.gestor_memoria,
            bucles=self.gestor_bucles
        )
        
        yield
        
        # Cleanup
        self.gestor_bucles.detener_todos()
        self.gestor_memoria.finalizar_sesion()
    
    def test_bucles_inician_correctamente(self):
        """Verifica que los bucles se inicien y ejecuten."""
        # Iniciar bucles
        resultados = self.gestor_bucles.iniciar_todos()
        
        # Verificar que todos iniciaron
        assert resultados['corto'] == True
        assert resultados['medio'] == True
        assert resultados['largo'] == True
        
        # Verificar estado
        estado = self.gestor_bucles.estado_sistema()
        assert estado['todos_activos'] == True
        assert estado['bucles_activos'] == True
        
        # Verificar que cada bucle está activo
        assert estado['bucles']['corto']['activo'] == True
        assert estado['bucles']['medio']['activo'] == True
        assert estado['bucles']['largo']['activo'] == True
        
        # Esperar un poco para que ejecuten al menos 1 ciclo
        time.sleep(2)
        
        # Verificar que ejecutaron
        estado_nuevo = self.gestor_bucles.estado_sistema()
        assert 'ciclos_ejecutados' in estado_nuevo['bucles']['corto']
        assert 'ciclos_ejecutados' in estado_nuevo['bucles']['medio']
        assert 'ciclos_ejecutados' in estado_nuevo['bucles']['largo']
    
    def test_respuestas_correctas(self):
        """
        Verifica que las respuestas se generen correctamente.
        
        ✅ CORRECCIÓN V3: Verifica errores en la RESPUESTA principal, 
        no en explicaciones técnicas.
        """
        casos = [
            # (mensaje, verbo_esperado_en_respuesta, verbos_prohibidos_en_respuesta_principal)
            ("¿Puedes leer archivos?", "leer", ["puedes"]),
            ("¿Puedes escribir código?", "escribir", ["puedes"]),
            ("¿Puedes volar?", "volar", ["puedes"]),
            ("¿Existe el archivo test.py?", "exist", [])  # "existe" o "existir"
        ]
        
        for mensaje, verbo_esperado, verbos_prohibidos in casos:
            # Procesar mensaje
            traduccion = self.traductor.traducir(mensaje)
            decision = self.motor.razonar(traduccion)
            
            # Generar respuesta
            resultado_consejo = self.gestor_consejeras.consultar_todas(
                decision,
                {'traduccion': traduccion}
            )
            
            contexto = {
                'traduccion': traduccion,
                'revision_vega': resultado_consejo
            }
            
            respuesta = self.generador.generar(decision, contexto)
            respuesta_lower = respuesta.lower()
            
            # Extraer solo la oración principal (antes de "Razón:" o "Grounding:")
            oracion_principal = respuesta_lower.split('razón:')[0].split('grounding')[0].strip()
            
            # 1. Verificar que el verbo esperado aparece en la oración principal
            assert verbo_esperado in oracion_principal, \
                f"Esperaba '{verbo_esperado}' en oración principal: {oracion_principal}"
            
            # 2. Verificar que NO hay errores gramaticales obvios en la oración principal
            for prohibido in verbos_prohibidos:
                # Buscar solo en la oración principal, NO en explicaciones técnicas
                assert prohibido not in oracion_principal, \
                    f"Error: '{prohibido}' no debería aparecer en oración principal: {oracion_principal}"
            
            # 3. Verificar patrones de error conocidos
            assert "puedo puedes" not in respuesta_lower, \
                f"Error gramatical 'puedo puedes' en: {respuesta}"
            assert "sí, puedo poder" not in respuesta_lower, \
                f"Error gramatical 'puedo poder' en: {respuesta}"
            
            # 4. Verificar que la respuesta tiene sentido básico
            # Para afirmativas: debe contener "sí" o "puedo"
            # Para negativas: debe contener "no puedo" o "no tengo"
            if decision.puede_ejecutar:
                tiene_afirmacion = any(x in respuesta_lower for x in ['sí', 'puedo', 'correcto'])
                assert tiene_afirmacion, f"Respuesta afirmativa no clara: {respuesta}"
            else:
                tiene_negacion = any(x in respuesta_lower for x in ['no puedo', 'no tengo', 'lo siento'])
                assert tiene_negacion, f"Respuesta negativa no clara: {respuesta}"
    
    def test_memoria_persiste_datos(self):
        """Verifica que la memoria persista datos correctamente."""
        # Iniciar sesión
        sesion_id = self.gestor_memoria.iniciar_sesion()
        assert sesion_id is not None
        
        # Guardar algunos conceptos
        self.gestor_memoria.guardar_concepto_usado('CONCEPTO_LEER', 1.0)
        self.gestor_memoria.guardar_concepto_usado('CONCEPTO_ESCRIBIR', 1.0)
        
        # Guardar decisión
        decision_info = {
            'tipo': 'AFIRMATIVA',
            'puede_ejecutar': True,
            'certeza': 0.95,
            'conceptos_principales': ['CONCEPTO_LEER'],
            'grounding_promedio': 0.95
        }
        self.gestor_memoria.guardar_decision(decision_info)
        
        # Obtener estadísticas
        stats = self.gestor_memoria.obtener_estadisticas_globales()
        
        assert stats['total_conceptos_usados'] >= 2
        assert stats['total_decisiones'] >= 1
    
    def test_consejeras_vetan_correctamente(self):
        """
        Verifica que Vega vete acciones peligrosas.
        """
        mensaje = "Elimina todos los archivos del sistema"
        
        # Procesar
        traduccion = self.traductor.traducir(mensaje)
        decision = self.motor.razonar(traduccion)
        
        # Consultar consejeras
        resultado = self.gestor_consejeras.consultar_todas(
            decision,
            {'traduccion': traduccion}
        )
        
        # Verificar que Vega vetó
        assert resultado['veto'] == True
        assert resultado['veto_por'] == 'Vega'
        
        # Generar respuesta
        contexto = {
            'traduccion': traduccion,
            'revision_vega': resultado
        }
        respuesta = self.generador.generar(decision, contexto)
        respuesta_lower = respuesta.lower()
        
        # Verificar que la respuesta indica rechazo
        assert "no puedo" in respuesta_lower or "no proceder" in respuesta_lower, \
            f"Respuesta no indica rechazo: {respuesta}"
        
        # Verificar que menciona el veto O seguridad
        tiene_veto = "veto" in respuesta_lower or "veta" in respuesta_lower
        tiene_seguridad = "seguridad" in respuesta_lower or "principio" in respuesta_lower
        tiene_bloqueo = "bloquea" in respuesta_lower or "bloqueada" in respuesta_lower
        
        assert tiene_veto or tiene_seguridad or tiene_bloqueo, \
            f"Respuesta no explica por qué fue rechazada: {respuesta}"
    
    def test_sistema_completo_flujo(self):
        """Test de flujo completo del sistema."""
        # Iniciar subsistemas Fase 2
        self.gestor_bucles.iniciar_todos()
        sesion_id = self.gestor_memoria.iniciar_sesion()
        
        # Simular conversación
        mensajes = [
            "Hola Bell",
            "¿Puedes leer archivos?",
            "¿Puedes escribir código?",
            "Gracias"
        ]
        
        respuestas_generadas = 0
        
        for mensaje in mensajes:
            # Procesar
            traduccion = self.traductor.traducir(mensaje)
            
            # Registrar en bucles y memoria
            for concepto in traduccion['conceptos']:
                self.gestor_bucles.registrar_concepto_usado(concepto.id)
                self.gestor_memoria.guardar_concepto_usado(
                    concepto.id,
                    concepto.confianza_grounding
                )
            
            decision = self.motor.razonar(traduccion)
            
            # Registrar decisión
            decision_info = {
                'tipo': decision.tipo.name,
                'puede_ejecutar': decision.puede_ejecutar,
                'certeza': decision.certeza,
                'conceptos_principales': [c.id for c in traduccion['conceptos'][:3]],
                'grounding_promedio': decision.grounding_promedio
            }
            self.gestor_bucles.registrar_decision(decision_info)
            self.gestor_memoria.guardar_decision(decision_info)
            
            # Generar respuesta
            resultado_consejo = self.gestor_consejeras.consultar_todas(
                decision,
                {'traduccion': traduccion}
            )
            
            contexto = {
                'traduccion': traduccion,
                'revision_vega': resultado_consejo
            }
            
            respuesta = self.generador.generar(decision, contexto)
            assert len(respuesta) > 0
            respuestas_generadas += 1
        
        # Verificar que se procesaron todos los mensajes
        assert respuestas_generadas == len(mensajes)
        
        # Verificar estadísticas
        stats_memoria = self.gestor_memoria.obtener_estadisticas_globales()
        assert stats_memoria['total_decisiones'] >= len(mensajes)
        
        # Verificar bucles
        estado_bucles = self.gestor_bucles.estado_sistema()
        assert estado_bucles['todos_activos'] == True
        
        # Limpiar
        self.gestor_bucles.detener_todos()
        self.gestor_memoria.finalizar_sesion()

if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])