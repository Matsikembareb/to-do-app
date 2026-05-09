from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api

db = SQLAlchemy()
migrate = Migrate()
api = Api(title='Backend API', version='1.0', doc='/docs')

def create_app(config_class) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)


    from app.modules.health import bp as health_bp
    app.register_blueprint(health_bp)

    from app.modules.users import user_ns
    api.add_namespace(user_ns, path='/users')


    #initialize_swagger(app)

    return app
    """if config == 'development':
        app.run(debug=True)
    else:
        from werkzeug.serving import run_simple
        run_simple('0.0.0.0', 5000, app)"""