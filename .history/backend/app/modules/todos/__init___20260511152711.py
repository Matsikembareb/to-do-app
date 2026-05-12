"""Todo management module with CRUD operations."""
from flask_smorest import Blueprint

bp = Blueprint('todos', 'todos', description='Todo operations')

# Defer routes import to avoid circular imports at module load time
from app.modules.todos import routes  # noqa: F401

__all__ = ['bp']
