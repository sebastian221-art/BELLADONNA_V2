# main.py
# Punto de entrada de Bell
# Ejecutar desde C:\Users\Sebas\BELLADONNA\
# python main.py

import sys
from pathlib import Path

# La raíz del proyecto es donde está este archivo
RAIZ_BELL = Path(__file__).parent.resolve()

# Agregar al path para que los imports funcionen
sys.path.insert(0, str(RAIZ_BELL))

# Pasar la raíz al registro antes de importar
import os
os.environ['BELL_RAIZ'] = str(RAIZ_BELL)

from interfaz import iniciar

if __name__ == '__main__':
    print(f'Raíz de Bell: {RAIZ_BELL}')
    iniciar(
        host='127.0.0.1',
        port=5000,
        debug=False
    )