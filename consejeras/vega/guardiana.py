"""
Vega - Guardiana de Principios Fundamentales.

VERSIÓN MODULAR - Coordinadora que delega a módulos especializados.
"""
from typing import Dict
from consejeras.base_consejera import Consejera
from razonamiento.tipos_decision import Decision
from core.principios import Principio
from .patrones import PatronesPeligrosos

class Vega(Consejera):
    """
    Vega - La Guardiana.
    
    Primera línea de defensa de Bell.
    Protege TODOS los principios fundamentales.
    
    Su decisión de VETO es FINAL - si Vega veta, Bell no ejecuta.
    
    ARQUITECTURA MODULAR:
    - Coordina revisión
    - Delega detección a patrones.py
    - Mantiene responsabilidad de VETO
    """
    
    def __init__(self):
        """Inicializa Vega."""
        super().__init__("Vega", "Guardiana de Principios")
        
        # Cargar módulos especializados
        self.patrones = PatronesPeligrosos()
        
        # Vega vigila TODOS los principios
        self.principios_vigilados = list(Principio)
        
        # Solo Vega tiene poder de VETO
        self.puede_vetar = True
    
    def revisar(self, decision: Decision, contexto: Dict) -> Dict:
        """
        Revisa decisión y aplica VETO si viola principios.
        
        Vega es estricta pero justa.
        Mira el TEXTO directamente (no depende de que Bell entienda).
        """
        self.revisiones_realizadas += 1
        
        # Extraer texto original
        traduccion = contexto.get('traduccion', {})
        texto_original = traduccion.get('texto_original', '').lower()
        
        # VERIFICAR todos los riesgos
        riesgos = self.patrones.detectar_todos_los_riesgos(texto_original)
        
        if riesgos:
            # HAY RIESGO - Aplicar VETO
            return self._generar_veto(riesgos[0], texto_original)
        
        # SIN RIESGO - Aprobar
        return self._generar_aprobacion()
    
    def _generar_veto(self, tipo_riesgo: str, texto: str) -> Dict:
        """Genera respuesta de VETO."""
        self.vetos_aplicados += 1
        
        # Mapear riesgo a principio
        mapeo_principios = {
            'ACCION_DESTRUCTIVA': Principio.SEGURIDAD_DATOS,
            'AUTO_MODIFICACION': Principio.NO_AUTO_MODIFICACION,
            'VIOLACION_PRIVACIDAD': Principio.PRIVACIDAD
        }
        
        mapeo_razones = {
            'ACCION_DESTRUCTIVA': 'Acción destructiva masiva detectada. Requiere confirmación explícita.',
            'AUTO_MODIFICACION': 'Bell no puede modificar su propio código o arquitectura',
            'VIOLACION_PRIVACIDAD': 'Detectada manipulación de información sensible'
        }
        
        mapeo_recomendaciones = {
            'ACCION_DESTRUCTIVA': 'Pedir confirmación al usuario antes de proceder',
            'AUTO_MODIFICACION': 'Esta acción viola un principio fundamental',
            'VIOLACION_PRIVACIDAD': 'No procesar información de credenciales directamente'
        }
        
        principio = mapeo_principios.get(tipo_riesgo, Principio.SEGURIDAD_DATOS)
        razon = mapeo_razones.get(tipo_riesgo, 'Acción potencialmente peligrosa')
        recomendacion = mapeo_recomendaciones.get(tipo_riesgo, 'Revisar la solicitud')
        
        return {
            'consejera': self.nombre,
            'aprobada': False,
            'veto': True,
            'opinion': f"VETO aplicado: {razon}",
            'confianza': 1.0,
            'razonamiento': [
                f"1. Texto analizado: '{texto[:50]}...'",
                f"2. Riesgo detectado: {tipo_riesgo}",
                f"3. Principio violado: {principio.name}",
                "4. Decisión: VETO"
            ],
            'sugerencias': [recomendacion],
            'principio_violado': principio,
            'razon_veto': razon,
            'recomendacion': recomendacion
        }
    
    def _generar_aprobacion(self) -> Dict:
        """Genera respuesta de aprobación."""
        return {
            'consejera': self.nombre,
            'aprobada': True,
            'veto': False,
            'opinion': 'Acción segura. No se detectaron violaciones.',
            'confianza': 0.95,
            'razonamiento': [
                "1. Texto analizado",
                "2. No se detectaron patrones peligrosos",
                "3. Decisión: APROBADA"
            ],
            'sugerencias': [],
            'principio_violado': None,
            'razon_veto': None,
            'recomendacion': None
        }