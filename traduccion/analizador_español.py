"""
Analizador de Español - Semana 2.

Analiza texto en español usando spaCy para extraer información lingüística.
Bell NO entiende semántica, solo procesa estructura lingüística.
"""
import spacy
from typing import Dict, List

class AnalizadorEspañol:
    """
    Analiza texto en español y extrae información estructural.
    
    NO es IA mágica. Es análisis lingüístico determinista.
    """
    
    def __init__(self):
        """Inicializa el analizador con modelo spaCy."""
        try:
            self.nlp = spacy.load("es_core_news_sm")
        except OSError:
            print("ERROR: Modelo spaCy no encontrado.")
            print("Ejecuta: python -m spacy download es_core_news_sm")
            raise
    
    def analizar(self, texto: str) -> Dict:
        """
        Analiza texto y retorna información estructurada.
        
        Returns:
            {
                'texto_original': str,
                'tokens': List[str],           # Palabras separadas
                'lemas': List[str],            # Formas base
                'pos_tags': List[str],         # Categorías gramaticales
                'verbos': List[str],           # Verbos detectados
                'sustantivos': List[str],      # Sustantivos
                'es_pregunta': bool,           # ¿Tiene "?"?
                'longitud': int                # Número de tokens
            }
        """
        # Procesar con spaCy
        doc = self.nlp(texto)
        
        # Extraer tokens (palabras significativas)
        tokens = [token.text for token in doc if not token.is_punct]
        
        # Lematización (forma base de palabras)
        lemas = [token.lemma_.lower() for token in doc if not token.is_punct]
        
        # POS tags (Part Of Speech - categoría gramatical)
        pos_tags = [token.pos_ for token in doc if not token.is_punct]
        
        # Verbos (IMPORTANTE: incluir AUX para verbos auxiliares como "puedes")
        verbos = [token.lemma_.lower() for token in doc 
                 if token.pos_ in ['VERB', 'AUX']]  # ← CORREGIDO
        
        # Sustantivos
        sustantivos = [token.lemma_.lower() for token in doc 
                      if token.pos_ in ['NOUN', 'PROPN']]
        
        # Detectar pregunta (simple: busca "?")
        es_pregunta = '?' in texto
        
        return {
            'texto_original': texto,
            'tokens': tokens,
            'lemas': lemas,
            'pos_tags': pos_tags,
            'verbos': verbos,
            'sustantivos': sustantivos,
            'es_pregunta': es_pregunta,
            'longitud': len(tokens)
        }
    
    def es_frase_simple(self, analisis: Dict) -> bool:
        """¿Es una frase simple? (menos de 10 palabras)"""
        return analisis['longitud'] < 10
    
    def tiene_verbo(self, analisis: Dict) -> bool:
        """¿La frase tiene al menos un verbo?"""
        return len(analisis['verbos']) > 0
    
    def palabras_clave(self, analisis: Dict) -> List[str]:
        """
        Extrae palabras clave (verbos + sustantivos).
        
        Estas son las palabras más importantes para mapear a conceptos.
        """
        return analisis['verbos'] + analisis['sustantivos']