import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from config import config_by_name
from app.extensions import db

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(
        __name__, 
        static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend'),
        static_url_path=''
    )
    app.config.from_object(config_by_name.get(config_name, config_by_name['default']))

    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    CORS(app, supports_credentials=True)

    # Register API Blueprints
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.assistant import assistant_bp
    from app.routes.schemes import schemes_bp
    from app.routes.calculator import calculator_bp
    from app.routes.crop import crop_bp
    from app.routes.soil import soil_bp
    from app.routes.calendar import calendar_bp
    from app.routes.profile import profile_bp
    from app.routes.identity import identity_bp
    from app.routes.applications import applications_bp
    from app.routes.notifications import notifications_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(assistant_bp)
    app.register_blueprint(schemes_bp)
    app.register_blueprint(calculator_bp)
    app.register_blueprint(crop_bp)
    app.register_blueprint(soil_bp)
    app.register_blueprint(calendar_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(identity_bp)
    app.register_blueprint(applications_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(admin_bp)

    # Serve Frontend SPA
    @app.route('/')
    def serve_index():
        return send_from_directory(app.static_folder, 'index.html')

    @app.route('/login')
    def serve_login():
        return send_from_directory(app.static_folder, 'login.html')

    @app.route('/app')
    def serve_app():
        return send_from_directory(app.static_folder, 'app.html')

    @app.route('/admin')
    def serve_admin():
        return send_from_directory(app.static_folder, 'admin.html')

    @app.route('/fallow-row')
    def serve_fallow_row():
        return send_from_directory(os.path.dirname(app.static_folder), 'fallow-row.html')


    return app

