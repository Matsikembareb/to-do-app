from flask_smorest import Blueprint

bp = Blueprint('users', 'users', url_prefix='/api/users', description='User operations')

from app.modules.users import routes  # noqa: F401

__all__ = ['bp']
