"""Todo CRUD routes."""
from datetime import datetime
from flask import g
from flask.views import MethodView
from flask_smorest import Blueprint
from sqlalchemy import select

from app.db import db
from app.db.models import Todo, User
from app.modules.auth.decorators import token_required
from app.modules.todos import bp
from app.modules.todos.schemas import TodoSchema, TodoCreateSchema, TodoUpdateSchema


@bp.route('')
class TodoList(MethodView):
    """Todo list endpoints."""

    @bp.response(200, TodoSchema(many=True))
    @token_required
    def get(self):
        """Get all todos for the current user."""
        user_id = g.current_user_id
        todos = db.session.scalars(
            select(Todo).where(Todo.user_id == user_id).order_by(Todo.created_at.desc())
        ).all()
        return todos

    @bp.arguments(TodoCreateSchema)
    @bp.response(201, TodoSchema)
    @token_required
    def post(self, args):
        """Create a new todo for the current user."""
        user_id = g.current_user_id

        # Verify user exists
        user = db.session.get(User, user_id)
        if not user:
            return {'error': 'User not found'}, 404

        todo = Todo(
            title=args['title'],
            description=args.get('description'),
            user_id=user_id
        )
        db.session.add(todo)
        db.session.commit()
        return todo


@bp.route('/<int:todo_id>')
class TodoDetail(MethodView):
    """Todo detail endpoints."""

    def _get_todo_or_abort(self, todo_id: int):
        """Helper to get a todo and verify ownership."""
        user_id = g.current_user_id
        todo = db.session.get(Todo, todo_id)

        if not todo:
            return None, ({'error': 'Todo not found'}, 404)

        if todo.user_id != user_id:
            return None, ({'error': 'Unauthorized'}, 403)

        return todo, None

    @bp.response(200, TodoSchema)
    @token_required
    def get(self, todo_id: int):
        """Get a specific todo."""
        todo, error = self._get_todo_or_abort(todo_id)
        if error:
            return error
        return todo

    @bp.arguments(TodoUpdateSchema)
    @bp.response(200, TodoSchema)
    @token_required
    def put(self, args, todo_id: int):
        """Update a specific todo."""
        todo, error = self._get_todo_or_abort(todo_id)
        if error:
            return error

        if 'title' in args:
            todo.title = args['title']
        if 'description' in args:
            todo.description = args['description']
        if 'completed' in args:
            todo.completed = args['completed']

        db.session.commit()
        return todo

    @bp.response(200)
    @token_required
    def delete(self, todo_id: int):
        """Delete a specific todo."""
        todo, error = self._get_todo_or_abort(todo_id)
        if error:
            return error

        db.session.delete(todo)
        db.session.commit()
        return {'message': 'Todo deleted'}

