# capas/capa1/traductor.py
# ================================================
# TRADUCTOR A LENGUAJE BELL — v4
#
# Traduce texto humano a conceptos de Bell.
# Lo conocido → ConceptoTraducido
# Lo desconocido → Desconocido (zona de aprendizaje)
#
# v4:
# — Vocabulario base expandido (+80 términos)
# — Colombianismos reconocidos
# — Términos técnicos Bell (capa, motor, habilidad...)
# — Términos de programación frecuentes
# — Emociones y estados comunes
# — Stopwords más completas para menos ruido
# ================================================

from capas.capa1.paquete_capa1 import ConceptoTraducido, Desconocido
from typing import List, Tuple, Optional


class Traductor:

    def __init__(self):
        self._gestor = None
        self._inicializar_gestor()

    def _inicializar_gestor(self):
        try:
            from biblioteca.vocabulario.gestor_vocabulario import GestorVocabulario
            self._gestor = GestorVocabulario.obtener()
        except Exception as e:
            print(f'Traductor: vocabulario no disponible — {e}')
            self._gestor = None

    def traducir(
        self, contenido_normalizado: dict
    ) -> Tuple[List[ConceptoTraducido], List[Desconocido], float]:

        texto = contenido_normalizado.get('contenido_limpio', '')
        if not texto:
            return [], [], 0.0

        conceptos    = []
        desconocidos = []

        if self._gestor:
            resultados = self._gestor.buscar_frase(texto)
            palabras_encontradas = set()

            for resultado in resultados:
                palabra  = resultado['palabra']
                concepto = resultado['concepto']

                palabras_encontradas.add(palabra)
                if ' ' in palabra:
                    for componente in palabra.split():
                        palabras_encontradas.add(componente)

                conceptos.append(ConceptoTraducido(
                    id=concepto['id'],
                    texto_original=palabra,
                    grounding=concepto.get('grounding', 0.5),
                    certeza='directo',
                    tipo=concepto.get('tipo', 'concepto')
                ))

            tokens = self._tokenizar(texto)
            for token in tokens:
                if token in palabras_encontradas:
                    continue

                # 1. Buscar en GestorVocabulario
                concepto_gestor = self._gestor.buscar(token)
                if concepto_gestor:
                    conceptos.append(ConceptoTraducido(
                        id=concepto_gestor['id'],
                        texto_original=token,
                        grounding=concepto_gestor.get('grounding', 0.5),
                        certeza='directo',
                        tipo=concepto_gestor.get('tipo', 'concepto')
                    ))
                    palabras_encontradas.add(token)
                    continue

                # 2. Buscar en vocabulario base expandido
                concepto_base = self._buscar_vocabulario_base(token)
                if concepto_base:
                    conceptos.append(ConceptoTraducido(
                        id=concepto_base['id'],
                        texto_original=token,
                        grounding=concepto_base['grounding'],
                        certeza='directo',
                        tipo=concepto_base.get('tipo', 'concepto')
                    ))
                    palabras_encontradas.add(token)
                else:
                    desconocidos.append(Desconocido(
                        fragmento=token,
                        tipo='concepto',
                        inferencia=None
                    ))
        else:
            tokens = self._tokenizar(texto)
            for token in tokens:
                concepto = self._buscar_vocabulario_base(token)
                if concepto:
                    conceptos.append(ConceptoTraducido(
                        id=concepto['id'],
                        texto_original=token,
                        grounding=concepto['grounding'],
                        certeza='directo',
                        tipo=concepto.get('tipo', 'concepto')
                    ))
                else:
                    desconocidos.append(Desconocido(
                        fragmento=token,
                        tipo='concepto',
                        inferencia=None
                    ))

        certeza = (
            sum(c.grounding for c in conceptos) / len(conceptos)
            if conceptos else 0.0
        )

        return conceptos, desconocidos, certeza

    def _tokenizar(self, texto: str) -> List[str]:
        """
        Tokeniza el texto eliminando stopwords.
        v4: lista expandida para menos ruido en desconocidos.
        """
        stopwords = {
            # Artículos
            'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas',
            # Preposiciones
            'de', 'del', 'en', 'a', 'al', 'con', 'por', 'para',
            'sin', 'sobre', 'bajo', 'ante', 'tras', 'hasta', 'desde',
            'entre', 'hacia', 'durante', 'mediante', 'según',
            # Pronombres
            'se', 'me', 'te', 'le', 'nos', 'les', 'lo', 'vos',
            'mi', 'tu', 'su', 'mis', 'tus', 'sus', 'yo', 'él',
            'ella', 'ello', 'nosotros', 'ellos', 'ellas',
            'este', 'esta', 'esto', 'ese', 'esa', 'eso',
            'aquel', 'aquella', 'aquello',
            # Conjunciones
            'y', 'o', 'u', 'e', 'ni', 'pero', 'sino', 'aunque',
            'porque', 'que', 'si', 'cuando', 'mientras', 'donde',
            'como', 'pues', 'luego', 'entonces',
            # Auxiliares y cópulas
            'es', 'son', 'ha', 'han', 'hay', 'era', 'eran',
            'fue', 'fueron', 'ser', 'estar', 'soy', 'eres',
            'somos', 'sois', 'estoy', 'estás', 'está', 'estamos',
            'haber', 'tener', 'tengo', 'tienes', 'tiene',
            # Adverbios comunes
            'no', 'más', 'mas', 'ya', 'aún', 'aun', 'también',
            'tambien', 'solo', 'sólo', 'muy', 'bien', 'mal',
            'aquí', 'ahí', 'allí', 'antes', 'después', 'ahora',
            'siempre', 'nunca', 'algo', 'nada', 'todo', 'todos',
            # Interrogativos/relativos (sin tilde — normalizados)
            'cual', 'cuales', 'quien', 'quienes',
        }

        _PUNTUACION = set('.,;:!?¿¡\"\' ()[]{}')
        tokens = texto.lower().split()
        resultado = []
        for t in tokens:
            limpio = t
            for c in '.,;:!?¿¡\"\' ()[]{}': limpio = limpio.replace(c, '')
            if limpio and len(limpio) > 1 and limpio not in stopwords:
                resultado.append(limpio)
        return resultado

    def _buscar_vocabulario_base(self, token: str) -> Optional[dict]:
        """
        Vocabulario base expandido v4.
        Cubre: identidad Bell, acciones, entidades,
        términos técnicos, colombianismos, emociones.
        """
        base = {
            # ── Identidad Bell ───────────────────────────
            'bell':         {'id': 'BELL_NOMBRE_BELL',       'grounding': 1.0, 'tipo': 'identidad'},
            'belladonna':   {'id': 'BELL_NOMBRE_BELLADONNA',  'grounding': 1.0, 'tipo': 'identidad'},
            'sebastian':    {'id': 'NEURONA_SEBASTIAN',       'grounding': 1.0, 'tipo': 'identidad'},
            'sebas':        {'id': 'NEURONA_SEBASTIAN',       'grounding': 1.0, 'tipo': 'identidad'},

            # ── Acciones generales ───────────────────────
            'crear':        {'id': 'ACCION_CREAR',    'grounding': 0.9, 'tipo': 'accion'},
            'mostrar':      {'id': 'ACCION_MOSTRAR',  'grounding': 0.9, 'tipo': 'accion'},
            'buscar':       {'id': 'ACCION_BUSCAR',   'grounding': 0.9, 'tipo': 'accion'},
            'borrar':       {'id': 'ACCION_BORRAR',   'grounding': 0.9, 'tipo': 'accion'},
            'agregar':      {'id': 'ACCION_AGREGAR',  'grounding': 0.9, 'tipo': 'accion'},
            'analizar':     {'id': 'ACCION_ANALIZAR', 'grounding': 0.9, 'tipo': 'accion'},
            'ejecutar':     {'id': 'ACCION_EJECUTAR', 'grounding': 0.9, 'tipo': 'accion'},
            'ayuda':        {'id': 'VERBO_AYUDA',     'grounding': 0.9, 'tipo': 'verbo'},
            'ayudar':       {'id': 'VERBO_AYUDA',     'grounding': 0.9, 'tipo': 'verbo'},
            'hacer':        {'id': 'ACCION_HACER',    'grounding': 0.8, 'tipo': 'accion'},
            'decir':        {'id': 'ACCION_DECIR',    'grounding': 0.8, 'tipo': 'accion'},
            'ver':          {'id': 'ACCION_VER',      'grounding': 0.8, 'tipo': 'accion'},
            'saber':        {'id': 'ACCION_SABER',    'grounding': 0.8, 'tipo': 'accion'},
            'querer':       {'id': 'ACCION_QUERER',   'grounding': 0.8, 'tipo': 'accion'},
            'poder':        {'id': 'ACCION_PODER',    'grounding': 0.8, 'tipo': 'accion'},
            'ir':           {'id': 'ACCION_IR',       'grounding': 0.7, 'tipo': 'accion'},
            'venir':        {'id': 'ACCION_VENIR',    'grounding': 0.7, 'tipo': 'accion'},

            # ── Entidades comunes ────────────────────────
            'archivo':      {'id': 'ENTIDAD_ARCHIVO',   'grounding': 1.0, 'tipo': 'entidad'},
            'carpeta':      {'id': 'ENTIDAD_CARPETA',   'grounding': 1.0, 'tipo': 'entidad'},
            'código':       {'id': 'ENTIDAD_CODIGO',    'grounding': 1.0, 'tipo': 'entidad'},
            'codigo':       {'id': 'ENTIDAD_CODIGO',    'grounding': 1.0, 'tipo': 'entidad'},
            'error':        {'id': 'ENTIDAD_ERROR',     'grounding': 1.0, 'tipo': 'entidad'},
            'función':      {'id': 'ENTIDAD_FUNCION',   'grounding': 0.9, 'tipo': 'entidad'},
            'funcion':      {'id': 'ENTIDAD_FUNCION',   'grounding': 0.9, 'tipo': 'entidad'},
            'clase':        {'id': 'ENTIDAD_CLASE',     'grounding': 0.9, 'tipo': 'entidad'},
            'variable':     {'id': 'ENTIDAD_VARIABLE',  'grounding': 0.9, 'tipo': 'entidad'},
            'lista':        {'id': 'ENTIDAD_LISTA',     'grounding': 0.9, 'tipo': 'entidad'},
            'diccionario':  {'id': 'ENTIDAD_DICT',      'grounding': 0.9, 'tipo': 'entidad'},
            'base':         {'id': 'ENTIDAD_BASE',      'grounding': 0.7, 'tipo': 'entidad'},
            'datos':        {'id': 'ENTIDAD_DATOS',     'grounding': 0.9, 'tipo': 'entidad'},
            'proyecto':     {'id': 'ENTIDAD_PROYECTO',  'grounding': 1.0, 'tipo': 'entidad'},
            'sistema':      {'id': 'ENTIDAD_SISTEMA',   'grounding': 0.9, 'tipo': 'entidad'},
            'servidor':     {'id': 'ENTIDAD_SERVIDOR',  'grounding': 0.9, 'tipo': 'entidad'},
            'api':          {'id': 'ENTIDAD_API',       'grounding': 1.0, 'tipo': 'entidad'},
            'modelo':       {'id': 'ENTIDAD_MODELO',    'grounding': 0.9, 'tipo': 'entidad'},

            # ── Términos específicos de Bell ─────────────
            'capa':         {'id': 'BELL_CAPA',         'grounding': 1.0, 'tipo': 'bell_tech'},
            'capas':        {'id': 'BELL_CAPA',         'grounding': 1.0, 'tipo': 'bell_tech'},
            'motor':        {'id': 'BELL_MOTOR',        'grounding': 1.0, 'tipo': 'bell_tech'},
            'habilidad':    {'id': 'BELL_HABILIDAD',    'grounding': 1.0, 'tipo': 'bell_tech'},
            'habilidades':  {'id': 'BELL_HABILIDAD',    'grounding': 1.0, 'tipo': 'bell_tech'},
            'consejera':    {'id': 'BELL_CONSEJERA',    'grounding': 1.0, 'tipo': 'bell_tech'},
            'consejeras':   {'id': 'BELL_CONSEJERA',    'grounding': 1.0, 'tipo': 'bell_tech'},
            'memoria':      {'id': 'BELL_MEMORIA',      'grounding': 1.0, 'tipo': 'bell_tech'},
            'grounding':    {'id': 'BELL_GROUNDING',    'grounding': 1.0, 'tipo': 'bell_tech'},
            'pipeline':     {'id': 'BELL_PIPELINE',     'grounding': 1.0, 'tipo': 'bell_tech'},
            'nodo':         {'id': 'BELL_NODO',         'grounding': 1.0, 'tipo': 'bell_tech'},
            'nodos':        {'id': 'BELL_NODO',         'grounding': 1.0, 'tipo': 'bell_tech'},
            'vitalidad':    {'id': 'BELL_VITALIDAD',    'grounding': 1.0, 'tipo': 'bell_tech'},
            'sage':         {'id': 'CONSEJERA_SAGE',    'grounding': 1.0, 'tipo': 'consejera'},
            'vega':         {'id': 'CONSEJERA_VEGA',    'grounding': 1.0, 'tipo': 'consejera'},
            'lyra':         {'id': 'CONSEJERA_LYRA',    'grounding': 1.0, 'tipo': 'consejera'},
            'echo':         {'id': 'CONSEJERA_ECHO',    'grounding': 1.0, 'tipo': 'consejera'},
            'nova':         {'id': 'CONSEJERA_NOVA',    'grounding': 1.0, 'tipo': 'consejera'},
            'luna':         {'id': 'CONSEJERA_LUNA',    'grounding': 1.0, 'tipo': 'consejera'},
            'iris':         {'id': 'CONSEJERA_IRIS',    'grounding': 1.0, 'tipo': 'consejera'},
            'soma':         {'id': 'CONSEJERA_SOMA',    'grounding': 1.0, 'tipo': 'consejera'},

            # ── Emociones y estados ──────────────────────
            'bien':         {'id': 'ESTADO_BIEN',       'grounding': 0.9, 'tipo': 'estado'},
            'mal':          {'id': 'ESTADO_MAL',        'grounding': 0.9, 'tipo': 'estado'},
            'cansado':      {'id': 'ESTADO_CANSADO',    'grounding': 0.9, 'tipo': 'estado'},
            'feliz':        {'id': 'ESTADO_FELIZ',      'grounding': 0.9, 'tipo': 'estado'},
            'triste':       {'id': 'ESTADO_TRISTE',     'grounding': 0.9, 'tipo': 'estado'},
            'frustrado':    {'id': 'ESTADO_FRUSTRADO',  'grounding': 0.9, 'tipo': 'estado'},
            'emocionado':   {'id': 'ESTADO_EMOCIONADO', 'grounding': 0.9, 'tipo': 'estado'},
            'preocupado':   {'id': 'ESTADO_PREOCUPADO', 'grounding': 0.9, 'tipo': 'estado'},
            'tranquilo':    {'id': 'ESTADO_TRANQUILO',  'grounding': 0.9, 'tipo': 'estado'},
            'aburrido':     {'id': 'ESTADO_ABURRIDO',   'grounding': 0.9, 'tipo': 'estado'},

            # ── Colombianismos ───────────────────────────
            'parcero':      {'id': 'COLOQUIAL_PARCERO', 'grounding': 1.0, 'tipo': 'coloquial'},
            'parce':        {'id': 'COLOQUIAL_PARCERO', 'grounding': 1.0, 'tipo': 'coloquial'},
            'chimba':       {'id': 'COLOQUIAL_CHIMBA',  'grounding': 1.0, 'tipo': 'coloquial'},
            'bacano':       {'id': 'COLOQUIAL_BACANO',  'grounding': 1.0, 'tipo': 'coloquial'},
            'berraco':      {'id': 'COLOQUIAL_BERRACO', 'grounding': 1.0, 'tipo': 'coloquial'},
            'juepucha':     {'id': 'COLOQUIAL_EXPR',    'grounding': 0.9, 'tipo': 'coloquial'},
            'uff':          {'id': 'COLOQUIAL_UFF',     'grounding': 0.9, 'tipo': 'coloquial'},
            'uy':           {'id': 'COLOQUIAL_UY',      'grounding': 0.8, 'tipo': 'coloquial'},
            'pues':         {'id': 'COLOQUIAL_PUES',    'grounding': 0.8, 'tipo': 'coloquial'},
            'entonces':     {'id': 'COLOQUIAL_ENT',     'grounding': 0.7, 'tipo': 'coloquial'},

            # ── Términos frecuentes sin vocab ────────────
            'favorito':     {'id': 'CONCEPTO_FAVORITO', 'grounding': 0.8, 'tipo': 'concepto'},
            'favorita':     {'id': 'CONCEPTO_FAVORITO', 'grounding': 0.8, 'tipo': 'concepto'},
            'fyi':          {'id': 'CONCEPTO_FYI',      'grounding': 1.0, 'tipo': 'concepto'},
            'nombre':       {'id': 'CONCEPTO_NOMBRE',   'grounding': 0.9, 'tipo': 'concepto'},
            'color':        {'id': 'CONCEPTO_COLOR',    'grounding': 0.9, 'tipo': 'concepto'},
            'tiempo':       {'id': 'CONCEPTO_TIEMPO',   'grounding': 0.8, 'tipo': 'concepto'},
            'idea':         {'id': 'CONCEPTO_IDEA',     'grounding': 0.9, 'tipo': 'concepto'},
            'plan':         {'id': 'CONCEPTO_PLAN',     'grounding': 0.9, 'tipo': 'concepto'},
            'problema':     {'id': 'CONCEPTO_PROBLEMA', 'grounding': 0.9, 'tipo': 'concepto'},
            'solución':     {'id': 'CONCEPTO_SOLUCION', 'grounding': 0.9, 'tipo': 'concepto'},
            'solucion':     {'id': 'CONCEPTO_SOLUCION', 'grounding': 0.9, 'tipo': 'concepto'},
            'pregunta':     {'id': 'CONCEPTO_PREGUNTA', 'grounding': 0.9, 'tipo': 'concepto'},
            'respuesta':    {'id': 'CONCEPTO_RESPUESTA','grounding': 0.9, 'tipo': 'concepto'},
            'resultado':    {'id': 'CONCEPTO_RESULTADO','grounding': 0.9, 'tipo': 'concepto'},
            'información':  {'id': 'CONCEPTO_INFO',     'grounding': 0.8, 'tipo': 'concepto'},
            'informacion':  {'id': 'CONCEPTO_INFO',     'grounding': 0.8, 'tipo': 'concepto'},
            'ejemplo':      {'id': 'CONCEPTO_EJEMPLO',  'grounding': 0.9, 'tipo': 'concepto'},
            'diferencia':   {'id': 'CONCEPTO_DIFF',     'grounding': 0.8, 'tipo': 'concepto'},
            'cambio':       {'id': 'CONCEPTO_CAMBIO',   'grounding': 0.8, 'tipo': 'concepto'},
            'versión':      {'id': 'CONCEPTO_VERSION',  'grounding': 0.9, 'tipo': 'concepto'},
            'version':      {'id': 'CONCEPTO_VERSION',  'grounding': 0.9, 'tipo': 'concepto'},
        }
        return base.get(token.lower())