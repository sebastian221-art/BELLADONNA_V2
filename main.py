# main.py
# Punto de entrada de Bell
# Ejecutar desde C:\Users\Sebas\BELLADONNA\
# python main.py
from dotenv import load_dotenv
load_dotenv()
import sys
import os
from pathlib import Path

# ── RUTAS ────────────────────────────────────────────────────────────
RAIZ_BELL = Path(__file__).parent.resolve()
sys.path.insert(0, str(RAIZ_BELL))
os.environ['BELLADONNA_ROOT'] = str(RAIZ_BELL)
os.environ['BELL_RAIZ']       = str(RAIZ_BELL)

print(f'Raíz de Bell: {RAIZ_BELL}')

# ── PRE-SCAN (solo para registro rápido de archivos) ─────────────────
try:
    from interfaz.sistema_nodos.registro_nodos import RegistroNodos
    registro = RegistroNodos()
    registro.escanear_proyecto()
    stats = registro.obtener_estadisticas()
    print(
        f'Escaneo completo: '
        f'{stats.get("total_nodos", 0)} nodos, '
        f'{stats.get("total_conexiones", 0)} conexiones'
    )
except Exception as e:
    print(f'Escaneo previo no disponible: {e}')

# ── INICIAR BIBLIOTECA (UNA SOLA VEZ) ────────────────────────────────
from biblioteca import Biblioteca
biblioteca = Biblioteca.obtener()

# ── AUTO-REGISTRO (DESPUÉS de que la biblioteca esté lista) ──────────
# Esto evita la recursión: antes el cargador llamaba Biblioteca.obtener()
# desde adentro de _inicializar(). Ahora el auto-registro ocurre aquí,
# cuando la biblioteca ya está completamente inicializada.
if biblioteca and biblioteca.iniciada:
    try:
        from biblioteca.registrador_automatico import RegistradorAutomatico
        registrador = RegistradorAutomatico(biblioteca)
        total_nuevos = registrador.registrar_todo_el_proyecto(str(RAIZ_BELL))
        if total_nuevos > 0:
            print(f'  Auto-registro: {total_nuevos} nuevas neuronas integradas')
            # Aplicar grounding de vida a los nodos AUTO recién creados
            biblioteca.aplicar_vida_a_nuevos_nodos()
            print(f'  ✓ Grounding de vida aplicado a nodos AUTO')
        else:
            print('  ✓ Auto-registro: todo ya estaba en la red')
    except Exception as e:
        print(f'  ⚠ Auto-registro: {e}')

# ── INICIAR SERVIDOR ─────────────────────────────────────────────────
from interfaz import iniciar

if __name__ == '__main__':
    iniciar(
        host='127.0.0.1',
        port=5000,
        debug=False
    )