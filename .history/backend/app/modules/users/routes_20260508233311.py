from flask_restx import Namespace, Resource, fields
from app import db
from app.db.models import User

user_ns = Namespace('', description='User operations')

# Define the user model for serialization/deserialization
user_model = user_ns.model('User', {
    'id': fields.Integer(readOnly=True),
    'username': fields.String(required=True, min_length=3, max_length=64),
    'email': fields.String(required=True),
    'is_active': fields.Boolean(),
    'created_at': fields.DateTime(readOnly=True),
    'updated_at': fields.DateTime(readOnly=True),
})

# Create model (no id, no timestamps)
user_create_model = user_ns.model('UserCreate', {
    'username': fields.String(required=True, min_length=3, max_length=64),
    'email': fields.String(required=True),
    'password_hash': fields.String(required=True, min_length=6),
})


@user_ns.route('/')
class UserList(Resource):
    @user_ns.doc('list_users')
    @user_ns.marshal_list_with(user_model)
    def get(self):
        """Get all users"""
        return User.query.all()

    @user_ns.doc('create_user')
    @user_ns.expect(user_create_model)
    @user_ns.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user"""
        user = User(
            username=user_ns.payload['username'],
            email=user_ns.payload['email'],
            password_hash=user_ns.payload['password_hash'],
        )
        db.session.add(user)
        db.session.commit()
        return user, 201


@user_ns.route('/<int:user_id>')
class UserDetail(Resource):
    @user_ns.doc('get_user')
    @user_ns.marshal_with(user_model)
    def get(self, user_id):
        """Get a user by ID"""
        user = User.query.get_or_404(user_id)
        return user

    @user_ns.doc('update_user')
    @user_ns.expect(user_create_model)
    @user_ns.marshal_with(user_model)
    def put(self, user_id):
        """Update a user"""
        user = User.query.get_or_404(user_id)
        user.username = user_ns.payload['username']
        user.email = user_ns.payload['email']
        user.password_hash = user_ns.payload['password_hash']
        db.session.commit()
        return user

    @user_ns.doc('delete_user')
    def delete(self, user_id):
        """Delete a user"""
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted'}, 200
