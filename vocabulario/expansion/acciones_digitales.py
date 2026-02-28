"""
Acciones Digitales - Expansión Fase 4A.

Acciones que Bell SÍ puede ejecutar con alto grounding.
Estas son las capacidades REALES del sistema.

Conceptos: 40 total
Grounding promedio: 0.90
Tipo: OPERACION_SISTEMA (ejecutables)
"""
from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto


def obtener_conceptos_acciones_digitales():
    """
    Retorna acciones digitales que Bell puede ejecutar.
    
    Estas conectan directamente con operaciones del sistema.
    Grounding 0.85-1.0 porque SON ejecutables.
    
    Categorías:
    - Gestión de archivos (10)
    - Ejecución de código (10)
    - Análisis y búsqueda (10)
    - Comunicación/Output (10)
    """
    conceptos = []
    
    # ══════════ GESTIÓN DE ARCHIVOS ═════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CREAR_ARCHIVO_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["crear archivo", "hacer archivo", "generar archivo", "nuevo archivo"],
        confianza_grounding=0.95,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
            "modifica_sistema": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_ESCRIBIR", "CONCEPTO_TOUCH"},
        },
        operaciones=["touch", "echo > archivo"],
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LEER_ARCHIVO_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["leer archivo", "ver archivo", "mostrar archivo", "abrir archivo"],
        confianza_grounding=0.95,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
            "solo_lectura": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_LEER", "CONCEPTO_CAT"},
        },
        operaciones=["cat", "head", "tail", "less"],
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EDITAR_ARCHIVO_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["editar archivo", "modificar archivo", "cambiar archivo"],
        confianza_grounding=0.90,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
            "modifica_sistema": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_ESCRIBIR", "CONCEPTO_SED"},
        },
        operaciones=["sed", "echo >>"],
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ELIMINAR_ARCHIVO_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["eliminar archivo", "borrar archivo", "quitar archivo", "remover archivo"],
        confianza_grounding=0.90,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
            "modifica_sistema": True,
            "es_peligroso": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_ELIMINAR", "CONCEPTO_RM"},
        },
        operaciones=["rm"],
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_COPIAR_ARCHIVO_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["copiar archivo", "duplicar archivo", "clonar archivo"],
        confianza_grounding=0.95,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
            "modifica_sistema": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_CP"},
        },
        operaciones=["cp"],
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MOVER_ARCHIVO_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["mover archivo", "trasladar archivo", "reubicar archivo"],
        confianza_grounding=0.95,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
            "modifica_sistema": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_MV", "CONCEPTO_MOVER"},
        },
        operaciones=["mv"],
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RENOMBRAR_ARCHIVO_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["renombrar archivo", "cambiar nombre archivo"],
        confianza_grounding=0.95,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
            "modifica_sistema": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_MV", "CONCEPTO_RENOMBRAR"},
        },
        operaciones=["mv"],
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CREAR_CARPETA_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["crear carpeta", "nueva carpeta", "hacer directorio", "crear directorio"],
        confianza_grounding=0.95,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
            "modifica_sistema": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_MKDIR"},
        },
        operaciones=["mkdir"],
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LISTAR_ARCHIVOS_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["listar archivos", "ver archivos", "mostrar archivos", "qué hay en"],
        confianza_grounding=0.98,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
            "solo_lectura": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_LS", "CONCEPTO_LISTAR"},
        },
        operaciones=["ls", "ls -la", "dir"],
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DONDE_ESTOY_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["dónde estoy", "directorio actual", "ruta actual", "ubicación actual"],
        confianza_grounding=0.98,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
            "solo_lectura": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_PWD"},
        },
        operaciones=["pwd"],
    ))
    
    # ══════════ EJECUCIÓN DE CÓDIGO ═════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EJECUTAR_PYTHON_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["ejecutar python", "correr python", "run python", "evaluar código"],
        confianza_grounding=0.95,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
            "puede_fallar": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_PYTHON", "CONCEPTO_EJECUTAR"},
        },
        operaciones=["python", "python3", "exec"],
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CALCULAR_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["calcular", "computar", "resolver", "hacer cálculo"],
        confianza_grounding=0.95,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_SUMA", "CONCEPTO_RESTA", "CONCEPTO_MATH"},
        },
        operaciones=["eval", "python -c"],
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EJECUTAR_SCRIPT_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["ejecutar script", "correr script", "run script"],
        confianza_grounding=0.90,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
            "puede_fallar": True,
        },
        operaciones=["python script.py", "bash script.sh"],
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_IMPORTAR_MODULO_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["importar módulo", "cargar librería", "usar paquete"],
        confianza_grounding=0.90,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_IMPORT"},
        },
        operaciones=["import"],
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DEFINIR_FUNCION_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["definir función", "crear función", "hacer función"],
        confianza_grounding=0.90,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_FUNCION", "CONCEPTO_DEF"},
        },
        operaciones=["def"],
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INSTALAR_PAQUETE_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["instalar paquete", "pip install", "instalar librería"],
        confianza_grounding=0.85,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
            "modifica_sistema": True,
            "requiere_permisos": True,
        },
        operaciones=["pip install"],
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PROBAR_CODIGO_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["probar código", "testear", "verificar código", "correr tests"],
        confianza_grounding=0.90,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
        },
        operaciones=["pytest", "python -m pytest"],
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DEBUGGEAR_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["debuggear", "depurar", "encontrar error", "arreglar bug"],
        confianza_grounding=0.85,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
        },
        operaciones=["print", "pdb", "breakpoint"],
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FORMATEAR_CODIGO_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["formatear código", "limpiar código", "ordenar código"],
        confianza_grounding=0.90,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
        },
        operaciones=["black", "autopep8"],
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ANALIZAR_SINTAXIS_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["analizar sintaxis", "verificar sintaxis", "revisar código"],
        confianza_grounding=0.90,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
        },
        operaciones=["pylint", "flake8", "ast.parse"],
    ))
    
    # ══════════ ANÁLISIS Y BÚSQUEDA ═════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_BUSCAR_TEXTO_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["buscar texto", "encontrar texto", "grep", "buscar en archivo"],
        confianza_grounding=0.95,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
            "solo_lectura": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_GREP", "CONCEPTO_BUSCAR"},
        },
        operaciones=["grep", "grep -r"],
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CONTAR_LINEAS_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["contar líneas", "cuántas líneas", "número de líneas"],
        confianza_grounding=0.95,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
            "solo_lectura": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_WC"},
        },
        operaciones=["wc -l"],
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_VER_TAMANO_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["ver tamaño", "cuánto pesa", "tamaño de archivo", "espacio usado"],
        confianza_grounding=0.95,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
            "solo_lectura": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_DU", "CONCEPTO_DF"},
        },
        operaciones=["du -sh", "ls -lh"],
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_COMPARAR_ARCHIVOS_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["comparar archivos", "diferencias entre", "diff"],
        confianza_grounding=0.90,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
            "solo_lectura": True,
        },
        operaciones=["diff"],
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ORDENAR_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["ordenar", "sort", "organizar lista"],
        confianza_grounding=0.90,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
        },
        operaciones=["sort", "sorted()"],
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FILTRAR_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["filtrar", "filter", "seleccionar solo"],
        confianza_grounding=0.90,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
        },
        operaciones=["grep", "filter()", "awk"],
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EXTRAER_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["extraer", "sacar", "obtener datos de"],
        confianza_grounding=0.88,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
        },
        operaciones=["cut", "awk", "re.findall"],
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TRANSFORMAR_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["transformar", "convertir", "cambiar formato"],
        confianza_grounding=0.88,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
        },
        operaciones=["sed", "tr", "map()"],
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_VALIDAR_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["validar", "verificar", "comprobar", "checar"],
        confianza_grounding=0.90,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
        },
        operaciones=["assert", "isinstance", "validate"],
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PARSEAR_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["parsear", "analizar json", "leer json", "interpretar"],
        confianza_grounding=0.90,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_JSON"},
        },
        operaciones=["json.load", "json.loads", "ast.parse"],
    ))
    
    # ══════════ COMUNICACIÓN/OUTPUT ═════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MOSTRAR_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["mostrar", "imprimir", "print", "display", "enseñar"],
        confianza_grounding=0.98,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_PRINT", "CONCEPTO_ECHO"},
        },
        operaciones=["print", "echo"],
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EXPLICAR_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["explicar", "describir", "detallar", "aclarar"],
        confianza_grounding=0.85,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_EXPLICAR"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RESUMIR_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["resumir", "sintetizar", "hacer resumen"],
        confianza_grounding=0.85,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LISTAR_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["listar", "enumerar", "hacer lista"],
        confianza_grounding=0.90,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_COMPARAR_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["comparar", "contrastar", "qué diferencia hay"],
        confianza_grounding=0.85,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RECOMENDAR_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["recomendar", "sugerir", "aconsejar", "qué me recomiendas"],
        confianza_grounding=0.82,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_AYUDAR_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["ayudar", "asistir", "echar una mano", "ayúdame con"],
        confianza_grounding=0.90,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_AYUDA"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_GUARDAR_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["guardar", "save", "almacenar", "grabar"],
        confianza_grounding=0.92,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
            "modifica_sistema": True,
        },
        operaciones=["write", "save", "pickle.dump"],
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CARGAR_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["cargar", "load", "abrir datos", "recuperar"],
        confianza_grounding=0.92,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
        },
        operaciones=["open", "read", "pickle.load"],
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RECORDAR_ACCION",
        tipo=TipoConcepto.OPERACION_SISTEMA,
        palabras_español=["recordar", "memorizar", "tener en cuenta"],
        confianza_grounding=0.85,
        propiedades={
            "es_accion_digital": True,
            "bell_puede_ejecutar": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_MEMORIA"},
        },
    ))
    
    return conceptos


if __name__ == '__main__':
    conceptos = obtener_conceptos_acciones_digitales()
    grounding_prom = sum(c.confianza_grounding for c in conceptos) / len(conceptos)
    ejecutables = sum(1 for c in conceptos if len(c.operaciones) > 0)
    print(f"✅ Acciones Digitales: {len(conceptos)} conceptos")
    print(f"   Con operaciones: {ejecutables}")
    print(f"   Grounding promedio: {grounding_prom:.2f}")