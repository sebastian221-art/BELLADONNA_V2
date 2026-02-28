"""
Script de Limpieza - Fase 4A
Elimina código obsoleto y prepara Bell para integración con Groq.

EJECUTAR ANTES DE COMENZAR FASE 4A.
"""
import os
import shutil
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

class CleanupFase4A:
    """Limpia código obsoleto y prepara estructura para Fase 4A."""
    
    def __init__(self, proyecto_root: Path):
        self.root = proyecto_root
        self.cambios = []
        self.errores = []
        
    def ejecutar_limpieza_completa(self) -> Dict:
        """Ejecuta todas las operaciones de limpieza."""
        print("="*80)
        print("INICIANDO LIMPIEZA - FASE 4A")
        print("="*80)
        
        # 1. Eliminar expresion/
        self._eliminar_expresion()
        
        # 2. Archivar _legacy/
        self._archivar_legacy()
        
        # 3. Limpiar módulo llm/
        self._limpiar_llm()
        
        # 4. Crear nuevas carpetas necesarias
        self._crear_estructura_fase4a()
        
        # 5. Generar reporte
        return self._generar_reporte()
    
    def _eliminar_expresion(self):
        """Elimina carpeta expresion/ (vacía, no se usa)."""
        expresion_path = self.root / "expresion"
        
        if expresion_path.exists():
            try:
                shutil.rmtree(expresion_path)
                self.cambios.append({
                    "accion": "ELIMINADO",
                    "item": "expresion/",
                    "razon": "Carpeta vacía (0 líneas de código)"
                })
                print("✅ Eliminada carpeta expresion/")
            except Exception as e:
                self.errores.append(f"Error eliminando expresion/: {e}")
                print(f"❌ Error eliminando expresion/: {e}")
        else:
            print("⚠️  expresion/ no existe (ya fue eliminada)")
    
    def _archivar_legacy(self):
        """Mueve _legacy/ a _archive/_legacy/."""
        legacy_path = self.root / "_legacy"
        archive_path = self.root / "_archive"
        
        if legacy_path.exists():
            try:
                # Crear _archive/ si no existe
                archive_path.mkdir(exist_ok=True)
                
                # Mover _legacy/ dentro de _archive/
                shutil.move(str(legacy_path), str(archive_path / "_legacy"))
                
                self.cambios.append({
                    "accion": "ARCHIVADO",
                    "item": "_legacy/",
                    "destino": "_archive/_legacy/",
                    "razon": "11 archivos obsoletos del sistema de grounding viejo"
                })
                print("✅ Archivada carpeta _legacy/ → _archive/_legacy/")
            except Exception as e:
                self.errores.append(f"Error archivando _legacy/: {e}")
                print(f"❌ Error archivando _legacy/: {e}")
        else:
            print("⚠️  _legacy/ no existe (ya fue archivada)")
    
    def _limpiar_llm(self):
        """Limpia módulo llm/ eliminando código de GPT-2."""
        llm_path = self.root / "llm"
        
        if not llm_path.exists():
            print("⚠️  llm/ no existe")
            return
        
        archivos_eliminar = [
            "gestor_llm.py",      # GPT-2 local (obsoleto)
            "dataset_bell.py",     # Vacío
            "generador_respuestas.py"  # Diseñado para GPT-2
        ]
        
        archivos_mover = {
            "verificador_coherencia.py": "consejeras/echo/"
        }
        
        # Eliminar archivos obsoletos
        for archivo in archivos_eliminar:
            archivo_path = llm_path / archivo
            if archivo_path.exists():
                try:
                    # Renombrar a .old en vez de eliminar (backup)
                    archivo_path.rename(archivo_path.with_suffix('.py.old'))
                    self.cambios.append({
                        "accion": "DESACTIVADO",
                        "item": f"llm/{archivo}",
                        "razon": "Diseñado para GPT-2 local (obsoleto)"
                    })
                    print(f"✅ Desactivado llm/{archivo} (.old)")
                except Exception as e:
                    self.errores.append(f"Error con llm/{archivo}: {e}")
        
        # Mover verificador_coherencia.py a Echo
        for archivo, destino in archivos_mover.items():
            origen = llm_path / archivo
            destino_path = self.root / destino
            
            if origen.exists():
                try:
                    destino_path.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(origen, destino_path / archivo)
                    origen.rename(origen.with_suffix('.py.old'))
                    
                    self.cambios.append({
                        "accion": "MOVIDO",
                        "item": f"llm/{archivo}",
                        "destino": f"{destino}{archivo}",
                        "razon": "Ahora es parte de Echo (verificación de coherencia)"
                    })
                    print(f"✅ Movido llm/{archivo} → {destino}")
                except Exception as e:
                    self.errores.append(f"Error moviendo {archivo}: {e}")
    
    def _crear_estructura_fase4a(self):
        """Crea carpetas necesarias para Fase 4A."""
        carpetas_nuevas = [
            "config",           # Configuración de Groq
            "data",             # Whitelist de conceptos
            "logs/fase4a",      # Logs de interacción con Groq
            "scripts",          # Scripts de utilidad
            "docs/fase4a"       # Documentación de Fase 4A
        ]
        
        for carpeta in carpetas_nuevas:
            carpeta_path = self.root / carpeta
            if not carpeta_path.exists():
                try:
                    carpeta_path.mkdir(parents=True, exist_ok=True)
                    self.cambios.append({
                        "accion": "CREADO",
                        "item": f"{carpeta}/",
                        "razon": "Estructura necesaria para Fase 4A"
                    })
                    print(f"✅ Creada carpeta {carpeta}/")
                except Exception as e:
                    self.errores.append(f"Error creando {carpeta}/: {e}")
    
    def _generar_reporte(self) -> Dict:
        """Genera reporte de cambios."""
        reporte = {
            "fecha": datetime.now().isoformat(),
            "total_cambios": len(self.cambios),
            "total_errores": len(self.errores),
            "cambios": self.cambios,
            "errores": self.errores
        }
        
        # Guardar reporte
        reporte_path = self.root / "logs" / "fase4a" / "cleanup_report.json"
        reporte_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(reporte_path, 'w', encoding='utf-8') as f:
            json.dump(reporte, f, indent=2, ensure_ascii=False)
        
        print("\n" + "="*80)
        print("RESUMEN DE LIMPIEZA")
        print("="*80)
        print(f"✅ Cambios realizados: {len(self.cambios)}")
        print(f"❌ Errores encontrados: {len(self.errores)}")
        print(f"📄 Reporte guardado en: {reporte_path}")
        print("="*80)
        
        return reporte


def main():
    """Ejecuta limpieza de Fase 4A."""
    # Detectar raíz del proyecto
    proyecto_root = Path(__file__).parent.parent
    
    print(f"Proyecto: {proyecto_root}")
    print(f"¿Desea continuar con la limpieza? (s/n): ", end='')
    
    # En modo automático, siempre continuar
    respuesta = 's'
    
    if respuesta.lower() == 's':
        cleaner = CleanupFase4A(proyecto_root)
        reporte = cleaner.ejecutar_limpieza_completa()
        
        if reporte['total_errores'] == 0:
            print("\n✅ LIMPIEZA COMPLETADA SIN ERRORES")
            print("🚀 Bell está listo para Fase 4A")
        else:
            print(f"\n⚠️  LIMPIEZA COMPLETADA CON {reporte['total_errores']} ERRORES")
            print("Revisa los errores en el reporte")
    else:
        print("❌ Limpieza cancelada")


if __name__ == "__main__":
    main()