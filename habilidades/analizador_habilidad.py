# -*- coding: utf-8 -*-
"""
habilidades/analizador_habilidad.py — VERSION v1.1

CAMBIOS v1.1 sobre v1.0:
═══════════════════════════════════════════════════════════════════
FIX-A1  "analiza nova/vega/echo/lyra/luna/iris/sage" → operación vacía
        CAUSA: patrones de consejeras individuales no tenían grupo de
               captura (\w+), entonces extra="" y modulo="" → la
               operación analizar_modulo no encontraba el archivo.
        FIX:  Unificar todas las consejeras en un solo patrón con
               grupo de captura: r'anali[sz]a(?:r)?\s+(nova|vega|echo|...)'
               Agregar los 7 nombres completos.

FIX-A2  "métricas de Bell", "estadísticas de Bell", "score de Bell"
        → DESCONOCIDO
        CAUSA: _MAPA_ANALISIS solo cubría frases con "código" o
               "líneas" o "funciones". La palabra "Bell" sola no
               disparaba metricas_generales.
        FIX:  Agregar patrones sin "código" al bloque metricas_generales:
               r'metricas?\s+de\s+bell', r'estad[ií]sticas?\s+de\s+bell',
               r'score\s+de\s+bell', r'tama[nñ]o\s+de\s+bell',
               r'qu[eé]\s+tan\s+grande\s+es\s+bell', etc.

FIX-A3  Análisis de archivo por RUTA ABSOLUTA (Windows/Linux)
        CAUSA: _op_analizar_archivo() solo buscaba dentro del proyecto
               Bell usando rglob. No aceptaba rutas absolutas tipo
               C:\mis_scripts\archivo.py o /home/user/codigo.py.
        FIX:  Antes de buscar con rglob, verificar si el string
               recibido es una ruta absoluta válida que existe en disco.
               Si existe → leerla directamente.
               Esto permite: "analiza C:\ruta\mi_funcion.py"

Todo el código v1.0 preservado intacto fuera de los tres fixes.
═══════════════════════════════════════════════════════════════════
"""

import ast
import re
import logging
from pathlib import Path
from typing import Optional, Dict, List, Any, Tuple
from dataclasses import dataclass, field

from habilidades.registro_habilidades import (
    BaseHabilidad,
    HabilidadMatch,
    ResultadoHabilidad,
)

logger = logging.getLogger("habilidades.analizador_python")


# ======================================================================
# ESTRUCTURAS DE DATOS — idénticas a v1.0
# ======================================================================

@dataclass
class InfoFuncion:
    nombre:      str
    linea:       int
    complejidad: int
    num_args:    int
    tiene_doc:   bool
    tiene_hints: bool
    lineas:      int


@dataclass
class InfoClase:
    nombre:      str
    linea:       int
    num_metodos: int
    tiene_doc:   bool
    hereda_de:   List[str] = field(default_factory=list)


@dataclass
class Problema:
    tipo:        str
    descripcion: str
    linea:       Optional[int] = None
    nombre:      Optional[str] = None


@dataclass
class MetricasArchivo:
    lineas_total:      int   = 0
    lineas_codigo:     int   = 0
    lineas_comentario: int   = 0
    lineas_docstring:  int   = 0
    lineas_vacias:     int   = 0
    num_funciones:     int   = 0
    num_clases:        int   = 0
    num_imports:       int   = 0
    complejidad_total: int   = 0
    complejidad_prom:  float = 0.0
    complejidad_max:   int   = 0
    funcion_max_comp:  str   = ""
    ratio_comentarios: float = 0.0
    tiene_type_hints:  bool  = False


@dataclass
class ResultadoAnalisis:
    archivo:         str               = ""
    exitoso:         bool              = False
    error_parse:     str               = ""
    metricas:        MetricasArchivo   = field(default_factory=MetricasArchivo)
    funciones:       List[InfoFuncion] = field(default_factory=list)
    clases:          List[InfoClase]   = field(default_factory=list)
    imports:         List[str]         = field(default_factory=list)
    problemas:       List[Problema]    = field(default_factory=list)
    score_calidad:   int               = 0
    recomendaciones: List[str]         = field(default_factory=list)
    resumen_nova:    str               = ""


# ======================================================================
# MAPA DE INTENCIÓN → OPERACIÓN
# FIX-A1: patrones de consejeras con grupo de captura
# FIX-A2: patrones de métricas sin requerir "código"
# ======================================================================

_MAPA_ANALISIS: list = [

    # ── Análisis completo de Bell ─────────────────────────────────────
    (
        [r'anali[sz]a(?:r)?\s+(?:tu\s+)?(?:propio\s+)?c[oó]digo',
         r'anali[sz]a(?:r)?\s+(?:a\s+)?bell\b',
         r'anali[sz]a(?:r)?\s+(?:el\s+)?sistema',
         r'revisa(?:r)?\s+(?:tu\s+)?c[oó]digo',
         r'inspecci[oó]n\s+(?:de\s+)?bell',
         r'c[oó]mo\s+est[aá]\s+(?:tu\s+)?c[oó]digo',
         r'qu[eé]\s+tal\s+(?:tu\s+)?c[oó]digo'],
        "analizar_bell",
        "Análisis completo del código de Bell",
    ),

    # ── Consejeras individuales — FIX-A1 ─────────────────────────────
    # Un solo patrón con grupo de captura para las 7 consejeras.
    # Antes: patrones separados sin (\w+) → extra="" → modulo="" → falla.
    # Ahora: un regex captura el nombre y lo pasa como extra.
    (
        [r'anali[sz]a(?:r)?\s+(?:la\s+)?(?:consejera\s+)?(nova|vega|echo|lyra|luna|iris|sage)\b',
         r'revisa(?:r)?\s+(?:la\s+)?(?:consejera\s+)?(nova|vega|echo|lyra|luna|iris|sage)\b',
         r'c[oó]mo\s+est[aá]\s+(?:la\s+)?(nova|vega|echo|lyra|luna|iris|sage)\b',
         r'qu[eé]\s+hace\s+(?:la\s+)?(nova|vega|echo|lyra|luna|iris|sage)\b'],
        "analizar_modulo",
        "Análisis de consejera Bell",
    ),

    # ── Módulo Bell específico (no-consejera) ─────────────────────────
    (
        [r'anali[sz]a(?:r)?\s+(?:el\s+)?motor(?:_razonamiento)?',
         r'anali[sz]a(?:r)?\s+(?:el\s+)?generador',
         r'anali[sz]a(?:r)?\s+(?:el\s+)?registro',
         r'anali[sz]a(?:r)?\s+(?:el\s+)?m[oó]dulo\s+(\w+)',
         r'anali[sz]a(?:r)?\s+(?:la\s+)?habilidad\s+(\w+)',
         r'qu[eé]\s+hace\s+(?:el\s+)?motor',
         r'estructura\s+del?\s+motor',
         r'c[oó]mo\s+est[aá]\s+(?:el\s+)?m[oó]dulo\s+(\w+)',
         r'qu[eé]\s+contiene\s+(?:el\s+)?m[oó]dulo\s+(\w+)',
         r'anali[sz]a(?:r)?\s+(?:el\s+)?main'],
        "analizar_modulo",
        "Análisis de módulo Bell específico",
    ),

    # ── Archivo .py por nombre o ruta — FIX-A3 ───────────────────────
    # Acepta: "analiza motor_razonamiento.py"
    # Acepta: "analiza C:\ruta\archivo.py"  (ruta absoluta Windows)
    # Acepta: "analiza /home/user/archivo.py" (ruta absoluta Linux)
    (
        [r'anali[sz]a(?:r)?\s+([A-Za-z]:\\[^\s]+\.py)',          # ruta Windows
         r'anali[sz]a(?:r)?\s+(/[^\s]+\.py)',                     # ruta Linux/Mac
         r'anali[sz]a(?:r)?\s+(\w+\.py)',                         # nombre simple
         r'revisa(?:r)?\s+([A-Za-z]:\\[^\s]+\.py)',
         r'revisa(?:r)?\s+(/[^\s]+\.py)',
         r'revisa(?:r)?\s+(\w+\.py)',
         r'qu[eé]\s+problemas?\s+(?:tiene|hay\s+en)\s+(\w+\.py)',
         r'complejidad\s+de\s+(\w+\.py)',
         r'calidad\s+de\s+(\w+\.py)',
         r'metricas?\s+de\s+(\w+\.py)',
         r'c[oó]mo\s+est[aá]\s+(\w+\.py)',
         r'errores?\s+en\s+(\w+\.py)',
         r'score\s+de\s+(\w+\.py)'],
        "analizar_archivo",
        "Análisis de archivo Python por nombre o ruta",
    ),

    # ── Código inline ─────────────────────────────────────────────────
    (
        [r'anali[sz]a(?:r)?\s+(?:este\s+)?c[oó]digo',
         r'revisa(?:r)?\s+(?:este\s+)?c[oó]digo',
         r'qu[eé]\s+(?:problemas?|errores?)\s+tiene\s+(?:este\s+)?c[oó]digo',
         r'qu[eé]\s+est[aá]\s+mal\s+(?:en\s+)?(?:este\s+)?c[oó]digo',
         r'qu[eé]\s+piensas?\s+(?:de\s+)?(?:este\s+)?c[oó]digo',
         r'mejora(?:r)?\s+(?:este\s+)?c[oó]digo',
         r'c[oó]mo\s+mejorar[ií]as?\s+(?:este\s+)?c[oó]digo',
         r'```python',
         r'analiza\s+(?:el\s+)?siguiente\s+c[oó]digo'],
        "analizar_inline",
        "Análisis de código Python inline",
    ),

    # ── Métricas generales Bell — FIX-A2 ─────────────────────────────
    # Antes: solo cubría frases con "código", "líneas", "funciones".
    # Ahora: cubre también "métricas de Bell", "estadísticas de Bell",
    #        "score de Bell", "tamaño de Bell", etc.
    (
        [r'metricas?\s+(?:del?\s+|de\s+tu\s+)?c[oó]digo',
         r'metricas?\s+de\s+bell',                      # FIX-A2
         r'calidad\s+del?\s+c[oó]digo',
         r'complejidad\s+(?:del?\s+c[oó]digo|de\s+bell)',
         r'qu[eé]\s+tan\s+(?:bueno|complejo|grande)\s+es\s+(?:tu\s+)?c[oó]digo',
         r'qu[eé]\s+tan\s+grande\s+es\s+bell',         # FIX-A2
         r'cu[aá]ntas?\s+l[ií]neas?\s+(?:tiene|tienes)',
         r'cu[aá]ntas?\s+funciones?\s+(?:tiene|tienes)',
         r'cu[aá]ntas?\s+clases?\s+(?:tiene|tienes)',
         r'tama[nñ]o\s+(?:de\s+)?bell',
         r'estad[ií]sticas?\s+(?:de\s+)?bell',         # FIX-A2
         r'estad[ií]sticas?\s+del?\s+c[oó]digo',
         r'resumen\s+del?\s+c[oó]digo',
         r'score\s+(?:de\s+)?bell',                    # FIX-A2
         r'score\s+(?:del?\s+)?c[oó]digo',
         r'cu[aá]nto\s+c[oó]digo\s+(?:tiene|tienes)',  # FIX-A2
         r'cu[aá]ntas?\s+l[ií]neas?\s+(?:tiene|tienes)\s+bell'],  # FIX-A2
        "metricas_generales",
        "Métricas generales del sistema Bell",
    ),
]

# Módulos Bell conocidos → ruta relativa desde raíz del proyecto
_MODULOS_BELL: Dict[str, str] = {
    'motor':                 'razonamiento/motor_razonamiento.py',
    'motor_razonamiento':    'razonamiento/motor_razonamiento.py',
    'tipos_decision':        'razonamiento/tipos_decision.py',
    'patrones':              'razonamiento/patrones_habilidades.py',
    'patrones_habilidades':  'razonamiento/patrones_habilidades.py',
    'generador':             'generacion/generador_salida.py',
    'generador_salida':      'generacion/generador_salida.py',
    'generador_ejecutores':  'generacion/generador_ejecutores.py',
    'ejecutores':            'generacion/generador_ejecutores.py',
    'registro':              'habilidades/registro_habilidades.py',
    'registro_habilidades':  'habilidades/registro_habilidades.py',
    'shell':                 'habilidades/shell_habilidad.py',
    'shell_habilidad':       'habilidades/shell_habilidad.py',
    'sqlite':                'habilidades/sqlite_habilidad.py',
    'sqlite_habilidad':      'habilidades/sqlite_habilidad.py',
    'analizador':            'habilidades/analizador_habilidad.py',
    'analizador_habilidad':  'habilidades/analizador_habilidad.py',
    'main':                  'main.py',
    # ── Las 7 consejeras ─────────────────────────────────────────────
    'vega':                  'consejeras/vega/logica.py',
    'nova':                  'consejeras/nova/logica.py',
    'echo':                  'consejeras/echo/logica.py',
    'lyra':                  'consejeras/lyra/logica.py',
    'luna':                  'consejeras/luna/logica.py',
    'iris':                  'consejeras/iris/logica.py',
    'sage':                  'consejeras/sage/logica.py',
    # ── Core ─────────────────────────────────────────────────────────
    'capacidades':           'core/capacidades_fase.py',
    'capacidades_fase':      'core/capacidades_fase.py',
}

# Directorios/patrones a excluir del escaneo masivo
_EXCLUIR = {
    '__pycache__', '.git', 'venv', 'env', '.env',
    'node_modules', '.pytest_cache', 'dist', 'build',
}

_EXCLUIR_NOMBRES = {'test_', '_test', 'semana', 'semana1', 'semana2',
                     'semana3', 'semana4', 'semana5', 'semana6'}


def _detectar_operacion_analisis(msg: str) -> Optional[tuple]:
    """
    Retorna (op_id, descripcion, extra) o None.
    extra = primer grupo de captura del regex que matcheó, o "".
    """
    for patrones, op_id, desc in _MAPA_ANALISIS:
        for patron in patrones:
            m = re.search(patron, msg, re.IGNORECASE)
            if m:
                extra = m.group(1) if m.lastindex and m.lastindex >= 1 else ""
                return (op_id, desc, extra)
    return None


# ======================================================================
# ANALIZADOR AST INTERNO — idéntico a v1.0
# ======================================================================

class AnalizadorPythonAST:
    """
    Analizador Python usando ast estándar.
    Sin dependencias externas. Compatible con Python 3.8+.
    """

    def analizar_codigo(self, codigo: str, nombre: str = "código") -> ResultadoAnalisis:
        resultado = ResultadoAnalisis(archivo=nombre)

        try:
            arbol = ast.parse(codigo)
        except SyntaxError as e:
            resultado.exitoso     = False
            resultado.error_parse = f"SyntaxError en línea {e.lineno}: {e.msg}"
            return resultado
        except Exception as e:
            resultado.exitoso     = False
            resultado.error_parse = f"No se pudo parsear: {e}"
            return resultado

        resultado.exitoso = True
        lineas = codigo.split('\n')

        rangos_doc = self._rangos_docstrings(arbol)
        resultado.metricas = self._analizar_lineas(lineas, rangos_doc)

        resultado.funciones = self._inventario_funciones(arbol)
        resultado.metricas.num_funciones = len(resultado.funciones)

        resultado.clases = self._inventario_clases(arbol)
        resultado.metricas.num_clases = len(resultado.clases)

        resultado.imports = self._extraer_imports(arbol)
        resultado.metricas.num_imports = len(resultado.imports)

        self._poblar_complejidad(resultado)

        resultado.metricas.tiene_type_hints = self._tiene_type_hints(arbol)

        resultado.problemas = self._detectar_problemas(arbol)

        resultado.score_calidad, resultado.recomendaciones = \
            self._calcular_score(resultado)

        resultado.resumen_nova = self._generar_resumen_nova(resultado)

        return resultado

    # ------------------------------------------------------------------
    # Líneas
    # ------------------------------------------------------------------

    def _rangos_docstrings(self, arbol) -> set:
        lineas_doc = set()
        for nodo in ast.walk(arbol):
            if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef,
                                  ast.ClassDef, ast.Module)):
                if nodo.body and isinstance(nodo.body[0], ast.Expr):
                    val = nodo.body[0].value
                    if isinstance(val, ast.Constant) and isinstance(val.value, str):
                        inicio = getattr(val, 'lineno', 0)
                        fin    = getattr(val, 'end_lineno', inicio)
                        for ln in range(inicio, fin + 1):
                            lineas_doc.add(ln)
        return lineas_doc

    def _analizar_lineas(self, lineas: List[str], rangos_doc: set) -> MetricasArchivo:
        m = MetricasArchivo()
        m.lineas_total = len(lineas)
        for i, linea in enumerate(lineas, 1):
            strip = linea.strip()
            if not strip:
                m.lineas_vacias += 1
            elif strip.startswith('#'):
                m.lineas_comentario += 1
            elif i in rangos_doc:
                m.lineas_docstring += 1
            else:
                m.lineas_codigo += 1
        no_vacio = m.lineas_codigo + m.lineas_comentario + m.lineas_docstring
        if no_vacio > 0:
            m.ratio_comentarios = (m.lineas_comentario + m.lineas_docstring) / no_vacio
        return m

    # ------------------------------------------------------------------
    # Inventario
    # ------------------------------------------------------------------

    def _inventario_funciones(self, arbol) -> List[InfoFuncion]:
        fns = []
        for nodo in ast.walk(arbol):
            if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
                tiene_doc = (
                    bool(nodo.body)
                    and isinstance(nodo.body[0], ast.Expr)
                    and isinstance(nodo.body[0].value, ast.Constant)
                    and isinstance(nodo.body[0].value.value, str)
                )
                tiene_hints = (
                    any(a.annotation for a in nodo.args.args)
                    or nodo.returns is not None
                )
                fin    = getattr(nodo, 'end_lineno', nodo.lineno)
                lineas = fin - nodo.lineno + 1
                fns.append(InfoFuncion(
                    nombre      = nodo.name,
                    linea       = nodo.lineno,
                    complejidad = self._complejidad_nodo(nodo),
                    num_args    = len(nodo.args.args),
                    tiene_doc   = tiene_doc,
                    tiene_hints = tiene_hints,
                    lineas      = lineas,
                ))
        return fns

    def _inventario_clases(self, arbol) -> List[InfoClase]:
        clases = []
        for nodo in ast.walk(arbol):
            if isinstance(nodo, ast.ClassDef):
                tiene_doc = (
                    bool(nodo.body)
                    and isinstance(nodo.body[0], ast.Expr)
                    and isinstance(nodo.body[0].value, ast.Constant)
                    and isinstance(nodo.body[0].value.value, str)
                )
                metodos = [
                    n for n in ast.walk(nodo)
                    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                ]
                hereda = []
                for base in nodo.bases:
                    if isinstance(base, ast.Name):
                        hereda.append(base.id)
                    elif isinstance(base, ast.Attribute):
                        hereda.append(base.attr)
                clases.append(InfoClase(
                    nombre      = nodo.name,
                    linea       = nodo.lineno,
                    num_metodos = len(metodos),
                    tiene_doc   = tiene_doc,
                    hereda_de   = hereda,
                ))
        return clases

    def _extraer_imports(self, arbol) -> List[str]:
        imports = []
        for nodo in ast.walk(arbol):
            if isinstance(nodo, ast.Import):
                for alias in nodo.names:
                    imports.append(alias.name)
            elif isinstance(nodo, ast.ImportFrom):
                mod = nodo.module or ""
                for alias in nodo.names:
                    imports.append(f"{mod}.{alias.name}" if mod else alias.name)
        return imports

    # ------------------------------------------------------------------
    # Complejidad ciclomática McCabe
    # ------------------------------------------------------------------

    def _complejidad_nodo(self, nodo) -> int:
        c = 1
        for n in ast.walk(nodo):
            if isinstance(n, (ast.If, ast.While, ast.For, ast.ExceptHandler,
                               ast.With, ast.Assert, ast.AsyncFor, ast.AsyncWith)):
                c += 1
            elif isinstance(n, ast.BoolOp):
                c += len(n.values) - 1
            elif isinstance(n, (ast.ListComp, ast.SetComp,
                                  ast.DictComp, ast.GeneratorExp)):
                c += 1
        return c

    def _poblar_complejidad(self, r: ResultadoAnalisis):
        if not r.funciones:
            r.metricas.complejidad_total = 1
            r.metricas.complejidad_prom  = 1.0
            return
        comps = [f.complejidad for f in r.funciones]
        r.metricas.complejidad_total = sum(comps)
        r.metricas.complejidad_prom  = sum(comps) / len(comps)
        r.metricas.complejidad_max   = max(comps)
        idx = comps.index(max(comps))
        r.metricas.funcion_max_comp  = r.funciones[idx].nombre

    # ------------------------------------------------------------------
    # Type hints
    # ------------------------------------------------------------------

    def _tiene_type_hints(self, arbol) -> bool:
        for nodo in ast.walk(arbol):
            if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if any(a.annotation for a in nodo.args.args) or nodo.returns:
                    return True
        return False

    # ------------------------------------------------------------------
    # Detección de problemas
    # ------------------------------------------------------------------

    def _detectar_problemas(self, arbol) -> List[Problema]:
        problemas = []

        nombres_usados: set = set()
        for n in ast.walk(arbol):
            if isinstance(n, ast.Name):
                nombres_usados.add(n.id)
            elif isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name):
                nombres_usados.add(n.value.id)

        for nodo in ast.walk(arbol):

            if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if not nodo.name.startswith('_'):
                    tiene_doc = (
                        bool(nodo.body)
                        and isinstance(nodo.body[0], ast.Expr)
                        and isinstance(nodo.body[0].value, ast.Constant)
                        and isinstance(nodo.body[0].value.value, str)
                    )
                    if not tiene_doc:
                        problemas.append(Problema(
                            tipo="sugerencia",
                            descripcion=f"Función '{nodo.name}' sin docstring",
                            linea=nodo.lineno, nombre=nodo.name,
                        ))

                fin = getattr(nodo, 'end_lineno', nodo.lineno)
                if (fin - nodo.lineno + 1) > 50:
                    problemas.append(Problema(
                        tipo="advertencia",
                        descripcion=f"Función '{nodo.name}' muy larga "
                                    f"({fin - nodo.lineno + 1} líneas). Considera dividirla.",
                        linea=nodo.lineno, nombre=nodo.name,
                    ))

                comp = self._complejidad_nodo(nodo)
                if comp > 15:
                    problemas.append(Problema(
                        tipo="advertencia",
                        descripcion=f"Función '{nodo.name}' complejidad muy alta ({comp}). Refactorizar.",
                        linea=nodo.lineno, nombre=nodo.name,
                    ))
                elif comp > 10:
                    problemas.append(Problema(
                        tipo="sugerencia",
                        descripcion=f"Función '{nodo.name}' complejidad alta ({comp}). Considerar simplificar.",
                        linea=nodo.lineno, nombre=nodo.name,
                    ))

                if re.search(r'[a-z][A-Z]', nodo.name) and not nodo.name.startswith('__'):
                    problemas.append(Problema(
                        tipo="sugerencia",
                        descripcion=f"'{nodo.name}' usa camelCase. PEP8 recomienda snake_case.",
                        linea=nodo.lineno, nombre=nodo.name,
                    ))

            elif isinstance(nodo, ast.ClassDef):
                tiene_doc = (
                    bool(nodo.body)
                    and isinstance(nodo.body[0], ast.Expr)
                    and isinstance(nodo.body[0].value, ast.Constant)
                    and isinstance(nodo.body[0].value.value, str)
                )
                if not tiene_doc:
                    problemas.append(Problema(
                        tipo="sugerencia",
                        descripcion=f"Clase '{nodo.name}' sin docstring",
                        linea=nodo.lineno, nombre=nodo.name,
                    ))

            elif isinstance(nodo, ast.Import):
                for alias in nodo.names:
                    nombre_local = alias.asname or alias.name.split('.')[0]
                    if nombre_local not in nombres_usados:
                        problemas.append(Problema(
                            tipo="sugerencia",
                            descripcion=f"Import '{alias.name}' posiblemente sin usar",
                            linea=nodo.lineno, nombre=alias.name,
                        ))

        return problemas

    # ------------------------------------------------------------------
    # Score de calidad 0–100
    # ------------------------------------------------------------------

    def _calcular_score(self, r: ResultadoAnalisis) -> Tuple[int, List[str]]:
        score = 100
        recomendaciones = []

        sin_doc = sum(1 for p in r.problemas if 'sin docstring' in p.descripcion)
        score -= min(sin_doc * 5, 20)
        if sin_doc:
            recomendaciones.append(
                f"Agregar docstrings a {sin_doc} función(es)/clase(s) — mejora mantenibilidad."
            )

        imp_sin_usar = sum(
            1 for p in r.problemas if 'posiblemente sin usar' in p.descripcion
        )
        score -= min(imp_sin_usar * 3, 12)
        if imp_sin_usar:
            recomendaciones.append(f"Limpiar {imp_sin_usar} import(s) que no se usan.")

        muy_alta = sum(1 for p in r.problemas if 'muy alta' in p.descripcion)
        alta     = sum(
            1 for p in r.problemas
            if 'complejidad alta' in p.descripcion and 'muy' not in p.descripcion
        )
        score -= muy_alta * 8
        score -= alta * 4
        if muy_alta:
            recomendaciones.append(
                f"Refactorizar {muy_alta} función(es) con complejidad > 15."
            )
        elif alta:
            recomendaciones.append(
                f"Simplificar {alta} función(es) con complejidad entre 10 y 15."
            )

        largas = sum(1 for p in r.problemas if 'muy larga' in p.descripcion)
        score -= largas * 3
        if largas:
            recomendaciones.append(
                f"Dividir {largas} función(es) de más de 50 líneas."
            )

        camel = sum(1 for p in r.problemas if 'camelCase' in p.descripcion)
        score -= min(camel * 2, 6)
        if camel:
            recomendaciones.append("Renombrar funciones a snake_case (convención PEP8).")

        if r.metricas.ratio_comentarios > 0.15:
            score += 5

        if r.metricas.tiene_type_hints:
            score += 5
            recomendaciones.append("✅ Tiene type hints — buena práctica.")

        if not recomendaciones:
            recomendaciones.append(
                "✅ Código en buen estado. Sin problemas críticos detectados."
            )

        return max(0, min(100, score)), recomendaciones

    # ------------------------------------------------------------------
    # Resumen Nova
    # ------------------------------------------------------------------

    def _generar_resumen_nova(self, r: ResultadoAnalisis) -> str:
        m = r.metricas
        s = r.score_calidad
        if s >= 85:    valoracion = "excelente"
        elif s >= 70:  valoracion = "buena"
        elif s >= 50:  valoracion = "mejorable"
        else:          valoracion = "necesita trabajo"

        errores      = sum(1 for p in r.problemas if p.tipo == "error")
        advertencias = sum(1 for p in r.problemas if p.tipo == "advertencia")
        sugerencias  = sum(1 for p in r.problemas if p.tipo == "sugerencia")

        txt = (
            f"Calidad {valoracion} ({s}/100). "
            f"{m.lineas_total} líneas ({m.lineas_codigo} código, "
            f"{m.lineas_comentario + m.lineas_docstring} documentación). "
            f"{m.num_funciones} funciones, {m.num_clases} clases."
        )
        if m.num_funciones > 0:
            txt += (
                f" Complejidad promedio {m.complejidad_prom:.1f}"
                f" (máx {m.complejidad_max} en '{m.funcion_max_comp}')."
            )
        if errores:      txt += f" {errores} error(es)."
        if advertencias: txt += f" {advertencias} advertencia(s)."
        if sugerencias:  txt += f" {sugerencias} sugerencia(s)."
        return txt.strip()


# Instancia global del analizador AST
_analizador_ast = AnalizadorPythonAST()


# ======================================================================
# HABILIDAD PRINCIPAL — v1.1
# ======================================================================

class HabilidadAnalisisPython(BaseHabilidad):
    """
    Habilidad de análisis de código Python para Bell.

    Nova es la consejera propietaria.
    Vega aprueba (solo lectura = sin riesgo).
    Echo verifica coherencia del reporte.

    v1.1: FIX-A1 consejeras, FIX-A2 métricas Bell, FIX-A3 rutas absolutas.
    """

    def __init__(self):
        self._analizador_externo = None

    @property
    def id(self) -> str:
        return "ANALISIS_PYTHON"

    @property
    def descripcion_para_bell(self) -> str:
        return (
            "Análisis de código Python: métricas LOC, funciones, clases, "
            "complejidad ciclomática McCabe, detección de problemas (sin docstring, "
            "imports sin usar, alta complejidad, funciones largas), score de calidad "
            "0-100 y recomendaciones arquitectónicas. Nova interpreta los resultados. "
            "Puede analizar el código interno de Bell, archivos .py o rutas absolutas."
        )

    @property
    def consejeras_requeridas(self) -> list:
        return ["Nova", "Echo", "Vega"]

    # ------------------------------------------------------------------
    # Inyección
    # ------------------------------------------------------------------

    def configurar_analizador(self, analizador_externo):
        self._analizador_externo = analizador_externo
        logger.info("HabilidadAnalisisPython: analizador externo inyectado")

    def _obtener_analizador(self) -> AnalizadorPythonAST:
        return _analizador_ast

    # ------------------------------------------------------------------
    # Detección
    # ------------------------------------------------------------------

    def detectar(self, mensaje: str, conceptos: list, hechos: dict) -> Optional[HabilidadMatch]:
        msg = mensaje.lower().strip() if mensaje else ""
        if not msg:
            return None

        verbos_cap = ['puedes', 'sabes', 'eres capaz', 'podrias', 'es posible']
        if any(v in msg for v in verbos_cap):
            return None

        res = _detectar_operacion_analisis(msg)
        if res is None:
            return None

        op_id, descripcion, extra = res

        parametros = {
            "operacion":   op_id,
            "descripcion": descripcion,
            "extra":       extra,
            "mensaje":     mensaje,
        }

        if op_id == "analizar_modulo":
            # extra puede ser nombre de consejera (FIX-A1) o nombre de módulo
            nombre_mod = extra.lower() if extra else self._extraer_nombre_modulo(msg)
            parametros["modulo"]      = nombre_mod
            parametros["archivo_rel"] = _MODULOS_BELL.get(nombre_mod, "")

        elif op_id == "analizar_archivo":
            # extra puede ser ruta absoluta o nombre simple (FIX-A3)
            if extra:
                parametros["archivo"] = extra
            else:
                parametros["archivo"] = self._extraer_nombre_archivo(msg)

        return HabilidadMatch(
            habilidad_id="ANALISIS_PYTHON",
            confianza=0.91,
            parametros=parametros,
            habilidad=self,
        )

    def _extraer_nombre_modulo(self, msg: str) -> str:
        for clave in _MODULOS_BELL:
            if clave in msg:
                return clave
        return ""

    def _extraer_nombre_archivo(self, msg: str) -> str:
        # Ruta absoluta Windows: C:\...
        m = re.search(r'([A-Za-z]:\\[^\s]+\.py)', msg, re.IGNORECASE)
        if m:
            return m.group(1)
        # Ruta absoluta Linux/Mac: /...
        m = re.search(r'(/[^\s]+\.py)', msg)
        if m:
            return m.group(1)
        # Nombre simple
        m = re.search(r'(\w+\.py)', msg, re.IGNORECASE)
        return m.group(1) if m else ""

    # ------------------------------------------------------------------
    # Ejecución
    # ------------------------------------------------------------------

    def ejecutar(self, match: HabilidadMatch, nombre_usuario: str = "") -> ResultadoHabilidad:
        op = match.parametros.get("operacion", "")
        try:
            if op == "analizar_bell":
                return self._op_analizar_bell()
            elif op == "analizar_modulo":
                return self._op_analizar_modulo(
                    match.parametros.get("modulo", ""),
                    match.parametros.get("archivo_rel", ""),
                    match.parametros.get("mensaje", ""),
                )
            elif op == "analizar_archivo":
                return self._op_analizar_archivo(
                    match.parametros.get("archivo", ""),
                )
            elif op == "analizar_inline":
                return self._op_analizar_inline(
                    match.parametros.get("mensaje", ""),
                )
            elif op == "metricas_generales":
                return self._op_metricas_generales()
            else:
                return ResultadoHabilidad(
                    exitoso=False, valor="", descripcion="",
                    error=f"Operación '{op}' no reconocida.",
                    tipo_habilidad="ANALISIS_PYTHON",
                )
        except Exception as e:
            logger.error(f"HabilidadAnalisisPython.ejecutar error: {e}")
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error=f"Error en análisis: {e}",
                tipo_habilidad="ANALISIS_PYTHON",
            )

    # ------------------------------------------------------------------
    # Operaciones
    # ------------------------------------------------------------------

    def _op_analizar_bell(self) -> ResultadoHabilidad:
        raiz     = self._directorio_bell()
        archivos = self._listar_archivos_bell(raiz, limite=20)
        if not archivos:
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error="No encontré los archivos de Bell. ¿Estás en el directorio correcto?",
                tipo_habilidad="ANALISIS_PYTHON",
            )

        analizador = self._obtener_analizador()
        resultados, errores = [], []

        for ruta in archivos:
            try:
                codigo = ruta.read_text(encoding='utf-8', errors='replace')
                r = analizador.analizar_codigo(codigo, ruta.name)
                if r.exitoso:
                    resultados.append((ruta.name, r))
                else:
                    errores.append(f"{ruta.name}: {r.error_parse}")
            except Exception as e:
                errores.append(f"{ruta.name}: {e}")

        if not resultados:
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error=f"No pude analizar ningún archivo. {'; '.join(errores[:3])}",
                tipo_habilidad="ANALISIS_PYTHON",
            )

        return ResultadoHabilidad(
            exitoso=True,
            valor=self._reporte_bell_completo(resultados, errores),
            descripcion="Análisis completo de Bell",
            pasos=[f"Analicé {len(resultados)} archivos"],
            tipo_habilidad="ANALISIS_PYTHON",
            aprobado_vega=True,
        )

    def _op_analizar_modulo(self, nombre_mod: str, archivo_rel: str,
                             mensaje: str) -> ResultadoHabilidad:
        if not archivo_rel:
            nombre_mod  = self._extraer_nombre_modulo(mensaje.lower())
            archivo_rel = _MODULOS_BELL.get(nombre_mod, "")
        if not archivo_rel:
            mods = ", ".join(sorted(_MODULOS_BELL.keys())[:15])
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error=f"No reconocí el módulo '{nombre_mod}'. Módulos disponibles: {mods}.",
                tipo_habilidad="ANALISIS_PYTHON",
            )
        raiz = self._directorio_bell()
        ruta = raiz / archivo_rel
        if not ruta.exists():
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error=f"No encontré '{archivo_rel}' en el proyecto.",
                tipo_habilidad="ANALISIS_PYTHON",
            )
        return self._analizar_ruta(ruta)

    def _op_analizar_archivo(self, nombre_archivo: str) -> ResultadoHabilidad:
        """
        FIX-A3: Acepta rutas absolutas (Windows y Linux) además de nombres simples.
        Orden de búsqueda:
          1. Ruta absoluta que existe en disco → leer directamente
          2. Nombre simple → buscar en el proyecto Bell con rglob
          3. Sin extensión → intentar como módulo Bell conocido
        """
        if not nombre_archivo:
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error=(
                    "No identifiqué qué archivo analizar. "
                    "Ejemplo: 'analiza motor_razonamiento.py' "
                    "o 'analiza C:\\ruta\\mi_archivo.py'"
                ),
                tipo_habilidad="ANALISIS_PYTHON",
            )

        # ── 1. Ruta absoluta ─────────────────────────────────────────
        ruta_abs = Path(nombre_archivo)
        if ruta_abs.is_absolute() and ruta_abs.exists():
            return self._analizar_ruta(ruta_abs)

        raiz = self._directorio_bell()

        # ── 2. Nombre simple → buscar en proyecto ────────────────────
        ruta = self._buscar_archivo(nombre_archivo, raiz)

        # ── 3. Sin .py → intentar como módulo Bell ───────────────────
        if ruta is None:
            sin_ext = nombre_archivo.replace('.py', '').lower()
            rel = _MODULOS_BELL.get(sin_ext, "")
            if rel:
                ruta = raiz / rel

        if ruta is None or not ruta.exists():
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error=(
                    f"No encontré '{nombre_archivo}'. "
                    "Si es una ruta externa usa la ruta completa: "
                    "'analiza C:\\mis_scripts\\archivo.py'"
                ),
                tipo_habilidad="ANALISIS_PYTHON",
            )
        return self._analizar_ruta(ruta)

    def _op_analizar_inline(self, mensaje: str) -> ResultadoHabilidad:
        codigo = self._extraer_codigo_inline(mensaje)
        if not codigo:
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error=(
                    "No encontré código Python en el mensaje. "
                    "Para analizar código externo usa la ruta del archivo:\n"
                    "  'analiza C:\\ruta\\mi_archivo.py'\n"
                    "Para código inline incluye triple-backtick:\n"
                    "  ```python\n  # tu código\n  ```"
                ),
                tipo_habilidad="ANALISIS_PYTHON",
            )
        r = self._obtener_analizador().analizar_codigo(codigo, "código inline")
        return ResultadoHabilidad(
            exitoso=r.exitoso,
            valor=self._reporte_detallado(r, "código inline"),
            descripcion="Análisis de código inline",
            pasos=["Código extraído del mensaje", "Análisis AST completado"],
            tipo_habilidad="ANALISIS_PYTHON",
            aprobado_vega=True,
            error=r.error_parse if not r.exitoso else None,
        )

    def _op_metricas_generales(self) -> ResultadoHabilidad:
        raiz     = self._directorio_bell()
        archivos = self._listar_archivos_bell(raiz, limite=30)
        if not archivos:
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error="No encontré los archivos de Bell.",
                tipo_habilidad="ANALISIS_PYTHON",
            )
        analizador = self._obtener_analizador()
        total_loc = total_fn = total_cls = total_comp = n = 0
        scores = []
        procesados = []
        for ruta in archivos:
            try:
                codigo = ruta.read_text(encoding='utf-8', errors='replace')
                r = analizador.analizar_codigo(codigo, ruta.name)
                if r.exitoso:
                    total_loc  += r.metricas.lineas_total
                    total_fn   += r.metricas.num_funciones
                    total_cls  += r.metricas.num_clases
                    total_comp += r.metricas.complejidad_total
                    scores.append(r.score_calidad)
                    n += 1
                    procesados.append(ruta.name)
            except Exception:
                pass

        score_prom = sum(scores) / len(scores) if scores else 0
        comp_prom  = total_comp / total_fn if total_fn else 0

        lineas = [
            f"📊 Métricas generales de Bell ({n} archivos):",
            f"  {'─'*40}",
            f"  Líneas totales:          {total_loc:,}",
            f"  Funciones/métodos:       {total_fn}",
            f"  Clases:                  {total_cls}",
            f"  Complejidad total:       {total_comp}",
            f"  Complejidad prom/fn:     {comp_prom:.1f}",
            f"  Score calidad prom:      {score_prom:.0f}/100",
            f"  {'─'*40}",
            f"  Archivos analizados:",
        ]
        for nombre in procesados[:15]:
            lineas.append(f"    • {nombre}")
        if len(procesados) > 15:
            lineas.append(f"    ... y {len(procesados)-15} más")

        return ResultadoHabilidad(
            exitoso=True,
            valor="\n".join(lineas),
            descripcion="Métricas generales de Bell",
            pasos=[f"Escaneé {n} archivos"],
            tipo_habilidad="ANALISIS_PYTHON",
            aprobado_vega=True,
        )

    # ------------------------------------------------------------------
    # Helpers de archivos
    # ------------------------------------------------------------------

    def _analizar_ruta(self, ruta: Path) -> ResultadoHabilidad:
        try:
            codigo = ruta.read_text(encoding='utf-8', errors='replace')
        except Exception as e:
            return ResultadoHabilidad(
                exitoso=False, valor="", descripcion="",
                error=f"No pude leer '{ruta.name}': {e}",
                tipo_habilidad="ANALISIS_PYTHON",
            )
        r = self._obtener_analizador().analizar_codigo(codigo, ruta.name)
        return ResultadoHabilidad(
            exitoso=r.exitoso,
            valor=self._reporte_detallado(r, str(ruta)),
            descripcion=f"Análisis de {ruta.name}",
            pasos=[f"Analicé {r.metricas.lineas_total} líneas de {ruta.name}"],
            tipo_habilidad="ANALISIS_PYTHON",
            aprobado_vega=True,
            error=r.error_parse if not r.exitoso else None,
        )

    def _directorio_bell(self) -> Path:
        candidato = Path(__file__).parent.parent
        if (candidato / 'main.py').exists():
            return candidato
        cwd = Path.cwd()
        if (cwd / 'main.py').exists():
            return cwd
        for padre in cwd.parents:
            if (padre / 'main.py').exists() and (padre / 'habilidades').exists():
                return padre
        return cwd

    def _listar_archivos_bell(self, raiz: Path, limite: int = 20) -> List[Path]:
        archivos = []
        clave_orden = [
            'main.py',
            'razonamiento/motor_razonamiento.py',
            'razonamiento/tipos_decision.py',
            'razonamiento/patrones_habilidades.py',
            'generacion/generador_salida.py',
            'generacion/generador_ejecutores.py',
            'habilidades/registro_habilidades.py',
            'habilidades/shell_habilidad.py',
            'habilidades/sqlite_habilidad.py',
            'habilidades/analizador_habilidad.py',
            'core/capacidades_fase.py',
            'consejeras/vega/logica.py',
            'consejeras/nova/logica.py',
            'consejeras/echo/logica.py',
        ]
        for rel in clave_orden:
            p = raiz / rel
            if p.exists():
                archivos.append(p)
            if len(archivos) >= limite:
                return archivos
        try:
            for p in raiz.rglob('*.py'):
                if p in archivos:
                    continue
                if any(ex in p.parts for ex in _EXCLUIR):
                    continue
                if any(p.name.startswith(ex) for ex in _EXCLUIR_NOMBRES):
                    continue
                archivos.append(p)
                if len(archivos) >= limite:
                    break
        except Exception:
            pass
        return archivos

    def _buscar_archivo(self, nombre: str, raiz: Path) -> Optional[Path]:
        try:
            for p in raiz.rglob('*.py'):
                if any(ex in p.parts for ex in _EXCLUIR):
                    continue
                if p.name.lower() == nombre.lower():
                    return p
        except Exception:
            pass
        return None

    def _extraer_codigo_inline(self, mensaje: str) -> str:
        m = re.search(r'```(?:python|py)?\s*\n(.*?)```', mensaje, re.DOTALL | re.IGNORECASE)
        if m:
            return m.group(1).strip()
        m = re.search(r'```(.*?)```', mensaje, re.DOTALL)
        if m:
            contenido = m.group(1).strip()
            if '\n' in contenido:
                return contenido
        return ""

    # ------------------------------------------------------------------
    # Generadores de reportes — idénticos a v1.0
    # ------------------------------------------------------------------

    @staticmethod
    def _emoji_score(score: int) -> str:
        if score >= 85: return "✅"
        if score >= 70: return "🟡"
        if score >= 50: return "🟠"
        return "🔴"

    def _reporte_detallado(self, r: ResultadoAnalisis, ruta: str) -> str:
        if not r.exitoso:
            return f"❌ No pude analizar '{r.archivo}': {r.error_parse}"

        m = r.metricas
        lineas = [
            f"📋 Análisis: {r.archivo}",
            f"  Score de calidad:  {r.score_calidad}/100  {self._emoji_score(r.score_calidad)}",
            f"  {'─'*44}",
            f"  📏 Líneas:",
            f"     Total:           {m.lineas_total}",
            f"     Código:          {m.lineas_codigo}",
            f"     Comentarios:     {m.lineas_comentario}",
            f"     Docstrings:      {m.lineas_docstring}",
            f"     Vacías:          {m.lineas_vacias}",
            f"     Ratio docs:      {m.ratio_comentarios:.0%}",
            f"  {'─'*44}",
            f"  🧩 Estructura:",
            f"     Funciones:       {m.num_funciones}",
            f"     Clases:          {m.num_clases}",
            f"     Imports:         {m.num_imports}",
            f"     Type hints:      {'sí ✅' if m.tiene_type_hints else 'no'}",
        ]

        if m.num_funciones > 0:
            lineas += [
                f"  {'─'*44}",
                f"  🔀 Complejidad McCabe:",
                f"     Promedio:        {m.complejidad_prom:.1f}",
                f"     Máxima:          {m.complejidad_max}  ('{m.funcion_max_comp}')",
                f"     Total:           {m.complejidad_total}",
            ]

        if r.funciones:
            top = sorted(r.funciones, key=lambda f: f.complejidad, reverse=True)[:5]
            lineas += [f"  {'─'*44}", "  📊 Top funciones (por complejidad):"]
            for fn in top:
                d = "📝" if fn.tiene_doc   else "  "
                h = "🔖" if fn.tiene_hints else "  "
                lineas.append(
                    f"     {d}{h} {fn.nombre:<32} "
                    f"comp={fn.complejidad}  args={fn.num_args}  líneas={fn.lineas}"
                )

        if r.clases:
            lineas += [f"  {'─'*44}", f"  🏗 Clases ({len(r.clases)}):"]
            for cls in r.clases[:5]:
                d = "📝" if cls.tiene_doc else "  "
                h = f" ← {', '.join(cls.hereda_de)}" if cls.hereda_de else ""
                lineas.append(
                    f"     {d} {cls.nombre:<34} {cls.num_metodos} métodos{h}"
                )

        if r.problemas:
            errores      = [p for p in r.problemas if p.tipo == "error"]
            advertencias = [p for p in r.problemas if p.tipo == "advertencia"]
            sugerencias  = [p for p in r.problemas if p.tipo == "sugerencia"]
            lineas += [f"  {'─'*44}", f"  ⚠ Problemas ({len(r.problemas)}):"]
            for p in errores[:3]:
                lineas.append(f"     ❌ L{p.linea}: {p.descripcion}")
            for p in advertencias[:3]:
                lineas.append(f"     ⚠️  L{p.linea}: {p.descripcion}")
            for p in sugerencias[:5]:
                lineas.append(f"     💡 L{p.linea}: {p.descripcion}")
            mostrados = min(len(errores),3) + min(len(advertencias),3) + min(len(sugerencias),5)
            resto = len(r.problemas) - mostrados
            if resto > 0:
                lineas.append(f"     ... y {resto} más")

        lineas += [f"  {'─'*44}", "  💡 Nova recomienda:"]
        for rec in r.recomendaciones[:5]:
            lineas.append(f"     • {rec}")

        return "\n".join(lineas)

    def _reporte_bell_completo(self, resultados: List[tuple], errores: List[str]) -> str:
        total_loc  = sum(r.metricas.lineas_total    for _, r in resultados)
        total_fn   = sum(r.metricas.num_funciones   for _, r in resultados)
        total_cls  = sum(r.metricas.num_clases      for _, r in resultados)
        total_comp = sum(r.metricas.complejidad_total for _, r in resultados)
        scores     = [r.score_calidad for _, r in resultados]
        score_prom = sum(scores) / len(scores) if scores else 0
        comp_prom  = total_comp / total_fn if total_fn else 0

        ordenados = sorted(resultados, key=lambda x: x[1].score_calidad)

        lineas = [
            f"🔬 Análisis completo de Bell ({len(resultados)} módulos)",
            f"  {'─'*44}",
            f"  📊 Resumen del sistema:",
            f"     Líneas totales:       {total_loc:,}",
            f"     Funciones/métodos:    {total_fn}",
            f"     Clases:               {total_cls}",
            f"     Complejidad total:    {total_comp}",
            f"     Complejidad prom/fn:  {comp_prom:.1f}",
            f"     Score calidad prom:   {score_prom:.0f}/100  {self._emoji_score(int(score_prom))}",
            f"  {'─'*44}",
            f"  📋 Por módulo (score / líneas / funciones):",
        ]
        for nombre, r in sorted(resultados, key=lambda x: x[1].score_calidad, reverse=True):
            m = r.metricas
            lineas.append(
                f"     {self._emoji_score(r.score_calidad)} {nombre:<40} "
                f"score={r.score_calidad:3}  "
                f"LOC={m.lineas_total:4}  "
                f"fn={m.num_funciones:3}  "
                f"cls={m.num_clases}"
            )

        necesitan_atencion = [
            (n, r) for n, r in ordenados if r.score_calidad < 70
        ]
        if necesitan_atencion:
            lineas += [f"  {'─'*44}", "  🔴 Módulos que necesitan atención:"]
            for nombre, r in necesitan_atencion[:5]:
                primer_problema = r.problemas[0].descripcion if r.problemas else "ver reporte"
                lineas.append(f"     • {nombre}: score {r.score_calidad} — {primer_problema}")

        if errores:
            lineas += [f"  {'─'*44}", f"  ⚠ No se pudieron analizar ({len(errores)}):"]
            for e in errores[:3]:
                lineas.append(f"     • {e}")

        todos_problemas = [p for _, r in resultados for p in r.problemas]
        sin_doc = sum(1 for p in todos_problemas if 'sin docstring' in p.descripcion)
        alta    = sum(1 for p in todos_problemas if 'alta' in p.descripcion)
        lineas += [f"  {'─'*44}", "  💡 Nova recomienda (sistema):"]
        if sin_doc:
            lineas.append(f"     • {sin_doc} funciones/clases sin docstring en todo el sistema.")
        if alta:
            lineas.append(f"     • {alta} funciones con complejidad alta — revisar para refactorizar.")
        if score_prom >= 80:
            lineas.append("     • ✅ Bell tiene una base de código sólida. Mantener el estándar.")
        elif score_prom >= 60:
            lineas.append("     • Calidad buena pero con margen de mejora en documentación y complejidad.")
        else:
            lineas.append("     • Se recomienda una sesión de refactorización sistemática.")

        return "\n".join(lineas)

    # ------------------------------------------------------------------
    # Formateo de respuesta
    # ------------------------------------------------------------------

    def formatear_respuesta(self, resultado: ResultadoHabilidad, nombre_usuario: str = "") -> str:
        n = f", {nombre_usuario}" if nombre_usuario else ""
        if resultado.exitoso:
            return f"{resultado.valor}{n}."
        else:
            error = resultado.error or "Error desconocido en el análisis."
            return f"No pude completar el análisis{n}: {error}"