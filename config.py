import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Base application configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'raitasaathi-ai-dev-secret-key-2026')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    
    # AI and Integration Flags
    DEMO_MODE = os.environ.get('DEMO_MODE', 'true').lower() in ('true', '1', 'yes')
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
    DEFAULT_LANGUAGE = 'kn'  # Kannada primary default
    
    # Security
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = False  # Set True in production with HTTPS


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEV_DATABASE_URL', 
        f"sqlite:///{os.path.join(BASE_DIR, 'raitasaathi_dev.db')}" if os.path.exists(os.path.join(BASE_DIR, 'raitasaathi_dev.db')) else f"sqlite:///{os.path.join(BASE_DIR, 'krishi_mitra_dev.db')}"
    )


class TestingConfig(Config):
    TESTING = True
    DEMO_MODE = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    DEBUG = False
    DEMO_MODE = os.environ.get('DEMO_MODE', 'false').lower() in ('true', '1', 'yes')
    SESSION_COOKIE_SECURE = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 
        f"sqlite:///{os.path.join(BASE_DIR, 'raitasaathi_prod.db')}"
    )


config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

