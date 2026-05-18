# biblioteca/habilidades/lenguaje/dimensiones/tecnica.py
# ================================================
# DIMENSIÓN TÉCNICA — v2 con Python completo
# Detecta los 5 modos de la habilidad Python:
# analisis, generacion, explicacion, debug, auto_analisis
# También detecta verbosidad pedida por el usuario
# ================================================

import re
from .base import DimensionLenguaje, ResultadoDimension


class DimensionTecnica(DimensionLenguaje):

    NOMBRE = 'tecnica'
    PESO   = 1.4

    _DOMINIOS = {
        'BASE_DE_DATOS': {
            'habilidad': 'SQLITE',
            'coloquial': [
                'base de datos', 'tabla', 'tablas', 'guardar datos',
                'almacenar', 'registro', 'registros', 'fila', 'columna',
                'pon en la base', 'guarda en la base', 'busca en la base',
                'consulta la base', 'trae de la base', 'crear tabla',
                'nueva tabla', 'agregar columna',
            ],
            'tecnico': [
                'select', 'insert', 'update', 'delete', 'create table',
                'drop table', 'alter table', 'where', 'from', 'join',
                'inner join', 'left join', 'group by', 'order by',
                'having', 'distinct', 'count', 'sum', 'avg',
                'varchar', 'integer', 'primary key', 'foreign key',
                'sqlite', 'sql', 'database', 'db',
            ],
            'patrones': [
                r'\bbase\s+de\s+datos\b',
                r'\bguarda(?:r)?\s+(?:en|los?|las?|esto|eso)\b',
                r'\bcrea(?:r)?\s+(?:una?\s+)?tabla\b',
                r'\bpon(?:er)?\s+(?:en\s+)?(?:la\s+)?(?:base|tabla)\b',
                r'\bconsulta(?:r)?\b.*\b(?:base|tabla|datos)\b',
                r'\bselect\b', r'\binsert\b', r'\bcreate\s+table\b',
            ],
            'confianza': 0.88,
        },
        'CALCULO': {
            'habilidad': 'CALCULO',
            'coloquial': [
                'calcula', 'calcular', 'cuánto es', 'cuanto es',
                'cuánto da', 'cuanto da', 'dame el resultado',
                'resuelve', 'resolver', 'cuánto vale', 'cuanto vale',
                'convierte', 'convertir', 'pasa a', 'porcentaje de',
                'promedio de', 'media de', 'cuántos son', 'cuantos son',
            ],
            'tecnico': [
                'integral', 'derivada', 'factorial', 'raíz cuadrada',
                'raiz cuadrada', 'sqrt', 'logaritmo', 'log(',
                'potencia', 'exponente', 'módulo', 'modulo',
            ],
            'patrones': [
                r'\b\d+\s*[\+\-\*\/\^]\s*\d+\b',
                r'\bcalcula(?:r)?\b',
                r'\bcu[aá]nto\s+(?:es|da|vale|son)\b',
                r'\bresuelve(?:r)?\b',
                r'\bconvierte(?:r)?\s+\d+',
                r'\bpromedio\s+de\b',
                r'\b\d+\s*%\s+de\s+\d+\b',
            ],
            'confianza': 0.90,
        },
        # ── PYTHON COMPLETO — 5 modos ──────────────────────────────
        'CODIGO_PYTHON': {
            'habilidad': 'PYTHON_COMPLETO',
            # Modo 1: ANÁLISIS — Bell lee código y dice qué hace / qué tiene mal
            'coloquial_analisis': [
                'analiza este código', 'analiza el código', 'analiza mi código',
                'revisa este código', 'revisa el código', 'revísame el código',
                'qué hace este código', 'qué hace esta función', 'qué hace esta clase',
                'qué hace este script', 'lee este código', 'mira este código',
                'tiene errores', 'tiene bugs', 'qué está mal', 'qué falla',
                'qué malas prácticas', 'cómo mejoro este código', 'cómo optimizo',
                'retroalimentación del código', 'feedback del código',
                'qué puedo mejorar', 'está bien escrito', 'está mal escrito',
            ],
            # Modo 2: GENERACIÓN — Bell crea código desde descripción
            'coloquial_generacion': [
                'crea un script', 'crea una función', 'crea una clase',
                'escribe el código', 'escribe un script', 'escribe una función',
                'hazme el código', 'hazme un script', 'hazme una función',
                'genera el código', 'genera una función', 'programa que',
                'necesito un script', 'necesito una función', 'necesito el código',
                'crea el código para', 'escríbeme', 'genérame', 'hazme',
                'código que haga', 'función que', 'clase que',
            ],
            # Modo 3: EXPLICACIÓN — Bell explica conceptos Python
            'coloquial_explicacion': [
                'qué es un decorador', 'cómo funciona async', 'qué es async',
                'qué son los generadores', 'cómo funcionan los generadores',
                'qué es yield', 'qué es lambda', 'cómo funciona lambda',
                'qué es una lista por comprensión', 'list comprehension',
                'qué es gil', 'qué es el gil', 'qué es un context manager',
                'cómo funciona with', 'qué es unittest', 'qué es pytest',
                'qué es pip', 'qué es venv', 'qué es virtualenv',
                'qué son los type hints', 'qué es dataclass', 'qué es pydantic',
                'cómo funciona flask', 'cómo funciona django',
                'cómo funciona socketio', 'qué es websocket',
                'cómo funciona git', 'qué es un commit', 'qué es un branch',
                'cómo hago un bucle', 'cómo hago un loop', 'cómo itero',
                'cómo funciona', 'qué es', 'explícame', 'explicame',
                'no entiendo', 'cuéntame sobre',
            ],
            # Modo 4: DEBUG — Bell diagnostica errores
            'coloquial_debug': [
                'tengo este error', 'me sale este error', 'me da este error',
                'error de importación', 'error de import', 'moduleerror',
                'traceback', 'exception', 'attributeerror', 'typeerror',
                'valueerror', 'keyerror', 'indexerror', 'nameerror',
                'syntaxerror', 'indentationerror', 'runtimeerror',
                'por qué falla', 'por qué no funciona', 'no corre',
                'no arranca', 'se rompe', 'se cuelga', 'falla en',
                'ayúdame con el error', 'ayudame con el error',
                'cómo arreglo', 'cómo soluciono', 'cómo debugueo',
                'debugueo', 'debug', 'depurar',
            ],
            # Modo 5: AUTO-ANÁLISIS — Bell se analiza a sí misma
            'coloquial_auto': [
                'analiza tu propio código', 'analiza tu código',
                'analiza tus archivos', 'analiza tu capa', 'analiza tu biblioteca',
                'qué puedes mejorar de ti', 'qué puedes mejorar en tu código',
                'tienes bugs en tu código', 'qué falla en ti',
                'revisa tu código', 'cómo está tu código',
                'analiza belladonna', 'analiza tu arquitectura',
                'qué mejorarías de ti', 'analiza capa', 'analiza la capa',
            ],
            # Coloquial general (cualquier modo)
            'coloquial': [
                'código', 'codigo', 'script', 'programa', 'función', 'funcion',
                'clase', 'método', 'metodo', 'variable', 'bucle', 'loop',
                'módulo', 'modulo', 'archivo python', 'librería', 'libreria',
                'python', 'pip install', 'entorno virtual', 'venv',
                'flask', 'django', 'fastapi', 'pytest', 'unittest',
            ],
            'tecnico': [
                'def ', 'class ', 'import ', 'from ', 'return',
                'if __name__', 'lambda', 'yield', 'async', 'await',
                'try:', 'except:', 'for ', 'while ', '.py', 'python',
                '@', 'self.', '__init__', '__str__', '__repr__',
                'list(', 'dict(', 'tuple(', 'set(', 'isinstance(',
            ],
            'patrones': [
                r'\bdef\s+\w+\(',
                r'\bclass\s+\w+',
                r'\bimport\s+\w+',
                r'\bfunci[oó]n\s+(?:que|para|de|que)\b',
                r'\bescribe(?:r)?\s+(?:un?\s+)?c[oó]digo\b',
                r'\bcrea(?:r)?\s+(?:un?\s+)?script\b',
                r'\banaliza\s+(?:este|el|mi|tu)\s+c[oó]digo\b',
                r'\bqu[eé]\s+hace\s+(?:este|el|esta)\s+c[oó]digo\b',
                r'\btengo\s+(?:un\s+)?error\b',
                r'\bTraceback\b',
                r'\b\w+Error:\s*\w+',
                r'^\s*def\s+', r'^\s*class\s+', r'^\s*import\s+',
            ],
            'confianza': 0.90,
        },
        'SHELL': {
            'habilidad': 'SHELL',
            'coloquial': [
                'ejecuta', 'ejecutar', 'corre', 'correr', 'lanza', 'lanzar',
                'comando', 'terminal', 'consola', 'lista los archivos',
                'muestra los archivos', 'crea carpeta',
            ],
            'tecnico': [
                'ls', 'dir', 'cd', 'mkdir', 'rm', 'cp', 'mv', 'cat',
                'grep', 'find', 'chmod', 'git', 'npm', 'pip', 'bash',
                'powershell', 'cmd', '&&', '||',
            ],
            'patrones': [
                r'\bejecuta(?:r)?\b.*\bcomando\b',
                r'\blista(?:r)?\s+(?:los?\s+)?archivos\b',
                r'\bcrea(?:r)?\s+(?:una?\s+)?carpeta\b',
                r'\b(?:ls|dir|mkdir|cd|rm|cp|mv|cat|grep)(?:\s|$)',
                r'\bgit\s+(?:init|add|commit|push|pull|clone|status)\b',
                r'\bnpm\s+(?:install|start|run|build)\b',
            ],
            'confianza': 0.87,
        },
        'MATEMATICA_AVANZADA': {
            'habilidad': 'CALCULO',
            'coloquial': [
                'integral', 'derivada', 'límite', 'limite', 'ecuación',
                'ecuacion', 'sistema de ecuaciones', 'matriz', 'vector',
                'probabilidad', 'estadística', 'estadistica', 'media',
                'mediana', 'desviación estándar', 'varianza',
            ],
            'tecnico': [
                '∫', '∂', 'lim', 'Σ', 'π', '√', '±', 'dx', 'dy',
                'f(x)', 'sen', 'cos', 'tan', 'ln', 'arcsin',
            ],
            'patrones': [
                r'\bintegral\b', r'\bderivada\b',
                r'\blím(?:ite)?\b', r'\bm[aá]triz\b',
                r'\d+\s*\^\s*\d+', r'√\d+',
            ],
            'confianza': 0.85,
        },
    }

    # ── Palabras que indican verbosidad deseada ────────────────────
    _VERBOSIDAD_SIMPLE = [
        'más simple', 'mas simple', 'más sencillo', 'mas sencillo',
        'resúmelo', 'resumelo', 'resumir', 'más corto', 'mas corto',
        'brevemente', 'en pocas palabras', 'resumido', 'breve',
        'corto', 'simplifica', 'simplificado', 'de manera simple',
        'sin tecnicismos', 'fácil de entender', 'facil de entender',
        'como si fuera un niño', 'para alguien que no sabe',
        'sin tanto detalle', 'no tan técnico', 'no tan tecnico',
    ]
    _VERBOSIDAD_DETALLADA = [
        'más detallado', 'mas detallado', 'con más detalle', 'con mas detalle',
        'profundo', 'explícame bien', 'explicame bien', 'completo',
        'todo lo que puedas', 'el análisis completo', 'análisis profundo',
        'a fondo', 'explica cada parte', 'explícame todo',
        'en detalle', 'técnicamente', 'con tecnicismos',
    ]

    _ENTIDADES_TECNICAS = {
        'api': 'interfaz', 'endpoint': 'interfaz', 'webhook': 'interfaz',
        'json': 'formato', 'csv': 'formato', 'xml': 'formato',
        'http': 'protocolo', 'https': 'protocolo', 'rest': 'arquitectura',
        'token': 'seguridad', 'hash': 'seguridad',
        'servidor': 'infraestructura', 'request': 'protocolo',
        'response': 'protocolo', 'callback': 'patron', 'async': 'patron',
        'thread': 'sistema',
    }

    def analizar(self, texto: str, contexto: dict) -> ResultadoDimension:
        try:
            return self._analizar_interno(texto, contexto)
        except Exception:
            return self._resultado_vacio()

    def _analizar_interno(self, texto: str, contexto: dict) -> ResultadoDimension:
        tl = texto.lower().strip()

        vocab_match   = contexto.get('vocab_match', [])
        ids_conocidos = contexto.get('ids_conocidos', [])

        hallazgos = {}
        senales   = []

        conceptos_bell = [
            m for m in vocab_match
            if m.get('concepto', {}).get('tipo', '') in ('identidad_bell', 'pregunta_bell')
        ]
        conceptos_tecnicos_vocab = any(
            m.get('concepto', {}).get('tipo', '') == 'tecnico'
            for m in vocab_match
        )
        # Solo suprimir si hay concepto Bell Y no hay indicadores técnicos
        # TAMBIÉN checar los patrones regex antes de decidir — fix del early return
        if conceptos_bell and not conceptos_tecnicos_vocab:
            # Verificar patrones técnicos en el texto crudo antes de rendirse
            tl_check = texto.lower()
            tiene_patron_tecnico = any(
                re.search(p, tl_check, re.IGNORECASE | re.MULTILINE)
                for cfg in self._DOMINIOS.values()
                for p in cfg.get('patrones', [])
            )
            if not tiene_patron_tecnico:
                # Verificar también palabras técnicas simples
                tiene_tecnico_simple = any(
                    word in tl_check
                    for cfg in self._DOMINIOS.values()
                    for word in cfg.get('tecnico', [])[:5]  # solo primeras 5 por eficiencia
                )
                if not tiene_tecnico_simple:
                    return self._resultado(
                        activa=False, confianza=0.1,
                        hallazgos={'sobre_bell': True},
                        senales=['no_tecnico_sobre_bell'],
                    )

        # ── Detectar verbosidad ──────────────────────────────────────
        verbosidad = 'normal'
        if any(v in tl for v in self._VERBOSIDAD_SIMPLE):
            verbosidad = 'simple'
            senales.append('verbosidad:simple')
        elif any(v in tl for v in self._VERBOSIDAD_DETALLADA):
            verbosidad = 'detallado'
            senales.append('verbosidad:detallado')
        hallazgos['verbosidad'] = verbosidad

        # ── Detectar modo Python específico ─────────────────────────
        modo_python = None
        if self._detectar_modo(tl, 'coloquial_analisis'):
            modo_python = 'analisis'
        elif self._detectar_modo(tl, 'coloquial_debug'):
            modo_python = 'debug'
        elif self._detectar_modo(tl, 'coloquial_auto'):
            modo_python = 'auto_analisis'
        elif self._detectar_modo(tl, 'coloquial_generacion'):
            modo_python = 'generacion'
        elif self._detectar_modo(tl, 'coloquial_explicacion'):
            modo_python = 'explicacion'

        if modo_python:
            hallazgos['modo_python'] = modo_python
            senales.append(f'modo_python:{modo_python}')

        dominios_activos = self._detectar_dominios(tl)
        if dominios_activos:
            dominio_principal = dominios_activos[0]
            hallazgos['dominio_tecnico']     = dominio_principal['dominio']
            hallazgos['habilidad_requerida'] = dominio_principal['habilidad']
            hallazgos['confianza_dominio']   = dominio_principal['confianza']
            hallazgos['todos_dominios']      = [d['dominio'] for d in dominios_activos]
            senales.append(f'dominio:{dominio_principal["dominio"]}')
            if dominio_principal['habilidad']:
                senales.append(f'habilidad:{dominio_principal["habilidad"]}')

        nivel = self._evaluar_nivel_tecnicismo(tl)
        hallazgos['nivel_tecnicismo'] = nivel
        senales.append(f'nivel:{nivel}')

        entidades = {
            ent: tipo
            for ent, tipo in self._ENTIDADES_TECNICAS.items()
            if ent in tl
        }
        if entidades:
            hallazgos['entidades_tecnicas'] = entidades
            senales.append(f'entidades:{len(entidades)}')

        parametros = self._extraer_parametros(tl, dominios_activos)
        if parametros:
            hallazgos['parametros_extraidos'] = parametros
            senales.append('parametros_extraidos')

        if dominios_activos:
            es_coloquial = self._es_coloquial(tl, dominios_activos[0])
            hallazgos['lenguaje_coloquial']  = es_coloquial
            hallazgos['necesita_traduccion'] = es_coloquial
            if es_coloquial:
                senales.append('traduccion_requerida')

        activa    = len(dominios_activos) > 0 or len(entidades) > 0 or bool(modo_python)
        confianza = dominios_activos[0]['confianza'] if dominios_activos else (0.80 if modo_python else 0.3)
        confianza = min(0.95, confianza)

        return self._resultado(activa=activa, confianza=confianza,
                               hallazgos=hallazgos, senales=senales)

    def _detectar_modo(self, texto: str, clave_lista: str) -> bool:
        lista = self._DOMINIOS.get('CODIGO_PYTHON', {}).get(clave_lista, [])
        return any(p in texto for p in lista)

    def _detectar_dominios(self, texto: str) -> list:
        detectados = []
        for nombre, config in self._DOMINIOS.items():
            score = 0.0
            if any(p in texto for p in config.get('coloquial', [])):
                score += 0.3
            # Para CODIGO_PYTHON también checar las sublistas de modos
            if nombre == 'CODIGO_PYTHON':
                for clave in ['coloquial_analisis','coloquial_generacion',
                              'coloquial_explicacion','coloquial_debug','coloquial_auto']:
                    if any(p in texto for p in config.get(clave, [])):
                        score += 0.4
                        break
            if any(p in texto for p in config.get('tecnico', [])):
                score += 0.5
            for patron in config.get('patrones', []):
                if re.search(patron, texto, re.IGNORECASE | re.MULTILINE):
                    score += 0.4
                    break
            if score > 0:
                detectados.append({
                    'dominio':   nombre,
                    'habilidad': config['habilidad'],
                    'confianza': min(0.95, config['confianza'] * (score / 0.5)),
                    'score':     score,
                })
        detectados.sort(key=lambda x: x['score'], reverse=True)
        return detectados

    def _evaluar_nivel_tecnicismo(self, texto: str) -> str:
        alto  = ['select', 'insert', 'def ', 'class ', 'import ',
                 'async', 'await', 'api', 'endpoint']
        medio = ['función', 'funcion', 'variable', 'bucle', 'tabla',
                 'columna', 'dato', 'valor', 'archivo', 'carpeta']
        if sum(1 for t in alto  if t in texto) >= 2: return 'experto'
        if sum(1 for t in alto  if t in texto) >= 1: return 'intermedio'
        if sum(1 for t in medio if t in texto) >= 1: return 'basico'
        return 'coloquial'

    def _extraer_parametros(self, texto: str, dominios: list) -> dict:
        parametros = {}
        if not dominios:
            return parametros
        dominio = dominios[0]['dominio']
        if dominio == 'BASE_DE_DATOS':
            tabla = re.search(r'(?:tabla|table|en\s+la?\s+)[\s_"]?(\w+)', texto, re.IGNORECASE)
            if tabla:
                parametros['nombre_tabla'] = tabla.group(1)
            pares = re.findall(r'(\w+)\s*(?:=|sea|vale|es|igual\s+a)\s*([\"\']?\w+[\"\']?)', texto)
            if pares:
                parametros['pares_clave_valor'] = {k: v for k, v in pares}
        elif dominio in ('CALCULO', 'MATEMATICA_AVANZADA'):
            expresion = re.search(r'[\d\+\-\*\/\^\(\)\.\s]+', texto)
            if expresion:
                parametros['expresion'] = expresion.group(0).strip()
        return parametros

    def _es_coloquial(self, texto: str, dominio: dict) -> bool:
        palabras_tecnicas = self._DOMINIOS.get(dominio['dominio'], {}).get('tecnico', [])
        return not any(p in texto for p in palabras_tecnicas)