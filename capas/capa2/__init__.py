# capas/capa2/__init__.py
# ================================================
# CAPA 2 — Activación neuronal + grounding 9D
# CORREGIDO: red_activa siempre es dict
# ================================================
from biblioteca import Biblioteca
from biblioteca.zona_desconocimiento.zona import ZonaDesconocimiento


def procesar(paquete_capa1: dict) -> dict:
    try:
        return _procesar_interno(paquete_capa1)
    except Exception as e:
        import traceback; traceback.print_exc()
        return {
            'exitoso':       False,
            'error':         f'Error en Capa 2: {str(e)}',
            'red_activa':    {
                'nodos_primarios':    [],
                'nodos_secundarios':  [],
                'nodos_terciarios':   [],
                'energia_total':      0.0,
                'nivel_conocimiento': 0.0,
                'tiene_conocimiento': False,
                'total_activados':    0,
            },
            'paquete_capa1': paquete_capa1
        }


def _procesar_interno(paquete_capa1: dict) -> dict:

    biblioteca = Biblioteca.obtener()

    if not biblioteca.iniciada:
        return {
            'exitoso':    False,
            'error':      'Biblioteca neuronal no iniciada',
            'red_activa': {},
            'paquete_capa1': paquete_capa1
        }

    conceptos    = paquete_capa1.get('conceptos', [])
    desconocidos = paquete_capa1.get('desconocidos', [])
    contexto_raw = paquete_capa1.get('contexto', {})
    texto        = paquete_capa1.get('contenido_original', '')

    # Normalizar conceptos a dict
    conceptos_norm = []
    for c in conceptos:
        if isinstance(c, dict):
            conceptos_norm.append(c)
        else:
            conceptos_norm.append({
                'id':       getattr(c, 'id', ''),
                'grounding': getattr(c, 'grounding', 0.5),
                'certeza':   getattr(c, 'certeza', 'directo'),
                'tipo':      getattr(c, 'tipo', 'concepto')
            })

    # Enriquecer con grounding 9D
    conceptos_enriquecidos = _enriquecer_con_grounding(
        conceptos_norm, contexto_raw
    )

    # Activar la red — activador.py ahora SIEMPRE retorna dict
    red_activa = biblioteca.activar(conceptos_enriquecidos, texto)

    # Defensa extra: si por cualquier razón no es dict, convertir
    if not isinstance(red_activa, dict):
        if hasattr(red_activa, 'a_dict'):
            red_activa = red_activa.a_dict()
        else:
            red_activa = {
                'nodos_primarios':    [],
                'nodos_secundarios':  [],
                'nodos_terciarios':   [],
                'energia_total':      0.0,
                'nivel_conocimiento': 0.0,
                'tiene_conocimiento': False,
                'total_activados':    0,
            }

    # Registrar uso en grounding
    _registrar_uso_grounding(conceptos_norm, red_activa)

    # Enviar desconocidos a zona
    if desconocidos:
        zona = ZonaDesconocimiento.obtener()
        desconocidos_dicts = []
        for d in desconocidos:
            if isinstance(d, dict):
                desconocidos_dicts.append(d)
            else:
                desconocidos_dicts.append({
                    'fragmento':  getattr(d, 'fragmento', ''),
                    'tipo':       getattr(d, 'tipo', 'concepto'),
                    'inferencia': getattr(d, 'inferencia', None)
                })
        zona.agregar_desde_capa1(desconocidos_dicts)

    nivel_conocimiento = {
        'bell_conoce_esto':  red_activa.get('tiene_conocimiento', False),
        'profundidad':        red_activa.get('nivel_conocimiento', 0.0),
        'tiene_habilidades':  _verificar_habilidades(red_activa),
        'gaps_detectados':    _detectar_gaps(red_activa, desconocidos),
        'grounding_promedio': _calcular_grounding_promedio(conceptos_enriquecidos)
    }

    return {
        'exitoso':                True,
        'red_activa':             red_activa,
        'nivel_conocimiento':     nivel_conocimiento,
        'conceptos_enriquecidos': conceptos_enriquecidos,
        'desconocidos_enviados':  len(desconocidos),
        'paquete_capa1':          paquete_capa1
    }


def _enriquecer_con_grounding(conceptos: list, contexto: dict) -> list:
    try:
        from biblioteca.grounding.calculador import CalculadorGrounding
        calc = CalculadorGrounding.obtener()
        enriquecidos = []
        for c in conceptos:
            cid  = c.get('id', '')
            tipo = c.get('tipo', 'concepto')
            gb   = c.get('grounding', 0.5)
            g9d  = calc.calcular(cid, tipo, contexto, gb)
            enriquecido = dict(c)
            enriquecido['grounding_9d']       = g9d.resumen()
            enriquecido['grounding_efectivo'] = g9d.efectivo()
            enriquecido['puede_ejecutar']     = g9d.puede_ejecutar()
            enriquecido['nivel_comprension']  = g9d.nivel_comprension()
            enriquecido['es_seguro']          = g9d.es_seguro()
            enriquecido['grounding']          = g9d.efectivo()
            enriquecidos.append(enriquecido)
        return enriquecidos
    except Exception as e:
        print(f'Capa 2: grounding 9D no disponible ({e}), usando base')
        return conceptos


def _registrar_uso_grounding(conceptos: list, red_activa: dict):
    try:
        from biblioteca.grounding.calculador import CalculadorGrounding
        calc    = CalculadorGrounding.obtener()
        exitoso = red_activa.get('tiene_conocimiento', False)
        for c in conceptos:
            cid = c.get('id', '')
            if cid:
                calc.registrar_uso(cid, exitoso)
    except Exception:
        pass


def _calcular_grounding_promedio(conceptos: list) -> float:
    if not conceptos:
        return 0.0
    groundings = [
        c.get('grounding_efectivo', c.get('grounding', 0.5))
        for c in conceptos
    ]
    return round(sum(groundings) / len(groundings), 3)


def _verificar_habilidades(red_activa: dict) -> bool:
    todos = (
        red_activa.get('nodos_primarios', []) +
        red_activa.get('nodos_secundarios', [])
    )
    for nodo in todos:
        if isinstance(nodo, dict) and 'HABILIDAD' in nodo.get('nodo_id', '').upper():
            return True
    return False


def _detectar_gaps(red_activa: dict, desconocidos: list) -> list:
    gaps = []
    for desc in desconocidos:
        frag = (desc.get('fragmento', '') if isinstance(desc, dict)
                else getattr(desc, 'fragmento', ''))
        gaps.append({'tipo': 'concepto', 'descripcion': frag, 'origen': 'capa1'})
    if not red_activa.get('nodos_primarios'):
        gaps.append({
            'tipo': 'conocimiento',
            'descripcion': 'Sin activación primaria',
            'origen': 'capa2'
        })
    return gaps