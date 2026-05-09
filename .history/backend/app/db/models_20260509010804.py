from datetime import datetime
from typing import Optional
import sqlalchemy as sa
from app import db


class User(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(64), index=True, unique=True, nullable=False)
    email = sa.Column(sa.String(120), index=True, unique=True, nullable=False)
    password_hash = sa.Column(sa.String(256))
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = sa.Column(sa.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_active = sa.Column(sa.Boolean, default=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
