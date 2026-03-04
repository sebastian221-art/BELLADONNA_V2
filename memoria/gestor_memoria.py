"""
gestor_memoria.py — Memoria Narrativa y Episódica de Bell

UBICACIÓN: memoria/gestor_memoria.py
           (reemplaza el archivo actual — misma ubicación)

═══════════════════════════════════════════════════════════════════════
POR QUÉ SE REESCRIBIÓ
═══════════════════════════════════════════════════════════════════════
La versión v3 guardaba datos planos:
    self.datos_usuario = {'nombre': 'Sebastián', 'edad': '25'}

Eso no es memoria — es una ficha de datos.
Bell no puede decir "¿pasó algo con Sara?" con datos planos.
Bell no puede retomar el hilo de una conversación anterior.
Bell no puede saber que "eso" del turno 8 se refiere al grounding del turno 3.

La memoria real tiene TRES capas:
    Capa 1 — Sesión activa (RAM):
        Estado vivo: referentes, último tema, nombre a usar ahora mismo,
        lo que Bell preguntó, estado emocional actual.

    Capa 2 — Historia de la relación (JSON persistente):
        Episodios ordenados, modelos de personas (Sara, etc.),
        predicciones de Bell, temas abiertos entre sesiones.

    Capa 3 — Datos verificados (JSON persistente):
        Solo lo que Sebastián dijo explícitamente: nombre, edad, profesión.
        Certeza total. Ya existía en v3.

═══════════════════════════════════════════════════════════════════════
COMPATIBILIDAD GARANTIZADA CON TODO EL SISTEMA
═══════════════════════════════════════════════════════════════════════
Todos los métodos de v3 se mantienen con las MISMAS FIRMAS:

    generador_salida.py llama:
        mem.agregar_mensaje("usuario" | "bell", texto)     ✓ intacto
        mem.obtener_contexto_espera()                       ✓ intacto
        mem.limpiar_contexto_espera()                       ✓ intacto
        mem.obtener_contexto(n_mensajes=8)                  ✓ mejorado
        mem.el_usuario_se_llama()                           ✓ intacto
        mem.registrar_contexto_espera(tema, pregunta_bell)  ✓ intacto

    main.py (Belladonna) llama:
        self.gestor_memoria.iniciar_sesion()                ✓ intacto
        self.gestor_memoria.finalizar_sesion()              ✓ mejorado
        self.gestor_memoria.el_usuario_se_llama()           ✓ intacto
        self.gestor_memoria.guardar_concepto_usado(id, c)   ✓ intacto
        self.gestor_memoria.guardar_decision({...})         ✓ intacto
        self.gestor_memoria.obtener_datos_usuario()         ✓ intacto
        self.gestor_memoria.obtener_contexto(n_mensajes=6)  ✓ intacto

NUEVOS métodos (ninguno rompe nada existente):
    registrar_episodio()
    obtener_contexto_relevante()
    formatear_historia_para_prompt()
    actualizar_persona()
    obtener_persona()
    registrar_referente()
    resolver_referente()
    obtener_nombre_a_usar()
    hay_temas_abiertos()
    obtener_temas_pendientes()
    registrar_prediccion_bell()

═══════════════════════════════════════════════════════════════════════
SOBRE EL USO DE REGEX EN ESTE ARCHIVO
═══════════════════════════════════════════════════════════════════════
_extraer_datos_usuario() usa regex sobre texto crudo.
Esto ES compatible con el grounding porque:
    1. El motor_razonamiento.py hace exactamente lo mismo en
       _hechos_registro_usuario() — es el patrón establecido de Bell.
    2. El regex extrae datos ESTRUCTURADOS (nombre, edad, profesión)
       que tienen forma predecible en español.
    3. No hace razonamiento semántico — solo captura patrones fijos.
    4. Los resultados se guardan como hechos verificados (Capa 3),
       no como inferencias.

═══════════════════════════════════════════════════════════════════════
SOBRE LOS NUEVOS ARCHIVOS JSON
═══════════════════════════════════════════════════════════════════════
AlmacenJSON.archivos es un dict normal. En __init__ agregamos las
nuevas claves DINÁMICAMENTE sin tocar almacen.py:
    self.almacen.archivos['episodios_narrativos'] = Path(...)

AlmacenJSON.guardar() hace archivos.get(tipo) y retorna False si
la clave no existe. Al agregar las claves antes del primer uso,
todo funciona con el mecanismo existente.
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
import re

from memoria.almacen import AlmacenJSON
from memoria.tipos_memoria import (
    TipoMemoria,
    RegistroConcepto,
    RegistroDecision,
    RegistroPatron,
    RegistroInsight,
    RegistroAjuste,
    RegistroSesion,
)

# Importar sistema de nombres — sin dependencias circulares
try:
    from identidad_bell import obtener_nombre
    _IDENTIDAD_DISPONIBLE = True
except ImportError:
    _IDENTIDAD_DISPONIBLE = False


# ═══════════════════════════════════════════════════════════════════════
# FILTRO DE NOMBRES — igual que v3, preservado
# ═══════════════════════════════════════════════════════════════════════

_PALABRAS_EXCLUIDAS_NOMBRE = {
    # artículos
    'un', 'una', 'el', 'la', 'lo', 'los', 'las', 'unos', 'unas',
    # pronombres
    'yo', 'tu', 'tú', 'él', 'ella', 'mi', 'su', 'nos', 'vos',
    'me', 'te', 'se', 'le', 'les',
    # palabras comunes después de "soy" o "me llamo"
    'creador', 'usuario', 'humano', 'persona', 'hombre', 'mujer',
    'capaz', 'bueno', 'malo', 'nuevo', 'viejo', 'grande', 'pequeño',
    'feliz', 'triste', 'solo', 'aqui', 'aquí',
    # conectores y preposiciones
    'que', 'quien', 'cual', 'como', 'cuando', 'donde', 'para',
    'con', 'sin', 'por', 'de', 'del', 'al',
    # números escritos
    'uno', 'dos', 'tres', 'diez', 'veinte', 'cien',
}


class GestorMemoria:
    """
    Memoria narrativa y episódica de Bell.

    TRES capas de memoria:
        Capa 1 — Sesión activa (RAM):
            Estado vivo de la conversación: referentes activos, último tema,
            nombre a usar ahora mismo, lo que Bell preguntó.

        Capa 2 — Historia de la relación (JSON persistente):
            Episodios, personas conocidas, temas abiertos, predicciones de Bell.

        Capa 3 — Datos verificados (JSON persistente):
            Nombre, edad, profesión del usuario. Solo lo que dijo explícitamente.
    """

    # Claves en el almacén JSON — Capa 3 (existente)
    CLAVE_USUARIO = "usuario_persistente"

    # Claves en el almacén JSON — Capa 2 (nuevas)
    CLAVE_EPISODIOS    = "episodios_narrativos"
    CLAVE_PERSONAS     = "personas_conocidas"
    CLAVE_TEMAS        = "temas_abiertos"
    CLAVE_PREDICCIONES = "predicciones_bell"

    def __init__(self, directorio: str = "memoria_bell"):
        self.almacen = AlmacenJSON(directorio)

        # ── Registrar nuevos archivos JSON en AlmacenJSON ──────────────────
        # AlmacenJSON.archivos es un dict normal — podemos extenderlo
        # sin modificar almacen.py. guardar/cargar usan archivos.get(tipo).
        nuevos = {
            self.CLAVE_EPISODIOS:    "episodios_narrativos.json",
            self.CLAVE_PERSONAS:     "personas_conocidas.json",
            self.CLAVE_TEMAS:        "temas_abiertos.json",
            self.CLAVE_PREDICCIONES: "predicciones_bell.json",
        }
        for clave, nombre_archivo in nuevos.items():
            if clave not in self.almacen.archivos:
                self.almacen.archivos[clave] = (
                    self.almacen.directorio_base / nombre_archivo
                )

        self.sesion_actual: Optional[str] = None
        self.sesion_inicio: Optional[str] = None

        # ── Capa 1: Sesión activa en RAM ───────────────────────────────────
        self.historial_sesion: List[Dict[str, str]] = []
        self.datos_usuario: Dict[str, str] = {}

        # Estado vivo de la conversación (se resetea cada sesión)
        self._sesion: Dict[str, Any] = {
            "turno":                0,
            "tema_activo":          None,
            "temas_discutidos":     [],
            "ultima_pregunta_bell": None,
            "esperando_tema":       None,  # para resolver "sí"/"no"
            "referentes_activos":   {},    # {'eso': {'ref': 'grounding', 'turno': 3}}
            "estado_emocional":     "neutral",
            "nombre_a_usar":        "",
            "tipo_momento_actual":  "SOCIAL",
        }

        # ── Contexto de espera — compatibilidad v3 ─────────────────────────
        self.contexto_espera: Optional[Dict[str, str]] = None

        # ── Cache de personas en RAM ───────────────────────────────────────
        # Dict[nombre_str, Dict] — se carga desde JSON al iniciar sesión
        self._cache_personas: Dict[str, Dict] = {}

    # ═══════════════════════════════════════════════════════════════
    # SESIONES — Compatible v3
    # ═══════════════════════════════════════════════════════════════

    def iniciar_sesion(self) -> str:
        """
        Inicia una nueva sesión.
        Carga datos del usuario y personas conocidas desde sesiones anteriores.
        """
        self.sesion_actual = str(uuid.uuid4())
        self.sesion_inicio = datetime.now().isoformat()

        # Carga desde disco (Capa 3 y Capa 2)
        self.cargar_datos_usuario()
        self._cargar_personas_cache()

        # Actualizar nombre a usar con lo que ya sabemos
        if self.datos_usuario.get("nombre"):
            self._actualizar_nombre_a_usar("SOCIAL")

        sesion: RegistroSesion = {
            "id_sesion":           self.sesion_actual,
            "inicio":              self.sesion_inicio,
            "fin":                 None,
            "mensajes_procesados": 0,
            "decisiones_tomadas":  0,
            "conceptos_usados":    0,
            "patrones_detectados": 0,
        }
        self.almacen.guardar("sesiones", sesion)
        return self.sesion_actual

    def finalizar_sesion(self):
        """
        Finaliza la sesión. Guarda datos del usuario en disco.
        """
        if not self.sesion_actual:
            return

        self.guardar_datos_usuario()

        sesiones = self.almacen.cargar("sesiones")
        for s in sesiones:
            if s["id_sesion"] == self.sesion_actual:
                s["fin"] = datetime.now().isoformat()
                break
        self.almacen.limpiar("sesiones")
        for s in sesiones:
            self.almacen.guardar("sesiones", s)

        self.sesion_actual = None
        self.sesion_inicio = None

    def _actualizar_contador_sesion(self, campo: str):
        if not self.sesion_actual:
            return
        sesiones = self.almacen.cargar("sesiones")
        for s in sesiones:
            if s["id_sesion"] == self.sesion_actual:
                s[campo] = s.get(campo, 0) + 1
                break
        self.almacen.limpiar("sesiones")
        for s in sesiones:
            self.almacen.guardar("sesiones", s)

    # ═══════════════════════════════════════════════════════════════
    # CAPA 3: DATOS VERIFICADOS — Compatible v3
    # ═══════════════════════════════════════════════════════════════

    def guardar_datos_usuario(self):
        """Persiste datos verificados del usuario en disco."""
        if not self.datos_usuario:
            return
        try:
            self.almacen.limpiar(self.CLAVE_USUARIO)
            self.almacen.guardar(self.CLAVE_USUARIO, self.datos_usuario)
        except Exception:
            pass

    def cargar_datos_usuario(self):
        """Recupera datos verificados desde disco."""
        try:
            registros = self.almacen.cargar(self.CLAVE_USUARIO)
            if registros:
                self.datos_usuario = registros[-1]
        except Exception:
            pass

    def el_usuario_se_llama(self) -> str:
        """
        Retorna el nombre del usuario o '' si no se conoce.
        Compatible v3 — puede venir de sesiones anteriores.
        """
        return self.datos_usuario.get("nombre", "")

    def obtener_datos_usuario(self) -> Dict[str, str]:
        """Retorna todos los datos verificados del usuario."""
        return dict(self.datos_usuario)

    # ═══════════════════════════════════════════════════════════════
    # CONVERSACIÓN EN RAM — Mejorado sobre v3
    # ═══════════════════════════════════════════════════════════════

    def agregar_mensaje(self, rol: str, mensaje: str):
        """
        Registra un turno de conversación en RAM.

        Args:
            rol:     'usuario' | 'bell'
            mensaje: Texto del turno

        Compatible v3: misma firma, mismo comportamiento base.
        Mejora: incrementa turno, detecta personas ya conocidas.
        """
        self._sesion["turno"] += 1

        self.historial_sesion.append({
            "rol":       rol,
            "mensaje":   mensaje,
            "timestamp": datetime.now().isoformat(),
            "turno":     self._sesion["turno"],
        })

        if rol == "usuario":
            self._extraer_datos_usuario(mensaje)
            self._detectar_referencias_personas(mensaje)
        elif rol == "bell":
            # Si Bell termina con pregunta, registrar
            if mensaje.rstrip().endswith("?"):
                self._sesion["ultima_pregunta_bell"] = mensaje

        # Mantener solo los últimos 30 turnos
        if len(self.historial_sesion) > 30:
            self.historial_sesion = self.historial_sesion[-30:]

    def _extraer_datos_usuario(self, mensaje: str):
        """
        Extrae datos estructurados del usuario mientras conversa.

        USA REGEX — compatible con el grounding porque:
        - El motor hace lo mismo en _hechos_registro_usuario()
        - Captura patrones fijos del español, no significado semántico
        - Los resultados son hechos verificados, no inferencias

        Compatible v3: misma lógica, mismos patrones.
        Mejora v3: también extrae profesión.
        """
        mensaje_lower = mensaje.lower().strip()

        # ── Nombre ─────────────────────────────────────────────────────────
        if "nombre" not in self.datos_usuario:
            patron_nombre = (
                r"(?:mi nombre es|me llamo|soy|puedes llamarme|llámame|llamame)"
                r"\s+([a-záéíóúüñ]+)"
            )
            match = re.search(patron_nombre, mensaje_lower)
            if match:
                nombre_raw = match.group(1).strip()
                if (
                    len(nombre_raw) >= 3
                    and nombre_raw not in _PALABRAS_EXCLUIDAS_NOMBRE
                    and not nombre_raw.isdigit()
                ):
                    self.datos_usuario["nombre"] = nombre_raw.capitalize()
                    # Actualizar nombre a usar con el tipo actual
                    self._actualizar_nombre_a_usar(
                        self._sesion.get("tipo_momento_actual", "SOCIAL")
                    )

        # ── Edad — igual que v3 ─────────────────────────────────────────────
        if "edad" not in self.datos_usuario:
            match_edad = re.search(r"tengo\s+(\d+)\s+años", mensaje_lower)
            if match_edad:
                edad = int(match_edad.group(1))
                if 1 <= edad <= 120:
                    self.datos_usuario["edad"] = str(edad)

        # ── Profesión — nuevo ───────────────────────────────────────────────
        if "profesion" not in self.datos_usuario:
            patron_prof = (
                r"(?:trabajo como|me dedico a|soy)\s+"
                r"([a-záéíóúüñ\s]+?)(?:\s+en|\s+de|\.|,|$)"
            )
            match_prof = re.search(patron_prof, mensaje_lower)
            if match_prof:
                prof = match_prof.group(1).strip()
                if (
                    len(prof) >= 4
                    and prof.split()[0] not in _PALABRAS_EXCLUIDAS_NOMBRE
                ):
                    self.datos_usuario["profesion"] = prof

    def obtener_contexto(self, n_mensajes: int = 8) -> str:
        """
        Retorna los últimos N turnos como string para Groq.

        Compatible v3: misma firma, mismos defaults.
        Mejora: usa el nombre real del usuario para etiquetar sus turnos.

        Args:
            n_mensajes: Cuántos mensajes incluir (default 8 igual que v3)

        Returns:
            String con el historial formateado.
        """
        if not self.historial_sesion:
            return "Sin conversación previa en esta sesión."

        nombre = self.datos_usuario.get("nombre", "Usuario")
        ultimos = self.historial_sesion[-n_mensajes:]
        lineas = []
        for msg in ultimos:
            rol_display = nombre if msg["rol"] == "usuario" else "Bell"
            texto = msg["mensaje"][:200]  # truncar mensajes muy largos
            lineas.append(f"{rol_display}: {texto}")
        return "\n".join(lineas)

    # ═══════════════════════════════════════════════════════════════
    # CONTEXTO DE ESPERA — Compatible v3, sin cambios en la firma
    # ═══════════════════════════════════════════════════════════════

    def registrar_contexto_espera(self, tema: str, pregunta_bell: str):
        """
        Bell hizo una pregunta y espera confirmación.

        Cuando el usuario responde "sí"/"no"/"dale", el generador
        puede recuperar este contexto para saber A QUÉ está respondiendo.

        Compatible v3: misma firma, mismo comportamiento.
        """
        self.contexto_espera = {
            "tema":          tema,
            "pregunta_bell": pregunta_bell,
            "timestamp":     datetime.now().isoformat(),
        }
        self._sesion["esperando_tema"]       = tema
        self._sesion["ultima_pregunta_bell"] = pregunta_bell

    def obtener_contexto_espera(self) -> Optional[Dict[str, str]]:
        """Retorna el contexto de espera activo, o None. Compatible v3."""
        return self.contexto_espera

    def limpiar_contexto_espera(self):
        """Limpia el contexto de espera después de procesarlo. Compatible v3."""
        self.contexto_espera = None
        self._sesion["esperando_tema"] = None

    # ═══════════════════════════════════════════════════════════════
    # CAPA 1: ESTADO VIVO — NUEVO
    # El motor puede actualizar esto después de cada decisión
    # ═══════════════════════════════════════════════════════════════

    def actualizar_estado_sesion(
        self,
        tema_activo:     Optional[str] = None,
        estado_emocional: Optional[str] = None,
        tipo_momento:    Optional[str] = None,
    ):
        """
        Actualiza el estado vivo de la conversación.

        El motor_razonamiento puede llamar esto después de clasificar
        cada intención para mantener el estado coherente.

        Args:
            tema_activo:      TipoDecision.name del momento actual
            estado_emocional: emoción detectada ("neutral", "frustrado", etc.)
            tipo_momento:     mismo que tema_activo, para el sistema de nombres
        """
        if tema_activo:
            if tema_activo not in self._sesion["temas_discutidos"]:
                self._sesion["temas_discutidos"].append(tema_activo)
            self._sesion["tema_activo"] = tema_activo
            # Actualizar referente "eso" para que apunte al tema activo
            self.registrar_referente("eso", tema_activo)
            self.registrar_referente("esto", tema_activo)

        if estado_emocional:
            self._sesion["estado_emocional"] = estado_emocional

        if tipo_momento:
            self._sesion["tipo_momento_actual"] = tipo_momento
            self._actualizar_nombre_a_usar(tipo_momento)

    def _actualizar_nombre_a_usar(self, tipo_momento: str):
        """Actualiza qué nombre usar según el tipo de momento."""
        nombre_base = self.datos_usuario.get("nombre", "")
        if not nombre_base:
            self._sesion["nombre_a_usar"] = ""
            return

        if _IDENTIDAD_DISPONIBLE:
            self._sesion["nombre_a_usar"] = obtener_nombre(tipo_momento, nombre_base)
        else:
            # Fallback si identidad_bell no está disponible
            partes = nombre_base.strip().split()
            self._sesion["nombre_a_usar"] = partes[0] if partes else nombre_base

    def obtener_nombre_a_usar(self, tipo_momento: Optional[str] = None) -> str:
        """
        Devuelve el nombre correcto para usar ahora mismo.

        Args:
            tipo_momento: Si se pasa, actualiza antes de devolver.

        Returns:
            "Sebas", "Sebastián", "Juan Sebastián", o ""
        """
        if tipo_momento:
            self._actualizar_nombre_a_usar(tipo_momento)
        return self._sesion.get("nombre_a_usar", "")

    def obtener_estado_sesion(self) -> Dict[str, Any]:
        """Devuelve copia del estado vivo de la sesión."""
        return dict(self._sesion)

    # ═══════════════════════════════════════════════════════════════
    # REFERENCIAS DÉICTICAS — NUEVO
    # Resolver "eso", "ella", "lo de antes" a su referente real
    # ═══════════════════════════════════════════════════════════════

    def registrar_referente(self, palabra: str, referente: str):
        """
        Registra a qué apunta una palabra déictica.

        Ejemplos:
            registrar_referente("eso", "grounding computacional")
            registrar_referente("ella", "Sara")

        Args:
            palabra:   La palabra déictica ("eso", "ella", "lo")
            referente: A qué se refiere concretamente
        """
        self._sesion["referentes_activos"][palabra.lower()] = {
            "referente": referente,
            "turno":     self._sesion["turno"],
        }

    def resolver_referente(self, palabra: str) -> Optional[str]:
        """
        Resuelve a qué apunta una palabra déictica.

        Busca en este orden:
        1. Referentes activos registrados explícitamente
        2. Contexto de espera (para "sí"/"no")
        3. Último tema activo (para "eso", "esto")
        4. Última persona por género (para "ella", "él")

        Returns:
            El referente concreto, o None si no se puede resolver.
        """
        palabra_lower = palabra.lower().strip()

        # 1. Búsqueda directa — solo válida si es reciente (últimos 10 turnos)
        if palabra_lower in self._sesion["referentes_activos"]:
            ref_info = self._sesion["referentes_activos"][palabra_lower]
            if self._sesion["turno"] - ref_info["turno"] <= 10:
                return ref_info["referente"]

        # 2. Confirmaciones — apuntan a lo que Bell preguntó
        if palabra_lower in ("sí", "si", "dale", "claro", "ok", "sip", "adelante"):
            return (
                self._sesion.get("esperando_tema")
                or self._sesion.get("ultima_pregunta_bell")
            )

        # 3. Pronombres neutros — apuntan al tema activo
        if palabra_lower in ("eso", "esto", "lo", "aquello", "lo de antes"):
            return self._sesion.get("tema_activo")

        # 4. Pronombres de persona — buscar por género en cache
        if palabra_lower in ("ella", "esa"):
            for nombre, datos in self._cache_personas.items():
                if datos.get("genero") == "femenino":
                    return nombre

        if palabra_lower in ("él", "el", "ese"):
            for nombre, datos in self._cache_personas.items():
                if datos.get("genero") == "masculino":
                    return nombre

        return None

    # ═══════════════════════════════════════════════════════════════
    # CAPA 2: EPISODIOS NARRATIVOS — NUEVO
    # ═══════════════════════════════════════════════════════════════

    def registrar_episodio(
        self,
        resumen: str,
        tema_principal: str,
        personas_mencionadas: Optional[List[str]] = None,
        estado_emocional_usuario: str = "neutral",
        decision_tomada: Optional[str] = None,
        prediccion_bell: Optional[str] = None,
        temas_abiertos_generados: Optional[List[str]] = None,
    ):
        """
        Registra un episodio significativo en la historia narrativa.

        No todos los mensajes son episodios — solo los que importan:
        - Cuando se menciona una persona nueva con novedad
        - Cuando se toma una decisión importante
        - Cuando se revela algo personal significativo
        - Cuando Bell hace una predicción

        Args:
            resumen:                   Descripción en lenguaje natural
            tema_principal:            Categoría del episodio
            personas_mencionadas:      Nombres involucrados
            estado_emocional_usuario:  Estado detectado del usuario
            decision_tomada:           Si hubo una decisión concreta
            prediccion_bell:           Qué predice Bell que va a pasar
            temas_abiertos_generados:  Qué quedó pendiente para retomar
        """
        episodio = {
            "id":                       f"ep_{str(uuid.uuid4())[:8]}",
            "fecha":                    datetime.now().isoformat(),
            "sesion_id":                self.sesion_actual,
            "resumen":                  resumen,
            "tema_principal":           tema_principal,
            "personas_mencionadas":     personas_mencionadas or [],
            "estado_emocional_usuario": estado_emocional_usuario,
            "decision_tomada":          decision_tomada,
            "prediccion_bell":          prediccion_bell,
            "temas_abiertos":           temas_abiertos_generados or [],
        }
        self.almacen.guardar(self.CLAVE_EPISODIOS, episodio)

        # Registrar temas abiertos que genere este episodio
        if temas_abiertos_generados:
            for tema in temas_abiertos_generados:
                self._registrar_tema_abierto(tema, episodio["id"])

        # Registrar predicción si la hay
        if prediccion_bell:
            self.registrar_prediccion_bell(
                prediccion_bell, tema_principal, episodio["id"]
            )

    def obtener_contexto_relevante(self, tema_actual: str) -> Dict[str, Any]:
        """
        Recupera la historia relevante para el tema actual.

        No busca por keyword exacta — busca por similitud temática
        comparando palabras del tema con los episodios guardados.

        Returns:
            {
                'episodios':    List[Dict],  # Hasta 3 más relevantes
                'personas':     Dict[str, Dict],  # Personas relevantes
                'pendientes':   List[Dict],  # Temas abiertos relacionados
                'tiene_historia': bool
            }
        """
        episodios_todos = self.almacen.cargar(self.CLAVE_EPISODIOS)
        temas_todos     = self.almacen.cargar(self.CLAVE_TEMAS)

        tema_lower  = tema_actual.lower()
        palabras_tema = set(tema_lower.replace("_", " ").split())

        # Puntuar episodios por relevancia
        episodios_relevantes = []
        nombres_relevantes   = set()

        for ep in episodios_todos:
            score = 0
            tema_ep    = ep.get("tema_principal", "").lower()
            resumen_ep = ep.get("resumen", "").lower()
            personas_ep = [p.lower() for p in ep.get("personas_mencionadas", [])]

            for palabra in palabras_tema:
                if len(palabra) > 2:  # ignorar palabras cortas
                    if palabra in tema_ep:
                        score += 3
                    if palabra in resumen_ep:
                        score += 1
            for persona in personas_ep:
                if persona in tema_lower:
                    score += 2

            if score > 0:
                episodios_relevantes.append((score, ep))
                for p in ep.get("personas_mencionadas", []):
                    nombres_relevantes.add(p)

        episodios_relevantes.sort(key=lambda x: x[0], reverse=True)
        top_episodios = [ep for _, ep in episodios_relevantes[:3]]

        # Personas relevantes desde el cache
        personas_en_contexto = {}
        for nombre, datos in self._cache_personas.items():
            if nombre in nombres_relevantes or nombre.lower() in tema_lower:
                personas_en_contexto[nombre] = datos

        # Temas abiertos relacionados
        pendientes = []
        for tema in temas_todos:
            if not tema.get("resuelto", False):
                desc = tema.get("descripcion", "").lower()
                if (
                    tema_lower in desc
                    or any(p.lower() in desc for p in nombres_relevantes)
                ):
                    pendientes.append(tema)

        return {
            "episodios":    top_episodios,
            "personas":     personas_en_contexto,
            "pendientes":   pendientes[:3],
            "tiene_historia": bool(top_episodios or personas_en_contexto),
        }

    def formatear_historia_para_prompt(self, tema_actual: str) -> str:
        """
        Formatea el contexto relevante como texto para el prompt de Groq.

        prompts_naturales.py puede llamar esto para incluir historia
        real en el system prompt antes de llamar a Groq.

        Returns:
            String con la historia relevante, o "" si no hay.
        """
        contexto = self.obtener_contexto_relevante(tema_actual)

        if not contexto["tiene_historia"]:
            return ""

        partes = []

        if contexto["episodios"]:
            partes.append("HISTORIA RELEVANTE:")
            for ep in contexto["episodios"]:
                partes.append(f"  - {ep['resumen']}")
                if ep.get("decision_tomada"):
                    partes.append(f"    (decisión: {ep['decision_tomada']})")
                if ep.get("prediccion_bell"):
                    partes.append(f"    (Bell predijo: {ep['prediccion_bell']})")

        if contexto["personas"]:
            partes.append("PERSONAS CONOCIDAS:")
            for nombre, datos in contexto["personas"].items():
                historial = datos.get("historial", [])
                if historial:
                    partes.append(f"  - {nombre}: {historial[-1]}")

        if contexto["pendientes"]:
            partes.append("TEMAS PENDIENTES:")
            for tema in contexto["pendientes"]:
                partes.append(f"  - {tema.get('descripcion', '')}")

        return "\n".join(partes)

    # ═══════════════════════════════════════════════════════════════
    # PERSONAS CONOCIDAS — NUEVO
    # Modelo mental de las personas en la vida de Sebastián
    # ═══════════════════════════════════════════════════════════════

    def _cargar_personas_cache(self):
        """Carga las personas conocidas al iniciar sesión."""
        try:
            registros = self.almacen.cargar(self.CLAVE_PERSONAS)
            for r in registros:
                nombre = r.get("nombre", "")
                if nombre:
                    self._cache_personas[nombre] = r
                    # Restaurar referentes déicticos por género
                    if r.get("genero") == "femenino":
                        self.registrar_referente("ella", nombre)
                    elif r.get("genero") == "masculino":
                        self.registrar_referente("él", nombre)
        except Exception:
            pass

    def actualizar_persona(
        self,
        nombre: str,
        nueva_info: str,
        contexto_relacion: str = "",
        genero: Optional[str] = None,
    ):
        """
        Actualiza el modelo de una persona en la vida de Sebastián.

        El historial de cada persona crece con el tiempo. Bell puede
        ver toda la trayectoria de Sara, de un compañero de trabajo, etc.

        Args:
            nombre:            Nombre de la persona
            nueva_info:        Nueva información a agregar al historial
            contexto_relacion: "amistad", "trabajo", "romantico", etc.
            genero:            "masculino", "femenino", o None
        """
        if nombre not in self._cache_personas:
            self._cache_personas[nombre] = {
                "nombre":          nombre,
                "contexto":        contexto_relacion,
                "genero":          genero,
                "historial":       [],
                "primera_mencion": datetime.now().isoformat(),
            }

        persona = self._cache_personas[nombre]
        persona["historial"].append(nueva_info)
        persona["ultima_actualizacion"] = datetime.now().isoformat()

        if genero and not persona.get("genero"):
            persona["genero"] = genero
        if contexto_relacion and not persona.get("contexto"):
            persona["contexto"] = contexto_relacion

        # Actualizar referentes déicticos
        if persona.get("genero") == "femenino":
            self.registrar_referente("ella", nombre)
            self.registrar_referente("esa", nombre)
        elif persona.get("genero") == "masculino":
            self.registrar_referente("él", nombre)
            self.registrar_referente("ese", nombre)

        # Persistir en disco
        try:
            personas_existentes = self.almacen.cargar(self.CLAVE_PERSONAS)
            encontrado = False
            for i, p in enumerate(personas_existentes):
                if p.get("nombre") == nombre:
                    personas_existentes[i] = persona
                    encontrado = True
                    break
            if not encontrado:
                personas_existentes.append(persona)

            self.almacen.limpiar(self.CLAVE_PERSONAS)
            for p in personas_existentes:
                self.almacen.guardar(self.CLAVE_PERSONAS, p)
        except Exception:
            pass

    def obtener_persona(self, nombre: str) -> Optional[Dict]:
        """Devuelve el modelo completo de una persona, o None."""
        return self._cache_personas.get(nombre)

    def _detectar_referencias_personas(self, mensaje: str):
        """
        Detecta si el usuario menciona a alguien ya conocido.

        SOLO busca nombres que ya están en el cache — no descubre
        nombres nuevos. Descubrir nombres nuevos es tarea del motor.
        """
        for nombre, datos in self._cache_personas.items():
            if nombre.lower() in mensaje.lower():
                # Refrescar referentes déicticos
                genero = datos.get("genero")
                if genero == "femenino":
                    self.registrar_referente("ella", nombre)
                elif genero == "masculino":
                    self.registrar_referente("él", nombre)
                self.registrar_referente(nombre.lower(), nombre)

    # ═══════════════════════════════════════════════════════════════
    # TEMAS ABIERTOS — NUEVO
    # ═══════════════════════════════════════════════════════════════

    def _registrar_tema_abierto(self, descripcion: str, episodio_origen: str):
        """Registra un tema que quedó pendiente para retomar."""
        tema = {
            "id":              str(uuid.uuid4())[:8],
            "descripcion":     descripcion,
            "episodio_origen": episodio_origen,
            "fecha":           datetime.now().isoformat(),
            "resuelto":        False,
        }
        self.almacen.guardar(self.CLAVE_TEMAS, tema)

    def hay_temas_abiertos(self) -> bool:
        """¿Hay conversaciones pendientes que Bell debería retomar?"""
        try:
            temas = self.almacen.cargar(self.CLAVE_TEMAS)
            return any(not t.get("resuelto", False) for t in temas)
        except Exception:
            return False

    def obtener_temas_pendientes(self, n: int = 3) -> List[Dict]:
        """Retorna los N temas abiertos más recientes."""
        try:
            temas = self.almacen.cargar(self.CLAVE_TEMAS)
            pendientes = [t for t in temas if not t.get("resuelto", False)]
            return pendientes[-n:]
        except Exception:
            return []

    def marcar_tema_resuelto(self, tema_id: str):
        """Marca un tema como resuelto."""
        try:
            temas = self.almacen.cargar(self.CLAVE_TEMAS)
            for t in temas:
                if t.get("id") == tema_id:
                    t["resuelto"] = True
                    t["fecha_resolucion"] = datetime.now().isoformat()
                    break
            self.almacen.limpiar(self.CLAVE_TEMAS)
            for t in temas:
                self.almacen.guardar(self.CLAVE_TEMAS, t)
        except Exception:
            pass

    # ═══════════════════════════════════════════════════════════════
    # PREDICCIONES DE BELL — NUEVO
    # Bell predice, luego puede verificar si se cumplió
    # ═══════════════════════════════════════════════════════════════

    def registrar_prediccion_bell(
        self,
        prediccion: str,
        tema: str,
        episodio_origen: Optional[str] = None,
    ):
        """
        Bell hizo una predicción que puede verificar en el futuro.
        Ejemplo: "predije que iba a salir bien con Sara".
        """
        pred = {
            "id":              str(uuid.uuid4())[:8],
            "prediccion":      prediccion,
            "tema":            tema,
            "episodio_origen": episodio_origen,
            "fecha":           datetime.now().isoformat(),
            "verificada":      False,
            "resultado":       None,
        }
        self.almacen.guardar(self.CLAVE_PREDICCIONES, pred)

    def obtener_predicciones_tema(self, tema: str) -> List[Dict]:
        """Devuelve predicciones de Bell sobre un tema específico."""
        try:
            preds = self.almacen.cargar(self.CLAVE_PREDICCIONES)
            return [p for p in preds if tema.lower() in p.get("tema", "").lower()]
        except Exception:
            return []

    # ═══════════════════════════════════════════════════════════════
    # CONCEPTOS — Compatible v3, sin cambios
    # ═══════════════════════════════════════════════════════════════

    def guardar_concepto_usado(self, concepto_id: str, certeza: float = 0.0):
        registro: RegistroConcepto = {
            "concepto_id":    concepto_id,
            "timestamp":      datetime.now().isoformat(),
            "veces_usado":    1,
            "ultima_certeza": certeza,
        }
        self.almacen.guardar("conceptos", registro)
        self._actualizar_contador_sesion("conceptos_usados")

    def obtener_conceptos_mas_usados(self, n: int = 10) -> List[Dict[str, Any]]:
        conceptos = self.almacen.cargar("conceptos")
        conteo: Dict[str, Dict[str, Any]] = {}
        for r in conceptos:
            cid = r["concepto_id"]
            if cid not in conteo:
                conteo[cid] = {"concepto_id": cid, "usos": 0, "ultimo_uso": r["timestamp"]}
            conteo[cid]["usos"] += r["veces_usado"]
            conteo[cid]["ultimo_uso"] = max(conteo[cid]["ultimo_uso"], r["timestamp"])
        return sorted(conteo.values(), key=lambda x: x["usos"], reverse=True)[:n]

    # ═══════════════════════════════════════════════════════════════
    # DECISIONES — Compatible v3, sin cambios
    # ═══════════════════════════════════════════════════════════════

    def guardar_decision(self, decision_info: Dict[str, Any]):
        registro: RegistroDecision = {
            "timestamp":             datetime.now().isoformat(),
            "tipo":                  decision_info.get("tipo", "DESCONOCIDO"),
            "puede_ejecutar":        decision_info.get("puede_ejecutar", False),
            "certeza":               decision_info.get("certeza", 0.0),
            "conceptos_principales": decision_info.get("conceptos_principales", []),
            "grounding_promedio":    decision_info.get("grounding_promedio", 0.0),
        }
        self.almacen.guardar("decisiones", registro)
        self._actualizar_contador_sesion("decisiones_tomadas")

    def obtener_decisiones_recientes(self, n: int = 20) -> List[RegistroDecision]:
        return self.almacen.cargar("decisiones")[-n:]

    def obtener_estadisticas_decisiones(self) -> Dict[str, Any]:
        decisiones = self.almacen.cargar("decisiones")
        if not decisiones:
            return {"total": 0, "tasa_ejecucion": 0.0, "certeza_promedio": 0.0, "tipos": {}}
        ejecutables = sum(1 for d in decisiones if d["puede_ejecutar"])
        certezas    = [d["certeza"] for d in decisiones]
        tipos: Dict[str, int] = {}
        for d in decisiones:
            tipos[d["tipo"]] = tipos.get(d["tipo"], 0) + 1
        return {
            "total":            len(decisiones),
            "tasa_ejecucion":   (ejecutables / len(decisiones)) * 100,
            "certeza_promedio": sum(certezas) / len(certezas),
            "tipos":            tipos,
        }

    # ═══════════════════════════════════════════════════════════════
    # PATRONES — Compatible v3, sin cambios
    # ═══════════════════════════════════════════════════════════════

    def guardar_patron(self, patron_info: Dict[str, Any]):
        registro: RegistroPatron = {
            "timestamp":   datetime.now().isoformat(),
            "tipo_patron": patron_info.get("tipo", "DESCONOCIDO"),
            "descripcion": patron_info.get("descripcion", ""),
            "frecuencia":  patron_info.get("frecuencia", 0),
            "confianza":   patron_info.get("confianza", 0.0),
        }
        self.almacen.guardar("patrones", registro)
        self._actualizar_contador_sesion("patrones_detectados")

    def obtener_patrones_recientes(self, n: int = 10) -> List[RegistroPatron]:
        return self.almacen.cargar("patrones")[-n:]

    # ═══════════════════════════════════════════════════════════════
    # INSIGHTS — Compatible v3, sin cambios
    # ═══════════════════════════════════════════════════════════════

    def guardar_insight(self, insight_info: Dict[str, Any]):
        registro: RegistroInsight = {
            "timestamp":    datetime.now().isoformat(),
            "tipo_insight": insight_info.get("tipo", "DESCONOCIDO"),
            "descripcion":  insight_info.get("descripcion", ""),
            "relevancia":   insight_info.get("relevancia", "BAJA"),
            "datos":        insight_info.get("datos", {}),
        }
        self.almacen.guardar("insights", registro)

    def obtener_insights_recientes(
        self, n: int = 10, relevancia: Optional[str] = None
    ) -> List[RegistroInsight]:
        insights = self.almacen.cargar("insights")
        if relevancia:
            insights = [i for i in insights if i["relevancia"] == relevancia]
        return insights[-n:]

    # ═══════════════════════════════════════════════════════════════
    # AJUSTES DE GROUNDING — Compatible v3, sin cambios
    # ═══════════════════════════════════════════════════════════════

    def guardar_ajuste_grounding(
        self,
        concepto_id: str,
        grounding_anterior: float,
        grounding_nuevo: float,
        razon: str,
        aplicado: bool = True,
    ):
        registro: RegistroAjuste = {
            "timestamp":          datetime.now().isoformat(),
            "concepto_id":        concepto_id,
            "grounding_anterior": grounding_anterior,
            "grounding_nuevo":    grounding_nuevo,
            "razon":              razon,
            "aplicado":           aplicado,
        }
        self.almacen.guardar("ajustes", registro)

    def obtener_ajustes_concepto(self, concepto_id: str) -> List[RegistroAjuste]:
        return [
            a for a in self.almacen.cargar("ajustes")
            if a["concepto_id"] == concepto_id
        ]

    # ═══════════════════════════════════════════════════════════════
    # UTILIDADES — Compatible v3 + nuevos campos
    # ═══════════════════════════════════════════════════════════════

    def obtener_resumen_sesion(
        self, id_sesion: Optional[str] = None
    ) -> Optional[RegistroSesion]:
        id_buscar = id_sesion or self.sesion_actual
        if not id_buscar:
            return None
        for s in self.almacen.cargar("sesiones"):
            if s["id_sesion"] == id_buscar:
                return s
        return None

    def obtener_estadisticas_globales(self) -> Dict[str, Any]:
        return {
            # Compatible v3
            "total_sesiones":          self.almacen.contar("sesiones"),
            "total_conceptos_usados":  self.almacen.contar("conceptos"),
            "total_decisiones":        self.almacen.contar("decisiones"),
            "total_patrones":          self.almacen.contar("patrones"),
            "total_insights":          self.almacen.contar("insights"),
            "total_ajustes":           self.almacen.contar("ajustes"),
            "conceptos_mas_usados":    self.obtener_conceptos_mas_usados(5),
            "estadisticas_decisiones": self.obtener_estadisticas_decisiones(),
            "almacen":                 self.almacen.obtener_estadisticas(),
            "datos_usuario":           self.datos_usuario,
            # Nuevos
            "total_episodios":         self.almacen.contar(self.CLAVE_EPISODIOS),
            "total_personas":          len(self._cache_personas),
            "temas_abiertos":          len(self.obtener_temas_pendientes(50)),
            "estado_sesion":           self._sesion,
        }

    def limpiar_memoria(self, tipo: Optional[str] = None):
        if tipo:
            self.almacen.limpiar(tipo)
        else:
            self.almacen.limpiar_todo()

    def exportar_memoria(self, archivo: str) -> bool:
        return self.almacen.exportar(archivo)

    def importar_memoria(self, archivo: str) -> bool:
        return self.almacen.importar(archivo)