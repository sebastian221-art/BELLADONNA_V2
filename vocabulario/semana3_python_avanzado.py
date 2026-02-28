"""
Vocabulario Python Avanzado - Semana 3.

40 conceptos de programación Python avanzada.
Grounding medio-alto (0.6-0.9).
"""
from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto

def obtener_conceptos_python_avanzado():
    """Retorna conceptos Python avanzado (40 conceptos)."""
    conceptos = []
    
    # DECORADORES Y FUNCIONES AVANZADAS (8)
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DECORATOR",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["decorator", "decorador", "@"],
        confianza_grounding=0.8,
        propiedades={
            'es_funcion': True,
            'modifica_comportamiento': True,
            'sintaxis': '@decorator'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LAMBDA",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["lambda", "función anónima"],
        confianza_grounding=0.9,
        propiedades={
            'es_funcion': True,
            'inline': True,
            'sintaxis': 'lambda x: x+1'
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_GENERATOR",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["generator", "generador", "yield"],
        confianza_grounding=0.8,
        propiedades={
            'es_iterador': True,
            'lazy_evaluation': True,
            'usa_yield': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_COMPREHENSION",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["comprehension", "list comprehension"],
        confianza_grounding=0.9,
        propiedades={
            'es_expresion': True,
            'crea_lista': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CLOSURE",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["closure", "clausura"],
        confianza_grounding=0.7,
        propiedades={
            'captura_scope': True,
            'nested_function': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MAP",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["mapear"],
        confianza_grounding=0.9,
        propiedades={
            'es_funcion_orden_superior': True,
            'aplica_funcion': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FILTER",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["filter"],
        confianza_grounding=0.9,
        propiedades={
            'es_funcion_orden_superior': True,
            'filtra_elementos': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_REDUCE",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["reduce", "reducir"],
        confianza_grounding=0.8,
        propiedades={
            'es_funcion_orden_superior': True,
            'acumula_resultado': True
        }
    ))
    
    # ASYNC/AWAIT (6)
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ASYNC",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["async", "asíncrono"],
        confianza_grounding=0.7,
        propiedades={
            'es_keyword': True,
            'define_coroutine': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_AWAIT",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["await", "esperar"],
        confianza_grounding=0.7,
        propiedades={
            'es_keyword': True,
            'pausa_ejecucion': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_COROUTINE",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["coroutine", "corrutina"],
        confianza_grounding=0.6,
        propiedades={
            'es_funcion_async': True,
            'pausable': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ASYNCIO",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["asyncio"],
        confianza_grounding=0.7,
        propiedades={
            'es_libreria': True,
            'maneja_concurrencia': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TASK",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["task"],
        confianza_grounding=0.7,
        propiedades={
            'es_abstraccion': True,
            'wrap_coroutine': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FUTURE",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["future", "futuro"],
        confianza_grounding=0.6,
        propiedades={
            'representa_resultado': True,
            'eventual': True
        }
    ))
    
    # CLASES AVANZADAS (8)
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PROPERTY",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["property", "propiedad", "@property"],
        confianza_grounding=0.8,
        propiedades={
            'es_decorator': True,
            'getter_setter': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_STATICMETHOD",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["staticmethod", "@staticmethod"],
        confianza_grounding=0.8,
        propiedades={
            'es_decorator': True,
            'no_requiere_self': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CLASSMETHOD",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["classmethod", "@classmethod"],
        confianza_grounding=0.8,
        propiedades={
            'es_decorator': True,
            'recibe_cls': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INHERITANCE",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["inheritance", "herencia"],
        confianza_grounding=0.8,
        propiedades={
            'es_mecanismo_oop': True,
            'reutiliza_codigo': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SUPER",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["super", "padre"],
        confianza_grounding=0.8,
        propiedades={
            'accede_clase_padre': True,
            'es_builtin': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ABSTRACT",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["abstract", "abstracto", "ABC"],
        confianza_grounding=0.7,
        propiedades={
            'no_instanciable': True,
            'define_interfaz': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DATACLASS",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["dataclass", "@dataclass"],
        confianza_grounding=0.8,
        propiedades={
            'es_decorator': True,
            'auto_genera_metodos': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DUNDER",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["dunder", "__init__", "magic method"],
        confianza_grounding=0.8,
        propiedades={
            'doble_underscore': True,
            'comportamiento_especial': True
        }
    ))
    
    # MANEJO DE EXCEPCIONES (5)
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TRY",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["try", "intentar"],
        confianza_grounding=0.9,
        propiedades={
            'es_control_flujo': True,
            'maneja_errores': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EXCEPT",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["except"],
        confianza_grounding=0.9,
        propiedades={
            'captura_error': True,
            'requiere_try': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FINALLY",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["finally", "finalmente"],
        confianza_grounding=0.9,
        propiedades={
            'siempre_ejecuta': True,
            'cleanup': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RAISE",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["raise", "lanzar"],
        confianza_grounding=0.9,
        propiedades={
            'lanza_excepcion': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EXCEPTION_CLASS",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["exception"],
        confianza_grounding=0.8,
        propiedades={
            'es_clase': True,
            'representa_error': True
        }
    ))
    
    # CONTEXT MANAGERS (3)
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_WITH",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["with", "context manager"],
        confianza_grounding=0.9,
        propiedades={
            'gestiona_recursos': True,
            'auto_cleanup': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ENTER",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["__enter__", "enter"],
        confianza_grounding=0.7,
        propiedades={
            'es_dunder': True,
            'setup_context': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EXIT",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["__exit__", "exit"],
        confianza_grounding=0.7,
        propiedades={
            'es_dunder': True,
            'cleanup_context': True
        }
    ))
    
    # MÓDULOS Y PAQUETES (5)
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MODULE",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["module"],
        confianza_grounding=0.8,
        propiedades={
            'es_archivo_py': True,
            'agrupa_codigo': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PACKAGE",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["package", "paquete"],
        confianza_grounding=0.8,
        propiedades={
            'es_directorio': True,
            'contiene_modulos': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FROM",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["from", "desde"],
        confianza_grounding=0.9,
        propiedades={
            'importa_especifico': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_AS",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["as", "alias"],
        confianza_grounding=0.9,
        propiedades={
            'crea_alias': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INIT_PY",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["__init__.py", "init"],
        confianza_grounding=0.8,
        propiedades={
            'marca_package': True
        }
    ))
    
    # TIPOS Y TYPE HINTS (5)
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TYPE_HINT",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["type hint", "typing"],
        confianza_grounding=0.8,
        propiedades={
            'es_anotacion': True,
            'ayuda_ide': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_OPTIONAL",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["Optional", "opcional"],
        confianza_grounding=0.7,
        propiedades={
            'permite_none': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_UNION",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["Union", "unión"],
        confianza_grounding=0.7,
        propiedades={
            'multiples_tipos': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_GENERIC",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["Generic", "genérico"],
        confianza_grounding=0.6,
        propiedades={
            'tipo_parametrizado': True
        }
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PROTOCOL",
        tipo=TipoConcepto.CONCEPTO_ABSTRACTO,
        palabras_español=["Protocol", "protocolo"],
        confianza_grounding=0.6,
        propiedades={
            'structural_typing': True
        }
    ))
    
    return conceptos