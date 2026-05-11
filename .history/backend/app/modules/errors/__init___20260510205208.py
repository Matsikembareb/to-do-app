from flask import Blueprint

bp = Blueprint('errors', 'errors')

# Import error handlers
from app.modules.errors import errors  # noqa: F401

__all__ = ['bp']
