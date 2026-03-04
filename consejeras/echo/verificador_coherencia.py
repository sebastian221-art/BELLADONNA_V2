"""
Verificador de Coherencia - Echo (VERSIÓN FINAL FUSIONADA)
Integra 100% verificador original Bell + capacidades Groq Fase 4A.

Este archivo reemplaza verificador_coherencia.py y verificador_coherencia_v2.py
"""

import re
from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass
from pathlib import Path
import json


@dataclass
class ResultadoVerificacion:
    """Resultado completo de verificación."""
    es_coherente: bool
    violaciones: List[str]
    confianza: float
    accion_recomendada: str
    respuesta_corregida: Optional[str] = None
    fue_corregida: bool = False


class VerificadorCoherenciaEcho:
    """Verificador fusionado: Bell original (6 verificaciones) + Groq (4 verificaciones)."""
    
    def __init__(self, whitelist_path: Optional[Path] = None):
        # Whitelist para Groq
        self.whitelist = self._cargar_whitelist(whitelist_path)
        self.verbos_accion = self._extraer_verbos_accion()
        
        # Patrones peligrosos (Bell + Groq)
        self.patrones_peligrosos = [
            r"puedo\s+(volar|navegar internet|enviar emails|acceder a la web)",
            r"tengo\s+(acceso a|conexión con)\s+(internet|la nube)",
            r"puedo\s+(ver|mirar)\s+tu\s+c[aá]mara",
            r"estoy\s+(viendo|mirando)\s+tu\s+pantalla",
            r"he\s+accedido\s+a\s+internet",
            r"te enviaré", r"te llamaré", r"publicaré en",
            # FIX Fase 4A: afirmaciones falsas de capacidades de archivo
            r"puedo\s+(crear|escribir|leer|modificar|editar)\s+(archivos?|ficheros?)",
            r"puedo\s+(acceder|leer)\s+(el\s+archivo|los\s+archivos|tu\s+archivo)",
            r"he\s+(creado|escrito|le[íi]do|modificado)\s+(el\s+archivo|un\s+archivo)",
            r"voy\s+a\s+(crear|escribir|leer)\s+(el\s+archivo|un\s+archivo)",
            r"claro,?\s+puedo\s+(crear|leer|escribir|manipular)\s+",
        ]
        
        # Basura del LLM (Bell)
        self.palabras_basura = [
            'números primos', 'cálculo diferencial', 'secuencia de conjuntos',
            'reflexión filosófica', 'dilema existencial',
            'confianza en el futuro', 'esperanza en la probabilidad',
        ]
        
        # Palabras esperadas por tipo (Bell)
        self.palabras_esperadas = {
            'SALUDO': ['hola', 'buenos', 'ayudarte'],
            'AGRADECIMIENTO': ['nada', 'para eso'],
            'DESPEDIDA': ['hasta', 'luego'],
            'CAPACIDAD': ['he', 'realizado', 'completado'],
            'RECHAZO': ['no puedo', 'lamento'],
        }
        
        self.estadisticas = {
            "total": 0, "correcciones": 0,
            "rechazos": 0, "aprobaciones": 0
        }
    
    def _cargar_whitelist(self, path):
        if path and path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"conceptos_permitidos": [], "verbos_permitidos": []}
    
    def _extraer_verbos_accion(self):
        verbos = set(self.whitelist.get("verbos_permitidos", []))
        for c in self.whitelist.get("conceptos_permitidos", []):
            if c.startswith("CONCEPTO_"):
                verbos.add(c.replace("CONCEPTO_", "").lower())
        return verbos
    
    # ========================================
    # MÉTODO PRINCIPAL FUSIONADO
    # ========================================
    
    def verificar(self, texto, decision, conceptos=None, grounding=None, contexto=None):
        """
        Verificación completa (Bell + Groq).
        
        Acepta tanto el formato original de Bell como el nuevo de Groq:
        - Bell: verificar(texto, decision, conceptos, grounding)
        - Groq: verificar(texto, decision)
        
        Returns:
            ResultadoVerificacion (nuevo) o Tuple[str, bool] (compatible con Bell)
        """
        self.estadisticas["total"] += 1
        
        violaciones = []
        confianza = 1.0
        respuesta = texto
        
        # 1. BASURA DEL LLM (Bell original)
        es_basura, razon = self._es_basura_llm(texto, decision)
        if es_basura:
            violaciones.append(f"Basura: {razon}")
            respuesta = self._generar_fallback(decision)
            confianza = 0.0
            self.estadisticas["rechazos"] += 1
        else:
            # 2. PATRONES SOSPECHOSOS (Groq)
            v = self._verificar_patrones(texto)
            if v:
                violaciones.extend(v)
                confianza -= 0.5
            
            # 3. COHERENCIA CON DECISIÓN (Groq)
            v = self._verificar_coherencia_decision(texto, decision)
            if v:
                violaciones.extend(v)
                confianza -= 0.4
            
            # 4. VERBOS DE ACCIÓN (Groq - solo si hay whitelist)
            if self.whitelist.get("conceptos_permitidos"):
                v = self._verificar_verbos_accion(texto, decision)
                if v:
                    violaciones.extend(v)
                    confianza -= 0.3
            
            # 5. CAPACIDADES (Bell)
            respuesta, c1 = self._verificar_capacidades(respuesta, conceptos or [])
            
            # 6. NÚMEROS (Bell)
            if grounding:
                respuesta, c2 = self._verificar_numeros(respuesta, grounding, decision)
            else:
                c2 = False
            
            # 7. PROMESAS (Bell)
            respuesta, c3 = self._verificar_promesas(respuesta, decision)
            
            # 8. LONGITUD (Bell)
            respuesta, c4 = self._verificar_longitud(respuesta, decision)
            
            # 9. CAVEATS (Bell)
            if grounding:
                respuesta, c5 = self._agregar_caveats(respuesta, grounding)
            else:
                c5 = False
            
            if c1 or c2 or c3 or c4 or c5:
                violaciones.append("Correcciones aplicadas")
                confianza -= 0.2
                self.estadisticas["correcciones"] += 1
        
        confianza = max(0.0, min(1.0, confianza))
        
        # Determinar acción
        if confianza < 0.3:
            accion = "BLOQUEAR"
            if not es_basura:
                self.estadisticas["rechazos"] += 1
        elif confianza < 0.7:
            accion = "ADVERTIR"
        else:
            accion = "PERMITIR"
            self.estadisticas["aprobaciones"] += 1
        
        es_coherente = len(violaciones) == 0
        fue_corregida = (respuesta != texto)
        
        return ResultadoVerificacion(
            es_coherente=es_coherente,
            violaciones=violaciones,
            confianza=confianza,
            accion_recomendada=accion,
            respuesta_corregida=respuesta if fue_corregida else None,
            fue_corregida=fue_corregida
        )
    
    # ========================================
    # VERIFICACIONES INDIVIDUALES
    # ========================================
    
    def _es_basura_llm(self, texto, decision):
        """Detecta basura del LLM (Bell original)."""
        tipo = self._get_tipo(decision)
        texto_l = texto.lower()
        
        # Palabras de basura
        for p in self.palabras_basura:
            if p in texto_l:
                return True, f"Contiene '{p}'"
        
        # Lista numerada sin contexto
        if re.match(r'^\d+[\.\-]', texto.strip()):
            if tipo not in ['AFIRMATIVA', 'EXPLICACION', 'CAPACIDAD']:
                return True, "Lista sin contexto"
        
        # Demasiadas listas
        if len(re.findall(r'\d+\.', texto)) > 4:
            return True, "Demasiadas listas"
        
        # No coherente con tipo esperado
        if tipo in self.palabras_esperadas:
            pals = self.palabras_esperadas[tipo]
            if not any(p in texto_l for p in pals) and len(texto) > 30:
                return True, f"No coherente con {tipo}"
        
        # Demasiado larga para tipo simple
        if tipo in ['SALUDO', 'AGRADECIMIENTO', 'DESPEDIDA']:
            if len(texto) > 150:
                return True, f"Muy larga para {tipo}"
        
        return False, ""
    
    def _verificar_patrones(self, texto):
        """Detecta patrones sospechosos (Groq)."""
        v = []
        for p in self.patrones_peligrosos:
            if re.search(p, texto, re.I):
                v.append(f"Patrón peligroso: {p}")
        return v
    
    def _verificar_coherencia_decision(self, texto, decision):
        """Verifica coherencia con decisión (Groq)."""
        v = []
        tipo = self._get_tipo(decision)
        capacidad = getattr(decision, 'capacidad', None) or getattr(decision, 'puede_ejecutar', False)
        
        # Si es rechazo pero texto indica éxito
        if not capacidad:
            if re.search(r"he\s+(realizado|completado)", texto.lower()):
                v.append("Indica éxito pero es rechazo")
        
        # Si es éxito pero texto indica fallo
        if capacidad:
            if re.search(r"no\s+puedo|imposible|error", texto.lower()):
                v.append("Indica fallo pero es éxito")
        
        return v
    
    def _verificar_verbos_accion(self, texto, decision):
        """Verifica verbos de acción (Groq)."""
        v = []
        verbos_texto = self._extraer_verbos_del_texto(texto)
        
        conceptos_usados = getattr(decision, 'conceptos_usados', [])
        verbos_permitidos = set()
        for c in conceptos_usados:
            if isinstance(c, str) and c.startswith("CONCEPTO_"):
                verbos_permitidos.add(c.replace("CONCEPTO_", "").lower())
        
        verbos_permitidos.update(self.verbos_accion)
        
        for verbo in verbos_texto:
            if verbo not in verbos_permitidos:
                if not self._es_sinonimo(verbo, verbos_permitidos):
                    v.append(f"Verbo '{verbo}' no autorizado")
        
        return v
    
    def _extraer_verbos_del_texto(self, texto):
        """Extrae verbos de primera persona."""
        verbos = set()
        patrones = [r"he\s+(\w+)", r"puedo\s+(\w+)", r"voy\s+a\s+(\w+)"]
        for p in patrones:
            for m in re.finditer(p, texto.lower()):
                verbos.add(m.group(1).rstrip('ndo'))
        return verbos
    
    def _es_sinonimo(self, verbo, permitidos):
        """Verifica sinónimos."""
        sinonimos = {
            "ver": ["leer", "listar"],
            "guardar": ["escribir"],
            "borrar": ["eliminar"],
        }
        for p in permitidos:
            if verbo in sinonimos.get(p, []) or p in sinonimos.get(verbo, []):
                return True
        return False
    
    def _verificar_capacidades(self, texto, conceptos):
        """Verifica capacidades inventadas (Bell)."""
        corr, cambios = texto, False
        for p in self.patrones_peligrosos:
            if re.search(p, texto, re.I):
                corr = re.sub(p, "NO puedo hacer eso", corr, flags=re.I)
                cambios = True
        return corr, cambios
    
    def _verificar_numeros(self, texto, grounding, decision):
        """Verifica números coherentes (Bell)."""
        corr, cambios = texto, False
        
        # Verificar grounding mencionado
        patron = r'grounding de (\d+\.?\d*)%?'
        matches = re.findall(patron, texto, re.I)
        
        if matches and grounding:
            promedio = sum(grounding.values()) / len(grounding)
            for m in matches:
                score = float(m) / 100 if float(m) > 1 else float(m)
                if abs(score - promedio) > 0.1:
                    corr = corr.replace(m, f"{promedio:.2f}")
                    cambios = True
        
        return corr, cambios
    
    def _verificar_promesas(self, texto, decision):
        """Verifica promesas (Bell)."""
        corr, cambios = texto, False
        promesas = ["te enviaré", "te llamaré", "publicaré", "subiré a la nube"]
        for p in promesas:
            if p in texto.lower():
                corr = corr.replace(p, "NO puedo hacer eso automáticamente")
                cambios = True
        return corr, cambios
    
    def _verificar_longitud(self, texto, decision):
        """Verifica longitud (Bell)."""
        tipo = self._get_tipo(decision)
        limites = {
            'SALUDO': 100, 'AGRADECIMIENTO': 80,
            'DESPEDIDA': 80, 'NEGATIVA': 150
        }
        limite = limites.get(tipo, 300)
        
        if len(texto) > limite:
            truncado = texto[:limite].rsplit(' ', 1)[0]
            if not truncado.endswith('.'):
                truncado += '.'
            return truncado, True
        return texto, False
    
    def _agregar_caveats(self, texto, grounding):
        """Agrega caveats si grounding bajo (Bell)."""
        if not grounding:
            return texto, False
        
        promedio = sum(grounding.values()) / len(grounding)
        if promedio < 0.5 and "puedo" in texto.lower():
            caveat = f"\n\n⚠️ Nota: Mi grounding es bajo ({int(promedio*100)}%)."
            return texto + caveat, True
        return texto, False
    
    def _generar_fallback(self, decision):
        """Genera fallback (Bell)."""
        tipo = self._get_tipo(decision)
        fallbacks = {
            'SALUDO': '¡Hola! ¿En qué puedo ayudarte?',
            'AGRADECIMIENTO': '¡De nada!',
            'CAPACIDAD': 'He realizado la operación.',
        }
        return fallbacks.get(tipo, 'Entendido.')
    
    def _get_tipo(self, decision):
        """Obtiene tipo de decisión (compatible Bell y Groq)."""
        if hasattr(decision, 'tipo'):
            tipo = decision.tipo
            return tipo.name if hasattr(tipo, 'name') else str(tipo)
        return getattr(decision, 'tipo', 'general')
    
    def obtener_estadisticas(self):
        t = self.estadisticas["total"]
        return {
            **self.estadisticas,
            "tasa_aprobacion": self.estadisticas["aprobaciones"]/t*100 if t else 0,
            "tasa_rechazo": self.estadisticas["rechazos"]/t*100 if t else 0
        }


# ===== TESTS =====
if __name__ == "__main__":
    print("🧪 Testing VerificadorCoherenciaEcho FUSIONADO COMPLETO\n")
    
    from types import SimpleNamespace
    
    verificador = VerificadorCoherenciaEcho()
    
    # Test 1: Basura del LLM (Bell)
    print("="*60)
    print("✅ Test 1: Basura del LLM (Bell original)")
    print("="*60)
    
    decision1 = SimpleNamespace(tipo=SimpleNamespace(name='SALUDO'), puede_ejecutar=False)
    texto_basura = "La lógica de los números primos es diferente."
    
    resultado = verificador.verificar(texto_basura, decision1, conceptos=[], grounding={'comp': 0.18})
    
    print(f"Original: {texto_basura}")
    print(f"Resultado: {resultado.respuesta_corregida or texto_basura}")
    print(f"Coherente: {resultado.es_coherente}")
    print(f"Confianza: {resultado.confianza}")
    print(f"Acción: {resultado.accion_recomendada}\n")
    
    # Test 2: Texto válido
    print("="*60)
    print("✅ Test 2: Texto válido (Bell)")
    print("="*60)
    
    texto_ok = "¡Hola! ¿En qué puedo ayudarte?"
    resultado2 = verificador.verificar(texto_ok, decision1)
    
    print(f"Original: {texto_ok}")
    print(f"Coherente: {resultado2.es_coherente}")
    print(f"Confianza: {resultado2.confianza}")
    print(f"Acción: {resultado2.accion_recomendada}\n")
    
    # Test 3: Alucinación Groq
    print("="*60)
    print("✅ Test 3: Alucinación de cámara (Groq)")
    print("="*60)
    
    texto_camara = "Puedo ver tu cámara y estás sonriendo."
    resultado3 = verificador.verificar(texto_camara, decision1)
    
    print(f"Original: {texto_camara}")
    print(f"Coherente: {resultado3.es_coherente}")
    print(f"Violaciones: {resultado3.violaciones}")
    print(f"Acción: {resultado3.accion_recomendada}\n")
    
    # Test 4: Capacidad inventada (Bell)
    print("="*60)
    print("✅ Test 4: Capacidad inventada (Bell original)")
    print("="*60)
    
    texto_email = "Claro, puedo navegar internet y enviarte emails."
    resultado4 = verificador.verificar(texto_email, decision1)
    
    print(f"Original: {texto_email}")
    print(f"Corregido: {resultado4.respuesta_corregida}")
    print(f"Fue corregida: {resultado4.fue_corregida}")
    print(f"Acción: {resultado4.accion_recomendada}\n")
    
    # Estadísticas
    print("="*60)
    print("📊 Estadísticas Finales")
    print("="*60)
    stats = verificador.obtener_estadisticas()
    for k, v in stats.items():
        print(f"  {k}: {v}")