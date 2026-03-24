# capas/capa3/constructor_comprension.py
# ================================================
# CONSTRUCTOR DE COMPRENSIÓN — versión 4
# Ahora usa grounding 9D para comprensión genuina
# ================================================

from typing import Dict, Any


class ConstructorComprension:

    def construir(
        self,
        red_activa: dict,
        texto_original: str,
        contexto: dict,
        tono: str
    ) -> dict:

        primarios   = red_activa.get('nodos_primarios',   [])
        secundarios = red_activa.get('nodos_secundarios', [])
        terciarios  = red_activa.get('nodos_terciarios',  [])
        todos       = primarios + secundarios + terciarios

        ids_activos   = {n.get('nodo_id', '') for n in todos}
        ids_primarios = {n.get('nodo_id', '') for n in primarios}

        return {
            'literal':    self._comprension_literal(
                primarios, texto_original
            ),
            'contextual': self._comprension_contextual(
                ids_activos, ids_primarios, contexto, texto_original
            ),
            'profunda':   self._comprension_profunda(
                ids_activos, ids_primarios, contexto, tono,
                texto_original
            )
        }

    def _comprension_literal(self, primarios, texto):
        if not primarios:
            return {
                'nodos_directos':  [],
                'certeza':         0.0,
                'tiene_contenido': False,
                'texto_limpio':    texto
            }
        nodos   = [
            {
                'nodo_id': n.get('nodo_id', ''),
                'energia': n.get('energia', 0)
            }
            for n in primarios
        ]
        certeza = sum(n['energia'] for n in primarios) / len(primarios)
        return {
            'nodos_directos':  nodos,
            'certeza':         min(1.0, certeza),
            'tiene_contenido': True,
            'texto_limpio':    texto
        }

    def _comprension_contextual(
        self, ids_activos, ids_primarios, contexto, texto
    ):
        tipo_mensaje   = self._determinar_tipo_mensaje(
            ids_activos, ids_primarios, texto
        )
        hay_historial  = bool(
            contexto.get('conversacion', {}).get('historial_reciente')
        )
        momento        = contexto.get(
            'temporal', {}
        ).get('momento_dia', 'desconocido')
        nombre_usuario = contexto.get(
            'sebastian', {}
        ).get('nombre', 'Sebastian')
        certeza = 0.75 if hay_historial else 0.60

        return {
            'tipo_mensaje':     tipo_mensaje,
            'hay_historial':    hay_historial,
            'momento_dia':      momento,
            'nombre_usuario':   nombre_usuario,
            'ids_activos':      list(ids_activos),
            'certeza':          certeza
        }

    def _comprension_profunda(
        self, ids_activos, ids_primarios, contexto, tono, texto
    ):
        tipo      = self._determinar_tipo_mensaje(
            ids_activos, ids_primarios, texto
        )
        intencion = self._intencion_desde_tipo(tipo)
        necesidad = self._necesidad_desde_intencion(intencion)
        emocion   = self._detectar_emocion(ids_activos)

        # Enriquecer con grounding 9D
        info_9d   = self._obtener_info_grounding(ids_primarios, contexto)

        certeza = info_9d.get('confianza_promedio', 0.70) \
                  if intencion != 'desconocida' else 0.30

        return {
            'intencion_detectada':    intencion,
            'necesidad_real':         necesidad,
            'emocion_detectada':      emocion,
            'tono_base':              tono,
            'certeza':                certeza,
            'puede_ejecutar':         info_9d.get('puede_ejecutar', False),
            'nivel_comprension':      info_9d.get('nivel_comprension', 'parcial'),
            'grounding_promedio':     info_9d.get('grounding_promedio', 0.5),
            'dimensiones_dominantes': info_9d.get('dimensiones_dominantes', []),
        }

    def _determinar_tipo_mensaje(self, ids, ids_primarios, texto):
        texto_lower = texto.lower().strip()

        # ---- SALUDOS ----
        saludos = {
            'SALUDO_HOLA', 'SALUDO_BUENAS', 'SALUDO_HEY',
            'SALUDO_QUE_TAL', 'SALUDO_QUE_MAS',
            'SALUDO_BUENOS_DIAS', 'SALUDO_TARDES', 'SALUDO_NOCHES'
        }
        if ids_primarios & saludos:
            return 'saludo'

        if 'DESPEDIDA' in ids_primarios:
            return 'despedida'

        if 'GRATITUD' in ids_primarios:
            return 'gratitud'

        # ---- PRESENTACIÓN ----
        presentacion = {'PRESENTACION_NOMBRE', 'VERBO_SER_YO'}
        if (ids_primarios & presentacion and
                ('sebastian' in texto_lower or
                 'me llamo' in texto_lower or
                 'mi nombre' in texto_lower)):
            return 'presentacion_sebastian'

        # ---- QUIÉN ES BELL ----
        if ('PREG_QUIEN' in ids_primarios and
                'VERBO_SER_TU' in ids_primarios):
            return 'pregunta_identidad_bell'

        # ---- QUIÉN ES ALGUIEN MÁS ----
        if ('PREG_QUIEN' in ids_primarios and
                'VERBO_SER_EL' in ids_primarios):
            return 'pregunta_identidad_otro'

        # ---- CÓMO ESTÁ BELL ----
        if ('PREG_COMO' in ids_primarios and
                'VERBO_ESTAR_TU' in ids_primarios):
            return 'pregunta_estado_bell'

        # ---- CÓMO TE LLAMAS ----
        if ('PREG_COMO' in ids_primarios and
                'REF_TE' in ids_primarios):
            return 'pregunta_nombre_bell'

        # ---- QUÉ HACE / PUEDE HACER ----
        capacidad = {
            'VERBO_HACER_TU', 'VERBO_PODER_TU',
            'VERBO_PODER_EL', 'VERBO_HACER'
        }
        if (ids_primarios & capacidad and
                ('PREG_QUE' in ids_primarios or
                 'PREG_CUAL' in ids_primarios)):
            return 'pregunta_capacidad_bell'

        # ---- QUÉ ES BELL ----
        if ('PREG_QUE' in ids_primarios and
                'VERBO_SER_TU' in ids_primarios):
            return 'pregunta_identidad_bell'

        # ---- AYUDA ----
        ayuda = {'VERBO_AYUDAR_ME', 'VERBO_AYUDA', 'VERBO_AYUDAR'}
        if ids_primarios & ayuda:
            return 'solicitud_ayuda'

        # ---- EMOCIONES NEGATIVAS ----
        negativas = {
            'EMOCION_MAL', 'EMOCION_TRISTE', 'EMOCION_FRUSTRADO',
            'EMOCION_CANSADO', 'EMOCION_AGOTADO', 'EMOCION_ESTRESADO',
            'EMOCION_PREOCUPADO', 'EMOCION_ASUSTADO', 'EMOCION_ENOJADO',
            'EMOCION_MOLESTO'
        }
        if ids_primarios & negativas:
            return 'expresion_emocional_negativa'

        # ---- EMOCIONES POSITIVAS ----
        positivas = {
            'EMOCION_BIEN', 'EMOCION_GENIAL', 'EMOCION_FELIZ',
            'EMOCION_CONTENTO', 'EMOCION_ALEGRE', 'EMOCION_EMOCIONADO',
            'EMOCION_MOTIVADO', 'EMOCION_AGRADECIDO'
        }
        if ids_primarios & positivas:
            return 'expresion_emocional_positiva'

        # ---- CONFIRMACIÓN ----
        confirmaciones = {
            'AFIRMACION', 'AFIRMACION_FUERTE', 'EXPR_OK',
            'EXPR_DALE', 'EXPR_LISTO', 'EXPR_ENTENDIDO',
            'EXPR_DE_ACUERDO', 'EXPR_PERFECTO'
        }
        if ids_primarios & confirmaciones:
            return 'confirmacion'

        # ---- NEGACIÓN ----
        if {'NEGACION', 'NEGACION_FUERTE'} & ids_primarios:
            return 'negacion'

        # ---- PREGUNTA GENERAL ----
        preguntas = {
            'PREG_QUE', 'PREG_QUIEN', 'PREG_COMO',
            'PREG_CUANDO', 'PREG_DONDE', 'PREG_POR_QUE',
            'PREG_CUANTO', 'PREG_CUAL'
        }
        if ids_primarios & preguntas:
            return 'pregunta'

        return 'conversacional'

    def _intencion_desde_tipo(self, tipo):
        mapa = {
            'saludo':                       'saludar',
            'despedida':                    'despedirse',
            'gratitud':                     'agradecer',
            'pregunta_identidad_bell':      'conocer_bell',
            'pregunta_identidad_otro':      'conocer_persona',
            'pregunta_estado_bell':         'saber_estado_bell',
            'pregunta_nombre_bell':         'saber_nombre_bell',
            'pregunta_capacidad_bell':      'saber_capacidades_bell',
            'presentacion_sebastian':       'presentarse',
            'pregunta':                     'preguntar',
            'solicitud_ayuda':              'pedir_ayuda',
            'expresion_emocional_positiva': 'expresar_emocion_positiva',
            'expresion_emocional_negativa': 'expresar_emocion_negativa',
            'confirmacion':                 'confirmar',
            'negacion':                     'negar',
            'conversacional':               'conversar',
        }
        return mapa.get(tipo, 'desconocida')

    def _necesidad_desde_intencion(self, intencion):
        mapa = {
            'saludar':                    'conexion_social',
            'despedirse':                 'cierre_conversacion',
            'agradecer':                  'expresar_gratitud',
            'conocer_bell':               'conocimiento_bell',
            'conocer_persona':            'conocimiento_persona',
            'saber_estado_bell':          'conocimiento_bell',
            'saber_nombre_bell':          'conocimiento_bell',
            'saber_capacidades_bell':     'conocimiento_bell',
            'presentarse':                'ser_reconocido',
            'preguntar':                  'informacion',
            'pedir_ayuda':                'ayuda_practica',
            'expresar_emocion_positiva':  'compartir_alegria',
            'expresar_emocion_negativa':  'apoyo_emocional',
            'confirmar':                  'acuerdo',
            'negar':                      'desacuerdo',
            'conversar':                  'conexion_social',
        }
        return mapa.get(intencion, 'desconocida')

    def _detectar_emocion(self, ids):
        if 'GRATITUD' in ids: return 'gratitud'
        positivos = {
            'EMOCION_FELIZ', 'EMOCION_GENIAL', 'EMOCION_ALEGRE',
            'EMOCION_BIEN', 'EMOCION_EMOCIONADO', 'EMOCION_MOTIVADO'
        }
        negativos = {
            'EMOCION_TRISTE', 'EMOCION_MAL', 'EMOCION_FRUSTRADO',
            'EMOCION_CANSADO', 'EMOCION_AGOTADO', 'EMOCION_ESTRESADO',
            'EMOCION_PREOCUPADO', 'EMOCION_ASUSTADO', 'EMOCION_ENOJADO'
        }
        if ids & negativos: return 'negativa'
        if ids & positivos: return 'positiva'
        return 'neutra'

    def _obtener_info_grounding(
        self, ids_primarios: set, contexto: dict
    ) -> dict:
        """
        Obtiene información de grounding 9D de los
        nodos primarios para enriquecer la comprensión.
        """
        try:
            from biblioteca.grounding.calculador import CalculadorGrounding
            calc      = CalculadorGrounding.obtener()
            groundings = []

            for nodo_id in ids_primarios:
                tipo = self._tipo_desde_id(nodo_id)
                g9d  = calc.calcular(nodo_id, tipo, contexto)
                groundings.append(g9d)

            if not groundings:
                return {}

            g_prom = sum(g.efectivo() for g in groundings) / len(groundings)
            c_prom = sum(g.confianza for g in groundings) / len(groundings)
            puede  = all(g.puede_ejecutar() for g in groundings)

            niveles    = [g.nivel_comprension() for g in groundings]
            nivel_dom  = max(set(niveles), key=niveles.count)

            # Dimensiones más dominantes
            dims = {}
            for g in groundings:
                r = g.resumen()['dimensiones']
                for dim, val in r.items():
                    if isinstance(val, float):
                        dims[dim] = dims.get(dim, 0) + val

            dims_top = sorted(
                [
                    (d, round(v / len(groundings), 3))
                    for d, v in dims.items()
                    if isinstance(v, (int, float))
                ],
                key=lambda x: x[1],
                reverse=True
            )[:5]

            return {
                'grounding_promedio':     round(g_prom, 3),
                'confianza_promedio':     round(c_prom, 3),
                'puede_ejecutar':         puede,
                'nivel_comprension':      nivel_dom,
                'dimensiones_dominantes': [d[0] for d in dims_top]
            }

        except Exception:
            return {
                'grounding_promedio':     0.5,
                'confianza_promedio':     0.7,
                'puede_ejecutar':         False,
                'nivel_comprension':      'parcial',
                'dimensiones_dominantes': []
            }

    def _tipo_desde_id(self, nodo_id: str) -> str:
        """Infiere el tipo de grounding desde el ID del nodo."""
        if any(s in nodo_id for s in ['SALUDO', 'DESPEDIDA']):
            return 'saludo'
        if 'GRATITUD' in nodo_id:
            return 'gratitud'
        if 'EMOCION_' in nodo_id:
            neg = [
                'TRISTE', 'MAL', 'FRUSTRADO', 'CANSADO',
                'AGOTADO', 'ESTRESADO', 'PREOCUPADO',
                'ASUSTADO', 'ENOJADO', 'MOLESTO'
            ]
            return 'emocion_negativa' if any(
                n in nodo_id for n in neg
            ) else 'emocion_positiva'
        if 'PREG_' in nodo_id:
            return 'pregunta'
        if any(s in nodo_id for s in ['VERBO_ESTAR', 'VERBO_SER']):
            return 'verbo_estado'
        if 'VERBO_' in nodo_id:
            return 'verbo_accion'
        if 'BELL_' in nodo_id:
            return 'pregunta_sobre_bell'
        return 'concepto'