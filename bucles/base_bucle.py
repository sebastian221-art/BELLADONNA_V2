"""
Bucle Base - Clase abstracta para bucles autónomos.

Los bucles autónomos permiten que Bell "piense" en segundo plano,
revisando sus propias operaciones, patrones y aprendizajes.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime
import time
import threading

class BaseBucle(ABC):
    """
    Clase base abstracta para bucles autónomos.
    
    Cada bucle tiene:
    - Intervalo de ejecución (cuántos segundos entre ejecuciones)
    - Lógica específica de procesamiento
    - Estadísticas de ejecución
    - Control de inicio/parada
    """
    
    def __init__(self, nombre: str, intervalo_segundos: int):
        """
        Inicializa bucle.
        
        Args:
            nombre: Nombre descriptivo del bucle
            intervalo_segundos: Segundos entre ejecuciones
        """
        self.nombre = nombre
        self.intervalo_segundos = intervalo_segundos
        
        # Estado del bucle
        self._activo = False
        self._thread: Optional[threading.Thread] = None
        self._detener = False
        
        # Estadísticas
        self.estadisticas = {
            'ejecuciones': 0,
            'ultima_ejecucion': None,
            'tiempo_total_ms': 0,
            'errores': 0,
            'ultima_duracion_ms': 0
        }
        
        # Historial de resultados (últimas N ejecuciones)
        self.historial: List[Dict[str, Any]] = []
        self.max_historial = 10
    
    def iniciar(self) -> bool:
        """
        Inicia el bucle en un thread separado.
        
        Returns:
            True si se inició correctamente
        """
        if self._activo:
            return False
        
        self._activo = True
        self._detener = False
        self._thread = threading.Thread(target=self._ejecutar_loop, daemon=True)
        self._thread.start()
        
        return True
    
    def detener(self) -> bool:
        """
        Detiene el bucle.
        
        Returns:
            True si se detuvo correctamente
        """
        if not self._activo:
            return False
        
        self._detener = True
        self._activo = False
        
        # Esperar a que termine el thread (timeout corto porque sleep es interrumpible)
        if self._thread:
            self._thread.join(timeout=3)  # Máximo 3 segundos
        
        return True
    
    def _ejecutar_loop(self):
        """Loop principal del bucle (corre en thread separado)."""
        while not self._detener:
            try:
                # Ejecutar procesamiento
                inicio = time.time()
                resultado = self.procesar()
                duracion_ms = int((time.time() - inicio) * 1000)
                
                # Actualizar estadísticas
                self.estadisticas['ejecuciones'] += 1
                self.estadisticas['ultima_ejecucion'] = datetime.now().isoformat()
                self.estadisticas['tiempo_total_ms'] += duracion_ms
                self.estadisticas['ultima_duracion_ms'] = duracion_ms
                
                # Guardar en historial
                self._agregar_a_historial({
                    'timestamp': datetime.now().isoformat(),
                    'duracion_ms': duracion_ms,
                    'resultado': resultado,
                    'exito': True
                })
                
            except Exception as e:
                # Manejar errores sin detener el bucle
                self.estadisticas['errores'] += 1
                self._agregar_a_historial({
                    'timestamp': datetime.now().isoformat(),
                    'error': str(e),
                    'exito': False
                })
            
            # Esperar hasta la próxima ejecución (sleep interrumpible)
            # Dividir en sleeps de 1 segundo para poder detener rápido
            tiempo_restante = self.intervalo_segundos
            while tiempo_restante > 0 and not self._detener:
                time.sleep(min(1, tiempo_restante))
                tiempo_restante -= 1
    
    def _agregar_a_historial(self, entrada: Dict[str, Any]):
        """Agrega entrada al historial, manteniendo max_historial elementos."""
        self.historial.append(entrada)
        if len(self.historial) > self.max_historial:
            self.historial.pop(0)
    
    @abstractmethod
    def procesar(self) -> Dict[str, Any]:
        """
        Lógica específica del bucle (DEBE implementarse en subclases).
        
        Returns:
            Dict con resultados del procesamiento
        """
        pass
    
    def esta_activo(self) -> bool:
        """Retorna si el bucle está activo."""
        return self._activo
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """
        Retorna estadísticas del bucle.
        
        Returns:
            Dict con estadísticas completas
        """
        stats = self.estadisticas.copy()
        
        # Calcular promedios
        if stats['ejecuciones'] > 0:
            stats['tiempo_promedio_ms'] = stats['tiempo_total_ms'] / stats['ejecuciones']
        else:
            stats['tiempo_promedio_ms'] = 0
        
        # Agregar información del bucle
        stats['nombre'] = self.nombre
        stats['intervalo_segundos'] = self.intervalo_segundos
        stats['activo'] = self._activo
        
        return stats
    
    def obtener_historial(self, n: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Retorna historial de ejecuciones.
        
        Args:
            n: Número de últimas ejecuciones a retornar (None = todas)
        
        Returns:
            Lista de resultados de ejecuciones
        """
        if n is None:
            return self.historial.copy()
        return self.historial[-n:] if n > 0 else []
    
    def __repr__(self):
        estado = "ACTIVO" if self._activo else "DETENIDO"
        return f"<{self.__class__.__name__}(nombre={self.nombre}, intervalo={self.intervalo_segundos}s, estado={estado})>"