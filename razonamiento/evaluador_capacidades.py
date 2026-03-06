"""
evaluador_capacidades.py — VERSION v8

FIXES APLICADOS (sobre v7):
═══════════════════════════════════════════════════════════════════════

BUG-EC1  'list' object has no attribute 'keys'
         Causa: evaluar_capacidad_accion() hace:
             ops = getattr(concepto, 'operaciones', None) or {}
             operacion = list(ops.keys())[0] if ops else None
         Si concepto.operaciones es una lista no-vacía (edge case o concepto
         mal definido), 'ops or {}' retorna la lista (truthy), y ops.keys()
         explota con AttributeError.
         También ocurre cuando resultado de una habilidad llega como lista
         en vez de dict a través de algún flujo de datos inesperado.

         Fix: verificación isinstance(ops, dict) antes de cualquier .keys().
         Si ops no es dict → se trata como vacío → operacion = None → NEGATIVA.

COMPATIBILIDAD: 100% con v7. Mismas firmas externas.
═══════════════════════════════════════════════════════════════════════
"""
from typing import List, Tuple, Dict, Optional
from pathlib import Path
import json


class EvaluadorCapacidades:
    """
    Evalúa qué puede y no puede hacer Bell.

    v8: defiende ops.keys() con isinstance(ops, dict).
    v7: usa core/capacidades_fase.py como fuente primaria de verdad.
    """

    def __init__(self, whitelist_path: Optional[Path] = None):
        self._whitelist_path = whitelist_path
        self._whitelist: Optional[Dict] = None
        self._whitelist_cargada = False

        self._no_implementadas_ids = set()
        self._razon_no_implementada = {}
        self._cargar_capacidades_fase()

    def _cargar_capacidades_fase(self):
        try:
            from core.capacidades_fase import NO_IMPLEMENTADAS_IDS, NO_IMPLEMENTADAS
            self._no_implementadas_ids = NO_IMPLEMENTADAS_IDS
            self._razon_no_implementada = {k: v for k, v in NO_IMPLEMENTADAS.items()}
        except ImportError:
            pass

    def _cargar_whitelist(self) -> Optional[Dict]:
        if self._whitelist_cargada:
            return self._whitelist

        self._whitelist_cargada = True

        candidatos = []
        if self._whitelist_path:
            candidatos.append(Path(self._whitelist_path))

        candidatos += [
            Path("data/BELL_WHITELIST.json"),
            Path("BELL_WHITELIST.json"),
            Path("../data/BELL_WHITELIST.json"),
            Path("../BELL_WHITELIST.json"),
        ]

        for path in candidatos:
            if path.exists():
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        self._whitelist = json.load(f)
                    return self._whitelist
                except Exception:
                    continue

        return None

    # ──────────────────────────────────────────────────────────────────────────
    # API PRINCIPAL
    # ──────────────────────────────────────────────────────────────────────────

    def evaluar_capacidad_accion(self, conceptos: list) -> Dict:
        if not conceptos:
            return {
                'puede_ejecutar': False,
                'confianza': 0.0,
                'concepto_clave': None,
                'operacion': None,
                'razon': 'Sin conceptos para evaluar',
            }

        concepto_clave = None
        max_grounding = 0.0

        for concepto in conceptos:
            ops_raw = getattr(concepto, 'operaciones', None)
            # BUG-EC1 FIX: solo considerar operaciones si es un dict no vacío
            ops = ops_raw if isinstance(ops_raw, dict) and ops_raw else {}
            if ops and concepto.confianza_grounding > max_grounding:
                concepto_clave = concepto
                max_grounding = concepto.confianza_grounding

        if concepto_clave is None:
            return {
                'puede_ejecutar': False,
                'confianza': 0.0,
                'concepto_clave': None,
                'operacion': None,
                'razon': 'Ningún concepto tiene operaciones definidas',
            }

        puede, razon = self.verificar_contra_whitelist(concepto_clave)

        # BUG-EC1 FIX: proteger .keys() con isinstance
        ops_raw = getattr(concepto_clave, 'operaciones', {})
        ops = ops_raw if isinstance(ops_raw, dict) else {}
        if 'ejecutar' in ops:
            operacion = 'ejecutar'
        elif ops:
            operacion = list(ops.keys())[0]
        else:
            operacion = None

        return {
            'puede_ejecutar': puede,
            'confianza': concepto_clave.confianza_grounding if puede else 0.0,
            'concepto_clave': concepto_clave,
            'operacion': operacion if puede else None,
            'razon': razon,
        }

    def verificar_contra_whitelist(self, concepto) -> Tuple[bool, str]:
        concepto_id = concepto.id if hasattr(concepto, 'id') else str(concepto)

        # ── 1. Fuente única: capacidades_fase.py ─────────────────────────────
        if self._no_implementadas_ids:
            if concepto_id in self._no_implementadas_ids:
                razon = self._razon_no_implementada.get(
                    concepto_id,
                    f"{concepto_id} no implementado en Fase 4A"
                )
                return (False, razon)

        # ── 2. Whitelist JSON ─────────────────────────────────────────────────
        whitelist = self._cargar_whitelist()

        if whitelist is None:
            return (False, "Whitelist no disponible — asumiendo no permitido por seguridad")

        no_impl = (whitelist
                   .get('capacidades_fase4a', {})
                   .get('no_implementadas', []))
        if concepto_id in no_impl:
            return (False, f"{concepto_id} no implementado según whitelist (Fase 4A)")

        # ── 3. Verificar por tipo ─────────────────────────────────────────────
        tipo = getattr(concepto, 'tipo', None)
        tipo_nombre = tipo.name if hasattr(tipo, 'name') else str(tipo)

        if tipo_nombre == 'OPERACION_SISTEMA':
            return self._verificar_operacion_sistema(concepto_id, whitelist)

        elif tipo_nombre == 'ENTIDAD_DIGITAL':
            return (True, f"{concepto_id} es entidad digital — consulta permitida")

        elif tipo_nombre in ('CONCEPTO_MENTAL', 'ESTADO_EMOCIONAL', 'ACCION_COGNITIVA'):
            return (True, f"{concepto_id} es concepto cognitivo — disponible")

        # ── 4. Fallback conservador ───────────────────────────────────────────
        # BUG-EC1 FIX: proteger ops con isinstance
        ops_raw = getattr(concepto, 'operaciones', None)
        ops = ops_raw if isinstance(ops_raw, dict) else {}
        if ops and concepto.confianza_grounding >= 0.9:
            return (True, f"{concepto_id} verificado — operaciones disponibles con grounding alto")

        return (False, f"{concepto_id} no verificado en whitelist — asumiendo no permitido")

    def _verificar_operacion_sistema(self, concepto_id: str, whitelist: Dict) -> Tuple[bool, str]:
        comandos_permitidos = (whitelist
                               .get('operaciones_sistema', {})
                               .get('shell', {})
                               .get('comandos_permitidos', []))

        nombre_cmd = concepto_id.replace("CONCEPTO_", "").lower()

        if nombre_cmd in [c.lower() for c in comandos_permitidos]:
            return (True, f"Comando '{nombre_cmd}' permitido por whitelist")

        habilitadas = (whitelist
                       .get('capacidades_fase4a', {})
                       .get('habilitadas', []))
        if concepto_id in habilitadas:
            return (True, f"{concepto_id} en lista de habilitadas")

        return (False, f"Operación de sistema '{nombre_cmd}' no en lista de comandos permitidos")

    def obtener_capacidades_disponibles(self) -> List[str]:
        whitelist = self._cargar_whitelist()
        if whitelist:
            return whitelist.get('capacidades_fase4a', {}).get('habilitadas', [])
        try:
            from core.capacidades_fase import obtener_lista_no_implementadas
            return ["CONCEPTO_CALCULO", "CONCEPTO_MEMORIA_SESION", "CONCEPTO_DIRECTORIO"]
        except ImportError:
            return []

    def obtener_no_implementadas(self) -> List[str]:
        if self._no_implementadas_ids:
            return list(self._no_implementadas_ids)
        whitelist = self._cargar_whitelist()
        if whitelist:
            return whitelist.get('capacidades_fase4a', {}).get('no_implementadas', [])
        return []