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

    # Error handlers
    @app.errorhandler(400)
    def bad_request(error):
        """Handle bad request errors."""
        return jsonify({'error': 'Bad Request', 'message': str(error)}), 400

    @app.errorhandler(404)
    def not_found(error):
        """Handle not found errors."""
        return jsonify({'error': 'Not Found', 'message': 'The requested resource was not found.'}), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle method not allowed errors."""
        return jsonify({'error': 'Method Not Allowed', 'message': str(error)}), 405

    @app.errorhandler(422)
    def unprocessable_entity(error):
        """Handle validation errors from flask-smorest."""
        return jsonify({'error': 'Unprocessable Entity', 'message': str(error)}), 422

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        """Handle database integrity errors (unique constraints, etc.)."""
        db.session.rollback()
        return jsonify({
            'error': 'Conflict',
            'message': 'A database constraint was violated. This resource may already exist.'
        }), 409

    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(error):
        """Handle general SQLAlchemy errors."""
        db.session.rollback()
        return jsonify({
            'error': 'Database Error',
            'message': 'An unexpected database error occurred.'
        }), 500

    @app.errorhandler(500)
    def internal_error(error):
        """Handle internal server errors."""
        db.session.rollback()
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred. Please try again later.'
        }), 500

    return app
    """
    swagger app to be initialized
    if config == 'development':
        app.run(debug=True)
    else:
        from werkzeug.serving import run_simple
        run_simple('0.0.0.0', 5000, app)"""