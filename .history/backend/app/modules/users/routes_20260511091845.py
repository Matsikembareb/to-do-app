from flask.views import MethodView
from flask import abort
from marshmallow import Schema, fields, validate
from sqlalchemy import select
from app import db
from app.db.models import User
from app.modules.users import bp


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
