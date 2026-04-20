# biblioteca/habilidades/lenguaje/paquete.py
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class EntradaLenguaje:
    texto:          str  = ''
    contexto:       dict = field(default_factory=dict)
    historial:      list = field(default_factory=list)
    nombre_usuario: str  = 'Sebastian'


@dataclass
class SalidaLenguaje:
    exitoso:               bool  = False

    intencion:             str   = ''
    accion_principal:      str   = ''
    tipo_mensaje:          str   = 'conversacional'
    objetos:               list  = field(default_factory=list)
    habilidad_requerida:   str   = ''
    dominio_tecnico:       str   = ''
    parametros_tecnicos:   dict  = field(default_factory=dict)

    emocion_detectada:     str   = 'neutra'
    intensidad:            float = 0.0
    tono_base:             str   = 'neutral'
    necesidad_real:        str   = ''
    tono_respuesta:        str   = 'cercano_natural'
    id_lyra:               str   = ''
    # ids_activos en formato que usan las consejeras
    ids_activos:           list  = field(default_factory=list)

    respuesta_base:        str   = ''
    instruccion_habilidad: dict  = field(default_factory=dict)

    # Comprensión en formato para consejeras (Capa 4+)
    para_consejeras:       dict  = field(default_factory=dict)

    confianza:             float = 0.0
    dimensiones_activas:   list  = field(default_factory=list)
    error:                 Optional[str] = None

    def a_dict(self) -> dict:
        return {
            'exitoso':                self.exitoso,
            'intencion':              self.intencion,
            'accion_principal':       self.accion_principal,
            'tipo_mensaje':           self.tipo_mensaje,
            'objetos':                self.objetos,
            'habilidad_requerida':    self.habilidad_requerida,
            'dominio_tecnico':        self.dominio_tecnico,
            'parametros_tecnicos':    self.parametros_tecnicos,
            'emocion_detectada':      self.emocion_detectada,
            'intensidad':             self.intensidad,
            'tono_base':              self.tono_base,
            'necesidad_real':         self.necesidad_real,
            'tono_respuesta':         self.tono_respuesta,
            'id_lyra':                self.id_lyra,
            'ids_activos':            self.ids_activos,
            'respuesta_base':         self.respuesta_base,
            'instruccion_habilidad':  self.instruccion_habilidad,
            'para_consejeras':        self.para_consejeras,
            'confianza':              self.confianza,
            'dimensiones_activas':    self.dimensiones_activas,
            'error':                  self.error,
        }