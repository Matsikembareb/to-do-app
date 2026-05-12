from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_smorest import Api
from app.db import db
from app.utils.logging_config import setup_error_logging
from app.config.config import get_config_by_name

migrate = Migrate()
api = Api()

def create_app(config_class=get_config_by_name()) -> Flask:
    app = Flask(__name__)

    if isinstance(config_class, str):
        # Convert config names like "testing" into the matching config object i.e. when string passed
        config_class = get_config_by_name(config_class)

    app.config.from_object(config_class)


    # Setup logging (email errors if configured)
    setup_error_logging(app)

    # Allow the React frontend to call the API during local development.
    CORS(app, resources={
        r"/api/*": {"origins": app.config['CORS_ORIGINS']},
        r"/health*": {"origins": app.config['CORS_ORIGINS']}
    })

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)

    # Import blueprints AFTER db is initialized to avoid circular imports
    from app.modules.auth import bp as auth_bp
    api.register_blueprint(auth_bp, url_prefix='/api/auth')

    from app.modules.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.modules.health import bp as health_bp
    app.register_blueprint(health_bp, url_prefix='/health')

    from app.modules.users import bp as users_bp
    api.register_blueprint(users_bp, url_prefix='/api/users')

    from app.modules.todos import bp as todos_bp
    api.register_blueprint(todos_bp, url_prefix='/api/todos')

    return app
