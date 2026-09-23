import sys
import os

# Agrega la raíz del proyecto al path de Python para encontrar 'app' y 'lib'
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

# Si tienes la carpeta 'lib', la agregamos al path al igual que en tu run.py
lib_path = os.path.join(root_path, 'lib')
if os.path.exists(lib_path) and lib_path not in sys.path:
    sys.path.insert(0, lib_path)

# Importamos la función de fábrica desde el módulo app
from app import create_app

# Vercel buscará la variable 'app' para exponer la función Serverless
app = create_app()
