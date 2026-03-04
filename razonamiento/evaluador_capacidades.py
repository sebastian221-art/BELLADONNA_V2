"""
Evaluador de Capacidades - ¿Bell PUEDE hacer algo?

Este módulo determina si Bell tiene la capacidad REAL de hacer algo
basándose en el grounding de conceptos.

CAMBIOS v6 (diagnóstico 02/03/2026):
═══════════════════════════════════════════════════════════════════════

FIX A-05 — CRASH list.keys() (línea 68 original)
─────────────────────────────────────────────────
  Problema: operacion = list(concepto_principal.operaciones.keys())[0]
  lanza AttributeError si operaciones es una lista en vez de dict.
  Evidencia: "puedes calcular la raíz cuadrada de 256 y decirme
  quién eres" → ERROR en evaluador.

  Solución: _extraer_primera_operacion() maneja tanto dict como list
  con isinstance(), nunca lanza AttributeError.

FIX C-01 — AFIRMATIVA VERIFICA WHITELIST (honestidad radical)
──────────────────────────────────────────────────────────────
  Problema: evaluar_capacidad_accion() retornaba puede_ejecutar=True
  para cualquier concepto con grounding >= 0.9 y operaciones.
  Bell respondía "sí puedo crear archivos" aunque no pueda.

  Solución: verificar_contra_whitelist() carga BELL_WHITELIST.json
  y revisa si la operación está realmente permitida.
  Si no está en whitelist → puede_ejecutar=False + razón honesta.
  Si whitelist no disponible → advertencia en razon, no bloquea.

  Principio: solo afirmo lo que puedo ejecutar o verificar.

FIX Fase 4A — CAPACIDADES NO IMPLEMENTADAS
───────────────────────────────────────────
  Problema: conceptos como CONCEPTO_TOUCH tienen grounding 1.0
  (el comando existe en OS) pero Bell no tiene la funcionalidad
  implementada para el usuario. El evaluador retornaba puede_ejecutar=True.

  Solución: verificar_contra_whitelist() consulta la sección
  capacidades_fase4a.no_implementadas del JSON antes de evaluar
  la whitelist de seguridad. Separación clara entre:
    - grounding = "el concepto existe y es real"
    - implementado = "Bell puede ejecutarlo para el usuario ahora"
═══════════════════════════════════════════════════════════════════════
"""
import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from core.concepto_anclado import ConceptoAnclado


# ── Ruta a la whitelist ───────────────────────────────────────────────────
_WHITELIST_PATH = Path(__file__).parent.parent / "BELL_WHITELIST.json"

# Cache de whitelist cargada (None = no intentado, False = falló)
_whitelist_cache = None


def _cargar_whitelist() -> Optional[dict]:
    """
    Carga BELL_WHITELIST.json con cache.
    Retorna el dict si existe, None si no está disponible.
    """
    global _whitelist_cache
    if _whitelist_cache is not None:
        return _whitelist_cache if _whitelist_cache is not False else None

    try:
        with open(_WHITELIST_PATH, encoding="utf-8") as f:
            _whitelist_cache = json.load(f)
        return _whitelist_cache
    except (FileNotFoundError, json.JSONDecodeError):
        _whitelist_cache = False
        return None


class EvaluadorCapacidades:
    """
    Evalúa si Bell puede ejecutar una acción basándose en conceptos.

    NO es magia. Es evaluación lógica de grounding + whitelist.
    Principio: mejor rechazar honestamente que afirmar sin grounding.
    """

    UMBRAL_GROUNDING_ALTO = 0.9
    UMBRAL_GROUNDING_MEDIO = 0.7
    UMBRAL_GROUNDING_BAJO = 0.5

    def __init__(self):
        pass

    # ── FIX A-05: extractor seguro de primera operación ──────────────────

    def _extraer_primera_operacion(self, concepto: ConceptoAnclado) -> Optional[str]:
        """
        FIX A-05: extrae el nombre de la primera operación del concepto
        sin importar si operaciones es dict o list.
        """
        ops = concepto.operaciones
        if not ops:
            return None
        try:
            if isinstance(ops, dict):
                return next(iter(ops))
            elif isinstance(ops, (list, tuple)):
                item = ops[0]
                if isinstance(item, dict):
                    return next(iter(item))
                return str(item)
            else:
                return str(ops)
        except (StopIteration, IndexError, TypeError):
            return None

    # ── FIX C-01 + FIX Fase 4A: verificación contra whitelist ────────────

    def verificar_contra_whitelist(
        self,
        concepto: ConceptoAnclado,
        operacion: Optional[str]
    ) -> Tuple[bool, str]:
        """
        Verifica que la operación esté permitida en BELL_WHITELIST.json.

        Retorna (permitido: bool, razon: str).

        Orden de verificación:
          1. Si whitelist no disponible → permitido=True con advertencia
          2. Si concepto en capacidades_fase4a.no_implementadas → False
          3. Si operacion es None → False
          4. Verificar según tipo de concepto en whitelist de seguridad
        """
        whitelist = _cargar_whitelist()

        if whitelist is None:
            return (
                True,
                "Whitelist no disponible — asumiendo permitido (verificar BELL_WHITELIST.json)"
            )

        # FIX Fase 4A: separar "comando existe en OS" de "Bell puede ejecutarlo"
        no_implementadas = whitelist.get("capacidades_fase4a", {}).get("no_implementadas", [])
        if concepto.id in no_implementadas:
            return (
                False,
                f"'{concepto.id}' tiene grounding real pero no está implementado en Fase 4A"
            )

        if operacion is None:
            return (False, "No hay operación definida para ejecutar")

        tipo_concepto = concepto.tipo.name if hasattr(concepto.tipo, 'name') else str(concepto.tipo)

        try:
            if tipo_concepto == "OPERACION_SISTEMA":
                comandos_ok = whitelist.get("operaciones_sistema", {}) \
                                       .get("shell", {}) \
                                       .get("comandos_permitidos", [])
                nombre_cmd = operacion.lower().replace("ejecutar_", "").replace("_cmd", "")
                concepto_cmd = concepto.id.replace("CONCEPTO_", "").lower()
                if nombre_cmd in comandos_ok or concepto_cmd in comandos_ok:
                    return (True, f"Comando '{nombre_cmd}' en whitelist")
                for palabra in concepto.palabras_español:
                    if palabra.lower() in comandos_ok:
                        return (True, f"Comando '{palabra}' en whitelist")
                return (
                    False,
                    f"Comando '{nombre_cmd}' no está en la lista de comandos permitidos"
                )

            elif tipo_concepto in ("OPERACION_PYTHON", "CALCULO"):
                python_ops = whitelist.get("operaciones_python", {})
                if operacion == "calcular" or "calcul" in operacion:
                    calc = python_ops.get("calcular", {})
                    if calc.get("permitido", False):
                        return (True, "Cálculo matemático permitido (grounding 1.0)")
                    return (False, "Cálculo no permitido según whitelist")
                exec_cfg = python_ops.get("ejecutar_codigo", {})
                if exec_cfg.get("permitido", False):
                    return (True, "Ejecución Python permitida")
                return (False, "Ejecución de código no permitida")

            elif tipo_concepto in ("SOCIAL", "PALABRA_CONVERSACION", "CONCEPTO_ABSTRACTO"):
                conv_ops = whitelist.get("operaciones_conversacion", {})
                nombre_op = operacion.lower()
                if nombre_op in conv_ops:
                    if conv_ops[nombre_op].get("permitido", False):
                        return (True, f"Operación conversacional '{nombre_op}' permitida")
                    return (False, f"Operación '{nombre_op}' no permitida")
                return (True, "Operación conversacional permitida por defecto")

            else:
                return (
                    True,
                    f"Tipo '{tipo_concepto}' no verificado en whitelist — permitido por defecto"
                )

        except (KeyError, AttributeError, TypeError) as e:
            return (
                True,
                f"Error leyendo whitelist ({e}) — permitido por precaución"
            )

    # ── Evaluación principal ──────────────────────────────────────────────

    def evaluar_capacidad_accion(
        self,
        conceptos: List[ConceptoAnclado]
    ) -> Dict:
        """
        Evalúa si Bell puede realizar una acción basándose en conceptos.

        v6: aplica verificación de whitelist (FIX C-01) y extracción
        segura de operación (FIX A-05).

        Returns:
            {
                'puede_ejecutar': bool,
                'confianza': float,
                'operacion': str or None,
                'concepto_clave': ConceptoAnclado or None,
                'razon': str,
                'groundings': List[float],
                'whitelist_ok': bool,
                'razon_whitelist': str,
            }
        """
        if not conceptos:
            return {
                'puede_ejecutar': False,
                'confianza': 0.0,
                'operacion': None,
                'concepto_clave': None,
                'razon': 'No hay conceptos para evaluar',
                'groundings': [],
                'whitelist_ok': False,
                'razon_whitelist': 'Sin conceptos',
            }

        concepto_principal = max(conceptos, key=lambda c: c.confianza_grounding)
        groundings = [c.confianza_grounding for c in conceptos]
        tiene_operaciones = bool(concepto_principal.operaciones)

        # FIX A-05: extracción segura de operación
        operacion = self._extraer_primera_operacion(concepto_principal)

        if concepto_principal.confianza_grounding >= self.UMBRAL_GROUNDING_ALTO \
                and tiene_operaciones:
            whitelist_ok, razon_whitelist = self.verificar_contra_whitelist(
                concepto_principal, operacion
            )

            if whitelist_ok:
                return {
                    'puede_ejecutar': True,
                    'confianza': concepto_principal.confianza_grounding,
                    'operacion': operacion,
                    'concepto_clave': concepto_principal,
                    'razon': f'Grounding alto ({concepto_principal.confianza_grounding}) + whitelist ok',
                    'groundings': groundings,
                    'whitelist_ok': True,
                    'razon_whitelist': razon_whitelist,
                }
            else:
                return {
                    'puede_ejecutar': False,
                    'confianza': concepto_principal.confianza_grounding,
                    'operacion': None,
                    'concepto_clave': concepto_principal,
                    'razon': f'Operación no permitida: {razon_whitelist}',
                    'groundings': groundings,
                    'whitelist_ok': False,
                    'razon_whitelist': razon_whitelist,
                }

        elif concepto_principal.confianza_grounding >= self.UMBRAL_GROUNDING_MEDIO \
                and tiene_operaciones:
            whitelist_ok, razon_whitelist = self.verificar_contra_whitelist(
                concepto_principal, operacion
            )

            if whitelist_ok:
                return {
                    'puede_ejecutar': True,
                    'confianza': concepto_principal.confianza_grounding,
                    'operacion': operacion,
                    'concepto_clave': concepto_principal,
                    'razon': f'Grounding medio ({concepto_principal.confianza_grounding}), puede intentar',
                    'groundings': groundings,
                    'whitelist_ok': True,
                    'razon_whitelist': razon_whitelist,
                }
            else:
                return {
                    'puede_ejecutar': False,
                    'confianza': concepto_principal.confianza_grounding,
                    'operacion': None,
                    'concepto_clave': concepto_principal,
                    'razon': f'Operación no permitida: {razon_whitelist}',
                    'groundings': groundings,
                    'whitelist_ok': False,
                    'razon_whitelist': razon_whitelist,
                }

        else:
            if not tiene_operaciones:
                razon = f'Concepto "{concepto_principal.id}" no tiene operaciones ejecutables'
            else:
                razon = f'Grounding muy bajo ({concepto_principal.confianza_grounding})'

            return {
                'puede_ejecutar': False,
                'confianza': concepto_principal.confianza_grounding,
                'operacion': None,
                'concepto_clave': concepto_principal,
                'razon': razon,
                'groundings': groundings,
                'whitelist_ok': False,
                'razon_whitelist': 'Grounding insuficiente',
            }

    def verificar_requisitos(
        self,
        concepto: ConceptoAnclado,
        conceptos_disponibles: List[ConceptoAnclado]
    ) -> Tuple[bool, List[str]]:
        """
        Verifica si están presentes los conceptos requeridos.
        Sin cambios desde v5.
        """
        if 'requiere' not in concepto.relaciones:
            return (True, [])

        requeridos = concepto.relaciones['requiere']
        disponibles_ids = {c.id for c in conceptos_disponibles}
        faltantes = [req for req in requeridos if req not in disponibles_ids]

        return (len(faltantes) == 0, faltantes)

    def calcular_confianza_total(
        self,
        conceptos: List[ConceptoAnclado]
    ) -> float:
        """
        Calcula confianza total de una traducción.
        Penaliza si hay conceptos con grounding bajo.
        Sin cambios desde v5.
        """
        if not conceptos:
            return 0.0

        groundings = [c.confianza_grounding for c in conceptos]
        promedio = sum(groundings) / len(groundings)
        minimo = min(groundings)
        if minimo < 0.3:
            promedio *= 0.7

        return round(promedio, 2)