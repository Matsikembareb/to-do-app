from flask.views import MethodView
from flask import abort, request
from marshmallow import Schema, fields, validate
from sqlalchemy import select
from app import db
from app.db.models import User
from app.modules.users import bp
from app.utils.jwt_utils import generate_token, verify_token
from app.utils.decorators import token_required


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3, max=64))
    email = fields.Email(required=True)
    is_active = fields.Bool()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class UserCreateSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3, max=64))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))


class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class TokenSchema(Schema):
    access_token = fields.Str()
    token_type = fields.Str()
    user = fields.Nested(UserSchema)


@bp.route('/register')
class Register(MethodView):
    @bp.arguments(UserCreateSchema)
    @bp.response(201, TokenSchema)
    def post(self, new_data):
        """Register a new user"""
        # Check if user already exists
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
    @bp.arguments(LoginSchema)
    @bp.response(200, TokenSchema)
    def post(self, credentials):
        """Login user and return JWT token"""
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


@bp.route('/protected')
class ProtectedRoute(MethodView):
    @bp.response(200, UserSchema)
    def get(self):
        """Protected route example - requires valid JWT token"""
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                abort(401)
        
        if not token:
            abort(401)
        
        payload = verify_token(token)
        if 'error' in payload:
            abort(401)
        
        user = db.session.get(User, payload['user_id'])
        if not user:
            abort(404)
        
        return user


@bp.route('/')
class UserList(MethodView):
    @bp.response(200, UserSchema(many=True))
    def get(self):
        """Get all users"""
        stmt = select(User)
        users = db.session.scalars(stmt).all()
        return users

    @bp.arguments(UserCreateSchema)
    @bp.response(201, UserSchema)
    def post(self, new_data):
        """Create a new user"""
        user = User(
            username=new_data['username'],
            email=new_data['email'],
        )
        user.set_password(new_data['password'])
        db.session.add(user)
        db.session.commit()
        return user


@bp.route('/<int:user_id>')
class UserDetail(MethodView):
    @bp.response(200, UserSchema)
    def get(self, user_id):
        """Get a user by ID"""
        user = db.session.get(User, user_id)
        if user is None:
            abort(404)
        return user

    @bp.arguments(UserCreateSchema)
    @bp.response(200, UserSchema)
    def put(self, new_data, user_id):
        """Update a user"""
        user = db.session.get(User, user_id)
        if user is None:
            abort(404)
        user.username = new_data['username']
        user.email = new_data['email']
        user.set_password(new_data['password'])
        db.session.commit()
        return user

    def delete(self, user_id):
        """Delete a user"""
        user = db.session.get(User, user_id)
        if user is None:
            abort(404)
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted'}, 200
