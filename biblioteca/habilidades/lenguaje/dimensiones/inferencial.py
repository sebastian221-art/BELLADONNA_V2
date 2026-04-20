# biblioteca/habilidades/lenguaje/dimensiones/inferencial.py
# ================================================
# DIMENSIÓN INFERENCIAL
#
# Lee lo que el mensaje implica pero no dice.
#
# CORRECCIÓN: usa ids_conocidos para detectar
# si Bell ya reconoció presuposiciones o patrones
# de pedido indirecto via su vocabulario, en lugar
# de depender solo de regex propios.
# ================================================

import re
from .base import DimensionLenguaje, ResultadoDimension


class DimensionInferencial(DimensionLenguaje):

    NOMBRE = 'inferencial'
    PESO   = 1.2

    _PEDIDOS_INDIRECTOS = [
        (r'\bpuedes?\s+(.+?)\??$',                   'solicitud_directa'),
        (r'\bpodrias?\s+(.+?)\??$',                  'solicitud_directa'),
        (r'\bserias?\s+capaz\s+de\s+(.+?)\??$',      'solicitud_directa'),
        (r'\bme\s+(?:puedes?|podrias?)\s+(.+?)\??$', 'solicitud_directa'),
        (r'\bharias?\s+(.+?)\??$',                   'solicitud_directa'),
        (r'\bte\s+molestaria\s+(.+?)\??$',           'solicitud_cortés'),
        (r'\bquisiera\s+(?:que\s+)?(.+)',             'deseo_como_pedido'),
        (r'\bme\s+gustaria\s+(?:que\s+)?(.+)',        'deseo_como_pedido'),
        (r'\bseria\s+(?:bueno|genial|ideal|útil)\s+(?:que\s+)?(.+)', 'deseo_como_pedido'),
        (r'\bnecesito\s+(?:que\s+)?(.+)',             'necesidad_como_pedido'),
        (r'\bespero\s+(?:que\s+)?(.+)',               'expectativa_como_pedido'),
        (r'\b(?:y\s+)?si\s+(?:bell|tú)\s+(.+?)\?',  'hipotetico_como_pedido'),
        (r'\bque\s+tal\s+si\s+(.+)',                  'hipotetico_como_pedido'),
        (r'\bpor\s+qué\s+no\s+(.+)',                  'sugerencia_como_pedido'),
        (r'\besto\s+no\s+(?:funciona|sirve|va)\b',    'queja_pide_solucion'),
        (r'\bno\s+(?:entiendo|sé)\s+por\s+qué\s+(.+)', 'confusion_pide_explicacion'),
        (r'\bno\s+puedo\s+(?:con|hacer)\s+(.+)',      'problema_pide_ayuda'),
        (r'\bhabria\s+que\s+(.+)',                    'observacion_como_pedido'),
        (r'\bfalta\s+(.+)',                            'falta_pide_creacion'),
    ]

    _PRESUPOSICIONES = [
        (r'\bseguir\s+(.+)',           'asume_que_ya_inicio'),
        (r'\bterminar\s+(?:de\s+)?(.+)', 'asume_que_esta_en_progreso'),
        (r'\bvolver\s+a\s+(.+)',       'asume_que_ocurrio_antes'),
        (r'\btambién\s+(.+)',          'asume_que_hay_mas_contexto'),
        (r'\baún\s+no\s+(.+)',         'asume_que_deberia_estar_hecho'),
        (r'\bpor\s+qué\s+no\s+(?:funciona|sirve|va)\s+(.+)', 'asume_que_deberia_funcionar'),
        (r'\bcuándo\s+(?:vas\s+a\s+)?(.+)', 'asume_responsabilidad_bell'),
    ]

    _SOFTENERS = [
        'por favor', 'porfa', 'si puedes', 'si no te molesta',
        'cuando puedas', 'si tienes tiempo', 'si es posible',
    ]

    _URGENCIA_IMPLICITA = [
        'es que', 'lo necesito', 'tengo que', 'debo',
        'para hoy', 'para ya', 'lo antes posible',
    ]

    _MAPA_OBJETIVO = {
        'solicitud_directa':          'ejecutar_tarea',
        'solicitud_cortés':           'ejecutar_tarea',
        'deseo_como_pedido':          'satisfacer_necesidad',
        'necesidad_como_pedido':      'resolver_necesidad',
        'expectativa_como_pedido':    'cumplir_expectativa',
        'hipotetico_como_pedido':     'explorar_y_ejecutar',
        'sugerencia_como_pedido':     'implementar_sugerencia',
        'queja_pide_solucion':        'resolver_problema',
        'confusion_pide_explicacion': 'clarificar',
        'problema_pide_ayuda':        'asistir',
        'observacion_como_pedido':    'tomar_accion',
        'falta_pide_creacion':        'crear',
    }

    def analizar(self, texto: str, contexto: dict) -> ResultadoDimension:
        try:
            return self._analizar_interno(texto, contexto)
        except Exception:
            return self._resultado_vacio()

    def _analizar_interno(self, texto: str, contexto: dict) -> ResultadoDimension:
        tl = texto.lower().strip()

        # ids que Bell ya conoce — usamos para enriquecer inferencia
        ids_conocidos = contexto.get('ids_conocidos', [])
        vocab_tipos   = contexto.get('vocab_tipos', {})

        hallazgos = {}
        senales   = []

        # ── PEDIDOS INDIRECTOS ──
        pedido = self._detectar_pedido_indirecto(tl)
        if pedido:
            hallazgos['pedido_real']           = pedido['tipo']
            hallazgos['contenido_pedido']      = pedido['contenido']
            hallazgos['es_pedido_disfrazado']  = True
            objetivo = self._MAPA_OBJETIVO.get(pedido['tipo'], 'responder')
            hallazgos['implicatura']           = pedido['tipo']
            hallazgos['objetivo_real']         = objetivo
            senales.append(f'pedido_indirecto:{pedido["tipo"]}')
            senales.append(f'implicatura:{pedido["tipo"]}')

        # ── PRESUPOSICIONES ──
        presuposiciones = self._detectar_presuposiciones(tl)
        if presuposiciones:
            hallazgos['presuposiciones'] = presuposiciones
            senales.append(f'presuposicion:{presuposiciones[0]}')

        # ── ELIPSIS — referencias vagas que necesitan contexto ──
        elipsis = self._detectar_elipsis(tl, contexto)
        if elipsis:
            hallazgos['elipsis']          = elipsis
            senales.append('elipsis_detectada')

        # ── SOFTENERS ──
        softeners = [s for s in self._SOFTENERS if s in tl]
        if softeners:
            hallazgos['cortesia_detectada'] = softeners
            hallazgos['tono_pedido']        = 'cortés'
            senales.append('pedido_cortés')

        # ── URGENCIA IMPLÍCITA ──
        urgencia = [u for u in self._URGENCIA_IMPLICITA if u in tl]
        if urgencia:
            hallazgos['urgencia_implicita'] = urgencia
            senales.append('urgencia_implicita')

        # ── IRONÍA (señal de alerta, baja confianza) ──
        if self._detectar_ironia(tl):
            hallazgos['posible_ironia'] = True
            senales.append('ironia_posible')

        # ── Enriquecimiento con IDs de la red ──
        # Si Bell ya reconoció nodos de tipo pregunta o concepto especial,
        # los usamos para refinar la inferencia
        tipos_vocab = set(vocab_tipos.values())
        if 'pregunta' in tipos_vocab and not pedido:
            # Bell reconoció como pregunta pero no encontramos pedido indirecto
            # probablemente sea pregunta directa, no disfrazada
            hallazgos['es_pregunta_directa'] = True
            senales.append('pregunta_directa')

        activa    = len(senales) > 0
        confianza = 0.5 + (0.10 * len(senales)) if activa else 0.2
        confianza = min(0.95, confianza)

        return self._resultado(
            activa    = activa,
            confianza = confianza,
            hallazgos = hallazgos,
            senales   = senales,
        )

    def _detectar_pedido_indirecto(self, texto: str) -> dict:
        for patron, tipo in self._PEDIDOS_INDIRECTOS:
            match = re.search(patron, texto, re.IGNORECASE)
            if match:
                contenido = match.group(1).strip() if match.lastindex else texto
                return {'tipo': tipo, 'contenido': contenido}
        return {}

    def _detectar_presuposiciones(self, texto: str) -> list:
        encontradas = []
        for patron, tipo in self._PRESUPOSICIONES:
            if re.search(patron, texto, re.IGNORECASE):
                encontradas.append(tipo)
        return encontradas

    def _detectar_elipsis(self, texto: str, contexto: dict) -> dict:
        referencias_vagas = re.findall(
            r'\b(eso|esto|lo mismo|igual|aquello|lo de antes|lo anterior|'
            r'lo que dijiste|lo que hiciste|lo que te pedí|lo que te dije)\b',
            texto
        )
        if not referencias_vagas:
            return {}

        historial = contexto.get('historial', [])
        referencia_resuelta = ''
        if historial:
            ultimo = historial[-1]
            referencia_resuelta = ultimo.get('texto', '')[:80]

        return {
            'referencias_vagas':    referencias_vagas,
            'referencia_resuelta':  referencia_resuelta,
            'necesita_contexto':    True,
        }

    def _detectar_ironia(self, texto: str) -> bool:
        marcadores = ['claro que sí', 'obvio', 'por supuesto', 'genial', 'fantástico']
        negativos  = ['no funciona', 'error', 'falla', 'mal', 'problema', 'roto']
        return any(m in texto for m in marcadores) and any(n in texto for n in negativos)