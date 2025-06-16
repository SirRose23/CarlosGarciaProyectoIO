import os
from datetime import timedelta


class Config:
    
    # Configuración básica de Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'transporteIO-secret-key-2025-mesoamericana'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() in ['true', '1', 'yes']
    
    # Configuración de archivos
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB máximo
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    
    # Configuración de JSON
    JSONIFY_PRETTYPRINT_REGULAR = True
    JSON_SORT_KEYS = False
    
    # Configuración de la aplicación específica
    APP_NAME = 'TransporteIO'
    APP_VERSION = '1.0.0'
    UNIVERSIDAD = 'Universidad Mesoamericana'
    CURSO = 'Investigación de Operaciones'
    ANNO = '2025'
    
    # Límites de la aplicación
    MAX_ORIGENES = 10
    MAX_DESTINOS = 10
    MIN_ORIGENES = 2
    MIN_DESTINOS = 2
    
    # Métodos disponibles
    METODOS_DISPONIBLES = [
        'costo_minimo',
        'esquina_noroeste',
        'vogel',
        'russell'
    ]


class DevelopmentConfig(Config):
    """Configuración para desarrollo."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Configuración para producción."""
    DEBUG = False
    TESTING = False


# Configuraciones disponibles
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
