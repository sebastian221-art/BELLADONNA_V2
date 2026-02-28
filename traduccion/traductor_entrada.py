"""
Traductor de Entrada - Español → ConceptosAnclados.

MODIFICACIÓN FASE 4A: Ahora usa TraductorContextual para resolver duplicados.

Este es el PRIMER paso del proceso cognitivo de Bell:
Lenguaje humano → Lenguaje interno de Bell
"""
from typing import List, Dict, Optional
from core.concepto_anclado import ConceptoAnclado
from vocabulario.gestor_vocabulario import GestorVocabulario
from traduccion.analizador_español import AnalizadorEspañol

# ← NUEVO: Importar traductor contextual
from traduccion.traductor_contextual import TraductorContextual


class TraductorEntrada:
    """
    Traduce español al lenguaje interno de Bell (ConceptosAnclados).
    
    NUEVO: Resuelve duplicados usando contexto.
    
    Bell NO entiende español. Bell piensa en conceptos.
    Este traductor es el puente.
    """
    
    def __init__(self, gestor: GestorVocabulario = None):
        """
        Inicializa el traductor.
        
        Args:
            gestor: GestorVocabulario con conceptos cargados.
                   Si None, crea uno nuevo.
        """
        self.gestor = gestor or GestorVocabulario()
        self.analizador = AnalizadorEspañol()
        
        # ← NUEVO: Traductor contextual para resolver duplicados
        self.traductor_contextual = TraductorContextual()
    
    def traducir(self, texto: str) -> Dict:
        """
        Traduce texto español a conceptos internos.
        
        MODIFICADO: Ahora usa traductor contextual para resolver duplicados.
        
        Proceso:
        1. Analizar español (spaCy)
        2. Mapear palabras → conceptos candidatos
        3. ← NUEVO: Resolver duplicados por contexto
        4. Calcular confianza
        5. Detectar intención
        
        Returns:
            {
                'texto_original': str,
                'analisis': Dict,              # Del analizador
                'conceptos': List[ConceptoAnclado],
                'conceptos_ids': List[str],    # IDs para debugging
                'palabras_reconocidas': List[str],
                'palabras_desconocidas': List[str],
                'confianza': float,            # 0.0 - 1.0
                'es_pregunta': bool,
                'intencion': str               # Tipo de mensaje
            }
        """
        # 1. Analizar texto
        analisis = self.analizador.analizar(texto)
        
        # 2. Mapear lemas → conceptos
        conceptos_encontrados = []
        palabras_reconocidas = []
        palabras_desconocidas = []
        
        for lema in analisis['lemas']:
            # ← MODIFICADO: Buscar TODOS los candidatos (no solo el primero)
            candidatos = self.gestor.buscar_por_palabra(lema)
            
            if candidatos:
                # ← NUEVO: Si hay múltiples candidatos, usar contexto
                if isinstance(candidatos, list) and len(candidatos) > 1:
                    concepto = self.traductor_contextual.seleccionar_concepto_por_contexto(
                        lema,
                        candidatos,
                        texto
                    )
                elif isinstance(candidatos, list):
                    concepto = candidatos[0]
                else:
                    concepto = candidatos
                
                if concepto and concepto not in conceptos_encontrados:
                    conceptos_encontrados.append(concepto)
                    palabras_reconocidas.append(lema)
            else:
                if lema not in palabras_desconocidas:
                    palabras_desconocidas.append(lema)
        
        # 3. Calcular confianza
        total_palabras_significativas = len([l for l in analisis['lemas'] 
                                            if len(l) > 2])  # Ignorar "el", "la", etc.
        
        if total_palabras_significativas == 0:
            confianza = 0.0
        else:
            confianza = len(palabras_reconocidas) / total_palabras_significativas
        
        # 4. Detectar intención
        intencion = self._detectar_intencion(analisis, conceptos_encontrados)
        
        return {
            'texto_original': texto,
            'analisis': analisis,
            'conceptos': conceptos_encontrados,
            'conceptos_ids': [c.id for c in conceptos_encontrados],
            'palabras_reconocidas': palabras_reconocidas,
            'palabras_desconocidas': palabras_desconocidas,
            'confianza': round(confianza, 2),
            'es_pregunta': analisis['es_pregunta'],
            'intencion': intencion
        }
    
    def _detectar_intencion(self, analisis: Dict, 
                           conceptos: List[ConceptoAnclado]) -> str:
        """
        Detecta la intención del mensaje.
        
        Tipos de intención:
        - SALUDO: "hola", "buenos días"
        - PREGUNTA_CAPACIDAD: "¿puedes...?"
        - PETICION_ACCION: "lee este archivo"
        - PREGUNTA_INFO: "¿qué es...?"
        - AGRADECIMIENTO: "gracias"
        - CONVERSACION: Otros
        """
        conceptos_ids = {c.id for c in conceptos}
        
        # Saludo
        if 'CONCEPTO_HOLA' in conceptos_ids:
            return 'SALUDO'
        
        # Agradecimiento
        if 'CONCEPTO_GRACIAS' in conceptos_ids:
            return 'AGRADECIMIENTO'
        
        # Pregunta sobre capacidades
        if analisis['es_pregunta'] and 'CONCEPTO_PODER' in conceptos_ids:
            return 'PREGUNTA_CAPACIDAD'
        
        # Petición de acción (verbo sin pregunta)
        if not analisis['es_pregunta'] and len(analisis['verbos']) > 0:
            return 'PETICION_ACCION'
        
        # Pregunta general
        if analisis['es_pregunta']:
            return 'PREGUNTA_INFO'
        
        # Por defecto
        return 'CONVERSACION'
    
    def estadisticas(self, traduccion: Dict) -> str:
        """
        Genera reporte legible de una traducción.
        
        Útil para debugging.
        """
        return f"""
Traducción:
  Texto: "{traduccion['texto_original']}"
  Confianza: {traduccion['confianza']:.0%}
  Intención: {traduccion['intencion']}
  
  Reconocidas: {traduccion['palabras_reconocidas']}
  Desconocidas: {traduccion['palabras_desconocidas']}
  
  Conceptos: {traduccion['conceptos_ids']}
        """.strip()