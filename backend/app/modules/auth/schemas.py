"""Schemas for authentication operations."""
from marshmallow import Schema, fields


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
