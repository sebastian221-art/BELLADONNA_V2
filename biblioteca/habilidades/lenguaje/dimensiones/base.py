# biblioteca/habilidades/lenguaje/dimensiones/base.py
# ================================================
# BASE DE TODA DIMENSIÓN DE LENGUAJE
#
# Toda dimensión es una forma distinta de leer
# el mismo mensaje. El motor las ejecuta todas
# y construye la imagen completa.
#
# Agregar dimensión nueva = crear archivo en esta
# carpeta que herede DimensionLenguaje.
# No hay que tocar nada más.
# ================================================

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class ResultadoDimension:
    dimension:     str   = ''
    activa:        bool  = False
    confianza:     float = 0.0
    hallazgos:     dict  = field(default_factory=dict)
    senales:       list  = field(default_factory=list)
    peso_en_motor: float = 1.0

    def a_dict(self) -> dict:
        return {
            'dimension':     self.dimension,
            'activa':        self.activa,
            'confianza':     self.confianza,
            'hallazgos':     self.hallazgos,
            'senales':       self.senales,
            'peso_en_motor': self.peso_en_motor,
        }


class DimensionLenguaje(ABC):
    """
    La interfaz que toda dimensión debe implementar.

    Cada dimensión recibe el contexto completo que el ejecutor
    construyó: historial, vocab_match, ids_activos, conceptos_red.
    Debe usarlo como base — no rehacerlo.

    Regla: analizar() nunca lanza excepciones.
    Si algo falla retorna ResultadoDimension con activa=False.
    """

    NOMBRE: str   = ''
    PESO:   float = 1.0

    @abstractmethod
    def analizar(self, texto: str, contexto: dict) -> ResultadoDimension:
        """
        Lee el mensaje desde el ángulo de esta dimensión.

        contexto contiene (entre otros):
            nombre_usuario:  str
            historial:       list  — buffer de sesión
            vocab_match:     list  — GestorVocabulario.buscar_frase()
            ids_activos:     list  — IDs de nodos de la red neuronal
            ids_conocidos:   list  — igual que ids_activos (alias del motor)
            vocab_tipos:     dict  — {id_nodo: tipo_concepto}
            conceptos_red:   list  — nodos con grounding
        """
        pass

    def _resultado_vacio(self) -> ResultadoDimension:
        return ResultadoDimension(
            dimension     = self.NOMBRE,
            activa        = False,
            confianza     = 0.0,
            hallazgos     = {},
            senales       = [],
            peso_en_motor = self.PESO,
        )

    def _resultado(
        self,
        activa:    bool,
        confianza: float,
        hallazgos: dict,
        senales:   list = None,
    ) -> ResultadoDimension:
        return ResultadoDimension(
            dimension     = self.NOMBRE,
            activa        = activa,
            confianza     = min(1.0, max(0.0, confianza)),
            hallazgos     = hallazgos,
            senales       = senales or [],
            peso_en_motor = self.PESO,
        )