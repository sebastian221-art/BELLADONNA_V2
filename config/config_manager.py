"""
Gestor de Configuración ULTRA COMPLETO - Fase 4A

Carga configuración desde .env y archivos JSON.
Soporta todas las opciones de Groq, seguridad, logs y prompts.
"""
import os
import json
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime


# Configuración por defecto (basada en el JSON proporcionado)
_CONFIG_DEFAULT = {
    "api": {
        "modelo": "llama-3.3-70b-versatile",
        "temperatura": 0.3,
        "max_tokens": 500,
        "timeout": 10,
        "retry_intentos": 3,
        "retry_delay": 1
    },
    "seguridad": {
        "verificar_con_echo": True,
        "bloquear_en_duda": True,
        "nivel_confianza_minimo": 0.7
    },
    "logs": {
        "guardar_interacciones": True,
        "ruta_logs": "logs/fase4a/groq_interactions.jsonl",
        "guardar_errores": True,
        "ruta_errores": "logs/fase4a/groq_errors.jsonl"
    },
    "optimizacion": {
        "cache_respuestas": False,
        "max_cache_size": 100,
        "cache_ttl_seconds": 3600
    },
    "prompts": {
        "usar_prompts_naturales": True,
        "evitar_frases_roboticas": [
            "soy un sistema de software",
            "no tengo la capacidad de",
            "soy un programa de computadora",
            "no puedo porque soy software",
            "como inteligencia artificial",
            "mi programación no permite",
            "estoy diseñada para",
            "mi función es"
        ],
        "preferir_frases_naturales": [
            "no tengo acceso a",
            "eso está fuera de mi alcance",
            "no puedo hacer eso porque",
            "mis capacidades se limitan a",
            "claro que sí",
            "por supuesto",
            "con mucho gusto",
            "déjame ver"
        ]
    },
    "contexto": {
        "usar_traductor_contextual": True,
        "resolver_duplicados": True,
        "analizar_antes_de_traducir": True,
        "detectar_emociones": True,
        "ajustar_tono": True
    },
    "vocabulario": {
        "cargar_expansion": True,
        "usar_conceptos_relacionados": True,
        "max_conceptos_por_respuesta": 10
    }
}


class ConfigManager:
    """
    Administra TODA la configuración de Bell para Fase 4A.
    
    Fuentes de configuración (en orden de prioridad):
    1. Variables de entorno
    2. Archivo .env
    3. Archivo config.json
    4. Valores por defecto
    """
    
    def __init__(
        self, 
        env_path: Optional[Path] = None,
        config_json_path: Optional[Path] = None
    ):
        """
        Inicializa gestor de configuración.
        
        Args:
            env_path: Ruta al archivo .env
            config_json_path: Ruta al archivo config.json
        """
        self.proyecto_root = Path(__file__).parent.parent
        self.env_path = env_path or self.proyecto_root / ".env"
        self.config_json_path = config_json_path or self.proyecto_root / "config" / "groq_config.json"
        
        # Inicializar con defaults
        self.config = _CONFIG_DEFAULT.copy()
        
        # Cargar configuraciones
        self._cargar_json()
        self._cargar_env()
    
    def _cargar_json(self):
        """Carga configuración desde archivo JSON."""
        if self.config_json_path.exists():
            try:
                with open(self.config_json_path, 'r', encoding='utf-8') as f:
                    config_json = json.load(f)
                    self._merge_config(config_json)
                print(f"✅ Configuración JSON cargada: {self.config_json_path}")
            except Exception as e:
                print(f"⚠️  Error cargando JSON: {e}")
    
    def _cargar_env(self):
        """Carga variables del archivo .env."""
        if not self.env_path.exists():
            print(f"⚠️  Archivo .env no encontrado en: {self.env_path}")
            return
        
        with open(self.env_path, 'r', encoding='utf-8') as f:
            for linea in f:
                linea = linea.strip()
                
                if not linea or linea.startswith('#'):
                    continue
                
                if '=' in linea:
                    key, value = linea.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Remover comillas
                    if (value.startswith('"') and value.endswith('"')) or \
                       (value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]
                    
                    os.environ[key] = value
        
        print(f"✅ Variables .env cargadas: {self.env_path}")
    
    def _merge_config(self, nuevo: Dict):
        """Mezcla configuración nueva con existente (recursivo)."""
        def merge_dict(base: Dict, update: Dict):
            for key, value in update.items():
                if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                    merge_dict(base[key], value)
                else:
                    base[key] = value
        
        merge_dict(self.config, nuevo)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # GETTERS BÁSICOS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def get(self, key: str, default: Any = None) -> Any:
        """Obtiene valor de configuración (soporta notación de punto)."""
        # Primero buscar en variables de entorno
        env_value = os.getenv(key.upper().replace('.', '_'))
        if env_value is not None:
            return env_value
        
        # Luego buscar en config
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """Obtiene valor booleano."""
        value = self.get(key)
        if value is None:
            return default
        if isinstance(value, bool):
            return value
        return str(value).lower() in ('true', '1', 'yes', 'on')
    
    def get_int(self, key: str, default: int = 0) -> int:
        """Obtiene valor entero."""
        value = self.get(key)
        if value is None:
            return default
        try:
            return int(value)
        except (ValueError, TypeError):
            return default
    
    def get_float(self, key: str, default: float = 0.0) -> float:
        """Obtiene valor flotante."""
        value = self.get(key)
        if value is None:
            return default
        try:
            return float(value)
        except (ValueError, TypeError):
            return default
    
    def get_list(self, key: str, default: list = None) -> list:
        """Obtiene valor de lista."""
        value = self.get(key)
        if value is None:
            return default or []
        if isinstance(value, list):
            return value
        return [value]
    
    # ═══════════════════════════════════════════════════════════════════════════
    # GETTERS ESPECÍFICOS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def get_groq_config(self) -> Dict:
        """Obtiene configuración completa de Groq."""
        api_config = self.config.get("api", {})
        prompts_config = self.config.get("prompts", {})
        
        return {
            # API
            "api_key": os.getenv("GROQ_API_KEY"),
            "model": os.getenv("GROQ_MODEL", api_config.get("modelo", "llama-3.3-70b-versatile")),
            "temperature": self.get_float("GROQ_TEMPERATURE", api_config.get("temperatura", 0.3)),
            "max_tokens": self.get_int("GROQ_MAX_TOKENS", api_config.get("max_tokens", 500)),
            "timeout": self.get_int("GROQ_TIMEOUT", api_config.get("timeout", 10)),
            "retry_intentos": api_config.get("retry_intentos", 3),
            "retry_delay": api_config.get("retry_delay", 1),
            
            # Prompts
            "usar_prompts_naturales": prompts_config.get("usar_prompts_naturales", True),
            "evitar_frases_roboticas": prompts_config.get("evitar_frases_roboticas", []),
            "preferir_frases_naturales": prompts_config.get("preferir_frases_naturales", []),
        }
    
    def get_seguridad_config(self) -> Dict:
        """Obtiene configuración de seguridad."""
        return self.config.get("seguridad", {})
    
    def get_logs_config(self) -> Dict:
        """Obtiene configuración de logs."""
        return self.config.get("logs", {})
    
    def get_contexto_config(self) -> Dict:
        """Obtiene configuración de contexto."""
        return self.config.get("contexto", {})
    
    def get_vocabulario_config(self) -> Dict:
        """Obtiene configuración de vocabulario."""
        return self.config.get("vocabulario", {})
    
    # ═══════════════════════════════════════════════════════════════════════════
    # VALIDACIÓN
    # ═══════════════════════════════════════════════════════════════════════════
    
    def validar_config(self) -> Dict[str, Any]:
        """
        Valida que la configuración esté completa.
        
        Returns:
            Dict con 'valido' (bool) y 'errores' (list)
        """
        errores = []
        advertencias = []
        
        # Verificar GROQ_API_KEY
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key or api_key == "tu_api_key_aqui":
            errores.append("GROQ_API_KEY no configurada")
        
        # Verificar modelo
        modelo = self.get("api.modelo")
        modelos_validos = [
            "llama-3.3-70b-versatile",
            "llama-3.1-70b-versatile",
            "mixtral-8x7b-32768",
        ]
        if modelo not in modelos_validos:
            advertencias.append(f"Modelo '{modelo}' no reconocido")
        
        # Verificar directorios de logs
        logs_config = self.get_logs_config()
        if logs_config.get("guardar_interacciones"):
            ruta_logs = Path(logs_config.get("ruta_logs", "logs/"))
            ruta_logs.parent.mkdir(parents=True, exist_ok=True)
        
        # Verificar whitelist
        whitelist_path = self.proyecto_root / "data" / "BELL_WHITELIST.json"
        if not whitelist_path.exists():
            advertencias.append(f"Whitelist no encontrada: {whitelist_path}")
        
        return {
            'valido': len(errores) == 0,
            'errores': errores,
            'advertencias': advertencias,
        }
    
    # ═══════════════════════════════════════════════════════════════════════════
    # UTILIDADES
    # ═══════════════════════════════════════════════════════════════════════════
    
    def guardar_config_json(self, path: Optional[Path] = None):
        """Guarda configuración actual a JSON."""
        path = path or self.config_json_path
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Configuración guardada: {path}")
    
    def mostrar_config(self):
        """Muestra configuración actual formateada."""
        groq_config = self.get_groq_config()
        seg_config = self.get_seguridad_config()
        ctx_config = self.get_contexto_config()
        vocab_config = self.get_vocabulario_config()
        
        print()
        print("=" * 70)
        print("CONFIGURACIÓN DE BELLADONNA - FASE 4A COMPLETA")
        print("=" * 70)
        print(f"Proyecto root: {self.proyecto_root}")
        print(f"Archivo .env: {self.env_path}")
        print(f"Archivo JSON: {self.config_json_path}")
        
        print("\n📡 GROQ API:")
        print(f"  API Key: {'✅ Configurada' if groq_config['api_key'] else '❌ No configurada'}")
        print(f"  Modelo: {groq_config['model']}")
        print(f"  Temperatura: {groq_config['temperature']}")
        print(f"  Max Tokens: {groq_config['max_tokens']}")
        print(f"  Timeout: {groq_config['timeout']}s")
        print(f"  Prompts naturales: {'✅' if groq_config['usar_prompts_naturales'] else '❌'}")
        
        print("\n🔒 SEGURIDAD:")
        print(f"  Verificar con Echo: {'✅' if seg_config.get('verificar_con_echo') else '❌'}")
        print(f"  Bloquear en duda: {'✅' if seg_config.get('bloquear_en_duda') else '❌'}")
        print(f"  Confianza mínima: {seg_config.get('nivel_confianza_minimo', 0.7)}")
        
        print("\n🎯 CONTEXTO:")
        print(f"  Traductor contextual: {'✅' if ctx_config.get('usar_traductor_contextual') else '❌'}")
        print(f"  Detectar emociones: {'✅' if ctx_config.get('detectar_emociones') else '❌'}")
        print(f"  Ajustar tono: {'✅' if ctx_config.get('ajustar_tono') else '❌'}")
        
        print("\n📚 VOCABULARIO:")
        print(f"  Cargar expansión: {'✅' if vocab_config.get('cargar_expansion') else '❌'}")
        print(f"  Usar conceptos relacionados: {'✅' if vocab_config.get('usar_conceptos_relacionados') else '❌'}")
        
        # Validación
        validacion = self.validar_config()
        print("\n" + "=" * 70)
        if validacion['valido']:
            print("✅ CONFIGURACIÓN VÁLIDA")
        else:
            print("❌ ERRORES DE CONFIGURACIÓN:")
            for error in validacion['errores']:
                print(f"   - {error}")
        
        if validacion['advertencias']:
            print("⚠️  ADVERTENCIAS:")
            for adv in validacion['advertencias']:
                print(f"   - {adv}")
        
        print("=" * 70)


# ═══════════════════════════════════════════════════════════════════════════════
# INSTANCIA GLOBAL (SINGLETON)
# ═══════════════════════════════════════════════════════════════════════════════

_config_manager = None


def get_config() -> ConfigManager:
    """Obtiene instancia global del gestor de configuración."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager


def reset_config():
    """Resetea instancia global (útil para testing)."""
    global _config_manager
    _config_manager = None


# ═══════════════════════════════════════════════════════════════════════════════
# TEST
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    config = ConfigManager()
    config.mostrar_config()
    
    print("\n🧪 Test de getters:")
    print(f"  api.modelo: {config.get('api.modelo')}")
    print(f"  api.temperatura: {config.get('api.temperatura')}")
    print(f"  seguridad.verificar_con_echo: {config.get_bool('seguridad.verificar_con_echo')}")
    print(f"  prompts.evitar_frases_roboticas: {config.get_list('prompts.evitar_frases_roboticas')[:3]}...")