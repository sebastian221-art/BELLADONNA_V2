# biblioteca/conectador/conectador_inteligente.py
# ================================================
# CONECTADOR INTELIGENTE
# El más importante de la Capa 2
# Cuando algo nuevo entra a la biblioteca
# no solo lo agrega — lo conecta con todo
# lo relacionado automáticamente
# ================================================

class ConectadorInteligente:
    """
    Garantiza que nada exista aislado en la biblioteca.
    Cuando se agrega un nodo nuevo analiza la red
    y lo conecta inteligentemente con lo que existe.

    Principio fundamental:
    Un nodo sin conexiones no tiene significado para Bell.
    El significado ES las conexiones.
    """

    # Pesos mínimos para crear una conexión
    PESO_MINIMO_CONEXION = 0.3

    # Reglas de conexión automática por tipo
    # Cuando se agrega un nodo de X tipo
    # se conecta automáticamente a estos nodos
    REGLAS_POR_TIPO = {
        'valor': {
            'siempre_conectar': ['BELL_CORE'],
            'peso_base': 1.0,
            'tipo_relacion': 'tiene_valor'
        },
        'consejera': {
            'siempre_conectar': ['BELL_CORE', 'CONSEJERA_SAGE'],
            'peso_base': 1.0,
            'tipo_relacion': 'pertenece_a'
        },
        'habilidad': {
            'siempre_conectar': ['BELL_CORE'],
            'peso_base': 0.8,
            'tipo_relacion': 'tiene_habilidad'
        },
        'concepto': {
            'siempre_conectar': [],
            'peso_base': 0.7,
            'tipo_relacion': 'relacionado_con'
        },
        'memoria': {
            'siempre_conectar': ['BELL_CORE', 'NEURONA_SEBASTIAN'],
            'peso_base': 0.7,
            'tipo_relacion': 'recuerda'
        },
        'relacion': {
            'siempre_conectar': ['BELL_CORE'],
            'peso_base': 0.8,
            'tipo_relacion': 'tiene_relacion'
        },
        'identidad': {
            'siempre_conectar': ['BELL_CORE'],
            'peso_base': 1.0,
            'tipo_relacion': 'es_parte_de'
        }
    }

    def __init__(self, red_neuronal):
        self.red = red_neuronal

    def integrar_nodo(self, nodo_id: str) -> dict:
        """
        Integra un nodo recién agregado a la red.
        Lo conecta con todo lo relacionado.
        Retorna un reporte de las conexiones creadas.
        """
        nodo = self.red.obtener_nodo(nodo_id)
        if not nodo:
            return {'error': f'Nodo {nodo_id} no encontrado'}

        conexiones_creadas = []

        # 1. Aplicar reglas automáticas por tipo
        conexiones_tipo = self._aplicar_reglas_tipo(nodo)
        conexiones_creadas.extend(conexiones_tipo)

        # 2. Buscar nodos similares por subtipo
        conexiones_similares = self._conectar_similares(nodo)
        conexiones_creadas.extend(conexiones_similares)

        # 3. Buscar conexiones por vocabulario compartido
        conexiones_vocab = self._conectar_por_vocabulario(nodo)
        conexiones_creadas.extend(conexiones_vocab)

        return {
            'nodo_id': nodo_id,
            'conexiones_creadas': len(conexiones_creadas),
            'detalle': conexiones_creadas
        }

    def integrar_concepto_del_vocabulario(
        self, concepto_id: str, grounding: float,
        tipo: str = 'concepto'
    ) -> dict:
        """
        Integra un concepto que viene del vocabulario
        de la Capa 1 cuando Bell lo encuentra por
        primera vez.
        """
        # Verificar si ya existe
        if self.red.existe_nodo(concepto_id):
            return {'existia': True, 'nodo_id': concepto_id}

        # Crear el nodo
        self.red.agregar_nodo({
            'id': concepto_id,
            'nucleo': {
                'tipo': tipo,
                'subtipo': 'vocabulario',
                'grounding_base': grounding,
                'dimensiones_activas': ['conocimiento'],
                'archivo_real': None,
                'inmutable': False
            },
            'activacion': {
                'umbral': 1.0 - grounding,
                'velocidad': self._velocidad_por_grounding(grounding),
                'mielina': grounding >= 0.9
            },
            'memoria': {
                'veces_usado': 0,
                'ultimo_uso': None,
                'contextos_de_uso': [],
                'resultado_historico': grounding
            }
        })

        # Integrar con conexiones inteligentes
        reporte = self.integrar_nodo(concepto_id)
        reporte['existia'] = False
        return reporte

    def fortalecer_conexion(
        self, origen_id: str,
        destino_id: str, exito: bool
    ):
        """
        Fortalece o debilita una conexión
        según si llevó a un resultado exitoso.
        """
        conexion = self.red.obtener_conexion(origen_id, destino_id)
        if not conexion:
            return

        peso_actual = conexion.get('peso', 0.5)

        if exito:
            # Éxito — fortalecer la conexión
            nuevo_peso = min(1.0, peso_actual + 0.05)
        else:
            # Fallo — debilitar la conexión
            # Pero nunca debajo del mínimo
            nuevo_peso = max(
                self.PESO_MINIMO_CONEXION,
                peso_actual - 0.03
            )

        self.red.actualizar_peso_conexion(
            origen_id, destino_id, nuevo_peso
        )

    def crear_neurona_compuesta(
        self, id_nueva: str,
        nodos_componentes: list,
        contexto_creacion: str
    ) -> dict:
        """
        Crea una neurona compuesta cuando Bell
        aprende que una combinación de nodos funciona.
        """
        if not nodos_componentes:
            return {'error': 'No hay componentes'}

        # Calcular grounding promedio de los componentes
        groundings = []
        for nodo_id in nodos_componentes:
            nodo = self.red.obtener_nodo(nodo_id)
            if nodo:
                groundings.append(
                    nodo['nucleo'].get('grounding_base', 0.5)
                )

        grounding_compuesto = (
            sum(groundings) / len(groundings)
            if groundings else 0.5
        )

        # Crear la neurona compuesta
        self.red.agregar_nodo({
            'id': id_nueva,
            'nucleo': {
                'tipo': 'compuesta',
                'subtipo': 'aprendida',
                'grounding_base': grounding_compuesto,
                'dimensiones_activas': ['ejecutabilidad', 'conocimiento'],
                'archivo_real': None,
                'inmutable': False,
                'componentes': nodos_componentes,
                'contexto_creacion': contexto_creacion
            },
            'activacion': {
                'umbral': 0.3,
                'velocidad': 'media',
                'mielina': False
            },
            'memoria': {
                'veces_usado': 1,
                'ultimo_uso': None,
                'contextos_de_uso': [contexto_creacion],
                'resultado_historico': grounding_compuesto
            }
        })

        # Conectar con sus componentes
        for nodo_id in nodos_componentes:
            self.red.conectar(
                id_nueva, nodo_id, 0.9, 'compuesta_de'
            )
            self.red.conectar(
                nodo_id, id_nueva, 0.9, 'parte_de_compuesta'
            )

        # Integrar con el resto
        return self.integrar_nodo(id_nueva)

    def _aplicar_reglas_tipo(self, nodo: dict) -> list:
        """
        Aplica las reglas automáticas de conexión
        según el tipo del nodo.
        """
        tipo = nodo['nucleo'].get('tipo', 'concepto')
        reglas = self.REGLAS_POR_TIPO.get(tipo, {})
        conexiones = []

        nodos_obligatorios = reglas.get('siempre_conectar', [])
        peso_base = reglas.get('peso_base', 0.7)
        tipo_relacion = reglas.get('tipo_relacion', 'relacionado_con')

        for nodo_obligatorio in nodos_obligatorios:
            if not self.red.existe_nodo(nodo_obligatorio):
                continue
            if nodo['id'] == nodo_obligatorio:
                continue
            if self.red.existe_conexion(nodo['id'], nodo_obligatorio):
                continue

            self.red.conectar(
                nodo['id'],
                nodo_obligatorio,
                peso_base,
                tipo_relacion
            )
            conexiones.append({
                'origen': nodo['id'],
                'destino': nodo_obligatorio,
                'peso': peso_base,
                'tipo': tipo_relacion,
                'razon': 'regla_tipo'
            })

        return conexiones

    def _conectar_similares(self, nodo: dict) -> list:
        """
        Conecta el nodo nuevo con nodos
        del mismo tipo que ya existen.
        """
        tipo = nodo['nucleo'].get('tipo', 'concepto')
        subtipo = nodo['nucleo'].get('subtipo', '')
        conexiones = []

        todos_los_nodos = self.red.obtener_todos_los_nodos()

        for otro_id, otro_nodo in todos_los_nodos.items():
            if otro_id == nodo['id']:
                continue

            otro_tipo = otro_nodo['nucleo'].get('tipo', '')
            otro_subtipo = otro_nodo['nucleo'].get('subtipo', '')

            # Mismo tipo y subtipo — conexión media
            if tipo == otro_tipo and subtipo == otro_subtipo:
                if not self.red.existe_conexion(nodo['id'], otro_id):
                    peso = 0.6
                    self.red.conectar(
                        nodo['id'], otro_id, peso, 'mismo_tipo_que'
                    )
                    conexiones.append({
                        'origen': nodo['id'],
                        'destino': otro_id,
                        'peso': peso,
                        'tipo': 'mismo_tipo_que',
                        'razon': 'similitud'
                    })

        return conexiones

    def _conectar_por_vocabulario(self, nodo: dict) -> list:
        """
        Busca conexiones por palabras clave compartidas
        en los IDs de los nodos.
        Esto permite que VALOR_HONESTIDAD se conecte
        automáticamente a todo lo que tenga
        HONESTIDAD en su ID.
        """
        id_nodo = nodo['id'].upper()
        palabras_clave = id_nodo.split('_')
        palabras_clave = [
            p for p in palabras_clave
            if len(p) > 3  # Ignorar palabras muy cortas
        ]

        conexiones = []
        todos_los_nodos = self.red.obtener_todos_los_nodos()

        for otro_id, otro_nodo in todos_los_nodos.items():
            if otro_id == nodo['id']:
                continue

            otro_id_upper = otro_id.upper()

            # Buscar palabras clave compartidas
            for palabra in palabras_clave:
                if (palabra in otro_id_upper and
                        not self.red.existe_conexion(
                            nodo['id'], otro_id
                        )):
                    peso = 0.65
                    self.red.conectar(
                        nodo['id'], otro_id, peso, 'vocabulario_compartido'
                    )
                    conexiones.append({
                        'origen': nodo['id'],
                        'destino': otro_id,
                        'peso': peso,
                        'tipo': 'vocabulario_compartido',
                        'razon': f'palabra_clave:{palabra}'
                    })
                    break  # Una conexión por nodo máximo

        return conexiones

    def _velocidad_por_grounding(self, grounding: float) -> str:
        """
        Determina la velocidad de activación
        según el grounding del nodo.
        """
        if grounding >= 0.9:
            return 'inmediata'
        elif grounding >= 0.7:
            return 'rapida'
        elif grounding >= 0.5:
            return 'media'
        else:
            return 'lenta'