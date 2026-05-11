from flask import Flask
from flask_migrate import Migrate
from flask_smorest import Api
from app.db import db
from app.utils.logging_config import setup_error_logging

migrate = Migrate()
api = Api()

def create_app(config_class) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Setup logging (email errors if configured)
    setup_error_logging(app)

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)

    # Import blueprints AFTER db is initialized to avoid circular imports
    from app.modules.auth import bp as auth_bp
    api.register_blueprint(auth_bp)

    from app.modules.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.modules.health import bp as health_bp
    app.register_blueprint(health_bp)

    from app.modules.users import bp as users_bp
    api.register_blueprint(users_bp)

    return app
    """
    swagger app to be initialized
    if config == 'development':
        app.run(debug=True)
    else:
        from werkzeug.serving import run_simple
        run_simple('0.0.0.0', 5000, app)"""