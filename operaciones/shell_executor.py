"""
Ejecutor de comandos shell con seguridad.
FASE 4A — VERSION v3.0 — SOPORTE WINDOWS + LINUX

CAMBIOS v3.0 sobre v2.0:
═══════════════════════════════════════════════════════════════════════

FIX-W1  _normalizar_comando() REESCRITO completamente.
        Antes: solo reemplazaba el primer token (ls→dir).
        Ahora: reemplaza el comando COMPLETO con su equivalente
        PowerShell/CMD correcto, incluyendo flags y argumentos.

FIX-W2  MAPEO_WINDOWS_COMPLETO: dict exhaustivo de 30+ comandos.
        Cada entrada es el comando Windows equivalente con sus
        propios flags. Ejemplo:
            'ls -la'     → 'dir /a'
            'ps aux'     → 'tasklist /v'
            'free -h'    → solo PowerShell puede dar RAM
        Para comandos sin equivalente directo se usa PowerShell.

FIX-W3  _ejecutar_powershell(): nuevo método para comandos que
        requieren PowerShell en Windows (free, df, uptime, etc.)
        Usa: powershell -Command "..."

FIX-W4  es_seguro() adaptado para Windows: el primer token puede
        ser 'powershell' cuando viene de _normalizar_comando().
        Se agrega 'powershell' a lista de tokens de sistema seguros.

FIX-W5  BLACKLIST Windows: se agregan comandos destructivos de
        Windows/PowerShell que no estaban: format c:, del /f /s,
        Remove-Item -Recurse, etc.

FIX-W6  _pipe_es_seguro() mejorado: en Windows los pipes usan
        PowerShell y los tokens pueden ser cmdlets (Get-Process,
        Select-String, etc.) — se agrega lista de cmdlets seguros.

MANTIENE: toda la funcionalidad v2.0 sin cambios en la API pública.
"""

import subprocess
import platform
from typing import Dict, List, Optional, Tuple
from pathlib import Path


class SecurityError(Exception):
    """Error de seguridad en ejecución de comandos."""
    pass


class ShellExecutor:
    """
    Ejecuta comandos del sistema operativo con validación de seguridad.
    Soporta Linux/macOS y Windows (CMD + PowerShell).
    """

    # ──────────────────────────────────────────────────────────────────
    # WHITELIST — comandos base permitidos (Linux/macOS)
    # ──────────────────────────────────────────────────────────────────
    COMANDOS_PERMITIDOS = [
        # Navegación y directorio
        'ls', 'dir', 'pwd', 'cd', 'tree',

        # Archivos — solo lectura
        'cat', 'type', 'head', 'tail', 'less', 'more',
        'file', 'stat', 'wc', 'md5sum', 'sha256sum',
        'diff', 'cmp',

        # Búsqueda y filtrado
        'grep', 'find', 'locate', 'which', 'whereis',
        'awk', 'sed', 'sort', 'uniq', 'cut', 'tr',
        'strings', 'hexdump',

        # Directorios — creación segura
        'mkdir', 'rmdir',

        # Sistema — información
        'echo', 'printf',
        'ps', 'top', 'htop', 'pgrep', 'pstree',
        'df', 'du', 'free', 'vmstat', 'iostat',
        'whoami', 'id', 'groups', 'who', 'w',
        'date', 'cal', 'timedatectl',
        'hostname', 'uname', 'arch',
        'uptime', 'last', 'lastlog',
        'env', 'printenv', 'set',
        'lscpu', 'lsmem', 'lsblk', 'lsusb', 'lspci',
        'dmesg', 'journalctl',
        'sysctl',

        # Red — solo información
        'ping', 'traceroute', 'tracepath',
        'curl', 'wget',
        'ifconfig', 'ip', 'ss', 'netstat',
        'nslookup', 'dig', 'host',
        'whois',

        # Procesos — solo información
        'lsof', 'fuser', 'strace',

        # Python y herramientas de desarrollo
        'python', 'python3', 'pip', 'pip3',
        'pytest', 'pylint', 'flake8', 'mypy',
        'node', 'npm', 'npx',
        'ruby', 'gem',
        'java', 'javac',
        'gcc', 'g++', 'make',

        # Git
        'git',

        # Archivos comprimidos
        'zip', 'unzip', 'tar', 'gzip', 'gunzip', 'zcat',
        'ls -la', 'ls -lh', 'ls -ltr',

        # Utilidades
        'timeout', 'sleep', 'time', 'watch',
        'xargs', 'tee', 'yes', 'true', 'false',
        'basename', 'dirname', 'realpath', 'readlink',
        'ln', 'cp', 'mv',

        # Hardware
        'nproc', 'arch', 'uname -a', 'uname -r',

        # Paquetes
        'apt', 'apt-get install', 'apt-cache',
        'yum', 'dnf', 'pacman -S', 'brew',
        'dpkg', 'rpm',

        # Texto
        'base64', 'xxd', 'od',
        'iconv', 'locale',

        # Shell
        'export', 'source', 'alias',
        'history', 'type', 'hash',

        # Permisos lectura
        'getfacl', 'namei',

        # Windows nativo (para whitelist en es_seguro)
        'powershell',
        'Get-Process', 'Get-Date', 'Get-ChildItem',
        'Get-Location', 'Get-ComputerInfo',
        'tasklist', 'systeminfo', 'ipconfig',
        'where', 'findstr',
    ]

    # ──────────────────────────────────────────────────────────────────
    # FIX-W2: MAPEO COMPLETO Linux → Windows
    # Clave: comando Linux (puede incluir flags)
    # Valor: comando Windows equivalente
    # ──────────────────────────────────────────────────────────────────
    _MAPEO_WINDOWS: dict = {
        # Listado de archivos
        'ls':                  'dir',
        'ls -la':              'dir /a',
        'ls -lh':              'dir /a',
        'ls -ltr':             'dir /a /o-d',
        'ls -la *.py':         'dir /a *.py',
        'ls -la *.log 2>/dev/null || echo \'No hay archivos .log en este directorio\'':
                               'dir /a *.log 2>nul || echo No hay archivos .log en este directorio',

        # Directorio actual
        'pwd':                 'cd',

        # Fecha y hora
        'date':                'powershell -Command "Get-Date"',

        # Usuario
        'whoami':              'whoami',
        'id':                  'whoami /all',

        # Sistema operativo
        'uname -a':            'powershell -Command "[System.Environment]::OSVersion | Select-Object VersionString, Platform, ServicePack | Format-List"',
        'uname':               'powershell -Command "[System.Environment]::OSVersion.VersionString"',
        'uname -m':            'powershell -Command "$env:PROCESSOR_ARCHITECTURE"',

        # Hostname
        'hostname':            'hostname',

        # Uptime
        'uptime':              'powershell -Command "$os = Get-WmiObject Win32_OperatingSystem; $uptime = (Get-Date) - $os.ConvertToDateTime($os.LastBootUpTime); \'Uptime: \' + $uptime.Days + \' dias, \' + $uptime.Hours + \' horas, \' + $uptime.Minutes + \' minutos\'"',

        # Procesos
        'ps':                  'tasklist',
        'ps aux':              'tasklist /v',
        'ps aux | grep python':'powershell -Command "Get-Process python* -ErrorAction SilentlyContinue | Format-Table Id, ProcessName, CPU, WorkingSet -AutoSize"',
        'ps aux | grep bell':  'powershell -Command "Get-Process | Where-Object {$_.ProcessName -like \'*bell*\'} | Format-Table Id, ProcessName, CPU -AutoSize"',

        # Memoria RAM
        'free':                'powershell -Command "$os = Get-WmiObject Win32_OperatingSystem; $total = [math]::Round($os.TotalVisibleMemorySize/1MB, 2); $free = [math]::Round($os.FreePhysicalMemory/1MB, 2); $used = $total - $free; Write-Host (\'Total RAM: \' + $total + \' GB\'); Write-Host (\'Usada:     \' + $used + \' GB\'); Write-Host (\'Libre:     \' + $free + \' GB\')"',
        'free -h':             'powershell -Command "$os = Get-WmiObject Win32_OperatingSystem; $total = [math]::Round($os.TotalVisibleMemorySize/1MB, 2); $free = [math]::Round($os.FreePhysicalMemory/1MB, 2); $used = $total - $free; Write-Host (\'Total RAM: \' + $total + \' GB\'); Write-Host (\'Usada:     \' + $used + \' GB\'); Write-Host (\'Libre:     \' + $free + \' GB\')"',

        # Disco
        'df':                  'powershell -Command "Get-PSDrive -PSProvider FileSystem | Select-Object Name, @{N=\'Used(GB)\';E={[math]::Round($_.Used/1GB,2)}}, @{N=\'Free(GB)\';E={[math]::Round($_.Free/1GB,2)}}, @{N=\'Total(GB)\';E={[math]::Round(($_.Used+$_.Free)/1GB,2)}} | Format-Table -AutoSize"',
        'df -h':               'powershell -Command "Get-PSDrive -PSProvider FileSystem | Select-Object Name, @{N=\'Used(GB)\';E={[math]::Round($_.Used/1GB,2)}}, @{N=\'Free(GB)\';E={[math]::Round($_.Free/1GB,2)}}, @{N=\'Total(GB)\';E={[math]::Round(($_.Used+$_.Free)/1GB,2)}} | Format-Table -AutoSize"',
        'du -sh .':            'powershell -Command "$size = (Get-ChildItem -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum; Write-Host ([math]::Round($size/1MB, 2).ToString() + \' MB (directorio actual)\')"',

        # Variables de entorno
        'env':                 'set',
        'printenv':            'set',

        # Red
        'ifconfig':            'ipconfig /all',
        'ip addr show 2>/dev/null || ifconfig': 'ipconfig /all',
        'ss -tuln':            'netstat -an',
        'netstat':             'netstat -an',
        'ping -c 3 google.com':'ping -n 3 google.com',

        # CPU
        'nproc':               'powershell -Command "[System.Environment]::ProcessorCount"',

        # Git (mismo en Windows)
        'git status':          'git status',
        'git log --oneline -10':'git log --oneline -10',
        'git diff':            'git diff',
        'git branch':          'git branch',

        # Python (puede ser python o py en Windows)
        'python3 --version':   'python --version',
        'pip3 list':           'pip list',

        # Historial
        'history | tail -20':  'powershell -Command "Get-History -Count 20 | Format-Table Id, CommandLine -AutoSize"',

        # Búsqueda
        'grep -r \'error\' . --include=\'*.py\' 2>/dev/null | head -20':
                               'powershell -Command "Select-String -Path \'*.py\' -Pattern \'error\' -Recurse | Select-Object -First 20 | Format-Table Filename, LineNumber, Line -AutoSize"',
        'grep -r \'TODO\\|FIXME\\|HACK\' . --include=\'*.py\' 2>/dev/null | head -20':
                               'powershell -Command "Select-String -Path \'*.py\' -Pattern \'TODO|FIXME|HACK\' -Recurse | Select-Object -First 20 | Format-Table Filename, LineNumber, Line -AutoSize"',

        # Estructura de directorios
        'tree -L 2':           'tree /f /a | more',

        # Información del sistema completa
        'systeminfo':          'systeminfo',
    }

    # ──────────────────────────────────────────────────────────────────
    # BLACKLIST — comandos siempre prohibidos
    # ──────────────────────────────────────────────────────────────────
    COMANDOS_PROHIBIDOS = [
        # Destructivos Linux
        'rm -rf', 'rm -r', 'rm -f',
        'format', 'mkfs', 'dd if=', 'shred', 'wipe',
        ':> ', '> /dev/',

        # Destructivos Windows
        'del /s', 'del /f', 'del /q',
        'format c:', 'format d:', 'format /q',
        'rd /s', 'rmdir /s',
        'Remove-Item -Recurse', 'Remove-Item -Force',
        'ri -recurse', 'ri -force',

        # Sistema — apagado/reinicio
        'shutdown', 'reboot', 'poweroff', 'halt', 'init',
        'systemctl stop', 'systemctl disable', 'service stop',
        'Stop-Computer', 'Restart-Computer',

        # Permisos peligrosos
        'chmod 777', 'chmod -R', 'chown', 'chgrp',
        'sudo', 'su ', 'doas',
        'runas /user:administrator',

        # Red peligrosa
        'nc -l', 'nc -e', 'nmap', 'tcpdump',
        'wireshark', 'ettercap', 'arpspoof',

        # Ejecución remota
        'ssh ', 'scp ', 'rsync ',
        'telnet', 'rsh', 'rlogin', 'rexec',
        'Enter-PSSession', 'Invoke-Command',

        # Modificación de sistema
        'apt-get remove', 'apt-get purge', 'apt-get autoremove',
        'yum remove', 'yum erase',
        'pacman -R', 'pacman -Rs',
        'pip uninstall', 'Uninstall-Package',

        # Loops infinitos / fork bombs
        'while true', 'for (;;)', ':(){ :|:& };:', 'yes |',
        'while ($true)', 'for(;;)',

        # Escritura a archivos críticos
        '> /etc/', '>> /etc/', '> /boot/', '>> /boot/',
        '> /sys/', '>> /sys/', 'tee /etc/',

        # Modificar usuarios
        'useradd', 'userdel', 'usermod',
        'groupadd', 'groupdel', 'groupmod',
        'passwd', 'visudo',
        'New-LocalUser', 'Remove-LocalUser',

        # Registro de Windows
        'reg delete', 'regedit', 'reg add',
        'Set-ItemProperty HKLM', 'Remove-Item HKCU',

        # Cron y tareas
        'crontab -r', 'at ',
        'schtasks /delete', 'schtasks /create',

        # Módulos del kernel
        'insmod', 'rmmod', 'modprobe',

        # Variables peligrosas
        'LD_PRELOAD=', 'LD_LIBRARY_PATH=',

        # Disco
        'fdisk', 'parted', 'gdisk',
        'mkswap', 'swapon', 'mount', 'umount',
        'diskpart', 'DiskPart',
    ]

    # ──────────────────────────────────────────────────────────────────
    # CARACTERES PELIGROSOS
    # ──────────────────────────────────────────────────────────────────
    CARACTERES_PELIGROSOS = [
        ';',    # separador de comandos
        '`',    # command substitution (bash y PowerShell)
        '$(',   # command substitution bash
        '&&',   # AND lógico
    ]

    _PIPES_SEGUROS = [
        'grep', 'head', 'tail', 'sort', 'uniq', 'wc',
        'less', 'more', 'cat', 'awk', 'sed', 'cut',
        # PowerShell cmdlets seguros
        'select-object', 'where-object', 'format-table',
        'format-list', 'select-string', 'get-process',
        'measure-object', 'out-string',
    ]

    # ──────────────────────────────────────────────────────────────────
    # INIT
    # ──────────────────────────────────────────────────────────────────

    def __init__(self, timeout: int = 30, working_dir: Optional[Path] = None):
        self.timeout     = timeout
        self.working_dir = working_dir or Path.cwd()
        self.sistema     = platform.system()
        self._whitelist  = set(self.COMANDOS_PERMITIDOS)

    # ──────────────────────────────────────────────────────────────────
    # MÉTODO PRINCIPAL
    # ──────────────────────────────────────────────────────────────────

    def ejecutar(self, comando: str, capture_output: bool = True) -> Dict:
        """
        Ejecuta un comando con validación de seguridad.
        En Windows normaliza automáticamente a equivalente CMD/PowerShell.
        """
        if not self.es_seguro(comando):
            raise SecurityError(
                f"Comando prohibido o inseguro: {comando}\n"
                f"Razón: {self._razon_inseguridad(comando)}"
            )

        comando_normalizado = self._normalizar_comando(comando)

        try:
            resultado = subprocess.run(
                comando_normalizado,
                shell=True,
                capture_output=capture_output,
                text=True,
                timeout=self.timeout,
                cwd=self.working_dir,
                encoding='utf-8',
                errors='replace',
            )
            return {
                'stdout':  resultado.stdout if capture_output else '',
                'stderr':  resultado.stderr if capture_output else '',
                'codigo':  resultado.returncode,
                'exitoso': resultado.returncode == 0,
                'comando': comando_normalizado,
            }
        except subprocess.TimeoutExpired:
            raise TimeoutError(
                f"Comando excedió timeout de {self.timeout}s: {comando}"
            )
        except Exception as e:
            return {
                'stdout':  '',
                'stderr':  str(e),
                'codigo':  -1,
                'exitoso': False,
                'comando': comando_normalizado,
                'error':   str(e),
            }

    # ──────────────────────────────────────────────────────────────────
    # SEGURIDAD
    # ──────────────────────────────────────────────────────────────────

    def es_seguro(self, comando: str) -> bool:
        """
        Valida si un comando es seguro de ejecutar.
        Orden: blacklist → chars peligrosos → whitelist.
        """
        comando_lower = comando.lower().strip()

        # 1. Blacklist
        for prohibido in self.COMANDOS_PROHIBIDOS:
            if prohibido.lower() in comando_lower:
                return False

        # 2. Caracteres peligrosos
        for char in self.CARACTERES_PELIGROSOS:
            if char in comando:
                return False

        # Pipe condicional
        if '|' in comando:
            if not self._pipe_es_seguro(comando):
                return False

        # Redirección condicional
        if '>' in comando:
            if not self._redireccion_es_segura(comando):
                return False

        # 3. Whitelist
        primer_token = comando_lower.split()[0] if comando_lower else ''

        # FIX-W4: powershell es seguro cuando viene de _normalizar_comando
        if primer_token == 'powershell':
            return True

        # Token en whitelist
        if primer_token in [cmd.split()[0].lower() for cmd in self.COMANDOS_PERMITIDOS]:
            return True

        # Comandos compuestos
        for permitido in self.COMANDOS_PERMITIDOS:
            if comando_lower.startswith(permitido.lower()):
                return True

        return False

    def _pipe_es_seguro(self, comando: str) -> bool:
        partes = [p.strip() for p in comando.split('|')]
        for parte in partes:
            if not parte:
                continue
            primer_token = parte.lower().split()[0]
            en_whitelist = any(
                primer_token == cmd.split()[0].lower()
                for cmd in self.COMANDOS_PERMITIDOS
            ) or primer_token in [p.lower() for p in self._PIPES_SEGUROS]
            tiene_prohibido = any(
                prohibido.lower() in parte.lower()
                for prohibido in self.COMANDOS_PROHIBIDOS
            )
            if not en_whitelist or tiene_prohibido:
                return False
        return True

    def _redireccion_es_segura(self, comando: str) -> bool:
        cmd_lower = comando.lower()
        if cmd_lower.startswith('echo'):
            rutas_criticas = ['/etc/', '/boot/', '/sys/', '/proc/', '/dev/']
            if any(ruta in cmd_lower for ruta in rutas_criticas):
                return False
            return True
        # En Windows, powershell con Write-Host o Out-File limitado también es seguro
        if cmd_lower.startswith('powershell') and '> nul' in cmd_lower:
            return True
        return False

    def _razon_inseguridad(self, comando: str) -> str:
        cmd_lower = comando.lower().strip()
        for prohibido in self.COMANDOS_PROHIBIDOS:
            if prohibido.lower() in cmd_lower:
                return f"Contiene comando prohibido: '{prohibido}'"
        for char in self.CARACTERES_PELIGROSOS:
            if char in comando:
                return f"Contiene carácter peligroso: '{char}'"
        if '|' in comando and not self._pipe_es_seguro(comando):
            return "Pipeline inseguro"
        if '>' in comando and not self._redireccion_es_segura(comando):
            return "Redirección insegura"
        primer_token = cmd_lower.split()[0] if cmd_lower else ''
        return f"Comando '{primer_token}' no está en la lista de comandos permitidos por Vega"

    def _razón_inseguridad(self, comando: str) -> str:
        return self._razon_inseguridad(comando)

    # ──────────────────────────────────────────────────────────────────
    # FIX-W1: NORMALIZACIÓN COMPLETA Linux → Windows
    # ──────────────────────────────────────────────────────────────────

    def _normalizar_comando(self, comando: str) -> str:
        """
        Normaliza el comando según el sistema operativo.

        Linux/macOS: retorna sin cambios.
        Windows:     busca equivalente exacto en _MAPEO_WINDOWS,
                     si no encuentra intenta mapeo por token,
                     si no hay mapeo lo deja como está (git, python, etc.
                     funcionan igual en Windows).
        """
        if self.sistema != 'Windows':
            return comando

        # Búsqueda exacta (respeta flags y argumentos)
        if comando in self._MAPEO_WINDOWS:
            return self._MAPEO_WINDOWS[comando]

        # Búsqueda por prefijo (el comando empieza igual)
        for linux_cmd, win_cmd in self._MAPEO_WINDOWS.items():
            if comando.startswith(linux_cmd + ' ') or comando == linux_cmd:
                return win_cmd

        # Comandos que funcionan igual en Windows (git, python, pip, etc.)
        _UNIVERSALES = {
            'git', 'python', 'python3', 'pip', 'pip3',
            'node', 'npm', 'npx', 'java', 'javac',
            'echo', 'hostname', 'whoami', 'ping',
            'netstat', 'ipconfig', 'dir', 'cd',
            'tasklist', 'systeminfo', 'where',
        }
        primer_token = comando.split()[0].lower()
        if primer_token in _UNIVERSALES:
            # Normalizar python3 → python en Windows
            if primer_token == 'python3':
                return comando.replace('python3', 'python', 1)
            if primer_token == 'pip3':
                return comando.replace('pip3', 'pip', 1)
            return comando

        # Si llegamos aquí, no hay equivalente conocido
        # Intentar ejecutar como PowerShell como último recurso
        return f'powershell -Command "{comando}"'

    # ──────────────────────────────────────────────────────────────────
    # UTILIDADES
    # ──────────────────────────────────────────────────────────────────

    def listar_comandos_disponibles(self) -> List[str]:
        return sorted(self.COMANDOS_PERMITIDOS)

    def obtener_info_sistema(self) -> Dict:
        return {
            'sistema':        self.sistema,
            'plataforma':     platform.platform(),
            'arquitectura':   platform.machine(),
            'version':        platform.version(),
            'python':         platform.python_version(),
            'working_dir':    str(self.working_dir),
            'total_comandos': len(self.COMANDOS_PERMITIDOS),
            'modo_windows':   self.sistema == 'Windows',
        }

    def ejecutar_seguro(self, comando: str) -> Tuple[bool, str, str]:
        """Versión simplificada: retorna (exitoso, stdout, error). No lanza excepciones."""
        try:
            resultado = self.ejecutar(comando)
            return resultado['exitoso'], resultado.get('stdout', ''), resultado.get('stderr', '')
        except SecurityError as e:
            return False, '', str(e)
        except TimeoutError as e:
            return False, '', str(e)
        except Exception as e:
            return False, '', str(e)


# ──────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    executor = ShellExecutor()
    sistema = executor.sistema
    print(f"ShellExecutor v3.0 — {sistema} — {len(executor.COMANDOS_PERMITIDOS)} comandos\n")

    if sistema == 'Windows':
        pruebas = [
            ('ls -la',         True,  "listar archivos (→ dir /a)"),
            ('pwd',            True,  "directorio actual (→ cd)"),
            ('date',           True,  "fecha (→ PowerShell Get-Date)"),
            ('free -h',        True,  "memoria RAM (→ PowerShell WMI)"),
            ('df -h',          True,  "disco (→ PowerShell Get-PSDrive)"),
            ('ps aux',         True,  "procesos (→ tasklist /v)"),
            ('uname -a',       True,  "sistema (→ PowerShell OSVersion)"),
            ('rm -rf /',       False, "destructivo bloqueado"),
            ('shutdown now',   False, "apagado bloqueado"),
        ]
    else:
        pruebas = [
            ('ls -la',         True,  "listar archivos"),
            ('pwd',            True,  "directorio actual"),
            ('date',           True,  "fecha del sistema"),
            ('free -h',        True,  "memoria RAM"),
            ('df -h',          True,  "espacio en disco"),
            ('ps aux',         True,  "procesos"),
            ('rm -rf /',       False, "destructivo bloqueado"),
            ('shutdown now',   False, "apagado bloqueado"),
        ]

    for cmd, debe_ser_seguro, desc in pruebas:
        es_seg = executor.es_seguro(cmd)
        ok = es_seg == debe_ser_seguro
        icono = "✅" if ok else "❌"
        normalizado = executor._normalizar_comando(cmd) if es_seg else "BLOQUEADO"
        print(f"{icono} {desc}")
        print(f"   Original:    {cmd}")
        if es_seg and normalizado != cmd:
            print(f"   Normalizado: {normalizado}")
        print()