"""JWT utilities for token generation and verification."""
import jwt
from datetime import datetime, timedelta
from flask import current_app


def generate_token(user_id: int, username: str) -> str:
    """Generate JWT token for user."""
    payload = {
        'user_id': user_id,
        'username': username,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(hours=current_app.config.get('JWT_EXPIRY_HOURS', 24))
    }
    token = jwt.encode(
        payload,
        current_app.config.get('JWT_SECRET_KEY'),
        algorithm=current_app.config.get('JWT_ALGORITHM')
    )
    return token


def verify_token(token: str) -> dict:
    """Verify and decode JWT token."""
    try:
        payload = jwt.decode(
            token,
            current_app.config.get('JWT_SECRET_KEY'),
            algorithms=[current_app.config.get('JWT_ALGORITHM')]
        )
        return payload
    except jwt.ExpiredSignatureError:
        return {'error': 'Token expired'}
    except jwt.InvalidTokenError:
        return {'error': 'Invalid token'}
