"""
Ejecutor de comandos shell con seguridad.
FASE 3 - Semana 1-2
"""

import subprocess
import platform
from typing import Dict, List, Optional
from pathlib import Path


class SecurityError(Exception):
    """Error de seguridad en ejecución de comandos."""
    pass


class ShellExecutor:
    """
    Ejecuta comandos del sistema operativo con validación de seguridad.
    
    Características:
    - Whitelist de comandos permitidos
    - Blacklist de comandos peligrosos
    - Timeout automático (30s)
    - Captura de stdout/stderr
    - Validación de sintaxis
    """
    
    # Comandos permitidos (whitelist)
    COMANDOS_PERMITIDOS = [
        # Navegación y listado
        'ls', 'dir', 'pwd', 'cd', 'tree',
        
        # Directorios
        'mkdir', 'rmdir',
        
        # Archivos (lectura)
        'cat', 'type', 'head', 'tail', 'less', 'more',
        
        # Información del sistema
        'echo', 'ps', 'top', 'df', 'du', 'whoami',
        'date', 'hostname', 'uname', 'uptime',
        
        # Red (solo info, no modificación)
        'ping', 'curl', 'wget',
        
        # Python
        'python', 'python3', 'pip', 'pytest',
        
        # Git
        'git status', 'git log', 'git diff', 'git branch',
        
        # Utilidades de tiempo (para tests)
        'timeout', 'sleep',
    ]
    
    # Comandos/patrones PROHIBIDOS (blacklist)
    COMANDOS_PROHIBIDOS = [
        # Destructivos
        'rm -rf', 'rm -r', 'del /s', 'format', 'mkfs', 'dd if=',
        
        # Sistema
        'shutdown', 'reboot', 'poweroff', 'halt', 'init',
        
        # Permisos
        'chmod 777', 'chown', 'chgrp',
        
        # Red peligrosa
        'nc -l', 'nmap', 'tcpdump',
        
        # Ejecución remota
        'ssh', 'telnet', 'rsh',
        
        # Modificación de sistema
        'apt-get remove', 'yum remove', 'pacman -R',
        
        # Loops infinitos
        'while true', 'for (;;)',
        
        # Fork bombs
        ':(){ :|:& };:',
    ]
    
    # Caracteres peligrosos en comandos
    CARACTERES_PELIGROSOS = [
        ';',   # Separador de comandos
        '|',   # Pipe (puede encadenar comandos)
        '&',   # Background/AND
        '>',   # Redirección (puede sobrescribir archivos)
        '<',   # Redirección entrada
        '`',   # Command substitution
        '$(',  # Command substitution
        ')',   # Cierre de substitution
    ]
    
    def __init__(self, timeout: int = 30, working_dir: Optional[Path] = None):
        """
        Inicializa el ejecutor.
        
        Args:
            timeout: Timeout en segundos (default: 30)
            working_dir: Directorio de trabajo (default: directorio actual)
        """
        self.timeout = timeout
        self.working_dir = working_dir or Path.cwd()
        self.sistema = platform.system()  # Windows, Linux, Darwin (Mac)
        
    def ejecutar(self, comando: str, capture_output: bool = True) -> Dict:
        """
        Ejecuta un comando del sistema con validación de seguridad.
        
        Args:
            comando: Comando a ejecutar
            capture_output: Si capturar stdout/stderr
            
        Returns:
            Dict con:
                - stdout: Salida estándar
                - stderr: Salida de error
                - codigo: Código de retorno
                - exitoso: True si código == 0
                - comando: Comando ejecutado
                
        Raises:
            SecurityError: Si el comando es inseguro
            subprocess.TimeoutExpired: Si excede timeout
        """
        # Validar seguridad
        if not self.es_seguro(comando):
            raise SecurityError(
                f"Comando prohibido o inseguro: {comando}\n"
                f"Razón: {self._razón_inseguridad(comando)}"
            )
        
        # Normalizar comando según sistema operativo
        comando_normalizado = self._normalizar_comando(comando)
        
        try:
            # Ejecutar comando
            resultado = subprocess.run(
                comando_normalizado,
                shell=True,
                capture_output=capture_output,
                text=True,
                timeout=self.timeout,
                cwd=self.working_dir
            )
            
            return {
                'stdout': resultado.stdout if capture_output else '',
                'stderr': resultado.stderr if capture_output else '',
                'codigo': resultado.returncode,
                'exitoso': resultado.returncode == 0,
                'comando': comando_normalizado
            }
            
        except subprocess.TimeoutExpired:
            raise TimeoutError(
                f"Comando excedió timeout de {self.timeout}s: {comando}"
            )
        except Exception as e:
            return {
                'stdout': '',
                'stderr': str(e),
                'codigo': -1,
                'exitoso': False,
                'comando': comando_normalizado,
                'error': str(e)
            }
    
    def es_seguro(self, comando: str) -> bool:
        """
        Verifica si un comando es seguro de ejecutar.
        
        Args:
            comando: Comando a validar
            
        Returns:
            True si es seguro, False si no
        """
        comando_lower = comando.lower().strip()
        
        # 1. Verificar blacklist (comandos prohibidos)
        for prohibido in self.COMANDOS_PROHIBIDOS:
            if prohibido in comando_lower:
                return False
        
        # 2. Verificar caracteres peligrosos
        for char in self.CARACTERES_PELIGROSOS:
            if char in comando:
                # Excepciones: algunos caracteres son OK en contextos específicos
                if char == '>' and 'echo' in comando_lower:
                    continue  # echo "text" > file.txt es OK
                if char == '|' and 'git log' in comando_lower:
                    continue  # git log | head es OK
                return False
        
        # 3. Verificar whitelist (al menos el primer comando debe estar)
        primer_comando = comando_lower.split()[0] if comando_lower else ''
        
        # Comandos exactos
        if primer_comando in [cmd.split()[0] for cmd in self.COMANDOS_PERMITIDOS]:
            return True
        
        # Comandos compuestos (ej: "git status")
        for permitido in self.COMANDOS_PERMITIDOS:
            if comando_lower.startswith(permitido.lower()):
                return True
        
        # Si no está en whitelist, rechazar
        return False
    
    def _razón_inseguridad(self, comando: str) -> str:
        """
        Determina por qué un comando es inseguro.
        
        Args:
            comando: Comando a analizar
            
        Returns:
            Razón de inseguridad
        """
        comando_lower = comando.lower().strip()
        
        # Verificar blacklist
        for prohibido in self.COMANDOS_PROHIBIDOS:
            if prohibido in comando_lower:
                return f"Contiene comando prohibido: '{prohibido}'"
        
        # Verificar caracteres peligrosos
        for char in self.CARACTERES_PELIGROSOS:
            if char in comando:
                return f"Contiene carácter peligroso: '{char}'"
        
        # No está en whitelist
        primer_comando = comando_lower.split()[0] if comando_lower else ''
        return f"Comando '{primer_comando}' no está en lista de comandos permitidos"
    
    def _normalizar_comando(self, comando: str) -> str:
        """
        Normaliza comando según sistema operativo.
        
        En Windows: ls → dir, cat → type, etc.
        En Linux/Mac: mantiene comandos Unix
        
        Args:
            comando: Comando original
            
        Returns:
            Comando normalizado
        """
        if self.sistema == 'Windows':
            # Mapeo de comandos Unix → Windows
            mapeo = {
                'ls': 'dir',
                'cat': 'type',
                'pwd': 'cd',
                'rm': 'del',
                'cp': 'copy',
                'mv': 'move',
                'clear': 'cls',
                'which': 'where',
                'date': 'echo %date% %time%',  # date en Windows espera input, usar alternativa
            }
            
            primer_comando = comando.split()[0]
            if primer_comando in mapeo:
                # Para 'date', reemplazar completamente
                if primer_comando == 'date':
                    return mapeo[primer_comando]
                return comando.replace(primer_comando, mapeo[primer_comando], 1)
        
        return comando
    
    def listar_comandos_disponibles(self) -> List[str]:
        """
        Retorna lista de comandos disponibles.
        
        Returns:
            Lista de comandos permitidos
        """
        return sorted(self.COMANDOS_PERMITIDOS)
    
    def obtener_info_sistema(self) -> Dict:
        """
        Obtiene información del sistema operativo.
        
        Returns:
            Dict con info del sistema
        """
        return {
            'sistema': self.sistema,
            'plataforma': platform.platform(),
            'arquitectura': platform.machine(),
            'version': platform.version(),
            'python': platform.python_version(),
            'working_dir': str(self.working_dir)
        }


# Ejemplo de uso
if __name__ == '__main__':
    executor = ShellExecutor()
    
    # Comando seguro
    try:
        resultado = executor.ejecutar('ls')
        print("✅ Comando seguro ejecutado:")
        print(resultado['stdout'])
    except SecurityError as e:
        print(f"❌ Error de seguridad: {e}")
    
    # Comando inseguro
    try:
        resultado = executor.ejecutar('rm -rf /')
        print("❌ ESTO NO DEBERÍA EJECUTARSE")
    except SecurityError as e:
        print(f"✅ Comando bloqueado correctamente: {e}")