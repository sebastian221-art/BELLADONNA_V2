# biblioteca/vocabulario/gestor_vocabulario.py
# ================================================
# GESTOR DE VOCABULARIO — v2 COMPLETO
# Carga todos los módulos de vocabulario.
# ================================================

from typing import Optional, Dict, List


class GestorVocabulario:
    _instancia = None

    def __init__(self):
        self._vocabulario:  Dict[str, dict]       = {}
        self._indice_id:    Dict[str, List[str]]  = {}
        self._cargado = False

    @classmethod
    def obtener(cls) -> 'GestorVocabulario':
        if cls._instancia is None:
            cls._instancia = cls()
            cls._instancia.cargar_todo()
        return cls._instancia

    def cargar_todo(self):
        modulos = [
            # ── Núcleo original ──────────────────────────
            ('saludos',               'SALUDOS'),
            ('verbos_comunes',        'VERBOS_COMUNES'),
            ('preguntas',             'PREGUNTAS'),
            ('emociones',             'EMOCIONES'),
            ('tiempo',                'TIEMPO'),
            ('conectores',            'CONECTORES'),
            ('bell_identidad',        'BELL_IDENTIDAD'),
            # ── Módulos v2 ───────────────────────────────
            ('cotidiano',             'CONCEPTOS_COTIDIANO'),
            ('colombia',              'CONCEPTOS_COLOMBIA'),
            ('tecnologia',            'CONCEPTOS_TECNOLOGIA'),
            ('conversacion_profunda', 'CONCEPTOS_PROFUNDO'),
            ('internet_redes',        'CONCEPTOS_INTERNET'),
            ('gastronomia',           'CONCEPTOS_GASTRONOMIA'),
            ('expresiones_expandidas','CONCEPTOS_EXPRESIONES'),
            ('mundo_vida',            'CONCEPTOS_MUNDO'),
            # ── Expansión masiva v3 — cobertura 80%+ ─────
            ('articulos_determinantes','ARTICULOS_DETERMINANTES'),
            ('pronombres',             'PRONOMBRES'),
            ('adjetivos',              'ADJETIVOS'),
            ('colores',                'COLORES'),
            ('numeros_cantidades',     'NUMEROS_CANTIDADES'),
            ('familia',                'FAMILIA'),
            ('cuerpo_humano',          'CUERPO_HUMANO'),
            ('hogar',                  'HOGAR'),
            ('trabajo',                'TRABAJO'),
            ('salud',                  'SALUD'),
            ('dinero',                 'DINERO'),
            ('naturaleza',             'NATURALEZA'),
            ('entretenimiento',        'ENTRETENIMIENTO'),
            ('educacion',              'EDUCACION'),
            ('programacion',           'PROGRAMACION'),
            ('inteligencia_artificial','IA_ML'),
            ('filosofia_existencial',  'FILOSOFIA_EXISTENCIAL'),
            ('emociones_sebastian',    'EMOCIONES_SEBASTIAN'),
        ]
        total = 0
        for nombre_modulo, nombre_dict in modulos:
            cantidad = self._cargar_modulo(nombre_modulo, nombre_dict)
            total += cantidad

        self._cargado = True
        print(f'Vocabulario: {total} conceptos en {len(modulos)} módulos')

    def _cargar_modulo(self, nombre_modulo: str, nombre_dict: str) -> int:
        try:
            import importlib
            modulo = importlib.import_module(
                f'biblioteca.vocabulario.base.{nombre_modulo}'
            )
            diccionario = getattr(modulo, nombre_dict, {})
            for palabra, concepto in diccionario.items():
                self._agregar_concepto(palabra, concepto)
                # Registrar también todas las variantes
                for variante in concepto.get('variantes', []):
                    self._agregar_concepto(variante, concepto)
            return len(diccionario)
        except Exception as e:
            print(f'Vocabulario: error cargando {nombre_modulo} — {e}')
            return 0

    def _agregar_concepto(self, palabra: str, concepto: dict):
        palabra_lower = palabra.lower().strip()
        if not palabra_lower:
            return
        if palabra_lower in self._vocabulario:
            existente = self._vocabulario[palabra_lower]
            if concepto.get('grounding_base', 0) <= existente.get('grounding_base', 0):
                return
        self._vocabulario[palabra_lower] = concepto
        concepto_id = concepto.get('id', '')
        if concepto_id:
            if concepto_id not in self._indice_id:
                self._indice_id[concepto_id] = []
            if palabra_lower not in self._indice_id[concepto_id]:
                self._indice_id[concepto_id].append(palabra_lower)

    def buscar(self, palabra: str) -> Optional[dict]:
        if not palabra:
            return None
        resultado = self._vocabulario.get(palabra.lower().strip())
        if resultado:
            return resultado
        normalizada = self._normalizar(palabra)
        return self._vocabulario.get(normalizada)

    def buscar_multiples(self, palabras: List[str]) -> List[dict]:
        resultados = []
        for palabra in palabras:
            concepto = self.buscar(palabra)
            if concepto:
                resultados.append({'palabra': palabra, 'concepto': concepto})
        return resultados

    def buscar_frase(self, texto: str) -> List[dict]:
        if not texto:
            return []
        palabras = texto.lower().strip().split()
        resultados = []
        usadas = set()

        # Frases de 3 palabras
        for i in range(len(palabras) - 2):
            frase = f'{palabras[i]} {palabras[i+1]} {palabras[i+2]}'
            concepto = self.buscar(frase)
            if concepto:
                resultados.append({'palabra': frase, 'concepto': concepto})
                usadas.update([i, i+1, i+2])

        # Frases de 2 palabras
        for i in range(len(palabras) - 1):
            if i in usadas or i+1 in usadas:
                continue
            frase = f'{palabras[i]} {palabras[i+1]}'
            concepto = self.buscar(frase)
            if concepto:
                resultados.append({'palabra': frase, 'concepto': concepto})
                usadas.update([i, i+1])

        # Palabras individuales
        for i, palabra in enumerate(palabras):
            if i in usadas:
                continue
            concepto = self.buscar(palabra)
            if concepto:
                resultados.append({'palabra': palabra, 'concepto': concepto})
                usadas.add(i)

        return resultados

    def agregar_en_tiempo_real(
        self, palabra: str, concepto_id: str,
        grounding: float, tipo: str = 'concepto'
    ) -> bool:
        if not palabra or not concepto_id:
            return False
        self._agregar_concepto(palabra, {
            'id': concepto_id, 'grounding_base': grounding, 'tipo': tipo
        })
        return True

    def obtener_estadisticas(self) -> dict:
        return {
            'total_palabras':  len(self._vocabulario),
            'total_conceptos': len(self._indice_id),
            'cargado':         self._cargado,
        }

    @staticmethod
    def _normalizar(texto: str) -> str:
        reemplazos = {
            'á':'a','é':'e','í':'i','ó':'o','ú':'u',
            'Á':'a','É':'e','Í':'i','Ó':'o','Ú':'u',
            'ü':'u','ñ':'n','Ñ':'n',
        }
        resultado = texto.lower().strip()
        for orig, rep in reemplazos.items():
            resultado = resultado.replace(orig, rep)
        return resultado