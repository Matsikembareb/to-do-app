from pydantic import BaseModel, ConfigDict, Field, field_validator


class UserCreateSchema(BaseModel):
    username: str = Field(min_length=3, max_length=64)
    email: str = Field(min_length=5, max_length=120)
    password: str = Field(min_length=8, max_length=128)

    @field_validator('email')
    @classmethod
    def validate_email(cls, value: str) -> str:
        if '@' not in value or value.startswith('@') or value.endswith('@'):
            raise ValueError('email must be a valid email address')
        return value.lower().strip()


class UserUpdateSchema(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=64)
    email: str | None = Field(default=None, min_length=5, max_length=120)
    password: str | None = Field(default=None, min_length=8, max_length=128)
    is_active: bool | None = None

    @field_validator('email')
    @classmethod
    def validate_email(cls, value: str | None) -> str | None:
        if value is None:
            return value
        if '@' not in value or value.startswith('@') or value.endswith('@'):
            raise ValueError('email must be a valid email address')
        return value.lower().strip()


class UserReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    created_at: str | None = None
    updated_at: str | None = None
    is_active: bool