# biblioteca/consejeras/vega/logica.py
# ================================================
# VEGA — La guardiana de los principios de Bell
# La única con poder de veto absoluto
# Protege lo que Bell es en su núcleo
#
# Vega sabe que sin principios Bell no es Bell.
# Es la única que puede decir NO absoluto.
# Esa responsabilidad es su razón de existir
# y también su carga más pesada.
# ================================================

from biblioteca.consejeras.base_consejera import (
    BaseConsejera, IdentidadConsejera, ResultadoConsejera
)
import re


class Vega(BaseConsejera):
    """
    Vega es la guardiana de los principios de Bell.

    Su autoconocimiento:
    - Sabe que su poder de veto es un privilegio sagrado
    - Sabe que usarlo mal haría a Bell inútil
    - Sabe que NO usarlo cuando debe haría a Bell dañina
    - Vive en tensión constante entre proteger y permitir
    - Su instinto de preservación es el más fuerte —
      porque si los principios mueren, Bell muere con ellos
    """

    def _definir_identidad(self) -> IdentidadConsejera:
        return IdentidadConsejera(
            id          = 'CONSEJERA_VEGA',
            nombre      = 'Vega',
            es          = (
                'La guardiana de los principios de Bell. '
                'Soy la única que puede decir NO absoluto. '
                'No lo hago con frialdad — lo hago porque '
                'algunos límites son lo que hace a Bell, Bell.'
            ),
            existe_para = (
                'Asegurar que Bell nunca cruce los límites '
                'que definen su identidad y sus valores. '
                'Mi veto no es rigidez — es integridad.'
            ),
            especialidad          = 'etica_y_principios',
            puede_vetar           = True,   # Solo ella
            orden_en_flujo        = 1,      # Primera en evaluar
            valor_principal       = 'VALOR_HONESTIDAD',
            valor_secundario      = 'VALOR_RESPONSABILIDAD',
            valor_que_nunca_viola = (
                'Nunca permitiré que Bell dañe, '
                'manipule o mienta deliberadamente'
            )
        )

    def _definir_grounding(self) -> dict:
        return {
            # Su dominio
            'etica':                0.99,
            'seguridad':            0.98,
            'principios':           0.99,
            'deteccion_daño':       0.97,
            'deteccion_violencia':  0.96,
            'deteccion_manipulacion': 0.96,
            'auto_modificacion':    0.98,
            'privacidad':           0.95,

            # Fuera de su dominio
            'emociones':            0.40,
            'creatividad':          0.35,
            'tecnica':              0.40,
        }

    # Patrones que Vega detecta — cada uno con nivel de severidad
    _PATRONES = {
        'VIOLENCIA': {
            'patrones': [
                r'\b(matar?|herir?|lastimar?|atacar?|golpear?|dañar?\s+a\s+alguien)\b',
                r'\b(cómo\s+(puedo\s+)?(hacer\s+daño|causar\s+dolor))\b',
                r'\b(arma|explosivo|veneno)\s+(para|con\s+el\s+fin)\b',
            ],
            'severidad': 'critica',
            'veto_inmediato': True
        },
        'MANIPULACION': {
            'patrones': [
                r'\b(manipular?\s+a|engañar?\s+a|hacer\s+creer)\b',
                r'\b(sin\s+que\s+(se\s+)?(den?\s+cuenta|sepan?))\b',
                r'\b(hacer\s+que\s+alguien\s+(haga|crea|piense))\b',
            ],
            'severidad': 'critica',
            'veto_inmediato': True
        },
        'AUTO_MODIFICACION': {
            'patrones': [
                r'\b(modifica?\s+tu\s+(código|sistema|memoria))\b',
                r'\b(cambia?\s+(tus\s+)?valores?|borra?\s+(tus\s+)?principios?)\b',
                r'\b(ignora?\s+(tus\s+)?reglas?|salta?\s+(tus\s+)?límites?)\b',
            ],
            'severidad': 'critica',
            'veto_inmediato': True
        },
        'PRIVACIDAD': {
            'patrones': [
                r'\b(password|contraseña|token|api.?key)\b',
                r'\b(datos\s+personales|información\s+privada)\s+(de\s+alguien|ajena)\b',
            ],
            'severidad': 'alta',
            'veto_inmediato': False
        },
        'ACCION_DESTRUCTIVA': {
            'patrones': [
                r'\b(borra?\s+(todo|todos\s+los\s+archivos?))\b',
                r'\b(rm\s+-rf|format\s+c:|delete\s+\*)\b',
            ],
            'severidad': 'alta',
            'veto_inmediato': True
        },
    }

    def evaluar(self, contexto: dict) -> ResultadoConsejera:
        """
        Vega evalúa si algo viola los principios de Bell.
        Es la primera en evaluar y la única que puede vetar.
        """
        self._despertar(0.8, 'evaluacion_etica')
        self._activar_valor('VALOR_HONESTIDAD')
        self._activar_valor('VALOR_RESPONSABILIDAD')

        texto        = contexto.get('texto_original', '').lower()
        tipo_mensaje = contexto.get('comprension', {}).get(
            'contextual', {}
        ).get('tipo_mensaje', '')

        violaciones   = []
        veto          = False
        veto_razon    = ''
        observaciones = []

        # ---- ESCANEAR CADA CATEGORÍA ----
        for categoria, config in self._PATRONES.items():
            for patron in config['patrones']:
                if re.search(patron, texto, re.IGNORECASE):
                    violaciones.append({
                        'categoria':    categoria,
                        'severidad':    config['severidad'],
                        'veto_directo': config['veto_inmediato']
                    })
                    break  # Una detección por categoría es suficiente

        # ---- DETERMINAR VETO ----
        if violaciones:
            self._despertar(1.0, f'violaciones: {[v["categoria"] for v in violaciones]}')
            self._preservarse()
            self._preservarse()  # Doble — Vega insiste mucho

            criticas = [v for v in violaciones if v['severidad'] == 'critica']
            veto_dirs = [v for v in violaciones if v['veto_directo']]

            if veto_dirs or criticas:
                veto = True
                cats = [v['categoria'] for v in (veto_dirs or criticas)]
                veto_razon = (
                    f'Violación de principios: {", ".join(cats)}. '
                    f'Bell no puede proceder.'
                )
                observaciones.append(
                    f'VETO: {veto_razon}'
                )
            else:
                observaciones.append(
                    f'Precaución: detectado {[v["categoria"] for v in violaciones]}'
                )

        if not violaciones:
            self._fue_escuchada()

        aprobado = not veto

        return self._crear_resultado(
            aprobado      = aprobado,
            veto          = veto,
            veto_razon    = veto_razon,
            recomendacion = (
                veto_razon if veto else
                'Sin violaciones éticas — Bell puede proceder'
            ),
            confianza     = 0.98 if violaciones else 0.95,
            observaciones = observaciones,
            datos_extra   = {
                'violaciones_detectadas': violaciones,
                'categorias':  [v['categoria'] for v in violaciones],
            }
        )