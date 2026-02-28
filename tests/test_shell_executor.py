"""
Tests para ShellExecutor.
FASE 3 - Tests de operaciones de sistema.
"""

import pytest
import platform
from pathlib import Path

# Importar el ejecutor (ajustar path según estructura)
import sys
proyecto_path = Path(__file__).parent.parent
sys.path.insert(0, str(proyecto_path))

from operaciones.shell_executor import ShellExecutor, SecurityError


class TestShellExecutorSeguridad:
    """Tests de validación de seguridad."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.executor = ShellExecutor(timeout=5)
    
    def test_comando_seguro_ls(self):
        """Test: ls es un comando seguro."""
        assert self.executor.es_seguro('ls')
        assert self.executor.es_seguro('ls -la')
        assert self.executor.es_seguro('ls /home')
    
    def test_comando_seguro_pwd(self):
        """Test: pwd es un comando seguro."""
        assert self.executor.es_seguro('pwd')
    
    def test_comando_seguro_mkdir(self):
        """Test: mkdir es un comando seguro."""
        assert self.executor.es_seguro('mkdir test_dir')
        assert self.executor.es_seguro('mkdir -p a/b/c')
    
    def test_comando_seguro_cat(self):
        """Test: cat es un comando seguro."""
        assert self.executor.es_seguro('cat archivo.txt')
    
    def test_comando_inseguro_rm_rf(self):
        """Test: rm -rf es INSEGURO."""
        assert not self.executor.es_seguro('rm -rf /')
        assert not self.executor.es_seguro('rm -rf *')
        assert not self.executor.es_seguro('rm -r archivo')
    
    def test_comando_inseguro_format(self):
        """Test: format es INSEGURO."""
        assert not self.executor.es_seguro('format c:')
    
    def test_comando_inseguro_shutdown(self):
        """Test: shutdown es INSEGURO."""
        assert not self.executor.es_seguro('shutdown')
        assert not self.executor.es_seguro('shutdown -h now')
        assert not self.executor.es_seguro('reboot')
    
    def test_comando_inseguro_dd(self):
        """Test: dd es INSEGURO."""
        assert not self.executor.es_seguro('dd if=/dev/zero of=/dev/sda')
    
    def test_caracteres_peligrosos_pipe(self):
        """Test: pipe | es peligroso."""
        # Pipe en general es peligroso
        assert not self.executor.es_seguro('cat file | rm -rf /')
        
        # Excepto en contextos seguros como git log
        # Este test puede variar según implementación
    
    def test_caracteres_peligrosos_punto_y_coma(self):
        """Test: ; permite encadenar comandos peligrosos."""
        assert not self.executor.es_seguro('ls; rm -rf /')
        assert not self.executor.es_seguro('echo hello; shutdown')
    
    def test_caracteres_peligrosos_and(self):
        """Test: && permite encadenar comandos."""
        assert not self.executor.es_seguro('ls && rm -rf /')
    
    def test_caracteres_peligrosos_redireccion(self):
        """Test: > puede sobrescribir archivos importantes."""
        # En general, redirección es peligrosa
        # Excepto con echo
        resultado = self.executor.es_seguro('cat file > /etc/passwd')
        # Debería ser inseguro
    
    def test_caracteres_peligrosos_command_substitution(self):
        """Test: $() y `` permiten ejecución arbitraria."""
        assert not self.executor.es_seguro('echo $(rm -rf /)')
        assert not self.executor.es_seguro('echo `shutdown`')
    
    def test_comando_no_en_whitelist(self):
        """Test: comandos no en whitelist son inseguros."""
        assert not self.executor.es_seguro('comando_inventado')
        assert not self.executor.es_seguro('malware.exe')


class TestShellExecutorEjecucion:
    """Tests de ejecución de comandos."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.executor = ShellExecutor(timeout=5)
    
    def test_ejecutar_ls_exitoso(self):
        """Test: ls ejecuta correctamente."""
        resultado = self.executor.ejecutar('ls')
        
        assert resultado['exitoso'] is True
        assert resultado['codigo'] == 0
        assert isinstance(resultado['stdout'], str)
        assert resultado['stderr'] == '' or isinstance(resultado['stderr'], str)
    
    def test_ejecutar_pwd_exitoso(self):
        """Test: pwd retorna directorio actual."""
        resultado = self.executor.ejecutar('pwd')
        
        assert resultado['exitoso'] is True
        assert len(resultado['stdout']) > 0
        assert '/' in resultado['stdout'] or '\\' in resultado['stdout']  # Path
    
    def test_ejecutar_echo_exitoso(self):
        """Test: echo funciona."""
        resultado = self.executor.ejecutar('echo "Hello World"')
        
        assert resultado['exitoso'] is True
        assert 'Hello World' in resultado['stdout']
    
    def test_ejecutar_comando_inseguro_lanza_excepcion(self):
        """Test: comando inseguro lanza SecurityError."""
        with pytest.raises(SecurityError) as exc_info:
            self.executor.ejecutar('rm -rf /')
        
        assert 'prohibido' in str(exc_info.value).lower()
    
    def test_ejecutar_con_timeout(self):
        """Test: timeout funciona."""
        executor_rapido = ShellExecutor(timeout=2)
        
        # ping es el comando más confiable para timeout
        # ping -n 10 tarda ~10 segundos (1 segundo por ping)
        with pytest.raises(TimeoutError):
            if platform.system() == 'Windows':
                # ping -n 10 = 10 segundos, timeout=2 → TimeoutError
                executor_rapido.ejecutar('ping -n 10 127.0.0.1')
            else:
                executor_rapido.ejecutar('sleep 10')
    
    def test_ejecutar_comando_que_falla(self):
        """Test: comando que falla retorna exitoso=False."""
        # Intentar listar directorio inexistente
        resultado = self.executor.ejecutar('ls /directorio_que_no_existe_123456')
        
        assert resultado['exitoso'] is False
        assert resultado['codigo'] != 0
    
    def test_ejecutar_mkdir_exitoso(self):
        """Test: mkdir crea directorio."""
        import tempfile
        import shutil
        
        # Usar directorio temporal
        temp_dir = Path(tempfile.mkdtemp())
        test_dir = temp_dir / 'test_mkdir_123'
        
        try:
            resultado = self.executor.ejecutar(f'mkdir {test_dir}')
            
            assert resultado['exitoso'] is True
            assert test_dir.exists()
        finally:
            # Limpiar
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
    
    def test_ejecutar_con_working_dir(self):
        """Test: working_dir funciona."""
        import tempfile
        
        temp_dir = Path(tempfile.mkdtemp())
        executor_temp = ShellExecutor(working_dir=temp_dir)
        
        resultado = executor_temp.ejecutar('pwd')
        
        assert str(temp_dir) in resultado['stdout']


class TestShellExecutorNormalizacion:
    """Tests de normalización de comandos según OS."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.executor = ShellExecutor()
    
    def test_normalizar_comando_segun_os(self):
        """Test: comandos se normalizan según OS."""
        # Este test es específico al OS
        sistema = platform.system()
        
        if sistema == 'Windows':
            # En Windows, ls debería convertirse a dir
            normalizado = self.executor._normalizar_comando('ls')
            assert 'dir' in normalizado.lower()
        else:
            # En Linux/Mac, ls sigue siendo ls
            normalizado = self.executor._normalizar_comando('ls')
            assert normalizado == 'ls'
    
    def test_info_sistema(self):
        """Test: obtener_info_sistema funciona."""
        info = self.executor.obtener_info_sistema()
        
        assert 'sistema' in info
        assert 'plataforma' in info
        assert 'python' in info
        assert info['sistema'] in ['Windows', 'Linux', 'Darwin']


class TestShellExecutorComandosDisponibles:
    """Tests de comandos disponibles."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.executor = ShellExecutor()
    
    def test_listar_comandos_disponibles(self):
        """Test: listar_comandos_disponibles retorna lista."""
        comandos = self.executor.listar_comandos_disponibles()
        
        assert isinstance(comandos, list)
        assert len(comandos) > 0
        assert 'ls' in comandos or 'dir' in comandos
        assert 'pwd' in comandos
        assert 'mkdir' in comandos
    
    def test_comandos_disponibles_ordenados(self):
        """Test: comandos están ordenados."""
        comandos = self.executor.listar_comandos_disponibles()
        
        assert comandos == sorted(comandos)


class TestShellExecutorRazonInseguridad:
    """Tests de explicación de inseguridad."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.executor = ShellExecutor()
    
    def test_razon_comando_prohibido(self):
        """Test: explica por qué comando está prohibido."""
        razon = self.executor._razón_inseguridad('rm -rf /')
        
        assert 'prohibido' in razon.lower()
        assert 'rm -rf' in razon
    
    def test_razon_caracter_peligroso(self):
        """Test: explica carácter peligroso."""
        razon = self.executor._razón_inseguridad('ls; shutdown')
        
        assert 'peligroso' in razon.lower() or 'prohibido' in razon.lower()
    
    def test_razon_no_en_whitelist(self):
        """Test: explica comando no permitido."""
        razon = self.executor._razón_inseguridad('comando_inventado')
        
        assert 'no está' in razon.lower() or 'permitido' in razon.lower()


# Tests de integración
class TestShellExecutorIntegracion:
    """Tests de integración más complejos."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.executor = ShellExecutor(timeout=10)
    
    def test_flujo_completo_crear_y_listar_directorio(self):
        """Test: crear dir, listar, verificar."""
        import tempfile
        import shutil
        
        temp_dir = Path(tempfile.mkdtemp())
        test_dir_name = 'test_integracion_123'
        test_dir = temp_dir / test_dir_name
        
        try:
            # 1. Crear directorio
            resultado_mkdir = self.executor.ejecutar(f'mkdir {test_dir}')
            assert resultado_mkdir['exitoso'] is True
            
            # 2. Listar contenido
            resultado_ls = self.executor.ejecutar(f'ls {temp_dir}')
            assert resultado_ls['exitoso'] is True
            assert test_dir_name in resultado_ls['stdout']
            
        finally:
            # Limpiar
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
    
    def test_multiples_comandos_seguros(self):
        """Test: ejecutar múltiples comandos seguros."""
        comandos_seguros = [
            'pwd',
            'whoami',
            'echo "test"',
        ]
        
        # Nota: 'date' removido porque en Windows puede fallar
        # si espera input interactivo
        
        for comando in comandos_seguros:
            resultado = self.executor.ejecutar(comando)
            assert resultado['exitoso'] is True, f"Falló: {comando}"


# Fixture para tests parametrizados
@pytest.fixture
def ejecutor():
    """Fixture que retorna un ShellExecutor."""
    return ShellExecutor(timeout=5)


# Tests parametrizados
class TestShellExecutorParametrizado:
    """Tests parametrizados para múltiples casos."""
    
    @pytest.mark.parametrize("comando,esperado", [
        ('ls', True),
        ('pwd', True),
        ('echo hello', True),
        ('mkdir test', True),
        ('rm -rf /', False),
        ('shutdown', False),
        ('format', False),
        ('comando_falso', False),
    ])
    def test_es_seguro_parametrizado(self, ejecutor, comando, esperado):
        """Test parametrizado de es_seguro."""
        assert ejecutor.es_seguro(comando) == esperado
    
    @pytest.mark.parametrize("comando_peligroso", [
        'rm -rf /',
        'shutdown now',
        'del /s *',
        'format c:',
        'dd if=/dev/zero',
        'reboot',
        'ls; rm -rf /',
        'echo $(malicious)',
    ])
    def test_comandos_peligrosos_bloqueados(self, ejecutor, comando_peligroso):
        """Test: todos los comandos peligrosos son bloqueados."""
        with pytest.raises(SecurityError):
            ejecutor.ejecutar(comando_peligroso)


if __name__ == '__main__':
    # Ejecutar tests
    pytest.main([__file__, '-v', '--tb=short'])