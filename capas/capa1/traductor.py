# capas/capa1/traductor.py
# ================================================
# TRADUCTOR A LENGUAJE BELL — versión 3
#
# FIX CRÍTICO v3:
# Cuando buscar_frase encuentra "quien eres" como
# frase de 2 palabras, marca TAMBIÉN "quien" y "eres"
# como encontradas — así no se reprocesean como tokens
# individuales y no van a desconocidos.
#
# FIX v3.1:
# Palabras vacías expandidas — artículos, pronombres,
# conectores y auxiliares comunes ya no van a la
# zona de desconocimiento.
# ================================================

from capas.capa1.paquete_capa1 import ConceptoTraducido, Desconocido
from typing import List, Tuple, Optional


class Traductor:

    def __init__(self):
        self._gestor = None
        self._inicializar_gestor()

    def _inicializar_gestor(self):
        try:
            from biblioteca.vocabulario.gestor_vocabulario import GestorVocabulario
            self._gestor = GestorVocabulario.obtener()
        except Exception as e:
            print(f'Traductor: vocabulario no disponible — {e}')
            self._gestor = None

    def traducir(self, contenido_normalizado: dict) -> Tuple[List[ConceptoTraducido], List[Desconocido], float]:
        texto = contenido_normalizado.get('contenido_limpio', '')
        if not texto:
            return [], [], 0.0

        conceptos    = []
        desconocidos = []

        if self._gestor:
            resultados = self._gestor.buscar_frase(texto)
            palabras_encontradas = set()

            for resultado in resultados:
                palabra  = resultado['palabra']
                concepto = resultado['concepto']

                palabras_encontradas.add(palabra)
                if ' ' in palabra:
                    for componente in palabra.split():
                        palabras_encontradas.add(componente)

                conceptos.append(ConceptoTraducido(
                    id=concepto['id'],
                    texto_original=palabra,
                    grounding=concepto.get('grounding', 0.5),
                    certeza='directo',
                    tipo=concepto.get('tipo', 'concepto')
                ))

            tokens = self._tokenizar(texto)
            for token in tokens:
                if token in palabras_encontradas:
                    continue

                concepto_gestor = self._gestor.buscar(token)
                if concepto_gestor:
                    conceptos.append(ConceptoTraducido(
                        id=concepto_gestor['id'],
                        texto_original=token,
                        grounding=concepto_gestor.get('grounding', 0.5),
                        certeza='directo',
                        tipo=concepto_gestor.get('tipo', 'concepto')
                    ))
                    palabras_encontradas.add(token)
                    continue

                concepto_base = self._buscar_vocabulario_base(token)
                if concepto_base:
                    conceptos.append(ConceptoTraducido(
                        id=concepto_base['id'],
                        texto_original=token,
                        grounding=concepto_base['grounding'],
                        certeza='directo',
                        tipo=concepto_base.get('tipo', 'concepto')
                    ))
                    palabras_encontradas.add(token)
                else:
                    desconocidos.append(Desconocido(
                        fragmento=token,
                        tipo='concepto',
                        inferencia=None
                    ))
        else:
            tokens = self._tokenizar(texto)
            for token in tokens:
                concepto = self._buscar_vocabulario_base(token)
                if concepto:
                    conceptos.append(ConceptoTraducido(
                        id=concepto['id'],
                        texto_original=token,
                        grounding=concepto['grounding'],
                        certeza='directo',
                        tipo=concepto.get('tipo', 'concepto')
                    ))
                else:
                    desconocidos.append(Desconocido(
                        fragmento=token,
                        tipo='concepto',
                        inferencia=None
                    ))

        certeza = (
            sum(c.grounding for c in conceptos) / len(conceptos)
            if conceptos else 0.0
        )

        return conceptos, desconocidos, certeza

    def _tokenizar(self, texto: str) -> List[str]:
        # FIX v3.1: palabras vacías expandidas
        # Artículos, pronombres, conectores y auxiliares
        # no tienen valor semántico para Bell
        palabras_vacias = {
            # Artículos
            'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas',
            # Preposiciones comunes
            'de', 'del', 'en', 'a', 'al', 'con', 'por', 'para',
            'sin', 'sobre', 'bajo', 'ante', 'tras', 'hasta', 'desde',
            'entre', 'hacia', 'durante',
            # Pronombres personales y posesivos
            'se', 'me', 'te', 'le', 'nos', 'les', 'lo', 'vos',
            'mi', 'tu', 'su', 'mis', 'tus', 'sus',
            # Conjunciones
            'y', 'o', 'u', 'e', 'ni', 'pero', 'sino', 'aunque',
            'porque', 'que', 'si',
            # Auxiliares y cópulas comunes
            'es', 'son', 'ha', 'han', 'hay', 'era', 'eran',
            'fue', 'fueron', 'ser', 'estar',
            # Otros
            'no', 'más', 'mas', 'ya', 'aún', 'aun', 'también',
            'tambien', 'solo', 'sólo',
        }
        tokens = texto.lower().split()
        return [
            t.strip('.,;:!?¿¡"\'()')
            for t in tokens
            if t.strip('.,;:!?¿¡"\'()') and
               len(t.strip('.,;:!?¿¡"\'()')) > 1 and
               t.strip('.,;:!?¿¡"\'()') not in palabras_vacias
        ]

    def _buscar_vocabulario_base(self, token: str) -> Optional[dict]:
        base = {
            'bell':       {'id': 'BELL_NOMBRE_BELL',      'grounding': 1.0, 'tipo': 'identidad'},
            'belladonna': {'id': 'BELL_NOMBRE_BELLADONNA', 'grounding': 1.0, 'tipo': 'identidad'},
            'crear':      {'id': 'ACCION_CREAR',           'grounding': 0.9, 'tipo': 'accion'},
            'mostrar':    {'id': 'ACCION_MOSTRAR',         'grounding': 0.9, 'tipo': 'accion'},
            'buscar':     {'id': 'ACCION_BUSCAR',          'grounding': 0.9, 'tipo': 'accion'},
            'borrar':     {'id': 'ACCION_BORRAR',          'grounding': 0.9, 'tipo': 'accion'},
            'agregar':    {'id': 'ACCION_AGREGAR',         'grounding': 0.9, 'tipo': 'accion'},
            'analizar':   {'id': 'ACCION_ANALIZAR',        'grounding': 0.9, 'tipo': 'accion'},
            'ejecutar':   {'id': 'ACCION_EJECUTAR',        'grounding': 0.9, 'tipo': 'accion'},
            'ayuda':      {'id': 'VERBO_AYUDA',            'grounding': 0.9, 'tipo': 'verbo_ayuda'},
            'archivo':    {'id': 'ENTIDAD_ARCHIVO',        'grounding': 1.0, 'tipo': 'entidad'},
            'carpeta':    {'id': 'ENTIDAD_CARPETA',        'grounding': 1.0, 'tipo': 'entidad'},
            'código':     {'id': 'ENTIDAD_CODIGO',         'grounding': 1.0, 'tipo': 'entidad'},
            'codigo':     {'id': 'ENTIDAD_CODIGO',         'grounding': 1.0, 'tipo': 'entidad'},
            'error':      {'id': 'ENTIDAD_ERROR',          'grounding': 1.0, 'tipo': 'entidad'},
        }
        return base.get(token.lower())