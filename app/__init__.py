import os
import sys

# Asegurar carga de librerías locales
#_current_dir = os.path.dirname(os.path.abspath(__file__))
#_root_dir = os.path.dirname(_current_dir)
#_lib_dir = os.path.join(_root_dir, 'lib')
#if os.path.exists(_lib_dir) and _lib_dir not in sys.path:
#    sys.path.insert(0, _lib_dir)

from flask import Flask
from config import Config
from app.models.database import init_db

def create_app(config_class=Config):
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    
    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, 'templates'),
        static_folder=os.path.join(base_dir, 'static')
    )
    
#    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializar Base de Datos con tablas y datos semilla
    with app.app_context():
        init_db()

    # Registrar Controladores / Blueprints (MVC)
    from app.controllers.main_controller import main_bp
    from app.controllers.test_controller import test_bp
    from app.controllers.result_controller import result_bp
    from app.controllers.admin_controller import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(test_bp)
    app.register_blueprint(result_bp)
    app.register_blueprint(admin_bp)

    # Filtros personalizados de Jinja
    @app.template_filter('percentage_color')
    def percentage_color_filter(value):
        try:
            val = float(value)
            if val >= 85:
                return 'emerald'
            elif val >= 70:
                return 'blue'
            elif val >= 55:
                return 'amber'
            else:
                return 'slate'
        except (ValueError, TypeError):
            return 'blue'

    return app
