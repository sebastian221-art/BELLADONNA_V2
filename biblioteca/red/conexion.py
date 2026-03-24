# biblioteca/red/conexion.py
# ================================================
# CONEXION — Definición de relaciones entre nodos
# Una conexión es más que un enlace —
# tiene historia, tipo y fuerza variable
# ================================================

import time


# Tipos de relación válidos
TIPOS_RELACION = {
    # Estructura
    'es_parte_de',
    'tiene',
    'incluye',
    'pertenece_a',
    'contiene',

    # Identidad
    'es_mismo_que',
    'es_tipo_de',
    'tiene_valor',
    'tiene_consejera',
    'tiene_habilidad',
    'tiene_cuerpo',
    'tiene_vinculo',
    'tiene_relacion',

    # Acción y dirección
    'causa',
    'activa_a',
    'depende_de',
    'requiere',
    'produce',
    'dirige',
    'ejecuta_para',
    'orquesta',
    'reporta_a',

    # Supervisión
    'supervisa',
    'supervisado_por',
    'cuida_relacion',
    'sirve_a',
    'se_aplica_a',

    # Relación social
    'conoce_a',
    'es_creador_de',
    'une_a',
    'parte_de',
    'colabora_con',

    # Semántica
    'relacionado_con',
    'mismo_tipo_que',
    'vocabulario_compartido',
    'opuesto_a',

    # Aprendizaje
    'compuesta_de',
    'parte_de_compuesta',
    'aprendido_de',

    # Memoria
    'recuerda',
    'historia_de',

    # Genérico
    'conectado_a',
}


def validar_tipo_relacion(tipo: str) -> str:
    """
    Valida el tipo de relación.
    Si no es válido usa 'conectado_a'.
    """
    if tipo in TIPOS_RELACION:
        return tipo
    return 'conectado_a'


def calcular_peso_inicial(
    tipo_origen: str,
    tipo_destino: str,
    tipo_relacion: str
) -> float:
    """
    Calcula el peso inicial de una conexión
    según los tipos de los nodos involucrados.
    """
    # Conexiones con core o valores siempre son fuertes
    if tipo_destino in ('identidad', 'valor'):
        return 0.9

    # Conexiones entre consejeras son fuertes
    if tipo_origen == 'consejera' and tipo_destino == 'consejera':
        return 0.85

    # Conexiones habilidad → concepto son medias
    if tipo_origen == 'habilidad' and tipo_destino == 'concepto':
        return 0.7

    # Conexiones entre conceptos son variables
    if tipo_origen == 'concepto' and tipo_destino == 'concepto':
        return 0.6

    # Por defecto
    return 0.5