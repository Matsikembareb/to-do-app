from flask_smorest import Blueprint

bp = Blueprint('users', 'users', url_prefix='/api/users', description='User operations')

# Defer routes import to avoid circular imports at module load time
from app.modules.users import routes  # noqa: F401

__all__ = ['bp']
