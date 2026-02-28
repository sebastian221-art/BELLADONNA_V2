"""
Almacén de Memoria - Persistencia en JSON.

Maneja el guardado y carga de datos en archivos JSON.

MODIFICADO v3 — Corrección Arquitectónica:
- Agregado 'usuario_persistente' al dict self.archivos
  Requerido por GestorMemoria.guardar_datos_usuario() / cargar_datos_usuario()
  Sin esto: KeyError al intentar persistir datos del usuario entre sesiones
"""
import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

class AlmacenJSON:
    """
    Almacén de memoria persistente usando JSON.
    
    Guarda datos en archivos JSON organizados por tipo.
    """
    
    def __init__(self, directorio_base: str = "memoria_bell"):
        self.directorio_base = Path(directorio_base)
        self._crear_estructura()
        
        self.archivos = {
            'conceptos':    self.directorio_base / 'conceptos.json',
            'decisiones':   self.directorio_base / 'decisiones.json',
            'patrones':     self.directorio_base / 'patrones.json',
            'insights':     self.directorio_base / 'insights.json',
            'ajustes':      self.directorio_base / 'ajustes.json',
            'sesiones':     self.directorio_base / 'sesiones.json',
            'estadisticas': self.directorio_base / 'estadisticas.json',
            # ← NUEVO v3: persistencia de datos de usuario entre sesiones
            # GestorMemoria.CLAVE_USUARIO = "usuario_persistente"
            # guardar_datos_usuario() y cargar_datos_usuario() usan esta clave
            # limpiar(self.CLAVE_USUARIO) también la necesita — sin esto: KeyError
            'usuario_persistente': self.directorio_base / 'usuario_persistente.json',
        }
    
    def _crear_estructura(self):
        """Crea estructura de directorios si no existe."""
        self.directorio_base.mkdir(parents=True, exist_ok=True)
    
    def guardar(self, tipo: str, datos: Any) -> bool:
        try:
            archivo = self.archivos.get(tipo)
            if not archivo:
                return False
            datos_existentes = self._cargar_archivo(archivo)
            if isinstance(datos, list):
                datos_existentes.extend(datos)
            else:
                datos_existentes.append(datos)
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos_existentes, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error guardando {tipo}: {e}")
            return False
    
    def cargar(self, tipo: str) -> List[Any]:
        try:
            archivo = self.archivos.get(tipo)
            if not archivo:
                return []
            return self._cargar_archivo(archivo)
        except Exception as e:
            print(f"Error cargando {tipo}: {e}")
            return []
    
    def _cargar_archivo(self, archivo: Path) -> List[Any]:
        if not archivo.exists():
            return []
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    
    def buscar(self, tipo: str, filtro: Optional[Dict[str, Any]] = None,
               limite: Optional[int] = None) -> List[Any]:
        datos = self.cargar(tipo)
        if filtro:
            datos = [d for d in datos if all(d.get(k) == v for k, v in filtro.items())]
        if limite and limite > 0:
            datos = datos[-limite:]
        return datos
    
    def buscar_por_rango_fecha(self, tipo: str, desde: str,
                               hasta: Optional[str] = None) -> List[Any]:
        datos = self.cargar(tipo)
        if not hasta:
            hasta = datetime.now().isoformat()
        return [d for d in datos if 'timestamp' in d and desde <= d['timestamp'] <= hasta]
    
    def contar(self, tipo: str, filtro: Optional[Dict[str, Any]] = None) -> int:
        return len(self.buscar(tipo, filtro))
    
    def limpiar(self, tipo: str) -> bool:
        try:
            archivo = self.archivos.get(tipo)
            if archivo and archivo.exists():
                archivo.unlink()
            return True
        except Exception as e:
            print(f"Error limpiando {tipo}: {e}")
            return False
    
    def limpiar_todo(self) -> bool:
        try:
            for archivo in self.archivos.values():
                if archivo.exists():
                    archivo.unlink()
            return True
        except Exception as e:
            print(f"Error limpiando todo: {e}")
            return False
    
    def exportar(self, archivo_salida: str) -> bool:
        try:
            datos_completos = {tipo: self.cargar(tipo) for tipo in self.archivos.keys()}
            with open(archivo_salida, 'w', encoding='utf-8') as f:
                json.dump(datos_completos, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error exportando: {e}")
            return False
    
    def importar(self, archivo_entrada: str) -> bool:
        try:
            with open(archivo_entrada, 'r', encoding='utf-8') as f:
                datos_completos = json.load(f)
            for tipo, datos in datos_completos.items():
                if tipo in self.archivos:
                    for dato in datos:
                        self.guardar(tipo, dato)
            return True
        except Exception as e:
            print(f"Error importando: {e}")
            return False
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        return {
            'total_archivos': len([a for a in self.archivos.values() if a.exists()]),
            'tamano_mb': sum(
                a.stat().st_size for a in self.archivos.values() if a.exists()
            ) / (1024 * 1024),
            'conteos': {tipo: self.contar(tipo) for tipo in self.archivos.keys()}
        }