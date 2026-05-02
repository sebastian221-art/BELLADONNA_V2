# biblioteca/vocabulario/base/tecnologia.py
# ================================================
# VOCABULARIO TECNOLOGÍA Y PROGRAMACIÓN
# Bell entiende el mundo técnico de Sebastian
# ================================================

CONCEPTOS_TECNOLOGIA = {

    # ── Programación general ──────────────────────
    'codigo': {
        'id': 'TEC_CODIGO', 'tipo': 'concepto_tecnico',
        'variantes': ['código','codigo','el código','este código','mi código',
                      'el código ese','revisar código','escribir código'],
        'grounding_base': 0.85,
    },
    'bug': {
        'id': 'TEC_BUG', 'tipo': 'problema_tecnico',
        'variantes': ['bug','error','el error','hay un error','tengo un error',
                      'falla','está fallando','no funciona','rompe','se rompe',
                      'excepción','excepcion','traceback','crash'],
        'grounding_base': 0.88,
    },
    'funcion': {
        'id': 'TEC_FUNCION', 'tipo': 'elemento_codigo',
        'variantes': ['función','funcion','def','método','metodo','la función',
                      'esta función','una función'],
        'grounding_base': 0.83,
    },
    'clase': {
        'id': 'TEC_CLASE', 'tipo': 'elemento_codigo',
        'variantes': ['clase','class','la clase','esta clase','una clase','objeto',
                      'instancia','instanciar'],
        'grounding_base': 0.83,
    },
    'variable': {
        'id': 'TEC_VARIABLE', 'tipo': 'elemento_codigo',
        'variantes': ['variable','variables','la variable','valor','asignar'],
        'grounding_base': 0.80,
    },
    'archivo': {
        'id': 'TEC_ARCHIVO', 'tipo': 'elemento_sistema',
        'variantes': ['archivo','archivos','el archivo','este archivo','los archivos',
                      'fichero','file','los files'],
        'grounding_base': 0.82,
    },
    'import': {
        'id': 'TEC_IMPORT', 'tipo': 'elemento_codigo',
        'variantes': ['import','importar','importando','no importa','falla el import'],
        'grounding_base': 0.82,
    },

    # ── Python específico ─────────────────────────
    'python': {
        'id': 'TEC_PYTHON', 'tipo': 'lenguaje',
        'variantes': ['python','py','script python','archivo py'],
        'grounding_base': 0.87,
    },
    'flask': {
        'id': 'TEC_FLASK', 'tipo': 'framework',
        'variantes': ['flask','flask app','servidor flask','el servidor'],
        'grounding_base': 0.85,
    },
    'pip': {
        'id': 'TEC_PIP', 'tipo': 'herramienta',
        'variantes': ['pip','pip install','instalar con pip'],
        'grounding_base': 0.82,
    },
    'venv': {
        'id': 'TEC_VENV', 'tipo': 'herramienta',
        'variantes': ['venv','entorno virtual','virtualenv','el entorno'],
        'grounding_base': 0.82,
    },

    # ── Git y control de versiones ────────────────
    'git': {
        'id': 'TEC_GIT', 'tipo': 'herramienta',
        'variantes': ['git','github','commit','push','pull','merge','branch',
                      'repositorio','repo','el repo'],
        'grounding_base': 0.85,
    },

    # ── Servidores y deployment ───────────────────
    'servidor': {
        'id': 'TEC_SERVIDOR', 'tipo': 'infraestructura',
        'variantes': ['servidor','server','el servidor','el server','backend',
                      'api','endpoint','ruta','route'],
        'grounding_base': 0.83,
    },
    'deploy': {
        'id': 'TEC_DEPLOY', 'tipo': 'accion_tecnica',
        'variantes': ['deploy','desplegar','deployment','subir','subir a producción',
                      'en producción','produccion'],
        'grounding_base': 0.83,
    },

    # ── Base de datos ─────────────────────────────
    'base_datos': {
        'id': 'TEC_BASE_DATOS', 'tipo': 'concepto_tecnico',
        'variantes': ['base de datos','database','db','sqlite','sql','tabla',
                      'consulta','query'],
        'grounding_base': 0.83,
    },

    # ── Hardware y dispositivos ───────────────────
    'computador': {
        'id': 'TEC_COMPUTADOR', 'tipo': 'dispositivo',
        'variantes': ['computador','computadora','pc','laptop','el pc','mi pc',
                      'portátil','portatil'],
        'grounding_base': 0.78,
    },
    'celular': {
        'id': 'TEC_CELULAR', 'tipo': 'dispositivo',
        'variantes': ['celular','teléfono','telefono','el celu','mi celu','el cel'],
        'grounding_base': 0.78,
    },
    'internet': {
        'id': 'TEC_INTERNET', 'tipo': 'servicio',
        'variantes': ['internet','conexión','conexion','wifi','red','sin internet',
                      'sin conexión','la red'],
        'grounding_base': 0.78,
    },

    # ── Acciones técnicas ─────────────────────────
    'correr': {
        'id': 'TEC_CORRER', 'tipo': 'accion_tecnica',
        'variantes': ['correr','ejecutar','corre','corré','arranca','iniciar',
                      'lanzar','levantar','run'],
        'grounding_base': 0.82,
    },
    'instalar': {
        'id': 'TEC_INSTALAR', 'tipo': 'accion_tecnica',
        'variantes': ['instalar','instalando','instalé','instala','installation'],
        'grounding_base': 0.82,
    },
    'probar': {
        'id': 'TEC_PROBAR', 'tipo': 'accion_tecnica',
        'variantes': ['probar','probando','probé','test','testear','verificar',
                      'comprobar','revisar'],
        'grounding_base': 0.80,
    },
    'terminal': {
        'id': 'TEC_TERMINAL', 'tipo': 'herramienta',
        'variantes': ['terminal','consola','powershell','cmd','línea de comandos',
                      'command prompt','bash'],
        'grounding_base': 0.82,
    },

    # ── IA y Bell específico ──────────────────────
    'modelo': {
        'id': 'TEC_MODELO', 'tipo': 'concepto_ia',
        'variantes': ['modelo','modelo de lenguaje','llm','groq','llama','gpt'],
        'grounding_base': 0.83,
    },
    'api': {
        'id': 'TEC_API', 'tipo': 'concepto_tecnico',
        'variantes': ['api','api key','la api','llamada a la api','api de groq'],
        'grounding_base': 0.83,
    },
}