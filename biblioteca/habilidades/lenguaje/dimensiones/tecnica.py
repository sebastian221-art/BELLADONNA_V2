# biblioteca/habilidades/lenguaje/dimensiones/tecnica.py
# ================================================
# DIMENSIÓN TÉCNICA
#
# Entiende la intención técnica sin que se le
# tenga que hablar en lenguaje de máquina.
#
# CORRECCIÓN: usa vocab_match para saber si Bell
# ya reconoció conceptos técnicos (tabla, base de datos,
# función, etc.) via su vocabulario propio,
# y los usa como señales de alta confianza
# antes de buscar por regex.
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
                r'\b\w+\s*=\s*\d+\b.*\b(?:tabla|base|datos|guardar)\b',
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
                'raiz cuadrada', 'sqrt', 'logaritmo', 'log',
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
        'CODIGO_PYTHON': {
            'habilidad': 'ANALISIS_PYTHON',
            'coloquial': [
                'código', 'codigo', 'script', 'programa', 'función', 'funcion',
                'clase', 'método', 'metodo', 'variable', 'bucle', 'loop',
                'módulo', 'modulo', 'archivo python', 'crea el código',
                'escribe el código', 'hazme un script', 'programa que',
            ],
            'tecnico': [
                'def ', 'class ', 'import ', 'from ', 'return',
                'if __name__', 'lambda', 'yield', 'async', 'await',
                'try:', 'except:', 'for ', 'while ', '.py', 'python',
            ],
            'patrones': [
                r'\bdef\s+\w+\(',
                r'\bclass\s+\w+',
                r'\bimport\s+\w+',
                r'\bfunci[oó]n\s+(?:que|para|de)\b',
                r'\bescribe(?:r)?\s+(?:un?\s+)?c[oó]digo\b',
                r'\bcrea(?:r)?\s+(?:un?\s+)?script\b',
            ],
            'confianza': 0.85,
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
                r'\b(?:ls|dir|mkdir|cd|rm|cp|mv|cat|grep)\b',
                r'\bgit\s+(?:init|add|commit|push|pull|clone)\b',
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

        # vocab_match: qué reconoció Bell ya
        vocab_match   = contexto.get('vocab_match', [])
        ids_conocidos = contexto.get('ids_conocidos', [])

        hallazgos = {}
        senales   = []

        # ── PASO 1: Señales técnicas que Bell ya reconoció ──
        # Si GestorVocabulario identificó conceptos técnicos
        # (tabla, función, script...) les damos alta confianza
        conceptos_tecnicos_bell = [
            m for m in vocab_match
            if m.get('concepto', {}).get('tipo', '') in (
                'identidad_bell', 'pregunta_bell'
            )
        ]
        # Si son sobre Bell (no técnicos), esta dimensión baja su peso
        if conceptos_tecnicos_bell and not any(
            m.get('concepto', {}).get('tipo', '') == 'tecnico'
            for m in vocab_match
        ):
            # El mensaje es sobre Bell, no técnico
            return self._resultado(
                activa    = False,
                confianza = 0.1,
                hallazgos = {'sobre_bell': True},
                senales   = ['no_tecnico_sobre_bell'],
            )

        # ── PASO 2: Detección de dominio técnico ──
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

        # ── Nivel de tecnicismo ──
        nivel = self._evaluar_nivel_tecnicismo(tl)
        hallazgos['nivel_tecnicismo'] = nivel
        senales.append(f'nivel:{nivel}')

        # ── Entidades técnicas ──
        entidades = {
            ent: tipo
            for ent, tipo in self._ENTIDADES_TECNICAS.items()
            if ent in tl
        }
        if entidades:
            hallazgos['entidades_tecnicas'] = entidades
            senales.append(f'entidades:{len(entidades)}')

        # ── Parámetros técnicos extraídos ──
        parametros = self._extraer_parametros(tl, dominios_activos)
        if parametros:
            hallazgos['parametros_extraidos'] = parametros
            senales.append('parametros_extraidos')

        # ── Lenguaje coloquial vs técnico ──
        if dominios_activos:
            es_coloquial = self._es_coloquial(tl, dominios_activos[0])
            hallazgos['lenguaje_coloquial']   = es_coloquial
            hallazgos['necesita_traduccion']  = es_coloquial
            if es_coloquial:
                senales.append('traduccion_requerida')

        activa    = len(dominios_activos) > 0 or len(entidades) > 0
        confianza = dominios_activos[0]['confianza'] if dominios_activos else 0.3
        confianza = min(0.95, confianza)

        return self._resultado(
            activa    = activa,
            confianza = confianza,
            hallazgos = hallazgos,
            senales   = senales,
        )

    def _detectar_dominios(self, texto: str) -> list:
        detectados = []
        for nombre, config in self._DOMINIOS.items():
            score = 0.0
            if any(p in texto for p in config['coloquial']):
                score += 0.3
            if any(p in texto for p in config['tecnico']):
                score += 0.5
            for patron in config['patrones']:
                if re.search(patron, texto, re.IGNORECASE):
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
            tabla = re.search(
                r'(?:tabla|table|en\s+la?\s+)[\s_"]?(\w+)',
                texto, re.IGNORECASE
            )
            if tabla:
                parametros['nombre_tabla'] = tabla.group(1)

            pares = re.findall(
                r'(\w+)\s*(?:=|sea|vale|es|igual\s+a)\s*(["\']?\w+["\']?)',
                texto
            )
            if pares:
                parametros['pares_clave_valor'] = {k: v for k, v in pares}

        elif dominio in ('CALCULO', 'MATEMATICA_AVANZADA'):
            expresion = re.search(r'[\d\+\-\*\/\^\(\)\.\s]+', texto)
            if expresion:
                parametros['expresion'] = expresion.group(0).strip()

            conversion = re.search(
                r'(\d+(?:\.\d+)?)\s*(\w+)\s+(?:a|en)\s+(\w+)', texto
            )
            if conversion:
                parametros['valor']          = conversion.group(1)
                parametros['unidad_origen']  = conversion.group(2)
                parametros['unidad_destino'] = conversion.group(3)

        return parametros

    def _es_coloquial(self, texto: str, dominio: dict) -> bool:
        palabras_tecnicas = self._DOMINIOS.get(
            dominio['dominio'], {}
        ).get('tecnico', [])
        return not any(p in texto for p in palabras_tecnicas)