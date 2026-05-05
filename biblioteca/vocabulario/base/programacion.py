# biblioteca/vocabulario/base/programacion.py
# ================================================
# PROGRAMACIÓN — Vocabulario técnico de Sebastian
# Extraído del dataset real de conversaciones.
# Bell habla de código constantemente con su creador.
# ================================================

PROGRAMACION = {

    # ── CONCEPTOS CORE ───────────────────────────
    'código':      {'id': 'PROG_CODIGO',    'tipo': 'concepto_prog',   'grounding_base': 0.95, 'variantes': ['codigo', 'códigos', 'code', 'script']},
    'función':     {'id': 'PROG_FUNCION',   'tipo': 'concepto_prog',   'grounding_base': 0.93, 'variantes': ['funcion', 'funciones', 'function', 'método', 'metodo']},
    'variable':    {'id': 'PROG_VARIABLE',  'tipo': 'concepto_prog',   'grounding_base': 0.92, 'variantes': ['variables', 'var', 'let', 'const']},
    'error':       {'id': 'PROG_ERROR',     'tipo': 'problema_prog',   'grounding_base': 0.95, 'variantes': ['errores', 'bug', 'bugs', 'fallo', 'excepción', 'exception']},
    'bucle':       {'id': 'PROG_BUCLE',     'tipo': 'estructura_prog', 'grounding_base': 0.90, 'variantes': ['loop', 'loops', 'for', 'while', 'ciclo', 'iteración']},
    'clase':       {'id': 'PROG_CLASE',     'tipo': 'estructura_prog', 'grounding_base': 0.90, 'variantes': ['clases', 'class', 'objeto', 'objetos', 'instancia']},
    'módulo':      {'id': 'PROG_MODULO',    'tipo': 'estructura_prog', 'grounding_base': 0.90, 'variantes': ['modulo', 'módulos', 'modulos', 'librería', 'libreria', 'library']},
    'importar':    {'id': 'PROG_IMPORTAR',  'tipo': 'accion_prog',     'grounding_base': 0.90, 'variantes': ['import', 'importación', 'importacion', 'error de importación']},
    'ejecutar':    {'id': 'PROG_EJECUTAR',  'tipo': 'accion_prog',     'grounding_base': 0.92, 'variantes': ['ejecuta', 'ejecutando', 'ejecuté', 'run', 'correr el código']},
    'debug':       {'id': 'PROG_DEBUG',     'tipo': 'accion_prog',     'grounding_base': 0.92, 'variantes': ['debuggear', 'depurar', 'debugueando', 'debugueo', 'depuración']},
    'instalar':    {'id': 'PROG_INSTALAR',  'tipo': 'accion_prog',     'grounding_base': 0.90, 'variantes': ['instalación', 'instalo', 'instalé', 'install', 'pip install']},

    # ── PYTHON ───────────────────────────────────
    'python':      {'id': 'PROG_PYTHON',    'tipo': 'lenguaje_prog',   'grounding_base': 0.95, 'variantes': ['py', 'python3', 'python 3']},
    'pip':         {'id': 'PROG_PIP',       'tipo': 'herramienta_prog','grounding_base': 0.90, 'variantes': ['pip install', 'pip3']},
    'entorno virtual':{'id': 'PROG_VENV',   'tipo': 'herramienta_prog','grounding_base': 0.90, 'variantes': ['venv', 'virtualenv', 'entorno de python']},
    'requirements':{'id': 'PROG_REQS',      'tipo': 'archivo_prog',    'grounding_base': 0.88, 'variantes': ['requirements.txt', 'dependencias', 'paquetes']},
    'lista':       {'id': 'PROG_LISTA',     'tipo': 'estructura_datos','grounding_base': 0.88, 'variantes': ['listas', 'array', 'arreglo']},
    'diccionario': {'id': 'PROG_DICT',      'tipo': 'estructura_datos','grounding_base': 0.88, 'variantes': ['diccionarios', 'dict', 'objeto json']},
    'async':       {'id': 'PROG_ASYNC',     'tipo': 'concepto_prog',   'grounding_base': 0.88, 'variantes': ['async await', 'asíncrono', 'asincrono', 'await']},

    # ── WEB / BACKEND ────────────────────────────
    'flask':       {'id': 'PROG_FLASK',     'tipo': 'framework_prog',  'grounding_base': 0.93, 'variantes': ['Flask', 'flask app', 'servidor flask']},
    'api':         {'id': 'PROG_API',       'tipo': 'concepto_web',    'grounding_base': 0.93, 'variantes': ['APIs', 'endpoint', 'endpoints', 'ruta', 'rutas']},
    'websocket':   {'id': 'PROG_WEBSOCKET', 'tipo': 'concepto_web',    'grounding_base': 0.90, 'variantes': ['websockets', 'socket.io', 'socket io', 'socketio']},
    'http':        {'id': 'PROG_HTTP',      'tipo': 'protocolo_web',   'grounding_base': 0.90, 'variantes': ['https', 'get', 'post', 'request', 'response', 'petición']},
    'servidor':    {'id': 'PROG_SERVIDOR',  'tipo': 'infraestructura', 'grounding_base': 0.92, 'variantes': ['server', 'servidores', 'backend', 'back-end']},
    'webhook':     {'id': 'PROG_WEBHOOK',   'tipo': 'concepto_web',    'grounding_base': 0.88, 'variantes': ['webhooks']},
    'rest':        {'id': 'PROG_REST',      'tipo': 'arquitectura_web','grounding_base': 0.88, 'variantes': ['RESTful', 'rest api', 'api rest']},
    'json':        {'id': 'PROG_JSON',      'tipo': 'formato_datos',   'grounding_base': 0.92, 'variantes': ['JSON', 'json file', 'archivo json']},
    'html':        {'id': 'PROG_HTML',      'tipo': 'lenguaje_markup', 'grounding_base': 0.90, 'variantes': ['HTML', 'html5']},
    'css':         {'id': 'PROG_CSS',       'tipo': 'lenguaje_estilos','grounding_base': 0.90, 'variantes': ['CSS', 'estilos', 'stylesheet']},
    'javascript':  {'id': 'PROG_JS',        'tipo': 'lenguaje_prog',   'grounding_base': 0.90, 'variantes': ['js', 'JS', 'JavaScript']},
    'frontend':    {'id': 'PROG_FRONTEND',  'tipo': 'capa_web',        'grounding_base': 0.90, 'variantes': ['front-end', 'front', 'interfaz', 'UI', 'cliente']},
    'base de datos':{'id': 'PROG_BD',       'tipo': 'almacenamiento',  'grounding_base': 0.92, 'variantes': ['base datos', 'db', 'database', 'BD']},
    'sqlite':      {'id': 'PROG_SQLITE',    'tipo': 'bd_prog',         'grounding_base': 0.88, 'variantes': ['SQLite', 'sql', 'SQL', 'consulta SQL']},

    # ── GIT Y CONTROL DE VERSIONES ───────────────
    'git':         {'id': 'PROG_GIT',       'tipo': 'herramienta_prog','grounding_base': 0.92, 'variantes': ['Git', 'control de versiones']},
    'github':      {'id': 'PROG_GITHUB',    'tipo': 'plataforma_prog', 'grounding_base': 0.92, 'variantes': ['GitHub', 'repositorio', 'repo', 'gh']},
    'commit':      {'id': 'PROG_COMMIT',    'tipo': 'accion_git',      'grounding_base': 0.90, 'variantes': ['commits', 'hacer commit', 'git commit', 'git push']},
    'push':        {'id': 'PROG_PUSH',      'tipo': 'accion_git',      'grounding_base': 0.87, 'variantes': ['git push', 'subir cambios']},
    'branch':      {'id': 'PROG_BRANCH',    'tipo': 'concepto_git',    'grounding_base': 0.85, 'variantes': ['branches', 'rama', 'ramas']},

    # ── ARCHIVOS Y CONFIGURACIÓN ─────────────────
    'archivo':     {'id': 'PROG_ARCHIVO',   'tipo': 'objeto_prog',     'grounding_base': 0.92, 'variantes': ['archivos', 'file', 'files', 'fichero']},
    'carpeta':     {'id': 'PROG_CARPETA',   'tipo': 'objeto_prog',     'grounding_base': 0.88, 'variantes': ['carpetas', 'directorio', 'folder', 'path']},
    '.env':        {'id': 'PROG_ENV',       'tipo': 'archivo_config',  'grounding_base': 0.90, 'variantes': ['env file', 'variables de entorno', 'environment', 'dotenv']},
    'railway':     {'id': 'PROG_RAILWAY',   'tipo': 'plataforma_prog', 'grounding_base': 0.87, 'variantes': ['Railway', 'desplegar', 'deploy', 'deployment']},

    # ── PROBLEMAS COMUNES ────────────────────────
    'no funciona': {'id': 'PROG_NO_FUNC',   'tipo': 'problema_prog',   'grounding_base': 0.93, 'variantes': ['falló', 'falla', 'no corre', 'no sirve', 'tronó', 'se rompió']},
    'no entiendo el error': {'id': 'PROG_CONFUSED', 'tipo': 'problema_prog','grounding_base': 0.92, 'variantes': ['qué significa este error', 'error raro', 'por qué falla']},
    'cómo hago':   {'id': 'PROG_HOW_TO',    'tipo': 'solicitud_prog',  'grounding_base': 0.92, 'variantes': ['como hago', 'cómo se hace', 'cómo funciona', 'como funciona']},
}
