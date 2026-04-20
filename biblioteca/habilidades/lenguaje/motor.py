# biblioteca/habilidades/lenguaje/motor.py
# ================================================
# MOTOR DE COMPRENSIÓN PROFUNDA
#
# FIX CRÍTICO — _afinar_con_ids_bell():
# Solo sobreescribe tipo_mensaje a identidad
# si hay señal EXPLÍCITA de pregunta (PREG_*).
# Saludos, emociones y otros tipos con prioridad
# NUNCA son sobreescritos por IDs de Bell.
# ================================================

from typing import List, Optional
from biblioteca.habilidades.lenguaje.dimensiones.base import (
    DimensionLenguaje, ResultadoDimension
)

# IDs que la red siempre tiene activos por propagación.
# No representan el mensaje actual — son nodos base de Bell.
# Se excluyen del contexto que recibe el motor.
_IDS_RED_SIEMPRE_ACTIVOS = {
    'BELL_NOMBRE_BELL', 'BELL_NOMBRE_BELLADONNA',
    'BELL_NOMBRE_COMPLETO', 'BELL_NOMBRE_CORTO',
    'BELL_CONSCIENCIA', 'BELL_CORE',
}

# Tipos que tienen prioridad absoluta.
# Si el mensaje ya fue clasificado como uno de estos,
# _afinar_con_ids_bell NO lo toca.
_TIPOS_PRIORIDAD_ALTA = {
    'saludo',
    'despedida',
    'gratitud',
    'expresion_emocional_negativa',
    'expresion_emocional_positiva',
    'solicitud_accion',
    'solicitud_tecnica',
    'pregunta_estado_bell',
    'pregunta_capacidad_bell',
    'confirmacion',
    'negacion',
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
        }


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

        # Filtrar IDs siempre activos — no representan el mensaje actual
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

        self._sintetizar(resultado, resultados_dim, ctx)
        resultado.confianza_global = self._calcular_confianza(resultados_dim)

        return resultado

    def _sintetizar(self, r: ResultadoMotor, resultados: list, ctx: dict):
        mapa = {rd.dimension: rd for rd in resultados}

        # LITERAL
        lit = mapa.get('literal')
        if lit and lit.activa:
            h = lit.hallazgos
            r.accion_principal = h.get('accion_principal', '')
            r.objetos          = h.get('objetos', [])
            tipo_or = h.get('tipo_oracion', 'declaracion')
            if tipo_or == 'pregunta':
                r.tipo_mensaje = 'pregunta'
            elif tipo_or == 'orden':
                r.tipo_mensaje = 'solicitud_accion'

        # TÉCNICA
        tec = mapa.get('tecnica')
        if tec and tec.activa:
            h = tec.hallazgos
            r.dominio_tecnico     = h.get('dominio_tecnico', '')
            r.habilidad_requerida = h.get('habilidad_requerida', '')
            r.nivel_tecnicismo    = h.get('nivel_tecnicismo', 'coloquial')
            r.parametros_tecnicos = h.get('parametros_extraidos', {})
            if r.dominio_tecnico:
                r.tipo_mensaje = 'solicitud_tecnica'

        # INFERENCIAL
        inf = mapa.get('inferencial')
        if inf and inf.activa:
            h = inf.hallazgos
            if h.get('es_pedido_disfrazado'):
                impl = h.get('implicatura', '')
                if impl:
                    r.intencion = impl
                if r.tipo_mensaje == 'pregunta':
                    r.tipo_mensaje = 'solicitud_accion'

        # PSICOLÓGICA — emoción tiene alta prioridad
        psi = mapa.get('psicologica')
        if psi and psi.activa:
            h = psi.hallazgos
            r.emocion_detectada = h.get('emocion_detectada', 'neutra')
            r.intensidad        = h.get('intensidad_emocional', 0.0)
            r.tono_base         = h.get('tono_base', 'neutral')
            r.necesidad_real    = h.get('necesidad_real', '')
            id_lyra = h.get('id_lyra', '')
            r.id_lyra = id_lyra
            if id_lyra and id_lyra not in r.ids_activos:
                r.ids_activos.append(id_lyra)
            emocion = r.emocion_detectada
            if emocion in ('tristeza', 'frustracion', 'ansiedad', 'cansancio'):
                if r.tipo_mensaje == 'conversacional':
                    r.tipo_mensaje = 'expresion_emocional_negativa'
            elif emocion in ('entusiasmo', 'gratitud'):
                if r.tipo_mensaje == 'conversacional':
                    r.tipo_mensaje = 'expresion_emocional_positiva'

        # CONTEXTUAL
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

        # INTRÍNSECA
        intr = mapa.get('intrinseca')
        if intr and intr.activa:
            h = intr.hallazgos
            r.estado_subyacente  = h.get('estado_subyacente', '')
            r.lectura_intrinseca = h.get('lectura_intrinseca', '')
            r.nivel_energia      = h.get('nivel_energia', 'normal')
            r.modo_mental        = h.get('modo_mental', 'receptivo')

        # Afinar con IDs de Bell — con las reglas correctas
        self._afinar_con_ids_bell(r, ctx)

        if not r.intencion:
            r.intencion = self._inferir_intencion(r)

    def _afinar_con_ids_bell(self, r: ResultadoMotor, ctx: dict):
        """
        Refina tipo_mensaje usando IDs de Bell.

        REGLAS (en orden de prioridad):
        1. Tipos con prioridad alta → no tocar nunca.
        2. Frases compuestas directas sobre Bell → identidad.
        3. Componentes de Bell + pregunta explícita → identidad.
        4. PREG_QUIEN/QUE + VERBO_SER_TU → identidad ("quien eres").
        5. PREG_COMO + VERBO_ESTAR_TU → estado Bell ("cómo estás").
        6. Pregunta + VERBO_PODER_TU → capacidad Bell ("qué puedes hacer").
        7. Saludos y emociones solo si tipo sigue siendo conversacional.
        """
        ids = set(r.ids_activos)

        # REGLA 1: tipos con prioridad alta no se tocan
        if r.tipo_mensaje in _TIPOS_PRIORIDAD_ALTA:
            # Solo agregar id_lyra si falta
            emociones_red = {i for i in ids if i.startswith('EMOCION_')}
            if emociones_red and not r.id_lyra:
                r.id_lyra = next(iter(emociones_red))
            return

        # Señal de pregunta explícita en el mensaje actual
        ids_preg_explicita = {i for i in ids if i.startswith('PREG_')}

        # Frases compuestas del vocabulario que son preguntas directas sobre Bell
        ids_preg_bell_directa = {
            'PREG_CONSEJERAS_BELL', 'PREG_CAPAS_BELL', 'PREG_VALORES_BELL',
            'PREG_NODOS_BELL', 'PREG_CUANTAS_CONSEJERAS',
            'PREG_NOMBRE_BELL', 'PREG_QUIEN_ES_BELL', 'PREG_QUE_ES_BELL',
        }

        # REGLA 2a: pregunta directa sobre Bell (frase compuesta del vocabulario)
        if ids & ids_preg_bell_directa:
            r.tipo_mensaje = 'pregunta_identidad_bell'
            if not r.intencion:
                r.intencion = 'conocer_bell'
            return

        # Componentes de Bell — solo activan identidad CON pregunta explícita
        ids_componentes_bell = {
            'BELL_CONSEJERAS', 'BELL_CONSEJERA',
            'BELL_CAPAS', 'BELL_CAPA',
            'BELL_SOMA', 'BELL_VEGA', 'BELL_NOVA', 'BELL_ECHO',
            'BELL_LYRA', 'BELL_LUNA', 'BELL_IRIS', 'BELL_SAGE',
            'BELL_VALORES', 'BELL_PRINCIPIOS',
            'BELL_GROUNDING', 'BELL_BIBLIOTECA', 'BELL_VOCABULARIO',
        }

        # REGLA 2b: componente de Bell + pregunta explícita en el texto
        if ids & ids_componentes_bell and ids_preg_explicita:
            r.tipo_mensaje = 'pregunta_identidad_bell'
            if not r.intencion:
                r.intencion = 'conocer_bell'
            return

        # REGLA 2c: PREG_QUIEN/QUE + VERBO_SER_TU = "quien eres", "qué eres"
        # Cubre el caso donde buscar_frase no encontró la frase compuesta
        # pero sí encontró los IDs individuales
        ids_quien_que = {'PREG_QUIEN', 'PREG_QUE'}
        ids_ser_tu = {'VERBO_SER_TU'}
        if ids & ids_quien_que and ids & ids_ser_tu:
            r.tipo_mensaje = 'pregunta_identidad_bell'
            if not r.intencion:
                r.intencion = 'conocer_bell'
            return

        # REGLA 2d: PREG_COMO + VERBO_ESTAR_TU = "cómo estás"
        ids_estar_tu = {'VERBO_ESTAR_TU', 'VERBO_ESTAR_EL'}
        if 'PREG_COMO' in ids and ids & ids_estar_tu:
            r.tipo_mensaje = 'pregunta_estado_bell'
            return

        # REGLA 2e: nodos de estado de la red + pregunta
        if ('BELL_RED_NEURONAL' in ids or 'BELL_NODOS' in ids) and ids_preg_explicita:
            r.tipo_mensaje = 'pregunta_estado_bell'
            return

        # REGLA 2f: pregunta + VERBO_PODER_TU = "qué/cómo puedes..."
        # Cubre "qué puedes hacer", "qué puedes", "cómo puedes ayudar"
        if ids_preg_explicita and 'VERBO_PODER_TU' in ids:
            r.tipo_mensaje = 'pregunta_capacidad_bell'
            return

        # REGLA 3: Presentación de Sebastian — solo si 'sebastian' apareció en el texto
        if 'NEURONA_SEBASTIAN' in ids and r.tipo_mensaje == 'conversacional':
            vocab_tipos = ctx.get('vocab_tipos', {})
            tipo_sebastian = vocab_tipos.get('NEURONA_SEBASTIAN', '')
            if tipo_sebastian:  # la palabra apareció en el texto (no solo en la red)
                r.tipo_mensaje = 'presentacion_sebastian'
            return

        # REGLA 4: Saludos por IDs de la red — solo si tipo sigue siendo conversacional
        saludos_red = {i for i in ids if i.startswith('SALUDO_')}
        if saludos_red and r.tipo_mensaje == 'conversacional':
            r.tipo_mensaje = 'saludo'

        # REGLA 5: Emociones — solo agregar id_lyra si falta
        emociones_red = {i for i in ids if i.startswith('EMOCION_')}
        if emociones_red and not r.id_lyra:
            r.id_lyra = next(iter(emociones_red))

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
            'expresion_emocional_negativa': 'expresar_estado',
            'expresion_emocional_positiva': 'compartir_estado',
            'saludo':                       'conectar',
            'presentacion_sebastian':       'presentarse',
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