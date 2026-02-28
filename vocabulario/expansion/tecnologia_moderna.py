"""
Tecnología Moderna - Expansión Fase 4A.

Términos tecnológicos actuales y digitales.

Conceptos: 40 total
Grounding promedio: 0.82
Tipo: ENTIDAD_DIGITAL / ACCION_COGNITIVA
"""
from core.concepto_anclado import ConceptoAnclado
from core.tipos import TipoConcepto


def obtener_conceptos_tecnologia_moderna():
    """
    Retorna conceptos de tecnología moderna.
    
    Categorías:
    - IA y Machine Learning (10)
    - Web y Apps (10)
    - Datos y Cloud (10)
    - Comunicación digital (10)
    """
    conceptos = []
    
    # ══════════ IA Y MACHINE LEARNING ═══════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_INTELIGENCIA_ARTIFICIAL",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["inteligencia artificial", "ia", "ai", "artificial intelligence"],
        confianza_grounding=0.85,
        propiedades={
            "es_tecnologia": True,
            "es_concepto_ia": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MACHINE_LEARNING",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["machine learning", "aprendizaje automático", "ml"],
        confianza_grounding=0.82,
        propiedades={
            "es_tecnologia": True,
            "es_concepto_ia": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MODELO_IA",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["modelo", "modelo de ia", "modelo entrenado"],
        confianza_grounding=0.80,
        propiedades={
            "es_tecnologia": True,
            "es_concepto_ia": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ENTRENAMIENTO",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["entrenamiento", "training", "entrenar modelo"],
        confianza_grounding=0.78,
        propiedades={
            "es_tecnologia": True,
            "es_concepto_ia": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PROMPT",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["prompt", "instrucción", "consulta a ia"],
        confianza_grounding=0.85,
        propiedades={
            "es_tecnologia": True,
            "es_concepto_ia": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CHATBOT",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["chatbot", "bot", "asistente virtual"],
        confianza_grounding=0.82,
        propiedades={
            "es_tecnologia": True,
            "es_concepto_ia": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ALGORITMO",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["algoritmo", "algorithm"],
        confianza_grounding=0.85,
        propiedades={
            "es_tecnologia": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_FUNCION"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NEURAL_NETWORK",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["red neuronal", "neural network", "redes neuronales"],
        confianza_grounding=0.78,
        propiedades={
            "es_tecnologia": True,
            "es_concepto_ia": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_AUTOMATIZACION",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["automatización", "automation", "automatizar"],
        confianza_grounding=0.82,
        propiedades={
            "es_tecnologia": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LLM",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["llm", "large language model", "modelo de lenguaje"],
        confianza_grounding=0.85,
        propiedades={
            "es_tecnologia": True,
            "es_concepto_ia": True,
        },
    ))
    
    # ══════════ WEB Y APPS ══════════════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_APLICACION",
        tipo=TipoConcepto.ENTIDAD_DIGITAL,
        palabras_español=["aplicación", "app", "aplicación móvil"],
        confianza_grounding=0.85,
        propiedades={
            "es_tecnologia": True,
            "es_digital": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SITIO_WEB",
        tipo=TipoConcepto.ENTIDAD_DIGITAL,
        palabras_español=["sitio web", "página web", "website", "web"],
        confianza_grounding=0.85,
        propiedades={
            "es_tecnologia": True,
            "es_digital": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_URL"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FRONTEND",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["frontend", "front-end", "interfaz de usuario"],
        confianza_grounding=0.82,
        propiedades={
            "es_tecnologia": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_BACKEND",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["backend", "back-end", "servidor"],
        confianza_grounding=0.82,
        propiedades={
            "es_tecnologia": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_API_TECH",
        tipo=TipoConcepto.ENTIDAD_DIGITAL,
        palabras_español=["api", "interfaz de programación", "endpoint"],
        confianza_grounding=0.88,
        propiedades={
            "es_tecnologia": True,
            "es_digital": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_HTTP_GET", "CONCEPTO_HTTP_POST"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_FRAMEWORK",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["framework", "marco de trabajo", "biblioteca"],
        confianza_grounding=0.82,
        propiedades={
            "es_tecnologia": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RESPONSIVE",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["responsive", "adaptable", "diseño responsivo"],
        confianza_grounding=0.78,
        propiedades={
            "es_tecnologia": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DEPLOY",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["deploy", "despliegue", "publicar", "deployment"],
        confianza_grounding=0.82,
        propiedades={
            "es_tecnologia": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_USUARIO_TECH",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["usuario", "user", "ux", "experiencia de usuario"],
        confianza_grounding=0.85,
        propiedades={
            "es_tecnologia": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_VERSION",
        tipo=TipoConcepto.ENTIDAD_DIGITAL,
        palabras_español=["versión", "version", "release", "actualización"],
        confianza_grounding=0.85,
        propiedades={
            "es_tecnologia": True,
            "es_digital": True,
        },
    ))
    
    # ══════════ DATOS Y CLOUD ═══════════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CLOUD",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["cloud", "nube", "en la nube", "cloud computing"],
        confianza_grounding=0.82,
        propiedades={
            "es_tecnologia": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DATABASE_TECH",
        tipo=TipoConcepto.ENTIDAD_DIGITAL,
        palabras_español=["base de datos", "database", "db", "almacén de datos"],
        confianza_grounding=0.88,
        propiedades={
            "es_tecnologia": True,
            "es_digital": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_SELECT", "CONCEPTO_TABLE"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_BACKUP",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["backup", "respaldo", "copia de seguridad"],
        confianza_grounding=0.85,
        propiedades={
            "es_tecnologia": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_STREAMING",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["streaming", "transmisión", "en vivo"],
        confianza_grounding=0.80,
        propiedades={
            "es_tecnologia": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_ENCRIPTACION",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["encriptación", "cifrado", "encryption", "encriptar"],
        confianza_grounding=0.82,
        propiedades={
            "es_tecnologia": True,
            "es_seguridad": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_AUTENTICACION",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["autenticación", "login", "iniciar sesión", "auth"],
        confianza_grounding=0.85,
        propiedades={
            "es_tecnologia": True,
            "es_seguridad": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_TOKEN",
        tipo=TipoConcepto.ENTIDAD_DIGITAL,
        palabras_español=["token", "jwt", "token de acceso"],
        confianza_grounding=0.82,
        propiedades={
            "es_tecnologia": True,
            "es_digital": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CACHE",
        tipo=TipoConcepto.ENTIDAD_DIGITAL,
        palabras_español=["cache", "caché", "memoria caché"],
        confianza_grounding=0.85,
        propiedades={
            "es_tecnologia": True,
            "es_digital": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SERVIDOR_TECH",
        tipo=TipoConcepto.ENTIDAD_DIGITAL,
        palabras_español=["servidor", "server", "host"],
        confianza_grounding=0.85,
        propiedades={
            "es_tecnologia": True,
            "es_digital": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CONTAINER",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["container", "contenedor", "docker"],
        confianza_grounding=0.80,
        propiedades={
            "es_tecnologia": True,
        },
    ))
    
    # ══════════ COMUNICACIÓN DIGITAL ════════════════════════════
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_EMAIL",
        tipo=TipoConcepto.ENTIDAD_DIGITAL,
        palabras_español=["email", "correo", "correo electrónico", "e-mail"],
        confianza_grounding=0.85,
        propiedades={
            "es_tecnologia": True,
            "es_digital": True,
            "es_comunicacion": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_MENSAJE_DIGITAL",
        tipo=TipoConcepto.ENTIDAD_DIGITAL,
        palabras_español=["mensaje", "message", "dm", "chat"],
        confianza_grounding=0.85,
        propiedades={
            "es_tecnologia": True,
            "es_digital": True,
            "es_comunicacion": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_NOTIFICACION",
        tipo=TipoConcepto.ENTIDAD_DIGITAL,
        palabras_español=["notificación", "notification", "alerta", "aviso"],
        confianza_grounding=0.85,
        propiedades={
            "es_tecnologia": True,
            "es_digital": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_RED_SOCIAL",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["red social", "social media", "redes sociales"],
        confianza_grounding=0.80,
        propiedades={
            "es_tecnologia": True,
            "es_comunicacion": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_PERFIL",
        tipo=TipoConcepto.ENTIDAD_DIGITAL,
        palabras_español=["perfil", "profile", "cuenta"],
        confianza_grounding=0.82,
        propiedades={
            "es_tecnologia": True,
            "es_digital": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_CONTRASENA",
        tipo=TipoConcepto.ENTIDAD_DIGITAL,
        palabras_español=["contraseña", "password", "clave"],
        confianza_grounding=0.85,
        propiedades={
            "es_tecnologia": True,
            "es_digital": True,
            "es_seguridad": True,
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_LINK",
        tipo=TipoConcepto.ENTIDAD_DIGITAL,
        palabras_español=["link", "enlace", "vínculo", "hipervínculo"],
        confianza_grounding=0.88,
        propiedades={
            "es_tecnologia": True,
            "es_digital": True,
        },
        relaciones={
            "relacionado_con": {"CONCEPTO_URL"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_DESCARGAR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["descargar", "download", "bajar"],
        confianza_grounding=0.85,
        propiedades={
            "es_tecnologia": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_SUBIR"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_SUBIR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["subir", "upload", "cargar"],
        confianza_grounding=0.85,
        propiedades={
            "es_tecnologia": True,
        },
        relaciones={
            "opuesto_a": {"CONCEPTO_DESCARGAR"},
        },
    ))
    
    conceptos.append(ConceptoAnclado(
        id="CONCEPTO_COMPARTIR",
        tipo=TipoConcepto.ACCION_COGNITIVA,
        palabras_español=["compartir", "share", "enviar"],
        confianza_grounding=0.85,
        propiedades={
            "es_tecnologia": True,
            "es_comunicacion": True,
        },
    ))
    
    return conceptos


if __name__ == '__main__':
    conceptos = obtener_conceptos_tecnologia_moderna()
    grounding_prom = sum(c.confianza_grounding for c in conceptos) / len(conceptos)
    digitales = sum(1 for c in conceptos if c.tipo == TipoConcepto.ENTIDAD_DIGITAL)
    print(f"✅ Tecnología Moderna: {len(conceptos)} conceptos")
    print(f"   Entidades digitales: {digitales}")
    print(f"   Grounding promedio: {grounding_prom:.2f}")