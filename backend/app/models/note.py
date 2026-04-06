import uuid
from datetime import datetime, timezone
from ..extensions import db


class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    application_id = db.Column(
        db.String(36),
        db.ForeignKey('applications.id', ondelete='CASCADE'),
        nullable=False,
    )
    user_id = db.Column(
        db.String(36),
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        db.Index('ix_notes_application_id', 'application_id'),
    )

    def __repr__(self) -> str:
        return f'<Note {self.id[:8]}>'
