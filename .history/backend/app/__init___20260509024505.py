from flask import Flask
from flask import Flask, render_template, jsonify
from flask_migrate import Migrate
from flask_smorest import Api
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.db import db

migrate = Migrate()
api = Api()

def create_app(config_class) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['API_TITLE'] = 'Muzukuru API'
    app.config['API_VERSION'] = 'v1'
    app.config['OPENAPI_VERSION'] = '3.0.2'

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)

    # Import blueprints AFTER db is initialized to avoid circular imports
    from app.modules.health import bp as health_bp
    app.register_blueprint(health_bp)

    from app.modules.users import bp as users_bp
    api.register_blueprint(users_bp)

    from flask import jsonify

    @app.route('/docs')
    def swagger_ui():
        """Serve Swagger UI that loads the generated OpenAPI spec."""
        return render_template('swagger_ui.html')

    @app.route('/openapi.json')
    def openapi_json():
        """Return the generated OpenAPI JSON for the API."""
        # `api.spec` is an APISpec instance; convert to dict then jsonify
        try:
            spec_dict = api.spec.to_dict()
        except Exception:
            # Fallback: return empty spec
            spec_dict = {}
        return jsonify(spec_dict)

    return app
    """
    swagger app to be initialized
    if config == 'development':
        app.run(debug=True)
    else:
        from werkzeug.serving import run_simple
        run_simple('0.0.0.0', 5000, app)"""