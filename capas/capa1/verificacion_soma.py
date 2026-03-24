# capas/capa1/verificacion_soma.py
# ================================================
# VERIFICACIÓN SOMA EN CAPA 1
# Verifica integridad, origen y carga neuronal
# Solo cuida el proceso de recepción
# ================================================

from capas.capa1.paquete_capa1 import VerificacionSoma


class VerificadorSoma:
    """
    SOMA en la Capa 1 verifica exactamente tres cosas:
    1. Integridad del paquete
    2. Origen seguro
    3. Carga neuronal manejable

    No analiza contenido semántico.
    No evalúa si lo que se pidió es correcto.
    Solo cuida la integridad del proceso de recepción.
    """

    TAMANIO_MAXIMO_CARACTERES = 50000
    CONCEPTOS_MAXIMO = 200

    def verificar(
        self,
        contenido_normalizado: dict,
        conceptos: list,
        desconocidos: list
    ) -> VerificacionSoma:
        """
        Verifica el paquete y retorna el resultado.
        Nunca bloquea — solo reporta.
        """
        verificacion = VerificacionSoma(estado='aprobado')
        notas = []

        # 1. Verificar integridad
        integridad, nota_integridad = self._verificar_integridad(
            contenido_normalizado
        )
        verificacion.integridad = integridad
        if nota_integridad:
            notas.append(nota_integridad)

        # 2. Verificar origen
        origen_seguro, nota_origen = self._verificar_origen(
            contenido_normalizado
        )
        verificacion.origen_seguro = origen_seguro
        if nota_origen:
            notas.append(nota_origen)

        # 3. Verificar carga
        carga_normal, nota_carga = self._verificar_carga(
            contenido_normalizado,
            conceptos
        )
        verificacion.carga_normal = carga_normal
        if nota_carga:
            notas.append(nota_carga)

        # Determinar estado final
        if not integridad:
            verificacion.estado = 'retenido'
        elif not carga_normal:
            verificacion.estado = 'fragmentado'
        else:
            verificacion.estado = 'aprobado'

        verificacion.notas = notas
        return verificacion

    def _verificar_integridad(self, contenido: dict):
        """
        Verifica que el paquete tenga
        los campos mínimos necesarios.
        """
        campos_requeridos = [
            'contenido_limpio',
            'tipo_origen',
            'contenido_original'
        ]

        for campo in campos_requeridos:
            if campo not in contenido:
                return False, f'Campo requerido ausente: {campo}'

        if not contenido.get('exitoso', True):
            return False, f'Error en módulo: {contenido.get("error", "desconocido")}'

        return True, None

    def _verificar_origen(self, contenido: dict):
        """
        Verifica que el origen del estímulo
        no sea sospechoso.
        """
        tipo_origen = contenido.get('tipo_origen', 'texto')
        tipos_validos = {
            'texto', 'voz', 'imagen', 'archivo',
            'sensor', 'sistema'
        }

        if tipo_origen not in tipos_validos:
            return False, f'Tipo de origen desconocido: {tipo_origen}'

        return True, None

    def _verificar_carga(self, contenido: dict, conceptos: list):
        """
        Verifica que el paquete no sobrecargue
        la red neuronal.
        """
        # Verificar tamaño del contenido
        contenido_limpio = contenido.get('contenido_limpio', '')
        if len(contenido_limpio) > self.TAMANIO_MAXIMO_CARACTERES:
            return False, (
                f'Contenido demasiado grande: '
                f'{len(contenido_limpio)} caracteres. '
                f'Máximo: {self.TAMANIO_MAXIMO_CARACTERES}'
            )

        # Verificar cantidad de conceptos
        if len(conceptos) > self.CONCEPTOS_MAXIMO:
            return False, (
                f'Demasiados conceptos: {len(conceptos)}. '
                f'Máximo: {self.CONCEPTOS_MAXIMO}'
            )

        return True, None