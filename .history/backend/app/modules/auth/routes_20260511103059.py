"""Auth routes for register and login."""
from flask.views import MethodView
from flask import abort
from sqlalchemy import select
from app import db
from app.db.models import User
from app.modules.auth import bp
from app.modules.auth.jwt_utils import generate_token
from app.modules.auth.schemas import UserCreateSchema, LoginSchema, TokenSchema


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
