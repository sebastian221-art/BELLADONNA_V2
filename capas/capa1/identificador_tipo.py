# capas/capa1/identificador_tipo.py
# ================================================
# IDENTIFICADOR DE TIPO — v2
#
# Detecta con precisión el tipo de estímulo:
# texto, voz, imagen, archivo, sensor, sistema
#
# NUEVO v2:
# — Detección de código Python en texto
# — Detección de lenguaje de programación
# — Detección de colombianismos y tono
# — Detección de comandos internos de Bell
# — Detección de preguntas vs afirmaciones
# ================================================

from pathlib import Path
import re


class IdentificadorTipo:

    EXTENSIONES_IMAGEN   = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg'}
    EXTENSIONES_CODIGO   = {'.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rs',
                            '.rb', '.php', '.swift', '.kt', '.scala'}
    EXTENSIONES_ARCHIVO  = {'.txt', '.md', '.json', '.csv', '.html', '.pdf',
                            '.docx', '.xlsx', '.yaml', '.yml', '.xml', '.log'}

    # Patrones que indican código Python en el texto
    _PATRONES_CODIGO_PYTHON = [
        r'\bdef\s+\w+\s*\(',
        r'\bclass\s+\w+[\s:(]',
        r'\bimport\s+\w+',
        r'\bfrom\s+\w+\s+import\b',
        r'\bfor\s+\w+\s+in\s+',
        r'\bwhile\s+.+:',
        r'\bif\s+.+:',
        r'\btry:\s*\n',
        r'\bexcept\s+',
        r'\bprint\s*\(',
        r'\breturn\s+',
        r'=\s*\[\s*\]',
        r'=\s*\{\s*\}',
        r'\.append\(',
        r'\.get\(',
        r'__init__',
        r'self\.\w+',
        r'#\s+.*\n.*def\s',
    ]

    # Patrones que indican código de otros lenguajes
    _PATRONES_CODIGO_JS   = [r'\bfunction\s+\w+', r'\bconst\s+\w+\s*=', r'\blet\s+\w+\s*=',
                              r'\bconsole\.log\(', r'=>\s*{', r'\bawait\s+']
    _PATRONES_CODIGO_SQL  = [r'\bSELECT\b.*\bFROM\b', r'\bINSERT\s+INTO\b',
                              r'\bCREATE\s+TABLE\b', r'\bUPDATE\b.*\bSET\b']
    _PATRONES_CODIGO_BASH = [r'^\s*\$\s+', r'\bchmod\b', r'\bsudo\b', r'\bgrep\b.*\|',
                              r'\becho\s+"', r'\.sh\b']

    # Palabras que activan modo interno de Bell (comandos del sistema)
    _COMANDOS_SISTEMA = {
        'estado_bell', 'diagnostico', 'reiniciar_memoria',
        'exportar_sesion', 'limpiar_zona', 'ver_consejeras'
    }

    def identificar(self, estimulo) -> str:
        if estimulo is None:
            return 'texto'
        if isinstance(estimulo, dict):
            return self._identificar_dict(estimulo)
        if isinstance(estimulo, str):
            return self._identificar_string(estimulo)
        if isinstance(estimulo, bytes):
            return 'imagen'
        return 'texto'

    def identificar_detallado(self, estimulo) -> dict:
        """
        Retorna análisis completo del tipo de input.
        Usado por __init__.py para enriquecer el paquete.
        """
        tipo_base = self.identificar(estimulo)
        texto = estimulo if isinstance(estimulo, str) else (
            estimulo.get('texto') or estimulo.get('mensaje', '') if isinstance(estimulo, dict) else ''
        )

        return {
            'tipo':              tipo_base,
            'contiene_codigo':   self._detectar_codigo(texto),
            'lenguaje_codigo':   self._detectar_lenguaje_codigo(texto),
            'es_pregunta':       self._es_pregunta(texto),
            'es_comando_bell':   self._es_comando_interno(texto),
            'longitud':          len(texto),
            'complejidad':       self._calcular_complejidad(texto),
        }

    # ── Identificación por tipo ────────────────────────────

    def _identificar_dict(self, estimulo: dict) -> str:
        tipo_explicito = estimulo.get('tipo')
        if tipo_explicito in ('texto', 'voz', 'imagen', 'archivo', 'sensor', 'sistema'):
            return tipo_explicito

        if 'audio' in estimulo or 'transcripcion' in estimulo:
            return 'voz'
        if 'imagen_base64' in estimulo or 'imagen_ruta' in estimulo:
            return 'imagen'
        if 'señal' in estimulo or 'sensor_id' in estimulo:
            return 'sensor'
        if 'evento_interno' in estimulo or 'origen_bell' in estimulo:
            return 'sistema'
        if 'mensaje' in estimulo or 'texto' in estimulo:
            return 'texto'
        return 'texto'

    def _identificar_string(self, estimulo: str) -> str:
        # Verificar si es ruta de archivo existente
        ruta = Path(estimulo.strip())
        # Fix macOS OSError 63: límite 255 bytes por nombre de archivo
        _es_ruta = False
        if len(estimulo) < 255:
            try:
                _es_ruta = ruta.exists() and ruta.is_file()
            except (OSError, ValueError, TypeError):
                _es_ruta = False
        if _es_ruta:
            ext = ruta.suffix.lower()
            if ext in self.EXTENSIONES_IMAGEN:
                return 'imagen'
            if ext in self.EXTENSIONES_CODIGO or ext in self.EXTENSIONES_ARCHIVO:
                return 'archivo'

        # Verificar comandos internos de Bell
        if self._es_comando_interno(estimulo):
            return 'sistema'

        return 'texto'

    # ── Detección de código ────────────────────────────────

    def _detectar_codigo(self, texto: str) -> bool:
        """Detecta si el texto contiene fragmentos de código."""
        if not texto:
            return False

        # Bloques de código explícitos (markdown)
        if '```' in texto:
            return True

        # Indentación consistente (señal de código)
        lineas = texto.split('\n')
        lineas_con_indent = sum(1 for l in lineas if l.startswith('    ') or l.startswith('\t'))
        if lineas_con_indent >= 2 and len(lineas) >= 3:
            return True

        # Patrones de código Python
        for patron in self._PATRONES_CODIGO_PYTHON:
            if re.search(patron, texto, re.MULTILINE):
                return True

        # Patrones de otros lenguajes
        for patron in self._PATRONES_CODIGO_JS + self._PATRONES_CODIGO_SQL + self._PATRONES_CODIGO_BASH:
            if re.search(patron, texto, re.MULTILINE | re.IGNORECASE):
                return True

        return False

    def _detectar_lenguaje_codigo(self, texto: str) -> str:
        """Detecta el lenguaje del código si hay código presente."""
        if not texto:
            return 'ninguno'

        if not self._detectar_codigo(texto):
            return 'ninguno'

        # Bloques markdown con lenguaje explícito
        match = re.search(r'```(\w+)', texto)
        if match:
            lang = match.group(1).lower()
            mapa = {'py': 'python', 'js': 'javascript', 'ts': 'typescript',
                    'bash': 'bash', 'sh': 'bash', 'sql': 'sql'}
            return mapa.get(lang, lang)

        # Detectar por patrones
        for patron in self._PATRONES_CODIGO_PYTHON:
            if re.search(patron, texto, re.MULTILINE):
                return 'python'

        for patron in self._PATRONES_CODIGO_JS:
            if re.search(patron, texto):
                return 'javascript'

        for patron in self._PATRONES_CODIGO_SQL:
            if re.search(patron, texto, re.IGNORECASE):
                return 'sql'

        for patron in self._PATRONES_CODIGO_BASH:
            if re.search(patron, texto, re.MULTILINE):
                return 'bash'

        return 'desconocido'

    # ── Análisis lingüístico ───────────────────────────────

    def _es_pregunta(self, texto: str) -> bool:
        """Detecta si el mensaje es una pregunta."""
        if not texto:
            return False
        t = texto.strip()
        if t.endswith('?') or t.startswith('¿'):
            return True
        palabras_pregunta = {'qué', 'que', 'cómo', 'como', 'cuándo', 'cuando',
                             'dónde', 'donde', 'quién', 'quien', 'cuál', 'cual',
                             'por qué', 'para qué', 'cuánto', 'cuanto'}
        t_lower = t.lower()
        return any(t_lower.startswith(p) for p in palabras_pregunta)

    def _es_comando_interno(self, texto: str) -> bool:
        """Detecta comandos internos de Bell."""
        if not texto:
            return False
        t_lower = texto.lower().strip()
        return any(cmd in t_lower for cmd in self._COMANDOS_SISTEMA)

    def _calcular_complejidad(self, texto: str) -> str:
        """
        Clasifica la complejidad del mensaje.
        Ayuda a C6 a decidir qué motor usar.
        """
        if not texto:
            return 'vacia'

        n = len(texto)
        palabras = len(texto.split())

        if n < 30 or palabras < 5:
            return 'simple'
        elif n < 200 or palabras < 40:
            return 'media'
        else:
            return 'compleja'