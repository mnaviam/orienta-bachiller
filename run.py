import os
import sys

# Incluir dependencias locales de lib si existen
lib_path = os.path.join(os.path.dirname(__file__), 'lib')
if os.path.exists(lib_path) and lib_path not in sys.path:
    sys.path.insert(0, lib_path)

from app import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Iniciando OrientaBachiller en http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
