"""Auth routes for register and login."""
from flask.views import MethodView
from flask import abort
from marshmallow import Schema, fields
from sqlalchemy import select
from app import db
from app.db.models import User
from app.modules.auth import bp
from app.modules.auth.jwt_utils import generate_token


class UserSchema(Schema):
    """User response schema."""
    id = fields.Int(dump_only=True)
    username = fields.Str()
    email = fields.Email()
    is_active = fields.Bool()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class UserCreateSchema(Schema):
    """User creation schema."""
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class LoginSchema(Schema):
    """Login credentials schema."""
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class TokenSchema(Schema):
    """Token response schema."""
    access_token = fields.Str()
    token_type = fields.Str()
    user = fields.Nested(UserSchema)


@bp.route('/register')
class Register(MethodView):
    """Register a new user."""
    @bp.arguments(UserCreateSchema)
    @bp.response(201, TokenSchema)
    def post(self, new_data):
        """Register a new user and return JWT token."""
        existing_user = db.session.scalars(
            select(User).where(User.username == new_data['username'])
        ).first()
        if existing_user:
            abort(400)  # Username already exists

        user = User(
            username=new_data['username'],
            email=new_data['email'],
        )
        user.set_password(new_data['password'])
        db.session.add(user)
        db.session.commit()

        token = generate_token(user.id, user.username)
        return {
            'access_token': token,
            'token_type': 'Bearer',
            'user': user
        }


@bp.route('/login')
class Login(MethodView):
    """Login user."""
    @bp.arguments(LoginSchema)
    @bp.response(200, TokenSchema)
    def post(self, credentials):
        """Login user and return JWT token."""
        user = db.session.scalars(
            select(User).where(User.username == credentials['username'])
        ).first()

        if not user or not user.check_password(credentials['password']):
            abort(401)  # Invalid credentials

        token = generate_token(user.id, user.username)
        return {
            'access_token': token,
            'token_type': 'Bearer',
            'user': user
        }
