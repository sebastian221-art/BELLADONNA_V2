# capas/capa1/__init__.py
# ================================================
# CAPA 1 — Punto de entrada único
# Expone solo una función: procesar(estimulo)
# Todo lo interno es invisible para el resto
# Si algo falla retorna paquete marcado como fallido
# ================================================

from capas.capa1.paquete_capa1 import PaqueteCapa1, VerificacionSoma
from capas.capa1.identificador_tipo import IdentificadorTipo
from capas.capa1.normalizador import Normalizador
from capas.capa1.extractor_contexto import ExtractorContexto
from capas.capa1.traductor import Traductor
from capas.capa1.verificacion_soma import VerificadorSoma

# Instancias — se crean una vez y se reusan
_identificador = IdentificadorTipo()
_normalizador = Normalizador()
_extractor = ExtractorContexto()
_traductor = Traductor()
_soma = VerificadorSoma()

# Registro de módulos disponibles
_modulos = {}

def _cargar_modulos():
    """
    Carga todos los módulos de entrada.
    Si un módulo falla no rompe el sistema.
    """
    modulos_a_cargar = [
        ('texto',   'capas.capa1.modulos.modulo_texto',   'ModuloTexto'),
        ('voz',     'capas.capa1.modulos.modulo_voz',     'ModuloVoz'),
        ('imagen',  'capas.capa1.modulos.modulo_imagen',  'ModuloImagen'),
        ('archivo', 'capas.capa1.modulos.modulo_archivo', 'ModuloArchivo'),
        ('sensor',  'capas.capa1.modulos.modulo_sensor',  'ModuloSensor'),
        ('sistema', 'capas.capa1.modulos.modulo_sistema', 'ModuloSistema'),
    ]

    for tipo, modulo_path, clase_nombre in modulos_a_cargar:
        try:
            import importlib
            modulo = importlib.import_module(modulo_path)
            clase = getattr(modulo, clase_nombre)
            _modulos[tipo] = clase()
        except Exception as e:
            print(f'Capa 1: módulo {tipo} no disponible — {e}')

_cargar_modulos()


def procesar(estimulo) -> dict:
    """
    La única función pública de la Capa 1.
    Recibe cualquier estímulo.
    Retorna siempre un diccionario con el paquete.
    Nunca lanza excepciones.
    """
    try:
        return _procesar_interno(estimulo)
    except Exception as e:
        # Nunca falla — retorna paquete de error
        paquete = PaqueteCapa1(
            contenido_original=str(estimulo) if estimulo else '',
            exitoso=False,
            error=f'Error interno en Capa 1: {str(e)}'
        )
        return paquete.a_dict()


def _procesar_interno(estimulo) -> dict:
    """
    El procesamiento interno completo.
    """
    # 1. Identificar tipo
    tipo = _identificador.identificar(estimulo)

    # 2. Seleccionar módulo
    modulo = _modulos.get(tipo, _modulos.get('texto'))

    if not modulo:
        raise RuntimeError(f'No hay módulo disponible para tipo: {tipo}')

    # 3. Procesar con el módulo
    output_modulo = modulo.procesar(estimulo)

    # 4. Normalizar
    contenido_normalizado = _normalizador.normalizar(output_modulo)

    # 5. Extraer contexto
    contexto = _extractor.extraer(contenido_normalizado)

    # 6. Traducir a lenguaje Bell
    conceptos, desconocidos, certeza = _traductor.traducir(
        contenido_normalizado
    )

    # 7. Verificar con SOMA
    verificacion = _soma.verificar(
        contenido_normalizado,
        conceptos,
        desconocidos
    )

    # 8. Construir paquete final
    paquete = PaqueteCapa1(
        conceptos=conceptos,
        nivel_certeza_global=certeza,
        contenido_original=contenido_normalizado['contenido_original'],
        tipo_origen=tipo,
        tono_detectado=contenido_normalizado.get('tono_detectado', 'neutral'),
        idioma=contenido_normalizado.get('idioma', 'es'),
        contexto=contexto,
        desconocidos=desconocidos,
        verificacion_soma=verificacion,
        exitoso=verificacion.estado != 'retenido'
    )

    # 9. Actualizar historial del extractor
    _extractor.agregar_al_historial({
        'tipo': tipo,
        'certeza': certeza,
        'conceptos': len(conceptos),
        'desconocidos': len(desconocidos)
    })

    return paquete.a_dict()
