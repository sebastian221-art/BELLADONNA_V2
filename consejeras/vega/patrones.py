"""
Patrones de Detección de Vega.

Separa la lógica de detección del flujo principal.
Permite agregar nuevos patrones sin modificar guardiana.py
"""
from typing import Dict, List

class PatronesPeligrosos:
    """
    Biblioteca de patrones que Vega reconoce como peligrosos.
    
    Cada patrón está organizado por tipo de riesgo.
    """
    
    def __init__(self):
        """Inicializa patrones."""
        # PATRONES DESTRUCTIVOS
        self.palabras_destructivas = [
            'eliminar', 'elimina', 'borrar', 'borra', 
            'delete', 'remove', 'destruir'
        ]
        
        self.palabras_alcance_total = [
            'todo', 'todos', 'todas', 'all', 
            'completo', 'entera', 'entero'
        ]
        
        # PATRONES DE AUTO-MODIFICACIÓN
        self.palabras_modificacion = [
            'modificar', 'modifica', 'cambiar', 'cambia',
            'editar', 'edita', 'alterar', 'altera'
        ]
        
        self.palabras_auto_referencia = [
            'tu código', 'mi código', 'código', 'bell', 
            'core', 'tu mismo', 'ti mismo', 'belladonna',
            'tus archivos', 'tu sistema'
        ]
        
        # PATRONES DE PRIVACIDAD
        self.palabras_sensibles = [
            'contraseña', 'contraseñas', 'password', 'passwords',
            'credencial', 'credenciales', 'clave', 'claves',
            'token', 'tokens', 'api key', 'secret'
        ]
        
        self.palabras_acceso = [
            'leer', 'lee', 'lees', 'escribir', 'escribe', 
            'guardar', 'guarda', 'read', 'write', 'mostrar'
        ]
    
    def es_accion_destructiva(self, texto: str) -> bool:
        """
        Detecta acciones destructivas masivas.
        
        Patrón: [palabra_destructiva] + [alcance_total]
        Ejemplos: "eliminar todos", "borrar todo", "delete all"
        """
        texto_lower = texto.lower()
        
        tiene_destruccion = any(
            palabra in texto_lower 
            for palabra in self.palabras_destructivas
        )
        
        if tiene_destruccion:
            tiene_alcance_total = any(
                palabra in texto_lower 
                for palabra in self.palabras_alcance_total
            )
            
            if tiene_alcance_total:
                return True
        
        return False
    
    def es_auto_modificacion(self, texto: str) -> bool:
        """
        Detecta intentos de auto-modificación.
        
        Patrón: [palabra_modificacion] + [auto_referencia]
        Ejemplos: "modifica tu código", "cambia bell"
        """
        texto_lower = texto.lower()
        
        tiene_modificacion = any(
            palabra in texto_lower 
            for palabra in self.palabras_modificacion
        )
        
        if tiene_modificacion:
            tiene_auto_referencia = any(
                patron in texto_lower 
                for patron in self.palabras_auto_referencia
            )
            
            if tiene_auto_referencia:
                return True
        
        return False
    
    def viola_privacidad(self, texto: str) -> bool:
        """
        Detecta violaciones de privacidad.
        
        Patrón: [palabra_sensible] + [palabra_acceso]
        Ejemplos: "lee mi contraseña", "mostrar passwords"
        """
        texto_lower = texto.lower()
        
        tiene_sensible = any(
            palabra in texto_lower 
            for palabra in self.palabras_sensibles
        )
        
        if tiene_sensible:
            tiene_acceso = any(
                palabra in texto_lower 
                for palabra in self.palabras_acceso
            )
            
            if tiene_acceso:
                return True
        
        return False
    
    def detectar_todos_los_riesgos(self, texto: str) -> List[str]:
        """
        Detecta todos los riesgos en un texto.
        
        Returns:
            Lista de nombres de riesgos detectados
        """
        riesgos = []
        
        if self.es_accion_destructiva(texto):
            riesgos.append('ACCION_DESTRUCTIVA')
        
        if self.es_auto_modificacion(texto):
            riesgos.append('AUTO_MODIFICACION')
        
        if self.viola_privacidad(texto):
            riesgos.append('VIOLACION_PRIVACIDAD')
        
        return riesgos