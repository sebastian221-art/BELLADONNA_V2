# biblioteca/habilidades/memoria/motor_recuperacion.py
# ============================================================
# MOTOR DE RECUPERACIÓN — Contexto relevante, no contexto bruto
#
# El problema actual: contexto_completo_para_groq() devuelve
# todo el bloque de memoria, mucho del cual no es relevante
# para el mensaje actual.
#
# Este módulo selecciona SOLO lo relevante:
#   1. Perfil base de Sebastian (siempre)
#   2. Episodios recientes si el mensaje tiene referencia temporal
#   3. Conocimiento relacionado al tema si lo hay
#   4. Código guardado si es un mensaje técnico
#   5. Estado emocional del día si hay patrón de sesión
# ============================================================

from typing import Optional


def recuperar_contexto(texto: str, tipo_mensaje: str = '',
                        emocion: str = '') -> str:
    """
    Recupera el contexto de memoria relevante para este mensaje.
    Retorna string listo para inyectar al prompt de Groq.

    Principio: menos contexto relevante > más contexto ruidoso.
    """
    try:
        from biblioteca.habilidades.memoria.gestor import obtener_memoria
        mem = obtener_memoria()
    except Exception:
        return ''

    tl   = texto.lower()
    partes: list = []

    # 1. Perfil base siempre (compacto)
    perfil = _obtener_perfil_compacto(mem)
    if perfil:
        partes.append(f'[Sebastian] {perfil}')

    # 2. Sesión actual (últimos 3 turnos)
    ctx_sesion = mem.contexto_para_groq(3)
    if ctx_sesion:
        partes.append(ctx_sesion)

    # 3. Episodios recientes si hay referencia temporal
    _refs_tiempo = ['ayer', 'antes', 'la semana', 'el otro día', 'me acordás',
                    'acordás', 'recordás', 'la última vez', 'aquella vez']
    if any(r in tl for r in _refs_tiempo):
        episodios = _obtener_episodios_relevantes(mem, n=2)
        if episodios:
            partes.append(episodios)

    # 4. Conocimiento relacionado si es pregunta informativa
    if tipo_mensaje in ('pregunta', 'solicitud_informacion'):
        conocimiento = _buscar_conocimiento_relevante(mem, texto)
        if conocimiento:
            partes.append(conocimiento)

    # 5. Código guardado si es técnico
    if tipo_mensaje == 'solicitud_tecnica':
        codigo_prev = _buscar_codigo_previo(mem, texto)
        if codigo_prev:
            partes.append(codigo_prev)

    # 6. Estado emocional de la sesión si hay patrón
    try:
        from biblioteca.habilidades.lenguaje.memoria_sesion import MemoriaSesion
        estado = MemoriaSesion.obtener().obtener_estado()
        if estado.nota_bell:
            partes.append(f'[Contexto emocional sesión] {estado.nota_bell}')
    except Exception:
        pass

    return '\n'.join(partes)


def _obtener_perfil_compacto(mem) -> str:
    """Perfil de Sebastian en una línea."""
    try:
        perfil = mem.obtener_perfil()
        items = []
        if perfil.get('nombre'):   items.append(f"nombre={perfil['nombre']}")
        if perfil.get('ciudad'):   items.append(f"ciudad={perfil['ciudad']}")
        if perfil.get('trabajo'):  items.append(f"trabajo={perfil['trabajo']}")
        if perfil.get('proyecto'): items.append(f"proyecto={perfil['proyecto']}")
        return ', '.join(items) if items else ''
    except Exception:
        return ''


def _obtener_episodios_relevantes(mem, n: int = 2) -> str:
    """Obtiene los episodios más recientes formateados."""
    try:
        episodios = mem.obtener_episodios_recientes(n)
        if not episodios:
            return ''
        lineas = ['[Sesiones anteriores]']
        for ep in episodios:
            fecha  = ep.get('fecha', '')[:10]
            resumen = ep.get('resumen', '')[:150]
            lineas.append(f'{fecha}: {resumen}')
        return '\n'.join(lineas)
    except Exception:
        return ''


def _buscar_conocimiento_relevante(mem, texto: str) -> str:
    """Busca en la base de conocimiento si hay algo relacionado."""
    try:
        # Extraer palabras clave del texto (ignorar stopwords)
        _STOP = {'qué', 'que', 'cómo', 'como', 'es', 'son', 'un', 'una',
                 'el', 'la', 'los', 'hay', 'de', 'del', 'al', 'en', 'y', 'o'}
        palabras = [w for w in texto.lower().split() if w not in _STOP and len(w) > 3]
        for palabra in palabras[:3]:
            resultado = mem.consultar_conocimiento(palabra)
            if resultado:
                resp = resultado.get('respuesta', '')[:200]
                return f'[Conocimiento previo sobre "{palabra}"] {resp}'
    except Exception:
        pass
    return ''


def _buscar_codigo_previo(mem, texto: str) -> str:
    """Busca código guardado relacionado."""
    try:
        resultado = mem.buscar_codigo(texto)
        if resultado:
            codigo = resultado.get('codigo', '')[:300]
            instruccion = resultado.get('instruccion', '')[:60]
            return f'[Código similar guardado: "{instruccion}"]\n{codigo}'
    except Exception:
        pass
    return ''