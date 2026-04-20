# biblioteca/habilidades/lenguaje/dimensiones/literal.py
# ================================================
# DIMENSIÓN LITERAL
#
# Lee lo que el mensaje dice de manera directa.
# No interpreta, no infiere — lee.
#
# CORRECCIÓN: ahora usa vocab_match que viene de
# GestorVocabulario para saber qué palabras Bell
# ya reconoció, en lugar de procesar solo el texto.
# Las palabras reconocidas tienen más peso que las
# desconocidas al extraer acción y objetos.
# ================================================

import re
from .base import DimensionLenguaje, ResultadoDimension


class DimensionLiteral(DimensionLenguaje):

    NOMBRE = 'literal'
    PESO   = 1.0

    _VERBOS_ACCION = {
        'crea': 'crear', 'crear': 'crear', 'haz': 'crear', 'hace': 'crear',
        'hacer': 'crear', 'genera': 'crear', 'generar': 'crear',
        'construye': 'crear', 'construir': 'crear', 'arma': 'crear',
        'armar': 'crear', 'diseña': 'crear', 'diseñar': 'crear',
        'escribe': 'crear', 'escribir': 'crear', 'escríbeme': 'crear',

        'modifica': 'modificar', 'modificar': 'modificar',
        'cambia': 'modificar', 'cambiar': 'modificar',
        'actualiza': 'modificar', 'actualizar': 'modificar',
        'edita': 'modificar', 'editar': 'modificar',
        'corrige': 'modificar', 'corregir': 'modificar',
        'ajusta': 'modificar', 'ajustar': 'modificar',
        'agrega': 'agregar', 'agregar': 'agregar', 'añade': 'agregar',
        'añadir': 'agregar',
        'quita': 'quitar', 'quitar': 'quitar', 'elimina': 'quitar',
        'eliminar': 'quitar', 'borra': 'quitar', 'borrar': 'quitar',

        'muestra': 'consultar', 'mostrar': 'consultar',
        'dime': 'consultar', 'dame': 'consultar',
        'trae': 'consultar', 'traer': 'consultar',
        'busca': 'consultar', 'buscar': 'consultar',
        'encuentra': 'consultar', 'encontrar': 'consultar',
        'lista': 'consultar', 'listar': 'consultar',
        'consulta': 'consultar', 'consultar': 'consultar',
        'lee': 'consultar', 'leer': 'consultar',

        'ejecuta': 'ejecutar', 'ejecutar': 'ejecutar',
        'corre': 'ejecutar', 'correr': 'ejecutar',
        'lanza': 'ejecutar', 'lanzar': 'ejecutar',
        'inicia': 'ejecutar', 'iniciar': 'ejecutar',
        'abre': 'ejecutar', 'abrir': 'ejecutar',
        'instala': 'ejecutar', 'instalar': 'ejecutar',

        'calcula': 'calcular', 'calcular': 'calcular',
        'resuelve': 'calcular', 'resolver': 'calcular',
        'suma': 'calcular', 'sumar': 'calcular',
        'resta': 'calcular', 'restar': 'calcular',
        'multiplica': 'calcular', 'multiplicar': 'calcular',
        'divide': 'calcular', 'dividir': 'calcular',
        'convierte': 'calcular', 'convertir': 'calcular',

        'analiza': 'analizar', 'analizar': 'analizar',
        'revisa': 'analizar', 'revisar': 'analizar',
        'verifica': 'analizar', 'verificar': 'analizar',
        'explica': 'analizar', 'explicar': 'analizar', 'explícame': 'analizar',
        'describe': 'analizar', 'describir': 'analizar',
        'compara': 'analizar', 'comparar': 'analizar',
        'evalúa': 'analizar', 'evaluar': 'analizar',

        'dile': 'comunicar', 'envía': 'comunicar', 'enviar': 'comunicar',
        'manda': 'comunicar', 'mandar': 'comunicar',
        'responde': 'comunicar', 'responder': 'comunicar',

        'configura': 'configurar', 'configurar': 'configurar',
        'establece': 'configurar', 'establecer': 'configurar',
        'define': 'configurar', 'definir': 'configurar',
        'pon': 'configurar', 'poner': 'configurar',
        'asigna': 'configurar', 'asignar': 'configurar',
        'guarda': 'configurar', 'guardar': 'configurar',
    }

    _NUMEROS_TEXTO = {
        'un': 1, 'una': 1, 'uno': 1, 'dos': 2, 'tres': 3,
        'cuatro': 4, 'cinco': 5, 'seis': 6, 'siete': 7,
        'ocho': 8, 'nueve': 9, 'diez': 10,
        'varios': 'varios', 'muchos': 'muchos', 'todos': 'todos',
    }

    _CONDICIONES = [
        'si', 'cuando', 'mientras', 'siempre que', 'a menos que', 'solo si'
    ]

    _TIEMPO = {
        'ahora': 'inmediato', 'ya': 'inmediato', 'inmediatamente': 'inmediato',
        'hoy': 'hoy', 'mañana': 'mañana', 'después': 'despues',
        'luego': 'despues', 'siempre': 'siempre', 'nunca': 'nunca',
    }

    def analizar(self, texto: str, contexto: dict) -> ResultadoDimension:
        try:
            return self._analizar_interno(texto, contexto)
        except Exception:
            return self._resultado_vacio()

    def _analizar_interno(self, texto: str, contexto: dict) -> ResultadoDimension:
        tl       = texto.lower().strip()
        palabras = tl.split()

        # vocab_match: palabras que Bell ya reconoció
        # Las usamos para dar más peso a conceptos conocidos
        vocab_match   = contexto.get('vocab_match', [])
        palabras_bell = {m['palabra'] for m in vocab_match}

        hallazgos = {
            'texto_limpio':    tl,
            'palabras':        palabras,
            'longitud':        len(palabras),
            'tiene_contenido': len(palabras) > 0,
            'palabras_conocidas_bell': list(palabras_bell),
        }
        senales = []

        # ── ACCIÓN PRINCIPAL ──
        accion = self._extraer_accion(palabras)
        if accion:
            hallazgos['accion_principal'] = accion
            senales.append(f'accion:{accion}')

        # ── OBJETOS ──
        # Prioriza objetos que Bell ya conoce (vocab_match)
        objetos = self._extraer_objetos(tl, palabras, palabras_bell)
        if objetos:
            hallazgos['objetos'] = objetos
            senales.append(f'objetos:{len(objetos)}')

        # ── CANTIDADES Y ASIGNACIONES ──
        cantidades = self._extraer_cantidades(tl, palabras)
        if cantidades:
            hallazgos['cantidades'] = cantidades

        # ── CONDICIÓN ──
        condicion = self._extraer_condicion(tl)
        if condicion:
            hallazgos['condicion'] = condicion
            senales.append('tiene_condicion')

        # ── TIEMPO ──
        tiempo = self._extraer_tiempo(palabras)
        if tiempo:
            hallazgos['tiempo'] = tiempo
            senales.append(f'tiempo:{tiempo}')

        # ── EXPRESIÓN MATEMÁTICA ──
        expresion_mat = self._extraer_expresion_matematica(tl)
        if expresion_mat:
            hallazgos['expresion_matematica'] = expresion_mat
            senales.append('expresion_matematica')

        # ── TIPO DE ORACIÓN ──
        tipo_oracion = self._clasificar_oracion(tl, palabras)
        hallazgos['tipo_oracion'] = tipo_oracion
        senales.append(f'oracion:{tipo_oracion}')

        # ── NEGACIÓN ──
        if any(w in palabras for w in ['no', 'nunca', 'jamás', 'tampoco', 'sin']):
            hallazgos['tiene_negacion'] = True
            senales.append('negacion')

        # ── URGENCIA ──
        if any(w in tl for w in ['urgente', 'ya', 'ahora mismo', 'inmediatamente', 'rápido']):
            hallazgos['urgencia_explicita'] = True
            senales.append('urgencia')

        confianza = 0.5 + (0.08 * len(senales))
        confianza = min(0.95, confianza)

        return self._resultado(
            activa    = len(palabras) > 0,
            confianza = confianza,
            hallazgos = hallazgos,
            senales   = senales,
        )

    def _extraer_accion(self, palabras: list) -> str:
        # Buscar en las primeras 5 palabras primero
        for palabra in palabras[:5]:
            accion = self._VERBOS_ACCION.get(palabra)
            if accion:
                return accion
        # Si no, buscar en todo el texto
        for palabra in palabras:
            accion = self._VERBOS_ACCION.get(palabra)
            if accion:
                return accion
        return ''

    def _extraer_objetos(
        self, texto: str, palabras: list, palabras_bell: set
    ) -> list:
        objetos = []

        # Objetos que Bell ya conoce — máxima prioridad
        for palabra in palabras_bell:
            if palabra in texto and palabra not in objetos:
                objetos.append(palabra)

        # Objetos por artículo determinante
        patron_objeto = re.findall(
            r'(?:una?|el|la|los|las|mi|tu|su|este|esta|ese|esa)\s+(\w+)',
            texto
        )
        for o in patron_objeto:
            if o not in objetos:
                objetos.append(o)

        # Entidades técnicas explícitas
        tecnicos = re.findall(
            r'\b(base\s+de\s+datos|tabla|archivo|carpeta|script|función|'
            r'módulo|clase|variable|api|endpoint|servidor|chatbot|bot|'
            r'aplicación|app|página|web|formulario|reporte|informe)\b',
            texto
        )
        for t in tecnicos:
            if t not in objetos:
                objetos.append(t)

        return list(dict.fromkeys(objetos))

    def _extraer_cantidades(self, texto: str, palabras: list) -> dict:
        cantidades = {}

        numeros = re.findall(r'\b(\d+(?:\.\d+)?)\b', texto)
        if numeros:
            cantidades['numeros_explicitos'] = [
                float(n) if '.' in n else int(n) for n in numeros
            ]

        asignaciones = re.findall(
            r'(\w+)\s*(?:=|sea|igual\s+a|vale|es)\s*(["\']?\w+["\']?)',
            texto
        )
        if asignaciones:
            cantidades['asignaciones'] = {k: v for k, v in asignaciones}

        for palabra in palabras:
            if palabra in self._NUMEROS_TEXTO:
                cantidades['numero_texto'] = self._NUMEROS_TEXTO[palabra]
                break

        return cantidades

    def _extraer_condicion(self, texto: str) -> str:
        for cond in self._CONDICIONES:
            if cond in texto:
                idx = texto.find(cond)
                return texto[idx:idx+60].strip()
        return ''

    def _extraer_tiempo(self, palabras: list) -> str:
        for palabra in palabras:
            if palabra in self._TIEMPO:
                return self._TIEMPO[palabra]
        return ''

    def _extraer_expresion_matematica(self, texto: str) -> str:
        patron = re.search(
            r'\d+\s*[\+\-\*\/\^]\s*\d+(?:\s*[\+\-\*\/\^]\s*\d+)*',
            texto
        )
        return patron.group(0).strip() if patron else ''

    def _clasificar_oracion(self, texto: str, palabras: list) -> str:
        if not palabras:
            return 'vacia'
        primera = palabras[0]
        if texto.endswith('?') or primera in [
            'qué', 'que', 'cómo', 'como', 'cuándo', 'cuando',
            'dónde', 'donde', 'quién', 'quien', 'cuál', 'cual',
            'cuánto', 'cuanto',
        ]:
            return 'pregunta'
        if primera in self._VERBOS_ACCION:
            return 'orden'
        if texto.endswith('!'):
            return 'exclamacion'
        if primera in ['no', 'nunca', 'jamás']:
            return 'negacion'
        return 'declaracion'