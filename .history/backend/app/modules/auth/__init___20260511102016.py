"""Authentication module with JWT and register/login."""
from flask_smorest import Blueprint

bp = Blueprint('auth', 'auth', url_prefix='/api/auth', description='Authentication operations')

# Defer routes import to avoid circular imports at module load time
from app.modules.auth import routes  # noqa: F401

__all__ = ['bp']
