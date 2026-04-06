import os
from flask import Flask
from flask_cors import CORS
from .config import config_by_name
from .extensions import db, migrate, jwt, ma
from .utils.errors import register_error_handlers


def create_app(config_name: str = 'development') -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    ma.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Import models so Alembic discovers them
    from .models import user, application, note  # noqa: F401

    # Blueprints
    from .routes.auth import auth_bp
    from .routes.applications import applications_bp
    from .routes.notes import notes_bp
    from .routes.dashboard import dashboard_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(applications_bp, url_prefix='/api/applications')
    app.register_blueprint(notes_bp, url_prefix='/api/applications')
    app.register_blueprint(dashboard_bp, url_prefix='/api')

    register_error_handlers(app)

    return app
