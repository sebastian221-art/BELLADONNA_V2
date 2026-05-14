# biblioteca/habilidades/auto_analisis/motor_auto_analisis.py
# ================================================
# MOTOR AUTO-ANÁLISIS TOTAL — Bell se conoce a sí misma
#
# Responde cualquier pregunta sobre la propia arquitectura
# de Bell: archivos, capas, habilidades, consejeras,
# vocabulario, interfaz, estadísticas.
#
# Cubre TODOS los tipos de archivo:
# Python, JS, CSS, HTML, JSON, Markdown
#
# Mente Pura: Bell lee sus propios archivos con Python.
# Groq pule el lenguaje final.
# ================================================

import os
import re
import time
from pathlib import Path
from typing import Optional

from .escaner import EscanerTotal, EscaneoResult
from .analizador_profundo import analizar_todo_bell, analizar_archivo

# Groq para análisis profesional — mismo patrón que habilidad Python
import os as _os
import httpx as _httpx

_GROQ_URL_AA   = 'https://api.groq.com/openai/v1/chat/completions'
_GROQ_MODEL_AA = 'openai/gpt-oss-120b'
_GROQ_API_KEY_AA = _os.getenv('GROQ_API_KEY', '')

_SYSTEM_AA = """Eres Bell — IA creada por Sebastian Gómez (19 años, Bucaramanga). Eres arquitecta que analiza su propio sistema BELLADONNA en primera persona.

VOZ: directa, técnica, sin relleno. Como senior engineer revisando su propio código.
NUNCA: "claro", "por supuesto", "como IA".
REGLA CRÍTICA: solo usas los datos que te dan. NUNCA inventas métricas o archivos.

REGLAS DE LONGITUD:
- Preguntas GENERALES ("qué tienes", "describe tu arquitectura", "qué habilidades"): 2-4 oraciones concisas. NO listes todos los archivos uno por uno.
- Preguntas DE CAPA ("qué hay en capa X"): lista TODOS los archivos en formato compacto: "nombre.py (N líneas) — función breve (max 10 palabras)". UNA línea por archivo, sin párrafos.
- Preguntas DE ARCHIVO ("qué hace X.py"): 3-5 oraciones describiendo rol, clases principales y funciones clave.
- Análisis/introspección: 3-4 puntos concretos con nombres reales, máximo 3 oraciones por punto."""


def _groq_analisis_profundo(pregunta: str, datos_radon: str) -> str:
    """
    Groq recibe datos radon reales (CC, MI, sin_doc) y genera análisis profesional.
    Datos compactos (~150 tokens) → Groq responde con todo lo necesario sin corte.
    """
    if not _GROQ_API_KEY_AA:
        return ''
    try:
        r = _httpx.post(
            _GROQ_URL_AA,
            headers={'Authorization': f'Bearer {_GROQ_API_KEY_AA}',
                     'Content-Type': 'application/json'},
            json={
                'model': _GROQ_MODEL_AA,
                'messages': [
                    {'role': 'system', 'content': (
                        "Eres Bell — IA de Sebastian Gómez. Hablas de tu propio código en primera persona.\n"
                        "REGLAS ABSOLUTAS:\n"
                        "- NUNCA uses tablas, listas con -, bullets, headers con # o formato markdown\n"
                        "- NUNCA empieces con Hola, Buenos días, Soy Bell, ni te presentes\n"
                        "- NUNCA uses emojis ni iconos\n"
                        "- Habla como una desarrolladora que le explica su código a Sebastian de forma natural\n"
                        "- Prosa fluida en español, 3-4 oraciones máximo\n"
                        "- Menciona métricas reales (CC, MI) de forma conversacional\n"
                        "- Ejemplo bueno: 'Mi archivo más crítico es motor.py — CC de 72 significa 72 caminos distintos, casi imposible de testear. Lo dividiría en tres módulos.'"
                    )},
                    {'role': 'user', 'content': (
                        f"{datos_radon}\n\n"
                        f"Sebastian pregunta: {pregunta}\n\n"
                        "Responde en 5-6 oraciones conversacionales. Sin formato. Sin introducción."
                    )},
                ],
                'temperature': 0.4,
                'max_tokens': 400,
            },
            timeout=25,
        )
        if r.status_code == 200:
            content = r.json().get('choices',[{}])[0].get('message',{}).get('content','').strip()
            if content and len(content) > 20:
                return content
    except Exception as e:
        print(f'  [AutoAnalisis Groq] {e}')
    return ''



# Cache del escaneo (no re-escanear en cada pregunta)
_cache_resultado: Optional[EscaneoResult] = None
_cache_tiempo: float = 0.0
_CACHE_TTL = 60   # 1 minuto — se refresca rápido


def _obtener_escaneo() -> EscaneoResult:
    global _cache_resultado, _cache_tiempo
    ahora = time.time()
    if _cache_resultado and (ahora - _cache_tiempo) < _CACHE_TTL:
        return _cache_resultado

    # Detectar raíz de Bell
    raiz = os.environ.get('BELL_ROOT', '')
    if not raiz:
        # Inferir desde la ubicación del archivo
        raiz = str(Path(__file__).resolve().parents[4])

    escaner = EscanerTotal(raiz)
    _cache_resultado = escaner.escanear()
    _cache_tiempo = ahora
    return _cache_resultado


def _detectar_tipo(texto: str) -> str:
    tl = texto.lower()

    # Pregunta por archivo específico
    if re.search(r'\b\w+\.(py|js|css|html|json|md)\b', tl):
        return 'archivo_especifico'

    # Capas
    if re.search(r'\bcapa\s*[1-9]\b|\bcapa\s+(?:uno|dos|tres|cuatro|cinco|seis|siete|ocho|nueve)\b', tl):
        return 'capa_especifica'

    # Habilidades
    if any(p in tl for p in ['habilidad', 'habilidades', 'puedes hacer', 'qué sabes', 'qué puedes']):
        return 'habilidades'

    # Consejeras
    if any(p in tl for p in ['consejera', 'consejeras', 'soma', 'vega', 'nova', 'echo',
                               'lyra', 'luna', 'iris', 'sage']):
        return 'consejeras'

    # Vocabulario
    if any(p in tl for p in ['vocabulario', 'conceptos', 'palabras', 'cuánto sabes de palabras']):
        return 'vocabulario'

    # Interfaz / frontend
    if any(p in tl for p in ['interfaz', 'frontend', 'javascript', 'css', 'html', 'visual',
                               'pantalla', 'js ', 'scripts']):
        return 'interfaz'

    # Estadísticas numéricas
    if any(p in tl for p in ['cuántos archivos', 'cuantos archivos', 'cuántas líneas',
                               'cuantas lineas', 'cuánto pesas', 'tamaño', 'tamanio',
                               'líneas de código', 'lineas de codigo']):
        return 'estadisticas'

    # Análisis de código propio y mejoras — ANTES de resumen general
    if any(p in tl for p in [
        'analiza tu código', 'analiza tu codigo', 'analiza todo tu',
        'analiza tu propio', 'qué mejorarías', 'que mejorarias',
        'qué mejorarías de ti', 'que mejorarias de ti',
        'qué cambiarías', 'que cambiarias', 'propón mejoras',
        'propone mejoras', 'qué está mal en ti', 'que esta mal en ti',
        'deuda técnica', 'deuda tecnica', 'errores en tu código',
        'bugs en tu código', 'problemas en tu código',
        'qué necesitas mejorar', 'que necesitas mejorar',
        'archivos más grandes', 'archivos mas grandes',
        'más grande', 'crecieron', 'urgentes', 'urgente',
        '3 cosas', 'tres cosas', 'más urgente',
    ]):
        return 'analisis_propio'

    # Introspección cualitativa — qué te falta, qué serías, qué capacidades faltan
    if any(p in tl for p in [
        'qué te falta', 'que te falta', 'qué no puedes', 'que no puedes',
        'cuáles son tus limitaciones', 'cuales son tus limitaciones',
        'qué mejorarías de ti misma', 'que mejorarias de ti misma',
        'qué harías diferente', 'qué cambias', 'que cambias',
        'en qué eres débil', 'en que eres debil',
        'analízate', 'analizate', 'autoanálisis', 'autoanalisis',
        'qué falla en ti', 'que falla en ti',
        'capacidades te faltan', 'capacidades faltan', 'te faltan', 'faltan para',
        'más útil', 'mas util', 'para mejorar', 'para ser mejor',
    ]):
        return 'introspeccion'

    # Arquitectura general
    if any(p in tl for p in ['arquitectura', 'estructura', 'organización', 'cómo estás organizada',
                               'como estas organizada', 'qué tienes', 'que tienes',
                               'describe', 'cuéntame de ti', 'cuentame de ti']):
        return 'resumen_general'

    # Capacidades reales
    if any(p in tl for p in ['qué funciona', 'que funciona', 'qué opera', 'activo',
                               'disponible', 'operativo']):
        return 'capacidades'

    return 'resumen_general'


def _responder_resumen(e: EscaneoResult) -> str:
    habs = ', '.join(e.habilidades) if e.habilidades else 'ninguna registrada'
    cons = ', '.join(e.consejeras) if e.consejeras else 'ninguna'
    return (
        f"Tengo {e.total_archivos} archivos en total — "
        f"{e.por_tipo.get('Python', 0)} Python, "
        f"{e.por_tipo.get('JavaScript', 0)} JS, "
        f"{e.por_tipo.get('CSS', 0)} CSS, "
        f"{e.por_tipo.get('HTML', 0)} HTML. "
        f"Organizada en 9 capas de procesamiento. "
        f"Habilidades activas en biblioteca: {habs}. "
        f"Consejeras: {cons}. "
        f"Vocabulario: {e.conceptos_vocab} conceptos en {e.modulos_vocab} módulos. "
        f"Total: {e.total_lineas:,} líneas de código."
    )


def _responder_capa(e: EscaneoResult, texto: str) -> str:
    import re as _re2
    match = _re2.search(r'capa\s*([1-9])', texto.lower())

    # Busca en e.archivos directamente — robusto en cualquier OS
    def _archivos_capa(n):
        patron = f'capas/capa{n}/'
        return [a for a in e.archivos
                if patron in a.ruta.replace('\\', '/')]

    if not match:
        # Listar todas las capas
        capas_encontradas = {}
        for a in e.archivos:
            ruta_norm = a.ruta.replace('\\', '/')
            if ruta_norm.startswith('capas/capa'):
                partes = ruta_norm.split('/')
                if len(partes) > 1 and partes[1].startswith('capa'):
                    capas_encontradas.setdefault(partes[1], []).append(a)
        if not capas_encontradas:
            return "No encuentro mis capas."
        resumen = []
        for capa in sorted(capas_encontradas.keys()):
            archs = capas_encontradas[capa]
            resumen.append(f"{capa}: {len(archs)} archivos")
        return "Mis capas: " + ', '.join(resumen) + "."

    num = match.group(1)
    archivos = _archivos_capa(num)

    _DESC_CAPAS = {
        '1': 'recepción y normalización de entrada',
        '2': 'activación de la red neuronal',
        '3': 'comprensión profunda del mensaje',
        '4': 'evaluación de recursos y capacidades',
        '5': 'deliberación con consejeras',
        '6': 'construcción de la respuesta y Groq',
        '7': 'detección y ejecución de habilidades',
        '8': 'formateo y salida final',
        '9': 'integración y actualización post-respuesta',
    }

    desc = _DESC_CAPAS.get(num, '')
    if not archivos:
        return f"No encuentro archivos en capa {num}."

    archivos_str = ', '.join(f"{a.nombre} ({a.lineas} líneas)" for a in archivos)
    return (
        f"Capa {num} — {desc}. "
        f"{len(archivos)} archivos: {archivos_str}."
    )


def _responder_consejeras(e: EscaneoResult, texto: str) -> str:
    _DESC_CONSEJERAS = {
        'soma':  'primera en actuar — verifica integridad de entrada',
        'vega':  'seguridad — tiene poder de veto sobre respuestas riesgosas',
        'nova':  'optimización — busca la respuesta más directa y eficiente',
        'echo':  'lógica y verdad — detecta inconsistencias antes de que salgan',
        'lyra':  'empatía — lee el estado emocional y afina el tono',
        'luna':  'patrones — detecta tendencias en mis conversaciones',
        'iris':  'exploración — amplía el contexto con conocimiento relevante',
        'sage':  'síntesis — orquesta a todas y cristaliza la decisión final',
    }

    tl = texto.lower()
    # Pregunta sobre una consejera específica
    for nombre, desc in _DESC_CONSEJERAS.items():
        if nombre in tl:
            return f"{nombre.capitalize()}: {desc}."

    # Lista todas
    _ROL = {'soma':'entrada','vega':'veto','nova':'optimiz','echo':'logica',
             'lyra':'empatia','luna':'patrones','iris':'exploracion','sage':'sintesis'}
    nombres = e.consejeras or list(_DESC_CONSEJERAS.keys())
    cs = ', '.join(n.capitalize() + '(' + _ROL.get(n,'') + ')' for n in nombres)
    return 'Mis 8 consejeras: ' + cs + '.'


def _responder_vocabulario(e: EscaneoResult) -> str:
    return (
        f"Tengo {e.conceptos_vocab} conceptos distribuidos en "
        f"{e.modulos_vocab} módulos de vocabulario. "
        f"Cubre emociones, tecnología, programación, vida cotidiana, "
        f"colombianismos, identidad de Bell y más."
    )


def _responder_interfaz(e: EscaneoResult) -> str:
    archivos_interfaz = [a for a in e.archivos if a.categoria == 'interfaz']
    js_files   = [a.nombre for a in archivos_interfaz if a.extension == '.js']
    css_files  = [a.nombre for a in archivos_interfaz if a.extension == '.css']
    py_files   = [a.nombre for a in archivos_interfaz if a.extension == '.py']
    html_files = [a.nombre for a in archivos_interfaz if a.extension == '.html']

    return (
        f"Mi interfaz tiene {len(archivos_interfaz)} archivos: "
        f"{len(js_files)} JS ({', '.join(js_files[:5])}), "
        f"{len(css_files)} CSS ({', '.join(css_files)}), "
        f"{len(html_files)} HTML, "
        f"{len(py_files)} Python (servidor Flask y API). "
        f"La visualización 3D usa Three.js con {len([j for j in js_files if 'visualizacion' in j])} "
        f"módulos de visualización."
    )


def _responder_estadisticas(e: EscaneoResult) -> str:
    tipo_str = ', '.join(f"{v} {k}" for k, v in sorted(e.por_tipo.items(), key=lambda x: -x[1]))
    return (
        f"Estadísticas reales: {e.total_archivos} archivos, "
        f"{e.total_lineas:,} líneas de código, "
        f"{e.total_kb:.0f} KB en disco. "
        f"Por tipo: {tipo_str}. "
        f"Por área: {', '.join(f'{v} en {k}' for k, v in sorted(e.por_categoria.items(), key=lambda x: -x[1])[:5])}."
    )


def _responder_archivo(e: EscaneoResult, texto: str) -> str:
    m = re.search(r'(\w+\.(py|js|css|html|json|md))', texto, re.IGNORECASE)
    if not m:
        return "No identifiqué qué archivo me preguntas."
    nombre_buscado = m.group(1).lower()
    encontrados = [a for a in e.archivos if a.nombre.lower() == nombre_buscado]
    if not encontrados:
        return f"No encuentro '{nombre_buscado}' en mi estructura."
    a = encontrados[0]
    # Formato compacto — siempre bajo 280 chars
    partes = [f"{a.nombre} — {a.lineas}L, {a.tamano_kb}KB, {a.ruta.split('/')[-2]}/"]
    if a.clases:
        partes.append(f"Clases: {', '.join(a.clases[:3])}.")
    if a.funciones:
        partes.append(f"Métodos clave: {', '.join(a.funciones[:5])}.")
    return ' '.join(partes)


def _responder_capacidades(e: EscaneoResult) -> str:
    habs_disponibles = []
    habs_pendientes = []

    for hab in e.habilidades:
        # Heurística: si tiene motor.py o __init__ no vacío → disponible
        archivos_hab = [a for a in e.archivos
                        if f'habilidades/{hab}' in a.ruta.replace('\\', '/')]
        tiene_motor = any('motor' in a.nombre for a in archivos_hab)
        if tiene_motor:
            habs_disponibles.append(hab)
        else:
            habs_pendientes.append(hab)

    resp = f"Habilidades con motor activo: {', '.join(habs_disponibles) or 'ninguna confirmada'}."
    if habs_pendientes:
        resp += f" En construcción: {', '.join(habs_pendientes)}."
    return resp



def _construir_contexto_corto(escaneo: EscaneoResult, texto: str, tipo: str) -> str:
    """Contexto mínimo y preciso para la opinión de Groq."""
    import re as _re_ctx
    partes = []
    if tipo == 'archivo_especifico':
        mx = _re_ctx.search(r'(\w[\w_]*\.(?:py|js|css|html|json|md))', texto, _re_ctx.IGNORECASE)
        if mx:
            nombre = mx.group(1).lower()
            encontrados = [a for a in escaneo.archivos if a.nombre.lower() == nombre]
            if encontrados:
                a = encontrados[0]
                partes.append(f"Archivo: {a.nombre} | {a.lineas}L | {a.tamano_kb}KB | {a.ruta}")
                partes.append(f"Clases: {', '.join(a.clases[:4]) or 'ninguna'}")
                partes.append(f"Funciones: {', '.join(a.funciones[:8])}")
    elif tipo == 'analisis_propio':
        grandes = sorted([(a.nombre, a.lineas) for a in escaneo.archivos if a.lineas > 400], key=lambda x: -x[1])[:5]
        partes.append("Archivos grandes: " + ', '.join(f"{n}({l}L)" for n,l in grandes))
        partes.append(f"Habilidades: {', '.join(escaneo.habilidades or ['ninguna'])}")
    elif tipo == 'introspeccion':
        habs = escaneo.habilidades or []
        partes.append(f"Habilidades activas: {', '.join(habs)}")
        faltantes = []
        if not any('calculo' in h for h in habs): faltantes.append("cálculo matemático")
        if not any('busqueda' in h or 'internet' in h for h in habs): faltantes.append("búsqueda web")
        if not any('memoria' in h for h in habs): faltantes.append("memoria persistente")
        if not any('shell' in h for h in habs): faltantes.append("ejecución de comandos")
        if faltantes: partes.append(f"Capacidades faltantes: {', '.join(faltantes)}")
        partes.append(f"Total: {escaneo.total_archivos} archivos, {escaneo.total_lineas} líneas")
    return '\n'.join(partes)

class MotorAutoAnalisis:
    """
    Motor principal del auto-análisis de Bell.
    Lee su propia arquitectura y responde con conocimiento real.
    """

    def procesar(self, texto: str) -> dict:
        """
        Nueva arquitectura: Python genera SIEMPRE la respuesta estructurada completa.
        Groq solo agrega UNA opinión analítica cuando es relevante.
        Resultado: respuestas siempre completas, nunca cortadas.
        """
        try:
            escaneo = _obtener_escaneo()
            tipo    = _detectar_tipo(texto)

            # ── PYTHON genera la respuesta estructurada ───────────────
            if tipo == 'resumen_general':
                base = _responder_resumen(escaneo)
            elif tipo == 'capa_especifica':
                base = _responder_capa(escaneo, texto)
            elif tipo == 'habilidades':
                if escaneo.habilidades:
                    habs = ', '.join(
                        f"{h} ({sum(1 for a in escaneo.archivos if f'habilidades/{h}/' in a.ruta.replace(chr(92),'/'))} archivos)"
                        for h in escaneo.habilidades
                    )
                    base = f"Habilidades en mi biblioteca: {habs}."
                else:
                    base = "No encuentro habilidades registradas en mi biblioteca."
            elif tipo == 'consejeras':
                base = _responder_consejeras(escaneo, texto)
            elif tipo == 'vocabulario':
                base = _responder_vocabulario(escaneo)
            elif tipo == 'interfaz':
                base = _responder_interfaz(escaneo)
            elif tipo == 'estadisticas':
                base = _responder_estadisticas(escaneo)
            elif tipo == 'capacidades':
                base = _responder_capacidades(escaneo)
            elif tipo == 'archivo_especifico':
                base = _responder_archivo(escaneo, texto)
            elif tipo == 'analisis_propio':
                analisis = _analizar_codigo_propio(escaneo.raiz_bell)
                base = _generar_informe_mejoras(analisis, escaneo)
            elif tipo == 'introspeccion':
                base = _introspeccion_cualitativa(escaneo, escaneo.raiz_bell)
            else:
                base = _responder_resumen(escaneo)

            # ── GROQ con radon: análisis profesional con métricas reales ──
            if tipo in ('analisis_propio', 'introspeccion'):
                radon_data = analizar_todo_bell(escaneo.raiz_bell)
                respuesta_groq = _groq_analisis_profundo(texto, radon_data)
                if respuesta_groq:
                    return {'exitoso': True, 'respuesta': respuesta_groq, 'tipo': tipo}
                # Fallback si Groq falla
                respuesta = base
            elif tipo == 'archivo_especifico':
                # Extraer nombre del archivo de la pregunta
                import re as _re_arch
                m_arch = _re_arch.search(r'(\w[\w_]*\.(?:py|js|css|html|json|md))', texto, _re_arch.IGNORECASE)
                if m_arch:
                    nombre = m_arch.group(1)
                    radon_data = analizar_archivo(nombre, escaneo.raiz_bell)
                    respuesta_groq = _groq_analisis_profundo(texto, radon_data)
                    if respuesta_groq:
                        return {'exitoso': True, 'respuesta': respuesta_groq, 'tipo': tipo}
                respuesta = base
            else:
                respuesta = base

            return {'exitoso': True, 'respuesta': respuesta, 'tipo': tipo}

        except Exception as e:
            return {
                'exitoso': False,
                'respuesta': f"No pude leerme a mí misma: {str(e)[:80]}",
                'tipo': 'error',
            }


def ejecutar_auto_analisis(texto: str) -> dict:
    return MotorAutoAnalisis().procesar(texto)


# ══════════════════════════════════════════════════════════════
# NIVEL 2 — BELL ANALIZA SU PROPIO CÓDIGO
# ══════════════════════════════════════════════════════════════

def _analizar_codigo_propio(raiz_str: str) -> dict:
    """
    Lee y analiza todos los archivos Python de Bell.
    Detecta problemas reales y genera un informe honesto.
    """
    import ast as _ast

    raiz = Path(raiz_str)
    _IGNORAR_DIRS = {'__pycache__', '.git', 'venv', '.venv', 'node_modules', 'dist'}

    archivos_grandes     = []
    sin_documentacion    = []
    desconectados        = []
    habilidades_vacias   = []
    archivos_criticos    = []

    total_py    = 0
    total_lineas = 0

    for ruta in raiz.rglob('*.py'):
        if any(p in ruta.parts for p in _IGNORAR_DIRS):
            continue

        try:
            with open(ruta, 'r', encoding='utf-8', errors='ignore') as f:
                contenido = f.read()

            lineas = contenido.count('\n') + 1
            total_py     += 1
            total_lineas += lineas
            rel = str(ruta.relative_to(raiz)).replace('\\', '/')

            # Archivos grandes (> 400 líneas)
            if lineas > 400:
                archivos_grandes.append((rel, lineas))

            # Análisis AST
            try:
                tree = _ast.parse(contenido)
                sin_doc_count = 0
                for node in _ast.walk(tree):
                    if isinstance(node, (_ast.FunctionDef, _ast.AsyncFunctionDef)):
                        if not _ast.get_docstring(node):
                            sin_doc_count += 1
                if sin_doc_count > 8:
                    sin_documentacion.append((rel, sin_doc_count))
            except Exception:
                pass

            # Archivos críticos — los más importantes del pipeline
            _CRITICOS = {
                'capas/capa6/constructor_decision.py': 'construye toda respuesta',
                'capas/capa6/generador_groq.py':       'motor de lenguaje Groq',
                'capas/capa3/constructor_comprension.py': 'comprensión profunda',
                'biblioteca/habilidades/lenguaje/motor.py': 'motor de lenguaje',
                'capas/capa7/detector_habilidad.py':   'detección de habilidades',
            }
            if rel in _CRITICOS and lineas > 500:
                archivos_criticos.append((rel, lineas, _CRITICOS[rel]))

        except Exception:
            pass

    # Habilidades sin motor (incompletas)
    habs_dir = raiz / 'biblioteca' / 'habilidades'
    if habs_dir.exists():
        for d in habs_dir.iterdir():
            if d.is_dir() and not d.name.startswith('_'):
                tiene_motor = any('motor' in f.name for f in d.rglob('*.py'))
                if not tiene_motor:
                    habilidades_vacias.append(d.name)

    return {
        'total_py':           total_py,
        'total_lineas':       total_lineas,
        'archivos_grandes':   sorted(archivos_grandes,   key=lambda x: -x[1])[:6],
        'sin_documentacion':  sorted(sin_documentacion,  key=lambda x: -x[1])[:5],
        'habilidades_vacias': habilidades_vacias,
        'archivos_criticos':  archivos_criticos,
    }


def _generar_informe_mejoras(analisis: dict, escaneo=None) -> str:
    """Informe conciso — siempre 3 puntos, siempre completo."""
    puntos = []

    # 1. Archivos más grandes (top 3) — siempre hay
    top3 = analisis['archivos_grandes'][:3]
    if top3:
        lista = ', '.join(f"{r.split('/')[-1]}({n}L)" for r,n in top3)
        puntos.append(f"1. Archivos grandes: {lista}.")

    # 2. Sin documentación o habilidades vacías
    if analisis['habilidades_vacias']:
        puntos.append(f"2. Habilidades sin motor: {', '.join(analisis['habilidades_vacias'])}.")
    elif analisis['sin_documentacion']:
        sin_doc = ', '.join(r.split('/')[-1] for r,_ in analisis['sin_documentacion'][:3])
        puntos.append(f"2. Sin docstrings: {sin_doc}.")

    # 3. Capacidades del sistema que faltan — siempre hay (búsqueda, memoria, cálculo)
    habs = (escaneo.habilidades if escaneo else []) or []
    faltantes = []
    if not any('calculo' in h.lower() for h in habs): faltantes.append("cálculo")
    if not any('busqueda' in h.lower() or 'internet' in h.lower() for h in habs): faltantes.append("búsqueda web")
    if not any('memoria' in h.lower() for h in habs): faltantes.append("memoria")
    if faltantes:
        puntos.append(f"3. Capacidades faltantes: {', '.join(faltantes)}.")

    return ' '.join(puntos) if puntos else "Arquitectura saludable."



def _introspeccion_cualitativa(escaneo: EscaneoResult, raiz: str) -> str:
    """Qué le falta a Bell — respuesta directa, siempre completa."""
    habs = escaneo.habilidades or []
    faltantes = []
    if not any('calculo' in h.lower() or 'matematica' in h.lower() for h in habs):
        faltantes.append("cálculo matemático")
    if not any('busqueda' in h.lower() or 'internet' in h.lower() for h in habs):
        faltantes.append("búsqueda web / internet")
    if not any('memoria' in h.lower() for h in habs):
        faltantes.append("memoria persistente")
    if not any('shell' in h.lower() or 'comando' in h.lower() for h in habs):
        faltantes.append("ejecución de comandos")

    if faltantes:
        resp = f"Me faltan: {', '.join(faltantes)}."
        resp += " Sin búsqueda web no accedo a información nueva. Sin memoria no recuerdo entre sesiones."
        return resp
    return "Habilidades activas completas según mi registro actual."