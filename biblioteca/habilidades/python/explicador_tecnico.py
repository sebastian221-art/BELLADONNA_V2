# biblioteca/habilidades/python/explicador_tecnico.py
# ============================================================
# EXPLICADOR TÉCNICO — métricas reales + voz Bell
#
# Nunca inventa. Cada afirmación viene de datos calculados.
# Explica en español claro como si hablaras con un developer,
# no como si leyeras documentación.
# ============================================================

from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from biblioteca.habilidades.python.analizador_codigo import AnalisisCompleto


@dataclass
class Explicacion:
    texto_completo:   str
    puntos_clave:     list
    sugerencias:      list
    nivel_confianza:  str  # 'datos_reales' siempre


class ExplicadorTecnico:

    def explicar_analisis(self, analisis: 'AnalisisCompleto') -> Explicacion:
        """Convierte un AnalisisCompleto en explicación humana con voz Bell."""
        puntos = []
        sugerencias = []

        # ── Complejidad ────────────────────────────────────────────────────
        cc = analisis.metricas.cc
        if cc <= 5:
            puntos.append(
                f"Complejidad ciclomática CC={cc} — código muy simple, "
                f"fácil de testear y mantener. Cada función tiene pocos caminos posibles."
            )
        elif cc <= 10:
            puntos.append(
                f"Complejidad CC={cc} — dentro del rango profesional aceptable. "
                f"Puede tener hasta {int(cc)} caminos de ejecución distintos."
            )
        elif cc <= 15:
            puntos.append(
                f"Complejidad CC={cc} — elevada. Con más de 10 caminos de ejecución "
                f"el riesgo de bugs no probados aumenta significativamente."
            )
            sugerencias.append(
                f"Refactoriza las funciones con CC>{int(cc/2)} — extrae lógica en funciones más pequeñas."
            )
        else:
            puntos.append(
                f"Complejidad CC={cc} — crítica. Esto significa {int(cc)} rutas posibles "
                f"de ejecución. La probabilidad de bugs no detectados es muy alta."
            )
            sugerencias.append("Urgente: divide las funciones complejas — ninguna debería superar CC=10.")

        # ── Mantenibilidad ─────────────────────────────────────────────────
        mi = analisis.metricas.mi
        if mi >= 65:
            puntos.append(
                f"Índice de mantenibilidad MI={mi}/100 — código saludable. "
                f"Otro developer (o tú en 6 meses) lo va a entender sin problema."
            )
        elif mi >= 30:
            puntos.append(
                f"Mantenibilidad MI={mi}/100 — aceptable pero con margen de mejora. "
                f"El código funciona pero puede ser difícil de modificar."
            )
            sugerencias.append("Agrega docstrings y comentarios en las partes más densas.")
        else:
            puntos.append(
                f"Mantenibilidad MI={mi}/100 — código difícil de mantener. "
                f"Cada cambio tiene riesgo alto de romper algo inesperado."
            )
            sugerencias.append("Refactorización profunda necesaria antes de agregar más features.")

        # ── Tamaño ─────────────────────────────────────────────────────────
        loc = analisis.metricas.loc
        if loc > 0:
            puntos.append(f"Tamaño: {loc} líneas totales, {analisis.metricas.lloc} líneas lógicas.")

        # ── Funciones ──────────────────────────────────────────────────────
        if analisis.funciones:
            sin_doc = [f['nombre'] for f in analisis.funciones if not f.get('doc')]
            sin_types = [f['nombre'] for f in analisis.funciones if not f.get('returns') and f.get('args')]
            if sin_doc:
                sugerencias.append(f"Funciones sin docstring: {', '.join(sin_doc[:5])}.")
            if sin_types:
                sugerencias.append(f"Funciones sin type hints de retorno: {', '.join(sin_types[:5])}.")

        # ── Problemas específicos ──────────────────────────────────────────
        errores = [p for p in analisis.problemas if p.tipo == 'error']
        seguridad = [p for p in analisis.problemas if p.herramienta == 'bandit']

        if errores:
            for e in errores[:3]:
                puntos.append(f"Error línea {e.linea}: {e.mensaje}")

        if seguridad:
            for s in seguridad[:2]:
                puntos.append(f"⚠️  Seguridad línea {s.linea}: {s.mensaje}")
            sugerencias.append("Los problemas de seguridad deben corregirse antes de cualquier deploy.")

        # ── Texto completo ─────────────────────────────────────────────────
        texto = self._armar_texto(analisis, puntos, sugerencias)

        return Explicacion(
            texto_completo=texto,
            puntos_clave=puntos,
            sugerencias=sugerencias,
            nivel_confianza='datos_reales',
        )

    def explicar_error(self, error: str, codigo: str = '') -> str:
        """Explica un error de Python en lenguaje humano."""
        error_lower = error.lower()

        if 'nameerror' in error_lower:
            nombre = self._extraer_nombre_error(error)
            return (
                f"NameError: '{nombre}' no existe en este contexto. "
                f"Puede ser que no la definiste antes de usarla, o hay un typo en el nombre."
            )
        if 'typeerror' in error_lower:
            return (
                f"TypeError: estás pasando el tipo de dato incorrecto a alguna función. "
                f"Detalle: {error.split('TypeError:')[-1].strip()}"
            )
        if 'indexerror' in error_lower:
            return (
                "IndexError: intentas acceder a una posición que no existe en la lista. "
                "Verifica que el índice esté dentro del rango de la lista."
            )
        if 'keyerror' in error_lower:
            nombre = self._extraer_nombre_error(error)
            return (
                f"KeyError: la clave '{nombre}' no existe en el diccionario. "
                f"Usa dict.get('{nombre}') para evitar el error, o verifica que la clave exista."
            )
        if 'importerror' in error_lower or 'modulenotfounderror' in error_lower:
            return (
                f"ImportError: el módulo no está instalado o no se encuentra. "
                f"Detalle: {error.split(':')[-1].strip()}"
            )
        if 'syntaxerror' in error_lower:
            return (
                f"SyntaxError: el código tiene un error de escritura — Python no puede leerlo. "
                f"Detalle: {error.split('SyntaxError:')[-1].strip()}"
            )
        if 'attributeerror' in error_lower:
            return (
                f"AttributeError: estás accediendo a un atributo o método que no existe. "
                f"Detalle: {error.split('AttributeError:')[-1].strip()}"
            )
        if 'valueerror' in error_lower:
            return (
                f"ValueError: el valor que pasas es del tipo correcto pero el contenido "
                f"no es válido para esa operación. "
                f"Detalle: {error.split('ValueError:')[-1].strip()}"
            )

        return f"Error detectado: {error.strip()[:300]}"

    def _armar_texto(self, analisis, puntos: list, sugerencias: list) -> str:
        partes = []

        riesgo_emoji = {
            'bajo': '✅', 'medio': '⚠️', 'alto': '🔴', 'crítico': '🚨'
        }.get(analisis.metricas.nivel_riesgo, '')

        partes.append(
            f"{riesgo_emoji} Análisis completo — riesgo {analisis.metricas.nivel_riesgo.upper()}."
        )
        partes.append('')

        for p in puntos:
            partes.append(f"• {p}")

        if sugerencias:
            partes.append('')
            partes.append("Sugerencias de mejora:")
            for s in sugerencias:
                partes.append(f"  → {s}")

        return '\n'.join(partes)

    def _extraer_nombre_error(self, error: str) -> str:
        match = __import__('re').search(r"'([^']+)'", error)
        return match.group(1) if match else 'desconocido'


_instancia: Optional[ExplicadorTecnico] = None

def obtener() -> ExplicadorTecnico:
    global _instancia
    if _instancia is None:
        _instancia = ExplicadorTecnico()
    return _instancia