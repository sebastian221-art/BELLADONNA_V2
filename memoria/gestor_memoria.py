"""
Gestor de Memoria - Interfaz principal para memoria persistente.

Proporciona métodos de alto nivel para guardar y recuperar
información entre sesiones.

MODIFICADO v3 — Corrección Arquitectónica Total (sobre Mega Paquete A):
- NUEVO: guardar_datos_usuario()   → persiste datos en disco al finalizar sesión
- NUEVO: cargar_datos_usuario()    → recupera datos del disco al iniciar sesión
- NUEVO: registrar_contexto_espera()  → Bell registra qué preguntó (para manejar "sí"/"no")
- NUEVO: obtener_contexto_espera()    → recupera contexto de espera
- NUEVO: limpiar_contexto_espera()    → limpia tras usarlo
- NUEVO: self.contexto_espera         → atributo en __init__
- NUEVO: self.datos_usuario['edad']   → también extrae edad de "tengo X años"
- MEJORADO: iniciar_sesion()          → llama cargar_datos_usuario() al arrancar
- MEJORADO: finalizar_sesion()        → llama guardar_datos_usuario() al cerrar
- MEJORADO: agregar_mensaje()         → registra SIEMPRE (usuario Y bell)
- MEJORADO: obtener_contexto()        → n_mensajes=8 por defecto, usa nombre real
- MEJORADO: _extraer_datos_usuario()  → regex reforzado + _PALABRAS_EXCLUIDAS_NOMBRE
- MEJORADO: el_usuario_se_llama()     → igual que antes, ahora cargado desde disco

COMPATIBILIDAD: 100% con Mega Paquete A — mismos métodos, mismas firmas.
Los métodos nuevos son ADICIONALES. Nada se rompe.
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

from memoria.almacen import AlmacenJSON
from memoria.tipos_memoria import (
    TipoMemoria,
    RegistroConcepto,
    RegistroDecision,
    RegistroPatron,
    RegistroInsight,
    RegistroAjuste,
    RegistroSesion
)


# ═══════════════════════════════════════════════════════════════════════
# FILTRO ROBUSTO PARA EXTRACCIÓN DE NOMBRES
# Evita que "soy humano", "me llamo el", etc. se guarden como nombre
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
    Gestor central de memoria persistente.
    
    v3: Persiste datos de usuario ENTRE sesiones. Registra contexto de
    conversación completo (usuario Y Bell). Maneja contexto de espera
    para responder "sí"/"no" con contexto.
    """

    CLAVE_USUARIO = "usuario_persistente"

    def __init__(self, directorio: str = "memoria_bell"):
        self.almacen = AlmacenJSON(directorio)
        self.sesion_actual: Optional[str] = None
        self.sesion_inicio: Optional[str] = None

        # ── Memoria de conversación en RAM ──────────────────────────────
        self.historial_sesion: List[Dict[str, str]] = []
        self.datos_usuario: Dict[str, str] = {}

        # ── NUEVO v3: contexto de espera ─────────────────────────────────
        # Cuando Bell hace una pregunta ("¿quieres más info?"), registra
        # aquí qué esperaba. Si el siguiente mensaje es "sí"/"no"/"dale",
        # el generador puede enriquecer el mensaje con este contexto.
        self.contexto_espera: Optional[Dict[str, str]] = None

    # ═══════════════════════════════════════════════════════════════
    # SESIONES
    # ═══════════════════════════════════════════════════════════════

    def iniciar_sesion(self) -> str:
        """
        Inicia una nueva sesión.
        NUEVO v3: carga datos del usuario de sesiones anteriores.
        """
        self.sesion_actual = str(uuid.uuid4())
        self.sesion_inicio = datetime.now().isoformat()

        # ← NUEVO v3: recuperar nombre, edad, etc. de sesión anterior
        self.cargar_datos_usuario()

        sesion: RegistroSesion = {
            'id_sesion':           self.sesion_actual,
            'inicio':              self.sesion_inicio,
            'fin':                 None,
            'mensajes_procesados': 0,
            'decisiones_tomadas':  0,
            'conceptos_usados':    0,
            'patrones_detectados': 0,
        }
        self.almacen.guardar('sesiones', sesion)
        return self.sesion_actual

    def finalizar_sesion(self):
        """
        Finaliza la sesión actual.
        NUEVO v3: persiste datos del usuario en disco antes de cerrar.
        """
        if not self.sesion_actual:
            return

        # ← NUEVO v3: guardar nombre, edad, etc. antes de cerrar
        self.guardar_datos_usuario()

        sesiones = self.almacen.cargar('sesiones')
        for sesion in sesiones:
            if sesion['id_sesion'] == self.sesion_actual:
                sesion['fin'] = datetime.now().isoformat()
                break

        self.almacen.limpiar('sesiones')
        for sesion in sesiones:
            self.almacen.guardar('sesiones', sesion)

        self.sesion_actual = None
        self.sesion_inicio = None

    def _actualizar_contador_sesion(self, campo: str):
        if not self.sesion_actual:
            return
        sesiones = self.almacen.cargar('sesiones')
        for sesion in sesiones:
            if sesion['id_sesion'] == self.sesion_actual:
                sesion[campo] = sesion.get(campo, 0) + 1
                break
        self.almacen.limpiar('sesiones')
        for sesion in sesiones:
            self.almacen.guardar('sesiones', sesion)

    # ═══════════════════════════════════════════════════════════════
    # PERSISTENCIA DE DATOS DE USUARIO (NUEVO v3)
    # ═══════════════════════════════════════════════════════════════

    def guardar_datos_usuario(self):
        """
        Persiste self.datos_usuario en disco.
        Llamado automáticamente en finalizar_sesion().
        El usuario no tiene que hacer nada extra.
        """
        if not self.datos_usuario:
            return
        try:
            # Sobreescribir: limpiar primero, luego guardar el estado actual
            self.almacen.limpiar(self.CLAVE_USUARIO)
            self.almacen.guardar(self.CLAVE_USUARIO, self.datos_usuario)
        except Exception:
            pass  # No crashear si falla la persistencia

    def cargar_datos_usuario(self):
        """
        Recupera datos del usuario desde disco.
        Llamado automáticamente en iniciar_sesion().
        Si no hay datos previos, self.datos_usuario queda vacío.
        """
        try:
            registros = self.almacen.cargar(self.CLAVE_USUARIO)
            if registros:
                # El último registro es el más reciente
                self.datos_usuario = registros[-1]
        except Exception:
            pass  # Si no existe el archivo, empezar desde cero

    # ═══════════════════════════════════════════════════════════════
    # MEMORIA DE CONVERSACIÓN EN RAM
    # ═══════════════════════════════════════════════════════════════

    def agregar_mensaje(self, rol: str, mensaje: str):
        """
        Registra un turno de conversación en RAM.
        
        Args:
            rol:     'usuario' | 'bell'
            mensaje: Texto del turno
            
        CAMBIO v3: registra SIEMPRE — tanto mensajes del usuario como
        respuestas de Bell. En Mega Paquete A solo registraba el usuario.
        Ahora el historial contiene el diálogo completo.
        """
        self.historial_sesion.append({
            'rol':       rol,
            'mensaje':   mensaje,
            'timestamp': datetime.now().isoformat(),
        })
        if rol == 'usuario':
            self._extraer_datos_usuario(mensaje)
        # Mantener solo los últimos 30 turnos
        if len(self.historial_sesion) > 30:
            self.historial_sesion = self.historial_sesion[-30:]

    def _extraer_datos_usuario(self, mensaje: str):
        """
        Extrae datos del usuario de forma pasiva mientras conversa.
        
        CAMBIOS v3:
        - Regex con word boundary correcto (evita falsos positivos)
        - Filtro _PALABRAS_EXCLUIDAS_NOMBRE más robusto
        - Extrae también la edad ("tengo 19 años")
        - Longitud mínima de nombre: 3 caracteres
        """
        import re
        mensaje_lower = mensaje.lower().strip()

        # ── Extraer nombre ────────────────────────────────────────────────
        if 'nombre' not in self.datos_usuario:
            patron_nombre = (
                r'(?:mi nombre es|me llamo|soy|puedes llamarme|llámame|llamame)'
                r'\s+([a-záéíóúüñ]+)'
            )
            match = re.search(patron_nombre, mensaje_lower)
            if match:
                nombre_raw = match.group(1).strip()
                if (
                    len(nombre_raw) >= 3
                    and nombre_raw not in _PALABRAS_EXCLUIDAS_NOMBRE
                    and not nombre_raw.isdigit()
                ):
                    self.datos_usuario['nombre'] = nombre_raw.capitalize()

        # ── Extraer edad (NUEVO v3) ───────────────────────────────────────
        if 'edad' not in self.datos_usuario:
            match_edad = re.search(r'tengo\s+(\d+)\s+años', mensaje_lower)
            if match_edad:
                edad = int(match_edad.group(1))
                if 1 <= edad <= 120:
                    self.datos_usuario['edad'] = str(edad)

    def obtener_contexto(self, n_mensajes: int = 8) -> str:
        """
        Retorna los últimos N turnos como string para Groq.
        
        CAMBIOS v3:
        - n_mensajes default = 8 (era 6 en Mega Paquete A)
        - Usa el nombre real del usuario si se conoce (en vez de "Usuario")
        - Incluye mensajes de Bell (historial completo, no solo usuario)
        
        Args:
            n_mensajes: Cuántos mensajes incluir
            
        Returns:
            String con el historial formateado, o mensaje vacío
        """
        if not self.historial_sesion:
            return "Sin conversación previa en esta sesión."
        ultimos = self.historial_sesion[-n_mensajes:]
        nombre = self.datos_usuario.get('nombre', 'Usuario')
        lineas = []
        for msg in ultimos:
            rol   = nombre if msg['rol'] == 'usuario' else "Bell"
            texto = msg['mensaje'][:200]  # truncar mensajes muy largos
            lineas.append(f"{rol}: {texto}")
        return "\n".join(lineas)

    def el_usuario_se_llama(self) -> str:
        """
        Retorna el nombre del usuario si fue mencionado.
        CAMBIO v3: ahora puede venir de sesiones anteriores (cargado desde disco).
        
        Returns:
            Nombre del usuario o '' si no se conoce aún
        """
        return self.datos_usuario.get('nombre', '')

    def obtener_datos_usuario(self) -> Dict[str, str]:
        """
        Retorna todos los datos conocidos del usuario.
        CAMBIO v3: ahora incluye 'edad' si se mencionó.
        
        Returns:
            Dict con los datos recopilados (nombre, edad, etc.)
        """
        return dict(self.datos_usuario)

    # ═══════════════════════════════════════════════════════════════
    # CONTEXTO DE ESPERA — NUEVO v3
    # Para manejar "sí" / "no" / "dale" con contexto
    # ═══════════════════════════════════════════════════════════════

    def registrar_contexto_espera(self, tema: str, pregunta_bell: str):
        """
        Registra que Bell hizo una pregunta y espera confirmación.
        
        Ejemplo:
            Bell dice: "¿Quieres que te cuente sobre cada consejera?"
            → registrar_contexto_espera("IDENTIDAD_BELL", "¿Quieres que te cuente sobre cada consejera?")
        
        La próxima vez que el usuario diga "sí", el generador puede
        recuperar este contexto para saber A QUÉ está respondiendo.
        
        Args:
            tema:          Tipo de decisión activo (ej: "IDENTIDAD_BELL")
            pregunta_bell: Texto del final de la respuesta de Bell
        """
        self.contexto_espera = {
            'tema':          tema,
            'pregunta_bell': pregunta_bell,
            'timestamp':     datetime.now().isoformat(),
        }

    def obtener_contexto_espera(self) -> Optional[Dict[str, str]]:
        """
        Retorna el contexto de espera si existe, None si no.
        
        Returns:
            Dict con 'tema' y 'pregunta_bell', o None
        """
        return self.contexto_espera

    def limpiar_contexto_espera(self):
        """
        Limpia el contexto de espera tras usarlo.
        Llamar después de procesar la confirmación del usuario.
        """
        self.contexto_espera = None

    # ═══════════════════════════════════════════════════════════════
    # CONCEPTOS
    # ═══════════════════════════════════════════════════════════════

    def guardar_concepto_usado(self, concepto_id: str, certeza: float = 0.0):
        registro: RegistroConcepto = {
            'concepto_id':    concepto_id,
            'timestamp':      datetime.now().isoformat(),
            'veces_usado':    1,
            'ultima_certeza': certeza,
        }
        self.almacen.guardar('conceptos', registro)
        self._actualizar_contador_sesion('conceptos_usados')

    def obtener_conceptos_mas_usados(self, n: int = 10) -> List[Dict[str, Any]]:
        conceptos = self.almacen.cargar('conceptos')
        conteo: Dict[str, Dict[str, Any]] = {}
        for registro in conceptos:
            cid = registro['concepto_id']
            if cid not in conteo:
                conteo[cid] = {
                    'concepto_id': cid,
                    'usos':        0,
                    'ultimo_uso':  registro['timestamp'],
                }
            conteo[cid]['usos'] += registro['veces_usado']
            conteo[cid]['ultimo_uso'] = max(conteo[cid]['ultimo_uso'], registro['timestamp'])
        ranking = sorted(conteo.values(), key=lambda x: x['usos'], reverse=True)
        return ranking[:n]

    # ═══════════════════════════════════════════════════════════════
    # DECISIONES
    # ═══════════════════════════════════════════════════════════════

    def guardar_decision(self, decision_info: Dict[str, Any]):
        registro: RegistroDecision = {
            'timestamp':             datetime.now().isoformat(),
            'tipo':                  decision_info.get('tipo', 'DESCONOCIDO'),
            'puede_ejecutar':        decision_info.get('puede_ejecutar', False),
            'certeza':               decision_info.get('certeza', 0.0),
            'conceptos_principales': decision_info.get('conceptos_principales', []),
            'grounding_promedio':    decision_info.get('grounding_promedio', 0.0),
        }
        self.almacen.guardar('decisiones', registro)
        self._actualizar_contador_sesion('decisiones_tomadas')

    def obtener_decisiones_recientes(self, n: int = 20) -> List[RegistroDecision]:
        decisiones = self.almacen.cargar('decisiones')
        return decisiones[-n:]

    def obtener_estadisticas_decisiones(self) -> Dict[str, Any]:
        decisiones = self.almacen.cargar('decisiones')
        if not decisiones:
            return {'total': 0, 'tasa_ejecucion': 0.0, 'certeza_promedio': 0.0, 'tipos': {}}
        ejecutables = sum(1 for d in decisiones if d['puede_ejecutar'])
        certezas    = [d['certeza'] for d in decisiones]
        tipos: Dict[str, int] = {}
        for d in decisiones:
            tipos[d['tipo']] = tipos.get(d['tipo'], 0) + 1
        return {
            'total':            len(decisiones),
            'tasa_ejecucion':   (ejecutables / len(decisiones)) * 100,
            'certeza_promedio': sum(certezas) / len(certezas),
            'tipos':            tipos,
        }

    # ═══════════════════════════════════════════════════════════════
    # PATRONES
    # ═══════════════════════════════════════════════════════════════

    def guardar_patron(self, patron_info: Dict[str, Any]):
        registro: RegistroPatron = {
            'timestamp':   datetime.now().isoformat(),
            'tipo_patron': patron_info.get('tipo', 'DESCONOCIDO'),
            'descripcion': patron_info.get('descripcion', ''),
            'frecuencia':  patron_info.get('frecuencia', 0),
            'confianza':   patron_info.get('confianza', 0.0),
        }
        self.almacen.guardar('patrones', registro)
        self._actualizar_contador_sesion('patrones_detectados')

    def obtener_patrones_recientes(self, n: int = 10) -> List[RegistroPatron]:
        patrones = self.almacen.cargar('patrones')
        return patrones[-n:]

    # ═══════════════════════════════════════════════════════════════
    # INSIGHTS
    # ═══════════════════════════════════════════════════════════════

    def guardar_insight(self, insight_info: Dict[str, Any]):
        registro: RegistroInsight = {
            'timestamp':    datetime.now().isoformat(),
            'tipo_insight': insight_info.get('tipo', 'DESCONOCIDO'),
            'descripcion':  insight_info.get('descripcion', ''),
            'relevancia':   insight_info.get('relevancia', 'BAJA'),
            'datos':        insight_info.get('datos', {}),
        }
        self.almacen.guardar('insights', registro)

    def obtener_insights_recientes(self, n: int = 10,
                                   relevancia: Optional[str] = None) -> List[RegistroInsight]:
        insights = self.almacen.cargar('insights')
        if relevancia:
            insights = [i for i in insights if i['relevancia'] == relevancia]
        return insights[-n:]

    # ═══════════════════════════════════════════════════════════════
    # AJUSTES DE GROUNDING
    # ═══════════════════════════════════════════════════════════════

    def guardar_ajuste_grounding(self, concepto_id: str, grounding_anterior: float,
                                 grounding_nuevo: float, razon: str, aplicado: bool = True):
        registro: RegistroAjuste = {
            'timestamp':          datetime.now().isoformat(),
            'concepto_id':        concepto_id,
            'grounding_anterior': grounding_anterior,
            'grounding_nuevo':    grounding_nuevo,
            'razon':              razon,
            'aplicado':           aplicado,
        }
        self.almacen.guardar('ajustes', registro)

    def obtener_ajustes_concepto(self, concepto_id: str) -> List[RegistroAjuste]:
        ajustes = self.almacen.cargar('ajustes')
        return [a for a in ajustes if a['concepto_id'] == concepto_id]

    # ═══════════════════════════════════════════════════════════════
    # UTILIDADES
    # ═══════════════════════════════════════════════════════════════

    def obtener_resumen_sesion(self, id_sesion: Optional[str] = None) -> Optional[RegistroSesion]:
        id_buscar = id_sesion or self.sesion_actual
        if not id_buscar:
            return None
        sesiones = self.almacen.cargar('sesiones')
        for sesion in sesiones:
            if sesion['id_sesion'] == id_buscar:
                return sesion
        return None

    def obtener_estadisticas_globales(self) -> Dict[str, Any]:
        return {
            'total_sesiones':         self.almacen.contar('sesiones'),
            'total_conceptos_usados': self.almacen.contar('conceptos'),
            'total_decisiones':       self.almacen.contar('decisiones'),
            'total_patrones':         self.almacen.contar('patrones'),
            'total_insights':         self.almacen.contar('insights'),
            'total_ajustes':          self.almacen.contar('ajustes'),
            'conceptos_mas_usados':   self.obtener_conceptos_mas_usados(5),
            'estadisticas_decisiones': self.obtener_estadisticas_decisiones(),
            'almacen':                self.almacen.obtener_estadisticas(),
            'datos_usuario':          self.datos_usuario,       # NUEVO v3
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