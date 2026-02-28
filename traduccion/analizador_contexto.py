"""
Analizador de Contexto - Detecta el tipo de frase y contexto.

DETECTA:
- ¿Es pregunta? (¿, qué, cómo, etc.)
- ¿Es comando? (imperativo: "lista", "muestra")
- ¿Es técnico? (shell, código, archivo, etc.)
- ¿Es conversacional? (necesito, quiero, creo, etc.)
"""

from typing import Dict, List
import re


class AnalizadorContexto:
    """
    Analiza contexto lingüístico de una frase.
    
    Retorna metadata útil para selección de conceptos.
    """
    
    # Palabras interrogativas
    PALABRAS_PREGUNTA = {
        'qué', 'que', 'cómo', 'como', 'cuándo', 'cuando',
        'dónde', 'donde', 'quién', 'quien', 'por qué', 'porque',
        'cuál', 'cual', 'cuánto', 'cuanto'
    }
    
    # Palabras técnicas (shell/código)
    PALABRAS_TECNICAS = {
        'archivo', 'directorio', 'carpeta', 'comando', 'ejecutar',
        'shell', 'terminal', 'consola', 'script', 'código',
        'python', 'bash', 'linux', 'sistema', 'proceso',
        'función', 'clase', 'variable', 'módulo', 'importar',
        'compilar', 'debug', 'error', 'log', 'base de datos'
    }
    
    # Palabras conversacionales
    PALABRAS_CONVERSACIONALES = {
        'necesito', 'quiero', 'puedo', 'debo', 'creo',
        'pienso', 'siento', 'parece', 'probablemente', 'tal vez',
        'me gustaría', 'quisiera', 'podrías', 'deberías',
        'hola', 'gracias', 'por favor', 'disculpa', 'perdón'
    }
    
    # Verbos imperativos comunes
    VERBOS_COMANDO = {
        'lista', 'muestra', 'crea', 'elimina', 'modifica',
        'busca', 'encuentra', 'abre', 'cierra', 'guarda',
        'carga', 'descarga', 'instala', 'ejecuta', 'corre'
    }
    
    def analizar(self, texto: str) -> Dict:
        """
        Analiza contexto de una frase.
        
        Args:
            texto: Frase a analizar
        
        Returns:
            Dict con metadata contextual:
            {
                'es_pregunta': bool,
                'es_comando': bool,
                'es_tecnico': bool,
                'es_conversacional': bool,
                'palabras_clave': List[str],
                'nivel_confianza': float
            }
        """
        texto_lower = texto.lower()
        palabras = self._tokenizar(texto_lower)
        
        # Detectar tipo
        es_pregunta = self._es_pregunta(texto_lower, palabras)
        es_comando = self._es_comando(palabras)
        es_tecnico = self._es_tecnico(palabras)
        es_conversacional = self._es_conversacional(palabras)
        
        # Extraer palabras clave
        palabras_clave = self._extraer_keywords(palabras)
        
        # Calcular confianza
        nivel_confianza = self._calcular_confianza(
            es_pregunta, es_comando, es_tecnico, es_conversacional
        )
        
        return {
            'es_pregunta': es_pregunta,
            'es_comando': es_comando,
            'es_tecnico': es_tecnico,
            'es_conversacional': es_conversacional,
            'palabras_clave': palabras_clave,
            'nivel_confianza': nivel_confianza,
            'texto_original': texto
        }
    
    def _tokenizar(self, texto: str) -> List[str]:
        """Divide texto en palabras."""
        # Remover puntuación excepto ¿?
        texto = re.sub(r'[^\w\s¿?]', ' ', texto)
        return [p for p in texto.split() if p]
    
    def _es_pregunta(self, texto: str, palabras: List[str]) -> bool:
        """Detecta si es pregunta."""
        # Tiene signos de interrogación
        if '?' in texto or '¿' in texto:
            return True
        
        # Empieza con palabra interrogativa
        if palabras and palabras[0] in self.PALABRAS_PREGUNTA:
            return True
        
        # Contiene palabras interrogativas
        for palabra in palabras:
            if palabra in self.PALABRAS_PREGUNTA:
                return True
        
        return False
    
    def _es_comando(self, palabras: List[str]) -> bool:
        """Detecta si es comando/imperativo."""
        if not palabras:
            return False
        
        # Primera palabra es verbo imperativo
        primera = palabras[0]
        return primera in self.VERBOS_COMANDO
    
    def _es_tecnico(self, palabras: List[str]) -> bool:
        """Detecta si tiene contexto técnico."""
        contador = sum(
            1 for palabra in palabras
            if palabra in self.PALABRAS_TECNICAS
        )
        # Si tiene 2+ palabras técnicas, es contexto técnico
        return contador >= 2 or (
            contador >= 1 and len(palabras) <= 4
        )
    
    def _es_conversacional(self, palabras: List[str]) -> bool:
        """Detecta si es conversacional."""
        return any(
            palabra in self.PALABRAS_CONVERSACIONALES
            for palabra in palabras
        )
    
    def _extraer_keywords(self, palabras: List[str]) -> List[str]:
        """Extrae palabras clave importantes."""
        keywords = []
        
        for palabra in palabras:
            if (palabra in self.PALABRAS_TECNICAS or
                palabra in self.PALABRAS_CONVERSACIONALES or
                palabra in self.VERBOS_COMANDO):
                keywords.append(palabra)
        
        return keywords
    
    def _calcular_confianza(
        self,
        es_pregunta: bool,
        es_comando: bool,
        es_tecnico: bool,
        es_conversacional: bool
    ) -> float:
        """Calcula nivel de confianza del análisis."""
        # Si tiene clasificación clara, confianza alta
        tipos_detectados = sum([
            es_pregunta, es_comando,
            es_tecnico, es_conversacional
        ])
        
        if tipos_detectados == 0:
            return 0.3  # Baja confianza
        elif tipos_detectados == 1:
            return 0.9  # Alta confianza
        elif tipos_detectados == 2:
            return 0.7  # Media-alta
        else:
            return 0.5  # Media (ambiguo)


# TESTS
if __name__ == '__main__':
    print("🧪 Test de AnalizadorContexto")
    print("=" * 60)
    
    analizador = AnalizadorContexto()
    
    tests = [
        ("¿cómo estas?", {
            'es_pregunta': True,
            'es_conversacional': True
        }),
        ("lista archivos en directorio", {
            'es_comando': True,
            'es_tecnico': True
        }),
        ("buscar en archivo log.txt", {
            'es_tecnico': True
        }),
        ("necesito buscar información", {
            'es_conversacional': True
        }),
        ("hola, ¿qué puedes hacer?", {
            'es_pregunta': True,
            'es_conversacional': True
        })
    ]
    
    for texto, esperado in tests:
        print(f"\nTEST: '{texto}'")
        resultado = analizador.analizar(texto)
        
        print(f"  Pregunta: {resultado['es_pregunta']}")
        print(f"  Comando: {resultado['es_comando']}")
        print(f"  Técnico: {resultado['es_tecnico']}")
        print(f"  Conversacional: {resultado['es_conversacional']}")
        print(f"  Keywords: {resultado['palabras_clave']}")
        print(f"  Confianza: {resultado['nivel_confianza']:.2f}")
        
        # Verificar esperado
        ok = all(
            resultado[key] == value
            for key, value in esperado.items()
        )
        print(f"  {'✅ CORRECTO' if ok else '❌ ERROR'}")
    
    print("\n" + "=" * 60)
    print("✅ Tests completados")