import uuid
from datetime import datetime, timezone
from ..extensions import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    applications = db.relationship(
        'Application', backref='user', lazy=True, cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return f'<User {self.email}>'
