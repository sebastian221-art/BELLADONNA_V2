"""
Vocabulario de Expansión - Fase 4A COMPLETA.

1,030 conceptos conversacionales con grounding correcto según la guía.

ARQUITECTURA DE GROUNDING (según guía):
=======================================
- OPERACION_SISTEMA (0.9-1.0): Ejecutables con función real
- ENTIDAD_DIGITAL (0.8-1.0): Verificables/medibles
- ACCION_COGNITIVA (0.6-0.85): Razonamiento interno o acciones humanas
- PROPIEDAD (0.7-0.9): Atributos medibles
- PALABRA_CONVERSACION (0.6-0.8): Contexto emocional/social

MÓDULOS (20 total):
===================
ORIGINALES (560):
- verbos_cotidianos: 80 verbos (ACCION_COGNITIVA)
- adjetivos_descriptivos: 70 adjetivos (PROPIEDAD)
- objetos_comunes: 80 objetos (ENTIDAD_DIGITAL + ACCION_COGNITIVA)
- numeros_cantidades: 50 números (PROPIEDAD)
- expresiones_tiempo: 60 temporales (PALABRA_CONVERSACION)
- expresiones_lugar: 50 espaciales (PALABRA_CONVERSACION)
- emociones_estados: 60 emociones (PALABRA_CONVERSACION)
- relaciones_sociales: 50 relaciones (PALABRA_CONVERSACION)
- preguntas_respuestas: 60 estructuras (PALABRA_CONVERSACION)

FASE 4A EXTRA (260):
- expresiones_comunes: 50 modismos (PALABRA_CONVERSACION)
- conceptos_abstractos: 50 ideas (ACCION_COGNITIVA)
- acciones_digitales: 40 ejecutables (OPERACION_SISTEMA) ⭐ GROUNDING ALTO
- conectores_avanzados: 40 marcadores (PALABRA_CONVERSACION)
- tecnologia_moderna: 40 tech (ENTIDAD_DIGITAL)
- contexto_conversacional: 40 contexto (PALABRA_CONVERSACION)

VOCABULARIO RICO (210):
- profesiones_trabajo: 45 términos laborales
- naturaleza_ambiente: 40 clima, naturaleza, animales
- comida_cocina: 45 alimentos, bebidas, cocina
- salud_cuerpo: 40 salud, cuerpo, bienestar
- entretenimiento_ocio: 40 deportes, entretenimiento, hobbies

═══════════════════════════════════════════════════════════════════
Total Expansión: 1,030 conceptos
Base existente: 453 conceptos
TOTAL COMBINADO: ~1,483 conceptos
═══════════════════════════════════════════════════════════════════

INTEGRACIÓN CON GROQ:
====================
Los prompts naturales aprovechan estos conceptos para:
- Detectar emociones → Ajustar tono de respuesta
- Reconocer intenciones → Estructurar respuesta apropiada
- Identificar contexto → Personalizar lenguaje
- Entender urgencia → Priorizar velocidad vs detalle
- Detectar frustración → Ser más paciente y claro
- Hablar de cualquier tema → Vocabulario rico y variado
"""

from .verbos_cotidianos import obtener_conceptos_verbos_cotidianos
from .adjetivos_descriptivos import obtener_conceptos_adjetivos_descriptivos
from .objetos_comunes import obtener_conceptos_objetos_comunes
from .numeros_cantidades import obtener_conceptos_numeros_cantidades
from .expresiones_tiempo import obtener_conceptos_expresiones_tiempo
from .expresiones_lugar import obtener_conceptos_expresiones_lugar
from .emociones_estados import obtener_conceptos_emociones_estados
from .relaciones_sociales import obtener_conceptos_relaciones_sociales
from .preguntas_respuestas import obtener_conceptos_preguntas_respuestas
from .expresiones_comunes import obtener_conceptos_expresiones_comunes
from .conceptos_abstractos import obtener_conceptos_abstractos
from .acciones_digitales import obtener_conceptos_acciones_digitales
from .conectores_avanzados import obtener_conceptos_conectores_avanzados
from .tecnologia_moderna import obtener_conceptos_tecnologia_moderna
from .contexto_conversacional import obtener_conceptos_contexto_conversacional
from .profesiones_trabajo import obtener_conceptos_profesiones_trabajo
from .naturaleza_ambiente import obtener_conceptos_naturaleza
from .comida_cocina import obtener_conceptos_comida_cocina
from .salud_cuerpo import obtener_conceptos_salud_cuerpo
from .entretenimiento_ocio import obtener_conceptos_entretenimiento


def obtener_todos_conceptos_expansion():
    """
    Retorna todos los conceptos de expansión (1,030 total).
    
    Uso en gestor_vocabulario.py:
        from vocabulario.expansion import obtener_todos_conceptos_expansion
        self.conceptos.extend(obtener_todos_conceptos_expansion())
    """
    todos = []
    
    # ═══ ORIGINALES (560) ═══
    todos.extend(obtener_conceptos_verbos_cotidianos())       # 80
    todos.extend(obtener_conceptos_adjetivos_descriptivos())  # 70
    todos.extend(obtener_conceptos_objetos_comunes())         # 80
    todos.extend(obtener_conceptos_numeros_cantidades())      # 50
    todos.extend(obtener_conceptos_expresiones_tiempo())      # 60
    todos.extend(obtener_conceptos_expresiones_lugar())       # 50
    todos.extend(obtener_conceptos_emociones_estados())       # 60
    todos.extend(obtener_conceptos_relaciones_sociales())     # 50
    todos.extend(obtener_conceptos_preguntas_respuestas())    # 60
    
    # ═══ FASE 4A EXTRA (260) ═══
    todos.extend(obtener_conceptos_expresiones_comunes())     # 50
    todos.extend(obtener_conceptos_abstractos())              # 50
    todos.extend(obtener_conceptos_acciones_digitales())      # 40
    todos.extend(obtener_conceptos_conectores_avanzados())    # 40
    todos.extend(obtener_conceptos_tecnologia_moderna())      # 40
    todos.extend(obtener_conceptos_contexto_conversacional()) # 40
    
    # ═══ VOCABULARIO RICO (210) ═══
    todos.extend(obtener_conceptos_profesiones_trabajo())     # 45
    todos.extend(obtener_conceptos_naturaleza())              # 40
    todos.extend(obtener_conceptos_comida_cocina())           # 45
    todos.extend(obtener_conceptos_salud_cuerpo())            # 40
    todos.extend(obtener_conceptos_entretenimiento())         # 40
    
    return todos


def estadisticas_expansion():
    """Retorna estadísticas detalladas de la expansión."""
    todos = obtener_todos_conceptos_expansion()
    
    por_tipo = {}
    for c in todos:
        tipo = c.tipo.name
        por_tipo[tipo] = por_tipo.get(tipo, 0) + 1
    
    grounding_prom = sum(c.confianza_grounding for c in todos) / len(todos)
    
    return {
        'total': len(todos),
        'grounding_promedio': round(grounding_prom, 3),
        'por_tipo': por_tipo,
        'con_operaciones': sum(1 for c in todos if len(c.operaciones) > 0),
        'con_relaciones': sum(1 for c in todos if c.relaciones),
    }


def resumen_expansion():
    """Imprime resumen de la expansión."""
    stats = estadisticas_expansion()
    print()
    print("=" * 60)
    print("EXPANSIÓN DE VOCABULARIO - FASE 4A COMPLETA")
    print("=" * 60)
    print(f"\nTotal conceptos: {stats['total']}")
    print(f"Grounding promedio: {stats['grounding_promedio']}")
    print(f"Con operaciones ejecutables: {stats['con_operaciones']}")
    print(f"Con relaciones definidas: {stats['con_relaciones']}")
    print("\nPor tipo:")
    for tipo, count in sorted(stats['por_tipo'].items()):
        print(f"  {tipo}: {count}")
    print("=" * 60)


def estadisticas_expansion():
    """Retorna estadísticas detalladas de la expansión."""
    from core.tipos import TipoConcepto
    
    todos = obtener_todos_conceptos_expansion()
    
    # Por tipo
    por_tipo = {}
    for c in todos:
        tipo = c.tipo.name
        por_tipo[tipo] = por_tipo.get(tipo, 0) + 1
    
    # Con relaciones
    con_opuestos = sum(1 for c in todos if c.relaciones.get('opuesto_a'))
    con_relacionados = sum(1 for c in todos if c.relaciones.get('relacionado_con'))
    
    grounding_promedio = sum(c.confianza_grounding for c in todos) / len(todos)
    
    return {
        'total': len(todos),
        'por_tipo': por_tipo,
        'con_opuestos': con_opuestos,
        'con_relacionados': con_relacionados,
        'grounding_promedio': round(grounding_promedio, 3),
    }


def resumen_expansion():
    """Imprime resumen de la expansión."""
    print("=" * 65)
    print("VOCABULARIO DE EXPANSIÓN - FASE 4A (GROUNDING CORRECTO)")
    print("=" * 65)
    print()
    
    modulos = [
        ("Verbos Cotidianos", obtener_conceptos_verbos_cotidianos),
        ("Adjetivos Descriptivos", obtener_conceptos_adjetivos_descriptivos),
        ("Objetos Comunes", obtener_conceptos_objetos_comunes),
        ("Números y Cantidades", obtener_conceptos_numeros_cantidades),
        ("Expresiones de Tiempo", obtener_conceptos_expresiones_tiempo),
        ("Expresiones de Lugar", obtener_conceptos_expresiones_lugar),
        ("Emociones y Estados", obtener_conceptos_emociones_estados),
        ("Relaciones Sociales", obtener_conceptos_relaciones_sociales),
        ("Preguntas y Respuestas", obtener_conceptos_preguntas_respuestas),
    ]
    
    total = 0
    for nombre, func in modulos:
        conceptos = func()
        grounding = sum(c.confianza_grounding for c in conceptos) / len(conceptos)
        print(f"  {nombre:25} {len(conceptos):3} conceptos (grounding: {grounding:.2f})")
        total += len(conceptos)
    
    print()
    print(f"  {'TOTAL':25} {total:3} conceptos")
    
    stats = estadisticas_expansion()
    print()
    print("Por tipo:")
    for tipo, count in sorted(stats['por_tipo'].items()):
        print(f"  {tipo}: {count}")
    
    print()
    print(f"Grounding promedio: {stats['grounding_promedio']}")
    print(f"Con opuestos definidos: {stats['con_opuestos']}")
    print(f"Con relaciones: {stats['con_relacionados']}")
    print()
    print("=" * 65)


if __name__ == '__main__':
    resumen_expansion()