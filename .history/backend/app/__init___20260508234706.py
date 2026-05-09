from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api

db = SQLAlchemy()
migrate = Migrate()
api = Api()

def create_app(config_class) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app, version='1.0', title='Flask API', description='A Flask REST API with RESTX')

    from app.modules.health import bp as health_bp
    app.register_blueprint(health_bp)

    from app.modules.users.routes import user_ns as bp
    api.add_namespace(bp, path='/api/users')

    return app
    """
    swagger app to be initialized
    if config == 'development':
        app.run(debug=True)
    else:
        from werkzeug.serving import run_simple
        run_simple('0.0.0.0', 5000, app)"""