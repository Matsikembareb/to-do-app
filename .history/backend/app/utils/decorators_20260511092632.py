"""Decorators for authentication"""
from functools import wraps
from flask import request, abort
from app.utils.jwt_utils import verify_token


def token_required(f):
    """Decorator to check for valid JWT token in Authorization header"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Check for token in Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return {'error': 'Invalid Authorization header format'}, 401

        if not token:
            return {'error': 'Authorization token is missing'}, 401

        payload = verify_token(token)
        if 'error' in payload:
            return payload, 401

        kwargs['current_user_id'] = payload['user_id']
        return f(*args, **kwargs)

    return decorated
