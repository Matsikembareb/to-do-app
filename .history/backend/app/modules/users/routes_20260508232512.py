from datetime import datetime

from flask import request
from flask_restx import Namespace, Resource, fields
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from app import db
from app.db.models import User
from app.modules.users.schemas import UserCreateSchema, UserUpdateSchema

user_ns = Namespace('users', description='User operations')

user_model = user_ns.model(
    'User',
    {
        'id': fields.Integer(readonly=True),
        'username': fields.String(required=True),
        'email': fields.String(required=True),
        'created_at': fields.String,
        'updated_at': fields.String,
        'is_active': fields.Boolean,
    },
)

user_create_model = user_ns.model(
    'UserCreate',
    {
        'username': fields.String(required=True, min_length=3, max_length=64),
        'email': fields.String(required=True),
        'password': fields.String(required=True, min_length=8, max_length=128),
    },
)

user_update_model = user_ns.model(
    'UserUpdate',
    {
        'username': fields.String(required=False, min_length=3, max_length=64),
        'email': fields.String(required=False),
        'password': fields.String(required=False, min_length=8, max_length=128),
        'is_active': fields.Boolean(required=False),
    },
)


def _get_user_or_404(user_id: int) -> User:
    user = db.session.get(User, user_id)
    if user is None:
        user_ns.abort(404, f'User {user_id} not found')
    return user


@user_ns.route('')
class UserList(Resource):
    @user_ns.marshal_list_with(user_model)
    def get(self):
        return User.query.order_by(User.id.asc()).all()

    @user_ns.expect(user_create_model, validate=False)
    @user_ns.marshal_with(user_model, code=201)
    def post(self):
        try:
            payload = UserCreateSchema.model_validate(request.get_json(force=True))
        except ValidationError as exc:
            user_ns.abort(400, exc.errors())

        user = User(
            username=payload.username,
            email=payload.email,
            password_hash=payload.password,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            user_ns.abort(409, 'username or email already exists')

        return user, 201


@user_ns.route('/<int:user_id>')
class UserDetail(Resource):
    @user_ns.marshal_with(user_model)
    def get(self, user_id: int):
        return _get_user_or_404(user_id)

    @user_ns.expect(user_update_model, validate=False)
    @user_ns.marshal_with(user_model)
    def patch(self, user_id: int):
        user = _get_user_or_404(user_id)

        try:
            payload = UserUpdateSchema.model_validate(request.get_json(force=True))
        except ValidationError as exc:
            user_ns.abort(400, exc.errors())

        updates = payload.model_dump(exclude_unset=True)
        for field_name, field_value in updates.items():
            if field_name == 'password':
                user.password_hash = field_value
            else:
                setattr(user, field_name, field_value)

        user.updated_at = datetime.utcnow()

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            user_ns.abort(409, 'username or email already exists')

        return user

    def delete(self, user_id: int):
        user = _get_user_or_404(user_id)

        db.session.delete(user)
        db.session.commit()

        return {'message': f'User {user_id} deleted successfully'}, 200