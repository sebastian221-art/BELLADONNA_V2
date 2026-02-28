"""
Objetos Comunes - Expansión Fase 4A.

Objetos cotidianos que Bell puede reconocer en conversación.

Conceptos: 80 total
Grounding promedio: 0.75

Tipos:
- ENTIDAD_DIGITAL: Objetos tecnológicos que Bell puede verificar/manipular
- ACCION_COGNITIVA: Objetos físicos que Bell entiende pero no manipula
"""
from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto


def obtener_conceptos_objetos_comunes():
    """
    Retorna objetos comunes.
    
    Categorías:
    - Tecnología digital (16 conceptos) - ENTIDAD_DIGITAL, grounding 0.85-0.95
    - Tecnología física (12 conceptos) - ACCION_COGNITIVA, grounding 0.65
    - Muebles/hogar (16 conceptos) - ACCION_COGNITIVA, grounding 0.65
    - Utensilios (16 conceptos) - ACCION_COGNITIVA, grounding 0.65
    - Ropa (12 conceptos) - ACCION_COGNITIVA, grounding 0.65
    - Transporte (8 conceptos) - ACCION_COGNITIVA, grounding 0.65
    """
    conceptos = []
    
    # ══════════ TECNOLOGÍA DIGITAL ══════════════════════════════
    # Bell PUEDE verificar, medir o interactuar con estos
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_COMPUTADORA",
        tipo=TipoConcepto.ENTIDAD_DIGITAL,
        palabras_español=["computadora", "ordenador", "pc", "computer"],
        confianza_grounding=0.90,
        propiedades={
            "es_digital": True,
            "bell_puede_verificar": True,
        },
        relaciones={
            "contiene": {"CONCEPTO_ARCHIVO", "CONCEPTO_DIRECTORIO", "CONCEPTO_PROCESO"},
            "relacionado_con": {"CONCEPTO_PROCESO_SHELL"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SERVIDOR",
        tipo=TipoConcepto.ENTIDAD_DIGITAL,
        palabras_español=["servidor", "server", "host"],
        confianza_grounding=0.88,
        propiedades={
            "es_digital": True,
            "bell_puede_verificar": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_URL", "CONCEPTO_HOSTNAME"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TERMINAL_OBJ",
        tipo=TipoConcepto.ENTIDAD_DIGITAL,
        palabras_español=["terminal", "consola", "shell", "cmd", "línea de comandos"],
        confianza_grounding=0.95,
        propiedades={
            "es_digital": True,
            "bell_puede_ejecutar": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_BASH", "CONCEPTO_EJECUTAR"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NAVEGADOR",
        tipo=TipoConcepto.ENTIDAD_DIGITAL,
        palabras_español=["navegador", "browser", "chrome", "firefox"],
        confianza_grounding=0.85,
        propiedades={
            "es_digital": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_URL", "CONCEPTO_HTTP_GET"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CARPETA_OBJ",
        tipo=TipoConcepto.ENTIDAD_DIGITAL,
        palabras_español=["carpeta", "folder"],
        confianza_grounding=0.95,
        propiedades={
            "es_digital": True,
            "bell_puede_verificar": True,
            "es_contenedor": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_DIRECTORIO", "CONCEPTO_MKDIR"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DOCUMENTO_OBJ",
        tipo=TipoConcepto.ENTIDAD_DIGITAL,
        palabras_español=["documento", "doc", "fichero"],
        confianza_grounding=0.90,
        propiedades={
            "es_digital": True,
            "bell_puede_verificar": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_ARCHIVO", "CONCEPTO_LEER"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PROGRAMA_OBJ",
        tipo=TipoConcepto.ENTIDAD_DIGITAL,
        palabras_español=["programa", "aplicación", "app", "software"],
        confianza_grounding=0.88,
        propiedades={
            "es_digital": True,
            "bell_puede_ejecutar": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_EJECUTAR", "CONCEPTO_PROCESO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CODIGO_OBJ",
        tipo=TipoConcepto.ENTIDAD_DIGITAL,
        palabras_español=["código", "script", "código fuente"],
        confianza_grounding=0.92,
        propiedades={
            "es_digital": True,
            "bell_puede_leer": True,
            "bell_puede_ejecutar": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_PYTHON", "CONCEPTO_EJECUTAR"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_BASE_DATOS_OBJ",
        tipo=TipoConcepto.ENTIDAD_DIGITAL,
        palabras_español=["base de datos", "database", "bd", "db"],
        confianza_grounding=0.90,
        propiedades={
            "es_digital": True,
            "bell_puede_consultar": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_SELECT", "CONCEPTO_TABLE"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DISCO_OBJ",
        tipo=TipoConcepto.ENTIDAD_DIGITAL,
        palabras_español=["disco duro", "disco", "ssd", "hard drive"],
        confianza_grounding=0.88,
        propiedades={
            "es_digital": True,
            "bell_puede_verificar": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_DISCO", "CONCEPTO_DF"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RED_OBJ",
        tipo=TipoConcepto.ENTIDAD_DIGITAL,
        palabras_español=["red", "network", "internet"],
        confianza_grounding=0.85,
        propiedades={
            "es_digital": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_CONEXION", "CONCEPTO_URL"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_USB_OBJ",
        tipo=TipoConcepto.ENTIDAD_DIGITAL,
        palabras_español=["usb", "pendrive", "memoria usb"],
        confianza_grounding=0.82,
        propiedades={
            "es_digital": True,
            "es_almacenamiento": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_DIRECTORIO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DATOS_OBJ",
        tipo=TipoConcepto.ENTIDAD_DIGITAL,
        palabras_español=["datos", "data", "información digital"],
        confianza_grounding=0.88,
        propiedades={
            "es_digital": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_VARIABLE", "CONCEPTO_JSON"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_WIFI",
        tipo=TipoConcepto.ENTIDAD_DIGITAL,
        palabras_español=["wifi", "wi-fi", "wireless"],
        confianza_grounding=0.82,
        propiedades={
            "es_digital": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_CONEXION"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PANTALLA_OBJ",
        tipo=TipoConcepto.ENTIDAD_DIGITAL,
        palabras_español=["pantalla", "monitor", "display", "screen"],
        confianza_grounding=0.85,
        propiedades={
            "es_digital": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_PRINT", "CONCEPTO_ECHO"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TECLADO_OBJ",
        tipo=TipoConcepto.ENTIDAD_DIGITAL,
        palabras_español=["teclado", "keyboard"],
        confianza_grounding=0.82,
        propiedades={
            "es_digital": True,
            "es_entrada": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_INPUT"},
        },
    ))
    
    # ══════════ TECNOLOGÍA FÍSICA ═══════════════════════════════
    # Bell entiende pero NO puede manipular
    
    tecnologia_fisica = [
        ("CONCEPTO_TELEFONO", ["teléfono", "celular", "móvil", "smartphone"]),
        ("CONCEPTO_TABLET", ["tablet", "tableta", "ipad"]),
        ("CONCEPTO_LAPTOP", ["laptop", "portátil", "notebook"]),
        ("CONCEPTO_CAMARA", ["cámara", "camera", "webcam"]),
        ("CONCEPTO_AUDIFONOS", ["audífonos", "auriculares", "headphones"]),
        ("CONCEPTO_CARGADOR", ["cargador", "charger"]),
        ("CONCEPTO_CABLE", ["cable", "cord", "wire"]),
        ("CONCEPTO_BATERIA", ["batería", "pila", "battery"]),
        ("CONCEPTO_ROUTER", ["router", "modem"]),
        ("CONCEPTO_IMPRESORA", ["impresora", "printer"]),
        ("CONCEPTO_TELEVISION", ["televisión", "tv", "tele"]),
        ("CONCEPTO_CONTROL_REMOTO", ["control remoto", "mando", "control"]),
    ]
    
    for id_c, palabras in tecnologia_fisica:
        conceptos.append(ConceptoAnclado(
            id=id_c,
            tipo=TipoConcepto.ACCION_COGNITIVA,
            palabras_español=palabras,
            confianza_grounding=0.65,
            propiedades={
                "es_tecnologia": True,
                "bell_puede_ejecutar": False,
                "requiere_cuerpo_fisico": True,
            },
        ))
    
    # ══════════ MUEBLES Y HOGAR ═════════════════════════════════
    
    hogar = [
        ("CONCEPTO_MESA", ["mesa", "escritorio", "table"]),
        ("CONCEPTO_SILLA", ["silla", "asiento", "banqueta"]),
        ("CONCEPTO_SOFA", ["sofá", "sillón", "couch"]),
        ("CONCEPTO_CAMA", ["cama", "litera", "bed"]),
        ("CONCEPTO_ARMARIO", ["armario", "closet", "ropero"]),
        ("CONCEPTO_ESTANTE", ["estante", "repisa", "shelf"]),
        ("CONCEPTO_LAMPARA", ["lámpara", "luz", "foco"]),
        ("CONCEPTO_VENTANA", ["ventana", "window"]),
        ("CONCEPTO_PUERTA", ["puerta", "door"]),
        ("CONCEPTO_ESPEJO", ["espejo", "mirror"]),
        ("CONCEPTO_REFRIGERADOR", ["refrigerador", "nevera", "heladera", "frigorífico"]),
        ("CONCEPTO_HORNO", ["horno", "microondas", "oven"]),
        ("CONCEPTO_LAVADORA", ["lavadora", "washing machine"]),
        ("CONCEPTO_COCINA_OBJ", ["cocina", "estufa", "stove"]),
        ("CONCEPTO_BANO_OBJ", ["baño", "bathroom"]),
        ("CONCEPTO_HABITACION", ["habitación", "cuarto", "room"]),
    ]
    
    for id_c, palabras in hogar:
        conceptos.append(ConceptoAnclado(
            id=id_c,
            tipo=TipoConcepto.ACCION_COGNITIVA,
            palabras_español=palabras,
            confianza_grounding=0.65,
            propiedades={
                "es_objeto_fisico": True,
                "bell_puede_ejecutar": False,
                "requiere_cuerpo_fisico": True,
            },
        ))
    
    # ══════════ UTENSILIOS ══════════════════════════════════════
    
    utensilios = [
        ("CONCEPTO_VASO", ["vaso", "copa", "taza"]),
        ("CONCEPTO_PLATO", ["plato", "platillo"]),
        ("CONCEPTO_CUCHARA", ["cuchara", "cucharita"]),
        ("CONCEPTO_TENEDOR", ["tenedor", "fork"]),
        ("CONCEPTO_CUCHILLO_OBJ", ["cuchillo", "navaja", "knife"]),
        ("CONCEPTO_OLLA", ["olla", "cacerola"]),
        ("CONCEPTO_SARTEN", ["sartén", "paila"]),
        ("CONCEPTO_BOTELLA", ["botella", "envase"]),
        ("CONCEPTO_CAJA", ["caja", "cajón", "box"]),
        ("CONCEPTO_BOLSA", ["bolsa", "bag"]),
        ("CONCEPTO_LLAVE_OBJ", ["llave", "key"]),
        ("CONCEPTO_TIJERAS", ["tijeras", "scissors"]),
        ("CONCEPTO_LAPIZ", ["lápiz", "pencil"]),
        ("CONCEPTO_BOLIGRAFO", ["bolígrafo", "pluma", "pen"]),
        ("CONCEPTO_PAPEL_OBJ", ["papel", "hoja", "paper"]),
        ("CONCEPTO_LIBRO", ["libro", "book"]),
    ]
    
    for id_c, palabras in utensilios:
        conceptos.append(ConceptoAnclado(
            id=id_c,
            tipo=TipoConcepto.ACCION_COGNITIVA,
            palabras_español=palabras,
            confianza_grounding=0.65,
            propiedades={
                "es_objeto_fisico": True,
                "bell_puede_ejecutar": False,
                "requiere_cuerpo_fisico": True,
            },
        ))
    
    # ══════════ ROPA ════════════════════════════════════════════
    
    ropa = [
        ("CONCEPTO_CAMISA", ["camisa", "blusa", "camiseta"]),
        ("CONCEPTO_PANTALON", ["pantalón", "jeans", "vaqueros"]),
        ("CONCEPTO_VESTIDO", ["vestido", "dress"]),
        ("CONCEPTO_CHAQUETA", ["chaqueta", "chamarra", "abrigo"]),
        ("CONCEPTO_ZAPATOS", ["zapatos", "shoes", "zapatillas"]),
        ("CONCEPTO_CALCETINES", ["calcetines", "medias", "socks"]),
        ("CONCEPTO_GORRA", ["gorra", "sombrero", "hat"]),
        ("CONCEPTO_GAFAS", ["gafas", "lentes", "anteojos"]),
        ("CONCEPTO_RELOJ_OBJ", ["reloj", "watch"]),
        ("CONCEPTO_CARTERA", ["cartera", "billetera", "wallet"]),
        ("CONCEPTO_MOCHILA", ["mochila", "backpack"]),
        ("CONCEPTO_CINTURON", ["cinturón", "belt"]),
    ]
    
    for id_c, palabras in ropa:
        conceptos.append(ConceptoAnclado(
            id=id_c,
            tipo=TipoConcepto.ACCION_COGNITIVA,
            palabras_español=palabras,
            confianza_grounding=0.65,
            propiedades={
                "es_objeto_fisico": True,
                "bell_puede_ejecutar": False,
                "requiere_cuerpo_fisico": True,
            },
        ))
    
    # ══════════ TRANSPORTE ══════════════════════════════════════
    
    transporte = [
        ("CONCEPTO_CARRO", ["carro", "coche", "auto", "car"]),
        ("CONCEPTO_BICICLETA", ["bicicleta", "bici", "bike"]),
        ("CONCEPTO_MOTO", ["moto", "motocicleta"]),
        ("CONCEPTO_AUTOBUS", ["autobús", "bus", "camión"]),
        ("CONCEPTO_TREN", ["tren", "metro", "train"]),
        ("CONCEPTO_AVION", ["avión", "plane"]),
        ("CONCEPTO_BARCO", ["barco", "bote", "ship"]),
        ("CONCEPTO_TAXI", ["taxi", "uber", "cab"]),
    ]
    
    for id_c, palabras in transporte:
        conceptos.append(ConceptoAnclado(
            id=id_c,
            tipo=TipoConcepto.ACCION_COGNITIVA,
            palabras_español=palabras,
            confianza_grounding=0.65,
            propiedades={
                "es_transporte": True,
                "bell_puede_ejecutar": False,
                "requiere_cuerpo_fisico": True,
            },
        ))
    
    return conceptos


if __name__ == '__main__':
    conceptos = obtener_conceptos_objetos_comunes()
    grounding_prom = sum(c.confianza_grounding for c in conceptos) / len(conceptos)
    digitales = sum(1 for c in conceptos if c.tipo == TipoConcepto.ENTIDAD_DIGITAL)
    print(f"✅ Objetos Comunes: {len(conceptos)} conceptos")
    print(f"   Digitales (ENTIDAD_DIGITAL): {digitales}")
    print(f"   Físicos (ACCION_COGNITIVA): {len(conceptos) - digitales}")
    print(f"   Grounding promedio: {grounding_prom:.2f}")