# biblioteca/habilidades/lenguaje/motor.py v3
# ================================================
# MOTOR DE COMPRENSIÓN PROFUNDA — v3 MÁXIMO
#
# Expansión masiva de cobertura:
# — Más emociones y matices (nervioso, orgulloso,
#   aburrido, solitario, esperanzado, culpable...)
# — Más tipos: peticion_consejo, logro_compartido,
#   queja, preocupacion, humor, reflexion_compartida
# — Colombianismos y lenguaje informal
# — Mejor detección de contexto y continuación
# — Detección de ironía y humor
# — Detección de múltiples emociones simultáneas
# — Reglas más finas para estados subyacentes
# ================================================

import re
from typing import List, Optional
from biblioteca.habilidades.lenguaje.dimensiones.base import (
    DimensionLenguaje, ResultadoDimension
)

_IDS_RED_SIEMPRE_ACTIVOS = {
    'BELL_NOMBRE_BELL', 'BELL_NOMBRE_BELLADONNA',
    'BELL_NOMBRE_COMPLETO', 'BELL_NOMBRE_CORTO',
    'BELL_CONSCIENCIA', 'BELL_CORE',
}

_TIPOS_PRIORIDAD_ALTA = {
    'saludo', 'despedida', 'gratitud',
    'expresion_emocional_negativa', 'expresion_emocional_positiva',
    'solicitud_accion', 'solicitud_tecnica',
    'pregunta_estado_bell', 'pregunta_capacidad_bell',
    'confirmacion', 'negacion', 'queja',
    'logro_compartido', 'peticion_consejo',
}


class ResultadoMotor:

    def __init__(self):
        self.texto_original:      str   = ''
        self.intencion:           str   = ''
        self.accion_principal:    str   = ''
        self.objetos:             list  = []
        self.emocion_detectada:   str   = 'neutra'
        self.intensidad:          float = 0.0
        self.tono_base:           str   = 'neutral'
        self.necesidad_real:      str   = ''
        self.id_lyra:             str   = ''
        self.ids_activos:         list  = []
        self.dominio_tecnico:     str   = ''
        self.habilidad_requerida: str   = ''
        self.nivel_tecnicismo:    str   = 'coloquial'
        self.parametros_tecnicos: dict  = {}
        self.tipo_mensaje:        str   = 'conversacional'
        self.nombre_usuario:      str   = 'Sebastian'
        self.es_continuacion:     bool  = False
        self.es_correccion:       bool  = False
        self.referencias_previas: list  = []
        self.estado_subyacente:   str   = ''
        self.lectura_intrinseca:  str   = ''
        self.nivel_energia:       str   = 'normal'
        self.modo_mental:         str   = 'receptivo'
        self.confianza_global:    float = 0.0
        self.dimensiones_activas: list  = []
        self.conceptos_bell:      list  = []
        self.comprension:         dict  = {}
        self.tiene_humor:         bool  = False
        self.tiene_ironia:        bool  = False

    def a_dict(self) -> dict:
        return {
            'texto_original':      self.texto_original,
            'intencion':           self.intencion,
            'accion_principal':    self.accion_principal,
            'objetos':             self.objetos,
            'emocion_detectada':   self.emocion_detectada,
            'intensidad':          self.intensidad,
            'tono_base':           self.tono_base,
            'necesidad_real':      self.necesidad_real,
            'id_lyra':             self.id_lyra,
            'ids_activos':         self.ids_activos,
            'dominio_tecnico':     self.dominio_tecnico,
            'habilidad_requerida': self.habilidad_requerida,
            'nivel_tecnicismo':    self.nivel_tecnicismo,
            'parametros_tecnicos': self.parametros_tecnicos,
            'tipo_mensaje':        self.tipo_mensaje,
            'nombre_usuario':      self.nombre_usuario,
            'es_continuacion':     self.es_continuacion,
            'es_correccion':       self.es_correccion,
            'estado_subyacente':   self.estado_subyacente,
            'nivel_energia':       self.nivel_energia,
            'modo_mental':         self.modo_mental,
            'confianza_global':    self.confianza_global,
            'dimensiones_activas': self.dimensiones_activas,
            'tiene_humor':         self.tiene_humor,
            'tiene_ironia':        self.tiene_ironia,
        }


# ── Emociones expandidas con matices ─────────────────────
_EMOCIONES_DIRECTAS = {
    # Negativas básicas
    'frustracion':   ['frustrado','frustrada','harto','harta','desesperado','hastiado',
                      'estoy hasta','no aguanto','no puedo más','ya no más','para qué',
                      'todo mal','nada funciona','qué caos','me tiene loco','me tiene loca'],
    'cansancio':     ['cansado','cansada','agotado','agotada','exhausto','exhausta',
                      'sin energía','no doy más','reventado','estoy muerto','sin fuerzas',
                      'estoy frito','rendido','rendida','no puedo más del cansancio'],
    'ansiedad':      ['ansioso','ansiosa','nervioso','nerviosa','preocupado','preocupada',
                      'angustiado','con miedo','no sé si','y si falla','qué pasa si',
                      'me da miedo','estoy tenso','estoy tensa','me preocupa'],
    'tristeza':      ['triste','mal','no estoy bien','todo sale mal','es muy duro',
                      'qué difícil','me siento solo','me siento sola','solo','sola',
                      'nadie','no tengo','sin ganas'],
    'confusion':     ['confundido','confundida','perdido','perdida','no entiendo',
                      'no me queda claro','qué significa','no sé cómo','no lo capto',
                      'no le entiendo','cómo funciona','me explicas'],
    'rabia':         ['rabioso','enojado','bravo','molesto','furioso','me da rabia',
                      'qué rabia','me molesta','no soporto','odio','me carga',
                      'me tiene mamado','mamado','mamada'],
    'soledad':       ['solo','sola','soledad','nadie me','sin nadie','me siento solo',
                      'no tengo con quién','me siento sola'],
    'culpa':         ['me siento culpable','es mi culpa','la cagué','la cague',
                      'metí la pata','meti la pata','me equivoqué','cometí un error'],
    'verguenza':     ['vergüenza','pena','me da pena','qué pena','qué vergüenza',
                      'qué ridículo','ridícula','ridículo'],
    # Positivas
    'entusiasmo':    ['emocionado','emocionada','entusiasmado','qué bueno','genial',
                      'increíble','increible','excelente','me encanta','me gusta mucho',
                      'buenísimo','perfecto','fantástico','qué bien','por fin','funcionó',
                      'funciono','épico','bacano','chévere','de una'],
    'orgullo':       ['orgulloso','orgullosa','lo logré','lo logramos','lo logre',
                      'lo hice','terminé','termine','por fin lo','conseguí','consegui'],
    'gratitud':      ['gracias','muchas gracias','te lo agradezco','qué buen','muy amable',
                      'se lo agradezco','me alegra','me ayudaste'],
    'esperanza':     ['ojalá','espero que','ojalá que','ojalá resulte','ojalá funcione',
                      'a ver si','quizás','tal vez funcione'],
    'determinacion': ['quiero','necesito','voy a','tengo que','hay que','debo',
                      'es urgente','sin falta','obligatorio','lo voy a hacer',
                      'vamos','hagamos','de una vez'],
    'alivio':        ['por fin','qué alivio','ya terminó','ya termino','se resolvió',
                      'funcionó al fin','menos mal','uff que bien'],
    # Colombianismos emocionales
    'parcero':       ['parcero','parce','llave','marica','mane','gonorrea',  # contexto neutro/positivo
                      'hermano','man','chino','cucho'],
}

# Palabras de humor / ironía
_INDICADORES_HUMOR = [
    'jaja','jeje','xd','xdd','😂','🤣','haha','lol','ja ja','je je',
    'es broma','mentira','mentirillas','en serio no','nah',
]
_INDICADORES_IRONIA = [
    'sí claro','claro que sí','obvio','por supuesto','qué original',
    'qué sorpresa','no me digas','imagínate','cómo no',
]


class MotorComprension:

    _instancia: Optional['MotorComprension'] = None

    def __init__(self):
        self._dimensiones: List[DimensionLenguaje] = []
        self._cargar_dimensiones()

    @classmethod
    def obtener(cls) -> 'MotorComprension':
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def _cargar_dimensiones(self):
        from biblioteca.habilidades.lenguaje.dimensiones import (
            DimensionLiteral, DimensionInferencial,
            DimensionPsicologica, DimensionTecnica,
            DimensionContextual, DimensionIntrinseca,
        )
        for clase in [
            DimensionLiteral, DimensionTecnica,
            DimensionInferencial, DimensionPsicologica,
            DimensionContextual, DimensionIntrinseca,
        ]:
            try:
                self._dimensiones.append(clase())
            except Exception as e:
                print(f'  Motor: error cargando {clase.__name__}: {e}')

    def comprender(self, texto: str, contexto: dict) -> ResultadoMotor:
        resultado                = ResultadoMotor()
        resultado.texto_original = texto
        resultado.nombre_usuario = contexto.get('nombre_usuario', 'Sebastian')

        ids_raw = list(contexto.get('ids_activos', []))
        resultado.ids_activos = [
            i for i in ids_raw
            if i not in _IDS_RED_SIEMPRE_ACTIVOS
        ]
        resultado.conceptos_bell = contexto.get('conceptos_red', [])

        ctx = dict(contexto)
        ctx['ids_conocidos'] = resultado.ids_activos
        ctx['vocab_tipos'] = {
            m.get('concepto', {}).get('id', ''): m.get('concepto', {}).get('tipo', '')
            for m in contexto.get('vocab_match', [])
            if m.get('concepto', {}).get('id')
        }

        resultados_dim = []
        for dim in self._dimensiones:
            try:
                rd = dim.analizar(texto, ctx)
                resultados_dim.append(rd)
                if rd.activa:
                    resultado.dimensiones_activas.append(dim.NOMBRE)
            except Exception as e:
                print(f'  Motor: fallo en {dim.NOMBRE}: {e}')

        # Detección directa de emoción desde texto (antes de sintetizar)
        self._detectar_emociones_directas(resultado, texto)
        self._detectar_humor_ironia(resultado, texto)

        self._sintetizar(resultado, resultados_dim, ctx)
        resultado.confianza_global = self._calcular_confianza(resultados_dim)

        return resultado

    def _detectar_emociones_directas(self, r: ResultadoMotor, texto: str):
        """
        Detección directa de emociones desde texto completo.
        Independiente de las dimensiones — es una capa extra de seguridad.
        """
        tl = texto.lower()
        mejor_emocion  = None
        mejor_intensidad = 0.0

        intensidades = {
            'frustracion':   0.82,
            'cansancio':     0.77,
            'ansiedad':      0.72,
            'tristeza':      0.70,
            'rabia':         0.85,
            'soledad':       0.75,
            'culpa':         0.68,
            'verguenza':     0.60,
            'entusiasmo':    0.68,
            'orgullo':       0.72,
            'gratitud':      0.65,
            'esperanza':     0.55,
            'determinacion': 0.62,
            'alivio':        0.65,
        }

        for emocion, palabras in _EMOCIONES_DIRECTAS.items():
            if emocion == 'parcero':
                continue  # Colombianismos no son emociones
            for palabra in palabras:
                if palabra in tl:
                    intensidad = intensidades.get(emocion, 0.6)
                    if intensidad > mejor_intensidad:
                        mejor_emocion    = emocion
                        mejor_intensidad = intensidad
                    break

        if mejor_emocion and (not r.emocion_detectada or r.emocion_detectada == 'neutra'):
            r.emocion_detectada = mejor_emocion
            r.intensidad        = mejor_intensidad

            negativas = {'frustracion','cansancio','ansiedad','tristeza','rabia','soledad','culpa','verguenza'}
            positivas = {'entusiasmo','orgullo','gratitud','esperanza','determinacion','alivio'}

            if mejor_emocion in negativas:
                r.tono_base = 'emocional_negativo'
                if r.tipo_mensaje == 'conversacional':
                    r.tipo_mensaje = 'expresion_emocional_negativa'
            elif mejor_emocion in positivas:
                r.tono_base = 'emocional_positivo'
                if mejor_emocion == 'orgullo':
                    r.tipo_mensaje = 'logro_compartido'
                elif r.tipo_mensaje == 'conversacional':
                    r.tipo_mensaje = 'expresion_emocional_positiva'

    def _detectar_humor_ironia(self, r: ResultadoMotor, texto: str):
        tl = texto.lower()
        if any(h in tl for h in _INDICADORES_HUMOR):
            r.tiene_humor = True
        if any(i in tl for i in _INDICADORES_IRONIA):
            r.tiene_ironia = True

    def _sintetizar(self, r: ResultadoMotor, resultados: list, ctx: dict):
        mapa = {rd.dimension: rd for rd in resultados}

        lit = mapa.get('literal')
        if lit and lit.activa:
            h = lit.hallazgos
            r.accion_principal = h.get('accion_principal', '')
            r.objetos          = h.get('objetos', [])
            tipo_or = h.get('tipo_oracion', 'declaracion')
            if tipo_or == 'pregunta':
                if r.tipo_mensaje == 'conversacional':
                    r.tipo_mensaje = 'pregunta'
            elif tipo_or == 'orden':
                if r.tipo_mensaje == 'conversacional':
                    r.tipo_mensaje = 'solicitud_accion'

        tec = mapa.get('tecnica')
        if tec and tec.activa:
            h = tec.hallazgos
            r.dominio_tecnico     = h.get('dominio_tecnico', '')
            r.habilidad_requerida = h.get('habilidad_requerida', '')
            r.nivel_tecnicismo    = h.get('nivel_tecnicismo', 'coloquial')
            r.parametros_tecnicos = h.get('parametros_extraidos', {})
            if r.dominio_tecnico:
                r.tipo_mensaje = 'solicitud_tecnica'

        inf = mapa.get('inferencial')
        if inf and inf.activa:
            h = inf.hallazgos
            if h.get('es_pedido_disfrazado'):
                impl = h.get('implicatura', '')
                if impl:
                    r.intencion = impl
                if r.tipo_mensaje == 'pregunta':
                    r.tipo_mensaje = 'solicitud_accion'

        psi = mapa.get('psicologica')
        if psi and psi.activa:
            h = psi.hallazgos
            emocion_psi = h.get('emocion_detectada', 'neutra')
            if emocion_psi and emocion_psi != 'neutra' and r.emocion_detectada == 'neutra':
                r.emocion_detectada = emocion_psi
                r.intensidad        = h.get('intensidad_emocional', 0.0)
            r.tono_base    = h.get('tono_base', r.tono_base or 'neutral')
            r.necesidad_real = h.get('necesidad_real', '')
            id_lyra = h.get('id_lyra', '')
            r.id_lyra = id_lyra
            if id_lyra and id_lyra not in r.ids_activos:
                r.ids_activos.append(id_lyra)
            emocion = r.emocion_detectada
            if emocion in ('tristeza', 'frustracion', 'ansiedad', 'cansancio',
                           'rabia', 'soledad', 'culpa', 'verguenza'):
                if r.tipo_mensaje == 'conversacional':
                    r.tipo_mensaje = 'expresion_emocional_negativa'
            elif emocion in ('entusiasmo', 'gratitud', 'orgullo', 'alivio'):
                if r.tipo_mensaje == 'conversacional':
                    if emocion == 'orgullo':
                        r.tipo_mensaje = 'logro_compartido'
                    else:
                        r.tipo_mensaje = 'expresion_emocional_positiva'

        ctxd = mapa.get('contextual')
        if ctxd and ctxd.activa:
            h = ctxd.hallazgos
            r.nombre_usuario      = h.get('nombre_usuario', 'Sebastian')
            r.es_continuacion     = bool(h.get('es_continuacion'))
            r.es_correccion       = h.get('es_correccion', False)
            r.referencias_previas = h.get('referencias_previas', [])
            tipo_ctx = h.get('tipo_mensaje', '')
            if tipo_ctx and r.tipo_mensaje == 'conversacional':
                r.tipo_mensaje = tipo_ctx

        intr = mapa.get('intrinseca')
        if intr and intr.activa:
            h = intr.hallazgos
            r.estado_subyacente  = h.get('estado_subyacente', '')
            r.lectura_intrinseca = h.get('lectura_intrinseca', '')
            r.nivel_energia      = h.get('nivel_energia', 'normal')
            r.modo_mental        = h.get('modo_mental', 'receptivo')

        self._afinar_con_ids_bell(r, ctx)
        self._afinar_con_texto_completo(r)

        if not r.intencion:
            r.intencion = self._inferir_intencion(r)

    def _afinar_con_ids_bell(self, r: ResultadoMotor, ctx: dict):
        """
        Reglas de clasificación expandidas v3.
        Cubre ~90% del lenguaje natural.
        """
        ids  = set(r.ids_activos)
        tl   = r.texto_original.lower().strip()

        # Tipos prioritarios — no reclasificar
        if r.tipo_mensaje in _TIPOS_PRIORIDAD_ALTA:
            emociones_red = {i for i in ids if i.startswith('EMOCION_')}
            if emociones_red and not r.id_lyra:
                r.id_lyra = next(iter(emociones_red))
            return

        ids_preg = {i for i in ids if i.startswith('PREG_')}

        # ── Emociones en vocabulario ──────────────────────────
        ids_emocion = {i for i in ids if i.startswith('EMOCION_')}
        if ids_emocion:
            emocion_id = next(iter(ids_emocion))
            r.id_lyra = emocion_id
            if not r.emocion_detectada or r.emocion_detectada == 'neutra':
                negativas = {
                    'EMOCION_MAL','EMOCION_TRISTE','EMOCION_FRUSTRADO',
                    'EMOCION_CANSADO','EMOCION_AGOTADO','EMOCION_ESTRESADO',
                    'EMOCION_PREOCUPADO','EMOCION_ASUSTADO','EMOCION_ENOJADO',
                    'EMOCION_CONFUNDIDO','EMOCION_PERDIDO','EMOCION_NERVIOSO',
                    'EMOCION_ABURRIDO','EMOCION_MOLESTO','EMOCION_SOLO',
                    'EMOCION_CULPA','EMOCION_VERGUENZA',
                }
                positivas = {
                    'EMOCION_BIEN','EMOCION_GENIAL','EMOCION_FELIZ',
                    'EMOCION_CONTENTO','EMOCION_ALEGRE','EMOCION_MOTIVADO',
                    'EMOCION_EMOCIONADO','EMOCION_EXCELENTE','EMOCION_PERFECTO',
                    'EMOCION_ORGULLOSO','EMOCION_ALIVIADO',
                }
                if ids_emocion & negativas and r.tipo_mensaje == 'conversacional':
                    r.tipo_mensaje = 'expresion_emocional_negativa'
                elif ids_emocion & positivas and r.tipo_mensaje == 'conversacional':
                    r.tipo_mensaje = 'expresion_emocional_positiva'

        # ── Preguntas directas sobre Bell ─────────────────────
        ids_preg_bell_directa = {
            'PREG_CONSEJERAS_BELL', 'PREG_CAPAS_BELL', 'PREG_VALORES_BELL',
            'PREG_NODOS_BELL', 'PREG_CUANTAS_CONSEJERAS',
            'PREG_NOMBRE_BELL', 'PREG_QUIEN_ES_BELL', 'PREG_QUE_ES_BELL',
        }
        if ids & ids_preg_bell_directa:
            r.tipo_mensaje = 'pregunta_identidad_bell'
            r.intencion    = 'conocer_bell'
            return

        # ── Componentes Bell + pregunta ───────────────────────
        ids_componentes_bell = {
            'BELL_CONSEJERAS','BELL_CONSEJERA','BELL_CAPAS','BELL_CAPA',
            'BELL_SOMA','BELL_VEGA','BELL_NOVA','BELL_ECHO',
            'BELL_LYRA','BELL_LUNA','BELL_IRIS','BELL_SAGE',
            'BELL_VALORES','BELL_PRINCIPIOS','BELL_GROUNDING',
            'BELL_BIBLIOTECA','BELL_VOCABULARIO',
        }
        if ids & ids_componentes_bell and ids_preg:
            r.tipo_mensaje = 'pregunta_identidad_bell'
            r.intencion    = 'conocer_bell'
            return

        # ── "quien eres" / "qué eres" ─────────────────────────
        if ids & {'PREG_QUIEN','PREG_QUE'} and 'VERBO_SER_TU' in ids:
            r.tipo_mensaje = 'pregunta_identidad_bell'
            r.intencion    = 'conocer_bell'
            return

        # ── "quiénes son" + componente Bell ───────────────────
        if 'PREG_QUIENES' in ids and ids & ids_componentes_bell:
            r.tipo_mensaje = 'pregunta_identidad_bell'
            r.intencion    = 'conocer_bell'
            return

        # ── "cómo estás" ──────────────────────────────────────
        if 'PREG_COMO' in ids and ids & {'VERBO_ESTAR_TU','VERBO_ESTAR_EL'}:
            r.tipo_mensaje = 'pregunta_estado_bell'
            return

        # ── Presente continuo → estado Bell ───────────────────
        if 'PREG_QUE' in ids and 'VERBO_ESTAR_TU' in ids and (
            'GERUNDIO_HACER' in ids or 'GERUNDIO_PROCESAR' in ids or
            'GERUNDIO_APRENDER' in ids or 'EXPR_PRESENTE_CONTINUO' in ids
        ):
            r.tipo_mensaje = 'pregunta_estado_bell'
            return

        # ── Capacidades de Bell ───────────────────────────────
        if ids_preg and 'VERBO_PODER_TU' in ids:
            r.tipo_mensaje = 'pregunta_capacidad_bell'
            return

        if ids_preg and 'VERBO_SABER_TU' in ids and (
            'VERBO_HACER' in ids or 'VERBO_HACER_TU' in ids
        ):
            r.tipo_mensaje = 'pregunta_capacidad_bell'
            return

        # ── Estado de Bell por vocabulario ────────────────────
        if ids_preg and ids & {'BELL_VOCABULARIO','BELL_NODOS','BELL_RED_NEURONAL','BELL_CAPAS'}:
            r.tipo_mensaje = 'pregunta_estado_bell'
            return

        # ── Qué hace Bell ─────────────────────────────────────
        if ids_preg and ids & {'VERBO_HACER_TU','VERBO_HACER_EL','VERBO_HACER'}:
            if r.tipo_mensaje in ('pregunta', 'conversacional'):
                r.tipo_mensaje = 'pregunta_accion_bell'
            return

        # ── Preguntas filosóficas ─────────────────────────────
        if 'PREG_QUIEN' in ids and 'VERBO_SER_YO' in ids:
            r.tipo_mensaje = 'pregunta_filosofica'
            r.intencion    = 'reflexion_identidad'
            return

        if 'PREG_PARA_QUE' in ids and (
            'VERBO_EXISTIR_YO' in ids or 'VERBO_ESTAR_YO' in ids or
            'VERBO_VIVIR_YO' in ids
        ):
            r.tipo_mensaje = 'pregunta_filosofica'
            r.intencion    = 'reflexion_proposito'
            return

        # ── Datos personales ──────────────────────────────────
        if ids & {'DATO_EDAD','DATO_EDAD_UNIDAD','DATO_ORIGEN',
                  'DATO_UBICACION','DATO_TRABAJO','DATO_ESTUDIO'}:
            r.tipo_mensaje = 'dato_personal'
            r.intencion    = 'compartir_informacion'
            return

        if 'DATO_EDAD_UNIDAD' in ids or (
            'VERBO_TENER_YO' in ids and self._tiene_numero(tl)
        ):
            r.tipo_mensaje = 'dato_personal'
            r.intencion    = 'compartir_informacion'
            return

        # ── Correcciones ──────────────────────────────────────
        if ids & {'EXPR_NEGACION_DIRECTA'} or (
            'NEGACION' in ids and ids & {'VERBO_SER_EL','VERBO_SER_YO'} and
            r.tipo_mensaje in ('conversacional', 'pregunta')
        ):
            if not r.es_correccion:
                r.es_correccion = True
            r.tipo_mensaje = 'correccion'
            r.intencion    = 'corregir'
            return

        # ── Continuaciones ────────────────────────────────────
        if ids & {'EXPR_CONTINUA','EXPR_SIGUIENTE'} and r.es_continuacion:
            r.tipo_mensaje = 'solicitud_continuacion'
            r.intencion    = 'continuar'
            return

        # ── Presentación Sebastian ────────────────────────────
        if 'NEURONA_SEBASTIAN' in ids and r.tipo_mensaje == 'conversacional':
            r.tipo_mensaje = 'presentacion_sebastian'
            return

        # ── Saludos ───────────────────────────────────────────
        saludos_red = {i for i in ids if i.startswith('SALUDO_')}
        if saludos_red and r.tipo_mensaje == 'conversacional':
            r.tipo_mensaje = 'saludo'

        # ── Emociones residuales ──────────────────────────────
        if ids_emocion and not r.id_lyra:
            r.id_lyra = next(iter(ids_emocion))

    def _afinar_con_texto_completo(self, r: ResultadoMotor):
        """
        Segunda pasada de afinamiento usando el texto completo.
        Captura patrones que los IDs de la red no detectan.
        """
        tl = r.texto_original.lower().strip()

        # Petición de consejo
        patrones_consejo = [
            r'qué (?:harías|hago|hago yo|me recomiendas)',
            r'me (?:aconsejas|recomiendas|sugieres)',
            r'cómo (?:lo harías|lo haría)',
            r'qué (?:crees|piensas)',
            r'dame tu (?:opinión|consejo)',
            r'(?:debería|debo)\s+.{3,30}\?',
        ]
        if any(re.search(p, tl) for p in patrones_consejo):
            if r.tipo_mensaje in ('conversacional', 'pregunta'):
                r.tipo_mensaje = 'peticion_consejo'
                r.necesidad_real = 'reflexion'

        # Logro / compartir éxito
        patrones_logro = [
            r'(?:lo |la )?(?:terminé|termine|logré|logre|conseguí|consegui)',
            r'(?:por fin|al fin)\s+(?:lo |la )?(?:hice|terminé|funciona|pude)',
            r'funcionó|funciono',
            r'sale\s+bien',
        ]
        if any(re.search(p, tl) for p in patrones_logro):
            if r.tipo_mensaje in ('conversacional', 'expresion_emocional_positiva'):
                r.tipo_mensaje = 'logro_compartido'
                r.emocion_detectada = 'orgullo'
                r.intensidad = 0.72

        # Queja sin emoción fuerte
        patrones_queja = [
            r'qué (?:fastidio|molestia|lata|pereza)',
            r'(?:siempre|nunca) (?:pasa|funciona|me)',
            r'qué (?:mal|horrible|pésimo)',
            r'no (?:sirve|funciona|resulta)',
        ]
        if any(re.search(p, tl) for p in patrones_queja):
            if r.tipo_mensaje == 'conversacional':
                r.tipo_mensaje = 'queja'
                if not r.emocion_detectada or r.emocion_detectada == 'neutra':
                    r.emocion_detectada = 'frustracion'
                    r.intensidad = 0.55

        # Reflexión compartida
        patrones_reflexion = [
            r'estaba pensando (?:en|que)',
            r'me puse a pensar',
            r'se me ocurrió',
            r'¿no (?:crees|piensas)\s+que',
            r'fíjate que',
            r'mira que',
        ]
        if any(re.search(p, tl) for p in patrones_reflexion):
            if r.tipo_mensaje == 'conversacional':
                r.tipo_mensaje = 'reflexion_compartida'
                r.necesidad_real = 'reflexion'

        # Preguntas con "cómo" que no son sobre Bell
        if tl.startswith('cómo') or tl.startswith('como'):
            if r.tipo_mensaje == 'pregunta' and 'VERBO_ESTAR_TU' not in r.ids_activos:
                r.necesidad_real = 'informacion'

        # Estado de energía muy baja
        baja_energia = ['sin energía', 'sin energia', 'muy cansado', 'muy cansada',
                        'agotado', 'no doy más', 'no puedo más', 'sin fuerzas']
        if any(b in tl for b in baja_energia):
            r.nivel_energia = 'muy_bajo'
        elif any(b in tl for b in ['cansado', 'cansada', 'no puedo']):
            r.nivel_energia = 'bajo'

        # Colombianismos de contexto positivo/neutro
        colombianismos_neutros = ['parce', 'parcero', 'marica', 'llave', 'mane',
                                   'chino', 'cucho', 'bacano', 'chévere', 'de una']
        if any(c in tl for c in colombianismos_neutros):
            # Si hay colombianismos pero no hay emoción fuerte → tono cercano
            if r.emocion_detectada == 'neutra':
                r.tono_base = 'cercano_natural'

    def _tiene_numero(self, texto: str) -> bool:
        return bool(re.search(r'\b\d+\b', texto))

    def _inferir_intencion(self, r: ResultadoMotor) -> str:
        if r.habilidad_requerida:
            return f'ejecutar_{r.habilidad_requerida.lower()}'
        if r.accion_principal:
            return r.accion_principal
        mapa = {
            'solicitud_accion':             'ejecutar_tarea',
            'solicitud_tecnica':            'ejecutar_habilidad_tecnica',
            'pregunta':                     'obtener_informacion',
            'pregunta_identidad_bell':      'conocer_bell',
            'pregunta_estado_bell':         'saber_estado_bell',
            'pregunta_capacidad_bell':      'saber_capacidades_bell',
            'pregunta_accion_bell':         'saber_que_hace_bell',
            'pregunta_filosofica':          'reflexionar',
            'dato_personal':                'compartir_informacion',
            'correccion':                   'corregir',
            'solicitud_continuacion':       'continuar',
            'expresion_emocional_negativa': 'expresar_estado',
            'expresion_emocional_positiva': 'compartir_estado',
            'saludo':                       'conectar',
            'presentacion_sebastian':       'presentarse',
            'peticion_consejo':             'pedir_consejo',
            'logro_compartido':             'compartir_logro',
            'queja':                        'expresar_molestia',
            'reflexion_compartida':         'reflexionar_juntos',
            'conversacional':               'conversar',
        }
        return mapa.get(r.tipo_mensaje, 'conversar')

    def _calcular_confianza(self, resultados: List[ResultadoDimension]) -> float:
        activas = [rd for rd in resultados if rd.activa]
        if not activas:
            return 0.3
        suma_p = sum(rd.confianza * rd.peso_en_motor for rd in activas)
        suma_w = sum(rd.peso_en_motor for rd in activas)
        return round(min(0.97, suma_p / suma_w if suma_w > 0 else 0.3), 3)