# capas/capa7/detector_habilidad.py
# ================================================
# DETECTOR DE HABILIDAD — Capa 7
#
# ARQUITECTURA CORRECTA:
# La habilidad de lenguaje vive en Capa 6, no aquí.
# Capa 7 solo detecta habilidades de EJECUCIÓN:
# cálculo, base de datos, shell, código.
#
# "hola", "cómo estás", "quién eres" → no necesitan
# ninguna habilidad en Capa 7. Capa 6 ya los maneja.
# ================================================

import re

HABILIDADES = {
    'CALCULO': {
        'disponible':  False,
        'descripcion': 'Cálculo matemático con SymPy',
        'patrones': [
            r'\bcalcula\b', r'\bcuánto\s+es\b', r'\bcuanto\s+es\b',
            r'\bresuelve\b', r'\bintegral\b', r'\bderivada\b',
            r'\braíz\s+de\b', r'\braiz\s+de\b', r'\bpotencia\b',
            r'\bmultiplica\b', r'\bdivide\b',
            r'\b\d+\s*[\+\-\*\/\^]\s*\d+\b',
            r'\bpromedio\b', r'\bdesviaci[oó]n\b',
            r'\bfactorial\b', r'\blogaritmo\b',
            r'\bcu[aá]nto\s+(?:da|vale|son)\b',
            r'\b\d+\s*%\s+de\b',
        ],
    },
    'ANALISIS_PYTHON': {
        'disponible':  False,
        'descripcion': 'Análisis de código Python',
        'patrones': [
            r'\banaliza\s+este\s+c[oó]digo\b',
            r'\banaliza\s+el\s+c[oó]digo\b',
            r'\brevisame\s+el\s+c[oó]digo\b',
            r'\bqu[eé]\s+hace\s+este\s+c[oó]digo\b',
            r'\berrors?\s+en\s+el\s+c[oó]digo\b',
            r'\bdef\s+\w+\(\s*\)',
            r'\bclass\s+\w+\s*[:\(]',
        ],
    },
    'SHELL': {
        'disponible':  False,
        'descripcion': 'Comandos del sistema operativo',
        'patrones': [
            r'\bejecuta\s+(?:el\s+)?comando\b',
            r'\bcorre\s+el\s+comando\b',
            r'\blistar?\s+archivos\b',
            r'\b(?:ls|dir|pwd|mkdir|rmdir|rm|cp|mv|cat|grep|find)\b',
            r'\bgit\s+(?:init|add|commit|push|pull|clone|status)\b',
            r'\bnpm\s+(?:install|start|run|build|test)\b',
            r'\bpip\s+install\b',
        ],
    },
    'SQLITE': {
        'disponible':  False,
        'descripcion': 'Base de datos SQLite',
        'patrones': [
            r'\bbase\s+de\s+datos\b',
            r'\bcrea\s+(?:una?\s+)?tabla\b',
            r'\bguarda\s+(?:en|esto|eso)\b',
            r'\binserta\s+(?:en\s+)?\b',
            r'\bconsulta\s+(?:la\s+)?(?:base|tabla)\b',
            r'\b(?:select|insert|update|delete|create\s+table|drop\s+table)\b',
            r'\bpon\s+(?:en\s+)?(?:la\s+)?(?:base|tabla)\b',
        ],
    },
}


class DetectorHabilidad:

    def detectar(self, texto: str, decision_final: dict) -> dict:
        """
        Detecta si el mensaje necesita ejecutar una habilidad real.
        Mensajes conversacionales no necesitan ninguna habilidad aquí
        — Capa 6 ya los manejó.
        """
        texto_lower = texto.lower().strip()

        for habilidad_id, config in HABILIDADES.items():
            for patron in config['patrones']:
                if re.search(patron, texto_lower, re.IGNORECASE):
                    return {
                        'necesita_habilidad': True,
                        'habilidad_id':       habilidad_id,
                        'disponible':         config['disponible'],
                        'descripcion':        config['descripcion'],
                        'texto_original':     texto,
                    }

        return {
            'necesita_habilidad': False,
            'habilidad_id':       None,
            'disponible':         False,
            'descripcion':        '',
            'texto_original':     texto,
        }

    def estado(self) -> dict:
        return {
            hid: {
                'disponible':  cfg['disponible'],
                'descripcion': cfg['descripcion'],
                'n_patrones':  len(cfg.get('patrones', [])),
            }
            for hid, cfg in HABILIDADES.items()
        }