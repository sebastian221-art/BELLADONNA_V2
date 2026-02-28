"""
Motor de Aprendizaje - Coordina el sistema de aprendizaje.

Motor principal que integra:
- Ajustador de grounding
- Aplicador de insights
- Memoria persistente
- Bucles autónomos
"""
from typing import Dict, Any, List, Optional
from datetime import datetime

from aprendizaje.ajustador_grounding import AjustadorGrounding
from aprendizaje.aplicador_insights import AplicadorInsights
from aprendizaje.estrategias import EstrategiaAprendizaje


class MotorAprendizaje:
    """
    Motor principal de aprendizaje.
    
    Coordina todos los componentes del sistema de aprendizaje
    para crear un feedback loop continuo.
    
    Flujo:
    1. Bucles detectan patrones e insights
    2. Motor procesa insights y genera acciones
    3. Ajustador propone cambios de grounding
    4. Motor aplica cambios a conceptos
    5. Memoria guarda todo para futuro
    """
    
    def __init__(self, estrategia: Optional[EstrategiaAprendizaje] = None):
        """
        Inicializa motor de aprendizaje.
        
        Args:
            estrategia: Estrategia de aprendizaje (None = por defecto)
        """
        self.ajustador = AjustadorGrounding(estrategia)
        self.aplicador = AplicadorInsights()
        
        # Referencias a otros sistemas (inyectadas)
        self.gestor_vocabulario = None
        self.gestor_memoria = None
        self.gestor_bucles = None
        
        # Estado
        self.activo = False
        self.ciclos_ejecutados = 0
    
    def configurar_integraciones(
        self,
        vocabulario=None,
        memoria=None,
        bucles=None
    ):
        """
        Configura integraciones con otros sistemas.
        
        Args:
            vocabulario: GestorVocabulario
            memoria: GestorMemoria
            bucles: GestorBucles
        """
        self.gestor_vocabulario = vocabulario
        self.gestor_memoria = memoria
        self.gestor_bucles = bucles
    
    def ejecutar_ciclo_aprendizaje(self) -> Dict[str, Any]:
        """
        Ejecuta un ciclo completo de aprendizaje.
        
        Returns:
            Dict con resultados del ciclo
        """
        self.ciclos_ejecutados += 1
        
        resultado = {
            'ciclo': self.ciclos_ejecutados,
            'timestamp': datetime.now().isoformat(),
            'insights_procesados': 0,
            'acciones_generadas': 0,
            'ajustes_propuestos': 0,
            'ajustes_aplicados': 0,
            'errores': []
        }
        
        try:
            # Paso 1: Obtener insights de bucles
            insights = self._obtener_insights()
            resultado['insights_procesados'] = len(insights)
            
            if not insights:
                resultado['mensaje'] = 'Sin insights para procesar'
                return resultado
            
            # Paso 2: Procesar insights y generar acciones
            acciones = self.aplicador.procesar_multiples_insights(insights)
            resultado['acciones_generadas'] = len(acciones)
            
            # Paso 3: Aplicar acciones de ajuste de grounding
            ajustes_aplicados = self._aplicar_acciones_grounding(acciones)
            resultado['ajustes_aplicados'] = ajustes_aplicados
            
            # Paso 4: Guardar en memoria
            self._guardar_en_memoria(insights, acciones)
            
            resultado['mensaje'] = f'Ciclo completado: {ajustes_aplicados} ajustes aplicados'
        
        except Exception as e:
            resultado['errores'].append(str(e))
            resultado['mensaje'] = f'Error en ciclo: {str(e)}'
        
        return resultado
    
    def _obtener_insights(self) -> List[Dict[str, Any]]:
        """Obtiene insights de bucles o memoria."""
        insights = []
        
        # Intentar obtener de bucles
        if self.gestor_bucles:
            try:
                insights = self.gestor_bucles.obtener_insights()
            except:
                pass
        
        # Si no hay bucles, intentar de memoria
        if not insights and self.gestor_memoria:
            try:
                insights = self.gestor_memoria.obtener_insights_recientes(n=5, relevancia='ALTA')
            except:
                pass
        
        return insights
    
    def _aplicar_acciones_grounding(self, acciones: List[Dict[str, Any]]) -> int:
        """
        Aplica acciones de ajuste de grounding.
        
        Args:
            acciones: Lista de acciones
        
        Returns:
            Número de ajustes aplicados
        """
        if not self.gestor_vocabulario:
            return 0
        
        ajustes_aplicados = 0
        
        # Filtrar acciones de ajuste de grounding
        acciones_grounding = [
            a for a in acciones
            if a.get('tipo') == 'AJUSTAR_GROUNDING'
        ]
        
        for accion in acciones_grounding:
            try:
                # Obtener concepto
                concepto_id = accion.get('concepto_id')
                concepto = self.gestor_vocabulario.buscar_por_id(concepto_id)
                
                if not concepto:
                    continue
                
                # Crear contexto para ajuste
                contexto = {
                    'ajuste_sugerido': accion.get('ajuste_sugerido', 0.0),
                    'razon': accion.get('razon', ''),
                    'prioridad': accion.get('prioridad', 'MEDIA')
                }
                
                # Proponer ajuste
                propuesta = self.ajustador.proponer_ajuste(
                    concepto_id,
                    concepto.confianza_grounding,
                    contexto
                )
                
                if not propuesta:
                    continue
                
                # Aplicar ajuste
                if self.ajustador.aplicar_ajuste(concepto, propuesta):
                    ajustes_aplicados += 1
                    
                    # Guardar en memoria si está disponible
                    if self.gestor_memoria:
                        self.gestor_memoria.guardar_ajuste_grounding(
                            concepto_id,
                            propuesta['grounding_actual'],
                            propuesta['grounding_propuesto'],
                            propuesta['razon'],
                            True
                        )
            
            except Exception as e:
                # Continuar con siguiente acción en caso de error
                continue
        
        return ajustes_aplicados
    
    def _guardar_en_memoria(
        self,
        insights: List[Dict[str, Any]],
        acciones: List[Dict[str, Any]]
    ):
        """Guarda insights y acciones en memoria."""
        if not self.gestor_memoria:
            return
        
        try:
            # Guardar insights si no están ya
            for insight in insights:
                if 'timestamp' not in insight:
                    self.gestor_memoria.guardar_insight(insight)
        except:
            pass
    
    def procesar_uso_concepto(
        self,
        concepto_id: str,
        exitoso: bool,
        certeza: float = 0.0
    ):
        """
        Procesa el uso de un concepto para aprendizaje.
        
        Args:
            concepto_id: ID del concepto usado
            exitoso: Si el uso fue exitoso
            certeza: Certeza del uso
        """
        if not self.gestor_vocabulario:
            return
        
        try:
            # Obtener concepto
            concepto = self.gestor_vocabulario.buscar_por_id(concepto_id)
            if not concepto:
                return
            
            # Crear contexto
            contexto = {
                'usos_exitosos': 1 if exitoso else 0,
                'usos_fallidos': 0 if exitoso else 1,
                'razon': 'Ajuste por uso'
            }
            
            # Proponer ajuste
            propuesta = self.ajustador.proponer_ajuste(
                concepto_id,
                concepto.confianza_grounding,
                contexto
            )
            
            if propuesta:
                # Aplicar ajuste
                if self.ajustador.aplicar_ajuste(concepto, propuesta):
                    # Guardar en memoria
                    if self.gestor_memoria:
                        self.gestor_memoria.guardar_ajuste_grounding(
                            concepto_id,
                            propuesta['grounding_actual'],
                            propuesta['grounding_propuesto'],
                            propuesta['razon'],
                            True
                        )
        
        except Exception:
            pass
    
    def procesar_turno(self, datos_turno: Dict[str, Any]):
        """
        Procesa un turno de conversación para aprendizaje.
        
        Este método es llamado por main.py después de cada interacción
        con el usuario. Registra los conceptos usados y aprende de la experiencia.
        
        Args:
            datos_turno: Dict con:
                - 'conceptos': List[str] - IDs de conceptos usados en este turno
                - 'decision': Dict - Información de la decisión tomada
                - 'exitoso': bool (opcional) - Si la operación fue exitosa
                - 'certeza': float (opcional) - Certeza de la decisión
        
        Ejemplo:
            motor.procesar_turno({
                'conceptos': ['CONCEPTO_LEER', 'CONCEPTO_ARCHIVO'],
                'decision': {
                    'tipo': 'AFIRMATIVA',
                    'certeza': 0.95,
                    'puede_ejecutar': True
                },
                'exitoso': True,
                'certeza': 0.95
            })
        """
        if not datos_turno:
            return
        
        # Extraer datos del turno
        conceptos = datos_turno.get('conceptos', [])
        decision = datos_turno.get('decision', {})
        exitoso = datos_turno.get('exitoso', True)  # Asumir éxito por defecto
        
        # Obtener certeza (primero de datos_turno, sino de decision)
        certeza = datos_turno.get('certeza', 0.0)
        if certeza == 0.0 and decision:
            certeza = decision.get('certeza', 0.0)
        
        # Registrar uso de cada concepto
        for concepto_id in conceptos:
            try:
                self.procesar_uso_concepto(
                    concepto_id=concepto_id,
                    exitoso=exitoso,
                    certeza=certeza
                )
            except Exception as e:
                # Continuar con siguiente concepto si uno falla
                continue
        
        # Si hay gestor de memoria, guardar la decisión
        if self.gestor_memoria and decision:
            try:
                # Guardar decision en memoria para análisis futuro
                self.gestor_memoria.guardar_decision(decision)
            except Exception:
                # No fallar si no se puede guardar
                pass
    
    # ========== MÉTODOS FALTANTES - ARREGLADOS ==========
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas del motor.
        
        Returns:
            Dict con estadísticas completas
        """
        return {
            'ciclos_ejecutados': self.ciclos_ejecutados,
            'activo': self.activo,
            'ajustador': self.ajustador.obtener_estadisticas(),
            'aplicador': self.aplicador.obtener_estadisticas(),
            'integraciones': {
                'vocabulario': self.gestor_vocabulario is not None,
                'memoria': self.gestor_memoria is not None,
                'bucles': self.gestor_bucles is not None
            }
        }
    
    def obtener_historial_ajustes(
        self,
        concepto_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Obtiene historial de ajustes.
        
        Args:
            concepto_id: Filtrar por concepto (None = todos)
        
        Returns:
            Lista de ajustes
        """
        return self.ajustador.obtener_historial(concepto_id, solo_aplicados=True)
    
    def obtener_acciones_pendientes(self) -> List[Dict[str, Any]]:
        """
        Obtiene acciones pendientes de aplicar.
        
        Returns:
            Lista de acciones pendientes
        """
        return self.aplicador.obtener_acciones_pendientes(prioridad_minima='MEDIA')
    
    def reiniciar_estadisticas(self):
        """Reinicia contadores de estadísticas."""
        self.ciclos_ejecutados = 0
        self.ajustador.historial_ajustes.clear()
        self.aplicador.insights_procesados.clear()
        self.aplicador.acciones_generadas.clear()