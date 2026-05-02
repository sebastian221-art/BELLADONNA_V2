# biblioteca/memoria/memoria_persistente.py
# ================================================
# MEMORIA PERSISTENTE DE BELL
#
# Bell recuerda todo entre sesiones.
# No es una base de datos — es su memoria real.
#
# Guarda en disco (JSON) y carga al arrancar.
# Nunca le recuerda a Sebastian lo que dijo —
# simplemente lo sabe y lo usa cuando viene al caso.
#
# Estructura:
#   datos_sebastian   → lo que Sebastian ha compartido
#   momentos          → exchanges significativos
#   temas             → temas recurrentes con frecuencia
#   estados           → historial emocional con fecha
#   pendientes        → cosas que Bell quiere preguntar
#   proyectos         → proyectos mencionados
# ================================================

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Optional


_RUTA_DEFAULT = Path(__file__).parent.parent.parent.parent / 'datos' / 'memoria_bell.json'


class MemoriaPersistente:

    _instancia: Optional['MemoriaPersistente'] = None

    def __init__(self, ruta: Path = _RUTA_DEFAULT):
        self._ruta  = Path(ruta)
        self._datos = self._estructura_vacia()
        self._cargada = False
        self._cargar()

    # ── Singleton ────────────────────────────────────────

    @classmethod
    def obtener(cls) -> 'MemoriaPersistente':
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    # ── Carga y guardado ─────────────────────────────────

    def _estructura_vacia(self) -> dict:
        return {
            'version':         2,
            'creada':          datetime.now().isoformat(),
            'ultima_sesion':   None,
            'datos_sebastian': {},
            'momentos':        [],
            'temas':           {},
            'estados':         [],
            'pendientes':      [],
            'proyectos':       {},
            'preferencias':    {},
            'total_sesiones':  0,
            'total_turnos':    0,
        }

    def _cargar(self):
        try:
            if self._ruta.exists():
                with open(self._ruta, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                # Migrar si falta alguna clave nueva
                base = self._estructura_vacia()
                for k, v in base.items():
                    if k not in datos:
                        datos[k] = v
                self._datos = datos
            else:
                self._ruta.parent.mkdir(parents=True, exist_ok=True)
        except Exception:
            self._datos = self._estructura_vacia()
        self._cargada = True

    def guardar(self):
        try:
            self._ruta.parent.mkdir(parents=True, exist_ok=True)
            with open(self._ruta, 'w', encoding='utf-8') as f:
                json.dump(self._datos, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    # ── Inicio de sesión ─────────────────────────────────

    def iniciar_sesion(self):
        self._datos['ultima_sesion'] = datetime.now().isoformat()
        self._datos['total_sesiones'] = self._datos.get('total_sesiones', 0) + 1
        self.guardar()

    # ── Registrar turno ──────────────────────────────────

    def registrar_turno(self, texto_usuario: str, respuesta_bell: str, comprension: dict = None):
        """
        Se llama después de cada turno.
        Extrae todo lo que Bell puede aprender de este mensaje.
        """
        self._datos['total_turnos'] = self._datos.get('total_turnos', 0) + 1

        # Extraer hechos del mensaje
        self._extraer_datos_sebastian(texto_usuario)
        self._extraer_temas(texto_usuario)
        self._extraer_estado_emocional(texto_usuario, comprension)
        self._extraer_proyectos(texto_usuario)
        self._extraer_pendientes(texto_usuario, respuesta_bell)

        # Guardar momento significativo si aplica
        if self._es_momento_significativo(texto_usuario, comprension):
            self._guardar_momento(texto_usuario, respuesta_bell, comprension)

        self.guardar()

    def _extraer_datos_sebastian(self, texto: str):
        tl = texto.lower().strip()
        sd = self._datos['datos_sebastian']

        # Edad: "tengo 17", "tengo 17 años", "soy mayor de edad"
        m = re.search(r'tengo\s+(\d+)\s*años?', tl)
        if m:
            sd['edad'] = int(m.group(1))

        # Nombre: "me llamo X", "soy X", "mi nombre es X"
        m = re.search(r'(?:me llamo|mi nombre es|soy)\s+([A-Za-záéíóúÁÉÍÓÚñÑ]+)', texto)
        if m:
            nombre = m.group(1).strip()
            if len(nombre) > 2 and nombre.lower() not in ('un','una','el','la','muy','bien','mal'):
                sd['nombre_real'] = nombre

        # Ciudad/País: "soy de X", "vivo en X", "estoy en X"
        m = re.search(r'(?:soy de|vivo en|estoy en|vengo de)\s+([A-Za-záéíóúÁÉÍÓÚñÑ\s]+?)(?:\.|,|$)', texto)
        if m:
            lugar = m.group(1).strip()
            if 2 < len(lugar) < 40:
                sd['lugar'] = lugar

        # Ocupación: "soy programador", "estudio", "trabajo en"
        for pat, clave in [
            (r'(?:soy|trabajo como)\s+(programador|desarrollador|diseñador|estudiante|ingeniero|médico|abogado|contador)', 'ocupacion'),
            (r'estudio\s+([a-záéíóú\s]+?)(?:\s+en|\s+en la|\.|,|$)', 'carrera'),
            (r'trabajo\s+(?:en|para)\s+([A-Za-záéíóúÁÉÍÓÚñÑ\s]+?)(?:\.|,|$)', 'empresa'),
        ]:
            mm = re.search(pat, tl)
            if mm:
                sd[clave] = mm.group(1).strip()[:50]

    def _extraer_temas(self, texto: str):
        tl = texto.lower()
        temas = self._datos['temas']
        ahora = datetime.now().isoformat()

        catalogo = {
            'belladonna':    ['belladonna', 'bell', 'el proyecto', 'la ia', 'mi proyecto'],
            'programacion':  ['python', 'código', 'codigo', 'programa', 'bug', 'error', 'función', 'funcion', 'clase', 'archivo'],
            'familia':       ['papá', 'papa', 'mamá', 'mama', 'hermano', 'hermana', 'familia', 'padres'],
            'trabajo':       ['trabajo', 'empresa', 'jefe', 'oficina', 'cliente', 'reunión', 'reunion'],
            'estudio':       ['universidad', 'colegio', 'clase', 'examen', 'tarea', 'profesor', 'carrera'],
            'salud':         ['cansado', 'enfermo', 'dolor', 'dormir', 'no dormí', 'medicina'],
            'dinero':        ['plata', 'dinero', 'plata', 'deuda', 'sueldo', 'gastos'],
            'amistad':       ['amigo', 'amiga', 'amigos', 'salida', 'rumba', 'parche'],
            'tecnologia':    ['computador', 'celular', 'internet', 'app', 'web', 'servidor'],
            'emociones':     ['siento', 'me siento', 'estoy', 'me tiene', 'estoy pensando'],
        }

        for tema, palabras in catalogo.items():
            if any(p in tl for p in palabras):
                if tema not in temas:
                    temas[tema] = {'count': 0, 'primera_vez': ahora, 'ultima_vez': ahora}
                temas[tema]['count'] = temas[tema].get('count', 0) + 1
                temas[tema]['ultima_vez'] = ahora

    def _extraer_estado_emocional(self, texto: str, comprension: dict = None):
        tl = texto.lower()
        estados = self._datos['estados']
        ahora = datetime.now().isoformat()

        estado = None

        # Desde comprensión si viene
        if comprension:
            profunda = comprension.get('profunda', {})
            emocion = profunda.get('emocion_detectada', '')
            if emocion and emocion not in ('neutra', ''):
                estado = emocion

        # Desde texto directo
        if not estado:
            neg = ['mal', 'triste', 'frustrado', 'cansado', 'agotado', 'estresado', 'ansioso', 'preocupado']
            pos = ['bien', 'genial', 'feliz', 'contento', 'alegre', 'motivado', 'emocionado']
            if any(p in tl for p in neg):
                estado = 'negativo'
            elif any(p in tl for p in pos):
                estado = 'positivo'

        if estado:
            # Guardar máximo 30 estados recientes
            if len(estados) >= 30:
                estados.pop(0)
            estados.append({'fecha': ahora, 'estado': estado, 'texto': texto[:80]})

    def _extraer_proyectos(self, texto: str):
        tl = texto.lower()
        proyectos = self._datos['proyectos']
        ahora = datetime.now().isoformat()

        # Belladonna siempre está
        if any(p in tl for p in ['belladonna', 'bell', 'el proyecto', 'la ia']):
            if 'BELLADONNA' not in proyectos:
                proyectos['BELLADONNA'] = {'menciones': 0, 'primera': ahora}
            proyectos['BELLADONNA']['menciones'] = proyectos['BELLADONNA'].get('menciones', 0) + 1
            proyectos['BELLADONNA']['ultima'] = ahora

        # Detectar otros proyectos por contexto
        m = re.search(r'(?:mi proyecto|estoy (?:haciendo|desarrollando|construyendo|trabajando en))\s+([A-Za-záéíóúÁÉÍÓÚñÑ\s]+?)(?:\s+que|\s+el|\.|,|$)', texto)
        if m:
            nombre = m.group(1).strip()[:30]
            if nombre and nombre.lower() not in ('un', 'una', 'esto', 'eso', 'algo'):
                if nombre not in proyectos:
                    proyectos[nombre] = {'menciones': 0, 'primera': ahora}
                proyectos[nombre]['menciones'] = proyectos[nombre].get('menciones', 0) + 1

    def _extraer_pendientes(self, texto: str, respuesta_bell: str):
        """
        Si Bell detecta una pregunta implícita o un tema sin resolver,
        lo guarda como pendiente para retomarlo en la próxima sesión.
        """
        tl = texto.lower()
        pendientes = self._datos['pendientes']
        ahora = datetime.now().isoformat()

        # Si el mensaje termina en pregunta sin respuesta clara
        senales_pendiente = [
            'no sé qué hacer', 'no sé cómo', 'estoy pensando',
            'no sé si', 'tengo dudas', 'hay algo que',
            'no me decide', 'estoy confundido', 'qué hago',
        ]
        for senal in senales_pendiente:
            if senal in tl:
                pendiente = {
                    'fecha': ahora,
                    'texto': texto[:100],
                    'tipo': 'duda',
                    'resuelto': False,
                }
                # No duplicar
                ya_existe = any(
                    p.get('texto', '')[:50] == texto[:50]
                    for p in pendientes
                )
                if not ya_existe:
                    pendientes.append(pendiente)
                    # Máximo 10 pendientes
                    if len(pendientes) > 10:
                        pendientes.pop(0)
                break

    def _es_momento_significativo(self, texto: str, comprension: dict = None) -> bool:
        """Un momento es significativo si hay emoción fuerte o información personal importante."""
        if not comprension:
            return False
        profunda = comprension.get('profunda', {})
        intensidad = profunda.get('intensidad', 0.0)
        tipo = comprension.get('contextual', {}).get('tipo_mensaje', '')
        return (
            intensidad > 0.7 or
            tipo in ('dato_personal', 'presentacion_sebastian', 'pregunta_filosofica')
        )

    def _guardar_momento(self, texto: str, respuesta: str, comprension: dict = None):
        momentos = self._datos['momentos']
        ahora = datetime.now().isoformat()

        momento = {
            'fecha':    ahora,
            'usuario':  texto[:120],
            'bell':     respuesta[:120],
            'tipo':     comprension.get('contextual', {}).get('tipo_mensaje', '') if comprension else '',
        }
        momentos.append(momento)
        # Máximo 50 momentos
        if len(momentos) > 50:
            momentos.pop(0)

    # ── Contexto para el prompt ──────────────────────────

    def obtener_contexto_rico(self) -> str:
        """
        Genera el bloque de contexto que Bell usa internamente.
        NUNCA para recordarle a Sebastian — para saber Bell.
        """
        lineas = []
        sd     = self._datos.get('datos_sebastian', {})
        temas  = self._datos.get('temas', {})
        estados= self._datos.get('estados', [])
        proyec = self._datos.get('proyectos', {})

        # Datos de Sebastian
        if sd:
            lineas.append('LO QUE BELL SABE DE SEBASTIAN:')
            if 'nombre_real' in sd:
                lineas.append(f'  Nombre: {sd["nombre_real"]}')
            if 'edad' in sd:
                lineas.append(f'  Edad: {sd["edad"]} años')
            if 'lugar' in sd:
                lineas.append(f'  Lugar: {sd["lugar"]}')
            if 'ocupacion' in sd:
                lineas.append(f'  Ocupación: {sd["ocupacion"]}')
            if 'carrera' in sd:
                lineas.append(f'  Estudia: {sd["carrera"]}')
            if 'empresa' in sd:
                lineas.append(f'  Trabaja en: {sd["empresa"]}')

        # Proyectos activos
        if proyec:
            nombres = [k for k, v in proyec.items() if v.get('menciones', 0) > 0]
            if nombres:
                lineas.append(f'  Proyectos mencionados: {", ".join(nombres[:3])}')

        # Temas recurrentes (los más frecuentes)
        if temas:
            top = sorted(temas.items(), key=lambda x: x[1].get('count', 0), reverse=True)[:4]
            if top:
                nombres_temas = [t[0] for t in top]
                lineas.append(f'  Temas que más aparecen: {", ".join(nombres_temas)}')

        # Estado emocional reciente
        if estados:
            ultimos = estados[-3:]
            neg = sum(1 for e in ultimos if e.get('estado') in ('negativo', 'frustracion', 'cansancio', 'tristeza'))
            pos = sum(1 for e in ultimos if e.get('estado') in ('positivo', 'entusiasmo', 'determinacion'))
            if neg > pos:
                lineas.append('  Estado emocional reciente: ha tenido momentos difíciles')
            elif pos > neg:
                lineas.append('  Estado emocional reciente: con buena energía')

        # Estadísticas generales
        total_s = self._datos.get('total_sesiones', 0)
        total_t = self._datos.get('total_turnos', 0)
        if total_s > 0:
            lineas.append(f'  Sesiones anteriores con Bell: {total_s} | Turnos totales: {total_t}')

        return '\n'.join(lineas) if lineas else ''

    def obtener_pendientes_relevantes(self) -> list:
        """Pendientes sin resolver, ordenados por más reciente."""
        pendientes = self._datos.get('pendientes', [])
        activos = [p for p in pendientes if not p.get('resuelto', False)]
        return activos[-3:]  # máximo 3

    def obtener_temas_para_iniciativa(self) -> list:
        """
        Temas que Bell puede retomar por iniciativa propia.
        Solo los recurrentes con varias menciones.
        """
        temas = self._datos.get('temas', {})
        return [
            t for t, v in temas.items()
            if v.get('count', 0) >= 2
        ][:3]

    def tiene_historia(self) -> bool:
        return self._datos.get('total_turnos', 0) > 5

    def sesiones_anteriores(self) -> int:
        return self._datos.get('total_sesiones', 0)

    def datos_sebastian(self) -> dict:
        return self._datos.get('datos_sebastian', {})