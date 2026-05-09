from flask import Blueprint

bp = Blueprint('users', __name__)

from app.modules.users import routes
