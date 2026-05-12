"""Todo schemas for validation and serialization."""
from marshmallow import Schema, fields, validate


class TodoSchema(Schema):
    """Schema for Todo objects."""
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=256))
    description = fields.Str(allow_none=True)
    completed = fields.Bool(dump_only=False, load_default=False)
    user_id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class TodoCreateSchema(Schema):
    """Schema for creating a Todo."""
    title = fields.Str(required=True, validate=validate.Length(min=1, max=256))
    description = fields.Str(allow_none=True)


class TodoUpdateSchema(Schema):
    """Schema for updating a Todo."""
    title = fields.Str(validate=validate.Length(min=1, max=256))
    description = fields.Str(allow_none=True)
    completed = fields.Bool()
