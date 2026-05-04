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
    # FIX: el método correcto es obtener_estado_completo()
    stats = registro.obtener_estado_completo()
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
if biblioteca and biblioteca.iniciada:
    try:
        from biblioteca.registrador_automatico import RegistradorAutomatico
        registrador = RegistradorAutomatico(biblioteca)
        total_nuevos = registrador.registrar_todo_el_proyecto(str(RAIZ_BELL))
        if total_nuevos > 0:
            print(f'  Auto-registro: {total_nuevos} nuevas neuronas integradas')
            biblioteca.aplicar_vida_a_nuevos_nodos()
            print(f'  ✓ Grounding de vida aplicado a nodos AUTO')
        else:
            print('  ✓ Auto-registro: todo ya estaba en la red')
    except Exception as e:
        print(f'  ⚠ Auto-registro: {e}')

# ── INICIAR SERVIDOR ─────────────────────────────────────────────────
from interfaz import iniciar

if __name__ == '__main__':
    # FIX: host='0.0.0.0' para que el Nest Mini (192.168.1.3)
    # pueda acceder a los archivos de audio en Flask (192.168.1.7:5000).
    # Con '127.0.0.1' Flask solo escucha en localhost y el Nest
    # recibe connection refused al intentar cargar el MP3.
    iniciar(
        host='0.0.0.0',
        port=5000,
        debug=False
    )