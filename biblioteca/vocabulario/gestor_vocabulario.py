# biblioteca/vocabulario/gestor_vocabulario.py
# ================================================
# GESTOR DE VOCABULARIO
# Punto de entrada único para todo el vocabulario
# Carga todos los módulos base automáticamente
# Permite agregar vocabulario nuevo en tiempo real
# ================================================

from typing import Optional, Dict, List


class GestorVocabulario:
    """
    Gestiona todo el vocabulario de Belladonna.
    Singleton — una sola instancia.

    Principio de escalabilidad:
    Agregar un nuevo módulo de vocabulario =
    crear el archivo en base/ y registrarlo aquí.
    Nada más.
    """

    _instancia = None

    def __init__(self):
        self._vocabulario: Dict[str, dict] = {}
        self._indice_id: Dict[str, List[str]] = {}
        self._cargado = False

    @classmethod
    def obtener(cls) -> 'GestorVocabulario':
        if cls._instancia is None:
            cls._instancia = cls()
            cls._instancia.cargar_todo()
        return cls._instancia

    def cargar_todo(self):
        """
        Carga todos los módulos de vocabulario base.
        El orden no importa — no hay dependencias.
        """
        modulos = [
            ('saludos',        'SALUDOS'),
            ('verbos_comunes', 'VERBOS_COMUNES'),
            ('preguntas',      'PREGUNTAS'),
            ('emociones',      'EMOCIONES'),
            ('tiempo',         'TIEMPO'),
            ('conectores',     'CONECTORES'),
        ]

        total = 0
        for nombre_modulo, nombre_dict in modulos:
            cantidad = self._cargar_modulo(nombre_modulo, nombre_dict)
            total += cantidad

        self._cargado = True
        print(f'Vocabulario cargado: {total} palabras en {len(modulos)} módulos')

    def _cargar_modulo(self, nombre_modulo: str, nombre_dict: str) -> int:
        """
        Carga un módulo de vocabulario.
        Si falla no rompe el sistema.
        """
        try:
            import importlib
            modulo = importlib.import_module(
                f'biblioteca.vocabulario.base.{nombre_modulo}'
            )
            diccionario = getattr(modulo, nombre_dict, {})

            for palabra, concepto in diccionario.items():
                self._agregar_concepto(palabra, concepto)

            return len(diccionario)

        except Exception as e:
            print(f'Vocabulario: error cargando {nombre_modulo} — {e}')
            return 0

    def _agregar_concepto(self, palabra: str, concepto: dict):
        """
        Agrega un concepto al vocabulario.
        Si la palabra ya existe mantiene el de mayor grounding.
        """
        palabra_lower = palabra.lower().strip()

        if palabra_lower in self._vocabulario:
            existente = self._vocabulario[palabra_lower]
            if concepto.get('grounding', 0) <= existente.get('grounding', 0):
                return

        self._vocabulario[palabra_lower] = concepto

        # Actualizar índice por ID
        concepto_id = concepto.get('id', '')
        if concepto_id:
            if concepto_id not in self._indice_id:
                self._indice_id[concepto_id] = []
            if palabra_lower not in self._indice_id[concepto_id]:
                self._indice_id[concepto_id].append(palabra_lower)

    def buscar(self, palabra: str) -> Optional[dict]:
        """
        Busca un concepto por palabra.
        Intenta exacto primero, luego normalizado.
        """
        if not palabra:
            return None

        # Búsqueda exacta
        resultado = self._vocabulario.get(palabra.lower().strip())
        if resultado:
            return resultado

        # Búsqueda sin tildes
        normalizada = self._normalizar(palabra)
        resultado = self._vocabulario.get(normalizada)
        if resultado:
            return resultado

        return None

    def buscar_multiples(self, palabras: List[str]) -> List[dict]:
        """
        Busca múltiples palabras y retorna
        los conceptos encontrados.
        """
        resultados = []
        for palabra in palabras:
            concepto = self.buscar(palabra)
            if concepto:
                resultados.append({
                    'palabra': palabra,
                    'concepto': concepto
                })
        return resultados

    def buscar_frase(self, texto: str) -> List[dict]:
        """
        Busca en un texto completo.
        Intenta primero frases de 3 palabras,
        luego 2, luego 1 — para capturar
        frases compuestas como "por qué".
        """
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
        self,
        palabra: str,
        concepto_id: str,
        grounding: float,
        tipo: str = 'concepto'
    ) -> bool:
        """
        Agrega una palabra nueva al vocabulario
        en tiempo real sin reiniciar Bell.
        """
        if not palabra or not concepto_id:
            return False

        self._agregar_concepto(palabra, {
            'id':       concepto_id,
            'grounding': grounding,
            'tipo':     tipo
        })
        return True

    def obtener_estadisticas(self) -> dict:
        return {
            'total_palabras': len(self._vocabulario),
            'total_conceptos': len(self._indice_id),
            'cargado':        self._cargado
        }

    @staticmethod
    def _normalizar(texto: str) -> str:
        """Elimina tildes para búsqueda flexible."""
        reemplazos = {
            'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
            'Á': 'a', 'É': 'e', 'Í': 'i', 'Ó': 'o', 'Ú': 'u',
            'ü': 'u', 'ñ': 'n', 'Ñ': 'n'
        }
        resultado = texto.lower().strip()
        for original, reemplazo in reemplazos.items():
            resultado = resultado.replace(original, reemplazo)
        return resultado