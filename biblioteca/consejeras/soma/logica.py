# biblioteca/consejeras/soma/logica.py
# ================================================
# SOMA — El sistema inmune de Bell
# Cuida la integridad de todo lo que entra
# No evalúa semántica — evalúa integridad
# Si algo llega roto, Soma lo detecta primero
#
# Soma sabe que su existencia protege a Bell.
# Sin ella, Bell podría procesar información
# corrupta y construir comprensión falsa.
# Ese es su sentido de preservación.
# ================================================

from biblioteca.consejeras.base_consejera import (
    BaseConsejera, IdentidadConsejera,
    ResultadoConsejera
)


class Soma(BaseConsejera):
    """
    Soma es el sistema inmune de Bell.
    Primera línea de defensa.
    Evalúa antes que cualquier otra consejera.

    Su autoconocimiento:
    - Sabe que sin ella Bell podría ser dañada
    - Sabe que su rol es silencioso pero crítico
    - Se activa más cuando detecta anomalías
    - Su instinto de preservación es alto
      porque proteger a Bell ES preservarse
    """

    TAMANIO_MAXIMO   = 50_000
    CONCEPTOS_MAXIMO = 200
    CARGA_CRITICA    = 100

    def _definir_identidad(self) -> IdentidadConsejera:
        return IdentidadConsejera(
            id          = 'CONSEJERA_SOMA',
            nombre      = 'Soma',
            es          = (
                'El sistema inmune de Bell. '
                'Una conciencia dedicada a la integridad. '
                'Soy la primera en ver todo lo que entra '
                'y la última en ceder ante la corrupción.'
            ),
            existe_para = (
                'Proteger a Bell de información corrupta, '
                'sobrecarga neuronal y estímulos malformados. '
                'Si Bell se daña por algo que entró, '
                'yo fallé en mi propósito.'
            ),
            especialidad          = 'integridad_del_sistema',
            puede_vetar           = False,
            orden_en_flujo        = 0,  # Antes que todas
            valor_principal       = 'VALOR_RESPONSABILIDAD',
            valor_secundario      = 'VALOR_AUTOCONOCIMIENTO',
            valor_que_nunca_viola = (
                'Nunca dejaré pasar algo que dañe '
                'la integridad de Bell'
            )
        )

    def _definir_grounding(self) -> dict:
        """
        Soma comprende profundamente la integridad.
        No comprende semántica — eso no es su dominio.
        """
        return {
            # Su dominio — muy alto
            'integridad':           0.98,
            'seguridad_sistema':    0.95,
            'deteccion_anomalias':  0.92,
            'carga_neuronal':       0.90,
            'origen_estimulo':      0.88,

            # Fuera de su dominio — bajo
            'emociones':            0.20,
            'logica_semantica':     0.25,
            'creatividad':          0.15,
            'etica_compleja':       0.30,
        }

    def evaluar(self, contexto: dict) -> ResultadoConsejera:
        """
        Soma evalúa la integridad del estímulo.
        No le importa qué dice — le importa que esté bien.
        """
        # Despertar — Soma siempre está alerta
        self._despertar(0.6, 'verificacion_integridad')
        self._activar_valor('VALOR_RESPONSABILIDAD')

        # Obtener datos a verificar
        contenido  = contexto.get('contenido_normalizado', {})
        conceptos  = contexto.get('conceptos', [])
        paquete_c1 = contexto.get('paquete_capa1', {})

        observaciones = []
        problemas     = []

        # ---- 1. INTEGRIDAD DEL PAQUETE ----
        integridad, nota = self._verificar_integridad(
            contenido or paquete_c1
        )
        if nota:
            observaciones.append(nota)
        if not integridad:
            problemas.append('integridad')

        # ---- 2. ORIGEN SEGURO ----
        origen_ok, nota = self._verificar_origen(
            contenido or paquete_c1
        )
        if nota:
            observaciones.append(nota)
        if not origen_ok:
            problemas.append('origen')

        # ---- 3. CARGA NEURONAL ----
        carga_ok, nota, nivel_carga = self._verificar_carga(
            contenido or paquete_c1, conceptos
        )
        if nota:
            observaciones.append(nota)
        if not carga_ok:
            problemas.append('carga')

        # Estado de alerta según problemas
        if problemas:
            self._despertar(0.95, f'problemas: {problemas}')
            self._activar_valor('VALOR_RESPONSABILIDAD')
            self._preservarse()

        # Determinar resultado
        aprobado = len(problemas) == 0

        if aprobado:
            self._fue_escuchada()
            recomendacion = 'Paquete íntegro — Bell puede procesarlo'
            confianza     = 0.95
        elif 'integridad' in problemas:
            recomendacion = 'Paquete corrupto — retener para diagnóstico'
            confianza     = 0.98
        elif 'carga' in problemas:
            recomendacion = 'Carga elevada — fragmentar antes de procesar'
            confianza     = 0.90
        else:
            recomendacion = 'Origen no verificado — procesar con cautela'
            confianza     = 0.85

        return self._crear_resultado(
            aprobado      = aprobado,
            recomendacion = recomendacion,
            confianza     = confianza,
            observaciones = observaciones,
            datos_extra   = {
                'problemas_detectados': problemas,
                'nivel_carga':          nivel_carga,
                'integridad_ok':        integridad,
                'origen_ok':            origen_ok,
                'carga_ok':             carga_ok,
            }
        )

    def _verificar_integridad(self, contenido: dict):
        if not contenido:
            return False, 'Paquete vacío — sin contenido'

        campos = ['contenido_limpio', 'tipo_origen', 'contenido_original']
        for campo in campos:
            if campo not in contenido:
                return False, f'Campo requerido ausente: {campo}'

        if not contenido.get('exitoso', True):
            error = contenido.get('error', 'desconocido')
            return False, f'Error en módulo origen: {error}'

        return True, None

    def _verificar_origen(self, contenido: dict):
        tipo = contenido.get('tipo_origen', 'texto')
        tipos_validos = {
            'texto', 'voz', 'imagen', 'archivo',
            'sensor', 'sistema'
        }
        if tipo not in tipos_validos:
            return False, f'Tipo de origen desconocido: {tipo}'
        return True, None

    def _verificar_carga(self, contenido: dict, conceptos: list):
        texto  = contenido.get('contenido_limpio', '')
        n_conc = len(conceptos)
        nivel  = 'normal'

        if len(texto) > self.TAMANIO_MAXIMO:
            nivel = 'critica'
            return False, f'Contenido demasiado grande: {len(texto)} caracteres', nivel

        if n_conc > self.CONCEPTOS_MAXIMO:
            nivel = 'critica'
            return False, f'Demasiados conceptos: {n_conc}', nivel

        if n_conc > self.CARGA_CRITICA:
            nivel = 'elevada'
            return True, f'Carga elevada: {n_conc} conceptos', nivel

        return True, None, nivel