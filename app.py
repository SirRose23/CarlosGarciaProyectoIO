from flask import Flask
import os
from routes.main import main_bp


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'transporteIO-dev-key-2025'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
    JSONIFY_PRETTYPRINT_REGULAR = True


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Registrar blueprints
    app.register_blueprint(main_bp)
    
    # Manejo de errores
    @app.errorhandler(404)
    def not_found_error(error):
        return {'error': 'Recurso no encontrado'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Error interno del servidor'}, 500
    
    # Ruta de salud
    @app.route('/health')
    def health_check():
        return {
            'status': 'healthy',
            'app': 'TransporteIO',
            'version': '1.0.0',
            'universidad': 'Universidad Mesoamericana'
        }
    
    return app


# Crear aplicación
app = create_app()


if __name__ == '__main__':
    print("Iniciando TransporteIO - Solver de Problemas de Transporte")
    print(" Universidad Mesoamericana - Investigación de Operaciones 2025")
    print("\n Métodos implementados:")
    print("   • Costo Mínimo")
    print("   • Esquina Noroeste") 
    print("   • Aproximación de Vogel (VAM)")
    print("   • Russell")
    print("\n Servidor: http://localhost:5000")
    print("="*60)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )
