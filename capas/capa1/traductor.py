# capas/capa1/traductor.py
# ================================================
# TRADUCTOR A LENGUAJE BELL — versión 2
# Ahora usa el GestorVocabulario completo
# Mucho más rico en comprensión
# ================================================

from capas.capa1.paquete_capa1 import ConceptoTraducido, Desconocido
from typing import List, Tuple, Optional


class Traductor:
    """
    Traduce contenido a conceptos con grounding.
    Ahora usa el vocabulario completo de Bell.
    """

    def __init__(self):
        self._gestor = None
        self._inicializar_gestor()

    def _inicializar_gestor(self):
        try:
            from biblioteca.vocabulario.gestor_vocabulario import (
                GestorVocabulario
            )
            self._gestor = GestorVocabulario.obtener()
        except Exception as e:
            print(f'Traductor: vocabulario no disponible — {e}')
            self._gestor = None

    def traducir(
        self,
        contenido_normalizado: dict
    ) -> Tuple[List[ConceptoTraducido], List[Desconocido], float]:
        """
        Traduce el contenido a conceptos con grounding.
        """
        texto = contenido_normalizado.get('contenido_limpio', '')
        if not texto:
            return [], [], 0.0

        conceptos    = []
        desconocidos = []

        # Usar el gestor de vocabulario si está disponible
        if self._gestor:
            resultados = self._gestor.buscar_frase(texto)
            palabras_encontradas = set()

            for resultado in resultados:
                palabra  = resultado['palabra']
                concepto = resultado['concepto']

                palabras_encontradas.add(palabra)
                conceptos.append(ConceptoTraducido(
                    id=concepto['id'],
                    texto_original=palabra,
                    grounding=concepto.get('grounding', 0.5),
                    certeza='directo',
                    tipo=concepto.get('tipo', 'concepto')
                ))

            # También buscar en vocabulario base del traductor
            tokens = self._tokenizar(texto)
            for token in tokens:
                if token in palabras_encontradas:
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
                    # Intentar inferencia
                    inferido = self._inferir(token)
                    if inferido:
                        conceptos.append(ConceptoTraducido(
                            id=inferido['id'],
                            texto_original=token,
                            grounding=inferido['grounding'] * 0.7,
                            certeza='inferido',
                            tipo=inferido.get('tipo', 'concepto')
                        ))
                    else:
                        desconocidos.append(Desconocido(
                            fragmento=token,
                            tipo='concepto',
                            inferencia=None
                        ))
        else:
            # Fallback al vocabulario base
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

        # Calcular certeza global
        certeza = (
            sum(c.grounding for c in conceptos) / len(conceptos)
            if conceptos else 0.0
        )

        return conceptos, desconocidos, certeza

    def _tokenizar(self, texto: str) -> List[str]:
        palabras_vacias = {
            'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas',
            'de', 'del', 'en', 'a', 'al'
        }
        tokens = texto.lower().split()
        return [
            t.strip('.,;:!?¿¡"\'()')
            for t in tokens
            if t.strip('.,;:!?¿¡"\'()') and
               len(t.strip('.,;:!?¿¡"\'()')) > 1 and
               t.strip('.,;:!?¿¡"\'()') not in palabras_vacias
        ]

    def _inferir(self, token: str) -> Optional[dict]:
        """Intenta inferir el concepto por raíz."""
        if not self._gestor:
            return None
        if len(token) > 4:
            for palabra in self._gestor._vocabulario:
                if (palabra.startswith(token[:4]) and
                        len(palabra) > 3):
                    return self._gestor._vocabulario[palabra]
        return None

    def _buscar_vocabulario_base(self, token: str) -> Optional[dict]:
        """Vocabulario base hardcodeado como fallback."""
        base = {
            'bell':       {'id': 'BELL_NOMBRE_BELL',     'grounding': 1.0, 'tipo': 'identidad'},
            'belladonna': {'id': 'BELL_NOMBRE_BELLADONNA','grounding': 1.0, 'tipo': 'identidad'},
            'crear':      {'id': 'ACCION_CREAR',          'grounding': 0.9, 'tipo': 'accion'},
            'mostrar':    {'id': 'ACCION_MOSTRAR',        'grounding': 0.9, 'tipo': 'accion'},
            'buscar':     {'id': 'ACCION_BUSCAR',         'grounding': 0.9, 'tipo': 'accion'},
            'borrar':     {'id': 'ACCION_BORRAR',         'grounding': 0.9, 'tipo': 'accion'},
            'agregar':    {'id': 'ACCION_AGREGAR',        'grounding': 0.9, 'tipo': 'accion'},
            'analizar':   {'id': 'ACCION_ANALIZAR',       'grounding': 0.9, 'tipo': 'accion'},
            'ejecutar':   {'id': 'ACCION_EJECUTAR',       'grounding': 0.9, 'tipo': 'accion'},
            'ayuda':      {'id': 'VERBO_AYUDA',           'grounding': 0.9, 'tipo': 'verbo_ayuda'},
            'archivo':    {'id': 'ENTIDAD_ARCHIVO',       'grounding': 1.0, 'tipo': 'entidad'},
            'carpeta':    {'id': 'ENTIDAD_CARPETA',       'grounding': 1.0, 'tipo': 'entidad'},
            'código':     {'id': 'ENTIDAD_CODIGO',        'grounding': 1.0, 'tipo': 'entidad'},
            'codigo':     {'id': 'ENTIDAD_CODIGO',        'grounding': 1.0, 'tipo': 'entidad'},
            'error':      {'id': 'ENTIDAD_ERROR',         'grounding': 1.0, 'tipo': 'entidad'},
        }
        return base.get(token.lower())