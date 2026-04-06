import uuid
from datetime import datetime, timezone, date
from ..extensions import db


class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(
        db.String(36),
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )
    company_name = db.Column(db.String(150), nullable=False)
    role_title = db.Column(db.String(150), nullable=False)
    job_url = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(150), nullable=True)
    salary_min = db.Column(db.Integer, nullable=True)
    salary_max = db.Column(db.Integer, nullable=True)
    stage = db.Column(db.String(20), nullable=False, default='APPLIED')
    applied_date = db.Column(db.Date, nullable=False, default=date.today)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    notes = db.relationship(
        'Note', backref='application', lazy=True, cascade='all, delete-orphan'
    )

    __table_args__ = (
        db.Index('ix_applications_user_id', 'user_id'),
        db.Index('ix_applications_user_stage', 'user_id', 'stage'),
        db.CheckConstraint(
            "stage IN ('APPLIED','SCREENING','INTERVIEW','OFFER','REJECTED','WITHDRAWN')",
            name='ck_application_stage',
        ),
    )

    def __repr__(self) -> str:
        return f'<Application {self.company_name} — {self.stage}>'
